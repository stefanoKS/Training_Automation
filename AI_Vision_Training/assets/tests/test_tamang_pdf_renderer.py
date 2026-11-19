"""タマン語 PDF の描画経路 / the rendering path a ``*_ja_en_taj.pdf`` would use.

No Tamang booklet can be built yet (the localization gate blocks it), so this module verifies the
parts that do not depend on the text being approved:

* Devanagari is shaped by the same Chromium/HarfBuzz path and lands in the PDF as **searchable
  Unicode**, not as private-use glyphs;
* headings, tables, images, links and page breaks survive that path;
* ``export_trilingual_pdf --locale taj`` refuses to write ``*_ja_en_taj.pdf`` while the gate fails,
  and never renames a Nepali booklet into a Tamang one.

The Devanagari sample here is the attested name of the language (``तामाङ``), used as a *rendering*
fixture — it is not presented as a translation of any lesson.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

pytest.importorskip("playwright.sync_api")
pytest.importorskip("pypdfium2")

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "assets" / "scripts"))

import export_trilingual_pdf as exporter  # noqa: E402

SAMPLE = "तामाङ भाषा"


@pytest.fixture(scope="module")
def rendered(tmp_path_factory) -> dict:
    folder = tmp_path_factory.mktemp("taj-render")
    image = ROOT / "assets" / "diagrams" / "diagram_dataset_split.png"
    html = f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><style>
body {{ font-family: "Yu Gothic", "Nirmala UI", sans-serif; }}
table {{ border-collapse: collapse; }}
td, th {{ border: 1px solid #888; padding: 4px; }}
p {{ page-break-before: always; }}
</style></head><body>
<h1 lang="taj-Deva">固定の記録 / freeze record</h1>
<p lang="taj-Deva">{SAMPLE}</p>
<table><thead><tr><th>手順</th><th>Step</th></tr></thead>
<tbody><tr><td>1</td><td>split</td></tr></tbody></table>
<img src="{image.as_uri()}" style="width:80mm"/>
<p><a href="https://example.org/docs">link</a></p>
</body></html>"""
    html_path = folder / "sample.html"
    html_path.write_text(html, encoding="utf-8")
    pdf_path = folder / "sample.pdf"
    exporter.render(html_path, pdf_path, "taj rendering fixture")
    return {"pdf": pdf_path, "texts": exporter.page_texts(pdf_path)}


def test_devanagari_survives_as_searchable_text(rendered) -> None:
    text = "\n".join(rendered["texts"])
    assert SAMPLE in text, "the Devanagari sample must be searchable in the PDF text layer"
    assert "\u0924\u093e\u092e\u093e\u0919" in text  # तामाङ
    assert "freeze record" in text, "the Japanese/English heading must survive too"


def test_tables_and_links_survive_the_render(rendered) -> None:
    text = "\n".join(rendered["texts"])
    assert "split" in text and "手順" in text
    assert len(rendered["texts"]) >= 2, "the forced page break must produce a second page"


def test_the_gate_refuses_to_build_a_tamang_booklet(tmp_path) -> None:
    out = tmp_path / "pdf"
    out.mkdir()
    assert exporter.main(["--locale", "taj", "--only", "Day05", "--out", str(out)]) == 2
    assert not list(out.glob("*_ja_en_taj.pdf")), "no Tamang booklet may be produced yet"
    assert not list(out.glob("*.pdf"))


def test_switching_the_locale_does_not_relabel_the_nepali_booklets(tmp_path) -> None:
    exporter.configure_locale("ne")
    assert exporter.LOCALE.code == "ne"
    assert exporter.LANG_ATTR["ne"] == "ne-Latn"
    assert exporter.LOCALE.pdf_suffix() == "ja_en_ne"

    exporter.configure_locale("taj")
    assert exporter.LANG_ATTR["ne"] == "taj-Deva"
    assert exporter.LOCALE.pdf_suffix() == "ja_en_taj"
    # the Tamang build must not borrow the Romanized Nepali course title
    assert "hapta" not in exporter.COURSE_TITLE_NE
    exporter.configure_locale("ne")
