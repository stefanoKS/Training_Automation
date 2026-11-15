"""Deterministic numerical sources for the editable teaching figures."""

from __future__ import annotations

import numpy as np

BBOX_IMAGE_SIZE = (240, 240)
BBOX_XYXY = (96, 72, 168, 132)
MASS_INPUTS = (1300.0, 2500.0, 0.35, 1.4)
CALIBRATION_REFERENCE = ((30, 190), (150, 190), 100.0)
CALIBRATION_CHECK = ((270, 60), (270, 120), 50.0)
CALIBRATION_TARGETS = ((60, 40, 85, 59), (150, 90, 187, 115))
PIXEL_THRESHOLD = 120
GRAY_EXAMPLE = ((40, 120, 121), (210, 40, 210))


def pixel_canvas() -> np.ndarray:
    canvas = np.zeros((5, 7), dtype=np.uint8)
    canvas[0, 0], canvas[0, 6], canvas[4, 0], canvas[2, 3] = 255, 200, 150, 100
    return canvas


def spot_mask(size: int) -> np.ndarray:
    yy, xx = np.mgrid[:size, :size]
    # Multiplication before division keeps integer centres exact (e.g. 110, not 110+epsilon).
    cx, cy, radius = size * 42 / 100, size * 55 / 100, size * 45 / 1000
    return (xx - cx) ** 2 + (yy - cy) ** 2 < radius ** 2


def mask_box(mask: np.ndarray) -> tuple[int, int, int, int]:
    ys, xs = np.nonzero(mask)
    if not len(xs):
        raise ValueError("Cannot bound an empty mask")
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def calibrated_defects() -> tuple[np.ndarray, dict]:
    """Ideal same-plane scene; coordinate spans, not tick-pixel counts, define lengths."""
    image = np.full((240, 320, 3), 210, dtype=np.uint8)
    for x1, y1, x2, y2 in CALIBRATION_TARGETS:
        image[y1:y2 + 1, x1:x2 + 1] = 40
    (rx1, ry), (rx2, _), reference_mm = CALIBRATION_REFERENCE
    (cx, cy1), (_, cy2), check_mm = CALIBRATION_CHECK
    image[ry:ry + 2, rx1:rx2 + 1] = (30, 90, 220)
    image[cy1:cy2 + 1, cx:cx + 2] = (30, 90, 220)
    scale = (rx2 - rx1) / reference_mm
    targets = [
        {"xyxy": [x1, y1, x2, y2],
         "area_px2": (x2 - x1) * (y2 - y1),
         "foreground_pixels": (x2 - x1 + 1) * (y2 - y1 + 1),
         "area_mm2": (x2 - x1) * (y2 - y1) / scale ** 2}
        for x1, y1, x2, y2 in CALIBRATION_TARGETS
    ]
    return image, {
        "image": "calibrated_defects.png", "provenance": "computed synthetic, ideal same plane",
        "reference_points": [[rx1, ry], [rx2, ry]], "reference_mm": reference_mm,
        "check_points": [[cx, cy1], [cx, cy2]], "check_mm": check_mm,
        "px_per_mm": scale, "threshold": 80, "targets": targets,
    }
