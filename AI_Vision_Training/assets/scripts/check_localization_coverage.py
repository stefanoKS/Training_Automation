"""翻訳カバレッジの点検 / Report how much of each locale the course actually carries.

Five states are counted separately, per notebook cell and per document section:

``approved``
    A translated region exists **and** a reviewer signed that block off
    (``<!-- <locale>-status: <id> approved -->``).
``draft``
    A translated region exists but no reviewer approved it. Machine output is always a draft.
``pending``
    The catalog records the block as untranslated (``<!-- <locale>-pending: <id> | reason -->``)
    because no dependable translation could be produced. Nothing is invented to fill it.
``missing``
    A required block has neither a usable insertion nor a pending entry.
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
import re
import sys
from datetime import date
from pathlib import Path

import check_nepali_coverage as legacy
import apply_docs
import apply_translations
from apply_translations import catalog_metadata, parse_catalog, parse_pending
from course_notebooks import course_notebooks
from i18n_locales import DEVANAGARI_RE, LEGACY_REGION_RE, Locale, locale as get_locale, without_legacy

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


def directives(path: Path, pattern: re.Pattern) -> dict[str, str]:
    values = {}
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            match = pattern.fullmatch(line.strip())
            if match:
                key, value = match.groups()
                if key in values:
                    raise apply_translations.CatalogError(
                        f"{path.name}: duplicate directive for {key!r}")
                values[key] = value or ""
    return values


def has_review(metadata: dict[str, str], loc: Locale) -> bool:
    def identified(value: str) -> bool:
        return bool(any(character.isalpha() for character in value) and not re.match(
            r"(?i)^[\s(]*(?:none|unknown|pending|n/?a|tbd|todo|unreviewed|anonymous|placeholder|"
            r"machine|ai-generated)\b", value))

    try:
        reviewed_on = date.fromisoformat(metadata.get("reviewed-on", ""))
    except ValueError:
        return False
    return (reviewed_on <= date.today()
            and metadata.get("review") == "approved"
            and metadata.get("locale") == loc.code and metadata.get("bcp47") == loc.tag
            and metadata.get("script") == loc.script and metadata.get("variety") == loc.variety
            and identified(metadata.get("reviewer", ""))
            and identified(metadata.get("provenance", "")))


def catalog_errors(keys, entries, pending, claimed) -> list[str]:
    issues = []
    unknown = (entries.keys() | pending.keys() | claimed.keys()) - keys
    if unknown:
        issues.append(f"stale or unknown catalog keys: {sorted(unknown)}")
    conflict = pending.keys() & (entries.keys() | claimed.keys())
    if conflict:
        issues.append(f"pending entries conflict with text or review: {sorted(conflict)}")
    without_text = claimed.keys() - entries.keys()
    if without_text:
        issues.append(f"review status without catalog text: {sorted(without_text)}")
    return issues


def outside_errors(text: str, loc: Locale) -> list[str]:
    issues = []
    if marker_remains(text, loc):
        issues.append("unmatched or nested translation markers")
    if DEVANAGARI_RE.search(text):
        issues.append("untracked Devanagari outside a translation region")
    return issues


def marker_remains(text: str, loc: Locale) -> bool:
    return bool(re.search(r"<!--\s*(?:" + re.escape(loc.code) + r"|ne):(?:begin|end)\b", text))


def classify_notebook(path: Path, loc: Locale) -> dict:
    catalog = catalogue_path(loc, path.stem)
    entries, pending, claimed, metadata = {}, {}, {}, {}
    issues = []
    try:
        entries = parse_catalog(catalog, loc) if catalog.is_file() else {}
        pending = directives(catalog, loc.pending_directive_re())
        claimed = directives(catalog, loc.status_directive_re())
        metadata = catalog_metadata(catalog)
    except apply_translations.CatalogError as error:
        issues.append(str(error))
    notebook = json.loads(path.read_text(encoding="utf-8"))
    review = has_review(metadata, loc)
    report = {"path": path.relative_to(COURSE_ROOT).as_posix(), "catalog": catalog.name,
              "cells": {}, "counts": {label: 0 for label in STATUS_LABELS},
              "translated_ids": sorted(entries), "review": metadata.get("review", ""),
              "issues": issues}
    for cell in notebook["cells"]:
        if cell["cell_type"] != "markdown":
            continue
        cell_id = cell.get("id") or ""
        source = "".join(cell.get("source", []))
        if not cell_id or cell_id in report["cells"]:
            issues.append(f"missing or duplicate markdown cell ID: {cell_id!r}")
        source = without_legacy(source)
        outside = loc.region_re().sub("", source)
        cell_issues = outside_errors(outside, loc)
        bodies = {}
        wanted = {block["at"]: block["text"] for block in entries.get(cell_id, [])}
        try:
            regions = apply_translations.parse_regions(source, loc)
            bodies = {anchor: region["body"] for anchor, region in regions.items()}
            for anchor, body in bodies.items():
                apply_translations.validate_block(loc, body, f"cell {cell_id}, {anchor}")
                if marker_remains(body, loc):
                    cell_issues.append(f"{anchor}: nested translation markers")
            for anchor, body in wanted.items():
                if anchor != "end":
                    apply_translations.apply_blocks(outside, [{"at": anchor, "text": body}], loc)
        except apply_translations.CatalogError as error:
            cell_issues.append(str(error))
        if bodies != wanted:
            cell_issues.append("inserted translation anchors or content differ from the catalog")
        if claimed.get(cell_id) == "approved" and not review:
            cell_issues.append("approved claim lacks matching human review provenance")
        issues.extend(f"{cell_id}: {issue}" for issue in cell_issues)
        if bodies:
            status = "approved" if claimed.get(cell_id) == "approved" and review and not cell_issues else "draft"
        elif legacy.is_exempt(outside) and cell_id not in (entries.keys() | pending.keys()):
            status = "exempt"
        elif cell_id in pending:
            status = "pending"
        else:
            status = "missing"
        report["cells"][cell_id] = {"status": status, "chars": sum(len(b) for b in bodies.values()),
                                    "reason": pending.get(cell_id, "")}
        report["counts"][status] += 1
    issues.extend(catalog_errors(report["cells"].keys(), entries, pending, claimed))
    return report


def document_source(text: str, loc: Locale) -> str:
    blank = lambda match: "\n" * match.group().count("\n")
    return loc.doc_region_re().sub(blank, LEGACY_REGION_RE.sub(blank, text))


def document_sections(source: str) -> dict[str, tuple[int, int, bool]]:
    lines = source.split("\n")
    headings = apply_docs.section_anchors(lines)
    sections = {}
    for (start, heading), (end, _) in zip(headings, headings[1:] + [(len(lines), "")]):
        if heading in sections:
            raise apply_docs.CatalogError(f"duplicate document heading {heading!r}")
        body = "\n".join(lines[start + 1:end]).strip()
        # Exemptions are owned by the source, not claimed by a translation catalog.
        sections[heading] = (start, end, body == "<!-- localization-exempt -->")
    return sections


def classify_document(rel_path: str, loc: Locale) -> dict:
    path = COURSE_ROOT / rel_path
    catalog = doc_catalogue_path(loc, rel_path)
    entries, pending, claimed, metadata, sections, regions = {}, {}, {}, {}, {}, {}
    issues = []
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    text = without_legacy(text)
    source = document_source(text, loc)
    issues.extend(outside_errors(source, loc))
    try:
        sections = document_sections(source)
        if catalog.is_file():
            target, entries = apply_docs.parse_catalog(catalog, loc)
            if target != rel_path:
                issues.append(f"catalog target is {target!r}, expected {rel_path!r}")
            pending = directives(catalog, loc.doc_pending_directive_re())
            claimed = directives(catalog, loc.doc_status_directive_re())
            metadata = catalog_metadata(catalog)
        regions = apply_docs.region_spans(text, loc)
    except (apply_docs.CatalogError, apply_translations.CatalogError) as error:
        issues.append(str(error))
    review = has_review(metadata, loc)
    issues.extend(catalog_errors(sections.keys(), entries, pending, claimed))
    unknown = regions.keys() - {apply_docs.slug_of(heading) for heading in sections}
    if unknown:
        issues.append(f"stale inserted document anchors: {sorted(unknown)}")
    report = {"path": rel_path, "exists": path.is_file(), "regions": len(regions),
              "catalog": catalog.name, "chars": 0, "required_sections": 0,
              "sections": {}, "issues": issues, "review": metadata.get("review", ""),
              "pending": 0, "untranslated": [], "counts": {label: 0 for label in STATUS_LABELS}}
    if not sections:
        report["counts"]["missing"] = 1
        issues.append("source has no addressable sections")
    for heading, (start_line, end_line, exempt) in sections.items():
        span = regions.get(apply_docs.slug_of(heading))
        body = text[span[1]:span[2]] if span else ""
        status = "missing"
        if span:
            line = text.count("\n", 0, span[0]) + 1
            wanted = "\n".join(entries.get(heading, [])).strip("\n")
            correct = (start_line < line < end_line and bool(wanted) and wanted == body
                       and not marker_remains(body, loc))
            if not correct:
                issues.append(f"{heading}: inserted block is misplaced or differs from catalog")
            status = ("approved" if correct and claimed.get(heading) == "approved" and review
                      else "draft")
        elif heading in pending:
            status = "pending"
        elif exempt and heading not in entries:
            status = "exempt"
        if claimed.get(heading) == "approved" and not review:
            issues.append(f"{heading}: approved claim lacks matching human review provenance")
        report["sections"][heading] = {"status": status, "chars": len(body),
                                       "reason": pending.get(heading, "")}
        report["counts"][status] += 1
        report["chars"] += len(body)
        report["required_sections"] += status != "exempt"
        report["pending"] += status == "pending"
        if status == "missing":
            report["untranslated"].append(heading)
    return report


def run(loc: Locale) -> dict:
    notebooks = [classify_notebook(path, loc)
                 for path in course_notebooks(COURSE_ROOT / "notebooks")]
    documents = [classify_document(rel, loc) for rel in DOCUMENTS]
    items = notebooks + documents
    reviews = {item["review"] for item in items if item["review"]}
    issues = [f"{item['path']}: {issue}" for item in items for issue in item["issues"]]
    for kind, group in (("notebooks", notebooks), ("docs", documents)):
        expected = {item["catalog"] for item in group}
        actual = {path.name for path in loc.catalog_dir(kind).glob(f"*.{loc.code}.md")}
        issues.extend(f"unknown {kind} catalog: {name}" for name in sorted(actual - expected))
    totals = {label: sum(item["counts"][label] for item in notebooks) for label in STATUS_LABELS}
    doc_totals = {label: sum(item["counts"][label] for item in documents) for label in STATUS_LABELS}
    return {
        "locale": {"code": loc.code, "tag": loc.tag, "label": loc.label, "script": loc.script,
                   "confirmed": loc.confirmed, "variety": loc.variety,
                   "learner_facing": loc.learner_facing},
        "notebooks": notebooks,
        "documents": documents,
        "catalog_reviews": sorted(reviews),
        "issues": issues,
        "totals": totals,
        "document_totals": doc_totals,
        "catalogs_present": sum(1 for item in notebooks
                                if catalogue_path(loc, Path(item["path"]).stem).is_file()),
    }


def gate_failures(report: dict, loc: Locale) -> list[str]:
    """本番ゲート / why the production gate must fail (empty list = pass)."""
    failures = []
    failures.extend(report.get("issues", []))
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
        if translated or catalog_metadata(catalog).get("review") == "approved":
            continue
        pending_now = parse_pending(catalog, loc) if catalog.is_file() else {}
        for cell in notebook["cells"]:
            if cell["cell_type"] != "markdown":
                continue
            cell_id = cell.get("id") or ""
            source = "".join(cell.get("source", []))
            if loc.region_re().search(source) or cell_id in translated:
                continue
            if legacy.is_exempt(without_legacy(loc.region_re().sub("", source))):
                continue
            # 既存の pending はそのまま残す（理由つきで書き直さない）
            # Keep an existing pending entry, including its reason, instead of dropping it.
            reason = pending_now.get(cell_id, PENDING_REASON)
            lines.append(f"<!-- {loc.code}-pending: {cell_id} | {reason} -->")
        text = "\n".join(lines).rstrip() + "\n"
        if text != existing:
            written.append(str(catalog))
            if write:
                catalog.parent.mkdir(parents=True, exist_ok=True)
                catalog.write_text(text, encoding="utf-8")
    return written


def emit_pending_doc_catalogs(loc: Locale, write: bool) -> list[str]:
    """文書カタログも同じ方針で作る / record every required document section as pending."""
    written = []
    for rel in DOCUMENTS:
        catalog = doc_catalogue_path(loc, rel)
        path = COURSE_ROOT / rel
        if not path.is_file():
            continue
        required = sorted(heading for heading, (_, _, exempt) in document_sections(
            document_source(path.read_text(encoding="utf-8"), loc)).items() if not exempt)
        existing = catalog.read_text(encoding="utf-8") if catalog.is_file() else ""
        if catalog.is_file():
            _, translated = apply_docs.parse_catalog(catalog, loc)
            if translated or catalog_metadata(catalog).get("review") == "approved":
                continue
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
            written.append(str(catalog))
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
