"""データセットの検証 / Dataset validation.

日本語：YOLO データセットと PatchCore データセットが「学習に使える状態か」を確認します。
特に **ラベルの妥当性** と **データ漏れが無いこと** を重点的に見ます。

English: Checks that the YOLO and PatchCore datasets are usable for training, with emphasis on
**label validity** and **absence of data leakage**.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

COURSE_ROOT = Path(__file__).resolve().parents[2]
ASSETS = COURSE_ROOT / "assets"
DATASET = ASSETS / "yolo_dataset"
ANOMALY = ASSETS / "anomaly_dataset" / "pvc_sheet"
SCRIPTS = ASSETS / "scripts"

sys.path.insert(0, str(SCRIPTS))

SPLITS = ("train", "val", "test")


def _requires_yolo_dataset() -> None:
    if not (DATASET / "data.yaml").is_file():
        pytest.skip("YOLO dataset not generated; run prepare_datasets.py")


def _requires_anomaly_dataset() -> None:
    if not (ANOMALY / "dataset_layout.json").is_file():
        pytest.skip("anomaly dataset not generated; run prepare_datasets.py")


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# YOLO dataset
# ---------------------------------------------------------------------------


def test_yolo_dataset_structure() -> None:
    _requires_yolo_dataset()
    for split in SPLITS:
        assert (DATASET / "images" / split).is_dir(), f"missing images/{split}"
        assert (DATASET / "labels" / split).is_dir(), f"missing labels/{split}"

    summary = json.loads((DATASET / "dataset_summary.json").read_text(encoding="utf-8"))
    assert summary["classes"] == ["black_spot", "scratch", "streak"]
    assert summary["image_size"] > 0


def test_data_yaml_contains_required_keys() -> None:
    _requires_yolo_dataset()
    text = (DATASET / "data.yaml").read_text(encoding="utf-8")
    for key in ("path:", "train:", "val:", "test:", "names:"):
        assert key in text, f"data.yaml is missing {key}"
    for index, class_name in enumerate(("black_spot", "scratch", "streak")):
        assert f"{index}: {class_name}" in text


@pytest.mark.parametrize("split", SPLITS)
def test_every_image_has_a_label(split: str) -> None:
    _requires_yolo_dataset()
    images = {p.stem for p in (DATASET / "images" / split).glob("*.png")}
    labels = {p.stem for p in (DATASET / "labels" / split).glob("*.txt")}
    assert images, f"no images in {split}"
    assert images == labels, f"image/label mismatch in {split}: {images ^ labels}"


@pytest.mark.parametrize("split", SPLITS)
def test_labels_are_valid_yolo_lines(split: str) -> None:
    _requires_yolo_dataset()
    class_names = ["black_spot", "scratch", "streak"]
    checked = 0
    for label_path in sorted((DATASET / "labels" / split).glob("*.txt")):
        content = label_path.read_text(encoding="utf-8").strip()
        if not content:
            continue                        # 背景画像 / background image
        for line_number, line in enumerate(content.splitlines(), start=1):
            parts = line.split()
            assert len(parts) == 5, f"{label_path.name} line {line_number}: expected 5 values"
            class_id = int(parts[0])
            values = [float(v) for v in parts[1:]]
            assert 0 <= class_id < len(class_names), f"{label_path.name}: bad class id {class_id}"
            for value in values:
                assert 0.0 <= value <= 1.0, f"{label_path.name}: value {value} outside 0-1"
            assert values[2] > 0 and values[3] > 0, f"{label_path.name}: zero-size box"
            checked += 1
    assert checked > 0, f"no labelled boxes found in {split}"


@pytest.mark.parametrize("split", SPLITS)
def test_boxes_stay_inside_the_image(split: str) -> None:
    _requires_yolo_dataset()
    summary = json.loads((DATASET / "dataset_summary.json").read_text(encoding="utf-8"))
    size = summary["image_size"]

    for label_path in sorted((DATASET / "labels" / split).glob("*.txt")):
        content = label_path.read_text(encoding="utf-8").strip()
        for line in content.splitlines():
            class_id, xc, yc, w, h = [float(v) for v in line.split()]
            x1, y1 = (xc - w / 2) * size, (yc - h / 2) * size
            x2, y2 = (xc + w / 2) * size, (yc + h / 2) * size
            assert x1 >= -0.5 and y1 >= -0.5, f"{label_path.name}: box starts outside the image"
            assert x2 <= size + 0.5 and y2 <= size + 0.5, f"{label_path.name}: box ends outside"


def test_images_have_the_expected_size_and_mode() -> None:
    _requires_yolo_dataset()
    summary = json.loads((DATASET / "dataset_summary.json").read_text(encoding="utf-8"))
    size = summary["image_size"]
    path = next((DATASET / "images" / "train").glob("*.png"))
    with Image.open(path) as image:
        assert image.size == (size, size)
        assert image.mode in ("RGB", "L")


def test_no_data_leakage_between_splits() -> None:
    """同じ画像が 2 つ以上の分割に入っていないこと。"""
    _requires_yolo_dataset()
    seen: dict[str, str] = {}
    duplicates = []
    for split in SPLITS:
        for path in sorted((DATASET / "images" / split).glob("*.png")):
            digest = _digest(path)
            if digest in seen:
                duplicates.append((seen[digest], str(path)))
            else:
                seen[digest] = str(path)
    assert not duplicates, f"data leakage detected: {duplicates[:3]}"


def test_dataset_is_reproducible() -> None:
    """同じ seed で作り直すと、同じ画像になること（背景画像 1 枚で確認）。"""
    _requires_yolo_dataset()
    import prepare_datasets as pd_mod
    import pvc_synth as ps

    summary = json.loads((DATASET / "dataset_summary.json").read_text(encoding="utf-8"))
    seed = summary["seed"]
    size = summary["image_size"]

    # train_0060 は背景画像なので render_normal と直接比較できる
    # train_0060 is a background image, so it can be compared with render_normal directly
    train_index = 0
    image_index = 60
    expected = ps.render_normal(size, size, pd_mod._seed_for(train_index, image_index + 1, seed))
    actual = np.asarray(Image.open(DATASET / "images" / "train" / "train_0060.png").convert("RGB"))
    assert np.abs(expected.astype(int) - actual.astype(int)).max() <= 1


# ---------------------------------------------------------------------------
# Anomaly dataset
# ---------------------------------------------------------------------------


def test_anomaly_dataset_structure() -> None:
    _requires_anomaly_dataset()
    layout = json.loads((ANOMALY / "dataset_layout.json").read_text(encoding="utf-8"))

    assert (ANOMALY / layout["normal_dir"]).is_dir()
    assert (ANOMALY / layout["normal_test_dir"]).is_dir()
    for directory in layout["abnormal_dir"]:
        assert (ANOMALY / directory).is_dir(), f"missing abnormal dir {directory}"
    for directory in layout["mask_dir"]:
        assert (ANOMALY / directory).is_dir(), f"missing mask dir {directory}"


def test_training_set_contains_only_normal_images() -> None:
    """最重要：学習データに異常画像が混ざっていないこと。"""
    _requires_anomaly_dataset()
    layout = json.loads((ANOMALY / "dataset_layout.json").read_text(encoding="utf-8"))
    normal_dir = ANOMALY / layout["normal_dir"]
    images = list(normal_dir.glob("*.png"))
    assert images, "the normal training set is empty"

    train_root = ANOMALY / "train"
    other_folders = [p.name for p in train_root.iterdir() if p.is_dir() and p.name != "good"]
    assert not other_folders, f"unexpected folders inside train/: {other_folders}"


def test_every_abnormal_image_has_a_mask() -> None:
    _requires_anomaly_dataset()
    layout = json.loads((ANOMALY / "dataset_layout.json").read_text(encoding="utf-8"))

    for abnormal_dir, mask_dir in zip(layout["abnormal_dir"], layout["mask_dir"]):
        abnormal_images = {p.stem for p in (ANOMALY / abnormal_dir).glob("*.png")}
        mask_stems = {p.stem.replace("_mask", "") for p in (ANOMALY / mask_dir).glob("*.png")}
        assert abnormal_images, f"{abnormal_dir} is empty"
        assert abnormal_images == mask_stems, (
            f"mask mismatch in {abnormal_dir}: {abnormal_images ^ mask_stems}"
        )


def test_masks_are_binary_and_not_empty() -> None:
    _requires_anomaly_dataset()
    layout = json.loads((ANOMALY / "dataset_layout.json").read_text(encoding="utf-8"))
    for mask_dir in layout["mask_dir"]:
        for path in sorted((ANOMALY / mask_dir).glob("*.png")):
            mask = np.asarray(Image.open(path).convert("L"))
            assert mask.max() > 0, f"{path.name} is an empty mask"
            unique = np.unique(mask)
            assert set(unique.tolist()) <= {0, 255, *range(0, 256)}, "unexpected mask values"


def test_no_data_leakage_in_anomaly_dataset() -> None:
    _requires_anomaly_dataset()
    layout = json.loads((ANOMALY / "dataset_layout.json").read_text(encoding="utf-8"))
    folders = [layout["normal_dir"], layout["normal_test_dir"], *layout["abnormal_dir"]]

    seen: dict[str, str] = {}
    duplicates = []
    for folder in folders:
        for path in sorted((ANOMALY / folder).glob("*.png")):
            digest = _digest(path)
            if digest in seen:
                duplicates.append((seen[digest], str(path)))
            else:
                seen[digest] = str(path)
    assert not duplicates, f"data leakage detected: {duplicates[:3]}"
