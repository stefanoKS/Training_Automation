"""Generate missing clarity-review diagrams only; leave historical figures alone."""

from __future__ import annotations

import argparse
from pathlib import Path

from generate_svg_figures import AMBER, BLUE, GREEN, VIOLET, Canvas

ROOT = Path(__file__).resolve().parents[2]
FIELD_MM = 1300
WIDTHS_PX = (1300, 13000)
DEFECT_MM = 0.3
GRID_SIZE = 4
REGIONS = ((0, 0, 3, 3), (1, 1, 4, 4))


def fixed_fov() -> Canvas:
    c = Canvas("同じ視野・異なる尺度 / same field, different sampling", "calculated synthetic; not a detection guarantee")
    c.text(40, 83, f"対象平面の全幅 / full width at inspected plane = {FIELD_MM} mm", 22)
    for row, width_px in enumerate(WIDTHS_PX):
        y = 124 + row * 186
        scale = FIELD_MM / width_px
        span = DEFECT_MM / scale
        c.text(40, y, f"{width_px} px: {FIELD_MM}/{width_px} = {scale:g} mm/px", 22, BLUE)
        c.rect(40, y + 18, 780, 54, "#f6f8fa", BLUE)
        # Both strips have identical physical endpoints; drawn grid lines are schematic.
        divisions = width_px // 100
        for i in range(divisions + 1):
            x = 40 + 780 * i / divisions
            c.line(x, y + 18, x, y + 72, BLUE)
        c.text(40, y + 106, f"{DEFECT_MM:g} mm / {scale:g} mm/px = {span:g} px", 23, AMBER)
        c.text(40, y + 139, "1区間=100px、印は模式 / each interval=100px; mark not to scale", 18)
        # A labelled mark, not a false to-scale depiction of a subpixel feature.
        c.line(720, y + 30, 720, y + 60, AMBER)
        c.text(735, y + 52, "mark", 17, AMBER)
    c.line(40, 492, 820, 492, GREEN)
    for index in range(3):
        x = 40 + 780 * index / 2
        c.line(x, 484, x, 500, GREEN)
        c.text(max(40, x - 30), 526, f"{FIELD_MM * index / 2:g} mm", 18, GREEN)
    c.text(40, 550, "保存画像の拡大 ≠ 再撮影 / enlarging a saved image is not recapturing detail", 18)
    return c


def patch_overlap() -> Canvas:
    c = Canvas("比喩と特徴位置 / tile analogy versus feature locations", "schematic; region sizes are NOT actual CNN receptive fields")
    c.text(35, 83, "比喩：独立タイル / analogy: tiles", 22, AMBER)
    c.text(459, 83, "実際：重なる領域を要約 / actual: overlap", 22, BLUE)
    size, top = 56, 121
    for origin in (52, 489):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                c.rect(origin + col * size, top + row * size, size, size, "#f6f8fa")
        for i in range(GRID_SIZE):
            c.text(origin + i * size + 22, 111, str(i), 16)
            c.text(origin - 20, top + i * size + 32, str(i), 16)
    c.rect(52 + size, top + size, size, size, "none", AMBER)
    for (x1, y1, x2, y2), color in zip(REGIONS, (BLUE, VIOLET)):
        c.rect(489 + x1 * size, top + y1 * size, (x2 - x1) * size,
               (y2 - y1) * size, "none", color)
    c.text(35, 383, "タイルのRGB切出しではない", 21, AMBER)
    c.text(35, 416, "NOT literal disjoint RGB crops", 19, AMBER)
    c.text(459, 383, "共有画素 → 隣の特徴にも影響", 21, BLUE)
    c.text(459, 416, "Shared pixels affect both features.", 19, BLUE)
    for x, label, color in ((489, "f(0,0)", BLUE), (625, "f(1,1)", VIOLET)):
        c.rect(x, 438, 118, 34, "#f6f8fa", color)
        c.text(x + 21, 462, label, 19, color)
    c.text(459, 499, "CNN → 特徴マップの位置 → 数値列", 21)
    c.text(459, 534, "CNN -> feature location -> vector", 19)
    c.text(35, 489, "xは右、yは下 / x right, y down", 18)
    c.text(35, 524, "左上原点 / origin: top left", 18)
    return c


def batch_first_pass() -> Canvas:
    c = Canvas("まず一周を数える / first count one pass", "calculated schematic; 64 training images, batch=8")
    total, batch = 64, 8
    c.text(40, 84, f"{total} images / {batch} images per batch = {total // batch} batches", 23, BLUE)
    for row, start in enumerate(range(0, total, batch)):
        y = 110 + row * 49
        c.text(35, y + 29, f"batch {row + 1}", 20, BLUE)
        for col, image_id in enumerate(range(start, start + batch)):
            x = 170 + col * 80
            c.rect(x, y, 67, 39, "#e8f0ff", BLUE)
            c.text(x + 13, y + 27, str(image_id), 20)
    c.text(40, 519, "8行で1 epoch / eight rows = one epoch", 22)
    c.text(40, 548, "15 epochs = 15 passes; not a count of optimizer updates", 19, AMBER)
    return c


BUILDERS = {"teach_fixed_fov_sampling": fixed_fov, "teach_patch_overlap": patch_overlap,
            "teach_batch_first_pass": batch_first_pass}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    for name, builder in BUILDERS.items():
        builder().save(args.root, name)
        print(f"Generated {name}.svg and PNG fallback")


if __name__ == "__main__":
    main()
