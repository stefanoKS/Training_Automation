"""凍結実験の身元を確かめるテスト / Tests for the frozen-experiment identity.

Day 5 の封印テストは「固定した実験の成績」でなければ意味がありません。ここでは、小さな合成の
フィクスチャだけで、身元の照合と封印ファイルの検証を一件ずつ確かめます。重い PatchCore の学習は
しません。

The sealed Day 5 result only means something if it belongs to the frozen experiment. These tests use
small synthetic fixtures and never fit a real PatchCore model.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "assets" / "helpers"))

import experiment_identity as identity  # noqa: E402

ROLE = "declared_untouched_test"


# ---------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------


def _manifest() -> dict:
    manifest = {
        "dataset_name": "fixture",
        "dataset_seed": 1,
        "image_size": [8, 8],
        "split": {"library": "fixture", "val_split_mode": "from_test", "val_split_ratio": 0.5},
        "counts": {"calibration": 1, "patchcore_train": 1, "test": 2},
        "partitions": {
            "patchcore_train": ["train/good/d.png"],
            "calibration": ["test/good/c.png"],
            "test": ["test/good/a.png", "test/bad/b.png"],
        },
        "model": {"class": "Patchcore", "backbone": "resnet18"},
        "postprocessor": {"normalisation_enabled": True},
        "score_convention": "fixture convention",
    }
    return manifest


def _fitted(fill: float = 1.0, count: int = 6) -> dict:
    """A fake fitted state: only the tensors matter, so a tuple of bytes is enough."""
    tensors = [("memory_bank", [count, 2], "torch.float32", bytes([int(fill)] * count * 8)),
               ("linear.weight", [2, 2], "torch.float32", bytes([int(fill)] * 16))]
    return {
        "fingerprint": identity.digest_json([[name, shape, dtype, list(data)]
                                             for name, shape, dtype, data in tensors]),
        "tensor_count": len(tensors),
        "memory_bank": {"name": "memory_bank", "shape": [count, 2],
                        "dtype": "torch.float32", "bytes": count * 8},
    }


def _postprocessor(threshold: float = 0.5) -> dict:
    return {"available": True, "enable_normalization": True, "image_min": 0.1,
            "image_max": 0.9, "pixel_min": 0.2, "pixel_max": 0.8,
            "adaptive_threshold": threshold}


def _frozen(manifest=None, fitted=None, postprocessor=None, yolo=0.06, patchcore=0.5) -> dict:
    base = identity.base_identity(manifest or _manifest(), fitted or _fitted(),
                                  postprocessor or _postprocessor())
    return identity.frozen_identity(base, yolo_threshold=yolo, patchcore_threshold=patchcore)


def _payload(frozen: dict, *, rows=None, schema=identity.SEALED_SCHEMA,
             role="declared_untouched_test") -> dict:
    return {
        "schema_version": schema,
        "scored_partitions": ["test"],
        "experiment": frozen,
        "frozen": {"patchcore_threshold": frozen["thresholds"]["patchcore"],
                   "yolo_threshold": frozen["thresholds"]["yolo"],
                   "assessment_role": role},
        "images": rows if rows is not None else [
            {"partition": "test", "image": "test/good/a.png", "score": 0.12,
             "anomalib_predicted_ng": False, "truly_abnormal": False},
            {"partition": "test", "image": "test/bad/b.png", "score": 0.87,
             "anomalib_predicted_ng": True, "truly_abnormal": True},
        ],
    }


def _rows():
    return [
        {"partition": "test", "image": "test/good/a.png", "score": 0.12,
         "anomalib_predicted_ng": False, "truly_abnormal": False},
        {"partition": "test", "image": "test/bad/b.png", "score": 0.87,
         "anomalib_predicted_ng": True, "truly_abnormal": True},
    ]


# ---------------------------------------------------------------------------
# the identity itself
# ---------------------------------------------------------------------------


def test_fitted_fingerprint_is_stable_and_changes_with_the_fitted_bytes() -> None:
    class Tensor:
        def __init__(self, values):
            self.values = list(values)
            self.shape = (len(self.values),)
            self.dtype = "float32"
            self.numel_value = len(self.values)

        def detach(self):
            return self

        def cpu(self):
            return self

        def contiguous(self):
            return self

        def numpy(self):
            class Buffer:
                def __init__(self, values):
                    self.values = values

                def tobytes(self):
                    return bytes(int(value) for value in self.values)

            return Buffer(self.values)

        def numel(self):
            return self.numel_value

    class MemoryBank:
        def __init__(self, values):
            self.values = Tensor(values)
            self.memory_bank = self.values

    class Model:
        def __init__(self, values):
            self.model = MemoryBank(values)

    first = identity.fitted_state(Model([1, 2, 3, 4]))
    again = identity.fitted_state(Model([1, 2, 3, 4]))
    changed = identity.fitted_state(Model([1, 2, 3, 5]))
    assert first["fingerprint"] == again["fingerprint"]
    assert first["fingerprint"] != changed["fingerprint"]
    assert first["memory_bank"]["shape"] == [4]


def test_identity_ignores_object_identity_and_file_paths() -> None:
    first = _frozen()
    second = _frozen()
    assert first["experiment_id"] == second["experiment_id"]
    assert "path" not in json.dumps(first)
    assert "uuid" not in json.dumps(first).lower()


def test_thresholds_are_part_of_the_frozen_identity() -> None:
    low = _frozen(patchcore=0.5)
    high = _frozen(patchcore=0.6)
    assert low["experiment_id"] != high["experiment_id"]


def test_a_new_fit_is_a_new_experiment_even_with_the_same_settings() -> None:
    same_settings_other_fit = _frozen(fitted=_fitted(fill=2.0))
    assert same_settings_other_fit["experiment_id"] != _frozen()["experiment_id"]


def test_a_different_split_is_a_different_experiment() -> None:
    manifest = _manifest()
    manifest["partitions"]["test"] = ["test/good/a.png", "test/bad/other.png"]
    assert _frozen(manifest=manifest)["experiment_id"] != _frozen()["experiment_id"]


# ---------------------------------------------------------------------------
# the sealed file (CASE 1–7)
# ---------------------------------------------------------------------------


def test_case1_a_new_experiment_with_a_valid_seal_validates() -> None:
    frozen = _frozen()
    rows = identity.validate_sealed(_payload(frozen), schema_version=identity.SEALED_SCHEMA,
                                    expected=frozen, manifest=_manifest(),
                                 expected_role=ROLE)
    assert [row["image"] for row in rows] == ["test/good/a.png", "test/bad/b.png"]


def test_case2_the_same_frozen_experiment_reuses_the_same_seal() -> None:
    frozen = _frozen()
    payload = _payload(frozen)
    assert identity.validate_sealed(payload, schema_version=identity.SEALED_SCHEMA,
                                    expected=frozen, manifest=_manifest(),
                                 expected_role=ROLE) == payload["images"]


def test_case3_another_fitted_model_is_rejected() -> None:
    frozen = _frozen()
    other = _frozen(fitted=_fitted(fill=2.0))
    with pytest.raises(identity.ProvenanceError, match="different fitted model"):
        identity.validate_sealed(_payload(other), schema_version=identity.SEALED_SCHEMA,
                                 expected=frozen, manifest=_manifest(),
                                 expected_role=ROLE)


def test_case4_another_split_is_rejected() -> None:
    frozen = _frozen()
    other_manifest = _manifest()
    other_manifest["partitions"]["test"] = ["test/good/a.png", "test/bad/c.png"]
    other = _frozen(manifest=other_manifest)
    with pytest.raises(identity.ProvenanceError, match="different dataset split"):
        identity.validate_sealed(_payload(other), schema_version=identity.SEALED_SCHEMA,
                                 expected=frozen, manifest=_manifest(),
                                 expected_role=ROLE)


def test_case5_other_thresholds_are_rejected() -> None:
    frozen = _frozen()
    other = _frozen(patchcore=0.7)
    with pytest.raises(identity.ProvenanceError, match="different thresholds"):
        identity.validate_sealed(_payload(other), schema_version=identity.SEALED_SCHEMA,
                                 expected=frozen, manifest=_manifest(),
                                 expected_role=ROLE)


def test_case6_missing_test_images_are_rejected() -> None:
    frozen = _frozen()
    with pytest.raises(identity.ProvenanceError, match="do not cover the test partition"):
        identity.validate_sealed(_payload(frozen, rows=_rows()[:1]),
                                 schema_version=identity.SEALED_SCHEMA,
                                 expected=frozen, manifest=_manifest(),
                                 expected_role=ROLE)


def test_case7_duplicate_image_ids_are_rejected() -> None:
    frozen = _frozen()
    rows = _rows() + [_rows()[0]]
    with pytest.raises(identity.ProvenanceError, match="duplicate image IDs"):
        identity.validate_sealed(_payload(frozen, rows=rows),
                                 schema_version=identity.SEALED_SCHEMA,
                                 expected=frozen, manifest=_manifest(),
                                 expected_role=ROLE)


@pytest.mark.parametrize("field, value, message", [
    ("score", "0.12", "is not a number"),
    ("truly_abnormal", 1, "is not a boolean"),
    ("partition", "calibration", "non-test rows"),
])
def test_sealed_rows_are_type_and_partition_checked(field, value, message) -> None:
    frozen = _frozen()
    rows = _rows()
    rows[0] = {**rows[0], field: value}
    with pytest.raises(identity.ProvenanceError, match=message):
        identity.validate_sealed(_payload(frozen, rows=rows),
                                 schema_version=identity.SEALED_SCHEMA,
                                 expected=frozen, manifest=_manifest(),
                                 expected_role=ROLE)


def test_a_missing_field_is_named() -> None:
    frozen = _frozen()
    rows = _rows()
    rows[0] = {key: value for key, value in rows[0].items() if key != "score"}
    with pytest.raises(identity.ProvenanceError, match="no 'score'"):
        identity.validate_sealed(_payload(frozen, rows=rows),
                                 schema_version=identity.SEALED_SCHEMA,
                                 expected=frozen, manifest=_manifest(),
                                 expected_role=ROLE)


def test_an_older_schema_is_rejected_before_anything_else() -> None:
    frozen = _frozen()
    with pytest.raises(identity.ProvenanceError, match="stale sealed predictions"):
        identity.validate_sealed(_payload(frozen, schema=2),
                                 schema_version=identity.SEALED_SCHEMA,
                                 expected=frozen, manifest=_manifest(),
                                 expected_role=ROLE)


def test_case11_the_reused_data_designation_survives_validation() -> None:
    frozen = _frozen()
    payload = _payload(frozen, role="illustrative_reused_data")
    identity.validate_sealed(payload, schema_version=identity.SEALED_SCHEMA,
                             expected=frozen, manifest=_manifest(),
                             expected_role="illustrative_reused_data")
    assert payload["frozen"]["assessment_role"] == "illustrative_reused_data"


def test_an_unknown_assessment_role_is_rejected() -> None:
    frozen = _frozen()
    payload = _payload(frozen)
    payload["frozen"]["assessment_role"] = "untouched"
    with pytest.raises(identity.ProvenanceError, match="assessment role"):
        identity.validate_sealed(payload, schema_version=identity.SEALED_SCHEMA,
                                 expected=frozen, manifest=_manifest(),
                                 expected_role=ROLE)


def test_a_mismatched_assessment_role_is_rejected() -> None:
    frozen = _frozen()
    payload = _payload(frozen, role="illustrative_reused_data")
    with pytest.raises(identity.ProvenanceError, match="assessment role differs"):
        identity.validate_sealed(payload, schema_version=identity.SEALED_SCHEMA,
                                 expected=frozen, manifest=_manifest(),
                                 expected_role="declared_untouched_test")


def test_reused_data_cannot_become_untouched() -> None:
    """Editing the role field of an existing seal must never upgrade it."""
    frozen = _frozen()
    payload = _payload(frozen, role="declared_untouched_test")
    with pytest.raises(identity.ProvenanceError, match="assessment role differs"):
        identity.validate_sealed(payload, schema_version=identity.SEALED_SCHEMA,
                                 expected=frozen, manifest=_manifest(),
                                 expected_role="illustrative_reused_data")


def test_a_freeze_record_without_a_role_is_rejected() -> None:
    frozen = _frozen()
    with pytest.raises(identity.ProvenanceError, match="assessment role"):
        identity.validate_sealed(_payload(frozen), schema_version=identity.SEALED_SCHEMA,
                                 expected=frozen, manifest=_manifest(),
                                 expected_role=None)


def test_a_yolo_seal_validates_and_checks_the_same_contracts() -> None:
    frozen = _frozen()
    payload = {
        "schema_version": 1,
        "scored_partitions": ["test"],
        "experiment": frozen,
        "frozen": {"yolo_threshold": frozen["thresholds"]["yolo"],
                   "patchcore_threshold": frozen["thresholds"]["patchcore"],
                   "assessment_role": ROLE},
        "images": [
            {"partition": "test", "image": "test/good/a.png", "yolo_max_conf": 0.0,
             "truly_abnormal": False},
            {"partition": "test", "image": "test/bad/b.png", "yolo_max_conf": 0.93,
             "truly_abnormal": True},
        ],
    }
    rows = identity.validate_yolo_sealed(payload, schema_version=1, expected=frozen,
                                         manifest=_manifest(), expected_role=ROLE)
    assert [row["image"] for row in rows] == ["test/good/a.png", "test/bad/b.png"]

    payload["frozen"]["yolo_threshold"] = 0.99
    with pytest.raises(identity.ProvenanceError, match="another threshold"):
        identity.validate_yolo_sealed(payload, schema_version=1, expected=frozen,
                                      manifest=_manifest(), expected_role=ROLE)


# ---------------------------------------------------------------------------
# writing (CASE 10)
# ---------------------------------------------------------------------------


def test_postprocessor_state_reads_the_anomalib_2_axis_names() -> None:
    """anomalib 2.x exposes ``_image_threshold`` and NaN buffers before fitting."""
    import types

    class Tensor:
        def __init__(self, value):
            self.value = value

        def item(self):
            return self.value

    post_processor = types.SimpleNamespace(
        enable_normalization=True, image_min=Tensor(0.25), image_max=Tensor(0.75),
        pixel_min=Tensor(float("nan")), pixel_max=Tensor(0.5), _image_threshold=Tensor(0.4))
    model = types.SimpleNamespace(post_processor=post_processor)
    state = identity.postprocessor_state(model)

    assert state["available"] is True
    assert state["adaptive_threshold"] == 0.4
    assert state["image_min"] == 0.25 and state["image_max"] == 0.75
    # an unfitted statistic becomes None, never NaN, so the record stays valid JSON
    assert state["pixel_min"] is None
    assert "NaN" not in identity.canonical_json(state)


def test_case10_a_failed_write_publishes_nothing(tmp_path, monkeypatch) -> None:
    target = tmp_path / "patchcore_test_predictions.json"
    target.write_text('{"previous": true}', encoding="utf-8")

    def boom(*args, **kwargs):
        raise OSError("disk full")

    monkeypatch.setattr(identity.os, "replace", boom)
    with pytest.raises(OSError, match="disk full"):
        identity.write_json_atomic(target, {"new": True})

    assert json.loads(target.read_text(encoding="utf-8")) == {"previous": True}
    assert [path.name for path in tmp_path.iterdir()] == ["patchcore_test_predictions.json"]


def test_a_successful_write_replaces_the_file(tmp_path) -> None:
    target = tmp_path / "record.json"
    identity.write_json_atomic(target, {"first": 1})
    identity.write_json_atomic(target, {"second": 2})
    assert json.loads(target.read_text(encoding="utf-8")) == {"second": 2}
    assert sorted(path.suffix for path in tmp_path.iterdir()) == [".json"]


# ---------------------------------------------------------------------------
# image names
# ---------------------------------------------------------------------------


def test_image_ids_from_both_conventions_agree() -> None:
    assert identity.normalise_image_id("test/good/a.png") == "good/a.png"
    assert identity.normalise_image_id("good/a.png") == "good/a.png"
    assert identity.normalise_image_id("test\\bad\\b.png") == "bad/b.png"
    assert identity.test_partition(_manifest()) == {"good/a.png", "bad/b.png"}
