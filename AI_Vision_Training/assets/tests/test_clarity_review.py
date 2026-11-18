"""Focused runtime regressions for the beginner clarity changes (no model inference)."""

from __future__ import annotations

import copy
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import cv2
import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "assets" / "scripts"))
from course_notebooks import course_notebooks  # noqa: E402
from generate_clarity_figures import BUILDERS, REGIONS  # noqa: E402


def cells(prefix: str) -> list[dict]:
    path, = course_notebooks(ROOT / "notebooks", f"{prefix}*.ipynb")
    return json.loads(path.read_text(encoding="utf-8"))["cells"]


def code(prefix: str, identifier: str) -> str:
    return "".join(next(c for c in cells(prefix) if c.get("id") == "clarity-" + identifier)["source"])


def run(text: str, namespace: dict | None = None) -> dict:
    values = {"np": np, "cv2": cv2, "plt": plt, "show": lambda *args, **kwargs: None}
    if namespace:
        values.update(namespace)
    try:
        exec(compile(text, "<clarity lesson>", "exec"), values)
    finally:
        plt.close("all")
    return values


def test_executed_slice_uses_the_illustrated_canvas_and_exclusive_stops() -> None:
    notebook = cells("Day01_02")
    construction = next("".join(c["source"]) for c in notebook
                        if c["cell_type"] == "code" and "canvas = np.zeros" in "".join(c["source"]))
    values = run(construction + "\n" + code("Day01_02", "pixel-value") + "\n" + code("Day01_02", "slice-live"))
    assert values["canvas"][2, 3] == 100 and values["canvas"][3, 2] == 0
    np.testing.assert_array_equal(values["selected"], [[0, 0, 0], [0, 100, 0], [0, 0, 0]])
    expanded = run(code("Day01_02", "slice-live").replace("[1:4, 2:5]", "[1:4, 2:6]"),
                   {"canvas": values["canvas"]})
    assert expanded["selected"].shape == (3, 4)


def test_live_bgr_counterexample_and_same_mask_geometry() -> None:
    notebook = cells("Day02_03")
    preparation = next(i for i, c in enumerate(notebook) if "def show(images, titles=None" in "".join(c["source"]))
    demo = next(i for i, c in enumerate(notebook) if c.get("id") == "clarity-bgr-live")
    assert preparation < demo
    bgr = run(code("Day02_03", "bgr-live"))
    assert bgr["bgr_strip"][0, 0].tolist() == [0, 0, 255]
    assert bgr["rgb_strip"][0, 0].tolist() == [255, 0, 0]
    mask = run(code("Day02_03", "mask-live"))
    assert mask["white_pixels"] == 12
    assert mask["geometric_area"] == 6
    assert cv2.threshold(mask["truth_pixels"], 100, 255, cv2.THRESH_BINARY_INV)[1].tolist() == [[255, 255, 255, 0]]
    wider = run(code("Day02_03", "mask-live").replace("[2:5, 2:6]", "[2:5, 2:7]"))
    assert wider["white_pixels"] == 15 and wider["geometric_area"] == 8


def test_edited_box_changes_x_centre_and_width_only(capsys) -> None:
    values = run(code("Day03_01", "bbox-live"))
    assert values["box_width"] == 96 and values["centre_x"] == 144
    assert values["yolo_box"] == pytest.approx((.6, .425, .4, .25))
    assert "0 0.600000 0.425000 0.400000 0.250000" in capsys.readouterr().out
    with pytest.raises(ValueError, match="inside image"):
        run(code("Day03_01", "bbox-live").replace("right_edge_change = 24", "right_edge_change = 240"))


def test_c_severity_is_reported_as_ng_without_changing_public_grade(capsys) -> None:
    text = next("".join(c["source"]) for c in cells("Day02_02")
                if c["cell_type"] == "code" and "def grade_width(" in "".join(c["source"]))
    values = run(text)
    assert values["grade_width"](.6).startswith("C (warning")
    output = capsys.readouterr().out
    assert output.count("C (warning / 注意); 規格 / spec: NG") == 2


def freeze_namespace(tmp_path: Path) -> dict:
    day05 = tmp_path / "submissions" / "day05"
    day05.mkdir(parents=True)
    sys.path.insert(0, str(ROOT / "assets" / "helpers"))
    import experiment_identity as identity

    manifest = {"model": {"backbone": "test fixture"}, "postprocessor": {"enabled": True},
                "score_convention": "fixture", "partitions": {"test": ["test/a.png"]},
                "dataset_name": "fixture", "dataset_seed": 0, "image_size": [8, 8],
                "counts": {"calibration": 1, "test": 1},
                "split": {"library": "fixture", "val_split_mode": "from_test",
                          "val_split_ratio": 0.5}}
    experiment = identity.base_identity(
        manifest,
        {"fingerprint": "0" * 64, "tensor_count": 0, "memory_bank": None},
        {"available": False},
    )
    manifest["experiment"] = experiment
    (day05 / "patchcore_fitted_state.json").write_text(
        json.dumps({"schema_version": 1, "experiment": experiment}), encoding="utf-8")
    return {"COURSE_ROOT": tmp_path, "json": json, "YOLO_THRESHOLD": .06,
            "PATCHCORE_THRESHOLD": .5,
            "manifest": manifest,
            "yolo_data": {"weights": "fixture.pt"},
            "patchcore_data": {"experiment": experiment}}


def test_freeze_requires_written_declaration_and_persists_reused_data_status(tmp_path) -> None:
    text = code("Day05_03", "freeze-record")
    values = freeze_namespace(tmp_path)
    with pytest.raises(ValueError, match="declaration"):
        run(text, values)
    assert not (tmp_path / "submissions" / "day05" / "comparison_freeze_record.json").exists()
    values = run(text.replace('FREEZE_DECLARATION = ""', 'FREEZE_DECLARATION = "Frozen before test; no retuning"'), values)
    record = json.loads(values["freeze_path"].read_text(encoding="utf-8"))
    assert record["assessment_role"] == "illustrative_reused_data"
    assert record["test_already_seen"] is True
    assert record["yolo_threshold"] == .06
    evaluation = next("".join(c["source"]) for c in cells("Day05_03")
                      if c["cell_type"] == "code" and "test_predictions = {" in "".join(c["source"]))
    guard = evaluation.split("test_predictions = {")[0]
    run(guard, values)
    for changed in ("YOLO_THRESHOLD", "PATCHCORE_THRESHOLD"):
        altered = dict(values)
        altered[changed] += .01
        with pytest.raises(RuntimeError, match="frozen settings changed"):
            run(guard, altered)
    altered = copy.deepcopy(values["manifest"])
    altered["model"]["backbone"] = "different fixture"
    with pytest.raises(RuntimeError, match="frozen settings changed"):
        run(guard, {**values, "manifest": altered})


def test_test_archive_is_opt_in_and_calibration_controls_precede_freeze(capsys) -> None:
    notebook = cells("Day05_03")
    index = lambda token: next(i for i, c in enumerate(notebook) if token in "".join(c["source"]))
    assert index("patchcore_threshold_to_try =") < index('FREEZE_DECLARATION = ""') < index("test_predictions = {")
    assert all("ref_comparison_5col.png" not in "".join(c["source"])
               for c in notebook if c["cell_type"] == "markdown")
    run(code("Day05_03", "archive-gate"))
    assert "hidden" in capsys.readouterr().out
    with pytest.raises(RuntimeError, match="freeze and evaluate"):
        run(code("Day05_03", "archive-gate").replace("SHOW_ARCHIVED_TEST = False", "SHOW_ARCHIVED_TEST = True"))
    appendix = ROOT / "docs" / "instructor" / "day05_after_freeze_archive.md"
    assert "ref_comparison_5col.png" in appendix.read_text(encoding="utf-8")
    assert (appendix.parent / "../../assets/reference_outputs/ref_comparison_5col.png").resolve().is_file()


def test_legacy_figure_inserter_does_not_restore_retired_or_curated_captions() -> None:
    import insert_lesson_figures as figures

    retired = {"ref_comparison_5col.png", "ref_anomaly_panels.png", "teach_evaluation_sequence.png"}
    assert not retired.intersection(entry["image"] for entry in figures.FIGURES)
    sample = figures.FIGURES[0]
    edited = {"cell_type": "markdown", "id": figures._cell_id(sample),
              "metadata": {"aivision_caption": "clarity-review-2026-11-16"},
              "source": [f"![](../../assets/{sample['folder']}/{sample['image']})\n",
                         "意図的に短くした説明 / intentionally concise caption\n"]}
    assert figures._update({"cells": [edited]}, sample) is False


@pytest.mark.parametrize("prefix", ["Day05_01", "Day05_02", "Day05_03"])
def test_prefreeze_day5_has_no_archived_test_panel_or_worked_answer(prefix) -> None:
    prefreeze = []
    for cell in cells(prefix):
        if cell.get("id") == "clarity-freeze-record":
            break
        prefreeze.append("".join(cell["source"]))
        prefreeze.append(json.dumps(cell.get("outputs", []), ensure_ascii=False))
    text = "\n".join(prefreeze)
    for forbidden in ("ref_anomaly_panels.png", "ref_comparison_5col.png",
                      "21.439", "21.762", "saved scalar 1.000", "archived 1.000", "保存例1.000",
                      "black_spot_0000", "streak_0005"):
        assert forbidden not in text, f"{prefix}: early TEST evidence {forbidden}"


def test_assignment_prompt_has_an_immediate_editable_equality_example(capsys) -> None:
    notebook = cells("Day02_01")
    index = next(i for i, c in enumerate(notebook) if c.get("id") == "fig-teach_assign_vs_compare")
    example = notebook[index + 1]
    assert example["cell_type"] == "code"
    text = "".join(example["source"])
    assert 2 <= len(text.splitlines()) <= 4
    run(text)
    assert capsys.readouterr().out == "True\n"
    run(text.replace("width = 100.3", "width = 100.4"))
    assert capsys.readouterr().out == "False\n"
    assert notebook[index + 2]["id"] == "9ff42d85"


def test_bilingual_threshold_caption_and_calibration_cross_references() -> None:
    caption = "".join(next(c for c in cells("Day02_03") if c["id"] == "4a6c53f8")["source"])
    assert "左の元画像は、しきい値を変えても変わりません。" in caption
    assert "The left-hand original stays unchanged when the threshold T changes." in caption
    scoring = "".join(next(c for c in cells("Day05_03") if c["id"] == "3d343aab")["source"])
    assert "前の較正用スライダー" in scoring and "earlier calibration slider" in scoring
    assert "次の節のスライダー" not in scoring and "next section" not in scoring
    assert "original final test score" in scoring and "new untouched holdout" in scoring
    training = cells("Day05_02")
    index = next(i for i, c in enumerate(training) if c["id"] == "6c5c2682")
    bridge = "".join(training[index - 1]["source"])
    assert "engine.test()" in bridge and "val_dataloader()" in bridge
    assert "ライブラリのメソッド名" in bridge and "library method name" in bridge
    assert "not the held-out TEST" in bridge


def test_float_surprise_has_adjacent_explanation_and_toy_not_spec_tolerance() -> None:
    notebook = cells("Day02_01")
    expected = "".join(next(c for c in notebook if c["id"] == "acfe495e")["source"])
    assert "0.29999999999999716" in expected
    assert "保存した数の近似" in expected and "stored-number approximation" in expected
    optional = "\n".join("".join(c["source"]) for c in notebook
                         if c["id"] in {"1b60ce34", "50c7ee88", "91118470"})
    assert "safe comparison" not in optional
    assert "not a manufacturing acceptance criterion" in optional
    assert "規格" in optional and "1e-9" in optional


def test_original_figure_generator_preserves_clarity_manifest_section(tmp_path, monkeypatch) -> None:
    import generate_svg_figures as figures

    manifest = tmp_path / "docs" / "visual_figure_manifest.md"
    manifest.parent.mkdir()
    extra = ("## 2026-11-16 clarity additions / 明確化の追加図\n\n"
             "teach_fixed_fov_sampling / calculated synthetic\n\n")
    manifest.write_text(extra + "## Existing source-checked figures / 既存の検証済み図\n\nold rows",
                        encoding="utf-8")
    monkeypatch.setattr(figures, "FIGURES", {})
    monkeypatch.setattr(sys, "argv", ["generate_svg_figures.py", "--root", str(tmp_path)])
    assert figures.main() == 0
    result = manifest.read_text(encoding="utf-8")
    assert extra in result and "old rows" not in result
    assert figures.main() == 0
    assert manifest.read_text(encoding="utf-8") == result


@pytest.mark.parametrize("name", BUILDERS)
def test_new_diagrams_are_deterministic_offline_and_text_stays_inside_canvas(name, tmp_path) -> None:
    first, second = BUILDERS[name](), BUILDERS[name]()
    assert ET.tostring(first.root) == ET.tostring(second.root)
    first.save(tmp_path, name)
    tree = ET.parse(tmp_path / "assets" / "svg" / f"{name}.svg")
    text_boxes = []
    for element in tree.getroot().iter():
        assert not any("href" in key for key in element.attrib)
        if element.tag.endswith("text"):
            x, y = float(element.attrib["x"]), float(element.attrib["y"])
            size, width = float(element.attrib["font-size"]), float(element.attrib["data-text-width"])
            assert 0 <= x < x + width <= 890 and 0 <= y - size < y + size / 4 <= 590
            text_boxes.append((x, y, width, size))
    for i, (x, y, w, size) in enumerate(text_boxes):
        for x2, y2, w2, size2 in text_boxes[i + 1:]:
            if max(y - size, y2 - size2) < min(y + size / 4, y2 + size2 / 4):
                assert x + w <= x2 or x2 + w2 <= x
    if name == "teach_patch_overlap":
        a, b = REGIONS
        assert min(a[2], b[2]) > max(a[0], b[0])
        assert min(a[3], b[3]) > max(a[1], b[1])
