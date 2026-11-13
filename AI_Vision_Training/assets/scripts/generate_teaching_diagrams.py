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


def _wrap_caption(text: str, limit: int = 150) -> str:
    """図の幅を超えないように折り返す / wrap so a caption cannot widen the figure.

    日本語は 1 文字を 2 単位、英数字は 1 単位で数えます。
    Japanese characters count as two units and Latin characters as one.
    """
    import unicodedata

    def units(chunk: str) -> int:
        return sum(2 if unicodedata.east_asian_width(char) in "WF" else 1 for char in chunk)

    lines: list[str] = []
    for paragraph in text.split("\n"):
        line = ""
        for char in paragraph:
            if units(line) + units(char) > limit:
                cut = line.rfind(" ")
                if cut > 0 and units(line[cut:]) <= 40:
                    lines.append(line[:cut])
                    line = line[cut + 1:]
                else:
                    lines.append(line)
                    line = ""
            line += char
        lines.append(line)
    return "\n".join(lines)


def _caption(fig, text: str, y: float = -0.02) -> None:
    fig.text(0.5, y, _wrap_caption(text), ha="center", va="top", fontsize=8, color=MUTED)


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
    ax.text(left + 0.02, 0.700, "Markdown セル：説明のテキスト。編集はできますが、実行するコードはありません。",
            fontsize=8, color=MUTED)
    ax.text(left + 0.02, 0.670, "Markdown cell: text you can edit; there is no code to run.", fontsize=7.5,
            color=MUTED)

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
        (0.585, "① セル / cell", "Markdown とコードのセル\nMarkdown versus code", (right, 0.685)),
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
    fig, ax = _canvas((11.0, 4.6))
    ax.text(0.5, 0.975, "決まりを人が書く場合と、例から決まる場合 / "
                        "a rule written by a person versus a range fitted from examples",
            ha="center", fontsize=10.5, color=INK)

    ax.text(0.02, 0.915, "① 人が決まりを書く（幅のしきい値）/ a person writes the rule", fontsize=9.2,
            color=ACCENT)
    rule_boxes = [
        "if 幅 < 99.5 mm:\n    NG",
        "すべての製品に当てる\napply it to every part",
        "OK / NG\n数で決まる / decided by numbers",
    ]
    for index, text in enumerate(rule_boxes):
        x = 0.02 + index * 0.33
        _box(ax, x, 0.70, 0.28, 0.18, text, edge=ACCENT, face="#eef4ff", fontsize=8.2)
        if index < 2:
            _arrow(ax, (x + 0.28, 0.79), (x + 0.33, 0.79))
    ax.text(0.02, 0.655, "人が書いた決まり / a rule a person wrote", fontsize=7.6, color=MUTED)

    ax.text(0.02, 0.575,
            "② この研修の簡単な例：人が特徴を選び、値の範囲は例から決まる / "
            "the simple example here: a person picks the feature, the range is fitted",
            fontsize=9.2, color=WARN)
    learned_boxes = [
        "人が選ぶ特徴 / chosen by a person\n平均の明るさ\nmean brightness",
        "正常画像から平均とばらつきを決める\nmean and spread fitted\nfrom normal images",
        "その範囲で判定\nOK / NG inside the\nfitted range",
    ]
    for index, text in enumerate(learned_boxes):
        x = 0.02 + index * 0.33
        _box(ax, x, 0.36, 0.28, 0.18, text, edge=WARN, face="#fff8ec", fontsize=8.0)
        if index < 2:
            _arrow(ax, (x + 0.28, 0.45), (x + 0.33, 0.45), color=WARN)

    ax.text(0.02, 0.315,
            "人が決めるのは「平均の明るさを使う」という特徴の選び方です。範囲（平均と標準偏差）は正常画像から"
            "決まる、学習した部分です。\n"
            "Here a person chooses mean brightness as the feature; the mean and spread fitted from normal "
            "images are the learned part.\n"
            "この方法は仕組みを理解するための簡単な統計的手法で、深い特徴を学ぶ例ではありません。\n"
            "This is a deliberately simple statistical method for understanding the idea, not deep feature learning.",
            fontsize=7.8, color=MUTED, va="top", linespacing=1.6)
    _caption(fig, "図：人が書く決まりと、例から決まる範囲（模式図）/ "
                  "Figure: a hand-written rule and a range fitted from examples (schematic)")
    return _save(fig, out)


def teach_brightness_shift(out: Path) -> Path:
    rng = np.random.default_rng(11)
    good = rng.normal(loc=205.0, scale=4.0, size=400)
    shifted = rng.normal(loc=188.0, scale=4.0, size=200)

    limit = good.mean() - 3 * good.std(ddof=1)
    false_rejects = int((shifted < limit).sum())

    fig, ax = plt.subplots(figsize=(10.2, 4.6))
    bins = np.linspace(170, 225, 46)
    ax.hist(good, bins=bins, color="#8fb6ff", edgecolor=ACCENT,
            label="もとの照明 / original illumination (n=400)")
    ax.hist(shifted, bins=bins, color="#ffd580", edgecolor=WARN,
            label="照明を暗くした画像 / illumination lowered (n=200)")
    ax.axvline(limit, color=BAD, linewidth=2)
    ax.annotate(f"学習した下限 / learned lower limit\n{limit:.1f}",
                xy=(limit, ax.get_ylim()[1] * 0.72), xytext=(limit - 22, ax.get_ylim()[1] * 0.80),
                fontsize=8.5, color=BAD,
                arrowprops=dict(arrowstyle="-|>", color=BAD, linewidth=1.2))
    ax.axvspan(170, limit, color=BAD, alpha=0.06)
    ax.text(181, ax.get_ylim()[1] * 0.46,
            f"照明が変わった正常品のうち\n{false_rejects} 枚が NG と判定された\n"
            f"{false_rejects} good parts flagged as NG\n（＝偽陽性 / false reject）\n"
            "変えたのは照明の明るさだけ / only the illumination changed",
            fontsize=8.5, color=BAD)
    ax.set_xlabel("画像の平均明るさ（0–255、単位なしの画素値）/ mean brightness (0-255, unitless)")
    ax.set_ylabel("枚数 / number of images")
    ax.set_title("照明の明るさを下げると、正常品の平均も下がる / lowering the illumination moves "
                 "the good distribution",
                 fontsize=10)
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.25)
    _caption(fig, "図：合成した明るさの分布（実際の測定値ではありません）。変えたのは照明の明るさだけで、"
                  "カメラ・距離・製品は同じです。分布がどちらへ動くかは、条件の変え方によります。 / "
                  "Figure: synthetic brightness distributions, not plant measurements. Only the "
                  "illumination level changed; the direction depends on how the condition changes.")
    return _save(fig, out)


def teach_rgb_channels(out: Path) -> Path:
    image = _pvc_sheet(120, defect="spot", seed=21)
    px, py = 50, 66                                   # 1 つの画素を選ぶ / pick one pixel
    red, green, blue = (int(v) for v in image[py, px])
    grey = round(0.299 * red + 0.587 * green + 0.114 * blue, 1)

    fig, axes = plt.subplots(1, 4, figsize=(11.6, 3.6))
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
        ax.plot([px], [py], marker="o", markersize=9, markerfacecolor="none",
                markeredgecolor=BAD, markeredgewidth=1.8)

    axes[0].text(4, 12, f"同じ 1 画素 / the same pixel (x={px}, y={py})", fontsize=8,
                 color=BAD, va="top")
    axes[3].text(0.02, -0.06,
                 f"この画素の値 / this pixel: R={red}  G={green}  B={blue}\n"
                 f"グレースケール / grey = 0.299·R + 0.587·G + 0.114·B = {grey}",
                 transform=axes[3].transAxes, fontsize=7.8, color=INK, va="top",
                 family="monospace")
    _caption(fig, "図：1 枚の画像は 3 枚の 0–255 の表（チャンネル）でできている。1 画素は 3 つの数の組。 / "
                  "Figure: one image is three 0-255 tables, one per channel; one pixel is a triple of numbers.",
             y=-0.10)
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
    yy, xx = np.mgrid[0:image.shape[0], 0:image.shape[1]]
    # 4 つの出力は、どれも「同じ 1 つの欠陥」を表す / all four outputs describe the same defect
    mask = ((xx - 84) ** 2 + (yy - 110) ** 2 < 22 ** 2)
    ys, xs = np.nonzero(mask)
    x1, x2, y1, y2 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())

    fig, axes = plt.subplots(1, 4, figsize=(11.8, 4.0))
    titles = [
        "① 分類 / classification\n→ 「異常あり」(1 つの答え)",
        "② 検出 / detection\n→ 四角 + クラス + 確からしさ",
        "③ セグメンテーション / segmentation\n→ 画素ごとのマスク",
        "④ 異常検知 / anomaly detection\n→ スコア + ヒートマップ",
    ]
    for ax, title in zip(axes, titles):
        ax.imshow(image)
        ax.set_title(title, fontsize=8.5)
        ax.set_xticks([])
        ax.set_yticks([])

    axes[1].add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False, edgecolor=BAD,
                                linewidth=1.8, linestyle="--"))
    axes[1].text(x1, y1 - 4, f"defect 0.87  ({x1},{y1})-({x2},{y2})", fontsize=6.8, color=BAD,
                 va="bottom")

    overlay = image.astype(float).copy()
    overlay[mask] = overlay[mask] * 0.35 + np.array([255, 90, 90]) * 0.65
    axes[2].imshow(np.clip(overlay, 0, 255).astype(np.uint8))
    axes[2].text(4, 196, f"mask: {int(mask.sum())} px", fontsize=7, color="white", va="bottom")

    heat = np.exp(-(((xx - 84) ** 2 + (yy - 110) ** 2) / (2 * 22.0 ** 2)))
    axes[3].imshow(heat, cmap="magma", vmin=0, vmax=1)
    axes[3].text(4, 192, "score 0.93", fontsize=7, color="white")

    for ax in axes:
        ax.text(0.5, -0.05, "欠陥は 1 つ / one defect", transform=ax.transAxes, ha="center",
                fontsize=7.4, color=MUTED)

    fig.suptitle("模式図：実際のモデル出力ではありません / illustration, not real inference output",
                 fontsize=10)
    _caption(fig, "図：同じ 1 枚・同じ欠陥に対する 4 つの出力（模式図。実際のモデル出力ではありません）。"
                  "必要な正解データが違うことにも注意してください（分類＝画像に 1 ラベル、検出＝四角、"
                  "セグメンテーション＝画素マスク）。 / "
                  "Figure: four task outputs for the same image and the same defect (illustration, not real model "
                  "output). Note that each task needs a different kind of ground truth: one label per image, "
                  "a box, or a pixel mask.", y=-0.06)
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
    # ノートブックの演習と同じ値・同じ規格 / the same values and limits as the notebook exercise
    measurements = [100.0, 100.3, 99.7, 100.6, 99.4]
    nominal, tolerance = 100.0, 0.5
    fig, ax = plt.subplots(figsize=(10.6, 4.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.02, 0.955, "measurements_mm = [100.0, 100.3, 99.7, 100.6, 99.4]",
            fontsize=9, family="monospace")
    ax.text(0.02, 0.905, "def judge(measured_mm, nominal_mm=100.0, tolerance_mm=0.5):", fontsize=8.6,
            family="monospace", color=MUTED)
    ax.text(0.04, 0.862, "difference = round(measured_mm - nominal_mm, 6)", fontsize=8.4,
            family="monospace", color=MUTED)
    ax.text(0.04, 0.822, "if abs(difference) <= tolerance_mm:  →  OK   else  →  NG", fontsize=8.4,
            family="monospace", color=MUTED)

    headers = ["i", "測定値 (mm) / value", "|value − 100.0|", "条件 / condition",
               "判定 / result"]
    x = [0.03, 0.15, 0.34, 0.56, 0.84]
    for xpos, head in zip(x, headers):
        ax.text(xpos, 0.745, head, fontsize=8.5, color=INK, weight="bold")
    for row, value in enumerate(measurements):
        difference = round(abs(value - nominal), 6)
        ok = difference <= tolerance
        y = 0.655 - row * 0.105
        ax.add_patch(Rectangle((0.015, y - 0.035), 0.95, 0.072,
                               facecolor="#eaf7ee" if ok else "#fdecef", edgecolor="none"))
        ax.text(x[0], y, str(row), fontsize=9, family="monospace")
        ax.text(x[1], y, f"{value:.1f}", fontsize=9, family="monospace")
        ax.text(x[2], y, f"{difference:.1f}", fontsize=9, family="monospace")
        ax.text(x[3], y, f"{difference:.1f} <= 0.5 → {'真 / True' if ok else '偽 / False'}",
                fontsize=8.5, family="monospace", color=OK if ok else BAD)
        ax.text(x[4], y, "OK" if ok else "NG", fontsize=9.5, color=OK if ok else BAD, weight="bold")
    ng_indices = [row for row, value in enumerate(measurements)
                  if round(abs(value - nominal), 6) > tolerance]
    ng_text = "、".join(f"i={i}" for i in ng_indices) if ng_indices else "なし / none"
    ax.text(0.02, 0.075,
            f"NG は {len(ng_indices)} 件（{ng_text}）。演習の問題と同じ測定値・同じ規格です。\n"
            f"{len(ng_indices)} NG ({ng_text}) — the same measurements and limits as the exercise.\n"
            "ループは「今どの値か」を毎回確かめる作業です。 / A loop re-checks the current value each time.",
            fontsize=8.2, color=MUTED, va="top", linespacing=1.6)
    _caption(fig, "図：5 つの測定値を順に判定するときの実行トレース（値はノートブックと同じ）/ "
                  "Figure: the trace of judging five measurements in a loop (same values as the notebook)")
    return _save(fig, out)


def teach_function_io(out: Path) -> Path:
    measured, nominal, tolerance = 12.55, 12.50, 0.10
    difference = round(abs(measured - nominal), 6)
    verdict = "OK" if difference <= tolerance else "NG"
    other_measured = 12.92
    other_difference = round(abs(other_measured - nominal), 6)
    other_verdict = "OK" if other_difference <= tolerance else "NG"

    fig, ax = _canvas((10.8, 4.8))
    ax.text(0.5, 0.955, "関数：入力をすべて受け取り、決まりで 1 つの値を返す / "
                        "a function takes every input and returns one value",
            ha="center", fontsize=10.0, color=INK)

    _box(ax, 0.02, 0.32, 0.25, 0.52, "", edge=ACCENT, face="#eef4ff")
    ax.text(0.034, 0.835, "入力 / inputs", fontsize=9.0, color=ACCENT, va="top")
    ax.text(0.034, 0.775,
            f"measured = {measured}\nnominal  = {nominal}\ntolerance = {tolerance}",
            fontsize=8.6, family="monospace", color=INK, va="top", linespacing=1.9)
    ax.text(0.034, 0.470,
            "3 つとも必要です。\nAll three are needed.",
            fontsize=7.6, color=MUTED, va="top", linespacing=1.5)

    _arrow(ax, (0.27, 0.58), (0.31, 0.58))
    _arrow(ax, (0.66, 0.58), (0.70, 0.58), color=OK)
    _box(ax, 0.31, 0.24, 0.35, 0.60, "", edge=ACCENT, face="#f6f9ff")
    ax.text(0.324, 0.835, "関数 / function", fontsize=9.0, color=ACCENT, va="top")
    ax.text(0.324, 0.775,
            "def judge(measured, nominal,\n          tolerance):\n"
            "    diff = abs(measured - nominal)\n"
            "    return \"OK\" if diff <= tolerance\n"
            "              else \"NG\"",
            fontsize=7.8, family="monospace", color=INK, va="top", linespacing=1.7)
    ax.text(0.324, 0.400,
            "決まりを 1 か所にまとめる\none place for the rule",
            fontsize=7.6, color=MUTED, va="top", linespacing=1.5)

    _box(ax, 0.70, 0.32, 0.28, 0.52, "", edge=OK, face="#f2fbf5")
    ax.text(0.714, 0.835, "出力 / output", fontsize=9.0, color=OK, va="top")
    ax.text(0.714, 0.775,
            f"\"{verdict}\"\n\n|{measured} − {nominal}| = {difference:.2f}\n"
            f"{difference:.2f} ≤ {tolerance:.2f}",
            fontsize=8.6, family="monospace", color=INK, va="top", linespacing=1.7)
    ax.text(0.714, 0.455, "1 つの値が返る / one value back", fontsize=7.6, color=MUTED, va="top")

    ax.text(0.02, 0.165,
            f"別の入力では結果が変わります / another input gives another result："
            f"judge({other_measured}, {nominal}, {tolerance}) → |{other_measured} − {nominal}| = "
            f"{other_difference:.2f} > {tolerance:.2f} → \"{other_verdict}\"\n"
            "同じ関数でも、渡した値で答えが決まります。入力にない値で判定することはできません。\n"
            "The answer follows from the values you pass: a value that is not an input cannot decide the result.",
            fontsize=8.0, color=MUTED, va="top", linespacing=1.7)
    _caption(fig, "図：入力 → 決まり → 出力。しきい値（tolerance）も入力の 1 つです（結果は計算値）/ "
                  "Figure: inputs → rule → output; the tolerance is one of the inputs (results computed)")
    return _save(fig, out)


def teach_opencv_pipeline(out: Path) -> Path:
    import cv2

    image = _pvc_sheet(200, defect="spot", seed=51)
    grey = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    threshold_value = 150
    # ノートブックと同じ向き：暗い欠陥を白い前景にする / same polarity as the notebook
    _, foreground = cv2.threshold(grey, threshold_value, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(foreground, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    with_contours = image.copy()
    cv2.drawContours(with_contours, contours, -1, (255, 0, 0), 2)
    foreground_pixels = int((foreground > 0).sum())

    fig, axes = plt.subplots(1, 3, figsize=(11.8, 4.4))
    panels = [
        (image, "① 元の画像 / original",
         "欠陥はまわりより暗い画素です / the defect is darker than its surroundings"),
        (foreground, "② findContours に渡すマスク / the mask passed in",
         f"THRESH_BINARY_INV, T={threshold_value}：画素値 ≤ {threshold_value} が白（前景）"),
        (with_contours, f"③ 輪郭 / contours\n{len(contours)} 個 / found",
         "輪郭は白い前景の境界です / contours follow the white foreground"),
    ]
    for ax, (picture, title, note) in zip(axes, panels):
        if picture.ndim == 2:
            ax.imshow(picture, cmap="gray", vmin=0, vmax=255)
        else:
            ax.imshow(picture)
        ax.set_title(title, fontsize=8.8)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(0.0, -0.07, note, transform=ax.transAxes, fontsize=7.3, color=MUTED, va="top",
                linespacing=1.4)

    axes[1].text(4, 194, f"白 / white = {foreground_pixels} px", fontsize=7.2, color="#ffd166",
                 va="bottom")
    _caption(fig, "図：元の画像 → 実際に findContours へ渡す反転マスク → 輪郭の重ね描き（同じ大きさ・合成画像）/ "
                  "Figure: original → the exact inverted mask passed to findContours → contour overlay "
                  "(same size; computed from a synthetic image)", y=-0.06)
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

    for ax, title in zip(axes, ["① 2 つの四角 / two boxes", "② 交差の面積 / intersection",
                                "③ 和集合 / union"]):
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
    axes[2].text(14, 240, f"A={area_a} + B={area_b} − 交差 {inter} = 和集合 {union} px²",
                 fontsize=7.6, color=INK)

    fig.suptitle(f"IoU = 交差の面積 ÷ 和集合の面積 = {inter} ÷ {union} ≈ {iou:.2f}"
                 "   （0 に近い＝重なりが少ない / near 1 means a tight fit）", fontsize=10)
    _caption(fig, "図：実際に重ねた四角から計算した IoU。和集合 = A + B − 交差（重なりは 1 回だけ数える）/ "
                  "Figure: IoU from actually overlapping boxes; union = A + B − intersection, with the "
                  "overlap counted once")
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Day 4
# ---------------------------------------------------------------------------


def teach_yolo_label_fields(out: Path) -> Path:
    from PIL import Image

    root = Path(__file__).resolve().parents[2]
    image_path = root / "assets" / "yolo_dataset" / "images" / "train" / "train_0002.png"
    label_path = root / "assets" / "yolo_dataset" / "labels" / "train" / "train_0002.txt"
    if not (image_path.is_file() and label_path.is_file()):
        raise FileNotFoundError("assets/yolo_dataset が見つかりません / dataset files are missing")
    image = np.asarray(Image.open(image_path).convert("RGB"))
    height, width = image.shape[:2]
    fields = label_path.read_text(encoding="utf-8").split()
    if len(fields) != 5:
        raise ValueError("the label line must have five fields")
    class_id = int(fields[0])
    cx_n, cy_n, w_n, h_n = (float(value) for value in fields[1:])

    cx, cy = cx_n * width, cy_n * height
    box_w, box_h = w_n * width, h_n * height
    x1, y1 = cx - box_w / 2, cy - box_h / 2

    fig = plt.figure(figsize=(12.2, 5.2))
    ax_img = fig.add_axes([0.01, 0.06, 0.38, 0.84])
    ax_txt = fig.add_axes([0.44, 0.02, 0.56, 0.94])
    ax_txt.set_xlim(0, 1)
    ax_txt.set_ylim(0, 1)
    ax_txt.axis("off")

    ax_img.imshow(image)
    ax_img.add_patch(Rectangle((x1, y1), box_w, box_h, fill=False, edgecolor=BAD, linewidth=2))
    ax_img.plot([cx], [cy], marker="+", color=BAD, markersize=10)
    ax_img.annotate("中心 / centre", xy=(cx, cy), xytext=(cx + 46, cy - 44), fontsize=7.8,
                    color=BAD, arrowprops=dict(arrowstyle="-|>", color=BAD, linewidth=1.0))
    ax_img.annotate("高さ / height", xy=(x1 - 2, cy), xytext=(x1 - 60, cy + 52), fontsize=7.8,
                    color=ACCENT, arrowprops=dict(arrowstyle="-|>", color=ACCENT, linewidth=1.0))
    ax_img.set_title(f"① 画像とラベルの四角 / the image and its box\n"
                     f"train_0002.png（{width} × {height} px, 実データ / real file）", fontsize=8.6)
    ax_img.set_xticks([])
    ax_img.set_yticks([])

    ax_txt.text(0.0, 0.98, "1 行 = 1 つの物体 / one line per object", fontsize=9.4, color=INK,
                va="top")
    ax_txt.text(0.0, 0.915, f"{class_id}", fontsize=10.5, family="monospace", color=BAD, va="top")
    ax_txt.text(0.03, 0.915,
                f" {cx_n:.6f}  {cy_n:.6f}  {w_n:.6f}  {h_n:.6f}",
                fontsize=10.5, family="monospace", color=INK, va="top")
    ax_txt.text(0.0, 0.865, "①", fontsize=8.4, color=BAD, va="top")
    ax_txt.text(0.075, 0.865, "②", fontsize=8.4, color=MUTED, va="top")
    ax_txt.text(0.235, 0.865, "③", fontsize=8.4, color=MUTED, va="top")
    ax_txt.text(0.395, 0.865, "④", fontsize=8.4, color=MUTED, va="top")
    ax_txt.text(0.555, 0.865, "⑤", fontsize=8.4, color=MUTED, va="top")

    ax_txt.text(0.0, 0.815,
                f"① class_id = {class_id}（整数 / integer、正規化しない / not normalized）\n"
                f"② x_center = {cx_n:.6f}  = 中心 x ÷ 画像の幅 / centre x ÷ image width\n"
                f"③ y_center = {cy_n:.6f}  = 中心 y ÷ 画像の高さ / centre y ÷ image height\n"
                f"④ width    = {w_n:.6f}  = 幅 ÷ 画像の幅 / width ÷ image width\n"
                f"⑤ height   = {h_n:.6f}  = 高さ ÷ 画像の高さ / height ÷ image height",
                fontsize=8.0, color=INK, va="top", linespacing=1.9)

    ax_txt.text(0.0, 0.615,
                "0〜1 になるのは ②〜⑤ の 4 つだけです。① はクラス番号で、この研修では "
                "0=黒点 / black_spot、1=傷 / scratch、2=スジ / streak。\n"
                "Only the four geometry values are fractions of the image; ① is the class id.",
                fontsize=7.8, color=MUTED, va="top", linespacing=1.6)

    ax_txt.text(0.0, 0.525,
                f"画素に戻す計算 / converting back to pixels（{width} px の画像）\n"
                f"  x_center : {cx_n:.6f} × {width} = {cx:.2f} px\n"
                f"  y_center : {cy_n:.6f} × {height} = {cy:.2f} px\n"
                f"  width    : {w_n:.6f} × {width} = {box_w:.2f} px\n"
                f"  height   : {h_n:.6f} × {height} = {box_h:.2f} px\n"
                f"  x1 = {cx:.2f} − {box_w:.2f}/2 = {x1:.2f} px、"
                f"y1 = {cy:.2f} − {box_h:.2f}/2 = {y1:.2f} px",
                fontsize=8.0, family="monospace", color=INK, va="top", linespacing=1.7)

    ax_txt.text(0.0, 0.205,
                "左の四角は、この 1 行から計算して描いたものです。欠陥（スジ）を囲んでいます。\n"
                "The box on the left is drawn from this single line, and it encloses the streak.",
                fontsize=8.0, color=MUTED, va="top", linespacing=1.6)
    _caption(fig, "図：実データのラベル 1 行と、その行から描いた四角（数値はラベルファイルの値）/ "
                  "Figure: one real label line and the box it describes (numbers come from the label file)",
             y=0.005)
    return _save(fig, out)


def teach_split_roles(out: Path) -> Path:
    root = Path(__file__).resolve().parents[2]
    folder = root / "assets" / "yolo_dataset" / "images"
    counts = {}
    for split in ("train", "val", "test"):
        counts[split] = len(list((folder / split).glob("*.png"))) if (folder / split).is_dir() else 0
    if not all(counts.values()):
        raise FileNotFoundError("assets/yolo_dataset が見つかりません / dataset images are missing")
    total = sum(counts.values())

    fig, ax = _canvas((11.8, 5.2))
    ax.text(0.5, 0.975, "データの 3 つの役割と、この研修の実際の枚数 / "
                        "the three roles of the data and this course's actual counts",
            ha="center", fontsize=10.5, color=INK)

    rows = [
        ("学習 / train", "モデルが重みを合わせる / weights are fitted", ACCENT, "#eef4ff"),
        ("検証 / validation", "しきい値とモデルの選択 / thresholds and model choice", WARN,
         "#fff8ec"),
        ("試験 / test", "固定した設定の最終評価（1 回）/ final check of the frozen setting", OK,
         "#f2fbf5"),
    ]
    for index, (name, purpose, edge, face) in enumerate(rows):
        y = 0.62 - index * 0.25
        split = ("train", "val", "test")[index]
        share = counts[split] / total * 100
        _box(ax, 0.02, y, 0.44, 0.22,
             f"{name} — {counts[split]} 枚 / images（{share:.1f} %）\n{purpose}",
             edge=edge, face=face, fontsize=8.2)

    _box(ax, 0.52, 0.40, 0.46, 0.45, "", edge=BAD, face="#fdecef")
    ax.text(0.534, 0.825, "分けるときに守ること / rules for splitting", fontsize=9.0, color=BAD,
            va="top")
    ax.text(0.534, 0.765,
            "・撮影セッション・製品ロット単位で分ける\n"
            "  split by capture session or product lot\n"
            "・同じ日に撮った画像を両側に入れない\n"
            "  never put one session on both sides\n"
            "・近い画像が両側にあると、成績は実際より良く見える\n"
            "  near-duplicates on both sides inflate the score\n"
            "・各分割で使ったファイルの一覧を残す\n"
            "  keep the file list for every split",
            fontsize=7.8, color=INK, va="top", linespacing=1.6)

    ax.text(0.52, 0.355,
            f"このデータは train {counts['train']} / val {counts['val']} / test {counts['test']}"
            f"（{counts['train'] / total * 100:.1f} / {counts['val'] / total * 100:.1f} / "
            f"{counts['test'] / total * 100:.1f} %）。\n"
            "60/20/20 はよく使われる例で、このデータの値ではありません。\n"
            f"These are the actual counts ({counts['train']}/{counts['val']}/{counts['test']}); a "
            "60/20/20 split is only a common example.",
            fontsize=7.9, color=MUTED, va="top", linespacing=1.6)
    ax.text(0.52, 0.225,
            "分割の目的は「まだ見ていないデータで測ること」です。\n"
            "4 枚のサムネイルを見ても、学習に使われていないことの証明にはなりません。"
            "ファイル一覧と学習設定で確認します。\n"
            "The point is to measure on unseen data; thumbnails do not prove that. "
            "Check the file lists and the training configuration.",
            fontsize=7.9, color=MUTED, va="top", linespacing=1.6)
    _caption(fig, "図：train / val / test の役割と、assets/yolo_dataset の実際の枚数（合成画像）/ "
                  "Figure: the role of each split and the real file counts in assets/yolo_dataset")
    return _save(fig, out)


def teach_epoch_batch(out: Path) -> Path:
    batch_size, nominal_batch, images = 8, 64, 64
    accumulate = max(1, round(nominal_batch / batch_size))
    batches = images // batch_size
    updates = batches // accumulate
    update_word = "update" if updates == 1 else "updates"

    fig, ax = _canvas((11.8, 5.2))
    ax.text(0.5, 0.965, f"1 epoch = 学習画像 {images} 枚を 1 回ずつ見る / "
                        f"one epoch = one pass over the {images} training images",
            ha="center", fontsize=10.5, color=INK)

    for index in range(3):
        x = 0.02 + index * 0.22
        _box(ax, x, 0.66, 0.19, 0.20,
             f"batch {index + 1}\n{batch_size} 枚 / images\n\n勾配を計算 / gradient",
             edge=ACCENT, face="#eef4ff", fontsize=8.0)
        _arrow(ax, (x + 0.19, 0.76), (x + 0.22, 0.76))
    _box(ax, 0.68, 0.66, 0.28, 0.20, f"…\n全 {batches} batch / {batches} batches in total",
         edge=MUTED, face="#f7f8fa", fontsize=8.0)

    ax.text(0.02, 0.60,
            f"この研修の設定 / course settings：batch = {batch_size}、nbs（nominal batch）= "
            f"{nominal_batch} → {accumulate} batch 分の勾配を貯めて 1 回更新\n"
            f"gradients from {accumulate} batches are accumulated into one optimizer step",
            fontsize=8.0, color=INK, va="top", linespacing=1.6)

    _box(ax, 0.02, 0.26, 0.46, 0.24, "", edge=ACCENT, face="#f6f9ff")
    ax.text(0.034, 0.475, "batch（データローダ）/ data-loader batch", fontsize=8.8, color=ACCENT,
            va="top")
    ax.text(0.034, 0.415,
            "一度にまとめて読む枚数（ここでは 8 枚）。\n勾配はここで計算されます。\n"
            "how many images are read together;\nthe gradient is computed here.",
            fontsize=7.8, color=INK, va="top", linespacing=1.6)

    _box(ax, 0.52, 0.26, 0.46, 0.24, "", edge=OK, face="#f2fbf5")
    ax.text(0.534, 0.475, "optimizer step（重みの更新）/ the update", fontsize=8.8, color=OK,
            va="top")
    ax.text(0.534, 0.415,
            f"貯めた勾配で重みを 1 回動かす操作。\nここでは {accumulate} batch ごとに 1 回。\n"
            f"one move of the weights, every {accumulate}\nbatches with this configuration.",
            fontsize=7.8, color=INK, va="top", linespacing=1.6)

    ax.text(0.02, 0.205,
            f"1 epoch = {batches} batch。勾配の累積があるため、この設定では 1 epoch の更新は "
            f"{updates} 回です。\n"
            f"{batches} batches per epoch; with accumulation this configuration makes {updates} "
            f"weight {update_word} per epoch.\n"
            "warmup の間は学習率を徐々に上げます。学習率と更新回数は設定で変わります。\n"
            "During warmup the learning rate ramps up; the rate and the number of updates are "
            "configuration choices.\n"
            "簡略化：この図は「1 batch = 1 更新」ではありません。 / Simplification: this is not "
            "“one batch, one update”.",
            fontsize=7.9, color=MUTED, va="top", linespacing=1.6)
    _caption(fig, "図：epoch・batch・optimizer step の関係。batch の枚数と更新の回数は別です（模式図）/ "
                  "Figure: epochs, batches and optimizer steps — a batch is not always one update "
                  "(schematic)")
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
    matrix = np.array([[28, 6], [9, 57]])
    fig, ax = plt.subplots(figsize=(7.8, 5.2))
    ax.imshow(matrix, cmap="Blues", vmin=0, vmax=matrix.max())
    labels = [["TP = 28", "FN = 9"], ["FP = 6", "TN = 57"]]
    for row in range(2):
        for column in range(2):
            value = matrix[row, column]
            strong = value > 0.40 * matrix.max()
            ax.text(column, row, labels[row][column], ha="center", va="center", fontsize=13,
                    color="white" if strong else INK, weight="bold" if strong else "normal")
    ax.set_xticks([0, 1], ["予測 NG / predicted NG", "予測 OK / predicted OK"], fontsize=8)
    ax.set_yticks([0, 1], ["実際 NG / actually NG", "実際 OK / actually OK"], fontsize=8)
    ax.set_title("画像単位の混同行列 / image-level confusion matrix\n"
                 "1 マス = 画像 1 枚 / one cell = one image", fontsize=9.5, pad=10)
    ax.set_xlabel("行が「実際」、列が「予測」。物体検出の混同行列（Ultralytics）は軸の向きと"
                  "数える単位が違うので、軸ラベルを必ず読みます。\n"
                  "Rows are truth and columns are prediction here; the detection matrix labels its "
                  "axes differently and counts matches, so read its labels first.",
                  fontsize=7.6, color=MUTED, labelpad=8)
    for spine in ax.spines.values():
        spine.set_visible(False)
    _caption(fig, "図：画像単位の混同行列。色だけで読まず、数字と軸ラベルを読みます / "
                  "Figure: an image-level confusion matrix — read the numbers and axis labels, not the colour")
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
                  "Panel 3 is a teaching simplification, not the model's literal internal state.\n"
                  "実際の PatchCore は CNN の中間特徴マップを使い、1 つの位置は周囲の受容野を"
                  "まとめたものです。 / Real PatchCore uses intermediate CNN feature maps, so one "
                  "location summarizes a neighbourhood.")
    return _save(fig, out)


def teach_score_map_overlay(out: Path) -> Path:
    figure = _pvc_sheet(180, defect="spot", seed=91)
    yy, xx = np.mgrid[0:180, 0:180]
    score = 0.35 * np.exp(-(((xx - 76) ** 2 + (yy - 100) ** 2) / (2 * 16.0 ** 2)))
    score += 0.02 * np.random.default_rng(3).random((180, 180))

    fig, axes = plt.subplots(1, 3, figsize=(11.6, 4.0))
    axes[0].imshow(figure)
    axes[0].set_title("① 元の画像 / original\n（合成画像 / synthetic）", fontsize=9)

    image = axes[1].imshow(score, cmap="magma", vmin=0, vmax=0.4)
    axes[1].set_title("② 異常マップ（合成）/ synthetic map\n共通の色範囲 0.0–0.4", fontsize=9)
    cbar = fig.colorbar(image, ax=axes[1], fraction=0.046)
    cbar.set_label("模式的なスコア / schematic score", fontsize=8)

    axes[2].imshow(figure)
    axes[2].imshow(score, cmap="magma", vmin=0, vmax=0.4, alpha=0.55)
    axes[2].set_title("③ 重ねた表示 / overlay\n（同じ 0.0–0.4 で重ねる）", fontsize=9)

    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
    _caption(fig, "図：元画像・異常マップ・重ね表示を同じ色範囲（0.0–0.4）で並べた合成の模式図です。"
                  "実際の PatchCore の出力ではありません。\n"
                  "同じ値が同じ色になるよう、3 枚で共通の範囲を使っています"
                  "（画像ごとに自動にすると、正常画像でも最も明るい色が出ます）。\n"
                  "Figure: original, score map and overlay on one shared 0.0–0.4 scale — a synthetic "
                  "illustration, not actual PatchCore output.\n"
                  "One shared range means one value, one colour; an automatic range per image can make "
                  "a normal image show the brightest colour.",
             y=-0.02)
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Setup: 手順の流れ / the five-step procedure
# ---------------------------------------------------------------------------


def teach_setup_workflow(out: Path) -> Path:
    fig, ax = _canvas((11.4, 5.8))
    ax.text(0.5, 0.975, "ノートブックの流れ：編集 → 実行 → 出力の確認。エラーは実行のあとの分岐 / "
                        "the loop: edit, run, inspect; an error is a branch after the run",
            ha="center", fontsize=10.5, color=INK)

    _box(ax, 0.03, 0.885, 0.94, 0.07,
         "はじめに / before you start：① ノートブックを開く　② カーネル「Python 3 (AI Vision)」を選ぶ",
         edge=MUTED, face="#f7f8fa", fontsize=8.4)

    tops = [
        ("① セルを編集する / edit the cell",
         "コードを書く・直す\nwrite or fix the code\n\nMarkdown セルは説明を読むだけ\na Markdown cell is text to read"),
        ("② セルを実行する / run the cell",
         "Shift + Enter（または ▶）\n\nカーネルで上から順に動きます\nit runs in the kernel, top to bottom"),
        ("③ 出力を確認する / inspect the output",
         "結果・グラフ・エラーは\nセルの下に出ます\n\nthe result appears below the cell"),
    ]
    for index, (title, body) in enumerate(tops):
        x = 0.03 + index * 0.34
        _box(ax, x, 0.60, 0.28, 0.24, "", edge=ACCENT, face="#f6f9ff")
        ax.text(x + 0.014, 0.815, title, fontsize=9.0, color=ACCENT, va="top")
        ax.text(x + 0.014, 0.745, body, fontsize=7.7, color=INK, va="top", linespacing=1.45)

    for x in (0.31, 0.65):
        _arrow(ax, (x, 0.72), (x + 0.06, 0.72))

    _arrow(ax, (0.17, 0.885), (0.17, 0.845), color=MUTED)

    # error branch: only after the run (②), leading back to the edit (①)
    _arrow(ax, (0.51, 0.60), (0.51, 0.50), color=BAD)
    ax.text(0.52, 0.555, "エラーなら / if it errors", fontsize=7.6, color=BAD)
    _box(ax, 0.37, 0.30, 0.28, 0.20, "", edge=BAD, face="#fff5f6")
    ax.text(0.384, 0.465, "④ エラーを読む / read the error", fontsize=8.8, color=BAD, va="top")
    ax.text(0.384, 0.405,
            "最後の 1 行に理由\nFile \"...\", line N に場所\nthe last line: the reason;\nthe pointed line: the place",
            fontsize=7.6, color=INK, va="top", linespacing=1.45)

    _arrow(ax, (0.37, 0.40), (0.31, 0.40), color=BAD)
    _box(ax, 0.03, 0.30, 0.28, 0.20, "", edge=WARN, face="#fff8ec")
    ax.text(0.044, 0.465, "⑤ 原因のセルを直す / fix it", fontsize=8.8, color=WARN, va="top")
    ax.text(0.044, 0.405,
            "名前・値・しきい値を直す\ncorrect the name, the value\nor the limit",
            fontsize=7.6, color=INK, va="top", linespacing=1.45)
    _arrow(ax, (0.17, 0.50), (0.17, 0.60), color=OK)
    ax.text(0.19, 0.545, "① に戻る / back to ①", fontsize=7.6, color=OK)

    # success branch: only after inspecting the output (③)
    _arrow(ax, (0.85, 0.60), (0.85, 0.50), color=OK)
    ax.text(0.86, 0.555, "期待どおりなら / if as expected", fontsize=7.6, color=OK)
    _box(ax, 0.71, 0.30, 0.28, 0.20, "", edge=OK, face="#f2fbf5")
    ax.text(0.724, 0.465, "⑥ 次のセルへ / continue", fontsize=8.8, color=OK, va="top")
    ax.text(0.724, 0.405,
            "同じ手順を次のセルでも\nrepeat the same loop\nfor the next cell",
            fontsize=7.6, color=INK, va="top", linespacing=1.45)

    _box(ax, 0.03, 0.03, 0.94, 0.21,
         "もう一度実行する前に：エラーは全文を読みます。同じセルを 2 回実行しても、原因が残っていれば同じエラーです。\n"
         "Before re-running, read the whole message: running the same cell twice does not remove a cause that is still there.\n"
         "Kernel → Restart & Run All は「メモリを空にして、上から順に全部やり直す」操作です（古い値で動くのを防ぎます）。\n"
         "Restart & Run All clears the memory and replays every cell in order, so nothing runs on a stale value.",
         edge=ACCENT, face="#f6f9ff", fontsize=8.0)
    _caption(fig, "図：編集 → 実行 → 出力の確認。エラーからの復帰は、実行したあとの分岐です（模式図）/ "
                  "Figure: edit → run → inspect, with error recovery as a branch after the run (schematic)")
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Day 1: 学習と推論 / training versus inference
# ---------------------------------------------------------------------------


def teach_train_vs_inference(out: Path) -> Path:
    fig, ax = _canvas((11.8, 5.2))
    ax.text(0.5, 0.975, "学習（training）と推論（inference）は別の作業です / "
                        "training and inference are different jobs",
            ha="center", fontsize=11, color=INK)

    panels = [
        (0.02, "学習 / TRAINING — 何を合わせるか / what is fitted",
         "定義 / definition：学習データに合わせて\nパラメータ（重み）を決めること\n"
         "fitting the parameters to the training data",
         ["正解付きの例\nlabelled\nexamples", "パラメータを\n合わせる\nfit", "重み\nweights"],
         ACCENT, "#f6f9ff",
         "よくある例：時間がかかる・回数が少ない（再学習は何度でもできる）\n"
         "Typical, not a rule: slow, infrequent — retraining is always possible"),
        (0.51, "推論 / INFERENCE — 何をするか / what is applied",
         "定義 / definition：固定した重みを\n新しい入力に当てること\n"
         "applying the fitted model to a new input",
         ["新しい画像\nnew image", "固定した重みで\n計算\napply", "出力\nOK/NG・枠"],
         WARN, "#fffaf0",
         "よくある例：部品ごとに何度も・速い（バッチ推論や重い推論もある）\n"
         "Typical, not a rule: many times per part, fast; batch inference is possible"),
    ]
    for x, heading, body, minis, edge, face, note in panels:
        _box(ax, x, 0.42, 0.47, 0.49, "", edge=edge, face=face)
        ax.text(x + 0.016, 0.885, heading, fontsize=9.0, color=edge, va="top")
        ax.text(x + 0.016, 0.835, body, fontsize=7.8, color=INK, va="top", linespacing=1.5)
        for index, text in enumerate(minis):
            mx = x + 0.025 + index * 0.148
            _box(ax, mx, 0.585, 0.126, 0.15, text, edge=edge, face="white", fontsize=7.0)
            if index < 2:
                _arrow(ax, (mx + 0.126, 0.66), (mx + 0.148, 0.66), color=edge)
        ax.text(x + 0.016, 0.545, note, fontsize=7.5, color=MUTED, va="top", linespacing=1.5)

    _box(ax, 0.02, 0.05, 0.47, 0.31, "", edge=OK, face="#f2fbf5")
    ax.text(0.036, 0.325, "モデルの重み / model weights", fontsize=8.8, color=OK, va="top")
    ax.text(0.036, 0.270,
            "学習で決まり、学習のあとは凍結されます。\n推論では変えません。\n"
            "Fitted by training, then frozen;\ninference does not change them.",
            fontsize=7.8, color=INK, va="top", linespacing=1.5)

    _box(ax, 0.51, 0.05, 0.47, 0.31, "", edge=ACCENT, face="#eef4ff")
    ax.text(0.526, 0.325, "判定のしきい値 / decision threshold", fontsize=8.8, color=ACCENT,
            va="top")
    ax.text(0.526, 0.270,
            "較正（calibration）で決める設定値です。\n重みを変えずに変えられ、判定だけが変わります。\n"
            "A setting chosen in calibration: changing it\nchanges the decision, not the weights.",
            fontsize=7.8, color=INK, va="top", linespacing=1.5)

    _caption(fig, "図：学習は重みを決める作業、推論は決めた重みを当てる作業（しきい値は別の設定。模式図）/ "
                  "Figure: training fits the weights, inference applies them; the threshold is a separate "
                  "setting (schematic)")
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

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.8))
    ax = axes[0]
    ax.imshow(image)
    ax.add_patch(Rectangle((x1, y1), bw, bh, fill=False, edgecolor=BAD, linewidth=2))
    ax.plot([cx], [cy], marker="+", color=BAD, markersize=10)
    ax.text(x1 - 6, y1 - 6, f"y1={y1}", fontsize=8, color=BAD, ha="right", va="top")
    ax.text(x2 + 6, y1 + 6, f"x2={x2}", fontsize=8, color=BAD, ha="left", va="bottom")
    ax.text(x2 + 6, y2 - 6, f"y2={y2}", fontsize=8, color=BAD, ha="left", va="top")
    ax.annotate(f"x1={x1}", (x1, y1), textcoords="offset points", xytext=(-4, 14),
                fontsize=8, color=BAD, ha="center")
    ax.set_title(f"① 画素座標 / pixel coordinates\n画像サイズ / image size = {w} × {h}", fontsize=9)
    ax.set_xlabel("x（右へ増える / increases to the right）", fontsize=8)
    ax.set_ylabel("y（下へ増える / increases downwards）", fontsize=8)
    ax.set_xticks([0, 60, 120, 180, 239])
    ax.set_yticks([0, 60, 120, 180, 239])
    ax.tick_params(labelsize=7)

    ax2 = axes[1]
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    ax2.set_title("② 4 つの数 → 形式ごとの書き方 / four numbers in different formats", fontsize=9)

    rows = [
        ("左上 / top-left", f"({x1}, {y1})"),
        ("右下 / bottom-right", f"({x2}, {y2})"),
        ("幅 / width", f"{bw} px"),
        ("高さ / height", f"{bh} px"),
        ("中心 / centre", f"({cx:.0f}, {cy:.0f})"),
    ]
    ax2.text(0.02, 0.95, "画素の数 / pixel counts", fontsize=8.6, color=ACCENT)
    for i, (label, value) in enumerate(rows):
        ax2.text(0.04, 0.885 - i * 0.075, label, fontsize=8.0, color=INK)
        ax2.text(0.46, 0.885 - i * 0.075, value, fontsize=8.0, color=INK, family="monospace")

    normalised = [
        ("cx / W", f"{cx / w:.3f}"),
        ("cy / H", f"{cy / h:.3f}"),
        ("w / W", f"{bw / w:.3f}"),
        ("h / H", f"{bh / h:.3f}"),
    ]
    ax2.text(0.02, 0.520, "0〜1 に割った値 / fractions of the image", fontsize=8.6, color=WARN)
    for i, (label, value) in enumerate(normalised):
        ax2.text(0.04, 0.465 - i * 0.058, label, fontsize=8.0, color=INK)
        ax2.text(0.46, 0.465 - i * 0.058, value, fontsize=8.0, color=INK, family="monospace")

    ax2.text(0.02, 0.215,
             "API ごとの形式 / the format each API uses\n"
             "  角 / corners  xyxy = (x1, y1, x2, y2)\n"
             "  cv2.boundingRect → xywh = (x, y, w, h)\n"
             "  Ultralytics box.xywh → xywh（中心と大きさ / centre and size）\n"
             "  YOLO ラベル → class_id cx cy w h（0〜1）",
             fontsize=7.6, family="monospace", color=INK, va="top", linespacing=1.5)

    _caption(fig, "図：画素の数で書いた四角と、画像サイズで割った四角（同じ 1 つの箱）。"
                  "画像全体を一様に拡大・縮小しても 0〜1 の値は変わりませんが、crop や letterbox の"
                  "余白を入れると変わります。 / Figure: one box as pixel counts and as fractions. A "
                  "whole-image resize keeps the fractions; cropping or letterbox padding changes them.")
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

    _caption(fig, "図：同じ 1 回の推論結果を、しきい値で絞り込んでいるだけです"
                  "（緑の実線＝残した検出、灰色の点線＝捨てた検出。合成画像・例示用のスコア）。\n"
                  "3 → 1 → 1：しきい値を上げても、残る数が変わらないことがあります。"
                  "捨てた候補は「存在しない」わけではありません。\n"
                  "Figure: one inference filtered at three thresholds (solid green = kept, dotted grey "
                  "= dropped; synthetic image, illustrative scores).\n"
                  "Raising the threshold cannot increase the kept count, but it can stay the same; "
                  "filtered candidates are dropped, not nonexistent.")
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
        ax.set_title(f"{width} px 幅で標本化 / sampled at {width} px\n{scale:.1f} px/mm",
                     fontsize=8.8)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(0.0, -0.09,
                f"直径 / diameter ≈ {diameter_px:.1f} px   "
                f"中心の明るさの差 / Δ ≈ {signal:.0f}",
                transform=ax.transAxes, fontsize=7.6, color=INK, va="top")

    fig.suptitle(f"同じ視野 {field_mm:.0f} mm を 4 つの画素数で撮像したときの見え方（縮小は双一次補間）/ "
                 f"the same {field_mm:.0f} mm field of view sampled at four widths", fontsize=10)
    _caption(fig, "図：同じ合成画像を縮小し、欠陥の位置を等倍表示。Δ は「欠陥あり」と「欠陥なし」の"
                  "中心画素の差（計算値）です。\n"
                  "画素より小さくても明るさは変わり得ますが、形と位置を安定して判断するには足りません。"
                  "視野と縮小方法でも結果は変わります。\n"
                  "Figure: the same synthetic image downsampled, zoomed at the defect; Δ is the computed "
                  "difference at the centre pixel with and without the defect. A defect smaller than one "
                  "pixel can still change the intensity, but resolving its shape and position is another "
                  "matter; the field of view and the resampling method also change the result.",
             y=-0.05)
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
             ("P3", (142, 124, 38, 34), 0.72)]
    confidence_floor = 0.50

    def iou(a, b):
        ax0, ay0, aw, ah = a
        bx0, by0, bw, bh = b
        ix0, iy0 = max(ax0, bx0), max(ay0, by0)
        ix1, iy1 = min(ax0 + aw, bx0 + bw), min(ay0 + ah, by0 + bh)
        inter = max(0, ix1 - ix0) * max(0, iy1 - iy0)
        union = aw * ah + bw * bh - inter
        return inter / union if union else 0.0

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.8))
    ax = axes[0]
    ax.imshow(_pvc_sheet(220, defect=None, seed=74))
    for name, box in truth:
        ax.add_patch(Rectangle((box[0], box[1]), box[2], box[3], fill=False,
                               edgecolor=ACCENT, linewidth=2))
        ax.text(box[0], box[1] - 5, f"{name}（class 0）", fontsize=8, color=ACCENT)
    for name, box, conf in preds:
        ax.add_patch(Rectangle((box[0], box[1]), box[2], box[3], fill=False,
                               edgecolor=WARN, linewidth=1.6, linestyle="--"))
        ax.text(box[0] + box[2] - 2, box[1] + box[3] + 12, f"{name} {conf:.2f}",
                fontsize=7.6, color=WARN, ha="right")
    ax.set_title("① 正解（青の実線）と予測（橙の点線、すべて class 0）/ truth (solid blue) and "
                 "predictions (dashed orange)", fontsize=8.6)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 220)
    ax.set_ylim(220, 0)

    ax2 = axes[1]
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    ax2.set_title("② 対応づけのルール / the matching rule", fontsize=8.8)
    ax2.text(0.02, 0.93,
             "同じクラス・IoU ≥ 0.50・confidence ≥ 0.50・1 対 1（IoU の高い順に割り当てる）\n"
             "same class, IoU ≥ 0.50, confidence ≥ 0.50, one to one (highest IoU first)",
             fontsize=7.8, color=INK, va="top", linespacing=1.6)

    ax2.text(0.10, 0.80, "予測 / pred", fontsize=8.0, color=MUTED)
    for i, h in enumerate(["GT1", "GT2"]):
        ax2.text(0.46 + i * 0.20, 0.80, h, fontsize=8.4, color=ACCENT)
    for j, (name, box, conf) in enumerate(preds):
        y = 0.73 - j * 0.075
        eligible = conf >= confidence_floor
        ax2.text(0.06, y, f"{name}  conf {conf:.2f}", fontsize=8.2,
                 color=WARN if eligible else MUTED)
        for i, (_, gbox) in enumerate(truth):
            value = iou(box, gbox)
            matched = eligible and value >= 0.5
            ax2.text(0.46 + i * 0.20, y, f"{value:.2f}", fontsize=8.4,
                     color=OK if matched else MUTED, family="monospace")

    outcomes = [
        ("GT1 ↔ P1", "一致（TP）/ matched", OK),
        ("GT2 ↔ P3", "一致（TP）/ matched", OK),
        ("P2", "対応なし → FP / no partner", BAD),
        ("—", "対応のない正解なし / no unmatched truth", MUTED),
    ]
    ax2.text(0.02, 0.455, "結果 / outcome", fontsize=8.6, color=INK)
    for i, (pair, text, colour) in enumerate(outcomes):
        ax2.text(0.04, 0.395 - i * 0.065, pair, fontsize=8.0, color=colour)
        ax2.text(0.26, 0.395 - i * 0.065, text, fontsize=8.0, color=colour)
    ax2.text(0.02, 0.02,
             "画像単位の NG 判定は別の判断で、正解がなくても「対象クラスの検出が残ったか」で行います。\n"
             "The image-level decision is separate: it asks whether a retained target-class detection "
             "exists, and needs no ground truth.",
             fontsize=7.6, color=MUTED, va="bottom", linespacing=1.5)

    _caption(fig, "図：同じクラス・IoU・confidence の条件で 1 対 1 に対応づける模式図（座標は例示用）/ "
                  "Figure: one-to-one matching with a stated class, IoU and confidence policy "
                  "(illustrative coordinates)")
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Setup: 実行状態のストーリーボード / the execution-state storyboard
# ---------------------------------------------------------------------------


def teach_execution_state(out: Path) -> Path:
    fig, ax = _canvas((11.8, 6.0))
    ax.text(0.5, 0.975, "セルを実行すると、何がどこに残るか / what a run leaves behind",
            ha="center", fontsize=11, color=INK)

    phases = [
        ("① 未実行 / not yet run", "In [ ]",
         "このセルはまだ実行していません。\nカーネルのメモリは空とは限らず、\nほかのセルの値は残っています。\n"
         "This cell has not run; the kernel\nmemory is not necessarily empty.",
         MUTED, "#f7f8fa"),
        ("② 実行中 / kernel busy", "In [*]",
         "実行中です。print の出力は\n実行中でも流れます。\nOut の番号は終わってから。\n"
         "While it runs, print output can\nalready stream; Out waits for the end.",
         WARN, "#fff8ec"),
        ("③ 実行完了 / execution completed", "In [3]",
         "終わると番号が入ります。\n値はメモリに残り、表示は\nセルの下に出ます。\n"
         "Finished: the number is filled in;\nvalues stay, output is shown below.",
         OK, "#f2fbf5"),
    ]
    for index, (title, count, body, edge, face) in enumerate(phases):
        x = 0.02 + index * 0.33
        _box(ax, x, 0.56, 0.30, 0.36, "", edge=edge, face=face)
        ax.text(x + 0.014, 0.895, title, fontsize=9.2, color=edge, va="top")
        ax.text(x + 0.014, 0.840, count, fontsize=9.5, family="monospace", color=INK, va="top")
        ax.text(x + 0.014, 0.785, body, fontsize=7.8, color=INK, va="top", linespacing=1.5)
        if index < 2:
            _arrow(ax, (x + 0.30, 0.74), (x + 0.33, 0.74), color=MUTED)

    _box(ax, 0.02, 0.30, 0.47, 0.22, "", edge=ACCENT, face="#eef4ff")
    ax.text(0.034, 0.505, "表示される出力 / what is displayed", fontsize=8.8, color=ACCENT, va="top")
    ax.text(0.034, 0.450,
            "print() の文字、Out[3]、グラフ。\nセルを実行し直すと置き換わります。\n"
            "printed text, Out[3], plots; a re-run\nreplaces them.",
            fontsize=7.8, color=INK, va="top", linespacing=1.5)

    _box(ax, 0.51, 0.30, 0.47, 0.22, "", edge=ACCENT, face="#eef4ff")
    ax.text(0.524, 0.505, "変数と計算結果 / Python variables and cached values", fontsize=8.8,
            color=ACCENT, va="top")
    ax.text(0.524, 0.450,
            "名前 → 値 の対応はカーネルの中。\nセルを消しても Restart まで残ります。\n"
            "names and values live in the kernel until\na restart, even if the cell is deleted.",
            fontsize=7.8, color=INK, va="top", linespacing=1.5)

    _box(ax, 0.02, 0.03, 0.47, 0.24, "", edge=WARN, face="#fff8ec")
    ax.text(0.034, 0.250, "結果 1：古い値で動く（stale state）/ stale state", fontsize=8.8,
            color=WARN, va="top")
    ax.text(0.034, 0.195,
            "上のセルを実行し忘れると、下のセルは\n前の値で計算します。表示が正しく見えても\n値は古いことがあります。\n"
            "A skipped cell makes the next one use the\nold value; the output can still look right.",
            fontsize=7.8, color=INK, va="top", linespacing=1.5)

    _box(ax, 0.51, 0.03, 0.47, 0.24, "", edge=BAD, face="#fff5f6")
    ax.text(0.524, 0.250, "結果 2：名前が無い（NameError）/ undefined name", fontsize=8.8,
            color=BAD, va="top")
    ax.text(0.524, 0.195,
            "その名前をまだ一度も実行していないと\nNameError になります。In [ ] は\n「メモリが空」という意味ではありません。\n"
            "A name never created raises NameError;\nIn [ ] does not mean an empty kernel.",
            fontsize=7.8, color=INK, va="top", linespacing=1.5)

    _caption(fig, "図：実行前・実行中・実行後の状態。表示とメモリは別物です（模式図）/ "
                  "Figure: before, during and after a run — display and memory are different (schematic)")
    return _save(fig, out)


def teach_nameerror_recovery(out: Path) -> Path:
    fig, ax = _canvas((11.8, 4.8))
    ax.text(0.5, 0.965, "NameError は「名前が見つからない」という情報 / "
                        "a NameError says the name does not exist",
            ha="center", fontsize=11, color=INK)

    _box(ax, 0.02, 0.62, 0.30, 0.28, "", edge=BAD, face="#fff5f6")
    ax.text(0.035, 0.855, "① 実行したセル / the cell you ran", fontsize=9, color=BAD, va="top")
    ax.text(0.035, 0.79, "widht_mm = 100.2\nprint(width_mm)",
            fontsize=8.6, family="monospace", color=INK, va="top", linespacing=1.5)
    ax.text(0.035, 0.66, "1 文字ちがう / one letter differs", fontsize=8, color=BAD, va="top")

    _arrow(ax, (0.32, 0.76), (0.38, 0.76), color=BAD)

    _box(ax, 0.38, 0.55, 0.60, 0.35, "", edge=BAD, face="#fff5f6", fontsize=8)
    ax.text(0.395, 0.875, "② 表示されたエラー / the error shown", fontsize=9, color=BAD, va="top")
    ax.text(0.395, 0.815,
            "NameError                                 Traceback (most recent call last)\n"
            "Cell In[4], line 2\n"
            "      1 widht_mm = 100.2\n"
            "----> 2 print(width_mm)\n"
            "\n"
            "NameError: name 'width_mm' is not defined",
            fontsize=7.7, family="monospace", color=INK, va="top", linespacing=1.55)
    ax.annotate("③ 最後の行に理由 / the reason is on the last line",
                xy=(0.655, 0.585), xytext=(0.66, 0.505), fontsize=8, color=BAD, ha="left",
                arrowprops=dict(arrowstyle="-|>", color=BAD, linewidth=1.1))
    ax.annotate("④ どの行か / which line", xy=(0.60, 0.735), xytext=(0.78, 0.44),
                fontsize=8, color=MUTED, ha="left",
                arrowprops=dict(arrowstyle="-|>", color=MUTED, linewidth=1.0))

    steps = [
        ("⑤ 直す / fix", "名前を 1 か所にそろえる\nmake the name identical"),
        ("⑥ もう一度実行 / run again", "同じセルを再実行する\nre-run the same cell"),
    ]
    for index, (title, body) in enumerate(steps):
        x = 0.02 + index * 0.32
        _box(ax, x, 0.28, 0.28, 0.20, "", edge=OK, face="#f2fbf5")
        ax.text(x + 0.012, 0.445, title, fontsize=8.8, color=OK, va="top")
        ax.text(x + 0.012, 0.375, body, fontsize=8, color=INK, va="top", linespacing=1.45)

    ax.text(0.02, 0.20,
            "直したあと / after the fix:  print(width_mm)  →  100.2\n"
            "エラーは失敗の印ではなく、「どの名前が、どこで、なぜ見つからないか」を教えてくれる情報です。\n"
            "An error is not a failure mark: it tells you which name, where, and why it was not found.",
            fontsize=8.4, color=INK, va="top", linespacing=1.6, family="monospace")
    ax.text(0.02, 0.05,
            "セルを 2 回実行しても、NameError は消えません。原因の名前をそろえるまで同じです。 / "
            "Running the cell twice does not clear a NameError; only matching the name does.",
            fontsize=8, color=MUTED, va="bottom")
    _caption(fig, "図：エラーを読んで直す順番（模式図）/ "
                  "Figure: the order for reading and fixing an error (schematic)")
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Day 1: 自動化の中の役割 / the roles inside an inspection system
# ---------------------------------------------------------------------------


def teach_inspection_roles(out: Path) -> Path:
    fig, ax = _canvas((11.8, 5.8))
    ax.text(0.5, 0.975, "検査を自動化するときの役割（簡略化した流れ）/ "
                        "the roles in an automated inspection (a simplified pipeline)",
            ha="center", fontsize=10.5, color=INK)

    roles = [
        ("① 撮る / capture",
         "カメラ・照明・距離・固定\ncamera, lighting, distance,\nfixture — also engineered"),
        ("② 画素値から取り出す / extract",
         "寸法・位置・濃淡・特徴量を\n画素値から取り出す\n\ndimensions, positions,\nintensity, features"),
        ("③ 判定する / decide",
         "人が決めたしきい値か、\n例から学習したモデル\n\na limit set by a person,\nor a learned model"),
        ("④ 動かす / act",
         "ランプ・記録・排出\nlamp, log, reject"),
    ]
    for index, (title, body) in enumerate(roles):
        x = 0.02 + index * 0.25
        _box(ax, x, 0.64, 0.23, 0.26, "", edge=ACCENT, face="#eef4ff")
        ax.text(x + 0.012, 0.875, title, fontsize=8.8, color=ACCENT, va="top")
        ax.text(x + 0.012, 0.815, body, fontsize=7.6, color=INK, va="top", linespacing=1.5)
        if index < 3:
            _arrow(ax, (x + 0.23, 0.77), (x + 0.25, 0.77))

    ax.text(0.02, 0.585,
            "この 4 段階は説明を簡単にした流れで、AI が使える範囲を区切るものではありません。"
            "AI はどの段階にも使えます（例：② の領域抽出、③ のスコア計算）。\n"
            "These four stages are a simplified pipeline, not a boundary of AI: AI can support any "
            "stage — e.g. region extraction in ②, scoring in ③.",
            fontsize=7.9, color=MUTED, va="top", linespacing=1.5)

    _box(ax, 0.02, 0.26, 0.47, 0.24, "", edge=OK, face="#f2fbf5")
    ax.text(0.034, 0.475, "画像はすでに数値 / an image already is numbers", fontsize=8.8,
            color=OK, va="top")
    ax.text(0.034, 0.415,
            "画素値そのものが数値の表です。\n② で決めるのは「その数値から何を取り出すか」。\n"
            "Pixel values already form a table of numbers;\n② decides which features to extract.",
            fontsize=7.7, color=INK, va="top", linespacing=1.5)

    _box(ax, 0.51, 0.26, 0.47, 0.24, "", edge=WARN, face="#fff8ec")
    ax.text(0.524, 0.475, "③ は 2 つに分けて考える / split stage ③", fontsize=8.8,
            color=WARN, va="top")
    ax.text(0.524, 0.415,
            "数で書ける部分は if 文のまま。\n人が例から決める部分だけがモデルになります。\n"
            "The part you can write as a rule stays an\nif-statement; only the fitted part is a model.",
            fontsize=7.7, color=INK, va="top", linespacing=1.5)

    ax.text(0.02, 0.205,
            "「自動化した」と「AI を入れた」は別の話です。① ② ④ の設計が決まっていないと、"
            "③ のモデルを良くしても検査は良くなりません。\n"
            "“Automated” and “AI” are different claims: without a sound ① ② ④, a better model in ③ "
            "does not make the inspection better.",
            fontsize=7.9, color=MUTED, va="top", linespacing=1.6)
    _caption(fig, "図：検査の 4 つの役割（簡略化した流れ。AI はどれにも関われます）（模式図）/ "
                  "Figure: the four roles of an inspection (a simplified pipeline; AI can help with any of them)")
    return _save(fig, out)


def teach_ai_ml_dl_nested(out: Path) -> Path:
    fig, ax = _canvas((11.8, 5.6))
    ax.text(0.5, 0.975, "3 つの言葉は「入れ子」/ the three words nest inside one another",
            ha="center", fontsize=11, color=INK)

    ax.add_patch(Rectangle((0.02, 0.36), 0.46, 0.54, facecolor="#f4f7ff", edgecolor=ACCENT,
                           linewidth=1.8))
    ax.add_patch(Rectangle((0.06, 0.41), 0.36, 0.42, facecolor="#e8f0ff", edgecolor=ACCENT,
                           linewidth=1.6))
    ax.add_patch(Rectangle((0.10, 0.46), 0.24, 0.30, facecolor="#dbe7ff", edgecolor=ACCENT,
                           linewidth=1.6))

    ax.text(0.035, 0.885, "AI（人工知能）/ artificial intelligence", fontsize=9.2, color=ACCENT,
            weight="bold", va="top")
    ax.text(0.075, 0.815, "機械学習 / machine learning", fontsize=9.0, color=INK, weight="bold",
            va="top")
    ax.text(0.115, 0.745, "深層学習 / deep learning", fontsize=8.6, color=INK, weight="bold",
            va="top")
    ax.text(0.115, 0.690,
            "この研修で使うのは\nいちばん内側です\nthis course lives here",
            fontsize=7.8, color=INK, va="top", linespacing=1.6)
    ax.text(0.035, 0.43, "深層学習 ⊂ 機械学習 ⊂ AI", fontsize=8.0, color=MUTED, va="bottom")

    rows = [
        (ACCENT, "AI（人工知能）/ artificial intelligence",
         "人が使う知的な処理を機械で行うもの全般\n"
         "anything a machine does that we call intelligent\n"
         "例 / e.g. ルールベースの推論（エキスパートシステム）"),
        (INK, "機械学習 / machine learning",
         "人が決まりを書かず、例から決まりを決める\n"
         "the rule is fitted from examples, not written by hand\n"
         "例 / e.g. 決定木、SVM、k 近傍法"),
        (INK, "深層学習 / deep learning",
         "多層のニューラルネットで学ぶ\nlearned with a deep neural network\n"
         "例 / e.g. YOLO、PatchCore のバックボーン（ResNet）"),
    ]
    for index, (colour, title, body) in enumerate(rows):
        y = 0.900 - index * 0.215
        ax.text(0.52, y, title, fontsize=8.8, color=colour, weight="bold", va="top")
        ax.text(0.52, y - 0.048, body, fontsize=7.6, color=INK, va="top", linespacing=1.55)

    ax.text(0.02, 0.31,
            "・エキスパートシステム（人が書いたルールで推論する仕組み）は、ルールベースの AI です。\n"
            "  An expert system — reasoning with rules a person wrote — is rule-based AI.\n"
            "・「if 文で書けるから機械学習ではない」とは言えません。学習した決定木は if 文に書き下せます。\n"
            "  A learned decision tree can be written as if-statements, and it is still machine learning.\n"
            "・人が決めた幅のしきい値だけで判定するのは、ふつうの自動化です（例から決めていない）。\n"
            "  A width limit chosen by a person alone is ordinary automation: nothing was fitted from examples.",
            fontsize=7.7, color=MUTED, va="top", linespacing=1.6)
    _caption(fig, "図：AI・機械学習・深層学習の包含関係と、それぞれの例（模式図）/ "
                  "Figure: how AI, machine learning and deep learning nest, with one example each "
                  "(schematic)")
    return _save(fig, out)


def teach_gaussian_vs_skewed(out: Path) -> Path:
    rng = np.random.default_rng(4)
    gauss = rng.normal(100.0, 0.30, 4000)
    skewed = 99.4 + rng.gamma(2.0, 0.30, 4000)      # 平均 100.0、右に長い裾 / long right tail

    def coverage(values):
        lo, hi = values.mean() - 3 * values.std(ddof=1), values.mean() + 3 * values.std(ddof=1)
        return float(((values >= lo) & (values <= hi)).mean()), lo, hi

    cov_g, lo_g, hi_g = coverage(gauss)
    cov_s, lo_s, hi_s = coverage(skewed)

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.6), sharey=True)
    bins = np.linspace(98.4, 102.4, 60)
    for ax, values, name, colour, cov, lo, hi, is_gauss in (
        (axes[0], gauss, "正規分布（ガウス分布）/ Gaussian", ACCENT, cov_g, lo_g, hi_g, True),
        (axes[1], skewed, "右に裾を引く分布 / right-skewed", WARN, cov_s, lo_s, hi_s, False),
    ):
        ax.hist(values, bins=bins, color=colour, alpha=0.75, edgecolor=colour)
        ax.axvline(values.mean(), color=INK, linewidth=1.2)
        for bound in (lo, hi):
            ax.axvline(bound, color=BAD, linestyle="--", linewidth=1.4)
        ax.set_title(f"{name}\n平均 ± 3σ = {lo:.2f} – {hi:.2f}", fontsize=9.2)
        ax.set_xlabel("測定値 / measurement (mm)", fontsize=8.5)
        ax.grid(alpha=0.2)
        extra = "理論値 / theory ≈ 99.73 %" if is_gauss else "99.73 % は使えません / does not apply"
        ax.text(0.03, 0.95,
                f"この範囲に入る割合（実測）/ measured\n{cov * 100:.1f} %\n{extra}",
                transform=ax.transAxes, fontsize=8.2, color=INK, va="top", linespacing=1.5,
                bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=LINE))
    axes[0].set_ylabel("枚数 / number of images", fontsize=8.5)

    fig.suptitle("「μ ± 3σ に約 99.73 %」は正規分布の性質です。左右対称なだけでは、正規分布とは言えません。\n"
                 "About 99.73 % within μ ± 3σ is a Gaussian statement; symmetry alone does not make a "
                 "distribution Gaussian.", fontsize=9.2)
    _caption(fig, "図：合成した 2 つの分布（実測値ではありません）。右の分布では同じ ±3σ でも"
                  f"入る割合が {cov_s * 100:.1f} % で、99.73 % とは言えません。\n"
                  "平均・標準偏差は限られたサンプルから求めた推定値なので、割合も近似です。\n"
                  "Figure: two synthetic distributions, not plant measurements; the fraction here is a "
                  "finite-sample estimate, so it is approximate.\n"
                  "正常画像だけで数えられるのは「正常品を NG とした件数」です。見逃しは欠陥画像がなければ数えられません。\n"
                  "With normal images alone you can count false rejects; misses need defect samples.",
             y=-0.04)
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Day 1: 配列の添字 / array indexing
# ---------------------------------------------------------------------------


def teach_array_indexing(out: Path) -> Path:
    grid = np.arange(42).reshape(6, 7)
    row_slice, col_slice = slice(1, 4), slice(2, 5)
    part = grid[row_slice, col_slice]

    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.4),
                             gridspec_kw={"width_ratios": [1.15, 1.0]})
    ax = axes[0]
    ax.imshow(grid, cmap="Blues", vmin=-6, vmax=48)
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            inside = row_slice.start <= r < row_slice.stop and col_slice.start <= c < col_slice.stop
            ax.text(c, r, str(grid[r, c]), ha="center", va="center", fontsize=9,
                    color="white" if inside else INK,
                    weight="bold" if inside else "normal")
    ax.add_patch(Rectangle((col_slice.start - 0.5, row_slice.start - 0.5),
                           col_slice.stop - col_slice.start, row_slice.stop - row_slice.start,
                           fill=False, edgecolor=BAD, linewidth=2.2))
    ax.set_xticks(range(grid.shape[1]))
    ax.set_xticklabels([f"x={c}" for c in range(grid.shape[1])], fontsize=7.5)
    ax.set_yticks(range(grid.shape[0]))
    ax.set_yticklabels([f"y={r}" for r in range(grid.shape[0])], fontsize=7.5)
    ax.set_xlabel("列 x（右へ増える / columns grow rightwards）", fontsize=8)
    ax.set_ylabel("行 y（下へ増える / rows grow downwards）", fontsize=8)
    ax.set_title(f"image[y, x] = image[行, 列] / row first, then column\n"
                 f"shape = {grid.shape}（6 行 × 7 列）", fontsize=9)

    ax2 = axes[1]
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    ax2.set_title("切り出す / slicing", fontsize=9)
    lines = [
        f"image[{row_slice.start}:{row_slice.stop}, {col_slice.start}:{col_slice.stop}]",
        "",
        f"→ shape {part.shape}（行 × 列）",
        "",
        "切り出した中身 / the values taken out:",
    ]
    ax2.text(0.02, 0.90, "\n".join(lines), fontsize=8.6, family="monospace", color=INK,
             va="top", linespacing=1.6)
    for r in range(part.shape[0]):
        ax2.text(0.06 + r * 0.32, 0.52, str(part[r]), fontsize=8.8, family="monospace",
                 color=INK, va="top")
    ax2.text(0.02, 0.30,
             "行インデックス 1、2、3（上から 2〜4 行目）を選んでいます。/ "
             "row indices 1, 2, 3 — the second to fourth rows.\n"
             "内側の : は「以上・未満」/ the inner : means “from, up to but not including”.\n"
             f"{row_slice.stop} 行目は入りません / row {row_slice.stop} is not included.\n\n"
             "image[2, 3] は 1 つの数、image[2:4, 1:3] は 2 行 2 列のまとまり。\n"
             "image[2, 3] is one number; image[2:4, 1:3] is a 2×2 block.",
             fontsize=8, color=MUTED, va="top", linespacing=1.6)
    _caption(fig, "図：配列の添字は「行（y）→ 列（x）」の順。スライスは終わりの値の手前まで。 / "
                  "Figure: index arrays as row (y) then column (x); a slice stops one short of its end value.")
    return _save(fig, out)


def teach_resize_profile(out: Path) -> Path:
    from PIL import Image

    size = 320
    base = _pvc_sheet(size, defect=None, seed=64).astype(np.float32).mean(axis=2)
    yy, xx = np.mgrid[0:size, 0:size]
    spot = ((xx - 150) ** 2 + (yy - 160) ** 2) <= 3 ** 2
    with_defect = base.copy()
    with_defect[spot] -= 40.0

    widths = [320, 160, 80]
    row_original = 160
    fig, axes = plt.subplots(2, 3, figsize=(11.8, 5.6),
                             gridspec_kw={"height_ratios": [1.25, 1.0]})
    profiles = {}
    for column, width in enumerate(widths):
        img = Image.fromarray(np.clip(with_defect, 0, 255).astype(np.uint8))
        small = np.asarray(img.resize((width, width), Image.BILINEAR), dtype=np.float32)
        row = int(round(row_original * width / size))
        profile = small[row].astype(np.float32)
        positions = np.arange(profile.size) * (size / width)     # 元画像の x に戻す / back to source x
        profiles[width] = (positions, profile)

        crop_pad = 24
        x0 = int(150 * width / size) - crop_pad
        x1 = int(150 * width / size) + crop_pad
        y0 = int(160 * width / size) - crop_pad
        y1 = int(160 * width / size) + crop_pad
        ax = axes[0, column]
        ax.imshow(small[y0:y1, x0:x1], cmap="gray", vmin=0, vmax=255, interpolation="nearest")
        scale_note = "縮小なし / no scaling" if width == size else f"{size / width:.0f} 画素 → 1 画素"
        ax.set_title(f"{width} px（同じ領域・等倍表示）\n"
                     f"same region, shown 1:1\n{scale_note}",
                     fontsize=8.4)
        ax.set_xticks([])
        ax.set_yticks([])

    ax = axes[1, 0]
    ax.plot(profiles[320][0], profiles[320][1], color=ACCENT, linewidth=1.6)
    ax.set_title("断面の明るさ / intensity profile", fontsize=8.6)
    ax.set_xlabel("元画像の x / source x (px)", fontsize=8)
    ax.set_ylabel("画素値 / grey (0–255)", fontsize=8)
    ax.grid(alpha=0.25)
    ax.set_xlim(110, 190)
    for width, colour in ((160, WARN), (80, BAD)):
        axes[1, 1].plot(profiles[width][0], profiles[width][1], marker="o", markersize=3,
                        color=colour, linewidth=1.4, label=f"{width} px")
    axes[1, 1].plot(profiles[320][0], profiles[320][1], color=ACCENT, linewidth=1.2,
                    alpha=0.6, label="320 px")
    axes[1, 1].set_xlim(110, 190)
    axes[1, 1].set_title("縮小すると、この例では落ち込みが浅くなる / "
                         "the dip gets shallower here",
                         fontsize=8.6)
    axes[1, 1].set_xlabel("元画像の x / source x (px)", fontsize=8)
    axes[1, 1].set_ylim(150, 225)
    axes[1, 1].legend(fontsize=7.6, loc="lower right")
    axes[1, 1].grid(alpha=0.25)

    axes[1, 2].axis("off")
    depths = {}
    for width, (positions, profile) in profiles.items():
        depths[width] = float(np.median(np.sort(profile)[:6]) - np.median(profile))
    lines = ["同じ断面を 3 つの解像度で測った結果", "the same cross-section at three scales", ""]
    for width in widths:
        lines.append(f"{width:>3} px : 暗い 6 画素との差 / dip ≈ {abs(depths[width]):.0f}")
    lines += ["", "解像度を上げても、失った情報は戻りません。",
              "Raising the resolution later does not bring information back."]
    axes[1, 2].text(0.02, 0.92, "\n".join(lines), fontsize=8.4, color=INK, va="top",
                    family="monospace", linespacing=1.7)

    fig.suptitle("縮小したときの、同じ断面の測り方 / the cross-section measured at three widths",
                 fontsize=10)
    _caption(fig, "図：同じ合成画像・同じ領域を 3 つの解像度で切り出し、断面の明るさを同じ軸で比べたもの。\n"
                  "落ち込みの深さは計算値です（320 px の断面はそのまま、160・80 px は縮小後）。\n"
                  "Figure: the same synthetic image and region at three resolutions, with the\n"
                  "cross-section profiles drawn on one axis; the dip depths are computed values.\n"
                  "ほかの画像や縮小方法で同じ形になるとは限りません。/ other images or resampling "
                  "methods need not behave the same way.", y=-0.04)
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Day 1: セグメンテーションの 2 種類 / semantic versus instance segmentation
# ---------------------------------------------------------------------------


def teach_segmentation_modes(out: Path) -> Path:
    import cv2

    size = 220
    base = _pvc_sheet(size, defect=None, seed=45)
    yy, xx = np.mgrid[0:size, 0:size]
    # 離れた 2 つの欠陥 / two separated defects
    apart_a = ((xx - 70) ** 2 + (yy - 120) ** 2) <= 18 ** 2
    apart_b = ((xx - 155) ** 2 + (yy - 90) ** 2) <= 13 ** 2
    separated = base.copy()
    separated[apart_a] = [45, 45, 50]
    separated[apart_b] = [60, 55, 45]
    # 触れている 2 つの欠陥 / two touching defects
    touch_a = ((xx - 95) ** 2 + (yy - 110) ** 2) <= 20 ** 2
    touch_b = ((xx - 133) ** 2 + (yy - 110) ** 2) <= 20 ** 2
    touching = base.copy()
    touching[touch_a] = [45, 45, 50]
    touching[touch_b] = [60, 55, 45]

    def regions(mask):
        count, labels = cv2.connectedComponents(mask.astype(np.uint8), connectivity=4)
        sizes = [int((labels == index).sum()) for index in range(1, count)]
        return count - 1, sizes

    separated_regions, separated_sizes = regions(apart_a | apart_b)
    touching_regions, touching_sizes = regions(touch_a | touch_b)

    fig, axes = plt.subplots(1, 4, figsize=(12.2, 4.4))
    panels = [
        (separated, "① 離れた 2 つの欠陥\ntwo separated defects", None),
        (separated, "② セマンティック\n（画素ごとの分類）", apart_a | apart_b),
        (touching, "③ 触れている 2 つの欠陥\ntwo touching defects", None),
        (touching, "④ セマンティック＋連結領域\n（インスタンスは別）", touch_a | touch_b),
    ]
    for ax, (picture, title, mask) in zip(axes, panels):
        ax.imshow(picture)
        if mask is not None:
            overlay = np.zeros((size, size, 4))
            overlay[mask] = [0.85, 0.20, 0.20, 0.55]
            ax.imshow(overlay)
        ax.set_title(title, fontsize=8.6)
        ax.set_xticks([])
        ax.set_yticks([])

    axes[1].text(6, size - 10,
                 f"白い前景の画素 / foreground px = {int((apart_a | apart_b).sum())}",
                 fontsize=7.2, color="white")
    axes[1].text(6, 12, f"連結領域 / regions = {separated_regions}", fontsize=8.0, color="white",
                 weight="bold", va="top",
                 bbox=dict(facecolor="black", alpha=0.55, pad=2.5, edgecolor="none"))
    axes[3].text(6, size - 10, f"前景の画素 / foreground px = {int((touch_a | touch_b).sum())}",
                 fontsize=7.2, color="white")
    axes[3].text(6, 12,
                 f"連結領域 / regions = {touching_regions}\n"
                 f"（インスタンスなら 2 / instances = 2）",
                 fontsize=7.8, color="white", weight="bold", linespacing=1.5, va="top",
                 bbox=dict(facecolor="black", alpha=0.55, pad=2.5, edgecolor="none"))

    _caption(fig, "図：セマンティックセグメンテーションはクラスだけを返します。離れた欠陥は連結領域を数えれば "
                  f"{separated_regions} 個と数えられますが、触れている欠陥は {touching_regions} 個にまとまります。"
                  "1 つずつ区別するにはインスタンスが必要です（合成画像・面積は画素数）。\n"
                  "Figure: semantic segmentation returns only the class. Separated defects can be counted as "
                  f"{separated_regions} connected regions, but touching defects merge into {touching_regions}; "
                  "telling them apart needs instance identities. Areas are pixel counts in this synthetic image.",
             y=-0.06)
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Day 2: 単位の換算 / units and dimensions
# ---------------------------------------------------------------------------


def teach_units_conversion(out: Path) -> Path:
    width_mm, height_mm = 300.0, 200.0
    area_mm2 = width_mm * height_mm
    binary_sum = 0.1 + 0.2                  # 浮動小数点の例 / the floating-point example
    binary_diff = 100.3 - 100.0

    fig, ax = _canvas((11.8, 5.2))
    ax.text(0.5, 0.975, "単位・2 進浮動小数点・丸めは、それぞれ別の話です / "
                        "units, binary floats and rounding are three different things",
            ha="center", fontsize=10.5, color=INK)

    # ① physical units
    ax.text(0.02, 0.925, "① 物理単位 / physical units", fontsize=9.4, color=ACCENT)
    ax.add_patch(Rectangle((0.05, 0.575), 0.22, 0.147, facecolor="#dfe7f3", edgecolor=ACCENT,
                           linewidth=1.5))
    ax.text(0.16, 0.648, f"{width_mm:.0f} × {height_mm:.0f} mm", fontsize=8.6, va="center",
            ha="center")
    ax.annotate("", xy=(0.05, 0.775), xytext=(0.27, 0.775),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, linewidth=1.2))
    ax.text(0.16, 0.790, f"{width_mm:.0f} mm", ha="center", fontsize=8.0)
    ax.annotate("", xy=(0.30, 0.575), xytext=(0.30, 0.722),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, linewidth=1.1))
    ax.text(0.312, 0.648, f"{height_mm:.0f} mm", fontsize=8.0, rotation=90, va="center")
    ax.text(0.325, 0.855,
            f"mm  : {width_mm:.0f} × {height_mm:.0f}\n"
            f"cm  : {width_mm / 10:.1f} × {height_mm / 10:.1f}\n"
            f"m   : {width_mm / 1000:.3f} × {height_mm / 1000:.3f}\n"
            f"µm  : {width_mm * 1000:.0f} × {height_mm * 1000:.0f}\n"
            f"面積 / area : {area_mm2:.0f} mm² = {area_mm2 / 100:.1f} cm²",
            fontsize=8.0, family="monospace", color=INK, va="top", linespacing=1.8)
    ax.text(0.02, 0.52,
            "数値そのものは単位を持ちません。変数名と表の見出しに単位を書きます。\n"
            "単位を間違えると、計算は成功したまま答えだけが狂います。\n"
            "A number carries no unit: put it in the variable name and the column heading.\n"
            "A unit slip leaves the arithmetic valid and the answer wrong.",
            fontsize=7.8, color=MUTED, va="top", linespacing=1.6)

    # ② binary floating point
    ax.text(0.60, 0.925, "② 2 進浮動小数点 / binary floating point", fontsize=9.4, color=ACCENT)
    ax.text(0.60, 0.875,
            f"0.1 + 0.2      = {binary_sum!r}\n"
            f"100.3 − 100.0  = {binary_diff!r}",
            fontsize=8.2, family="monospace", color=INK, va="top", linespacing=1.8)
    ax.text(0.60, 0.775,
            "10 進の 0.3 は 2 進でぴったり表せません。\n"
            "The decimal 0.3 has no exact binary form, so the value is not exactly 0.3.\n"
            "これは単位ではなく、数の表し方の話です。 / this is representation, not units.",
            fontsize=7.8, color=MUTED, va="top", linespacing=1.6)

    # ③ tolerance and rounding policy
    ax.text(0.60, 0.600, "③ 許容差と丸めの取り決め / tolerance and the rounding policy",
            fontsize=9.4, color=ACCENT)
    ax.text(0.60, 0.550,
            "この研修の比べ方 / how this course compares:\n"
            "  difference = round(measured − nominal, 6)\n"
            "  if abs(difference) <= tolerance:  → OK",
            fontsize=8.0, family="monospace", color=INK, va="top", linespacing=1.8)
    ax.text(0.60, 0.430,
            "・丸めは「比べるための取り決め」で、測定の分解能ではありません。\n"
            "  Rounding is a comparison convention, not measurement resolution.\n"
            "・丸めた結果、規格のすぐ外側の値が通ることがあります。\n"
            "  After rounding, a value just outside the limit can pass.\n"
            "・整数の刻みや Decimal を使う方法もあります。\n"
            "  Integer ticks or Decimal avoid this.",
            fontsize=7.8, color=MUTED, va="top", linespacing=1.6)
    _caption(fig, "図：寸法と単位換算・浮動小数点の表れ方・丸めの取り決め（数値はすべて計算値）/ "
                  "Figure: dimensions and unit conversions, how a float is represented, and the rounding "
                  "policy (all values computed)",
             y=0.04)
    return _save(fig, out)


def teach_assign_vs_compare(out: Path) -> Path:
    a = 5
    fig, ax = _canvas((11.4, 5.0))
    ax.text(0.5, 0.975, "= は「名前に結びつける」、== は「聞く」/ = binds a name, == asks", ha="center",
            fontsize=11, color=INK)

    _box(ax, 0.02, 0.56, 0.44, 0.35, "", edge=ACCENT, face="#eef4ff")
    ax.text(0.035, 0.895, "① 代入 / assignment", fontsize=9.4, color=ACCENT, va="top")
    ax.text(0.035, 0.820, "a = 5", fontsize=12, family="monospace", color=INK, va="top")
    ax.text(0.035, 0.735,
            "右を計算して、左の名前に結びつける。\n"
            "この行だけでは何も表示されません。\n"
            "bind the name to the value; the line\nitself prints nothing.",
            fontsize=8.0, color=INK, va="top", linespacing=1.6)

    _box(ax, 0.54, 0.56, 0.44, 0.35, "", edge=WARN, face="#fff8ec")
    ax.text(0.555, 0.895, "② 比較 / comparison", fontsize=9.4, color=WARN, va="top")
    ax.text(0.555, 0.820, "a == 5", fontsize=12, family="monospace", color=INK, va="top")
    ax.text(0.555, 0.735,
            "質問して真偽値が返る。\n"
            "変数は変わらない。\n"
            "asks a question and returns a\nBoolean; nothing is stored.",
            fontsize=8.0, color=INK, va="top", linespacing=1.6)

    ax.text(0.02, 0.515, "実際に計算した値 / the values actually computed", fontsize=8.8,
            color=INK)
    results = [("a == 5", a == 5), ("a == 6", a == 6), ("a > 3", a > 3), ("a != 5", a != 5)]
    for index, (expression, value) in enumerate(results):
        x = 0.02 + index * 0.245
        _box(ax, x, 0.39, 0.22, 0.10, f"{expression}  →  {value}",
             edge=OK if value else BAD, face="#f2fbf5" if value else "#fff5f6", fontsize=8.6)

    fig.text(0.02, 0.32,
             "`a` とだけ書くと 5 が表示されます（最後の式の値）。ただし代入の行そのものは何も表示しません。\n"
             "Typing `a` on its own displays 5 — the value of the last expression — but the assignment line "
             "prints nothing.\n"
             "`if a = 5:` は SyntaxError です。条件の位置に代入は書けません"
             "（書き間違いを見つけるための仕組み）。\n"
             "`if a = 5:` is a SyntaxError: an assignment cannot stand where a condition is expected.",
             fontsize=8.1, color=MUTED, va="top", linespacing=1.7)
    fig.text(0.02, 0.13,
             "`is` は「同じものか」、`==` は「同じ値か」。数や文字列には `==` を使ってください。\n"
             "`is` asks “the same object”, `==` asks “the same value”; use `==` for numbers and strings.",
             fontsize=8.1, color=MUTED, va="top", linespacing=1.7)
    _caption(fig, "図：代入と比較の違い（比較の結果は実際に計算）/ "
                  "Figure: assignment versus comparison (the comparison results are computed)", y=0.03)
    return _save(fig, out)


def teach_traceback_annotated(out: Path) -> Path:
    tolerance, value = 0.0, 12.4
    text = (
        "ZeroDivisionError                         Traceback (most recent call last)\n"
        "Cell In[6], line 3\n"
        "      1 tolerance = 0.0\n"
        "      2 value = 12.4\n"
        "----> 3 ratio = value / tolerance\n"
        "\n"
        "ZeroDivisionError: float division by zero"
    )
    fig, ax = _canvas((11.8, 4.9))
    ax.text(0.5, 0.965, "エラーを読む順番 / the order for reading an error", ha="center",
            fontsize=11, color=INK)

    ax.add_patch(Rectangle((0.02, 0.50), 0.60, 0.38, facecolor="#fff5f6", edgecolor=BAD,
                           linewidth=1.2))
    ax.text(0.365, 0.865, text, fontsize=7.7, family="monospace", color=INK, ha="center",
            va="top", linespacing=1.55)

    marks = [
        ("① 最後の行＝理由 / the last line is the reason", (0.34, 0.515), (0.66, 0.62), BAD),
        ("② どのセル・どの行か / which cell and line", (0.34, 0.795), (0.66, 0.80), MUTED),
        ("③ その行の中身 / the line itself", (0.46, 0.665), (0.66, 0.70), ACCENT),
    ]
    for label, target, text_position, colour in marks:
        ax.annotate(label, xy=target, xytext=text_position, fontsize=8.2, color=colour,
                    arrowprops=dict(arrowstyle="-|>", color=colour, linewidth=1.1))

    fig.text(0.02, 0.475,
             "この例では tolerance = 0.0 のまま割っています。0 で割る計算は、どの言語でもエラーになります。\n"
             "Here the code divides by a tolerance that is still 0; dividing by zero fails in every language.",
             fontsize=8.2, color=INK, va="top", linespacing=1.6)

    steps = [
        ("④ 原因を確かめる / confirm", "print(tolerance)\n→ 0.0", WARN, "#fff8ec"),
        ("⑤ 防ぐ / guard", "if tolerance == 0:\n    raise ValueError(...)\nelse:\n    ratio = value / tolerance",
         OK, "#f2fbf5"),
        ("⑥ 記録する / record", "何をしたら直ったかを\n1 行残す\nwrite one line about the fix", ACCENT,
         "#eef4ff"),
    ]
    for index, (title, body, edge, face) in enumerate(steps):
        x = 0.02 + index * 0.33
        _box(ax, x, 0.08, 0.30, 0.30, "", edge=edge, face=face)
        ax.text(x + 0.012, 0.365, title, fontsize=8.8, color=edge, va="top")
        ax.text(x + 0.012, 0.295, body, fontsize=7.8, color=INK, va="top", family="monospace",
                linespacing=1.6)

    _caption(fig, "図：実際に起きる traceback の読み方と直し方（模式図）/ "
                  "Figure: how to read and fix a traceback like this one (schematic)", y=0.005)
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Day 2: 規格の境界 / the tolerance boundary
# ---------------------------------------------------------------------------


def teach_tolerance_boundary(out: Path) -> Path:
    lower, upper = 11.8, 12.2
    samples = [11.799, 11.800, 12.000, 12.200, 12.201]
    fig, ax = plt.subplots(figsize=(11.4, 4.2))
    ax.set_xlim(11.70, 12.30)
    ax.set_ylim(0.0, 1.85)
    ax.get_yaxis().set_visible(False)
    for spine in ("left", "right", "top"):
        ax.spines[spine].set_visible(False)

    ax.axvspan(lower, upper, color="#eaf7ee", zorder=0)
    ax.plot([11.70, 12.30], [0.80, 0.80], color=INK, linewidth=1.6, zorder=1)
    for bound, label, align in ((lower, f"下限 / lower = {lower:.2f} mm", "right"),
                                (upper, f"上限 / upper = {upper:.2f} mm", "left")):
        ax.axvline(bound, color=ACCENT, linestyle="--", linewidth=1.3, zorder=2)
        ax.text(bound + (-0.008 if align == "right" else 0.008), 0.70, label, ha=align,
                fontsize=8.4, color=ACCENT, va="top")

    outboard = {11.799: (-0.004, "right"), 11.800: (-0.008, "right"),
                12.200: (0.008, "left"), 12.201: (0.004, "left")}
    for index, value in enumerate(samples):
        inside = lower <= value <= upper
        above = index % 2 == 0
        marker = 0.80
        ax.plot([value], [marker], marker="o", markersize=8,
                color=OK if inside else BAD, zorder=3)
        label_y = 1.22 if above else 1.00
        dx, ha = outboard.get(value, (0.0, "center"))
        ax.annotate(f"{value:.3f} → {'OK' if inside else 'NG'}", xy=(value, marker),
                    xytext=(value + dx, label_y), ha=ha, va="bottom",
                    fontsize=8.2, color=OK if inside else BAD,
                    arrowprops=dict(arrowstyle="-", color=OK if inside else BAD, linewidth=0.8))

    ax.set_xlabel("測定値 / measured thickness (mm)", fontsize=8.8)
    ax.set_title("境界は「含む」。含むかどうかは 1 文字で決まる / "
                 "the bounds are inclusive; one character decides it", fontsize=10)
    ax.grid(axis="x", alpha=0.25)

    ax.text(11.705, 1.80,
            f"if {lower} <= x <= {upper}:   → 12.200 mm は OK、12.201 mm は NG\n"
            f"if {lower} <  x <  {upper}:   → 12.200 mm も NG（1 文字の違い）\n"
            "abs(x - 12.0) <= 0.2 と書いても同じ意味（中心 ± 0.2）。",
            fontsize=8.2, color=INK, va="top", family="monospace", linespacing=1.7,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor=LINE))
    _caption(fig, "図：規格 12.0 ± 0.2 mm の境界（点は実際に比較した値）/ "
                  "Figure: the bounds of 12.0 ± 0.2 mm, with the compared values marked")
    return _save(fig, out)


def teach_definition_vs_call(out: Path) -> Path:
    fig, ax = _canvas((11.6, 5.2))
    ax.text(0.5, 0.975, "def は「決める」、呼び出しは「実行する」/ def defines, a call runs",
            ha="center", fontsize=11, color=INK)

    _box(ax, 0.02, 0.50, 0.42, 0.40, "", edge=ACCENT, face="#eef4ff")
    ax.text(0.035, 0.875, "① 定義 / definition", fontsize=9.4, color=ACCENT, va="top")
    ax.text(0.035, 0.800,
            "def judge(value, nominal=12.5, tol=0.1):\n"
            "    diff = abs(value - nominal)\n"
            "    if diff <= tol:\n"
            "        return \"OK\"\n"
            "    return \"NG\"",
            fontsize=8.0, family="monospace", color=INK, va="top", linespacing=1.55)
    ax.text(0.035, 0.555,
            "この時点では何も判定していない。\nNothing is judged yet: the rule only has a name.",
            fontsize=7.8, color=MUTED, va="top", linespacing=1.5)

    _arrow(ax, (0.44, 0.71), (0.50, 0.71))

    _box(ax, 0.50, 0.50, 0.48, 0.40, "", edge=OK, face="#f2fbf5")
    ax.text(0.515, 0.875, "② 呼び出し / call", fontsize=9.4, color=OK, va="top")
    ax.text(0.515, 0.795,
            "judge(12.55)              # 引数 1 つ / one argument\n"
            "judge(12.92, tol=0.05)    # 名前を付けて渡す / by name",
            fontsize=7.8, family="monospace", color=INK, va="top", linespacing=1.6)
    ax.text(0.515, 0.665,
            "→ \"OK\"      （0.05 <= 0.10 / inside）\n"
            "→ \"NG\"      （0.42 > 0.05 / outside）",
            fontsize=8.4, family="monospace", color=INK, va="top", linespacing=1.7)
    ax.text(0.515, 0.555,
            "呼ぶたびに中身が動く。\nThe body runs on every call.",
            fontsize=7.8, color=MUTED, va="top", linespacing=1.5)

    ax.text(0.02, 0.455, "呼ぶたびに中で起きること / what happens inside on each call",
            fontsize=8.8, color=INK)
    trace_rows = [
        ("1 回目 / first", "judge(12.55)", "|12.55 − 12.50| = 0.05 ≤ 0.10", "OK"),
        ("2 回目 / second", "judge(12.92, tol=0.05)", "|12.92 − 12.50| = 0.42 > 0.05", "NG"),
    ]
    for index, (order, call, condition, result) in enumerate(trace_rows):
        y = 0.385 - index * 0.075
        ax.text(0.03, y, order, fontsize=8.2, color=MUTED)
        ax.text(0.16, y, call, fontsize=8.2, family="monospace", color=INK)
        ax.text(0.44, y, condition, fontsize=8.2, family="monospace", color=INK)
        ax.text(0.86, y, result, fontsize=8.6, family="monospace",
                color=OK if result == "OK" else BAD)

    fig.text(0.02, 0.22,
             "同じ定義を、値だけ変えて何度でも呼べる。判定の決まりが 1 か所にあるので、\n"
             "規格が変わったときも直すのは 1 行です。\n"
             "One definition can be called with different values; the rule lives in one place, so a\n"
             "changed specification is a one-line change.",
             fontsize=8.2, color=MUTED, va="top", linespacing=1.7)
    _caption(fig, "図：関数の定義とその呼び出し（判定は実際の計算結果）/ "
                  "Figure: a function definition and its calls (the verdicts are computed)", y=0.03)
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Day 2: 2 値化のしきい値を掃引する / sweeping the threshold
# ---------------------------------------------------------------------------


def _threshold_sweep(grey: np.ndarray, thresholds) -> list[dict]:
    import cv2

    rows = []
    for threshold in thresholds:
        _, binary = cv2.threshold(grey, threshold, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rows.append({
            "threshold": int(threshold),
            "binary": binary,
            "foreground": int((binary > 0).sum()),
            "regions": len(contours),
            "contours": contours,
        })
    return rows


def teach_threshold_sweep(out: Path) -> Path:
    import cv2

    image = _pvc_sheet(200, defect="spot", seed=52)
    grey = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    thresholds = list(range(40, 221, 10))
    sweep = _threshold_sweep(grey, thresholds)

    fig = plt.figure(figsize=(11.8, 6.2))
    grid = fig.add_gridspec(2, 3, height_ratios=[1.0, 1.35], hspace=0.42, wspace=0.22)

    samples = [next(r for r in sweep if r["threshold"] == t) for t in (100, 160, 210)]
    for column, row in enumerate(samples):
        sub = fig.add_subplot(grid[0, column])
        sub.imshow(row["binary"], cmap="gray", vmin=0, vmax=255)
        sub.set_title(f"しきい値 / threshold {row['threshold']}\n"
                      f"前景 {row['foreground']} px・{row['regions']} 領域", fontsize=8.6)
        sub.set_xticks([])
        sub.set_yticks([])

    ax = fig.add_subplot(grid[1, :])
    ax.plot([r["threshold"] for r in sweep], [r["foreground"] for r in sweep],
            marker="o", markersize=3.5, color=ACCENT, label="前景の画素数 / foreground pixels")
    ax.set_xlabel("しきい値 / threshold（THRESH_BINARY_INV：画素値 ≤ T が前景）", fontsize=8.6)
    ax.set_ylabel("前景の画素数 / foreground pixels", fontsize=8.6, color=ACCENT)
    ax.tick_params(labelsize=7.6)
    ax.grid(alpha=0.25)

    ax2 = ax.twinx()
    ax2.plot([r["threshold"] for r in sweep], [r["regions"] for r in sweep],
             marker="s", markersize=3.5, color=BAD, label="連結領域の数 / regions")
    ax2.set_ylabel("連結領域の数 / number of regions", fontsize=8.6, color=BAD)
    ax2.tick_params(labelsize=7.6)
    ax.set_title("しきい値を動かすと、前景の画素数と領域数が同時に動く / "
                 "the foreground pixel count and the region count both move", fontsize=9.6)

    for picked in (100, 160, 210):
        ax.axvline(picked, color=MUTED, linestyle=":", linewidth=1.1)
        row = next(r for r in sweep if r["threshold"] == picked)
        offset = (-64, 10) if row["foreground"] < 1000 else (-64, -30)
        ax.annotate(f"{picked}: {row['foreground']} px\n{row['regions']} 領域",
                    xy=(picked, row["foreground"]), textcoords="offset points",
                    xytext=offset, fontsize=7.2, color=MUTED)

    fig.suptitle(f"同じ 1 枚を、しきい値だけ変えて {len(thresholds)} 通りに処理した結果（合成画像）/ "
                 f"one image, {len(thresholds)} thresholds, everything else unchanged", fontsize=10)
    _caption(fig, "図：しきい値は「どこまでを欠陥と呼ぶか」を決める数。数え方が変わるので、"
                  "しきい値を書かずに面積や個数を比べてはいけません。ここで数えているのは校正前の"
                  "画素数で、mm² ではありません。 / "
                  "Figure: the threshold decides what counts as a defect, so a count is meaningless "
                  "without it; these are pixel counts, not calibrated areas.", y=-0.01)
    return _save(fig, out)


def teach_contour_merge(out: Path) -> Path:
    import cv2

    # 近い 2 つの欠陥と、その間の薄いムラ / two nearby defects with a faint bridge between them
    rng = np.random.default_rng(8)
    size = 200
    grey = 205 + rng.normal(0, 1.2, (size, size))
    yy, xx = np.mgrid[0:size, 0:size]
    spot_a = ((xx - 78) ** 2 + (yy - 100) ** 2) <= 7 ** 2
    spot_b = ((xx - 122) ** 2 + (yy - 100) ** 2) <= 7 ** 2
    bridge = (xx > 78) & (xx < 122) & (np.abs(yy - 100) <= 4)
    grey[spot_a | spot_b] = 55
    grey[bridge] = 150
    grey = np.clip(grey, 0, 255).astype(np.uint8)

    thresholds = list(range(80, 226, 5))
    sweep = _threshold_sweep(grey, thresholds)

    def pick(predicate, fallback):
        for row in sweep:
            if predicate(row):
                return row
        return fallback

    split_row = pick(lambda r: r["regions"] >= 2 and r["foreground"] < 600, sweep[0])
    merge_row = pick(lambda r: r["regions"] == 1 and r["foreground"] > split_row["foreground"],
                     sweep[-1])
    noise_row = max(sweep, key=lambda r: r["regions"])

    fig, axes = plt.subplots(1, 3, figsize=(11.8, 4.2))
    for ax, row, note in (
        (axes[0], split_row, "2 つに分かれる / two regions"),
        (axes[1], merge_row, "つながって 1 つ / merged"),
        (axes[2], noise_row, "背景のムラも拾う / noise too"),
    ):
        ax.imshow(grey, cmap="gray", vmin=0, vmax=255)
        for contour in row["contours"]:
            if cv2.contourArea(contour) < 6:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            ax.add_patch(Rectangle((x, y), w, h, fill=False, edgecolor=BAD, linewidth=1.4))
        ax.set_title(f"しきい値 / threshold = {row['threshold']}\n"
                     f"{row['foreground']} px・{row['regions']} 領域\n{note}", fontsize=8.0)
        ax.set_xticks([])
        ax.set_yticks([])

    counts = [r["regions"] for r in sweep]
    axes[2].text(0.01, -0.12,
                 f"同じ画像でも、領域数は {min(counts)}〜{max(counts)} と動きます。"
                 "低いしきい値では 2 つ、少し上げると 1 つ（つながる）、"
                 "さらに上げると背景のムラで急に増えます。\n"
                 f"The count moves between {min(counts)} and {max(counts)}: two regions, then one "
                 "(merged), then many (background noise).",
                 transform=axes[2].transAxes, fontsize=7.6, color=INK, va="top", linespacing=1.5)
    fig.suptitle("輪郭の数は「しきい値 × 対象の形」で決まる / the region count depends on both the "
                 "threshold and the shape of the defect", fontsize=10)
    _caption(fig, "図：しきい値を上げると、薄いムラが前景に入って領域がつながり、さらに上げると"
                  "背景のムラが増えて数が増えます（合成画像・実際の計算）。"
                  "輪郭は境界の表現で、画素数そのものではありません。 / "
                  "Figure: raising the threshold pulls faint mottling into the foreground (regions merge), "
                  "then background noise adds regions; computed on a synthetic image. A contour is a "
                  "boundary, not a pixel count.", y=-0.09)
    return _save(fig, out)


def teach_distance_345(out: Path) -> Path:
    a = (80, 80)
    b = (380, 480)
    dx, dy = b[0] - a[0], b[1] - a[1]
    distance = float(np.hypot(dx, dy))

    fig, ax = plt.subplots(figsize=(9.8, 5.4))
    ax.set_xlim(40, 460)
    ax.set_ylim(540, 30)
    ax.set_aspect("equal")
    ax.set_facecolor("#f7f8fa")
    ax.set_xticks([0, 100, 200, 300, 400])
    ax.set_yticks([0, 100, 200, 300, 400, 500])
    ax.tick_params(labelsize=7.5)
    ax.set_xlabel("x（右へ増える / increases to the right）", fontsize=8)
    ax.set_ylabel("y（下へ増える / increases downwards）", fontsize=8)
    ax.grid(alpha=0.2)

    ax.plot([a[0], b[0]], [a[1], a[1]], color=ACCENT, linewidth=2.2)
    ax.text((a[0] + b[0]) / 2, a[1] - 22, f"dx = {dx} px", ha="center", fontsize=9.5, color=ACCENT)
    ax.plot([b[0], b[0]], [a[1], b[1]], color=WARN, linewidth=2.2)
    ax.text(b[0] + 14, (a[1] + b[1]) / 2, f"dy = {dy} px", fontsize=9.5, color=WARN, va="center")
    ax.plot([a[0], b[0]], [a[1], b[1]], color=INK, linewidth=1.8, linestyle="--")
    ax.text((a[0] + b[0]) / 2 - 46, (a[1] + b[1]) / 2 + 26,
            f"距離 / distance = {distance:.0f} px", fontsize=9.2, color=INK, rotation=53)

    for point, label, offset in ((a, f"A = {a}", (12, 16)), (b, f"B = {b}", (-104, -22))):
        ax.plot([point[0]], [point[1]], marker="o", markersize=9, color=BAD)
        ax.annotate(label, xy=point, textcoords="offset points", xytext=offset, fontsize=8.8,
                    color=BAD, family="monospace")

    ax.text(60, 420,
            f"d = sqrt(dx² + dy²)\n"
            f"  = sqrt({dx}² + {dy}²)\n"
            f"  = sqrt({dx * dx} + {dy * dy})\n"
            f"  = {distance:.0f} px",
            fontsize=9.2, family="monospace", color=INK, va="top", linespacing=1.8,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor=LINE))
    ax.set_title("2 点の距離は「直角三角形の斜辺」/ the distance between two points is a hypotenuse",
                 fontsize=10)
    _caption(fig, "図：3-4-5 の直角三角形（dx=300, dy=400, 距離=500）。Python では np.hypot(dx, dy) / "
                  "Figure: a 3-4-5 triangle (dx=300, dy=400, distance=500); np.hypot(dx, dy) in Python")
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Day 3: スコアと正しさは別 / a model score is not correctness
# ---------------------------------------------------------------------------


def teach_score_vs_correctness(out: Path) -> Path:
    detections = [
        ("P1", 0.94, True, "欠陥にほぼ一致 / overlaps the defect"),
        ("P2", 0.88, False, "背景のムラ / background mottling"),
        ("P3", 0.71, True, "欠陥の一部だけ / only part of the defect"),
        ("P4", 0.43, True, "小さな欠陥 / a small defect"),
        ("P5", 0.31, False, "反射 / a reflection"),
    ]
    threshold = 0.60
    wrong_high = [name for name, conf, correct, _ in detections if conf >= threshold and not correct]
    right_low = [name for name, conf, correct, _ in detections if conf < threshold and correct]

    fig, ax = plt.subplots(figsize=(10.8, 4.6))
    for name, conf, correct, note in detections:
        ax.scatter([conf], [1.0 if correct else 0.0], s=170,
                   color=OK if correct else BAD, marker="o" if correct else "x",
                   linewidth=2.2, zorder=3)
        ax.annotate(f"{name} {conf:.2f}", (conf, 1.0 if correct else 0.0),
                    textcoords="offset points", xytext=(10, 6), fontsize=8.4,
                    color=OK if correct else BAD)

    ax.axvline(threshold, color=INK, linestyle="--", linewidth=1.6)
    ax.text(threshold + 0.012, 1.35, f"しきい値 / threshold = {threshold:.2f}", fontsize=8.6,
            color=INK)
    ax.set_yticks([0.0, 1.0])
    ax.set_yticklabels(["正しくない / wrong", "正しい / correct"], fontsize=8.6)
    ax.set_ylim(-0.45, 1.55)
    ax.set_xlim(0.2, 1.02)
    ax.set_xlabel("モデルが出した confidence スコア（正しさの確率ではありません）/ a score from the "
                  "model, not a probability of being correct",
                  fontsize=8.6)
    ax.grid(axis="x", alpha=0.25)
    ax.set_title("confidence はモデルが出したスコアで、正しさの保証ではありません / "
                 "confidence is a model score, not a guarantee of correctness", fontsize=9.6)

    ax.text(0.205, -0.42,
            f"しきい値より上なのに正しくない / above the line but wrong: {', '.join(wrong_high) or '—'}\n"
            f"しきい値より下なのに正しい / below the line but correct: {', '.join(right_low) or '—'}\n"
            "だから confidence だけで正しさを語らず、正解と突き合わせて数えます。低いスコアは"
            "「失敗」とは限りません。\n"
            "So confidence alone does not describe correctness: compare with ground truth and count; "
            "a low score is not automatically a failure.",
            fontsize=7.8, color=INK, va="bottom", linespacing=1.6,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=LINE))
    _caption(fig, "図：5 つの検出の confidence と正しさ（座標と値は例示用）/ "
                  "Figure: confidence versus correctness for five detections (illustrative values)",
             y=-0.02)
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Day 4: 学習 1 回の更新 / one training update
# ---------------------------------------------------------------------------


def teach_training_update(out: Path) -> Path:
    batch_size, nominal_batch = 8, 64
    accumulate = max(1, round(nominal_batch / batch_size))
    batches_per_epoch = 64 // batch_size
    updates_per_epoch = batches_per_epoch // accumulate

    fig, ax = _canvas((11.8, 5.4))
    ax.text(0.5, 0.97, "1 つの batch で起きること / what one batch does", ha="center",
            fontsize=11, color=INK)

    steps = [
        ("① 予測する / forward", "8 枚を入力し、\n四角とクラスを出す\npredict boxes and classes",
         ACCENT, "#eef4ff"),
        ("② 間違いを測る / loss", "正解との差を\n1 つの数にする\nthe error as one number",
         WARN, "#fff8ec"),
        ("③ 勾配を求める / backward", "どの重みをどちらへ\n動かすかを計算し、\n勾配を貯める",
         ACCENT, "#eef4ff"),
        ("④ 重みを更新する / step", f"{accumulate} batch 分を\nまとめて 1 回動かす\n"
                                    "one update per group", OK, "#f2fbf5"),
    ]
    for index, (title, body, edge, face) in enumerate(steps):
        x = 0.02 + index * 0.245
        _box(ax, x, 0.64, 0.22, 0.27, "", edge=edge, face=face)
        ax.text(x + 0.012, 0.885, title, fontsize=8.8, color=edge, va="top")
        ax.text(x + 0.012, 0.815, body, fontsize=7.8, color=INK, va="top", linespacing=1.5)
        if index < 3:
            _arrow(ax, (x + 0.22, 0.775), (x + 0.245, 0.775))

    ax.text(0.02, 0.595,
            "① ② ③ は batch ごとに起きます。④ は勾配を貯めたあとに 1 回だけです。\n"
            "① ② ③ happen for every batch; ④ happens once, after the gradients are accumulated.",
            fontsize=7.9, color=MUTED, va="top", linespacing=1.6)

    ax.text(0.02, 0.475, "数え方 / how the numbers are counted", fontsize=9, color=INK)
    numbering = [
        ("batch", f"{batch_size} 枚のまとまり / a group of {batch_size} images"),
        ("optimizer step", f"重みの更新 1 回（{accumulate} batch ごと）/ one update per "
                           f"{accumulate} batches"),
        ("epoch", f"64 枚を 1 周 = {batches_per_epoch} batch = {updates_per_epoch} 回の更新 / "
                  f"one pass = {batches_per_epoch} batches"),
        ("epoch 10", f"更新は {10 * updates_per_epoch} 回 / {10 * updates_per_epoch} updates"),
    ]
    for index, (name, note) in enumerate(numbering):
        y = 0.415 - index * 0.075
        ax.text(0.04, y, name, fontsize=8.4, family="monospace", color=ACCENT)
        ax.text(0.22, y, note, fontsize=8.2, color=INK)

    ax.text(0.62, 0.475, "重みは少しずつしか動かない / weights move a little", fontsize=9,
            color=INK)
    weights = [("w0", 0.512, 0.531), ("w1", -0.208, -0.221), ("w2", 1.004, 0.998)]
    for index, (name, before, after) in enumerate(weights):
        y = 0.415 - index * 0.075
        ax.text(0.64, y, f"{name}", fontsize=8.4, family="monospace", color=INK)
        ax.text(0.70, y, f"{before:+.3f} → {after:+.3f}", fontsize=8.4, family="monospace",
                color=INK)
        ax.text(0.88, y, f"Δ = {after - before:+.3f}", fontsize=8.2, family="monospace",
                color=MUTED)
    ax.text(0.62, 0.215,
            "1 回の更新で変わる量は小さいので、\n何度も繰り返します。\n"
            "warmup の間は学習率を徐々に上げます。\n"
            "One update changes little, so the loop\nrepeats; warmup ramps the learning rate up.",
            fontsize=7.9, color=MUTED, va="top", linespacing=1.6)
    ax.text(0.02, 0.105,
            "推論では ① だけを行い、重みは動かしません。 / Inference runs only ①; the weights stay.",
            fontsize=7.9, color=MUTED, va="top")
    _caption(fig, "図：batch ごとの勾配計算と、まとめて行う 1 回の更新（重みの数値は例示。模式図）/ "
                  "Figure: a gradient per batch and one accumulated update (weight values illustrative)")
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Day 4: データセットの中身 / what the dataset actually contains
# ---------------------------------------------------------------------------


def _dataset_images(root: Path, split: str, limit: int) -> list[Path]:
    folder = root / "assets" / "yolo_dataset" / "images" / split
    return sorted(folder.glob("*.png"))[:limit] if folder.exists() else []


def teach_dataset_contact_sheet(out: Path) -> Path:
    root = Path(__file__).resolve().parents[2]
    splits = [("train", 4), ("val", 4), ("test", 4)]
    picks = {split: _dataset_images(root, split, count) for split, count in splits}
    if any(not paths for paths in picks.values()):
        raise FileNotFoundError("assets/yolo_dataset が見つかりません / dataset images are missing")

    counts = {}
    for split, _count in splits:
        images = list((root / "assets" / "yolo_dataset" / "images" / split).glob("*.png"))
        labels = list((root / "assets" / "yolo_dataset" / "labels" / split).glob("*.txt"))
        boxes = 0
        for label in labels:
            boxes += len([line for line in label.read_text(encoding="utf-8").splitlines() if line.strip()])
        counts[split] = (len(images), len(labels), boxes)

    fig, axes = plt.subplots(3, 4, figsize=(11.6, 8.2))
    from PIL import Image

    for row, (split, _count) in enumerate(splits):
        for column, path in enumerate(picks[split]):
            ax = axes[row, column]
            ax.imshow(np.asarray(Image.open(path).convert("RGB")))
            ax.set_xticks([])
            ax.set_yticks([])
            label_file = root / "assets" / "yolo_dataset" / "labels" / split / f"{path.stem}.txt"
            box_count = 0
            if label_file.exists():
                for line in label_file.read_text(encoding="utf-8").splitlines():
                    parts = line.split()
                    if len(parts) != 5:
                        continue
                    box_count += 1
                    cx, cy, w, h = (float(v) for v in parts[1:])
                    height, width = np.asarray(Image.open(path)).shape[:2]
                    x1, y1 = (cx - w / 2) * width, (cy - h / 2) * height
                    ax.add_patch(Rectangle((x1, y1), w * width, h * height, fill=False,
                                           edgecolor=BAD, linewidth=1.3))
            if row == 0:
                ax.set_title(f"{path.name}", fontsize=7.4)
        axes[row, 0].set_ylabel(
            f"{split}\n{counts[split][0]} 枚 / {counts[split][2]} 個の四角", fontsize=8.6)

    fig.suptitle("この研修で実際に使うデータセット（合成画像・実際のファイル）/ "
                 "the dataset this course actually uses (synthetic images, real files)", fontsize=10)
    _caption(fig, "図：train / val / test の先頭 4 枚ずつ。四角はラベルファイルから描いたもの。"
                  "「枚数」と「四角の数」は別物です（1 枚に複数の欠陥があり得る）。 / "
                  "Figure: the first four images of each split; boxes are drawn from the label files. "
                  "The number of images and the number of boxes are different quantities.\n"
                  "この図で分かるのは見た目とラベルだけです。学習に使われていないことの証明にはなりません"
                  "（ファイル一覧と学習設定で確認）。 / This shows appearance and labels only; it does "
                  "not prove which files trained the model — check the file lists and the training "
                  "configuration.", y=-0.02)
    return _save(fig, out)


def teach_leakage_split(out: Path) -> Path:
    from PIL import Image

    root = Path(__file__).resolve().parents[2]
    source = sorted((root / "assets" / "yolo_dataset" / "images" / "train").glob("*.png"))[:1]
    if not source:
        raise FileNotFoundError("assets/yolo_dataset が見つかりません / dataset images are missing")
    original = np.asarray(Image.open(source[0]).convert("RGB"))
    rng = np.random.default_rng(12)
    # 画素値に ±1 のノイズを加えるだけ。位置はずらしていない。
    # only the pixel intensity changes by ±1 level; nothing is shifted.
    twin = np.clip(original.astype(np.int16) + rng.integers(-1, 2, original.shape), 0, 255)
    twin = twin.astype(np.uint8)
    difference = float(np.abs(original.astype(float) - twin.astype(float)).mean())

    fig = plt.figure(figsize=(11.8, 5.2))
    left = fig.add_axes([0.02, 0.48, 0.20, 0.38])
    right = fig.add_axes([0.24, 0.48, 0.20, 0.38])
    left.imshow(original)
    right.imshow(twin)
    left.set_title("① 撮影セッション A\ntrain_0000.png", fontsize=8.2)
    right.set_title("② ほぼ同じ絵（別ファイル）\ntest_0000.png", fontsize=8.2)
    for ax in (left, right):
        ax.set_xticks([])
        ax.set_yticks([])
    fig.text(0.02, 0.445,
             f"1 枚をコピーし、画素値に ±1 のノイズを加えただけ。位置はずらしていません。\n"
             f"±1 intensity noise only — no spatial shift; mean difference = {difference:.2f}",
             fontsize=7.8, color=MUTED, va="top", linespacing=1.6)

    fig.text(0.50, 0.905, "③ 2 通りの分け方 / two ways to split", fontsize=9.2, color=INK, va="top")
    fig.text(0.50, 0.835,
             "フレームで分ける（誤り）/ split by frame (wrong)\n"
             "  1 枚目 → train、2 枚目 → test\n"
             "→ 試験に「ほぼ答え」が入る / the answer leaks into test",
             fontsize=8.2, color=BAD, va="top", linespacing=1.7)
    fig.text(0.50, 0.665,
             "撮影セッションで分ける（正しい）/ split by capture session (correct)\n"
             "  セッション A（2 枚とも）→ train、セッション B → test\n"
             "→ 別の日に撮った画像で測る / measured on another day's captures",
             fontsize=8.2, color=OK, va="top", linespacing=1.7)

    fig.text(0.02, 0.325,
             "ファイル名もハッシュも違うので、名前や md5 の照合では見つかりません。\n"
             "同じ撮影セッション・同じ製品ロットの画像も、1 つのグループとして片側にまとめます。\n"
             "Different names and hashes hide this from a hash check. Whole capture sessions and "
             "product lots are groups: keep each group on one side.",
             fontsize=8.0, color=MUTED, va="top", linespacing=1.7)
    fig.suptitle("近い画像や同じグループを両側に分けると、成績は実際より良く見えます\n"
                 "near-duplicates or whole groups on both sides make the score look better than it is",
                 fontsize=10, y=0.985)
    _caption(fig, "図：実際のデータセット画像 1 枚をコピーし、画素値に ±1 のノイズを加えた「ほぼ同じ画像」"
                  "（位置は変えていません）/ "
                  "Figure: a copy of one real dataset image with ±1 intensity noise, not a spatial shift.",
             y=0.14)
    return _save(fig, out)


# ---------------------------------------------------------------------------
# Day 5: 正常のばらつき / normal variation versus a defect
# ---------------------------------------------------------------------------


def teach_normal_variation(out: Path) -> Path:
    rng = np.random.default_rng(31)
    base = _pvc_sheet(140, defect=None, seed=99).astype(np.float32).mean(axis=2)
    offsets = [-3.0, 0.0, 2.5, -1.5]      # 同じ正常品でも照明でこれだけ動く / lighting alone moves the mean
    normalish = []
    for offset in offsets:
        noisy = base + offset + rng.normal(0, 1.6, base.shape)
        normalish.append(noisy)
    defect = base.copy()
    defect[60:80, 50:70] -= 26.0

    stats = [(float(patch.mean()), float(patch.std())) for patch in normalish]
    defect_stats = (float(defect.mean()), float(defect.std()))
    good_low = min(mean for mean, _std in stats)
    good_high = max(mean for mean, _std in stats)

    fig, axes = plt.subplots(1, 5, figsize=(12.0, 3.2))
    for index, patch in enumerate(normalish):
        axes[index].imshow(np.clip(patch, 0, 255), cmap="gray", vmin=180, vmax=225)
        mean, std = stats[index]
        axes[index].set_title(f"正常 {index + 1}\n平均 {mean:.1f}・σ {std:.1f}", fontsize=8)
    axes[4].imshow(np.clip(defect, 0, 255), cmap="gray", vmin=180, vmax=225)
    axes[4].set_title(f"欠陥あり / defect\n平均 {defect_stats[0]:.1f}・σ {defect_stats[1]:.1f}",
                      fontsize=8, color=BAD)
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])

    _caption(fig, "図：正常 4 枚は照明とノイズで少しずつ違う（合成画像）。正常の平均は "
                  f"{good_low:.1f}〜{good_high:.1f} に収まるのに、欠陥ありは {defect_stats[0]:.1f} まで下がります。\n"
                  "「いつもと違う」を測るのが異常検知で、「決まった範囲の外」を測るのが規格判定です。"
                  "平均の明るさだけでは異常の難しさは決まりません（形・模様・位置も見ます）。\n"
                  f"Four good parts differ through lighting and noise (synthetic); their means stay between "
                  f"{good_low:.1f} and {good_high:.1f} while the defect drags its mean to {defect_stats[0]:.1f}.\n"
                  "Anomaly detection measures “unlike the others”; a spec measures “outside a fixed limit”, "
                  "and global brightness alone does not establish difficulty.",
             y=-0.04)
    return _save(fig, out)


def teach_memory_bank(out: Path) -> Path:
    rng = np.random.default_rng(17)
    bank = rng.normal(0, 1, (24, 2)) * 0.55 + np.array([0.0, 0.0])
    query_ok = np.array([0.25, -0.30])
    query_ng = np.array([2.05, 1.60])
    d_ok = float(np.linalg.norm(bank - query_ok, axis=1).min())
    d_ng = float(np.linalg.norm(bank - query_ng, axis=1).min())

    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.4),
                             gridspec_kw={"width_ratios": [1.4, 1.0]})
    ax = axes[0]
    ax.scatter(bank[:, 0], bank[:, 1], s=30, facecolors="none", edgecolors=MUTED,
               label=f"メモリバンク / memory bank（{len(bank)} 個の特徴）")
    ax.set_xlim(bank[:, 0].min() - 0.6, max(bank[:, 0].max(), query_ng[0]) + 0.6)
    ax.set_ylim(bank[:, 1].min() - 0.6, max(bank[:, 1].max(), query_ng[1]) + 0.6)
    for point, colour, label, distance, offset in (
        (query_ok, OK, "正常に近いパッチ / a near-normal patch", d_ok, (-90, -26)),
        (query_ng, BAD, "欠陥パッチ / a defective patch", d_ng, (-150, -30)),
    ):
        ax.scatter([point[0]], [point[1]], s=110, marker="*", color=colour, label=label)
        nearest = bank[int(np.argmin(np.linalg.norm(bank - point, axis=1)))]
        ax.plot([point[0], nearest[0]], [point[1], nearest[1]], color=colour, linestyle=":",
                linewidth=1.4)
        ax.annotate(f"最近傍までの距離 / nearest distance = {distance:.2f}",
                    xy=(point[0], point[1]), textcoords="offset points", xytext=offset,
                    fontsize=8, color=colour, ha="left",
                    arrowprops=dict(arrowstyle="-", color=colour, linewidth=0.8))
    ax.set_title("① メモリバンクと 2 つのクエリ / the bank and two queries（2 次元の模式図）",
                 fontsize=9)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(fontsize=7.4, loc="lower right")
    ax.grid(alpha=0.2)

    ax2 = axes[1]
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    ax2.set_title("② 距離がスコアになる / distance becomes the score", fontsize=9)
    ax2.text(0.03, 0.96,
             "1. パッチを特徴ベクトルにする\n"
             "2. メモリバンクの全特徴と距離を測る\n"
             "3. 最も近い 1 つ（または k 個）を選ぶ\n"
             "4. その距離が異常スコア\n\n"
             "1. turn the patch into a feature vector\n"
             "2. measure the distance to every stored feature\n"
             "3. keep the nearest one (or k of them)\n"
             "4. that distance is the anomaly score",
             fontsize=7.8, color=INK, va="top", linespacing=1.6)
    ax2.text(0.03, 0.24,
             f"この図では 正常 {d_ok:.2f} < 欠陥 {d_ng:.2f}。\n"
             "距離の大小が「いつもと違う度合い」になります。\n"
             "The distance is the “unlikeness”; no label is needed for it.",
             fontsize=7.8, color=MUTED, va="top", linespacing=1.6)
    _caption(fig, "図：PatchCore のメモリバンクと最近傍探索（2 次元の模式図。実際の特徴は数百次元）。"
                  "正常データに異常が混ざるとスコアが下がり、見逃しが増えることがありますが、"
                  "必ず永久に検出できなくなるわけではありません。混入した例を取り除いて作り直し、"
                  "別の画像で確認します。 / "
                  "Figure: PatchCore's memory bank and nearest-neighbour search (a 2-D schematic). "
                  "Contaminated normal data can lower scores and add misses, but it does not guarantee "
                  "permanent failure: remove the contaminated images, rebuild and verify on held-out data.")
    return _save(fig, out)


def teach_score_levels(out: Path) -> Path:
    patch_scores = np.array([
        [0.02, 0.05, 0.03, 0.04],
        [0.06, 0.71, 0.55, 0.03],
        [0.03, 0.48, 0.88, 0.05],
        [0.02, 0.04, 0.06, 0.03],
    ])
    image_score = float(patch_scores.max())
    mean_score = float(patch_scores.mean())
    threshold = 0.50
    flagged = patch_scores >= threshold

    fig = plt.figure(figsize=(12.2, 4.6))
    ax = fig.add_axes([0.03, 0.28, 0.17, 0.52])
    ax2 = fig.add_axes([0.23, 0.28, 0.17, 0.52])
    ax3 = fig.add_axes([0.43, 0.04, 0.55, 0.90])
    ax3.axis("off")

    ax.imshow(patch_scores, cmap="magma", vmin=0, vmax=1)
    for row in range(patch_scores.shape[0]):
        for column in range(patch_scores.shape[1]):
            value = patch_scores[row, column]
            ax.text(column, row, f"{value:.2f}", ha="center", va="center", fontsize=8.5,
                    color="black" if value > 0.6 else "white")
    ax.set_title("① パッチごとのスコア\n（おもちゃの例 / toy example）", fontsize=8.8)
    ax.set_xticks([])
    ax.set_yticks([])

    ax2.imshow(patch_scores, cmap="magma", vmin=0, vmax=1)
    for row in range(patch_scores.shape[0]):
        for column in range(patch_scores.shape[1]):
            if flagged[row, column]:
                ax2.add_patch(Rectangle((column - 0.5, row - 0.5), 1, 1, fill=False,
                                        edgecolor=OK, linewidth=2))
    ax2.set_title(f"② 空間に戻す（おもちゃ）\nしきい値 {threshold:.2f} 以上 = "
                  f"{int(flagged.sum())} マス", fontsize=8.8)
    ax2.set_xticks([])
    ax2.set_yticks([])

    ax3.text(0.0, 0.97, "③ 画像 1 枚の値（おもちゃ）/ one number per image", fontsize=9.0,
             color=INK, va="top")
    ax3.text(0.0, 0.885,
             f"画像スコア（最大）/ max here = {image_score:.2f}\n"
             f"画像スコア（平均）/ mean here = {mean_score:.2f}\n"
             f"しきい値 / threshold       = {threshold:.2f}\n"
             f"判定 / decision            = "
             f"{'NG' if image_score >= threshold else 'OK'}",
             fontsize=8.4, family="monospace", color=INK, va="top", linespacing=1.9)
    ax3.text(0.0, 0.600,
             "3 つは別のものです / three different things\n"
             "・パッチのスコア（マスごとの数）\n"
             "・画像のスコア（1 枚を 1 つの数にまとめたもの）\n"
             "・空間マップ（どこが高いかを示す図）",
             fontsize=8.2, color=INK, va="top", linespacing=1.5)
    ax3.text(0.0, 0.380,
             "この研修の設定では、画像スコアは「最大のパッチ距離」を\n"
             "近傍 9 個（num_neighbors=9）の正常特徴で重み付けした値です。\n"
             "表示するマップは補間・平滑化されるため、map.max() とは一致しません。\n"
             "In the course configuration the image score weights the largest patch\n"
             "distance with num_neighbors=9 normal features; the displayed map is\n"
             "interpolated, so map.max() need not equal the image score.\n"
             "この図の値は、仕組みを説明するための簡単な例です / toy values.",
             fontsize=7.4, color=MUTED, va="top", linespacing=1.5)
    _caption(fig, "図：パッチのスコア・画像のスコア・空間マップを混ぜずに読む（値は例示用）/ "
                  "Figure: patch scores, the image score and the spatial map read separately "
                  "(illustrative values)", y=0.0)
    return _save(fig, out)


def teach_backbone_vs_memory(out: Path) -> Path:
    fig, ax = _canvas((11.8, 4.4))
    ax.text(0.5, 0.975, "PatchCore の「学習」で変わるのはメモリバンクだけ / "
                        "only the memory bank is fitted", ha="center", fontsize=11, color=INK)

    _box(ax, 0.02, 0.53, 0.44, 0.39, "", edge=MUTED, face="#f7f8fa")
    ax.text(0.036, 0.895, "① バックボーン（変えない）/ backbone — frozen", fontsize=9.0,
            color=MUTED, va="top")
    ax.text(0.036, 0.835,
            "ResNet-18（ImageNet で学習済み）\n"
            "・重みは 1 つも更新しない\n"
            "・正常画像を通すのに使うだけ\n"
            "ResNet-18, pretrained on ImageNet:\nno weight is updated",
            fontsize=7.6, color=INK, va="top", linespacing=1.55)
    ax.text(0.036, 0.560, "変化しません / unchanged", fontsize=8.0, color=MUTED)

    _arrow(ax, (0.46, 0.725), (0.54, 0.725))

    _box(ax, 0.54, 0.53, 0.44, 0.39, "", edge=OK, face="#f2fbf5")
    ax.text(0.556, 0.895, "② メモリバンク（ここが「学習」）/ the fitted part", fontsize=9.0,
            color=OK, va="top")
    ax.text(0.556, 0.835,
            "正常画像 32 枚の特徴を保存し、\n"
            "コアセットで 10 % に間引く。\n"
            "・画像を足すと中身が増える\n"
            "・同じデータを繰り返しても増えない\n"
            "stores the features of the normal images",
            fontsize=7.6, color=INK, va="top", linespacing=1.55)
    ax.text(0.556, 0.560, "画像を足すと変わる / changes with the data", fontsize=8.0, color=OK)

    ax.text(0.02, 0.470,
            "だから PatchCore では、学習データを入れ替えることが「モデルを直す」ことになります。"
            "YOLO のように epoch を回して重みを調整する作業はありません。\n"
            "With PatchCore, changing the training data is how you change the model; there is no "
            "epoch loop that adjusts weights, unlike YOLO.\n"
            "較正で決める後処理（正規化の統計としきい値）は、メモリバンクとは別に保存されます。 / "
            "The postprocessing fitted in calibration is stored separately from the bank.",
            fontsize=8.0, color=MUTED, va="top", linespacing=1.6)

    comparison = [
        ("何を保存するか / what is stored", "特徴の集合（メモリバンク）/ a set of features"),
        ("何回まわすか / how many passes",
         "この手順では 1 回の走査で足りる / one pass is enough here"),
        ("良くする方法 / how to improve", "正常画像を増やす・そろえる / add or tidy the normal images"),
    ]
    for index, (question, answer) in enumerate(comparison):
        y = 0.295 - index * 0.080
        ax.text(0.03, y, question, fontsize=8.2, color=ACCENT)
        ax.text(0.42, y, answer, fontsize=8.2, color=INK)

    _caption(fig, "図：固定したバックボーンと、データで決まるメモリバンク（模式図）/ "
                  "Figure: the frozen backbone and the data-determined memory bank (schematic)")
    return _save(fig, out)


def teach_evaluation_sequence(out: Path) -> Path:
    fig, ax = _canvas((11.9, 5.2))
    ax.text(0.5, 0.975, "評価の順番を入れ替えると、数字の意味が変わります / "
                        "change the order and the numbers mean something else",
            ha="center", fontsize=10.5, color=INK)

    _box(ax, 0.02, 0.775, 0.96, 0.12,
         "⓪ 分ける / split（学習の前に決める / decide before fitting）：撮影セッション単位で "
         "train / calibration / test の 3 つに分ける",
         edge=MUTED, face="#f7f8fa", fontsize=8.2)

    steps = [
        ("① 学習 / fit", "train の正常画像で\nメモリバンクを作る\nfit on normal train images", ACCENT,
         "#eef4ff"),
        ("② 較正 / calibrate", "calibration で\nしきい値を決める\nchoose the threshold", WARN,
         "#fff8ec"),
        ("③ 固定 / freeze", "しきい値と前処理を\n保存して動かさない\nsave them; do not move them",
         BAD, "#fff5f6"),
        ("④ 評価 / evaluate", "test（holdout）で\n1 回だけ測る\nmeasure once", OK, "#f2fbf5"),
        ("⑤ 報告 / report", "固定した値と\n一緒に報告する\nreport with the frozen values", OK,
         "#f2fbf5"),
    ]
    for index, (title, body, edge, face) in enumerate(steps):
        x = 0.02 + index * 0.196
        _box(ax, x, 0.40, 0.168, 0.30, "", edge=edge, face=face)
        ax.text(x + 0.010, 0.675, title, fontsize=8.4, color=edge, va="top")
        ax.text(x + 0.010, 0.605, body, fontsize=7.4, color=INK, va="top", linespacing=1.5)
        if index < 4:
            _arrow(ax, (x + 0.168, 0.55), (x + 0.194, 0.55), color=edge)

    _box(ax, 0.02, 0.06, 0.96, 0.29,
         "試験結果を見て設定を変えたら、その試験データは「まだ見ていないデータ」ではなくなります。\n"
         "変更後の性能は、新しい未使用データで測ります。同じ設定での再実行は、再現性の確認です。\n"
         "If you change a setting after seeing the test result, that test set is no longer untouched; "
         "measure the revised system on a new holdout.\n"
         "Re-running the same configuration only checks reproducibility — it is not a fresh test.",
         edge=BAD, face="#fff5f6", fontsize=8.2)
    _caption(fig, "図：分割 → 学習 → 較正 → 固定 → 評価 → 報告 の順番（較正から報告へ直接進む近道はありません。模式図）/ "
                  "Figure: split, fit, calibrate, freeze, evaluate, report — in that order, with no "
                  "shortcut from calibration to reporting (schematic)")
    return _save(fig, out)


def teach_threshold_freeze(out: Path) -> Path:
    root = Path(__file__).resolve().parents[2]
    sheet = root / "assets" / "anomaly_dataset" / "pvc_sheet" / "test"
    if not sheet.is_dir():
        raise FileNotFoundError("assets/anomaly_dataset が見つかりません / anomaly images are missing")
    normal_total = len(list((sheet / "good").glob("*.png")))
    abnormal_total = sum(len(list(folder.glob("*.png"))) for folder in sheet.iterdir()
                         if folder.is_dir() and folder.name != "good")
    # この研修の実行では test 側を半分に分けて較正用にした / the run split the test images in half
    calibration_normal, calibration_abnormal = normal_total // 2, abnormal_total // 2

    scores = {
        "YOLO": dict(
            normal=[0.01, 0.02, 0.02, 0.03, 0.04, 0.05],
            abnormal=[0.22, 0.26, 0.31, 0.35, 0.41, 0.44, 0.48, 0.52, 0.55, 0.58,
                      0.62, 0.66, 0.70, 0.74, 0.79, 0.84, 0.88, 0.91, 0.95, 0.98]),
        "PatchCore": dict(
            normal=[0.05, 0.12, 0.18, 0.24, 0.31, 0.36],
            abnormal=[0.52, 0.54, 0.56, 0.58, 0.60, 0.62, 0.64, 0.66, 0.68, 0.70,
                      0.72, 0.74, 0.76, 0.78, 0.80, 0.83, 0.86, 0.89, 0.94, 0.98]),
    }
    candidates = {"YOLO": (0.06, 0.15, 0.30), "PatchCore": (0.40, 0.50, 0.70)}
    FROZEN = {"YOLO": 0.06, "PatchCore": 0.50}      # 記録された実行の値 / values from the recorded run

    fig, axes = plt.subplots(1, 2, figsize=(11.9, 4.8), sharex=True)
    for ax, (method, data) in zip(axes, scores.items()):
        normal = np.array(data["normal"])
        abnormal = np.array(data["abnormal"])
        ax.scatter(normal, np.full_like(normal, 1.0), s=55, color=ACCENT, marker="o",
                   label=f"正常 / normal（n={normal.size}）")
        ax.scatter(abnormal, np.full_like(abnormal, 0.0), s=55, color=BAD, marker="x",
                   label=f"異常 / abnormal（n={abnormal.size}）")
        ax.set_yticks([0.0, 1.0])
        ax.set_yticklabels(["異常 / abnormal", "正常 / normal"], fontsize=8.4)
        ax.set_ylim(-0.75, 1.6)
        ax.set_xlim(-0.02, 1.02)
        ax.set_xlabel("較正用データのスコア / score on the calibration partition", fontsize=8.4)
        ax.grid(axis="x", alpha=0.25)
        ax.legend(fontsize=7.0, loc="lower right", ncol=1)

        lines = []
        for threshold in candidates[method]:
            missed = int((abnormal < threshold).sum())
            false_alarm = int((normal >= threshold).sum())
            lines.append(f"{threshold:.2f} → 見逃し {missed} / {abnormal.size}・"
                         f"誤報 {false_alarm} / {normal.size}")
            ax.axvline(threshold, color=MUTED, linestyle=":", linewidth=1.1)
        frozen = FROZEN[method]
        ax.axvline(frozen, color=OK, linewidth=2.4)
        ax.text(frozen + 0.012, 1.30, f"固定 / frozen = {frozen:.2f}", fontsize=8.2, color=OK)
        ax.text(0.02, -0.68, "\n".join(lines), fontsize=7.2, color=INK, va="bottom",
                family="monospace")
        ax.set_title(f"{method}: 較正用データだけを見る / calibration data only", fontsize=9.2)

    fig.suptitle(f"しきい値は較正用データで決めて固定する（較正用 {calibration_normal + calibration_abnormal} 枚 = "
                 f"異常 {calibration_abnormal} + 正常 {calibration_normal}）/ fix the threshold on "
                 f"calibration data only", fontsize=9.8)
    _caption(fig, "図：較正用データ上のスコアと、しきい値を動かしたときの見逃し・誤報。"
                  "スコアの値は例示用、しきい値 0.06 / 0.50 と分母は記録された実行の値です。\n"
                  f"正常 {calibration_normal} 枚で誤報率 10 % 以下とは、この 6 枚での誤報 0 件のこと。"
                  "6 枚では母集団の誤報率を保証できません。\n"
                  "Figure: scores are illustrative; the frozen thresholds and the denominators come "
                  "from the recorded run. Zero false rejects in six normal images does not establish a "
                  "production rate below 10 %.",
             y=-0.03)
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
    # --- added: the explanations that used to be text only -------------------
    "teach_execution_state.png": teach_execution_state,
    "teach_nameerror_recovery.png": teach_nameerror_recovery,
    "teach_inspection_roles.png": teach_inspection_roles,
    "teach_ai_ml_dl_nested.png": teach_ai_ml_dl_nested,
    "teach_gaussian_vs_skewed.png": teach_gaussian_vs_skewed,
    "teach_array_indexing.png": teach_array_indexing,
    "teach_resize_profile.png": teach_resize_profile,
    "teach_segmentation_modes.png": teach_segmentation_modes,
    "teach_units_conversion.png": teach_units_conversion,
    "teach_assign_vs_compare.png": teach_assign_vs_compare,
    "teach_traceback_annotated.png": teach_traceback_annotated,
    "teach_tolerance_boundary.png": teach_tolerance_boundary,
    "teach_definition_vs_call.png": teach_definition_vs_call,
    "teach_threshold_sweep.png": teach_threshold_sweep,
    "teach_contour_merge.png": teach_contour_merge,
    "teach_distance_345.png": teach_distance_345,
    "teach_score_vs_correctness.png": teach_score_vs_correctness,
    "teach_training_update.png": teach_training_update,
    "teach_dataset_contact_sheet.png": teach_dataset_contact_sheet,
    "teach_leakage_split.png": teach_leakage_split,
    "teach_normal_variation.png": teach_normal_variation,
    "teach_memory_bank.png": teach_memory_bank,
    "teach_score_levels.png": teach_score_levels,
    "teach_backbone_vs_memory.png": teach_backbone_vs_memory,
    "teach_evaluation_sequence.png": teach_evaluation_sequence,
    "teach_threshold_freeze.png": teach_threshold_freeze,
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
