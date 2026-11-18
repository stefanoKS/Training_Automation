"""共通画像セットの分割を、推論より先に決めておく / decide the shared-set split before any inference.

Day 4 の YOLO 環境と Day 5 の anomalib 環境は別のカーネルなので、Python の変数を共有できません。
「較正用」と「試験用」の区別も共有できません。しかし区別が 2 つあれば比較になりません。
そこでこのモジュールが、anomalib の ``Folder`` と同じ規則で分割を先に確定します。
Day 4 はここで決めた較正用だけを採点し、Day 5 は実際の ``datamodule`` と照合します。

Day 4 (YOLO) and Day 5 (anomalib) run in separate kernels and cannot share Python variables, so the
calibration/test split has to be written to a file. This module reproduces the rule anomalib's
``Folder`` uses, so Day 4 can score the calibration partition only, and Day 5 can prove that the
installed anomalib agrees before it freezes anything.

規則 / the rule (anomalib ``Folder`` with ``val_split_mode="from_test"``)
-----------------------------------------------------------------------
1. Every image under the dataset's ``test`` folders is collected; normal images get ``label_index``
   0 and abnormal images ``label_index`` 1, and the whole frame is sorted by ``image_path``.
2. ``random_split(..., label_aware=True)`` handles each label group separately: a fresh
   ``torch.Generator().manual_seed(seed)`` drives ``torch.randperm(n)`` for that group.
3. ``val_split_ratio=0.5`` gives ``floor(n * 0.5)`` images to the **first** half and the rest to the
   second; an odd count puts the extra image in the first half.
4. ``test_data, val_data = random_split(...)``, so the first half is the **test** partition and the
   second half is the **calibration** (validation) partition.

This module never fits anything and never reads an anomaly score. Day 5 re-checks the result against
the installed anomalib and refuses to continue if the two disagree.
"""

from __future__ import annotations

import math
from pathlib import Path

SCHEMA = 1

VAL_SPLIT_MODE = "from_test"
VAL_SPLIT_RATIO = 0.5

RULES = {
    "applies_to": "images under the dataset's test folders",
    "library_rule": (
        "anomalib Folder(val_split_mode='from_test', val_split_ratio=0.5, seed=<dataset seed>)"
    ),
    "label_aware": True,
    "ordering": "both label groups sorted by image path, as anomalib sorts the sample frame",
    "rng": (
        "torch.randperm(n, generator=torch.Generator().manual_seed(seed)), seeded again for each "
        "label group"
    ),
    "assignment": "the first half of each group is the test partition, the second half is calibration",
}

PARTITIONS = ("patchcore_train", "calibration", "test")


def _images(root: Path, folder: str) -> list[str]:
    """フォルダ内の画像を、パスの文字列順で / one folder's images, in path order."""
    return sorted(path.resolve().relative_to(root.resolve()).as_posix()
                  for path in (root / folder).rglob("*.png"))


def _halves(names: list[str], seed: int) -> tuple[list[str], list[str]]:
    """1 つのラベル群を anomalib と同じ方法で 2 つに分ける / one label group, split like anomalib."""
    import torch

    first = int(math.floor(len(names) * VAL_SPLIT_RATIO))
    order = torch.randperm(len(names), generator=torch.Generator().manual_seed(int(seed))).tolist()
    shuffled = [names[index] for index in order]
    return shuffled[:first], shuffled[first:]


def _overlaps(partitions: dict[str, list[str]]) -> dict[str, list[str]]:
    overlaps = {}
    for name_a, files_a in partitions.items():
        for name_b, files_b in partitions.items():
            if name_a >= name_b:
                continue
            overlaps[f"{name_a} & {name_b}"] = sorted(set(files_a) & set(files_b))
    return overlaps


def build(dataset_root, layout: dict) -> dict:
    """分割の記録を作る / the split record, before any model sees the data."""
    dataset_root = Path(dataset_root)
    seed = int(layout["seed"])

    normal_test = _images(dataset_root, layout["normal_test_dir"])
    abnormal = sorted(name for folder in layout["abnormal_dir"]
                      for name in _images(dataset_root, folder))

    normal_test_first, normal_calibration = _halves(normal_test, seed)
    abnormal_first, abnormal_calibration = _halves(abnormal, seed)

    partitions = {
        "patchcore_train": _images(dataset_root, layout["normal_dir"]),
        "calibration": sorted(normal_calibration + abnormal_calibration),
        "test": sorted(normal_test_first + abnormal_first),
    }
    overlaps = _overlaps(partitions)
    for name, shared in overlaps.items():
        if shared:
            raise ValueError(f"分割が重なっています / partitions overlap: {name}: {shared[:3]}")

    return {
        "schema_version": SCHEMA,
        "dataset_root": str(dataset_root.resolve()),
        "dataset_name": layout["name"],
        "dataset_seed": seed,
        "image_size": layout["image_size"],
        "split": {
            "library": "anomalib Folder (reproduced without importing anomalib)",
            "val_split_mode": VAL_SPLIT_MODE,
            "val_split_ratio": VAL_SPLIT_RATIO,
            "seed": seed,
            "rules": RULES,
        },
        "counts": {name: len(files) for name, files in partitions.items()},
        "partitions": partitions,
        "overlap_check": {name: len(shared) for name, shared in overlaps.items()},
    }


def digest(partitions: dict[str, list[str]]) -> str:
    """分割の指紋 / a digest of the partition lists, shared with ``experiment_identity``."""
    from experiment_identity import digest_json

    return digest_json({name: sorted(files) for name, files in partitions.items()})


def partition_lookup(partitions: dict[str, list[str]]) -> dict[str, str]:
    """`test/good/a.png` と `good/a.png` のどちらでも引ける索引 / name -> partition."""
    from experiment_identity import normalise_image_id

    lookup = {}
    for partition, files in partitions.items():
        for name in files:
            key = normalise_image_id(name)
            if key in lookup and lookup[key] != partition:
                raise ValueError(
                    f"同じ画像が 2 つの分割にあります / one image in two partitions: {key}")
            lookup[key] = partition
    return lookup


def write(path, split: dict) -> Path:
    """途中で失敗しても壊れたファイルを残さない / publish the split atomically."""
    from experiment_identity import write_json_atomic

    return write_json_atomic(Path(path), split)


def matches(split_partitions: dict[str, list[str]],
            other_partitions: dict[str, list[str]]) -> list[str]:
    """どの分割が違うかを名指しする / name the partitions that differ."""
    problems = []
    for name in PARTITIONS:
        here = sorted(split_partitions.get(name, []))
        there = sorted(other_partitions.get(name, []))
        if here != there:
            only_here = sorted(set(here) - set(there))[:3]
            only_there = sorted(set(there) - set(here))[:3]
            problems.append(f"{name}: only in the shared split={only_here} only in anomalib={only_there}")
    return problems
