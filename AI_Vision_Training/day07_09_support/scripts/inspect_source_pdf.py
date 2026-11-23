"""Inspect the immutable source PDF used by the Day 7-9 curriculum.

Run from any directory (repository virtual environment):
    python AI_Vision_Training\\day07_09_support\\scripts\\inspect_source_pdf.py

The original Japanese five-day trainee PDF is the primary curriculum source.
This script never modifies it. It records:
  * SHA-256, byte size and page count;
  * the extracted text of every page;
  * a rendered PNG of every page (for human visual inspection);
  * a machine-readable report used by the audit trail.

Rendering uses pypdfium2, which ships with the training virtual environment.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parents[2]
SOURCE_PDF = ROOT / "docs" / "reference" / "自動化設備製作研修_5日間_詳細版_受講者用.pdf"
REFERENCE_DATA = ROOT / "day07_09_support" / "reference_data"
OUT_DIR = REFERENCE_DATA / "pdf_extract"
RENDER_DIR = OUT_DIR / "pages"
EXPECTED_SHA256 = "3380c2b67e148cd9a71b0f9071963744f3b0acba7491b309708b0f31183707ae"


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect(render: bool = True) -> dict:
    if not SOURCE_PDF.exists():
        raise FileNotFoundError(f"Source PDF missing: {SOURCE_PDF}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if render:
        RENDER_DIR.mkdir(parents=True, exist_ok=True)

    digest = sha256_of(SOURCE_PDF)
    document = pdfium.PdfDocument(str(SOURCE_PDF))
    page_count = len(document)
    pages = []
    text_chunks = []
    for index in range(page_count):
        page = document[index]
        text = page.get_textpage().get_text_bounded()
        text_chunks.append(f"===== PAGE {index + 1} =====\n{text}")
        rendered = None
        if render:
            bitmap = page.render(scale=2.0)
            image = bitmap.to_pil()
            target = RENDER_DIR / f"page-{index + 1:03d}.png"
            image.save(target)
            rendered = str(target.relative_to(ROOT)).replace("\\", "/")
        pages.append(
            {
                "pdf_page": index + 1,
                "characters": len(text.strip()),
                "rendered_png": rendered,
            }
        )

    (OUT_DIR / "source_text.txt").write_text("\n".join(text_chunks), encoding="utf-8")
    report = {
        "source_pdf": str(SOURCE_PDF.relative_to(ROOT)).replace("\\", "/"),
        "sha256": digest,
        "expected_sha256": EXPECTED_SHA256,
        "sha256_matches_expected": digest == EXPECTED_SHA256,
        "bytes": SOURCE_PDF.stat().st_size,
        "page_count": page_count,
        "pages": pages,
        "note": (
            "Text extraction is a navigation aid only. Ladder diagrams, pneumatic "
            "circuits and wiring drawings were inspected as rendered images because "
            "text extraction cannot verify graphical symbol semantics."
        ),
    }
    (OUT_DIR / "inspection_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"SHA-256: {digest}")
    print(f"Expected match: {digest == EXPECTED_SHA256}")
    print(f"Pages: {page_count}")
    print(f"Text:  {OUT_DIR / 'source_text.txt'}")
    if render:
        print(f"PNGs:  {RENDER_DIR} ({page_count} pages)")
    return report


if __name__ == "__main__":
    inspect(render=True)
