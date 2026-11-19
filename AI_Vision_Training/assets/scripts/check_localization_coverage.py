"""翻訳カバレッジの点検 / Report how much of each locale the course actually carries.

Four states are counted separately, per notebook cell and per document section:

``approved``
    A translated region exists **and** a reviewer signed that block off
    (``<!-- <locale>-status: <id> approved -->``).
``draft``
    A translated region exists but no reviewer approved it. Machine output is always a draft.
``pending``
    The catalog records the block as untranslated (``<!-- <locale>-pending: <id> | reason -->``)
    because no dependable translation could be produced. Nothing is invented to fill it.
``exempt``
    The cell deliberately stays untranslated: separators, empty scaffolding, "write your code here"
    placeholders.

``--strict`` is the production gate: it fails while any required block is draft or pending, while the
catalog's own provenance says it is unreviewed, or while the locale's variety is unconfirmed. A
machine translation can therefore never open the gate by itself.

Script detection is **not** language verification. ``approved`` records a human decision, not a
script test.

使い方 / Usage
--------------
    python assets\\scripts\\check_localization_coverage.py --locale taj
    python assets\\scripts\\check_localization_coverage.py --locale taj --strict
    python assets\\scripts\\check_localization_coverage.py --locale taj --json --inventory out.json
    python assets\\scripts\\check_localization_coverage.py --locale taj --emit-pending-catalogs --write
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import check_nepali_coverage as legacy
import apply_docs
from apply_translations import catalog_metadata, parse_catalog, parse_pending, parse_status
from course_notebooks import course_notebooks
from i18n_locales import DEVANAGARI_RE, Locale, locale as get_locale

COURSE_ROOT = Path(__file__).resolve().parents[2]
DOCUMENTS = legacy.DOCUMENTS

PENDING_REASON = ("no dependable reference translation is available in this environment; "
                  "a native/advanced Tamang reviewer must supply and sign off the text")

STATUS_LABELS = ("approved", "draft", "pending", "missing", "exempt")


def catalogue_path(loc: Locale, stem: str) -> Path:
    return loc.catalog_dir("notebooks") / f"{stem}.{loc.code}.md"


def doc_catalogue_path(loc: Locale, name: str) -> Path:
    return loc.catalog_dir("docs") / f"{doc_catalog_stem(name)}.{loc.code}.md"


def doc_catalog_stem(rel_path: str) -> str:
    """文書カタログの名前 / a unique catalog name for a document.

    ``README.md`` and ``docs/pdf/README.md`` are different documents, so the folder has to be part of
    the name; otherwise one catalog would overwrite the other.
    """
    return "-".join(Path(rel_path).with_suffix("").parts)


def classify_notebook(path: Path, loc: Locale) -> dict:
    catalog = catalogue_path(loc, path.stem)
    entries = parse_catalog(catalog, loc) if catalog.is_file() else {}
    pending = parse_pending(catalog, loc)
    claimed = parse_status(catalog, loc)
    notebook = json.loads(path.read_text(encoding="utf-8"))
    report = {"path": path.relative_to(COURSE_ROOT).as_posix(), "catalog": catalog.name,
              "cells": {}, "counts": {label: 0 for label in STATUS_LABELS},
              "translated_ids": sorted(entries)}
    for cell in notebook["cells"]:
        if cell["cell_type"] != "markdown":
            continue
        cell_id = cell.get("id") or ""
        source = "".join(cell.get("source", []))
        outside = loc.region_re().sub("", source)
        bodies = [match.group("body") for match in loc.region_re().finditer(source)]
        if bodies:
            status = "approved" if claimed.get(cell_id) == "approved" else "draft"
        elif legacy.is_exempt(outside):
            status = "exempt"
        elif cell_id in pending:
            status = "pending"
        else:
            status = "missing"
        report["cells"][cell_id] = {"status": status, "chars": sum(len(b) for b in bodies),
                                    "reason": pending.get(cell_id, "")}
        report["counts"][status] += 1
    return report


def classify_document(rel_path: str, loc: Locale) -> dict:
    path = COURSE_ROOT / rel_path
    catalog = doc_catalogue_path(loc, rel_path)
    pending = apply_docs.parse_pending(catalog, loc) if catalog.is_file() else {}
    legacy_catalog = COURSE_ROOT / "assets" / "i18n" / "ne" / "docs" / f"{Path(rel_path).stem}.ne.md"
    required = (sorted(apply_docs.parse_catalog(legacy_catalog, get_locale("ne"))[1])
                if legacy_catalog.is_file() else [])
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    regions = [match.group("body") for match in loc.doc_region_re().finditer(text)]
    report = {"path": rel_path, "exists": path.is_file(), "regions": len(regions),
              "chars": sum(len(body) for body in regions), "required_sections": len(required),
              "pending": len([heading for heading in required if heading in pending]),
              "untranslated": sorted(heading for heading in required if heading not in pending),
              "counts": {label: 0 for label in STATUS_LABELS}}
    if not path.is_file():
        report["counts"]["missing"] = len(required) or 1
        return report
    status = "draft" if regions else ("pending" if pending else "missing")
    report["counts"][status] = len(required) or 1
    return report


def run(loc: Locale) -> dict:
    notebooks = [classify_notebook(path, loc)
                 for path in course_notebooks(COURSE_ROOT / "notebooks")]
    documents = [classify_document(rel, loc) for rel in DOCUMENTS]
    metadata = [catalog_metadata(catalogue_path(loc, Path(item["path"]).stem)) for item in notebooks]
    reviews = {item.get("review", "") for item in metadata}
    totals = {label: sum(item["counts"][label] for item in notebooks) for label in STATUS_LABELS}
    doc_totals = {label: sum(item["counts"][label] for item in documents) for label in STATUS_LABELS}
    return {
        "locale": {"code": loc.code, "tag": loc.tag, "label": loc.label, "script": loc.script,
                   "confirmed": loc.confirmed, "variety": loc.variety,
                   "learner_facing": loc.learner_facing},
        "notebooks": notebooks,
        "documents": documents,
        "catalog_reviews": sorted(reviews),
        "totals": totals,
        "document_totals": doc_totals,
        "catalogs_present": sum(1 for item in notebooks
                                if catalogue_path(loc, Path(item["path"]).stem).is_file()),
    }


def gate_failures(report: dict, loc: Locale) -> list[str]:
    """本番ゲート / why the production gate must fail (empty list = pass)."""
    failures = []
    totals = report["totals"]
    if totals["missing"]:
        failures.append(f"{totals['missing']} required notebook cells have no entry at all")
    if totals["pending"]:
        failures.append(f"{totals['pending']} notebook cells are recorded as pending")
    if totals["draft"]:
        failures.append(f"{totals['draft']} notebook cells hold an unapproved draft")
    if totals["approved"] == 0:
        failures.append("no notebook cell carries an approved translation")
    doc_totals = report["document_totals"]
    if doc_totals["draft"] or doc_totals["pending"] or doc_totals["missing"]:
        failures.append(f"document catalogs are not approved ({doc_totals})")
    if any(review != "approved" for review in report["catalog_reviews"]):
        failures.append("a catalog's provenance header is not marked review: approved")
    if not loc.confirmed:
        failures.append(f"the {loc.code} variety and script are unconfirmed "
                        f"({loc.variety})")
    return failures


def emit_pending_catalogs(loc: Locale, write: bool) -> list[str]:
    """未翻訳カタログを作る / write a catalog that records every required block as pending."""
    written = []
    for path in course_notebooks(COURSE_ROOT / "notebooks"):
        catalog = catalogue_path(loc, path.stem)
        notebook = json.loads(path.read_text(encoding="utf-8"))
        lines = [
            "<!--",
            f"locale: {loc.code}",
            f"bcp47: {loc.tag}",
            f"variety: {loc.variety}",
            f"script: {loc.script}",
            "provenance: none (no translation produced yet)",
            "review: pending-native-review",
            "reviewer: (none)",
            "note: every block below is recorded as pending. Nothing here has been translated, so",
            "note: nothing here can be mistaken for a finished translation; the production gate",
            "note: keeps failing until a Tamang reviewer supplies and approves the text.",
            "-->",
            f"# {path.stem} — {loc.label}",
            "",
        ]
        existing = catalog.read_text(encoding="utf-8") if catalog.is_file() else ""
        translated = set(parse_catalog(catalog, loc)) if catalog.is_file() else set()
        pending_now = parse_pending(catalog, loc) if catalog.is_file() else {}
        for cell in notebook["cells"]:
            if cell["cell_type"] != "markdown":
                continue
            cell_id = cell.get("id") or ""
            source = "".join(cell.get("source", []))
            if loc.region_re().search(source) or cell_id in translated:
                continue
            if legacy.is_exempt(loc.region_re().sub("", source)):
                continue
            # 既存の pending はそのまま残す（理由つきで書き直さない）
            # Keep an existing pending entry, including its reason, instead of dropping it.
            reason = pending_now.get(cell_id, PENDING_REASON)
            lines.append(f"<!-- {loc.code}-pending: {cell_id} | {reason} -->")
        text = "\n".join(lines).rstrip() + "\n"
        if text != existing:
            written.append(str(catalog.relative_to(COURSE_ROOT)))
            if write:
                catalog.parent.mkdir(parents=True, exist_ok=True)
                catalog.write_text(text, encoding="utf-8")
    return written


def emit_pending_doc_catalogs(loc: Locale, write: bool) -> list[str]:
    """文書カタログも同じ方針で作る / record every required document section as pending."""
    written = []
    for rel in DOCUMENTS:
        catalog = doc_catalogue_path(loc, rel)
        legacy_catalog = (COURSE_ROOT / "assets" / "i18n" / "ne" / "docs"
                          / f"{Path(rel).stem}.ne.md")
        if not legacy_catalog.is_file():
            continue
        required = sorted(apply_docs.parse_catalog(legacy_catalog, get_locale("ne"))[1])
        existing = catalog.read_text(encoding="utf-8") if catalog.is_file() else ""
        pending_now = apply_docs.parse_pending(catalog, loc) if catalog.is_file() else {}
        lines = [
            "<!--",
            f"locale: {loc.code}",
            f"bcp47: {loc.tag}",
            f"variety: {loc.variety}",
            f"script: {loc.script}",
            "provenance: none (no translation produced yet)",
            "review: pending-native-review",
            "reviewer: (none)",
            "note: every section below is recorded as pending; no text is supplied.",
            "-->",
            f"# {Path(rel).stem} — {loc.label}",
            "",
            f"<!-- {loc.code}-doc: {rel} -->",
            "",
        ]
        for heading in required:
            reason = pending_now.get(heading, PENDING_REASON)
            lines.append(f"<!-- {loc.code}-pending: {heading} | {reason} -->")
        text = "\n".join(lines).rstrip() + "\n"
        if text != existing:
            written.append(str(catalog.relative_to(COURSE_ROOT)))
            if write:
                catalog.parent.mkdir(parents=True, exist_ok=True)
                catalog.write_text(text, encoding="utf-8")
    return written


def print_report(report: dict, loc: Locale) -> None:
    print(f"[locale] {loc.code} ({loc.tag}) — {loc.label}")
    print(f"[locale] variety: {loc.variety}")
    print(f"[locale] confirmed: {loc.confirmed}  learner_facing: {loc.learner_facing}")
    for item in report["notebooks"]:
        counts = item["counts"]
        print(f"[nb]  {item['path']:<70} approved={counts['approved']:>3} "
              f"draft={counts['draft']:>3} pending={counts['pending']:>3} "
              f"exempt={counts['exempt']:>2} missing={counts['missing']:>3}")
    for item in report["documents"]:
        print(f"[doc] {item['path']:<70} regions={item['regions']:>2} "
              f"sections={item['required_sections']:>2} pending={item['pending']:>2}")
    totals = report["totals"]
    print(f"[done] notebooks: approved={totals['approved']} draft={totals['draft']} "
          f"pending={totals['pending']} missing={totals['missing']} exempt={totals['exempt']}")
    print(f"[done] documents: {report['document_totals']}")
    print(f"[done] catalog provenance reviews: {report['catalog_reviews']}")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Report one locale's coverage of the course.")
    parser.add_argument("--locale", default="taj", help="locale code (ne, taj)")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    parser.add_argument("--strict", action="store_true", help="production gate: fail unless approved")
    parser.add_argument("--inventory", default=None, help="write the inventory JSON here")
    parser.add_argument("--emit-pending-catalogs", action="store_true",
                        help="record every untranslated block as pending in the catalog")
    parser.add_argument("--write", action="store_true", help="write the generated catalogs")
    args = parser.parse_args(argv)

    if args.locale == "ne":
        if args.strict:
            return legacy.main(["--strict"])
        return legacy.main([])

    loc = get_locale(args.locale)
    if args.emit_pending_catalogs:
        written = emit_pending_catalogs(loc, args.write)
        written += emit_pending_doc_catalogs(loc, args.write)
        verb = "written" if args.write else "would be written"
        print(f"[catalogs] {len(written)} {verb}")
        for path in written:
            print(f"   {path}")

    report = run(loc)
    if args.inventory:
        Path(args.inventory).parent.mkdir(parents=True, exist_ok=True)
        Path(args.inventory).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                                        encoding="utf-8")
        print(f"[inventory] {args.inventory}")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_report(report, loc)

    failures = gate_failures(report, loc)
    if args.strict:
        if failures:
            print("[gate] BLOCKED — the production gate fails:")
            for reason in failures:
                print(f"   - {reason}")
            return 1
        print("[gate] PASS — every required block is approved")
        return 0
    if failures:
        print("[gate] not ready (run --strict for the production gate):")
        for reason in failures[:5]:
            print(f"   - {reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
