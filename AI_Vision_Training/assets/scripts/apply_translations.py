"""言語ごとの翻訳をノートブックへ差し込む / insert one locale's translations into the notebooks.

This is the language-aware version of ``apply_nepali_translations.py``. The text lives in
``assets/i18n/<locale>/notebooks/<stem>.<locale>.md`` so that translation, review and re-application
stay separate, repeatable steps. Nothing else in a notebook is touched: code cells, cell ids,
outputs, execution counts and the original Japanese/English prose stay byte-for-byte the same.

カタログの書き方 / catalog format
--------------------------------
One sidecar per notebook. A block starts with a directive line owned by its locale::

    <!-- taj-cell: 79dc91db -->                 # append at the end of the cell
    <!-- taj-cell: 79dc91db | after-heading --> # directly after the leading heading block
    <!-- taj-cell: figure-id | after-image:../../assets/diagrams/example.png -->

and runs until the next directive. Two more directives carry review state rather than text::

    <!-- taj-status: 79dc91db approved -->      # a reviewer signed this block off
    <!-- taj-pending: 79dc91db | reason -->     # no dependable text yet; nothing is inserted

``pending`` exists so an untranslated cell is *recorded as pending* instead of being filled with
something invented. The coverage checker counts the two states separately.

差し込みの仕組み / how insertion stays idempotent
-------------------------------------------------
Each inserted region is a marker pair that names its anchor, e.g. ``<!-- taj:begin end -->`` …
``<!-- taj:end -->``. Re-running a catalog rewrites only the *inside* of an existing region, so a
second run is a no-op. Devanagari outside a region is reported as a conflict instead of being
rewritten, so hand-written text is never silently lost.

使い方 / Usage
--------------
    python assets\\scripts\\apply_translations.py --locale taj            # 点検 / dry run
    python assets\\scripts\\apply_translations.py --locale taj --write    # 書き込み / write
    python assets\\scripts\\apply_translations.py --locale taj --only Day05
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from course_notebooks import course_notebooks
from i18n_locales import DEVANAGARI_RE, Locale, locale as get_locale
from romanize_nepali import looks_like_nepali_latin

COURSE_ROOT = Path(__file__).resolve().parents[2]

FORBIDDEN_LABELS = ("日本語：", "日本語:", "English:", "English：")
VALID_ANCHORS = ("end", "after-heading")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")
CAPTION_RE = re.compile(
    r"^(?:図[：:]|Figure[：:]|चित्र[：:]|चित्रमा|फोटो[：:]|写真[：:]|Photo[：:]"
    r"|[Cc]hitra[：:]|[Cc]hitrama|[Tt]asbir[：:]|[Pp]hoto[：:])")
LATIN_WORD_RE = re.compile(r"[A-Za-z]{4,}")


class CatalogError(SystemExit):
    pass


def valid_anchor(anchor: str) -> bool:
    return anchor in VALID_ANCHORS or (
        anchor.startswith("after-image:") and bool(anchor.partition(":")[2]))


def begin_marker(loc: Locale, anchor: str) -> str:
    return f"<!-- {loc.marker}:begin {anchor} -->"


def end_marker(loc: Locale) -> str:
    return f"<!-- {loc.marker}:end -->"


# ---------------------------------------------------------------------------
# block validation — a script test is not a language test
# ---------------------------------------------------------------------------


def validate_block(loc: Locale, body: str, where: str) -> None:
    """書かれた文字が、その言語の前提を満たすか / does the block meet the locale's script rule?

    This is a *script* check. It cannot prove that the text is good Tamang, so it is never reported
    as language verification; that only a reviewer can give.
    """
    if not body.strip():
        raise CatalogError(f"{where}: empty {loc.code} block")
    for label in FORBIDDEN_LABELS:
        if label in body:
            raise CatalogError(f"{where}: the forbidden label {label} is present")
    if loc.script == "devanagari":
        if not DEVANAGARI_RE.search(body):
            raise CatalogError(
                f"{where}: a {loc.code} block must be written in Devanagari; "
                "copied English or Latin transliteration cannot pass as Tamang")
        return
    if not DEVANAGARI_RE.search(body) and not looks_like_nepali_latin(body):
        raise CatalogError(f"{where}: the block is neither Devanagari nor Romanized Nepali")


def is_placeholder_heavy(body: str) -> bool:
    """Latin の長い語が多い＝英語のまま / mostly Latin words, i.e. untranslated prose."""
    words = LATIN_WORD_RE.findall(body)
    return len(words) > 3 and len(words) > len(body.split()) / 3


# ---------------------------------------------------------------------------
# regions inside a notebook cell
# ---------------------------------------------------------------------------


def image_captions(lines: list[str], start: int) -> tuple[list[str], int]:
    """Read caption paragraphs, including wrapped lines, but never lesson prose."""
    captions = []
    index = start
    while index < len(lines):
        while index < len(lines) and not lines[index].strip():
            index += 1
        if index == len(lines) or not CAPTION_RE.match(lines[index].strip()):
            break
        paragraph = [lines[index].strip()]
        index += 1
        while index < len(lines) and lines[index].strip():
            line = lines[index].strip()
            if CAPTION_RE.match(line) or line.startswith(("<!--", "#", "**", "![", "|", "```")):
                break
            paragraph.append(line)
            index += 1
        captions.append(" ".join(paragraph))
    return captions, index


def parse_regions(source: str, loc: Locale) -> dict[str, dict]:
    """差し込み済みの領域を取り出す / collect the existing regions of one cell."""
    regions: dict[str, dict] = {}
    for match in loc.region_re().finditer(source):
        anchor = match.group("anchor")
        if not valid_anchor(anchor):
            raise CatalogError(f"unknown anchor in notebook source: {anchor!r}")
        if anchor in regions:
            raise CatalogError(f"two {loc.code} regions with anchor {anchor!r} in one cell")
        regions[anchor] = {"span": match.span(), "body": match.group("body")}
    return regions


def strip_regions(source: str, loc: Locale) -> str:
    """領域を取り除いた元の本文 / the original source without the translated regions."""
    text = loc.region_re().sub("", source)
    return text.rstrip("\n") + "\n" if text.strip() else text


def _heading_insert_index(lines: list[str]) -> int:
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


def _insert_region(text: str, anchor: str, body: str, loc: Locale) -> str:
    marker = begin_marker(loc, anchor)
    end = end_marker(loc)
    if anchor.startswith("after-image:"):
        target = anchor.partition(":")[2]
        lines = text.split("\n")
        matches = [(index, match) for index, line in enumerate(lines)
                   for match in IMAGE_RE.finditer(line) if match.group(2) == target]
        if len(matches) != 1:
            raise CatalogError(f"image anchor {target!r}: expected one image, found {len(matches)}")
        index, _ = matches[0]
        _, stop = image_captions(lines, index + 1)
        head, tail = "\n".join(lines[:stop]), "\n".join(lines[stop:])
        return head + f"\n{marker}\n{body}\n{end}\n\n" + tail
    if anchor == "after-heading":
        lines = text.split("\n")
        index = _heading_insert_index(lines)
        head = "\n".join(lines[:index])
        tail = "\n".join(lines[index:])
        if not head.endswith("\n"):
            head += "\n"
        return head + "\n" + marker + "\n" + body + "\n" + end + "\n" + tail
    return text.rstrip("\n") + f"\n\n{marker}\n{body}\n{end}\n"


def apply_blocks(source: str, blocks: list[dict], loc: Locale) -> str:
    """1 つのセルの領域を、あれば中身だけ書き換える / insert or rewrite."""
    wanted = {block["at"]: block["text"] for block in blocks}
    original = strip_regions(source, loc)
    for anchor in wanted:
        if not valid_anchor(anchor):
            raise CatalogError(f"unknown anchor: {anchor!r}")
        if anchor.startswith("after-image:"):
            target = anchor.partition(":")[2]
            count = sum(match.group(2) == target for match in IMAGE_RE.finditer(original))
            if count != 1:
                raise CatalogError(f"image anchor {target!r}: expected one image, found {count}")
    existing = parse_regions(source, loc)

    text = source
    for anchor, region in sorted(existing.items(), key=lambda item: -item[1]["span"][0]):
        if anchor in wanted:
            continue
        start, stop = region["span"]
        text = text[:start] + text[stop:]

    for anchor, body in wanted.items():
        current = parse_regions(text, loc)
        if anchor in current:
            span_start, _span_stop = current[anchor]["span"]
            match = loc.region_re().match(text, span_start)
            if match and match.group("anchor") == anchor:
                text = text[:match.start("body")] + body + text[match.end("body"):]
                continue
        text = _insert_region(text, anchor, body, loc)

    return text if text.endswith("\n") else text + "\n"


# ---------------------------------------------------------------------------
# catalogs
# ---------------------------------------------------------------------------


def parse_catalog(path: Path, loc: Locale) -> dict[str, list[dict]]:
    """副ファイルを、セル ID ごとのブロックにする / parse one sidecar file."""
    text = path.read_text(encoding="utf-8")
    entries: dict[str, list[dict]] = {}
    state: dict = {"current": None, "buffer": [], "in_comment": False}
    directive = loc.cell_directive_re()
    pending = loc.pending_directive_re()
    status = loc.status_directive_re()

    def flush() -> None:
        current = state["current"]
        if current is None:
            return
        cell_id, anchor = current
        body = "\n".join(state["buffer"]).strip("\n")
        validate_block(loc, body, f"{path.name}: block {cell_id}")
        entries.setdefault(cell_id, []).append({"at": anchor, "text": body})

    for line in text.splitlines():
        stripped = line.strip()
        if pending.match(stripped) or status.match(stripped):
            flush()
            state["current"], state["buffer"] = None, []
            continue
        match = directive.match(stripped)
        if match:
            flush()
            anchor = match.group(2) or "end"
            if not valid_anchor(anchor):
                raise CatalogError(f"{path.name}: bad anchor {anchor!r} for {match.group(1)}")
            state["current"] = (match.group(1), anchor)
            state["buffer"] = []
            continue
        if state["current"] is None:
            if state["in_comment"]:
                state["in_comment"] = not stripped.endswith("-->")
                continue
            if stripped.startswith("<!--"):
                state["in_comment"] = not stripped.endswith("-->")
                continue
            if stripped and not stripped.startswith("#"):
                raise CatalogError(f"{path.name}: text before the first directive: {line!r}")
            continue
        state["buffer"].append(line)
    flush()

    for cell_id, blocks in entries.items():
        anchors = [block["at"] for block in blocks]
        if len(anchors) != len(set(anchors)):
            raise CatalogError(f"{path.name}: {cell_id} has two blocks at the same anchor")
    return entries


def parse_pending(path: Path, loc: Locale) -> dict[str, str]:
    """未翻訳として明示されたセル / cells the catalog records as pending, with the reason."""
    pending: dict[str, str] = {}
    if not path.is_file():
        return pending
    pattern = loc.pending_directive_re()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line.strip())
        if match:
            pending[match.group(1)] = (match.group(2) or "").strip()
    return pending


def parse_status(path: Path, loc: Locale) -> dict[str, str]:
    """セルごとのレビュー状態 / per-cell review status claimed by the catalog."""
    status: dict[str, str] = {}
    if not path.is_file():
        return status
    pattern = loc.status_directive_re()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line.strip())
        if match:
            status[match.group(1)] = match.group(2)
    return status


def catalog_metadata(path: Path) -> dict[str, str]:
    """カタログ先頭の来歴 / the provenance header of a catalog."""
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    head = text[: text.find("-->")] if text.lstrip().startswith("<!--") else ""
    metadata = {}
    for line in head.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            if key and not key.startswith("#"):
                metadata[key] = value.strip()
    return metadata


def apply_catalog(path: Path, entries: dict[str, list[dict]], write: bool, loc: Locale) -> dict:
    notebook_path = path
    nb = json.loads(notebook_path.read_text(encoding="utf-8"))
    by_id = {cell.get("id"): cell for cell in nb["cells"] if cell.get("id")}
    report = {"path": notebook_path.relative_to(COURSE_ROOT).as_posix(), "changed": 0,
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
        if DEVANAGARI_RE.search(loc.region_re().sub("", current)):
            report["untracked_devanagari"].append(cell_id)
            continue
        updated = apply_blocks(current, blocks, loc)
        if updated != current:
            report["changed"] += 1
            if write:
                cell["source"] = updated.splitlines(keepends=True)

    for cell in nb["cells"]:
        if cell["cell_type"] != "markdown" or cell.get("id") in entries:
            continue
        if DEVANAGARI_RE.search(loc.region_re().sub("", "".join(cell["source"]))):
            report["untracked_devanagari"].append(cell.get("id"))

    if write and report["changed"]:
        notebook_path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n",
                                 encoding="utf-8")
    return report


def catalogs(loc: Locale, only: str | None = None) -> list[Path]:
    paths = sorted(loc.catalog_dir("notebooks").glob(f"*.{loc.code}.md"))
    if only:
        paths = [path for path in paths if only in path.name]
    return paths


def main(argv=None, default_locale: str = "ne") -> int:
    parser = argparse.ArgumentParser(description="Insert one locale's translations into notebooks.")
    parser.add_argument("--locale", default=default_locale,
                        help="locale code (ne, taj)")
    parser.add_argument("--write", action="store_true", help="write the notebooks")
    parser.add_argument("--only", default=None, help="substring of the catalog file name")
    args = parser.parse_args(argv)
    loc = get_locale(args.locale)

    course = {path.stem: path for path in course_notebooks(COURSE_ROOT / "notebooks")}
    problems = 0
    total_changed = 0
    for catalog_path in catalogs(loc, args.only):
        entries = parse_catalog(catalog_path, loc)
        stem = catalog_path.name[: -len(f".{loc.code}.md")]
        target = course.get(stem)
        if target is None:
            print(f"[unknown notebook] {stem}")
            problems += 1
            continue
        report = apply_catalog(target, entries, args.write, loc)
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
