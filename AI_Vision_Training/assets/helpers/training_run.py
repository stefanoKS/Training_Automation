"""Explicit training-run handoff, with a visible timestamp fallback for older runs."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def save_training_run(course_root: Path, run_dir: Path, parameters: dict) -> Path:
    weights = (run_dir / "weights" / "best.pt").resolve()
    if not weights.is_file():
        raise FileNotFoundError(f"Training produced no best.pt: {weights}")
    manifest = course_root / "submissions" / "day04" / "training_run.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "weights": str(weights.relative_to(course_root.resolve())),
        "run_dir": str(run_dir.resolve().relative_to(course_root.resolve())),
        "parameters": parameters, "saved_at": datetime.now(timezone.utc).isoformat(),
    }
    manifest.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return manifest


def select_training_run(course_root: Path) -> tuple[Path, dict]:
    manifest = course_root / "submissions" / "day04" / "training_run.json"
    if manifest.is_file():
        record = json.loads(manifest.read_text(encoding="utf-8"))
        weights = (course_root / record["weights"]).resolve()
        if not weights.is_file():
            raise FileNotFoundError(f"Manifest points to missing weights: {weights}; rerun Day04_02")
        print("保存した学習を使用 / using saved training run:", manifest)
        print("学習設定 / training parameters:", record["parameters"])
        return weights, record
    candidates = sorted(
        (course_root / "training_results" / "day04").glob("*/weights/best.pt"),
        key=lambda path: (path.stat().st_mtime_ns, str(path)),
    )
    if not candidates:
        raise FileNotFoundError("No trained weights; run Day04_02 first")
    print("警告：記録がありません / WARNING: no run manifest.")
    print("更新時刻で選択（同時刻はパス順）/ selecting by mtime (path breaks ties):")
    for path in candidates:
        print(path, path.stat().st_mtime_ns)
    weights = candidates[-1]
    args_path = weights.parent.parent / "args.yaml"
    if args_path.is_file():
        print("保存された設定 / saved settings:\n", args_path.read_text(encoding="utf-8"))
    else:
        print("学習設定は不明 / training parameters unavailable; verify the run before reporting.")
    return weights, {"selection": "mtime fallback", "weights": str(weights)}
