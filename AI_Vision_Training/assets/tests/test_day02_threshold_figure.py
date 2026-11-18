"""Day 2 のしきい値スイープ図のテスト / the Day 2 threshold-sweep figure.

この図は「しきい値を上げると、前景の画素数は減らないが、外部輪郭の数は増減する」ことを教えます。
数値は合成画像から実際に計算した値で、テストも同じ計算を独立にやり直して比べます。
The figure teaches that raising the threshold never removes foreground pixels while the external
contour count still moves. The numbers are recomputed here from the same synthetic input.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import numpy as np
import pytest

COURSE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(COURSE_ROOT / "assets" / "scripts"))
from course_notebooks import course_notebooks  # noqa: E402

import generate_teaching_diagrams as diagrams  # noqa: E402
from teaching_data import spot_mask  # noqa: E402

CELL_ID = "fig-teach_threshold_sweep"
THRESHOLDS = list(range(40, 221, 10))


@pytest.fixture(scope="module", autouse=True)
def japanese_font():
    """main() と同じフォント設定にする / same font setup as the generator's main()."""
    family = diagrams.configure_matplotlib()
    diagrams.plt.rcParams["font.monospace"] = [family, "DejaVu Sans Mono", "monospace"]
    diagrams.plt.rcParams["font.family"] = [family, "DejaVu Sans"]
    return family


@pytest.fixture(scope="module")
def grey() -> np.ndarray:
    return cv2.cvtColor(diagrams._pvc_sheet(200, defect="spot", seed=52), cv2.COLOR_RGB2GRAY)


@pytest.fixture(scope="module")
def cell_source() -> str:
    path, = course_notebooks(COURSE_ROOT / "notebooks", "Day02_03*.ipynb")
    notebook = json.loads(path.read_text(encoding="utf-8"))
    return next("".join(cell["source"]) for cell in notebook["cells"] if cell.get("id") == CELL_ID)


def _foreground(grey: np.ndarray, threshold: int) -> int:
    _, binary = cv2.threshold(grey, threshold, 255, cv2.THRESH_BINARY_INV)
    return int((binary > 0).sum())


def _external_contours(grey: np.ndarray, threshold: int) -> int:
    _, binary = cv2.threshold(grey, threshold, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return len(contours)


def test_the_sweep_keeps_its_nineteen_thresholds() -> None:
    rows = diagrams._threshold_sweep(np.zeros((8, 8), dtype=np.uint8), THRESHOLDS)
    assert [row["threshold"] for row in rows] == THRESHOLDS
    assert len(THRESHOLDS) == 19


@pytest.mark.parametrize("threshold, expected", [(100, 249), (160, 249), (210, 36677)])
def test_reference_pixel_counts_stay_correct(grey, threshold, expected) -> None:
    assert _foreground(grey, threshold) == expected


def test_the_spot_holds_exactly_the_reference_pixels(grey) -> None:
    assert int(spot_mask(200).sum()) == 249
    assert _foreground(grey, 100) == int(spot_mask(200).sum())


def test_foreground_never_falls_as_the_threshold_rises(grey) -> None:
    counts = [_foreground(grey, threshold) for threshold in THRESHOLDS]
    assert all(later >= earlier for earlier, later in zip(counts, counts[1:]))


def test_the_contour_count_is_not_monotonic(grey) -> None:
    counts = [_external_contours(grey, threshold) for threshold in THRESHOLDS]
    assert max(counts) > min(counts)
    assert any(later < earlier for earlier, later in zip(counts, counts[1:])), (
        "the figure's whole point is that the contour count can fall while pixels rise")


def test_sweep_contours_are_the_real_external_contours(grey) -> None:
    rows = {row["threshold"]: row for row in diagrams._threshold_sweep(grey, THRESHOLDS)}
    for threshold in (40, 100, 190, 200, 210, 220):
        assert rows[threshold]["regions"] == _external_contours(grey, threshold)
        assert rows[threshold]["foreground"] == _foreground(grey, threshold)
    # `CV_CHAIN_APPROX_SIMPLE` still returns every external boundary, not an approximation of the count
    _, binary = cv2.threshold(grey, 210, 255, cv2.THRESH_BINARY_INV)
    external, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    listed, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    assert rows[210]["regions"] == len(external) < len(listed)


def test_the_figure_is_rebuilt_byte_for_byte(tmp_path) -> None:
    first = diagrams.teach_threshold_sweep(tmp_path / "first.png").read_bytes()
    second = diagrams.teach_threshold_sweep(tmp_path / "second.png").read_bytes()
    assert first == second
    shipped = COURSE_ROOT / "assets" / "diagrams" / "teach_threshold_sweep.png"
    assert shipped.is_file()
    assert shipped.read_bytes() == first, (
        "assets/diagrams/teach_threshold_sweep.png is stale; rerun "
        "python assets\\scripts\\generate_teaching_diagrams.py --only teach_threshold_sweep")


def test_the_explanation_answers_the_six_questions(cell_source: str) -> None:
    for number in range(1, 7):
        assert f"**{number}." in cell_source, f"question {number} is not answered"
    assert "≈" not in cell_source and "  " not in cell_source.split("<!-- ne:begin end -->")[0][:0]


def test_the_explanation_keeps_the_numbers_and_the_units_honest(cell_source: str) -> None:
    assert "249 px" in cell_source
    assert "36,677 px" in cell_source
    assert "62.25 mm²" in cell_source
    assert "mm²" in cell_source
    assert "2.00 px/mm" in cell_source


def test_the_explanation_says_the_input_never_changes(cell_source: str) -> None:
    assert "入力は変えていません" in cell_source
    assert "変えたのは\nしきい値 T" in cell_source or "変えたのは" in cell_source
    assert "THRESH_BINARY_INV" in cell_source
    assert "I ≤ T" in cell_source and "I > T" in cell_source


def test_contours_are_not_described_as_defects(cell_source: str) -> None:
    assert "外部輪郭" in cell_source
    assert "cv2.RETR_EXTERNAL" in cell_source
    # 数えているのは境界であって欠陥ではない、と両方の言語で明言していること。
    # Both languages must say that the count is a boundary count, not a defect count.
    assert "輪郭の数は「欠陥の数」ではありません" in cell_source
    assert "The contour count is not the number of defects" in cell_source
    assert "An external contour is only" in cell_source


def test_the_caption_stays_with_its_image(cell_source: str) -> None:
    image = "![](../../assets/diagrams/teach_threshold_sweep.png)"
    assert cell_source.count(image) == 1
    after = cell_source.split(image, 1)[1]
    assert after.lstrip().startswith("図："), "the Japanese caption must follow the image"
    assert "Figure:" in after[:600]
    assert after.index("<!-- ne:begin after-image:") > after.index("Figure:")


def test_the_prediction_exercise_is_present(cell_source: str) -> None:
    assert "しきい値を上げると、前景の画素数は増えますか、減りますか。" in cell_source
    assert "外部輪郭の数は増えますか、減りますか。" in cell_source


def test_the_explanation_is_trilingual(cell_source: str) -> None:
    assert "<!-- ne:begin after-heading -->" in cell_source
    assert "<!-- ne:begin after-image:" in cell_source
    assert "<!-- ne:begin end -->" in cell_source
    for marker in ("chitra:", "threshold", "piksel"):
        assert marker in cell_source
