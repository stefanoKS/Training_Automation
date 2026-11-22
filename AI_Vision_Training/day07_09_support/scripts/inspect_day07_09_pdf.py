"""Render every Day 7-9 PDF page to PNG for visual inspection and run text checks.

Run from any directory:
    python AI_Vision_Training\\day07_09_support\\scripts\\inspect_day07_09_pdf.py

Output goes to docs/pdf/_pages/ (ignored by Git). The command fails when a required
module title, language sample or embedded figure count is missing.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pypdfium2 as pdfium
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
PDF_DIR = ROOT / "docs" / "pdf"
PAGES = PDF_DIR / "_pages"

REQUIRED = {
    "Day07": ("機械の基礎", "Mechanical Fundamentals", "センサと信号", "Sensors and Signals",
              "アクチュエータと機械構成", "Actuators and Machine Construction"),
    "Day08": ("PLCの基礎", "PLC Fundamentals", "ラダープログラムの基礎", "Ladder Programming Basics",
              "シーケンス制御", "Sequence Control"),
    "Day09": ("視覚ハードウェア", "Vision Hardware", "産業用PCとAI処理", "Industrial PC and AI Processing",
              "システム統合", "Complete System Integration"),
}


def main() -> int:
    failures: list[str] = []
    for day, required in REQUIRED.items():
        pdf_path = PDF_DIR / f"{day}_explanation_ja_en.pdf"
        if not pdf_path.is_file():
            failures.append(f"missing {pdf_path.name}")
            continue
        reader = PdfReader(str(pdf_path))
        text = re.sub(r"\s+", " ", "\n".join(page.extract_text() or "" for page in reader.pages))
        offsets = []
        for phrase in required:
            index = text.find(phrase)
            if index < 0:
                failures.append(f"{day}: missing text {phrase!r}")
            offsets.append(index if index >= 0 else 10 ** 9)
        if offsets[:2] != sorted(offsets[:2]) or offsets[2:4] != sorted(offsets[2:4]) or offsets[4:6] != sorted(offsets[4:6]):
            failures.append(f"{day}: module order is wrong")
        if not re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", text):
            failures.append(f"{day}: no Japanese text found")
        if not re.search(r"\b(?:the|and|ladder|result)\b", text, re.I):
            failures.append(f"{day}: no English text found")
        figures = sum(len(page.images) for page in reader.pages)
        if figures < 6:
            failures.append(f"{day}: only {figures} embedded images")
        if len(reader.pages) < 8:
            failures.append(f"{day}: only {len(reader.pages)} pages")

        target = PAGES / day
        target.mkdir(parents=True, exist_ok=True)
        document = pdfium.PdfDocument(str(pdf_path))
        for index in range(len(document)):
            image = document[index].render(scale=1.6).to_pil()
            image.save(target / f"page-{index + 1:02d}.png")
        print(f"{day}: {len(reader.pages)} pages, {figures} images, rendered to {target.relative_to(ROOT)}")

    if failures:
        print("\n".join("FAIL: " + failure for failure in failures), file=sys.stderr)
        return 1
    print("PDF inspection passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
