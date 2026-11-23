"""Export the three Day 7-9 bilingual explanation PDFs.

Run from any directory:
    python AI_Vision_Training\\day07_09_support\\scripts\\export_day07_09_pdf.py

Inputs are the canonical notebooks and the captured reference outputs.  The
exporter does not execute notebook cells.  It verifies the notebook fingerprint
before reading, and refuses to export a stale notebook.

Output:
    docs/pdf/Day07_explanation_ja_en.pdf
    docs/pdf/Day08_explanation_ja_en.pdf
    docs/pdf/Day09_explanation_ja_en.pdf

Design goals: selectable text, Japanese and English, a real table of contents,
page numbers, readable diagrams, no raw HTML and no broken IP addresses.
"""

from __future__ import annotations

import hashlib
import json
import re
from html import escape
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parents[2]
NOTEBOOKS = ROOT / "notebooks"
PDF_DIR = ROOT / "docs" / "pdf"
SUPPORT = ROOT / "day07_09_support"
REFERENCE_OUTPUTS = SUPPORT / "reference_data" / "reference_outputs.json"
DIAGRAM_PNG = SUPPORT / "reference_data" / "diagram_png"
FONT_CANDIDATES = (
    Path("C:/Windows/Fonts/meiryo.ttc"),
    Path("C:/Windows/Fonts/YuGothR.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
)
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

DAY_INFO = {
    "day07": {
        "title": "第7日：自動化設備の構想・機械設計",
        "title_en": "Day 7: Automation Planning and Mechanical Design",
        "intro_ja": "要求仕様、ECRS、生産能力、方式比較、機械構成、空圧、シリンダとモーターの選定を学びます。",
        "intro_en": "Requirements, ECRS, capacity, concept comparison, machine architecture, pneumatics and cylinder/motor selection.",
        "accent": "#1F5C99",
    },
    "day08": {
        "title": "第8日：電気設計・センサー・PLC・ラダー制御",
        "title_en": "Day 8: Electrical Design, Sensors and PLC Control",
        "intro_ja": "DC24Vの電気、センサーとNPN/PNP、I/O、自己保持、タイマー、状態シーケンス、異常処理と再起動防止を学びます。",
        "intro_en": "DC24V electricity, sensors and NPN/PNP, I/O, self-holding, timers, state sequences, fault handling and restart prevention.",
        "accent": "#6B3FA0",
    },
    "day09": {
        "title": "第9日：通信・試運転・改善提案",
        "title_en": "Day 9: Industrial Communication, Commissioning and Automation Proposal",
        "intro_ja": "IPとサブネット、TCP/UDP、産業用通信、段階ゲート、試験記録、費用対効果、最終提案を学びます。",
        "intro_en": "IP and subnets, TCP/UDP, industrial protocols, staged gates, test records, cost-benefit and the final proposal.",
        "accent": "#1B7A4B",
    },
}
REFERENCES = (
    ("ISO 12100:2010 — risk assessment", "https://www.iso.org/standard/51528.html"),
    ("ISO 13849-1:2023 — safety-related control systems", "https://www.iso.org/standard/73481.html"),
    ("ISO 13850:2015 — emergency stop", "https://www.iso.org/standard/59970.html"),
    ("IEC 60204-1:2016+A1:2021 — electrical equipment of machines", "https://webstore.iec.ch/en/publication/71256"),
    ("IEC 61131-3 — PLC programming languages", "https://webstore.iec.ch/en/publication/68533"),
    ("SMC cylinder selection (entry point)", "https://www.smcworld.com/select/air/en-jp/"),
    ("Mitsubishi Electric FA manuals (entry point)", "https://www.mitsubishielectric.co.jp/fa/download/search.page"),
    ("Omron proximity sensor technical guide (entry point)", "https://www.fa.omron.co.jp/guide/technicalguide/41/17/"),
    ("Modbus specifications", "https://www.modbus.org/modbus-specifications"),
    ("RFC 3021 — 31-bit prefixes", "https://www.rfc-editor.org/rfc/rfc3021"),
)


def register_font() -> str:
    for candidate in FONT_CANDIDATES:
        if candidate.exists():
            pdfmetrics.registerFont(TTFont("DayFont", str(candidate), subfontIndex=0))
            return "DayFont"
    raise RuntimeError("No Japanese-capable font found")


def rich(text: str) -> str:
    text = escape(text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'\1 (\2)', text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r'<font color="#175a70">\1</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"\b\d{1,3}(?:\.\d{1,3}){3}(?:/\d{1,2})?\b", r"<nobr>\g<0></nobr>", text)
    return text


def styles_for(face: str) -> dict[str, ParagraphStyle]:
    common = dict(fontName=face, wordWrap="CJK", splitLongWords=0)
    return {
        "body": ParagraphStyle("body", fontSize=10.6, leading=18.0, spaceAfter=7,
                               textColor=colors.HexColor("#22313F"), **common),
        "bullet": ParagraphStyle("bullet", fontSize=10.4, leading=17.0, spaceAfter=4,
                                 leftIndent=12, firstLineIndent=-12,
                                 textColor=colors.HexColor("#22313F"), **common),
        "h1": ParagraphStyle("h1", fontSize=17, leading=24, spaceBefore=10, spaceAfter=12,
                             textColor=colors.HexColor("#164B79"), **common),
        "h2": ParagraphStyle("h2", fontSize=13, leading=19, spaceBefore=14, spaceAfter=7,
                             textColor=colors.HexColor("#164B79"), **common),
        "h3": ParagraphStyle("h3", fontSize=11.4, leading=16, spaceBefore=9, spaceAfter=5,
                             textColor=colors.HexColor("#1F5C99"), **common),
        "small": ParagraphStyle("small", fontSize=8.6, leading=12.4, spaceAfter=3,
                                textColor=colors.HexColor("#22313F"), **common),
        "caption": ParagraphStyle("caption", fontSize=8.8, leading=12.6, spaceAfter=9,
                                  textColor=colors.HexColor("#526378"), **common),
        "code": ParagraphStyle("code", fontName=face, fontSize=8.3, leading=11.8,
                               textColor=colors.HexColor("#142B3F"), backColor=colors.HexColor("#F2F6FA"),
                               borderPadding=5, spaceBefore=4, spaceAfter=7),
        "quote": ParagraphStyle("quote", fontSize=10.0, leading=16.6, spaceAfter=7,
                                leftIndent=10, rightIndent=6, backColor=colors.HexColor("#FDF2F2"),
                                borderColor=colors.HexColor("#A32B2B"), borderWidth=2,
                                borderPadding=7, textColor=colors.HexColor("#4A2020"), **common),
        "toc0": ParagraphStyle("toc0", fontName=face, fontSize=9.6, leading=14.0,
                               leftIndent=0, firstLineIndent=0),
        "toc1": ParagraphStyle("toc1", fontName=face, fontSize=8.8, leading=12.4,
                               leftIndent=14, firstLineIndent=0),
    }


class BilingualDoc(BaseDocTemplate):
    def __init__(self, filename: str, **kwargs):
        super().__init__(filename, **kwargs)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")
        self.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=self._decorate)])
        self._day_label = "Day 7-9"
        self.toc_entries = 0

    def _decorate(self, canvas, doc):
        canvas.saveState()
        canvas.setFont("DayFont", 7.6)
        canvas.setFillColor(colors.HexColor("#526378"))
        canvas.drawString(18 * mm, 10 * mm,
                          f"{self._day_label} — 架空の学習用資料 / fictional training material")
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, str(doc.page))
        canvas.setStrokeColor(colors.HexColor("#C1D0DD"))
        canvas.setLineWidth(0.4)
        canvas.line(18 * mm, 13 * mm, A4[0] - 18 * mm, 13 * mm)
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            level = getattr(flowable, "_toc_level", None)
            if level is not None:
                text = getattr(flowable, "_toc_text", "")
                self.notify("TOCEntry", (level, text, self.page))


def split_table_row(line: str) -> list[str]:
    value = line.strip()
    if value.startswith("|"):
        value = value[1:]
    if value.endswith("|"):
        value = value[:-1]
    cells: list[str] = []
    current = ""
    in_code = False
    for char in value:
        if char == "`":
            in_code = not in_code
            current += char
        elif char == "|" and not in_code:
            cells.append(current.strip())
            current = ""
        else:
            current += char
    cells.append(current.strip())
    return cells


def add_table(story, lines, start_index, styles, width) -> int:
    headers = split_table_row(lines[start_index])
    position = start_index + 2
    rows = []
    while position < len(lines) and lines[position].strip().startswith("|"):
        rows.append(split_table_row(lines[position]))
        position += 1
    if any(len(row) != len(headers) for row in rows):
        details = [row for row in rows if len(row) != len(headers)]
        raise ValueError(f"malformed Markdown table {headers}: {details}")
    weights = []
    face = styles["small"].fontName
    for column in range(len(headers)):
        candidates = [headers[column]] + [row[column] for row in rows]
        widest = max(pdfmetrics.stringWidth(value, face, 8.4) for value in candidates)
        weights.append(max(24.0, widest + 10.0))
    total = sum(weights)
    widths = [width * weight / total for weight in weights]
    cells = [[Paragraph(rich(value), styles["small"]) for value in row] for row in [headers] + rows]
    table = Table(cells, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAF1F8")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C1D0DD")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(table)
    story.append(Spacer(1, 7))
    return position


def wrap_code(text: str, face: str, size: float, max_width: float) -> str:
    out = []
    for line in text.splitlines():
        if pdfmetrics.stringWidth(line, face, size) <= max_width:
            out.append(line)
            continue
        current = ""
        for char in line:
            if current and pdfmetrics.stringWidth(current + char, face, size) > max_width:
                out.append(current)
                current = "    " + char
            else:
                current += char
        out.append(current)
    return "\n".join(out)


def add_image(story, target: Path, width: float) -> None:
    with PILImage.open(target) as picture:
        iw, ih = picture.size
    figure_width = min(width, 168 * mm)
    figure_height = figure_width * ih / iw
    if figure_height > 128 * mm:
        figure_height = 128 * mm
        figure_width = figure_height * iw / ih
    story.append(KeepTogether([Image(str(target), width=figure_width, height=figure_height)]))
    story.append(Spacer(1, 5))


def flow_markdown(story, text: str, base_dir: Path, styles, width: float, face: str) -> None:
    lines = text.splitlines()
    position = 0
    paragraph_buffer: list[str] = []

    def flush() -> None:
        nonlocal paragraph_buffer
        if paragraph_buffer:
            story.append(Paragraph(rich(" ".join(paragraph_buffer)), styles["body"]))
            paragraph_buffer = []

    while position < len(lines):
        raw = lines[position]
        line = raw.strip()
        position += 1
        if not line:
            flush()
            continue
        image = IMAGE_RE.search(line)
        if image:
            flush()
            target = (base_dir / image.group(2)).resolve()
            if not target.is_file():
                raise FileNotFoundError(f"missing figure: {target}")
            png = DIAGRAM_PNG / target.parent.name / f"{target.stem}.png"
            add_image(story, png if png.is_file() else target, width)
            continue
        if line.startswith("#"):
            flush()
            level = len(line) - len(line.lstrip("#"))
            value = line[level:].strip()
            style = styles["h1" if level == 1 else ("h2" if level == 2 else "h3")]
            paragraph = Paragraph(rich(value), style)
            if level <= 2:
                paragraph._toc_level = 0 if level == 1 else 1
                paragraph._toc_text = value
            story.append(paragraph)
            continue
        if line.startswith("|") and position < len(lines) and re.match(
                r"^\|\s*:?-{2,}", lines[position].strip()):
            flush()
            position = add_table(story, lines, position - 1, styles, width)
            continue
        if line.startswith("---"):
            flush()
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#C1D0DD")))
            story.append(Spacer(1, 4))
            continue
        if line.startswith(">"):
            flush()
            quote = [line.lstrip("> ").strip()]
            while position < len(lines) and lines[position].strip().startswith(">"):
                quote.append(lines[position].strip().lstrip("> ").strip())
                position += 1
            story.append(Paragraph(rich(" ".join(quote)), styles["quote"]))
            continue
        if line.startswith("```"):
            flush()
            fence = line.strip("`").strip()
            code_lines = []
            while position < len(lines) and not lines[position].strip().startswith("```"):
                code_lines.append(lines[position])
                position += 1
            position += 1
            story.append(Preformatted(wrap_code("\n".join(code_lines), face, 8.3, width - 12),
                                      styles["code"]))
            continue
        checkbox = re.match(r"^[-*]\s+\[( |x|X)\]\s+(.*)$", line)
        if checkbox:
            flush()
            mark = "☑" if checkbox.group(1).lower() == "x" else "☐"
            story.append(Paragraph(f"{mark} {rich(checkbox.group(2))}", styles["bullet"]))
            continue
        bullet = re.match(r"^[-*]\s+(.*)$", line)
        if bullet:
            flush()
            story.append(Paragraph("• " + rich(bullet.group(1)), styles["bullet"]))
            continue
        numbered = re.match(r"^(\d+)\.\s+(.*)$", line)
        if numbered:
            flush()
            story.append(Paragraph(f"{numbered.group(1)}. {rich(numbered.group(2))}", styles["bullet"]))
            continue
        if line.startswith("*") and line.endswith("*") and len(line) > 2:
            flush()
            story.append(Paragraph(rich(line), styles["caption"]))
            continue
        paragraph_buffer.append(line)
    flush()


def cover(day: dict, lessons: list[dict], styles, face: str) -> list:
    accent = colors.HexColor(day["accent"])
    story = [
        Spacer(1, 10 * mm),
        Paragraph(day["title"], ParagraphStyle("cover", fontName=face, fontSize=25, leading=34,
                                               textColor=accent, wordWrap="CJK")),
        Paragraph(day["title_en"], ParagraphStyle("cover_en", fontName=face, fontSize=17, leading=25,
                                                  textColor=colors.HexColor("#526378"), wordWrap="CJK")),
        Spacer(1, 5 * mm),
        HRFlowable(width="100%", thickness=2, color=accent),
        Spacer(1, 4 * mm),
        Paragraph(day["intro_ja"], styles["body"]),
        Paragraph(day["intro_en"], styles["body"]),
        Spacer(1, 4 * mm),
    ]
    rows = [["#", "ノートブック / notebook", "時間 / min", "元PDF / source pages"]]
    for lesson in lessons:
        rows.append([str(lesson["order"]), f"{lesson['name']} — {lesson['title_ja']} / {lesson['title_en']}",
                     str(lesson["duration_min"]), lesson["pdf_pages"]])
    table = Table([[Paragraph(rich(cell), styles["small"]) for cell in row] for row in rows],
                  colWidths=[10 * mm, 112 * mm, 18 * mm, 30 * mm], repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAF1F8")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C1D0DD")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story += [table, Spacer(1, 5 * mm)]
    story.append(Paragraph("研修の時間 / course time", styles["h3"]))
    story.append(Paragraph(
        "08:00–09:00 講師説明 / instructor · 09:00–10:20 ノートブック01 · 10:20–10:35 休憩 / break · "
        "10:35–12:00 ノートブック02 · 12:00–12:50 昼食 / lunch · 12:50–13:50 講師フォロー / instructor · "
        "13:50–15:10 ノートブック03 前半 · 15:10–15:25 休憩 / break · 15:25–16:20 ノートブック03 後半 · "
        "16:20–16:50 ワークシートと提出 / worksheet and submission. 合計 / total 530 min.",
        styles["small"]))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(
        "<b>安全境界 / Safety boundary.</b> 本資料は教育用です。実機の配線・通電・空圧供給・シリンダ動作・"
        "安全回路の調整を指示するものではありません。実機作業は、リスクアセスメント、事前承認、隔離、"
        "残留エネルギー確認、有資格者の監督のもとで別に行います。通常のPLC制御は安全機能ではありません。"
        " / This material is educational. It does not authorise real wiring, energisation, compressed air, "
        "cylinder motion or safety-circuit adjustment. Real work requires a risk assessment, prior approval, "
        "isolation, stored-energy verification and qualified supervision. Ordinary PLC control is not a safety function.",
        styles["quote"]))
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph(
        "本PDFの数値例・シミュレーション結果は、明示した仮定に基づく参考値です。実機の測定値ではありません。"
        " / Numeric examples and simulation results are reference values under stated assumptions, not measurements from a real machine.",
        styles["small"]))
    return story


def appendix(story, title_ja: str, title_en: str, path: Path, styles, width: float, face: str) -> None:
    story.append(PageBreak())
    story.append(Paragraph(rich(f"{title_ja} / {title_en}"), styles["h1"]))
    flow_markdown(story, path.read_text(encoding="utf-8"), path.parent, styles, width, face)


def render_day(day_id: str, manifest: dict, outputs: dict, face: str) -> Path:
    day = next(item for item in manifest["days"] if item["id"] == day_id)
    info = DAY_INFO[day_id]
    styles = styles_for(face)
    output = PDF_DIR / f"{day_id.capitalize()}_explanation_ja_en.pdf"
    doc = BilingualDoc(
        str(output), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=16 * mm, bottomMargin=18 * mm, title=info["title"],
        author="Training_Automation", subject=info["title_en"],
    )
    doc._day_label = f"{day_id[:3].upper()} {day_id[3:]} / Day {int(day_id[3:])}"
    width = A4[0] - 36 * mm

    toc = TableOfContents()
    toc.levelStyles = [styles["toc0"], styles["toc1"]]

    story: list = cover(info, day["lessons"], styles, face)
    story += [PageBreak(), Paragraph("目次 / Contents", styles["h1"]), toc, PageBreak()]

    for lesson_index, lesson in enumerate(day["lessons"]):
        notebook_path = NOTEBOOKS / day["folder"] / f"{lesson['name']}.ipynb"
        if not notebook_path.is_file():
            raise FileNotFoundError(f"missing notebook: {notebook_path}")
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
        if lesson_index:
            story.append(PageBreak())
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#94A9BB")))
        for cell in notebook["cells"]:
            source = "".join(cell["source"])
            if cell["cell_type"] == "markdown":
                flow_markdown(story, source, notebook_path.parent, styles, width, face)
            else:
                exec_id = cell.get("metadata", {}).get("day07_09_exercise", "?")
                reference = outputs.get(lesson["name"], {}).get(exec_id, {})
                story.append(Paragraph(
                    f"実行可能セル / executable cell — <font color='#175a70'>{escape(exec_id)}</font>",
                    styles["h3"]))
                story.append(Preformatted(wrap_code(source, face, 8.3, width - 12), styles["code"]))
                captured = reference.get("output", "").strip()
                if captured:
                    story.append(Paragraph("参考出力（オフラインシミュレーション）/ reference output (offline simulation)",
                                           styles["caption"]))
                    story.append(Preformatted(wrap_code(captured, face, 8.1, width - 12), styles["code"]))
                else:
                    story.append(Paragraph("このセルは図を生成します。 / this cell generates a figure.",
                                           styles["caption"]))

    appendix(story, "付録A 公式・確認カード", "Appendix A: formula and check card",
             SUPPORT / "reference_data" / f"quick_reference_{day_id}.md", styles, width, face)
    appendix(story, "付録B 技術用語集", "Appendix B: technical glossary",
             SUPPORT / "worksheets" / "Glossary_ja_en.md", styles, width, face)
    story.append(PageBreak())
    story.append(Paragraph("付録C 参考資料 / Appendix C: references", styles["h1"]))
    story.append(Paragraph(
        "以下は公式資料への入口です。URLの内容を保証するものではありません。使用する版・確認日を記録してください。"
        " / Entry points to official material. A URL is not a guarantee of content; record the revision and date you checked.",
        styles["body"]))
    for name, url in REFERENCES:
        story.append(Paragraph(rich(f"{name}: {url}"), styles["small"]))
        story.append(Spacer(1, 2))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(
        "本教材の図はすべて自作の編集可能なSVGで、学習目的の概念図です。実機の製作図・安全設計図ではありません。"
        " / All figures are original editable SVGs made for teaching. They are not construction or safety-design drawings.",
        styles["small"]))

    doc.multiBuild(story)
    return output


def main() -> int:
    face = register_font()
    manifest = json.loads((SUPPORT / "lesson_manifest.json").read_text(encoding="utf-8"))
    outputs = json.loads(REFERENCE_OUTPUTS.read_text(encoding="utf-8"))
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    for day in manifest["days"]:
        path = render_day(day["id"], manifest, outputs, face)
        print(f"Exported {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
