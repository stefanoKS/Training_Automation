"""Generate the 36 bilingual SVG teaching diagrams for Days 7-9.

Run from any directory:
    python AI_Vision_Training\\day07_09_support\\scripts\\generate_day07_09_diagrams.py

The output is deterministic: the same source always produces byte-identical SVG files.
"""

from __future__ import annotations

import math
from pathlib import Path

from svgkit import (
    ACCENT,
    BAD,
    CARD,
    EN_BG,
    GOOD,
    INK,
    JP_BG,
    MUTED,
    PALE,
    SAFE,
    WARN,
    Svg,
    new_diagram,
    text_width,
)

ROOT = Path(__file__).resolve().parents[2]
DIAGRAMS = ROOT / "assets" / "diagrams"


def chain(svg: Svg, items, y, h=120, x0=80, x1=1360, gap=28) -> None:
    count = len(items)
    width = (x1 - x0 - gap * (count - 1)) / count
    for index, item in enumerate(items):
        x = x0 + index * (width + gap)
        svg.card(x, y, width, h, item[0], item[1], accent=item[2] if len(item) > 2 else ACCENT)
        if index < count - 1:
            svg.line(x + width + 4, y + h / 2, x + width + gap - 2, y + h / 2)


def ladder_contact(svg: Svg, x: float, y: float, nc: bool, address: str, addr_size=16, label_dy=42) -> None:
    svg.line(x - 24, y, x - 10, y, marker=False)
    svg.line(x - 10, y - 18, x - 10, y + 18, marker=False)
    svg.line(x + 10, y - 18, x + 10, y + 18, marker=False)
    svg.line(x + 10, y, x + 24, y, marker=False)
    if nc:
        svg.line(x - 14, y + 16, x + 14, y - 16, marker=False)
    svg.text(x, y + label_dy, address, addr_size, 700, ACCENT, "middle")


def ladder_coil(svg: Svg, x: float, y: float, address: str) -> None:
    svg.parts.append(
        f'<path d="M{x - 18} {y - 18} Q{x - 34} {y} {x - 18} {y + 18}" fill="none" stroke="{ACCENT}" stroke-width="2.4"/>'
        f'<path d="M{x + 18} {y - 18} Q{x + 2} {y} {x + 18} {y + 18}" fill="none" stroke="{ACCENT}" stroke-width="2.4"/>'
    )
    svg.line(x - 46, y, x - 32, y, marker=False)
    svg.line(x + 18, y, x + 62, y, marker=False)
    svg.text(x, y + 44, address, 16, 700, ACCENT, "middle")
    svg._track(x + 62, y + 44)


def truth_table(svg: Svg, x, y, headers, rows, col_w=96, row_h=38, title_ja="", title_en="") -> None:
    if title_ja:
        svg.text(x, y - 20, title_ja, 18, 700, INK)
        svg.text(x, y + 2, title_en, 15, 400, MUTED)
        y += 26
    for row_index, row in enumerate([headers] + rows):
        top = y + row_index * row_h
        for col_index, value in enumerate(row):
            svg.rect(x + col_index * col_w, top, col_w, row_h, fill=JP_BG if row_index == 0 else CARD,
                     stroke=ACCENT, sw=1, rx=3)
            svg.text(x + col_index * col_w + col_w / 2, top + row_h * 0.68, str(value),
                     17, 700 if row_index == 0 else 400, INK, "middle")
    svg._track(x + col_w * len(headers), y + row_h * (len(rows) + 1))


def waveform(svg: Svg, x, y, w, high, low, pattern, color=ACCENT, sw=2.6) -> None:
    """pattern: list of (start_fraction, level 0/1)."""
    points = [(x, low if pattern[0][1] == 0 else high)]
    for start, level in pattern:
        level_y = high if level else low
        points.append((x + start * w, points[-1][1]))
        points.append((x + start * w, level_y))
    points.append((x + w, points[-1][1]))
    path = " ".join(f"{px:.1f},{py:.1f}" for px, py in points)
    svg.parts.append(
        f'<polyline points="{path}" fill="none" stroke="{color}" stroke-width="{sw}"/>'
    )
    svg._track(x + w, max(high, low))


# --------------------------------------------------------------------------- Day 7
def d07_01(out: Path) -> None:
    svg = new_diagram("D07-01", "連続シート検査機の全体構成", "Full physical inspection machine overview",
                      "DAY 07 / MECHANICAL STRUCTURE", 940)
    svg.rect(80, 300, 1280, 26, fill="#D9C9A8", stroke="#B9A57C", sw=1, rx=2)
    svg.text(80, 356, "材料の流れ → / material flow", 18, 700, "#7A6533")
    stations = [
        (96, "供給ロール", "Unwinder roll", ACCENT),
        (352, "ガイドローラ", "Guide rollers", ACCENT),
        (608, "検査ステーション", "Inspection station", GOOD),
        (864, "駆動ローラ", "Driven roller", WARN),
        (1120, "巻取り", "Winder", ACCENT),
    ]
    for x, ja, en, color in stations:
        svg.card(x, 196, 220, 132, ja, en, accent=color)
        svg.line(x + 100, 334, x + 100, 298, color)
    svg.line(1120, 300, 1320, 300, marker=False)
    svg.card(608, 372, 240, 120, "カメラと照明", "Camera and illumination", accent=GOOD)
    svg.line(728, 300, 728, 368, GOOD)
    svg.card(352, 372, 220, 120, "材料の位置決め", "Material positioning", accent=ACCENT)
    svg.line(462, 300, 462, 368, ACCENT)
    svg.card(864, 372, 240, 120, "搬送速度の管理", "Transport speed control", accent=WARN)
    svg.line(984, 300, 984, 368, WARN)
    svg.text(80, 540, "制御・計算・表示の構成要素 / control, computing and display elements", 20, 700, INK)
    width = (1280 - 4 * 24) / 5
    for index, (ja, en) in enumerate([("PLC", "配線された制御 / wired control"),
                                      ("産業用PC", "画像とAI / imaging and AI"),
                                      ("HMI", "操作と表示 / operation and display"),
                                      ("安全系", "独立した保護 / independent protection"),
                                      ("記録", "結果の保存 / result records")]):
        x = 80 + index * (width + 24)
        svg.card(x, 566, width, 112, ja[0] if isinstance(ja, tuple) else ja,
                 en.split(" / ")[0] if " / " in en else en, accent=SAFE if index == 3 else ACCENT)
    svg.text(80, 724, "機械・センサ・制御・AI・安全は別々の役割を持ち、一つの検査結果を作ります。", 19, 700, INK)
    svg.text(80, 752, "Mechanics, sensors, control, AI and safety keep separate roles and together produce one inspection result.", 17, 400, MUTED)
    svg.footer("材料は連続して流れ、検査結果は位置と結び付けて記録します。 / The web flows continuously; results are recorded with position.")
    svg.save(out / "D07-01.svg")


def d07_02(out: Path) -> None:
    svg = new_diagram("D07-02", "フレーム・軸・ベアリング・ローラ", "Frame, rollers, shafts and bearings",
                      "DAY 07 / MECHANICAL COMPONENTS", 820)
    parts = [
        ("フレーム", "Frame", "すべての部品を支える構造 / carries the structure"),
        ("シャフト", "Shaft", "回転を伝える軸 / transmits rotation"),
        ("ベアリング", "Bearing", "摩擦を減らして支える / supports with low friction"),
        ("ローラ", "Roller", "シートに接触する回転体 / rotating contact surface"),
    ]
    width = (1280 - 3 * 22) / 4
    for index, (ja, en, detail) in enumerate(parts):
        svg.card(80 + index * (width + 22), 186, width, 168, ja, en, sub=detail)
    svg.text(80, 404, "組立の関係 / how the parts fit together", 20, 700, INK)
    svg.rect(96, 430, 1248, 240, fill=CARD, stroke=ACCENT, sw=2)
    svg.rect(120, 470, 120, 170, fill=JP_BG, stroke=ACCENT, sw=2)
    svg.text(180, 500, "フレーム", 18, 700, INK, "middle")
    svg.text(180, 524, "frame", 15, 400, MUTED, "middle")
    svg.rect(280, 548, 720, 26, fill="#B9C8D6", stroke="#8497A8", sw=2)
    svg.text(640, 542, "シャフト / shaft", 17, 700, "#455A6C", "middle")
    for cx in (360, 920):
        svg.circle(cx, 561, 34, fill="#EDF2F8", stroke=SAFE, sw=3)
        svg.circle(cx, 561, 10, fill=CARD, stroke=SAFE, sw=2)
    svg.text(360, 628, "ベアリング / bearing", 16, 700, SAFE, "middle")
    svg.text(920, 628, "ベアリング / bearing", 16, 700, SAFE, "middle")
    svg.circle(640, 561, 62, fill="#F2E7D2", stroke=WARN, sw=3)
    svg.circle(640, 561, 14, fill=CARD, stroke=WARN, sw=2)
    svg.text(640, 650, "ローラ / roller", 18, 700, WARN, "middle")
    svg.line(1030, 561, 1150, 561, marker=True)
    svg.text(1160, 548, "回転方向", 17, 700, ACCENT)
    svg.text(1160, 570, "rotation", 15, 400, MUTED)
    svg.text(80, 700, "ベアリングの摩耗は振動と位置ずれを生み、検査画像のぼけや位置ずれにつながります。", 18, 700, INK)
    svg.text(80, 726, "Worn bearings add vibration and misalignment, which blur images and shift their position.", 16, 400, MUTED)
    svg.footer("軸・ベアリング・ローラは一組で剛性と回転精度を決めます。 / Shaft, bearing and roller together set stiffness and rotation accuracy.")
    svg.save(out / "D07-02.svg")


def d07_03(out: Path) -> None:
    svg = new_diagram("D07-03", "回転運動と直線運動", "Linear versus rotational motion",
                      "DAY 07 / MOTION", 760)
    svg.rect(80, 186, 610, 300, fill=CARD, stroke=ACCENT, sw=2)
    svg.text(110, 224, "回転運動 / rotational motion", 21, 700, ACCENT)
    svg.circle(250, 340, 86, fill=JP_BG, stroke=ACCENT, sw=3)
    svg.circle(250, 340, 8, fill=ACCENT, stroke=ACCENT, sw=1)
    svg.parts.append(
        f'<path d="M250 240 A100 100 0 0 1 344 330" fill="none" stroke="{WARN}" stroke-width="4" marker-end="url(#arrow)"/>'
    )
    svg.text(250, 462, "角度 θ・回転数 rpm / angle and rpm", 17, 400, MUTED, "middle")
    svg.line(268, 340, 330, 340, marker=False)
    svg.text(334, 334, "r", 20, 700, INK)
    svg.text(360, 250, "同じ点が円を描く", 17, 700, INK)
    svg.text(360, 274, "a point traces a circle", 15, 400, MUTED)
    svg.text(360, 306, "単位：度・回転/分", 17, 700, INK)
    svg.text(360, 330, "units: degrees, rpm", 15, 400, MUTED)
    svg.rect(710, 186, 650, 300, fill=CARD, stroke=GOOD, sw=2)
    svg.text(740, 224, "直線運動 / linear motion", 21, 700, GOOD)
    svg.rect(780, 330, 500, 20, fill="#B9C8D6", stroke="#8497A8", sw=1, rx=2)
    svg.rect(830, 300, 90, 80, fill=JP_BG, stroke=GOOD, sw=3)
    svg.line(950, 340, 1240, 340, stroke=GOOD, sw=4)
    svg.text(1090, 318, "変位 d / displacement", 17, 700, GOOD, "middle")
    svg.text(800, 462, "速度 = 変位 ÷ 時間 / speed = displacement ÷ time", 17, 400, MUTED)
    svg.text(740, 262, "まっすぐ動く", 17, 700, INK)
    svg.text(740, 286, "moves in a straight line", 15, 400, MUTED)
    svg.text(80, 528, "比較 / comparison", 20, 700, INK)
    truth_table(svg, 80, 556, ["量 / quantity", "回転 / rotation", "直線 / linear"], [
        ["位置 / position", "角度 θ / angle", "距離 d / distance"],
        ["速さ / rate", "rpm・rad/s", "mm/s・m/min"],
        ["加速度 / acceleration", "角加速度", "m/s² / linear"],
    ], col_w=400, row_h=42)
    svg.footer("回転はローラで直線のシート移動に変換されます。 / Rotation becomes straight sheet travel through rollers.")
    svg.save(out / "D07-03.svg")


def d07_04(out: Path) -> None:
    svg = new_diagram("D07-04", "ローラ径・回転数・材料速度", "Roller speed, diameter and material movement",
                      "DAY 07 / ROLLER MECHANICS", 800)
    svg.circle(330, 380, 150, fill=JP_BG, stroke=ACCENT, sw=4)
    svg.circle(330, 380, 12, fill=ACCENT, stroke=ACCENT, sw=1)
    svg.line(330, 380, 436, 274, marker=False)
    svg.text(400, 316, "半径 r / radius", 18, 700, INK)
    svg.line(150, 560, 510, 560, marker=False)
    svg.line(150, 548, 150, 572, marker=False)
    svg.line(510, 548, 510, 572, marker=False)
    svg.text(330, 592, "直径 D = 2r / diameter", 18, 700, ACCENT, "middle")
    svg.parts.append(
        f'<path d="M180 290 A160 160 0 0 1 300 234" fill="none" stroke="{WARN}" stroke-width="4" marker-end="url(#arrow)"/>'
    )
    svg.text(180, 220, "回転 N rpm / rotation", 18, 700, WARN)
    svg.rect(600, 200, 760, 190, fill=CARD, stroke=ACCENT, sw=2)
    svg.text(626, 238, "式 / formula", 20, 700, ACCENT)
    svg.text(626, 280, "円周 C = π × D", 22, 700, INK)
    svg.text(626, 314, "表面速度 v = C × N", 22, 700, INK)
    svg.text(626, 348, "v = π × D × N   （滑りなし / no slip）", 19, 400, MUTED)
    svg.rect(600, 410, 760, 220, fill=EN_BG, stroke=GOOD, sw=2)
    svg.text(626, 448, "仮定例 / hypothetical example", 20, 700, GOOD)
    svg.text(626, 486, "D = 100 mm、N = 100 rpm", 20, 700, INK)
    svg.text(626, 520, "C = π × 100 ≈ 314.159 mm", 19, 400, INK)
    svg.text(626, 554, "v ≈ 314.159 mm/回転 × 100 回転/分 = 31,415.9 mm/min", 18, 400, INK)
    svg.text(626, 588, "= 約 31.416 m/min", 20, 700, GOOD)
    svg.text(626, 614, "※実際は滑り・張力・摩耗で異なります / real speed differs with slip and tension", 15, 400, MUTED)
    svg.text(80, 666, "駆動ローラは動力を伝え、アイドラローラは案内します。 / A driven roller transmits power; an idler only guides.")
    svg.text(80, 692, "ローラ表面速度とシート速度が常に等しいとは限りません。 / Roller surface speed is not always sheet speed.")
    svg.footer("直径・回転数・滑りの3点を分けて考えます。 / Keep diameter, rotation and slip as three separate ideas.")
    svg.save(out / "D07-04.svg")


def d07_05(out: Path) -> None:
    svg = new_diagram("D07-05", "張力・しわ・蛇行と位置合わせ", "Web tension, wrinkles and alignment",
                      "DAY 07 / WEB HANDLING", 800)
    panels = [
        (80, "適正な張力", "Correct tension", GOOD),
        (525, "張力不足としわ", "Low tension and wrinkles", WARN),
        (970, "蛇行と位置ずれ", "Lateral drift and misalignment", BAD),
    ]
    for x, ja, en, color in panels:
        svg.rect(x, 186, 390, 300, fill=CARD, stroke=color, sw=2)
        svg.text(x + 20, 222, ja, 20, 700, color)
        svg.text(x + 20, 246, en, 16, 400, MUTED)
    svg.rect(100, 322, 350, 16, fill="#D9C9A8", stroke="#B9A57C", sw=1, rx=2)
    svg.line(110, 306, 440, 306, marker=True)
    svg.text(275, 290, "張力 T / tension", 17, 700, GOOD, "middle")
    svg.text(100, 372, "しわなし・平行に流れる", 17, 700, INK)
    svg.text(100, 396, "no wrinkles, parallel travel", 15, 400, MUTED)
    svg.text(100, 430, "検査画像が安定する", 17, 700, INK)
    svg.text(100, 454, "inspection images stay stable", 15, 400, MUTED)
    svg.parts.append(
        '<path d="M545 330 q 40 -26 80 0 q 40 26 80 0 q 40 -26 80 0 q 40 26 80 0" fill="none" '
        f'stroke="#D9C9A8" stroke-width="16"/>'
    )
    svg.text(545, 372, "しわが明暗を作る", 17, 700, INK)
    svg.text(545, 396, "wrinkles create light and shadow", 15, 400, MUTED)
    svg.text(545, 430, "正常品を異常に見せる", 17, 700, BAD)
    svg.text(545, 454, "makes good material look defective", 15, 400, MUTED)
    svg.rect(990, 306, 350, 16, fill="#D9C9A8", stroke="#B9A57C", sw=1, rx=2)
    svg.parts.append(
        f'<path d="M990 314 L1340 314" stroke="{BAD}" stroke-width="2" stroke-dasharray="8 6"/>'
    )
    svg.parts.append('<path d="M990 250 L990 306" fill="none" stroke="#A32B2B" stroke-width="3" marker-end="url(#arrow-red)"/>')
    svg.text(1000, 244, "横方向のずれ / lateral offset", 16, 700, BAD)
    svg.text(990, 372, "エッジ位置が変化する", 17, 700, INK)
    svg.text(990, 396, "edge position changes", 15, 400, MUTED)
    svg.text(990, 430, "画角から外れる危険", 17, 700, BAD)
    svg.text(990, 454, "risk of leaving the field of view", 15, 400, MUTED)
    svg.text(80, 530, "張力・しわ・蛇行は「見え方」を変えます。照明と機械の安定がAIの前提です。", 20, 700, INK)
    svg.text(80, 558, "Tension, wrinkles and drift change appearance. Stable mechanics and lighting are prerequisites for AI.", 16, 400, MUTED)
    chain(svg, [("張力制御", "Tension control"), ("ガイド", "Edge guide"), ("振動の抑制", "Vibration control"),
                ("照明の固定", "Fixed illumination")], 606, 104)
    svg.footer("機械の安定が保証できないと、AIの判定根拠も安定しません。 / Without mechanical stability, AI decisions have no stable basis.")
    svg.save(out / "D07-05.svg")


def d07_06(out: Path) -> None:
    svg = new_diagram("D07-06", "機械式の動力伝達", "Mechanical power transmission",
                      "DAY 07 / POWER TRANSMISSION", 760)
    items = [
        ("モータ", "Motor"), ("カップリング", "Coupling"), ("軸", "Shaft"),
        ("プーリ", "Pulley"), ("ベルト", "Belt"), ("ローラ", "Roller"),
    ]
    chain(svg, items, 190, 116)
    svg.text(80, 352, "動力の流れ / power flow", 19, 700, ACCENT)
    labels = [
        (150, "回転を作る", "creates rotation"),
        (365, "心を合わせて伝える", "aligns and transmits"),
        (580, "回転を運ぶ", "carries rotation"),
        (795, "径の比で速度を変える", "changes speed by radius ratio"),
        (1010, "摩擦で伝える", "transmits by friction"),
        (1225, "シートに接触する", "contacts the sheet"),
    ]
    for x, ja, en in labels:
        svg.text(x, 382, ja, 16, 700, INK, "middle")
        svg.text(x, 404, en, 14, 400, MUTED, "middle")
    svg.rect(80, 440, 600, 190, fill=CARD, stroke=ACCENT, sw=2)
    svg.text(104, 476, "速度比 / speed ratio", 19, 700, ACCENT)
    svg.text(104, 514, "n2 / n1 = D1 / D2", 24, 700, INK)
    svg.text(104, 550, "大きいプーリが駆動なら従動側は速くなる", 17, 400, MUTED)
    svg.text(104, 578, "a larger driving pulley speeds up the driven one", 15, 400, MUTED)
    svg.text(104, 610, "（滑りのない仮定 / assuming no slip）", 15, 400, MUTED)
    svg.rect(712, 440, 648, 190, fill=JP_BG, stroke=ACCENT, sw=2)
    svg.text(736, 476, "点検の観点 / what to inspect", 19, 700, ACCENT)
    for index, (ja, en) in enumerate([("ベルト張力", "belt tension"), ("芯合わせ", "alignment"),
                                     ("異音・発熱", "noise and heat"), ("潤滑と摩耗", "lubrication and wear")]):
        top = 510 + index * 28
        svg.text(736, top, f"・{ja} / {en}", 16, 400, INK)
    svg.text(80, 668, "機械式伝達は簡単ですが、滑り・伸び・摩耗で速度が変わります。", 19, 700, INK)
    svg.text(80, 694, "Mechanical drives are simple, but slip, stretch and wear change the actual speed.", 16, 400, MUTED)
    svg.footer("指令した回転数と実際のシート速度は別に確認します。 / Commanded rpm and actual sheet speed are checked separately.")
    svg.save(out / "D07-06.svg")


def d07_07(out: Path) -> None:
    svg = new_diagram("D07-07", "モータとアクチュエータの種類", "Motor and actuator types",
                      "DAY 07 / ACTUATORS", 800)
    cards = [
        ("直流モータ", "DC motor", "簡単な速度制御・ブラシ摩耗に注意", "simple speed control; brush wear"),
        ("誘導モータ", "AC induction motor", "丈夫で連続運転向き・速度はVFDで調整", "rugged for continuous duty; VFD sets speed"),
        ("サーボモータ", "Servomotor", "位置と速度を高精度に制御・フィードバック必須", "precise position and speed; needs feedback"),
        ("ステッピングモータ", "Stepper motor", "開ループで段階的に動く・脱調に注意", "open-loop steps; watch for lost steps"),
    ]
    width = (1280 - 3 * 22) / 4
    for index, (ja, en, dja, den) in enumerate(cards):
        x = 80 + index * (width + 22)
        svg.card(x, 186, width, 210, ja, en, sub=f"{dja} / {den}")
    svg.text(80, 442, "指令と動力は別 / command versus power", 20, 700, ACCENT)
    chain(svg, [("PLC出力", "PLC output"), ("ドライバ", "Driver"), ("モータ", "Motor"), ("機械", "Machine")], 474, 108)
    svg.text(80, 622, "PLCは小さな信号を出し、ドライバが大きな電力を供給します。", 19, 700, INK)
    svg.text(80, 648, "The PLC issues a small signal; the driver supplies the large electrical power.", 16, 400, MUTED)
    svg.rect(80, 672, 1280, 62, fill=JP_BG, stroke=ACCENT, sw=1, rx=8)
    svg.text(100, 712, "空気圧シリンダ・電動シリンダもアクチュエータです。動力の種類が違うだけで役割は同じです。", 17, 700, INK)
    svg.footer("アクチュエータは「指令」と「エネルギー」の両方が必要です。 / An actuator needs both a command and energy.")
    svg.save(out / "D07-07.svg")


def d07_08(out: Path) -> None:
    svg = new_diagram("D07-08", "センサの分類", "Sensor taxonomy",
                      "DAY 07 / SENSORS", 860)
    svg.card(80, 186, 1280, 96, "物理量を情報に変える / a sensor converts a physical condition into usable information",
             "検出（あり/なし）と計測（連続値）を区別します / separate detection from measurement", accent=ACCENT)
    svg.card(80, 312, 610, 120, "接触式", "Contact type", sub="機械スイッチ・リミットスイッチ / mechanical and limit switches")
    svg.card(750, 312, 610, 120, "非接触式", "Non-contact type", sub="光・磁気・静電・超音波・回転 / optical, magnetic, capacitive, ultrasonic, rotary")
    leafs = [
        (80, "光電センサ", "Photoelectric", "透過・反射・拡散 / through, retro, diffuse"),
        (410, "誘導形近接", "Inductive", "主に金属を検出 / mainly metal targets"),
        (740, "静電容量形", "Capacitive", "材質を選びにくい / less material-specific"),
        (1070, "超音波", "Ultrasonic", "距離・透明物に有効な場合 / distance and some transparent targets"),
    ]
    for x, ja, en, sub in leafs:
        svg.card(x, 456, 290, 130, ja, en, sub=sub, accent=GOOD)
    more = [
        (80, "ロータリエンコーダ", "Rotary encoder", "回転量・位置 / rotation and position"),
        (410, "リニアスケール", "Linear scale", "直線位置 / linear position"),
        (740, "温度センサ", "Temperature sensor", "熱の監視 / thermal monitoring"),
        (1070, "圧力・荷重", "Pressure and load", "張力の目安 / tension indication"),
    ]
    for x, ja, en, sub in more:
        svg.card(x, 610, 290, 130, ja, en, sub=sub, accent=WARN)
    svg.text(80, 776, "センサは対象材質・環境・必要精度・PLCの入力方式で選びます。", 18, 700, INK)
    svg.text(80, 800, "Select sensors by target material, environment, required precision and the PLC input type.", 15, 400, MUTED)
    svg.footer("「どのセンサでも同じように検出できる」とは限りません。 / No single sensor detects every material equally well.")
    svg.save(out / "D07-08.svg")


def d07_09(out: Path) -> None:
    svg = new_diagram("D07-09", "デジタル信号とアナログ信号", "Digital versus analog signals",
                      "DAY 07 / SIGNALS", 800)
    svg.rect(80, 186, 610, 340, fill=CARD, stroke=ACCENT, sw=2)
    svg.text(104, 222, "デジタル / digital: ON/OFF", 21, 700, ACCENT)
    svg.line(120, 400, 660, 400, marker=False)
    svg.text(104, 390, "1", 16, 700, MUTED)
    svg.text(104, 262, "0", 16, 700, MUTED)
    waveform(svg, 130, 396, 510, 260, 396, [(0.1, 1), (0.32, 0), (0.55, 1), (0.78, 0)])
    svg.text(104, 440, "検出 / detected = 1、非検出 / not detected = 0", 17, 400, MUTED)
    svg.text(104, 472, "PLC入力はビット（TRUE/FALSE）で扱います", 17, 700, INK)
    svg.text(104, 496, "the PLC handles the input as one bit", 15, 400, MUTED)
    svg.rect(750, 186, 610, 340, fill=CARD, stroke=GOOD, sw=2)
    svg.text(774, 222, "アナログ / analog: 連続値", 21, 700, GOOD)
    svg.line(790, 400, 1330, 400, marker=False)
    svg.line(790, 400, 790, 250, marker=False)
    svg.parts.append(
        '<path d="M790 380 C 880 380, 900 270, 1000 280 S 1180 380, 1330 300" fill="none" '
        'stroke="#1B7A4B" stroke-width="3"/>'
    )
    svg.text(794, 242, "電圧/電流 / voltage or current", 15, 400, MUTED)
    svg.text(774, 440, "例：0–10 V、4–20 mA（機器により異なる）", 17, 400, MUTED)
    svg.text(774, 472, "アナログ入力モジュールで数値に変換します", 17, 700, INK)
    svg.text(774, 496, "an analog input module converts it to a number", 15, 400, MUTED)
    truth_table(svg, 80, 570, ["項目 / item", "デジタル / digital", "アナログ / analog"], [
        ["表現 / value", "0 か 1", "連続した数値 / continuous"],
        ["用途 / use", "有無・位置", "距離・圧力・張力"],
        ["注意 / caution", "チャタリング・ノイズ", "スケーリング・校正"],
    ], col_w=426, row_h=40)
    svg.footer("信号の種類は選んだ機器の仕様で確認します。 / Confirm signal types in the selected device's specification.")
    svg.save(out / "D07-09.svg")


def d07_10(out: Path) -> None:
    svg = new_diagram("D07-10", "インクリメンタルエンコーダとパルス", "Incremental encoder and pulse interpretation",
                      "DAY 07 / ENCODERS", 820)
    svg.text(80, 200, "A相・B相のパルス / A and B channel pulses", 20, 700, ACCENT)
    svg.line(120, 330, 700, 330, marker=False)
    waveform(svg, 130, 300, 540, 232, 300, [(0.0, 1), (0.25, 0), (0.5, 1), (0.75, 0)], color=ACCENT)
    svg.text(96, 240, "A", 18, 700, ACCENT)
    svg.line(120, 400, 700, 400, marker=False)
    waveform(svg, 130, 400, 540, 332, 400, [(0.125, 1), (0.375, 0), (0.625, 1), (0.875, 0)], color=GOOD)
    svg.text(96, 340, "B", 18, 700, GOOD)
    svg.text(96, 412, "", 10)
    svg.text(130, 444, "AとBのずれで回転方向が分かります / the A-B phase difference gives direction", 17, 400, MUTED)
    svg.rect(760, 190, 600, 200, fill=CARD, stroke=ACCENT, sw=2)
    svg.text(784, 226, "用語 / terms", 20, 700, ACCENT)
    svg.text(784, 262, "PPR: 1回転あたりのパルス数 / pulses per revolution", 17, 400, INK)
    svg.text(784, 292, "分解能: 方式によりカウント数が変わる", 17, 700, INK)
    svg.text(784, 316, "resolution: decoded counts depend on the mode", 15, 400, MUTED)
    svg.text(784, 352, "（1倍・2倍・4倍の逓倍 / x1, x2, x4 decoding）", 15, 400, MUTED)
    truth_table(svg, 80, 500, ["項目 / item", "値の例 / example", "意味 / meaning"], [
        ["PPR", "1,000", "1回転のA相パルス / A pulses per turn"],
        ["4倍カウント", "4,000", "1回転の分解カウント / decoded counts per turn"],
        ["移動量", "カウント × 1カウントの距離", "位置の計算 / position calculation"],
    ], col_w=420, row_h=42)
    svg.text(80, 700, "PPRとカウント数を混同すると、位置計算が4倍ずれることがあります。", 18, 700, BAD)
    svg.text(80, 726, "Confusing PPR with decoded counts can make position wrong by a factor of four.", 15, 400, MUTED)
    svg.footer("エンコーダの取付位置と分解能の定義を先に確認します。 / Confirm mounting position and resolution definition first.")
    svg.save(out / "D07-10.svg")


def d07_11(out: Path) -> None:
    svg = new_diagram("D07-11", "空気圧シリンダと電磁弁", "Pneumatic cylinder and solenoid valve",
                      "DAY 07 / PNEUMATICS", 780)
    svg.text(80, 200, "空気の流れ / air flow", 20, 700, ACCENT)
    chain(svg, [("空気源", "Air supply"), ("レギュレータ", "Regulator"), ("電磁弁", "Solenoid valve"),
                ("シリンダ", "Cylinder")], 228, 110)
    svg.rect(100, 400, 1240, 150, fill=CARD, stroke=ACCENT, sw=2)
    svg.rect(300, 430, 640, 90, fill=JP_BG, stroke=ACCENT, sw=3, rx=8)
    svg.rect(340, 448, 220, 54, fill="#B9C8D6", stroke="#8497A8", sw=2, rx=4)
    svg.text(450, 482, "ピストン / piston", 16, 700, "#455A6C", "middle")
    svg.line(560, 475, 860, 475, stroke=WARN, sw=4)
    svg.text(700, 462, "ロッド / rod", 15, 400, WARN, "middle")
    svg.parts.append('<path d="M946 475 L1040 475" fill="none" stroke="#B4541E" stroke-width="4" marker-end="url(#arrow)"/>')
    svg.text(994, 450, "前進 / extend", 15, 700, WARN, "middle")
    svg.text(1000, 530, "後退 / retract", 15, 700, ACCENT, "middle")
    svg.text(80, 592, "電磁弁への電気信号が空気の経路を切り替えます。", 19, 700, INK)
    svg.text(80, 618, "An electrical signal to the solenoid valve switches the air path.", 16, 400, MUTED)
    svg.text(80, 654, "シリンダ端のセンサで「所定位置に着いたか」を確認します。", 18, 700, INK)
    svg.text(80, 680, "Cylinder-end sensors confirm that the actuator reached the expected position.", 15, 400, MUTED)
    svg.footer("空気圧は大きな力を出せますが、速度と停止位置の管理には注意が必要です。 / Air gives force, but speed and stopping position need care.")
    svg.save(out / "D07-11.svg")


def d07_12(out: Path) -> None:
    svg = new_diagram("D07-12", "機械の危険源と保護境界", "Machinery hazards and protective boundaries",
                      "DAY 07 / SAFETY BOUNDARIES", 860)
    svg.rect(80, 186, 1280, 340, fill=CARD, stroke=ACCENT, sw=2)
    svg.rect(140, 220, 1160, 270, fill="none", stroke=SAFE, sw=4, rx=16, dash="14 8")
    svg.text(150, 250, "保護範囲 / guarded boundary（設計・検証された安全系）", 17, 700, SAFE)
    svg.rect(210, 300, 240, 120, fill=JP_BG, stroke=ACCENT, sw=2)
    svg.text(330, 344, "ローラ", 18, 700, INK, "middle")
    svg.text(330, 368, "roller", 15, 400, MUTED, "middle")
    svg.rect(480, 300, 240, 120, fill=JP_BG, stroke=ACCENT, sw=2)
    svg.text(600, 344, "カメラ", 18, 700, INK, "middle")
    svg.text(600, 368, "camera", 15, 400, MUTED, "middle")
    svg.rect(750, 300, 240, 120, fill=JP_BG, stroke=ACCENT, sw=2)
    svg.text(870, 344, "制御盤", 18, 700, INK, "middle")
    svg.text(870, 368, "control cabinet", 15, 400, MUTED, "middle")
    svg.rect(1020, 300, 220, 120, fill="#F2E7D2", stroke=WARN, sw=2)
    svg.text(1130, 344, "駆動部", 18, 700, WARN, "middle")
    svg.text(1130, 368, "drive", 15, 400, MUTED, "middle")
    for x, ja, en in [(330, "巻き込み", "nip point"), (600, "落下物", "falling parts"),
                      (870, "感電", "electric shock"), (1130, "突然の起動", "unexpected start")]:
        svg.text(x, 452, f"⚠ {ja}", 16, 700, BAD, "middle")
        svg.text(x, 474, en, 14, 400, MUTED, "middle")
    svg.text(80, 570, "機械安全はリスクアセスメントに基づき、AIや通常のラダーとは独立して設計されます。", 19, 700, INK)
    svg.text(80, 596, "Machine safety is engineered from a risk assessment, independently of AI and ordinary ladder logic.", 16, 400, MUTED)
    chain(svg, [("ガード", "Guarding"), ("インターロック", "Interlock"), ("非常停止", "Emergency stop"),
                ("作業手順", "Safe procedure")], 630, 104, x0=80, x1=1360)
    svg.footer("本教材は安全回路を設計・生成しません。実務は有資格者と現地手順に従います。 / This course never designs or deploys safety circuits.")
    svg.save(out / "D07-12.svg")


# --------------------------------------------------------------------------- Day 8
def d08_01(out: Path) -> None:
    svg = new_diagram("D08-01", "PLCの構成と入出力", "PLC components and I/O modules",
                      "DAY 08 / PLC ARCHITECTURE", 820)
    svg.text(80, 200, "架空のMELSEC風ラック / fictional MELSEC-style rack (not the installed hardware)", 18, 700, MUTED)
    svg.rect(80, 218, 1280, 170, fill="#DCE4EC", stroke="#8497A8", sw=3, rx=10)
    modules = [
        ("電源", "Power supply", ACCENT), ("CPU", "CPU", GOOD), ("入力", "Digital input", ACCENT),
        ("出力", "Digital output", WARN), ("アナログ", "Analog", ACCENT), ("通信", "Comm.", SAFE),
    ]
    width = (1240 - 5 * 12) / 6
    for index, (ja, en, color) in enumerate(modules):
        x = 100 + index * (width + 12)
        svg.rect(x, 238, width, 130, fill=CARD, stroke=color, sw=2, rx=8)
        svg.text(x + width / 2, 286, ja, 19, 700, color, "middle")
        svg.text(x + width / 2, 310, en, 15, 400, MUTED, "middle")
        for led in range(4):
            svg.circle(x + 22 + led * 20, 342, 6, fill="#BFD3E4", stroke="#8497A8", sw=1)
    svg.text(80, 442, "信号の種類 / signal types", 20, 700, ACCENT)
    chain(svg, [("デジタル入力", "Digital input"), ("デジタル出力", "Digital output"),
                ("アナログ入力", "Analog input"), ("アナログ出力", "Analog output"), ("通信データ", "Comm. data")], 474, 112)
    svg.text(80, 626, "PLC内部では、ビット（X/Y/M）と数値レジスタ（Dなど）を使い分けます。", 19, 700, INK)
    svg.text(80, 652, "Inside the PLC, bits (X/Y/M) and numeric registers (such as D) serve different purposes.", 16, 400, MUTED)
    svg.text(80, 686, "装置名・番号・命令の意味はCPUとソフトの版で必ず確認します。", 17, 700, BAD)
    svg.text(80, 712, "Always confirm device names, numbers and instructions for the actual CPU and software version.", 15, 400, MUTED)
    svg.footer("PLCは入力・判断・出力を繰り返す産業用の制御装置です。 / A PLC repeatedly samples inputs, evaluates logic and updates outputs.")
    svg.save(out / "D08-01.svg")


def d08_02(out: Path) -> None:
    svg = new_diagram("D08-02", "センサからアクチュエータまでの信号経路", "Sensor → input → PLC → output → driver → actuator",
                      "DAY 08 / SIGNAL PATH", 720)
    chain(svg, [("センサ", "Sensor"), ("PLC入力", "PLC input"), ("プログラム", "Program"),
                ("PLC出力", "PLC output"), ("ドライバ", "Driver"), ("アクチュエータ", "Actuator")], 210, 130)
    svg.text(80, 378, "信号（小さい電力）/ signal (low power)", 17, 700, ACCENT)
    svg.text(80, 404, "プログラムは入力の状態から出力の状態を決めます。", 19, 700, INK)
    svg.text(80, 430, "The program decides output states from input states.", 16, 400, MUTED)
    svg.rect(80, 466, 620, 130, fill=CARD, stroke=ACCENT, sw=2)
    svg.text(104, 502, "信号側 / signal side", 19, 700, ACCENT)
    svg.text(104, 536, "24 V DC の入力・出力、通信", 17, 400, INK)
    svg.text(104, 560, "24 V DC I/O and communications", 15, 400, MUTED)
    svg.rect(732, 466, 628, 130, fill="#F2E7D2", stroke=WARN, sw=2)
    svg.text(756, 502, "動力側 / power side", 19, 700, WARN)
    svg.text(756, 536, "ドライバ・接触器が大きな電力を供給", 17, 400, INK)
    svg.text(756, 560, "drivers and contactors supply the large power", 15, 400, MUTED)
    svg.text(80, 646, "PLC出力はモータの運転電力を直接作るものではありません。", 18, 700, BAD)
    svg.text(80, 672, "A PLC output does not by itself provide a motor's operating power.", 15, 400, MUTED)
    svg.footer("信号の経路と動力の経路を分けて描くと、故障の切り分けができます。 / Drawing signal and power paths separately makes fault isolation possible.")
    svg.save(out / "D08-02.svg")


def d08_03(out: Path) -> None:
    svg = new_diagram("D08-03", "PLCのスキャン（タスク実行）周期", "Simplified PLC scan/task cycle",
                      "DAY 08 / SCAN CYCLE", 760)
    svg.rect(420, 210, 280, 120, fill=CARD, stroke=ACCENT, sw=3)
    svg.text(560, 258, "入力の取り込み", 20, 700, ACCENT, "middle")
    svg.text(560, 284, "input refresh", 16, 400, MUTED, "middle")
    svg.rect(420, 400, 280, 120, fill=CARD, stroke=GOOD, sw=3)
    svg.text(560, 448, "プログラム実行", 20, 700, GOOD, "middle")
    svg.text(560, 474, "program execution", 16, 400, MUTED, "middle")
    svg.rect(420, 590, 280, 110, fill=CARD, stroke=WARN, sw=3)
    svg.text(560, 636, "出力の更新", 20, 700, WARN, "middle")
    svg.text(560, 662, "output update", 16, 400, MUTED, "middle")
    svg.line(570, 334, 570, 392, stroke=ACCENT, sw=3)
    svg.line(570, 524, 570, 582, stroke=GOOD, sw=3)
    svg.parts.append(
        f'<path d="M420 645 C 240 645 240 270 412 270" fill="none" stroke="{WARN}" stroke-width="3" marker-end="url(#arrow)"/>'
    )
    svg.text(250, 452, "繰り返し", 18, 700, WARN)
    svg.text(250, 476, "repeat", 15, 400, MUTED)
    svg.rect(780, 240, 580, 200, fill=JP_BG, stroke=ACCENT, sw=2)
    svg.text(804, 276, "重要な注意 / important caution", 19, 700, ACCENT)
    svg.text(804, 310, "・周期の長さはCPU・設定・通信で変わります", 16, 400, INK)
    svg.text(804, 336, "・全てのPLCが同じ順序とは限りません", 16, 400, INK)
    svg.text(804, 362, "・通信の更新は別のタイミングの場合があります", 16, 400, INK)
    svg.text(804, 388, "・実際の順序はマニュアルで確認します", 16, 400, INK)
    svg.text(780, 482, "入力の変化が出力に反映されるまでに時間がかかります。", 19, 700, INK)
    svg.text(780, 508, "A change at an input takes time to appear at an output.", 16, 400, MUTED)
    svg.text(780, 544, "速い現象（欠陥通過・パルス）は取りこぼしに注意します。", 18, 700, WARN)
    svg.text(780, 570, "Fast events (defects passing, pulses) can be missed between scans.", 15, 400, MUTED)
    svg.footer("スキャン時間は「応答時間」の一部です。 / Scan time is only part of total response time.")
    svg.save(out / "D08-03.svg")


def d08_04(out: Path) -> None:
    svg = new_diagram("D08-04", "物理的なセンサ状態とPLC入力ビット", "Input state versus physical sensor state",
                      "DAY 08 / LOGICAL VERSUS PHYSICAL", 820)
    svg.text(80, 196, "同じ「停止」でも、配線・ビット・接点評価は別の話です。", 20, 700, INK)
    svg.text(80, 222, "The same “stop” involves separate questions of wiring, bit state and contact evaluation.", 16, 400, MUTED)
    headers = ["項目 / item", "例A / example A", "例B / example B"]
    rows = [
        ["現場の状態 / field condition", "押されていない / not pressed", "押されている / pressed"],
        ["接点の物理配線 / wiring", "NO（閉でON）", "NO"],
        ["PLC入力ビット X0", "0（OFF）", "1（ON）"],
        ["NO論理接点の評価", "偽 / false", "真 / true"],
        ["NC論理接点の評価", "真 / true", "偽 / false"],
    ]
    truth_table(svg, 80, 258, headers, rows, col_w=400, row_h=44)
    svg.rect(80, 542, 1280, 120, fill=JP_BG, stroke=ACCENT, sw=2)
    svg.text(104, 578, "ラダーのNC接点は「参照ビットが0のときに導通」と評価されます。", 19, 700, ACCENT)
    svg.text(104, 606, "A ladder NC instruction conducts when the referenced bit is 0.", 16, 400, MUTED)
    svg.text(104, 638, "これは現場スイッチの物理配線がNCであることを意味しません。", 17, 700, BAD)
    svg.text(80, 700, "配線（NO/NC）と論理（NO/NC）を混同すると、停止条件の誤解につながります。", 18, 700, INK)
    svg.text(80, 726, "Confusing physical wiring with logical contact type leads to wrong stop-condition reasoning.", 15, 400, MUTED)
    svg.footer("「ビットが0」と「スイッチが押されていない」は別の情報です。 / “Bit is 0” and “switch not pressed” are different facts.")
    svg.save(out / "D08-04.svg")


def d08_05(out: Path) -> None:
    svg = new_diagram("D08-05", "NO接点とNC接点の論理", "Normally open and normally closed logical contacts",
                      "DAY 08 / LADDER CONTACTS", 740)
    for index, (label_ja, label_en, nc) in enumerate([("NO接点（a接点）", "NO contact", False),
                                                     ("NC接点（b接点）", "NC contact", True)]):
        top = 200 + index * 250
        svg.rect(80, top, 1280, 210, fill=CARD, stroke=ACCENT if not nc else WARN, sw=2)
        svg.text(104, top + 36, label_ja, 20, 700, ACCENT if not nc else WARN)
        svg.text(104, top + 60, label_en, 16, 400, MUTED)
        svg.line(360, top + 120, 1080, top + 120, marker=False)
        ladder_contact(svg, 620, top + 120, nc, "X0")
        ladder_coil(svg, 940, top + 120, "Y0")
        if nc:
            svg.text(620, top + 86, "ビット0で導通 / conducts when bit = 0", 15, 700, WARN, "middle")
            svg.text(104, top + 160, "X0 = 0 → 導通 → Y0 ON", 18, 700, INK)
            svg.text(104, top + 184, "X0 = 1 → 遮断 → Y0 OFF", 18, 400, MUTED)
        else:
            svg.text(620, top + 86, "ビット1で導通 / conducts when bit = 1", 15, 700, ACCENT, "middle")
            svg.text(104, top + 160, "X0 = 1 → 導通 → Y0 ON", 18, 700, INK)
            svg.text(104, top + 184, "X0 = 0 → 遮断 → Y0 OFF", 18, 400, MUTED)
    svg.text(80, 700, "どちらも「ビットの値」を評価する論理命令であり、電線の種類ではありません。", 18, 700, INK)
    svg.text(80, 726, "Both are logical instructions that evaluate a bit value, not descriptions of the cable.", 15, 400, MUTED)
    svg.footer("訓練用の仮想回路です。実機の配線や安全回路の代用ではありません。 / Training logic only; not a substitute for real wiring or safety circuits.")
    svg.save(out / "D08-05.svg")


def d08_06(out: Path) -> None:
    svg = new_diagram("D08-06", "AND・OR・NOTのラダーと真理値表", "Ladder AND/OR/NOT with truth tables",
                      "DAY 08 / BOOLEAN LOGIC", 880)
    panels = [
        (60, "AND（直列）", "AND (series)", [("0", "0", "0"), ("0", "1", "0"), ("1", "0", "0"), ("1", "1", "1")], False),
        (500, "OR（並列）", "OR (parallel)", [("0", "0", "0"), ("0", "1", "1"), ("1", "0", "1"), ("1", "1", "1")], True),
        (940, "NOT（反転）", "NOT (invert)", [("0", "1"), ("1", "0")], False),
    ]
    for x, ja, en, rows, parallel in panels:
        svg.rect(x, 186, 440, 450, fill=CARD, stroke=ACCENT, sw=2)
        svg.text(x + 20, 222, ja, 19, 700, ACCENT)
        svg.text(x + 20, 246, en, 15, 400, MUTED)
        if parallel:
            svg.line(x + 40, 330, x + 300, 330, marker=False)
            svg.line(x + 40, 280, x + 40, 380, marker=False)
            svg.line(x + 40, 280, x + 300, 280, marker=False)
            svg.line(x + 40, 380, x + 300, 380, marker=False)
            svg.line(x + 300, 280, x + 300, 380, marker=False)
            ladder_contact(svg, x + 170, 280, False, "X1", 14, label_dy=-24)
            ladder_contact(svg, x + 170, 380, False, "X2", 14, label_dy=40)
            svg.line(x + 300, 330, x + 410, 330, marker=False)
            ladder_coil(svg, x + 370, 330, "Y0")
        elif len(rows[0]) == 2:
            svg.line(x + 40, 330, x + 410, 330, marker=False)
            ladder_contact(svg, x + 180, 330, True, "X0", 14)
            ladder_coil(svg, x + 370, 330, "Y0")
        else:
            svg.line(x + 40, 330, x + 410, 330, marker=False)
            ladder_contact(svg, x + 100, 330, False, "X0", 14)
            ladder_contact(svg, x + 210, 330, False, "X1", 14)
            ladder_coil(svg, x + 370, 330, "Y0")
        if len(rows[0]) == 3:
            truth_table(svg, x + 40, 442, ["X0", "X1", "Y0"], [list(r) for r in rows],
                        col_w=110, row_h=34)
        else:
            truth_table(svg, x + 60, 442, ["X0", "Y0"], [list(r) for r in rows], col_w=150, row_h=34)
    svg.text(80, 676, "直列＝すべて真で導通、並列＝どれか真で導通、反転＝真偽を入れ替えます。", 18, 700, INK)
    svg.text(80, 702, "Series means all true; parallel means any true; invert swaps true and false.", 15, 400, MUTED)
    svg.text(80, 740, "すべてシミュレーション用の仮想入出力です。 / All inputs and outputs here are simulated training signals.", 17, 700, BAD)
    svg.text(80, 766, "実機の安全停止をこの論理だけで構成することはできません。 / This logic alone cannot form a real safety stop.", 15, 400, MUTED)
    svg.footer("真理値表とラダーを必ず突き合わせて確認します。 / Always check the ladder against its truth table.")
    svg.save(out / "D08-06.svg")


def d08_07(out: Path) -> None:
    svg = new_diagram("D08-07", "自己保持（保持回路）", "Self-holding virtual indicator circuit",
                      "DAY 08 / SELF-HOLDING", 720)
    svg.rect(80, 190, 1280, 260, fill=CARD, stroke=ACCENT, sw=2)
    svg.text(104, 226, "起動は押しボタン、保持は内部ビット、停止はNC接点", 19, 700, ACCENT)
    svg.text(104, 250, "Start from a momentary button, hold with an internal bit, stop with an NC contact", 15, 400, MUTED)
    svg.line(140, 350, 1200, 350, marker=False)
    ladder_contact(svg, 260, 350, False, "X0 起動 / start")
    svg.line(284, 350, 340, 350, marker=False)
    svg.line(300, 320, 300, 350, marker=False)
    svg.line(300, 320, 400, 320, marker=False)
    ladder_contact(svg, 400, 320, False, "M0")
    svg.line(424, 320, 470, 320, marker=False)
    svg.line(470, 320, 470, 350, marker=False)
    ladder_contact(svg, 640, 350, True, "X1 停止 / stop")
    ladder_coil(svg, 900, 350, "M0 / Y0")
    svg.text(80, 490, "1. X0を短く押す → M0がON", 18, 700, INK)
    svg.text(80, 516, "2. M0の接点がX0と並列に閉じ、指を離してもM0はON", 18, 400, MUTED)
    svg.text(80, 542, "3. X1（停止要求）がON → NC接点が開きM0はOFF", 18, 700, INK)
    svg.text(80, 576, "1. A short X0 press turns M0 ON. 2. The M0 contact holds it ON after release.", 16, 400, MUTED)
    svg.text(80, 600, "3. X1 (stop request) turns ON, the NC contact opens and M0 goes OFF.", 16, 400, MUTED)
    svg.rect(80, 630, 1280, 56, fill=JP_BG, stroke=WARN, sw=1, rx=8)
    svg.text(100, 664, "停止要求を最優先にし、非常停止や安全回路の代用にはしません。 / Stop request has priority; never used as an emergency stop.", 16, 700, WARN)
    svg.footer("保持は「覚えている状態」であり、安全を保証する機能ではありません。 / Holding is remembered state, not a safety function.")
    svg.save(out / "D08-07.svg")


def d08_08(out: Path) -> None:
    svg = new_diagram("D08-08", "オン遅延タイマの動作", "ON-delay timer timing chart",
                      "DAY 08 / TIMERS", 760)
    svg.line(140, 200, 1300, 200, marker=False)
    svg.text(100, 206, "", 10)
    svg.text(140, 190, "時間 / time", 15, 400, MUTED)
    # X0
    svg.text(90, 280, "X0", 18, 700, ACCENT)
    svg.line(160, 300, 1280, 300, marker=False)
    waveform(svg, 200, 288, 1000, 240, 288, [(0.0, 0), (0.2, 1), (0.6, 0)])
    svg.text(700, 226, "入力ONの時間が設定値に達すると完了", 16, 400, MUTED, "middle")
    # T0
    svg.text(90, 420, "T0", 18, 700, GOOD)
    svg.line(160, 440, 1280, 440, marker=False)
    waveform(svg, 200, 428, 1000, 380, 428, [(0.0, 0), (0.4, 1), (0.6, 0)])
    svg.text(400, 366, "設定時間 / preset", 15, 700, GOOD, "middle")
    svg.text(600, 470, "蓄積が完了すると接点が変化 / contact changes on completion", 15, 400, MUTED, "middle")
    # Y0
    svg.text(90, 560, "Y0", 18, 700, WARN)
    svg.line(160, 580, 1280, 580, marker=False)
    waveform(svg, 200, 568, 1000, 520, 568, [(0.0, 0), (0.4, 1), (0.6, 0)], color=WARN)
    svg.text(500, 508, "出力ON / output ON", 15, 700, WARN, "middle")
    svg.rect(80, 616, 1280, 60, fill=JP_BG, stroke=ACCENT, sw=1, rx=8)
    svg.text(100, 640, "時間の単位と基準（100 ms・10 msなど）はCPUと命令で異なります。", 16, 700, INK)
    svg.text(100, 662, "Time base (100 ms, 10 ms, ...) depends on the CPU and instruction; check the manual.", 15, 400, MUTED)
    svg.footer("「T0 K50＝必ず5秒」とは限りません。 / “T0 K50 equals 5 s” is not universal.")
    svg.save(out / "D08-08.svg")


def d08_09(out: Path) -> None:
    svg = new_diagram("D08-09", "カウンタと立ち上がりエッジ", "Counter and rising-edge behaviour",
                      "DAY 08 / COUNTERS", 760)
    svg.text(80, 196, "連続ONは何度も数えません。数えるのは「変化」です。", 20, 700, INK)
    svg.text(80, 222, "A continuous ON condition is not counted repeatedly; the counter counts transitions.", 16, 400, MUTED)
    svg.text(90, 290, "X0", 18, 700, ACCENT)
    svg.line(160, 312, 1280, 312, marker=False)
    waveform(svg, 200, 300, 1000, 248, 300, [(0.0, 0), (0.1, 1), (0.22, 0), (0.35, 1), (0.47, 0), (0.6, 1), (0.85, 0)])
    for index, fraction in enumerate((0.1, 0.35, 0.6)):
        px = 200 + fraction * 1000
        svg.line(px, 236, px, 320, stroke=GOOD, sw=2, dash="5 5", marker=False)
        svg.text(px, 224, f"↑ {index + 1}", 17, 700, GOOD, "middle")
    truth_table(svg, 80, 360, ["項目 / item", "値 / value", "説明 / explanation"], [
        ["カウント", "1 → 2 → 3", "立ち上がりごとに+1 / +1 per rising edge"],
        ["連続ON", "変化なし", "ONのままでは増えない / no count while held"],
        ["プリセット", "3に到達", "出力ON・自己保持の場合あり"],
        ["リセット", "0に戻る", "RST命令・入力で初期化"],
    ], col_w=420, row_h=42)
    svg.text(80, 600, "カウント値の保持・リセット条件・応答は、実装ごとに確認が必要です。", 18, 700, INK)
    svg.text(80, 626, "Retention, reset conditions and response of counters must be checked for each implementation.", 15, 400, MUTED)
    svg.text(80, 664, "ノイズによる短いパルスも数えることがあります。入力フィルタを検討します。", 17, 700, WARN)
    svg.text(80, 690, "Short noise pulses can also be counted; consider input filtering.", 15, 400, MUTED)
    svg.footer("数える対象は「回数」か「位置」かを先に決めます。 / Decide first whether you count events or measure position.")
    svg.save(out / "D08-09.svg")


def d08_10(out: Path) -> None:
    svg = new_diagram("D08-10", "機械の状態遷移", "Machine-state sequence",
                      "DAY 08 / SEQUENCE CONTROL", 860)
    states = [
        (80, 200, "待機", "Idle", ACCENT),
        (420, 200, "準備完了", "Ready", GOOD),
        (760, 200, "起動中", "Starting", ACCENT),
        (1100, 200, "運転中", "Running", GOOD),
        (1100, 420, "検査中", "Inspecting", GOOD),
        (760, 420, "停止処理", "Stopping", WARN),
        (420, 420, "故障", "Fault", BAD),
        (80, 420, "復旧", "Recovery", SAFE),
    ]
    for x, y, ja, en, color in states:
        svg.rect(x, y, 260, 110, fill=CARD, stroke=color, sw=3)
        svg.text(x + 24, y + 46, ja, 21, 700, color)
        svg.text(x + 24, y + 72, en, 16, 400, MUTED)
    svg.line(342, 255, 416, 255, marker=True)
    svg.text(378, 244, "条件成立", 14, 700, ACCENT, "middle")
    svg.line(682, 255, 756, 255, marker=True)
    svg.line(1022, 255, 1096, 255, marker=True)
    svg.line(1230, 312, 1230, 466, marker=True)
    svg.text(1244, 396, "検査開始 / start", 15, 700, GOOD)
    svg.line(1100, 525, 1024, 525, marker=True)
    svg.text(1062, 512, "停止要求", 14, 700, WARN, "middle")
    svg.text(1062, 552, "stop", 13, 400, MUTED, "middle")
    svg.line(760, 525, 684, 525, marker=True)
    svg.text(722, 512, "異常", 14, 700, BAD, "middle")
    svg.text(722, 552, "fault", 13, 400, MUTED, "middle")
    svg.line(420, 525, 344, 525, marker=True)
    svg.text(380, 512, "原因除去", 13, 700, SAFE, "middle")
    svg.text(380, 552, "clear", 13, 400, MUTED, "middle")
    svg.line(210, 466, 210, 314, marker=True)
    svg.text(222, 396, "再起動許可", 15, 700, SAFE)
    svg.text(222, 418, "restart permit", 13, 400, MUTED)
    svg.text(80, 630, "すべての遷移には「理由」があります。理由のない遷移は設計の穴です。", 20, 700, INK)
    svg.text(80, 656, "Every transition has a reason; an unexplained transition is a design gap.", 16, 400, MUTED)
    svg.rect(80, 686, 1280, 96, fill=JP_BG, stroke=ACCENT, sw=1, rx=8)
    svg.text(100, 712, "異常停止のあとの自動再起動は危険な場合があります。再起動は人が許可する設計を検討します。", 16, 700, INK)
    svg.text(100, 736, "Automatic restart after an unexpected stop can be hazardous; consider authorization by a person.", 15, 400, MUTED)
    svg.text(100, 762, "品質のNGと機械の故障は別の状態です。混ぜると対応を誤ります。", 16, 700, BAD)
    svg.footer("状態と遷移条件を表にして、全員が同じ理解を持つようにします。 / A state/transition table gives everyone the same understanding.")
    svg.save(out / "D08-10.svg")


def d08_11(out: Path) -> None:
    svg = new_diagram("D08-11", "HMI・PLC・診断情報", "HMI, PLC and diagnostics",
                      "DAY 08 / HMI AND DIAGNOSTICS", 800)
    svg.rect(80, 190, 560, 330, fill=CARD, stroke=ACCENT, sw=2)
    svg.text(104, 226, "HMI画面の例（架空）", 19, 700, ACCENT)
    svg.text(104, 250, "Example HMI screen (fictional)", 15, 400, MUTED)
    svg.rect(104, 268, 512, 220, fill="#0F2536", stroke="#0F2536", sw=2, rx=8)
    svg.text(124, 300, "状態 / status: 運転中", 17, 700, "#7FD1A8")
    svg.text(124, 330, "速度 / speed: (仮想) 0.50 m/s", 16, 400, "#DDE8F2")
    svg.text(124, 358, "カメラ / camera: 正常", 16, 400, "#DDE8F2")
    svg.text(124, 386, "AI: 正常", 16, 400, "#DDE8F2")
    svg.rect(124, 404, 200, 42, fill="#1B7A4B", stroke="#1B7A4B", sw=1, rx=6)
    svg.text(224, 431, "起動 / START", 16, 700, "white", "middle")
    svg.rect(340, 404, 240, 42, fill="#8A2B2B", stroke="#8A2B2B", sw=1, rx=6)
    svg.text(460, 431, "停止 / STOP", 16, 700, "white", "middle")
    svg.rect(680, 190, 680, 330, fill=CARD, stroke=GOOD, sw=2)
    svg.text(704, 226, "HMIの役割 / role of the HMI", 19, 700, GOOD)
    for index, (ja, en) in enumerate([("状態の表示", "show machine state"), ("警報と原因の表示", "alarms and causes"),
                                     ("操作（権限内）", "operations within permission"), ("読み取り専用の診断", "read-only diagnostics"),
                                     ("パラメータ変更の制限", "restricted parameter changes")]):
        svg.text(704, 264 + index * 30, f"・{ja} / {en}", 16, 400, INK)
    svg.text(704, 434, "HMIは安全条件を無効にする画面ではありません。", 17, 700, BAD)
    svg.text(704, 458, "The HMI is not a screen that disables safety conditions.", 15, 400, MUTED)
    svg.text(704, 490, "操作権限と記録（誰が何をしたか）を決めます。", 16, 700, INK)
    svg.text(80, 570, "警報は「何が起きたか」「何を確認するか」「誰が対応するか」まで表示します。", 19, 700, INK)
    svg.text(80, 596, "An alarm should state what happened, what to check and who responds.", 16, 400, MUTED)
    chain(svg, [("PLC", "control"), ("HMI", "display"), ("記録", "records"), ("人の判断", "human decision")], 628, 104)
    svg.footer("診断情報は原因究明のために残し、安全判断の代用にしません。 / Diagnostics support investigation; they do not replace safety judgement.")
    svg.save(out / "D08-11.svg")


def d08_12(out: Path) -> None:
    svg = new_diagram("D08-12", "プロセスインターロックと安全機能", "Process interlocks versus safety-related functions",
                      "DAY 08 / INTERLOCK CLASSES", 820)
    svg.rect(80, 190, 610, 330, fill=CARD, stroke=ACCENT, sw=2)
    svg.text(104, 226, "プロセス／品質インターロック", "Process and quality interlocks", 18, 700, ACCENT) if False else None
    svg.text(104, 226, "プロセス／品質インターロック", 18, 700, ACCENT)
    svg.text(104, 250, "Process and quality interlocks", 15, 400, MUTED)
    for index, (ja, en) in enumerate([("材料がない → 検査を開始しない", "no material → do not start"),
                                      ("AI結果が無効 → 良品にしない", "invalid AI result → not OK"),
                                      ("カメラ未準備 → 開始しない", "camera not ready → do not start"),
                                      ("通信断 → 保留にして人へ", "comm. lost → hold and notify")]):
        svg.text(104, 292 + index * 34, f"・{ja}", 16, 700, INK)
        svg.text(104, 312 + index * 34, f"  {en}", 14, 400, MUTED)
    svg.text(104, 486, "通常のラダーで実装できる制御ロジック", 16, 700, ACCENT)
    svg.text(104, 508, "ordinary control logic that can be written in a PLC", 14, 400, MUTED)
    svg.rect(750, 190, 610, 330, fill=CARD, stroke=SAFE, sw=2)
    svg.text(774, 226, "安全関連の機能（別設計）", 18, 700, SAFE)
    svg.text(774, 250, "Safety-related functions, engineered separately", 15, 400, MUTED)
    for index, (ja, en) in enumerate([("ガードの開放 → 危険動作を停止", "guard opened → stop hazardous motion"),
                                      ("非常停止 → 動力の遮断", "emergency stop → remove power"),
                                      ("両手操作・光カーテン", "two-hand control or light curtain"),
                                      ("リスクアセスメントと検証", "risk assessment and validation")]):
        svg.text(774, 292 + index * 34, f"・{ja}", 16, 700, INK)
        svg.text(774, 312 + index * 34, f"  {en}", 14, 400, MUTED)
    svg.text(774, 486, "通常のPLC出力では代用できない", 16, 700, SAFE)
    svg.text(774, 508, "cannot be replaced by an ordinary PLC output", 14, 400, MUTED)
    svg.line(720, 190, 720, 520, stroke=BAD, sw=4, dash="10 8", marker=False)
    svg.text(720, 170, "境界 / boundary", 16, 700, BAD, "middle")
    svg.text(80, 570, "「AIがNGと言ったから停止」は品質対応です。安全機能とは目的も基準も違います。", 19, 700, INK)
    svg.text(80, 596, "“Stop because AI said NG” is a quality response, with different purpose and standards from safety.", 15, 400, MUTED)
    svg.rect(80, 626, 1280, 90, fill=JP_BG, stroke=SAFE, sw=1, rx=8)
    svg.text(100, 654, "安全機能の設計・検証は、実際の危険源・要求性能・規格・有資格のレビューに基づきます。", 16, 700, INK)
    svg.text(100, 678, "Safety design depends on actual hazards, required performance, standards and competent review.", 15, 400, MUTED)
    svg.text(100, 702, "本教材は展開可能な安全プログラムを作りません。 / This course does not produce deployable safety programs.", 15, 700, BAD)
    svg.footer("3種類のインターロックを名前で区別して議論します。 / Name the three interlock classes explicitly in every discussion.")
    svg.save(out / "D08-12.svg")


# --------------------------------------------------------------------------- Day 9
def d09_01(out: Path) -> None:
    svg = new_diagram("D09-01", "検査システムの全体アーキテクチャ", "Complete inspection-system architecture",
                      "DAY 09 / SYSTEM ARCHITECTURE", 940)
    lanes = [
        ("機械 / mechanics", ACCENT, [("シート搬送", "web transport"), ("ローラ", "rollers"), ("駆動", "drive")]),
        ("センサ / sensors", ACCENT, [("材料有無", "material presence"), ("エンコーダ", "encoder"), ("エッジ", "edge")]),
        ("制御 / control", GOOD, [("PLC", "PLC"), ("HMI", "HMI"), ("安全系", "safety system")]),
        ("画像 / imaging", WARN, [("カメラ", "camera"), ("照明", "illumination"), ("トリガ", "trigger")]),
        ("AI / AI", WARN, [("産業用PC", "industrial PC"), ("YOLO/PatchCore", "models"), ("結果有効性", "validity")]),
        ("記録・人 / records", SAFE, [("保存", "storage"), ("警報", "alerts"), ("人による確認", "human review")]),
    ]
    y = 186
    for name, color, items in lanes:
        svg.rect(80, y, 250, 100, fill=CARD, stroke=color, sw=2)
        svg.text(104, y + 42, name.split(" / ")[0], 18, 700, color)
        svg.text(104, y + 66, name.split(" / ")[1], 14, 400, MUTED)
        width = (1030 - 2 * 20) / 3
        for index, (ja, en) in enumerate(items):
            x = 360 + index * (width + 20)
            svg.card(x, y, width, 100, ja, en, accent=color)
        y += 116
    svg.text(80, 892, "各層は別の種類の情報を運びます。すべてを同じ線で描くと誤解を生みます。", 17, 700, INK)
    svg.text(80, 918, "Each layer carries a different kind of information; drawing them all as one line causes misunderstanding.", 15, 400, MUTED)
    svg.footer("機械・信号・制御・画像・AI・人・安全を層として分けます。 / Separate mechanics, signals, control, imaging, AI, people and safety into layers.")
    svg.save(out / "D09-01.svg")


def d09_02(out: Path) -> None:
    svg = new_diagram("D09-02", "エリアスキャンとラインスキャン", "Area scan versus line scan",
                      "DAY 09 / CAMERA TYPES", 820)
    svg.rect(80, 190, 610, 350, fill=CARD, stroke=ACCENT, sw=2)
    svg.text(104, 226, "エリアスキャン", 20, 700, ACCENT)
    svg.text(104, 250, "Area scan: one 2-D image per exposure", 15, 400, MUTED)
    svg.rect(160, 280, 450, 230, fill="#DCE4EC", stroke="#8497A8", sw=2, rx=6)
    for row in range(3):
        for col in range(6):
            svg.rect(180 + col * 72, 300 + row * 70, 62, 60, fill="#EFF4F9", stroke="#9FB2C4", sw=1, rx=3)
    svg.text(385, 548, "1回の露光で2次元 / a full 2-D frame", 15, 400, MUTED, "middle")
    svg.rect(750, 190, 610, 350, fill=CARD, stroke=GOOD, sw=2)
    svg.text(774, 226, "ラインスキャン", 20, 700, GOOD)
    svg.text(774, 250, "Line scan: lines assembled using relative motion", 15, 400, MUTED)
    svg.rect(790, 330, 530, 22, fill="#D9C9A8", stroke="#B9A57C", sw=1, rx=2)
    svg.line(800, 310, 1300, 310, stroke=ACCENT, sw=2, marker=False)
    svg.rect(930, 280, 200, 34, fill=JP_BG, stroke=GOOD, sw=2, rx=4)
    svg.text(1030, 303, "1ラインずつ取得", 16, 700, GOOD, "middle")
    svg.line(1030, 318, 1030, 330, stroke=GOOD, sw=2)
    for index in range(9):
        svg.rect(800 + index * 58, 360 + index * 12, 530 - index * 58, 8, fill="#C7DBEA", stroke="#9FB2C4", sw=1)
    svg.text(1030, 548, "移動しながら積み上げる / assembled while the web moves", 15, 400, MUTED, "middle")
    truth_table(svg, 80, 580, ["観点 / aspect", "エリア / area", "ライン / line"], [
        ["対象 / target", "停止・間欠", "連続搬送"],
        ["画像 / image", "2次元フレーム", "ラインの連結"],
        ["同期 / sync", "トリガ", "移動と露光の同期"],
    ], col_w=426, row_h=40)
    svg.text(80, 756, "ラインスキャンが常に優れているわけではありません。速度・照明・対象で選びます。", 16, 700, BAD)
    svg.footer("連続シートではラインスキャンが候補になりますが、万能ではありません。 / Line scan is a candidate for continuous webs, not a universal answer.")
    svg.save(out / "D09-02.svg")


def d09_03(out: Path) -> None:
    svg = new_diagram("D09-03", "レンズ・視野・画素スケール", "Lens, field of view and pixel scale",
                      "DAY 09 / OPTICS", 800)
    svg.rect(80, 190, 640, 360, fill=CARD, stroke=ACCENT, sw=2)
    svg.text(104, 226, "視野（FOV）と作動距離", 19, 700, ACCENT)
    svg.text(104, 250, "Field of view and working distance", 15, 400, MUTED)
    svg.rect(300, 276, 90, 56, fill=JP_BG, stroke=ACCENT, sw=2, rx=6)
    svg.text(345, 310, "カメラ", 16, 700, INK, "middle")
    svg.poly([(345, 332), (160, 500), (530, 500)], marker=False, stroke=ACCENT)
    svg.line(345, 332, 345, 500, stroke=MUTED, sw=1, dash="6 5", marker=False)
    svg.text(354, 420, "作動距離 WD", 15, 700, MUTED)
    svg.line(160, 514, 530, 514, stroke=BAD, sw=3, marker=False)
    svg.text(345, 540, "視野 FOV / field of view", 16, 700, BAD, "middle")
    svg.rect(760, 190, 600, 200, fill=EN_BG, stroke=GOOD, sw=2)
    svg.text(784, 226, "画素スケール / pixel scale", 19, 700, GOOD)
    svg.text(784, 266, "mm/画素 = FOV ÷ 横画素数", 21, 700, INK)
    svg.text(784, 294, "mm/px = FOV ÷ horizontal pixels", 16, 400, MUTED)
    svg.text(784, 330, "仮定：FOV 600 mm、4096画素", 17, 700, INK)
    svg.text(784, 356, "600 ÷ 4096 ≈ 0.1465 mm/px", 19, 700, GOOD)
    svg.rect(760, 412, 600, 138, fill=CARD, stroke=ACCENT, sw=2)
    svg.text(784, 446, "注意 / caution", 18, 700, ACCENT)
    svg.text(784, 478, "1画素より小さい欠陥が必ず検出できる、", 16, 400, INK)
    svg.text(784, 502, "という意味ではありません。", 16, 400, INK)
    svg.text(784, 528, "コントラスト・光学・ノイズ・動き・モデルに依存します。", 15, 400, MUTED)
    svg.text(80, 588, "画素数を増やせば必ず良くなる、とは限りません。", 19, 700, BAD)
    svg.text(80, 614, "More pixels do not automatically mean better inspection.", 16, 400, MUTED)
    svg.text(80, 650, "被写界深度・歪み・照明ムラも検査能力に影響します。", 17, 700, INK)
    svg.text(80, 676, "Depth of field, distortion and uneven lighting also affect capability.", 15, 400, MUTED)
    svg.footer("スケールは仮定値です。実機は校正して確認します。 / The scale is hypothetical; real systems are calibrated and verified.")
    svg.save(out / "D09-03.svg")


def d09_04(out: Path) -> None:
    svg = new_diagram("D09-04", "照明方式による見え方の違い", "Inspection lighting comparisons",
                      "DAY 09 / ILLUMINATION", 860)
    panels = [
        (80, "拡散照明", "Diffuse", "反射を抑え表面の色むらを見る", "soft light shows surface tones", GOOD),
        (390, "直接照明", "Direct", "きずの陰影を強調・光沢は苦手", "emphasises shadows; glare risk", WARN),
        (700, "バックライト", "Backlight", "輪郭・穴・欠けの silhouette", "silhouette of edges and holes", ACCENT),
        (1010, "暗視野", "Dark field", "微細な凹凸・傷を光らせる", "makes fine scratches bright", SAFE),
    ]
    for x, ja, en, dja, den, color in panels:
        svg.rect(x, 190, 290, 340, fill=CARD, stroke=color, sw=2)
        svg.text(x + 16, 226, ja, 18, 700, color)
        svg.text(x + 16, 250, en, 14, 400, MUTED)
        svg.rect(x + 20, 268, 250, 160, fill="#EDEDE3", stroke="#C9C9B8", sw=2, rx=6)
        if ja == "バックライト":
            svg.rect(x + 60, 310, 170, 76, fill="#0F2536", stroke="#0F2536", sw=2, rx=6)
            svg.text(x + 145, 368, "輪郭のみ / silhouette", 13, 700, "#F2F6FA", "middle")
        else:
            svg.parts.append(
                f'<ellipse cx="{x + 130}" cy="350" rx="34" ry="12" fill="{"#6E6E5A" if ja == "拡散照明" else "#8A2B2B"}" opacity="0.75"/>'
            )
            svg.text(x + 190, 354, "きず / defect", 13, 700, MUTED)
        svg.text(x + 16, 462, dja, 15, 700, INK)
        svg.text(x + 16, 492, den, 14, 400, MUTED)
        svg.text(x + 16, 536, "同じ欠陥でも見え方が変わる", 14, 400, MUTED) if False else None
    svg.text(80, 572, "照明は「AIの前」の品質を決めます。照明が不安定ならモデルも不安定になります。", 19, 700, INK)
    svg.text(80, 598, "Lighting sets the quality before the AI runs; unstable lighting makes models unstable.", 16, 400, MUTED)
    svg.rect(80, 628, 1280, 60, fill=JP_BG, stroke=ACCENT, sw=1, rx=8)
    svg.text(100, 652, "照度・色温度・反射・経時変化を記録し、定期的に確認します（教育用の例示）。", 16, 700, INK)
    svg.text(100, 674, "Record intensity, colour, reflection and drift, and check them periodically.", 14, 400, MUTED)
    svg.footer("照明の変更はモデル性能を変えます。変更は再評価が必要です。 / A lighting change changes model performance and requires re-evaluation.")
    svg.save(out / "D09-04.svg")


def d09_05(out: Path) -> None:
    svg = new_diagram("D09-05", "材料の移動とモーションブラー", "Material movement and motion blur",
                      "DAY 09 / MOTION BLUR", 760)
    svg.text(80, 196, "移動距離 = 速度 × 露光時間", 24, 700, INK)
    svg.text(80, 226, "distance moved = velocity × exposure time", 17, 400, MUTED)
    cases = [
        (80, "短い露光", "short exposure", "0.1 ms", "鮮明 / sharp", GOOD, 20),
        (500, "中程度", "medium", "1.0 ms", "軽いぼけ / slight blur", WARN, 90),
        (920, "長い露光", "long exposure", "5.0 ms", "大きなぼけ / strong blur", BAD, 280),
    ]
    for x, ja, en, t, result, color, blur in cases:
        svg.rect(x, 268, 390, 300, fill=CARD, stroke=color, sw=2)
        svg.text(x + 16, 302, ja, 19, 700, color)
        svg.text(x + 16, 326, en, 14, 400, MUTED)
        svg.rect(x + 20, 344, 350, 140, fill="#EDEDE3", stroke="#C9C9B8", sw=2, rx=6)
        svg.parts.append(f'<ellipse cx="{x + 195}" cy="414" rx="{max(14, blur)}" ry="16" fill="#8A2B2B" opacity="0.7"/>')
        svg.text(x + 16, 516, f"露光 {t} / exposure", 16, 700, INK)
        svg.text(x + 16, 544, result, 16, 400, MUTED)
    svg.text(80, 610, "仮定：材料速度 0.5 m/s。0.5 m/s × 0.001 s = 0.5 mm の移動（中程度の例）。", 18, 700, INK)
    svg.text(80, 636, "Example: 0.5 m/s × 0.001 s = 0.5 mm of travel during exposure.", 15, 400, MUTED)
    svg.text(80, 672, "短い露光だけでは暗くなるため、十分な光量が必要です。", 17, 700, WARN)
    svg.text(80, 698, "Short exposure needs enough light; otherwise the image is dark and noisy.", 15, 400, MUTED)
    svg.footer("ぼけは欠陥コントラストを下げ、検出を不安定にします。 / Blur lowers defect contrast and destabilises detection.")
    svg.save(out / "D09-05.svg")


def d09_06(out: Path) -> None:
    svg = new_diagram("D09-06", "エンコーダ同期のライン取得", "Encoder-synchronized line acquisition",
                      "DAY 09 / SYNCHRONISATION", 820)
    svg.rect(80, 190, 1280, 180, fill=CARD, stroke=ACCENT, sw=2)
    svg.rect(100, 260, 1240, 26, fill="#D9C9A8", stroke="#B9A57C", sw=1, rx=2)
    for index in range(11):
        x = 140 + index * 112
        svg.line(x, 286, x, 320, stroke=ACCENT, sw=2)
        svg.text(x, 342, f"{index + 1}", 15, 400, MUTED, "middle")
    svg.text(106, 236, "移動方向 → / direction of travel", 17, 700, ACCENT)
    svg.text(100, 342 - 76, "", 10)
    svg.text(80, 402, "エンコーダのパルスが「1ライン」の間隔を決めます。", 20, 700, INK)
    svg.text(80, 428, "Encoder pulses define the travel interval for each acquired line.", 16, 400, MUTED)
    svg.text(90, 486, "ENC", 18, 700, GOOD)
    svg.line(160, 508, 1280, 508, marker=False)
    waveform(svg, 180, 496, 1080, 450, 496, [(0.02, 1), (0.07, 0), (0.12, 1), (0.17, 0), (0.22, 1), (0.27, 0),
                                             (0.32, 1), (0.37, 0), (0.42, 1), (0.47, 0), (0.52, 1), (0.57, 0),
                                             (0.62, 1), (0.67, 0), (0.72, 1), (0.77, 0), (0.82, 1), (0.87, 0)], color=GOOD)
    svg.text(90, 570, "TRIG", 18, 700, WARN)
    svg.line(160, 592, 1280, 592, marker=False)
    waveform(svg, 180, 580, 1080, 534, 580, [(0.05, 1), (0.075, 0), (0.15, 1), (0.175, 0), (0.25, 1), (0.275, 0),
                                              (0.35, 1), (0.375, 0), (0.45, 1), (0.475, 0), (0.55, 1), (0.575, 0),
                                              (0.65, 1), (0.675, 0), (0.75, 1), (0.775, 0), (0.85, 1), (0.875, 0)], color=WARN)
    truth_table(svg, 80, 616, ["項目 / item", "仮定値 / hypothetical", "意味 / meaning"], [
        ["材料速度", "30 m/min = 500 mm/s", "移動量の基準"],
        ["サンプル間隔", "0.2 mm/line", "1ラインの移動距離"],
        ["ライン周波数", "500 ÷ 0.2 = 2500 lines/s", "必要取得速度"],
    ], col_w=420, row_h=40)
    svg.footer("これは設計例です。実機はスケーリング・露光・照明・タイミングを検証します。 / A design example only; verify scaling, exposure, lighting and timing.")
    svg.save(out / "D09-06.svg")


def d09_07(out: Path) -> None:
    svg = new_diagram("D09-07", "画像取得からPC処理まで", "Image acquisition and industrial PC processing",
                      "DAY 09 / PROCESSING PIPELINE", 720)
    chain(svg, [("カメラ", "Camera"), ("転送", "Transfer"), ("バッファ", "Buffer"), ("前処理", "Preprocess")], 200, 120)
    chain(svg, [("AI推論", "AI inference"), ("後処理", "Postprocess"), ("結果", "Result"), ("記録", "Record")], 380, 120)
    svg.parts.append('<path d="M1310 320 L1310 345 L130 345 L130 376" fill="none" stroke="#2563A6" stroke-width="2.4" marker-end="url(#arrow)"/>')
    svg.text(80, 520, "各段階に時間があり、合計が「結果が出るまでの時間」になります。", 19, 700, INK)
    svg.text(80, 546, "Every stage takes time; the total is the time until a result is available.", 16, 400, MUTED)
    svg.text(80, 582, "バッファがいっぱいになると画像を取りこぼす可能性があります。", 18, 700, WARN)
    svg.text(80, 608, "A full buffer can cause images to be dropped.", 15, 400, MUTED)
    svg.text(80, 644, "産業用PCとAIモデルは別の概念です。PCは実行環境、モデルは計算手法です。", 17, 700, INK)
    svg.text(80, 670, "An industrial PC and an AI model are different: the PC is a platform, the model is a computation.", 15, 400, MUTED)
    svg.footer("処理のどの段階が遅いかを測ることが、性能改善の第一歩です。 / Measure which stage is slow before optimising.")
    svg.save(out / "D09-07.svg")


def d09_08(out: Path) -> None:
    svg = new_diagram("D09-08", "YOLOとPatchCoreの出力の違い", "YOLO versus PatchCore inference outputs",
                      "DAY 09 / MODEL OUTPUTS", 840)
    svg.rect(80, 190, 610, 340, fill=CARD, stroke=ACCENT, sw=2)
    svg.text(104, 226, "YOLO：学習した種類の検出", 19, 700, ACCENT)
    svg.text(104, 250, "YOLO: detection of learned classes", 15, 400, MUTED)
    svg.rect(120, 272, 530, 190, fill="#EDEDE3", stroke="#C9C9B8", sw=2, rx=6)
    svg.rect(210, 316, 150, 110, fill="none", stroke=GOOD, sw=3)
    svg.text(214, 306, "scratch 0.91", 15, 700, GOOD)
    svg.rect(400, 340, 120, 80, fill="none", stroke=WARN, sw=3)
    svg.text(404, 330, "spot 0.77", 15, 700, WARN)
    svg.text(120, 486, "クラス・枠・信頼度 / class, box, score", 16, 700, INK)
    svg.text(120, 510, "未知の欠陥は検出できないことがあります", 15, 400, MUTED)
    svg.rect(750, 190, 610, 340, fill=CARD, stroke=WARN, sw=2)
    svg.text(774, 226, "PatchCore：正常との差分", 19, 700, WARN)
    svg.text(774, 250, "PatchCore: difference from normal examples", 15, 400, MUTED)
    svg.rect(790, 272, 530, 190, fill="#EDEDE3", stroke="#C9C9B8", sw=2, rx=6)
    for cx, cy, r, fill in ((880, 340, 60, "#F3C08A"), (1030, 400, 46, "#E38E5A"), (1180, 330, 70, "#F7D9B4")):
        svg.circle(cx, cy, r, fill=fill, stroke="#C97B3B", sw=2)
    svg.text(790, 486, "異常スコア・異常マップ / score and anomaly map", 16, 700, INK)
    svg.text(790, 510, "原因や欠陥名は直接は示しません", 15, 400, MUTED)
    truth_table(svg, 80, 560, ["観点 / aspect", "YOLO", "PatchCore"], [
        ["学習 / training", "ラベル付き画像", "正常画像のみ"],
        ["出力 / output", "種類・位置・信頼度", "スコア・位置の目安"],
        ["閾値 / threshold", "検出閾値", "異常閾値"],
        ["限界 / limit", "未知クラス", "原因の説明"],
    ], col_w=426, row_h=40)
    svg.text(80, 776, "スコアは校正済みの確率ではありません。合格判定には別の基準が必要です。", 16, 700, BAD)
    svg.footer("2つのモデルを併用するときは、判定方針を文書で決めます。 / When combining models, define the decision policy in writing.")
    svg.save(out / "D09-08.svg")


def d09_09(out: Path) -> None:
    svg = new_diagram("D09-09", "PCとPLCの結果受け渡し", "PLC–PC communication and result validity",
                      "DAY 09 / HANDSHAKE", 840)
    svg.text(300, 200, "PLC", 21, 700, ACCENT, "middle")
    svg.text(1000, 200, "産業用PC", 21, 700, GOOD, "middle")
    svg.line(300, 216, 300, 740, stroke=ACCENT, sw=2, dash="8 6", marker=False)
    svg.line(1000, 216, 1000, 740, stroke=GOOD, sw=2, dash="8 6", marker=False)
    messages = [
        (280, "検査準備OK", "ready", True),
        (330, "検査要求＋ID", "request + ID", True),
        (390, "受付（ビジー）", "busy", False),
        (450, "結果＋ID＋有効/無効", "result + ID + valid/invalid", False),
        (510, "受領確認", "acknowledge", True),
        (570, "エラー／タイムアウト", "error or timeout", True),
    ]
    for y, text, en, left_to_right in messages:
        if left_to_right:
            svg.line(316, y, 984, y, stroke=ACCENT, sw=2.4)
            svg.text(650, y - 10, f"{text} / {en}", 15, 700, INK, "middle")
        else:
            svg.line(984, y, 316, y, stroke=GOOD, sw=2.4)
            svg.text(650, y - 10, f"{text} / {en}", 15, 700, INK, "middle")
    svg.rect(80, 620, 1280, 150, fill=JP_BG, stroke=ACCENT, sw=1, rx=8)
    svg.text(100, 650, "重要な区別 / essential distinctions", 17, 700, ACCENT)
    svg.text(100, 678, "・古い結果（前回のID）を今回の結果として使ってはいけません。", 16, 400, INK)
    svg.text(100, 702, "・通信成功は「結果が正しい」ことを証明しません。", 16, 400, INK)
    svg.text(100, 726, "・タイムアウトは「良品」ではありません。", 16, 700, BAD)
    svg.text(100, 750, "Old results, successful communication and timeouts must not be treated as a valid OK.", 15, 400, MUTED)
    svg.footer("結果には必ず「識別子」と「有効性」を付けます。 / Always attach an identity and a validity flag to each result.")
    svg.save(out / "D09-09.svg")


def d09_10(out: Path) -> None:
    svg = new_diagram("D09-10", "欠陥位置とマーキングの同期", "Defect-position and marking synchronization",
                      "DAY 09 / POSITION TRACKING", 800)
    svg.rect(80, 212, 1280, 26, fill="#D9C9A8", stroke="#B9A57C", sw=1, rx=2)
    svg.line(100, 198, 1320, 198, stroke=MUTED, sw=2, marker=True)
    svg.text(120, 188, "材料の移動方向 / web travel", 16, 700, MUTED)
    svg.rect(240, 262, 240, 90, fill=JP_BG, stroke=GOOD, sw=2, rx=8)
    svg.text(360, 298, "検査点", 18, 700, GOOD, "middle")
    svg.text(360, 322, "inspection point", 14, 400, MUTED, "middle")
    svg.line(360, 238, 360, 258, stroke=GOOD, sw=2)
    svg.rect(820, 262, 240, 90, fill="#F2E7D2", stroke=WARN, sw=2, rx=8)
    svg.text(940, 298, "マーキング点", 18, 700, WARN, "middle")
    svg.text(940, 322, "marking station", 14, 400, MUTED, "middle")
    svg.line(940, 238, 940, 258, stroke=WARN, sw=2)
    svg.line(360, 412, 940, 412, stroke=BAD, sw=3, marker=False)
    svg.text(650, 400, "既知の距離 L（仮定）/ known distance L (hypothetical)", 16, 700, BAD, "middle")
    svg.rect(360, 442, 16, 26, fill=BAD, stroke=BAD, sw=1)
    svg.text(388, 460, "欠陥発生位置（エンコーダ値で記録）", 16, 400, INK)
    svg.rect(80, 502, 620, 160, fill=CARD, stroke=ACCENT, sw=2)
    svg.text(104, 536, "計算の例 / calculation example", 18, 700, ACCENT)
    svg.text(104, 568, "速度 0.5 m/s、結果遅延 0.12 s → 60 mm 移動", 17, 400, INK)
    svg.text(104, 596, "0.5 × 0.12 = 0.06 m = 60 mm", 17, 700, INK)
    svg.text(104, 628, "移動量は「位置ずれ誤差」と同じではありません", 16, 700, BAD)
    svg.rect(732, 502, 628, 160, fill=JP_BG, stroke=ACCENT, sw=2)
    svg.text(756, 536, "同期に必要な情報 / what sync needs", 18, 700, ACCENT)
    for index, (ja, en) in enumerate([("エンコーダ位置", "encoder position"), ("可変速度", "variable speed"),
                                     ("処理遅延", "processing delay"), ("動作遅延", "actuation delay")]):
        svg.text(756, 568 + index * 26, f"・{ja} / {en}", 15, 400, INK)
    svg.text(80, 710, "一定速度だけで設計すると、加減速時に位置がずれます。", 18, 700, WARN)
    svg.text(80, 736, "Designing for constant speed alone causes position error during acceleration.", 15, 400, MUTED)
    svg.footer("位置追跡・処理遅延・判断可能時刻・動作時刻を分けて扱います。 / Treat tracking, delay, decision time and action time separately.")
    svg.save(out / "D09-10.svg")


def d09_11(out: Path) -> None:
    svg = new_diagram("D09-11", "システム全体の遅延とバッファ", "Complete system latency and buffering",
                      "DAY 09 / REAL-TIME PERFORMANCE", 820)
    stages = [
        ("取得", "acquire", 18, ACCENT), ("転送", "transfer", 10, ACCENT), ("待ち", "queue", 22, WARN),
        ("前処理", "preprocess", 12, GOOD), ("推論", "inference", 30, GOOD), ("後処理", "postprocess", 10, ACCENT),
        ("通信", "comm.", 14, ACCENT),
    ]
    total = sum(stage[2] for stage in stages)
    x = 120
    svg.text(80, 200, "遅延の内訳（仮定の割合）/ latency breakdown (illustrative proportions)", 19, 700, INK)
    for ja, en, value, color in stages:
        width = value / total * 1160
        svg.rect(x, 226, width, 90, fill=CARD, stroke=color, sw=2)
        svg.text(x + width / 2, 264, ja, 15, 700, color, "middle")
        svg.text(x + width / 2, 286, en, 12, 400, MUTED, "middle")
        svg.text(x + width / 2, 308, f"{value}", 13, 400, MUTED, "middle")
        x += width
    svg.text(80, 356, "平均値だけでは不十分です。最大値（ワーストケース）とばらつき（ジッタ）を見ます。", 19, 700, INK)
    svg.text(80, 382, "Averages are not enough; examine worst-case values and jitter.", 16, 400, MUTED)
    for index, (ja, en, color) in enumerate([("空き", "empty", GOOD), ("処理中", "processing", ACCENT),
                                            ("待ち", "waiting", WARN), ("満杯（喪失リスク）", "full: drop risk", BAD)]):
        x = 80 + index * 320
        svg.rect(x, 420, 300, 110, fill=CARD, stroke=color, sw=2)
        svg.text(x + 20, 456, ja, 18, 700, color)
        svg.text(x + 20, 480, en, 14, 400, MUTED)
        for box in range(5):
            fill = color if box <= index else "#E6ECF2"
            svg.rect(x + 20 + box * 52, 496, 44, 20, fill=fill, stroke=color, sw=1, rx=3)
    svg.text(80, 588, "バッファ容量は「遅延の許容」と「取りこぼしの許容」の trade-off です。", 17, 700, INK)
    svg.text(80, 614, "Buffer size trades acceptable latency against acceptable dropped images.", 15, 400, MUTED)
    svg.text(80, 650, "推論時間だけを全体の応答時間と考えてはいけません。", 18, 700, BAD)
    svg.text(80, 676, "Do not treat inference time as the whole machine response time.", 15, 400, MUTED)
    svg.text(80, 712, "遅い結果が後から届くと、古い位置に誤って対応付ける危険があります。", 17, 700, WARN)
    svg.footer("遅延・順序・取りこぼしを測ってから能力を判断します。 / Measure latency, ordering and drops before judging capacity.")
    svg.save(out / "D09-11.svg")


def d09_12(out: Path) -> None:
    svg = new_diagram("D09-12", "故障時の品質判断と受入確認", "Fault handling, quality decision and acceptance checks",
                      "DAY 09 / FAULT HANDLING", 900)
    svg.rect(420, 186, 600, 84, fill=JP_BG, stroke=ACCENT, sw=2, rx=10)
    svg.text(720, 222, "検査ユニットの結果", 19, 700, ACCENT, "middle")
    svg.text(720, 248, "inspection unit result", 15, 400, MUTED, "middle")
    svg.line(720, 270, 720, 300, stroke=ACCENT, sw=2)
    branches = [
        (80, "有効・OK", "valid OK", "記録して次へ", "record and continue", GOOD),
        (390, "有効・NG", "valid NG", "記録・通知・下流対応", "record, notify, downstream action", WARN),
        (700, "無効", "invalid", "保留・人による確認", "hold and human review", BAD),
        (1010, "タイムアウト／通信断", "timeout / comm. loss", "良品にしない・原因確認", "never OK; find the cause", SAFE),
    ]
    for x, ja, en, action_ja, action_en, color in branches:
        svg.line(720, 300, 720, 320, stroke=ACCENT, sw=2, marker=False)
        svg.line(x + 140, 320, x + 140, 348, stroke=ACCENT, sw=2)
        svg.line(720, 320, x + 140, 320, stroke=ACCENT, sw=2, marker=False)
        svg.rect(x, 348, 280, 130, fill=CARD, stroke=color, sw=3)
        svg.text(x + 20, 384, ja, 18, 700, color)
        svg.text(x + 20, 408, en, 14, 400, MUTED)
        svg.text(x + 20, 440, action_ja, 15, 700, INK)
        svg.text(x + 20, 462, action_en, 13, 400, MUTED)
    svg.rect(80, 506, 1280, 120, fill=JP_BG, stroke=BAD, sw=2, rx=8)
    svg.text(104, 540, "必須の原則：有効でないAI結果を、黙って良品にしてはいけません。", 20, 700, BAD)
    svg.text(104, 568, "Mandatory rule: never silently convert an invalid AI result into product OK.", 16, 400, MUTED)
    svg.text(104, 600, "タイムアウト・画像なし・通信断・古いIDは、すべて「保留」として扱います。", 16, 700, INK)
    svg.text(80, 664, "受入確認の例 / acceptance checks (examples)", 19, 700, ACCENT)
    for index, (ja, en) in enumerate([("既知の良品・不良品で正しく判定", "known good and bad samples judged correctly"),
                                     ("無効結果がOKにならない", "invalid results never become OK"),
                                     ("再起動後に古い結果を使わない", "old results not reused after restart"),
                                     ("故障注入で検出できる", "fault injection is detected"),
                                     ("安全系がAIと独立している", "safety functions independent of AI")]):
        svg.text(80, 698 + index * 26, f"☐ {ja} / {en}", 15, 400, INK)
    svg.footer("故障を想定した試験が、システムの信頼性を決めます。 / Fault-injection testing is what establishes trustworthiness.")
    svg.save(out / "D09-12.svg")


# --------------------------------------------------------------------------- main
BUILDERS = {
    "day07": (d07_01, d07_02, d07_03, d07_04, d07_05, d07_06, d07_07, d07_08, d07_09, d07_10, d07_11, d07_12),
    "day08": (d08_01, d08_02, d08_03, d08_04, d08_05, d08_06, d08_07, d08_08, d08_09, d08_10, d08_11, d08_12),
    "day09": (d09_01, d09_02, d09_03, d09_04, d09_05, d09_06, d09_07, d09_08, d09_09, d09_10, d09_11, d09_12),
}


def main() -> None:
    failures = []
    for day, builders in BUILDERS.items():
        out = DIAGRAMS / day
        out.mkdir(parents=True, exist_ok=True)
        for builder in builders:
            try:
                builder(out)
            except AssertionError as error:
                failures.append(str(error))
    total = sum(len(builders) for builders in BUILDERS.values())
    print(f"Generated {total} diagrams under {DIAGRAMS}")
    for failure in failures:
        print("LAYOUT:", failure)
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
