"""Regression tests for the audit's geometric, physical and notebook-behaviour fixes."""

from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import cv2
import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "assets" / "scripts"))
sys.path.insert(0, str(ROOT / "assets" / "helpers"))

import generate_svg_figures as svg  # noqa: E402
from generate_teaching_diagrams import _pvc_sheet  # noqa: E402
from teaching_data import BBOX_XYXY, calibrated_defects, mask_box, spot_mask  # noqa: E402
from training_run import save_training_run, select_training_run  # noqa: E402


def notebook(stem: str) -> dict:
    path = next((ROOT / "notebooks").glob(f"*/{stem}.ipynb"))
    return json.loads(path.read_text(encoding="utf-8"))


def sources(stem: str, kind: str = "code") -> list[str]:
    return ["".join(c["source"]) for c in notebook(stem)["cells"] if c["cell_type"] == kind]


def load_function(stem: str, name: str):
    source = next(s for s in sources(stem) if f"def {name}(" in s)
    tree = ast.parse(source)
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    namespace: dict = {}
    exec(compile(ast.Module(body=[function], type_ignores=[]), "<notebook function>", "exec"), namespace)
    return namespace[name]


def test_four_tasks_use_the_source_spot_geometry() -> None:
    mask = spot_mask(200)
    source = _pvc_sheet(200, defect="spot", seed=44)
    np.testing.assert_array_equal(np.all(source == (40, 40, 44), axis=2), mask)
    assert mask.sum() == 249
    assert mask_box(mask) == (76, 102, 93, 119)
    x1, y1, x2, y2 = mask_box(mask)
    assert np.count_nonzero(mask[y1:y2, x1:x2]) == mask.sum()
    figure = svg.build_figure("teach_cv_tasks_outputs")
    text = " ".join(n.text or "" for n in figure.root.iter())
    assert "GT: 249 pixels" in text
    assert "not model output" in text
    assert "0.87" not in text and "0.93" not in text


@pytest.mark.parametrize("name", ["judge", "judge_width"])
@pytest.mark.parametrize("measurement,expected", [
    (99.5, "OK"), (100.5, "OK"), (100.4999999, "OK"),
    (100.5001, "NG"), (100.5000001, "NG"), (99.4999999, "NG"),
])
def test_tolerance_is_inclusive_without_rounding(name: str, measurement: float, expected: str) -> None:
    judge = load_function("Day02_02_Conditions_Loops_Functions", name)
    assert judge(measurement) == expected


def test_float_caveat_is_explicit_not_a_silent_epsilon() -> None:
    judge = load_function("Day02_02_Conditions_Loops_Functions", "judge")
    assert judge(2.1, 2.0, 0.1) == "NG"
    markdown = "\n".join(sources("Day02_02_Conditions_Loops_Functions", "markdown"))
    assert "binary" in markdown and "instrument resolution" in markdown


def test_same_plane_calibration_measures_independent_feature_and_area() -> None:
    image, info = calibrated_defects()
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, mask = cv2.threshold(gray, info["threshold"], 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])
    assert len(contours) == 2
    scale = np.linalg.norm(np.diff(info["reference_points"], axis=0)) / info["reference_mm"]
    assert scale == 1.2
    assert np.linalg.norm(np.diff(info["check_points"], axis=0)) / scale == 50
    assert cv2.countNonZero(mask) == sum(t["foreground_pixels"] for t in info["targets"]) == 1508
    for contour, target in zip(contours, info["targets"]):
        area = cv2.contourArea(contour)
        assert area == target["area_px2"]
        assert area / scale ** 2 == pytest.approx(target["area_mm2"])
        assert area != target["foreground_pixels"]
    assert [cv2.contourArea(c) / scale ** 2 for c in contours] == pytest.approx(
        [329.861111111, 642.361111111]
    )


def test_conversion_lesson_uses_new_scene_and_preserves_unsolved_exercise() -> None:
    from remediate_notebooks import CALIBRATION_CODE

    namespace = {"ASSETS": ROOT / "assets", "cv2": cv2, "json": json,
                 "distance_px": lambda a, b: float(np.linalg.norm(np.array(a) - np.array(b))),
                 "show": lambda *args, **kwargs: None}
    exec(compile(CALIBRATION_CODE, "<calibrated lesson>", "exec"), namespace)
    assert namespace["check_length_mm"] == 50
    assert len(namespace["calibrated_contours"]) == 2
    exercises = [s for s in sources("Day02_03_OpenCV_Image_Processing")
                 if "area_mm2 = 0.0" in s]
    assert len(exercises) == 1
    assert "enumerate(calibrated_contours," in exercises[0]
    assert "enumerate(kept," not in exercises[0]
    caption = next(s for s in sources("Day02_03_OpenCV_Image_Processing", "markdown")
                   if "teach_pixel_to_mm.png" in s)
    assert "assumed edge-location uncertainty" in caption
    assert "one pixel of error" not in caption


def test_bbox_diagram_and_executed_notebook_use_one_example(capsys) -> None:
    source = next(s for s in sources("Day03_01_YOLO_Concepts") if "x1, y1, x2, y2 = 96" in s)
    namespace: dict = {}
    exec(compile(source, "<bbox>", "exec"), namespace)
    assert tuple(namespace[v] for v in ("x1", "y1", "x2", "y2")) == BBOX_XYXY
    assert tuple(namespace[v] for v in ("xc", "yc", "w", "h")) == pytest.approx((.55, .425, .3, .25))
    assert "0 0.550000 0.425000 0.300000 0.250000" in capsys.readouterr().out
    text = " ".join(n.text or "" for n in svg.build_figure("teach_bbox_one_example").root.iter())
    assert "0 0.550 0.425 0.300 0.250" in text


def test_iou_retains_correct_mathematics() -> None:
    iou = load_function("Day03_01_YOLO_Concepts", "iou")
    # The retained teach_iou_rects figure uses xywh (60,60,110,90) and (80,75,120,100).
    assert iou((60, 60, 170, 150), (80, 75, 200, 175)) == pytest.approx(6750 / 15150)


def test_matching_diagram_matrix_and_one_to_one_counts() -> None:
    _, _, matrix = svg.matching_values()
    np.testing.assert_allclose(matrix, [[1, 3480 / 3720], [0, 0]])
    text = " ".join(n.text or "" for n in svg.draw_matching().root.iter())
    assert "TP=1, FP=1, FN=1" in text
    assert "conf >= 0.50" in text


def test_mass_figure_inputs_match_unsolved_exercise() -> None:
    from teaching_data import MASS_INPUTS

    source = next(s for s in sources("Day02_01_Python_Basics") if "density_g_per_cm3 = 1.4" in s)
    namespace: dict = {}
    exec(compile(source, "<mass exercise>", "exec"), namespace)
    inputs = tuple(namespace[k] for k in ("width_mm", "length_mm", "thickness_mm", "density_g_per_cm3"))
    assert inputs == MASS_INPUTS
    width, length, thickness, density = inputs
    assert width * length * thickness / 1000 * density / 1000 == pytest.approx(1.5925)
    assert namespace["mass_kg"] == 0.0  # The learner must still complete the exercise.


def test_current_batch_and_leakage_captions_keep_their_technical_caveats() -> None:
    import insert_lesson_figures as figures

    entry = next(e for e in figures.FIGURES if e["image"] == "teach_training_update.png")
    caption = next(s for s in sources("Day04_02_YOLO_Training", "markdown")
                   if "teach_training_update.png" in s)
    assert entry["notice_en"] in caption
    assert "warmup can also change the accumulation count" in caption
    assert "8 loader iterations and 1 weight update" not in caption
    leakage = next(s for s in sources("Day04_01_YOLO_Dataset_Annotation", "markdown")
                   if "teach_leakage_split.png" in s)
    assert "pixel-intensity noise, not a spatial shift" in leakage


def test_legacy_figures_do_not_reintroduce_rounding_or_universal_update_counts(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.text import Text
    import generate_teaching_diagrams as diagrams

    text = []

    def capture(figure, output):
        text.extend(artist.get_text() for artist in figure.findobj(Text))
        plt.close(figure)
        return output

    monkeypatch.setattr(diagrams, "_save", capture)
    diagrams.teach_loop_trace(tmp_path / "loop.png")
    assert "difference = measured_mm - nominal_mm" in text
    assert not any("round(" in line for line in text)
    text.clear()
    diagrams.teach_units_conversion(tmp_path / "units.png")
    assert any("later thickness exercise only" in line for line in text)
    for function in (diagrams.teach_epoch_batch, diagrams.teach_training_update):
        text.clear()
        function(tmp_path / "updates.png")
        joined = "\n".join(text)
        assert "nominal" in joined and "warmup" in joined
        assert "updates depend" in joined or "depends on settings" in joined
        assert not any("weight update per epoch" in line or "epoch 10" == line for line in text)


def test_model_selection_uses_mtime_not_lexical_order(tmp_path: Path) -> None:
    older = tmp_path / "training_results" / "day04" / "z_run" / "weights" / "best.pt"
    newer = tmp_path / "training_results" / "day04" / "a_run" / "weights" / "best.pt"
    for path in (older, newer):
        path.parent.mkdir(parents=True)
        path.write_bytes(b"test weights")
    os.utime(older, (100, 100))
    os.utime(newer, (200, 200))
    chosen, record = select_training_run(tmp_path)
    assert chosen == newer
    assert record["selection"] == "mtime fallback"
    save_training_run(tmp_path, older.parent.parent, {"epochs": 15})
    chosen, record = select_training_run(tmp_path)
    assert chosen == older and record["parameters"] == {"epochs": 15}
    older.unlink()
    with pytest.raises(FileNotFoundError, match="Manifest"):
        select_training_run(tmp_path)


def test_hash_output_does_not_claim_absence_of_leakage(tmp_path: Path, capsys) -> None:
    stem = "Day04_01_YOLO_Dataset_Annotation"
    source = next(s for s in sources(stem) if "def digest(" in s)
    for split in ("train", "val", "test"):
        directory = tmp_path / "images" / split
        directory.mkdir(parents=True)
        (directory / "frame.png").write_bytes(split.encode())
    exec(compile(source, "<hash lesson>", "exec"), {"dataset_dir": tmp_path})
    output = capsys.readouterr().out
    assert "No byte-identical duplicate files detected" in output
    assert "session/lot leakage are not excluded" in output
    assert "no leakage detected" not in output


def test_setup_sequence_and_historical_results_are_unambiguous() -> None:
    guide = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
    steps = [int(n) for n in re.findall(r"^## ステップ (\d+)", guide, re.M)]
    assert steps == list(range(1, 12))
    assert guide.index("generate_training_assets.py") < guide.index("Complete preflight")
    assert "CurrentUser" not in guide
    assert "--offline" in guide
    report = (ROOT / "docs" / "test_report.md").read_text(encoding="utf-8")
    assert report.index("Current main protocol") < report.index("17 / 26")
    assert "SUPERSEDED / biased" in report


@pytest.mark.parametrize("name", svg.FIGURES)
def test_svg_offline_resources_bounds_and_notebook_captions(name: str) -> None:
    path = ROOT / "assets" / "svg" / f"{name}.svg"
    tree = ET.parse(path)
    root = tree.getroot()
    assert root.attrib["viewBox"] == "0 0 900 590"
    forbidden = {"script", "image", "foreignObject", "style"}
    texts = []
    for element in root.iter():
        assert element.tag.rsplit("}", 1)[-1] not in forbidden
        assert not any("href" in key for key in element.attrib)
        if element.tag.endswith("text"):
            x, y = float(element.attrib["x"]), float(element.attrib["y"])
            size = float(element.attrib["font-size"])
            width = float(element.attrib["data-text-width"])
            assert 0 <= x < x + width <= 890
            assert 0 <= y - size and y + size * .25 <= 590
            texts.append((x, y, size, width))
        if element.tag.endswith("rect"):
            x, y = float(element.attrib["x"]), float(element.attrib["y"])
            w, h = float(element.attrib["width"]), float(element.attrib["height"])
            assert 0 <= x <= x + w <= 900
            assert 0 <= y <= y + h <= 590
    # Same-line label extents must not collide. Other geometric overlap requires visual inspection.
    for i, (x, y, size, width) in enumerate(texts):
        for x2, y2, size2, width2 in texts[i + 1:]:
            if abs(y - y2) < min(size, size2):
                assert x + width <= x2 or x2 + width2 <= x
    assert (ROOT / "assets" / "diagrams" / f"{name}_svg.png").is_file()
    stem = svg.FIGURES[name][0]
    caption = next(s for s in sources(stem, "markdown") if f"/{name}.svg" in s)
    assert caption.index("図：") < caption.index("Figure:")
    assert "What to notice" in caption and "Try to answer" in caption
    ignored = subprocess.run(["git", "check-ignore", "-q", str(path)], cwd=ROOT)
    assert ignored.returncode == 1
    fallback = ROOT / "assets" / "diagrams" / f"{name}_svg.png"
    assert subprocess.run(["git", "check-ignore", "-q", str(fallback)], cwd=ROOT).returncode == 1


def test_all_lessons_have_a_specific_learning_loop() -> None:
    from remediate_notebooks import LEARNING_LOOPS

    for stem in LEARNING_LOOPS:
        c = next(c for c in notebook(stem)["cells"] if c.get("id") == "audit-learning-loop")
        source = "".join(c["source"])
        assert "予想" in source and "predict" in source.lower()
        assert "deliberately erroneous" in source


def test_patchcore_offline_cache_policy_is_set_before_imports() -> None:
    code = sources("Day05_02_PatchCore_Training")
    combined = "\n".join(code)
    assert combined.index('os.environ["TIMM_USE_OLD_CACHE"]') < combined.index("import anomalib")
    model = next(s for s in code if "model = Patchcore(" in s)
    assert model.index("check_cached_file") < model.index("model = Patchcore(")
    assert "raise FileNotFoundError" in model
    markdown = "\n".join(sources("Day05_02_PatchCore_Training", "markdown"))
    assert "does not download automatically" in markdown


def test_svg_pdf_fallback_uses_same_generated_asset() -> None:
    from export_explanations_pdf import _image_size, _pdf_image_path

    vector = ROOT / "assets" / "svg" / "teach_slice_walkthrough.svg"
    assert _pdf_image_path(vector).name == "teach_slice_walkthrough_svg.png"
    assert _image_size(vector) == (1800, 1180)


def test_pixel_and_slice_figures_are_distinct_and_match_the_executed_array() -> None:
    from PIL import Image, ImageChops

    source = next(s for s in sources("Day01_02_Pixels_and_Images") if "canvas = np.zeros" in s)
    namespace = {"np": np}
    exec(compile(source, "<pixel lesson>", "exec"), namespace)
    array = namespace["canvas"]
    np.testing.assert_array_equal(svg.pixel_canvas(), array)
    assert array.shape == (5, 7) and array[2, 3] == 100 and array[3, 2] == 0
    np.testing.assert_array_equal(array[1:4, 2:5], [[0, 0, 0], [0, 100, 0], [0, 0, 0]])
    figures = [svg.build_figure(name) for name in ("teach_pixel_inspector", "teach_slice_walkthrough")]
    assert ET.tostring(figures[0].root) != ET.tostring(figures[1].root)
    pixel_text, slice_text = [" ".join(n.text or "" for n in figure.root.iter()) for figure in figures]
    assert "canvas[2, 3] = 100" in pixel_text and "canvas[1:4" not in pixel_text
    assert "canvas[1:4, 2:5]" in slice_text and "shape = (3, 3)" in slice_text
    assert "stop-exclusive" in slice_text
    for figure, selected_count in zip(figures, (1, 18)):
        selected = [n for n in figure.root.iter() if n.tag.endswith("rect")
                    and n.attrib.get("fill") == "#e8f0ff" and n.attrib.get("stroke") == svg.BLUE]
        assert len(selected) == selected_count  # One cell vs nine source cells + nine output cells.
    paths = [ROOT / "assets" / "svg" / f"{name}.svg"
             for name in ("teach_pixel_inspector", "teach_slice_walkthrough")]
    assert paths[0].read_bytes() != paths[1].read_bytes()
    with Image.open(ROOT / "assets" / "diagrams" / "teach_pixel_inspector_svg.png") as pixel:
        with Image.open(ROOT / "assets" / "diagrams" / "teach_slice_walkthrough_svg.png") as sliced:
            assert ImageChops.difference(pixel, sliced).getbbox() is not None
