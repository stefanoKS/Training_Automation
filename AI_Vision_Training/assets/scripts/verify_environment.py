"""環境確認 / Environment verification.

このスクリプトは「いま使っている Python が正しい環境か」を確認します。
ノートブックでエラーが出たときの最初の切り分けに使います。

This script answers one question: "Is the Python environment I am using the right one?"
Run it first whenever a notebook fails.

使い方 / Usage
--------------
    python verify_environment.py                # 基本パッケージのみ確認 / base profile
    python verify_environment.py --profile yolo # YOLO 用も確認 / include YOLO
    python verify_environment.py --profile anomalib
    python verify_environment.py --profile all --json

終了コード / Exit codes
-----------------------
    0 : すべて利用可能 / everything required is importable
    1 : 不足あり / at least one required package is missing
"""

from __future__ import annotations

import argparse
import importlib
import json
import platform
import sys
from importlib import metadata
from pathlib import Path

# ---------------------------------------------------------------------------
# プロファイル定義 / profile definitions
# ---------------------------------------------------------------------------

PROFILES: dict[str, list[str]] = {
    "base": ["numpy", "matplotlib", "PIL", "pandas", "cv2", "skimage"],
    "yolo": ["torch", "torchvision", "ultralytics"],
    "anomalib": ["torch", "torchvision", "anomalib", "lightning", "kornia"],
    "course": ["jupyterlab", "ipykernel", "nbformat", "nbclient", "nbconvert"],
}

# import 名と PyPI 名が違うもの / packages whose import name differs from the PyPI name
DIST_NAME = {
    "PIL": "pillow",
    "cv2": "opencv-python",
    "skimage": "scikit-image",
}

MIN_PYTHON = (3, 10)


def _package_version(dist_name: str) -> str | None:
    try:
        return metadata.version(dist_name)
    except metadata.PackageNotFoundError:
        return None


def check_packages(profile: str) -> list[dict]:
    """1 プロファイル分のパッケージ状態を返す / check one profile."""
    results = []
    for module_name in PROFILES[profile]:
        dist_name = DIST_NAME.get(module_name, module_name)
        try:
            importlib.import_module(module_name)
            importable = True
            error = None
        except Exception as exc:                     # インストール済みでも import が失敗することがある
            importable = False
            error = f"{type(exc).__name__}: {exc}"
        version = _package_version(dist_name)
        results.append(
            {
                "module": module_name,
                "distribution": dist_name,
                "version": version,
                "importable": importable,
                "error": error,
            }
        )
    return results


def detect_device() -> dict:
    """GPU が使えるかを確認する。無くても失敗ではない。

    Report whether a CUDA GPU is usable. A missing GPU is NOT an error.
    """
    info = {"torch_installed": False, "cuda_available": False, "device_count": 0, "device_names": []}
    try:
        import torch
    except Exception:
        return info
    info["torch_installed"] = True
    try:
        info["cuda_available"] = bool(torch.cuda.is_available())
        info["device_count"] = int(torch.cuda.device_count())
        if info["cuda_available"]:
            info["device_names"] = [torch.cuda.get_device_name(i) for i in range(info["device_count"])]
    except Exception as exc:                         # pragma: no cover - driver specific
        info["error"] = str(exc)
    return info


def detect_backend_precision() -> str:
    """Matplotlib が画面なしでも動くか / confirm matplotlib can run headless."""
    import matplotlib

    return matplotlib.get_backend()


def check_project_assets(root: Path) -> list[dict]:
    """生成済みアセットがあるかを確認 / verify that generated assets exist."""
    expected = {
        "diagram (pixel grid)": root / "assets" / "diagrams" / "diagram_pixel_grid.png",
        "calibration image": root / "assets" / "diagrams" / "calibration_image.png",
        "normal samples": root / "assets" / "normal_samples",
        "defect samples": root / "assets" / "defect_samples",
        "yolo dataset": root / "assets" / "yolo_dataset" / "data.yaml",
        "anomaly dataset": root / "assets" / "anomaly_dataset" / "pvc_sheet",
    }
    return [
        {"name": name, "path": str(path), "exists": path.exists()}
        for name, path in expected.items()
    ]


def _profile_belongs_to_this_env(profile: str) -> bool:
    """このプロファイルが、いま使っている仮想環境のものかを判定する。

    The `anomalib` profile lives in `.venv-anomalib`; everything else lives in `.venv`.
    Running `--profile all` from `.venv` must therefore NOT report the Anomalib packages as
    "missing" — they are simply in the other environment.
    """
    wants_anomalib_env = profile == "anomalib"
    is_anomalib_env = "anomalib" in Path(sys.prefix).name.lower()
    return wants_anomalib_env == is_anomalib_env


def build_report(profile: str, root: Path) -> dict:
    if profile == "all":
        requested = list(PROFILES)
    elif profile in PROFILES:
        requested = [profile]
    else:
        requested = []

    relevant = [name for name in requested if _profile_belongs_to_this_env(name)]
    other_envs = [name for name in requested if name not in relevant]

    packages = {name: check_packages(name) for name in relevant}

    missing = [
        f"{entry['distribution']} ({profile_name})"
        for profile_name, entries in packages.items()
        for entry in entries
        if not entry["importable"]
    ]
    expected_env = ".venv-anomalib" if "anomalib" in Path(sys.prefix).name.lower() else ".venv"
    return {
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "executable": sys.executable,
            "prefix": sys.prefix,
            "is_virtualenv": sys.prefix != getattr(sys, "base_prefix", sys.prefix),
            "expected_environment": expected_env,
        },
        "platform": {"system": platform.system(), "release": platform.release(),
                     "machine": platform.machine()},
        "profiles": packages,
        "other_environments": other_envs,
        "device": detect_device(),
        "matplotlib_backend": detect_backend_precision(),
        "assets": check_project_assets(root),
        "missing": missing,
        "ok": not missing and sys.version_info[:2] >= MIN_PYTHON,
    }


def _print_human(report: dict) -> None:
    py = report["python"]
    print("=" * 66)
    print("ENVIRONMENT CHECK")
    print("=" * 66)
    print(f"Python        : {py['version']} ({py['implementation']})")
    print(f"Executable    : {py['executable']}")
    print(f"Virtual env   : {'yes' if py['is_virtualenv'] else 'NO  <-- check your kernel!'}")
    print(f"Platform      : {report['platform']['system']} {report['platform']['release']} "
          f"{report['platform']['machine']}")
    print(f"Matplotlib    : {report['matplotlib_backend']}")

    device = report["device"]
    if device["torch_installed"]:
        if device["cuda_available"]:
            print(f"GPU           : CUDA available ({', '.join(device['device_names'])})")
        else:
            print("GPU           : not available -> CPU mode (this is fine for Week 1)")
    else:
        print("GPU           : torch not installed in this environment")

    for profile_name, entries in report["profiles"].items():
        print(f"\n--- profile: {profile_name} ---")
        for entry in entries:
            if entry["importable"]:
                print(f"  [OK]   {entry['distribution']:<22} {entry['version']}")
            else:
                print(f"  [MISS] {entry['distribution']:<22} {entry['error']}")

    print("\n--- generated assets ---")
    for asset in report["assets"]:
        mark = "OK  " if asset["exists"] else "MISS"
        print(f"  [{mark}] {asset['name']:<22} {asset['path']}")

    if report["other_environments"]:
        print("\n--- other environments (not checked here) ---")
        print(f"  This interpreter belongs to: {report['python']['expected_environment']}")
        for name in report["other_environments"]:
            target = ".venv-anomalib" if name == "anomalib" else ".venv"
            print(f"  profile {name!r} lives in {target}; run this script there to check it.")

    print("\n" + "=" * 66)
    if report["ok"]:
        print("READY")
    else:
        print("NOT READY")
        for item in report["missing"]:
            print(f"  - missing: {item}")
        if sys.version_info[:2] < MIN_PYTHON:
            print(f"  - Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} or newer is required")
        print("\nSee docs/troubleshooting/installation.md for the fix steps.")
    print("=" * 66)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify the course Python environment.")
    parser.add_argument("--profile", default="base", choices=sorted(PROFILES) + ["all"])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = parser.parse_args(argv)

    report = build_report(args.profile, args.root.resolve())
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        _print_human(report)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
