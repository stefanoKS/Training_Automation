"""教材用の追加図を生成する / Generate the additional teaching diagrams.

このスクリプトは、ノートブックを実行しなくても見える **静的図** を作ります。
These are the **static diagrams** a learner must see before running any code.

方針 / Rules
------------
* 座標・数式・グラフ・コードの流れは、すべて **計算して描きます**。AI 生成の画像は使いません。
  Coordinates, equations, charts and code flow are drawn from computed data — never AI imagery.
* 合成データ・模式図・保存済みの例は、図の中に明記します。
  Synthetic data, schematics and saved examples are labelled inside the figure.
* 色だけで OK/NG を伝えません。文字と形も使います。
  OK/NG is never communicated by colour alone; text and shape are always present.
* 出力先は ``assets/diagrams/`` です。既存の図は上書きしません。
  Output goes to ``assets/diagrams/`` and existing figures are not overwritten.

使い方 / Usage
--------------
    python assets\\scripts\\generate_teaching_diagrams.py
    python assets\\scripts\\generate_teaching_diagrams.py --only rule_vs_learned
"""

from __future__ import annotations

import argparse
import sys
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_training_assets import configure_matplotlib  # noqa: E402

DPI = 140
INK = "#24292f"
MUTED = "#57606a"
ACCENT = "#1f6feb"
LINE = "#d0d7de"
OK = "#1a7f37"
WARN = "#9a6700"
BAD = "#a40e26"
JA_FONT = None


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _save(fig, path: Path) -> Path:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[diagram] {path.name}")
    return path


def _box(ax, x, y, w, h, text, *, edge=ACCENT, face="#eef4ff", fontsize=9, ink=INK, radius=0.02):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad=0.006,rounding_size={radius}",
        linewidth=1.2, edgecolor=edge, facecolor=face,
    ))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize, color=ink,
            wrap=True)


def _arrow(ax, start, end, color=ACCENT, width=1.5):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=13,
                                 color=color, linewidth=width))


def _canvas(figsize=(10, 4.4)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax


def _caption(fig, text: str, y: float = -0.02) -> None:
    fig.text(0.5, y, text, ha="center", va="top", fontsize=8, color=MUTED)


# ---------------------------------------------------------------------------
# 合成素材 / synthetic material
# ---------------------------------------------------------------------------


def _pvc_sheet(size: int = 240, defect: str | None = None, seed: int = 7) -> np.ndarray:
    """PVC シートの合成画像 / a synthetic PVC sheet."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:size, 0:size]
    base = 205 + 6 * np.sin(xx / 18.0) + 4 * np.cos(yy / 23.0)
    image = np.stack([base * 1.00, base * 0.99, base * 0.96], axis=-1)
    image += rng.normal(0, 2.2, image.shape)
    if defect == "spot":
        mask = (xx - size * 0.42) ** 2 + (yy - size * 0.55) ** 2 < (size * 0.045) ** 2
        image[mask] = [40, 40, 44]
    elif defect == "scratch":
        mask = (np.abs((yy - size * 0.30) - 0.35 * (xx - size * 0.15)) < 2.0) & (xx > size * 0.2) \
            & (xx < size * 0.75)
        image[mask] = [70, 70, 76]
    return np.clip(image, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------------------
# Setup: Jupyter 画面の模式図 / annotated Jupyter interface schematic
# ---------------------------------------------------------------------------


def teach_setup_jupyter_ui(out: Path) -> Path:
    fig, ax = plt.subplots(figsize=(11, 6.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # window frame
    ax.add_patch(Rectangle((0.02, 0.06), 0.96, 0.90, facecolor="#ffffff", edgecolor=INK, linewidth=1.6))
    ax.add_patch(Rectangle((0.02, 0.90), 0.96, 0.06, facecolor="#f0f3f6", edgecolor=INK, linewidth=1.2))
    ax.text(0.05, 0.93, "JupyterLab（模式図 / schematic — 実際の画面写真ではありません）",
            fontsize=9, color=INK, va="center")

    # left file browser
    ax.add_patch(Rectangle((0.03, 0.07), 0.19, 0.82, facecolor="#f7f8fa", edgecolor=LINE))
    ax.text(0.125, 0.855, "ファイル一覧", ha="center", fontsize=8.5, color=INK)
    ax.text(0.125, 0.830, "file browser", ha="center", fontsize=7.5, color=MUTED)
    for i, name in enumerate(["notebooks/", "  Day01_01.ipynb", "  Day01_02.ipynb", "assets/",
                              "COURSE_SYLLABUS.md"]):
        ax.text(0.04, 0.79 - i * 0.045, name, fontsize=7.5, color=ACCENT if i == 1 else INK)

    left, right = 0.23, 0.70

    # kernel selector
    ax.add_patch(Rectangle((left, 0.845), 0.28, 0.035, facecolor="#ffffff", edgecolor=ACCENT,
                           linewidth=1.4))
    ax.text(left + 0.012, 0.8625, "Python 3 (AI Vision)  ▾", fontsize=8, color=ACCENT, va="center")

    # toolbar run button
    ax.add_patch(Rectangle((left, 0.795), 0.09, 0.035, facecolor="#eef4ff", edgecolor=ACCENT))
    ax.text(left + 0.045, 0.8125, "Run", ha="center", fontsize=8, color=ACCENT, va="center")

    # markdown cell
    ax.add_patch(Rectangle((left, 0.60), right - left, 0.17, facecolor="#ffffff", edgecolor=LINE,
                           linewidth=1.1))
    ax.text(left + 0.02, 0.735, "## 画素とは / What is a pixel", fontsize=9, color=INK)
    ax.text(left + 0.02, 0.700, "Markdown セル：説明を読むだけ。実行しません。", fontsize=8, color=MUTED)
    ax.text(left + 0.02, 0.670, "Markdown cell: read it; nothing to run.", fontsize=7.5, color=MUTED)

    # code cell with input prompt
    ax.add_patch(Rectangle((left, 0.40), right - left, 0.17, facecolor="#f6f8fa", edgecolor=LINE,
                           linewidth=1.1))
    ax.text(left - 0.005, 0.485, "In [7]:", ha="right", fontsize=8, color=ACCENT)
    ax.text(left + 0.02, 0.500, "# 実行のみ / Run only", fontsize=7.5, color=MUTED, family="monospace")
    ax.text(left + 0.02, 0.470, "print(2 + 3)", fontsize=8.5, color=INK, family="monospace")
    ax.text(left + 0.02, 0.435, "print('画像 / image')", fontsize=8.5, color=INK, family="monospace")

    # output area
    ax.add_patch(Rectangle((left, 0.22), right - left, 0.15, facecolor="#ffffff", edgecolor="#b6e3c4",
                           linewidth=1.1, linestyle="--"))
    ax.text(left + 0.02, 0.320, "5", fontsize=8.5, color=INK, family="monospace")
    ax.text(left + 0.02, 0.285, "画像 / image", fontsize=8.5, color=INK, family="monospace")
    ax.text(left + 0.02, 0.240, "← ④ 出力 / output（ここに出ます）", fontsize=7.5, color=OK)

    # restart / running state
    _box(ax, left, 0.09, 0.23, 0.09,
         "⑤ Kernel → Restart & Run All\n（値を忘れたら最初から / start clean）",
         edge=WARN, face="#fff8e5", fontsize=7.5)
    _box(ax, 0.47, 0.09, 0.23, 0.09,
         "In [*] = 実行中 / running\n終わると In [8] のように数字",
         edge=MUTED, face="#f7f8fa", fontsize=7.5)

    # right-hand annotation column
    annotations = [
        (0.865, "③ カーネル / kernel", "この名前が合っているか見る\ncheck the kernel name", (0.51, 0.8625)),
        (0.775, "② 実行 / run", "Shift + Enter と同じ\nsame as Shift + Enter", (left + 0.09, 0.8125)),
        (0.585, "① セル / cell", "読むセルと、実行するセル\nread-only vs runnable", (right, 0.685)),
        (0.395, "① セル（コード）/ code cell", "In [ ] の数字が実行番号\nIn [ ] shows the run order",
         (right, 0.485)),
        (0.245, "④ 出力 / output", "結果はここに出る\nprint() の結果はここ", (right, 0.285)),
    ]
    for y, title, body, target in annotations:
        ax.text(0.725, y, title, fontsize=8.5, color=ACCENT, va="center")
        ax.text(0.725, y - 0.036, body, fontsize=7.5, color=MUTED, va="center")
        _arrow(ax, (0.72, y), target, color=ACCENT, width=1.0)

    _caption(fig, "図：JupyterLab の画面構成（模式図）/ Figure: the JupyterLab notebook screen (schematic)")
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Day 1
# ---------------------------------------------------------------------------


def teach_rule_vs_learned(out: Path) -> Path:
    fig, ax = _canvas((10.4, 4.4))
    _box(ax, 0.02, 0.62, 0.28, 0.28,
         "① 人は決まりを書く\nrule:\nif 幅 < 99.5 mm:\n    NG",
         edge=ACCENT, face="#eef4ff", fontsize=8.5)
    _box(ax, 0.35, 0.62, 0.28, 0.28,
         "② 決まりを当てる\napply the rule\nto every product",
         edge=ACCENT, face="#eef4ff", fontsize=8.5)
    _box(ax, 0.68, 0.62, 0.30, 0.28,
         "③ 結果\nOK / NG\n\n決まりを書けた仕事だけ",
         edge=OK, face="#eaf7ee", fontsize=8.5)
    _arrow(ax, (0.30, 0.76), (0.35, 0.76))
    _arrow(ax, (0.63, 0.76), (0.68, 0.76))
    ax.text(0.51, 0.95, "ルールで書ける検査 / inspection a rule can handle",
            ha="center", fontsize=10, color=INK)
    ax.text(0.51, 0.90, "例：幅・厚さ・長さ（数で測れるもの）/ e.g. width, thickness, length",
            ha="center", fontsize=8, color=MUTED)

    _box(ax, 0.02, 0.12, 0.28, 0.28,
         "① 例を見せる\nshow examples\n正常 200 枚\n異常 40 枚",
         edge=WARN, face="#fff8e5", fontsize=8.5)
    _box(ax, 0.35, 0.12, 0.28, 0.28,
         "② コンピュータが\n特徴を学ぶ\nlearns the features\n（人が決まりを書かない）",
         edge=WARN, face="#fff8e5", fontsize=8.5)
    _box(ax, 0.68, 0.12, 0.30, 0.28,
         "③ 新しい画像を判定\nOK / NG + スコア\n\n決まりを書けない仕事",
         edge=OK, face="#eaf7ee", fontsize=8.5)
    _arrow(ax, (0.30, 0.26), (0.35, 0.26), color=WARN)
    _arrow(ax, (0.63, 0.26), (0.68, 0.26), color=WARN)
    ax.text(0.51, 0.46, "学習する検査 / learned inspection",
            ha="center", fontsize=10, color=INK)
    ax.text(0.51, 0.41, "例：黒点・ムラ・細かいキズ（言葉にしにくいもの）/ e.g. spots, streaks, uneven marks",
            ha="center", fontsize=8, color=MUTED)
    _caption(fig, "図：決まりを書く検査と、例から学ぶ検査 / Figure: rule-based versus learned inspection")
    return _save(fig, out)


def teach_brightness_shift(out: Path) -> Path:
    rng = np.random.default_rng(11)
    good = rng.normal(loc=205.0, scale=4.0, size=400)
    shifted = rng.normal(loc=188.0, scale=4.0, size=200)

    limit = good.mean() - 3 * good.std(ddof=1)
    false_rejects = int((shifted < limit).sum())

    fig, ax = plt.subplots(figsize=(10.2, 4.6))
    bins = np.linspace(170, 225, 46)
    ax.hist(good, bins=bins, color="#8fb6ff", edgecolor=ACCENT, label="工程の明るさ / normal lighting (n=400)")
    ax.hist(shifted, bins=bins, color="#ffd580", edgecolor=WARN,
            label="照明が変わった日 / lighting changed (n=200)")
    ax.axvline(limit, color=BAD, linewidth=2)
    ax.annotate(f"学習した下限 / learned lower limit\n{limit:.1f}",
                xy=(limit, ax.get_ylim()[1] * 0.72), xytext=(limit - 22, ax.get_ylim()[1] * 0.80),
                fontsize=8.5, color=BAD,
                arrowprops=dict(arrowstyle="-|>", color=BAD, linewidth=1.2))
    ax.axvspan(170, limit, color=BAD, alpha=0.06)
    ax.text(181, ax.get_ylim()[1] * 0.46,
            f"照明が変わった正常品のうち\n{false_rejects} 枚が NG と判定された\n"
            f"{false_rejects} good parts flagged as NG\n（＝偽陽性 / false reject）",
            fontsize=8.5, color=BAD)
    ax.set_xlabel("画像の平均明るさ（0–255、単位なしの画素値）/ mean brightness (0-255, unitless)")
    ax.set_ylabel("枚数 / number of images")
    ax.set_title("同じ正常品でも、照明で明るさは変わる / the same good part looks different under new lighting",
                 fontsize=10)
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.25)
    _caption(fig, "図：合成した明るさの分布（実際の測定値ではありません）/ "
                  "Figure: synthetic brightness distributions, not plant measurements")
    return _save(fig, out)


def teach_rgb_channels(out: Path) -> Path:
    image = _pvc_sheet(120, defect="spot", seed=21)
    fig, axes = plt.subplots(1, 4, figsize=(11, 3.3))
    axes[0].imshow(image)
    axes[0].set_title("元の画像 / original\nRGB 3 チャンネル", fontsize=9)
    for ax, channel, name, cmap in zip(
        axes[1:],
        range(3),
        ["R（赤）", "G（緑）", "B（青）"],
        ["Reds", "Greens", "Blues"],
    ):
        ax.imshow(image[..., channel], cmap=cmap, vmin=0, vmax=255)
        ax.set_title(f"{name} だけ / channel only\n0–255", fontsize=9)
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
    axes[3].plot([], [])
    _caption(fig, "図：1 枚の画像は 3 枚の 0–255 の表（チャンネル）でできている / "
                  "Figure: one image is three 0-255 tables, one per channel")
    return _save(fig, out)


def teach_downsample_defect(out: Path) -> Path:
    from PIL import Image

    source = _pvc_sheet(480, defect="scratch", seed=33)
    sizes = [480, 120, 30]
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.9))
    for ax, size in zip(axes, sizes):
        small = Image.fromarray(source).resize((size, size), Image.BILINEAR)
        shown = small.resize((480, 480), Image.NEAREST)
        ax.imshow(np.asarray(shown))
        contrast = float(np.asarray(small, dtype=float).std())
        ax.set_title(f"元 {480} px → 縮小 {size} px\n"
                     f"（{size}×{size} として保存 / stored at {size}×{size}）\n"
                     f"画素値のばらつき / spread = {contrast:.1f}", fontsize=8.5)
        ax.set_xticks([])
        ax.set_yticks([])
        if size == 30:
            ax.add_patch(Rectangle((150, 150), 180, 180, fill=False, edgecolor=BAD, linewidth=1.6))
            ax.text(150, 145, "キズが判別できない / defect no longer separable", fontsize=7.5, color=BAD)
    _caption(fig, "図：縮小すると細いキズは消える（合成画像を実際に縮小した結果）/ "
                  "Figure: a thin scratch disappears after downsampling (computed from a synthetic image)")
    return _save(fig, out)


def teach_cv_tasks_outputs(out: Path) -> Path:
    image = _pvc_sheet(200, defect="spot", seed=44)
    fig, axes = plt.subplots(1, 4, figsize=(11.4, 3.6))
    titles = [
        "分類 / classification\n→ 「異常あり」(1 つの答え)",
        "検出 / detection\n→ 四角 + クラス + 確からしさ",
        "セグメンテーション / segmentation\n→ 画素ごとのマスク",
        "異常検知 / anomaly detection\n→ スコア + ヒートマップ",
    ]
    for ax, title in zip(axes, titles):
        ax.imshow(image)
        ax.set_title(title, fontsize=8.5)
        ax.set_xticks([])
        ax.set_yticks([])

    axes[1].add_patch(Rectangle((62, 92), 40, 40, fill=False, edgecolor=BAD, linewidth=1.8,
                                linestyle="--"))
    axes[1].text(62, 88, "defect 0.87", fontsize=7, color=BAD, va="bottom")

    mask = np.zeros(image.shape[:2])
    yy, xx = np.mgrid[0:image.shape[0], 0:image.shape[1]]
    mask[(xx - 84) ** 2 + (yy - 110) ** 2 < 22 ** 2] = 1
    overlay = image.astype(float).copy()
    overlay[mask > 0] = overlay[mask > 0] * 0.35 + np.array([255, 90, 90]) * 0.65
    axes[2].imshow(np.clip(overlay, 0, 255).astype(np.uint8))

    heat = np.exp(-(((xx - 84) ** 2 + (yy - 110) ** 2) / (2 * 22.0 ** 2)))
    axes[3].imshow(heat, cmap="magma", vmin=0, vmax=1)
    axes[3].text(4, 192, "score 0.93", fontsize=7, color="white")

    _caption(fig, "図：同じ 1 枚に対する 4 つの出力（模式図。実際のモデル出力ではありません）/ "
                  "Figure: four task outputs on one image (illustration, not real model output)")
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Day 2
# ---------------------------------------------------------------------------


def teach_variable_trace(out: Path) -> Path:
    fig, ax = _canvas((10.0, 4.2))
    ax.text(0.02, 0.94, "コード / code", fontsize=9, color=INK)
    ax.text(0.46, 0.94, "実行の順番 / step", fontsize=9, color=INK)
    ax.text(0.66, 0.94, "このときの値 / value now", fontsize=9, color=INK)

    code = ["width_mm = 100.2", "width_mm = width_mm + 0.5", "is_ok = width_mm < 101.0"]
    values = ["100.2", "100.7", "True"]
    notes = ["① 代入", "② 右を計算してから代入", "③ 比べた結果（真偽値）"]
    for i, (line, value, note) in enumerate(zip(code, values, notes)):
        y = 0.70 - i * 0.20
        ax.add_patch(Rectangle((0.02, y - 0.07), 0.40, 0.14, facecolor="#f6f8fa",
                               edgecolor=LINE))
        ax.text(0.035, y, line, fontsize=9, family="monospace", color=INK, va="center")
        ax.text(0.46, y, note, fontsize=8, color=MUTED, va="center")
        ax.add_patch(Rectangle((0.66, y - 0.07), 0.20, 0.14, facecolor="#eaf7ee", edgecolor=OK))
        ax.text(0.76, y, value, fontsize=10, family="monospace", color=OK, ha="center", va="center")
    ax.text(0.02, 0.06,
            "同じ名前でも、行が進むと値は変わる。1 行ずつ「今いくつか」を追う。\n"
            "The same name holds a different value after each line; follow “what is it now”.",
            fontsize=8.5, color=MUTED)
    _caption(fig, "図：変数に値が入る順番 / Figure: the order in which values land in a variable")
    return _save(fig, out)


def teach_loop_trace(out: Path) -> Path:
    measurements = [12.41, 12.55, 12.38, 12.92, 12.44]
    nominal, tolerance = 12.50, 0.10
    fig, ax = plt.subplots(figsize=(10.2, 4.3))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.02, 0.95, "for i, value in enumerate(measurements):", fontsize=9, family="monospace")
    ax.text(0.04, 0.89, "if abs(value - 12.50) <= 0.10:   →  OK   else  →  NG", fontsize=8.5,
            family="monospace", color=MUTED)

    headers = ["i", "測定値 / value", "|value − 12.50|", "条件 / condition", "判定 / result"]
    x = [0.03, 0.15, 0.36, 0.60, 0.82]
    for xpos, head in zip(x, headers):
        ax.text(xpos, 0.79, head, fontsize=8.5, color=INK, weight="bold")
    for row, value in enumerate(measurements):
        difference = abs(value - nominal)
        ok = difference <= tolerance
        y = 0.68 - row * 0.11
        ax.text(x[0], y, str(row), fontsize=9, family="monospace")
        ax.text(x[1], y, f"{value:.2f}", fontsize=9, family="monospace")
        ax.text(x[2], y, f"{difference:.2f}", fontsize=9, family="monospace")
        ax.text(x[3], y, f"{difference:.2f} <= 0.10 → {'真 / True' if ok else '偽 / False'}",
                fontsize=8.5, family="monospace", color=OK if ok else BAD)
        ax.text(x[4], y, "OK" if ok else "NG", fontsize=9.5, color=OK if ok else BAD, weight="bold")
        ax.add_patch(Rectangle((0.015, y - 0.035), 0.95, 0.075,
                               facecolor="#eaf7ee" if ok else "#fdecef", edgecolor="none"))
    ax.text(0.02, 0.03,
            "NG は 1 件（i=3）。ループは「今どの値か」を毎回確かめる作業。\n"
            "One NG at i=3. A loop is just “check the current value, every time”.",
            fontsize=8.5, color=MUTED)
    _caption(fig, "図：5 つの測定値を順に判定するときの実行トレース / "
                  "Figure: the trace of deciding five measurements in a loop")
    return _save(fig, out)


def teach_function_io(out: Path) -> Path:
    fig, ax = _canvas((10.0, 3.4))
    _box(ax, 0.02, 0.34, 0.22, 0.34, "入力 / input\nmeasured = 12.55\nnominal = 12.50", fontsize=8.5)
    _box(ax, 0.30, 0.24, 0.34, 0.54,
         "関数 / function\njudge(value, nominal, tolerance)\n\n決まりを 1 か所にまとめる\none place for the rule",
         edge=ACCENT, face="#eef4ff", fontsize=8.5)
    _box(ax, 0.70, 0.34, 0.26, 0.34, "出力 / output\n\"NG\"\n（値が 1 つ返る / one value back）",
         edge=OK, face="#eaf7ee", fontsize=8.5)
    _arrow(ax, (0.24, 0.51), (0.30, 0.51))
    _arrow(ax, (0.64, 0.51), (0.70, 0.51), color=OK)
    ax.text(0.5, 0.92, "同じ関数を、値だけ変えて何度でも呼べる / call the same function with different values",
            ha="center", fontsize=9, color=INK)
    _caption(fig, "図：関数は「入力 → 決まり → 出力」/ Figure: a function is input → rule → output")
    return _save(fig, out)


def teach_opencv_pipeline(out: Path) -> Path:
    import cv2

    image = _pvc_sheet(200, defect="spot", seed=51)
    grey = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(grey, 128, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(255 - binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    with_contours = image.copy()
    cv2.drawContours(with_contours, contours, -1, (255, 0, 0), 2)

    fig, axes = plt.subplots(1, 4, figsize=(11.4, 3.4))
    axes[0].imshow(image)
    axes[0].set_title("① 元の画像 / original RGB", fontsize=9)
    axes[1].imshow(grey, cmap="gray", vmin=0, vmax=255)
    axes[1].set_title("② グレースケール / greyscale\n0–255", fontsize=9)
    axes[2].imshow(binary, cmap="gray", vmin=0, vmax=255)
    axes[2].set_title("③ 2 値化 / binary\nしきい値 128 / threshold 128", fontsize=9)
    axes[3].imshow(with_contours)
    axes[3].set_title(f"④ 輪郭 / contours\n{len(contours)} 個 / found", fontsize=9)
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
    _caption(fig, "図：同じ 1 枚を順に処理した実際の結果（合成画像）/ "
                  "Figure: the same image through the pipeline (computed from a synthetic image)")
    return _save(fig, out)


def teach_pixel_to_mm(out: Path) -> Path:
    fig, ax = plt.subplots(figsize=(9.4, 4.2))
    ax.set_xlim(0, 400)
    ax.set_ylim(0, 180)
    ax.set_facecolor("#f7f8fa")
    ax.add_patch(Rectangle((30, 40), 200, 90, facecolor="#dfe7f3", edgecolor=ACCENT))
    ax.text(130, 90, "シートの幅 / sheet width\n200 px", ha="center", fontsize=9)
    ax.annotate("", xy=(30, 140), xytext=(230, 140),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, linewidth=1.4))
    ax.text(130, 148, "200 px", ha="center", fontsize=8.5)
    ax.add_patch(Rectangle((260, 40), 100, 12, facecolor="#c6f0d3", edgecolor=OK))
    ax.annotate("", xy=(260, 64), xytext=(360, 64),
                arrowprops=dict(arrowstyle="<|-|>", color=OK, linewidth=1.4))
    ax.text(310, 72, "参照長 / reference\n100 px = 50.0 mm", ha="center", fontsize=8.5, color=OK)
    ax.text(30, 22,
            "px/mm = 100 px ÷ 50.0 mm = 2.00 px/mm\n"
            "200 px ÷ 2.00 px/mm = 100.0 mm\n"
            "誤差 / error = 0.5 px ÷ 2.00 px/mm = ±0.25 mm",
            fontsize=9, color=INK, family="monospace")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("画素 → ミリメートル（参照長が基準）/ pixels to millimetres, based on a reference length",
                 fontsize=10)
    _caption(fig, "図：倍率は「参照長」から決める。単位を必ず書く / "
                  "Figure: the scale comes from a reference length; always write the unit")
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Day 3
# ---------------------------------------------------------------------------


def teach_iou_rects(out: Path) -> Path:
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 3.8))
    a = (60, 60, 110, 90)   # x, y, w, h  (image coords, y down)
    b = (80, 75, 120, 100)
    ix0, iy0 = max(a[0], b[0]), max(a[1], b[1])
    ix1, iy1 = min(a[0] + a[2], b[0] + b[2]), min(a[1] + a[3], b[1] + b[3])
    inter = max(0, ix1 - ix0) * max(0, iy1 - iy0)
    area_a, area_b = a[2] * a[3], b[2] * b[3]
    union = area_a + area_b - inter
    iou = inter / union if union else 0.0

    for ax, title in zip(axes, ["① 2 つの四角 / two boxes", "② 交差 / intersection",
                                "③ 合計 / union"]):
        ax.set_xlim(0, 300)
        ax.set_ylim(260, 0)
        ax.set_xticks([0, 100, 200, 300])
        ax.set_yticks([0, 100, 200])
        ax.set_title(title, fontsize=9)
        ax.grid(alpha=0.2)

    for ax in axes:
        ax.add_patch(Rectangle((a[0], a[1]), a[2], a[3], fill=False, edgecolor=ACCENT, linewidth=2))
        ax.add_patch(Rectangle((b[0], b[1]), b[2], b[3], fill=False, edgecolor=WARN, linewidth=2,
                               linestyle="--"))

    axes[0].text(a[0], a[1] - 10, "A（正解 / truth）", fontsize=8, color=ACCENT)
    axes[0].text(b[0], b[1] + b[3] + 22, "B（予測 / predicted）", fontsize=8, color=WARN)

    axes[1].add_patch(Rectangle((ix0, iy0), ix1 - ix0, iy1 - iy0, facecolor="#ffd580",
                                edgecolor=BAD, linewidth=2))
    axes[1].text(ix0 + 4, iy0 + 26, f"交差 {inter} px²", fontsize=9, color=BAD)

    axes[2].add_patch(Rectangle((a[0], a[1]), a[2], a[3], facecolor="#8fb6ff", alpha=0.55,
                                edgecolor=ACCENT))
    axes[2].add_patch(Rectangle((b[0], b[1]), b[2], b[3], facecolor="#ffd580", alpha=0.45,
                                edgecolor=WARN))
    axes[2].text(20, 240, f"A={area_a} px², B={area_b} px², 合計/union={union} px²",
                 fontsize=8.5, color=INK)

    fig.suptitle(f"IoU = 交差 ÷ 合計 = {inter} ÷ {union} = {iou:.2f}"
                 "   （0 に近い＝重なりが少ない / near 1 means a tight fit）", fontsize=10)
    _caption(fig, "図：実際に重ねた四角から計算した IoU / Figure: IoU computed from actually overlapping boxes")
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Day 4
# ---------------------------------------------------------------------------


def teach_yolo_label_fields(out: Path) -> Path:
    figure = _pvc_sheet(240, defect="spot", seed=61)
    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    ax.imshow(figure)
    ax.set_xlim(0, 240)
    ax.set_ylim(240, 0)
    box = (74, 100, 32, 32)
    ax.add_patch(Rectangle(box[:2], box[2], box[3], fill=False, edgecolor=BAD, linewidth=2))
    cx = (box[0] + box[2] / 2) / 240
    cy = (box[1] + box[3] / 2) / 240
    aw, ah = box[2] / 240, box[3] / 240
    ax.annotate("中心 / centre", xy=(box[0] + 16, box[1] + 16), xytext=(150, 40),
                fontsize=8, color=BAD, arrowprops=dict(arrowstyle="-|>", color=BAD, linewidth=1.2))
    ax.annotate("幅 / width", xy=(box[0] + box[2], box[1] + box[3] / 2), xytext=(170, 120),
                fontsize=8, color=ACCENT, arrowprops=dict(arrowstyle="-|>", color=ACCENT, linewidth=1.0))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(244, 20, "1 行 = 1 つの物体 / one line per object", fontsize=9, color=INK)
    ax.text(244, 62, "0        0.3750   0.4833   0.1333   0.1333", fontsize=10,
            family="monospace", color=INK)
    ax.text(244, 96, "①          ②            ③            ④           ⑤", fontsize=9, color=MUTED)
    ax.text(244, 130, "① クラス番号 / class id\n"
                      "② 中心 x ÷ 幅　/ centre x ÷ image width\n"
                      "③ 中心 y ÷ 高さ / centre y ÷ image height\n"
                      "④ 幅 ÷ 画像の幅 / width ÷ image width\n"
                      "⑤ 高さ ÷ 画像の高さ / height ÷ image height",
            fontsize=8.5, color=INK, va="top")
    ax.text(244, 232, "すべて 0〜1。px ではなく「画像に対する割合」。\n"
                      "All values 0-1: fractions of the image, not pixels.",
            fontsize=8, color=MUTED, va="top")
    _caption(fig, "図：四角と YOLO ラベルの 5 つの値（合成画像）/ "
                  "Figure: the box and the five YOLO label fields (synthetic image)")
    return _save(fig, out)


def teach_split_roles(out: Path) -> Path:
    fig, ax = _canvas((10.4, 4.2))
    rows = [
        ("学習 / train", "モデルが重みを決める\nweights are fitted", "60%", "#eef4ff", ACCENT),
        ("検証 / validation", "しきい値とモデル選択\nthresholds and model choice", "20%", "#fff8e5", WARN),
        ("試験 / test", "最後に 1 回だけ評価\nused once, at the end", "20%", "#eaf7ee", OK),
    ]
    for i, (name, purpose, share, face, edge) in enumerate(rows):
        y = 0.62 - i * 0.24
        _box(ax, 0.02, y, 0.24, 0.20, f"{name}\n{share}", edge=edge, face=face, fontsize=8.5)
        ax.text(0.29, y + 0.10, purpose, fontsize=8.5, color=INK, va="center")
    ax.text(0.02, 0.97, "データの 3 つの役割 / the three roles of the data", fontsize=10, color=INK)

    _box(ax, 0.58, 0.50, 0.40, 0.30,
         "同じ撮影セッションの\nよく似た画像 / near-duplicates\nfrom one capture session",
         edge=BAD, face="#fdecef", fontsize=8.5)
    ax.text(0.58, 0.44,
            "ファイル名も md5 も違うのに、ほぼ同じ絵。\n"
            "学習と試験に分かれても、情報は漏れる。\n"
            "Different file names and hashes, almost the same picture.\n"
            "Split into train and test, the information still leaks.",
            fontsize=8, color=BAD, va="top")
    ax.text(0.58, 0.14,
            "対策 / what to do:\n"
            "・撮影セッション単位で分ける / split by capture session\n"
            "・同じ製品・同じ照明の画像を両側に入れない / never both sides",
            fontsize=8, color=INK, va="top")
    _caption(fig, "図：学習・検証・試験の役割と、近い画像による漏れ / "
                  "Figure: train/validation/test roles and near-duplicate leakage")
    return _save(fig, out)


def teach_epoch_batch(out: Path) -> Path:
    fig, ax = _canvas((10.6, 3.9))
    ax.text(0.02, 0.92, "1 epoch = すべての学習画像を 1 回ずつ見る / one epoch = one pass over the training set",
            fontsize=9.5, color=INK)
    for step in range(3):
        x = 0.02 + step * 0.26
        _box(ax, x, 0.55, 0.22, 0.24,
             f"batch {step + 1}\n8 枚 / 8 images\n\n重みを 1 回更新\none weight update",
             edge=ACCENT, face="#eef4ff", fontsize=8)
        if step < 2:
            _arrow(ax, (x + 0.22, 0.67), (x + 0.26, 0.67))
    _box(ax, 0.80, 0.55, 0.18, 0.24, "…", edge=MUTED, face="#f7f8fa", fontsize=12)
    ax.text(0.02, 0.44, "batch = 一度にまとめて見る枚数 / how many images are looked at together",
            fontsize=8.5, color=MUTED)
    _box(ax, 0.02, 0.10, 0.46, 0.26,
         "loss（損失）= 今どれだけ間違えているか\nhow wrong the model is right now",
         edge=WARN, face="#fff8e5", fontsize=8.5)
    _box(ax, 0.52, 0.10, 0.46, 0.26,
         "epoch を重ねる = 同じデータを何周もする\nrepeat the pass; the loss should fall",
         edge=OK, face="#eaf7ee", fontsize=8.5)
    _caption(fig, "図：epoch と batch の関係 / Figure: how epochs and batches relate")
    return _save(fig, out)


def teach_train_val_curves(out: Path) -> Path:
    epochs = np.arange(1, 21)
    train = 1.8 * np.exp(-epochs / 3.2) + 0.12
    val = 1.85 * np.exp(-epochs / 3.0) + 0.12 + 0.028 * np.clip(epochs - 9, 0, None)
    fig, ax = plt.subplots(figsize=(9.8, 4.4))
    ax.plot(epochs, train, marker="o", markersize=3, color=ACCENT, label="学習 loss / training loss")
    ax.plot(epochs, val, marker="s", markersize=3, color=WARN, label="検証 loss / validation loss")
    ax.set_xlabel("epoch（同じデータを何周したか / passes over the training set）")
    ax.set_ylabel("loss（小さいほど良い / lower is better）")
    ax.set_title("学習 loss は下がり続ける。検証 loss は途中から上がる。 / "
                 "training keeps falling while validation turns up", fontsize=9.5)
    ax.axvline(9, color=BAD, linestyle=":", linewidth=1.4)
    ax.annotate("ここから過学習 / overfitting starts here\n"
                "学習 loss だけを見ると、良くなったと誤解する\n"
                "watching training loss alone looks like progress",
                xy=(9, 0.5), xytext=(11, 1.15), fontsize=8, color=BAD,
                arrowprops=dict(arrowstyle="-|>", color=BAD, linewidth=1.1))
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8.5)
    _caption(fig, "図：形の例（模式的な曲線。あなたの実行結果ではありません）/ "
                  "Figure: an illustrative curve shape, not your training run")
    return _save(fig, out)


def teach_image_level_confusion(out: Path) -> Path:
    fig, axes = plt.subplots(1, 4, figsize=(11.6, 3.5))
    cases = [
        ("TP\n本当に NG、NG と判定\n真の異常を検出", _pvc_sheet(120, "spot", seed=71), OK),
        ("FP\n本当は OK、NG と判定\n偽陽性（誤報）", _pvc_sheet(120, None, seed=72), WARN),
        ("FN\n本当は NG、OK と判定\n偽陰性（見逃し）", _pvc_sheet(120, "scratch", seed=73), BAD),
        ("TN\n本当に OK、OK と判定\n正しく OK", _pvc_sheet(120, None, seed=74), MUTED),
    ]
    for ax, (title, image, colour) in zip(axes, cases):
        ax.imshow(image)
        ax.set_title(title, fontsize=8.5, color=colour)
        ax.set_xticks([])
        ax.set_yticks([])

    _caption(fig, "図：画像単位の 4 つの結果（合成画像。実際のモデル出力ではありません）/ "
                  "Figure: the four image-level outcomes (synthetic images, not model output)")
    return _save(fig, out)


def teach_image_level_confusion_matrix(out: Path) -> Path:
    fig, ax = plt.subplots(figsize=(5.6, 4.2))
    matrix = np.array([[28, 6], [9, 57]])
    ax.imshow(matrix, cmap="Blues")
    labels = [["TP = 28", "FN = 9"], ["FP = 6", "TN = 57"]]
    for row in range(2):
        for column in range(2):
            ax.text(column, row, labels[row][column], ha="center", va="center", fontsize=12,
                    color=INK)
    ax.set_xticks([0, 1], ["予測 NG / predicted NG", "予測 OK / predicted OK"], fontsize=8)
    ax.set_yticks([0, 1], ["実際 NG / actually NG", "実際 OK / actually OK"], fontsize=8)
    ax.set_title("画像単位の混同行列 / image-level confusion matrix\n"
                 "（合成データの例 / example counts）", fontsize=9.5)
    _caption(fig, "図：行が「実際」、列が「予測」。色だけで読まないこと / "
                  "Figure: rows are truth, columns are prediction; do not read it by colour alone")
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Day 5
# ---------------------------------------------------------------------------


def teach_patch_neighbour(out: Path) -> Path:
    figure = _pvc_sheet(180, defect="spot", seed=81)
    fig, axes = plt.subplots(1, 4, figsize=(11.6, 3.6),
                             gridspec_kw={"width_ratios": [1.1, 1.1, 1.3, 1.2]})

    axes[0].imshow(figure)
    axes[0].add_patch(Rectangle((60, 84), 32, 32, fill=False, edgecolor=BAD, linewidth=2))
    axes[0].set_title("① 1 つのパッチを選ぶ\npick one patch", fontsize=9)

    patch = figure[84:116, 60:92]
    axes[1].imshow(patch)
    axes[1].set_title("② パッチの中身\n32 × 32 px", fontsize=9)

    rng = np.random.default_rng(5)
    normal = rng.normal(0, 1, (36, 2)) * 0.6 + np.array([0.0, 0.0])
    this_patch = np.array([1.9, 1.5])
    distances = np.linalg.norm(normal - this_patch, axis=1)
    nearest = normal[int(np.argmin(distances))]
    score = float(distances.min())
    axes[2].scatter(normal[:, 0], normal[:, 1], s=26, facecolors="none", edgecolors=MUTED,
                    label="正常パッチの特徴 / normal patches")
    axes[2].scatter([this_patch[0]], [this_patch[1]], s=90, marker="*", color=BAD,
                    label="このパッチ / this patch")
    axes[2].plot([this_patch[0], nearest[0]], [this_patch[1], nearest[1]], color=BAD,
                 linestyle=":", linewidth=1.3)
    axes[2].set_title("③ 特徴の位置（2 次元に落とした模式図）\nfeature position — a 2-D simplification",
                      fontsize=8.5)
    axes[2].set_xticks([])
    axes[2].set_yticks([])
    axes[2].legend(fontsize=7.5, loc="upper left")

    axes[3].set_xlim(0, 1)
    axes[3].set_ylim(0, 1)
    axes[3].axis("off")
    axes[3].text(0.02, 0.86, "④ 最も近い正常パッチを探す", fontsize=9, color=INK)
    axes[3].text(0.02, 0.76, "find the nearest normal patch", fontsize=8, color=MUTED)
    axes[3].text(0.02, 0.60, f"距離 / distance = {score:.2f}", fontsize=9, family="monospace")
    axes[3].text(0.02, 0.48, "近い → 正常 / near → normal", fontsize=8.5, color=OK)
    axes[3].text(0.02, 0.40, "遠い → 異常 / far → anomaly", fontsize=8.5, color=BAD)
    axes[3].text(0.02, 0.22, f"このパッチのスコア\nscore = {score:.2f}", fontsize=9.5, color=BAD)
    axes[3].add_patch(Rectangle((0.02, 0.06), 0.9, 0.10, facecolor="#fdecef", edgecolor=BAD))
    axes[3].text(0.47, 0.11, "→ 異常と判定 / flagged as anomalous", ha="center", fontsize=8.5,
                 color=BAD)

    for ax in axes[:2]:
        ax.set_xticks([])
        ax.set_yticks([])
    _caption(fig, "図：パッチ → 特徴の位置 → 最近傍の正常パッチ → スコア。"
                  "③ は説明用の 2 次元の模式図で、モデルの内部表現そのものではありません。 / "
                  "Figure: patch → feature position → nearest normal patch → score. "
                  "Panel 3 is a teaching simplification, not the model's literal internal state.")
    return _save(fig, out)


def teach_score_map_overlay(out: Path) -> Path:
    figure = _pvc_sheet(180, defect="spot", seed=91)
    grey = figure.mean(axis=2)
    yy, xx = np.mgrid[0:180, 0:180]
    score = 0.35 * np.exp(-(((xx - 76) ** 2 + (yy - 100) ** 2) / (2 * 16.0 ** 2)))
    score += 0.02 * np.random.default_rng(3).random((180, 180))

    fig, axes = plt.subplots(1, 3, figsize=(11.4, 3.7))
    axes[0].imshow(figure)
    axes[0].set_title("① 元の画像 / original", fontsize=9)

    image = axes[1].imshow(score, cmap="magma", vmin=0, vmax=0.4)
    axes[1].set_title("② 異常マップ / anomaly map\n同じ色スケール 0.0–0.4", fontsize=9)
    cbar = fig.colorbar(image, ax=axes[1], fraction=0.046)
    cbar.set_label("異常スコア / score（無次元 / unitless）", fontsize=8)

    axes[2].imshow(figure)
    axes[2].imshow(score, cmap="magma", vmin=0, vmax=0.4, alpha=0.55)
    axes[2].set_title("③ 重ねた表示 / overlay\n（同じ 0.0–0.4 で重ねる）", fontsize=9)

    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
    _caption(fig, "図：元画像・異常マップ・重ね表示を同じスケールで並べる / "
                  "Figure: original, score map and overlay on one comparable scale")
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Setup: 手順の流れ / the five-step procedure
# ---------------------------------------------------------------------------


def teach_setup_workflow(out: Path) -> Path:
    fig, ax = _canvas((11.8, 6.4))
    ax.text(0.5, 0.975, "ノートブックを開いてから、エラーから戻るまで / "
                        "from opening a notebook to recovering from an error",
            ha="center", fontsize=11, color=INK)

    steps = [
        ("① ノートブックを開く\nOpen the notebook",
         "左のファイル一覧で\nnotebooks/ を開き、\n.ipynb をダブルクリック\n\n"
         "file browser → notebooks/\n→ double-click the .ipynb"),
        ("② カーネルを選ぶ\nSelect the kernel",
         "右上のカーネル名を押し、\n「Python 3 (AI Vision)」を選ぶ\n\n"
         "top-right kernel selector\n→ Python 3 (AI Vision)"),
        ("③ セルを実行する\nRun a cell",
         "セルをクリックして\nShift + Enter\n（または ▶ ボタン）\n\n"
         "click the cell, then\nShift + Enter (or ▶)"),
    ]
    positions = [(0.02, 0.60), (0.35, 0.60), (0.68, 0.60)]
    for (x, y), (title, body) in zip(positions, steps):
        _box(ax, x, y, 0.30, 0.33, "", edge=ACCENT, face="#f6f9ff")
        ax.text(x + 0.015, y + 0.295, title, fontsize=9.5, color=ACCENT, va="top")
        ax.text(x + 0.015, y + 0.195, body, fontsize=7.8, color=INK, va="top", linespacing=1.45)

    for x in (0.32, 0.65):
        _arrow(ax, (x, 0.76), (x + 0.03, 0.76))

    steps2 = [
        ("④ 出力を確認する\nCheck the output",
         "In [7]: → Out に結果が出る\nエラーなら赤い文字が出る\n\n"
         "The result appears below\nIn [7]:. An error appears\nin red text."),
        ("⑤ エラーから戻る\nRecover from an error",
         "1. 最後の 1 行を読む\n2. 原因のセルを直す\n"
         "3. Kernel → Restart & Run All\n\n"
         "1. read the LAST line\n2. fix the cell named there\n"
         "3. Kernel → Restart & Run All"),
    ]
    positions2 = [(0.02, 0.16), (0.35, 0.16)]
    for (x, y), (title, body) in zip(positions2, steps2):
        good = title.startswith("④")
        _box(ax, x, y, 0.30, 0.33, "", edge=OK if good else WARN,
             face="#f4fbf6" if good else "#fffaf0")
        ax.text(x + 0.015, y + 0.295, title, fontsize=9.5,
                color=OK if good else WARN, va="top")
        ax.text(x + 0.015, y + 0.195, body, fontsize=7.8, color=INK, va="top", linespacing=1.45)

    _arrow(ax, (0.17, 0.58), (0.17, 0.51))
    _arrow(ax, (0.50, 0.58), (0.50, 0.51))
    _arrow(ax, (0.32, 0.325), (0.35, 0.325))

    _box(ax, 0.68, 0.16, 0.30, 0.33,
         "エラーは「失敗」ではなく情報です\nAn error is information\n\n"
         "読む順番 / read in this order\n"
         "1. 一番下の行 / the last line\n"
         "2. File \"...\", line N\n"
         "3. その行のコード / that line\n\n"
         "詰まったら「何番の手順か」を\n講師に伝えてください\n"
         "If stuck, say which step number.",
         edge=MUTED, face="#f7f8fa", fontsize=7.9)
    _caption(fig, "図：手順の模式図（実際の画面写真ではありません）/ "
                  "Figure: schematic of the procedure (not a screenshot)")
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Day 1: 学習と推論 / training versus inference
# ---------------------------------------------------------------------------


def teach_train_vs_inference(out: Path) -> Path:
    fig, ax = _canvas((11.4, 4.9))
    ax.text(0.5, 0.965, "学習（training）と推論（inference）は別の作業です / "
                        "training and inference are different jobs",
            ha="center", fontsize=11, color=INK)

    # training row
    ax.text(0.02, 0.855, "学習 / TRAINING", fontsize=10, color=ACCENT)
    ax.text(0.02, 0.805, "1 回だけ・時間がかかる / once, and slow", fontsize=8, color=MUTED)
    _box(ax, 0.02, 0.52, 0.20, 0.24,
         "答え付きの例\nlabeled examples\n\nOK の画像 200 枚\nNG の画像 200 枚", fontsize=8.2)
    _box(ax, 0.28, 0.52, 0.20, 0.24,
         "学習\nlearning\n\n重み（数字の組）を\n少しずつ調整する", edge=WARN, face="#fff8ec", fontsize=8.2)
    _box(ax, 0.54, 0.52, 0.17, 0.24,
         "重み\nweights\n\n(model file)", edge=OK, face="#f2fbf5", fontsize=8.2)
    _arrow(ax, (0.22, 0.64), (0.28, 0.64))
    _arrow(ax, (0.48, 0.64), (0.54, 0.64))
    ax.text(0.75, 0.72, "学習の途中で\n見ていないデータで\n確認する\n\n"
                        "check on data the\nmodel has not\nbeen trained on",
            fontsize=7.6, color=MUTED, va="top")

    # inference row
    ax.text(0.02, 0.415, "推論 / INFERENCE", fontsize=10, color=WARN)
    ax.text(0.02, 0.365, "部品ごとに何度でも・速い / every part, many times, fast",
            fontsize=8, color=MUTED)
    _box(ax, 0.02, 0.09, 0.20, 0.22, "新しい画像\nnew image\n\n現場の 1 枚", fontsize=8.2)
    _box(ax, 0.28, 0.09, 0.20, 0.22,
         "重みは変えない\nweights are frozen\n\n同じモデルのまま", edge=OK, face="#f2fbf5", fontsize=8.2)
    _box(ax, 0.54, 0.09, 0.17, 0.22, "答え\nanswer\n\nOK / NG・四角\n・スコア", edge=WARN, face="#fff8ec",
         fontsize=8.2)
    _arrow(ax, (0.22, 0.20), (0.28, 0.20))
    _arrow(ax, (0.48, 0.20), (0.54, 0.20))
    _arrow(ax, (0.625, 0.52), (0.625, 0.36), color=OK, width=1.8)
    ax.text(0.645, 0.44, "同じ重みを使う / the same weights", fontsize=7.8, color=OK)

    _box(ax, 0.76, 0.09, 0.22, 0.32,
         "推論のときは\n学習しません\n\n"
         "Inference does not\ntrain anything.\n\n"
         "スライダーを動かしても\nモデルは変わりません\n"
         "Moving a slider does not\nchange the model.",
         edge=BAD, face="#fff5f6", fontsize=7.8)
    _caption(fig, "図：学習と推論の役割の違い（模式図）/ "
                  "Figure: what training does that inference does not (schematic)")
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Day 2: 条件分岐 / a condition on a real measurement
# ---------------------------------------------------------------------------


def teach_condition_branch(out: Path) -> Path:
    fig, ax = _canvas((11.2, 4.6))

    # measurement
    _box(ax, 0.02, 0.60, 0.19, 0.24,
         "測定値 / measurement\n\nthickness = 12.14 mm\n（規格 / spec: 12.0 ± 0.2）", fontsize=8.4)
    _arrow(ax, (0.21, 0.72), (0.27, 0.72))

    # diamond
    cx, cy, hw, hh = 0.40, 0.72, 0.115, 0.19
    ax.add_patch(patches.Polygon(
        [(cx, cy + hh), (cx + hw, cy), (cx, cy - hh), (cx - hw, cy)],
        closed=True, facecolor="#eef4ff", edgecolor=ACCENT, linewidth=1.6))
    ax.text(cx, cy + 0.045, "11.8 ≤ x ≤ 12.2 ?", ha="center", fontsize=8.6, color=ACCENT)
    ax.text(cx, cy - 0.045, "条件 / condition", ha="center", fontsize=7.6, color=MUTED)

    # branches
    _arrow(ax, (cx + hw, cy + 0.01), (0.66, 0.86))
    _arrow(ax, (cx + hw, cy - 0.01), (0.66, 0.50))
    ax.text(0.58, 0.86, "はい / True", fontsize=8.2, color=OK)
    ax.text(0.58, 0.46, "いいえ / False", fontsize=8.2, color=BAD)

    _box(ax, 0.66, 0.76, 0.30, 0.19,
         "OK と表示する（合格）\n\nprint(\"OK\")", edge=OK, face="#f2fbf5", fontsize=8.4)
    _box(ax, 0.66, 0.36, 0.30, 0.19,
         "NG と表示する（不合格）\n\nprint(\"NG\")", edge=BAD, face="#fff5f6", fontsize=8.4)

    ax.text(0.02, 0.50,
            "同じ測定値でも、しきい値（11.8 / 12.2）が変われば答えが変わります。\n"
            "しきい値は「決まり」であり、AI が決めるものではありません。\n\n"
            "The same measurement gives a different answer if the limits change.\n"
            "The limits are a rule, not something the model decides.",
            fontsize=7.8, color=MUTED, va="top", linespacing=1.55)

    # worked numbers
    values = [("12.10 mm", True), ("11.74 mm", False), ("12.31 mm", False), ("12.20 mm", True)]
    ax.text(0.02, 0.255, "実際の値を当てはめる / apply the condition to real numbers",
            fontsize=8.6, color=INK)
    for i, (text, ok) in enumerate(values):
        x = 0.02 + i * 0.245
        _box(ax, x, 0.07, 0.22, 0.12,
             f"{text}\n→ {'OK' if ok else 'NG'}", edge=OK if ok else BAD,
             face="#f2fbf5" if ok else "#fff5f6", fontsize=8.4)

    _caption(fig, "図：測定値から OK/NG を決める条件の流れ（境界値 12.20 mm は「以内」なので OK）/ "
                  "Figure: how a condition turns a measurement into OK/NG (12.20 mm is inclusive)")
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Day 3: 四角の座標 / box coordinates on the image
# ---------------------------------------------------------------------------


def teach_bbox_coords(out: Path) -> Path:
    image = _pvc_sheet(240, defect="spot", seed=41)
    h, w = image.shape[:2]
    x1, y1, x2, y2 = 84, 108, 132, 152
    bw, bh = x2 - x1, y2 - y1
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.3))
    ax = axes[0]
    ax.imshow(image)
    ax.add_patch(Rectangle((x1, y1), bw, bh, fill=False, edgecolor=BAD, linewidth=2))
    ax.plot([cx], [cy], marker="+", color=BAD, markersize=10)
    ax.text(x1 - 6, y1 - 6, f"y1={y1}", fontsize=8, color=BAD, ha="right", va="top")
    ax.text(x2 + 6, y1 + 6, f"x2={x2}", fontsize=8, color=BAD, ha="left", va="bottom")
    ax.text(x2 + 6, y2 - 6, f"y2={y2}", fontsize=8, color=BAD, ha="left", va="top")
    ax.annotate(f"x1={x1}", (x1, y1), textcoords="offset points", xytext=(-4, 14),
                fontsize=8, color=BAD, ha="center")
    ax.set_title(f"① 画素座標 / pixel coordinates\n画像サイズ / image size = {w} × {h}",
                 fontsize=9)
    ax.set_xlabel("x（右へ増える / increases to the right）", fontsize=8)
    ax.set_ylabel("y（下へ増える / increases downwards）", fontsize=8)
    ax.set_xticks([0, 60, 120, 180, 239])
    ax.set_yticks([0, 60, 120, 180, 239])
    ax.tick_params(labelsize=7)

    ax2 = axes[1]
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    ax2.set_title("② 4 つの数 → モデルが使う 5 つの数 / four numbers → the five a model uses",
                  fontsize=9)

    rows = [
        ("左上 / top-left", f"({x1}, {y1})"),
        ("右下 / bottom-right", f"({x2}, {y2})"),
        ("幅 / width", f"{bw} px"),
        ("高さ / height", f"{bh} px"),
        ("中心 / centre", f"({cx:.0f}, {cy:.0f})"),
    ]
    ax2.text(0.02, 0.92, "画素の数 / pixel counts", fontsize=8.6, color=ACCENT)
    for i, (label, value) in enumerate(rows):
        ax2.text(0.04, 0.83 - i * 0.10, label, fontsize=8.2, color=INK)
        ax2.text(0.44, 0.83 - i * 0.10, value, fontsize=8.2, color=INK, family="monospace")

    normalised = [
        ("cx / W", f"{cx / w:.3f}"),
        ("cy / H", f"{cy / h:.3f}"),
        ("w / W", f"{bw / w:.3f}"),
        ("h / H", f"{bh / h:.3f}"),
    ]
    ax2.text(0.02, 0.32, "0〜1 に割った値（YOLO ラベルの 5 つのうち 4 つ）/ "
                         "divided by the image size", fontsize=8.6, color=WARN)
    for i, (label, value) in enumerate(normalised):
        ax2.text(0.04, 0.25 - i * 0.062, label, fontsize=8.2, color=INK)
        ax2.text(0.44, 0.25 - i * 0.062, value, fontsize=8.2, color=INK, family="monospace")
    ax2.text(0.04, 0.0, "5 つめはクラス番号 / the fifth value is the class id",
             fontsize=7.8, color=MUTED, va="bottom")

    _caption(fig, "図：画素の数で書いた四角と、画像サイズで割った四角（同じ 1 つの箱） / "
                  "Figure: one box written as pixel counts and as fractions of the image size")
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Day 3: confidence で絞る / filtering one result set by confidence
# ---------------------------------------------------------------------------


def teach_confidence_filter(out: Path) -> Path:
    image = _pvc_sheet(220, defect="spot", seed=52)
    # 1 回の推論で得た「同じ」検出の一覧 / one inference, one list of detections
    detections = [
        (78, 107, 30, 28, 0.91, "black_spot"),
        (120, 96, 30, 28, 0.44, "scratch"),
        (64, 150, 26, 24, 0.27, "streak"),
        (150, 40, 24, 22, 0.18, "black_spot"),
    ]
    thresholds = [0.25, 0.50, 0.75]

    fig, axes = plt.subplots(1, 3, figsize=(11.4, 4.1))
    for ax, thresh in zip(axes, thresholds):
        ax.imshow(image)
        kept = 0
        for x, y, w, h, conf, name in detections:
            kept_here = conf >= thresh
            kept += int(kept_here)
            ax.add_patch(Rectangle(
                (x, y), w, h, fill=False, linewidth=2 if kept_here else 1.2,
                edgecolor=OK if kept_here else MUTED,
                linestyle="-" if kept_here else ":"))
            ax.text(x, y - 4, f"{name} {conf:.2f}", fontsize=7.2,
                    color=OK if kept_here else MUTED)
        ax.set_title(f"しきい値 / threshold = {thresh:.2f}\n残った検出 / kept = {kept} 件",
                     fontsize=9.5, color=INK)
        ax.set_xticks([])
        ax.set_yticks([])

    _caption(fig, "図：同じ 1 回の推論結果を、しきい値で絞り込んでいるだけです（緑の実線＝残した検出、灰色の点線＝捨てた検出）。\n"
                  "合成画像と例示用の値で、実際のモデル出力ではありません / "
                  "Figure: one inference filtered at three thresholds (solid green = kept, dotted grey = dropped); "
                  "synthetic image and illustrative scores, not model output")
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Day 3: 解像度と小さな物体 / resolution and small objects
# ---------------------------------------------------------------------------


def teach_resolution_effect(out: Path) -> Path:
    # 64 mm を何画素で撮るか / how many pixels we spend on 64 mm
    field_mm = 64.0
    defect_mm = 0.4
    widths = [640, 320, 160, 80]
    clean = _pvc_sheet(640, defect=None, seed=63).astype(np.float32)
    yy, xx = np.mgrid[0:640, 0:640]
    radius_px = defect_mm / 2 * (640 / field_mm)
    spot = ((xx - 300) ** 2 + (yy - 330) ** 2) <= radius_px ** 2
    defect = clean.copy()
    defect[spot] -= 45.0
    defect = np.clip(defect, 0, 255).astype(np.uint8)
    clean_u8 = np.clip(clean, 0, 255).astype(np.uint8)

    fig, axes = plt.subplots(1, 4, figsize=(11.8, 4.2))
    for ax, width in zip(axes, widths):
        scale = width / field_mm                       # px per mm
        small = cv2_resize(defect, width)
        baseline = cv2_resize(clean_u8, width)
        diameter_px = defect_mm * scale
        cx_px = 300 * width / 640
        cy_px = 330 * width / 640
        pad = max(7, int(round(diameter_px * 3)))
        y0, y1 = int(cy_px) - pad, int(cy_px) + pad
        x0, x1 = int(cx_px) - pad, int(cx_px) + pad
        crop = np.asarray(small)[max(0, y0):y1, max(0, x0):x1]
        base_crop = np.asarray(baseline)[max(0, y0):y1, max(0, x0):x1]
        # 欠陥の中心画素での差＝信号の強さ / signal strength at the centre pixel
        cy_i, cx_i = min(crop.shape[0] - 1, pad), min(crop.shape[1] - 1, pad)
        grey_crop = crop.mean(axis=2) if crop.ndim == 3 else crop
        grey_base = base_crop.mean(axis=2) if base_crop.ndim == 3 else base_crop
        signal = float(grey_base[cy_i, cx_i]) - float(grey_crop[cy_i, cx_i])
        ax.imshow(crop, interpolation="nearest")
        ax.set_title(f"{width} px で撮影 / captured at {width} px\n{scale:.1f} px/mm", fontsize=8.8)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(0.0, -0.09,
                f"直径 / diameter ≈ {diameter_px:.1f} px   "
                f"中心の明るさの差 / Δ ≈ {signal:.0f}",
                transform=ax.transAxes, fontsize=7.6, color=INK, va="top")

    fig.suptitle(f"{defect_mm} mm の欠陥を、視野 {field_mm:.0f} mm（640 px）で撮ったときの見え方 / "
                 f"a {defect_mm} mm defect at four camera resolutions", fontsize=10)
    _caption(fig, "図：同じ合成画像を実際に縮小し、欠陥の位置を等倍表示。Δ は「欠陥あり」と「欠陥なし」の中心画素の差（計算値）。\n"
                  "1 画素未満になると、その差はノイズと同じ大きさになります / "
                  "Figure: one synthetic image actually downsampled and zoomed at the defect; Δ is the computed difference at the "
                  "centre pixel between the same image with and without the defect. Below one pixel the difference is the size of the noise.",
             y=-0.06)
    return _save(fig, out)


def cv2_resize(image: np.ndarray, width: int) -> np.ndarray:
    """PIL で縮小する / shrink with PIL so the result does not depend on OpenCV."""
    from PIL import Image

    height = max(1, int(round(image.shape[0] * width / image.shape[1])))
    resized = Image.fromarray(image).resize((width, height), Image.BILINEAR)
    return np.asarray(resized)


# ---------------------------------------------------------------------------
# Day 4: 物体単位の対応づけ / object-level matching
# ---------------------------------------------------------------------------


def teach_object_level_matching(out: Path) -> Path:
    truth = [("GT1", (40, 60, 36, 34)), ("GT2", (140, 120, 40, 36))]
    preds = [("P1", (44, 64, 34, 32), 0.88), ("P2", (98, 168, 30, 28), 0.61),
             ("P3", (142, 124, 38, 34), 0.42)]

    def iou(a, b):
        ax0, ay0, aw, ah = a
        bx0, by0, bw, bh = b
        ix0, iy0 = max(ax0, bx0), max(ay0, by0)
        ix1, iy1 = min(ax0 + aw, bx0 + bw), min(ay0 + ah, by0 + bh)
        inter = max(0, ix1 - ix0) * max(0, iy1 - iy0)
        union = aw * ah + bw * bh - inter
        return inter / union if union else 0.0

    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.4))
    ax = axes[0]
    ax.imshow(_pvc_sheet(220, defect=None, seed=74))
    for name, box in truth:
        ax.add_patch(Rectangle((box[0], box[1]), box[2], box[3], fill=False,
                               edgecolor=ACCENT, linewidth=2))
        ax.text(box[0], box[1] - 5, name, fontsize=8, color=ACCENT)
    for name, box, conf in preds:
        ax.add_patch(Rectangle((box[0], box[1]), box[2], box[3], fill=False,
                               edgecolor=WARN, linewidth=1.6, linestyle="--"))
        ax.text(box[0] + box[2] - 2, box[1] + box[3] + 12, f"{name} {conf:.2f}",
                fontsize=7.6, color=WARN, ha="right")
    ax.set_title("① 正解（青の実線）と予測（橙の点線）/ truth (solid blue), predictions (dashed orange)",
                 fontsize=8.6)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 220)
    ax.set_ylim(220, 0)

    ax2 = axes[1]
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    ax2.set_title("② 1 対 1 で対応づける（IoU ≥ 0.5）/ match one to one at IoU ≥ 0.5",
                  fontsize=8.6)

    header = ["", "GT1", "GT2"]
    ax2.text(0.10, 0.90, "予測 / pred", fontsize=8.2, color=MUTED)
    for i, h in enumerate(header[1:]):
        ax2.text(0.46 + i * 0.20, 0.90, h, fontsize=8.4, color=ACCENT)
    for j, (name, box, conf) in enumerate(preds):
        y = 0.80 - j * 0.10
        ax2.text(0.06, y, f"{name}  (conf {conf:.2f})", fontsize=8.2, color=WARN)
        for i, (_, gbox) in enumerate(truth):
            value = iou(box, gbox)
            colour = OK if value >= 0.5 else MUTED
            ax2.text(0.46 + i * 0.20, y, f"{value:.2f}", fontsize=8.4, color=colour,
                     family="monospace")

    outcomes = [
        ("GT1 ↔ P1", "一致（TP）/ matched", OK),
        ("GT2 ↔ P3", "一致（TP）/ matched", OK),
        ("P2", "対応なし → FP / no partner", BAD),
        ("—", "対応のない正解なし / no unmatched truth", MUTED),
    ]
    ax2.text(0.02, 0.50, "結果 / outcome", fontsize=8.6, color=INK)
    for i, (pair, text, colour) in enumerate(outcomes):
        ax2.text(0.04, 0.42 - i * 0.07, pair, fontsize=8, color=colour)
        ax2.text(0.26, 0.42 - i * 0.07, text, fontsize=8, color=colour)

    ax2.text(0.02, 0.04, "物体単位の数え方は、画像単位の OK/NG と別です。混ぜないでください。\n"
                         "Object-level counting is separate from the image-level OK/NG decision.",
             fontsize=7.6, color=MUTED, va="bottom", linespacing=1.5)

    _caption(fig, "図：IoU で 1 対 1 に対応づける模式図（座標は例示用。同じ画像で画像単位の判定は別に行います）/ "
                  "Figure: one-to-one matching by IoU (illustrative coordinates; the image-level decision is separate)")
    return _save(fig, out)


# ---------------------------------------------------------------------------
# registry
# ---------------------------------------------------------------------------

DIAGRAMS = {
    "teach_bbox_coords.png": teach_bbox_coords,
    "teach_confidence_filter.png": teach_confidence_filter,
    "teach_resolution_effect.png": teach_resolution_effect,
    "teach_object_level_matching.png": teach_object_level_matching,
    "teach_setup_workflow.png": teach_setup_workflow,
    "teach_train_vs_inference.png": teach_train_vs_inference,
    "teach_condition_branch.png": teach_condition_branch,
    "teach_setup_jupyter_ui.png": teach_setup_jupyter_ui,
    "teach_rule_vs_learned.png": teach_rule_vs_learned,
    "teach_brightness_shift.png": teach_brightness_shift,
    "teach_rgb_channels.png": teach_rgb_channels,
    "teach_downsample_defect.png": teach_downsample_defect,
    "teach_cv_tasks_outputs.png": teach_cv_tasks_outputs,
    "teach_variable_trace.png": teach_variable_trace,
    "teach_loop_trace.png": teach_loop_trace,
    "teach_function_io.png": teach_function_io,
    "teach_opencv_pipeline.png": teach_opencv_pipeline,
    "teach_pixel_to_mm.png": teach_pixel_to_mm,
    "teach_iou_rects.png": teach_iou_rects,
    "teach_yolo_label_fields.png": teach_yolo_label_fields,
    "teach_split_roles.png": teach_split_roles,
    "teach_epoch_batch.png": teach_epoch_batch,
    "teach_train_val_curves.png": teach_train_val_curves,
    "teach_image_level_confusion.png": teach_image_level_confusion,
    "teach_image_level_confusion_matrix.png": teach_image_level_confusion_matrix,
    "teach_patch_neighbour.png": teach_patch_neighbour,
    "teach_score_map_overlay.png": teach_score_map_overlay,
}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Generate the additional teaching diagrams.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--only", default=None, help="substring of a single diagram key")
    args = parser.parse_args(argv)

    family = configure_matplotlib()
    print(f"[font] using: {family}")
    # monospace でも日本語が出るようにする / keep Japanese readable in monospace text
    plt.rcParams["font.monospace"] = [family, "DejaVu Sans Mono", "monospace"]
    plt.rcParams["font.family"] = [family, "DejaVu Sans"]

    out_dir = args.root.resolve() / "assets" / "diagrams"
    for name, func in DIAGRAMS.items():
        if args.only and args.only not in name:
            continue
        func(out_dir / name)
    print("\nDone. Teaching diagrams are written to assets/diagrams/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
