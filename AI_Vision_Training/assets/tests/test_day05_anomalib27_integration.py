"""Genuine ``anomalib==2.7.0`` run of the Day 4 → Day 5 cells (opt-in).

The rest of the suite runs the real notebook cells against duck-typed model/engine stand-ins, because
the course's default environment cannot install two ``cv2`` builds at once. This module is the other
half of the evidence: where the pinned Day 5 stack (``anomalib>=2`` with ``PostProcessor``,
``lightning``, ``torch``) is importable, the PatchCore half is executed for real — real ``Folder``
split, real ``Engine.fit``, real ``PostProcessor`` statistics, real test scoring.

It is skipped, with a reason, in the base course environment (``anomalib 1.1.0dev`` has no
``anomalib.post_processing``). A skip is reported as **BLOCKED**, never as PASS.

Run it with the pinned interpreter:

    .venv-anomalib\\Scripts\\python.exe -m pytest assets/tests/test_day05_anomalib27_integration.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]

torch = pytest.importorskip("torch")
anomalib = pytest.importorskip("anomalib")
pytest.importorskip("lightning")
_post_processing = pytest.importorskip(
    "anomalib.post_processing",
    reason="anomalib 2.x is required: the base course environment ships 1.1.0dev, which has no "
           "PostProcessor class (BLOCKED, not PASS)")

sys.path.insert(0, str(ROOT / "assets" / "helpers"))
sys.path.insert(0, str(ROOT / "assets" / "scripts"))
sys.path.insert(0, str(Path(__file__).parent))

import experiment_identity as identity  # noqa: E402
import shared_set_split  # noqa: E402
from test_day04_day05_contracts import _FakeYolo, run_cell  # noqa: E402

DATASET_ROOT = ROOT / "assets" / "anomaly_dataset" / "pvc_sheet"
MODEL_SETTINGS = {"backbone": "resnet18", "layers": ["layer2", "layer3"], "pre_trained": True,
                  "coreset_sampling_ratio": 0.1, "num_neighbors": 9}


@pytest.fixture(scope="module")
def real_run(tmp_path_factory):
    """Fit a real PatchCore once and run the real cells up to the sealed comparison."""
    from anomalib.data import Folder
    from anomalib.engine import Engine
    from anomalib.models import Patchcore

    course_root = tmp_path_factory.mktemp("course")
    layout = json.loads((DATASET_ROOT / "dataset_layout.json").read_text(encoding="utf-8"))
    best_weights = course_root / "training_results" / "day04" / "run" / "weights" / "best.pt"
    best_weights.parent.mkdir(parents=True)
    best_weights.write_bytes(b"YOLO stand-in: ultralytics is not installed in this environment")
    (course_root / "submissions" / "day05").mkdir(parents=True)
    (course_root / "submissions" / "day04").mkdir(parents=True)

    common = {"COURSE_ROOT": course_root, "ASSETS": ROOT / "assets", "json": json, "Path": Path,
              "pd": pd, "best_weights": best_weights, "shared_set_split": shared_set_split,
              "model": _FakeYolo()}

    # Day 4: split first, then calibration-only scores
    run_cell(common, "Day04_03", "f7f5833b")
    run_cell(common, "Day04_03", "552d3581")
    split = json.loads((course_root / "submissions" / "day04" / "shared_set_split.json")
                       .read_text(encoding="utf-8"))

    # Day 5 Notebook 02: the real Folder split, checked against the Day 4 record
    datamodule_ns = {"Folder": Folder, "layout": layout, "dataset_root": DATASET_ROOT}
    run_cell(datamodule_ns, "Day05_02", "f1a28c15")
    datamodule = datamodule_ns["datamodule"]

    model = Patchcore(**MODEL_SETTINGS)
    engine = Engine(default_root_dir=str(course_root / "training_results" / "day05"),
                    accelerator="cpu", devices=1, max_epochs=1, logger=False,
                    enable_progress_bar=False, enable_model_summary=False)
    notebook = dict(common)
    notebook.update({"model": model, "datamodule": datamodule, "engine": engine,
                     "Engine": Engine, "Folder": Folder,
                     "layout": layout, "dataset_root": DATASET_ROOT,
                     "anomalib": anomalib, "torch": torch, "MODEL_SETTINGS": MODEL_SETTINGS,
                     "results_root": course_root / "training_results" / "day05"})
    run_cell(notebook, "Day05_02", "befc72c6")      # real Engine.fit
    run_cell(notebook, "Day05_02", "daed190f")      # real split manifest + fitted fingerprint
    run_cell(notebook, "Day05_02", "82f543da")      # real calibration predict
    run_cell(notebook, "Day05_02", "1c4cd018")      # canonical postprocessor accessor

    # Day 5 Notebook 03: pair on calibration, choose thresholds, freeze
    consumer = dict(notebook)
    run_cell(consumer, "Day05_03", "39ee7a27")
    run_cell(consumer, "Day05_03", "ae192ae8")
    run_cell(consumer, "Day05_03", "d26eb085")
    run_cell(consumer, "Day05_03", "cccf0ff7")
    run_cell(consumer, "Day05_03", "935ef5b9")
    run_cell(consumer, "Day05_03", "clarity-freeze-record", (
        ('FREEZE_DECLARATION = ""', 'FREEZE_DECLARATION = "frozen before test; real anomalib run"'),
        ("TEST_ALREADY_SEEN = True", "TEST_ALREADY_SEEN = False")))

    # sealed test scoring: YOLO stand-in, real PatchCore
    yolo_seal = dict(common)
    yolo_seal.update({"json": json, "Path": Path})
    run_cell(yolo_seal, "Day04_03", "shared-sealed-test")
    sealed_ns = dict(notebook)
    sealed_ns["save_map"] = lambda batch, index, path: path.write_bytes(
        json.dumps([float(value) for value in
                    batch["anomaly_map"][index].detach().cpu().numpy().ravel()[:8]]).encode())
    run_cell(sealed_ns, "Day05_02", "clarity-sealed-test-scoring")

    # final comparison from both seals
    final = dict(consumer)
    run_cell(final, "Day05_03", "clarity-load-sealed-test")
    run_cell(final, "Day05_03", "9747ac10")

    return {"course_root": course_root, "split": split, "notebook": notebook,
            "consumer": consumer, "final": final, "layout": layout, "datamodule": datamodule,
            "model": model, "patchcore": model}


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
    assert isinstance(threshold, float) and threshold == threshold  # finite, not NaN/None
    assert payload["experiment"]["postprocessor"]["adaptive_threshold"] == threshold
    assert payload["scored_partitions"] == ["calibration"] and payload["test_scored"] is False
    # the pinned PostProcessor really has no `adaptive_threshold` attribute
    assert not hasattr(real_run["model"].post_processor, "adaptive_threshold")


def test_the_fitted_model_survives_real_calibration_scoring(real_run) -> None:
    notebook = real_run["notebook"]
    assert identity.fitted_state(real_run["model"])["fingerprint"] == (
        notebook["FITTED_STATE"]["fingerprint"])


def test_the_sealed_test_scoring_used_the_real_engine_once(real_run) -> None:
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


def test_the_yolo_weights_digest_is_the_real_file_digest(real_run) -> None:
    weights = real_run["course_root"] / "training_results" / "day04" / "run" / "weights" / "best.pt"
    payload = json.loads((real_run["course_root"] / "submissions" / "day04"
                          / "yolo_predictions_on_shared_set.json").read_text(encoding="utf-8"))
    assert payload["weights_sha256"] == identity.file_sha256(weights)
