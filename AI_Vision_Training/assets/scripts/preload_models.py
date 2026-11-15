"""Preflight downloads only; offline mode checks caches without constructing models."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("yolo", "anomalib"), required=True)
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    if args.profile == "yolo":
        from ultralytics import YOLO
        from ultralytics.utils import ASSETS
        from ultralytics.utils.downloads import download

        directory = root / "assets" / "models"
        directory.mkdir(parents=True, exist_ok=True)
        weights = directory / "yolo26n.pt"
        bus = Path(ASSETS) / "bus.jpg"
        if not args.offline:
            YOLO(str(weights))
            if not bus.is_file():
                download("https://ultralytics.com/images/bus.jpg", dir=Path(ASSETS))
        required = [weights, bus]
    else:
        import timm
        import torch
        from timm.models import get_pretrained_cfg
        from timm.models._hub import check_cached_file

        # Force timm's URL cache, not Hugging Face: the classroom must not query a hub.
        config = get_pretrained_cfg("resnet18")
        if config is None or not config.url:
            raise RuntimeError("Installed timm has no resnet18 URL configuration")
        cache = Path(torch.hub.get_dir()) / "checkpoints" / config.url.rsplit("/", 1)[-1]
        if not args.offline:
            timm.create_model("resnet18", pretrained=True, pretrained_cfg_overlay={"hf_hub_id": None})
        if not check_cached_file(config.url):
            raise FileNotFoundError(f"resnet18 URL cache missing or invalid: {cache}")
        required = [cache]
    missing = [str(path) for path in required if not path.is_file() or path.stat().st_size == 0]
    if missing:
        raise FileNotFoundError("Offline model inputs missing:\n" + "\n".join(missing))
    for path in required:
        print("READY:", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
