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
    report = coverage.run(TAJ)
    nepali = coverage.legacy.run()
    nepali_translated = sum(item["translated"] for item in nepali["notebooks"])
    totals = report["totals"]
    assert totals["pending"] == nepali_translated
    assert totals["missing"] == 0, "every required cell is pending, apart from exempt cells"
    assert totals["approved"] == 0 and totals["draft"] == 0
    assert totals["exempt"] == nepali["totals"]["exempt"]


def test_the_document_inventory_counts_every_legacy_section() -> None:
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


def test_a_tamang_block_must_be_devanagari(tmp_path) -> None:
    latin = _catalog(tmp_path, "<!-- taj-cell: abc -->\n"
                              "This is English text copied into the Tamang catalog.\n")
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
