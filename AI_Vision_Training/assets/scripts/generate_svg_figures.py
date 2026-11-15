"""Editable, offline teaching vectors and PDF-compatible PNGs from the same drawing operations."""

from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from teaching_data import (
    BBOX_IMAGE_SIZE, BBOX_XYXY, MASS_INPUTS,
    calibrated_defects, mask_box, spot_mask,
)

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "assets" / "helpers"))
from aivision import find_japanese_font  # noqa: E402

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
BLUE, AMBER, GREEN, RED, VIOLET = "#1f6feb", "#9a6700", "#1a7f37", "#a40e26", "#8250df"
INK = "#24292f"
FONT = "Yu Gothic, Meiryo, Noto Sans JP, sans-serif"

# Each tuple maps the figure to its lesson, anchor and bilingual prediction prompt.
FIGURES = {
    "teach_code_cell_lifecycle": ("00_Environment_Setup", "Part 4", "値はセルではなくカーネルに残ります。", "Values persist in the kernel, not the cell.",
        "加算セルだけをもう一度実行すると、4 は何になりますか。", "What happens to 4 if only the increment cell runs again?"),
    "teach_pixel_inspector": ("Day01_02_Pixels_and_Images", "canvas = np.zeros", "行が y、列が x です。", "Rows are y; columns are x.",
        "canvas[2, 3] と canvas[3, 2] は同じですか。", "Are canvas[2, 3] and canvas[3, 2] the same?"),
    "teach_slice_walkthrough": ("Day01_02_Pixels_and_Images", "canvas = np.zeros", "終点の番号は含めません。", "The stop index is excluded.",
        "[1:4, 2:5] の列の終点を 6 に変えると shape はどうなりますか。", "What shape results if the column stop changes from 5 to 6?"),
    "teach_cv_tasks_outputs": ("Day01_03_Computer_Vision_Tasks", "teach_cv_tasks_outputs.png", "同じマスクから四角を求めます。", "The box is derived from the same mask.",
        "マスクの画素数と四角の面積は等しいですか。", "Does mask pixel count equal box area?"),
    "teach_mass_units_chain": ("Day02_01_Python_Basics", "演習 2（中級）", "面積と体積を区別します。答えは自分で計算します。", "Separate area from volume; calculate the answer yourself.",
        "厚さだけを2倍にすると、面積と重さはどう変わりますか。", "If only thickness doubles, what happens to area and mass?"),
    "teach_if_live_trace": ("Day02_02_Conditions_Loops_Functions", "measured_mm = 100.3", "表示の丸めを判定に使いません。", "Display rounding is not the acceptance policy.",
        "100.5001 mm に変えるとどちらの枝を通りますか。", "Which branch runs for 100.5001 mm?"),
    "teach_opencv_pixel_pipeline": ("Day02_03_OpenCV_Image_Processing", "Part 2", "しきい値と面積の条件は別です。", "Intensity threshold and area filter are different.",
        "画素値がしきい値と等しいと、反転マスクでは何になりますか。", "What does inverse threshold output when a pixel equals the threshold?"),
    "teach_calibration_same_plane": ("Day02_03_OpenCV_Image_Processing", "calibrated_defects.png", "基準線と対象は同じ画像・平面です。", "Reference and targets share one image and plane.",
        "倍率を2倍に仮定すると、同じ px² の mm² は何倍ですか。", "If assumed px/mm doubles, how does the same px² convert to mm²?"),
    "teach_bbox_one_example": ("Day03_01_YOLO_Concepts", "image_width, image_height = 240", "class_id は整数で、正規化しません。", "class_id is an integer and is not normalised.",
        "x2 だけを24 px増やすと中心と幅はどう変わりますか。", "How do centre and width change if only x2 grows by 24 px?"),
    "teach_yolo_result_object": ("Day03_02_YOLO_Inference", "Part 1", "confidence はモデルのスコアで、正解の保証ではありません。", "Confidence is a model score, not a guarantee of truth.",
        "検出が0件なら、表には何行ありますか。", "How many table rows are there when no box is detected?"),
    "teach_epoch_batch_step": ("Day04_02_YOLO_Training", "EPOCHS = 15", "バッチ数と更新回数は同じとは限りません。", "Batch count need not equal optimizer update count.",
        "64枚で batch=4 にすると、1 epoch のバッチ数はどうなりますか。", "With 64 images and batch=4, how many batches make one epoch?"),
    "teach_detection_matching": ("Day04_03_YOLO_Evaluation", "Part 3", "同じクラスの四角を1対1で対応させます。", "Match same-class boxes one to one.",
        "1つの正解に予測が2つ重なると、両方がTPですか。", "If two predictions overlap one truth box, are both TP?"),
    "teach_patchcore_stages": ("Day05_02_PatchCore_Training", "model = Patchcore(", "画像座標と特徴空間を区別します。", "Distinguish image coordinates from feature space.",
        "正常メモリに異常を入れると、距離による判定はどう変わりそうですか。", "What could happen if anomalies enter the normal memory?"),
    "teach_frozen_threshold_pipeline": ("Day05_03_YOLO_vs_PatchCore", "固定したしきい値で", "試験から調整へ戻る矢印はありません。", "There is no feedback from test into tuning.",
        "試験結果を見て設定を変えたら、最終評価には何が必要ですか。", "After tuning on test results, what is needed for a final evaluation?"),
    "teach_group_split_vs_frame_split": ("Day04_01_YOLO_Dataset_Annotation", "import hashlib", "同じ撮影群を分割の境界に置きません。", "Keep an acquisition group on one side of the split.",
        "別のファイル形式なら SHA-256 が違っても独立した画像ですか。", "Does a different SHA-256 after re-encoding prove independence?"),
}


class Canvas:
    def __init__(self, title: str, provenance: str = "schematic", height: int = 590):
        self.height = height
        self.root = ET.Element(f"{{{NS}}}svg", {"viewBox": f"0 0 900 {height}", "width": "900",
                                              "height": str(height), "role": "img"})
        ET.SubElement(self.root, f"{{{NS}}}title").text = title
        self.preview = Image.new("RGB", (1800, height * 2), "white")
        self.draw = ImageDraw.Draw(self.preview)
        font = find_japanese_font()
        if font is None:
            raise RuntimeError("Japanese font required for PNG preview generation")
        self.font_path = str(font)
        self.rect(0, 0, 900, height, "white")
        self.text(24, 36, title, 23)
        self.text(24, height - 18, f"出典 / source: {provenance}", 15)

    def rect(self, x: float, y: float, w: float, h: float, fill: str, stroke: str = "#d0d7de"):
        ET.SubElement(self.root, f"{{{NS}}}rect", {
            "x": str(x), "y": str(y), "width": str(w), "height": str(h), "fill": fill, "stroke": stroke,
        })
        self.draw.rectangle((x * 2, y * 2, (x + w) * 2, (y + h) * 2),
                            fill=None if fill == "none" else fill, outline=stroke, width=2)

    def text(self, x: float, y: float, value: str, size: int = 19, color: str = INK):
        font = ImageFont.truetype(self.font_path, size * 2)
        width = self.draw.textlength(value, font=font) / 2
        if x < 0 or x + width > 890 or y - size < 0 or y + size * 0.25 > self.height:
            raise ValueError(f"Text outside canvas: {value!r}")
        element = ET.SubElement(self.root, f"{{{NS}}}text", {
            "x": str(x), "y": str(y), "font-size": str(size), "font-family": FONT,
            "fill": color, "data-text-width": f"{width:.2f}",
        })
        element.text = value
        self.draw.text((x * 2, y * 2), value, font=font, fill=color, anchor="ls")

    def panel(self, index: int, heading: str, lines: list[str], color: str = BLUE):
        x, y = 24 + (index % 2) * 438, 62 + (index // 2) * 157
        self.rect(x, y, 414, 141, "#f6f8fa", color)
        self.text(x + 14, y + 29, heading, 20, color)
        for row, value in enumerate(lines):
            self.text(x + 14, y + 59 + row * 27, value, 18)

    def line(self, x1: float, y1: float, x2: float, y2: float, color: str = BLUE):
        ET.SubElement(self.root, f"{{{NS}}}line", {
            "x1": str(x1), "y1": str(y1), "x2": str(x2), "y2": str(y2),
            "stroke": color, "stroke-width": "2",
        })
        self.draw.line((x1 * 2, y1 * 2, x2 * 2, y2 * 2), fill=color, width=4)

    def arrow(self, x1: float, y: float, x2: float, color: str = BLUE):
        self.line(x1, y, x2, y, color)
        self.line(x2 - 6, y - 4, x2, y, color)
        self.line(x2 - 6, y + 4, x2, y, color)

    def save(self, root: Path, name: str):
        svg = root / "assets" / "svg" / f"{name}.svg"
        png = root / "assets" / "diagrams" / f"{name}_svg.png"
        svg.parent.mkdir(parents=True, exist_ok=True)
        png.parent.mkdir(parents=True, exist_ok=True)
        ET.indent(self.root)
        ET.ElementTree(self.root).write(svg, encoding="utf-8", xml_declaration=True)
        self.preview.save(png)


def pixel_canvas() -> np.ndarray:
    canvas = np.zeros((5, 7), dtype=np.uint8)
    canvas[0, 0], canvas[0, 6], canvas[4, 0], canvas[2, 3] = 255, 200, 150, 100
    return canvas


def draw_pixels(name: str) -> Canvas:
    c = Canvas("画素とスライス / pixels and slices", "computed synthetic; Day01_02 canvas")
    array = pixel_canvas()
    for row in range(5):
        c.text(28, 147 + row * 60, f"y={row}", 17)
        for col in range(7):
            x, y = 84 + col * 60, 110 + row * 60
            selected = 1 <= row < 4 and 2 <= col < 5
            c.rect(x, y, 58, 58, "#e8f0ff" if selected else "#f6f8fa", BLUE if selected else "#d0d7de")
            c.text(x + 9, y + 35, str(array[row, col]), 18)
            if row == 0:
                c.text(x + 8, 96, f"x={col}", 17)
    c.text(540, 140, "canvas.shape = (5, 7)", 20, BLUE)
    c.text(540, 180, "canvas[2, 3] = 100", 20)
    c.text(540, 225, "canvas[1:4, 2:5]", 20, AMBER)
    selected = array[1:4, 2:5]
    c.text(540, 264, f"shape = {selected.shape}", 20)
    for row, values in enumerate(selected):
        c.text(540, 305 + row * 33, str(values.tolist()), 20)
    c.text(84, 466, "青枠: y=1,2,3 / x=2,3,4（終点は含めない）", 21)
    c.text(84, 508, "Blue selection: stop indices 4 and 5 are excluded.", 20)
    return c


def draw_tasks() -> Canvas:
    c = Canvas("同じ欠陥の4タスク / four tasks, one defect", "computed synthetic GT; schematic outputs")
    mask = spot_mask(200)
    x1, y1, x2, y2 = mask_box(mask)
    ys, xs = np.nonzero(mask)
    for i, title in enumerate(("分類 / classification", "検出 / detection", "画素マスク / segmentation", "異常マップ / anomaly map")):
        x, y = 24 + (i % 2) * 438, 76 + (i // 2) * 248
        c.text(x, y, title, 22, VIOLET)
        c.rect(x, y + 15, 200, 200, "#d2d0c9")
        for py, px in zip(ys, xs):
            color = RED if i == 2 else "#28282c"
            c.rect(x + int(px), y + 15 + int(py), 1, 1, color, color)
        if i == 1:
            c.rect(x + x1, y + 15 + y1, x2 - x1, y2 - y1, "none", RED)
        if i == 3:
            # A schematic distance map, centred on the very same mask, not model inference.
            cx, cy = xs.mean(), ys.mean()
            for dy in range(-14, 15, 2):
                for dx in range(-14, 15, 2):
                    level = np.exp(-(dx ** 2 + dy ** 2) / (2 * 9 ** 2))
                    color = f"#{int(90 + 165 * level):02x}305e"
                    c.rect(x + cx + dx, y + 15 + cy + dy, 2, 2, color, color)
        labels = [
            ["NG / 異常あり", "画像ラベル / label"],
            [f"GT: {x1},{y1}", f"to {x2},{y2}", "右下は含めない"],
            [f"GT: {int(mask.sum())} pixels", "同じ描画マスク"],
            ["模式値 / schematic", "not model output"],
        ][i]
        for row, line in enumerate(labels):
            c.text(x + 212, y + 66 + row * 35, line, 18)
    return c


def draw_calibration() -> Canvas:
    c = Canvas("同じ平面の校正 / same-plane calibration", "computed synthetic; calibrated_defects()")
    _, info = calibrated_defects()
    c.rect(50, 105, 320, 240, "#d2d2d2")
    for target in info["targets"]:
        x1, y1, x2, y2 = target["xyxy"]
        c.rect(50 + x1, 105 + y1, x2 - x1, y2 - y1, "#282828", "#282828")
    (x1, y1), (x2, y2) = info["reference_points"]
    c.line(50 + x1, 105 + y1, 50 + x2, 105 + y2, BLUE)
    for x in (x1, x2):
        c.line(50 + x, 105 + y1 - 7, 50 + x, 105 + y1 + 7, BLUE)
    (cx, cy1), (_, cy2) = info["check_points"]
    c.line(50 + cx, 105 + cy1, 50 + cx, 105 + cy2, GREEN)
    c.text(50, 82, "320 × 240 px（理想的な同一平面）", 20, BLUE)
    c.text(50, 382, f"青 / blue: {x2-x1} px = {info['reference_mm']:g} mm", 20, BLUE)
    c.text(50, 419, f"緑 / green: {cy2-cy1} px = {info['check_mm']:g} mm", 20, GREEN)
    scale = info["px_per_mm"]
    lines = [
        f"px/mm = {x2-x1} / {info['reference_mm']:g} = {scale:g}",
        f"mm/px = 1 / {scale:g} = {1/scale:.6f}",
        f"Check: {cy2-cy1} / {scale:g} = {info['check_mm']:g} mm",
        "length_mm = length_px / scale",
        "area_mm2 = area_px2 / scale²",
        "Contour area != foreground count",
    ]
    for row, line in enumerate(lines):
        c.text(422, 134 + row * 43, line, 20, GREEN if row == 2 else INK)
    c.text(50, 476, "同じ平面・正方画素。傾き、歪み、基準の不確かさを確認。", 21, AMBER)
    c.text(50, 515, "Same plane, square pixels; check tilt, distortion and uncertainty.", 20)
    return c


def draw_bbox() -> Canvas:
    c = Canvas("1つの四角、3つの形式 / one box, three formats", "computed schematic; BBOX_XYXY")
    W, H = BBOX_IMAGE_SIZE
    x1, y1, x2, y2 = BBOX_XYXY
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    w, h = x2 - x1, y2 - y1
    c.rect(60, 110, W, H, "#e8f0ff", BLUE)
    c.rect(60 + x1, 110 + y1, w, h, "none", RED)
    c.line(60 + cx - 6, 110 + cy, 60 + cx + 6, 110 + cy, RED)
    c.line(60 + cx, 110 + cy - 6, 60 + cx, 110 + cy + 6, RED)
    c.text(60, 87, f"W={W} px; H={H} px", 22, BLUE)
    c.text(60, 391, f"左上 / top-left: ({x1},{y1})", 21, RED)
    c.text(60, 430, f"右下 / bottom-right: ({x2},{y2})", 21, RED)
    c.text(370, 123, f"xyxy = {BBOX_XYXY}", 20)
    c.text(370, 166, f"OpenCV xywh = ({x1},{y1},{w},{h})", 20)
    c.text(370, 209, f"Ultralytics xywh = ({cx:g},{cy:g},{w},{h})", 20)
    c.text(370, 256, "xc=(x1+x2)/2/W; yc=(y1+y2)/2/H", 20)
    c.text(370, 299, "w=(x2-x1)/W; h=(y2-y1)/H", 20)
    c.text(370, 348, f"YOLO: 0 {cx/W:.3f} {cy/H:.3f} {w/W:.3f} {h/H:.3f}", 22, VIOLET)
    c.text(370, 391, "class_id=0 is an integer", 20)
    c.text(370, 434, "Only the four coordinates are normalised.", 20)
    c.text(60, 502, "右下の端は含めない / right and bottom edges are exclusive", 21, AMBER)
    return c


def draw_batches() -> Canvas:
    c = Canvas("epoch・batch・更新 / epoch, batch, update", "schematic; 64 images, batch=8, nominal nbs=64")
    for row in range(8):
        for col in range(8):
            x, y = 50 + col * 32, 110 + row * 32
            c.rect(x, y, 28, 28, "#e8f0ff", BLUE)
            c.text(x + 3, y + 20, str(row * 8 + col + 1), 13)
    c.text(50, 82, "1行 = 8枚 / one row = one batch", 20, BLUE)
    c.text(50, 402, "64枚 / 8枚 = 8 batches / epoch", 20)
    lines = [
        "8 images -> forward -> loss",
        "backward -> gradients",
        "Accumulate gradients (~8 batches)",
        "optimizer.step() -> update weights",
        "Clear gradients; repeat",
    ]
    for row, line in enumerate(lines):
        c.rect(390, 85 + row * 67, 462, 49, "#f6f8fa", VIOLET)
        c.text(405, 116 + row * 67, line, 20)
    c.text(50, 469, "この研修の名目設定。warmup 中は蓄積数が変わり得ます。", 21, AMBER)
    c.text(50, 511, "Course nominal settings; warmup can alter accumulation. Read args.yaml.", 20)
    return c


def matching_values() -> tuple[list[tuple[int, ...]], list[tuple[int, ...]], np.ndarray]:
    truth = [(20, 20, 80, 80), (110, 20, 160, 70)]
    predicted = [(20, 20, 80, 80), (22, 20, 82, 80)]
    matrix = np.zeros((2, 2))
    for i, a in enumerate(truth):
        for j, b in enumerate(predicted):
            intersection = max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))
            area_a, area_b = (a[2]-a[0]) * (a[3]-a[1]), (b[2]-b[0]) * (b[3]-b[1])
            matrix[i, j] = intersection / (area_a + area_b - intersection)
    return truth, predicted, matrix


def draw_matching() -> Canvas:
    c = Canvas("四角を1対1で対応させる / one-to-one matching", "computed schematic; same class; IoU cutoff=0.50")
    truth, predicted, matrix = matching_values()
    c.rect(50, 110, 300, 180, "#f6f8fa")
    for boxes, color in ((truth, BLUE), (predicted, VIOLET)):
        for x1, y1, x2, y2 in boxes:
            c.rect(50 + x1 * 1.5, 110 + y1 * 1.5, (x2-x1) * 1.5, (y2-y1) * 1.5, "none", color)
    c.text(50, 80, "青: GT / 紫: predictions", 20)
    c.text(50, 330, "GT1 と P1 は一致。P2 は重複。", 20)
    c.text(50, 369, "GT2 に対応する予測はありません。", 20, RED)
    c.text(405, 110, "IoU matrix: columns P1, P2", 22, VIOLET)
    for row in range(2):
        c.text(405, 160 + row * 45, f"GT{row+1}:  {matrix[row,0]:.4f}   {matrix[row,1]:.4f}", 22)
    c.text(405, 268, "Same class; IoU >= 0.50", 22)
    c.text(405, 312, "Match highest IoU first, one to one.", 20)
    used_truth, used_predictions = set(), set()
    for i, j in sorted(np.ndindex(matrix.shape), key=lambda ij: matrix[ij], reverse=True):
        if matrix[i, j] >= .50 and i not in used_truth and j not in used_predictions:
            used_truth.add(i)
            used_predictions.add(j)
    tp, fp, fn = len(used_truth), len(predicted) - len(used_predictions), len(truth) - len(used_truth)
    c.text(405, 358, "Both predictions pass conf >= 0.50.", 20)
    c.text(405, 405, f"Object counts: TP={tp}, FP={fp}, FN={fn}", 20)
    c.text(50, 467, "画像単位: 異常画像1枚をNG → TP=1（四角の件数とは別）", 21, GREEN)
    c.text(50, 511, "Image-level: one abnormal image called NG -> TP=1, not box counts.", 20)
    return c


def build_figure(name: str) -> Canvas:
    if name in ("teach_pixel_inspector", "teach_slice_walkthrough"):
        return draw_pixels(name)
    if name == "teach_cv_tasks_outputs":
        return draw_tasks()
    special = {
        "teach_calibration_same_plane": draw_calibration,
        "teach_bbox_one_example": draw_bbox,
        "teach_epoch_batch_step": draw_batches,
        "teach_detection_matching": draw_matching,
    }
    if name in special:
        return special[name]()
    c = Canvas(name.removeprefix("teach_").replace("_", " "), "schematic; source-checked course constants")
    if name == "teach_code_cell_lifecycle":
        panels = [
            ("① 初期化 / initialise", ["defect_count = 3", "Shift+Enter -> kernel: 3"]),
            ("② 加算セル / increment cell", ["defect_count = defect_count + 1", "kernel: 3 -> 4"]),
            ("③ 出力 / stdout", ["print(defect_count)", "4"]),
            ("④ 加算だけ再実行 / rerun", ["kernel: 4 -> 5", "print -> 5"]),
            ("⑤ 再起動 / restart", ["Variables are cleared.", "Run initialise before increment."]),
            ("⑥ エラー / error", ["Undefined name -> NameError", "Run the missing earlier cell."]),
        ]
    elif name == "teach_mass_units_chain":
        width, length, thickness, density = MASS_INPUTS
        panels = [
            ("① 長さ / lengths", [f"{width:g} mm x {length:g} mm", f"thickness = {thickness:g} mm"]),
            ("② 体積 / volume", ["width x length x thickness", "mm x mm x mm = mm³"]),
            ("③ 換算 / convert volume", ["volume_mm3 / 1000", "= volume_cm3 (cm³)"]),
            ("④ 密度 / density", [f"{density:g} g/cm³", "volume_cm3 x density -> g"]),
            ("⑤ 重さ / mass", ["mass_g / 1000 -> kg", "Calculate the exercise yourself."]),
            ("⑥ 区別 / distinguish", ["Area uses two lengths (mm²).", "Volume uses three (mm³)."]),
        ]
    elif name == "teach_if_live_trace":
        delta = abs(100.3 - 100)
        panels = [
            ("① 入力 / input", ["measured=100.3 mm", "nominal=100; tolerance=0.5 mm"]),
            ("② 差 / difference", [f"abs(100.3 - 100) = {delta:.1f} mm", "Formatting does not change delta."]),
            ("③ 条件 / condition", ["abs(delta) <= 0.5", "True -> if branch"]),
            ("④ 出力 / output", ["print -> 判定 / result : OK", "100.5001 -> NG"]),
            ("⑤ 境界を含む / inclusive", ["99.5 -> OK; 100.5 -> OK", "No rounding before comparison."]),
            ("⑥ 実数表現 / float caveat", ["2.1 - 2.0 > 0.1 in float.", "Resolution needs a separate policy."]),
        ]
    elif name == "teach_opencv_pixel_pipeline":
        import cv2
        values = np.array([[40, 120, 121], [210, 40, 210]], dtype=np.uint8)
        _, mask = cv2.threshold(values, 120, 255, cv2.THRESH_BINARY_INV)
        count = cv2.connectedComponents(mask)[0] - 1
        panels = [
            ("① 入力 / source", ["cv2.imread -> BGR channels", "BGR -> cv2.cvtColor -> gray"]),
            ("② 画素値 / gray toy array", [str(row.tolist()) for row in values]),
            ("③ 反転しきい値 / inverse", ["gray <= 120 -> 255 (white)", "gray > 120 -> 0 (black)"]),
            ("④ マスク / binary mask", [str(row.tolist()) for row in mask]),
            ("⑤ 輪郭 / contours", [f"Foreground: {np.count_nonzero(mask)} pixels", f"Connected regions: {count}"]),
            ("⑥ 面積条件 / area filter", ["cv2.contourArea -> px²", "Not brightness, not pixel count."]),
        ]
    elif name == "teach_yolo_result_object":
        panels = [
            ("① 入力 / input", ["Local image + saved YOLO weights", "model.predict(image)"]),
            ("② 戻り値 / return", ["list of Results", "One Results per image"]),
            ("③ 四角 / Boxes", ["result.boxes.cls -> class IDs", "result.boxes.conf -> scores"]),
            ("④ 座標 / coordinates", ["result.boxes.xyxy -> original px", "N boxes -> N rows, 4 coordinates"]),
            ("⑤ 表示と保存 / outputs", ["result.plot() -> BGR image", "CSV: class, score, x1,y1,x2,y2"]),
            ("⑥ 解釈 / interpretation", ["Confidence is not truth probability.", "No boxes -> empty table (0 rows)"]),
        ]
    elif name == "teach_patchcore_stages":
        panels = [
            ("① 正常画像 / normal fit", ["Frozen pretrained resnet18", "No backbone-weight updates"]),
            ("② 特徴 / embeddings", ["layer2 + layer3 patch features", "Coreset -> normal memory bank"]),
            ("③ 試験入力 / inference", ["Same preprocessing and backbone", "New patch -> feature vector"]),
            ("④ 距離 / nearest neighbour", ["Compare to stored normal features.", "Distance -> map + image score"]),
            ("⑤ 較正 / calibration only", ["Fit separate score/map statistics.", "Freeze memory and postprocessor."]),
            ("⑥ 注意 / interpretation", ["2D feature sketches are not x/y.", "Image score != displayed map max"]),
        ]
    elif name == "teach_frozen_threshold_pipeline":
        panels = [
            ("① 撮影群を分ける / group split", ["Fit / calibration / untouched test", "No acquisition group crosses splits."]),
            ("② 学習 / fit", ["YOLO labels / PatchCore normals", "Freeze weights and normal memory."]),
            ("③ 較正のみ / calibrate only", ["Choose thresholds on calibration.", "Fit normalisation there only."]),
            ("④ 全設定を固定 / freeze all", ["Weights + preprocessing + memory", "Postprocessor + decision thresholds"]),
            ("⑤ 試験1回 / test once", ["No test-to-tuning feedback.", "Changed settings need new holdout."]),
            ("⑥ 報告 / report", ["comparison_test_results.json / CSV", "Tiny synthetic set, not factory accuracy"]),
        ]
    else:
        panels = [
            ("① フレーム分割 / frame split", ["Session A: A1 train / A2 test", "Related frames cross the boundary."]),
            ("② 撮影群分割 / group split", ["Session A -> train only", "Session B -> test only"]),
            ("③ バイト比較 / byte hash", ["SHA-256 compares file bytes.", "Re-encoding changes the digest."]),
            ("④ 近似画像 / near duplicates", ["±1 intensity-level noise", "No spatial shift was performed."]),
            ("⑤ 限界 / limits", ["Different hashes != no leakage.", "Perceptual checks are not infallible."]),
            ("⑥ 記録 / record", ["Keep lot/session IDs before splitting.", "Audit groups and capture conditions."]),
        ]
    for i, (heading, lines) in enumerate(panels):
        c.panel(i, heading, lines, (BLUE, AMBER, VIOLET, GREEN, RED, AMBER)[i])
    for row in range(3):
        c.arrow(438, 132 + row * 157, 459, AMBER)
    return c


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    rows = []
    for name, (notebook, anchor, jp, en, question_jp, question_en) in FIGURES.items():
        build_figure(name).save(args.root, name)
        rows.append(f"| `{name}.svg` | `{notebook}`: `{anchor}` | "
                    f"`generate_svg_figures.build_figure` / `teaching_data.py` | computed synthetic / schematic | "
                    f"[SVG](../assets/svg/{name}.svg) / [PNG](../assets/diagrams/{name}_svg.png) | {question_jp} {question_en} |")
    manifest = args.root / "docs" / "visual_figure_manifest.md"
    manifest.write_text(
        "# 図の出典と学習の問い / Visual figure manifest\n\n"
        "SVG は編集可能な文字・図形です。PNG は同じ描画操作から作る PDF 用の代替です。\n"
        "SVG uses editable text/shapes; PNG is a PDF fallback from the same drawing operations.\n\n"
        "写真・保存済みモデル出力は再生成していません。streak_0005 の元記録はないため新しい数値図は省略しました。\n"
        "Photos and saved model outputs were not regenerated. The new streak_0005 numeric figure is omitted: source records unavailable.\n\n"
        "| Asset | Notebook section | Source code/data | Provenance | Preview | Learning question |\n"
        "|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n\n"
        "Source-checked values: box (96,72,168,132), image 240×240 -> YOLO 0 0.550 0.425 0.300 0.250; "
        "spot radius 9 px at (84,110), bounding edges from mask; "
        "canvas[1:4,2:5] has shape (3,3); 120 px / 100 mm = 1.2 px/mm; independent 60 px = 50 mm. "
        "Calibrated target contour areas: 475 / 925 px² -> 329.861111 / 642.361111 mm²; "
        "foreground pixel count is 1508, not the sum of geometric contour areas. "
        "Mass inputs match the unsolved exercise; its calculated answer is not inserted into exercise code.\n",
        encoding="utf-8",
    )
    print(f"Generated {len(FIGURES)} SVGs, PNG fallbacks and {manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
