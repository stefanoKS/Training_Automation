"""教材図のテスト / Teaching-asset tests.

「Python を実行しなくても、図が見える」ことを、ファイルの存在と Git の追跡状態で確かめます。
These tests verify that the essential teaching diagrams are visible **without running Python**:
they must exist, resolve from the notebook's own folder, and be tracked by Git (not ignored by
`.gitignore`), because a learner who cannot start a kernel must still see them.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

COURSE_ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK_DIR = COURSE_ROOT / "notebooks"
DIAGRAM_DIR = COURSE_ROOT / "assets" / "diagrams"
SCRIPTS = COURSE_ROOT / "assets" / "scripts"

sys.path.insert(0, str(SCRIPTS))

MD_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")
ASSET_DIR_RE = re.compile(r"^assets/diagrams/", re.I)

CONCEPT_NOTEBOOKS = [
    "Day01_01_Introduction_to_AI",
    "Day01_02_Pixels_and_Images",
    "Day01_03_Computer_Vision_Tasks",
    "Day02_01_Python_Basics",
    "Day02_02_Conditions_Loops_Functions",
    "Day02_03_OpenCV_Image_Processing",
    "Day03_01_YOLO_Concepts",
    "Day03_02_YOLO_Inference",
    "Day04_01_YOLO_Dataset_Annotation",
    "Day04_02_YOLO_Training",
    "Day04_03_YOLO_Evaluation",
    "Day05_01_Anomaly_Detection_Concepts",
    "Day05_02_PatchCore_Training",
    "Day05_03_YOLO_vs_PatchCore",
]


def _notebook(stem: str) -> Path:
    matches = sorted(NOTEBOOK_DIR.rglob(f"{stem}.ipynb"))
    assert len(matches) == 1, (stem, matches)
    return matches[0]


def _markdown_images(path: Path) -> list[str]:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    targets = []
    for cell in notebook["cells"]:
        if cell["cell_type"] != "markdown":
            continue
        source = "".join(cell["source"])
        targets.extend(t for t in MD_IMAGE_RE.findall(source)
                       if not t.startswith(("http://", "https://", "data:")))
    return targets


def _git_ignored(relative: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", relative],
        cwd=str(COURSE_ROOT), capture_output=True, text=True,
    )
    if result.returncode not in (0, 1):
        pytest.skip(f"git is unavailable ({result.stderr.strip()})")
    return result.returncode == 0


@pytest.mark.parametrize("stem", CONCEPT_NOTEBOOKS)
def test_every_concept_notebook_has_a_visible_figure(stem: str) -> None:
    images = _markdown_images(_notebook(stem))
    assert images, f"{stem}: no Markdown image reference; the concept is invisible without a kernel"


@pytest.mark.parametrize("stem", CONCEPT_NOTEBOOKS + ["00_Environment_Setup"])
def test_markdown_images_resolve_relative_to_the_notebook(stem: str) -> None:
    path = _notebook(stem)
    missing = []
    for target in _markdown_images(path):
        if not (path.parent / target).resolve().is_file():
            missing.append(target)
    assert not missing, f"{stem}: unresolved Markdown images -> {missing}"


def test_essential_diagrams_are_not_gitignored() -> None:
    """配布物に含まれること / the essential diagrams are part of the deliverable."""
    referenced = set()
    for path in NOTEBOOK_DIR.rglob("*.ipynb"):
        for target in _markdown_images(path):
            resolved = (path.parent / target).resolve()
            try:
                relative = resolved.relative_to(COURSE_ROOT.resolve()).as_posix()
            except ValueError:
                continue
            if ASSET_DIR_RE.match(relative):
                referenced.add(relative)
    assert referenced, "no diagram is referenced from any notebook"
    ignored = sorted(relative for relative in referenced if _git_ignored(relative))
    assert not ignored, f"these teaching diagrams are excluded from the deliverable: {ignored}"


def test_non_teaching_assets_stay_out_of_the_deliverable() -> None:
    """例外を広げすぎていないこと / the allow rules stayed narrow."""
    for relative in (
        "assets/diagrams/calibration_image.png",
        "assets/diagrams/diagram_classification.png",
        "assets/anomaly_dataset/pvc_sheet/test/good/good_test_0000.png",
    ):
        assert _git_ignored(relative), f"{relative} should stay ignored"


def test_diagram_generator_covers_every_reference() -> None:
    import generate_teaching_diagrams as gtd

    registered = set(gtd.DIAGRAMS)
    referenced = set()
    for path in NOTEBOOK_DIR.rglob("*.ipynb"):
        for target in _markdown_images(path):
            referenced.add(Path(target).name)
    produced = {name for name in referenced if name.startswith("teach_")}
    assert produced <= registered, f"referenced but not generated: {sorted(produced - registered)}"


def test_teaching_diagram_files_exist() -> None:
    import generate_teaching_diagrams as gtd

    missing = [name for name in gtd.DIAGRAMS if not (DIAGRAM_DIR / name).is_file()]
    assert not missing, f"missing diagram files: {missing}. Run generate_teaching_diagrams.py"


def test_diagrams_are_labelled_as_illustrations() -> None:
    """模式図・合成データであることを図の中で明示する / illustrations say so inside the figure."""
    generator = (SCRIPTS / "generate_teaching_diagrams.py").read_text(encoding="utf-8")
    for phrase in ("模式図", "合成", "schematic", "synthetic"):
        assert phrase in generator


def test_every_visual_has_a_purpose_and_a_question() -> None:
    """各図に「気づいてほしいこと」と学習者への問いがあること。"""
    for stem in CONCEPT_NOTEBOOKS:
        path = _notebook(stem)
        notebook = json.loads(path.read_text(encoding="utf-8"))
        for cell in notebook["cells"]:
            if cell["cell_type"] != "markdown":
                continue
            source = "".join(cell["source"])
            if not MD_IMAGE_RE.search(source):
                continue
            assert "気づいてほしいこと" in source, f"{stem}: figure without 'what to notice'"
            assert "What to notice" in source, f"{stem}: figure without the English 'what to notice'"
            assert "考えてみてください / Try to answer" in source, (
                f"{stem}: figure without a learner question"
            )


# ---------------------------------------------------------------------------
# 必須の視覚トピック / the concepts that must be visible without a kernel
# ---------------------------------------------------------------------------

REQUIRED_VISUALS = {
    "Day01_01_Introduction_to_AI": ["teach_train_vs_inference.png"],
    "Day01_02_Pixels_and_Images": ["diagram_pixel_grid.png", "teach_rgb_channels.png",
                                   "teach_downsample_defect.png"],
    "Day01_03_Computer_Vision_Tasks": ["teach_cv_tasks_outputs.png"],
    "Day02_02_Conditions_Loops_Functions": ["teach_condition_branch.png", "teach_loop_trace.png",
                                            "teach_function_io.png"],
    "Day02_03_OpenCV_Image_Processing": ["teach_opencv_pipeline.png", "teach_pixel_to_mm.png"],
    "Day03_01_YOLO_Concepts": ["teach_bbox_coords.png", "teach_iou_rects.png"],
    "Day03_03_YOLO_Experiments": ["teach_confidence_filter.png", "ref_confidence_counts.png",
                                  "teach_resolution_effect.png"],
    "Day04_01_YOLO_Dataset_Annotation": ["teach_yolo_label_fields.png", "teach_split_roles.png"],
    "Day04_02_YOLO_Training": ["teach_epoch_batch.png", "teach_train_val_curves.png",
                               "ref_train_val_curves.png"],
    "Day04_03_YOLO_Evaluation": ["teach_object_level_matching.png",
                                 "teach_image_level_confusion.png",
                                 "ref_detections_label_vs_pred.png"],
    "Day05_01_Anomaly_Detection_Concepts": ["teach_patch_neighbour.png"],
    "Day05_02_PatchCore_Training": ["ref_anomaly_panels.png"],
    "Day05_03_YOLO_vs_PatchCore": ["ref_score_distribution.png", "ref_comparison_5col.png"],
}


@pytest.mark.parametrize("stem", sorted(REQUIRED_VISUALS))
def test_required_visual_topics_are_visible(stem: str) -> None:
    images = {Path(target).name for target in _markdown_images(_notebook(stem))}
    missing = [name for name in REQUIRED_VISUALS[stem] if name not in images]
    assert not missing, f"{stem}: these figures are not visible before execution -> {missing}"


def test_reference_outputs_are_tracked_and_labelled() -> None:
    """実際の結果から作った図が配布物に入り、図の中で「参考出力」と名乗っていること。"""
    folder = COURSE_ROOT / "assets" / "reference_outputs"
    referenced = set()
    for path in NOTEBOOK_DIR.rglob("*.ipynb"):
        for target in _markdown_images(path):
            if "reference_outputs" in target:
                referenced.add(Path(target).name)
    assert referenced, "no reference output is referenced from any notebook"
    missing = sorted(name for name in referenced if not (folder / name).is_file())
    assert not missing, f"referenced but missing: {missing}"
    ignored = sorted(name for name in referenced
                     if _git_ignored(f"assets/reference_outputs/{name}"))
    assert not ignored, f"reference outputs excluded from the deliverable: {ignored}"


def test_reference_generator_states_its_sources() -> None:
    generator = (SCRIPTS / "generate_reference_outputs.py").read_text(encoding="utf-8")
    for phrase in ("参考出力", "Reference output", "MissingSource", "results.csv"):
        assert phrase in generator, f"reference generator does not mention {phrase!r}"


def test_figure_insertion_is_idempotent() -> None:
    """差し込みスクリプトを 2 回動かしても増えないこと（ノートブックを直接数えて確認）。"""
    import json as _json

    import insert_lesson_figures as ilf

    for entry in ilf.FIGURES:
        path = ilf._notebook(entry["notebook"])
        notebook = _json.loads(path.read_text(encoding="utf-8"))
        count = sum(1 for cell in notebook["cells"]
                    if cell["cell_type"] == "markdown"
                    and entry["image"] in "".join(cell["source"]))
        assert count == 1, f"{path.name}: {entry['image']} appears {count} times"


def test_every_code_only_diagram_has_a_static_equivalent() -> None:
    """コードでしか出ない図にも、実行前に見える静的図があること（重複した説明を避けつつ確認）。"""
    import json as _json

    code_images = {}
    for path in NOTEBOOK_DIR.rglob("*.ipynb"):
        notebook = _json.loads(path.read_text(encoding="utf-8"))
        for cell in notebook["cells"]:
            if cell["cell_type"] != "code":
                continue
            for name in re.findall(r"diagram_[a-z_]+\.png", "".join(cell["source"])):
                code_images.setdefault(path.stem, set()).add(name)

    static = {Path(target).name for path in NOTEBOOK_DIR.rglob("*.ipynb")
              for target in _markdown_images(path)}
    # コードで表示する図は、同じノートブックか同じ日の静的図で代替できること
    coverage = {
        "Day01_02_Pixels_and_Images": "diagram_pixel_grid.png",
        "Day01_03_Computer_Vision_Tasks": "teach_cv_tasks_outputs.png",
        "Day02_03_OpenCV_Image_Processing": "teach_pixel_to_mm.png",
        "Day03_01_YOLO_Concepts": "teach_yolo_label_fields.png",
        "Day04_01_YOLO_Dataset_Annotation": "teach_split_roles.png",
        "Day05_01_Anomaly_Detection_Concepts": "teach_patch_neighbour.png",
        "Day05_03_YOLO_vs_PatchCore": "ref_comparison_5col.png",
        "Day02_02_Conditions_Loops_Functions": "teach_condition_branch.png",
    }
    for stem in code_images:
        if stem not in coverage:
            continue
        assert coverage[stem] in static, (
            f"{stem}: code shows a diagram, but {coverage[stem]} is not visible statically")
