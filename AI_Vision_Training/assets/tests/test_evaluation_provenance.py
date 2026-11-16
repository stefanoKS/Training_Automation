"""比較と較正のテスト / Comparison and calibration tests.

Day 5 Notebook 03 は、かつて「評価に使うデータそのもの」から PatchCore のしきい値を決めていました。
このテストは、その方法に戻っていないことと、新しい較正の手順が実際に正しく動くことを確かめます。
Day 5 Notebook 03 used to choose the PatchCore threshold from the very dataset it then evaluated.
These tests make sure the old method cannot come back, and that the new calibration actually works.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

COURSE_ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK_DIR = COURSE_ROOT / "notebooks"
sys.path.insert(0, str(COURSE_ROOT / "assets" / "scripts"))
from course_notebooks import course_notebooks  # noqa: E402


def _notebook_text(stem: str) -> str:
    path, = course_notebooks(NOTEBOOK_DIR, f"{stem}.ipynb")
    notebook = json.loads(path.read_text(encoding="utf-8"))
    return "\n".join("".join(cell["source"]) for cell in notebook["cells"])


def _cell_sources(stem: str) -> list[str]:
    path, = course_notebooks(NOTEBOOK_DIR, f"{stem}.ipynb")
    notebook = json.loads(path.read_text(encoding="utf-8"))
    return ["".join(cell["source"]) for cell in notebook["cells"]
            if cell["cell_type"] == "code"]


@pytest.fixture(scope="module")
def comparison_source() -> str:
    return _notebook_text("Day05_03_YOLO_vs_PatchCore")


# ---------------------------------------------------------------------------
# 旧方式に戻っていないこと / the old method cannot come back
# ---------------------------------------------------------------------------


def test_no_threshold_from_max_normal_and_min_abnormal(comparison_source: str) -> None:
    forbidden = [
        "normal_scores.max() + abnormal_scores.min()",
        "正常の最大と異常の最小",
        "between the max normal and min abnormal score",
    ]
    for phrase in forbidden:
        assert phrase not in comparison_source, f"the test-set threshold formula is back: {phrase}"


def test_thresholds_are_selected_on_the_calibration_partition(comparison_source: str) -> None:
    assert "calibration_frame" in comparison_source
    assert "choose_threshold(" in comparison_source
    assert "MAX_FALSE_REJECT_RATE" in comparison_source
    assert "selected_on" in comparison_source


def test_test_partition_is_only_scored_once_and_by_name(comparison_source: str) -> None:
    assert 'test_frame = combined[combined["partition"] == "test"]' in comparison_source
    assert "comparison_test_results.json" in comparison_source


def test_split_manifest_and_provenance_are_required(comparison_source: str) -> None:
    assert "split_manifest.json" in comparison_source
    assert "REQUIRED_SCHEMA" in comparison_source
    assert "schema_version" in comparison_source
    assert "score_convention" in comparison_source


def test_missing_results_are_reported_not_silently_dropped(comparison_source: str) -> None:
    assert "missing_yolo" in comparison_source
    assert "missing_patchcore" in comparison_source
    assert "excluded_no_yolo" in comparison_source


def test_old_results_are_marked_superseded(comparison_source: str) -> None:
    assert '"superseded"' in comparison_source
    assert "yolo_vs_patchcore.csv" in comparison_source


def test_patchcore_fits_on_normal_images_only() -> None:
    training_source = _notebook_text("Day05_02_PatchCore_Training")
    assert 'normal_dir=layout["normal_dir"]' in training_source
    assert "train に正常以外の画像が入っています" in training_source
    assert "patchcore_train" in training_source


def test_split_manifest_records_what_matters() -> None:
    training_source = _notebook_text("Day05_02_PatchCore_Training")
    for key in ('"partitions"', '"overlap_check"', '"score_convention"', '"model"',
                '"postprocessor"', '"yolo_training_overlap"'):
        assert key in training_source, f"the split manifest does not record {key}"


def test_normalisation_statistics_are_not_fitted_on_test() -> None:
    training_source = _notebook_text("Day05_02_PatchCore_Training")
    assert "enable_normalization" in training_source
    assert "CALIBRATION (validation) partition" in training_source


# ---------------------------------------------------------------------------
# 新しい較正ロジックが動くこと / the new calibration logic really works
# ---------------------------------------------------------------------------


def _load_calibration_namespace() -> dict:
    """較正セルを実行して、関数だけを取り出す / execute the calibration cell."""
    source = next(
        (text for text in _cell_sources("Day05_03_YOLO_vs_PatchCore")
         if "def choose_threshold(" in text),
        None,
    )
    assert source is not None, "the calibration cell is missing"

    namespace: dict = {"pd": pd, "np": np}
    # 依存する値だけを用意する / provide only what the cell needs before the helper functions
    head = source.split("yolo_candidates =")[0]
    namespace["yolo_data"] = {"min_inference_conf": 0.01}
    exec(compile(head, "<calibration>", "exec"), namespace)  # noqa: S102 - course code fixture
    return namespace


def test_choose_threshold_maximises_recall_within_the_false_reject_cap() -> None:
    namespace = _load_calibration_namespace()
    choose = namespace["choose_threshold"]
    counts = namespace["counts"]

    truth = pd.Series([True] * 6 + [False] * 4)
    scores = pd.Series([0.90, 0.80, 0.70, 0.60, 0.30, 0.20] + [0.15, 0.40, 0.10, 0.05])
    best = choose([i / 100 for i in range(0, 101)], scores, truth,
                  lambda values, threshold: values >= threshold)

    assert best is not None
    # 正常 4 枚で誤報率 10% なので FP は 0 枚まで / 4 normals at 10% allows zero false alarms
    assert best["table"]["FP"] == 0
    # 0.40（正常の最大）より上で、0.60（4 番目の異常）までは 4 件を検出できる
    # above 0.40 (highest normal) and up to 0.60 (fourth abnormal) four defects stay detected
    assert best["table"]["TP"] == 4
    assert 0.40 < best["threshold"] <= 0.60
    assert counts(pd.Series([True, False]), pd.Series([True, True]))["FN"] == 1


def test_choose_threshold_returns_none_when_the_objective_cannot_be_evaluated() -> None:
    """正常品が 1 枚も無ければ目的関数を評価できない / a false-reject rate needs normal images."""
    namespace = _load_calibration_namespace()
    choose = namespace["choose_threshold"]
    truth = pd.Series([True, True, True])
    scores = pd.Series([0.9, 0.5, 0.1])
    assert choose([i / 100 for i in range(0, 101)], scores, truth,
                  lambda values, threshold: values >= threshold) is None


def test_partitions_in_the_schedule_and_manifest_are_disjoint_by_construction() -> None:
    """Day05_02 は分割の重なりを assert している / the notebook asserts disjoint partitions."""
    training_source = _notebook_text("Day05_02_PatchCore_Training")
    assert "assert not shared" in training_source
    assert "partitions overlap" in training_source


def test_schedule_has_a_day5_calibration_slot() -> None:
    syllabus = (COURSE_ROOT / "COURSE_SYLLABUS.md").read_text(encoding="utf-8")
    assert "Day05_03" in syllabus
    assert re.search(r"Day05_03.*Part 4", syllabus), "Day 5 timetable does not cover Part 4"


def test_prefreeze_toy_is_calculated_without_any_saved_data(tmp_path, monkeypatch) -> None:
    import generate_reference_outputs as figures

    def forbidden(*args, **kwargs):
        pytest.fail("the synthetic toy attempted to read inference/dataset evidence")

    for helper in ("_read_scores", "_saved_scores", "_load_map", "_dataset_image"):
        monkeypatch.setattr(figures, helper, forbidden)
    distances, smoothed, raw, transformed = figures.toy_numeric_map()
    assert distances.shape == smoothed.shape == (5, 5)
    assert raw == pytest.approx(4.8)
    assert smoothed.max() == pytest.approx(2)
    assert transformed == pytest.approx(.6)
    assert raw != smoothed.max() and transformed >= .5
    for value in (raw, smoothed.max(), transformed):
        assert f"{value:.3f}" in _notebook_text("Day05_02_PatchCore_Training")
    family = figures.configure_matplotlib()
    with figures.plt.rc_context({"font.family": [family, "DejaVu Sans"]}):
        first = figures.teach_numeric_map_toy(tmp_path, tmp_path).read_bytes()
        second = figures.teach_numeric_map_toy(tmp_path, tmp_path).read_bytes()
    assert first == second


@pytest.mark.parametrize("name", ["ref_anomaly_panels", "ref_comparison_5col"])
def test_reference_generation_preserves_existing_test_archive_bytes(name, tmp_path) -> None:
    import generate_reference_outputs as figures

    archive = tmp_path / f"{name}.png"
    archive.write_bytes(b"historical evidence, never overwrite")
    for _ in range(2):
        assert getattr(figures, name)(tmp_path, tmp_path) == archive
        assert archive.read_bytes() == b"historical evidence, never overwrite"


def test_score_distribution_uses_only_calibration_even_when_test_rows_exist(tmp_path, monkeypatch) -> None:
    import generate_reference_outputs as figures

    monkeypatch.setattr(figures, "_read_scores", lambda root: [
        {"partition": "calibration", "score": ".2", "truly_abnormal": "False"},
        {"partition": "calibration", "score": ".7", "truly_abnormal": "True"},
        {"partition": "test", "score": ".123456", "truly_abnormal": "False"},
        {"partition": "test", "score": ".987654", "truly_abnormal": "True"},
    ])
    plotted = []

    def capture(fig, path):
        plotted.extend(float(point[0]) for artist in fig.axes[0].collections
                       for point in artist.get_offsets())
        figures.plt.close(fig)
        return path

    monkeypatch.setattr(figures, "_save", capture)
    figures.ref_score_distribution(tmp_path, tmp_path)
    assert sorted(plotted) == [.2, .7]


@pytest.mark.parametrize("role", ["calibration", "test"])
def test_archived_panel_rejects_non_test_source_or_missing_matching_score(role, tmp_path, monkeypatch) -> None:
    import generate_reference_outputs as figures

    maps = tmp_path / "submissions" / "day05" / "maps"
    maps.mkdir(parents=True)
    (maps / "black_spot_0000_map.npz").touch()
    monkeypatch.setattr(figures, "_load_map", lambda *args: {"image": f"{role}/fixture.png"})
    monkeypatch.setattr(figures, "_dataset_image", lambda *args: np.zeros((2, 2, 3)))
    monkeypatch.setattr(figures, "_saved_scores", lambda *args: {})
    with pytest.raises(figures.MissingSource, match="TEST"):
        figures.ref_anomaly_panels(tmp_path, tmp_path)


def test_all_day5_static_images_have_explicit_provenance_and_only_one_prefreeze_reference() -> None:
    manifest = (COURSE_ROOT / "docs" / "visual_figure_manifest.md").read_text(encoding="utf-8")
    provenance = manifest.split("### Day 5 follow-up:", 1)[1].split("## Existing source-checked", 1)[0]
    reference_images = set()
    for path in course_notebooks(NOTEBOOK_DIR, "Day05_*.ipynb"):
        notebook = json.loads(path.read_text(encoding="utf-8"))
        for cell in notebook["cells"]:
            if cell.get("id") == "clarity-freeze-record":
                break
            source = "".join(cell["source"])
            for name in re.findall(r'"(diagram_[^"]+\.png)"', source):
                assert f"`{name}`" in provenance, f"unclassified runtime diagram: {name}"
            for target in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", source):
                name = Path(target).name
                assert f"`{name}`" in provenance, f"unclassified learner figure: {name}"
                assert (path.parent / target).resolve().is_file()
                if name.startswith("ref_"):
                    reference_images.add(name)
    assert reference_images == {"ref_score_distribution.png"}
    archive = (COURSE_ROOT / "docs" / "instructor" / "day05_after_freeze_archive.md").read_text(encoding="utf-8")
    for target in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", archive):
        assert (COURSE_ROOT / "docs" / "instructor" / target).resolve().is_file()
    for evidence in ("21.439", "21.762", "1.000", "test/black_spot/black_spot_0000.png",
                     "ref_anomaly_panels.png", "ref_comparison_5col.png"):
        assert evidence in archive
