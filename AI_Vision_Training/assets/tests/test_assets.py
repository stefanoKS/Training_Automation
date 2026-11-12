"""生成アセットの検証 / Validation of the generated assets.

    python -m pytest assets/tests -v

日本語：生成された図・サンプル画像・校正データが「使える状態か」を確認します。
English: Checks that the generated diagrams, sample images and calibration data are usable.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

COURSE_ROOT = Path(__file__).resolve().parents[2]
ASSETS = COURSE_ROOT / "assets"
DIAGRAMS = ASSETS / "diagrams"
SCRIPTS = ASSETS / "scripts"

sys.path.insert(0, str(SCRIPTS))

EXPECTED_DIAGRAMS = [
    "diagram_pixel_grid.png",
    "diagram_grayscale_values.png",
    "diagram_coordinate_system.png",
    "diagram_classification.png",
    "diagram_detection.png",
    "diagram_segmentation.png",
    "diagram_instance_segmentation.png",
    "diagram_anomaly_heatmap.png",
    "diagram_control_flow.png",
    "diagram_dataset_split.png",
    "diagram_yolo_annotation.png",
    "diagram_pixel_distance.png",
    "diagram_calibration_concept.png",
    "diagram_patchcore_concept.png",
    "diagram_yolo_vs_patchcore.png",
]

# 小さすぎる図は、日本語や数字が読めない / a diagram this small cannot be read
MIN_DIAGRAM_WIDTH = 600
MIN_DIAGRAM_HEIGHT = 300


def test_all_required_diagrams_exist() -> None:
    missing = [name for name in EXPECTED_DIAGRAMS if not (DIAGRAMS / name).is_file()]
    assert not missing, f"missing diagrams: {missing}"


@pytest.mark.parametrize("name", EXPECTED_DIAGRAMS)
def test_diagram_is_readable(name: str) -> None:
    path = DIAGRAMS / name
    if not path.is_file():
        pytest.skip(f"{name} not generated yet")
    with Image.open(path) as image:
        width, height = image.size
    assert width >= MIN_DIAGRAM_WIDTH, f"{name} is too narrow ({width}px)"
    assert height >= MIN_DIAGRAM_HEIGHT, f"{name} is too short ({height}px)"


def test_calibration_image_matches_ground_truth() -> None:
    """校正画像の基準線の長さが、記録された値と一致するか。"""
    info_path = DIAGRAMS / "calibration_ground_truth.json"
    image_path = DIAGRAMS / "calibration_image.png"
    if not (info_path.is_file() and image_path.is_file()):
        pytest.skip("calibration assets not generated yet")

    info = json.loads(info_path.read_text(encoding="utf-8"))
    array = np.asarray(Image.open(image_path).convert("L"))

    dark_columns = np.where((array[info["bar_y"]] < 80))[0]
    assert len(dark_columns) > 0, "the reference bar is not visible"

    measured = int(dark_columns.max() - dark_columns.min()) + 1
    assert abs(measured - info["reference_px"]) <= 3, (
        f"bar length {measured}px does not match the recorded {info['reference_px']}px"
    )
    assert info["px_per_mm"] == pytest.approx(info["reference_px"] / info["reference_mm"])


def test_defect_samples_have_matching_masks() -> None:
    index_path = ASSETS / "defect_samples" / "defects.json"
    if not index_path.is_file():
        pytest.skip("sample images not generated yet")

    records = json.loads(index_path.read_text(encoding="utf-8"))
    assert records, "defects.json is empty"

    for record in records:
        image_path = ASSETS / "defect_samples" / record["image"]
        mask_path = ASSETS / "defect_samples" / record["mask"]
        assert image_path.is_file(), f"missing image {image_path}"
        assert mask_path.is_file(), f"missing mask {mask_path}"

        mask = np.asarray(Image.open(mask_path).convert("L"))
        assert mask.max() > 0, f"{record['image']} has an all-black mask"
        assert record["defects"], f"{record['image']} has no defect records"


def test_defect_boxes_enclose_mask_pixels() -> None:
    """記録されたバウンディングボックスが、実際のマスクを囲んでいるか。"""
    index_path = ASSETS / "defect_samples" / "defects.json"
    if not index_path.is_file():
        pytest.skip("sample images not generated yet")

    records = json.loads(index_path.read_text(encoding="utf-8"))
    for record in records:
        mask = np.asarray(Image.open(ASSETS / "defect_samples" / record["mask"]).convert("L"))
        for defect in record["defects"]:
            x1, y1, x2, y2 = defect["bbox"]
            assert 0 <= x1 < x2 <= mask.shape[1], f"bad bbox {defect['bbox']} in {record['image']}"
            assert 0 <= y1 < y2 <= mask.shape[0], f"bad bbox {defect['bbox']} in {record['image']}"
            inside = mask[y1:y2, x1:x2]
            assert inside.max() > 0, f"bbox {defect['bbox']} contains no defect pixels"


def test_generator_is_deterministic() -> None:
    """同じ seed からは同じ画像が出るか（再現性）。"""
    import pvc_synth as ps

    first = ps.render_normal(64, 64, seed=1234)
    second = ps.render_normal(64, 64, seed=1234)
    other = ps.render_normal(64, 64, seed=9999)

    assert np.array_equal(first, second), "same seed produced different images"
    assert not np.array_equal(first, other), "different seeds produced identical images"


def test_defective_render_produces_requested_defects() -> None:
    import pvc_synth as ps

    image, mask, defects = ps.render_defective(
        128, 128, seed=77, defect_types=("black_spot", "scratch", "streak"), count=3
    )
    assert image.shape == (128, 128, 3)
    assert mask.shape == (128, 128)
    assert len(defects) == 3
    assert {d.cls for d in defects} == {"black_spot", "scratch", "streak"}
    for defect in defects:
        x1, y1, x2, y2 = defect.bbox
        assert x1 >= 0 and y1 >= 0 and x2 <= 128 and y2 <= 128
        assert defect.width > 0 and defect.height > 0


def test_yolo_coordinates_are_normalised() -> None:
    import pvc_synth as ps

    defect = ps.Defect(cls="black_spot", bbox=(96, 72, 168, 132))
    xc, yc, w, h = defect.to_yolo(240, 240)
    assert 0.0 <= xc <= 1.0 and 0.0 <= yc <= 1.0
    assert 0.0 < w <= 1.0 and 0.0 < h <= 1.0
    assert xc == pytest.approx(0.55)
    assert yc == pytest.approx(0.425)
    assert w == pytest.approx(0.3)
    assert h == pytest.approx(0.25)


def test_environment_verifier_runs_without_crashing() -> None:
    import verify_environment as ve

    report = ve.build_report("base", COURSE_ROOT)
    assert report["python"]["version"]
    assert isinstance(report["assets"], list)
    assert report["missing"] == [] or isinstance(report["missing"], list)
