"""データセット準備 / Dataset preparation.

2 つのデータセットを決定的に生成します。
Deterministically builds the two datasets used on Day 4 and Day 5:

1. YOLO 物体検出データセット   -> assets/yolo_dataset/
   YOLO object-detection dataset (images + label .txt + data.yaml)

2. PatchCore 異常検知データセット -> assets/anomaly_dataset/pvc_sheet/
   Anomalib ``Folder`` layout (normal-only training images + held-out test images
   with ground-truth masks)

使い方 / Usage
--------------
    python prepare_datasets.py                    # 生成 / build both datasets
    python prepare_datasets.py --force            # 既存を消して作り直す / rebuild
    python prepare_datasets.py --only yolo        # YOLO のみ / YOLO only
    python prepare_datasets.py --only anomaly

注意 / Notes
------------
* すべて合成画像です。実際の工場画像ではありません。
  Everything here is synthetic. These are NOT real factory images.
* 訓練・検証・試験セットの間で画像は 1 枚も重複しません。
  No image content is shared between train / val / test.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pvc_synth as ps  # noqa: E402

YOLO_IMAGE_SIZE = 320
YOLO_SPLITS = {"train": 64, "val": 16, "test": 16}
YOLO_NEGATIVE_RATIO = 0.18        # 欠陥の無い背景画像の割合 / share of defect-free background images

ANOMALY_IMAGE_SIZE = 256
ANOMALY_COUNTS = {"train_good": 32, "test_good": 12, "per_defect": 10}


# ---------------------------------------------------------------------------
# YOLO データセット / YOLO dataset
# ---------------------------------------------------------------------------


def _seed_for(split_index: int, index: int, base: int) -> int:
    """分割と通し番号から一意な seed を作る / unique deterministic seed per split and index."""
    return base + split_index * 100_000 + index * 17


def build_yolo_dataset(root: Path, seed: int, force: bool = False) -> dict:
    dataset = root / "assets" / "yolo_dataset"
    if dataset.exists() and force:
        shutil.rmtree(dataset)
    for sub in ("images/train", "images/val", "images/test", "labels/train", "labels/val", "labels/test"):
        (dataset / sub).mkdir(parents=True, exist_ok=True)

    summary: dict[str, dict] = {}
    all_images: list[Path] = []

    for split_index, (split, count) in enumerate(YOLO_SPLITS.items()):
        n_defect_images = int(round(count * (1.0 - YOLO_NEGATIVE_RATIO)))
        class_counts = {name: 0 for name in ps.YOLO_CLASSES}
        for idx in range(count):
            stem = f"{split}_{idx:04d}"
            image_path = dataset / "images" / split / f"{stem}.png"
            label_path = dataset / "labels" / split / f"{stem}.txt"
            image_seed = _seed_for(split_index, idx + 1, seed)

            if idx < n_defect_images:
                # 欠陥の種類を順番に割り当てる（偏りを避ける）/ rotate defect classes to balance them
                defect_type = ps.YOLO_CLASSES[idx % len(ps.YOLO_CLASSES)]
                # 3 枚に 1 枚は 2 種類目の欠陥も入れる。2 種類目は交互に入れ替えて偏りを防ぐ。
                # Every third image also gets a second defect type; alternate it so counts stay balanced.
                extra_offset = 1 + (idx // 3) % (len(ps.YOLO_CLASSES) - 1)
                extra = ps.YOLO_CLASSES[(idx + extra_offset) % len(ps.YOLO_CLASSES)]
                types = (defect_type, extra) if idx % 3 == 0 else (defect_type,)
                image, _mask, defects = ps.render_defective(
                    YOLO_IMAGE_SIZE, YOLO_IMAGE_SIZE, image_seed, defect_types=types, count=len(types)
                )
                lines = []
                for defect in defects:
                    class_id = ps.YOLO_CLASSES.index(defect.cls)
                    xc, yc, w, h = defect.to_yolo(YOLO_IMAGE_SIZE, YOLO_IMAGE_SIZE)
                    lines.append(f"{class_id} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}")
                    class_counts[defect.cls] += 1
                label_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            else:
                image = ps.render_normal(YOLO_IMAGE_SIZE, YOLO_IMAGE_SIZE, image_seed)
                label_path.write_text("", encoding="utf-8")   # 背景画像は空ファイル / empty label

            ps.save_rgb(image, image_path)
            all_images.append(image_path)

        summary[split] = {
            "images": count,
            "defect_images": n_defect_images,
            "background_images": count - n_defect_images,
            "instances": class_counts,
        }

    ps.assert_unique_images(all_images, label="YOLO images")

    data_yaml = dataset / "data.yaml"
    data_yaml.write_text(_yolo_yaml(dataset), encoding="utf-8")

    summary_doc = {
        "image_size": YOLO_IMAGE_SIZE,
        "classes": list(ps.YOLO_CLASSES),
        "class_names_ja": [ps.CLASS_NAMES_JA[c] for c in ps.YOLO_CLASSES],
        "splits": summary,
        "seed": seed,
        "duplicate_images_across_splits": 0,
    }
    (dataset / "dataset_summary.json").write_text(
        json.dumps(summary_doc, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return summary_doc


def _yolo_yaml(dataset: Path) -> str:
    """Ultralytics 用の data.yaml を作る / compose the Ultralytics data.yaml."""
    names = "\n".join(f"  {i}: {name}" for i, name in enumerate(ps.YOLO_CLASSES))
    # ``path`` は絶対パスで書き出します。フォルダを移動した場合はこのスクリプトを再実行してください。
    # ``path`` is written as an absolute path. Re-run this script if you move the folder.
    return (
        "# 広島化成 第1週 研修用 合成データセット / synthetic dataset for the Week 1 course\n"
        f"path: {dataset.as_posix()}\n"
        "train: images/train\n"
        "val: images/val\n"
        "test: images/test\n"
        "names:\n"
        f"{names}\n"
    )


def write_yolo_yaml(dataset: Path) -> Path:
    """data.yaml を現在の場所に合わせて書き直す / rewrite data.yaml for the current location."""
    target = dataset / "data.yaml"
    target.write_text(_yolo_yaml(dataset), encoding="utf-8")
    return target


# ---------------------------------------------------------------------------
# Anomalib Folder データセット / Anomalib Folder dataset
# ---------------------------------------------------------------------------


def build_anomaly_dataset(root: Path, seed: int, force: bool = False) -> dict:
    """Anomalib の ``Folder`` データモジュールが読める形で生成する。

    Build the layout expected by ``anomalib.data.Folder``.

    Layout::

        pvc_sheet/
            train/good/                 normal images only   (fit に使う / used to fit)
            test/good/                  held-out normal       (試験 / held-out)
            test/<defect_type>/         held-out defects
            ground_truth/<defect_type>/ matching binary masks
    """
    dataset = root / "assets" / "anomaly_dataset" / "pvc_sheet"
    if dataset.exists() and force:
        shutil.rmtree(dataset)

    (dataset / "train" / "good").mkdir(parents=True, exist_ok=True)
    (dataset / "test" / "good").mkdir(parents=True, exist_ok=True)

    all_images: list[Path] = []

    # --- 正常画像（学習） / normal training images ---
    for idx in range(ANOMALY_COUNTS["train_good"]):
        image = ps.render_normal(ANOMALY_IMAGE_SIZE, ANOMALY_IMAGE_SIZE, _seed_for(1, idx + 1, seed))
        path = dataset / "train" / "good" / f"good_train_{idx:04d}.png"
        ps.save_rgb(image, path)
        all_images.append(path)

    # --- 正常画像（試験） / held-out normal images ---
    for idx in range(ANOMALY_COUNTS["test_good"]):
        image = ps.render_normal(ANOMALY_IMAGE_SIZE, ANOMALY_IMAGE_SIZE, _seed_for(2, idx + 1, seed))
        path = dataset / "test" / "good" / f"good_test_{idx:04d}.png"
        ps.save_rgb(image, path)
        all_images.append(path)

    # --- 欠陥画像（試験）+ 正解マスク / held-out defect images with ground truth ---
    defect_dirs = []
    mask_dirs = []
    counts: dict[str, int] = {}
    for type_index, defect_type in enumerate(ps.ANOMALY_DEFECTS):
        image_dir = dataset / "test" / defect_type
        mask_dir = dataset / "ground_truth" / defect_type
        image_dir.mkdir(parents=True, exist_ok=True)
        mask_dir.mkdir(parents=True, exist_ok=True)
        defect_dirs.append(image_dir.relative_to(dataset).as_posix())
        mask_dirs.append(mask_dir.relative_to(dataset).as_posix())
        counts[defect_type] = 0

        for idx in range(ANOMALY_COUNTS["per_defect"]):
            image_seed = _seed_for(3 + type_index, idx + 1, seed)
            image, mask, _defects = ps.render_defective(
                ANOMALY_IMAGE_SIZE, ANOMALY_IMAGE_SIZE, image_seed,
                defect_types=(defect_type,), count=1,
            )
            stem = f"{defect_type}_{idx:04d}"
            image_path = image_dir / f"{stem}.png"
            mask_path = mask_dir / f"{stem}_mask.png"
            ps.save_rgb(image, image_path)
            ps.save_mask(mask, mask_path)
            all_images.append(image_path)
            counts[defect_type] += 1

    ps.assert_unique_images(all_images, label="anomaly images")

    layout = {
        "dataset_root": dataset.as_posix(),
        "name": "pvc_sheet",
        "normal_dir": "train/good",
        "normal_test_dir": "test/good",
        "abnormal_dir": defect_dirs,
        "mask_dir": mask_dirs,
        "image_size": ANOMALY_IMAGE_SIZE,
        "counts": {
            "train_good": ANOMALY_COUNTS["train_good"],
            "test_good": ANOMALY_COUNTS["test_good"],
            **counts,
        },
        "seed": seed,
        "duplicate_images_across_splits": 0,
        "note": (
            "Synthetic PVC-like surfaces. Training uses normal images only; "
            "test images were never seen during fitting."
        ),
    }
    (dataset / "dataset_layout.json").write_text(
        json.dumps(layout, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return layout


# ---------------------------------------------------------------------------
# メイン / entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the synthetic YOLO and PatchCore datasets.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--only", choices=["yolo", "anomaly"], default=None)
    parser.add_argument("--force", action="store_true", help="delete existing data first")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    if args.only in (None, "yolo"):
        summary = build_yolo_dataset(root, args.seed, args.force)
        print("=== YOLO dataset ===")
        for split, info in summary["splits"].items():
            print(f"  {split:<6} images={info['images']:<3} defects={info['defect_images']:<3} "
                  f"background={info['background_images']:<3} instances={info['instances']}")
        print(f"  yaml: {(root / 'assets' / 'yolo_dataset' / 'data.yaml').as_posix()}")

    if args.only in (None, "anomaly"):
        layout = build_anomaly_dataset(root, args.seed, args.force)
        print("=== Anomaly dataset (Anomalib Folder layout) ===")
        print(f"  root: {layout['dataset_root']}")
        for key, value in layout["counts"].items():
            print(f"  {key:<16} {value}")

    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
