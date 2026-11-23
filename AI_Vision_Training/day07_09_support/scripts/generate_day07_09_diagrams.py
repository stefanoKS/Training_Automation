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

The drawings are conceptual teaching figures, not construction drawings,
not ISO 1219-1 pneumatic schematics and not safety-certified designs.
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


def arrow_label(svg: Svg, x1, y1, x2, y2, label, color=ACCENT, dash=None, size=14) -> None:
    svg.line(x1, y1, x2, y2, stroke=color, sw=2.2, dash=dash)
    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
    svg.text(mid_x + 6, mid_y - 8, label, size, 600, color)


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
    svg.parts.append(
        f'<path d="M{x - 18} {y - 19} Q{x - 36} {y} {x - 18} {y + 19}" fill="none" '
        f'stroke="{ACCENT}" stroke-width="2.4"/>'
        f'<path d="M{x + 18} {y - 19} Q{x + 1} {y} {x + 18} {y + 19}" fill="none" '
        f'stroke="{ACCENT}" stroke-width="2.4"/>'
    )
    svg.line(x - 48, y, x - 34, y, marker=False, sw=2)
    svg.line(x + 18, y, x + 62, y, marker=False, sw=2)
    svg.text(x, y + 44, address, 15, 700, ACCENT, "middle")
    if label:
        svg.text(x, y - 28, label, 13, 400, MUTED, "middle")


def cylinder_symbol(svg: Svg, x, y, w=360, h=120, rod=90, ja="複動シリンダ", en="double-acting cylinder") -> None:
    svg.rect(x, y, w, h, fill=FILL_MECH, stroke=MECH, sw=2.4, rx=8)
    # piston and rod
    px = x + w * 0.58
    svg.rect(px - 8, y + 8, 16, h - 16, fill=MECH, stroke=MECH, sw=1)
    svg.rect(px, y + h / 2 - 9, w - (px - x) + rod, 18, fill="#B9C9D9", stroke=MECH, sw=1.4, rx=3)
    svg.text(x + w / 2, y + h + 26, ja, 16, 700, INK, "middle")
    svg.text(x + w / 2, y + h + 46, en, 13, 400, MUTED, "middle")


def valve_symbol(svg: Svg, x, y, ja="5/2 単一ソレノイド弁", en="5/2 single-solenoid valve") -> None:
    w, h = 210, 110
    svg.rect(x, y, w / 2, h, fill=FILL_ENERGY, stroke=ENERGY, sw=2, rx=2)
    svg.rect(x + w / 2, y, w / 2, h, fill=FILL_ENERGY, stroke=ENERGY, sw=2, rx=2)
    # functional flow arrows (not a construction drawing)
    svg.line(x + 18, y + 30, x + 78, y + 30, stroke=ENERGY, sw=2)
    svg.line(x + 18, y + 80, x + 78, y + 80, stroke=ENERGY, sw=2)
    svg.line(x + w / 2 + 18, y + 30, x + w / 2 + 78, y + 80, stroke=ENERGY, sw=2)
    svg.line(x + w / 2 + 18, y + 80, x + w / 2 + 78, y + 30, stroke=ENERGY, sw=2)
    # solenoid box and spring
    svg.rect(x - 42, y + 30, 34, 50, fill=CARD, stroke=CONTROL, sw=1.8, rx=3)
    svg.text(x - 25, y + 60, "SOL", 12, 700, CONTROL, "middle")
    svg.parts.append(
        f'<path d="M{x + w + 4} {y + 40} q12 15 0 30 q12 15 0 30" fill="none" stroke="{ENERGY}" stroke-width="1.8"/>'
    )
    svg.text(x + w / 2, y + h + 26, ja, 16, 700, INK, "middle")
    svg.text(x + w / 2, y + h + 46, en, 13, 400, MUTED, "middle")
    for index, port in enumerate(("P", "A", "B", "R1", "R2")):
        svg.text(x + 14 + index * 42, y - 10, port, 13, 700, ENERGY)


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
        color, label = item[0], item[1]
        if len(item) >= 3:
            label = f"{item[1]} / {item[2]}"
        top = y + index * 32
        svg.rect(x, top, 26, 18, fill=color, stroke=color, sw=1, rx=3)
        svg.text(x + 36, top + 15, label, 14, 400, MUTED)


# --------------------------------------------------------------------------- #
# Day 7
# --------------------------------------------------------------------------- #
def d07_01() -> Svg:
    svg = new_diagram("D07-01", "設備開発の8段階", "Eight stages of equipment development",
                      "第7日 / Day 7", 980)
    stages = [
        ("① 課題抽出", "Problem finding", "困りごと一覧 / problem list", MECH),
        ("② 現状把握", "Observation", "時間・数量・不良 / time, quantity, defects", MECH),
        ("③ 構想・要求", "Concept and requirements", "要求仕様書 / requirements", CONTROL),
        ("④ 比較・見積", "Comparison and estimate", "方式比較・概算 / options and estimate", CONTROL),
        ("⑤ 詳細設計", "Detailed design", "図面・BOM・ラダー / drawings, BOM, ladder", SENSOR),
        ("⑥ 調達・製作", "Procurement and build", "製作記録 / build record", SENSOR),
        ("⑦ 試験・評価", "Test and evaluation", "試運転記録 / commissioning record", ENERGY),
        ("⑧ 導入・保全", "Introduction and maintenance", "標準書・保全計画 / standards and plan", ENERGY),
    ]
    for row in range(2):
        subset = stages[row * 4:(row + 1) * 4]
        y = 230 + row * 290
        for index, (ja, en, sub, color) in enumerate(subset):
            x = 70 + index * 330
            svg.card(x, y, 300, 170, ja, en, sub=sub, stroke=color, accent=color, fill=CARD)
            if index < 3:
                svg.line(x + 304, y + 85, x + 326, y + 85, stroke=color, sw=2.4)
        if row == 0:
            svg.line(1370, 405, 1370, 470, stroke=ACCENT, sw=2, marker=False)
            svg.line(1370, 470, 70, 470, stroke=ACCENT, sw=2, marker=False)
            svg.line(70, 470, 70, 520, stroke=ACCENT, sw=2)
            svg.text(720, 500, "次の段階へ / to the next stage", 15, 600, ACCENT, "middle")
    svg.line(140, 620, 140, 700, stroke=HAZARD, sw=2, dash="8 6")
    svg.line(140, 700, 500, 700, stroke=HAZARD, sw=2, dash="8 6")
    svg.line(500, 700, 500, 620, stroke=HAZARD, sw=2, dash="8 6")
    svg.text(320, 728, "戻り（設計の成熟）/ iteration is how the design matures", 15, 700, HAZARD, "middle")
    legend_swatches(svg, 70, 790, [
        (MECH, "機械・構想 / mechanics and concept"),
        (CONTROL, "要求・比較 / requirements and comparison"),
        (SENSOR, "設計・製作 / design and build"),
        (ENERGY, "試験・運用 / test and operation"),
        (HAZARD, "戻り・危険 / iteration and hazard"),
    ])
    svg.footer("各段階の成果物が次段階の入力になる。成果物なしで進むと手戻りが大きい。",
               "Each stage output feeds the next. Skipping a deliverable makes later rework larger.")
    return svg


def d07_02() -> Svg:
    svg = new_diagram("D07-02", "ECRSで押出し作業を見直す", "Re-examining the push task with ECRS",
                      "第7日 / Day 7", 820)
    cards = [
        ("E なくす", "Eliminate", "レイアウト変更で押す必要を消す / remove the need to push", MECH),
        ("C まとめる", "Combine", "押出しと検査を同じ動作にする / combine push and inspection", CONTROL),
        ("R 順序・配置", "Rearrange", "投入口を押出し位置の真上へ / place the feed above the push point", SENSOR),
        ("S 簡単にする", "Simplify", "ガイドとストッパで位置決め / guide and stopper instead of skill", ENERGY),
    ]
    for index, (ja, en, sub, color) in enumerate(cards):
        svg.card(70 + index * 330, 220, 300, 200, ja, en, sub=sub, stroke=color, accent=color)
        if index < 3:
            svg.line(370 + index * 330, 320, 396 + index * 330, 320, stroke=color, sw=2.4)
    svg.text(70, 490, "設備投資の前に / before capital investment", 20, 700, INK)
    steps = [
        ("現状 / current", "人が毎回押す / manual push"),
        ("E・C・R / eliminate, combine, rearrange", "押す回数を減らす / fewer pushes"),
        ("S・設備 / simplify, equipment", "残った動作だけ自動化 / automate what remains"),
    ]
    chain(svg, steps, 520, 120, x0=70, x1=1230, gap=40, accent=MECH)
    svg.rect(1260, 520, 110, 120, fill=FILL_HAZARD, stroke=HAZARD, sw=1.6, rx=8)
    svg.text(1315, 565, "投資", 18, 700, HAZARD, "middle")
    svg.text(1315, 588, "invest", 13, 400, HAZARD, "middle")
    svg.text(1315, 615, "最後", 13, 400, HAZARD, "middle")
    svg.footer("E・C・Rを先に検討すると、設備費と工数を減らせる場合がある。 / E, C and R first can reduce both cost and effort.",
               "Eliminate, combine and rearrange before buying equipment.")
    return svg


def d07_03() -> Svg:
    svg = new_diagram("D07-03", "タクト・サイクル・実力能力", "Takt, cycle and effective capacity",
                      "第7日 / Day 7", 900)
    panel(svg, 70, 190, 620, 300, "時間の関係 / time relationship", "target pace versus machine cycle")
    svg.line(110, 330, 640, 330, stroke=MUTED, sw=3)
    svg.text(110, 305, "0 s", 14, 400, MUTED)
    svg.text(640, 305, "42 s", 14, 400, MUTED)
    svg.rect(110, 345, 530, 22, fill=FILL_DATA, stroke=DATA, sw=1.4, rx=4)
    svg.text(375, 362, "タクトタイム 42 s/個（目標）/ takt, target", 14, 600, DATA, "middle")
    svg.rect(110, 390, 189, 22, fill=FILL_MECH, stroke=MECH, sw=1.4, rx=4)
    svg.text(205, 407, "サイクル 15 s/個 / cycle", 13, 600, MECH, "middle")
    svg.text(110, 450, "サイクル < タクト でも、停止と不良を別に考える。", 15, 600, INK)
    svg.text(110, 474, "Cycle < takt, but downtime and defects must still be counted.", 13, 400, MUTED)

    panel(svg, 720, 190, 650, 300, "能力の計算 / capacity calculation", "theoretical, effective and required")
    bar(svg, 760, 250, 110, 150, 240, 260, MECH, "理論 240", "theoretical /h")
    bar(svg, 930, 250, 110, 150, 199.92, 260, DATA, "実力 199.92", "effective /h")
    bar(svg, 1100, 250, 110, 150, 85.71, 260, SENSOR, "必要 85.71", "required /h")
    svg.text(760, 470, "実力 = 3600/15 × 0.85 × 0.98 = 199.92 個/時", 15, 600, INK)
    svg.text(760, 492, "effective = theoretical × availability × good yield", 13, 400, MUTED)

    svg.rect(70, 540, 1300, 110, fill=FILL_SENSOR, stroke=SENSOR, sw=1.6, rx=10)
    svg.text(90, 575, "余裕の読み方 / reading the margin", 17, 700, SENSOR)
    svg.text(90, 605, "必要 85.71 個/時 < 実力 199.92 個/時。ただし、これは仮定値であり、実測ではない。",
             15, 400, INK)
    svg.text(90, 630, "The requirement is below the effective capacity, but the inputs are assumptions, not measurements.",
             13, 400, MUTED)
    legend_swatches(svg, 70, 700, [
        (DATA, "タクト・実力 / takt and effective"),
        (MECH, "サイクル・理論 / cycle and theoretical"),
        (SENSOR, "必要能力 / required"),
        (HAZARD, "過信しない / do not over-trust"),
    ])
    svg.footer("3つの時間と能力を混ぜない。タクトは目標、サイクルは実力、実力能力は停止と不良を含む。",
               "Keep takt, cycle and effective capacity separate. Only effective capacity includes downtime and defects.")
    return svg


def d07_04() -> Svg:
    svg = new_diagram("D07-04", "手動・空圧・電動の3案比較", "Manual, pneumatic and electric concepts",
                      "第7日 / Day 7", 860)
    columns = [
        ("A 手動治具", "Manual fixture", [
            "ガイド・ストッパ・レバー / guide, stopper, lever",
            "初期費用 低 / low initial cost",
            "人手が残る / person remains",
            "安全: 手と工具 / hands and tools",
        ], MECH),
        ("B 空圧半自動", "Pneumatic semi-auto", [
            "シリンダ・弁・センサー・PLC / cylinder, valve, sensor, PLC",
            "初期費用 中 / medium cost",
            "2点間反復が得意 / good for two positions",
            "安全: 手と可動部の分離 / separate hand from motion",
        ], CONTROL),
        ("C 電動全自動", "Electric full-auto", [
            "電動アクチュエータ・供給・検査 / electric actuator, feed, inspection",
            "初期費用 高 / high cost",
            "多点・高能力 / multiple positions, high rate",
            "安全: 危険源が増える / more hazards",
        ], ENERGY),
    ]
    for index, (ja, en, bullets, color) in enumerate(columns):
        x = 70 + index * 440
        svg.rect(x, 210, 400, 360, fill=CARD, stroke=color, sw=2, rx=12)
        svg.rect(x, 210, 400, 74, fill=color, stroke=color, sw=2, rx=12)
        svg.text(x + 20, 242, ja, 23, 700, "white")
        svg.text(x + 20, 268, en, 15, 400, "white")
        for row, bullet in enumerate(bullets):
            cursor = 318 + row * 58
            for line in _wrap("• " + bullet, 356, 13):
                svg.text(x + 20, cursor, line, 13, 400, INK)
                cursor += 18
    svg.rect(70, 610, 1300, 100, fill=JP_BG, stroke=ACCENT, sw=1.6, rx=10)
    svg.text(90, 645, "同じ評価軸で比べる / compare on the same criteria", 17, 700, INK)
    svg.text(90, 675, "初期費用・省人・品種変更・復旧性・安全・設置スペース・保守・納期",
             14, 400, INK)
    svg.text(90, 697, "initial cost, labour saving, flexibility, recovery, safety, space, maintenance, lead time",
             12, 400, MUTED)
    svg.footer("方式名ではなく「何を人に残すか」で比較する。必須の安全要求を満たさない案は、点数が高くても採用しない。",
               "Compare what remains with the person, not the technology label. A concept that fails a mandatory safety requirement is not selected.")
    return svg


def d07_05() -> Svg:
    svg = new_diagram("D07-05", "要求から受入までの流れ", "From requirement to acceptance",
                      "第7日 / Day 7", 820)
    items = [
        ("現場の困りごと", "shop-floor problem", "事実と測定値 / facts and measurements", MECH),
        ("要求", "requirement", "何を達成するか / what must be achieved", CONTROL),
        ("測定方法", "measurement method", "何を、どの条件で測るか / what and under which condition", SENSOR),
        ("合格条件", "acceptance criterion", "誰が見ても合否を判断できる / another person can judge", ENERGY),
    ]
    chain(svg, items, 230, 170, x0=70, x1=1370, gap=34)
    svg.rect(70, 470, 620, 210, fill=FILL_SENSOR, stroke=SENSOR, sw=1.6, rx=10)
    svg.text(90, 505, "良い受入基準 / a good criterion", 18, 700, SENSOR)
    svg.text(90, 545, "後退端で停止したとき、押出し面の位置が", 15, 400, INK)
    svg.text(90, 570, "基準面から ±2 mm 以内。10回連続で測り、", 15, 400, INK)
    svg.text(90, 595, "10回すべて合格。", 15, 400, INK)
    svg.text(90, 635, "Measurand + condition + range + sample size", 13, 400, MUTED)
    svg.rect(710, 470, 660, 210, fill=FILL_HAZARD, stroke=HAZARD, sw=1.6, rx=10)
    svg.text(730, 505, "悪い要求 / a weak requirement", 18, 700, HAZARD)
    svg.text(730, 545, "「速く動く」「安全」「簡単に交換」", 16, 400, INK)
    svg.text(730, 575, "これでは合否を判断できない。", 14, 400, INK)
    svg.text(730, 615, "測定方法・条件・回数・合格範囲を決める。", 14, 600, HAZARD)
    svg.text(730, 640, "Define method, condition, sample size and pass range.", 12, 400, MUTED)
    svg.footer("要求は、測定方法と合格条件が決まって初めて検証できる。 / A requirement is verifiable only when its measurement and pass condition are defined.",
               "Write requirements so that another person can judge pass or fail.")
    return svg


def d07_06() -> Svg:
    svg = new_diagram("D07-06", "押出し装置の機械構成", "Annotated architecture of the pusher machine",
                      "第7日 / Day 7", 1000)
    # frame and guide
    svg.rect(120, 600, 1100, 28, fill=FILL_MECH, stroke=MECH, sw=2.4, rx=4)
    svg.text(130, 623, "フレーム / frame", 14, 600, MECH)
    svg.line(240, 505, 900, 505, stroke=MECH, sw=4, marker=False)
    svg.text(250, 545, "ガイド / guide", 14, 600, MECH)
    # cylinder drawn explicitly so the rod direction is unambiguous
    svg.rect(180, 400, 250, 90, fill=FILL_MECH, stroke=MECH, sw=2.4, rx=8)
    svg.rect(298, 408, 14, 74, fill=MECH, stroke=MECH, sw=1)
    svg.rect(312, 437, 198, 16, fill="#B9C9D9", stroke=MECH, sw=1.4, rx=3)
    svg.text(305, 382, "複動シリンダ / double-acting cylinder", 13, 700, INK, "middle")
    svg.rect(200, 392, 22, 8, fill=CARD, stroke=ENERGY, sw=1.2, rx=1)
    svg.rect(330, 392, 22, 8, fill=CARD, stroke=ENERGY, sw=1.2, rx=1)
    svg.text(211, 386, "A", 10, 700, ENERGY, "middle")
    svg.text(341, 386, "B", 10, 700, ENERGY, "middle")
    # pusher and workpiece
    svg.rect(510, 440, 120, 50, fill="#D7E4F0", stroke=MECH, sw=1.6, rx=4)
    svg.text(570, 470, "押し板 / pusher", 12, 700, INK, "middle")
    svg.rect(670, 425, 130, 65, fill="#F2E6D0", stroke=WARN, sw=2, rx=4)
    svg.text(735, 453, "ワーク", 13, 700, INK, "middle")
    svg.text(735, 472, "workpiece", 11, 400, MUTED, "middle")
    svg.text(735, 404, "8 kg（仮）/ hypothetical", 11, 400, MUTED, "middle")
    # sensors near the guide, with adjacent labels
    for x, label in ((500, "X2 後退端 / retracted"), (810, "X3 前進端 / extended")):
        svg.rect(x, 518, 46, 24, fill=FILL_SENSOR, stroke=SENSOR, sw=1.8, rx=4)
        svg.text(x + 23, 535, "S", 13, 700, SENSOR, "middle")
        svg.text(x + 56, 536, label, 10, 600, SENSOR)
    # hazard at the pinch point
    hazard_marker(svg, 640, 360)
    svg.text(640, 310, "挟まれ / pinch point", 12, 700, HAZARD, "middle")
    # valve and controller
    valve_symbol(svg, 180, 700, "電磁弁 / solenoid valve", "")
    svg.rect(880, 680, 300, 110, fill=FILL_CONTROL, stroke=CONTROL, sw=2, rx=8)
    svg.text(1030, 715, "PLC / 制御器", 18, 700, CONTROL, "middle")
    svg.text(1030, 740, "X0-X3 / Y0-Y2 / T0", 14, 400, INK, "middle")
    svg.text(1030, 766, "fictional training addresses", 12, 400, MUTED, "middle")
    # energy and signal lines
    svg.line(390, 760, 390, 470, stroke=ENERGY, sw=2.4, dash="8 6", marker=False)
    svg.line(390, 470, 341, 470, stroke=ENERGY, sw=2.4, dash="8 6", marker=False)
    svg.line(341, 470, 341, 404, stroke=ENERGY, sw=2.4, dash="8 6")
    svg.line(390, 760, 880, 760, stroke=ENERGY, sw=2.4, dash="8 6", marker=False)
    svg.text(450, 785, "圧縮空気 / compressed air (conceptual)", 12, 600, ENERGY)
    svg.line(1010, 678, 1010, 745, stroke=CONTROL, sw=2, dash="3 5", marker=False)
    svg.line(1010, 745, 400, 745, stroke=CONTROL, sw=2, dash="3 5")
    svg.text(700, 732, "制御信号 / control signal", 11, 600, CONTROL)
    # legend as a single bilingual line
    svg.rect(70, 855, 1300, 64, fill=JP_BG, stroke=ACCENT, sw=1, rx=6)
    svg.text(90, 880, "凡例 / legend: 青=機械 / mechanical・緑=センサー / sensing・紫=制御 / control・橙=エネルギー / energy・赤=危険 / hazard",
             12, 600, INK)
    svg.text(90, 902, "色だけでなく、形・線種・ラベルでも区別する。 / Distinguish by shape, line style and labels, not colour alone.", 10, 400, MUTED)
    svg.footer("シリンダは動かす、ガイドは案内する、センサーは状態を測る、弁はエネルギーを切り替える、PLCは信号を出す。",
               "The cylinder moves, the guide aligns, the sensor measures state, the valve switches energy and the PLC issues signals.")
    return svg


def d07_07() -> Svg:
    svg = new_diagram("D07-07", "機能的な空圧回路（概念）", "Functional pneumatic circuit (concept)",
                      "第7日 / Day 7", 980)
    # air source
    svg.circle(130, 330, 46, fill=FILL_ENERGY, stroke=ENERGY, sw=2.4)
    svg.text(130, 325, "空気源", 15, 700, ENERGY, "middle")
    svg.text(130, 345, "air source", 11, 400, ENERGY, "middle")
    # isolation valve
    svg.rect(230, 300, 80, 60, fill=CARD, stroke=ENERGY, sw=2, rx=4)
    svg.line(245, 330, 295, 330, stroke=ENERGY, sw=2, marker=False)
    svg.line(245, 345, 295, 315, stroke=ENERGY, sw=2, marker=False)
    svg.text(270, 388, "遮断・ロック", 13, 700, ENERGY, "middle")
    svg.text(270, 406, "isolation", 11, 400, MUTED, "middle")
    # FRL
    svg.rect(360, 280, 150, 100, fill=CARD, stroke=ENERGY, sw=2, rx=4)
    svg.text(435, 315, "フィルタ", 13, 700, ENERGY, "middle")
    svg.text(435, 335, "レギュレータ", 13, 700, ENERGY, "middle")
    svg.text(435, 355, "FRL", 14, 700, ENERGY, "middle")
    svg.circle(435, 365, 0.1)
    # gauge
    svg.circle(435, 405, 18, fill=CARD, stroke=ENERGY, sw=1.6)
    svg.text(435, 410, "P", 12, 700, ENERGY, "middle")
    # valve
    valve_symbol(svg, 640, 280, "方向切替弁 / directional valve", "")
    svg.text(745, 440, "5/2 単一ソレノイド・ばね戻り（機能表現）", 12, 600, ENERGY, "middle")
    svg.text(745, 458, "functional representation, not ISO 1219-1", 10, 400, MUTED, "middle")
    # cylinder
    cylinder_symbol(svg, 1030, 250, 330, 110, rod=40, ja="", en="")
    svg.text(1195, 236, "複動シリンダ / double-acting cylinder", 14, 700, INK, "middle")
    # lines
    svg.line(176, 330, 230, 330, stroke=ENERGY, sw=2.4)
    svg.line(310, 330, 360, 330, stroke=ENERGY, sw=2.4)
    svg.line(510, 330, 640, 330, stroke=ENERGY, sw=2.4)
    svg.line(850, 290, 1030, 290, stroke=ENERGY, sw=2.4)
    svg.line(850, 340, 1030, 340, stroke=ENERGY, sw=2.4)
    # flow controls
    for y, label in ((290, "FC-A"), (340, "FC-B")):
        svg.rect(895, y - 12, 40, 24, fill=CARD, stroke=ENERGY, sw=1.6, rx=2)
        svg.parts.append(
            f'<path d="M905 {y - 6} L925 {y + 6}" stroke="{ENERGY}" stroke-width="1.6"/>'
            f'<path d="M905 {y + 6} L925 {y - 6}" stroke="{ENERGY}" stroke-width="1.6"/>'
        )
        svg.text(915, y - 18, label, 10, 600, ENERGY, "middle")
    # exhaust
    svg.line(745, 390, 745, 455, stroke=ENERGY, sw=2, dash="7 5")
    svg.text(765, 478, "排気 / exhaust", 12, 600, ENERGY)
    # position sensors
    for x, label in ((1080, "前進端 / extended"), (1250, "後退端 / retracted")):
        svg.rect(x, 400, 80, 30, fill=FILL_SENSOR, stroke=SENSOR, sw=1.8, rx=3)
        svg.text(x + 40, 420, "S", 14, 700, SENSOR, "middle")
        svg.text(x + 40, 455, label, 11, 600, SENSOR, "middle")
    # bleed
    svg.line(310, 360, 310, 500, stroke=ENERGY, sw=2, dash="6 5")
    svg.circle(310, 508, 8, fill=CARD, stroke=ENERGY, sw=1.6)
    svg.text(325, 514, "残圧排気 / bleed", 12, 600, ENERGY)
    # notes
    svg.rect(70, 560, 1300, 210, fill=FILL_HAZARD, stroke=HAZARD, sw=1.4, rx=10)
    svg.text(90, 595, "この図は概念です。実配管・弁型式・安全設計を確定するものではありません。", 16, 700, HAZARD)
    svg.text(90, 622, "This is a concept. It does not define piping, valve model or safety design.", 13, 400, MUTED)
    svg.text(90, 655, "・無通電の弁位置は機種で異なる。負荷・配管・トラップ空気で動き方が変わる。", 14, 400, INK)
    svg.text(90, 680, "・遮断しただけでは残圧は抜けない。排気と零確認が必要。", 14, 400, INK)
    svg.text(90, 705, "・電磁弁をOFFにしても、シリンダが安全な状態になる保証はない。", 14, 600, HAZARD)
    svg.text(90, 730, "De-energising a solenoid does not guarantee a safe cylinder state.", 12, 400, MUTED)
    legend_swatches(svg, 1100, 560, [])
    svg.footer("空気は 発生→遮断→空気準備→方向切替→速度制御→シリンダ の順に流れる。遮断・排気・零確認は別の対策。",
               "Air flows source, isolation, preparation, directional valve, flow control, cylinder. Isolation, bleed and zero verification are separate measures.")
    return svg


def d07_08() -> Svg:
    svg = new_diagram("D07-08", "ガイドと側荷重", "Guides and side load",
                      "第7日 / Day 7", 860)
    # correct arrangement
    panel(svg, 70, 190, 620, 380, "正しい: ガイドで受ける", "correct: the guide carries the load")
    svg.rect(120, 400, 480, 30, fill=FILL_MECH, stroke=MECH, sw=2, rx=3)
    svg.text(360, 425, "ガイドレール / guide rail", 13, 600, MECH, "middle")
    svg.rect(300, 330, 120, 70, fill="#D7E4F0", stroke=MECH, sw=2, rx=4)
    svg.text(360, 370, "押し板 / pusher", 13, 700, INK, "middle")
    svg.rect(220, 250, 280, 60, fill="#F2E6D0", stroke=WARN, sw=2, rx=4)
    svg.text(360, 286, "ワーク / workpiece", 13, 700, INK, "middle")
    svg.line(360, 310, 360, 330, stroke=HAZARD, sw=3)
    svg.text(455, 315, "重心 / centre of gravity", 12, 600, HAZARD)
    svg.line(240, 400, 240, 345, stroke=SENSOR, sw=2.4)
    svg.line(540, 400, 540, 345, stroke=SENSOR, sw=2.4)
    svg.text(250, 440, "反力 / reaction", 12, 600, SENSOR)
    svg.text(475, 440, "反力 / reaction", 12, 600, SENSOR)
    # wrong arrangement
    panel(svg, 720, 190, 650, 380, "不適切: ロッドで受ける", "incorrect: the rod carries the load")
    svg.rect(760, 400, 560, 30, fill=FILL_MECH, stroke=MECH, sw=2, rx=3)
    svg.rect(1000, 350, 18, 50, fill=MECH, stroke=MECH, sw=1)
    svg.rect(820, 250, 260, 70, fill="#F2E6D0", stroke=WARN, sw=2, rx=4)
    svg.text(950, 290, "長い押し板 / long pusher", 13, 700, INK, "middle")
    svg.line(950, 320, 950, 350, stroke=MECH, sw=4)
    svg.parts.append(
        f'<path d="M1009 300 q70 40 -20 80" fill="none" stroke="{HAZARD}" stroke-width="3" stroke-dasharray="7 5"/>'
    )
    svg.text(1085, 320, "曲げモーメント", 13, 700, HAZARD)
    svg.text(1085, 340, "bending moment", 11, 400, MUTED)
    hazard_marker(svg, 1010, 470)
    svg.text(1060, 500, "シール・ロッド損傷 / seal and rod damage", 12, 600, HAZARD)
    # formula
    svg.rect(70, 610, 1300, 90, fill=JP_BG, stroke=ACCENT, sw=1.4, rx=8)
    svg.text(90, 645, "M = F × L   （F: 横荷重 [N], L: 距離 [m], M: モーメント [N·m]）", 16, 700, INK)
    svg.text(90, 672, "Side load creates a moment. Support it with the guide, not with the cylinder rod.", 13, 400, MUTED)
    svg.footer("ワークの質量と回転はガイドに負担させる。ロッドは横荷重を受ける部品ではない。",
               "Let the guide carry mass and rotation. The cylinder rod is not a side-load bearing.")
    return svg


def d07_09() -> Svg:
    svg = new_diagram("D07-09", "力のつり合いと内径選定", "Free body and bore selection",
                      "第7日 / Day 7", 900)
    # free body
    panel(svg, 70, 190, 560, 360, "ワークに働く力 / forces on the workpiece", "free-body diagram")
    svg.rect(240, 330, 180, 90, fill="#F2E6D0", stroke=WARN, sw=2, rx=4)
    svg.text(330, 380, "m = 8 kg", 15, 700, INK, "middle")
    ax = 330
    ay = 420
    # weight
    svg.line(ax, ay, ax, ay + 80, stroke=HAZARD, sw=3)
    svg.text(ax + 12, ay + 90, "mg = 78.48 N", 13, 600, HAZARD)
    # normal
    svg.line(ax, ay, ax, ay - 70, stroke=SENSOR, sw=3)
    svg.text(ax + 12, ay - 76, "N", 13, 600, SENSOR)
    # push
    svg.line(240, 375, 140, 375, stroke=MECH, sw=3)
    svg.text(150, 355, "F_push", 13, 600, MECH)
    # friction
    svg.line(420, 400, 520, 400, stroke=ENERGY, sw=3)
    svg.text(430, 430, "F_friction = μmg", 12, 600, ENERGY)
    svg.text(110, 510, "F_friction = 0.25 × 8 × 9.81 = 19.62 N", 13, 600, INK)
    # bore graph
    panel(svg, 670, 190, 700, 360, "内径と理論推力 / bore and theoretical force", "at 0.4 MPa, push side")
    axis_x, axis_y = 720, 470
    svg.line(axis_x, axis_y, 1320, axis_y, stroke=MUTED, sw=2, marker=False)
    svg.line(axis_x, axis_y, axis_x, 250, stroke=MUTED, sw=2, marker=False)
    svg.text(1320, 492, "内径 / bore [mm]", 13, 400, MUTED, "end")
    svg.text(700, 250, "力 [N]", 13, 400, MUTED, "end")
    for bore in (12, 16, 20, 25, 32, 40):
        x = axis_x + (bore - 10) * 17
        force = 0.4e6 * 3.141592653589793 * (bore / 1000) ** 2 / 4
        y = axis_y - force * 1.35
        svg.circle(x, y, 5, fill=MECH, stroke=MECH, sw=1)
        svg.text(x, y - 12, f"{bore}", 11, 400, MUTED, "middle")
    svg.line(axis_x, axis_y - 39.24 * 1.35, 1320, axis_y - 39.24 * 1.35, stroke=HAZARD, sw=1.8, dash="7 5")
    svg.text(1240, axis_y - 39.24 * 1.35 - 8, "設計力 39.24 N", 12, 600, HAZARD, "end")
    svg.text(1120, 520, "理論内径 11.18 mm は下限。", 13, 600, INK, "end")
    svg.text(1120, 542, "カタログ選定ではない。", 13, 600, HAZARD, "end")
    # selection chain
    svg.rect(70, 610, 1300, 100, fill=FILL_SENSOR, stroke=SENSOR, sw=1.4, rx=8)
    svg.text(90, 645, "力 → 設計力 → 理論内径 → 候補 → 負荷率・速度・モーメント・圧力損失・センサー → 未確認記録",
             15, 700, INK)
    svg.text(90, 670, "force → design force → theoretical bore → candidates → load factor, speed, moment, pressure loss, sensing → open items",
             12, 400, MUTED)
    svg.text(90, 696, "11.18 mm を超える最小内径をそのまま選ぶ、という意味ではない。 / It does not mean choosing the smallest bore above 11.18 mm.",
             13, 600, HAZARD)
    svg.footer("質量と力を区別し、摩擦力・余裕係数・圧力から理論下限を出す。カタログ選定は別の作業。",
               "Distinguish mass from force, then derive a theoretical lower bound. Catalogue selection is a separate task.")
    return svg


# --------------------------------------------------------------------------- #
# Day 8
# --------------------------------------------------------------------------- #
def d08_01() -> Svg:
    svg = new_diagram("D08-01", "電圧・電流・抵抗のアナロジー", "Voltage, current and resistance analogy",
                      "第8日 / Day 8", 840)
    panel(svg, 70, 190, 600, 380, "水路 / water circuit", "head, flow and restriction")
    svg.rect(120, 250, 180, 130, fill=FILL_DATA, stroke=DATA, sw=2, rx=4)
    svg.rect(120, 250, 180, 70, fill="#BEE3EA", stroke=DATA, sw=1)
    svg.text(210, 290, "水位差 h", 15, 700, DATA, "middle")
    svg.text(210, 312, "head", 12, 400, MUTED, "middle")
    svg.line(300, 340, 420, 340, stroke=DATA, sw=8)
    svg.line(420, 340, 420, 420, stroke=DATA, sw=8)
    svg.line(420, 420, 300, 420, stroke=DATA, sw=8)
    svg.rect(380, 360, 30, 40, fill=CARD, stroke=DATA, sw=1.6, rx=3)
    svg.text(440, 370, "流量 Q", 14, 700, DATA)
    svg.text(440, 390, "flow", 11, 400, MUTED)
    svg.text(340, 462, "管の狭さ = 抵抗 / restriction", 13, 600, INK, "middle")
    svg.text(210, 500, "水位差 → 電圧、流量 → 電流、狭さ → 抵抗", 13, 400, INK, "middle")

    panel(svg, 710, 190, 660, 380, "電気回路 / electrical circuit", "battery, lamp and current")
    svg.rect(760, 270, 80, 150, fill=CARD, stroke=ENERGY, sw=2, rx=3)
    svg.text(800, 320, "24 V", 15, 700, ENERGY, "middle")
    svg.text(800, 342, "電源", 13, 700, ENERGY, "middle")
    svg.line(840, 285, 1180, 285, stroke=ENERGY, sw=3)
    svg.line(840, 405, 1180, 405, stroke=ENERGY, sw=3)
    svg.circle(1180, 345, 58, fill=FILL_MECH, stroke=MECH, sw=2)
    svg.text(1180, 340, "負荷", 14, 700, MECH, "middle")
    svg.text(1180, 360, "lamp", 12, 400, MUTED, "middle")
    svg.line(1180, 285, 1180, 287, stroke=ENERGY, sw=2, marker=False)
    svg.text(900, 268, "I = 0.25 A →", 14, 700, DATA)
    svg.text(760, 470, "V = I × R        P = V × I", 18, 700, INK)
    svg.text(760, 498, "24 V × 0.25 A = 6 W", 14, 400, MUTED)
    svg.rect(760, 520, 560, 42, fill=JP_BG, stroke=ACCENT, sw=1, rx=4)
    svg.text(775, 539, "アナロジーは直感用。電流は閉回路を流れて戻る。", 12, 400, INK)
    svg.text(775, 555, "Analogy only; current returns in a closed loop.", 10, 400, MUTED)

    svg.rect(70, 610, 1300, 80, fill=FILL_HAZARD, stroke=HAZARD, sw=1.4, rx=8)
    svg.text(90, 642, "アナロジーの限界: 電圧は2点間の差、交流は向きが変わる、コイルは逆起電力を生む。", 14, 600, HAZARD)
    svg.text(90, 666, "Limits: voltage is a difference between two points; AC changes direction; coils produce back-EMF.", 12, 400, MUTED)
    svg.footer("電圧は電位差、電流は電荷の流れ、抵抗は流れにくさ、電力はエネルギーの移動速度。",
               "Voltage is a potential difference, current is charge flow, resistance opposes flow and power is the rate of energy transfer.")
    return svg


def d08_02() -> Svg:
    svg = new_diagram("D08-02", "DC24Vの電力供給と保護", "DC24V distribution and protection",
                      "第8日 / Day 8", 900)
    # supply
    svg.rect(80, 300, 150, 150, fill=FILL_ENERGY, stroke=ENERGY, sw=2.2, rx=8)
    svg.text(155, 350, "DC24V", 18, 700, ENERGY, "middle")
    svg.text(155, 374, "電源", 14, 700, ENERGY, "middle")
    svg.text(155, 398, "supply", 12, 400, MUTED, "middle")
    # breaker
    svg.rect(280, 330, 90, 90, fill=CARD, stroke=ENERGY, sw=2, rx=4)
    svg.text(325, 365, "遮断器", 13, 700, ENERGY, "middle")
    svg.text(325, 385, "breaker", 11, 400, MUTED, "middle")
    svg.parts.append(f'<path d="M310 405 L345 355" stroke="{ENERGY}" stroke-width="2"/>')
    # terminal block
    svg.rect(420, 300, 150, 160, fill=CARD, stroke=ACCENT, sw=2, rx=6)
    svg.text(495, 335, "端子台", 15, 700, ACCENT, "middle")
    svg.text(495, 355, "terminals", 11, 400, MUTED, "middle")
    for i in range(4):
        svg.rect(440, 375 + i * 20, 110, 10, fill=JP_BG, stroke=GRID, sw=1, rx=2)
    # branches
    branches = [
        ("PLC", CONTROL, 240, "X/Y"),
        ("センサー", SENSOR, 320, "0.06 A ×3"),
        ("ランプ", WARN, 400, "3 W ×2"),
        ("電磁弁", ENERGY, 480, "0.15 A ×2"),
    ]
    for index, (ja, color, y, note) in enumerate(branches):
        svg.rect(760, y, 250, 58, fill=CARD, stroke=color, sw=2, rx=6)
        svg.text(775, y + 24, ja, 15, 700, color)
        svg.text(775, y + 44, note, 11, 400, MUTED)
        svg.line(570, 380, 700, 380, stroke=ENERGY, sw=2, marker=False)
        svg.line(700, 380, 700, y + 29, stroke=ENERGY, sw=2, marker=False)
        svg.line(700, y + 29, 758, y + 29, stroke=ENERGY, sw=2)
    # return rail
    svg.line(155, 450, 155, 560, stroke=MUTED, sw=3, marker=False)
    svg.line(155, 560, 1010, 560, stroke=MUTED, sw=3, marker=False)
    for y in (269, 349, 429, 509):
        svg.line(1010, y, 1010, 560, stroke=MUTED, sw=2, marker=False)
    svg.text(600, 590, "0V return / 0V帰線", 14, 600, MUTED, "middle")
    # earth
    svg.line(155, 560, 155, 610, stroke=GOOD, sw=2, marker=False)
    svg.line(135, 610, 175, 610, stroke=GOOD, sw=2, marker=False)
    svg.line(142, 620, 168, 620, stroke=GOOD, sw=2, marker=False)
    svg.line(150, 630, 160, 630, stroke=GOOD, sw=2, marker=False)
    svg.text(190, 618, "保護接地 / PE (concept)", 12, 600, GOOD)
    # notes
    svg.rect(70, 660, 1300, 120, fill=JP_BG, stroke=ACCENT, sw=1.4, rx=8)
    svg.text(90, 695, "保護は電線と機器を守る。感電防止とは別。", 15, 700, INK)
    svg.text(90, 718, "定格電圧・電流・遮断容量・電線保護・選択協調を確認する。", 13, 400, INK)
    svg.text(90, 742, "Protection protects wiring and equipment, not people. Check ratings, breaking capacity, wire protection and coordination.", 11, 400, MUTED)
    svg.footer("電源→保護→分岐→負荷。0V帰線と保護接地を忘れない。 / Supply, protection, branches, loads. Do not forget the 0 V return and protective earth.",
               "A DC distribution concept, not a panel construction drawing.")
    return svg


def d08_03() -> Svg:
    svg = new_diagram("D08-03", "スイッチとリレーの違い", "Switch versus relay",
                      "第8日 / Day 8", 830)
    panel(svg, 70, 190, 620, 330, "スイッチ: 人が接点を操作", "switch: a person operates the contact")
    svg.line(130, 270, 530, 270, stroke=ENERGY, sw=3)
    svg.text(150, 255, "+24V", 13, 700, ENERGY)
    svg.line(300, 270, 300, 310, stroke=ENERGY, sw=2, marker=False)
    svg.line(300, 310, 380, 350, stroke=MECH, sw=2.4, marker=False)
    svg.line(380, 310, 300, 350, stroke=MECH, sw=2.4, marker=False)
    svg.text(340, 390, "スイッチ / switch", 13, 700, MECH, "middle")
    svg.circle(480, 320, 30, fill=FILL_MECH, stroke=MECH, sw=2)
    svg.text(480, 325, "負荷", 12, 700, MECH, "middle")
    svg.line(530, 270, 530, 320, stroke=ENERGY, sw=2, marker=False)
    svg.line(480, 350, 480, 420, stroke=MUTED, sw=2, marker=False)
    svg.text(480, 440, "0V", 12, 700, MUTED, "middle")
    svg.text(130, 490, "接点定格・操作頻度・負荷種別を確認する。", 13, 400, INK)

    panel(svg, 710, 190, 660, 330, "リレー: コイルで接点を操作", "relay: a coil operates the contact")
    svg.line(760, 260, 1160, 260, stroke=ENERGY, sw=3)
    svg.text(775, 245, "+24V", 13, 700, ENERGY)
    svg.rect(850, 285, 120, 70, fill=FILL_CONTROL, stroke=CONTROL, sw=2, rx=4)
    svg.text(910, 315, "コイル", 13, 700, CONTROL, "middle")
    svg.text(910, 335, "coil", 11, 400, MUTED, "middle")
    svg.line(910, 260, 910, 285, stroke=ENERGY, sw=2, marker=False)
    svg.line(910, 355, 910, 420, stroke=MUTED, sw=2, marker=False)
    svg.text(910, 440, "0V", 12, 700, MUTED, "middle")
    svg.line(1040, 320, 1130, 320, stroke=CONTROL, sw=2, dash="4 4")
    svg.text(1080, 305, "電磁力", 12, 600, CONTROL, "middle")
    svg.line(1180, 260, 1280, 260, stroke=ENERGY, sw=2, marker=False)
    svg.line(1180, 350, 1280, 350, stroke=ENERGY, sw=2, marker=False)
    svg.line(1180, 260, 1180, 285, stroke=ENERGY, sw=2, marker=False)
    svg.line(1180, 350, 1180, 325, stroke=ENERGY, sw=2, marker=False)
    svg.text(1230, 390, "接点 / contact", 12, 600, MECH, "middle")
    svg.text(760, 490, "小さな信号で大きな負荷を間接操作できる。", 13, 400, INK)
    # truth table
    table_grid(svg, 70, 560, ["物理接点 / contact", "通常 / normal", "操作 / operated"],
               [["NO", "開 / open", "閉 / closed"], ["NC", "閉 / closed", "開 / open"]],
               [360, 250, 250], row_h=38)
    svg.rect(980, 560, 390, 120, fill=FILL_HAZARD, stroke=HAZARD, sw=1.2, rx=8)
    svg.text(1000, 592, "物理NC ≠ ラダーのNC命令", 14, 700, HAZARD)
    svg.text(1000, 616, "physical NC is not automatically", 11, 400, MUTED)
    svg.text(1000, 636, "a logical NC instruction.", 11, 400, MUTED)
    svg.text(1000, 660, "入力のON/OFFで論理を組み立てる。", 12, 600, INK)
    svg.footer("スイッチは直接、リレーはコイルを介して接点を動かす。どちらも接点定格と負荷種別を確認する。",
               "A switch operates a contact directly; a relay uses a coil. Both require contact ratings and load-type checks.")
    return svg


def d08_04() -> Svg:
    svg = new_diagram("D08-04", "PLC出力から負荷まで", "From PLC output to load",
                      "第8日 / Day 8", 850)
    svg.rect(120, 250, 300, 300, fill=FILL_CONTROL, stroke=CONTROL, sw=2.2, rx=10)
    svg.text(270, 290, "PLC", 24, 700, CONTROL, "middle")
    svg.text(270, 316, "program", 12, 400, MUTED, "middle")
    svg.rect(170, 360, 200, 60, fill=CARD, stroke=CONTROL, sw=1.6, rx=4)
    svg.text(270, 388, "出力ユニット", 14, 700, CONTROL, "middle")
    svg.text(270, 407, "relay or transistor", 11, 400, MUTED, "middle")
    svg.text(150, 470, "Y0 / Y1 / Y2", 13, 700, CONTROL)

    # relay output branch
    svg.rect(520, 230, 300, 130, fill=CARD, stroke=MECH, sw=2, rx=8)
    svg.text(670, 262, "リレー出力", 15, 700, MECH, "middle")
    svg.text(670, 282, "relay output", 11, 400, MUTED, "middle")
    svg.text(670, 315, "接点で負荷回路を開閉", 12, 400, INK, "middle")
    svg.text(670, 338, "AC/DC, slower, contact life", 11, 400, MUTED, "middle")

    # transistor output branch
    svg.rect(520, 400, 300, 130, fill=CARD, stroke=SENSOR, sw=2, rx=8)
    svg.text(670, 432, "トランジスタ出力", 15, 700, SENSOR, "middle")
    svg.text(670, 452, "transistor output", 11, 400, MUTED, "middle")
    svg.text(670, 485, "DC負荷, 速い, 漏れ電流", 12, 400, INK, "middle")
    svg.text(670, 508, "DC load, fast, leakage", 11, 400, MUTED, "middle")

    # loads
    for y, label, note in ((255, "ランプ / lamp", "Y0, Y1"), (425, "電磁弁 / solenoid", "Y2 + suppression")):
        svg.rect(900, y - 40, 260, 100, fill=CARD, stroke=ENERGY, sw=2, rx=8)
        svg.text(1030, y - 5, label, 15, 700, ENERGY, "middle")
        svg.text(1030, y + 18, note, 11, 400, MUTED, "middle")
        svg.line(826, y + 10, 896, y + 10, stroke=ENERGY, sw=2.4)
    # signal vs power
    svg.line(420, 320, 516, 295, stroke=CONTROL, sw=2, dash="4 5")
    svg.text(468, 300, "信号", 11, 600, CONTROL, "middle")
    svg.line(1220, 175, 1220, 245, stroke=ENERGY, sw=2.4, dash="8 6")
    svg.line(1220, 245, 1160, 245, stroke=ENERGY, sw=2.4, dash="8 6")
    svg.text(1240, 210, "負荷電源", 12, 600, ENERGY)
    # note
    svg.rect(120, 610, 1200, 90, fill=FILL_HAZARD, stroke=HAZARD, sw=1.4, rx=8)
    svg.text(140, 645, "PLC出力は信号であり、無制限の電源ではない。定格を超える負荷はリレー等で間接操作する。", 15, 700, HAZARD)
    svg.text(140, 670, "A PLC output is a signal, not an unrestricted supply. Use a relay for loads above the rating.", 12, 400, MUTED)
    svg.footer("信号の経路と、負荷に電力を届ける経路を分けて考える。 / Separate the signal path from the power path.",
               "Check per-point and per-common ratings, inrush, surge and leakage.")
    return svg


def d08_05() -> Svg:
    svg = new_diagram("D08-05", "センサーの種類と選び方", "Sensor types and selection",
                      "第8日 / Day 8", 860)
    cards = [
        ("光電 / photoelectric", "物体の有無・通過", "presence and passage",
         "色・反射・透明体・背景 / colour, reflection, transparent target, background", DATA),
        ("誘導形近接 / inductive", "金属の接近・位置", "metal approach and position",
         "対象金属・距離・埋込 / target metal, distance, shielded mounting", SENSOR),
        ("静電容量形 / capacitive", "金属以外の近接", "non-metal proximity",
         "水分・堆積物・感度 / moisture, deposits, sensitivity", SENSOR),
        ("磁気 / magnetic", "シリンダの磁石位置", "cylinder magnet position",
         "対応シリンダ・取付 / compatible cylinder, mounting", CONTROL),
        ("リミット / limit switch", "機械的接触", "mechanical contact",
         "接触力・寿命・位置ずれ / force, life, drift", MECH),
        ("エンコーダ / encoder", "回転・移動量", "rotation and travel",
         "分解能・出力・ノイズ / resolution, output, noise", ENERGY),
    ]
    for index, (ja, ja_sub, en_sub, check, color) in enumerate(cards):
        row, col = divmod(index, 3)
        x = 70 + col * 440
        y = 200 + row * 270
        svg.rect(x, y, 400, 220, fill=CARD, stroke=color, sw=2, rx=10)
        svg.rect(x, y, 8, 220, fill=color, stroke=color, sw=0, rx=3)
        svg.text(x + 26, y + 36, ja, 18, 700, color)
        svg.text(x + 26, y + 62, ja_sub, 14, 700, INK)
        svg.text(x + 26, y + 84, en_sub, 12, 400, MUTED)
        svg.text(x + 26, y + 120, "確認 / check:", 12, 700, INK)
        for line_index, line in enumerate(_wrap(check, 340, 13)):
            svg.text(x + 26, y + 145 + line_index * 20, line, 13, 400, MUTED)
    svg.rect(70, 760, 1300, 70, fill=JP_BG, stroke=ACCENT, sw=1.2, rx=8)
    svg.text(90, 790, "選定5ステップ: 対象 → 距離・応答 → 対象物と背景 → 取付・環境 → 信号・電源",
             14, 700, INK)
    svg.text(90, 812, "Five steps: target, distance and response, target and background, mounting and environment, signal and supply.",
             11, 400, MUTED)
    svg.footer("方式名ではなく、対象物・環境・信号方式で選ぶ。迷ったら実物で最悪条件を試す。",
               "Select by target, environment and signal type, not by technology name. Test the worst case with the real target.")
    return svg


def _wrap(text: str, max_width: float, size: float) -> list[str]:
    lines = []
    current = ""
    for char in text:
        if current and text_width(current + char, size) > max_width:
            lines.append(current)
            current = char
        else:
            current += char
    if current:
        lines.append(current)
    return lines


def d08_06() -> Svg:
    svg = new_diagram("D08-06", "NPN・PNPとPLC入力の電流経路", "NPN and PNP current paths through PLC inputs",
                      "第8日 / Day 8", 980)
    # ---------------- PNP + sinking input
    panel(svg, 60, 180, 640, 560, "PNP + シンク入力（共通0V）", "")
    svg.text(100, 252, "+24V rail", 13, 700, HAZARD)
    svg.line(100, 265, 650, 265, stroke=HAZARD, sw=3, marker=False)
    svg.line(100, 690, 650, 690, stroke=MUTED, sw=3, marker=False)
    svg.text(110, 715, "0V", 13, 700, MUTED)
    # sensor
    svg.rect(150, 310, 180, 210, fill=FILL_SENSOR, stroke=SENSOR, sw=2, rx=8)
    svg.text(240, 342, "PNP", 20, 700, SENSOR, "middle")
    svg.text(240, 366, "sensor", 12, 400, MUTED, "middle")
    svg.line(200, 265, 200, 310, stroke=HAZARD, sw=2, marker=False)
    svg.text(210, 292, "+", 12, 700, HAZARD)
    svg.line(200, 520, 200, 690, stroke=MUTED, sw=2, marker=False)
    svg.text(210, 560, "0V", 12, 700, MUTED)
    svg.line(330, 410, 430, 410, stroke=SENSOR, sw=3)
    svg.text(352, 392, "OUT", 12, 700, SENSOR)
    # PLC input
    svg.rect(430, 310, 220, 200, fill=FILL_CONTROL, stroke=CONTROL, sw=2, rx=8)
    svg.text(540, 344, "PLC入力", 16, 700, CONTROL, "middle")
    svg.text(540, 366, "sinking input", 11, 400, MUTED, "middle")
    svg.circle(500, 420, 14, fill=CARD, stroke=CONTROL, sw=1.6)
    svg.parts.append(f'<path d="M492 414 L508 414 L500 426 Z" fill="{CONTROL}"/>')
    svg.text(500, 455, "入力回路", 11, 400, CONTROL, "middle")
    # common path to 0 V
    svg.line(650, 470, 650, 690, stroke=MUTED, sw=2.4, marker=False)
    svg.text(600, 500, "COM → 0V", 11, 700, MUTED, "middle")
    # current arrows
    svg.parts.append(f'<path d="M240 270 q0 35 0 35" fill="none" stroke="{HAZARD}" stroke-width="2.4" marker-end="url(#arrow-red)"/>')
    svg.parts.append(f'<path d="M340 400 q40 0 70 0" fill="none" stroke="{HAZARD}" stroke-width="2.4" marker-end="url(#arrow-red)"/>')
    svg.parts.append(f'<path d="M590 460 q30 0 55 0" fill="none" stroke="{HAZARD}" stroke-width="2.4" marker-end="url(#arrow-red)"/>')
    svg.parts.append(f'<path d="M650 540 q0 60 0 60" fill="none" stroke="{HAZARD}" stroke-width="2.4" marker-end="url(#arrow-red)"/>')
    svg.text(150, 600, "電流: +24V → センサー → 出力 → 入力 → COM(0V)", 13, 700, HAZARD)
    svg.text(150, 622, "Current: +24 V → sensor → output → input → COM (0 V)", 11, 400, MUTED)

    # ---------------- NPN + sourcing input
    panel(svg, 740, 180, 640, 560, "NPN + ソース入力（共通+24V）", "")
    svg.text(780, 252, "+24V rail", 13, 700, HAZARD)
    svg.line(780, 265, 1330, 265, stroke=HAZARD, sw=3, marker=False)
    svg.line(780, 690, 1330, 690, stroke=MUTED, sw=3, marker=False)
    svg.text(790, 715, "0V", 13, 700, MUTED)
    # PLC input
    svg.rect(830, 310, 220, 200, fill=FILL_CONTROL, stroke=CONTROL, sw=2, rx=8)
    svg.text(940, 344, "PLC入力", 16, 700, CONTROL, "middle")
    svg.text(940, 366, "sourcing input", 11, 400, MUTED, "middle")
    svg.circle(900, 420, 14, fill=CARD, stroke=CONTROL, sw=1.6)
    svg.parts.append(f'<path d="M892 414 L908 414 L900 426 Z" fill="{CONTROL}"/>')
    svg.line(830, 470, 830, 265, stroke=HAZARD, sw=2.4, marker=False)
    svg.text(780, 300, "COM → +24V", 11, 700, HAZARD)
    # sensor
    svg.rect(1110, 310, 180, 210, fill=FILL_SENSOR, stroke=SENSOR, sw=2, rx=8)
    svg.text(1200, 342, "NPN", 20, 700, SENSOR, "middle")
    svg.text(1200, 366, "sensor", 12, 400, MUTED, "middle")
    svg.line(1240, 265, 1240, 310, stroke=HAZARD, sw=2, marker=False)
    svg.text(1250, 292, "+", 12, 700, HAZARD)
    svg.line(1200, 520, 1200, 690, stroke=MUTED, sw=2, marker=False)
    svg.line(1050, 410, 1110, 410, stroke=SENSOR, sw=3)
    svg.text(1078, 392, "OUT", 12, 700, SENSOR)
    # current arrows
    svg.parts.append(f'<path d="M900 270 q0 35 0 35" fill="none" stroke="{HAZARD}" stroke-width="2.4" marker-end="url(#arrow-red)"/>')
    svg.parts.append(f'<path d="M990 400 q40 0 55 0" fill="none" stroke="{HAZARD}" stroke-width="2.4" marker-end="url(#arrow-red)"/>')
    svg.parts.append(f'<path d="M1180 540 q0 60 0 60" fill="none" stroke="{HAZARD}" stroke-width="2.4" marker-end="url(#arrow-red)"/>')
    svg.text(780, 600, "電流: +24V → COM → 入力 → 出力 → 0V", 13, 700, HAZARD)
    svg.text(780, 622, "Current: +24 V → COM → input → output → 0 V", 11, 400, MUTED)

    svg.rect(60, 770, 1320, 70, fill=FILL_HAZARD, stroke=HAZARD, sw=1.4, rx=8)
    svg.text(80, 800, "どちらも入力共通端子までの閉回路で考える。端子配置はPLCのハードウェアマニュアルで確認する。", 14, 700, HAZARD)
    svg.text(80, 822, "Think in a closed circuit through the input common. Confirm terminal arrangement in the PLC hardware manual.", 11, 400, MUTED)
    svg.footer("PNPはソース、NPNはシンク。PLC入力の共通端子の電位と入力方式で適合が決まる。",
               "PNP sources; NPN sinks. Compatibility depends on the input common potential and input circuit type.")
    return svg


def d08_07() -> Svg:
    svg = new_diagram("D08-07", "統一I/O表と概略配線", "Canonical I/O map and conceptual wiring",
                      "第8日 / Day 8", 980)
    # PLC body
    svg.rect(520, 210, 400, 560, fill=FILL_CONTROL, stroke=CONTROL, sw=2.2, rx=10)
    svg.text(720, 250, "PLC", 26, 700, CONTROL, "middle")
    svg.text(720, 276, "fictional training addresses", 11, 400, MUTED, "middle")
    # input rows
    inputs = [
        ("X0", "START pushbutton", "OFF; ON while pressed"),
        ("X1", "STOP_OK (physical NC)", "ON while healthy"),
        ("X2", "retracted confirmation", "ON at retracted end"),
        ("X3", "extended confirmation", "ON at extended end"),
    ]
    for index, (addr, device, normal) in enumerate(inputs):
        y = 330 + index * 70
        svg.rect(90, y - 24, 380, 58, fill=CARD, stroke=SENSOR, sw=1.6, rx=6)
        svg.text(104, y - 2, f"{addr}  {device}", 13, 700, SENSOR)
        svg.text(104, y + 18, normal, 11, 400, MUTED)
        svg.line(470, y + 5, 520, y + 5, stroke=SENSOR, sw=2)
        svg.text(540, y + 10, f"{addr}", 14, 700, SENSOR)
    svg.text(90, 660, "入力共通 / input common", 13, 700, MUTED)
    svg.line(90, 680, 500, 680, stroke=MUTED, sw=2, marker=False)
    svg.line(500, 680, 500, 610, stroke=MUTED, sw=2, marker=False)
    svg.line(500, 610, 520, 610, stroke=MUTED, sw=2, marker=False)
    # output rows
    outputs = [
        ("Y0", "RUN indicator lamp", "ON while RUN"),
        ("Y1", "delayed indicator lamp", "ON after T0 = 3 s"),
        ("Y2", "extend solenoid command", "OFF = spring return"),
    ]
    for index, (addr, device, normal) in enumerate(outputs):
        y = 330 + index * 80
        svg.rect(970, y - 24, 380, 62, fill=CARD, stroke=ENERGY, sw=1.6, rx=6)
        svg.text(984, y - 2, f"{addr}  {device}", 13, 700, ENERGY)
        svg.text(984, y + 18, normal, 11, 400, MUTED)
        svg.line(920, y + 6, 970, y + 6, stroke=ENERGY, sw=2)
        svg.text(890, y + 11, f"{addr}", 14, 700, ENERGY, "end")
    svg.text(970, 660, "出力共通 / output common", 13, 700, MUTED)
    svg.line(970, 680, 1350, 680, stroke=MUTED, sw=2, marker=False)
    svg.line(920, 680, 920, 610, stroke=MUTED, sw=2, marker=False)
    svg.line(920, 610, 900, 610, stroke=MUTED, sw=2, marker=False)
    # internal state
    svg.rect(560, 390, 320, 60, fill=JP_BG, stroke=CONTROL, sw=1.2, rx=6)
    svg.text(720, 416, "M0 RUN  /  T0 timer", 14, 700, CONTROL, "middle")
    svg.text(720, 436, "internal state, not a terminal", 10, 400, MUTED, "middle")
    # note
    svg.rect(70, 760, 1300, 90, fill=FILL_HAZARD, stroke=HAZARD, sw=1.4, rx=8)
    svg.text(90, 792, "Y1は遅延ランプ専用。電磁弁はY2。アドレスと物理端子番号は別。", 15, 700, HAZARD)
    svg.text(90, 815, "Y1 is only the delayed lamp; the solenoid is Y2. Addresses are not physical terminal numbers.", 11, 400, MUTED)
    svg.text(90, 836, "実機の端子・コモン・保護・接地は、PLCと機器のマニュアルで確認する。", 12, 400, INK)
    svg.footer("Day 8とDay 9で同じI/O表を使う。アドレス・機器・正常状態を一致させる。",
               "Days 8 and 9 use the same I/O table. Keep address, device and normal state consistent.")
    return svg


def d08_08() -> Svg:
    svg = new_diagram("D08-08", "正しい自己保持回路", "Correct self-holding circuit",
                      "第8日 / Day 8", 900)
    # rails
    svg.line(150, 230, 150, 600, stroke=INK, sw=3, marker=False)
    svg.line(1290, 230, 1290, 600, stroke=INK, sw=3, marker=False)
    svg.text(150, 215, "L", 14, 700, INK, "middle")
    svg.text(1290, 215, "N", 14, 700, INK, "middle")
    # rung 1
    y = 320
    svg.line(150, y, 300, y, stroke=INK, sw=2, marker=False)
    svg.line(300, y, 300, y - 70, stroke=INK, sw=2, marker=False)
    svg.line(300, y, 300, y + 70, stroke=INK, sw=2, marker=False)
    svg.line(300, y - 70, 370, y - 70, stroke=INK, sw=2, marker=False)
    svg.line(300, y + 70, 370, y + 70, stroke=INK, sw=2, marker=False)
    ladder_contact(svg, 400, y - 70, False, "X0", "START / 押している間ON")
    ladder_contact(svg, 540, y - 70, False, "X2", "後退端 / start only")
    ladder_contact(svg, 400, y + 70, False, "M0", "保持 / seal-in")
    svg.line(430, y - 70, 510, y - 70, stroke=INK, sw=2, marker=False)
    svg.line(570, y - 70, 700, y - 70, stroke=INK, sw=2, marker=False)
    svg.line(430, y + 70, 700, y + 70, stroke=INK, sw=2, marker=False)
    svg.line(700, y - 70, 700, y + 70, stroke=INK, sw=2, marker=False)
    svg.line(700, y, 880, y, stroke=INK, sw=2, marker=False)
    ladder_contact(svg, 950, y, False, "X1", "停止許可 / stop permission")
    svg.line(880, y, 920, y, stroke=INK, sw=2, marker=False)
    svg.line(980, y, 1072, y, stroke=INK, sw=2, marker=False)
    ladder_coil(svg, 1120, y, "M0", "RUN state")
    svg.line(1182, y, 1290, y, stroke=INK, sw=2, marker=False)
    # rung 2
    y2 = 500
    svg.line(150, y2, 370, y2, stroke=INK, sw=2, marker=False)
    ladder_contact(svg, 400, y2, False, "M0", "RUN")
    svg.line(430, y2, 980, y2, stroke=INK, sw=2, marker=False)
    ladder_contact(svg, 1010, y2, False, "T0.DN", "3 s done")
    svg.line(1040, y2, 1092, y2, stroke=INK, sw=2, marker=False)
    ladder_coil(svg, 1140, y2, "Y1", "delayed lamp")
    svg.line(1202, y2, 1290, y2, stroke=INK, sw=2, marker=False)
    # labels
    svg.rect(70, 620, 1300, 110, fill=JP_BG, stroke=ACCENT, sw=1.2, rx=8)
    svg.text(90, 652, "並列枝: (X0 AND X2) OR M0   直列: X1（停止許可）", 16, 700, INK)
    svg.text(90, 678, "M0の保持枝はX2を通らない。だから前進してX2がOFFになってもRUNを維持できる。", 13, 400, INK)
    svg.text(90, 702, "The M0 seal-in branch does not pass through X2, so RUN survives X2 turning OFF.", 11, 400, MUTED)
    svg.rect(70, 760, 1300, 80, fill=FILL_HAZARD, stroke=HAZARD, sw=1.3, rx=8)
    svg.text(90, 792, "元PDFの31ページには、この並列保持接点がない。STARTを離すとRUNが消える。", 14, 700, HAZARD)
    svg.text(90, 815, "The source PDF page 31 lacks this parallel holding contact, so RUN would drop when START is released.", 11, 400, MUTED)
    svg.footer("STARTを離してもRUNが続く。STOP許可がOFFになるとRUNが落ち、T0もリセットされる。",
               "RUN survives START release. When stop permission goes OFF, RUN drops and T0 resets.")
    return svg


def d08_09() -> Svg:
    svg = new_diagram("D08-09", "状態ベースのシーケンス", "State-based sequence",
                      "第8日 / Day 8", 900)
    positions = {
        "IDLE": (70, 300),
        "READY": (270, 300),
        "EXTEND": (470, 300),
        "WAIT_EXTENDED": (690, 300),
        "RETRACT": (910, 300),
        "WAIT_RETRACTED": (1130, 300),
        "COMPLETE": (1130, 520),
        "FAULT": (620, 560),
    }
    colors = {
        "IDLE": MUTED, "READY": CONTROL, "EXTEND": ENERGY, "WAIT_EXTENDED": SENSOR,
        "RETRACT": ENERGY, "WAIT_RETRACTED": SENSOR, "COMPLETE": GOOD, "FAULT": HAZARD,
    }
    subtitles = {
        "IDLE": "all OFF / fresh START",
        "READY": "Y0 ON / run",
        "EXTEND": "Y2 ON / command",
        "WAIT_EXTENDED": "wait X3 / timeout F001",
        "RETRACT": "Y2 OFF / command",
        "WAIT_RETRACTED": "wait X2 / timeout F003",
        "COMPLETE": "Y0, Y1 / new START",
        "FAULT": "all OFF / reset only",
    }
    for state, (x, y) in positions.items():
        w = 180
        svg.rect(x, y, w, 86, fill=CARD, stroke=colors[state], sw=2.4, rx=10)
        svg.text(x + w / 2, y + 34, state, 14 if len(state) > 12 else 17, 700, colors[state], "middle")
        svg.text(x + w / 2, y + 60, subtitles[state], 10, 400, MUTED, "middle")
    for start, end in (("IDLE", "READY"), ("READY", "EXTEND"), ("EXTEND", "WAIT_EXTENDED"),
                       ("WAIT_EXTENDED", "RETRACT"), ("RETRACT", "WAIT_RETRACTED")):
        x1, y1 = positions[start]
        x2, y2 = positions[end]
        svg.line(x1 + 182, y1 + 43, x2 - 2, y2 + 43, stroke=INK, sw=2)
    # wait retracted -> complete
    svg.line(1300, 388, 1300, 518, stroke=GOOD, sw=2)
    svg.text(1290, 470, "X2 ON, X3 OFF", 10, 600, GOOD, "end")
    # timeouts bus (above COMPLETE, below the top row)
    svg.line(780, 388, 780, 440, stroke=HAZARD, sw=2, dash="6 4", marker=False)
    svg.line(1160, 388, 1160, 440, stroke=HAZARD, sw=2, dash="6 4", marker=False)
    svg.line(780, 440, 1160, 440, stroke=HAZARD, sw=2, dash="6 4", marker=False)
    svg.line(780, 440, 780, 558, stroke=HAZARD, sw=2, dash="6 4")
    svg.text(795, 425, "F001", 10, 700, HAZARD)
    svg.text(1070, 425, "F003", 10, 700, HAZARD)
    # complete -> ready (new START)
    svg.line(1220, 608, 1220, 720, stroke=GOOD, sw=2, marker=False)
    svg.line(1220, 720, 360, 720, stroke=GOOD, sw=2, marker=False)
    svg.line(360, 720, 360, 388, stroke=GOOD, sw=2)
    svg.text(790, 742, "new START / 新しいSTART（位置確認後のみ）", 11, 600, GOOD, "middle")
    # reset -> IDLE
    svg.line(620, 600, 500, 600, stroke=HAZARD, sw=2, marker=False)
    svg.line(500, 600, 500, 670, stroke=HAZARD, sw=2, marker=False)
    svg.line(500, 670, 160, 670, stroke=HAZARD, sw=2, marker=False)
    svg.line(160, 670, 160, 388, stroke=HAZARD, sw=2)
    svg.text(515, 628, "reset + START released", 10, 600, HAZARD)
    svg.text(515, 645, "reset does not start motion", 9, 400, MUTED)
    # note
    svg.rect(70, 775, 1300, 80, fill=JP_BG, stroke=ACCENT, sw=1.2, rx=8)
    svg.text(90, 805, "指令（EXTEND/RETRACT）と確認（WAIT_EXTENDED/WAIT_RETRACTED）を分ける。", 13, 700, INK)
    svg.text(90, 827, "確認が来なければタイムアウトでFAULT。リセットは動作開始ではない。", 11, 400, INK)
    svg.text(90, 845, "A command is not a confirmation. Missing confirmation gives FAULT; reset is not a start.", 10, 400, MUTED)
    svg.footer("状態ごとに出力と遷移条件を決める。位置確認とタイムアウトを状態に含める。",
               "Define outputs and transitions per state. Include position confirmation and timeouts in the states.")
    return svg


def d08_10() -> Svg:
    svg = new_diagram("D08-10", "タイミングチャート", "Timing chart",
                      "第8日 / Day 8", 900)
    # time axis
    x0, x1 = 250, 1330
    svg.line(x0, 780, x1, 780, stroke=MUTED, sw=2, marker=False)
    for second in range(0, 9):
        x = x0 + (x1 - x0) * second / 8
        svg.line(x, 775, x, 785, stroke=MUTED, sw=1.5, marker=False)
        svg.text(x, 805, f"{second}s", 11, 400, MUTED, "middle")
    rows = [
        ("START", [(0, 0.4, 1), (0.4, 8, 0)], CONTROL),
        ("X1 STOP_OK", [(0, 8, 1)], SENSOR),
        ("M0 RUN", [(0.5, 8, 1)], CONTROL),
        ("T0", [(0.5, 3.5, 1), (3.5, 8, 1)], MUTED),
        ("Y1", [(3.5, 8, 1)], GOOD),
        ("Y2 extend", [(0.8, 2.8, 1)], ENERGY),
        ("X3 extended", [(1.8, 3.4, 1)], SENSOR),
    ]
    for index, (label, segments, color) in enumerate(rows):
        y = 220 + index * 72
        svg.text(230, y + 5, label, 13, 700, color, "end")
        svg.line(x0, y + 18, x1, y + 18, stroke=GRID, sw=1, marker=False)
        for start, end, level in segments:
            left = x0 + (x1 - x0) * start / 8
            right = x0 + (x1 - x0) * end / 8
            top = y - 12 if level else y + 18
            svg.line(left, top, right, top, stroke=color, sw=2.6, marker=False)
            if 0 <= start <= 8:
                svg.line(left, y - 12, left, y + 18, stroke=color, sw=1.4, marker=False)
    # annotations
    for second, text in ((0.4, "release"), (1.8, "X3 ON"), (3.5, "3 s"), (3.2, "STOP")):
        x = x0 + (x1 - x0) * second / 8
        svg.line(x, 190, x, 740, stroke=HAZARD, sw=1, dash="3 4", marker=False)
        svg.text(x, 182, text, 11, 600, HAZARD, "middle")
    svg.rect(70, 840, 1300, 46, fill=JP_BG, stroke=ACCENT, sw=1, rx=6)
    svg.text(90, 868, "模式図です。実機の時間はスキャン周期・入力フィルタ・タイマー分解能で変わります。 / Schematic only; real timing depends on scan, filter and timer resolution.",
             11, 400, INK)
    svg.footer("STARTを離してもM0は続く。T0はM0の間だけ進み、3秒でY1がON。STOPで全てリセット。",
               "M0 continues after START release. T0 advances while RUN is on; Y1 turns on at 3 s. STOP resets all.")
    return svg


def d08_11() -> Svg:
    svg = new_diagram("D08-11", "異常処理マトリクス", "Fault handling matrix",
                      "第8日 / Day 8", 880)
    headers = ["異常 / fault", "検出 / detection", "応答 / response", "リセット・再起動 / reset and restart"]
    rows = [
        ["前進端未確認 / extend not confirmed", "WAIT_EXTENDED 3 s 超過", "F001, Y2 OFF, RUN OFF", "原因除去→reset→new START"],
        ["後退端未確認 / retract not confirmed", "WAIT_RETRACTED 3 s 超過", "F003, Y2 OFF, RUN OFF", "原因除去→reset→new START"],
        ["前後端同時ON / both sensors ON", "X2 and X3 both ON", "F002, all outputs OFF", "原因除去→reset→new START"],
        ["停止操作 / stop operated", "X1 OFF", "RUN OFF, Y2 OFF, T0=0", "停止解除→new START"],
        ["停電・復電 / power restore", "initialisation", "outputs OFF, RUN OFF", "new STARTのみ / fresh START only"],
        ["リセット中のSTART / START held", "reset and START ON", "reset refused", "STARTを離す / release START"],
    ]
    table_grid(svg, 60, 190, headers, rows, [360, 300, 300, 330], row_h=72, size=13)
    svg.rect(60, 710, 1290, 100, fill=FILL_HAZARD, stroke=HAZARD, sw=1.4, rx=8)
    svg.text(80, 742, "リセットは動作開始ではない。復電時も、保持ビットや押しっぱなしのSTARTで自動再起動しない。", 14, 700, HAZARD)
    svg.text(80, 765, "Reset is not a start. Power restoration must not restart from a retained bit or a held START.", 11, 400, MUTED)
    svg.text(80, 790, "通常のPLC制御と安全機能は別。この表は安全教育用で、安全PLCの設計ではない。", 12, 600, INK)
    svg.footer("異常の検出・応答・リセット・再起動をセットで設計する。 / Design detection, response, reset and restart together.",
               "A fault response without a restart rule is incomplete.")
    return svg


# --------------------------------------------------------------------------- #
# Day 9
# --------------------------------------------------------------------------- #
def d09_01() -> Svg:
    svg = new_diagram("D09-01", "LANとスイッチ", "LAN and switch",
                      "第9日 / Day 9", 850)
    # switch
    svg.rect(570, 380, 300, 130, fill=FILL_DATA, stroke=DATA, sw=2.4, rx=8)
    svg.text(720, 425, "スイッチ", 20, 700, DATA, "middle")
    svg.text(720, 450, "L2 switch", 13, 400, MUTED, "middle")
    svg.text(720, 478, "同一LAN内を中継", 12, 400, INK, "middle")
    devices = [
        ("PC", "192.168.10.10", 220, 240, DATA),
        ("PLC", "192.168.10.20", 1020, 240, CONTROL),
        ("HMI", "192.168.10.40", 220, 590, SENSOR),
        ("カメラ / camera", "192.168.10.30", 1020, 590, ENERGY),
    ]
    for name, ip, x, y, color in devices:
        svg.rect(x, y, 240, 100, fill=CARD, stroke=color, sw=2, rx=8)
        svg.text(x + 120, y + 34, name, 16, 700, color, "middle")
        svg.text(x + 120, y + 60, ip, 14, 600, INK, "middle")
        svg.text(x + 120, y + 82, "/24", 11, 400, MUTED, "middle")
    svg.line(460, 290, 660, 380, stroke=DATA, sw=2.2)
    svg.line(1020, 290, 780, 380, stroke=DATA, sw=2.2)
    svg.line(460, 640, 660, 510, stroke=DATA, sw=2.2)
    svg.line(1020, 640, 780, 510, stroke=DATA, sw=2.2)
    # router
    svg.rect(1120, 390, 220, 110, fill=CARD, stroke=WARN, sw=2, rx=8)
    svg.text(1230, 425, "ルータ / router", 15, 700, WARN, "middle")
    svg.text(1230, 448, "別ネットワークへ", 11, 400, INK, "middle")
    svg.text(1230, 468, "gateway", 11, 400, MUTED, "middle")
    svg.line(870, 445, 1118, 445, stroke=WARN, sw=2, dash="7 5")
    # legend
    svg.rect(60, 730, 1320, 50, fill=JP_BG, stroke=ACCENT, sw=1, rx=6)
    svg.text(80, 760, "同じスイッチにつながっていても、別サブネットなら通常はルータが必要。 / A shared switch does not remove the need for a router between subnets.",
             12, 400, INK)
    svg.footer("スイッチは同一LAN内を中継し、ルータは別ネットワークへつなぐ。IPとマスクで到達範囲が決まる。",
               "A switch forwards within a LAN; a router connects networks. IP and mask define reachability.")
    return svg


def d09_02() -> Svg:
    svg = new_diagram("D09-02", "IPv4とサブネットマスク", "IPv4 and subnet masks",
                      "第9日 / Day 9", 900)
    # octet bar
    svg.text(70, 205, "IPv4 = 32ビット = 4オクテット / 32 bits in four octets", 16, 700, INK)
    for index, octet in enumerate(("192", "168", "10", "20")):
        x = 70 + index * 240
        svg.rect(x, 225, 240, 70, fill=FILL_DATA if index < 3 else FILL_CONTROL,
                 stroke=DATA if index < 3 else CONTROL, sw=1.6, rx=4)
        svg.text(x + 120, 260, octet, 22, 700, INK, "middle")
        svg.text(x + 120, 284, f"octet {index + 1}", 10, 400, MUTED, "middle")
    # /24 bar
    svg.text(70, 350, "/24: 先頭24ビットがネットワーク部 / first 24 bits are network", 15, 700, INK)
    svg.rect(70, 370, 720, 34, fill=FILL_DATA, stroke=DATA, sw=1.4, rx=3)
    svg.rect(790, 370, 240, 34, fill=FILL_CONTROL, stroke=CONTROL, sw=1.4, rx=3)
    svg.text(430, 394, "network 192.168.10", 13, 700, INK, "middle")
    svg.text(910, 394, "host 0-255", 13, 700, CONTROL, "middle")
    # /25 bar
    svg.text(70, 455, "/25: ネットワーク部が25ビットに増える / the network part grows to 25 bits", 15, 700, INK)
    svg.rect(70, 475, 480, 34, fill=FILL_DATA, stroke=DATA, sw=1.4, rx=3)
    svg.rect(550, 475, 240, 34, fill=FILL_SENSOR, stroke=SENSOR, sw=1.4, rx=3)
    svg.rect(790, 475, 240, 34, fill=FILL_CONTROL, stroke=CONTROL, sw=1.4, rx=3)
    svg.text(310, 499, "network 192.168.10.0", 12, 700, INK, "middle")
    svg.text(670, 499, "subnet .128", 12, 700, SENSOR, "middle")
    svg.text(910, 499, "host 0-127", 12, 700, CONTROL, "middle")
    # table
    headers = ["項目 / item", "/24 example", "/25 example"]
    rows = [
        ["IP", "192.168.10.10", "192.168.10.130"],
        ["mask", "255.255.255.0", "255.255.255.128"],
        ["network", "192.168.10.0", "192.168.10.128"],
        ["broadcast", "192.168.10.255", "192.168.10.255"],
        ["assignable", ".1 - .254 (254)", ".129 - .254 (126)"],
    ]
    table_grid(svg, 70, 560, headers, rows, [220, 400, 400], row_h=42, size=13)
    svg.rect(1130, 560, 250, 230, fill=FILL_HAZARD, stroke=HAZARD, sw=1.4, rx=8)
    svg.text(1150, 595, "同じ第3オクテット", 13, 700, HAZARD)
    svg.text(1150, 617, "でも別サブネット", 13, 700, HAZARD)
    svg.text(1150, 639, "same third octet,", 10, 400, MUTED)
    svg.text(1150, 657, "different subnet", 10, 400, MUTED)
    svg.text(1150, 685, ".20/25 → .0/25", 12, 600, INK)
    svg.text(1150, 707, ".130/25 → .128/25", 12, 600, INK)
    svg.text(1150, 735, "マスクと一緒に判定", 11, 600, HAZARD)
    svg.text(1150, 755, "judge with the mask", 10, 400, MUTED)
    svg.footer("ネットワーク・ブロードキャスト・割当可能範囲を、マスクと一緒に計算する。",
               "Calculate network, broadcast and assignable range together with the mask.")
    return svg


def d09_03() -> Svg:
    svg = new_diagram("D09-03", "同一サブネットとルーティング", "Same subnet and routing",
                      "第9日 / Day 9", 830)
    # same subnet
    panel(svg, 60, 190, 620, 290, "同一サブネット / same subnet", "192.168.10.0/24")
    svg.rect(100, 300, 240, 80, fill=CARD, stroke=DATA, sw=2, rx=6)
    svg.text(220, 332, "PC", 15, 700, DATA, "middle")
    svg.text(220, 354, "192.168.10.10", 12, 400, MUTED, "middle")
    svg.rect(440, 300, 200, 80, fill=CARD, stroke=CONTROL, sw=2, rx=6)
    svg.text(540, 332, "PLC", 15, 700, CONTROL, "middle")
    svg.text(540, 354, "192.168.10.20", 12, 400, MUTED, "middle")
    svg.line(342, 340, 438, 340, stroke=GOOD, sw=3)
    svg.text(390, 325, "直接", 11, 700, GOOD, "middle")
    svg.text(390, 365, "direct", 10, 400, MUTED, "middle")
    svg.text(100, 430, "同じネットワーク。スイッチ内で通信できる。", 13, 400, INK)
    # different subnet
    panel(svg, 720, 190, 650, 290, "別サブネット / different subnet", "192.168.10.0/24 and 192.168.20.0/24")
    svg.rect(760, 300, 220, 80, fill=CARD, stroke=DATA, sw=2, rx=6)
    svg.text(870, 332, "PC", 15, 700, DATA, "middle")
    svg.text(870, 354, "192.168.10.10/24", 12, 400, MUTED, "middle")
    svg.rect(1110, 300, 220, 80, fill=CARD, stroke=CONTROL, sw=2, rx=6)
    svg.text(1220, 332, "PLC", 15, 700, CONTROL, "middle")
    svg.text(1220, 354, "192.168.20.20/24", 12, 400, MUTED, "middle")
    svg.rect(980, 420, 150, 60, fill=CARD, stroke=WARN, sw=2, rx=6)
    svg.text(1055, 447, "ルータ", 15, 700, WARN, "middle")
    svg.text(1055, 466, "router", 10, 400, MUTED, "middle")
    svg.line(980, 340, 982, 420, stroke=WARN, sw=2, dash="6 4")
    svg.line(1110, 340, 1108, 420, stroke=WARN, sw=2, dash="6 4")
    svg.text(760, 500, "別ネットワーク。通常はルータとゲートウェイ設定が必要。", 13, 400, INK)
    # note
    svg.rect(60, 540, 1310, 130, fill=JP_BG, stroke=ACCENT, sw=1.2, rx=8)
    svg.text(80, 575, "同一サブネットかどうかは、同じマスクで計算したネットワークアドレスが一致するかで判定する。", 15, 700, INK)
    svg.text(80, 600, "Two addresses are in the same subnet when their network addresses, computed with the same mask, are equal.", 11, 400, MUTED)
    svg.text(80, 630, "ゲートウェイは、別ネットワークへ出るための次の通信先。 / The gateway is the next hop to another network.", 12, 400, INK)
    svg.footer("物理的に同じスイッチでも、別サブネットならルーティングが必要。 / Even on one switch, different subnets require routing.",
               "Same subnet is a logical condition, not a cable condition.")
    return svg


def d09_04() -> Svg:
    svg = new_diagram("D09-04", "TCP・UDP・ポート・プロトコル", "TCP, UDP, ports and protocols",
                      "第9日 / Day 9", 850)
    layers = [
        ("アプリケーション / application", "Modbus TCP, vendor protocol, HMI", CONTROL),
        ("ポート / port", "502 (Modbus TCP), 80, vendor ports", SENSOR),
        ("トランスポート / transport", "TCP (connection, retransmission) or UDP (connectionless)", DATA),
        ("ネットワーク / network", "IPv4 address, subnet mask, gateway", ENERGY),
        ("物理 / physical", "Ethernet cable, switch, link", MECH),
    ]
    for index, (ja, en, color) in enumerate(layers):
        y = 210 + index * 105
        svg.rect(120, y, 900, 84, fill=CARD, stroke=color, sw=2, rx=8)
        svg.rect(120, y, 10, 84, fill=color, stroke=color, sw=0, rx=3)
        svg.text(150, y + 34, ja, 16, 700, color)
        svg.text(150, y + 58, en, 12, 400, MUTED)
        svg.text(960, y + 50, f"L{5 - index}", 14, 700, color, "end")
    svg.rect(1060, 210, 320, 250, fill=FILL_DATA, stroke=DATA, sw=1.4, rx=8)
    svg.text(1080, 245, "IPアドレス", 15, 700, DATA)
    svg.text(1080, 268, "which device", 11, 400, MUTED)
    svg.text(1080, 300, "ポート", 15, 700, SENSOR)
    svg.text(1080, 323, "which service", 11, 400, MUTED)
    svg.text(1080, 355, "TCP/UDP", 15, 700, MUTED)
    svg.text(1080, 378, "how data is carried", 11, 400, MUTED)
    svg.text(1080, 410, "アプリ / app", 15, 700, CONTROL)
    svg.text(1080, 433, "what the bytes mean", 11, 400, MUTED)
    svg.rect(1060, 490, 320, 160, fill=FILL_HAZARD, stroke=HAZARD, sw=1.2, rx=8)
    svg.text(1080, 522, "リンク・IP・アプリは別", 13, 700, HAZARD)
    svg.text(1080, 545, "ping OK ≠ Modbus OK", 12, 600, INK)
    svg.text(1080, 568, "cable OK ≠ IP OK", 12, 600, INK)
    svg.text(1080, 591, "IP OK ≠ application OK", 12, 600, INK)
    svg.text(1080, 620, "each layer must be checked.", 10, 400, MUTED)
    svg.footer("IPは機器、ポートはサービス、TCP/UDPは運び方、アプリはデータの意味を決める。",
               "IP selects the device, the port selects the service, TCP/UDP carry the data and the application defines its meaning.")
    return svg


def d09_05() -> Svg:
    svg = new_diagram("D09-05", "ネットワーク構成と通信設定", "Network block diagram and configuration record",
                      "第9日 / Day 9", 900)
    # switch
    svg.rect(600, 380, 240, 100, fill=FILL_DATA, stroke=DATA, sw=2.2, rx=8)
    svg.text(720, 420, "スイッチ / switch", 15, 700, DATA, "middle")
    svg.text(720, 445, "192.168.10.0/24", 11, 400, MUTED, "middle")
    nodes = [
        ("PC", "192.168.10.10", 120, 220, DATA),
        ("PLC", "192.168.10.20", 1080, 220, CONTROL),
        ("カメラ", "192.168.10.30", 120, 600, ENERGY),
        ("HMI", "192.168.10.40", 1080, 600, SENSOR),
    ]
    for name, ip, x, y, color in nodes:
        svg.rect(x, y, 250, 80, fill=CARD, stroke=color, sw=2, rx=6)
        svg.text(x + 125, y + 30, name, 15, 700, color, "middle")
        svg.text(x + 125, y + 52, ip, 12, 400, MUTED, "middle")
    svg.line(372, 260, 640, 380, stroke=DATA, sw=2)
    svg.line(1080, 260, 800, 380, stroke=CONTROL, sw=2)
    svg.line(372, 640, 640, 480, stroke=ENERGY, sw=2)
    svg.line(1080, 640, 800, 480, stroke=SENSOR, sw=2)
    # data labels
    svg.text(470, 300, "Modbus TCP :502", 11, 700, CONTROL)
    svg.text(820, 300, "state / result", 11, 600, CONTROL)
    svg.text(470, 620, "images", 11, 700, ENERGY)
    svg.text(820, 620, "HMI data", 11, 600, SENSOR)
    # router/gateway
    svg.rect(640, 680, 200, 70, fill=CARD, stroke=WARN, sw=2, rx=6)
    svg.text(740, 708, "GW 192.168.10.1", 12, 700, WARN, "middle")
    svg.text(740, 728, "to other networks", 10, 400, MUTED, "middle")
    svg.line(720, 480, 720, 678, stroke=WARN, sw=2, dash="6 4")
    # record table
    svg.rect(70, 780, 1300, 60, fill=JP_BG, stroke=ACCENT, sw=1, rx=6)
    svg.text(90, 807, "記録: 機器 / IP / マスク / GW / プロトコル / ポート / 版 / 変更日 / 復旧手順", 13, 700, INK)
    svg.text(90, 828, "Record: device, IP, mask, gateway, protocol, port, revision, change date and recovery procedure.", 10, 400, MUTED)
    svg.footer("設定を変更する前に構成を記録する。記録がなければ復旧できない。 / Record the configuration before changing it; without a record, recovery is not possible.",
               "All addresses are fictional training values.")
    return svg


def d09_06() -> Svg:
    svg = new_diagram("D09-06", "段階的な試運転ゲート", "Staged commissioning gates",
                      "第9日 / Day 9", 980)
    gates = [
        ("G0", "文書 / documentation", "要求・図面・BOM・I/O・ラダー・試験計画", "paper review", CONTROL),
        ("G1", "機械 / mechanical", "取付・ガイド・ストローク・カバー", "inspection", MECH),
        ("G2", "電気（隔離）/ electrical", "配線・極性・保護・接地・無電圧", "qualified, isolated", ENERGY),
        ("G3", "オフライン制御 / offline", "自己保持・タイマー・シーケンス・異常", "simulation", SENSOR),
        ("G4", "監督下準備 / readiness", "ガード・隔離・残留エネルギー・復旧", "supervisor", WARN),
        ("G5", "通電試験 / energised", "承認された手順のみ", "NOT PERFORMED", HAZARD),
        ("G6", "最終受入 / acceptance", "要求との照合・記録・引継ぎ", "acceptor", GOOD),
    ]
    for index, (code, ja, detail, approval, color) in enumerate(gates):
        y = 190 + index * 105
        svg.rect(110, y, 120, 80, fill=color, stroke=color, sw=2, rx=8)
        svg.text(170, y + 48, code, 24, 700, "white", "middle")
        svg.rect(240, y, 780, 80, fill=CARD, stroke=color, sw=1.8, rx=8)
        svg.text(260, y + 30, ja, 15, 700, color)
        svg.text(260, y + 54, detail, 11, 400, MUTED)
        svg.text(800, y + 53, approval, 10, 600, MUTED, "end")
        if index < len(gates) - 1:
            svg.line(170, y + 82, 170, y + 103, stroke=color, sw=2)
        if code == "G5":
            svg.text(920, y + 50, "課程では未実施", 12, 700, HAZARD, "middle")
            svg.text(920, y + 68, "not required", 10, 400, MUTED, "middle")
    svg.text(1000, 250, "前のゲートが", 13, 700, INK)
    svg.text(1000, 272, "完了するまで", 13, 700, INK)
    svg.text(1000, 294, "次へ進まない", 13, 700, HAZARD)
    svg.text(1000, 330, "Do not pass a gate", 11, 400, MUTED)
    svg.text(1000, 350, "until the previous", 11, 400, MUTED)
    svg.text(1000, 370, "gate is complete.", 11, 400, MUTED)
    svg.rect(990, 430, 360, 210, fill=FILL_HAZARD, stroke=HAZARD, sw=1.3, rx=8)
    svg.text(1010, 462, "G5は必須ではない", 14, 700, HAZARD)
    svg.text(1010, 486, "Energised testing is optional", 11, 400, MUTED)
    svg.text(1010, 515, "未実施は BLOCKED または", 12, 600, INK)
    svg.text(1010, 537, "NOT TESTED と記録する。", 12, 600, INK)
    svg.text(1010, 560, "PASS にしない。", 12, 700, HAZARD)
    svg.text(1010, 588, "Never record an unperformed", 10, 400, MUTED)
    svg.text(1010, 606, "energised test as PASS.", 10, 400, MUTED)
    svg.footer("文書→機械→電気（隔離）→オフライン→監督下準備→承認された通電→受入の順。G5は必須ではない。",
               "Documentation, mechanics, isolated electrical, offline, supervised readiness, approved energised, acceptance. G5 is optional.")
    return svg


def d09_07() -> Svg:
    svg = new_diagram("D09-07", "試験結果の4状態", "Four test-result states",
                      "第9日 / Day 9", 820)
    states = [
        ("PASS", "期待と一致した", "matched the expected result", GOOD, 90, 250),
        ("FAIL", "期待と違った", "did not match", HAZARD, 560, 250),
        ("NOT TESTED", "まだ実施していない", "not yet performed", MUTED, 1030, 250),
        ("BLOCKED", "前提・許可・設備がない", "cannot be performed", WARN, 560, 470),
    ]
    for label, ja, en, color, x, y in states:
        svg.rect(x, y, 320, 150, fill=CARD, stroke=color, sw=2.6, rx=10)
        svg.text(x + 160, y + 44, label, 20, 700, color, "middle")
        svg.text(x + 160, y + 78, ja, 14, 700, INK, "middle")
        svg.text(x + 160, y + 104, en, 11, 400, MUTED, "middle")
        svg.text(x + 160, y + 130, "evidence required" if label == "PASS" else "", 10, 400, MUTED, "middle")
    svg.line(410, 325, 558, 325, stroke=GOOD, sw=2)
    svg.line(880, 325, 1028, 325, stroke=GOOD, sw=2)
    svg.line(720, 402, 720, 468, stroke=HAZARD, sw=2, dash="6 4")
    svg.text(1050, 520, "BLOCKEDをPASSに", 12, 700, HAZARD)
    svg.text(1050, 540, "読み替えない", 12, 700, HAZARD)
    svg.text(1050, 565, "never reinterpret", 10, 400, MUTED)
    svg.text(1050, 583, "BLOCKED as PASS", 10, 400, MUTED)
    svg.rect(70, 660, 1300, 90, fill=JP_BG, stroke=ACCENT, sw=1.2, rx=8)
    svg.text(90, 692, "記録には、試験ID、要求ID、前提、手順、期待、実測、合否、証跡、実施者、日付、是正処置を入れる。", 13, 700, INK)
    svg.text(90, 715, "A record contains test ID, requirement ID, preconditions, procedure, expected, actual, status, evidence, operator, date and corrective action.", 10, 400, MUTED)
    svg.text(90, 738, "PASSは証跡とセット。 / PASS comes with evidence.", 12, 600, GOOD)
    svg.footer("PASS・FAIL・NOT TESTED・BLOCKEDを区別する。未実施を合格にしない。",
               "Distinguish PASS, FAIL, NOT TESTED and BLOCKED. An unperformed test is not a pass.")
    return svg


def d09_08() -> Svg:
    svg = new_diagram("D09-08", "課題から提案までの流れ", "From problem to proposal",
                      "第9日 / Day 9", 900)
    steps = [
        ("課題", "problem", "現状・測定 / current state"),
        ("要求", "requirements", "能力・品質・安全 / capacity, quality, safety"),
        ("構想", "concept", "3案比較 / three options"),
        ("機械", "mechanical", "駆動・ガイド・センサー / drive, guide, sensor"),
        ("電気・PLC", "electrical and PLC", "I/O・シーケンス / I/O and sequence"),
        ("通信", "communication", "IP・プロトコル / IP and protocol"),
        ("試験", "test", "ゲート・受入 / gates and acceptance"),
        ("提案", "proposal", "費用・リスク・次 / cost, risk, next"),
    ]
    for index, (ja, en, sub) in enumerate(steps):
        row, col = divmod(index, 4)
        x = 70 + col * 330
        y = 230 + row * 260
        color = (MECH, CONTROL, SENSOR, ENERGY)[index % 4]
        svg.rect(x, y, 300, 180, fill=CARD, stroke=color, sw=2, rx=10)
        svg.text(x + 20, y + 40, f"{index + 1}. {ja}", 18, 700, color)
        svg.text(x + 20, y + 64, en, 13, 400, MUTED)
        for line_index, line in enumerate(_wrap(sub, 250, 14)):
            svg.text(x + 20, y + 100 + line_index * 22, line, 13, 400, INK)
        if col < 3:
            svg.line(x + 304, y + 90, x + 326, y + 90, stroke=color, sw=2.2)
    # return loop
    svg.line(1280, 410, 1360, 410, stroke=HAZARD, sw=2, dash="7 5")
    svg.line(1360, 410, 1360, 690, stroke=HAZARD, sw=2, dash="7 5", marker=False)
    svg.line(1360, 690, 70, 690, stroke=HAZARD, sw=2, dash="7 5", marker=False)
    svg.line(70, 690, 70, 640, stroke=HAZARD, sw=2, dash="7 5")
    svg.text(720, 715, "測定・レビューで戻る / iterate with measurement and review", 13, 700, HAZARD, "middle")
    # final chain
    svg.rect(70, 760, 1300, 60, fill=JP_BG, stroke=ACCENT, sw=1, rx=6)
    svg.text(90, 795, "何を改善するか → どんな機械か → どう動くか → どう検知するか → PLCがどう制御するか → どう通信するか → どう試験するか → 何が残るか",
             12, 700, INK)
    svg.footer("提案は1枚の絵ではなく、要求から試験までの一貫した流れ。 / A proposal is a consistent chain from requirement to test, not a single picture.",
               "Each step must remain traceable to the previous one.")
    return svg


def d09_09() -> Svg:
    svg = new_diagram("D09-09", "費用対効果と回収期間", "Cost, benefit and payback",
                      "第9日 / Day 9", 880)
    # formula
    svg.rect(70, 190, 1300, 110, fill=JP_BG, stroke=ACCENT, sw=1.4, rx=8)
    svg.text(90, 230, "年間効果 = 削減時間/日 × 稼働日 × 時間単価", 18, 700, INK)
    svg.text(90, 256, "annual value = time saved per day × working days × hourly rate", 13, 400, MUTED)
    svg.text(90, 282, "回収期間 = 投資 ÷ (年間効果 − 年間運用費)    payback = investment / (annual benefit − annual operating cost)", 12, 600, ACCENT)
    # numbers
    values = [
        ("削減 / saved", "12 s × 180 = 36 min/day", MECH),
        ("年間 / annual", "0.6 h × 220 × 2,400 = 316,800 JPY", SENSOR),
        ("投資 / investment", "450,000 JPY", ENERGY),
        ("回収 / payback", "450,000 / 316,800 = 1.42 years", GOOD),
    ]
    for index, (label, value, color) in enumerate(values):
        x = 70 + index * 330
        svg.rect(x, 340, 300, 120, fill=CARD, stroke=color, sw=2, rx=8)
        svg.text(x + 16, 372, label, 13, 700, color)
        for line_index, line in enumerate(_wrap(value, 260, 14)):
            svg.text(x + 16, 404 + line_index * 22, line, 14, 600, INK)
    # sensitivity bars
    svg.text(70, 520, "投資と運用費による回収期間の変化 / payback sensitivity", 16, 700, INK)
    scenarios = [
        ("300k, 0", 300_000, 0, 0.95),
        ("450k, 0", 450_000, 0, 1.42),
        ("600k, 0", 600_000, 0, 1.89),
        ("450k, 100k", 450_000, 100_000, 2.07),
        ("450k, 200k", 450_000, 200_000, 3.61),
    ]
    base_y = 720
    for index, (label, investment, operating, years) in enumerate(scenarios):
        x = 90 + index * 250
        height = min(150, years * 40)
        color = GOOD if years <= 1.5 else (WARN if years <= 3 else HAZARD)
        svg.rect(x, base_y - height, 120, height, fill=color, stroke=color, sw=1, rx=4)
        svg.text(x + 60, base_y + 22, label, 11, 600, MUTED, "middle")
        svg.text(x + 60, base_y - height - 8, f"{years:.2f} y", 13, 700, color, "middle")
    svg.line(70, base_y, 1340, base_y, stroke=MUTED, sw=1.6, marker=False)
    svg.text(1260, 545, "運用費が増えると", 12, 600, HAZARD)
    svg.text(1260, 565, "回収は長くなる", 12, 600, HAZARD)
    svg.text(1260, 590, "効果が実現しなければ", 12, 600, HAZARD)
    svg.text(1260, 610, "回収は無限", 12, 700, HAZARD)
    svg.footer("1.42年は仮定した数値での単純回収。労務時間の換算価値と、実現する利益を区別する。",
               "1.42 years is a simple payback on assumed numbers. Distinguish labour-time value from realised profit.")
    return svg


# --------------------------------------------------------------------------- #
# entry point
# --------------------------------------------------------------------------- #
BUILDERS = {
    "D07-01": d07_01, "D07-02": d07_02, "D07-03": d07_03, "D07-04": d07_04,
    "D07-05": d07_05, "D07-06": d07_06, "D07-07": d07_07, "D07-08": d07_08, "D07-09": d07_09,
    "D08-01": d08_01, "D08-02": d08_02, "D08-03": d08_03, "D08-04": d08_04,
    "D08-05": d08_05, "D08-06": d08_06, "D08-07": d08_07, "D08-08": d08_08,
    "D08-09": d08_09, "D08-10": d08_10, "D08-11": d08_11,
    "D09-01": d09_01, "D09-02": d09_02, "D09-03": d09_03, "D09-04": d09_04,
    "D09-05": d09_05, "D09-06": d09_06, "D09-07": d09_07, "D09-08": d09_08, "D09-09": d09_09,
}


def build() -> list[Path]:
    outputs = []
    for fid, builder in BUILDERS.items():
        day = fid[:3].lower().replace("d0", "day0")
        folder = DIAGRAMS / day
        folder.mkdir(parents=True, exist_ok=True)
        svg = builder()
        output = folder / f"{fid}.svg"
        svg.save(output)
        outputs.append(output)
    return outputs


def main() -> int:
    outputs = build()
    for path in outputs:
        print(f"Wrote {path.relative_to(ROOT)}")
    print(f"Generated {len(outputs)} diagrams")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


