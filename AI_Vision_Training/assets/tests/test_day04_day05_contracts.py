"""Day 4 → Day 5 の契約を、本物の producer / consumer セルで通す / the Day 4 → Day 5 contracts.

このテストはノートブックのセルをそのまま実行して、ファイル契約が成立するかを確かめます。差し替える
のはモデルとエンジンだけです。分割・身元・封印・比較のロジックはノートブックと共有ヘルパーの実物を
使います。

The test runs the real notebook cells; only the model and the engine are small duck-typed stand-ins.
Nothing here re-implements the split, the identity, the seal or the comparison.

The path exercised:

    Day04_03  f7f5833b → 552d3581              split first, calibration scores only
    Day05_02  1c4cd018                         calibration payload + post-calibration record
    Day05_03  39ee7a27 → ae192ae8 → d26eb085 → cccf0ff7 → 935ef5b9 → clarity-freeze-record
    Day04_03  shared-sealed-test               sealed YOLO test scores, after the freeze
    Day05_02  clarity-sealed-test-scoring      sealed PatchCore test scores, after the freeze
    Day05_03  clarity-load-sealed-test → 9747ac10
"""

from __future__ import annotations

import json
import sys
import types
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

torch = pytest.importorskip("torch")

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "assets" / "helpers"))
sys.path.insert(0, str(ROOT / "assets" / "scripts"))

import experiment_identity as identity  # noqa: E402
import shared_set_split  # noqa: E402

NOTEBOOKS = {
    "Day04_03": ROOT / "notebooks" / "Day04_YOLO_Training" / "Day04_03_YOLO_Evaluation.ipynb",
    "Day05_02": ROOT / "notebooks" / "Day05_PatchCore" / "Day05_02_PatchCore_Training.ipynb",
    "Day05_03": ROOT / "notebooks" / "Day05_PatchCore" / "Day05_03_YOLO_vs_PatchCore.ipynb",
}


def cell_source(stem: str, cell_id: str) -> str:
    notebook = json.loads(NOTEBOOKS[stem].read_text(encoding="utf-8"))
    for cell in notebook["cells"]:
        if cell.get("id") == cell_id:
            return "".join(cell["source"])
    raise AssertionError(f"{stem}: no cell {cell_id}")


def run_cell(namespace: dict, stem: str, cell_id: str,
             replacements: tuple[tuple[str, str], ...] = ()) -> None:
    source = cell_source(stem, cell_id)
    for old, new in replacements:
        assert source.count(old) == 1, (cell_id, old)
        source = source.replace(old, new)
    exec(compile(source, f"<{stem}:{cell_id}>", "exec"), namespace)  # noqa: S102


# ---------------------------------------------------------------------------
# stand-ins: only the model and the engine are synthetic
# ---------------------------------------------------------------------------


class _Tensor:
    """``detach().cpu().numpy()`` and ``tolist()`` are all the notebook cells use."""

    def __init__(self, values):
        self.values = np.asarray(values)

    def detach(self):
        return self

    def cpu(self):
        return self

    def numpy(self):
        return self.values

    def tolist(self):
        return self.values.tolist()


class _Boxes:
    def __init__(self, confidences):
        self.conf = _Tensor(confidences)
        self.cls = _Tensor([0] * len(confidences))

    def __len__(self):
        return len(self.conf.values)


class _Prediction:
    def __init__(self, confidences):
        self.boxes = _Boxes(confidences)
        self.names = {0: "defect"}


class _FakeYolo:
    """Abnormal images get a detection, normal images get none."""

    def __init__(self):
        self.calls = []

    def predict(self, source, conf, imgsz, verbose):
        path = Path(source)
        self.calls.append(path)
        abnormal = path.parent.name != "good"
        return [_Prediction([0.92, 0.31] if abnormal else [])]


class _Batch:
    def __init__(self, paths, scores, truths):
        self.image_path = [str(path) for path in paths]
        self.pred_score = _Tensor(scores)
        self.pred_label = _Tensor([score >= 0.5 for score in scores])
        self.gt_label = _Tensor(truths)


class _FakeEngine:
    def __init__(self, scores, truths, dataset_root):
        self.scores = scores
        self.truths = truths
        self.dataset_root = dataset_root

    def predict(self, model, dataloaders):
        names = dataloaders
        return [_Batch([self.dataset_root / name for name in names],
                       [self.scores[Path(name).name] for name in names],
                       [self.truths[Path(name).name] for name in names])]


class _FakeDataModule:
    def __init__(self, names):
        self.names = names

    def test_dataloader(self):
        return self.names


class _Inner:
    def __init__(self, tensor):
        self.tensor = tensor
        self.memory_bank = tensor

    def state_dict(self):
        return {"memory_bank": self.tensor}


class _Patchcore:
    """A real torch tensor behind the two attributes ``experiment_identity`` reads."""

    def __init__(self):
        self.model = _Inner(torch.arange(6, dtype=torch.float32))
        self.post_processor = types.SimpleNamespace(
            enable_normalization=True, image_min=0.1, image_max=0.9,
            pixel_min=0.2, pixel_max=0.8, adaptive_threshold=0.5)


# ---------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------


def _write_png(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"\x89PNG fixture")


def _dataset(course_root: Path) -> Path:
    """Three normal and four abnormal comparison images, plus four training images."""
    root = course_root / "assets" / "anomaly_dataset" / "pvc_sheet"
    for index in range(4):
        _write_png(root / "train" / "good" / f"train_{index:02d}.png")
    for index in range(3):
        _write_png(root / "test" / "good" / f"good_{index:02d}.png")
    for folder in ("black_spot", "scratch"):
        for index in range(2):
            _write_png(root / "test" / folder / f"{folder}_{index:04d}.png")
    layout = {
        "name": "pvc_sheet",
        "normal_dir": "train/good",
        "normal_test_dir": "test/good",
        "abnormal_dir": ["test/black_spot", "test/scratch"],
        "mask_dir": ["ground_truth/black_spot", "ground_truth/scratch"],
        "image_size": 256,
        "seed": 2026,
        "counts": {"train_good": 4, "test_good": 3},
    }
    (root / "dataset_layout.json").write_text(json.dumps(layout), encoding="utf-8")
    return root


def _scores(split: dict) -> tuple[dict, dict]:
    scores, truths = {}, {}
    for partition in ("calibration", "test"):
        for name in split["partitions"][partition]:
            normal = Path(name).parent.name == "good"
            scores[Path(name).name] = 0.12 if normal else 0.86
            truths[Path(name).name] = not normal
    return scores, truths


def _manifest(dataset_root: Path, split: dict) -> dict:
    """The record Notebook 02 writes; the split verification itself runs here."""
    manifest = {
        "schema_version": 3,
        "dataset_root": str(dataset_root.resolve()),
        "dataset_name": split["dataset_name"],
        "dataset_seed": split["dataset_seed"],
        "image_size": split["image_size"],
        "split": {"library": "fixture", "val_split_mode": "from_test", "val_split_ratio": 0.5},
        "counts": split["counts"],
        "partitions": split["partitions"],
        "overlap_check": split["overlap_check"],
        "shared_split": {"path": "submissions/day04/shared_set_split.json", "schema_version": 1,
                         "verified": True,
                         "partitions_digest": shared_set_split.digest(split["partitions"])},
        "model": {"class": "Patchcore", "backbone": "resnet18"},
        "postprocessor": {"normalisation_enabled": True},
        "score_convention": "fixture convention",
    }
    assert shared_set_split.matches(manifest["partitions"], split["partitions"]) == []
    return manifest


def _pipeline(tmp_path: Path) -> dict:
    """Run the real cells up to the freeze; return everything the later steps need."""
    course_root = tmp_path / "course"
    dataset_root = _dataset(course_root)
    layout = json.loads((dataset_root / "dataset_layout.json").read_text(encoding="utf-8"))
    split = shared_set_split.build(dataset_root, layout)
    day05 = course_root / "submissions" / "day05"
    day05.mkdir(parents=True)
    best_weights = course_root / "training_results" / "day04" / "run" / "weights" / "best.pt"
    best_weights.parent.mkdir(parents=True)

    common = {"COURSE_ROOT": course_root, "ASSETS": course_root / "assets",
              "model": _FakeYolo(), "best_weights": best_weights,
              "shared_set_split": shared_set_split}

    # step 1 — the split is decided before any inference
    run_cell(common, "Day04_03", "f7f5833b")
    run_cell(common, "Day04_03", "552d3581")

    # step 2 — the manifest, then the calibration producer
    patchcore = _Patchcore()
    fitted = identity.fitted_state(patchcore)
    postprocessor = identity.postprocessor_state(patchcore)
    manifest = _manifest(dataset_root, split)
    manifest["experiment"] = identity.base_identity(manifest, fitted, postprocessor)
    (day05 / "split_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (day05 / "patchcore_fitted_state.json").write_text(json.dumps(
        {"schema_version": 1, "experiment": manifest["experiment"], "fitted": fitted,
         "postprocessor": postprocessor}), encoding="utf-8")

    scores, truths = _scores(split)
    calibration = split["partitions"]["calibration"]
    producer = dict(common)
    producer.update({
        "manifest": manifest,
        "model": patchcore,
        "FITTED_STATE": fitted,
        "predictions_by_partition": {"calibration": [_Batch(
            [dataset_root / name for name in calibration],
            [scores[Path(name).name] for name in calibration],
            [truths[Path(name).name] for name in calibration])]},
        "submission_dir": day05,
        "dataset_root": dataset_root,
        "pd": pd,
        "np": np,
        "Path": Path,
    })
    run_cell(producer, "Day05_02", "1c4cd018")

    # step 3 — read, pair, choose thresholds on calibration and freeze
    consumer = dict(common)
    consumer.update({"Path": Path, "json": json})
    run_cell(consumer, "Day05_03", "39ee7a27")
    run_cell(consumer, "Day05_03", "ae192ae8")
    run_cell(consumer, "Day05_03", "d26eb085")
    run_cell(consumer, "Day05_03", "cccf0ff7")
    run_cell(consumer, "Day05_03", "935ef5b9")
    consumer.update({"FREEZE_DECLARATION": "frozen before test; no retuning",
                     "TEST_ALREADY_SEEN": False})
    run_cell(consumer, "Day05_03", "clarity-freeze-record", (
        ('FREEZE_DECLARATION = ""',
         'FREEZE_DECLARATION = "frozen before test; no retuning"'),
        ("TEST_ALREADY_SEEN = True", "TEST_ALREADY_SEEN = False"),
    ))

    return {"course_root": course_root, "dataset_root": dataset_root, "split": split,
            "day05": day05, "common": common, "consumer": consumer, "manifest": manifest,
            "patchcore": patchcore, "scores": scores, "truths": truths}


def _seal_test_scores(state: dict, save_map) -> None:
    sealed_cell = dict(state["common"])
    sealed_cell.update({
        "manifest": state["manifest"],
        "datamodule": _FakeDataModule(state["split"]["partitions"]["test"]),
        "engine": _FakeEngine(state["scores"], state["truths"], state["dataset_root"]),
        "save_map": save_map,
        "dataset_root": state["dataset_root"],
        "model": state["patchcore"],
        "json": json,
        "Path": Path,
    })
    run_cell(sealed_cell, "Day05_02", "clarity-sealed-test-scoring")


# ---------------------------------------------------------------------------
# GROUP A — split integrity
# ---------------------------------------------------------------------------


def test_the_shared_split_is_deterministic_and_label_aware() -> None:
    dataset_root = ROOT / "assets" / "anomaly_dataset" / "pvc_sheet"
    layout = json.loads((dataset_root / "dataset_layout.json").read_text(encoding="utf-8"))
    first = shared_set_split.build(dataset_root, layout)
    again = shared_set_split.build(dataset_root, layout)

    assert first["partitions"] == again["partitions"]
    assert first["counts"] == {"patchcore_train": 32, "calibration": 26, "test": 26}
    for files in first["partitions"].values():
        assert len(files) == len(set(files))
    assert not set(first["partitions"]["calibration"]) & set(first["partitions"]["test"])
    assert not set(first["partitions"]["patchcore_train"]) & set(first["partitions"]["test"])
    assert first["split"]["val_split_ratio"] == 0.5 and first["split"]["seed"] == 2026


def test_the_archived_test_images_land_in_the_test_partition() -> None:
    """The archived run recorded both images as TEST; the reproduced split must agree."""
    dataset_root = ROOT / "assets" / "anomaly_dataset" / "pvc_sheet"
    layout = json.loads((dataset_root / "dataset_layout.json").read_text(encoding="utf-8"))
    lookup = shared_set_split.partition_lookup(
        shared_set_split.build(dataset_root, layout)["partitions"])
    assert lookup["black_spot/black_spot_0000.png"] == "test"
    assert lookup["streak/streak_0005.png"] == "test"


# ---------------------------------------------------------------------------
# GROUP B — the Day 4 → Day 5 file contracts, through the real cells
# ---------------------------------------------------------------------------


def test_the_prefreeze_export_holds_calibration_rows_only(tmp_path, capsys) -> None:
    course_root = tmp_path / "course"
    dataset_root = _dataset(course_root)
    namespace = {"COURSE_ROOT": course_root, "ASSETS": course_root / "assets",
                 "model": _FakeYolo(), "shared_set_split": shared_set_split,
                 "best_weights": course_root / "training_results/day04/run/weights/best.pt"}

    run_cell(namespace, "Day04_03", "f7f5833b")
    run_cell(namespace, "Day04_03", "552d3581")
    printed = capsys.readouterr().out

    split = json.loads((course_root / "submissions" / "day04"
                        / "shared_set_split.json").read_text(encoding="utf-8"))
    payload = json.loads((course_root / "submissions" / "day04"
                          / "yolo_predictions_on_shared_set.json").read_text(encoding="utf-8"))
    calibration = set(split["partitions"]["calibration"])
    test = set(split["partitions"]["test"])
    scored = {row["image"] for row in payload["images"]}

    assert split["counts"] == namespace["shared_split"]["counts"]
    assert payload["schema_version"] == 3
    assert payload["scored_partitions"] == ["calibration"]
    assert payload["test_scored"] is False
    assert payload["split_partitions_digest"] == shared_set_split.digest(split["partitions"])
    assert scored == calibration and not scored & test
    # no test image was ever seen by the model before the freeze
    assert {path.relative_to(dataset_root).as_posix() for path in namespace["model"].calls} == calibration
    assert "calibration only" in printed


def test_end_to_end_from_the_split_to_the_final_comparison(tmp_path) -> None:
    state = _pipeline(tmp_path)
    day05, split, course_root = state["day05"], state["split"], state["course_root"]
    freeze = json.loads((day05 / "comparison_freeze_record.json").read_text(encoding="utf-8"))
    assert freeze["assessment_role"] == "declared_untouched_test"

    # step 4 — Day 4 seals the YOLO test scores
    sealer = dict(state["common"])
    sealer.update({"json": json})
    run_cell(sealer, "Day04_03", "shared-sealed-test")
    yolo_seal = json.loads((course_root / "submissions" / "day04"
                            / "yolo_predictions_sealed_test.json").read_text(encoding="utf-8"))
    assert {row["image"] for row in yolo_seal["images"]} == set(split["partitions"]["test"])

    # step 5 — Notebook 02 seals the PatchCore test scores
    _seal_test_scores(state, lambda batch, index, path: path.write_bytes(b"map"))
    assert (day05 / "patchcore_test_predictions.json").is_file()
    assert not (day05 / "maps_pending").exists()
    assert len(list((day05 / "maps").glob("*_map.npz"))) == len(split["partitions"]["test"])

    # a second run reuses the seal instead of scoring test again
    before = (day05 / "patchcore_test_predictions.json").read_bytes()
    _seal_test_scores(state, lambda batch, index, path: pytest.fail("test must not be re-scored"))
    assert (day05 / "patchcore_test_predictions.json").read_bytes() == before

    # step 6 — Notebook 03 pairs the two seals by image ID
    final = dict(state["consumer"])
    final.update({"pd": pd, "Path": Path, "json": json})
    run_cell(final, "Day05_03", "clarity-load-sealed-test")
    test_frame = final["test_frame"]
    expected_ids = {identity.normalise_image_id(name) for name in split["partitions"]["test"]}
    assert set(test_frame.index) == expected_ids
    assert len(test_frame) == len(expected_ids)
    assert set(final["sealed_frame"].index) == set(final["yolo_test_frame"].index) == expected_ids

    run_cell(final, "Day05_03", "9747ac10")
    results = json.loads((day05 / "comparison_test_results.json").read_text(encoding="utf-8"))
    assert results["assessment_role"] == "declared_untouched_test"
    assert results["assessment_is_final"] is True
    for method in results["test"]:
        assert method["n_images"] == len(test_frame)
        assert method["TP"] + method["FP"] + method["FN"] + method["TN"] == len(test_frame)
    csv = pd.read_csv(day05 / "comparison_test_results.csv")
    assert set(csv["assessment_role"]) == {"declared_untouched_test"}
    assert list(csv["n_images"]) == [len(test_frame)] * len(csv)


def test_relabelling_the_role_after_the_seal_is_rejected(tmp_path) -> None:
    state = _pipeline(tmp_path)
    day05 = state["day05"]
    sealer = dict(state["common"])
    sealer.update({"json": json})
    run_cell(sealer, "Day04_03", "shared-sealed-test")
    _seal_test_scores(state, lambda batch, index, path: path.write_bytes(b"map"))

    freeze = json.loads((day05 / "comparison_freeze_record.json").read_text(encoding="utf-8"))
    freeze["assessment_role"] = "illustrative_reused_data"
    (day05 / "comparison_freeze_record.json").write_text(json.dumps(freeze), encoding="utf-8")

    reader = {"COURSE_ROOT": state["course_root"], "manifest": state["manifest"],
              "freeze_record": freeze, "pd": pd, "Path": Path, "json": json}
    with pytest.raises(identity.ProvenanceError, match="assessment role differs"):
        run_cell(reader, "Day05_03", "clarity-load-sealed-test")


# ---------------------------------------------------------------------------
# GROUP D / E — the freeze gate and publication failures
# ---------------------------------------------------------------------------


def test_a_partial_calibration_cannot_be_frozen(tmp_path) -> None:
    course_root = tmp_path / "course"
    dataset_root = _dataset(course_root)
    layout = json.loads((dataset_root / "dataset_layout.json").read_text(encoding="utf-8"))
    split = shared_set_split.build(dataset_root, layout)
    (course_root / "submissions" / "day05").mkdir(parents=True)
    namespace = {
        "COURSE_ROOT": course_root,
        "manifest": {"partitions": split["partitions"]},
        "yolo_frame": pd.DataFrame({"image": [], "partition": [], "truly_abnormal": []}),
        "patchcore_frame": pd.DataFrame({"image": [], "partition": [], "truly_abnormal": []}),
        "pd": pd, "Path": Path,
        "FREEZE_DECLARATION": "frozen before test",
        "TEST_ALREADY_SEEN": False,
        "comparison_is_final": False,
        "missing_yolo": ["good/good_00.png"],
        "missing_patchcore": [],
    }
    with pytest.raises(RuntimeError, match="calibration partition is incomplete"):
        run_cell(namespace, "Day05_03", "clarity-freeze-record")
    assert not (course_root / "submissions" / "day05"
                / "comparison_freeze_record.json").exists()


def test_a_rejected_map_publish_leaves_no_seal_behind(tmp_path) -> None:
    """If the numeric maps cannot pair one-to-one with the images, nothing is published."""
    state = _pipeline(tmp_path)
    day05 = state["day05"]

    def collide(batch, index, path):
        (path.parent / "same_map.npz").write_bytes(b"collision")

    with pytest.raises(identity.ProvenanceError, match="do not pair one-to-one"):
        _seal_test_scores(state, collide)
    assert not (day05 / "patchcore_test_predictions.json").exists()
    maps = day05 / "maps"
    assert not maps.is_dir() or not list(maps.glob("*.npz"))


def test_the_archive_gate_cannot_relabel_a_sealed_role(tmp_path) -> None:
    """Opening the archive may record a downgrade, but never rewrite a sealed role."""
    course_root = tmp_path / "course"
    docs = course_root / "docs" / "instructor"
    docs.mkdir(parents=True)
    (docs / "day05_after_freeze_archive.md").write_text("# archive", encoding="utf-8")
    day05 = course_root / "submissions" / "day05"
    day05.mkdir(parents=True)
    freeze_path = day05 / "comparison_freeze_record.json"
    freeze = {"declaration": "frozen before test", "assessment_role": "declared_untouched_test",
              "test_already_seen": False}
    freeze_path.write_text(json.dumps(freeze), encoding="utf-8")

    show = (("SHOW_ARCHIVED_TEST = False", "SHOW_ARCHIVED_TEST = True"),)

    # no seal yet: the downgrade is recorded, with its reason
    namespace = {"COURSE_ROOT": course_root, "comparison": None,
                 "freeze_record": dict(freeze), "freeze_path": freeze_path, "json": json}
    run_cell(namespace, "Day05_03", "clarity-archive-gate", show)
    recorded = json.loads(freeze_path.read_text(encoding="utf-8"))
    assert recorded["assessment_role"] == "illustrative_reused_data"
    assert "assessment_role_downgraded" in recorded

    # a seal exists: the record must be left exactly as it is
    freeze_path.write_text(json.dumps(freeze), encoding="utf-8")
    (day05 / "patchcore_test_predictions.json").write_text("{}", encoding="utf-8")
    namespace = {"COURSE_ROOT": course_root, "comparison": None,
                 "freeze_record": dict(freeze), "freeze_path": freeze_path, "json": json}
    run_cell(namespace, "Day05_03", "clarity-archive-gate", show)
    assert json.loads(freeze_path.read_text(encoding="utf-8"))["assessment_role"] == (
        "declared_untouched_test")


def test_the_repository_holds_no_generated_comparison_artifacts() -> None:
    """The work itself must never ship a fabricated comparison result."""
    generated = {path.name for path in (ROOT / "submissions").rglob("*.json")}
    assert "comparison_test_results.json" not in generated
    assert "patchcore_test_predictions.json" not in generated
    assert (ROOT / "assets" / "reference_outputs" / "ref_comparison_5col.png").is_file()
