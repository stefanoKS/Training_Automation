"""タマン語ローカライズの契約 / the Tamang (taj) localization contracts.

These tests pin the properties that matter and that a script test cannot give:

* the locale is declared as Tamang in Devanagari, **unconfirmed**, and separate from Nepali;
* all 16 notebook catalogs and all 12 document catalogs exist and carry provenance;
* the *inventory* of pending blocks equals the set of cells the legacy Nepali pass translated, so
  replacing the language did not silently drop teaching content;
* the insertion tools refuse Latin/English text as Tamang, keep the Japanese and English source
  untouched, and are idempotent;
* the production gate fails while any block is pending, unreviewed, or the variety is unconfirmed —
  and cannot be opened by a script test or by a machine draft.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "assets" / "helpers"))
sys.path.insert(0, str(ROOT / "assets" / "scripts"))

import apply_docs  # noqa: E402
import apply_translations  # noqa: E402
import check_localization_coverage as coverage  # noqa: E402
from course_notebooks import course_notebooks  # noqa: E402
from i18n_locales import LOCALES, locale  # noqa: E402

TAJ = locale("taj")


def catalog_paths(loc) -> list[Path]:
    folder = loc.catalog_dir("notebooks")
    return sorted(folder.glob(f"*.{loc.code}.md"))


def doc_catalog_paths(loc) -> list[Path]:
    folder = loc.catalog_dir("docs")
    return sorted(folder.glob(f"*.{loc.code}.md"))


# ---------------------------------------------------------------------------
# the locale decision
# ---------------------------------------------------------------------------


def test_tamang_is_declared_separately_from_nepali() -> None:
    assert TAJ.code == "taj" and TAJ.tag == "taj-Deva"
    assert TAJ.script == "devanagari"
    assert TAJ.confirmed is False, "the variety/script must stay unconfirmed until the trainees say"
    assert "Eastern" in TAJ.variety and "tdg" in TAJ.variety
    nepali = LOCALES["ne"]
    assert nepali.code == "ne" and nepali.script == "romanized"
    assert nepali.learner_facing is False, "Nepali is legacy/rollback material, not classroom text"
    assert TAJ.catalog_root != nepali.catalog_root


def test_every_notebook_has_a_tamang_catalog() -> None:
    notebooks = sorted(path.stem for path in course_notebooks(ROOT / "notebooks"))
    assert len(notebooks) == 16
    assert sorted(path.name[: -len(".taj.md")] for path in catalog_paths(TAJ)) == notebooks


DAY5 = ("Day05_01_Anomaly_Detection_Concepts", "Day05_02_PatchCore_Training",
        "Day05_03_YOLO_vs_PatchCore")


def test_day5_is_translated_per_concept_and_days_1_4_per_cell() -> None:
    """Day 5 は概念単位、第 1〜4 日はセル単位 / Day 5 is unit-level; Days 1-4 stay cell-level."""
    report = coverage.run(TAJ)
    legacy = coverage.legacy.run()
    day5_units = sum(item["units"] for item in report["notebooks"]
                     if Path(item["path"]).stem in DAY5)
    legacy_units = sum(item["counts"]["pending"] + item["counts"]["approved"]
                       + item["counts"]["draft"] + item["counts"]["missing"]
                       for item in report["notebooks"] if Path(item["path"]).stem not in DAY5)
    assert day5_units > 3 * sum(1 for item in report["notebooks"]
                                if Path(item["path"]).stem in DAY5), "one unit per concept, not one per cell"
    assert legacy_units == sum(item["translated"] for item in legacy["notebooks"]
                               if Path(item["path"]).stem not in DAY5), \
        "Days 1-4 keep exactly the cells the legacy Nepali pass translated"
    totals = report["totals"]
    assert totals["pending"] == day5_units + legacy_units
    assert totals["missing"] == 0, "every required unit is pending, apart from exempt cells"
    assert totals["approved"] == 0 and totals["draft"] == 0
    day5_exempt = sum(item["counts"]["exempt"] for item in report["notebooks"]
                      if Path(item["path"]).stem in DAY5)
    assert totals["exempt"] == legacy["totals"]["exempt"] + day5_exempt


def test_every_day5_concept_slot_is_recorded_as_pending() -> None:
    """承認済みのタマン語はまだ無い / no Day 5 concept carries Tamang text yet."""
    for stem in DAY5:
        path, = course_notebooks(ROOT / "notebooks", stem + ".ipynb")
        notebook = json.loads(path.read_text(encoding="utf-8"))
        catalog = coverage.catalogue_path(TAJ, stem)
        pending = {line.strip().rsplit(" | ", 1)[0].split(":", 1)[1].strip()
                   for line in catalog.read_text(encoding="utf-8").splitlines()
                   if line.strip().startswith("<!-- taj-pending:")}
        for cell in notebook["cells"]:
            if cell["cell_type"] != "markdown":
                continue
            source = "".join(cell["source"])
            for anchor in apply_translations.unit_anchors(source, TAJ):
                assert f"{cell['id']}/{anchor}" in pending, (stem, cell["id"], anchor)
            assert "taj:begin" not in source, "no Tamang text may be inserted yet"


def test_every_learner_document_has_a_tamang_catalog() -> None:
    documents = coverage.DOCUMENTS
    assert len(documents) == 12
    assert len({coverage.doc_catalog_stem(name) for name in documents}) == 12, \
        "two documents must never share one catalog file"
    expected = {coverage.doc_catalog_stem(name) for name in documents}
    actual = {path.name[: -len(".taj.md")] for path in doc_catalog_paths(TAJ)}
    assert actual == expected


@pytest.mark.parametrize("path", doc_catalog_paths(TAJ), ids=lambda p: p.stem)
def test_document_catalog_records_its_provenance(path: Path) -> None:
    metadata = apply_translations.catalog_metadata(path)
    assert metadata["locale"] == "taj"
    assert metadata["bcp47"] == "taj-Deva"
    assert metadata["review"] == "pending-native-review"
    assert metadata["provenance"], "a catalog must say where its text came from"


@pytest.mark.parametrize("path", catalog_paths(TAJ), ids=lambda p: p.stem)
def test_notebook_catalog_records_its_provenance(path: Path) -> None:
    metadata = apply_translations.catalog_metadata(path)
    assert metadata["locale"] == "taj"
    assert metadata["review"] == "pending-native-review"
    assert metadata["provenance"]


# ---------------------------------------------------------------------------
# the inventory: pending set == the legacy translated set
# ---------------------------------------------------------------------------


def test_the_pending_inventory_covers_every_cell_the_nepali_pass_translated() -> None:
    """第 1〜4 日の在庫はネパール語の対象セルと一致する / Days 1-4 still match the Nepali pass."""
    report = coverage.run(TAJ)
    nepali = coverage.legacy.run()
    days_1_4 = [item for item in nepali["notebooks"] if Path(item["path"]).stem not in DAY5]
    nepali_translated = sum(item["translated"] for item in days_1_4)
    tamang_days = [item for item in report["notebooks"] if Path(item["path"]).stem not in DAY5]
    assert sum(item["counts"]["pending"] for item in tamang_days) == nepali_translated
    assert sum(item["counts"]["missing"] for item in tamang_days) == 0


def test_the_document_inventory_counts_every_current_section() -> None:
    report = coverage.run(TAJ)
    assert report["document_totals"]["missing"] == 0
    assert report["document_totals"]["pending"] == sum(
        item["required_sections"] for item in report["documents"])


# ---------------------------------------------------------------------------
# the insertion tools: marker-aware, idempotent, and strict about the script
# ---------------------------------------------------------------------------


def _catalog(tmp_path: Path, body: str, name: str = "sample.taj.md") -> Path:
    path = tmp_path / name
    path.write_text(body, encoding="utf-8")
    return path


@pytest.mark.parametrize("text", ["This is English text copied into the Tamang catalog.",
                                  "This is English with Devanagari punctuation।"])
def test_a_tamang_block_must_be_devanagari(tmp_path, text) -> None:
    latin = _catalog(tmp_path, "<!-- taj-cell: abc -->\n"
                              f"{text}\n")
    with pytest.raises(apply_translations.CatalogError, match="must be written in Devanagari"):
        apply_translations.parse_catalog(latin, TAJ)


def test_an_empty_block_is_refused(tmp_path) -> None:
    empty = _catalog(tmp_path, "<!-- taj-cell: abc -->\n\n")
    with pytest.raises(apply_translations.CatalogError, match="empty"):
        apply_translations.parse_catalog(empty, TAJ)


def test_insertion_is_idempotent_and_keeps_the_source_text(tmp_path) -> None:
    catalog = _catalog(tmp_path, "<!-- taj-cell: abc -->\nतामाङ भाषा\n")
    entries = apply_translations.parse_catalog(catalog, TAJ)
    source = "# 見出し / Heading\n\n日本語の本文です。\n\nThe English body.\n"

    once = apply_translations.apply_blocks(source, entries["abc"], TAJ)
    twice = apply_translations.apply_blocks(once, entries["abc"], TAJ)
    assert once == twice
    assert apply_translations.strip_regions(once, TAJ).strip() == source.strip()
    assert "<!-- taj:begin end -->" in once and "तामाङ भाषा" in once
    assert "日本語の本文です。" in once and "The English body." in once


def test_nepali_and_tamang_regions_do_not_collide(tmp_path) -> None:
    """The legacy ne region stays inert while taj is inserted, so a rollback is possible."""
    source = "# 見出し / Heading\n"
    nepali = apply_translations.apply_blocks(
        source, [{"at": "after-heading", "text": "नेपाली पाठ"}], locale("ne"))
    assert "<!-- ne:begin after-heading -->" in nepali

    tamang = apply_translations.apply_blocks(
        nepali, [{"at": "after-heading", "text": "तामाङ पाठ"}], TAJ)
    assert "<!-- taj:begin after-heading -->" in tamang
    assert "<!-- ne:begin after-heading -->" in tamang, "taj must not rewrite the ne region"
    # removing the taj region leaves the legacy region alone
    without_taj = apply_translations.strip_regions(tamang, TAJ)
    assert "<!-- ne:begin after-heading -->" in without_taj
    assert without_taj.count("नेपाली पाठ") == 1
    assert "तामाङ पाठ" not in without_taj


def test_concept_anchors_are_discovered_in_source_order() -> None:
    source = ("#### 見出し / Heading\n\n日本語。\n\n<!-- taj-unit: heading -->\n\n"
              "| 項目<br>Item | 説明<br>Explanation |\n| --- | --- |\n"
              "| しきい値<br>threshold | 説明 <!-- taj-row: threshold --> |\n")
    assert apply_translations.unit_anchors(source, TAJ) == ["unit:heading", "row:threshold"]
    with pytest.raises(apply_translations.CatalogError, match="duplicate"):
        apply_translations.unit_anchors(source + "\n<!-- taj-unit: heading -->\n", TAJ)


def test_a_concept_block_lands_under_its_own_anchor() -> None:
    source = ("#### 第一 / First\n\n日本語の説明。\n\nEnglish explanation.\n\n"
              "<!-- taj-unit: first -->\n\n#### 第二 / Second\n\n次の説明。\n\nSecond explanation.\n\n"
              "<!-- taj-unit: second -->\n")
    blocks = [{"at": "unit:second", "text": "तामाङ दोस्रो।"}]
    once = apply_translations.apply_blocks(source, blocks, TAJ)
    twice = apply_translations.apply_blocks(once, blocks, TAJ)
    assert once == twice
    assert once.index("तामाङ दोस्रो।") > once.index("Second explanation.")
    assert once.index("तामाङ दोस्रो।") < once.index("<!-- taj-unit: second -->") + 200
    assert "taj-unit: first" in once and "तामाङ दोस्रो।" not in once.split("#### 第二")[0]
    assert apply_translations.strip_regions(once, TAJ).strip() == source.strip()


def test_a_table_row_concept_stays_inside_its_row() -> None:
    source = ("| 項目<br>Item | 説明<br>Explanation |\n| --- | --- |\n"
              "| 低い<br>low | 説明<br>explanation <!-- taj-row: low --> |\n"
              "| 高い<br>high | 説明<br>explanation <!-- taj-row: high --> |\n")
    blocks = [{"at": "row:low", "text": "तामाङ व्याख्या।"}]
    once = apply_translations.apply_blocks(source, blocks, TAJ)
    twice = apply_translations.apply_blocks(once, blocks, TAJ)
    assert once == twice, "a second run must not duplicate the row text"
    low_row, high_row = [line for line in once.splitlines() if line.startswith("| ")][-2:]
    assert "तामाङ व्याख्या।" in low_row and "तामाङ व्याख्या।" not in high_row
    assert once.count("तामाङ व्याख्या।") == 1
    assert apply_translations.strip_regions(once, TAJ).strip() == source.strip()


def test_a_catalog_anchor_that_no_longer_exists_is_refused() -> None:
    source = "#### 見出し / Heading\n\n説明。\n\n<!-- taj-unit: heading -->\n"
    with pytest.raises(apply_translations.CatalogError, match="does not exist"):
        apply_translations.apply_blocks(
            source, [{"at": "unit:renamed-heading", "text": "तामाङ"}], TAJ)


def test_reapplying_a_catalog_updates_instead_of_duplicating() -> None:
    source = "#### 見出し / Heading\n\n説明。\n\n<!-- taj-unit: heading -->\n"
    once = apply_translations.apply_blocks(source, [{"at": "unit:heading", "text": "एक"}], TAJ)
    twice = apply_translations.apply_blocks(once, [{"at": "unit:heading", "text": "दुई"}], TAJ)
    assert "एक" not in twice and twice.count("दुई") == 1
    assert apply_translations.strip_regions(twice, TAJ).strip() == source.strip()


def test_an_empty_day5_unit_stays_empty_while_it_is_pending() -> None:
    """未承認の単位は何も差し込まない / a pending unit inserts nothing."""
    path, = course_notebooks(ROOT / "notebooks", "Day05_01_Anomaly_Detection_Concepts.ipynb")
    notebook = json.loads(path.read_text(encoding="utf-8"))
    catalog = coverage.catalogue_path(TAJ, path.stem)
    entries = apply_translations.parse_catalog(catalog, TAJ) if catalog.is_file() else {}
    for cell in notebook["cells"]:
        if cell["cell_type"] != "markdown":
            continue
        source = "".join(cell["source"])
        assert entries.get(cell["id"]) is None, "every Day 5 unit is still pending"
        assert apply_translations.apply_blocks(source, [], TAJ) == source


@pytest.mark.parametrize("stem", DAY5)
def test_a_synthetic_approved_catalog_reaches_every_day5_unit(stem) -> None:
    """承認済みの合成カタログが、すべての単位に一度ずつ入る / idempotent per concept."""
    squeeze = lambda text: [line for line in text.splitlines() if line.strip()]  # noqa: E731
    path, = course_notebooks(ROOT / "notebooks", stem + ".ipynb")
    notebook = json.loads(path.read_text(encoding="utf-8"))
    inserted = 0
    for cell in notebook["cells"]:
        if cell["cell_type"] != "markdown":
            continue
        source = "".join(cell["source"])
        anchors = apply_translations.unit_anchors(source, TAJ)
        if not anchors:
            continue
        blocks = [{"at": anchor, "text": f"तामाङ पाठ {index + 1} अन्त।"}
                  for index, anchor in enumerate(anchors)]
        once = apply_translations.apply_blocks(source, blocks, TAJ)
        twice = apply_translations.apply_blocks(once, blocks, TAJ)
        assert once == twice, (stem, cell["id"])
        assert squeeze(apply_translations.strip_regions(once, TAJ)) == squeeze(source)
        for index, anchor in enumerate(anchors):
            marker = f"तामाङ पाठ {index + 1} अन्त।"
            assert once.count(marker) == 1, (stem, cell["id"], anchor)
        inserted += len(anchors)
    assert inserted > 40, f"{stem}: only {inserted} concept slots found"


def test_document_blocks_are_marker_aware(tmp_path) -> None:
    document = tmp_path / "doc.taj.md"
    document.write_text("<!-- taj-doc: README.md -->\n"
                        "<!-- taj-section: ## 2. Setup -->\nतामाङ पाठ\n", encoding="utf-8")
    target, blocks = apply_docs.parse_catalog(document, TAJ)
    assert target == "README.md"
    (heading,) = blocks
    once = apply_docs.apply_blocks("## 2. Setup\n\nbody\n\n## 3. Next\n", blocks, TAJ)
    twice = apply_docs.apply_blocks(once, blocks, TAJ)
    assert once == twice
    restored = apply_docs.strip_regions(once, TAJ)
    assert "तामाङ पाठ" not in restored
    squeeze = lambda text: [line for line in text.splitlines() if line.strip()]  # noqa: E731
    assert squeeze(restored) == squeeze("## 2. Setup\n\nbody\n\n## 3. Next\n")


def test_document_pending_lines_are_keyed_by_heading(tmp_path) -> None:
    document = tmp_path / "doc.taj.md"
    document.write_text("<!-- taj-doc: README.md -->\n"
                        "<!-- taj-pending: ## 2. Setup | no reviewer yet -->\n", encoding="utf-8")
    assert apply_docs.parse_pending(document, TAJ) == {"## 2. Setup": "no reviewer yet"}


def review_header(loc) -> str:
    """Synthetic provenance, written only to pytest's temporary catalogs."""
    return (f"<!--\nlocale: {loc.code}\nbcp47: {loc.tag}\nscript: {loc.script}\n"
            f"variety: {loc.variety}\nreview: approved\nreviewer: Fixture reviewer\n"
            "provenance: Rendering fixture review record 1\nreviewed-on: 2020-01-01\n-->\n")


@pytest.fixture
def temporary_document(tmp_path, monkeypatch):
    source = tmp_path / "example.md"
    source.write_text("# First / 最初\n\nSource English and 日本語.\n\n"
                      "```python\n# Not an anchor\n```\n\n"
                      "## Unreviewed\n\nKeep me.\n\n## Waiting\n\n## Omitted\n\n"
                      "## Separator\n\n<!-- localization-exempt -->\n", encoding="utf-8")
    catalog = tmp_path / "example.taj.md"
    monkeypatch.setattr(coverage, "COURSE_ROOT", tmp_path)
    monkeypatch.setattr(coverage, "doc_catalogue_path", lambda *_: catalog)
    monkeypatch.setattr(apply_docs, "COURSE_ROOT", tmp_path)
    catalog.write_text(review_header(TAJ) + "<!-- taj-doc: example.md -->\n"
                       "<!-- taj-section: # First / 最初 -->\nतामाङ\n"
                       "<!-- taj-status: # First / 最初 | approved -->\n"
                       "<!-- taj-section: ## Unreviewed -->\nतामाङ\n"
                       "<!-- taj-pending: ## Waiting | no review -->\n", encoding="utf-8")
    return source, catalog


def test_document_approval_is_per_section_and_requires_the_inserted_text(temporary_document):
    source, catalog = temporary_document
    before = coverage.classify_document(source.name, TAJ)
    assert before["sections"]["# First / 最初"]["status"] == "missing"
    assert apply_docs.apply_catalog(catalog, True, TAJ)["changed"]
    assert not apply_docs.apply_catalog(catalog, True, TAJ)["changed"]
    report = coverage.classify_document(source.name, TAJ)
    assert report["counts"] == dict(approved=1, draft=1, pending=1, missing=1, exempt=1)
    assert report["issues"] == []
    assert "Source English and 日本語." in source.read_text(encoding="utf-8")


@pytest.mark.parametrize(("mutation", "message"), [
    ("unknown", "stale or unknown"),
    ("stale", "stale inserted"),
    ("duplicate", "two blocks"),
    ("duplicate-region", "duplicate taj document region"),
    ("script", "written in Devanagari"),
    ("reviewer", "human review provenance"),
    ("provenance", "human review provenance"),
    ("target", "expected 'example.md'"),
])
def test_document_coverage_blocks_invalid_approval(temporary_document, mutation, message):
    source, catalog = temporary_document
    apply_docs.apply_catalog(catalog, True, TAJ)
    text = catalog.read_text(encoding="utf-8")
    if mutation == "unknown":
        text += "<!-- taj-pending: ## Old heading | renamed -->\n"
    elif mutation == "stale":
        source.write_text(source.read_text(encoding="utf-8").replace("## Unreviewed", "## Renamed"),
                          encoding="utf-8")
    elif mutation == "duplicate":
        text += "<!-- taj-section: ## Unreviewed -->\nतामाङ\n"
    elif mutation == "duplicate-region":
        document = source.read_text(encoding="utf-8")
        region = TAJ.doc_region_re().search(document).group()
        source.write_text(document + region, encoding="utf-8")
    elif mutation == "script":
        text = text.replace("तामाङ", "copied English")
    elif mutation == "reviewer":
        text = text.replace("reviewer: Fixture reviewer\n", "")
    elif mutation == "provenance":
        text = text.replace("provenance: Rendering fixture review record 1", "provenance: none")
    else:
        text = text.replace("taj-doc: example.md", "taj-doc: wrong.md")
    catalog.write_text(text, encoding="utf-8")
    report = coverage.classify_document(source.name, TAJ)
    assert any(message in issue for issue in report["issues"])


def test_notebook_approval_requires_live_catalog_cells_and_figure_anchors(tmp_path, monkeypatch):
    source = tmp_path / "figure.ipynb"
    original = "![Diagram](figure.png)\n\n日本語。\n\nThe English text.\n"
    translation = {"at": "after-image:figure.png", "text": "तामाङ"}
    inserted = apply_translations.apply_blocks(original, [translation], TAJ)
    cell = {"cell_type": "markdown", "id": "diagram", "source": inserted}

    def write_cell(text):
        source.write_text(json.dumps({"cells": [dict(cell, source=text)]}), encoding="utf-8")

    write_cell(inserted)
    catalog = _catalog(tmp_path, review_header(TAJ)
                       + "<!-- taj-cell: diagram | after-image:figure.png -->\n"
                       + "तामाङ\n<!-- taj-status: diagram approved -->\n")
    monkeypatch.setattr(coverage, "COURSE_ROOT", tmp_path)
    monkeypatch.setattr(coverage, "catalogue_path", lambda *_: catalog)
    good = coverage.classify_notebook(source, TAJ)
    assert good["cells"]["diagram"]["status"] == "approved"
    assert not good["issues"]

    write_cell(inserted.replace("](figure.png)", "](renamed.png)"))
    stale = coverage.classify_notebook(source, TAJ)
    assert any("expected one image, found 0" in issue for issue in stale["issues"])

    write_cell(inserted)
    with catalog.open("a", encoding="utf-8") as handle:
        handle.write("<!-- taj-pending: deleted-cell | pending -->\n")
    unknown = coverage.classify_notebook(source, TAJ)
    assert any("stale or unknown" in issue and "deleted-cell" in issue
               for issue in unknown["issues"])


# ---------------------------------------------------------------------------
# the production gate
# ---------------------------------------------------------------------------


def _report(**totals) -> dict:
    base = {"approved": 0, "draft": 0, "pending": 0, "missing": 0, "exempt": 0}
    base.update(totals)
    return {"totals": base, "document_totals": dict(base),
            "catalog_reviews": ["pending-native-review"]}


def test_the_gate_blocks_a_pending_catalog() -> None:
    failures = coverage.gate_failures(_report(pending=656), TAJ)
    assert any("pending" in failure for failure in failures)


def test_the_gate_blocks_a_machine_draft_even_when_every_block_has_text() -> None:
    failures = coverage.gate_failures(_report(draft=656), TAJ)
    assert any("unapproved draft" in failure for failure in failures)


def test_the_gate_blocks_an_unconfirmed_variety_even_if_a_translator_approved_everything() -> None:
    report = _report(approved=656)
    report["catalog_reviews"] = ["approved"]
    report["document_totals"] = {"approved": 154, "draft": 0, "pending": 0, "missing": 0,
                                 "exempt": 0}
    assert any("unconfirmed" in failure for failure in coverage.gate_failures(report, TAJ))


def test_the_gate_passes_only_when_everything_is_approved_and_the_variety_is_confirmed() -> None:
    from dataclasses import replace

    confirmed = replace(TAJ, confirmed=True)
    report = _report(approved=656)
    report["catalog_reviews"] = ["approved"]
    report["document_totals"] = {"approved": 154, "draft": 0, "pending": 0, "missing": 0,
                                 "exempt": 0}
    assert coverage.gate_failures(report, confirmed) == []


def test_the_repository_gate_is_blocked_today() -> None:
    assert coverage.main(["--locale", "taj", "--strict"]) == 1


def test_the_nepali_coverage_tool_still_reports_the_legacy_material() -> None:
    assert coverage.main(["--locale", "ne"]) == 0


def test_the_inventory_file_matches_a_fresh_run() -> None:
    inventory = ROOT / "assets" / "i18n" / "taj" / "coverage_inventory.json"
    if not inventory.is_file():
        pytest.skip("inventory not generated in this checkout")
    recorded = json.loads(inventory.read_text(encoding="utf-8"))
    fresh = coverage.run(TAJ)
    assert recorded["totals"] == fresh["totals"]
    assert recorded["document_totals"] == fresh["document_totals"]
