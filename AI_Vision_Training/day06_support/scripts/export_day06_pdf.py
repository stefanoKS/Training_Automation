"""Export the five Day 6 Markdown-only notebooks as an independent A4 PDF.

Run from any directory: python AI_Vision_Training\\day06_support\\scripts\\export_day06_pdf.py
Requires ReportLab, Pillow, Playwright and a locally installed Chrome or Edge browser.
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

from build_day06_notebooks import LESSONS, LESSON_DIR, ROOT
from render_pricing import load_snapshot

OUTPUT = ROOT / "docs" / "pdf" / "Day06_explanation_ja_en.pdf"
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def font() -> str:
    candidates = (
        Path("C:/Windows/Fonts/meiryo.ttc"),
        Path("C:/Windows/Fonts/YuGothR.ttc"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    )
    for candidate in candidates:
        if candidate.exists():
            pdfmetrics.registerFont(TTFont("Day06Japanese", str(candidate), subfontIndex=0))
            return "Day06Japanese"
    raise RuntimeError("No supported Japanese-capable font found; PDF not exported")


def rich(text: str) -> str:
    text = escape(text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r'<font color="#175a70">\1</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text.replace("  ", " ").replace(" / ", " / ")


def export() -> None:
    face = font()
    styles = {
        "body": ParagraphStyle(
            "body", fontName=face, fontSize=11, leading=18.5, spaceAfter=9,
            textColor=colors.HexColor("#223344"), wordWrap="CJK",
        ),
        "title": ParagraphStyle(
            "title", fontName=face, fontSize=17, leading=24, spaceBefore=8,
            spaceAfter=12, textColor=colors.HexColor("#164b79"), wordWrap="CJK",
        ),
        "heading": ParagraphStyle(
            "heading", fontName=face, fontSize=13, leading=19, spaceBefore=12,
            spaceAfter=9, textColor=colors.HexColor("#164b79"), wordWrap="CJK",
        ),
        "small": ParagraphStyle(
            "small", fontName=face, fontSize=9, leading=13.5, spaceAfter=5,
            wordWrap="CJK",
        ),
        "source": ParagraphStyle(
            "source", fontName=face, fontSize=8.3, leading=11.8, spaceAfter=4,
            wordWrap="CJK",
        ),
    }
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=20 * mm, bottomMargin=20 * mm,
        title="第6日：AIエージェントによるソフトウェア開発入門 / Day 6",
    )
    width = A4[0] - 40 * mm
    story = []
    with tempfile.TemporaryDirectory(prefix="day06_pdf_") as temporary:
        temp = Path(temporary)
        browsers = (
            Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
            Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
        )
        chrome = next((candidate for candidate in browsers if candidate.exists()), None)
        if chrome is None:
            raise RuntimeError("Local Chrome or Edge not found; cannot render Japanese SVG text")
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, executable_path=str(chrome))
            try:
                page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1.5)
                for index, name in enumerate(LESSONS):
                    notebook_path = LESSON_DIR / f"{name}.ipynb"
                    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
                    source = LESSON_DIR / f"{name}.md"
                    digest = hashlib.sha256(source.read_bytes()).hexdigest()
                    if notebook["metadata"].get("day06_source_sha256") != digest:
                        raise RuntimeError(f"Stale notebook: rebuild {notebook_path.name} before exporting")
                    if index:
                        story.append(PageBreak())
                    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#94a9bb")))
                    for cell in notebook["cells"]:
                        if cell["cell_type"] != "markdown":
                            raise ValueError(f"Executable cell in {name}")
                        lines = "".join(cell["source"]).splitlines()
                        position = 0
                        while position < len(lines):
                            line = lines[position].strip()
                            position += 1
                            if not line:
                                continue
                            image = IMAGE_RE.search(line)
                            if image:
                                target = (notebook_path.parent / image.group(2)).resolve()
                                if not target.is_file() or ROOT not in target.parents:
                                    raise FileNotFoundError(f"Missing Day 6 figure: {target}")
                                png = temp / f"{name}_{target.stem}.png"
                                if not png.exists():
                                    page.goto(target.as_uri())
                                    page.evaluate("document.fonts.ready")
                                    page.locator("svg").screenshot(path=str(png))
                                with PILImage.open(png) as picture:
                                    iw, ih = picture.size
                                figure_width = min(width, 170 * mm)
                                figure_height = figure_width * ih / iw
                                if figure_height > 125 * mm:
                                    figure_height = 125 * mm
                                    figure_width = figure_height * iw / ih
                                story.append(KeepTogether([
                                    Image(str(png), width=figure_width, height=figure_height),
                                    Paragraph(rich(image.group(1)), styles["small"]),
                                ]))
                            elif line.startswith("#"):
                                level = len(line) - len(line.lstrip("#"))
                                story.append(Paragraph(rich(line[level:].strip()), styles["title" if level == 1 else "heading"]))
                            elif line.startswith("|") and position < len(lines) and re.match(r"^\|\s*:?-{2,}", lines[position].strip()):
                                headers = [x.strip() for x in line.strip("|").split("|")]
                                position += 1
                                rows = [headers]
                                while position < len(lines) and lines[position].strip().startswith("|"):
                                    rows.append([x.strip() for x in lines[position].strip().strip("|").split("|")])
                                    position += 1
                                columns = len(headers)
                                if any(len(row) != columns for row in rows):
                                    raise ValueError(f"Malformed table in {name}")
                                cells = [[Paragraph(rich(value), styles["small"]) for value in row] for row in rows]
                                column_widths = (
                                    [width * fraction for fraction in (0.27, 0.12, 0.12, 0.17, 0.32)]
                                    if columns == 5 and headers[0].startswith("提供元")
                                    else [width / columns] * columns
                                )
                                table = Table(cells, colWidths=column_widths, repeatRows=1, hAlign="LEFT")
                                table.setStyle(TableStyle([
                                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eaf1f8")),
                                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c1d0dd")),
                                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                                ]))
                                story.extend([table, Spacer(1, 7)])
                            elif line.startswith("---"):
                                story.append(HRFlowable(width="100%", thickness=0.5))
                            else:
                                story.append(Paragraph(rich(line), styles["body"]))
            finally:
                browser.close()
        story.append(PageBreak())
        story.append(Paragraph("参考資料・完了チェック / References and completion checklist", styles["heading"]))
        story.append(Paragraph(
            "公式資料と各図の出典は day06_support/SOURCES_AND_LICENSES.md。"
            " 目的・要件・計画・実装・試験・人による受入を確認。"
            " / Official references and figure authorship: day06_support/SOURCES_AND_LICENSES.md."
            " Check purpose, requirements, plan, implementation, tests and human acceptance.",
            styles["body"],
        ))
        for label, url in (
            ("GitHub Copilot", "https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-on-github"),
            ("VS Code", "https://code.visualstudio.com/docs/chat/chat-overview"),
            ("Anthropic Claude Code", "https://code.claude.com/docs/en/overview"),
            ("OpenAI ChatGPT Work and Codex", "https://help.openai.com/en/articles/20001275"),
        ):
            story.append(Paragraph(rich(f"{label}: {url}"), styles["small"]))
        snapshot = load_snapshot()
        story.append(Spacer(1, 8))
        story.append(Paragraph(
            f"API価格の公式出典（{snapshot['verified_on']}） / Official API pricing sources",
            styles["heading"],
        ))
        story.append(Paragraph(
            "以下のリンクは表の各モデルに対応します。料金単位は米ドル/100万トークン。"
            "最新の単価と条件は使用前に公式サイトで確認してください。"
            " / Links correspond to each model in the lesson table. Units: USD per million tokens."
            " Recheck official rates and conditions before use.",
            styles["body"],
        ))
        for row in snapshot["entries"]:
            story.append(Paragraph(
                rich(f"{row['provider']} — {row['model_id']} ({row['condition']}): {row['source']}"),
                styles["source"],
            ))

        def footer(canvas, pdf_doc):
            canvas.saveState()
            canvas.setFont(face, 8)
            canvas.drawString(17 * mm, 10 * mm, "第6日 / Day 6 — 架空の学習用資料 / fictional training material")
            canvas.drawRightString(A4[0] - 17 * mm, 10 * mm, str(pdf_doc.page))
            canvas.restoreState()

        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Exported {OUTPUT}")


if __name__ == "__main__":
    export()
