"""日本語・English・Nepali (Romanized, ne-Latn) の 3 言語解説 PDF を作る / build tri-language PDFs.

Why a second exporter exists
----------------------------
``export_explanations_pdf.py`` (ReportLab) stays exactly as it is and keeps producing the six
``*_ja_en.pdf`` files. ReportLab 5.1 can shape Devanagari through uharfbuzz, but the shaped glyph
clusters are written to the PDF as private-use code points, so copying or searching for a word such
as ``prashikshan`` from the finished PDF does not work. This exporter therefore renders the same
sources through Chromium (Playwright), which shapes Devanagari with HarfBuzz *and* writes a correct
``ToUnicode`` map: the text is both visually correct and selectable/searchable.

Nothing here retrains a model, regenerates a figure or rewrites a picture. The only inputs are the
learner-facing Markdown/docs and the pictures those files already reference.

作られるもの / What is produced (docs/pdf/)
------------------------------------------
    Day01_explanation_ja_en_ne.pdf … Day05_explanation_ja_en_ne.pdf
    Week1_explanation_ja_en_ne.pdf
    Setup_ja_en_ne.pdf                          (notebooks/00_Setup)
    Installation_Guide_ja_en_ne.pdf             (START_HERE.md + installation troubleshooting)
    Repository_Guide_ja_en_ne.pdf               (README.md)
    Course_Syllabus_ja_en_ne.pdf                (COURSE_SYLLABUS.md)

使い方 / Usage (Windows CMD, course environment activated)
---------------------------------------------------------
    python -m pip install -r requirements\\pdf.txt
    python assets\\scripts\\export_trilingual_pdf.py
    python assets\\scripts\\export_trilingual_pdf.py --only Day05
    python assets\\scripts\\export_trilingual_pdf.py --check          # build to a temp folder only
    python assets\\scripts\\inspect_pdf_pages.py --languages ja,en,ne

The first run needs the Chromium that Playwright manages (PDF-author step only, never learner setup):

    python -m playwright install chromium
"""

from __future__ import annotations

import argparse
import bisect
import datetime as _dt
import html
import json
import re
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image as PILImage

from course_notebooks import course_notebooks
from apply_nepali_translations import REGION_RE, CAPTION_RE, image_captions

COURSE_ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK_DIR = COURSE_ROOT / "notebooks"
OUTPUT_DIR = COURSE_ROOT / "docs" / "pdf"
TERMINOLOGY = COURSE_ROOT / "assets" / "i18n" / "ne" / "terminology.md"

BUILD_DATE = _dt.date.today().isoformat()
REBUILD_COMMAND = r"python assets\scripts\export_trilingual_pdf.py"

COURSE_TITLE_JA = "広島化成 第 1 週 AI・マシンビジョン研修"
COURSE_TITLE_EN = "Hiroshima Kasei Week 1 AI & Machine Vision Training"
COURSE_TITLE_NE = "Hiroshima Kasei — hapta 1: AI ra machine vision talim"

# 端末に入っている書体だけを使う（フォントは同梱しない / never ship a font binary）
JA_STACK = '"Yu Gothic", "YuGothic", "Meiryo", "Noto Sans JP", "MS Gothic", sans-serif'
# Romanized Nepali is Latin text; the Devanagari families stay in the stack only for the notebooks
# that have not been migrated yet (Days 1-3 during the pilot).
NE_STACK = ('"Segoe UI", "Nirmala UI", "Noto Sans Devanagari", "Mangal", '
            '"Arial Unicode MS", sans-serif')
MONO_STACK = 'Consolas, "Cascadia Mono", "Noto Sans Mono", monospace'

FIGURE_DPI = 140
PORTRAIT_MAX_NATURAL_WIDTH_MM = 236.0
MAX_CODE_CHARS = 88

WIDGET_MARKERS = ("ipywidgets", "widgets.interact", "IntSlider", "interactive(")
INSTRUCTOR_MARKERS = ("docs/instructor", "docs\\instructor")
DEVANAGARI_RE = re.compile(r"[\u0900-\u097f]")
JP_CHAR_RE = re.compile(r"[\u3040-\u30ff\u4e00-\u9fff\uff01-\uff60]")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")
# 目次に載せない見出し / headings kept out of the table of contents
NOT_IN_TOC = ("実行結果の例", "Expected output", "natijako udaharan", "कोड उदाहरण", "コード例",
              "code example", "Nepali ma")
LANG_ATTR = {"ja": "ja", "en": "en", "ne": "ne-Latn"}

# 本文の開始を示す見えにくい目印 / an invisible marker that survives into the PDF text layer.
# 目次にも本文にも同じ文字列が現れないので、目次ページを飛ばして本文の 1 ページ目を確実に求める。
BODY_SENTINEL = "BODYSTARTOFDOCUMENT"
SENTINEL_HTML = ('<div class="sentinel">' + BODY_SENTINEL + "</div>")


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------


def glyph_language(text: str) -> str:
    """文字種から日本語か英語かだけを決める / glyph-based choice for Japanese or English only.

    Nepali is **never** inferred this way: Romanized Nepali and English share the Latin alphabet, so
    the Nepali language tag comes from the ``ne:`` region the applier inserted (see
    ``nepali_lines``). Devanagari is still recognised so the notebooks that have not been migrated
    yet keep rendering correctly.
    """
    if DEVANAGARI_RE.search(text):
        return "ne"
    if JP_CHAR_RE.search(text):
        return "ja"
    return "en"


def nepali_lines(text: str) -> set[int]:
    """ネパール語領域の行番号 / line numbers covered by an explicit Nepali region."""
    covered: set[int] = set()
    for match in REGION_RE.finditer(text):
        if match.group("anchor").startswith("after-image:"):
            continue
        start = text[: match.start("body")].count("\n")
        end = text[: match.end("body")].count("\n")
        covered.update(range(start, end + 1))
    return covered


def language_at(text: str, index: int, covered: set[int], force: str | None = None) -> str:
    """行の言語 / the language of one source line, provenance first, glyphs second."""
    if force:
        return force
    if index in covered:
        return "ne"
    lines = text.splitlines()
    line = lines[index] if 0 <= index < len(lines) else ""
    return glyph_language(line)


def lang_attr(language: str) -> str:
    return LANG_ATTR.get(language, "en")


def script_class(text: str) -> str:
    """下位互換の別名 / kept for callers that only need a CSS class."""
    return glyph_language(text)


def display_len(text: str) -> int:
    return sum(2 if JP_CHAR_RE.match(char) or DEVANAGARI_RE.match(char) else 1 for char in text)


def _esc(text: str) -> str:
    return html.escape(text, quote=False)


def inline(text: str) -> str:
    """Markdown のインライン記法を HTML にする / inline Markdown to HTML."""
    spans: dict[str, str] = {}

    def keep_code(match: re.Match) -> str:
        key = f"\x00{len(spans)}\x00"
        spans[key] = f"<code>{_esc(match.group(1))}</code>"
        return key

    text = re.sub(r"`([^`]+)`", keep_code, text)
    text = _esc(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', text)
    for key, replacement in spans.items():
        text = text.replace(key, replacement)
    return text


def is_heading(line: str) -> tuple[int, str] | None:
    match = re.match(r"^(#{1,4})\s+(.*)$", line)
    if not match:
        return None
    return len(match.group(1)), match.group(2).strip()


def wrap_code_line(line: str, limit: int = MAX_CODE_CHARS) -> list[str]:
    pieces = []
    while len(line) > limit:
        cut = line.rfind(" ", 0, limit)
        if cut <= limit // 3:
            cut = limit
        pieces.append(line[:cut].rstrip())
        line = "    ↳ " + line[cut:].lstrip()
    pieces.append(line)
    return pieces


def image_path(path: Path) -> Path:
    """SVG は既存の PNG 代替を使う（作り直さない）/ reuse the pre-existing PNG fallback."""
    if path.suffix.lower() == ".svg":
        fallback = path.parent.parent / "diagrams" / f"{path.stem}_svg.png"
        if not fallback.is_file():
            raise FileNotFoundError(f"SVG PDF fallback missing: {fallback}")
        return fallback
    return path


def image_is_wide(path: Path) -> bool:
    path = image_path(path)
    with PILImage.open(path) as handle:
        width = handle.size[0]
    return width / FIGURE_DPI * 25.4 > PORTRAIT_MAX_NATURAL_WIDTH_MM


def file_uri(path: Path) -> str:
    return path.resolve().as_uri()


# ---------------------------------------------------------------------------
# document model
# ---------------------------------------------------------------------------


@dataclass
class Heading:
    level: int
    ja: str
    en: str | None = None
    ne: str | None = None
    anchor: str = ""

    @property
    def plain(self) -> str:
        parts = [part for part in (self.ja, self.en, self.ne) if part]
        return " / ".join(parts)

    @property
    def in_toc(self) -> bool:
        if self.level > 3:
            return False
        return not any(marker in self.plain for marker in NOT_IN_TOC)


@dataclass
class Document:
    """1 冊ぶんの HTML と目次 / one PDF's HTML body and table of contents."""

    title_ja: str
    title_en: str
    title_ne: str
    subtitle_html: str = ""
    body: list[str] = field(default_factory=list)
    toc: list[Heading] = field(default_factory=list)

    def add(self, markup: str) -> None:
        self.body.append(markup)


# ---------------------------------------------------------------------------
# markdown cell -> HTML
# ---------------------------------------------------------------------------


def _heading_html(heading: Heading) -> str:
    level = heading.level
    parts = [f'<span class="ja" lang="ja">{inline(heading.ja)}</span>'] if heading.ja else []
    if heading.en:
        parts.append(f'<span class="en" lang="en">{inline(heading.en)}</span>')
    if heading.ne:
        parts.append(f'<span class="ne" lang="ne-Latn">{inline(heading.ne)}</span>')
    inner = "<br/>".join(parts)
    ident = f' id="{heading.anchor}"' if heading.anchor else ""
    return f"<h{level}{ident}>{inner}</h{level}>"


def _code_block(code: str) -> str:
    lines: list[str] = []
    for line in code.splitlines():
        lines.extend(wrap_code_line(line.rstrip()))
    body = "\n".join(_esc(line) for line in lines)
    return f'<pre class="code"><code>{body}</code></pre>'


def _table_html(rows: list[list[str]], header: bool, force: str | None = None) -> str:
    columns = max(len(row) for row in rows)
    weights = []
    for column in range(columns):
        longest = max((display_len(row[column]) for row in rows if column < len(row)), default=1)
        weights.append(min(max(longest, 8), 64))
    total = sum(weights)
    shares = "".join(f'<col style="width:{100 * weight / total:.2f}%"/>' for weight in weights)
    out = [f'<table><colgroup>{shares}</colgroup>']
    for index, row in enumerate(rows):
        cells = row + [""] * (columns - len(row))
        tag = "th" if (index == 0 and header) else "td"
        rendered_cells = []
        for cell in cells:
            language = force or glyph_language(cell)
            rendered_cells.append(
                f'<{tag} class="{language}" lang="{lang_attr(language)}">{inline(cell)}</{tag}>')
        out.append(f"<tr>{''.join(rendered_cells)}</tr>")
    out.append("</table>")
    return "".join(out)


def _figure_html(path: Path, captions: list[str], wide: bool, notes_html: str = "",
                 caption_languages: list[str] | None = None) -> str:
    classes = "figure wide" if wide else "figure"
    rendered_captions = []
    for position, text in enumerate(captions):
        if caption_languages and position < len(caption_languages):
            language = caption_languages[position]
        else:
            language = glyph_language(text)
        rendered_captions.append(
            f'<div class="cap {language}" lang="{lang_attr(language)}">{inline(text)}</div>')
    caption = "".join(rendered_captions)
    return (f'<div class="{classes}" data-image="{html.escape(path.name, quote=True)}">'
            f'<img src="{file_uri(image_path(path))}" alt=""/>'
            f'{caption}<div class="visual-notes">{notes_html}</div></div>')


def semantic_headings(lines: list[str], covered: set[int] | None = None,
                      text: str | None = None) -> tuple[dict[int, Heading], set[int]]:
    """Only explicit localization anchors may join non-adjacent semantic headings."""
    covered = covered or set()
    text = text if text is not None else "\n".join(lines)
    headings = {}
    fenced = False
    for index, line in enumerate(lines):
        if line.strip().startswith("```"):
            fenced = not fenced
        item = is_heading(line.strip())
        if item and not fenced:
            level, title = item
            language = language_at(text, index, covered)
            headings[index] = Heading(level, title if language == "ja" else "",
                                      title if language == "en" else None,
                                      title if language == "ne" else None)
    suppressed = set()
    text = "\n".join(lines) + "\n"
    for match in REGION_RE.finditer(text):
        if match.group("anchor") != "after-heading":
            continue
        start = text[:match.start("body")].count("\n")
        end = text[:match.end("body")].count("\n")
        preceding = [i for i in headings if i < start]
        if not preceding:
            raise ValueError("after-heading translation has no source heading")
        body = match.group("body")
        pair = re.search(r"^<!-- ne-pair: (.+) -->$", body, re.M)
        source_index = max(preceding)
        if pair and headings[source_index].en == pair.group(1):
            sources = [i for i in preceding if headings[i].ja
                       and headings[i].level == headings[source_index].level]
            if not sources:
                raise ValueError(f"paired English heading has no Japanese source: {pair.group(1)!r}")
            source_index = max(sources)
        source = headings[source_index]
        translated = [(i, headings[i].ne) for i in headings
                      if start <= i <= end and headings[i].ne]
        bold = re.search(r"^\*\*(.+)\*\*$", body, re.M)
        if translated:
            source.ne = translated[0][1]
            suppressed.add(translated[0][0])
        elif bold and (start + body[:bold.start()].count("\n") in covered
                       or DEVANAGARI_RE.search(bold.group(1))):
            source.ne = bold.group(1)
            suppressed.add(start + body[:bold.start()].count("\n"))
        else:
            raise ValueError("after-heading region needs a Nepali title")
        if pair:
            targets = [i for i, h in headings.items()
                       if h.en == pair.group(1) and h.level == source.level]
            if len(targets) != 1 or targets[0] <= source_index:
                raise ValueError(f"ambiguous or missing English heading: {pair.group(1)!r}")
            source.en = headings[targets[0]].en
            suppressed.add(targets[0])
    return headings, suppressed


def markdown_cell_html(text: str, notebook_dir: Path, anchor_prefix: str,
                       document: Document, force_language: str | None = None) -> str:
    """1 つの Markdown セルを HTML にする / one Markdown cell to HTML.

    ``force_language`` is used for the body of a Nepali figure note, which is parsed on its own
    (without its ``ne:`` markers) after the figure markup has been produced.
    """
    visual_regions = {}
    for match in REGION_RE.finditer(text):
        anchor = match.group("anchor")
        if anchor.startswith("after-image:"):
            target = anchor.partition(":")[2]
            if target in visual_regions:
                raise ValueError(f"duplicate image translation target: {target!r}")
            visual_regions[target] = match.group("body")
    for target in visual_regions:
        count = sum(match.group(2) == target for match in IMAGE_RE.finditer(text))
        if count != 1:
            raise ValueError(f"image translation target {target!r}: expected one image, found {count}")
    text = REGION_RE.sub(
        lambda match: "\n" if match.group("anchor").startswith("after-image:") else match.group(),
        text)
    lines = text.splitlines()
    covered = set() if force_language else nepali_lines(text)
    grouped, suppressed = semantic_headings(lines, covered, text)
    out: list[str] = []
    index = 0

    stripped = [line for line in lines if line.strip() and not line.strip().startswith("---")]
    if stripped and all(is_heading(line) for line in stripped):
        joined = " ".join(stripped)
        if ("実行結果の例" in joined or "Expected output" in joined
                or "natijako udaharan" in joined or "नतिजाको उदाहरण" in joined):
            out.append(
                '<div class="note"><span class="ja" lang="ja">この節の出力はノートブックで実行すると'
                '表示されます。</span><br/><span class="en" lang="en">Run the notebook to see this '
                'output.</span><br/><span class="ne" lang="ne-Latn">Yo bhaagko natija notebook '
                'chalaunda dekHinchha.</span></div>')
            return "".join(out)

    while index < len(lines):
        if index in suppressed:
            index += 1
            continue
        raw = lines[index]
        line = raw.strip()

        if not line:
            index += 1
            continue

        if line.startswith("<!--"):
            # ne: マーカーは組版しない / never typeset the Nepali region markers
            index += 1
            continue

        if line in ("---", "***", "___"):
            out.append('<hr/>')
            index += 1
            continue

        if any(marker in line for marker in INSTRUCTOR_MARKERS):
            index += 1
            continue

        if index in grouped:
            item = grouped[index]
            item.anchor = f"{anchor_prefix}-h{len(document.toc)}"
            document.toc.append(item)
            out.append(_heading_html(item))
            index += 1
            continue

        image_match = IMAGE_RE.search(line)
        if image_match:
            target = image_match.group(2)
            resolved = (notebook_dir / target).resolve()
            if not target.startswith(("http://", "https://", "data:")) and resolved.is_file():
                captions, probe = image_captions(lines, index + 1)
                caption_languages = [glyph_language(text) for text in captions]
                body = visual_regions.pop(target, "")
                notes = [part for part in body.split("\n\n") if part.strip()]
                caption_index = 0
                if notes and re.fullmatch(r"\*\*[AB]: .+\*\*", notes[0]):
                    caption_index = 1
                if len(notes) > caption_index and CAPTION_RE.match(notes[caption_index]):
                    captions.append(" ".join(notes.pop(caption_index).splitlines()))
                    caption_languages.append("ne")
                notes_html = markdown_cell_html("\n\n".join(notes), notebook_dir,
                                                anchor_prefix + "-visual", document,
                                                force_language="ne")
                out.append(_figure_html(resolved, captions, image_is_wide(resolved), notes_html,
                                        caption_languages))
                index = probe if captions else index + 1
                continue
            index += 1
            continue

        if line.startswith("```"):
            body = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                body.append(lines[index])
                index += 1
            index += 1
            out.append(_code_block("\n".join(body)))
            continue

        if line.startswith(">"):
            quote_start = index
            body = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                body.append(lines[index].strip()[1:].strip())
                index += 1
            joined = " ".join(part for part in body if part)
            language = force_language or ("ne" if quote_start in covered else glyph_language(joined))
            out.append(f'<div class="note {language}" lang="{lang_attr(language)}">'
                       f"{inline(joined)}</div>")
            continue

        if line.startswith("|"):
            table_start = index
            rows: list[list[str]] = []
            has_separator = False
            while index < len(lines) and lines[index].strip().startswith("|"):
                cells = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
                if all(re.fullmatch(r":?-{2,}:?", cell) for cell in cells):
                    has_separator = True
                else:
                    rows.append(cells)
                index += 1
            if rows:
                out.append(_table_html(rows, has_separator and len(rows) > 1,
                                       language_at(text, table_start, covered, force_language)))
            continue

        bullet = re.match(r"^(\s*)([-*・]|\d+[.)])\s+(.*)$", raw)
        if bullet:
            bullet_start = index
            ordered = bool(re.match(r"^\d+[.)]$", bullet.group(2)))
            base_indent = len(bullet.group(1))
            items: list[str] = []
            while index < len(lines):
                match = re.match(r"^(\s*)([-*・]|\d+[.)])\s+(.*)$", lines[index])
                if not match:
                    # 箇条書きの継続行 / a wrapped continuation line
                    if items and lines[index].strip() and lines[index].startswith("      "):
                        items[-1] = items[-1] + " " + lines[index].strip()
                        index += 1
                        continue
                    break
                text_ = match.group(3).strip()
                indent = len(match.group(1))
                if indent > base_indent and items:
                    # 元の Markdown は対訳を字下げで並べる / keep a translation next to its line
                    items[-1] = items[-1] + " || " + text_
                else:
                    items.append(text_)
                index += 1
            tag = "ol" if ordered else "ul"
            bullet_forced = force_language or ("ne" if bullet_start in covered else None)
            body = ""
            for item in items:
                parts = [part.strip() for part in item.split(" || ")]
                rendered = []
                for part in parts:
                    checkbox = ""
                    if part.startswith("[ ]"):
                        checkbox, part = "☐ ", part[3:].strip()
                    elif part.startswith("[x]"):
                        checkbox, part = "☑ ", part[3:].strip()
                    language = bullet_forced or glyph_language(part)
                    rendered.append(f'<span class="{language}" lang="{lang_attr(language)}">'
                                    f"{checkbox}{inline(part)}</span>")
                body += f"<li>{'<br/>'.join(rendered)}</li>"
            out.append(f"<{tag}>{body}</{tag}>")
            continue

        paragraph = []
        paragraph_start = index
        while index < len(lines):
            candidate = lines[index]
            candidate_stripped = candidate.strip()
            if not candidate_stripped:
                break
            if (candidate_stripped.startswith(("```", ">", "|", "<!--"))
                    or is_heading(candidate_stripped)
                    or IMAGE_RE.search(candidate_stripped)
                    or re.match(r"^(\s*)([-*・]|\d+[.)])\s+", candidate)
                    or candidate_stripped in ("---", "***", "___")):
                break
            paragraph.append(candidate_stripped)
            index += 1
        if paragraph:
            joined = " ".join(paragraph)
            language = force_language or ("ne" if paragraph_start in covered
                                          else glyph_language(joined))
            out.append(f'<p class="{language}" lang="{lang_attr(language)}">{inline(joined)}</p>')
        else:
            index += 1

    if visual_regions:
        raise ValueError(f"unmatched image translation(s): {list(visual_regions)}")
    return "".join(out)


# ---------------------------------------------------------------------------
# notebooks
# ---------------------------------------------------------------------------


def notebook_title(nb: dict) -> tuple[str, str, str]:
    first = "".join(nb["cells"][0]["source"])
    covered = nepali_lines(first)
    ja = en = ne = ""
    for index, line in enumerate(first.splitlines()):
        match = re.match(r"^#\s+(.*)$", line.strip())
        if not match:
            continue
        text = match.group(1).strip()
        if index in covered or DEVANAGARI_RE.search(text):
            language = "ne"
        elif JP_CHAR_RE.search(text):
            language = "ja"
        else:
            language = "en"
        if language == "ne" and not ne:
            ne = text
        elif language == "ja" and not ja:
            ja = text
        elif language == "en" and not en:
            en = text
    return ja or en, en, ne


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


def notebook_html(path: Path, document: Document, toc_level: int = 1) -> None:
    nb = json.loads(path.read_text(encoding="utf-8"))
    ja, en, ne = notebook_title(nb)
    title = Heading(level=toc_level, ja=ja, en=en or None, ne=ne or None,
                    anchor=f"nb-{path.stem}-title")
    document.toc.append(title)
    document.add(_heading_html(title))
    rel = path.relative_to(COURSE_ROOT).as_posix()
    document.add(f'<p class="path en">notebook: <code>{rel}</code></p>')

    for position, cell in enumerate(nb["cells"]):
        source = "".join(cell["source"])
        if cell["cell_type"] == "markdown":
            if position == 0:
                lines = source.splitlines()
                while lines:
                    stripped = lines[0].strip()
                    heading = is_heading(stripped)
                    if (not stripped or stripped in ("---", "***", "___")
                            or stripped.startswith("<!--")):
                        lines.pop(0)
                        continue
                    if heading and heading[0] == 1:
                        lines.pop(0)
                        continue
                    break
                source = "\n".join(lines)
            document.add(markdown_cell_html(source, path.parent, f"{path.stem}-{position}",
                                            document))
            continue

        code = clean_code(source)
        if not code:
            continue
        if any(marker in code for marker in WIDGET_MARKERS):
            document.add(
                '<div class="note warn"><span class="ja">この節はノートブック上での対話操作です。'
                'PDF では前の静的図で代わりに示しています。</span><br/>'
                '<span class="en">This section is interactive in the notebook only; the static '
                'figure above stands in for it here.</span><br/>'
                '<span class="ne" lang="ne-Latn">Yo bhaag notebook ma matra interactive chha. Yahan mathiko sthir '
                'chitrale tyasko pratinidhitwa garchha.</span></div>')
            continue
        if not code_is_worth_showing(cell, code):
            continue
        document.add('<p class="code-label en">コード例 / code example / code udaharan</p>')
        document.add(_code_block(code))


# ---------------------------------------------------------------------------
# day metadata
# ---------------------------------------------------------------------------

DAYS = {
    "Day01": dict(
        ja="第 1 日　AI とデジタル画像の基礎",
        en="Day 1 — AI and the basics of digital images",
        ne="Din 1 — AI ra digital tasbirko adhar",
        notebooks=["Day01_01_Introduction_to_AI", "Day01_02_Pixels_and_Images",
                   "Day01_03_Computer_Vision_Tasks"],
        prerequisites_ja="Python の知識は不要です。`00_Environment_Setup.ipynb` を済ませてください。",
        prerequisites_en="No prior programming. Finish the environment setup first.",
        prerequisites_ne="Python ko pahileko gyan aawashyak chhaina. Pahile "
                         "`00_Environment_Setup.ipynb` saknuhos.",
        objectives=[
            ("プログラム・自動化・AI の違いを、現場の言葉で説明できる",
             "Explain how a program, automation and AI differ, in shop-floor words",
             "Karyakram, swachalan ra AI bichko farak karyasthalako bhasama bataun sakne."),
            ("画素・解像度・RGB が、検査の見え方をどう決めるかを説明できる",
             "Explain how pixels, resolution and RGB decide what an inspection can see",
             "Pixel, resolution ra RGB le nirikshan ma ke dekhinchha bhanne kura kasari tay "
             "garchha bataun sakne."),
            ("分類・検出・セグメンテーション・異常検知の出力の違いを選べる",
             "Choose between the outputs of classification, detection, segmentation and "
             "anomaly detection",
             "Bargikaran, pahichan, segmentation ra asamanyata pahichanka natija chhutyaun sakne."),
        ],
    ),
    "Day02": dict(
        ja="第 2 日　Python と OpenCV の基礎",
        en="Day 2 — Python and OpenCV fundamentals",
        ne="Din 2 — Python ra OpenCV ko adhar",
        notebooks=["Day02_01_Python_Basics", "Day02_02_Conditions_Loops_Functions",
                   "Day02_03_OpenCV_Image_Processing"],
        prerequisites_ja="第 1 日の内容（画素と RGB）。プログラミング経験は不要です。",
        prerequisites_en="Day 1 (pixels and RGB). No programming experience required.",
        prerequisites_ne="Din 1 ko bishay (pixel ra RGB). Programming ko anubhav aawashyak chhaina.",
        objectives=[
            ("変数・条件・繰り返し・関数を、測定値の判定に使える",
             "Use variables, conditions, loops and functions to judge measurements",
             "Variable, sart, dohorine kaam ra function prayog garera napiyeko maanko nirnaya "
             "garna sakne."),
            ("グレースケール・2 値化・輪郭という処理の流れを説明できる",
             "Explain the pipeline grayscale, binarise, find contours",
             "Grayscale, binarikaran ra contour khojne kram bataun sakne."),
            ("画素を mm に変換し、校正の限界を説明できる",
             "Convert pixels to millimetres and explain the limits of calibration",
             "Pixel lai mm ma badalna ra calibration ko sima bataun sakne."),
        ],
    ),
    "Day03": dict(
        ja="第 3 日　YOLO による物体検出の基礎",
        en="Day 3 — Object detection with YOLO",
        ne="Din 3 — YOLO le wastu pahichanko adhar",
        notebooks=["Day03_01_YOLO_Concepts", "Day03_02_YOLO_Inference",
                   "Day03_03_YOLO_Experiments"],
        prerequisites_ja="第 2 日（Python と OpenCV）。GPU は不要です。",
        prerequisites_en="Day 2. No GPU required.",
        prerequisites_ne="Din 2 (Python ra OpenCV). GPU aawashyak chhaina.",
        objectives=[
            ("バウンディングボックスを 4 つ／5 つの数で読み書きできる",
             "Read and write a bounding box as four or five numbers",
             "Bounding box char wa paanch sankhyama padhna ra lekhna sakne."),
            ("IoU を計算し、検出の良し悪しを数で説明できる",
             "Compute IoU and describe detection quality with numbers",
             "IoU ganana garera pahichan ramro wa naramro bhaeko kura sankhyale bataun sakne."),
            ("confidence と解像度が検出結果をどう変えるかを説明できる",
             "Explain how confidence and resolution change the detections",
             "Confidence ra resolution le pahichanko natija kasari badalchha bataun sakne."),
        ],
    ),
    "Day04": dict(
        ja="第 4 日　YOLO の学習と評価",
        en="Day 4 — Training and evaluating YOLO",
        ne="Din 4 — YOLO ko prashikshan ra mulyankan",
        notebooks=["Day04_01_YOLO_Dataset_Annotation", "Day04_02_YOLO_Training",
                   "Day04_03_YOLO_Evaluation"],
        prerequisites_ja="第 3 日（検出の読み方）。学習には CPU で数分かかります。",
        prerequisites_en="Day 3. Training takes a few minutes on CPU.",
        prerequisites_ne="Din 3 (pahichan kasari padhne). CPU ma prashikshan garna kehi minet lagchha.",
        objectives=[
            ("YOLO 形式のラベルを読み、データセットの分割を説明できる",
             "Read YOLO labels and explain how the dataset is split",
             "YOLO dhanchako label padhna ra dataset kasari bandinchha bataun sakne."),
            ("epoch・batch・学習曲線を読み、学習の良し悪しを判断できる",
             "Read epochs, batches and the learning curve to judge a run",
             "Epoch, batch ra sikai bakra padhera prashikshan ramro bhayo ki bhaena bataun sakne."),
            ("物体単位と画像単位の指標を混同せずに報告できる",
             "Report object-level and image-level metrics without mixing them up",
             "Wastu-star ra tasbir-starka maapan namisai report garna sakne."),
        ],
    ),
    "Day05": dict(
        ja="第 5 日　PatchCore による異常検知と手法比較",
        en="Day 5 — Anomaly detection with PatchCore and method comparison",
        ne="Din 5 — PatchCore le asamanyata pahichan ra bidhi tulna",
        notebooks=["Day05_01_Anomaly_Detection_Concepts", "Day05_02_PatchCore_Training",
                   "Day05_03_YOLO_vs_PatchCore"],
        prerequisites_ja="第 4 日（学習と評価）。PatchCore の学習は CPU で 1〜2 分です。",
        prerequisites_en="Day 4. PatchCore fit takes 1-2 minutes on CPU.",
        prerequisites_ne="Din 4 (prashikshan ra mulyankan). PatchCore ko prashikshan CPU ma 1-2 "
                         "minet lagchha.",
        objectives=[
            ("パッチ・特徴・記憶（memory bank）・最近傍の流れを説明できる",
             "Explain patches, features, the memory bank and the nearest neighbour",
             "Patch, feature, memory bank ra najikako chhimekiko kram bataun sakne."),
            ("較正用データでしきい値を決め、試験用データで 1 回だけ評価できる",
             "Pick the threshold on calibration data and evaluate once on test data",
             "Calibration databaat threshold tay garera parikshan datama ek patak matra "
             "mulyankan garna sakne."),
            ("YOLO と PatchCore の出力の違いを、同じ画像で比較できる",
             "Compare YOLO and PatchCore outputs on the same picture",
             "Eutai tasbir ma YOLO ra PatchCore ko natija tulna garna sakne."),
        ],
    ),
}

DAY_ORDER = ["Day01", "Day02", "Day03", "Day04", "Day05"]


# ---------------------------------------------------------------------------
# HTML shell
# ---------------------------------------------------------------------------

CSS = """
@page { size: A4; margin: 20mm 18mm 18mm 18mm; }
@page landscape { size: A4 landscape; margin: 16mm 14mm 14mm 14mm; }
html { -webkit-print-color-adjust: exact; }
body { font-family: %(NE)s; font-size: 9.6pt; line-height: 1.62; color: #24292f; margin: 0; }
.ja { font-family: %(JA)s; }
.en { }
/* Chromium's PDF backend inserts real space glyphs between Devanagari clusters whenever above-base
   mark positioning shifts a mark (the written advance no longer matches the font metrics), which
   makes the searchable text layer read "ता लि ममा" for "तालिममा". Turning abvm off keeps the
   rendered glyphs identical (measured: mean pixel difference 0.05/255 on a 20 pt sample) and lets
   the text layer carry the original code points, so the PDF stays searchable. */
/* Romanized Nepali is Latin: inherit the body stack, keep the colour cue. The Devanagari
   families remain in the stack only for the notebooks that are not migrated yet. */
.ne { font-family: inherit; font-feature-settings: "abvm" 0; color: #2f2f2f; }
h1, h2, h3, h4 { break-after: avoid; page-break-after: avoid; margin: 0.55em 0 0.25em; }
h1 { font-size: 16.5pt; line-height: 1.35; color: #1f6feb; }
h2 { font-size: 13pt; line-height: 1.35; }
h3 { font-size: 11pt; line-height: 1.35; color: #1a3d6d; }
h4 { font-size: 10pt; line-height: 1.35; }
h1 .en, h2 .en, h3 .en, h4 .en { font-size: 0.72em; color: #57606a; font-weight: 600; }
h1 .ne, h2 .ne, h3 .ne, h4 .ne { font-size: 0.84em; color: #3b3b3b; font-weight: 600; }
p { margin: 0 0 0.45em; }
ul, ol { margin: 0.2em 0 0.55em 1.2em; padding: 0; }
li { margin: 0 0 0.15em; }
hr { border: 0; border-top: 0.6pt solid #d0d7de; margin: 0.6em 0; }
a { color: #1f6feb; text-decoration: none; }
code { font-family: %(MONO)s; font-size: 0.88em; background: #f6f8fa; padding: 0 0.15em;
       border-radius: 2px; }
pre.code { font-family: %(MONO)s; font-size: 7.6pt; line-height: 1.32; background: #f6f8fa;
           border: 0.4pt solid #d0d7de; border-radius: 3px; padding: 5pt 6pt; margin: 0.3em 0 0.7em;
           white-space: pre-wrap; word-break: break-word; break-inside: avoid; }
pre.code code { background: none; padding: 0; font-size: 1em; }
.code-label { color: #57606a; font-size: 7.8pt; margin: 0.35em 0 0.1em; }
.path { color: #57606a; font-size: 8.2pt; margin: -0.2em 0 0.6em; }
table { border-collapse: collapse; width: 100%%; margin: 0.25em 0 0.7em; font-size: 8.5pt;
        table-layout: fixed; }
th, td { border: 0.4pt solid #d0d7de; padding: 2.5pt 3.5pt; vertical-align: top;
         word-wrap: break-word; overflow-wrap: anywhere; }
th { background: #eef4ff; font-weight: 700; }
thead { display: table-header-group; }
tr { break-inside: avoid; }
.note { background: #f2f6ff; border: 0.4pt solid #d0d7de; border-radius: 3px;
        padding: 4pt 6pt; margin: 0.3em 0 0.7em; font-size: 8.8pt; color: #333; }
.note.warn { background: #fffaf0; color: #9a6700; }
.figure { margin: 0.4em 0 0.8em; break-inside: avoid; text-align: left; }
.figure img { max-width: 100%%; max-height: 106mm; width: auto; height: auto; }
.figure .cap { font-size: 8.4pt; color: #57606a; margin-top: 2pt; }
.figure.wide { page: landscape; break-before: page; break-after: page; }
.figure.wide img { max-width: 100%%; max-height: 150mm; }
.figure.wide:has(.visual-notes:not(:empty)) {
  display: flex; flex-direction: column; height: 175mm; }
.figure.wide:has(.visual-notes:not(:empty)) img {
  flex: 0 1 auto; min-height: 0; width: 100%%;
  object-fit: contain; object-position: left top; }
.figure.wide .cap, .figure.wide .visual-notes { flex-shrink: 0; }
.visual-notes { margin-top: 5pt; }
.visual-notes .ne, .figure .cap.ne { font-size: 9pt; }
.cover { break-after: page; padding-top: 34mm; }
.cover .t { font-size: 25pt; color: #1f6feb; line-height: 1.3; }
.cover .m { font-size: 10pt; color: #57606a; margin-top: 3pt; }
.cover .d { font-size: 17pt; margin-top: 14mm; }
.cover .dn { font-family: %(NE)s; font-size: 15pt; margin-top: 4pt; }
.cover .body { font-size: 9.4pt; margin-top: 12mm; }
.toc { break-after: page; }
.toc.hidden { visibility: hidden; }
.toc ol { list-style: none; margin: 0; padding: 0; }
.toc li { margin: 0.12em 0; }
.toc li.l1 { font-weight: 700; margin-top: 0.35em; }
.toc li.l2 { margin-left: 1.1em; }
.toc li.l3 { margin-left: 2.2em; font-size: 0.93em; color: #57606a; }
.toc .en { font-size: 0.86em; color: #57606a; }
.toc .ne { font-size: 9pt; color: #3b3b3b; }
.toc .pg { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
.toc a { color: #24292f; display: grid; grid-template-columns: minmax(0, 1fr) 3em;
         column-gap: 0.6em; }
.section { break-before: page; }
.sentinel { font-size: 1pt; line-height: 1pt; color: transparent; height: 1pt; margin: 0; }
/* Chromium keeps the Devanagari text layer clean only when the type size is a multiple of 1.5 pt
   (measured at 6, 7.5, 9, 10.5, 12, 13.5, 15, 16.5 and 18 pt). Every Nepali container is pinned
   here so a later style change cannot silently break searchability again. */
.ne { font-size: 10.5pt; }
h1 .ne { font-size: 13.5pt; }
h2 .ne { font-size: 12pt; }
h3 .ne { font-size: 10.5pt; }
h4 .ne { font-size: 9pt; }
th .ne, td .ne { font-size: 9pt; }
.note .ne { font-size: 9pt; }
.figure .cap .ne { font-size: 9pt; }
.toc .ne { font-size: 9pt; }
.path .ne { font-size: 7.5pt; }
.cover .body .ne, .cover .m .ne { font-size: 9pt; }
""" % {"JA": JA_STACK, "NE": NE_STACK, "MONO": MONO_STACK}


def html_document(document: Document) -> str:
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            f"<title>{html.escape(document.title_en)}</title><style>{CSS}</style></head>"
            f"<body>{''.join(document.body)}</body></html>")


def cover_html(document: Document, day_label: str, day_ja: str, day_en: str, day_ne: str) -> str:
    return (
        '<section class="cover">'
        f'<div class="t ja">{inline(COURSE_TITLE_JA)}</div>'
        f'<div class="m en">{inline(COURSE_TITLE_EN)}</div>'
        f'<div class="m ne">{inline(COURSE_TITLE_NE)}</div>'
        f'<div class="d ja">{inline(day_label)}</div>'
        f'<div class="d ja">{inline(day_ja)}</div>'
        f'<div class="m en">{inline(day_en)}</div>'
        f'<div class="dn ne">{inline(day_ne)}</div>'
        '<div class="body">'
        '<p class="ja">解説資料（日本語 → English → Nepali (Roman)）</p>'
        '<p class="en">Explanation companion: Japanese first, then English, then Nepali.</p>'
        '<p class="ne" lang="ne-Latn">Byakhya samagri: pahile Japani, tyaspachhi Angreji, tyaspachhi Nepali (Roman).</p>'
        '<p class="ja">これはノートブックの説明をそのまま組んだ冊子です。演習はノートブックで'
        '行ってください。</p>'
        '<p class="en">This booklet is typeset from the notebooks themselves. Do the exercises in '
        'Jupyter.</p>'
        '<p class="ne" lang="ne-Latn">Yo pustika notebookkai byakhyabaat tayar bhaeko ho. Abhyas Jupyter mai '
        'garnuhos.</p>'
        f'<p class="m">作成日 / built: {BUILD_DATE}</p>'
        f'<p class="m">再生成 / rebuild: {inline(REBUILD_COMMAND)}</p>'
        '</div></section>')


ABOUT_JA = "この資料について"
ABOUT_EN = "About this companion"
ABOUT_NE = "Yo samagriko barema"

ABOUT_HTML = """
<section class="section">
<h1><span class="ja">{ja}</span><br/><span class="en">{en}</span><br/><span class="ne" lang="ne-Latn">{ne}</span></h1>
<p class="ja">この PDF は、研修のノートブック（Markdown セル）から自動で組んでいます。本文・図・
キャプション・演習は、ノートブックと同じ内容です。日本語のあとに同じ内容の英語、そのあとに同じ
内容のネパール語を置いています。</p>
<p class="en">This PDF is typeset from the notebooks' Markdown cells. The prose, figures, captions
and exercises are the same as in Jupyter. Each idea appears first in Japanese, then in English, then
in Nepali (Romanized).</p>
<p class="ne" lang="ne-Latn">Yo PDF notebookka Markdown cellbaat swatah tayar bhaeko ho. Lekhai,
chitra, caption ra abhyas notebookkai jastai chhan. Harek bichar pahile Japanima, tyaspachhi
Angrejima ra antama Nepali (Roman) ma dieko chha.</p>

<h3><span class="ja">含めているもの</span><br/><span class="en">What is included</span><br/>
<span class="ne" lang="ne-Latn">Ke-ke samabesh chha</span></h3>
<ul>
<li class="ja">学習目標・前提・説明（日本語のあとに同じ内容の英語とネパール語）</li>
<li class="en">Learning objectives, prerequisites and explanations in all three languages</li>
<li class="ne" lang="ne-Latn">Sikai lakshya, poorwashart ra byakhya tinai bhasama</li>
<li class="ja">実行前から見える静的図と、そのキャプション・気づいてほしいこと・問い</li>
<li class="en">The static figures with their captions, "what to notice" notes and questions</li>
<li class="ne" lang="ne-Latn">Chalaunuaghi nai dekhine sthir chitra, tinka caption, dhyan dinuparne
kura ra prashna</li>
<li class="ja">学習者が書き換える短いコード例・演習・ヒント・理解度チェック</li>
<li class="en">The short code examples the learner edits, exercises, hints and questions</li>
<li class="ne" lang="ne-Latn">Vidyarthile badalne chhota code udaharan, abhyas, sanket ra bujhai
jaanchne prashna</li>
<li class="ja">各ノートブックのパスと、図の出典</li>
<li class="en">Each notebook's path and the figure provenance</li>
<li class="ne" lang="ne-Latn">Harek notebookko bato ra chitrako srot</li>
</ul>

<h3><span class="ja">含めていないもの</span><br/><span class="en">What is not included</span><br/>
<span class="ne" lang="ne-Latn">Ke-ke samabesh chhaina</span></h3>
<ul>
<li class="ja">実行ログ・スタックトレース・長い準備コード（ノートブックで確認してください）</li>
<li class="en">Run logs, stack traces and long preparation code (see the notebook)</li>
<li class="ne" lang="ne-Latn">Chalaeko log, stack trace ra lamo tayari code (notebook ma hernuhos)</li>
<li class="ja">講師用の解答（docs/instructor にあります）</li>
<li class="en">Instructor answer keys (kept in docs/instructor)</li>
<li class="ne" lang="ne-Latn">Prashikshakka uttarharu (docs/instructor ma chhan)</li>
<li class="ja">実行していない学習・検証の結果。保存された結果だけを「参考出力」として示します。</li>
<li class="en">Results of runs that were never executed; only saved results appear, labelled as
reference output</li>
<li class="ne" lang="ne-Latn">Nachalaieka prashikshan wa parikshanko natija. Surakshit bhaeka
natija matra "sandarbha natija" bhanera dekhainchha.</li>
</ul>

<h3><span class="ja">この PDF の読み方</span><br/><span class="en">How to read it</span><br/>
<span class="ne" lang="ne-Latn">Yo PDF kasari padhne</span></h3>
<p class="ja">図には「模式図（schematic）」・「合成データ（synthetic）」・「参考出力（参考に保存された
実際の結果）」のどれかを必ず書いています。実際に測った値と、説明のために描いた図を区別してください。
画像そのものは書き換えていません。</p>
<p class="en">Every figure is labelled as schematic, synthetic, or a reference output from a real
saved run. Keep measured numbers and explanatory drawings apart. No picture was redrawn or
edited.</p>
<p class="ne" lang="ne-Latn">Harek chitrama "yojanabaddha", "sansleshit data" wa "sandarbha natija"
bhanera lekhieko chha. Bastabik maap ra byakhyaka lagi banaiyeka chitra chhuttyaunuhos. Chitra aphai
bhane badalieko chhaina.</p>

<h3><span class="ja">この PDF に含まれる日</span><br/><span class="en">Days in this file</span><br/>
<span class="ne" lang="ne-Latn">Yo file ma bhaeka din</span></h3>
{day_list}

<h2><span class="ja">目次 / Table of contents</span><br/>
<span class="ne" lang="ne-Latn">Bishayasoochi</span></h2>
</section>
"""



def about_html(day_keys: list[str]) -> str:
    rows = []
    for key in day_keys:
        info = DAYS[key]
        rows.append(f'<li class="ja">{inline(info["ja"])}</li>'
                    f'<li class="en">{inline(info["en"])}</li>'
                    f'<li class="ne">{inline(info["ne"])}</li>')
    return ABOUT_HTML.format(ja=ABOUT_JA, en=ABOUT_EN, ne=ABOUT_NE, day_list="".join(rows))


def toc_html(toc: list[Heading], pages: dict[str, int] | None = None,
             hidden: bool = False) -> str:
    items = []
    for heading in toc:
        if not heading.in_toc or not heading.anchor:
            continue
        level = min(heading.level, 3)
        page = (pages or {}).get(heading.anchor, 0)
        parts = [f'<span class="ja" lang="ja">{inline(heading.ja)}</span>'] if heading.ja else []
        if heading.en:
            parts.append(f'<span class="en" lang="en">{inline(heading.en)}</span>')
        if heading.ne:
            parts.append(f'<span class="ne" lang="ne-Latn">{inline(heading.ne)}</span>')
        label = " ".join(parts)
        items.append(f'<li class="l{level}"><a href="#{heading.anchor}">'
                     f'<span class="toc-label">{label}</span>'
                     f'<span class="pg">{page}</span></a></li>')
    classes = "toc hidden" if hidden else "toc"
    return f'<nav class="{classes}"><ol>' + "".join(items) + "</ol></nav>"


def sources_html(day_keys: list[str]) -> str:
    rows = []
    for key in day_keys:
        info = DAYS[key]
        rows.append(f'<h3><span class="ja">{inline(info["ja"])}</span><br/>'
                    f'<span class="en">{inline(info["en"])}</span><br/>'
                    f'<span class="ne" lang="ne-Latn">{inline(info["ne"])}</span></h3><ul>')
        for stem in info["notebooks"]:
            matches = course_notebooks(NOTEBOOK_DIR, f"{stem}.ipynb")
            if matches:
                rows.append(f'<li class="en"><code>'
                            f'{matches[0].relative_to(COURSE_ROOT).as_posix()}</code></li>')
        rows.append("</ul>")
    return (
        '<section class="section">'
        '<h1><span class="ja">出典と参照</span><br/><span class="en">Sources and references</span>'
        '<br/><span class="ne" lang="ne-Latn">Srot ra sandarbha</span></h1>'
        '<p class="ja">本文と図の出典です。ノートブックを開いて、同じ内容を確認してください。</p>'
        '<p class="en">Sources for the text and figures. Open the notebooks to see the same '
        'material.</p>'
        '<p class="ne" lang="ne-Latn">Lekhai ra chitraka srot yi hun. Notebook kholera uhi samagri '
        'jaanchnuhos.</p>'
        + "".join(rows) +
        '<h3><span class="ja">図の出典</span><br/><span class="en">Figure provenance</span><br/>'
        '<span class="ne" lang="ne-Latn">Chitrako srot</span></h3><ul>'
        '<li class="en"><code>assets/diagrams/</code> — schematic and synthetic figures produced by '
        '<code>assets/scripts/generate_teaching_diagrams.py</code>; they are used unchanged.</li>'
        '<li class="ne" lang="ne-Latn"><code>assets/diagrams/</code> — '
        '<code>assets/scripts/generate_teaching_diagrams.py</code> le banaeka yojanabaddha ra '
        'sansleshit chitra; ti jastaka tastai prayog bhaeka chhan.</li>'
        '<li class="en"><code>assets/reference_outputs/</code> — figures built from results actually '
        'saved during this course.</li>'
        '<li class="ne" lang="ne-Latn"><code>assets/reference_outputs/</code> — yo talim ma saanchchai '
        'surakshit bhaeka natijabaat banaeka chitra.</li>'
        '</ul>'
        '<div class="note"><span class="ja">この資料は「うまくいった」とは書いていません。数字は'
        'すべて、保存された記録がある場合にだけ示しています。</span><br/>'
        '<span class="en">This companion never claims that training or testing succeeded. Numbers '
        'appear only where a saved record exists.</span><br/>'
        '<span class="ne" lang="ne-Latn">Yo samagrile "ramrosang saphal bhayo" bhanera dabi '
        'gardaina. Surakshit abhilekh bhaeko awastha ma matra sankhya dekhaieko chha.</span></div>'
        '</section>')





# ---------------------------------------------------------------------------
# build
# ---------------------------------------------------------------------------


def build_document(day_keys: list[str], *, single: bool) -> tuple[Document, int]:
    if single:
        info = DAYS[day_keys[0]]
        document = Document(info["ja"], info["en"], info["ne"])
        label = f"{day_keys[0][:3]} {int(day_keys[0][3:])}"
        document.add(cover_html(document, label, info["ja"], info["en"], info["ne"]))
    else:
        document = Document("第 1 週のまとめ", "the whole week in one document",
                            "Hapta 1 ko saransh")
        document.add(cover_html(document, "第 1 週（5 日間）/ Week 1 (five days)",
                                "第 1 週のまとめ", "the whole week in one document",
                                "Hapta 1 ko samagra samagri"))
    document.add(about_html(day_keys))
    toc_marker = len(document.body)
    document.add("")            # 目次はあとで入れる / the TOC is filled in after pass 1

    for position, key in enumerate(day_keys):
        info = DAYS[key]
        if len(day_keys) > 1:
            heading = Heading(level=1, ja=info["ja"], en=info["en"], ne=info["ne"],
                              anchor=f"day-{key}")
            document.toc.append(heading)
            document.add(f'<section class="section">{_heading_html(heading)}')
        else:
            document.add('<section class="section">')
        if position == 0:
            document.add(SENTINEL_HTML)
        document.add('<h3><span class="ja">前提</span><br/><span class="en">Prerequisites</span>'
                     '<br/><span class="ne" lang="ne-Latn">Poorwashart</span></h3>')
        document.add(f'<p class="ja">{inline(info["prerequisites_ja"])}</p>'
                     f'<p class="en">{inline(info["prerequisites_en"])}</p>'
                     f'<p class="ne">{inline(info["prerequisites_ne"])}</p>')
        document.add('<h3><span class="ja">この日の到達点</span><br/>'
                     '<span class="en">Learning objectives</span><br/>'
                     '<span class="ne" lang="ne-Latn">Yo dinko upalabdhi</span></h3><ol>')
        for ja, en, ne in info["objectives"]:
            document.add(f'<li><span class="ja">{inline(ja)}</span><br/>'
                         f'<span class="en">{inline(en)}</span><br/>'
                         f'<span class="ne">{inline(ne)}</span></li>')
        document.add("</ol>")

        for stem in info["notebooks"]:
            matches = course_notebooks(NOTEBOOK_DIR, f"{stem}.ipynb")
            if len(matches) != 1:
                raise SystemExit(f"{stem}: expected exactly one notebook, found {matches}")
            notebook_html(matches[0], document, toc_level=1 if not single else 1)
        document.add("</section>")

    document.add(sources_html(day_keys))
    return document, toc_marker


def check_fonts(page, needs_devanagari: bool) -> dict:
    """Check the actual Chromium platform fonts, not fonts.check's generic fallback.

    Romanized Nepali is Latin text, so the Latin probe must resolve to a real installed family.
    The Devanagari probe only runs for the notebooks that still carry Devanagari (Days 1-3 during
    the migration); a Latin-only booklet must not require a Devanagari font.
    """
    page.evaluate("""async () => {
        const make = (id, text) => {
            const span = document.createElement('span');
            span.id = id;
            span.className = 'ne';
            span.style.cssText = 'position:fixed;left:0;top:0';
            span.textContent = text;
            document.body.append(span);
        };
        make('ne-latin-check', 'Pahile calibration datama threshold chhannuhos.');
        make('ne-devanagari-check', 'प्रशिक्षणक्षत्रज्ञश्रनिर्देशाङ्क');
        await document.fonts.ready;
        document.querySelectorAll('#ne-latin-check,#ne-devanagari-check')
            .forEach((node) => node.getBoundingClientRect());
    }""")
    session = page.context.new_cdp_session(page)
    session.send("DOM.enable")
    session.send("CSS.enable")
    root = session.send("DOM.getDocument")["root"]["nodeId"]

    def families(selector: str) -> list[str]:
        node = session.send("DOM.querySelector",
                            {"nodeId": root, "selector": selector})["nodeId"]
        fonts = session.send("CSS.getPlatformFontsForNode", {"nodeId": node})["fonts"]
        return [font["familyName"] for font in fonts if font["glyphCount"]]

    latin = families("#ne-latin-check")
    devanagari = families("#ne-devanagari-check") if needs_devanagari else []
    page.evaluate("() => document.querySelectorAll('#ne-latin-check,#ne-devanagari-check')"
                  ".forEach((node) => node.remove())")
    session.detach()

    if not latin or any(family == "LastResort" for family in latin):
        raise RuntimeError(
            "No verified font coverage for the Nepali text. Install Segoe UI (or another Latin "
            f"family). Chromium resolved: {latin!r}")
    if needs_devanagari:
        supported = {"Nirmala UI", "Noto Sans Devanagari", "Mangal", "Arial Unicode MS"}
        if not devanagari or any(family not in supported for family in devanagari):
            raise RuntimeError(
                "No verified Devanagari font coverage. This booklet still contains Devanagari "
                "Nepali; install Nirmala UI, Noto Sans Devanagari or Mangal before exporting. "
                f"Chromium resolved: {devanagari!r}")
    return {"latin": latin, "devanagari": devanagari}


def render(html_path: Path, pdf_path: Path, footer_label: str) -> None:
    from playwright.sync_api import sync_playwright

    header = (
        '<div style="font-size:7px;color:#57606a;width:100%;padding:0 18mm;'
        'display:flex;justify-content:space-between;">'
        f'<span>{html.escape(footer_label)}</span>'
        f'<span style="font-family:\'Yu Gothic\',sans-serif;">{html.escape(COURSE_TITLE_JA)}</span>'
        "</div>")
    footer = (
        '<div style="font-size:7px;color:#57606a;width:100%;padding:0 18mm;'
        'display:flex;justify-content:space-between;">'
        '<span>p. <span class="pageNumber"></span> / <span class="totalPages"></span></span>'
        f'<span>再生成 / rebuild: {html.escape(REBUILD_COMMAND)}</span>'
        "</div>")
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.goto(html_path.as_uri(), wait_until="load")
        page.emulate_media(media="print")
        page.evaluate("document.fonts.ready")
        needs_devanagari = bool(DEVANAGARI_RE.search(html_path.read_text(encoding="utf-8")))
        check_fonts(page, needs_devanagari)
        page.pdf(path=str(pdf_path), format="A4", print_background=True, prefer_css_page_size=True,
                 display_header_footer=True, header_template=header, footer_template=footer,
                 margin={"top": "20mm", "bottom": "18mm", "left": "18mm", "right": "18mm"})
        browser.close()


def page_texts(pdf_path: Path) -> list[str]:
    import pypdfium2 as pdfium

    pdf = pdfium.PdfDocument(str(pdf_path))
    texts = []
    for index in range(len(pdf)):
        page = pdf[index]
        texts.append(page.get_textpage().get_text_range())
    return texts


def locate_headings(texts: list[str], toc: list[Heading],
                    body_start: int = 1) -> dict[str, int]:
    """見出しのページ番号を、本文の出現順から求める / map each heading to its page number.

    ``body_start`` is the first page of the body, i.e. the page after the table of contents.
    The hidden TOC still leaves its text in the PDF text layer, so the search must not start inside
    it: otherwise every entry resolves to the TOC page that happens to list it.
    """
    pages: dict[str, int] = {}
    keys = [_search_key(text) for text in texts]
    offsets = [0]
    for key in keys:
        offsets.append(offsets[-1] + len(key))
    body = "".join(keys)
    cursor = offsets[max(body_start - 1, 0)]
    for heading in toc:
        if not heading.anchor or not heading.in_toc:
            continue
        # 言語ごとに分けて探します。長い見出しがページ境界にまたがると、抽出した文字列の間に
        # ヘッダ・フッタが入り、連結した 1 つの文字列では見つからなくなるためです。
        # Search one language at a time: a long heading that crosses a page boundary has the running
        # header and footer interleaved in the text layer, so the concatenated form is not found.
        parts = [part for part in (_search_key(piece) for piece
                                   in (heading.ja, heading.en, heading.ne) if piece) if part]
        if not parts:
            raise ValueError(f"PDF heading has no searchable text: {heading.plain!r}")
        start = None
        for part in parts:
            position = body.find(part, cursor)
            if position < 0:
                raise ValueError(f"PDF heading not found in body order: {heading.plain!r}")
            if start is None:
                start = position
            cursor = position + len(part)
        pages[heading.anchor] = bisect.bisect_right(offsets, start)
    return pages


def body_start_page(texts: list[str]) -> int:
    """本文の最初のページ / the first page of the body, found by its sentinel."""
    for index, text in enumerate(texts):
        if BODY_SENTINEL in _search_key(text):
            return index + 1
    raise ValueError("PDF body marker missing; refusing to assign TOC page numbers")


def _search_key(text: str) -> str:
    """比較用に、空白と組み版用の記号を落とす / normalise text for page lookups."""
    text = re.sub(r"[`*]", "", text)
    return re.sub(r"\s+", "", text)


def add_bookmarks(pdf_path: Path, toc: list[Heading], pages: dict[str, int]) -> None:
    from pypdf import PdfReader, PdfWriter

    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    writer.append(reader)
    parents: dict[int, object] = {}
    for heading in toc:
        page = pages.get(heading.anchor)
        if not page or page > len(reader.pages):
            continue
        title = re.sub(r"\s+", " ", heading.plain).strip()[:180] or "(untitled)"
        level = min(heading.level, 3)
        if level <= 1:
            parents = {1: writer.add_outline_item(title, page - 1)}
        else:
            parent = parents.get(level - 1) or parents.get(1)
            parents[level] = writer.add_outline_item(title, page - 1, parent=parent)
    writer.add_metadata({"/Title": reader.metadata.get("/Title", "") if reader.metadata else "",
                         "/Author": "Training_Automation course",
                         "/Subject": "Japanese / English / Nepali (Romanized, ne-Latn) companion"})
    with pdf_path.open("wb") as handle:
        writer.write(handle)


def build_pdf(out_path: Path, day_keys: list[str], footer_label: str) -> dict:
    document, toc_marker = build_document(day_keys, single=len(day_keys) == 1)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="trilingual-") as tmp:
        html_path = Path(tmp) / "doc.html"
        probe_path = Path(tmp) / "probe.pdf"

        document.body[toc_marker] = toc_html(document.toc, hidden=True)
        html_path.write_text(html_document(document), encoding="utf-8")
        render(html_path, probe_path, footer_label)
        probe_pages = page_texts(probe_path)
        pages = locate_headings(probe_pages, document.toc, body_start_page(probe_pages))

        document.body[toc_marker] = toc_html(document.toc, pages)
        html_path.write_text(html_document(document), encoding="utf-8")
        render(html_path, out_path, footer_label)

    final_pages = page_texts(out_path)
    final_map = locate_headings(final_pages, document.toc, body_start_page(final_pages))
    if final_map != pages:
        raise ValueError(f"TOC pagination changed between passes: {out_path.name}")
    add_bookmarks(out_path, document.toc, final_map)
    return {"pages": len(final_pages), "toc_entries": len(pages)}


def general_pdf(out_path: Path, job: dict) -> dict:
    """一般文書（START_HERE / README / シラバス / 準備ノートブック）の 3 言語 PDF。

    The general companion reuses the same two-pass render as a day booklet: the table of contents
    is laid out invisibly first so the page numbers can be looked up, then again with the numbers.
    """
    document = Document(job["ja"], job["en"], job["ne"])
    document.add(cover_html(document, job["label"], job["ja"], job["en"], job["ne"]))
    document.add(about_html([]))
    toc_marker = len(document.body)
    document.add("")

    document.add('<section class="section">')
    document.add(SENTINEL_HTML)
    for number, (path, label) in enumerate(job["sources"], start=1):
        heading = Heading(level=1, ja=label, anchor=f"src-{number}")
        document.toc.append(heading)
        document.add(_heading_html(heading))
        if path.suffix == ".ipynb":
            notebook_html(path, document, toc_level=2)
        else:
            document.add(f'<p class="path en">source: <code>'
                         f'{path.relative_to(COURSE_ROOT).as_posix()}</code></p>')
            document.add(markdown_cell_html(path.read_text(encoding="utf-8"), path.parent,
                                            path.stem, document))
    document.add("</section>")
    document.add(sources_html([]))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="trilingual-") as tmp:
        html_path = Path(tmp) / "doc.html"
        probe_path = Path(tmp) / "probe.pdf"
        document.body[toc_marker] = toc_html(document.toc, hidden=True)
        html_path.write_text(html_document(document), encoding="utf-8")
        render(html_path, probe_path, job["label"])
        probe_pages = page_texts(probe_path)
        pages = locate_headings(probe_pages, document.toc, body_start_page(probe_pages))

        document.body[toc_marker] = toc_html(document.toc, pages)
        html_path.write_text(html_document(document), encoding="utf-8")
        render(html_path, out_path, job["label"])

    final_pages = page_texts(out_path)
    final_map = locate_headings(final_pages, document.toc, body_start_page(final_pages))
    if final_map != pages:
        raise ValueError(f"TOC pagination changed between passes: {out_path.name}")
    add_bookmarks(out_path, document.toc, final_map)
    return {"pages": len(final_pages), "toc_entries": len(pages)}


JOBS = [(key, [key], f"{key} 解説 / explanation") for key in DAY_ORDER]
JOBS.append(("Week1", DAY_ORDER, "第 1 週 まとめ / Week 1 companion"))

DOC_JOBS = [
    dict(
        name="Setup",
        label="準備ノートブック / setup notebook",
        ja="第 0 日　環境セットアップ",
        en="Day 0 — setting up the environment",
        ne="Din 0 — batabaran setup",
        sources=[(NOTEBOOK_DIR / "00_Setup" / "00_Environment_Setup.ipynb",
                  "環境セットアップ / Environment setup / Batabaran setup")],
    ),
    dict(
        name="Installation_Guide",
        label="インストール手順 / installation guide",
        ja="インストールとトラブル対処",
        en="Installation and troubleshooting",
        ne="Installation ra samasya samadhan",
        sources=[
            (COURSE_ROOT / "START_HERE.md",
             "はじめかた / START HERE / Suru garne tarika"),
            (COURSE_ROOT / "docs" / "troubleshooting" / "installation.md",
             "インストール時のトラブル対処 / Installation troubleshooting / "
             "Installation ka samasya"),
        ],
    ),
    dict(
        name="Repository_Guide",
        label="リポジトリ案内 / repository guide",
        ja="研修リポジトリの案内",
        en="Guide to the course repository",
        ne="Talim repository ko parichay",
        sources=[
            (COURSE_ROOT / "README.md",
             "README / リポジトリ概要 / Repository ko saransh"),
            (COURSE_ROOT / "requirements" / "tested_versions.md",
             "検証済みバージョン / Tested versions / Janchieka sanskaran"),
        ],
    ),
    dict(
        name="Course_Syllabus",
        label="研修シラバス / course syllabus",
        ja="研修シラバス",
        en="Course syllabus",
        ne="Talimko samayatalika",
        sources=[
            (COURSE_ROOT / "COURSE_SYLLABUS.md",
             "研修シラバス / COURSE SYLLABUS / Talimko samayatalika"),
        ],
    ),
]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Export tri-language (ja, en, ne) PDFs.")
    parser.add_argument("--only", default=None,
                        help="Day01 … Day05, Week1, Setup, Installation, Repository, Syllabus")
    parser.add_argument("--check", action="store_true", help="build into a temporary folder")
    parser.add_argument("--out", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--languages", default="ja,en,ne",
                        help="accepted for symmetry with the ReportLab exporter; must name ne")
    args = parser.parse_args(argv)

    if "ne" not in [part.strip() for part in args.languages.split(",")]:
        parser.error("the tri-language exporter needs 'ne' in --languages")

    results = {}
    for name, keys, label in JOBS:
        if args.only and args.only not in name:
            continue
        out_path = args.out / f"{name}_explanation_ja_en_ne.pdf"
        info = build_pdf(out_path, keys, label)
        results[name] = info
        print(f"[pdf] {out_path.name}  pages={info['pages']}  toc={info['toc_entries']}"
              f"  {out_path.stat().st_size / 1024:,.0f} KB")
    for job in DOC_JOBS:
        if args.only and args.only not in job["name"]:
            continue
        out_path = args.out / f"{job['name']}_ja_en_ne.pdf"
        info = general_pdf(out_path, job)
        results[job["name"]] = info
        print(f"[pdf] {out_path.name}  pages={info['pages']}  toc={info['toc_entries']}"
              f"  {out_path.stat().st_size / 1024:,.0f} KB")
    return 0 if results else 1


if __name__ == "__main__":
    raise SystemExit(main())
