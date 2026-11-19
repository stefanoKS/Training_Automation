"""実験の同一性を指紋で確かめる / Prove that two runs are the same frozen experiment.

Day 5 では「固定した 1 つの実験」を、ノートブック 02（学習と採点）とノートブック 03（比較と固定）の
2 つのカーネルで扱います。カーネルは別なので、Python の変数を共有できません。そこで実験の身元を
ファイルに残し、封印した試験成績が **その身元の実験** のものかを毎回確かめます。

Day 5 handles one frozen experiment across two kernels, so the identity of the experiment has to be
written to a file instead of living in Python variables. These helpers build that identity and check
it, so a stale result is never mistaken for the current one.

指紋の作り方 / how the fingerprint is built
------------------------------------------
``fitted_state`` は学習で決まったテンソル（memory bank と PostProcessor の統計）を、名前・形・
dtype・中身のバイト列の順でハッシュします。モデル名や設定だけでは、同じ設定で作り直した別の
モデルを区別できません。

``fitted_state`` hashes the tensors that fitting actually decides (the memory bank and the
PostProcessor statistics), in a stable order, together with each name, shape and dtype. A matching
model name and configuration does **not** prove that two fitted models are the same; the bytes do.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import tempfile
from pathlib import Path

SCHEMA = 1

# 封印予測ファイルの形式 / the schema of ``patchcore_test_predictions.json``.
SEALED_SCHEMA = 3

# ``patchcore_test_predictions.json`` の 1 行 / one row of the sealed PatchCore predictions.
IMAGE_FIELDS = {
    "partition": str,
    "image": str,
    "score": (int, float),
    "anomalib_predicted_ng": bool,
    "truly_abnormal": bool,
}

# ``yolo_predictions_sealed_test.json`` の 1 行 / one row of the sealed YOLO predictions.
YOLO_IMAGE_FIELDS = {
    "partition": str,
    "image": str,
    "yolo_max_conf": (int, float),
    "truly_abnormal": bool,
}

# 記録してよい評価の役割 / the only two assessment roles that may be claimed.
ASSESSMENT_ROLES = ("declared_untouched_test", "illustrative_reused_data")

# PostProcessor の統計（正規化に使う値）。これも学習データで決まるので指紋に入れます。
# The PostProcessor statistics are fitted too, so they belong in the fingerprint.
#
# anomalib 2.x の ``PostProcessor`` は ``image_min`` / ``image_max`` / ``pixel_min`` / ``pixel_max`` を
# バッファとして持ち、しきい値は ``_image_threshold`` / ``_pixel_threshold`` に置きます。名前は
# バージョンで変わってきたので、候補を順に探します。見つからない項目は None になります。
# anomalib 2.x keeps image_min / image_max / pixel_min / pixel_max as buffers and the threshold in
# ``_image_threshold``. The names have moved between versions, so each key lists its candidates; a
# key that matches nothing is recorded as None instead of silently borrowing another value.
POSTPROCESSOR_KEYS = {
    "enable_normalization": ("enable_normalization",),
    "image_min": ("image_min",),
    "image_max": ("image_max",),
    "pixel_min": ("pixel_min",),
    "pixel_max": ("pixel_max",),
    "adaptive_threshold": ("adaptive_threshold", "image_threshold", "_image_threshold"),
}


class ProvenanceError(RuntimeError):
    """実験の身元を確かめられなかった / the frozen experiment could not be verified."""


def canonical_json(payload) -> str:
    """同じ内容なら必ず同じ文字列 / a canonical string for hashing."""
    return json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def digest_json(payload) -> str:
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def _scalar(value):
    """テンソルや numpy の値を普通の数にする / plain JSON-friendly scalar."""
    if value is None:
        return None
    for method in ("item", "tolist"):
        if hasattr(value, method):
            try:
                value = getattr(value, method)()
                break
            except (TypeError, ValueError):
                continue
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        # 未学習の PostProcessor は NaN を持ちます。NaN は JSON に書けないので None にします。
        # An unfitted PostProcessor holds NaN; NaN is not valid JSON, so record None instead.
        return value if math.isfinite(value) else None
    if isinstance(value, str):
        return value
    return str(value)


def tensor_bytes(tensor) -> bytes:
    """テンソルの中身をバイト列にする / the raw bytes of a tensor, whatever its dtype."""
    tensor = tensor.detach().cpu().contiguous()
    try:
        return tensor.numpy().tobytes()
    except (TypeError, RuntimeError):
        pass
    try:
        return bytes(tensor.untyped_storage())
    except AttributeError:
        return canonical_json(tensor.flatten().tolist()).encode("utf-8")


def _iter_state(model):
    """学習で決まるテンソルを取り出す / the tensors that fitting decides."""
    inner = getattr(model, "model", model)
    tensors = {}
    state = inner.state_dict() if hasattr(inner, "state_dict") else {}
    for name in sorted(state):
        tensor = state[name]
        if tensor is None or not hasattr(tensor, "detach"):
            continue
        tensors[name] = tensor
    bank = getattr(inner, "memory_bank", None)
    if bank is not None and hasattr(bank, "detach"):
        tensors.setdefault("memory_bank", bank)
    return tensors


def fitted_state(model) -> dict:
    """学習済みモデルの指紋 / the deterministic fingerprint of a fitted model."""
    digest = hashlib.sha256()
    tensors = []
    total_values = 0
    state = _iter_state(model)
    for name in sorted(state):
        tensor = state[name]
        data = tensor_bytes(tensor)
        digest.update(name.encode("utf-8"))
        digest.update(b"\x00")
        digest.update(str(tuple(tensor.shape)).encode("utf-8"))
        digest.update(b"\x00")
        digest.update(str(tensor.dtype).encode("utf-8"))
        digest.update(b"\x00")
        digest.update(data)
        digest.update(b"\x00")
        tensors.append({"name": name, "shape": list(tensor.shape),
                        "dtype": str(tensor.dtype), "bytes": len(data)})
        total_values += int(getattr(tensor, "numel", lambda: 0)())
    return {
        "fingerprint": digest.hexdigest(),
        "tensor_count": len(tensors),
        "total_values": total_values,
        "memory_bank": next((item for item in tensors if item["name"] == "memory_bank"), None),
        "tensors": tensors,
    }


def postprocessor_state(model) -> dict:
    """後処理の設定と統計 / the postprocessing configuration and its fitted statistics."""
    postprocessor = getattr(model, "post_processor", None)
    state = {"available": postprocessor is not None}
    for key, candidates in POSTPROCESSOR_KEYS.items():
        value = None
        if postprocessor is not None:
            for name in candidates:
                if hasattr(postprocessor, name):
                    value = _scalar(getattr(postprocessor, name))
                    if value is not None:
                        break
        state[key] = value
    return state


def dataset_identity(manifest: dict) -> dict:
    """分割の身元 / the identity of the dataset split."""
    partitions = manifest["partitions"]
    return {
        "name": manifest.get("dataset_name"),
        "seed": manifest.get("dataset_seed"),
        "image_size": manifest.get("image_size"),
        "library": manifest.get("split", {}).get("library"),
        "val_split_mode": manifest.get("split", {}).get("val_split_mode"),
        "val_split_ratio": manifest.get("split", {}).get("val_split_ratio"),
        "counts": manifest.get("counts"),
        "partitions_digest": digest_json(partitions),
    }


def base_identity(manifest: dict, fitted: dict, postprocessor: dict) -> dict:
    """学習直後に決まる身元 / the identity that exists as soon as fitting is done."""
    identity = {
        "schema": SCHEMA,
        "dataset": dataset_identity(manifest),
        "model": manifest.get("model"),
        "fitted": {
            "fingerprint": fitted["fingerprint"],
            "tensor_count": fitted.get("tensor_count"),
            "memory_bank": fitted.get("memory_bank"),
        },
        "postprocessor": postprocessor,
        "score_convention": manifest.get("score_convention"),
    }
    identity["experiment_id"] = digest_json(identity)
    return identity


def frozen_identity(base: dict, *, yolo_threshold, patchcore_threshold) -> dict:
    """固定した身元 / the identity of the frozen experiment, thresholds included."""
    identity = json.loads(canonical_json(base))
    identity.pop("experiment_id", None)
    identity["thresholds"] = {"yolo": yolo_threshold, "patchcore": patchcore_threshold}
    identity["experiment_id"] = digest_json(identity)
    return identity


def write_text_atomic(path: Path, text: str) -> Path:
    """途中で失敗しても壊れたファイルを残さない / publish a complete file or nothing."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise
    return path


def write_json_atomic(path: Path, payload) -> Path:
    """JSON も同じやり方で公開する / publish a JSON file the same way."""
    return write_text_atomic(path, json.dumps(payload, indent=2, ensure_ascii=False))


def file_sha256(path: Path) -> str:
    """ファイルの中身の指紋 / the SHA-256 of the file contents.

    A relative path proves only where a file was looked for. The digest proves *which* file it
    was, so a retrained ``best.pt`` under the same name cannot inherit the frozen provenance.
    """
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def file_set_digest(paths) -> dict:
    """ファイル集合の指紋 / a digest over a set of files (name → SHA-256, then one hash).

    Counting files is not enough: two runs can publish the same *number* of maps for different
    images. Hashing the names together with their contents is what makes the set identifiable.
    """
    digests = {Path(path).name: file_sha256(path) for path in paths}
    return {"count": len(digests), "digest": digest_json(digests)}


def check_file_sha256(path: Path, expected, *, what: str) -> str:
    """期待した中身かを確かめて、指紋を返す / verify the contents, then hand the digest back."""
    if not expected:
        raise ProvenanceError(
            f"{what} の中身の指紋が記録されていません / no SHA-256 was recorded for {what}")
    path = Path(path)
    if not path.is_file():
        raise ProvenanceError(f"{what} が見つかりません / {what} is missing: {path}")
    actual = file_sha256(path)
    if actual != expected:
        raise ProvenanceError(
            f"{what} の中身が記録と違います / the contents of {what} changed: "
            f"recorded={str(expected)[:16]}… actual={actual[:16]}…")
    return actual


def recover_fitted_model(model_class, checkpoint_path: Path, *, frozen_fingerprint: str,
                         map_location: str = "cpu"):
    """チェックポイントを読み、固定した実験と同一だと確かめてから返す。

    A kernel restart removes the fitted model but not the ``.ckpt``. Reloading that checkpoint
    restores the *same* memory bank, so the recovered model can still stand behind the frozen
    identity — but only if the fingerprint agrees. A refit never does: it builds a new memory
    bank and therefore a new experiment, so it is rejected here instead of being passed off as a
    recovery.

    Load the checkpoint and prove it is the frozen experiment; a refit is a different experiment.
    """
    loaded = model_class.load_from_checkpoint(str(checkpoint_path), map_location=map_location)
    recovered = fitted_state(loaded)
    if recovered["fingerprint"] != frozen_fingerprint:
        raise ProvenanceError(
            "読み直したチェックポイントは固定したモデルではありません。fit し直すと別の実験に"
            "なります / the checkpoint is not the frozen model "
            f"(checkpoint={recovered['fingerprint'][:12]}, frozen={str(frozen_fingerprint)[:12]}). "
            "A refit is a new experiment: redo the freeze; never reuse the sealed test scores.")
    return loaded


def normalise_image_id(name: str) -> str:
    """`test/good/a.png` と `good/a.png` を同じ名前として扱う / one name for one image."""
    name = str(name).replace("\\", "/")
    return name[len("test/"):] if name.startswith("test/") else name


def test_partition(manifest: dict) -> set[str]:
    return {normalise_image_id(name) for name in manifest["partitions"]["test"]}


def calibration_partition(manifest: dict) -> set[str]:
    return {normalise_image_id(name) for name in manifest["partitions"]["calibration"]}


def _check_experiment(sealed_experiment: dict, expected: dict) -> None:
    """身元のどこが違うかを名指しする / name exactly which part of the identity differs."""
    if not isinstance(sealed_experiment, dict):
        raise ProvenanceError(
            "封印予測に実験の身元がありません / the sealed predictions carry no experiment identity")
    reasons = []
    sealed_fitted = sealed_experiment.get("fitted", {})
    expected_fitted = expected.get("fitted", {})
    if sealed_fitted.get("fingerprint") != expected_fitted.get("fingerprint"):
        reasons.append(
            "学習したモデルが違います / a different fitted model "
            f"(sealed={str(sealed_fitted.get('fingerprint'))[:12]}, "
            f"frozen={str(expected_fitted.get('fingerprint'))[:12]})")
    sealed_dataset = sealed_experiment.get("dataset", {})
    expected_dataset = expected.get("dataset", {})
    if sealed_dataset.get("partitions_digest") != expected_dataset.get("partitions_digest"):
        reasons.append("分割が違います / a different dataset split")
    if sealed_experiment.get("thresholds") != expected.get("thresholds"):
        reasons.append(
            "しきい値が違います / different thresholds "
            f"(sealed={sealed_experiment.get('thresholds')}, frozen={expected.get('thresholds')})")
    if sealed_experiment.get("score_convention") != expected.get("score_convention"):
        reasons.append("スコアの決まりが違います / a different score convention")
    if sealed_experiment.get("postprocessor") != expected.get("postprocessor"):
        reasons.append("後処理の設定が違います / a different postprocessor configuration")
    if sealed_experiment.get("model") != expected.get("model"):
        reasons.append("モデルの設定が違います / a different model configuration")
    if reasons:
        raise ProvenanceError(
            "封印予測はこの固定実験のものではありません / the sealed predictions belong to another "
            "frozen experiment:\n  - " + "\n  - ".join(reasons))
    if sealed_experiment.get("experiment_id") != expected.get("experiment_id"):
        raise ProvenanceError(
            "実験 ID が一致しません / the experiment IDs differ even though the parts match")


def validate_sealed(payload: dict, *, schema_version: int, expected: dict,
                    manifest: dict, expected_role: str) -> list[dict]:
    """封印予測を検証して、そのまま使える行を返す / verify, then hand back the rows.

    ``expected_role`` は固定記録が宣言した評価の役割です。封印ファイルが別の役割を名乗っていたら
    失敗します。事後に役割だけを書き換えても、封印は通りません。

    ``expected_role`` is the assessment role the freeze record declared. A sealed file that claims a
    different role fails, so relabelling the role after the fact cannot make a seal valid.

    失敗したときは ``ProvenanceError`` を送出し、ファイルには一切書き込みません。
    Raises ``ProvenanceError`` and never writes: the caller keeps the existing file untouched.
    """
    return _validate(
        payload,
        schema_version=schema_version,
        expected=expected,
        manifest=manifest,
        expected_role=expected_role,
        fields=IMAGE_FIELDS,
        threshold_key="patchcore_threshold",
        threshold_value=expected.get("thresholds", {}).get("patchcore"),
    )


def validate_yolo_sealed(payload: dict, *, schema_version: int, expected: dict,
                         manifest: dict, expected_role: str) -> list[dict]:
    """Day 4 が封印した YOLO の試験予測を検証する / verify the YOLO seal Day 4 published."""
    return _validate(
        payload,
        schema_version=schema_version,
        expected=expected,
        manifest=manifest,
        expected_role=expected_role,
        fields=YOLO_IMAGE_FIELDS,
        threshold_key="yolo_threshold",
        threshold_value=expected.get("thresholds", {}).get("yolo"),
    )


def _check_assessment_role(sealed_frozen: dict, expected_role: str) -> None:
    """封印と固定記録が同じ役割を名乗っているか / the seal and the freeze record must agree."""
    role = sealed_frozen.get("assessment_role")
    if role not in ASSESSMENT_ROLES:
        raise ProvenanceError(
            "評価の役割が記録されていません / the assessment role is missing or unknown: "
            f"{role!r}")
    if expected_role not in ASSESSMENT_ROLES:
        raise ProvenanceError(
            "固定記録の評価の役割が不明です / the freeze record has no valid assessment role: "
            f"{expected_role!r}")
    if role != expected_role:
        raise ProvenanceError(
            "評価の役割が固定記録と違います / the sealed assessment role differs from the freeze "
            f"record: sealed={role!r} frozen={expected_role!r}. Relabel the role only by starting a "
            "new experiment; never by editing a sealed file")


def _check_row_types(rows: list, fields: dict) -> set[str]:
    """行の型・分割・重複を確かめる / check each row's type, partition and uniqueness."""
    seen: set[str] = set()
    duplicates = []
    for row in rows:
        for field, kind in fields.items():
            if field not in row:
                raise ProvenanceError(
                    f"封印予測に {field} がありません / a sealed row has no {field!r}")
            value = row[field]
            if kind is bool:
                if not isinstance(value, bool):
                    raise ProvenanceError(
                        f"封印予測の {field} が真偽値ではありません / {field!r} is not a boolean")
            elif kind is float or kind == (int, float):
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    raise ProvenanceError(
                        f"封印予測の {field} が数値ではありません / {field!r} is not a number")
            elif not isinstance(value, kind):
                raise ProvenanceError(
                    f"封印予測の {field} の型が違います / {field!r} has the wrong type")
        if row["partition"] != "test":
            raise ProvenanceError(
                "封印予測に試験用以外の行があります / non-test rows in the sealed predictions")
        key = normalise_image_id(row["image"])
        if key in seen:
            duplicates.append(key)
        seen.add(key)
    if duplicates:
        raise ProvenanceError(
            "封印予測に同じ画像が複数行あります / duplicate image IDs in the sealed predictions: "
            f"{sorted(duplicates)[:5]}")
    return seen


def _validate(payload: dict, *, schema_version: int, expected: dict, manifest: dict,
              expected_role: str, fields: dict, threshold_key: str,
              threshold_value) -> list[dict]:
    if payload.get("schema_version") != schema_version:
        raise ProvenanceError(
            "封印予測の形式が古いです / stale sealed predictions: "
            f"schema_version={payload.get('schema_version')!r} (required {schema_version})")
    _check_experiment(payload.get("experiment", {}), expected)
    if payload.get("scored_partitions") != ["test"]:
        raise ProvenanceError(
            "封印予測には試験用だけを記録します / the sealed payload must score the test partition only")
    frozen = payload.get("frozen", {})
    if frozen.get(threshold_key) != threshold_value:
        raise ProvenanceError(
            "封印予測と固定記録のしきい値が違います / the sealed predictions used another threshold: "
            f"sealed={frozen.get(threshold_key)!r} frozen={threshold_value!r}")
    _check_assessment_role(frozen, expected_role)

    rows = payload.get("images")
    if not isinstance(rows, list) or not rows:
        raise ProvenanceError(
            "封印予測に画像の記録がありません / the sealed predictions contain no image rows")
    seen = _check_row_types(rows, fields)

    expected_images = test_partition(manifest)
    missing = sorted(expected_images - seen)
    unknown = sorted(seen - expected_images)
    if missing or unknown:
        raise ProvenanceError(
            "封印予測と分割記録が一致しません / the sealed predictions do not cover the test partition: "
            f"missing={missing[:5]} unknown={unknown[:5]}")
    return rows
