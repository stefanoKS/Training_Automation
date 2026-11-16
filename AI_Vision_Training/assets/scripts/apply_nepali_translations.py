"""ネパール語の翻訳をノートブックへ差し込む / Insert approved Nepali translations.

The Nepali text lives in ``assets/i18n/ne/notebooks/<stem>.ne.md`` so that translation, review and
re-application stay separate, repeatable steps. Nothing else in a notebook is touched: code cells,
cell ids, outputs, execution counts and the original Japanese/English prose stay byte-for-byte the
same.

カタログの書き方 / catalog format
--------------------------------
One sidecar file per notebook. Each block starts with a directive line::

    <!-- ne-cell: 79dc91db -->                 # append at the end of the cell
    <!-- ne-cell: 79dc91db | after-heading --> # directly after the leading heading block

and runs until the next directive. ``after-heading`` keeps a Nepali heading next to the
Japanese/English heading; ``end`` adds the Nepali explanation after the existing prose.

差し込みの仕組み / how insertion stays idempotent
-------------------------------------------------
Each inserted region is a marker pair that names its anchor::

    <!-- ne:begin end -->   … <!-- ne:end -->
    <!-- ne:begin after-heading --> … <!-- ne:end -->

The markers are invisible in Jupyter. Re-running a catalog rewrites only the *inside* of an existing
region and leaves the surrounding blank lines untouched, so a second run is a no-op. Devanagari
outside a region is reported as a conflict instead of being rewritten, so hand-written Nepali is
never silently lost.

使い方 / Usage
--------------
    python assets\\scripts\\apply_nepali_translations.py            # 点検のみ / dry run
    python assets\\scripts\\apply_nepali_translations.py --write    # 書き込み / write
    python assets\\scripts\\apply_nepali_translations.py --only Day02
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from course_notebooks import course_notebooks

COURSE_ROOT = Path(__file__).resolve().parents[2]
CATALOG_DIR = COURSE_ROOT / "assets" / "i18n" / "ne" / "notebooks"

BEGIN = "<!-- ne:begin {anchor} -->"
END = "<!-- ne:end -->"
REGION_RE = re.compile(
    r"\n<!--\s*ne:begin\s+(?P<anchor>[a-z\-]+)\s*-->\n"
    r"(?P<body>.*?)\n<!--\s*ne:end\s*-->\n", re.S)
DIRECTIVE_RE = re.compile(r"^<!--\s*ne-cell:\s*([A-Za-z0-9_\-]+)\s*(?:\|\s*([a-z\-]+)\s*)?-->$")
DEVANAGARI_RE = re.compile(r"[\u0900-\u097f]")
FORBIDDEN_LABELS = ("日本語：", "日本語:", "English:", "English：")
VALID_ANCHORS = ("end", "after-heading")


class CatalogError(SystemExit):
    pass


def parse_regions(source: str) -> dict[str, dict]:
    """差し込み済みの領域を取り出す / collect the existing Nepali regions of one cell."""
    regions: dict[str, dict] = {}
    for match in REGION_RE.finditer(source):
        anchor = match.group("anchor")
        if anchor not in VALID_ANCHORS:
            raise CatalogError(f"unknown anchor in notebook source: {anchor!r}")
        if anchor in regions:
            raise CatalogError(f"two Nepali regions with anchor {anchor!r} in one cell")
        regions[anchor] = {"span": match.span(), "body": match.group("body")}
    return regions


def strip_regions(source: str) -> str:
    """領域を取り除いた元の本文 / the original source without the Nepali regions."""
    text = REGION_RE.sub("", source)
    return text.rstrip("\n") + "\n" if text.strip() else text


def _heading_insert_index(lines: list[str]) -> int:
    """先頭の見出しブロックの直後の行番号 / index just after the leading heading block."""
    index = 0
    while index < len(lines) and not lines[index].strip():
        index += 1
    last_heading = None
    while index < len(lines):
        stripped = lines[index].strip()
        if stripped.startswith("#"):
            last_heading = index
            index += 1
            continue
        if not stripped and last_heading is not None:
            index += 1
            continue
        break
    if last_heading is None:
        raise CatalogError("cell has no leading heading for the 'after-heading' anchor")
    return last_heading + 1


def _insert_region(text: str, anchor: str, body: str) -> str:
    marker = BEGIN.format(anchor=anchor)
    if anchor == "after-heading":
        lines = text.split("\n")
        index = _heading_insert_index(lines)
        head = "\n".join(lines[:index])
        tail = "\n".join(lines[index:])
        if not head.endswith("\n"):
            head += "\n"
        return head + "\n" + marker + "\n" + body + "\n" + END + "\n" + tail
    return text.rstrip("\n") + f"\n\n{marker}\n{body}\n{END}\n"


def apply_blocks(source: str, blocks: list[dict]) -> str:
    """1 つのセルのネパール語ブロックを、あれば中身だけ書き換える / insert or rewrite."""
    wanted = {block["at"]: block["text"] for block in blocks}
    existing = parse_regions(source)

    text = source
    # drop regions the catalog no longer defines, right to left so the spans stay valid
    for anchor, region in sorted(existing.items(), key=lambda item: -item[1]["span"][0]):
        if anchor in wanted:
            continue
        start, end = region["span"]
        text = text[:start] + text[end:]

    for anchor, body in wanted.items():
        if anchor in existing:
            span_start, _span_end = existing[anchor]["span"]
            match = REGION_RE.match(text, span_start)
            if match and match.group("anchor") == anchor:
                text = text[:match.start("body")] + body + text[match.end("body"):]
                continue
        text = _insert_region(text, anchor, body)

    return text if text.endswith("\n") else text + "\n"


def parse_catalog(path: Path) -> dict[str, list[dict]]:
    """Markdown の副ファイルを、セル ID ごとのブロックにする / parse the sidecar file."""
    text = path.read_text(encoding="utf-8")
    entries: dict[str, list[dict]] = {}
    state: dict = {"current": None, "buffer": [], "in_comment": False}

    def flush() -> None:
        current = state["current"]
        if current is None:
            return
        cell_id, anchor = current
        body = "\n".join(state["buffer"]).strip("\n")
        if not body.strip():
            raise CatalogError(f"{path.name}: empty Nepali block for {cell_id}")
        if not DEVANAGARI_RE.search(body):
            raise CatalogError(f"{path.name}: block {cell_id} has no Devanagari text")
        for label in FORBIDDEN_LABELS:
            if label in body:
                raise CatalogError(f"{path.name}: block {cell_id} has the forbidden label {label}")
        entries.setdefault(cell_id, []).append({"at": anchor, "text": body})

    for line in text.splitlines():
        match = DIRECTIVE_RE.match(line.strip())
        if match:
            flush()
            anchor = match.group(2) or "end"
            if anchor not in VALID_ANCHORS:
                raise CatalogError(f"{path.name}: bad anchor {anchor!r} for {match.group(1)}")
            state["current"] = (match.group(1), anchor)
            state["buffer"] = []
            continue
        if state["current"] is None:
            stripped = line.strip()
            if state["in_comment"]:
                state["in_comment"] = not stripped.endswith("-->")
                continue
            if stripped.startswith("<!--"):
                state["in_comment"] = not stripped.endswith("-->")
                continue
            if stripped and not stripped.startswith("#"):
                raise CatalogError(f"{path.name}: text before the first ne-cell directive: {line!r}")
            continue
        state["buffer"].append(line)
    flush()

    for cell_id, blocks in entries.items():
        anchors = [block["at"] for block in blocks]
        if len(anchors) != len(set(anchors)):
            raise CatalogError(f"{path.name}: {cell_id} has two blocks at the same anchor")
    return entries


def apply_catalog(path: Path, entries: dict[str, list[dict]], write: bool) -> dict:
    nb = json.loads(path.read_text(encoding="utf-8"))
    by_id = {cell.get("id"): cell for cell in nb["cells"] if cell.get("id")}
    report = {"path": path.relative_to(COURSE_ROOT).as_posix(), "changed": 0,
              "conflicts": [], "missing_ids": [], "untracked_devanagari": []}

    for cell_id, blocks in entries.items():
        cell = by_id.get(cell_id)
        if cell is None:
            report["missing_ids"].append(cell_id)
            continue
        if cell["cell_type"] != "markdown":
            report["conflicts"].append(f"{cell_id}: not a markdown cell")
            continue
        current = "".join(cell["source"])
        if DEVANAGARI_RE.search(REGION_RE.sub("", current)):
            report["untracked_devanagari"].append(cell_id)
            continue
        updated = apply_blocks(current, blocks)
        if updated != current:
            report["changed"] += 1
            if write:
                cell["source"] = updated.splitlines(keepends=True)

    for cell in nb["cells"]:
        if cell["cell_type"] != "markdown" or cell.get("id") in entries:
            continue
        if DEVANAGARI_RE.search(REGION_RE.sub("", "".join(cell["source"]))):
            report["untracked_devanagari"].append(cell.get("id"))

    if write and report["changed"]:
        path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return report


def catalogs(only: str | None = None) -> list[Path]:
    paths = sorted(CATALOG_DIR.glob("*.ne.md"))
    if only:
        paths = [path for path in paths if only in path.name]
    return paths


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Insert Nepali translations into notebooks.")
    parser.add_argument("--write", action="store_true", help="write the notebooks")
    parser.add_argument("--only", default=None, help="substring of the catalog file name")
    args = parser.parse_args(argv)

    course = {path.stem: path for path in course_notebooks(COURSE_ROOT / "notebooks")}
    problems = 0
    total_changed = 0
    for catalog_path in catalogs(args.only):
        entries = parse_catalog(catalog_path)
        stem = catalog_path.name[: -len(".ne.md")]
        target = course.get(stem)
        if target is None:
            print(f"[unknown notebook] {stem}")
            problems += 1
            continue
        report = apply_catalog(target, entries, args.write)
        total_changed += report["changed"]
        state = "written" if args.write else "pending"
        print(f"[{state}] {report['path']}  blocks={len(entries)}  changed={report['changed']}")
        for key in ("conflicts", "missing_ids", "untracked_devanagari"):
            if report[key]:
                problems += 1
                print(f"   ! {key}: {report[key][:5]}")
    verb = "written" if args.write else "would change"
    print(f"[done] {total_changed} cells {verb}; {problems} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
