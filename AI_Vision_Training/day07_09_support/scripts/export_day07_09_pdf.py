"""Export the nine Day 7-9 Markdown notebooks as three independent A4 PDFs.

Run from any directory:
    python AI_Vision_Training\\day07_09_support\\scripts\\export_day07_09_pdf.py

Requires ReportLab, Pillow, Playwright and a locally installed Chrome or Edge browser.
The notebooks (generated from the manuscripts) are the single source of the lessons;
the exporter refuses to run when a notebook does not match its manuscript hash.
Each PDF also carries the day's formula card and the shared bilingual glossary.
"""

from __future__ import annotations

import hashlib
import json
import re
import tempfile
from html import escape
from pathlib import Path

from PIL import Image as PILImage
from playwright.sync_api import sync_playwright
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from build_day07_09_notebooks import DAYS, NOTEBOOKS, ROOT

PDF_DIR = ROOT / "docs" / "pdf"
SUPPORT = ROOT / "day07_09_support"
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
FONT_CANDIDATES = (
    Path("C:/Windows/Fonts/meiryo.ttc"),
    Path("C:/Windows/Fonts/YuGothR.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
)
BROWSERS = (
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
)

DAY_TITLES = {
    "Day07_Machine_Fundamentals": "第7日：検査装置の機械構造・センサ・アクチュエータ / Day 7: Mechanical Structure, Sensors and Actuators",
    "Day08_PLC_Control": "第8日：PLC制御とラダープログラムの基礎 / Day 8: PLC Control and Ladder Programming",
    "Day09_System_Integration": "第9日：カメラ・PLC・PC・AIの統合による自動検査システム / Day 9: Integrated Machine Vision, PLC, PC and AI",
}
DAY_SHORT = {
    "Day07_Machine_Fundamentals": ("Day07", "第7日 / Day 7", "quick_reference_day07.md"),
    "Day08_PLC_Control": ("Day08", "第8日 / Day 8", "quick_reference_day08.md"),
    "Day09_System_Integration": ("Day09", "第9日 / Day 9", "quick_reference_day09.md"),
}
REFERENCES = (
    ("IEC 61131-3:2025", "https://webstore.iec.ch/en/publication/68533"),
    ("Mitsubishi Electric FA", "https://www.mitsubishielectric.com/fa/"),
    ("ISO 12100:2010", "https://www.iso.org/standard/51528.html"),
    ("ISO 13849-1:2023", "https://www.iso.org/standard/73481.html"),
    ("ISO 13850:2015", "https://www.iso.org/standard/59970.html"),
    ("IEC 60204-1:2016+A1:2021", "https://webstore.iec.ch/en/publication/71256"),
    ("EMVA GenICam", "https://www.emva.org/standards-technology/genicam/"),
    ("Basler documentation", "https://docs.baslerweb.com/"),
    ("OPC Foundation reference", "https://reference.opcfoundation.org/"),
    ("Modbus specifications", "https://www.modbus.org/modbus-specifications"),
    ("Ultralytics YOLO detect", "https://docs.ultralytics.com/tasks/detect/"),
    ("Anomalib PatchCore", "https://anomalib.readthedocs.io/en/lib-v2.7.0/markdown/guides/reference/models/image/patchcore.html"),
)


def register_font() -> str:
    for candidate in FONT_CANDIDATES:
        if candidate.exists():
            pdfmetrics.registerFont(TTFont("Day0709Japanese", str(candidate), subfontIndex=0))
            return "Day0709Japanese"
    raise RuntimeError("No Japanese-capable font found; PDF not exported")


def rich(text: str) -> str:
    text = escape(text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r'<font color="#175a70">\1</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    return text.replace("  ", " ")


def styles_for(face: str) -> dict[str, ParagraphStyle]:
    return {
        "body": ParagraphStyle("body", fontName=face, fontSize=11, leading=19.4, spaceAfter=9,
                               textColor=colors.HexColor("#223344"), wordWrap="CJK"),
        "title": ParagraphStyle("title", fontName=face, fontSize=17.5, leading=25, spaceBefore=8,
                                spaceAfter=12, textColor=colors.HexColor("#164b79"), wordWrap="CJK"),
        "heading": ParagraphStyle("heading", fontName=face, fontSize=13, leading=19, spaceBefore=12,
                                  spaceAfter=9, textColor=colors.HexColor("#164b79"), wordWrap="CJK"),
        "small": ParagraphStyle("small", fontName=face, fontSize=8.5, leading=12.6, spaceAfter=3,
                                textColor=colors.HexColor("#223344"), wordWrap="CJK"),
        "caption": ParagraphStyle("caption", fontName=face, fontSize=9.2, leading=13.4, spaceAfter=10,
                                  textColor=colors.HexColor("#526378"), wordWrap="CJK"),
        "source": ParagraphStyle("source", fontName=face, fontSize=8.3, leading=11.8, spaceAfter=3,
                                 wordWrap="CJK"),
    }


def table_widths(headers: list[str], rows: list[list[str]], width: float) -> list[float]:
    weights = []
    for column in range(len(headers)):
        longest = max([len(headers[column])] + [len(row[column]) for row in rows])
        weights.append(max(6, min(longest, 34)))
    total = sum(weights)
    return [width * weight / total for weight in weights]


def add_table(story, lines, header_index, styles, width):
    headers = [cell.strip() for cell in lines[header_index].strip("|").split("|")]
    position = header_index + 2  # skip the header and the separator row
    rows = []
    while position < len(lines) and lines[position].strip().startswith("|"):
        rows.append([cell.strip() for cell in lines[position].strip().strip("|").split("|")])
        position += 1
    if any(len(row) != len(headers) for row in rows):
        raise ValueError("Malformed Markdown table")
    cells = [[Paragraph(rich(value), styles["small"]) for value in row] for row in [headers] + rows]
    table = Table(cells, colWidths=table_widths(headers, rows, width), repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eaf1f8")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c1d0dd")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.extend([table, Spacer(1, 6)])
    return position


def flow_markdown(story, text, base_dir, styles, width, page, temp):
    """Append a Markdown document (with local SVG figures) to the story."""
    lines = text.splitlines()
    position = 0
    while position < len(lines):
        line = lines[position].strip()
        position += 1
        if not line:
            continue
        image = IMAGE_RE.search(line)
        if image:
            target = (base_dir / image.group(2)).resolve()
            if not target.is_file() or ROOT not in target.parents:
                raise FileNotFoundError(f"Missing figure: {target}")
            png = temp / f"{target.stem}.png"
            if not png.exists():
                page.goto(target.as_uri())
                page.evaluate("document.fonts.ready")
                page.locator("svg").screenshot(path=str(png))
            with PILImage.open(png) as picture:
                iw, ih = picture.size
            figure_width = min(width, 172 * mm)
            figure_height = figure_width * ih / iw
            if figure_height > 138 * mm:
                figure_height = 138 * mm
                figure_width = figure_height * iw / ih
            # The manuscripts carry a bilingual "Figure ..." caption on the next lines,
            # so the PDF shows the figure itself here and lets that caption follow.
            story.append(KeepTogether([Image(str(png), width=figure_width, height=figure_height)]))
        elif line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            story.append(Paragraph(rich(line[level:].strip()),
                                   styles["title" if level == 1 else "heading"]))
        elif line.startswith("|") and position < len(lines) and re.match(
                r"^\|\s*:?-{2,}", lines[position].strip()):
            position = add_table(story, lines, position - 1, styles, width)
        elif line.startswith("---"):
            story.append(HRFlowable(width="100%", thickness=0.5))
        elif re.match(r"^[-*]\s+", line):
            story.append(Paragraph("• " + rich(re.sub(r"^[-*]\s+", "", line)), styles["body"]))
        elif re.match(r"^\d+\.\s+", line):
            story.append(Paragraph(rich(line), styles["body"]))
        elif line.startswith("☐"):
            story.append(Paragraph(rich(line), styles["body"]))
        else:
            story.append(Paragraph(rich(line), styles["body"]))


COVER_TEXT = {
    "Day07_Machine_Fundamentals": (
        "検査機の機械部品・センサ・アクチュエータの役割と相互作用を学び、機械の不安定さが検査画像に与える影響を理解します。",
        "Learn the role and interaction of mechanical parts, sensors and actuators, and how mechanical instability degrades inspection images.",
    ),
    "Day08_PLC_Control": (
        "センサからPLC入力・プログラム・出力・ドライバ・アクチュエータまでの流れを学び、簡単なラダーとシーケンスを読めるようになります。",
        "Follow the path from sensor to PLC input, program, output, driver and actuator, and read simple ladder logic and sequences.",
    ),
    "Day09_System_Integration": (
        "画像取得・AI判定・結果の有効性・PLC連携・品質対応・安全境界を、一つの検査システムとして説明できるようになります。",
        "Explain acquisition, AI decision, result validity, PLC integration, quality response and safety boundaries as one inspection system.",
    ),
}

LESSON_TITLES = {
    "Day07_Machine_Fundamentals": ("07-01 機械の基礎 / Mechanical fundamentals",
                                   "07-02 センサと信号 / Sensors and signals",
                                   "07-03 アクチュエータと機械構成 / Actuators and machine construction"),
    "Day08_PLC_Control": ("08-01 PLCの基礎 / PLC fundamentals",
                          "08-02 ラダープログラムの基礎 / Ladder programming basics",
                          "08-03 シーケンス制御 / Sequence control"),
    "Day09_System_Integration": ("09-01 視覚ハードウェア / Vision hardware",
                                 "09-02 産業用PCとAI処理 / Industrial PC and AI processing",
                                 "09-03 システム統合 / Complete system integration"),
}


def cover_story(day_folder, styles, code):
    ja, en = COVER_TEXT[day_folder]
    story = [Paragraph(DAY_TITLES[day_folder], styles["title"]),
             Paragraph(ja, styles["body"]), Paragraph(en, styles["body"]),
             Spacer(1, 8), Paragraph("目次 / Contents", styles["heading"])]
    rows = [["章 / section", "内容 / content"]]
    for index, title in enumerate(LESSON_TITLES[day_folder], start=1):
        rows.append([str(index), title])
    rows.append(["付録 A / Appendix A", "公式・確認カード / formula and check card"])
    rows.append(["付録 B / Appendix B", "技術用語集 / technical glossary"])
    rows.append(["付録 C / Appendix C", "参考資料 / references"])
    table = Table([[Paragraph(rich(cell), styles["small"]) for cell in row] for row in rows],
                  colWidths=[45 * mm, 120 * mm], repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eaf1f8")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c1d0dd")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story += [table, Spacer(1, 10)]
    story.append(Paragraph("時間割 / Timetable", styles["heading"]))
    story.append(Paragraph(
        "08:00–09:00 講師説明 / instructor · 09:00–10:20 ノートブック01 / notebook 01 · "
        "10:20–10:35 休憩 / break · 10:35–12:00 ノートブック02 / notebook 02 · "
        "12:00–12:50 昼食 / lunch · 12:50–13:50 講師実演 / instructor · "
        "13:50–15:10 ノートブック03 前半 / notebook 03 part 1 · 15:10–15:25 休憩 / break · "
        "15:25–16:20 ノートブック03 後半 / notebook 03 part 2 · 16:20–16:50 提出 / submission. "
        "合計 / total 530 min.", styles["body"]))
    story.append(Paragraph("安全 / Safety", styles["heading"]))
    story.append(Paragraph(
        "本資料は教育用です。実機の分解・配線・プログラム変更・安全回路の設計は行いません。"
        " 安全機能は、リスクアセスメントに基づく独立した安全系で実現します。"
        " / Training material only. It does not cover work on real machines, wiring, program changes or safety-circuit design."
        " Safety functions come from an independent system designed from a risk assessment.", styles["body"]))
    return story


def render_day(day_folder: str, browser_page, temp: Path, face: str, width: float) -> Path:
    styles = styles_for(face)
    code, label, quick_reference = DAY_SHORT[day_folder]
    output = PDF_DIR / f"{code}_explanation_ja_en.pdf"
    doc = SimpleDocTemplate(
        str(output), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=18 * mm, bottomMargin=18 * mm, title=DAY_TITLES[day_folder],
    )
    story = cover_story(day_folder, styles, code)
    story.append(PageBreak())
    for index, name in enumerate(DAYS[day_folder]):
        notebook_path = NOTEBOOKS / day_folder / f"{name}.ipynb"
        manuscript = NOTEBOOKS / day_folder / f"{name}.md"
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
        digest = hashlib.sha256(manuscript.read_bytes()).hexdigest()
        if notebook["metadata"].get("day07_09_source_sha256") != digest:
            raise RuntimeError(f"Stale notebook {notebook_path.name}: rebuild before exporting")
        if index:
            story.append(PageBreak())
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#94a9bb")))
        for cell in notebook["cells"]:
            if cell["cell_type"] != "markdown":
                raise ValueError(f"Executable cell in {name}")
            flow_markdown(story, "".join(cell["source"]), notebook_path.parent,
                          styles, width, browser_page, temp)

    story.append(PageBreak())
    flow_markdown(story, (SUPPORT / "reference_data" / quick_reference).read_text(encoding="utf-8"),
                  SUPPORT / "reference_data", styles, width, browser_page, temp)
    story.append(PageBreak())
    flow_markdown(story, (SUPPORT / "worksheets" / "Glossary_ja_en.md").read_text(encoding="utf-8"),
                  SUPPORT / "worksheets", styles, width, browser_page, temp)

    story.append(PageBreak())
    story.append(Paragraph("参考資料 / References", styles["heading"]))
    story.append(Paragraph(
        "本教材の数値例はすべて仮定であり、実機の仕様ではありません。"
        " 出典と図の作成方法は day07_09_support/SOURCES_AND_LICENSES.md を参照してください。"
        " / All numeric examples are hypothetical; they are not machine specifications."
        " See day07_09_support/SOURCES_AND_LICENSES.md for sources and figure authorship.",
        styles["body"],
    ))
    for name, url in REFERENCES:
        story.append(Paragraph(rich(f"{name}: {url}"), styles["source"]))

    def footer(canvas, pdf_doc):
        canvas.saveState()
        canvas.setFont(face, 8)
        canvas.drawString(17 * mm, 10 * mm, f"{label} — 架空の学習用資料 / fictional training material")
        canvas.drawRightString(A4[0] - 17 * mm, 10 * mm, str(pdf_doc.page))
        canvas.restoreState()

    PDF_DIR.mkdir(parents=True, exist_ok=True)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return output


def main() -> None:
    face = register_font()
    width = A4[0] - 40 * mm
    chrome = next((candidate for candidate in BROWSERS if candidate.exists()), None)
    if chrome is None:
        raise RuntimeError("Local Chrome or Edge not found; cannot render SVG figures")
    with tempfile.TemporaryDirectory(prefix="day0709_pdf_") as temporary:
        temp = Path(temporary)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, executable_path=str(chrome))
            try:
                page = browser.new_page(viewport={"width": 1500, "height": 1100}, device_scale_factor=1.6)
                for day_folder in DAYS:
                    output = render_day(day_folder, page, temp, face, width)
                    print(f"Exported {output.relative_to(ROOT)}")
            finally:
                browser.close()


if __name__ == "__main__":
    main()
