"""Generate the bilingual SVG diagrams used by the Day 7-9 curriculum.

Run from any directory:
    python AI_Vision_Training\\day07_09_support\\scripts\\generate_day07_09_diagrams.py

Design rules
------------
* 1440 px wide, deterministic output, editable SVG text.
* Japanese above English in every label group.
* One colour family per concept: mechanical (blue), sensing (green),
  control (purple), energy (orange), data (teal), hazard (red).
* Line style carries meaning: solid = material/mechanical, dashed = energy,
  dotted = data. Arrows always show direction.
* Every diagram has a caption band that says what the student should notice.

The drawings are conceptual teaching figures: not construction drawings, not
ISO 1219-1 pneumatic schematics and not safety-certified designs.
"""

from __future__ import annotations

from pathlib import Path

from svgkit import (
    ACCENT,
    BAD,
    CARD,
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

MECH = "#1F5C99"
SENSOR = "#1B7A4B"
CONTROL = "#6B3FA0"
ENERGY = "#B4541E"
DATA = "#0E7490"
HAZARD = "#A32B2B"
GRID = "#C1D0DD"

FILL_MECH = "#E8F1FA"
FILL_SENSOR = "#EAF6EE"
FILL_CONTROL = "#F1ECF8"
FILL_ENERGY = "#FBEEE6"
FILL_DATA = "#E6F4F7"
FILL_HAZARD = "#F8E7E7"
FILL_GREY = "#EEF2F6"

FILL_COLOR = {
    ENERGY: FILL_ENERGY,
    DATA: FILL_DATA,
    CONTROL: FILL_CONTROL,
    GOOD: FILL_SENSOR,
    MECH: FILL_MECH,
    BAD: FILL_HAZARD,
}


# --------------------------------------------------------------------------- #
# layout helpers
# --------------------------------------------------------------------------- #
def panel(svg: Svg, x, y, w, h, ja, en, stroke=GRID, fill=CARD) -> None:
    svg.rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.4, rx=10)
    svg.text(x + 16, y + 30, ja, 19, 700, INK)
    svg.text(x + 16, y + 52, en, 14, 400, MUTED)


def chain(svg: Svg, items, y, h=120, x0=70, x1=1370, gap=26, accent=ACCENT) -> None:
    count = len(items)
    width = (x1 - x0 - gap * (count - 1)) / count
    for index, item in enumerate(items):
        x = x0 + index * (width + gap)
        ja, en = item[0], item[1]
        sub = item[2] if len(item) > 2 else None
        stroke = item[3] if len(item) > 3 else accent
        svg.card(x, y, width, h, ja, en, stroke=stroke, accent=stroke, sub=sub)
        if index < count - 1:
            svg.line(x + width + 2, y + h / 2, x + width + gap - 2, y + h / 2,
                     stroke=accent, sw=2.2)
    return width


def table_grid(svg: Svg, x, y, headers, rows, widths, row_h=42, header_h=38,
               header_fill=JP_BG, size=14) -> None:
    total = 0
    for index, header in enumerate(headers):
        w = widths[index]
        svg.rect(x + total, y, w, header_h, fill=header_fill, stroke=GRID, sw=1, rx=2)
        svg.text(x + total + w / 2, y + header_h * 0.68, header, size, 700, INK, "middle")
        total += w
    for row_index, row in enumerate(rows):
        top = y + header_h + row_index * row_h
        total = 0
        for col_index, value in enumerate(row):
            w = widths[col_index]
            svg.rect(x + total, top, w, row_h, fill=CARD, stroke=GRID, sw=1, rx=2)
            svg.text(x + total + 12, top + row_h * 0.66, str(value), size, 400, INK)
            total += w
    svg._track(x + sum(widths), y + header_h + row_h * len(rows))


def bar(svg: Svg, x, y, w, h, value, max_value, color, label, sub=None) -> None:
    height = 0 if max_value <= 0 else h * value / max_value
    svg.rect(x, y + h - height, w, height, fill=color, stroke=color, sw=1, rx=4)
    svg.text(x + w / 2, y + h + 24, label, 14, 600, INK, "middle")
    if sub:
        svg.text(x + w / 2, y + h + 44, sub, 13, 400, MUTED, "middle")
    svg.text(x + w / 2, y + h - height - 10, f"{value:g}", 14, 700, color, "middle")


def ladder_contact(svg: Svg, x, y, nc, address, label=None) -> None:
    svg.line(x - 30, y, x - 11, y, marker=False, sw=2)
    svg.line(x - 11, y - 18, x - 11, y + 18, marker=False, sw=2)
    svg.line(x + 11, y - 18, x + 11, y + 18, marker=False, sw=2)
    svg.line(x + 11, y, x + 30, y, marker=False, sw=2)
    if nc:
        svg.line(x - 15, y + 16, x + 15, y - 16, marker=False, sw=1.8)
    svg.text(x, y + 42, address, 15, 700, ACCENT, "middle")
    if label:
        svg.text(x, y - 28, label, 13, 400, MUTED, "middle")


def ladder_coil(svg: Svg, x, y, address, label=None) -> None:
    svg.rect(x - 17, y - 20, 34, 40, fill=CARD, stroke=ACCENT, sw=2.2, rx=17)
    svg.line(x - 62, y, x - 17, y, marker=False, sw=2)
    svg.line(x + 17, y, x + 62, y, marker=False, sw=2)
    svg.text(x, y + 44, address, 15, 700, ACCENT, "middle")
    if label:
        svg.text(x, y - 32, label, 13, 400, MUTED, "middle")


def ladder_row(svg: Svg, y, elements, start_x=230, step=130, label=None) -> float:
    """Draw one rung: contact/coil elements joined left to right. Returns the end x."""
    x = start_x
    previous_end = start_x - 80
    svg.line(start_x - 80, y, start_x - 30, y, marker=False, sw=2.4)
    for element in elements:
        if element[0] == "contact":
            _, nc, address, text = element
            ladder_contact(svg, x, y, nc, address, text)
            svg.line(previous_end, y, x - 30, y, marker=False, sw=2.4)
            previous_end = x + 30
            x += step
        else:
            _, address, text = element
            ladder_coil(svg, x + 30, y, address, text)
            svg.line(previous_end, y, x + 30 - 62, y, marker=False, sw=2.4)
            previous_end = x + 30 + 62
            x += step
    if label:
        svg.text(start_x - 80, y - 46, label, 15, 700, MUTED)
    return previous_end


def cylinder_symbol(svg: Svg, x, y, w=300, h=96, ja="複動シリンダ", en="double-acting cylinder") -> None:
    svg.rect(x, y, w, h, fill=FILL_MECH, stroke=MECH, sw=2.4, rx=8)
    px = x + w * 0.58
    svg.rect(px - 8, y + 8, 16, h - 16, fill=MECH, stroke=MECH, sw=1)
    svg.rect(px, y + h / 2 - 8, w * 0.56 + 46, 16, fill="#B9C9D9", stroke=MECH, sw=1.4, rx=3)
    svg.text(x + w / 2, y + h + 24, ja, 15, 700, INK, "middle")
    svg.text(x + w / 2, y + h + 44, en, 13, 400, MUTED, "middle")


def valve_symbol(svg: Svg, x, y, ja="電磁弁", en="solenoid valve") -> None:
    w, h = 190, 96
    svg.rect(x, y, w / 2, h, fill=FILL_ENERGY, stroke=ENERGY, sw=2, rx=2)
    svg.rect(x + w / 2, y, w / 2, h, fill=FILL_ENERGY, stroke=ENERGY, sw=2, rx=2)
    svg.line(x + 16, y + 26, x + 70, y + 26, stroke=ENERGY, sw=2)
    svg.line(x + 16, y + 70, x + 70, y + 70, stroke=ENERGY, sw=2)
    svg.line(x + w / 2 + 16, y + 26, x + w / 2 + 70, y + 70, stroke=ENERGY, sw=2)
    svg.line(x + w / 2 + 16, y + 70, x + w / 2 + 70, y + 26, stroke=ENERGY, sw=2)
    svg.rect(x - 40, y + 24, 32, 46, fill=CARD, stroke=CONTROL, sw=1.8, rx=3)
    svg.text(x - 24, y + 52, "SOL", 12, 700, CONTROL, "middle")
    svg.text(x + w / 2, y + h + 24, ja, 15, 700, INK, "middle")
    svg.text(x + w / 2, y + h + 44, en, 13, 400, MUTED, "middle")


def hazard_marker(svg: Svg, x, y, ja="危険", en="hazard") -> None:
    svg.parts.append(
        f'<path d="M{x} {y - 22} L{x + 22} {y + 16} L{x - 22} {y + 16} Z" '
        f'fill="#FBE3E3" stroke="{HAZARD}" stroke-width="2.4"/>'
    )
    svg.text(x, y + 8, "!", 20, 700, HAZARD, "middle")
    svg.text(x, y + 40, ja, 13, 700, HAZARD, "middle")
    svg.text(x, y + 58, en, 11, 400, HAZARD, "middle")


def legend_swatches(svg: Svg, x, y, items) -> None:
    for index, item in enumerate(items):
        color = item[0]
        label = f"{item[1]} / {item[2]}" if len(item) >= 3 else item[1]
        top = y + index * 32
        svg.rect(x, top, 26, 18, fill=color, stroke=color, sw=1, rx=3)
        svg.text(x + 36, top + 15, label, 14, 400, MUTED)


def label_box(svg: Svg, x, y, w, h, ja, en, fill=CARD, stroke=GRID, size=13) -> None:
    svg.rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.4, rx=6)
    svg.text(x + w / 2, y + h * 0.44, ja, size + 2, 700, INK, "middle")
    svg.text(x + w / 2, y + h * 0.78, en, size - 1, 400, MUTED, "middle")


def note(svg: Svg, y, ja, en, x=70, w=1300, stroke=ACCENT, fill=JP_BG) -> None:
    svg.rect(x, y, w, 78, fill=fill, stroke=stroke, sw=1.2, rx=8)
    svg.text(x + 18, y + 30, ja, 15, 700, INK)
    svg.text(x + 18, y + 54, en, 13, 400, MUTED)


# --------------------------------------------------------------------------- #
# Day 7
# --------------------------------------------------------------------------- #
def d07_01() -> Svg:
    svg = new_diagram("D07-01", "自動化設備の全体像", "Anatomy of an automation machine",
                      "第7日 / Day 7", 900)
    chain(svg, [
        ("入力・材料", "input / material", "材料が入る / material arrives", MECH),
        ("機械的な取扱い", "mechanical handling", "位置決め・搬送 / position, transport", MECH),
        ("加工・検査", "process or inspection", "加工・撮像 / process, imaging", SENSOR),
        ("出力・仕分け", "output or sorting", "良品・不良品 / good, reject", MECH),
    ], y=180, h=130)
    panel(svg, 70, 400, 1300, 340, "機械を説明する6つの要素", "the six elements that explain a machine")
    items = [
        ("構造", "structure", "フレーム・ガイド / frame, guide", MECH),
        ("動力", "power source", "空気・油圧・電気 / air, oil, electricity", ENERGY),
        ("アクチュエータ", "actuator", "シリンダ・モーター / cylinder, motor", MECH),
        ("センサー", "sensor", "位置・有無 / position, presence", SENSOR),
        ("制御装置", "controller", "PLC・PC / PLC, PC", CONTROL),
        ("ワーク", "workpiece", "製品・材料 / product, material", DATA),
    ]
    card_w = (1300 - 40 - 5 * 20) / 6
    for index, (ja, en, sub, color) in enumerate(items):
        x = 90 + index * (card_w + 20)
        svg.card(x, 480, card_w, 150, ja, en, stroke=color, accent=color, sub=sub)
    note(svg, 660, "自動化は「入力→取扱い→加工/検査→出力」の流れで説明できる。",
         "Automation can be described as input, handling, process or inspection, and output.")
    svg.footer("入力・取扱い・加工・検査・出力と、構造・動力・アクチュエータ・センサー・制御・ワーク",
               "Input, handling, process, inspection and output; structure, power, actuator, sensor, controller and workpiece")
    return svg


def d07_02() -> Svg:
    svg = new_diagram("D07-02", "1サイクル15秒のタイムライン", "A 15-second cycle on a timeline",
                      "第7日 / Day 7", 780)
    ops = [("位置決め", "positioning", 4, MECH), ("検出", "detection", 2, SENSOR),
           ("検査", "inspection", 5, DATA), ("動作", "actuation", 2, ENERGY),
           ("戻り", "return", 2, MECH)]
    x0, y = 100, 230
    scale = 84
    total = sum(op[2] for op in ops)
    cursor = x0
    svg.line(x0, y - 30, x0, y + 150, marker=False, sw=2, stroke=GRID)
    for second in range(total + 1):
        x = x0 + second * scale
        svg.line(x, y, x, y + 10, marker=False, sw=1.6, stroke=GRID)
        svg.text(x, y - 42, str(second), 14, 600, MUTED, "middle")
    for ja, en, duration, color in ops:
        width = duration * scale
        svg.rect(cursor, y, width, 100, fill=FILL_MECH if color == MECH else CARD, stroke=color, sw=2, rx=4)
        svg.text(cursor + width / 2, y + 42, ja, 17, 700, INK, "middle")
        svg.text(cursor + width / 2, y + 66, en, 12, 400, MUTED, "middle")
        svg.text(cursor + width / 2, y + 88, f"{duration} s", 13, 700, color, "middle")
        cursor += width
    svg.text(x0, 200, "時間 / time (s)", 14, 600, MUTED)
    table_grid(svg, 100, 430, ["合計 / total", "逐次 / sequential", "重なり / overlap"],
               [["15 s", "4+2+5+2+2 = 15 s", "図で確認してから合計 / check the timeline first"]],
               [220, 320, 520], row_h=56, size=15)
    note(svg, 560, "逐次なら足し算。重なる作業は図で確かめる。",
         "Add the times when the operations are sequential; confirm overlaps on the drawing.")
    svg.footer("1サイクルを時間軸に分けると、どこが長いか、どこが重なるかが見える",
               "Laying one cycle on a timeline shows which operation is long and which can overlap")
    return svg


def d07_03() -> Svg:
    svg = new_diagram("D07-03", "タクト・サイクル・生産能力", "Takt time, cycle time and capacity",
                      "第7日 / Day 7", 820)
    panel(svg, 70, 180, 400, 400, "タクトタイム（必要ペース）", "takt time (required pace)")
    svg.text(90, 290, "生産時間 ÷ 必要数量", 20, 700, INK)
    svg.text(90, 320, "available time ÷ required pieces", 14, 400, MUTED)
    svg.text(90, 390, "420×60 ÷ 600 = 42 秒/個", 24, 700, ACCENT)
    svg.text(90, 425, "42 s/piece", 16, 400, MUTED)
    svg.text(90, 490, "「間に合う速さ」の基準", 15, 400, INK)
    svg.text(90, 515, "the pace needed to finish on time", 13, 400, MUTED)

    panel(svg, 500, 180, 400, 400, "サイクルタイム（機械の時間）", "cycle time (machine time)")
    svg.text(520, 290, "1サイクルの所要時間", 20, 700, INK)
    svg.text(520, 320, "time for one machine cycle", 14, 400, MUTED)
    svg.text(520, 390, "15 秒/サイクル", 24, 700, MECH)
    svg.text(520, 425, "15 s/cycle", 16, 400, MUTED)
    svg.text(520, 490, "「決められた動作時間」", 15, 400, INK)
    svg.text(520, 515, "the defined operation duration", 13, 400, MUTED)

    panel(svg, 930, 180, 440, 400, "生産能力（個/時）", "production capacity (pieces/hour)")
    svg.text(950, 280, "3600 ÷ サイクル × 個数", 20, 700, INK)
    svg.text(950, 310, "3600 ÷ cycle × pieces per cycle", 14, 400, MUTED)
    svg.text(950, 370, "3600 ÷ 15 × 1 = 240 個/時", 22, 700, GOOD)
    svg.text(950, 405, "240 pieces/hour", 15, 400, MUTED)
    svg.text(950, 460, "×2個/サイクル = 480 個/時", 20, 700, GOOD)
    svg.text(950, 490, "two pieces per cycle doubles it", 14, 400, MUTED)
    svg.text(950, 540, "個数を言わないと能力は決まらない", 15, 700, WARN)
    svg.text(950, 562, "capacity is undefined without pieces per cycle", 12, 400, MUTED)

    note(svg, 620, "タクトは「必要」、サイクルは「機械」。単位を必ず書く。",
         "Takt is what is required; cycle is the machine. Always write the unit.")
    svg.footer("タクト42秒/個に対してサイクル15秒なら速度は足りる。能力は個数/サイクルで変わる",
               "A 15 s cycle meets a 42 s takt; capacity changes with pieces per cycle")
    return svg


def d07_04() -> Svg:
    svg = new_diagram("D07-04", "ボトルネックの考え方", "Understanding the bottleneck",
                      "第7日 / Day 7", 760)
    processes = [("工程A", "process A", 12, MECH), ("工程B", "process B", 20, BAD), ("工程C", "process C", 10, MECH)]
    x = 120
    for ja, en, seconds, color in processes:
        label_box(svg, x, 210, 240, 90, ja, en, fill=CARD, stroke=color, size=18)
        svg.text(x + 120, 350, f"{seconds} 秒/個", 26, 700, color, "middle")
        svg.text(x + 120, 378, f"{seconds} s/piece", 15, 400, MUTED, "middle")
        bar(svg, x + 60, 420, 120, 140, seconds, 20, color, "秒 / s")
        if x < 800:
            svg.line(x + 244, 255, x + 336, 255, stroke=ACCENT, sw=2.4)
        x += 400
    panel(svg, 70, 600, 1300, 120, "ライン全体の速さ = 一番遅い工程", "line output = the slowest process")
    svg.text(90, 690, "工程Bが20秒なので、全体は20秒/個より速くならない。 / process B limits the line to 20 s/piece.",
             16, 400, INK)
    svg.footer("速いアクチュエータを入れても、律速工程が変わらなければ生産数は増えない",
               "A faster actuator does not raise output while another process remains the limit")
    return svg


def d07_05() -> Svg:
    svg = new_diagram("D07-05", "効果金額の計算と前後比較", "Financial effect calculation and before/after comparison",
                      "第7日 / Day 7", 880)
    chain(svg, [
        ("削減時間", "time saved", "12秒/回 / 12 s per operation", MECH),
        ("年間工数", "annual hours", "132 時間/年 / 132 h/year", ENERGY),
        ("金額換算", "monetary value", "316,800 円/年 / JPY/year", GOOD),
        ("純効果", "net benefit", "316,800 − 運用費 / minus operating cost", CONTROL),
        ("回収期間", "payback", "1.42 年 / years", DATA),
    ], y=180, h=140)
    panel(svg, 70, 400, 620, 300, "改善前 / before", "before the improvement")
    bar(svg, 140, 470, 140, 150, 300, 300, BAD, "作業時間 / work time", "基準 / baseline")
    svg.text(330, 510, "1回12秒を180回/日", 18, 700, INK)
    svg.text(330, 540, "12 s × 180 per day", 14, 400, MUTED)
    svg.text(330, 590, "年間 220日 / 220 days a year", 15, 400, INK)
    svg.text(330, 615, "2,400 円/時 / JPY per hour", 15, 400, INK)

    panel(svg, 720, 400, 650, 300, "改善後 / after", "after the improvement")
    bar(svg, 790, 470, 140, 150, 240, 300, GOOD, "作業時間 / work time", "12秒短縮 / 12 s saved")
    svg.text(980, 510, "132時間/年 を削減", 18, 700, INK)
    svg.text(980, 540, "132 hours a year saved", 14, 400, MUTED)
    svg.text(980, 590, "年間効果 316,800 円/年", 18, 700, GOOD)
    svg.text(980, 615, "annual value 316,800 JPY/year", 14, 400, MUTED)
    svg.text(980, 660, "※現金化できるかは別の話 / cash realisation is separate", 13, 400, WARN)

    note(svg, 740, "回収期間 = 導入費 ÷ 年間純効果。純効果が0以下なら回収期間は意味を持たない。",
         "Payback = investment ÷ annual net benefit. It is meaningless at zero or negative net benefit.")
    svg.footer("削減時間 → 年間工数 → 金額 → 純効果 → 回収期間の順に計算する",
               "Calculate in the order: time saved, annual hours, money, net benefit, payback")
    return svg


def d07_06() -> Svg:
    svg = new_diagram("D07-06", "空圧・油圧・電気の比較", "Pneumatic, hydraulic and electrical power compared",
                      "第7日 / Day 7", 980)
    columns = [
        ("空圧 / pneumatic", ENERGY, ["エネルギー: 圧縮空気", "力: 軽〜中負荷", "速度: 流量制御", "位置: 2位置が基本",
                                      "保守: ドレン・漏れ", "制約: 圧縮性・残留圧力"]),
        ("油圧 / hydraulic", MECH, ["エネルギー: 加圧オイル", "力: 高い力を出しやすい", "速度: 流量制御",
                                     "位置: 中間は難しい", "保守: 油管理・漏れ", "制約: 発熱・高圧危険"]),
        ("電気 / electric", CONTROL, ["エネルギー: 電力", "力: 減速機で増幅", "速度: 精密制御",
                                       "位置: 得意（サーボ）", "保守: 比較的少ない", "制約: 保持・電気安全"]),
    ]
    for index, (title, color, rows) in enumerate(columns):
        x = 70 + index * 440
        svg.rect(x, 180, 400, 620, fill=CARD, stroke=color, sw=2, rx=12)
        svg.text(x + 200, 225, title, 22, 700, color, "middle")
        for row_index, text in enumerate(rows):
            svg.text(x + 24, 285 + row_index * 62, text, 15, 400, INK)
    note(svg, 830, "どれが一番よいかではなく、用途で選ぶ。絶対的な順位はない。",
         "This is not a ranking. Choose by application; there is no universal order.")
    svg.footer("空圧・油圧・電気の典型的な特徴。長所と制約を両方書く",
               "Typical characteristics of pneumatic, hydraulic and electrical power, including limitations")
    return svg


def d07_07() -> Svg:
    svg = new_diagram("D07-07", "油圧のエネルギーの流れ", "Hydraulic energy flow",
                      "第7日 / Day 7", 820)
    chain(svg, [
        ("電動機", "electric motor", "ポンプを回す / drives the pump", CONTROL),
        ("油圧ポンプ", "hydraulic pump", "オイルを加圧 / pressurises oil", MECH),
        ("リリーフ弁", "relief valve", "最高圧を制限 / limits pressure", ENERGY),
    ], y=190, h=140, x0=80, x1=800)
    chain(svg, [
        ("方向制御弁", "directional valve", "流れを切替 / switches flow", ENERGY),
        ("油圧シリンダ", "hydraulic cylinder", "直線運動 / linear motion", MECH),
        ("タンク・戻り", "tank and return", "油を戻す / returns oil", DATA),
    ], y=380, h=140, x0=80, x1=800)
    svg.line(800, 260, 900, 380, stroke=MECH, sw=2.4)
    panel(svg, 930, 190, 440, 330, "高圧の危険", "high-pressure hazards")
    for index, text in enumerate(["オイル漏れ / oil leakage", "発熱 / heat generation",
                                  "汚れ管理 / contamination control", "蓄えられた圧力 / stored energy"]):
        svg.text(950, 275 + index * 40, text, 15, 400, INK)
    hazard_marker(svg, 1250, 460)
    note(svg, 570, "油圧は大きな力が得意。ただし漏れ・発熱・高圧の危険を必ず扱う。",
         "Hydraulics suit high force, but leakage, heat and high pressure must be managed.")
    svg.footer("電動機 → ポンプ → 加圧オイル → 弁 → アクチュエータ → タンクの機能的な流れ",
               "Functional flow: motor, pump, pressurised oil, valve, actuator, tank")
    return svg


def d07_08() -> Svg:
    svg = new_diagram("D07-08", "空圧のエネルギーの流れ", "Pneumatic energy flow",
                      "第7日 / Day 7", 860)
    chain(svg, [
        ("コンプレッサ", "compressor", "空気を圧縮 / compresses air", ENERGY),
        ("フィルタ・レギュレータ", "filter and regulator", "ごみ除去・圧力調整 / clean and set pressure", DATA),
        ("電磁弁", "solenoid valve", "流れを切替 / switches flow", CONTROL),
    ], y=190, h=140, x0=80, x1=800)
    chain(svg, [
        ("流量制御弁", "flow control valve", "速度を調整 / sets speed", ENERGY),
        ("シリンダ", "cylinder", "直線運動 / linear motion", MECH),
        ("位置センサー", "position sensor", "端を確認 / confirms the end", SENSOR),
    ], y=380, h=140, x0=80, x1=800)
    svg.line(800, 260, 900, 380, stroke=ENERGY, sw=2.4)
    panel(svg, 930, 190, 440, 330, "空圧の制約", "pneumatic limitations")
    for index, text in enumerate(["圧縮性で速度が変わる / speed varies with load",
                                  "中間位置は苦手 / weak at intermediate positions",
                                  "漏れはエネルギー損失 / leaks waste energy",
                                  "残留圧力で動く / residual pressure moves it"]):
        svg.text(950, 275 + index * 40, text, 14, 400, INK)
    note(svg, 570, "フィルタレギュレータはFRLユニットではない。潤滑は機器が要求する場合だけ。",
         "A filter regulator is not an FRL unit. Lubricate only where the equipment requires it.")
    svg.footer("コンプレッサからシリンダまでの空圧の流れと、各機器の役割",
               "Pneumatic flow from compressor to cylinder, with the role of each component")
    return svg


def d07_09() -> Svg:
    svg = new_diagram("D07-09", "単動・複動シリンダと受圧面積", "Single-acting and double-acting cylinders, and effective areas",
                      "第7日 / Day 7", 900)
    panel(svg, 70, 180, 620, 300, "単動（ばね戻り）", "single-acting (spring return)")
    svg.rect(110, 270, 380, 90, fill=FILL_MECH, stroke=MECH, sw=2.4, rx=8)
    svg.rect(300, 258, 16, 114, fill=MECH, stroke=MECH, sw=1)
    svg.rect(316, 312, 210, 16, fill="#B9C9D9", stroke=MECH, sw=1.4, rx=3)
    svg.parts.append('<path d="M240 300 q10 -14 20 0 q10 14 20 0 q10 -14 20 0" fill="none" stroke="%s" stroke-width="2"/>' % ENERGY)
    svg.text(440, 400, "戻りはばね / return by spring", 15, 400, MUTED)
    svg.text(110, 440, "空気は片側だけ / air on one side only", 15, 400, INK)

    panel(svg, 750, 180, 620, 300, "複動（両側に空気）", "double-acting (air both sides)")
    svg.rect(790, 270, 380, 90, fill=FILL_MECH, stroke=MECH, sw=2.4, rx=8)
    svg.rect(980, 258, 16, 114, fill=MECH, stroke=MECH, sw=1)
    svg.rect(996, 312, 210, 16, fill="#B9C9D9", stroke=MECH, sw=1.4, rx=3)
    svg.line(760, 300, 786, 300, stroke=ENERGY, sw=2)
    svg.line(1176, 300, 1202, 300, stroke=ENERGY, sw=2)
    svg.text(860, 400, "押しも引きも空気 / air for both directions", 15, 400, MUTED)
    svg.text(790, 440, "戻り方を設計で決める / the return method is designed", 15, 400, INK)

    panel(svg, 70, 520, 1300, 250, "受圧面積 / effective areas", "effective areas")
    svg.text(100, 610, "押し側 A = π × D² ÷ 4", 22, 700, MECH)
    svg.text(100, 645, "extension: full piston area", 15, 400, MUTED)
    svg.text(100, 700, "0.5 × π × 20² ÷ 4 ≈ 157.08 N", 20, 700, INK)
    svg.text(700, 610, "引き側 A = π × (D² − d²) ÷ 4", 22, 700, MECH)
    svg.text(700, 645, "retraction: piston area minus rod area", 15, 400, MUTED)
    svg.text(700, 700, "0.5 × π × (20² − 8²) ÷ 4 ≈ 131.95 N", 20, 700, INK)
    svg.text(100, 750, "1 MPa = 1 N/mm² / ゲージ圧で計算 / use gauge pressure", 14, 400, MUTED)
    svg.footer("ロッドがある分、引き側の面積と力は小さくなる。値は理論値",
               "The rod reduces the retraction area and force; the values are theoretical")
    return svg


def d07_10() -> Svg:
    svg = new_diagram("D07-10", "電動アクチュエータのエネルギーの流れ", "Electric actuator energy flow",
                      "第7日 / Day 7", 800)
    chain(svg, [
        ("電源", "electrical supply", "AC/DC / AC or DC", ENERGY),
        ("ドライバ", "driver", "指令を作る / produces the command", CONTROL),
        ("モーター", "motor", "回転を作る / produces rotation", MECH),
        ("伝達機構", "transmission", "ねじ・ベルト・ギヤ / screw, belt, gear", MECH),
        ("負荷", "load", "ワークを動かす / moves the workpiece", DATA),
    ], y=200, h=150)
    panel(svg, 70, 420, 1300, 220, "制御とフィードバックはシステム全体で決まる", "control and feedback are system-level properties")
    svg.text(90, 510, "・モーター単体では位置決めの可否は決まらない / a motor alone does not decide positioning capability", 15, 400, INK)
    svg.text(90, 545, "・エンコーダ付きステッピングもある / stepping systems can include an encoder", 15, 400, INK)
    svg.text(90, 580, "・サーボが常に最適とは限らない / a servo is not always the best answer", 15, 400, INK)
    note(svg, 660, "用途・精度・速度・コストで選ぶ。動力とアクチュエータは別の概念。",
         "Choose by application, accuracy, speed and cost. Power source and actuator differ.")
    svg.footer("電気の供給からドライバ、モーター、伝達機構、負荷までの流れ",
               "From the electrical supply through driver, motor and transmission to the load")
    return svg


def d07_11() -> Svg:
    svg = new_diagram("D07-11", "動きの種類とハンドリング", "Motion types and handling",
                      "第7日 / Day 7", 860)
    cards = [
        ("直線運動", "linear motion", "シリンダ・電動リニア / cylinder, electric linear", MECH),
        ("回転運動", "rotary motion", "モーター・ロータリアクチュエータ / motor, rotary actuator", MECH),
        ("把持", "gripping", "エア・電動グリッパ / air or electric gripper", SENSOR),
        ("真空吸着", "vacuum holding", "圧力差で保持 / holds by pressure difference", DATA),
    ]
    for index, (ja, en, sub, color) in enumerate(cards):
        x = 70 + index * 335
        svg.card(x, 190, 310, 200, ja, en, stroke=color, accent=color, sub=sub)
    panel(svg, 70, 440, 620, 250, "真空吸着の条件", "vacuum holding conditions")
    svg.text(90, 530, "保持力は次で変わる / holding force depends on", 16, 700, INK)
    for index, text in enumerate(["パッド面積 / cup area", "圧力差 / pressure difference",
                                  "表面状態 / surface condition", "ワーク重量と加速度 / weight and acceleration"]):
        svg.text(90, 570 + index * 30, f"・{text}", 14, 400, INK)
    panel(svg, 750, 440, 620, 250, "向かない面", "unsuitable surfaces")
    for index, text in enumerate(["ざらつきが大きい / very rough", "通気性がある / porous",
                                  "反り・しわが大きい / warped or wrinkled", "油分が多い / oily"]):
        svg.text(770, 530 + index * 40, f"・{text}", 15, 400, INK)
    note(svg, 720, "真空はすべての面に向くわけではない。表面と加速度で決まる。",
         "Vacuum is not suitable for every surface; the surface and acceleration decide.")
    svg.footer("直線・回転・把持・真空の使い分けと、真空保持の条件",
               "Choosing linear, rotary, gripping or vacuum handling, and the conditions for vacuum holding")
    return svg


def d07_12() -> Svg:
    svg = new_diagram("D07-12", "モーターの使い分け", "Choosing between motor types",
                      "第7日 / Day 7", 900)
    columns = [
        ("AC誘導モーター", "AC induction motor", GOOD,
         ["連続回転 / continuous rotation", "インバータで速度可変", "位置決めは苦手",
          "例: コンベヤ搬送", "利点: 丈夫・安価", "制約: 停止精度"]),
        ("サーボモーター", "servo motor", MECH,
         ["高精度の位置・速度", "エンコーダでフィードバック", "アンプで調整が必要",
          "例: 精密位置決め", "利点: 追従性", "制約: コスト・調整"]),
        ("ステッピングモーター", "stepping motor", CONTROL,
         ["決めた角度ずつ回転", "パルス数で角度", "脱調に注意",
          "例: 軽い位置決め", "利点: 安価で簡単", "制約: 発熱・脱調"]),
    ]
    for index, (ja, en, color, rows) in enumerate(columns):
        x = 70 + index * 440
        svg.rect(x, 180, 400, 600, fill=CARD, stroke=color, sw=2, rx=12)
        svg.text(x + 200, 220, ja, 21, 700, color, "middle")
        svg.text(x + 200, 248, en, 14, 400, MUTED, "middle")
        for row_index, text in enumerate(rows):
            svg.text(x + 24, 305 + row_index * 70, text, 15, 400, INK)
    note(svg, 810, "制御方式とフィードバックはシステム全体で決まる。型で決めつけない。",
         "Control method and feedback are system properties; do not decide from the type name alone.")
    svg.footer("AC誘導・サーボ・ステッピングの比較と、製造業での使い分け",
               "AC induction, servo and stepping motors compared for manufacturing applications")
    return svg


def d07_13() -> Svg:
    svg = new_diagram("D07-13", "仕様の意味", "What the selection specifications mean",
                      "第7日 / Day 7", 940)
    panel(svg, 70, 180, 620, 240, "荷重と質量", "load and mass")
    svg.rect(110, 250, 150, 70, fill="#D9C7A8", stroke="#8A6A3A", sw=2, rx=4)
    svg.text(185, 292, "8 kg", 20, 700, INK, "middle")
    svg.line(160, 350, 160, 400, stroke=BAD, sw=3)
    svg.text(185, 385, "F = 8 × 9.81 = 78.5 N", 16, 700, BAD)
    svg.text(110, 420, "質量kgと力Nは別の量 / mass in kg and force in N differ", 13, 400, MUTED)

    panel(svg, 750, 180, 620, 240, "ストロークと速度", "stroke and speed")
    svg.line(790, 320, 1290, 320, stroke=MECH, sw=3)
    svg.line(790, 305, 790, 335, stroke=MECH, sw=3)
    svg.line(1290, 305, 1290, 335, stroke=MECH, sw=3)
    svg.text(1040, 300, "100 mm", 18, 700, MECH, "middle")
    svg.text(1040, 370, "200 mm/s（平均） / average", 16, 400, INK, "middle")

    panel(svg, 70, 460, 620, 250, "推力とトルク", "thrust and torque")
    svg.line(110, 580, 300, 580, stroke=MECH, sw=4)
    svg.text(150, 610, "推力 F [N]", 16, 700, MECH)
    svg.circle(430, 580, 60, fill=CARD, stroke=CONTROL, sw=3)
    svg.line(430, 580, 500, 550, stroke=CONTROL, sw=3)
    svg.text(455, 660, "T = r × F [N·m]", 16, 700, CONTROL)

    panel(svg, 750, 460, 620, 250, "偏荷重", "offset load")
    svg.rect(800, 520, 60, 120, fill=FILL_MECH, stroke=MECH, sw=2, rx=4)
    svg.line(860, 530, 1090, 530, stroke=MECH, sw=3)
    svg.line(1090, 530, 1090, 610, stroke=BAD, sw=3)
    svg.text(840, 660, "距離 × 力 がモーメント / distance × force is a moment", 14, 700, BAD)
    svg.text(880, 500, "L [mm]", 15, 400, MUTED)

    note(svg, 750, "位置決め精度は目標との差、繰返し精度は同じ指令でのばらつき。",
         "Positioning accuracy is the error to the target; repeatability is the spread for one command.")
    svg.footer("荷重・質量・ストローク・速度・推力・トルク・偏荷重の意味",
               "Meaning of load, mass, stroke, speed, thrust, torque and offset load")
    return svg


def d07_14() -> Svg:
    svg = new_diagram("D07-14", "選定の進め方", "Selection workflow",
                      "第7日 / Day 7", 820)
    chain(svg, [
        ("要求の整理", "gather requirements", "力・ストローク・速度 / force, stroke, speed", MECH),
        ("方式の候補", "candidate technologies", "空圧・電動など / pneumatic or electric", ENERGY),
        ("計算", "calculation", "推力・トルク / thrust, torque", DATA),
        ("カタログ確認", "catalogue check", "負荷率・偏荷重 / load ratio, offset load", CONTROL),
        ("実機確認", "real-machine check", "安全・取付・環境 / safety, mounting, environment", SENSOR),
    ], y=190, h=150)
    panel(svg, 70, 430, 1300, 190, "カタログの前に決めること", "decide before opening the catalogue")
    svg.text(90, 520, "何を動かすか / どの方向か / どのくらいの力か / 何秒で動かすか / どこに止めるか",
             16, 400, INK)
    svg.text(90, 555, "what moves, in which direction, with what force, in what time, to which position",
             14, 400, MUTED)
    svg.text(90, 600, "周囲の環境 / 保守性 / 停止時の動き / 予算", 16, 400, INK)
    svg.text(90, 630, "environment, maintainability, behaviour at stop, budget", 14, 400, MUTED)
    note(svg, 660, "計算は候補を絞る道具。最終選定ではない。",
         "Calculation narrows candidates; it is not the final selection.")
    svg.footer("要求 → 候補 → 計算 → カタログ → 実機確認の順に進める",
               "Proceed in the order: requirements, candidates, calculation, catalogue, real-machine check")
    return svg


DAY7 = [d07_01, d07_02, d07_03, d07_04, d07_05, d07_06, d07_07,
        d07_08, d07_09, d07_10, d07_11, d07_12, d07_13, d07_14]


# --------------------------------------------------------------------------- #
# Day 8
# --------------------------------------------------------------------------- #
def d08_01() -> Svg:
    svg = new_diagram("D08-01", "電圧・電流・抵抗の関係", "Voltage, current and resistance",
                      "第8日 / Day 8", 900)
    panel(svg, 70, 180, 620, 340, "水道のたとえ", "the water analogy")
    svg.rect(110, 250, 120, 90, fill=FILL_DATA, stroke=DATA, sw=2, rx=6)
    svg.text(170, 300, "水", 18, 700, INK, "middle")
    svg.text(110, 375, "水圧 / pressure", 15, 400, MUTED)
    svg.rect(300, 285, 240, 20, fill="#D7E7F5", stroke=DATA, sw=1.6)
    svg.text(420, 340, "流量 / flow", 15, 400, MUTED)
    svg.rect(540, 265, 40, 60, fill="#CBD5DF", stroke=MUTED, sw=1.6, rx=3)
    svg.text(500, 360, "細い管 / restriction", 14, 400, MUTED)
    svg.line(230, 295, 296, 295, stroke=DATA, sw=2.4)
    svg.text(110, 470, "抵抗 = 流れにくさ / resistance is restriction", 14, 400, MUTED)

    panel(svg, 750, 180, 620, 340, "電気の言葉", "the electrical quantities")
    rows = [
        ("電圧 / voltage", "V（ボルト）", "押し出す力 / push"),
        ("電流 / current", "A（アンペア）", "流れる量 / flow"),
        ("抵抗 / resistance", "Ω（オーム）", "流れにくさ / restriction"),
        ("電力 / power", "W（ワット）", "1秒あたり / per second"),
    ]
    for index, (name, unit, meaning) in enumerate(rows):
        top = 260 + index * 60
        svg.text(780, top, name, 16, 700, INK)
        svg.text(1010, top, unit, 15, 600, ACCENT)
        svg.text(1150, top, meaning, 12, 400, MUTED)

    panel(svg, 70, 560, 1300, 200, "たとえの限界", "limits of the analogy")
    svg.text(90, 650, "交流・電磁誘導・静電気・電子の動きの向きは、水では正しく表せない。",
             16, 400, INK)
    svg.text(90, 680, "AC, electromagnetic induction, static charge and electron motion are not represented by water.",
             14, 400, MUTED)
    svg.text(90, 720, "たとえは入口。細かい話は電気の言葉で考える。 / The analogy is an entry point; think electrically afterwards.",
             15, 400, INK)
    svg.footer("電圧は水圧、電流は流量、抵抗は流れにくさ。電力は1秒あたりのエネルギー",
               "Voltage is pressure, current is flow, resistance is restriction, power is energy per second")
    return svg


def d08_02() -> Svg:
    svg = new_diagram("D08-02", "電圧の使い分けと電力の流れ", "Voltage applications and power distribution",
                      "第8日 / Day 8", 900)
    panel(svg, 70, 170, 1300, 190, "AC電源と動力回路", "AC supply and the power circuit")
    chain(svg, [("AC電源", "AC supply", "100V / 200V", ENERGY),
                ("保護", "protection", "遮断器・漏電 / breaker, earth leakage", HAZARD),
                ("動力回路", "power circuit", "モーター・ドライブ / motor, drive", MECH)],
          y=210, h=120, x0=90, x1=1350, gap=90)

    panel(svg, 70, 390, 1300, 190, "ACからDC24Vへ", "AC to DC24V")
    chain(svg, [("AC電源", "AC supply", "100V / 200V", ENERGY),
                ("スイッチング電源", "switching power supply", "AC → 安定したDC / regulated DC", CONTROL),
                ("DC24V分配", "DC24V distribution", "PLC・センサー・リレー・電磁弁", DATA)],
          y=430, h=120, x0=90, x1=1350, gap=90)

    panel(svg, 70, 610, 1300, 190, "DC24Vから12V・5Vへ", "DC24V to 12V and 5V")
    chain(svg, [("DC24V", "DC24V", "制御用 / control", DATA),
                ("DC/DCコンバータ", "DC/DC converter", "定格内で変換 / within ratings", CONTROL),
                ("12V・5V機器", "12V and 5V devices", "カメラ・マイコン / camera, microcontroller", SENSOR)],
          y=650, h=120, x0=90, x1=1350, gap=90)
    note(svg, 820, "承認済みの施工図ではない。電圧の値だけで制御用・動力用は決まらない。",
         "Not an approved installation drawing. Voltage alone does not define control or power circuits.")
    svg.footer("AC100/200Vは動力と機器電源、DC24Vは制御と負荷、12V/5Vは対応機器",
               "AC100/200V for power and equipment supplies, DC24V for control and loads, 12V/5V for compatible devices")
    return svg


def d08_03() -> Svg:
    svg = new_diagram("D08-03", "制御盤の機器", "Control panel components",
                      "第8日 / Day 8", 1060)
    components = [
        ("配線用遮断器", "circuit breaker", "過電流保護 / overcurrent"),
        ("漏電遮断器", "earth-leakage device", "漏れ電流 / leakage"),
        ("ヒューズ", "fuse", "規定特性で溶断 / opens on overcurrent"),
        ("スイッチング電源", "switching power supply", "AC → DC"),
        ("DC/DCコンバータ", "DC/DC converter", "DC → DC"),
        ("リレー", "relay", "信号で接点 / switches contacts"),
        ("電磁接触器", "contactor", "動力負荷 / power loads"),
        ("サーマルリレー", "overload relay", "モーター保護 / motor overload"),
        ("端子台", "terminal block", "接続点 / connection points"),
        ("押しボタン", "pushbutton", "作業者の指令 / operator input"),
        ("表示灯", "indicator lamp", "状態表示 / state display"),
        ("非常停止", "emergency stop", "人の危険の停止 / stops for danger"),
        ("PLC", "programmable controller", "入力→判断→出力 / input, decide, output"),
        ("インバータ", "inverter", "速度可変 / variable speed"),
        ("サーボアンプ", "servo amplifier", "フィードバック制御 / closed loop"),
        ("保護・接地", "protection and earthing", "感電・ノイズ / shock, noise"),
    ]
    card_w = (1300 - 60 - 3 * 20) / 4
    for index, (ja, en, sub) in enumerate(components):
        row, col = divmod(index, 4)
        x = 70 + col * (card_w + 20)
        y = 180 + row * 190
        svg.card(x, y, card_w, 165, ja, en, stroke=MECH if col % 2 == 0 else CONTROL,
                 accent=MECH if col % 2 == 0 else CONTROL, sub=sub)
    note(svg, 960, "形・色・端子配置は機種で違う。公式カタログとマニュアルで確認する。",
         "Shape, colour and terminal layout differ by model; check the official catalogue and manual.")
    svg.footer("盤の主要機器の位置と役割。模式的な形であり実機の外観ではない",
               "Position and role of the main panel devices; schematic shapes, not real appearance")
    return svg


def d08_04() -> Svg:
    svg = new_diagram("D08-04", "保護機器の違い", "What each protective device covers",
                      "第8日 / Day 8", 880)
    panels = [
        ("配線用遮断器", "circuit breaker", MECH,
         ["守る: 定格内の過電流、配線", "protects: overcurrent within ratings, wiring"],
         ["守らない: すべての故障", "does not: every fault"]),
        ("漏電遮断器", "earth-leakage device", HAZARD,
         ["守る: 設計に応じた漏れ電流", "protects: specified leakage current"],
         ["守らない: 過電流一般", "does not: general overcurrent"]),
        ("ヒューズ", "fuse", ENERGY,
         ["守る: 規定の過電流特性", "protects: specified overcurrent characteristic"],
         ["注意: 溶断後は交換", "note: replaced after operation"]),
        ("サーマルリレー", "overload relay", CONTROL,
         ["守る: モーターなどの過負荷", "protects: overload, commonly motors"],
         ["守らない: 短絡保護", "does not: short-circuit protection"]),
    ]
    for index, (ja, en, color, good, bad) in enumerate(panels):
        x = 70 + index * 335
        svg.rect(x, 180, 305, 440, fill=CARD, stroke=color, sw=2, rx=12)
        svg.text(x + 152, 225, ja, 19, 700, color, "middle")
        svg.text(x + 152, 250, en, 13, 400, MUTED, "middle")
        svg.rect(x + 20, 280, 265, 130, fill=FILL_SENSOR, stroke=GOOD, sw=1.4, rx=8)
        svg.text(x + 30, 320, good[0], 14, 700, INK)
        svg.text(x + 30, 350, good[1], 12, 400, MUTED)
        svg.rect(x + 20, 430, 265, 130, fill=FILL_HAZARD, stroke=BAD, sw=1.4, rx=8)
        svg.text(x + 30, 470, bad[0], 14, 700, INK)
        svg.text(x + 30, 500, bad[1], 12, 400, MUTED)
    note(svg, 650, "守る範囲は、定格と特性の範囲内。組み合わせで初めて系統を保護する。",
         "Each device protects within its ratings and characteristics; the combination protects the system.")
    svg.footer("遮断器・漏電遮断器・ヒューズ・サーマルリレーの守る範囲の違い",
               "Differences in the coverage of breaker, earth-leakage device, fuse and overload relay")
    return svg


def d08_05() -> Svg:
    svg = new_diagram("D08-05", "スイッチング電源・DC/DC・リレーと接触器", "Switching power supply, DC/DC converter, relay and contactor",
                      "第8日 / Day 8", 860)
    panel(svg, 70, 180, 620, 300, "スイッチング電源", "switching power supply")
    svg.rect(110, 260, 120, 90, fill=FILL_ENERGY, stroke=ENERGY, sw=2, rx=6)
    svg.text(170, 300, "AC入力", 15, 700, INK, "middle")
    svg.text(170, 325, "AC input", 12, 400, MUTED, "middle")
    svg.line(232, 305, 330, 305, stroke=ENERGY, sw=2.4)
    svg.rect(334, 260, 150, 90, fill=FILL_CONTROL, stroke=CONTROL, sw=2, rx=6)
    svg.text(409, 295, "変換", 16, 700, INK, "middle")
    svg.text(409, 320, "conversion", 12, 400, MUTED, "middle")
    svg.line(486, 305, 560, 305, stroke=CONTROL, sw=2.4)
    svg.rect(564, 260, 100, 90, fill=FILL_DATA, stroke=DATA, sw=2, rx=6)
    svg.text(614, 295, "DC出力", 15, 700, INK, "middle")
    svg.text(614, 320, "DC output", 12, 400, MUTED, "middle")
    svg.text(110, 400, "入力電圧・出力電圧・出力電流・定格出力を確認", 14, 400, INK)
    svg.text(110, 430, "check input, output voltage and current, rated power", 12, 400, MUTED)

    panel(svg, 750, 180, 620, 300, "DC/DCコンバータ", "DC/DC converter")
    svg.rect(790, 260, 120, 90, fill=FILL_DATA, stroke=DATA, sw=2, rx=6)
    svg.text(850, 300, "DC24V", 15, 700, INK, "middle")
    svg.line(912, 305, 1010, 305, stroke=DATA, sw=2.4)
    svg.rect(1014, 260, 160, 90, fill=FILL_CONTROL, stroke=CONTROL, sw=2, rx=6)
    svg.text(1094, 295, "変換", 16, 700, INK, "middle")
    svg.text(1094, 320, "conversion", 12, 400, MUTED, "middle")
    svg.line(1176, 305, 1250, 305, stroke=CONTROL, sw=2.4)
    svg.rect(1254, 260, 90, 90, fill=FILL_SENSOR, stroke=SENSOR, sw=2, rx=6)
    svg.text(1299, 295, "12V/5V", 14, 700, INK, "middle")
    svg.text(790, 400, "入力範囲・出力・効率を確認", 14, 400, INK)
    svg.text(790, 430, "check input range, output and efficiency", 12, 400, MUTED)

    panel(svg, 70, 510, 620, 240, "リレー", "relay")
    svg.text(90, 600, "制御入力で接点を切り替える", 16, 700, INK)
    svg.text(90, 628, "a control input switches contacts", 13, 400, MUTED)
    svg.text(90, 675, "コイル電圧と接点容量を確認", 15, 400, INK)
    svg.text(90, 700, "check coil voltage and contact rating", 12, 400, MUTED)

    panel(svg, 750, 510, 620, 240, "電磁接触器", "contactor")
    svg.text(770, 600, "定格の大きい動力負荷を開閉する", 16, 700, INK)
    svg.text(770, 628, "switches appropriately rated power loads", 13, 400, MUTED)
    svg.text(770, 675, "定格電流と使用カテゴリを確認", 15, 400, INK)
    svg.text(770, 700, "check rated current and utilisation category", 12, 400, MUTED)
    svg.footer("AC→DCの変換、DC→DCの変換、信号用リレーと動力用接触器の違い",
               "AC-to-DC conversion, DC-to-DC conversion, and signal relay versus power contactor")
    return svg


def d08_06() -> Svg:
    svg = new_diagram("D08-06", "入力から出力までの信号の流れ", "Signal flow from input to output",
                      "第8日 / Day 8", 900)
    chain(svg, [("物理的な出来事", "physical event", "製品が来る / a product arrives", MECH),
                ("センサー", "sensor", "状態を電気に / state to a signal", SENSOR),
                ("PLC入力", "PLC input", "信号を受け取る / receives the signal", CONTROL),
                ("プログラム", "program", "条件を判断 / evaluates conditions", CONTROL)],
          y=190, h=140, x0=80, x1=1360)
    chain(svg, [("PLC出力", "PLC output", "指令を出す / issues a command", CONTROL),
                ("ドライバ・弁", "driver or valve", "負荷を動かす / drives the load", ENERGY),
                ("アクチュエータ", "actuator", "実際に動く / moves", MECH),
                ("物理的な動き", "physical movement", "結果 / the result", MECH)],
          y=400, h=140, x0=80, x1=1360)
    svg.line(1300, 340, 1300, 396, stroke=ACCENT, sw=2.4)
    svg.line(1250, 545, 1250, 640, stroke=SENSOR, sw=2.4, dash="7 5")
    svg.line(1250, 640, 330, 640, stroke=SENSOR, sw=2.4, dash="7 5")
    svg.line(330, 640, 330, 340, stroke=SENSOR, sw=2.4, dash="7 5")
    svg.text(400, 630, "位置センサーが結果を入力へ戻す（フィードバック） / a position sensor feeds the result back", 14, 600, SENSOR)
    note(svg, 690, "指令を出しても、動いたことにはならない。確認入力を待つ。",
         "A command does not prove motion; wait for the confirmation input.")
    svg.footer("物理 → センサー → 入力 → プログラム → 出力 → ドライバ → 動作 → フィードバック",
               "Physical event, sensor, input, program, output, driver, motion, feedback")
    return svg


def d08_07() -> Svg:
    svg = new_diagram("D08-07", "センサーの種類と原理", "Sensor types and detection principles",
                      "第8日 / Day 8", 1040)
    sensors = [
        ("透過型光電", "through-beam", "光を遮る / blocks the beam", "不透明物・通過 / opaque, passage", MECH),
        ("再帰反射型", "retroreflective", "反射板の光を遮る / blocks the return", "比較的大きな物 / larger objects", MECH),
        ("拡散反射型", "diffuse-reflective", "対象の反射光 / light from the target", "近距離の有無 / presence nearby", DATA),
        ("誘導型近接", "inductive proximity", "金属の影響 / responds to metal", "金属部品 / metal parts", ENERGY),
        ("静電容量型", "capacitive proximity", "容量変化 / capacitance change", "樹脂・液体 / plastic, liquid", CONTROL),
        ("磁気シリンダ", "magnetic cylinder", "ピストンの磁石 / piston magnet", "ストローク端 / end positions", SENSOR),
        ("リミットスイッチ", "limit switch", "機械的接触 / mechanical contact", "端の確認 / end confirmation", MECH),
        ("超音波", "ultrasonic", "音波の反射 / sound reflection", "距離・液面 / distance, level", DATA),
        ("圧力センサー", "pressure sensor", "圧力を信号に / pressure to a signal", "空気・油の圧力 / air or oil", ENERGY),
        ("エンコーダ", "encoder", "回転をパルスに / rotation to pulses", "回転量・速度 / rotation, speed", CONTROL),
        ("カメラ", "camera", "画像から特徴 / features from an image", "外観検査 / appearance", SENSOR),
    ]
    card_w = (1300 - 40 - 3 * 20) / 4
    for index, (ja, en, principle, use, color) in enumerate(sensors):
        row, col = divmod(index, 4)
        x = 70 + col * (card_w + 20)
        y = 180 + row * 210
        svg.card(x, y, card_w, 180, ja, en, stroke=color, accent=color, sub=f"{principle} / {use}")
    note(svg, 880, "反射型が透明体・黒色を必ず検出するわけではない。実対象で試験する。",
         "Reflective sensors do not reliably detect every clear or black target; test the actual target.")
    svg.footer("代表的なセンサーの検出原理と用途。制約は材質・色・距離で変わる",
               "Detection principles and applications; limitations depend on material, colour and distance")
    return svg


def d08_08() -> Svg:
    svg = new_diagram("D08-08", "センサー選定の手順", "Sensor selection workflow",
                      "第8日 / Day 8", 1000)
    steps = [
        ("何を検出するか", "what to detect"),
        ("対象の材質・色", "material and colour"),
        ("必要な検出距離", "required distance"),
        ("対象の速さ", "target speed"),
        ("必要な応答時間", "response time"),
        ("環境（粉じん・水・油）", "environment"),
        ("デジタルかアナログか", "digital or analog"),
        ("必要な電源電圧", "supply voltage"),
        ("出力インターフェース", "output interface"),
        ("PLC入力との整合", "PLC input compatibility"),
    ]
    for index, (ja, en) in enumerate(steps):
        col = index // 5
        row = index % 5
        x = 80 + col * 660
        y = 190 + row * 140
        svg.circle(x + 40, y + 45, 26, fill=JP_BG, stroke=ACCENT, sw=2)
        svg.text(x + 40, y + 53, str(index + 1), 20, 700, ACCENT, "middle")
        label_box(svg, x + 80, y, 540, 90, ja, en, size=15)
        if row < 4:
            svg.line(x + 40, y + 75, x + 40, y + 130, stroke=ACCENT, sw=2)
    svg.line(620, 470, 740, 470, stroke=ACCENT, sw=2.4)
    svg.line(740, 470, 740, 235, stroke=ACCENT, sw=2.4)
    panel(svg, 80, 900, 1300, 90, "信号の種類", "signal types")
    svg.text(100, 975, "ON/OFF・アナログ（0–10V、4–20mA）・パルス・通信 / ON/OFF, analog, pulse, communication",
             15, 400, INK)
    svg.footer("対象 → 距離 → 速さ → 環境 → 信号 → PLC入力の順に整理する",
               "Work through target, distance, speed, environment, signal and PLC input")
    return svg


def d08_09() -> Svg:
    svg = new_diagram("D08-09", "PNP・NPNとPLC入力の電流経路", "PNP and NPN current paths through PLC inputs",
                      "第8日 / Day 8", 980)
    panel(svg, 70, 170, 620, 380, "PNP：+側から電流を出す", "PNP sources current from +24V")
    svg.line(100, 260, 660, 260, stroke=ENERGY, sw=3)
    svg.text(100, 245, "+24V", 16, 700, ENERGY)
    svg.line(100, 500, 660, 500, stroke=MUTED, sw=3)
    svg.text(100, 525, "0V（入力共通）/ input common", 15, 700, MUTED)
    svg.rect(190, 300, 150, 90, fill=FILL_SENSOR, stroke=SENSOR, sw=2, rx=6)
    svg.text(265, 335, "PNPセンサー", 16, 700, INK, "middle")
    svg.text(265, 360, "PNP sensor", 13, 400, MUTED, "middle")
    svg.line(265, 262, 265, 298, stroke=ENERGY, sw=2.4)
    svg.rect(420, 300, 150, 90, fill=FILL_CONTROL, stroke=CONTROL, sw=2, rx=6)
    svg.text(495, 335, "PLC入力", 16, 700, INK, "middle")
    svg.text(495, 360, "PLC input", 13, 400, MUTED, "middle")
    svg.line(342, 345, 418, 345, stroke=BAD, sw=2.8)
    svg.line(495, 392, 495, 498, stroke=BAD, sw=2.8)
    svg.text(348, 330, "出力", 12, 700, BAD)
    svg.text(348, 346, "output", 10, 400, BAD)
    svg.text(505, 450, "電流 / current", 13, 700, BAD)

    panel(svg, 750, 170, 620, 380, "NPN：0Vへ電流を引き込む", "NPN sinks current toward 0V")
    svg.line(780, 260, 1340, 260, stroke=ENERGY, sw=3)
    svg.text(780, 245, "+24V（入力共通）/ input common", 15, 700, ENERGY)
    svg.line(780, 500, 1340, 500, stroke=MUTED, sw=3)
    svg.text(780, 525, "0V", 16, 700, MUTED)
    svg.rect(1100, 300, 150, 90, fill=FILL_SENSOR, stroke=SENSOR, sw=2, rx=6)
    svg.text(1175, 335, "NPNセンサー", 16, 700, INK, "middle")
    svg.text(1175, 360, "NPN sensor", 13, 400, MUTED, "middle")
    svg.line(1175, 392, 1175, 498, stroke=BAD, sw=2.8)
    svg.rect(870, 300, 150, 90, fill=FILL_CONTROL, stroke=CONTROL, sw=2, rx=6)
    svg.text(945, 335, "PLC入力", 16, 700, INK, "middle")
    svg.text(945, 360, "PLC input", 13, 400, MUTED, "middle")
    svg.line(945, 262, 945, 298, stroke=ENERGY, sw=2.4)
    svg.line(1022, 345, 1098, 345, stroke=BAD, sw=2.8)
    svg.text(1185, 450, "電流 / current", 13, 700, BAD)

    table_grid(svg, 70, 590, ["センサー / sensor", "動作時 / when active", "入力共通 / input common", "電流 / current"],
               [["PNP", "+から出す / sources", "0V（シンク入力）", "+24V → センサー → PLC → 0V"],
                ["NPN", "0Vへ引く / sinks", "+24V（ソース入力）", "+24V → PLC → センサー → 0V"]],
               [180, 300, 300, 520], row_h=52, size=15)
    note(svg, 760, "NPN/PNPは出力インターフェース。検出原理ではない。配線色は例でありデータシートに従う。",
         "NPN/PNP describe the output interface, not the detection principle. Wire colours are examples; follow the datasheet.")
    svg.footer("PNPは共通0Vの入力へ、NPNは共通+24Vの入力へ。電流の向きで理解する",
               "PNP pairs with a 0V-common input; NPN with a +24V-common input. Understand it by current direction")
    return svg


def d08_10() -> Svg:
    svg = new_diagram("D08-10", "ラダーの基本と物理接点・論理接点", "Ladder basics, and physical versus logical contacts",
                      "第8日 / Day 8", 1000)
    panel(svg, 70, 170, 1300, 300, "AND・OR・NOT", "AND, OR and NOT")
    ladder_row(svg, 260, [("contact", False, "A", None), ("contact", False, "B", None),
                          ("coil", "Y", "Y = A AND B")], start_x=230, step=150)
    ladder_row(svg, 350, [("contact", False, "A", None), ("coil", "Y", "Y = A OR B")], start_x=230, step=150)
    ladder_row(svg, 440, [("contact", True, "A", None), ("coil", "Y", "Y = NOT A")], start_x=230, step=150)
    svg.text(700, 350, "並列はOR。直列はAND。NC接点は否定。", 15, 400, MUTED)
    svg.text(700, 375, "series is AND; parallel is OR; an NC contact negates", 13, 400, MUTED)

    panel(svg, 70, 500, 620, 300, "物理接点", "physical contact")
    svg.text(90, 590, "物理NCのSTOPを、健全時にPLC入力ONとなるように配線する。", 15, 400, INK)
    svg.text(90, 618, "Wire a physical NC stop so the PLC input is ON while healthy.", 13, 400, MUTED)
    svg.text(90, 670, "プログラムでは「ONで許可」として使う。", 15, 400, INK)
    svg.text(90, 698, "In the program the state is used as an ON permission.", 13, 400, MUTED)
    svg.text(90, 750, "断線したときにONかOFFかを設計者が理解する。", 15, 700, WARN)
    svg.text(90, 775, "Know whether a broken wire produces ON or OFF.", 12, 400, MUTED)

    panel(svg, 750, 500, 620, 300, "論理接点とタイマー", "logical contact and timer")
    ladder_row(svg, 600, [("contact", False, "M0", None), ("contact", False, "T0", None),
                          ("coil", "Y1", "on-delay")], start_x=880, step=150)
    svg.text(770, 700, "T0はM0がONの間だけ時間を数える。", 15, 400, INK)
    svg.text(770, 728, "T0 counts only while M0 is ON.", 13, 400, MUTED)
    svg.text(770, 770, "図の接点は論理状態の評価であり、実接点や実電流ではない。", 14, 700, INK)
    note(svg, 840, "物理的にNCのスイッチを、必ずNC論理接点で使う規則はない。",
         "There is no rule that a physically NC switch must use an NC logical instruction.")
    svg.footer("NO/NC接点・コイル・AND/OR/NOT・物理接点と論理接点・オンディレイタイマー",
               "NO/NC contacts, coils, AND/OR/NOT, physical versus logical contacts, on-delay timer")
    return svg


def d08_11() -> Svg:
    svg = new_diagram("D08-11", "基本の自己保持回路", "The basic self-holding circuit",
                      "第8日 / Day 8", 900)
    panel(svg, 70, 170, 1300, 330, "基本の自己保持（教材用）", "basic self-holding (teaching example)")
    ladder_row(svg, 300, [("contact", False, "X1", "STOP_OK"), ("contact", False, "X0", "START"),
                          ("coil", "M0", "RUN")], start_x=230, step=170)
    svg.line(430, 300, 430, 380, stroke=ACCENT, sw=2.4)
    svg.line(430, 380, 520, 380, stroke=ACCENT, sw=2.4)
    svg.line(520, 380, 520, 330, stroke=ACCENT, sw=2.4)
    svg.line(490, 380, 550, 380, stroke=ACCENT, sw=2.4)
    svg.text(470, 415, "M0の保持枝 / the M0 holding branch", 14, 700, ACCENT)
    ladder_row(svg, 470, [("contact", False, "M0", None), ("coil", "Y0", "RUN lamp")],
               start_x=230, step=170)

    panel(svg, 70, 530, 1300, 290, "5つの場面", "five situations")
    situations = [
        "1. STARTを離す → RUNが続く（保持）/ release START: RUN stays on",
        "2. STARTを押す → RUNになる / press START: RUN turns on",
        "3. 押してから離す → RUNのまま / press then release: still RUN",
        "4. STOP許可がOFF → RUNがOFF / permission OFF: RUN off",
        "5. STOP許可が戻る → STARTを押しっぱなしだとRUNが戻る / permission restored: RUN returns while START is held",
    ]
    for index, text in enumerate(situations):
        color = BAD if index == 4 else INK
        svg.text(90, 600 + index * 40, text, 15, 700 if index == 4 else 400, color)
    note(svg, 850, "基本回路は「記憶」の説明用。再起動防止の機能はない。",
         "The basic circuit explains memory; it has no restart prevention.")
    svg.footer("自己保持は並列のM0接点による。5番目の場面が拡張ロジックの出発点",
               "Self-holding comes from the parallel M0 contact; situation 5 motivates the extended logic")
    return svg


def d08_12() -> Svg:
    svg = new_diagram("D08-12", "再起動防止を含む拡張ロジック", "Extended logic with restart prevention",
                      "第8日 / Day 8", 1290)
    panel(svg, 70, 170, 1300, 620, "汎用的な概念ラダー（機種固有ではない）", "generic conceptual ladder (not model-specific)")
    ladder_row(svg, 300, [("contact", True, "X0", None), ("contact", False, "X1", None),
                          ("contact", False, "X2", None), ("contact", True, "X3", None),
                          ("coil", "M1", "armed")], start_x=200, step=125)
    svg.text(90, 250, "N1 STARTが離れているときだけアーム / arm only while START is released", 13, 400, MUTED)
    ladder_row(svg, 450, [("contact", False, "X0", None), ("contact", False, "M1", None),
                          ("contact", False, "P", "edge"), ("contact", False, "X1", None),
                          ("coil", "M2", "accept")], start_x=200, step=125)
    svg.text(90, 372, "N2 新しい立ち上がりだけで起動を受け付ける / accept only a new rising edge", 13, 400, MUTED)
    ladder_row(svg, 600, [("contact", False, "X1", None), ("contact", True, "FAULT", None),
                          ("contact", False, "M2", None), ("coil", "M0", "RUN")], start_x=200, step=125)
    svg.text(90, 522, "N3 STOP許可とFAULTで解除。M0は自己保持 / STOP and FAULT clear it; M0 seals in", 13, 400, MUTED)
    ladder_row(svg, 730, [("contact", False, "RESET", None), ("contact", True, "X0", None),
                          ("contact", False, "X1", None), ("coil", "RST", "FAULT")], start_x=200, step=125)
    svg.text(90, 674, "N4 リセットはSTARTを離しているときだけ。運転は開始しない / reset only with START released; it never starts", 13, 400, MUTED)

    panel(svg, 70, 820, 620, 240, "必要条件", "requirements")
    for index, text in enumerate(["起動時RUN=OFF / RUN is OFF at power-up",
                                  "保持されたSTARTでは起動しない / a held START does not start",
                                  "STOPはSTARTより優先 / STOP precedes START",
                                  "リセットは運転開始ではない / reset is not a start"]):
        svg.text(90, 900 + index * 34, f"・{text}", 14, 400, INK)
    panel(svg, 750, 820, 620, 240, "確認", "checks")
    for index, text in enumerate(["STARTを離して押し直すまで動かない / no motion until START is released and pressed",
                                  "許可が戻っても自動で動かない / restoring a permissive does not restart",
                                  "異常復帰でも自動で動かない / fault recovery does not restart",
                                  "安全機能ではない / not a safety function"]):
        svg.text(770, 900 + index * 34, f"・{text}", 14, 400, INK)
    note(svg, 1090, "シミュレーションは教育用モデル。実機PLCの実装や安全機能の証明ではない。",
         "The simulation is a teaching model; it does not prove a real PLC implementation or a safety function.")
    svg.footer("アーム・立ち上がり検出・STOP優先・位置確認・リセット分離で再起動を防ぐ",
               "Arming, edge detection, STOP precedence, position confirmation and a separate reset prevent restart")
    return svg


def d08_13() -> Svg:
    svg = new_diagram("D08-13", "インターロックの例", "Interlock example",
                      "第8日 / Day 8", 880)
    panel(svg, 70, 170, 1300, 260, "前進と後退の相互排他", "mutual exclusion of forward and reverse")
    ladder_row(svg, 290, [("contact", False, "FWD_REQ", None), ("contact", True, "REV_OUT", None),
                          ("coil", "FWD_OUT", None)], start_x=250, step=200)
    ladder_row(svg, 380, [("contact", False, "REV_REQ", None), ("contact", True, "FWD_OUT", None),
                          ("coil", "REV_OUT", None)], start_x=250, step=200)
    svg.text(90, 250, "相互に打ち消すだけの形は、スキャン順に依存する / cross-linked contacts depend on scan order",
             14, 700, WARN)

    panel(svg, 70, 460, 620, 260, "教材の設計", "teaching design")
    svg.text(90, 550, "同時要求は両方OFF（拒否）。", 17, 700, INK)
    svg.text(90, 580, "Both requests OFF; the conflict is rejected.", 14, 400, MUTED)
    svg.text(90, 630, "決定的で、並び順に依存しない。", 15, 400, INK)
    svg.text(90, 658, "Deterministic and independent of rung order.", 13, 400, MUTED)
    svg.text(90, 700, "実際の反転接触器は電気的・機械的ILも必要。", 14, 700, WARN)
    svg.text(90, 724, "Real reversing contactors also need electrical and mechanical interlocking.", 12, 400, MUTED)

    table_grid(svg, 750, 460, ["要求 / request", "FWD", "REV", "競合 / conflict"],
               [["前進のみ / forward only", "ON", "OFF", "なし / none"],
                ["後退のみ / reverse only", "OFF", "ON", "なし / none"],
                ["両方 / both", "OFF", "OFF", "あり / yes"],
                ["停止 / stop", "OFF", "OFF", "なし / none"]],
               [200, 90, 90, 150], row_h=48, size=15)
    note(svg, 760, "ソフトのインターロックを、安全定格のガードとして扱わない。",
         "Software interlocks are not safety-rated guarding functions.")
    svg.footer("反対側の出力で自分の指令を禁止する。同時要求は決定的に拒否する",
               "Each command is inhibited by the opposite output; simultaneous requests are deterministically rejected")
    return svg


def d08_14() -> Svg:
    svg = new_diagram("D08-14", "シーケンスとタイミング", "Sequence and timing",
                      "第8日 / Day 8", 900)
    chain(svg, [("製品検出", "product detected", "X4", SENSOR),
                ("前進指令", "extend command", "Y2", CONTROL),
                ("前進端の確認", "extended confirmed", "X3", SENSOR),
                ("後退指令", "retract command", "Y2 OFF", CONTROL),
                ("後退端の確認", "retracted confirmed", "X2", SENSOR)],
          y=190, h=140, x0=70, x1=1370, gap=24)
    panel(svg, 70, 400, 1300, 300, "タイミングとタイムアウト", "timing and timeout")
    svg.line(110, 500, 1310, 500, stroke=GRID, sw=2)
    segments = [("前進指令", "extend", 200, MECH), ("確認待ち", "wait", 300, ENERGY),
                ("後退", "retract", 200, MECH), ("確認待ち", "wait", 250, ENERGY)]
    cursor = 120
    for ja, en, width, color in segments:
        svg.rect(cursor, 470, width, 60, fill=CARD, stroke=color, sw=2, rx=3)
        svg.text(cursor + width / 2, 495, ja, 14, 700, INK, "middle")
        svg.text(cursor + width / 2, 516, en, 12, 400, MUTED, "middle")
        cursor += width
    svg.line(620, 440, 620, 560, stroke=BAD, sw=3, dash="8 6")
    svg.text(630, 440, "タイムアウト（教材値3秒）/ timeout (training value 3 s)", 14, 700, BAD)
    svg.text(110, 620, "指令と確認は別。確認が来ない場合を設計する。", 16, 400, INK)
    svg.text(110, 648, "Commands and confirmations differ; design the missing-confirmation case.", 14, 400, MUTED)
    svg.text(110, 690, "電磁弁OFF＝必ず停止、ではない。ばね戻りでは動くことがある。", 15, 700, WARN)
    svg.text(110, 712, "OFF does not always mean stopped; a spring-return valve can move.", 12, 400, MUTED)
    svg.footer("製品検出 → 前進 → 確認 → 後退 → 確認。タイムアウトの位置を決める",
               "Product detection, extend, confirm, retract, confirm, with a defined timeout")
    return svg


DAY8 = [d08_01, d08_02, d08_03, d08_04, d08_05, d08_06, d08_07,
        d08_08, d08_09, d08_10, d08_11, d08_12, d08_13, d08_14]


# --------------------------------------------------------------------------- #
# Day 9
# --------------------------------------------------------------------------- #
def d09_01() -> Svg:
    svg = new_diagram("D09-01", "撮像の流れ", "The imaging chain",
                      "第9日 / Day 9", 900)
    chain(svg, [("対象物", "object", "シート・製品 / sheet, product", MECH),
                ("照明", "illumination", "光を当てる / lights the object", ENERGY),
                ("レンズ", "lens", "結像する / forms the image", CONTROL),
                ("撮像素子", "image sensor", "光を電気に / light to signal", SENSOR),
                ("デジタル画像", "digital image", "画素の集まり / array of pixels", DATA),
                ("コンピュータ", "computer", "処理・AI / processing, AI", CONTROL)],
          y=190, h=150, x0=60, x1=1380, gap=22)
    panel(svg, 70, 420, 1300, 330, "カメラの要素", "camera elements")
    items = [
        ("画素", "pixel", "画像の最小単位 / smallest unit"),
        ("解像度", "resolution", "横×縦の画素数 / pixels across and down"),
        ("センササイズ", "sensor size", "撮像素子の大きさ / physical size"),
        ("露光", "exposure", "光を受ける時間 / collection time"),
        ("ゲイン", "gain", "信号の増幅 / amplification"),
        ("トリガ", "trigger", "撮影のきっかけ / capture start"),
    ]
    card_w = (1300 - 40 - 5 * 20) / 6
    for index, (ja, en, sub) in enumerate(items):
        x = 90 + index * (card_w + 20)
        svg.card(x, 490, card_w, 230, ja, en, stroke=DATA, accent=DATA, sub=sub)
    note(svg, 780, "産業用カメラは画像を撮る装置。AI推論はPCなどが行う。",
         "An industrial camera captures images; AI inference runs on a PC or processor.")
    svg.footer("物体 → 照明 → レンズ → 撮像素子 → デジタル画像 → コンピュータ",
               "Object, illumination, lens, image sensor, digital image, computer")
    return svg


def d09_02() -> Svg:
    svg = new_diagram("D09-02", "解像度と欠陥のピクセル数", "Resolution and the pixel size of a defect",
                      "第9日 / Day 9", 900)
    for index, (cols, label, mm_per_px) in enumerate([(12, "低解像度 / low resolution", 0.5),
                                                      (24, "中解像度 / medium", 0.25),
                                                      (48, "高解像度 / high", 0.125)]):
        x = 90 + index * 440
        cell = 220 / cols
        svg.rect(x, 200, 220, 220, fill="#FFFFFF", stroke=GRID, sw=1.4)
        for row in range(cols):
            for col in range(cols):
                if (row + col) % 2 == 0:
                    svg.rect(x + col * cell, 200 + row * cell, cell, cell,
                             fill="#EDF2F7", stroke="none", sw=0, rx=0)
        defect = max(cell * (0.5 / mm_per_px), 1)
        sx = x + 220 * 0.42
        sy = 200 + 220 * 0.42
        svg.rect(sx, sy, defect, defect, fill=BAD, stroke=BAD, sw=1, rx=0)
        svg.text(x + 110, 455, label, 16, 700, INK, "middle")
        svg.text(x + 110, 480, f"{mm_per_px} mm/px", 14, 400, MUTED, "middle")
        pixels = 0.5 / mm_per_px
        svg.text(x + 110, 512, f"0.5 mm ≈ {pixels:g} px", 16, 700, BAD, "middle")
    panel(svg, 70, 560, 1300, 220, "ピクセル数だけで検出は決まらない", "pixel count alone does not decide detection")
    svg.text(90, 650, "・光学分解能・ピント・コントラスト・照明・動体ぶれ", 15, 400, INK)
    svg.text(90, 675, "  optical resolution, focus, contrast, lighting, motion blur", 12, 400, MUTED)
    svg.text(90, 715, "・レンズ性能・撮像素子・前処理・AI入力解像度・検証データ", 15, 400, INK)
    svg.text(90, 740, "  lens quality, sensor, preprocessing, model input resolution, validation data", 12, 400, MUTED)
    note(svg, 800, "1,920 px・視野240 mm → 0.125 mm/px。0.5 mmの欠陥は約4 px。",
         "1920 px across 240 mm is 0.125 mm/px; a 0.5 mm defect covers about 4 pixels.")
    svg.footer("同じ欠陥でも解像度でピクセル数が変わる。4 pxでも検出保証ではない",
               "The same defect covers different pixel counts; four pixels is not a guarantee")
    return svg


def d09_03() -> Svg:
    svg = new_diagram("D09-03", "視野・作動距離・被写界深度", "Field of view, working distance and depth of field",
                      "第9日 / Day 9", 980)
    panel(svg, 70, 170, 620, 360, "広い視野・短い作動距離", "wide field of view, short working distance")
    svg.rect(200, 230, 120, 40, fill=FILL_CONTROL, stroke=CONTROL, sw=2, rx=4)
    svg.text(260, 220, "カメラ / camera", 13, 700, CONTROL, "middle")
    svg.poly([(230, 272), (290, 272), (470, 450), (50, 450)], fill=FILL_DATA, stroke=DATA, sw=1.6, marker=False)
    svg.line(260, 450, 260, 480, stroke=MUTED, sw=1.6, marker=False)
    svg.text(270, 500, "作動距離 WD / working distance", 13, 400, MUTED)
    svg.line(60, 440, 460, 440, stroke=MECH, sw=3, marker=False)
    svg.text(260, 430, "広い視野 / wide FOV", 14, 700, MECH, "middle")

    panel(svg, 750, 170, 620, 360, "狭い視野・長い作動距離", "narrow field of view, long working distance")
    svg.rect(1030, 230, 120, 40, fill=FILL_CONTROL, stroke=CONTROL, sw=2, rx=4)
    svg.text(1090, 220, "カメラ / camera", 13, 700, CONTROL, "middle")
    svg.poly([(1060, 272), (1120, 272), (1190, 450), (990, 450)], fill=FILL_DATA, stroke=DATA, sw=1.6, marker=False)
    svg.line(1090, 450, 1090, 480, stroke=MUTED, sw=1.6, marker=False)
    svg.text(1100, 500, "長い作動距離 / long WD", 13, 400, MUTED)
    svg.line(1000, 440, 1180, 440, stroke=MECH, sw=3, marker=False)
    svg.text(1090, 430, "狭い視野 / narrow FOV", 14, 700, MECH, "middle")

    panel(svg, 70, 570, 1300, 240, "ピントと被写界深度", "focus and depth of field")
    for index, (label, width, color) in enumerate([("浅い / shallow", 160, BAD),
                                                   ("深い / deep", 420, GOOD)]):
        y = 620 + index * 70
        svg.rect(520, y, width, 34, fill=CARD, stroke=color, sw=2, rx=4)
        svg.text(530, y + 23, label, 14, 700, color)
    svg.text(110, 790, "絞ると深くなる。光は減る。 / stopping down deepens it and reduces light.", 14, 400, MUTED)
    note(svg, 840, "焦点距離だけでレンズは選べない。視野・WD・センササイズ・絞りを見る。",
         "A lens is not chosen from focal length alone; FOV, WD, sensor size and aperture matter.")
    svg.footer("広い視野と狭い視野、短いWDと長いWD、浅い被写界深度と深い被写界深度",
               "Wide and narrow FOV, short and long working distance, shallow and deep depth of field")
    return svg


def d09_04() -> Svg:
    svg = new_diagram("D09-04", "グローバルとローリングシャッター", "Global and rolling shutter",
                      "第9日 / Day 9", 860)
    panel(svg, 70, 170, 620, 360, "グローバルシャッター", "global shutter")
    svg.rect(120, 240, 520, 240, fill="#FFFFFF", stroke=GRID, sw=1.4)
    svg.rect(240, 300, 120, 120, fill=FILL_MECH, stroke=MECH, sw=2.4, rx=2)
    svg.text(400, 400, "→ 移動 / motion", 14, 600, MUTED)
    svg.text(120, 520, "全画素が同じ時間に露光する / all pixels expose at the same time", 15, 400, INK)
    svg.text(120, 548, "行ごとの時間ずれによるゆがみがない / no row-timing distortion", 13, 400, MUTED)

    panel(svg, 750, 170, 620, 360, "ローリングシャッター", "rolling shutter")
    svg.rect(800, 240, 520, 240, fill="#FFFFFF", stroke=GRID, sw=1.4)
    svg.parts.append(
        f'<path d="M920 300 L1040 300 L1000 420 L880 420 Z" fill="{FILL_MECH}" stroke="{MECH}" stroke-width="2.4"/>')
    svg.text(1080, 400, "→ 移動 / motion", 14, 600, MUTED)
    svg.text(800, 520, "行ごとに時間をずらして露光する / rows expose at different times", 15, 400, INK)
    svg.text(800, 548, "動く対象では像が斜めにゆがむことがある / a moving object can skew", 13, 700, BAD)

    panel(svg, 70, 570, 1300, 190, "共通の注意", "common caution")
    svg.text(90, 650, "グローバルでも、動体ぶれはなくならない。ぶれは露光時間で決まる。",
             16, 400, INK)
    svg.text(90, 680, "A global shutter does not remove motion blur; blur depends on exposure time.",
             14, 400, MUTED)
    svg.text(90, 720, "移動するシートの寸法・位置の判断では、ゆがみの影響を確認する。",
             14, 400, INK)
    svg.footer("グローバルは行ごとの時間ずれを避ける。ぶれは露光で決まる",
               "A global shutter avoids row-timing distortion; blur is set by exposure")
    return svg


def d09_05() -> Svg:
    svg = new_diagram("D09-05", "露光と動体ぶれ", "Exposure and motion blur",
                      "第9日 / Day 9", 880)
    panel(svg, 70, 170, 1300, 300, "速度・露光・移動量", "speed, exposure and movement")
    svg.text(90, 250, "材料速度 1,000 mm/s、露光 1 ms", 18, 700, INK)
    svg.text(90, 280, "material speed 1,000 mm/s, exposure 1 ms", 14, 400, MUTED)
    svg.text(90, 340, "移動量 = 1,000 × 0.001 = 1 mm", 22, 700, BAD)
    svg.text(90, 372, "movement during exposure = 1 mm", 15, 400, MUTED)
    svg.text(90, 420, "1 px = 0.125 mm/px のとき  1 ÷ 0.125 = 8 px", 20, 700, BAD)
    svg.text(90, 448, "at 0.125 mm/px the blur is 8 pixels", 15, 400, MUTED)
    svg.text(760, 250, "1 px以内の目標", 18, 700, GOOD)
    svg.text(760, 280, "target of one pixel or less", 14, 400, MUTED)
    svg.text(760, 340, "露光 ≈ 0.125 ÷ 1,000 = 0.125 ms", 22, 700, GOOD)
    svg.text(760, 372, "exposure about 0.125 ms", 15, 400, MUTED)
    svg.text(760, 420, "※例示的な目標であり保証ではない", 15, 700, WARN)
    svg.text(760, 448, "an illustrative target, not a guarantee", 13, 400, MUTED)

    panel(svg, 70, 510, 1300, 240, "短くすると光が減る", "shorter exposure collects less light")
    svg.rect(110, 590, 500, 40, fill=FILL_ENERGY, stroke=ENERGY, sw=2, rx=4)
    svg.text(360, 617, "露光1 ms：光が多い / more light", 15, 700, INK, "middle")
    svg.rect(110, 650, 125, 40, fill=FILL_ENERGY, stroke=ENERGY, sw=2, rx=4)
    svg.text(260, 677, "露光0.125 ms：光が1/8 / one eighth of the light", 14, 700, BAD)
    svg.text(110, 730, "照明の明るさと画質（ノイズ・コントラスト）に直結する。", 14, 400, MUTED)
    svg.footer("ぶれ = 速度 × 露光時間。短い露光は光量とのトレードオフ",
               "Blur is speed times exposure; a shorter exposure trades against light")
    return svg


def d09_06() -> Svg:
    svg = new_diagram("D09-06", "照明の種類", "Lighting types",
                      "第9日 / Day 9", 1000)
    cards = [
        ("バックライト", "backlight", "シルエット・透過", "silhouette, transmission", ENERGY),
        ("リング照明", "ring light", "レンズ周囲から", "around the lens", DATA),
        ("バー照明", "bar light", "直線・方向", "linear, directional", CONTROL),
        ("拡散照明", "diffuse lighting", "光沢・むらを低減", "gloss and unevenness", GOOD),
        ("同軸照明", "coaxial lighting", "平面の反射面", "flat reflective surfaces", MECH),
        ("低角度・暗視野", "low angle, dark field", "傷・異物・微細な凹凸", "scratches, particles, relief", BAD),
    ]
    card_w = (1300 - 40 - 2 * 20) / 3
    for index, (ja, en, ja2, en2, color) in enumerate(cards):
        row, col = divmod(index, 3)
        x = 70 + col * (card_w + 20)
        y = 180 + row * 290
        svg.rect(x, y, card_w, 260, fill=CARD, stroke=color, sw=2, rx=12)
        svg.rect(x + 30, y + 30, 90, 46, fill=FILL_COLOR.get(color, FILL_GREY), stroke=color, sw=1.8, rx=4)
        svg.text(x + 75, y + 60, "光", 16, 700, INK, "middle")
        svg.line(x + 130, y + 53, x + 210, y + 100, stroke=color, sw=2)
        svg.rect(x + 160, y + 100, 90, 24, fill="#E3E8EE", stroke=MUTED, sw=1.4, rx=3)
        svg.text(x + 205, y + 150, ja, 18, 700, color, "middle")
        svg.text(x + 205, y + 175, en, 13, 400, MUTED, "middle")
        svg.text(x + 30, y + 215, f"{ja2} / {en2}", 13, 400, INK)
    note(svg, 790, "効果は材質と欠陥形状に依存する。1種類で全欠陥は見えない。",
         "Effectiveness depends on material and defect geometry; one type does not show every defect.")
    svg.footer("バックライト・リング・バー・拡散・同軸・低角度の模式的な比較",
               "Schematic comparison of backlight, ring, bar, diffuse, coaxial and low-angle lighting")
    return svg


def d09_07() -> Svg:
    svg = new_diagram("D09-07", "カメラと照明の配置", "Camera and lighting arrangement",
                      "第9日 / Day 9", 980)
    svg.rect(120, 200, 1200, 480, fill="#FBFCFE", stroke=GRID, sw=2, rx=10)
    svg.text(140, 232, "囲い・遮光 / enclosure and light shield", 14, 700, MUTED)
    svg.line(180, 520, 1260, 520, stroke=MECH, sw=6, marker=False)
    svg.text(700, 556, "材料（移動するシート）/ material (moving sheet)", 15, 700, MECH, "middle")
    svg.line(180, 520, 180, 560, stroke=MECH, sw=1.6, marker=False)
    svg.line(1260, 520, 1260, 560, stroke=MECH, sw=1.6, marker=False)
    svg.rect(660, 260, 120, 60, fill=FILL_CONTROL, stroke=CONTROL, sw=2.4, rx=6)
    svg.text(720, 250, "カメラ / camera", 14, 700, CONTROL, "middle")
    svg.text(740, 336, "固定した作動距離 / fixed working distance", 13, 400, MUTED, "start")
    svg.line(720, 320, 720, 470, stroke=DATA, sw=2, dash="7 5")
    svg.rect(620, 580, 200, 40, fill=FILL_ENERGY, stroke=ENERGY, sw=2, rx=4)
    svg.text(720, 646, "バックライト / backlight", 14, 700, ENERGY, "middle")
    svg.line(720, 580, 720, 524, stroke=ENERGY, sw=2)
    svg.rect(300, 400, 90, 60, fill=FILL_DATA, stroke=DATA, sw=2, rx=4)
    svg.text(345, 390, "斜め照明 / oblique", 13, 700, DATA, "middle")
    svg.line(345, 462, 430, 516, stroke=DATA, sw=2)
    svg.rect(1010, 430, 90, 60, fill=FILL_HAZARD, stroke=BAD, sw=2, rx=4)
    svg.text(1055, 420, "低角度 / low angle", 13, 700, BAD, "middle")
    svg.line(1010, 476, 930, 518, stroke=BAD, sw=2)
    svg.line(720, 240, 720, 200, stroke=CONTROL, sw=3, marker=False)
    svg.text(760, 214, "調整可能な取付 / adjustable mount", 13, 400, MUTED)
    note(svg, 700, "剛性・固定・遮光・清掃性・安全アクセスで配置を決める。",
         "Arrangement follows rigidity, fixation, shielding, cleanability and safe access.")
    svg.footer("材料の上にカメラ、後ろにバックライト、斜め照明、低角度照明、囲い、固定WD",
               "Camera above the material, backlight behind, oblique and low-angle lighting, enclosure, fixed working distance")
    return svg


def d09_08() -> Svg:
    svg = new_diagram("D09-08", "撮像条件の比較（合成例）", "Imaging conditions compared (synthetic)",
                      "第9日 / Day 9", 1000)
    tiles = [
        ("露出不足", "underexposed", "#4A5560"),
        ("適正", "correct", "#B9C4CE"),
        ("露出過多", "overexposed", "#F7FAFC"),
        ("低コントラスト", "low contrast", "#C9CED4"),
        ("高コントラスト", "high contrast", "#8A939C"),
        ("グレア", "glare", "#FFFFFF"),
        ("拡散照明", "diffuse light", "#AEB8C2"),
        ("方向を変えた照明", "changed direction", "#9AA5B0"),
    ]
    tile_w, tile_h = 300, 150
    for index, (ja, en, grey) in enumerate(tiles):
        row, col = divmod(index, 4)
        x = 70 + col * (tile_w + 20)
        y = 190 + row * 230
        svg.rect(x, y, tile_w, tile_h, fill=grey, stroke=GRID, sw=2, rx=4)
        if index == 5:
            svg.circle(x + 150, y + 70, 46, fill="#FFFFFF", stroke="#FFFFFF", sw=0)
        else:
            svg.circle(x + 150, y + 70, 26, fill="#5B6670" if index != 4 else "#3A434C", stroke="none", sw=0)
        svg.text(x + tile_w / 2, y + tile_h + 30, ja, 15, 700, INK, "middle")
        svg.text(x + tile_w / 2, y + tile_h + 54, en, 13, 400, MUTED, "middle")
    panel(svg, 70, 660, 1300, 130, "合成例について", "about these synthetic examples")
    svg.text(90, 740, "これらは学習用の合成例です。実際のPVC工場の測定値ではありません。",
             16, 700, WARN)
    svg.text(90, 768, "These are synthetic teaching examples, not measurements from a real PVC line.",
             14, 400, MUTED)
    note(svg, 820, "露出・ピント・コントラスト・グレア・照明方向は、見え方を大きく変える。",
         "Exposure, focus, contrast, glare and light direction change what is visible.")
    svg.footer("露出不足・適正・露出過多、低/高コントラスト、グレア、拡散、照明方向の比較（合成）",
               "Underexposed, correct, overexposed, low/high contrast, glare, diffuse and direction changes (synthetic)")
    return svg


def d09_09() -> Svg:
    svg = new_diagram("D09-09", "AI検査システムの構成", "AI inspection system architecture",
                      "第9日 / Day 9", 1080)
    chain(svg, [("カメラ・レンズ・照明", "camera, lens, lighting", "画像を作る / creates the image", SENSOR),
                ("画像取込み", "image acquisition", "PCへ転送 / transfer to the PC", DATA),
                ("前処理", "preprocessing", "リサイズ・変換 / resize, convert", CONTROL)],
          y=180, h=130, x0=70, x1=1380, gap=40)
    chain(svg, [("AI推論", "AI inference", "モデルで判定 / model output", CONTROL),
                ("検査判定", "inspection decision", "OK / NG / 無効", DATA),
                ("PLC通信", "PLC communication", "結果を渡す / send the result", CONTROL)],
          y=360, h=130, x0=70, x1=1380, gap=40)
    chain(svg, [("機械設備", "mechanical equipment", "仕分け・停止 / sort, stop", MECH),
                ("センサー", "sensor", "結果を確認 / confirms the result", SENSOR),
                ("記録・画像保存", "logging and image storage", "任意 / optional", DATA)],
          y=540, h=130, x0=70, x1=1380, gap=40)
    svg.line(1290, 312, 1290, 356, stroke=ACCENT, sw=2.4)
    svg.line(1290, 492, 1290, 536, stroke=ACCENT, sw=2.4)
    panel(svg, 70, 730, 620, 240, "矢印の種類", "arrow types")
    legend_swatches(svg, 90, 800, [(DATA, "画像データ", "image data"),
                                   (CONTROL, "制御信号", "control signal"),
                                   (ENERGY, "電力", "power")])
    legend_swatches(svg, 340, 800, [(MECH, "機械動作", "mechanical"),
                                    (SENSOR, "フィードバック", "feedback")])
    panel(svg, 750, 730, 620, 240, "役割の分離", "separation of roles")
    svg.text(770, 810, "AIは結果を制御装置へ渡す。", 15, 700, INK)
    svg.text(770, 838, "AI passes results to the controller.", 13, 400, MUTED)
    svg.text(770, 886, "危険な動作は機械側の制御と安全で扱う。", 14, 400, INK)
    svg.text(770, 914, "Hazardous motion is handled by the machine control and safety system.", 12, 400, MUTED)
    note(svg, 990, "記録と画像保存は任意。制御と安全の役割を混ぜない。",
         "Logging and storage are optional; do not mix control and safety roles.")
    svg.footer("画像データ・制御信号・電力・機械動作・フィードバックを区別して描く",
               "Distinguish image data, control signals, power, mechanical movement and feedback")
    return svg


def d09_10() -> Svg:
    svg = new_diagram("D09-10", "撮像タイミングと遅れ", "Inspection timing and latency",
                      "第9日 / Day 9", 900)
    panel(svg, 70, 170, 1300, 300, "時間の積み重ね", "the accumulation of time")
    segments = [("撮像間隔", "interval", 200, MECH), ("転送", "transfer", 140, DATA),
                ("推論", "inference", 220, CONTROL), ("判定", "decision", 120, SENSOR),
                ("応答", "actuator", 160, ENERGY)]
    cursor = 110
    for ja, en, width, color in segments:
        svg.rect(cursor, 280, width, 90, fill=CARD, stroke=color, sw=2, rx=4)
        svg.text(cursor + width / 2, 320, ja, 15, 700, INK, "middle")
        svg.text(cursor + width / 2, 344, en, 12, 400, MUTED, "middle")
        cursor += width
    svg.line(110, 400, 1310, 400, stroke=GRID, sw=2, marker=False)
    svg.text(110, 435, "判定までの遅れ / end-to-end decision latency", 14, 700, MUTED)
    svg.line(110, 250, 110, 460, stroke=GRID, sw=1.4, marker=False)
    svg.line(840, 250, 840, 460, stroke=GRID, sw=1.4, marker=False)

    panel(svg, 70, 510, 620, 260, "計算例", "worked example")
    svg.text(90, 600, "30 FPS、材料1,000 mm/s", 17, 700, INK)
    svg.text(90, 630, "30 FPS at 1,000 mm/s", 14, 400, MUTED)
    svg.text(90, 690, "1,000 ÷ 30 ≈ 33.33 mm", 24, 700, BAD)
    svg.text(90, 722, "movement between nominal frames", 13, 400, MUTED)

    panel(svg, 750, 510, 620, 260, "注意", "caution")
    svg.text(770, 600, "移動方向の視野と幅方向の視野を混同しない。", 15, 700, INK)
    svg.text(770, 628, "Do not confuse travel-direction FOV with width FOV.", 12, 400, MUTED)
    svg.text(770, 676, "FPSが足りても、完全な検査は約束できない。", 15, 400, INK)
    svg.text(770, 704, "Nominal FPS does not promise complete inspection.", 12, 400, MUTED)
    svg.text(770, 744, "カメラFPS ≠ 検査FPS / camera FPS is not inspection FPS", 14, 700, WARN)
    svg.footer("撮像間隔・転送・推論・判定・応答を積み上げて、全体の遅れを考える",
               "Add capture interval, transfer, inference, decision and actuator response")
    return svg


def d09_11() -> Svg:
    svg = new_diagram("D09-11", "最終チェックリストとPC・PLC・機械", "Final checklist and the PC, PLC and machine relationship",
                      "第9日 / Day 9", 980)
    panel(svg, 70, 170, 700, 500, "撮像条件の記録", "record the imaging conditions")
    items = ["カメラ機種 / camera model", "レンズ / lens", "作動距離 / working distance",
             "視野 / field of view", "カメラ角度 / camera angle", "照明の種類と位置 / light type and position",
             "露光時間・ゲイン / exposure, gain", "フレームレート／ライン速度 / frame or line rate",
             "材料速度 / material speed", "代表的な欠陥サンプル / defect samples"]
    for index, text in enumerate(items):
        svg.text(90, 260 + index * 38, f"・{text}", 15, 400, INK)

    panel(svg, 810, 170, 560, 500, "PC・PLC・機械", "the PC, PLC and machine")
    svg.rect(850, 250, 200, 80, fill=FILL_CONTROL, stroke=CONTROL, sw=2, rx=6)
    svg.text(950, 290, "PC", 20, 700, INK, "middle")
    svg.text(950, 315, "AI推論 / inference", 12, 400, MUTED, "middle")
    svg.line(1052, 290, 1130, 290, stroke=CONTROL, sw=2.4)
    svg.rect(1134, 250, 200, 80, fill=FILL_DATA, stroke=DATA, sw=2, rx=6)
    svg.text(1234, 290, "PLC", 20, 700, INK, "middle")
    svg.text(1234, 315, "結果を受け取る / receives", 12, 400, MUTED, "middle")
    svg.line(1234, 332, 1234, 420, stroke=MECH, sw=2.4)
    svg.rect(1100, 424, 270, 80, fill=FILL_MECH, stroke=MECH, sw=2, rx=6)
    svg.text(1235, 462, "機械設備", 18, 700, INK, "middle")
    svg.text(1235, 487, "machine", 12, 400, MUTED, "middle")
    svg.line(1100, 464, 1030, 464, stroke=SENSOR, sw=2.2, dash="7 5")
    svg.text(880, 456, "フィードバック / feedback", 12, 700, SENSOR)
    svg.text(850, 560, "AIは結果を渡す。危険な動作は機械側で扱う。", 14, 400, INK)
    svg.text(850, 588, "AI passes the result; the machine handles hazardous motion.", 12, 400, MUTED)
    svg.text(850, 630, "無効（INVALID）をOKにしない。", 14, 700, WARN)

    note(svg, 720, "短いチェックリストで十分。提案書や発表は不要。",
         "A short checklist is enough; no proposal document or presentation is required.")
    svg.footer("撮像条件の記録項目と、PC・PLC・機械設備の関係",
               "Imaging-condition record items and the PC, PLC and machine relationship")
    return svg


DAY9 = [d09_01, d09_02, d09_03, d09_04, d09_05, d09_06,
        d09_07, d09_08, d09_09, d09_10, d09_11]


def build() -> list[Path]:
    outputs: list[Path] = []
    for builder in DAY7 + DAY8 + DAY9:
        svg = builder()
        folder = DIAGRAMS / f"day{svg.fid[1:3]}"
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"{svg.fid}.svg"
        svg.save(path)
        outputs.append(path)
        print(f"Wrote {path.relative_to(ROOT)} ({svg.width}x{svg.height})")
    return outputs


def main() -> int:
    outputs = build()
    print(f"Wrote {len(outputs)} diagrams")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
