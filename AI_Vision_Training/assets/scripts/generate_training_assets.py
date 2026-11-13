"""教材用アセット生成 / Course asset generator.

このスクリプトは研修で使う「図」と「サンプル画像」をすべてローカルで生成します。
外部から画像をダウンロードしません。ネットワークが無くても再現できます。

This script renders every diagram and sample image used by the course, entirely
locally. Nothing is downloaded, so the assets are reproducible offline.

使い方 / Usage
--------------
    python generate_training_assets.py
    python generate_training_assets.py --root ..\\..
    python generate_training_assets.py --seed 2026 --clean

出力先 / Outputs
----------------
    assets/diagrams/*.png          ... 概念図 / concept diagrams
    assets/normal_samples/*.png    ... 正常例 / normal examples
    assets/defect_samples/*.png    ... 欠陥例 + マスク / defect examples + masks
"""

from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # 画面の無い環境でも保存できるようにする / allow headless rendering

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager, patches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pvc_synth as ps  # noqa: E402  (パス追加後に読み込む / loaded after sys.path tweak)

DPI = 130
ACCENT = "#1f6feb"
DANGER = "#d1242f"
OK_GREEN = "#1a7f37"
INK = "#24292f"
MUTED = "#57606a"


# ---------------------------------------------------------------------------
# 日本語フォントの設定 / Japanese font configuration
# ---------------------------------------------------------------------------


def configure_matplotlib() -> str:
    """日本語が表示できるフォントを選ぶ。見つからなければ英語ラベルに切り替える。

    Pick a font that can render Japanese. Returns the selected family name.
    """
    candidates = [
        Path("C:/Windows/Fonts/NotoSansJP-Regular.ttf"),
        Path("C:/Windows/Fonts/YuGothR.ttc"),
        Path("C:/Windows/Fonts/meiryo.ttc"),
        Path("C:/Windows/Fonts/msgothic.ttc"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
        Path("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"),
    ]
    for path in candidates:
        if path.exists():
            try:
                font_manager.fontManager.addfont(str(path))
                family = font_manager.FontProperties(fname=str(path)).get_name()
                plt.rcParams["font.family"] = [family, "DejaVu Sans"]
                plt.rcParams["axes.unicode_minus"] = False
                return family
            except Exception:  # pragma: no cover - font problems must not stop the build
                continue
    plt.rcParams["font.family"] = ["DejaVu Sans"]
    return "DejaVu Sans"


# ---------------------------------------------------------------------------
# 共通ヘルパ / shared helpers
# ---------------------------------------------------------------------------


def _blank_axes(figsize: tuple[float, float]):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color("#d0d7de")
    return fig, ax


def _show_rgb(ax, image: np.ndarray, **kwargs) -> None:
    ax.imshow(np.clip(image, 0, 255).astype(np.uint8), **kwargs)
    ax.set_xticks([])
    ax.set_yticks([])


def _save(fig, path: Path, title: str | None = None) -> Path:
    if title:
        fig.suptitle(title, fontsize=13, color=INK)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def _arrow(ax, start, end, color=ACCENT, width=1.6):
    ax.add_patch(
        FancyArrowPatch(start, end, arrowstyle="->", mutation_scale=14, color=color, linewidth=width)
    )


# ---------------------------------------------------------------------------
# 図 1-3: ピクセルと座標 / pixels and coordinates
# ---------------------------------------------------------------------------


def diagram_pixel_grid(out: Path) -> Path:
    """8x8 の画素を拡大し、座標と値を可視化する / magnified 8x8 pixel grid."""
    rng = np.random.default_rng(7)
    small = ps.make_base_surface(8, 8, rng, grain_strength=9.0)
    small[2:4, 5:7] *= 0.35                     # 暗い画素のかたまり / a darker patch
    gray = small.mean(axis=2)

    fig, (ax_img, ax_grid) = plt.subplots(1, 2, figsize=(10.5, 4.6), gridspec_kw={"width_ratios": [1, 1.35]})
    _show_rgb(ax_img, small)
    ax_img.set_title("$\\it{Original}$ 8x8 image", fontsize=11, color=MUTED)

    ax_grid.imshow(gray, cmap="gray", vmin=0, vmax=255)
    for i in range(9):
        ax_grid.axhline(i - 0.5, color="#8c959f", linewidth=0.6)
        ax_grid.axvline(i - 0.5, color="#8c959f", linewidth=0.6)
    for row in range(8):
        for col in range(8):
            value = int(round(gray[row, col]))
            ax_grid.text(
                col, row, str(value), ha="center", va="center", fontsize=7.5,
                color="white" if value < 128 else "#24292f",
            )
    ax_grid.set_title("$\\it{Zoomed}$: each square = 1 pixel, number = brightness (0-255)", fontsize=11, color=MUTED)
    ax_grid.set_xlabel("x  (column index ->)")
    ax_grid.set_ylabel("y  (row index ->)")
    ax_grid.set_xticks(range(0, 8, 2))
    ax_grid.set_yticks(range(0, 8, 2))
    ax_grid.tick_params(labelsize=8, colors=MUTED)
    return _save(fig, out, "A digital image is a grid of numbers")


def diagram_grayscale_values(out: Path) -> Path:
    """0-255 の濃淡と数値の対応 / relationship between brightness and numbers."""
    fig = plt.figure(figsize=(10.5, 4.4))
    ax_bar = fig.add_axes([0.08, 0.62, 0.84, 0.16])
    gradient = np.linspace(0, 255, 256).reshape(1, -1)
    ax_bar.imshow(gradient, cmap="gray", aspect="auto", extent=[0, 255, 0, 1])
    ax_bar.set_yticks([])
    ax_bar.set_xticks([0, 32, 64, 96, 128, 160, 192, 224, 255])
    ax_bar.tick_params(labelsize=8, colors=MUTED)
    ax_bar.set_title("0 = black,  255 = white", fontsize=10, color=MUTED)

    ax_grid = fig.add_axes([0.08, 0.06, 0.84, 0.42])
    values = np.array([[0, 32, 64, 96, 128, 160], [192, 208, 224, 240, 248, 255]])
    ax_grid.imshow(values, cmap="gray", vmin=0, vmax=255)
    for row in range(values.shape[0]):
        for col in range(values.shape[1]):
            value = int(values[row, col])
            ax_grid.text(
                col, row, str(value), ha="center", va="center", fontsize=12,
                color="white" if value < 128 else "#24292f",
            )
    ax_grid.set_xticks([])
    ax_grid.set_yticks([])
    for spine in ax_grid.spines.values():
        spine.set_visible(False)
    return _save(fig, out, "Grayscale: one number per pixel")


def diagram_coordinate_system(out: Path) -> Path:
    """画像座標系（左上が原点、y は下向き）/ image coordinate system."""
    rng = np.random.default_rng(11)
    image = ps.render_normal(160, 220, seed=11)
    fig, ax = _blank_axes((8.4, 5.0))
    _show_rgb(ax, image)
    _arrow(ax, (0, -8), (110, -8), color=ACCENT)
    _arrow(ax, (-10, 0), (-10, 90), color=DANGER)
    ax.text(112, -9, "x (width)", color=ACCENT, fontsize=10, va="center")
    ax.text(-12, 94, "y (height)", color=DANGER, fontsize=10, ha="center")

    points = [(20, 30), (80, 45), (150, 120), (196, 24)]
    for idx, (x, y) in enumerate(points, start=1):
        ax.plot(x, y, marker="o", markersize=7, color="#bf3989", markeredgecolor="white")
        ax.annotate(f"({x}, {y})", (x, y), textcoords="offset points", xytext=(8, -12),
                    fontsize=9, color="#24292f")
    ax.plot(0, 0, marker="s", markersize=6, color=INK)
    ax.annotate("origin (0, 0)\ntop-left corner", (0, 0), textcoords="offset points", xytext=(10, 16),
                fontsize=9, color=INK)
    ax.set_xlim(-24, 250)
    ax.set_ylim(160, -26)
    return _save(fig, out, "Image coordinates: origin at top-left, y increases downward")


# ---------------------------------------------------------------------------
# 図 4-8: コンピュータビジョンのタスク / computer-vision tasks
# ---------------------------------------------------------------------------


def _demo_defective(size: int = 220, seed: int = 4242):
    return ps.render_defective(size, size, seed, ("black_spot", "scratch", "streak"), count=3)


def diagram_classification(out: Path) -> Path:
    """画像全体を 1 つのラベルに分類 / whole-image classification."""
    image, _, defects = _demo_defective(seed=4242)
    fig, (ax_img, ax_txt) = plt.subplots(1, 2, figsize=(9.6, 4.2), gridspec_kw={"width_ratios": [1, 1]})
    _show_rgb(ax_img, image)
    ax_img.set_title("Input image", fontsize=10, color=MUTED)

    ax_txt.axis("off")
    ax_txt.add_patch(FancyBboxPatch((0.12, 0.56), 0.76, 0.22, boxstyle="round,pad=0.02",
                                    linewidth=2, edgecolor=DANGER, facecolor="#ffebe9"))
    ax_txt.text(0.5, 0.67, "NG", ha="center", va="center", fontsize=26, color=DANGER, fontweight="bold")
    ax_txt.add_patch(FancyBboxPatch((0.12, 0.16), 0.76, 0.22, boxstyle="round,pad=0.02",
                                    linewidth=1.2, edgecolor=MUTED, facecolor="#f6f8fa"))
    ax_txt.text(0.5, 0.27, "confidence 0.88", ha="center", va="center", fontsize=12, color=MUTED)
    _arrow(ax_txt, (0.5, 0.50), (0.5, 0.42), color=MUTED)
    ax_txt.text(0.5, 0.95, "1 image  ->  1 answer", ha="center", fontsize=12, color=INK)
    ax_txt.text(0.5, 0.04, "(where is the defect? -> unknown)", ha="center", fontsize=9, color=MUTED)
    return _save(fig, out, "Image classification")


def diagram_detection(out: Path) -> Path:
    """バウンディングボックスによる物体検出 / bounding-box object detection."""
    image, _, defects = _demo_defective(seed=4242)
    fig, ax = _blank_axes((7.0, 6.4))
    _show_rgb(ax, image)
    colors = {"black_spot": DANGER, "scratch": ACCENT, "streak": "#8250df", "irregular_mark": OK_GREEN}
    for idx, defect in enumerate(defects):
        x1, y1, x2, y2 = defect.bbox
        color = colors.get(defect.cls, ACCENT)
        ax.add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False, edgecolor=color, linewidth=2))
        ax.text(x1, max(y1 - 5, 10), f"{defect.cls} {0.95 - 0.07 * idx:.2f}", color=color,
                fontsize=9, fontweight="bold",
                bbox=dict(facecolor="white", edgecolor=color, boxstyle="round,pad=0.18", linewidth=0.8))
    return _save(fig, out, "Object detection: where + what")


def diagram_segmentation(out: Path) -> Path:
    """画素単位のマスク / pixel-level mask."""
    image, mask, _ = _demo_defective(seed=4242)
    overlay = image.copy()
    overlay[mask > 0] = overlay[mask > 0] * 0.25 + np.array([255, 60, 60]) * 0.75

    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.4))
    _show_rgb(axes[0], image)
    axes[0].set_title("Input", fontsize=10, color=MUTED)
    axes[1].imshow(mask, cmap="gray", vmin=0, vmax=255)
    axes[1].set_title("Defect mask (pixels)", fontsize=10, color=MUTED)
    axes[1].set_xticks([]); axes[1].set_yticks([])
    _show_rgb(axes[2], overlay)
    axes[2].set_title("Overlay", fontsize=10, color=MUTED)
    return _save(fig, out, "Semantic segmentation: every defect pixel is marked")


def diagram_instance_segmentation(out: Path) -> Path:
    """インスタンスごとに色分け / per-instance colouring."""
    image, mask, defects = _demo_defective(seed=4242)
    fig, ax = _blank_axes((7.0, 6.4))
    _show_rgb(ax, image)
    palette = ["#d1242f", "#1f6feb", "#8250df"]
    palette_rgb = [(209, 36, 47), (31, 111, 235), (130, 80, 223)]
    for idx, defect in enumerate(defects):
        x1, y1, x2, y2 = defect.bbox
        local = mask[y1:y2, x1:x2]
        # 各インスタンスを個別の色で塗る（簡易表現） / paint each instance with its own colour
        tint = np.zeros((y2 - y1, x2 - x1, 3), dtype=np.float32)
        tint[:, :] = palette_rgb[idx % len(palette_rgb)]
        alpha = (local.astype(np.float32) / 255.0)[..., None] * 0.7
        region = image[y1:y2, x1:x2] * (1 - alpha) + tint * alpha
        image[y1:y2, x1:x2] = region
        ax.text(x1, max(y1 - 5, 10), f"instance {idx + 1}", color=palette[idx % len(palette)],
                fontsize=9, fontweight="bold")
    _show_rgb(ax, image)
    return _save(fig, out, "Instance segmentation: which pixel belongs to which defect")


def diagram_anomaly_heatmap(out: Path) -> Path:
    """異常スコアのヒートマップ（概念図）/ anomaly-score heatmap (conceptual)."""
    image, mask, _ = _demo_defective(seed=4242)
    score = ps.gaussian_blur(mask.astype(np.float64) / 255.0, sigma=6.0)
    score = score / max(score.max(), 1e-9)

    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.4))
    _show_rgb(axes[0], image)
    axes[0].set_title("Input", fontsize=10, color=MUTED)
    im = axes[1].imshow(score, cmap="inferno", vmin=0, vmax=1)
    axes[1].set_title("Anomaly score map", fontsize=10, color=MUTED)
    axes[1].set_xticks([]); axes[1].set_yticks([])
    fig.colorbar(im, ax=axes[1], fraction=0.046, pad=0.02)
    _show_rgb(axes[2], image)
    axes[2].imshow(score, cmap="inferno", alpha=0.55, vmin=0, vmax=1)
    axes[2].set_title("Heatmap overlay", fontsize=10, color=MUTED)
    return _save(fig, out, "Anomaly detection: a score map, not a label")


# ---------------------------------------------------------------------------
# 図 9: 制御フロー / control flow
# ---------------------------------------------------------------------------


def diagram_control_flow(out: Path) -> Path:
    """if / else の流れ / flowchart of an if-else decision."""
    fig, ax = _blank_axes((8.6, 5.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    box = dict(boxstyle="round,pad=0.4", linewidth=1.4)

    ax.add_patch(FancyBboxPatch((3.1, 4.9), 3.8, 0.95, edgecolor=MUTED, facecolor="#f6f8fa", **box))
    ax.text(5.0, 5.38, "measured_width = 100.3", ha="center", va="center", fontsize=11, color=INK)

    ax.add_patch(patches.Polygon([(5.0, 4.45), (7.15, 3.55), (5.0, 2.65), (2.85, 3.55)],
                                 closed=True, edgecolor=ACCENT, facecolor="#ddf4ff", linewidth=1.6))
    ax.text(5.0, 3.55, "|100.3 - 100| <= 0.5 ?", ha="center", va="center", fontsize=10.5, color=INK)

    ax.add_patch(FancyBboxPatch((0.45, 1.0), 3.0, 0.95, edgecolor=OK_GREEN, facecolor="#dafbe1", **box))
    ax.text(1.95, 1.47, "result = \"OK\"", ha="center", va="center", fontsize=11, color=OK_GREEN)
    ax.add_patch(FancyBboxPatch((6.55, 1.0), 3.0, 0.95, edgecolor=DANGER, facecolor="#ffebe9", **box))
    ax.text(8.05, 1.47, "result = \"NG\"", ha="center", va="center", fontsize=11, color=DANGER)

    _arrow(ax, (5.0, 4.9), (5.0, 4.45))
    _arrow(ax, (2.85, 3.55), (1.95, 3.55), color=OK_GREEN)
    _arrow(ax, (1.95, 3.55), (1.95, 1.95), color=OK_GREEN)
    _arrow(ax, (7.15, 3.55), (8.05, 3.55), color=DANGER)
    _arrow(ax, (8.05, 3.55), (8.05, 1.95), color=DANGER)
    ax.text(2.25, 3.75, "True", fontsize=10, color=OK_GREEN)
    ax.text(7.35, 3.75, "False", fontsize=10, color=DANGER)
    ax.text(5.0, 0.35, "Only ONE branch runs. The other is skipped.",
            ha="center", fontsize=10, color=MUTED)
    return _save(fig, out, "if / else: choosing one path")


# ---------------------------------------------------------------------------
# 図 10: データ分割 / dataset split
# ---------------------------------------------------------------------------


def diagram_dataset_split(out: Path) -> Path:
    """訓練・検証・試験の分離 / train-validation-test separation."""
    fig, ax = _blank_axes((10.0, 4.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.6)

    specs = [
        (0.35, "Training set", "学習", "70%", "#ddf4ff", ACCENT),
        (3.55, "Validation set", "検証", "15%", "#fff8c5", "#9a6700"),
        (6.75, "Test set", "試験", "15%", "#dafbe1", OK_GREEN),
    ]
    for x, en, ja, pct, face, edge in specs:
        ax.add_patch(FancyBboxPatch((x, 1.05), 2.9, 2.25, boxstyle="round,pad=0.05",
                                    edgecolor=edge, facecolor=face, linewidth=1.8))
        ax.text(x + 1.45, 2.85, en, ha="center", fontsize=11.5, color=edge, fontweight="bold")
        ax.text(x + 1.45, 2.35, ja, ha="center", fontsize=13, color=edge)
        ax.text(x + 1.45, 1.60, pct, ha="center", fontsize=20, color=edge, fontweight="bold")

    ax.text(5.0, 0.55, "The three sets must never share the same image.",
            ha="center", fontsize=10.5, color=MUTED)
    ax.text(5.0, 0.15, "An image in the test set was NOT used for training.",
            ha="center", fontsize=10.5, color=MUTED)
    for x in (3.15, 6.35):
        ax.plot([x, x], [1.0, 3.4], linestyle=":", color="#8c959f", linewidth=1.5)
    return _save(fig, out, "Why we split the data")


# ---------------------------------------------------------------------------
# 図 11-12: YOLO 注釈と距離 / YOLO annotation and pixel distance
# ---------------------------------------------------------------------------


def diagram_yolo_annotation(out: Path) -> Path:
    """YOLO 形式の座標計算 / YOLO normalised coordinates."""
    width = height = 240
    image = ps.render_normal(height, width, seed=99)
    bbox = (96, 72, 168, 132)
    x1, y1, x2, y2 = bbox
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

    fig, ax = _blank_axes((7.2, 6.6))
    _show_rgb(ax, image)
    ax.add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False, edgecolor=DANGER, linewidth=2))
    ax.plot([cx], [cy], marker="+", markersize=14, color=ACCENT, markeredgewidth=2)
    ax.annotate("", xy=(cx, y2 + 16), xytext=(cx, y1 - 4),
                arrowprops=dict(arrowstyle="<->", color=ACCENT, linewidth=1.2))
    ax.annotate("", xy=(x1 - 4, cy), xytext=(x2 + 16, cy),
                arrowprops=dict(arrowstyle="<->", color=ACCENT, linewidth=1.2))
    ax.text(cx + 6, y2 + 20, f"w = {x2 - x1} px", fontsize=9, color=ACCENT)
    ax.text(x1 - 6, y1 - 8, f"h = {y2 - y1} px", fontsize=9, color=ACCENT, ha="right")
    ax.text(x2 + 20, cy - 6, f"center ({cx:.0f}, {cy:.0f})", fontsize=9, color=ACCENT)

    formula = (
        "x_center = 132 / 240 = 0.550\n"
        "y_center = 102 / 240 = 0.425\n"
        "width    =  72 / 240 = 0.300\n"
        "height   =  60 / 240 = 0.250\n\n"
        "label file line:\n"
        "0 0.550 0.425 0.300 0.250"
    )
    ax.text(1.06, 0.98, formula, transform=ax.transAxes, va="top", ha="left", fontsize=9.5,
            family="DejaVu Sans Mono", color=INK,
            bbox=dict(facecolor="#f6f8fa", edgecolor="#d0d7de", boxstyle="round,pad=0.5"))
    ax.set_xlim(0, width)
    ax.set_ylim(height, 0)
    return _save(fig, out, "YOLO annotation: normalised centre, width, height")


def diagram_pixel_distance(out: Path) -> Path:
    """2 点間距離と三平方の定理 / distance between two points."""
    fig, ax = _blank_axes((7.4, 5.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    p1, p2 = (1.6, 5.4), (7.6, 1.8)
    ax.plot(*p1, marker="o", markersize=9, color=DANGER)
    ax.plot(*p2, marker="o", markersize=9, color=ACCENT)
    ax.text(p1[0], p1[1] + 0.38, "point A (x1, y1)", fontsize=10, color=DANGER, ha="center")
    ax.text(p2[0], p2[1] - 0.55, "point B (x2, y2)", fontsize=10, color=ACCENT, ha="center")
    ax.plot([p1[0], p2[0]], [p1[1], p1[1]], linestyle="--", color=MUTED, linewidth=1.4)
    ax.plot([p2[0], p2[0]], [p1[1], p2[1]], linestyle="--", color=MUTED, linewidth=1.4)
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=INK, linewidth=2.2)
    ax.text((p1[0] + p2[0]) / 2, p1[1] + 0.22, "dx = x2 - x1", fontsize=10, color=MUTED, ha="center")
    ax.text(p2[0] + 0.18, (p1[1] + p2[1]) / 2, "dy = y2 - y1", fontsize=10, color=MUTED,
            rotation=90, va="center")
    ax.text((p1[0] + p2[0]) / 2 - 1.9, (p1[1] + p2[1]) / 2 + 0.2, "distance", fontsize=11,
            color=INK, rotation=-30)
    ax.text(5.0, 6.55, "distance (pixels) = sqrt(dx*dx + dy*dy)", fontsize=13, color=INK, ha="center")
    return _save(fig, out, "Euclidean distance between two points")


def diagram_calibration_concept(out: Path) -> Path:
    """カメラ距離とスケールの関係 / camera distance changes the scale."""
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.3))
    for ax, px_len, label in zip(axes, (120, 240), ("camera far", "camera near")):
        ax.set_xlim(0, 300)
        ax.set_ylim(0, 160)
        ax.plot([90, 90 + px_len], [80, 80], color=DANGER, linewidth=4, solid_capstyle="round")
        ax.plot([90, 90], [70, 90], color=INK, linewidth=1.5)
        ax.plot([90 + px_len, 90 + px_len], [70, 90], color=INK, linewidth=1.5)
        ax.text(90 + px_len / 2, 96, f"{px_len} px", ha="center", fontsize=11, color=DANGER)
        ax.text(150, 30, "the SAME 100 mm reference bar", ha="center", fontsize=10, color=MUTED)
        ax.set_title(label, fontsize=11, color=INK)
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("#d0d7de")
    axes[0].text(90 + 60, 118, "1.20 px/mm", ha="center", fontsize=10, color=ACCENT)
    axes[1].text(90 + 120, 118, "2.40 px/mm", ha="center", fontsize=10, color=ACCENT)
    return _save(fig, out, "Calibration must be done at the real camera distance")


# ---------------------------------------------------------------------------
# 図 13-15: PatchCore と比較 / PatchCore and comparison
# ---------------------------------------------------------------------------


def diagram_patchcore_concept(out: Path) -> Path:
    """PatchCore の考え方 / the PatchCore idea."""
    fig, ax = _blank_axes((10.4, 5.0))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.5)

    def stage(x, title, ja, color):
        ax.add_patch(FancyBboxPatch((x, 3.20), 2.0, 1.85, boxstyle="round,pad=0.06",
                                    edgecolor=color, facecolor="white", linewidth=1.8))
        ax.text(x + 1.0, 4.85, title, ha="center", fontsize=10, color=color, fontweight="bold")
        ax.text(x + 1.0, 4.55, ja, ha="center", fontsize=10, color=color)

    stage(0.35, "1. Split", "分割", MUTED)
    for i in range(3):
        for j in range(3):
            ax.add_patch(Rectangle((0.60 + i * 0.58, 3.38 + j * 0.30), 0.56, 0.28,
                                   facecolor="#eaeef2", edgecolor="#afb8c1", linewidth=0.8))
    stage(3.0, "2. Features", "特徴", ACCENT)
    for i in range(3):
        ax.text(3.25, 4.12 - i * 0.35, f"[{i}.14  {i}.73  {i}.08]", family="DejaVu Sans Mono",
                fontsize=8.5, color=ACCENT)
    stage(5.65, "3. Memory bank", "記憶", "#8250df")
    ax.text(6.65, 4.12, "normal patches\nonly", ha="center", va="center", fontsize=9.5, color="#8250df")
    ax.text(6.65, 3.48, "stored once", ha="center", fontsize=8.5, color=MUTED)
    stage(8.3, "4. Score", "評価", DANGER)
    ax.text(9.3, 4.12, "nearest\nneighbour", ha="center", va="center", fontsize=9.5, color=DANGER)
    ax.text(9.3, 3.48, "distance=score", ha="center", fontsize=8.5, color=MUTED)

    for x in (2.42, 5.07, 7.72):
        _arrow(ax, (x, 4.10), (x + 0.52, 4.10), color=MUTED)
    ax.text(5.5, 1.55, "Training images are ALL normal. No defect labels are needed.",
            ha="center", fontsize=10.5, color=INK)
    ax.text(5.5, 1.00, "A large distance to every stored normal patch => suspicious region.",
            ha="center", fontsize=9.5, color=MUTED)
    return _save(fig, out, "PatchCore: comparing local patches with normal patches")


def diagram_yolo_vs_patchcore(out: Path) -> Path:
    """YOLO と PatchCore の違い / YOLO vs PatchCore."""
    fig, ax = _blank_axes((11.0, 5.6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.2)
    rows = [
        ("Needs defect labels?", "Yes (bounding boxes)", "No (normal images)"),
        ("Output", "box + class + confidence", "score + heatmap"),
        ("Says WHAT the defect is", "Yes", "Usually no"),
        ("Finds unseen defect types", "Only learned classes", "More likely, but not guaranteed"),
        ("Typical use", "known defects, counting", "surface anomaly screening"),
    ]
    ax.text(1.55, 5.55, "Topic", fontsize=11, color=MUTED, fontweight="bold")
    ax.text(5.1, 5.55, "YOLO (supervised)", fontsize=11, color=ACCENT, fontweight="bold")
    ax.text(8.75, 5.55, "PatchCore (anomaly)", fontsize=11, color="#8250df", fontweight="bold")
    for idx, (topic, yolo, patch) in enumerate(rows):
        y = 4.75 - idx * 0.85
        ax.plot([0.2, 10.8], [y + 0.42, y + 0.42], color="#eaeef2", linewidth=1)
        ax.text(0.25, y, topic, fontsize=9.5, color=INK)
        ax.text(4.55, y, yolo, fontsize=9.5, color=ACCENT)
        ax.text(8.2, y, patch, fontsize=9.5, color="#8250df")
    ax.plot([3.6, 3.6], [0.5, 5.9], color="#d0d7de", linewidth=1)
    ax.plot([7.9, 7.9], [0.5, 5.9], color="#d0d7de", linewidth=1)
    return _save(fig, out, "Two different answers to two different questions")


# ---------------------------------------------------------------------------
# サンプル画像 / sample images
# ---------------------------------------------------------------------------


def build_samples(assets: Path, seed: int) -> dict:
    """正常例と欠陥例を保存する / write normal and defective sample images."""
    normal_dir = assets / "normal_samples"
    defect_dir = assets / "defect_samples"
    normal_dir.mkdir(parents=True, exist_ok=True)
    defect_dir.mkdir(parents=True, exist_ok=True)

    written: list[str] = []
    for idx in range(4):
        image = ps.render_normal(240, 320, seed=seed + 1000 + idx)
        path = normal_dir / f"normal_{idx + 1:02d}.png"
        ps.save_rgb(image, path)
        written.append(str(path))

    index = []
    for idx, cls in enumerate(("black_spot", "scratch", "streak", "irregular_mark")):
        image, mask, defects = ps.render_defective(
            240, 320, seed=seed + 2000 + idx, defect_types=(cls,), count=1
        )
        stem = f"defect_{cls}"
        ps.save_rgb(image, defect_dir / f"{stem}.png")
        ps.save_mask(mask, defect_dir / f"{stem}_mask.png")
        index.append({"image": f"{stem}.png", "mask": f"{stem}_mask.png",
                      "defects": [d.as_dict() for d in defects]})

    multi, multi_mask, multi_defects = ps.render_defective(
        240, 320, seed=seed + 2100, defect_types=("black_spot", "scratch", "streak"), count=3
    )
    ps.save_rgb(multi, defect_dir / "defect_multi.png")
    ps.save_mask(multi_mask, defect_dir / "defect_multi_mask.png")
    index.append({"image": "defect_multi.png", "mask": "defect_multi_mask.png",
                  "defects": [d.as_dict() for d in multi_defects]})

    (defect_dir / "defects.json").write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"normal": written, "defects": len(index)}


def build_calibration_image(assets: Path, seed: int) -> dict:
    """校正用画像（既知長の基準線入り）を作る / calibration image with a known-length bar.

    基準線は 120 px = 100 mm として描画します。受講者はこの 2 つの数値から
    px/mm を計算し、別の距離測定に利用します。
    さらに **校正に使っていない** 検査用の線（60 px = 50 mm）も描きます。倍率を決めたあと、
    こちらを測って 50 mm に戻るか確かめれば、独立した確認になります。
    A second bar (60 px = 50 mm) that is **not** used to derive the scale is also drawn, so the
    scale can be checked independently afterwards.
    """
    width, height = 320, 240
    image = ps.render_normal(height, width, seed=seed + 3000)
    x1, x2, y = 100, 220, 150
    image[y - 1 : y + 2, x1:x2] = 30.0          # 横の基準線 / horizontal reference bar
    image[y - 12 : y + 13, x1 : x1 + 2] = 30.0  # 左の目盛 / left tick
    image[y - 12 : y + 13, x2 - 2 : x2] = 30.0  # 右の目盛 / right tick

    check_x, check_y1, check_y2 = 45, 60, 120   # 縦の検査線（校正には使わない）/ check bar
    image[check_y1:check_y2, check_x - 1 : check_x + 2] = 30.0
    image[check_y1 : check_y1 + 2, check_x - 9 : check_x + 10] = 30.0
    image[check_y2 - 2 : check_y2, check_x - 9 : check_x + 10] = 30.0

    path = assets / "diagrams" / "calibration_image.png"
    ps.save_rgb(image, path)
    info = {"image": "calibration_image.png", "reference_px": x2 - x1,
            "reference_mm": 100.0, "px_per_mm": (x2 - x1) / 100.0,
            "bar_y": y, "bar_x1": x1, "bar_x2": x2,
            "check_px": check_y2 - check_y1, "check_mm": 50.0,
            "check_x": check_x, "check_y1": check_y1, "check_y2": check_y2}
    (assets / "diagrams" / "calibration_ground_truth.json").write_text(
        json.dumps(info, indent=2), encoding="utf-8"
    )
    return info


# ---------------------------------------------------------------------------
# メイン / entry point
# ---------------------------------------------------------------------------


DIAGRAMS = {
    "diagram_pixel_grid.png": diagram_pixel_grid,
    "diagram_grayscale_values.png": diagram_grayscale_values,
    "diagram_coordinate_system.png": diagram_coordinate_system,
    "diagram_classification.png": diagram_classification,
    "diagram_detection.png": diagram_detection,
    "diagram_segmentation.png": diagram_segmentation,
    "diagram_instance_segmentation.png": diagram_instance_segmentation,
    "diagram_anomaly_heatmap.png": diagram_anomaly_heatmap,
    "diagram_control_flow.png": diagram_control_flow,
    "diagram_dataset_split.png": diagram_dataset_split,
    "diagram_yolo_annotation.png": diagram_yolo_annotation,
    "diagram_pixel_distance.png": diagram_pixel_distance,
    "diagram_calibration_concept.png": diagram_calibration_concept,
    "diagram_patchcore_concept.png": diagram_patchcore_concept,
    "diagram_yolo_vs_patchcore.png": diagram_yolo_vs_patchcore,
}


def default_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate all Week 1 training assets.")
    parser.add_argument("--root", type=Path, default=default_root(),
                        help="AI_Vision_Training project root (default: auto-detected)")
    parser.add_argument("--seed", type=int, default=2026, help="base random seed")
    parser.add_argument("--clean", action="store_true", help="delete previously generated PNGs first")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    assets = root / "assets"
    diagrams_dir = assets / "diagrams"
    diagrams_dir.mkdir(parents=True, exist_ok=True)

    if args.clean:
        for path in list(diagrams_dir.glob("*.png")) + list((assets / "normal_samples").glob("*.png")) \
                + list((assets / "defect_samples").glob("*.png")):
            path.unlink()

    family = configure_matplotlib()
    print(f"[font] using: {family}")
    print(f"[seed] {args.seed}")

    for name, func in DIAGRAMS.items():
        path = func(diagrams_dir / name)
        print(f"[diagram] {path.relative_to(root)}")

    calibration = build_calibration_image(assets, args.seed)
    print(f"[calibration] {calibration['reference_px']} px = {calibration['reference_mm']} mm "
          f"({calibration['px_per_mm']} px/mm)")

    samples = build_samples(assets, args.seed)
    print(f"[samples] {len(samples['normal'])} normal, {samples['defects']} defect records")

    print("\nDone. All assets were generated successfully.")
    print("NOTE: console messages are ASCII only so they stay readable on any Windows codepage.")
    print("      Japanese explanations live in the notebooks and in docs/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
