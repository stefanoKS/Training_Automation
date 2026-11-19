"""Genuine Day 4 → Day 5 CPU run with separate YOLO and anomalib interpreters.

Set ``DAY05_YOLO_PYTHON`` to the YOLO interpreter (absolute path), then run:

    .venv-anomalib\\Scripts\\python.exe -m pytest assets/tests/test_day05_anomalib27_integration.py

Missing opt-in or anomalib 2.7.0 means BLOCKED, not PASS. A locally initialized YOLO
checkpoint and a non-pretrained PatchCore backbone avoid downloads. This verifies
the artifact and scoring contracts, not the accuracy of either model.
"""

from __future__ import annotations

import json
import math
import os
import shutil
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "assets" / "helpers"))
sys.path.insert(0, str(ROOT / "assets" / "scripts"))

import experiment_identity as identity  # noqa: E402
import shared_set_split  # noqa: E402
from test_day04_day05_contracts import run_cell  # noqa: E402

DATASET_ROOT = ROOT / "assets" / "anomaly_dataset" / "pvc_sheet"
MODEL_SETTINGS = {"backbone": "resnet18", "layers": ["layer2", "layer3"], "pre_trained": False,
                  "coreset_sampling_ratio": 0.1, "num_neighbors": 9}


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _weights_path(course_root: Path) -> Path:
    return course_root / "training_results" / "day04" / "run" / "weights" / "best.pt"


def _yolo_worker(phase: str, course_root: Path) -> None:
    """Run the actual YOLO producer cells outside the process that imports anomalib."""
    import torch
    import ultralytics
    from ultralytics import YOLO

    torch.manual_seed(17)
    torch.set_num_threads(2)
    best_weights = _weights_path(course_root)
    day04 = course_root / "submissions" / "day04"
    if phase == "calibration":
        best_weights.parent.mkdir(parents=True)
        random_detector = YOLO("yolov8n.yaml")
        torch.save({"model": random_detector.model, "train_args": {"task": "detect"}},
                   best_weights)

    model = YOLO(str(best_weights))
    ns = {"COURSE_ROOT": course_root, "ASSETS": ROOT / "assets", "Path": Path,
          "best_weights": best_weights, "model": model, "shared_set_split": shared_set_split}
    split_path = day04 / "shared_set_split.json"
    with patch.object(model, "predict", wraps=model.predict) as predict:
        if phase == "calibration":
            run_cell(ns, "Day04_03", "f7f5833b")
            run_cell(ns, "Day04_03", "552d3581")
        else:
            assert phase == "test"
            ns["shared_split"] = _read_json(split_path)
            ns["MIN_INFERENCE_CONF"] = _read_json(
                day04 / "yolo_predictions_on_shared_set.json")["min_inference_conf"]
            run_cell(ns, "Day04_03", "shared-sealed-test")
            seal_path = day04 / "yolo_predictions_sealed_test.json"
            original_seal = seal_path.read_bytes()
            run_cell(ns, "Day04_03", "shared-sealed-test")
            assert seal_path.read_bytes() == original_seal
        expected = _read_json(split_path)["partitions"][phase]
        assert [Path(call.kwargs["source"]).relative_to(DATASET_ROOT).as_posix()
                for call in predict.call_args_list] == expected

    print(f"ultralytics {ultralytics.__version__}, torch {torch.__version__}: "
          f"genuine {phase} inference on exactly {len(expected)} images")


def _run_yolo(python: Path, phase: str, course_root: Path) -> None:
    config = course_root / "yolo_config"
    config.mkdir(exist_ok=True)
    proc = subprocess.run(
        [str(python), str(Path(__file__).resolve()), phase, str(course_root)],
        cwd=course_root,
        env={**os.environ, "YOLO_CONFIG_DIR": str(config), "YOLO_AUTOINSTALL": "false",
             "CUDA_VISIBLE_DEVICES": "-1", "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True, encoding="utf-8", errors="replace", timeout=180, check=False,
    )
    assert proc.returncode == 0, f"YOLO {phase} failed:\n{proc.stdout}\n{proc.stderr}"
    print(proc.stdout.strip())


@pytest.fixture(scope="module")
def real_run(tmp_path_factory):
    """Fit a real PatchCore once and run the real cells up to the sealed comparison."""
    anomalib = pytest.importorskip("anomalib")
    if anomalib.__version__ != "2.7.0":
        pytest.skip(f"BLOCKED: need anomalib 2.7.0, found {anomalib.__version__}")
    pytest.importorskip("lightning")
    yolo_python = os.environ.get("DAY05_YOLO_PYTHON")
    if not yolo_python:
        pytest.skip("BLOCKED: set DAY05_YOLO_PYTHON to the separate YOLO interpreter")
    yolo_executable = Path(yolo_python).resolve(strict=True)
    assert yolo_executable != Path(sys.executable).resolve(), "YOLO needs its own environment"

    import torch
    from anomalib.data import Folder
    from anomalib.engine import Engine
    from anomalib.models import Patchcore
    from matplotlib import pyplot as plt

    course_root = tmp_path_factory.getbasetemp() / "day05_course"
    day05 = course_root / "submissions" / "day05"
    day05.mkdir(parents=True)
    layout = _read_json(DATASET_ROOT / "dataset_layout.json")
    _run_yolo(yolo_executable, "calibration", course_root)
    split = _read_json(course_root / "submissions" / "day04" / "shared_set_split.json")

    # Day 5 Notebook 02: the real Folder split, checked against the Day 4 record
    datamodule_ns = {"Folder": Folder, "layout": layout, "dataset_root": DATASET_ROOT}
    run_cell(datamodule_ns, "Day05_02", "f1a28c15")
    datamodule = datamodule_ns["datamodule"]

    previous_threads = torch.get_num_threads()
    torch.set_num_threads(2)
    try:
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(17)
            model = Patchcore(**MODEL_SETTINGS)
            notebook = {"COURSE_ROOT": course_root, "ASSETS": ROOT / "assets", "json": json,
                        "Path": Path, "pd": pd, "np": np, "plt": plt, "model": model,
                        "datamodule": datamodule,
                        "Engine": Engine, "Folder": Folder, "layout": layout,
                        "dataset_root": DATASET_ROOT, "anomalib": anomalib, "torch": torch,
                        "MODEL_SETTINGS": MODEL_SETTINGS}
            run_cell(notebook, "Day05_02", "befc72c6")  # real Engine.fit
            run_cell(notebook, "Day05_02", "daed190f")  # split + fitted fingerprint
            run_cell(notebook, "Day05_02", "82f543da")  # real calibration predict
            run_cell(notebook, "Day05_02", "39a9c510")  # actual save_map + calibration NPZs
            run_cell(notebook, "Day05_02", "1c4cd018")  # canonical postprocessor accessor

        calibration_maps = sorted((day05 / "maps_calibration").glob("*_map.npz"))
        assert {path.name for path in calibration_maps} == {
            f"{Path(image).stem}_map.npz" for image in split["partitions"]["calibration"]
        }
        calibration_digest = identity.file_set_digest(calibration_maps)
        assert not (day05 / "patchcore_test_predictions.json").exists()
        assert not (course_root / "submissions" / "day04"
                    / "yolo_predictions_sealed_test.json").exists()

        consumer = dict(notebook)
        for cell_id in ("39ee7a27", "ae192ae8", "d26eb085", "cccf0ff7", "935ef5b9"):
            run_cell(consumer, "Day05_03", cell_id)
        run_cell(consumer, "Day05_03", "clarity-freeze-record", (
            ('FREEZE_DECLARATION = ""', 'FREEZE_DECLARATION = "frozen before test; integration run"'),
            ("TEST_ALREADY_SEEN = True", "TEST_ALREADY_SEEN = False")))

        _run_yolo(yolo_executable, "test", course_root)
        sealed_ns = dict(notebook)
        interruption = _interrupt_and_resume(sealed_ns, day05)
        assert identity.file_set_digest((day05 / "maps_calibration").glob("*_map.npz")) == (
            calibration_digest)
        # Engine.predict restores training mode; get an independent raw inference reference.
        with torch.no_grad():
            model.model.eval()
            raw_batches = [model.model(batch["image"]) for batch in sealed_ns["test_batches"]]
    finally:
        torch.set_num_threads(previous_threads)

    # final comparison from both seals
    final = dict(consumer)
    run_cell(final, "Day05_03", "clarity-load-sealed-test")
    run_cell(final, "Day05_03", "9747ac10")

    return {"course_root": course_root, "split": split, "notebook": notebook,
            "consumer": consumer, "test_frame": final["test_frame"],
            "model": model, "interruption": interruption,
            "test_batches": sealed_ns["test_batches"], "raw_batches": raw_batches}


def _interrupt_and_resume(ns: dict, day05: Path) -> dict:
    """Interrupt after publishing the map directory but before committing the seal."""
    maps = day05 / "maps"
    pending = day05 / "maps_pending"
    seal = day05 / "patchcore_test_predictions.json"
    write_json = identity.write_json_atomic
    before_commit = {}

    def interrupt_before_commit(path, payload):
        if path == seal:
            assert not pending.exists() and not seal.exists()
            before_commit.update(identity.file_set_digest(maps.glob("*_map.npz")))
            assert before_commit == {key: payload["maps"][key] for key in ("count", "digest")}
            raise KeyboardInterrupt("injected before NPZ seal commit")
        return write_json(path, payload)

    with patch.object(ns["engine"], "predict", wraps=ns["engine"].predict) as predict:
        with patch.object(identity, "write_json_atomic", interrupt_before_commit):
            with pytest.raises(KeyboardInterrupt, match="before NPZ seal commit"):
                run_cell(ns, "Day05_02", "clarity-sealed-test-scoring")
        staged = sorted(pending.glob("*_map.npz"))
        assert not seal.exists() and not maps.exists()
        assert identity.file_set_digest(staged) == before_commit
        for path in staged:
            with np.load(path, allow_pickle=False) as data:
                assert data["anomaly_map"].dtype == np.float32

        # Also leave a real orphan NPZ behind, as an abrupt process stop could.
        maps.mkdir()
        orphan = maps / "orphan_map.npz"
        shutil.copyfile(staged[0], orphan)
        orphan_hash = identity.file_sha256(orphan)
        run_cell(ns, "Day05_02", "clarity-sealed-test-scoring")
        assert not orphan.exists()
        quarantined = list((day05 / "maps_unsealed").glob("maps-*/orphan_map.npz"))
        assert len(quarantined) == 1
        assert identity.file_sha256(quarantined[0]) == orphan_hash
        first_seal = seal.read_bytes()
        first_maps = identity.file_set_digest(maps.glob("*_map.npz"))
        run_cell(ns, "Day05_02", "clarity-sealed-test-scoring")
        assert seal.read_bytes() == first_seal
        assert identity.file_set_digest(maps.glob("*_map.npz")) == first_maps
    return {"staged": len(staged), "predict_calls": predict.call_count}


def test_the_real_anomalib_split_matches_the_day4_record(real_run) -> None:
    split = real_run["split"]
    assert split["counts"] == {"patchcore_train": 32, "calibration": 26, "test": 26}
    manifest = json.loads((real_run["course_root"] / "submissions" / "day05"
                           / "split_manifest.json").read_text(encoding="utf-8"))
    assert manifest["shared_split"]["verified"] is True
    assert manifest["split"]["library"].startswith("anomalib==2.")


def test_the_real_postprocessor_threshold_is_recorded(real_run) -> None:
    payload = json.loads((real_run["course_root"] / "submissions" / "day05"
                          / "patchcore_predictions.json").read_text(encoding="utf-8"))
    threshold = payload["postprocessor_threshold"]
    assert isinstance(threshold, float) and math.isfinite(threshold)
    assert payload["experiment"]["postprocessor"]["adaptive_threshold"] == threshold
    assert payload["scored_partitions"] == ["calibration"] and payload["test_scored"] is False
    # the pinned PostProcessor really has no `adaptive_threshold` attribute
    assert not hasattr(real_run["model"].post_processor, "adaptive_threshold")


def test_the_fitted_model_survives_real_calibration_scoring(real_run) -> None:
    notebook = real_run["notebook"]
    assert identity.fitted_state(real_run["model"])["fingerprint"] == (
        notebook["FITTED_STATE"]["fingerprint"])


def test_real_npz_contents_align_with_test_images_and_scores(real_run) -> None:
    day05 = real_run["course_root"] / "submissions" / "day05"
    sealed = _read_json(day05 / "patchcore_test_predictions.json")
    rows = {row["image"]: row for row in sealed["images"]}
    assert len(rows) == len(sealed["images"]) == 26
    assert set(rows) == set(real_run["split"]["partitions"]["test"])
    paths = sorted((day05 / "maps").glob("*_map.npz"))
    assert {path.name for path in paths} == {f"{Path(image).stem}_map.npz" for image in rows}
    assert sealed["maps"] == {"directory": "maps", **identity.file_set_digest(paths)}
    for batch, raw in zip(real_run["test_batches"], real_run["raw_batches"], strict=True):
        for index, image_path in enumerate(batch.image_path):
            image = Path(image_path).resolve().relative_to(DATASET_ROOT.resolve()).as_posix()
            path = day05 / "maps" / f"{Path(image).stem}_map.npz"
            row = rows[image]
            with np.load(path, allow_pickle=False) as data:
                assert set(data.files) == {"anomaly_map", "raw_score", "truly_abnormal", "image"}
                assert data["image"].shape == () and data["image"].item() == image
                assert data["truly_abnormal"].shape == ()
                assert data["truly_abnormal"].dtype == np.bool_
                assert data["truly_abnormal"].item() is row["truly_abnormal"]
                assert row["truly_abnormal"] == (Path(image).parent.name != "good")
                assert data["raw_score"].shape == () and data["raw_score"].dtype == np.float32
                assert np.isfinite(data["raw_score"]).item()
                assert data["raw_score"].item() == pytest.approx(raw.pred_score[index].item())
                actual_map = data["anomaly_map"]
                expected_map = raw.anomaly_map[index].detach().cpu().numpy().squeeze()
                assert actual_map.ndim == 2 and actual_map.dtype == np.float32
                assert np.isfinite(actual_map).all()
                np.testing.assert_allclose(actual_map, expected_map, rtol=1e-5, atol=1e-6)
            assert row["score"] == round(batch.pred_score[index].item(), 4)
    print(f"Verified all {len(paths)} test NPZs against raw tensors, sealed scores and image IDs")


def test_interrupted_map_publish_rolls_back_and_retry_seals_once(real_run) -> None:
    day05 = real_run["course_root"] / "submissions" / "day05"
    interruption = real_run["interruption"]
    assert interruption["staged"] == 26
    assert interruption["predict_calls"] == 2  # interrupted attempt and retry, not seal reload
    assert not (day05 / "maps_pending").exists()
    print("Interrupted before JSON commit: all 26 NPZs rolled back to staging, no public maps or seal; "
          "retry sealed the complete set and reopening it did not rescore")


def test_comparison_rejects_replaced_npz_without_discarding_sealed_scores(real_run) -> None:
    maps = real_run["course_root"] / "submissions" / "day05" / "maps"
    replaced, other = sorted(maps.glob("*_map.npz"))[:2]
    original = replaced.read_bytes()
    reader = dict(real_run["consumer"])
    try:
        shutil.copyfile(other, replaced)  # still a valid NPZ; file names and count are unchanged
        run_cell(reader, "Day05_03", "clarity-load-sealed-test")
        status = reader["numeric_maps_status"]
        assert status["verified"] is False
        assert status["actual"]["count"] == status["recorded"]["count"] == 26
        assert status["actual"]["digest"] != status["recorded"]["digest"]
        pd.testing.assert_frame_equal(reader["test_frame"], real_run["test_frame"])
    finally:
        replaced.write_bytes(original)


def test_real_patchcore_seal_matches_freeze(real_run) -> None:
    sealed = json.loads((real_run["course_root"] / "submissions" / "day05"
                         / "patchcore_test_predictions.json").read_text(encoding="utf-8"))
    assert sealed["scored_partitions"] == ["test"]
    assert len(sealed["images"]) == 26
    assert sealed["maps"]["count"] == 26
    assert sealed["experiment"]["experiment_id"] == real_run["consumer"]["freeze_record"][
        "experiment"]["experiment_id"]
    # the real scores are on the documented 0-1 scale
    scores = [row["score"] for row in sealed["images"]]
    assert min(scores) >= 0.0 and max(scores) <= 1.0


def test_the_final_comparison_uses_the_full_test_partition(real_run) -> None:
    results = json.loads((real_run["course_root"] / "submissions" / "day05"
                          / "comparison_test_results.json").read_text(encoding="utf-8"))
    assert results["assessment_role"] == "declared_untouched_test"
    assert results["assessment_is_final"] is True
    for method in results["test"]:
        assert method["n_images"] == 26
        assert method["TP"] + method["FP"] + method["FN"] + method["TN"] == 26
    assert results["yolo_weights"]["sha256"]
    assert results["numeric_maps"]["verified"] is True


def test_real_yolo_outputs_cover_the_split_and_match_the_frozen_checkpoint(real_run) -> None:
    root = real_run["course_root"]
    day04 = root / "submissions" / "day04"
    calibration = _read_json(day04 / "yolo_predictions_on_shared_set.json")
    sealed = _read_json(day04 / "yolo_predictions_sealed_test.json")
    frozen = real_run["consumer"]["freeze_record"]
    sha256 = identity.file_sha256(_weights_path(root))
    assert calibration["weights_sha256"] == frozen["yolo_weights"]["sha256"] == sha256
    assert sealed["model"]["weights_sha256"] == sha256
    assert sealed["experiment"]["experiment_id"] == frozen["experiment"]["experiment_id"]
    assert calibration["test_scored"] is False
    for phase, payload in (("calibration", calibration), ("test", sealed)):
        assert payload["scored_partitions"] == [phase]
        assert sorted(row["image"] for row in payload["images"]) == sorted(
            real_run["split"]["partitions"][phase])
        assert all(0 <= row["yolo_max_conf"] <= 1 for row in payload["images"])


if __name__ == "__main__":
    _yolo_worker(sys.argv[1], Path(sys.argv[2]))
