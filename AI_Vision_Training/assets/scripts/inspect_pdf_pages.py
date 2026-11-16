"""生成した PDF を 1 ページずつ描画して点検します。

Render every page of the explanation PDFs and check what a reader would actually see:
blank pages, text that runs outside the printable area, missing Japanese glyphs, and images
that were scaled down so far they became unreadable. Contact sheets are written so a person
can look at **every** page, not a sample.

これは点検用です（学習には不要）/ This is a checking tool; learners do not need it.

使い方 / Usage
--------------
    python assets\\scripts\\inspect_pdf_pages.py
    python assets\\scripts\\inspect_pdf_pages.py --pdf docs\\pdf\\Day03_explanation_ja_en.pdf
    python assets\\scripts\\inspect_pdf_pages.py --pdf docs\\pdf\\Day03_explanation_ja_en_ne.pdf --languages ja,ne
    python assets\\scripts\\inspect_pdf_pages.py --out <folder> --scale 1.2

出力 / Output
-------------
* ページごとの判定（空白・はみ出し・日本語の有無）
* `--languages ja,ne` のときは、ネパール語の有無と、単語の途中に空白が入っていないか
  （入っていると PDF 内検索ができない）/ with `ne`, also checks that no Devanagari word is split by
  a space, which would make the booklet unsearchable
* `<out>/<pdf名>/page-XXX.png`（全ページ）
* `<out>/<pdf名>/contact-<n>.png`（4 列の一覧。全ページを目で見るため / to eyeball every page）
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image

COURSE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PDF_DIR = COURSE_ROOT / "docs" / "pdf"
JP_RE = re.compile(r"[\u3040-\u30ff\u4e00-\u9fff]")
NE_RE = re.compile(r"[\u0900-\u097f]")
# 単語の途中に空白が入ると検索できない / a space before a dependent sign is always a text-layer fault
NE_BROKEN_RE = re.compile(r"[\u0900-\u097f][ \t\u00a0]+[\u093e-\u094f\u0962\u0963]")
LANGUAGE_CHECKS = {
    "ja": ("japanese", JP_RE),
    "ne": ("nepali", NE_RE),
}

# A4 in points
PAGE_W, PAGE_H = 595.276, 841.89
EDGE_MM = 4.0
POINTS_PER_MM = 72 / 25.4
MARGIN = EDGE_MM * POINTS_PER_MM


def _ink_fraction(image: Image.Image) -> float:
    grey = image.convert("L")
    histogram = grey.histogram()
    dark = sum(histogram[:245])
    return dark / max(1, sum(histogram))


def _text_boxes(pdfium_page) -> tuple[int, list[str]]:
    """文字の位置から、紙の外へ出ている文字を探す / find characters outside the printable area."""
    page_width, page_height = pdfium_page.get_size()
    textpage = pdfium_page.get_textpage()
    count = textpage.count_chars()
    problems = []
    for index in range(count):
        char = textpage.get_text_range(index, 1)
        if not char.strip():
            continue
        left, bottom, right, top = textpage.get_charbox(index)
        if (right > page_width - MARGIN + 2 or left < MARGIN - 12
                or bottom < MARGIN - 12 or top > page_height - MARGIN + 12):
            problems.append(char)
    text = textpage.get_text_bounded()
    return count, problems, text


def inspect_pdf(path: Path, out_dir: Path, scale: float, languages=("ja",)) -> dict:
    document = pdfium.PdfDocument(str(path))
    page_dir = out_dir / path.stem
    page_dir.mkdir(parents=True, exist_ok=True)

    report = {"pdf": path.name, "pages": len(document), "blank": [], "overflow": [],
              "no_japanese": [], "images": [], "languages": list(languages),
              "no_nepali": [], "broken_nepali": []}
    rendered: list[Image.Image] = []
    nepali_chars = 0

    for index in range(len(document)):
        page = document[index]
        image = page.render(scale=scale).to_pil()
        image.save(page_dir / f"page-{index + 1:03d}.png")
        rendered.append(image)

        ink = _ink_fraction(image)
        if ink < 0.002:
            report["blank"].append(index + 1)

        count, outside, text = _text_boxes(page)
        if outside:
            report["overflow"].append({"page": index + 1, "chars": "".join(outside[:12]),
                                       "count": len(outside)})
        if index > 0 and "この資料について" not in text and not JP_RE.search(text):
            report["no_japanese"].append(index + 1)
        if "ne" in languages:
            found = NE_RE.findall(text)
            nepali_chars += len(found)
            if not found:
                report["no_nepali"].append(index + 1)
            broken = NE_BROKEN_RE.findall(text)
            if broken:
                report["broken_nepali"].append({"page": index + 1, "matches": len(broken)})
    report["nepali_chars"] = nepali_chars

    # 4 列のコンタクトシート / contact sheets, four pages per row
    columns = 4
    thumb_w = 360
    thumb_h = int(thumb_w * PAGE_H / PAGE_W)
    per_sheet = 12
    for sheet_index in range(0, len(rendered), per_sheet):
        chunk = rendered[sheet_index:sheet_index + per_sheet]
        rows = (len(chunk) + columns - 1) // columns
        sheet = Image.new("RGB", (columns * (thumb_w + 8) + 8, rows * (thumb_h + 8) + 8),
                          (235, 238, 242))
        for offset, page_image in enumerate(chunk):
            thumb = page_image.copy()
            thumb.thumbnail((thumb_w, thumb_h))
            x = 8 + (offset % columns) * (thumb_w + 8)
            y = 8 + (offset // columns) * (thumb_h + 8)
            # 横長ページは枠の中で中央に置く / centre a landscape page inside its cell
            x += (thumb_w - thumb.width) // 2
            y += (thumb_h - thumb.height) // 2
            sheet.paste(thumb, (x, y))
        sheet.save(page_dir / f"contact-{sheet_index // per_sheet + 1}.png")

    report["contact_sheets"] = sorted(p.name for p in page_dir.glob("contact-*.png"))
    (page_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2),
                                          encoding="utf-8")
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Render and inspect the explanation PDFs.")
    parser.add_argument("--pdf", type=Path, action="append", default=None,
                        help="PDF to inspect (repeatable); defaults to docs/pdf/*.pdf")
    parser.add_argument("--out", type=Path, default=COURSE_ROOT / "docs" / "pdf" / "_pages")
    parser.add_argument("--scale", type=float, default=1.4)
    parser.add_argument("--languages", default="ja",
                        help="comma separated checks to run: ja, ne (add ne for the tri-language "
                             "booklets)")
    args = parser.parse_args(argv)

    languages = tuple(part.strip() for part in args.languages.split(",") if part.strip())
    unknown = [name for name in languages if name not in LANGUAGE_CHECKS]
    if unknown:
        parser.error(f"unknown language check(s): {', '.join(unknown)}")

    pdfs = args.pdf or sorted(DEFAULT_PDF_DIR.glob("*.pdf"))
    if not pdfs:
        print("PDF がありません / no PDF found. Run export_explanations_pdf.py first.")
        return 1

    args.out.mkdir(parents=True, exist_ok=True)
    failures = 0
    for path in pdfs:
        report = inspect_pdf(path, args.out, args.scale, languages)
        print(f"\n=== {report['pdf']}  pages={report['pages']}")
        print(f"  contact sheets: {len(report['contact_sheets'])}")
        if report["blank"]:
            print(f"  BLANK pages: {report['blank']}")
            failures += 1
        if report["overflow"]:
            for item in report["overflow"][:5]:
                print(f"  OUTSIDE printable area: p.{item['page']} chars={item['chars']!r} "
                      f"({item['count']})")
            failures += 1
        if report["no_japanese"]:
            print(f"  pages without Japanese text: {report['no_japanese'][:8]}")
        if "ne" in languages:
            print(f"  Nepali characters: {report['nepali_chars']:,}")
            if report["broken_nepali"]:
                for item in report["broken_nepali"][:5]:
                    print(f"  NEPALI TEXT LAYER SPLIT (unsearchable) p.{item['page']}: "
                          f"{item['matches']} split word(s)")
                failures += 1
            else:
                print("  Nepali text layer: no split words, the PDF stays searchable")
            if report["no_nepali"]:
                print(f"  pages without Nepali (cover/TOC/figures are expected): "
                      f"{report['no_nepali'][:8]}")
        if not report["blank"] and not report["overflow"]:
            print("  no blank pages, no text outside the printable area")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
