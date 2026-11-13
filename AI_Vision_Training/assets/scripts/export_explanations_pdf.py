"""ノートブックの説明から、日ごとの解説 PDF を作ります。

Build the offline explanation PDFs **from the notebooks themselves**, so the prose cannot drift
away from what the learners read in Jupyter. Nothing is retrained and no model is downloaded:
only Markdown cells, the figures those cells reference, and short code examples are used.

作られるもの / What is produced (docs/pdf/)
-----------------------------------------
Day01_explanation_ja_en.pdf … Day05_explanation_ja_en.pdf
Week1_explanation_ja_en.pdf     （5 日分をまとめたもの / all five days)

含めるもの / Included
---------------------
* 学習目標・前提・説明・静的図（キャプション付き）
* 短いコード例（学習者が書き換えるセルだけ / only the cells a learner edits)
* 演習・ヒント・理解度チェック（ノートブックにあるもの / as written in the notebook）
* 出典（ノートブックのパス、図の由来）

含めないもの / Excluded
-----------------------
* 実行ログ・スタックトレース・生の JSON（コード出力は一切使わない / no cell outputs at all)
* 長い準備コード、`advanced-prep` タグのセル
* 講師用の解答（`docs/instructor/...` を指す行 / lines pointing at instructor answer keys)
* 実行していない学習・検証の結果（保存された結果だけを「参考出力」として示す）

使い方 / Usage
--------------
    python assets\\scripts\\export_explanations_pdf.py
    python assets\\scripts\\export_explanations_pdf.py --only Day03
    python assets\\scripts\\export_explanations_pdf.py --check     # 生成せず点検のみ / verify only

必要なもの / Requires
---------------------
`requirements/pdf.txt`（reportlab）。学習者用の `requirements/base.txt` とは分けてあります。
Install with:  python -m pip install -r requirements\\pdf.txt
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Flowable, Frame, HRFlowable, Image, KeepTogether, NextPageTemplate,
    PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

COURSE_ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK_DIR = COURSE_ROOT / "notebooks"
OUTPUT_DIR = COURSE_ROOT / "docs" / "pdf"

COURSE_TITLE_JA = "広島化成 第 1 週 AI・マシンビジョン研修"
COURSE_TITLE_EN = "Hiroshima Kasei Week 1 AI & Machine Vision Training"
BUILD_DATE = _dt.date.today().isoformat()

REBUILD_COMMAND = r"python assets\scripts\export_explanations_pdf.py"

INK = colors.HexColor("#24292f")
MUTED = colors.HexColor("#57606a")
ACCENT = colors.HexColor("#1f6feb")
RULE = colors.HexColor("#d0d7de")
CODE_BG = colors.HexColor("#f6f8fa")
NOTE_BG = colors.HexColor("#f2f6ff")

PAGE_W, PAGE_H = A4
MARGIN_X = 18 * mm
MARGIN_TOP = 20 * mm
MARGIN_BOTTOM = 18 * mm
FRAME_W = PAGE_W - 2 * MARGIN_X

MAX_IMAGE_W = FRAME_W
MAX_IMAGE_H = 106 * mm

# 横長すぎる図は縦向きだと文字が小さくなりすぎる。図の「自然な幅」で判断する。
# Very wide figures become unreadable in portrait, so judge by the figure's natural width
# (the teaching generators draw at 140 dpi).
FIGURE_DPI = 140
PORTRAIT_MAX_NATURAL_WIDTH_MM = 236.0     # ~9.3 in; wider than this goes on a landscape page
LAND_MARGIN_X = 14 * mm
LAND_MARGIN_TOP = 16 * mm
LAND_MARGIN_BOTTOM = 14 * mm
LAND_FRAME_W = PAGE_H - 2 * LAND_MARGIN_X
LAND_FRAME_H = PAGE_W - LAND_MARGIN_TOP - LAND_MARGIN_BOTTOM
LAND_MAX_IMAGE_H = LAND_FRAME_H - 34 * mm
MAX_CODE_CHARS = 88

WIDGET_MARKERS = ("ipywidgets", "widgets.interact", "IntSlider", "interactive(")
INSTRUCTOR_MARKERS = ("docs/instructor", "docs\\instructor")


# ---------------------------------------------------------------------------
# fonts
# ---------------------------------------------------------------------------


def _find_font(candidates: list[tuple[Path, int]]) -> tuple[Path, int]:
    for path, index in candidates:
        if path.exists():
            return path, index
    raise SystemExit(
        "日本語フォントが見つかりません / no Japanese font found. Looked for:\n  "
        + "\n  ".join(str(p) for p, _ in candidates)
    )


def register_fonts() -> tuple[str, str]:
    """日本語が出るフォントを登録する / register a Japanese-capable font pair."""
    regular_candidates = [
        (Path("C:/Windows/Fonts/NotoSansJP-Regular.ttf"), 0),
        (Path("C:/Windows/Fonts/YuGothR.ttc"), 0),
        (Path("C:/Windows/Fonts/meiryo.ttc"), 0),
        (Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"), 0),
        (Path("/usr/share/fonts/truetype/noto/NotoSansJP-Regular.ttf"), 0),
        (Path("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"), 0),
    ]
    bold_candidates = [
        (Path("C:/Windows/Fonts/NotoSansJP-Bold.ttf"), 0),
        (Path("C:/Windows/Fonts/YuGothB.ttc"), 0),
        (Path("C:/Windows/Fonts/meiryob.ttc"), 0),
        (Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"), 0),
        (Path("/usr/share/fonts/truetype/noto/NotoSansJP-Bold.ttf"), 0),
        (Path("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"), 0),
    ]
    regular, index = _find_font(regular_candidates)
    try:
        bold, bold_index = _find_font(bold_candidates)
    except SystemExit:
        bold, bold_index = regular, index

    pdfmetrics.registerFont(TTFont("JP", str(regular), subfontIndex=index))
    pdfmetrics.registerFont(TTFont("JP-Bold", str(bold), subfontIndex=bold_index))
    # 斜体・太字斜体も同じ書体にする（グリフ欠けを避ける / avoid missing glyphs）
    registerFontFamily("JP", normal="JP", bold="JP-Bold", italic="JP", boldItalic="JP-Bold")
    pdfmetrics.registerFont(TTFont("Mono", str(regular), subfontIndex=index))
    return regular.name, bold.name


def build_styles() -> dict[str, ParagraphStyle]:
    base = dict(fontName="JP", textColor=INK, alignment=TA_LEFT)
    return {
        "cover_title": ParagraphStyle("cover_title", fontSize=25, leading=33, spaceAfter=8,
                                      **{**base, "textColor": ACCENT}),
        "cover_sub": ParagraphStyle("cover_sub", fontSize=15, leading=21, spaceAfter=6, **base),
        "cover_meta": ParagraphStyle("cover_meta", fontSize=10, leading=15, textColor=MUTED,
                                     fontName="JP"),
        "bookmark": ParagraphStyle("bookmark", fontSize=12, leading=16, **base),
        "h1": ParagraphStyle("h1", fontSize=16.5, leading=22, spaceBefore=4, spaceAfter=6,
                             fontName="JP-Bold", textColor=ACCENT, keepWithNext=1),
        "h2": ParagraphStyle("h2", fontSize=13, leading=18, spaceBefore=12, spaceAfter=5,
                             fontName="JP-Bold", textColor=INK, keepWithNext=1),
        "h3": ParagraphStyle("h3", fontSize=11, leading=15.5, spaceBefore=9, spaceAfter=4,
                             fontName="JP-Bold", textColor=colors.HexColor("#1a3d6d"),
                             keepWithNext=1),
        "h4": ParagraphStyle("h4", fontSize=10, leading=14, spaceBefore=7, spaceAfter=3,
                             fontName="JP-Bold", textColor=INK, keepWithNext=1),
        "body": ParagraphStyle("body", fontSize=9.3, leading=13.6, spaceAfter=4, **base),
        "note": ParagraphStyle("note", fontSize=8.6, leading=12.4, textColor=MUTED, spaceAfter=4,
                               fontName="JP"),
        "bullet": ParagraphStyle("bullet", fontSize=9.3, leading=13.4, leftIndent=10,
                                 bulletIndent=2, spaceAfter=1.5, **base),
        "caption": ParagraphStyle("caption", fontSize=8.4, leading=11.8, textColor=MUTED,
                                  spaceBefore=1, spaceAfter=6, fontName="JP"),
        "code": ParagraphStyle("code", fontSize=7.7, leading=10.4, fontName="Mono",
                               textColor=INK),
        "code_label": ParagraphStyle("code_label", fontSize=7.8, leading=10, textColor=MUTED,
                                     fontName="JP", spaceBefore=4, spaceAfter=2),
        "table": ParagraphStyle("table", fontSize=8.2, leading=11, **base),
        "table_head": ParagraphStyle("table_head", fontSize=8.2, leading=11, fontName="JP-Bold",
                                     textColor=INK),
        "toc0": ParagraphStyle("toc0", fontSize=10.5, leading=15, fontName="JP-Bold",
                               textColor=INK, spaceBefore=6),
        "toc1": ParagraphStyle("toc1", fontSize=9.2, leading=13, leftIndent=10, fontName="JP"),
        "toc2": ParagraphStyle("toc2", fontSize=8.4, leading=12, leftIndent=22, fontName="JP",
                               textColor=MUTED),
        "warn": ParagraphStyle("warn", fontSize=8.6, leading=12, textColor=colors.HexColor("#9a6700"),
                               fontName="JP"),
    }


# ---------------------------------------------------------------------------
# markdown -> flowables
# ---------------------------------------------------------------------------


def _esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _inline(text: str) -> str:
    """Markdown のインライン記法を組版用のタグにする / turn inline Markdown into reportlab markup."""
    # インラインコードを先に退避する（`**` などを中で誤解釈しないため）
    # take code spans out first so their contents are never read as bold markers
    spans: dict[str, str] = {}

    def keep_code(match: re.Match) -> str:
        key = f"\x00{len(spans)}\x00"
        spans[key] = f'<font name="Mono" size="8.6">{_esc(match.group(1))}</font>'
        return key

    text = re.sub(r"`([^`]+)`", keep_code, text)
    text = _esc(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)
    for key, replacement in spans.items():
        text = text.replace(key, replacement)
    return text


def _is_heading(line: str) -> tuple[int, str] | None:
    match = re.match(r"^(#{1,4})\s+(.*)$", line)
    if not match:
        return None
    return len(match.group(1)), match.group(2).strip()


def _is_japanese(text: str) -> bool:
    return bool(re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", text))


HEADING_STYLES = {1: "h1", 2: "h2", 3: "h3", 4: "h4"}
HEADING_TOC = {1: 1, 2: 1, 3: 2, 4: None}     # level -> TOC depth
# 目次に載せない見出し（出力待ちの見出しなど）/ headings kept out of the table of contents
NOT_IN_TOC = ("実行結果の例", "Expected output", "コード例", "code example")


class Heading(Paragraph):
    """TOC に載る見出し / a heading that also writes a table-of-contents entry."""

    def __init__(self, text: str, style: ParagraphStyle, toc_level: int | None):
        super().__init__(text, style)
        self.toc_level = toc_level


def _heading_flowable(level: int, ja: str, en: str | None, styles: dict,
                      toc_level: int | None = -1) -> Heading:
    style = styles[HEADING_STYLES[level]]
    if en:
        markup = f"{_inline(ja)}<br/><font size=\"{max(7.6, style.fontSize - 1.6)}\" " \
                 f"color=\"#57606a\">{_inline(en)}</font>"
        plain = f"{ja} / {en}"
    else:
        markup = _inline(ja)
        plain = ja
    depth = HEADING_TOC[level] if toc_level == -1 else toc_level
    if any(marker in plain for marker in NOT_IN_TOC):
        depth = None
    flowable = Heading(markup, style, depth)
    flowable.toc_text = plain
    return flowable


def _wrap_code_line(line: str, limit: int) -> list[str]:
    """長い行を折り返す（切り取られないように）/ wrap a long line instead of clipping it."""
    pieces = []
    while len(line) > limit:
        cut = line.rfind(" ", 0, limit)
        if cut <= limit // 3:
            cut = limit
        pieces.append(line[:cut].rstrip())
        line = "    ↳ " + line[cut:].lstrip()
    pieces.append(line)
    return pieces


def _code_flowable(code: str, styles: dict) -> list:
    lines: list[str] = []
    for line in code.splitlines():
        lines.extend(_wrap_code_line(line.rstrip(), MAX_CODE_CHARS))
    # 空白を &nbsp; にして、Python のインデントをそのまま保つ / keep the indentation exactly
    body = "<br/>".join(_esc(line).replace(" ", "&nbsp;") for line in lines)
    text = Paragraph(body, styles["code"])
    table = Table([[text]], colWidths=[FRAME_W])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
        ("BOX", (0, 0), (-1, -1), 0.4, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return [table, Spacer(1, 5)]


def _paragraph_flowable(text: str, styles: dict) -> Paragraph:
    return Paragraph(_inline(text), styles["body"])


def _bullet_flowable(text: str, styles: dict, depth: int = 0) -> Paragraph:
    style = ParagraphStyle(
        f"bullet{depth}", parent=styles["bullet"],
        leftIndent=10 + 10 * depth, bulletIndent=2 + 10 * depth)
    return Paragraph(_inline(text), style, bulletText="•")


def _table_flowable(rows: list[list[str]], styles: dict) -> Table:
    columns = max(len(row) for row in rows)
    rows = [row + [""] * (columns - len(row)) for row in rows]
    data = []
    for index, row in enumerate(rows):
        style = styles["table_head"] if index == 0 else styles["table"]
        data.append([Paragraph(_inline(cell), style) for cell in row])

    # 列幅は「見た目の長さ」の比率で決める（日本語は 1 文字を 2 として数える）
    # column widths follow the visible length; a Japanese character counts as two
    def display_len(text: str) -> int:
        return sum(2 if JP_CHAR_RE.match(char) else 1 for char in text)

    weights = []
    for column in range(columns):
        longest = max(display_len(row[column]) for row in rows) or 1
        weights.append(min(max(longest, 8), 64))
    total = sum(weights)
    widths = [FRAME_W * weight / total for weight in weights]

    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eef4ff")),
        ("GRID", (0, 0), (-1, -1), 0.4, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3.5),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    return table


def _note_flowable(text: str, styles: dict, colour=NOTE_BG) -> Table:
    table = Table([[Paragraph(_inline(text), styles["note"])]], colWidths=[FRAME_W])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colour),
        ("BOX", (0, 0), (-1, -1), 0.4, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def _image_size(path: Path) -> tuple[int, int]:
    with PILImage.open(path) as handle:
        return handle.size


def _image_flowable(path: Path, max_w: float = MAX_IMAGE_W,
                    max_h: float = MAX_IMAGE_H) -> Image:
    width, height = _image_size(path)
    scale = min(max_w / width, max_h / height, 1.0)
    return Image(str(path), width=width * scale, height=height * scale)


IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")
JP_CHAR_RE = re.compile(r"[\u3040-\u30ff\u4e00-\u9fff\uff01-\uff60]")


def _markdown_flowables(text: str, notebook_dir: Path, styles: dict) -> list:
    """1 つの Markdown セルを flowable の並びにする / convert one Markdown cell."""
    lines = text.splitlines()
    flowables: list = []
    cell_start = 0
    index = 0

    # 「実行結果の例」だけのセルは、ノートブックで見る旨の注記にする
    stripped = [line for line in lines if line.strip() and not line.strip().startswith("---")]
    if stripped and all(_is_heading(line) for line in stripped):
        joined = " ".join(line for line in stripped)
        if "実行結果の例" in joined or "Expected output" in joined:
            return [_note_flowable(
                "この節の出力はノートブックで実行すると表示されます / "
                "run the notebook to see this output.", styles)]

    while index < len(lines):
        line = lines[index]
        stripped_line = line.strip()

        if not stripped_line:
            index += 1
            continue

        if stripped_line in ("---", "***", "___"):
            flowables.append(Spacer(1, 3))
            flowables.append(HRFlowable(width="100%", thickness=0.6, color=RULE, spaceAfter=5))
            index += 1
            continue

        if any(marker in stripped_line for marker in INSTRUCTOR_MARKERS):
            index += 1
            continue

        heading = _is_heading(stripped_line)
        if heading:
            level, title = heading
            # 直後の同レベル見出しが英語だけなら、日本語＋英語の 1 つに見出しとして組む
            english = None
            if not _is_japanese(title) and index + 1 < len(lines):
                english = title
                title = ""
            elif index + 1 < len(lines):
                nxt = _is_heading(lines[index + 1].strip())
                if nxt and nxt[0] == level and not _is_japanese(nxt[1]):
                    english = nxt[1]
                    index += 1
            if not title:
                title = english or ""
                english = None
            flowables.append(_heading_flowable(level, title, english, styles))
            index += 1
            continue

        image_match = IMAGE_RE.search(stripped_line)
        if image_match:
            target = image_match.group(2)
            if not target.startswith(("http://", "https://", "data:")):
                resolved = (notebook_dir / target).resolve()
                if resolved.is_file():
                    caption_lines = []
                    probe = index + 1
                    while probe < len(lines) and len(caption_lines) < 2:
                        candidate = lines[probe].strip()
                        if candidate and (candidate.startswith("図") or
                                          candidate.startswith("Figure")):
                            caption_lines.append(candidate)
                        elif candidate:
                            break
                        probe += 1
                    caption = "<br/>".join(_inline(text_) for text_ in caption_lines)
                    width, height = _image_size(resolved)
                    natural_width_mm = width / FIGURE_DPI * 25.4
                    wide = natural_width_mm > PORTRAIT_MAX_NATURAL_WIDTH_MM
                    if wide:
                        block = [_image_flowable(resolved, LAND_FRAME_W, LAND_MAX_IMAGE_H)]
                        if caption:
                            block.append(Paragraph(caption, styles["caption"]))
                        # 直前に出した見出しは、図と同じ横長ページへ移す（見出しだけ取り残さない）
                        # carry the heading emitted in this cell onto the figure page
                        carry: list = []
                        while len(flowables) > cell_start and isinstance(flowables[-1], Heading):
                            carry.insert(0, flowables.pop())
                        flowables.append(NextPageTemplate("landscape"))
                        flowables.append(PageBreak())
                        flowables.extend(carry)
                        flowables.append(KeepTogether(block))
                        # 元の縦向きに戻す指示は「改ページの前」に置く
                        # switch back BEFORE the break, or the next page keeps the landscape
                        flowables.append(NextPageTemplate("body"))
                        flowables.append(PageBreak())
                    else:
                        block = [_image_flowable(resolved)]
                        if caption:
                            block.append(Paragraph(caption, styles["caption"]))
                        flowables.append(KeepTogether(block))
                    index = probe if caption_lines else index + 1
                    continue
            index += 1
            continue

        if stripped_line.startswith("```"):
            fence = stripped_line[:3]
            body = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith(fence):
                body.append(lines[index])
                index += 1
            index += 1
            flowables.extend(_code_flowable("\n".join(body), styles))
            continue

        if stripped_line.startswith(">"):
            body = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                body.append(lines[index].strip()[1:].strip())
                index += 1
            flowables.append(_note_flowable(" ".join(body), styles))
            continue

        if stripped_line.startswith("|"):
            rows = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                cells = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", cell) for cell in cells):
                    rows.append(cells)
                index += 1
            if rows:
                flowables.append(Spacer(1, 2))
                flowables.append(_table_flowable(rows, styles))
                flowables.append(Spacer(1, 6))
            continue

        bullet_match = re.match(r"^(\s*)([-*・]|\d+[.)])\s+(.*)$", line)
        if bullet_match:
            indent = len(bullet_match.group(1))
            flowables.append(_bullet_flowable(bullet_match.group(3), styles, indent // 2))
            index += 1
            continue

        # 段落 / paragraph
        body = []
        while index < len(lines):
            candidate = lines[index]
            stripped_candidate = candidate.strip()
            if not stripped_candidate:
                break
            if (stripped_candidate.startswith(("```", ">", "|"))
                    or _is_heading(stripped_candidate)
                    or IMAGE_RE.search(stripped_candidate)
                    or re.match(r"^(\s*)([-*・]|\d+[.)])\s+", candidate)
                    or stripped_candidate in ("---", "***", "___")):
                break
            body.append(stripped_candidate)
            index += 1
        if body:
            flowables.append(_paragraph_flowable(" ".join(body), styles))
        else:
            index += 1

    return flowables


# ---------------------------------------------------------------------------
# notebook -> flowables
# ---------------------------------------------------------------------------


NOTEBOOK_TITLE_RE = re.compile(r"^#\s+(.*)$", re.M)


def notebook_title(nb: dict) -> tuple[str, str]:
    first = "".join(nb["cells"][0]["source"])
    ja, en = "", ""
    for line in first.splitlines():
        match = NOTEBOOK_TITLE_RE.match(line.strip())
        if not match:
            continue
        text = match.group(1).strip()
        if _is_japanese(text) and not ja:
            ja = text
        elif not en:
            en = text
    return ja or en, en


def clean_code(source: str) -> str:
    lines = [line for line in source.splitlines() if not line.startswith("# ▸")]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def code_is_worth_showing(cell: dict, code: str) -> bool:
    role = cell.get("metadata", {}).get("aivision_role")
    tags = cell.get("metadata", {}).get("tags", [])
    if "advanced-prep" in tags:
        return False
    if any(marker in code for marker in WIDGET_MARKERS):
        return False
    if "%pip" in code or "!pip" in code or "pip install" in code:
        return False
    lines = code.splitlines()
    if not lines:
        return False
    if role == "run-only" and len(lines) > 6:
        return False
    if len(lines) > 20:
        return False
    return True


def notebook_flowables(path: Path, styles: dict, title_toc_level: int = 1) -> list:
    nb = json.loads(path.read_text(encoding="utf-8"))
    ja, en = notebook_title(nb)
    flowables: list = [PageBreak()]
    flowables.append(_heading_flowable(1, ja, en or None, styles, toc_level=title_toc_level))
    flowables.append(Paragraph(
        _inline(f"ノートブック / notebook: `{path.relative_to(COURSE_ROOT).as_posix()}`"),
        styles["note"]))

    for position, cell in enumerate(nb["cells"]):
        source = "".join(cell["source"])
        if cell["cell_type"] == "markdown":
            if position == 0:
                # 先頭セルの H1（ノートブック表題）は上ですでに見出しにしているので落とす。
                # H2 以降は本文の一部なので残す / drop only the title lines, keep the rest.
                lines = source.splitlines()
                while lines:
                    stripped_line = lines[0].strip()
                    heading = _is_heading(stripped_line)
                    if not stripped_line or stripped_line in ("---", "***", "___"):
                        lines.pop(0)
                        continue
                    if heading and heading[0] == 1:
                        lines.pop(0)
                        continue
                    break
                source = "\n".join(lines)
            flowables.extend(_markdown_flowables(source, path.parent, styles))
            continue

        code = clean_code(source)
        if not code:
            continue
        if any(marker in code for marker in WIDGET_MARKERS):
            flowables.append(_note_flowable(
                "この節はノートブック上での対話操作です。PDF では前の静的図で代わりに示しています。"
                " / This section is interactive in the notebook only; the static figure above "
                "stands in for it here.", styles, colour=colors.HexColor("#fffaf0")))
            continue
        if not code_is_worth_showing(cell, code):
            continue
        flowables.append(Paragraph("コード例 / code example", styles["code_label"]))
        flowables.extend(_code_flowable(code, styles))

    return flowables


# ---------------------------------------------------------------------------
# document template
# ---------------------------------------------------------------------------


class ExplanationDoc(BaseDocTemplate):
    def __init__(self, filename, *, footer_label: str, styles: dict, **kwargs):
        super().__init__(filename, pagesize=A4, leftMargin=MARGIN_X, rightMargin=MARGIN_X,
                         topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM,
                         title=footer_label, author="Training_Automation course",
                         subject="Bilingual explanation companion", **kwargs)
        self.footer_label = footer_label
        self.styles = styles
        portrait_frame = Frame(MARGIN_X, MARGIN_BOTTOM, FRAME_W,
                               PAGE_H - MARGIN_TOP - MARGIN_BOTTOM, id="body")
        landscape_frame = Frame(LAND_MARGIN_X, LAND_MARGIN_BOTTOM, LAND_FRAME_W,
                                LAND_FRAME_H, id="figure")
        self.addPageTemplates([
            PageTemplate(id="cover", frames=[portrait_frame]),
            PageTemplate(id="body", frames=[portrait_frame], onPage=self._draw_header_footer),
            # 横長の図のページ / a landscape page for very wide figures
            PageTemplate(id="landscape", frames=[landscape_frame],
                         onPage=self._draw_header_footer,
                         pagesize=(PAGE_H, PAGE_W)),
        ])

    def _draw_header_footer(self, canvas, doc):
        width, height = canvas._pagesize
        margin = LAND_MARGIN_X if width > height else MARGIN_X
        canvas.saveState()
        canvas.setFont("JP", 7.6)
        canvas.setFillColor(MUTED)
        canvas.drawString(margin, height - MARGIN_TOP + 6 * mm, self.footer_label)
        canvas.drawRightString(width - margin, height - MARGIN_TOP + 6 * mm, COURSE_TITLE_JA)
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.5)
        canvas.line(margin, height - MARGIN_TOP + 4.5 * mm,
                    width - margin, height - MARGIN_TOP + 4.5 * mm)
        canvas.drawString(margin, MARGIN_BOTTOM - 8 * mm, f"p. {doc.page}")
        canvas.drawRightString(width - margin, MARGIN_BOTTOM - 8 * mm,
                               "再生成 / rebuild: " + REBUILD_COMMAND)
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if not isinstance(flowable, Heading) or flowable.toc_level is None:
            return
        text = getattr(flowable, "toc_text", None) or flowable.getPlainText()
        self.notify("TOCEntry", (flowable.toc_level, text, self.page))


# ---------------------------------------------------------------------------
# day definitions
# ---------------------------------------------------------------------------


DAYS = {
    "Day01": dict(
        ja="第 1 日　AI とデジタル画像の基礎", en="Day 1 — AI and the basics of digital images",
        notebooks=["Day01_01_Introduction_to_AI", "Day01_02_Pixels_and_Images",
                   "Day01_03_Computer_Vision_Tasks"],
        prerequisites="Python の知識は不要です。`00_Environment_Setup.ipynb` を済ませてください。"
                      " / No prior programming. Finish the environment setup first.",
        objectives=[
            "プログラム・自動化・AI の違いを、現場の言葉で説明できる",
            "画素・解像度・RGB が、検査の見え方をどう決めるかを説明できる",
            "分類・検出・セグメンテーション・異常検知の出力の違いを選べる",
        ],
    ),
    "Day02": dict(
        ja="第 2 日　Python と OpenCV の基礎", en="Day 2 — Python and OpenCV fundamentals",
        notebooks=["Day02_01_Python_Basics", "Day02_02_Conditions_Loops_Functions",
                   "Day02_03_OpenCV_Image_Processing"],
        prerequisites="第 1 日の内容（画素と RGB）。プログラミング経験は不要です。"
                      " / Day 1 (pixels and RGB). No programming experience required.",
        objectives=[
            "変数・条件・繰り返し・関数を、測定値の判定に使える",
            "グレースケール・2 値化・輪郭という処理の流れを説明できる",
            "画素を mm に変換し、校正の限界を説明できる",
        ],
    ),
    "Day03": dict(
        ja="第 3 日　YOLO による物体検出の基礎", en="Day 3 — Object detection with YOLO",
        notebooks=["Day03_01_YOLO_Concepts", "Day03_02_YOLO_Inference",
                   "Day03_03_YOLO_Experiments"],
        prerequisites="第 2 日（Python と OpenCV）。GPU は不要です。"
                      " / Day 2. No GPU required.",
        objectives=[
            "バウンディングボックスを 4 つ／5 つの数で読み書きできる",
            "IoU を計算し、検出の良し悪しを数で説明できる",
            "confidence と解像度が検出結果をどう変えるかを説明できる",
        ],
    ),
    "Day04": dict(
        ja="第 4 日　YOLO の学習と評価", en="Day 4 — Training and evaluating YOLO",
        notebooks=["Day04_01_YOLO_Dataset_Annotation", "Day04_02_YOLO_Training",
                   "Day04_03_YOLO_Evaluation"],
        prerequisites="第 3 日（検出の読み方）。学習には CPU で数分かかります。"
                      " / Day 3. Training takes a few minutes on CPU.",
        objectives=[
            "YOLO 形式のラベルを読み、データセットの分割を説明できる",
            "epoch・batch・学習曲線を読み、学習の良し悪しを判断できる",
            "物体単位と画像単位の指標を混同せずに報告できる",
        ],
    ),
    "Day05": dict(
        ja="第 5 日　PatchCore による異常検知と手法比較",
        en="Day 5 — Anomaly detection with PatchCore and method comparison",
        notebooks=["Day05_01_Anomaly_Detection_Concepts", "Day05_02_PatchCore_Training",
                   "Day05_03_YOLO_vs_PatchCore"],
        prerequisites="第 4 日（学習と評価）。PatchCore の学習は CPU で 1〜2 分です。"
                      " / Day 4. PatchCore fit takes 1–2 minutes on CPU.",
        objectives=[
            "パッチ・特徴・記憶（memory bank）・最近傍の流れを説明できる",
            "較正用データでしきい値を決め、試験用データで 1 回だけ評価できる",
            "YOLO と PatchCore の出力の違いを、同じ画像で比較できる",
        ],
    ),
}

DAY_ORDER = ["Day01", "Day02", "Day03", "Day04", "Day05"]


def _cover(day_label: str, day_ja: str, day_en: str, styles: dict) -> list:
    return [
        Spacer(1, 42 * mm),
        Paragraph(COURSE_TITLE_JA, styles["cover_title"]),
        Paragraph(COURSE_TITLE_EN, styles["cover_meta"]),
        Spacer(1, 12 * mm),
        Paragraph(day_label, styles["cover_sub"]),
        Paragraph(_esc(day_ja), styles["cover_sub"]),
        Paragraph(_esc(day_en), styles["cover_meta"]),
        Spacer(1, 18 * mm),
        Paragraph("解説資料（日本語 → English）/ Explanation companion (Japanese first, then English)",
                  styles["body"]),
        Paragraph("これはノートブックの説明をそのまま組んだ冊子です。演習はノートブックで行ってください。"
                  " / This booklet is typeset from the notebooks themselves. Do the exercises in "
                  "Jupyter.", styles["note"]),
        Spacer(1, 6 * mm),
        Paragraph(f"作成日 / built: {BUILD_DATE}", styles["cover_meta"]),
        Paragraph(f"再生成 / rebuild: {REBUILD_COMMAND}", styles["cover_meta"]),
        NextPageTemplate("body"),
        PageBreak(),
    ]


def _about(styles: dict, day_keys: list[str]) -> list:
    flowables = [
        Paragraph("この資料について / About this companion", styles["h1"]),
        Paragraph(
            "この PDF は、研修のノートブック（Markdown セル）から自動で組んでいます。"
            "本文・図・キャプション・演習は、ノートブックと同じ内容です。"
            " / This PDF is typeset from the notebooks' Markdown cells. The prose, figures, captions "
            "and exercises are the same as in Jupyter.", styles["body"]),
        Paragraph("含めているもの / What is included", styles["h3"]),
    ]
    for text in [
        "学習目標・前提・説明（日本語のあとに同じ内容の英語）",
        "実行前から見える静的図と、そのキャプション・気づいてほしいこと・問い",
        "学習者が書き換える短いコード例",
        "演習・ヒント・理解度チェック",
        "各ノートブックのパスと、図の出典",
    ]:
        flowables.append(_bullet_flowable(text, styles))

    flowables.append(Paragraph("含めていないもの / What is not included", styles["h3"]))
    for text in [
        "実行ログ・スタックトレース・長い準備コード（ノートブックで確認してください）",
        "講師用の解答（`docs/instructor/` にあります）",
        "実行していない学習・検証の結果。保存された結果だけを「参考出力」として示します。",
        "対話ウィジェットそのもの。代わりに静的図と、ノートブックで操作する旨の注記を置いています。",
    ]:
        flowables.append(_bullet_flowable(text, styles))

    flowables.append(Paragraph("この PDF の読み方 / How to read it", styles["h3"]))
    flowables.append(_paragraph_flowable(
        "図には「模式図（schematic）」・「合成データ（synthetic）」・「参考出力（参考に保存された実際の結果）」の"
        "どれかを必ず書いています。実際に測った値と、説明のために描いた図を区別してください。"
        " / Every figure is labelled as schematic, synthetic, or a reference output from a real saved "
        "run. Keep measured numbers and explanatory drawings apart.", styles))
    flowables.append(Spacer(1, 4))

    flowables.append(Paragraph("この PDF に含まれる日 / Days in this file", styles["h3"]))
    for key in day_keys:
        info = DAYS[key]
        flowables.append(_bullet_flowable(f"{info['ja']} — {info['en']}", styles))
    flowables.append(Spacer(1, 3))
    flowables.append(Paragraph("目次 / Table of contents", styles["h2"]))
    return flowables


def _sources(styles: dict, day_keys: list[str]) -> list:
    flowables = [PageBreak(), Paragraph("出典と参照 / Sources and references", styles["h1"])]
    flowables.append(_paragraph_flowable(
        "本文と図の出典です。ノートブックを開いて、同じ内容を確認してください。"
        " / Sources for the text and figures. Open the notebooks to see the same material.", styles))
    for key in day_keys:
        flowables.append(Paragraph(f"{DAYS[key]['ja']} / {DAYS[key]['en']}", styles["h3"]))
        for stem in DAYS[key]["notebooks"]:
            matches = sorted(NOTEBOOK_DIR.rglob(f"{stem}.ipynb"))
            if matches:
                flowables.append(_bullet_flowable(
                    matches[0].relative_to(COURSE_ROOT).as_posix(), styles))
    flowables.append(Paragraph("図の出典 / Figure provenance", styles["h3"]))
    for text in [
        "`assets/diagrams/` — `assets/scripts/generate_teaching_diagrams.py` が生成する模式図・合成データの図。",
        "`assets/reference_outputs/` — `assets/scripts/generate_reference_outputs.py` が、この研修で"
        "実際に保存した結果（`submissions/`, `training_results/`）から作る参考図。",
        "`docs/pdf/` — この PDF。再生成は上記の 1 コマンドだけです。",
    ]:
        flowables.append(_bullet_flowable(text, styles))
    flowables.append(Spacer(1, 6))
    flowables.append(_note_flowable(
        "学習・検証の結果について、この資料は「うまくいった」とは書いていません。"
        "数字はすべて、保存された記録がある場合にだけ示しています。"
        " / This companion never claims that training or testing succeeded. Numbers appear only "
        "where a saved record exists.", styles))
    return flowables


def build_pdf(out_path: Path, day_keys: list[str], footer_label: str, styles: dict) -> Path:
    doc = ExplanationDoc(str(out_path), footer_label=footer_label, styles=styles)

    toc = TableOfContents()
    toc.levelStyles = [styles["toc0"], styles["toc1"], styles["toc2"]]
    toc.dotsMinLevel = 0

    story: list = []
    single = len(day_keys) == 1
    if single:
        info = DAYS[day_keys[0]]
        label = f"{day_keys[0][:3]} {int(day_keys[0][3:])}"
        story += _cover(label, info["ja"], info["en"], styles)
        story += _about(styles, day_keys)
    else:
        story += _cover("第 1 週（5 日間）/ Week 1 (five days)",
                        "第 1 週のまとめ", "the whole week in one document", styles)
        story += _about(styles, day_keys)

    story.append(toc)
    story.append(Spacer(1, 6))

    for key in day_keys:
        info = DAYS[key]
        if len(day_keys) > 1:
            story.append(PageBreak())
            story.append(_heading_flowable(1, info["ja"], info["en"], styles, toc_level=0))
        story.append(Paragraph("前提 / Prerequisites", styles["h3"]))
        story.append(_paragraph_flowable(info["prerequisites"], styles))
        story.append(Paragraph("この日の到達点 / Learning objectives", styles["h3"]))
        for index, objective in enumerate(info["objectives"], start=1):
            story.append(_bullet_flowable(f"{index}. {objective}", styles))

        for stem in info["notebooks"]:
            matches = sorted(NOTEBOOK_DIR.rglob(f"{stem}.ipynb"))
            if not matches:
                raise SystemExit(f"notebook not found: {stem}")
            story.extend(notebook_flowables(matches[0], styles,
                                            title_toc_level=0 if single else 1))

    story += _sources(styles, day_keys)

    doc.multiBuild(story)
    return out_path


# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------


def inspect_pdf(path: Path) -> dict:
    """ページ数と、日本語が埋め込まれているかを確かめる / page count and embedded Japanese text."""
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    text = []
    for page in reader.pages:
        text.append(page.extract_text() or "")
    joined = "\n".join(text)
    japanese = len(re.findall(r"[\u3040-\u30ff\u4e00-\u9fff]", joined))
    return {"pages": len(reader.pages), "japanese_chars": japanese,
            "chars": len(joined), "blank_pages": sum(1 for t in text if len(t.strip()) < 20)}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Export bilingual explanation PDFs.")
    parser.add_argument("--only", default=None, help="Day01 … Day05, or Week1")
    parser.add_argument("--check", action="store_true",
                        help="generate into a temporary folder and only report")
    parser.add_argument("--out", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args(argv)

    regular, bold = register_fonts()
    print(f"[font] regular={regular} bold={bold}")
    styles = build_styles()
    args.out.mkdir(parents=True, exist_ok=True)

    jobs = [(key, [key], f"{key} 解説 / explanation") for key in DAY_ORDER]
    jobs.append(("Week1", DAY_ORDER, "第 1 週 まとめ / Week 1 companion"))

    exit_code = 0
    for name, keys, label in jobs:
        if args.only and args.only not in name:
            continue
        out_path = args.out / f"{name}_explanation_ja_en.pdf"
        build_pdf(out_path, keys, label, styles)
        size_kb = out_path.stat().st_size / 1024
        print(f"[pdf] {out_path.name}  {size_kb:,.0f} KB")
        try:
            info = inspect_pdf(out_path)
        except Exception as error:  # pypdf は任意 / pypdf is optional
            print(f"      (inspection skipped: {error})")
            continue
        print(f"      pages={info['pages']}  japanese_chars={info['japanese_chars']}"
              f"  text_chars={info['chars']}")
        if info["pages"] < 3:
            print("      ERROR: too few pages")
            exit_code = 1
        if info["japanese_chars"] < 500:
            print("      ERROR: Japanese text did not survive the export")
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
