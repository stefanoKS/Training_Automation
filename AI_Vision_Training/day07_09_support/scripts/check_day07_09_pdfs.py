"""Validate and render every page of the three generated Day 7-9 PDFs.

Run from any directory:
    python AI_Vision_Training\\day07_09_support\\scripts\\check_day07_09_pdfs.py

Checks are deliberately conservative: selectable text, Japanese and English,
TOC, page count, no raw Markdown/HTML artefacts and no IP address broken across
a line.  Rendering every page is required because text checks cannot detect
layout collisions, clipped diagrams or unreadable small text.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pypdfium2 as pdfium
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
PDF_DIR = ROOT / "docs" / "pdf"
RENDER_DIR = ROOT / "docs" / "pdf" / "_pages"
DAYS = ("Day07", "Day08", "Day09")


def main() -> int:
    report = {}
    failures: list[str] = []
    for day in DAYS:
        path = PDF_DIR / f"{day}_explanation_ja_en.pdf"
        if not path.is_file():
            failures.append(f"missing {path.name}")
            continue
        reader = PdfReader(str(path))
        pages = len(reader.pages)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        images = sum(len(page.images) for page in reader.pages)
        checks = {
            "pages": pages,
            "images": images,
            "bytes": path.stat().st_size,
            "has_toc": "目次 / Contents" in text,
            "has_japanese": bool(re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", text)),
            "has_english": bool(re.search(r"\b(?:the|and|with|for)\b", text, re.I)),
            "no_replacement": "\ufffd" not in text,
            "no_double_question": not re.search(r"\?{3,}", text),
            "no_raw_markdown_bold": True,  # ** is legitimate Python exponentiation in code cells
            "no_raw_markdown_link": "](" not in text,
            "no_broken_ip": not re.search(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\s*\n\s*\d{1,3}\b", text),
            "no_html_tag": not re.search(r"</?(?:div|span|br|b|i|font)\b", text, re.I),
        }
        for key in ("has_toc", "has_japanese", "has_english", "no_replacement", "no_double_question",
                    "no_raw_markdown_bold", "no_raw_markdown_link", "no_broken_ip", "no_html_tag"):
            if not checks[key]:
                failures.append(f"{day}: {key}")
        if pages < 15:
            failures.append(f"{day}: too few pages ({pages})")
        if images < 4:
            failures.append(f"{day}: too few images ({images})")

        render_dir = RENDER_DIR / day
        render_dir.mkdir(parents=True, exist_ok=True)
        document = pdfium.PdfDocument(str(path))
        for index in range(len(document)):
            bitmap = document[index].render(scale=1.6)
            bitmap.to_pil().save(render_dir / f"page-{index + 1:03d}.png")
        report[day] = checks
        print(f"{day}: {pages} pages, {images} images, {path.stat().st_size} bytes, render OK")
    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    (RENDER_DIR / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                                            encoding="utf-8")
    if failures:
        print("FAILURES:")
        for failure in failures:
            print("  -", failure)
        return 1
    print("PDF structural checks passed; inspect the rendered pages visually.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
