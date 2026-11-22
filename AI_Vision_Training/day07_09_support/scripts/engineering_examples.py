"""Reference calculations used by the Day 7-9 lessons and their tests.

All numbers are hypothetical teaching examples. Keeping the arithmetic in one
place lets the tests prove that the manuscripts, diagrams and simulators agree.
"""

from __future__ import annotations

import math

DECISIONS = ("ACCEPT_OK", "ACCEPT_NG", "HOLD", "REJECT_DUPLICATE", "REJECT_STALE")


def roller_circumference_mm(diameter_mm: float) -> float:
    if diameter_mm <= 0:
        raise ValueError("diameter must be positive")
    return math.pi * diameter_mm


def roller_surface_speed_m_per_min(diameter_mm: float, rpm: float) -> float:
    if rpm < 0:
        raise ValueError("rpm must not be negative")
    return roller_circumference_mm(diameter_mm) * rpm / 1000


def pixel_scale_mm_per_px(fov_mm: float, horizontal_pixels: int) -> float:
    if fov_mm <= 0 or horizontal_pixels <= 0:
        raise ValueError("field of view and pixel count must be positive")
    return fov_mm / horizontal_pixels


def line_rate_lines_per_s(speed_m_per_min: float, sampling_mm_per_line: float) -> float:
    if speed_m_per_min < 0 or sampling_mm_per_line <= 0:
        raise ValueError("speed must not be negative and sampling must be positive")
    return (speed_m_per_min * 1000 / 60) / sampling_mm_per_line


def image_data_rate_bytes_s(pixels_per_line: int, lines_per_s: float, bytes_per_pixel: int = 1) -> float:
    if min(pixels_per_line, lines_per_s, bytes_per_pixel) <= 0:
        raise ValueError("all image-rate inputs must be positive")
    return pixels_per_line * lines_per_s * bytes_per_pixel


def travel_mm(speed_m_per_s: float, latency_s: float) -> float:
    if speed_m_per_s < 0 or latency_s < 0:
        raise ValueError("speed and latency must not be negative")
    return speed_m_per_s * latency_s * 1000


def scale_linear(value: float, in_min: float, in_max: float,
                 physical_min: float, physical_max: float) -> float:
    if in_max == in_min:
        raise ValueError("electrical range must have non-zero span")
    if not in_min <= value <= in_max:
        raise ValueError("value outside the electrical range")
    fraction = (value - in_min) / (in_max - in_min)
    return physical_min + fraction * (physical_max - physical_min)


def encoder_counts_per_turn(ppr: int, decode: int = 4) -> int:
    if decode not in (1, 2, 4):
        raise ValueError("decode must be 1, 2 or 4")
    if ppr <= 0:
        raise ValueError("ppr must be positive")
    return ppr * decode


def encoder_deg_per_count(ppr: int, decode: int = 4) -> float:
    return 360.0 / encoder_counts_per_turn(ppr, decode)


def encoder_mm_per_count(diameter_mm: float, ppr: int, decode: int = 4) -> float:
    return roller_circumference_mm(diameter_mm) / encoder_counts_per_turn(ppr, decode)


def on_delay(input_on: bool, elapsed_ms: float, preset_ms: float) -> tuple[bool, float]:
    if input_on and elapsed_ms >= preset_ms:
        return True, preset_ms
    return False, (elapsed_ms if input_on else 0.0)


def counter_step(count: int, rising_edge: bool, preset: int, reset: bool) -> tuple[int, bool]:
    if reset:
        return 0, False
    next_count = count + 1 if rising_edge else count
    return next_count, next_count >= preset


def decide_result(kind: str, result_id: int, valid: bool = True,
                  last_accepted_id: int | None = None) -> str:
    """Mirror of the browser simulator's result protocol."""
    if result_id < 1:
        raise ValueError("result id must be positive")
    if kind in ("TIMEOUT", "INVALID") or not valid:
        return "HOLD"
    if last_accepted_id is not None and result_id < last_accepted_id:
        return "REJECT_STALE"
    if kind == "STALE":
        return "REJECT_STALE"
    if last_accepted_id is not None and result_id == last_accepted_id:
        return "REJECT_DUPLICATE"
    if kind == "DUPLICATE":
        return "REJECT_DUPLICATE"
    if kind == "OK":
        return "ACCEPT_OK"
    if kind == "NG":
        return "ACCEPT_NG"
    return "HOLD"


if __name__ == "__main__":
    print("roller 100 mm @ 100 rpm:", round(roller_surface_speed_m_per_min(100, 100), 3), "m/min")
    print("pixel scale 600/4096:", round(pixel_scale_mm_per_px(600, 4096), 6), "mm/px")
    print("line rate 30 m/min @ 0.2 mm:", line_rate_lines_per_s(30, 0.2), "lines/s")
    print("data rate:", image_data_rate_bytes_s(4096, 2500), "bytes/s")
    print("travel 0.5 m/s @ 0.12 s:", travel_mm(0.5, 0.12), "mm")
