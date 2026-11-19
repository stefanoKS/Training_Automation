"""言語ごとの翻訳を Markdown 文書へ差し込む / insert one locale's text into the documents.

Notebooks have cell ids; documents do not, so this script keys each block on the **exact heading
line** of the section it belongs to and appends the translated block at the end of that section.

カタログの書き方 / catalog format
--------------------------------
One sidecar per document under ``assets/i18n/<locale>/docs/``::

    <!-- taj-doc: START_HERE.md -->
    <!-- taj-section: ## 3. 仮想環境を作る -->
    …translated block…

The first directive names the target file (relative to the course root). Every ``<locale>-section``
line must match an existing heading key (qualified with parents if the heading occurs more than
once); an unmatched heading is an error, so a heading rename cannot silently drop a translation.

Each block is wrapped in a marker pair that names the section::

    <!-- taj:begin doc:3f4c1a == --> … <!-- taj:end -->

Re-running a catalog rewrites only the body inside an existing region. Command blocks, numbers and
paths inside the translated text are copied from the original; nothing else in the document changes.

使い方 / Usage
--------------
    python assets\\scripts\\apply_docs.py --locale taj            # dry run
    python assets\\scripts\\apply_docs.py --locale taj --write    # write
"""

from __future__ import annotations

import argparse
import hashlib
import re
from collections import Counter
from pathlib import Path

from i18n_locales import DEVANAGARI_RE, Locale, has_devanagari_letters, locale as get_locale
from romanize_nepali import looks_like_nepali_latin

COURSE_ROOT = Path(__file__).resolve().parents[2]
FORBIDDEN_LABELS = ("日本語：", "日本語:", "English:", "English：")


class CatalogError(SystemExit):
    pass


def slug_of(heading: str) -> str:
    return hashlib.sha1(heading.strip().encode("utf-8")).hexdigest()[:10]


def begin_marker(loc: Locale, slug: str) -> str:
    return f"<!-- {loc.marker}:begin doc:{slug} -->"


def end_marker(loc: Locale) -> str:
    return f"<!-- {loc.marker}:end -->"


def validate_block(loc: Locale, body: str, where: str) -> None:
    if not body.strip():
        raise CatalogError(f"{where}: empty {loc.code} block")
    for label in FORBIDDEN_LABELS:
        if label in body:
            raise CatalogError(f"{where}: the forbidden label {label} is present")
    if loc.script == "devanagari":
        if not has_devanagari_letters(body):
            raise CatalogError(
                f"{where}: a {loc.code} block must be written in Devanagari; copied English or "
                "Latin transliteration cannot pass as Tamang")
        return
    if not DEVANAGARI_RE.search(body) and not looks_like_nepali_latin(body):
        raise CatalogError(f"{where}: the block is neither Devanagari nor Romanized Nepali")


def parse_catalog(path: Path, loc: Locale) -> tuple[str, dict[str, list[str]]]:
    """副ファイルを、見出し行ごとのブロックにする / parse one sidecar file."""
    target = None
    blocks: dict[str, list[str]] = {}
    current = None
    buffer: list[str] = []
    in_comment = False
    doc_re = loc.doc_re()
    section_re = loc.section_directive_re()
    pending_re = loc.doc_pending_directive_re()

    def flush() -> None:
        nonlocal current, buffer
        if current is None:
            return
        body = "\n".join(buffer).strip("\n")
        validate_block(loc, body, f"{path.name}: block {current!r}")
        if current in blocks:
            raise CatalogError(f"{path.name}: two blocks for the same heading {current!r}")
        blocks[current] = buffer
        current, buffer = None, []

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        doc_match = doc_re.match(stripped)
        if doc_match:
            if target is not None or current is not None:
                raise CatalogError(f"{path.name}: repeated or misplaced document target")
            target = doc_match.group("path")
            continue
        if pending_re.match(stripped) or loc.doc_status_directive_re().match(stripped):
            flush()
            continue
        section_match = section_re.match(stripped)
        if section_match:
            flush()
            current = section_match.group("heading")
            buffer = []
            continue
        if current is None:
            if in_comment:
                in_comment = not stripped.endswith("-->")
                continue
            if stripped.startswith("<!--"):
                in_comment = not stripped.endswith("-->")
                continue
            if stripped and not stripped.startswith("#"):
                raise CatalogError(f"{path.name}: text before the first section directive: {line!r}")
            continue
        buffer.append(line)
    flush()

    if target is None:
        raise CatalogError(f"{path.name}: no '<!-- {loc.code}-doc: ... -->' target line")
    return target, blocks


def parse_pending(path: Path, loc: Locale) -> dict[str, str]:
    """未翻訳として明示された節 / sections the catalog records as pending."""
    pending: dict[str, str] = {}
    pattern = loc.doc_pending_directive_re()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line.strip())
        if match:
            pending[match.group("key").strip()] = (match.group("reason") or "").strip()
    return pending


def headings(lines: list[str]) -> list[tuple[int, str]]:
    """Return ATX headings, ignoring fenced code and HTML comments."""
    found = []
    fence = ""
    comment = False
    for index, line in enumerate(lines):
        line = line.strip()
        if comment or (not fence and line.startswith("<!--")):
            comment = "-->" not in line
            continue
        match = re.match(r"^(`{3,}|~{3,})(.*)$", line)
        if match:
            marker, tail = match.groups()
            if not fence:
                fence = marker
            elif marker.startswith(fence) and not tail.strip():
                fence = ""
            continue
        if not fence and re.match(r"^#{1,6}\s+\S", line):
            found.append((index, line))
    return found


def section_anchors(lines: list[str]) -> list[tuple[int, str]]:
    found = headings(lines)
    counts = Counter(heading for _, heading in found)
    parents: list[tuple[int, str]] = []
    anchors = []
    for index, heading in found:
        level = len(heading.split(maxsplit=1)[0])
        while parents and parents[-1][0] >= level:
            parents.pop()
        key = " > ".join([*(title for _, title in parents), heading]) if counts[heading] > 1 else heading
        anchors.append((index, key))
        parents.append((level, heading))
    return anchors


def section_bounds(lines: list[str], heading: str, *, exact: bool = False) -> tuple[int, int]:
    if exact:
        anchors = section_anchors(lines)
        positions = [index for index, _ in anchors]
        matches = [index for index, key in anchors if key == heading.strip()]
    elif heading.strip().startswith("#"):
        matches = [i for i, line in enumerate(lines) if line.startswith(heading.strip())]
    else:
        matches = [i for i, line in enumerate(lines)
                   if line.startswith("#") and heading.strip() in line]
    if not matches:
        raise CatalogError(f"heading not found: {heading!r}")
    if len(matches) > 1:
        raise CatalogError(f"heading {heading!r} matches {len(matches)} headings; be more specific")
    start = matches[0]
    if exact:
        return start, next((index for index in positions if index > start), len(lines))
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("#"):
            return start, index
    return start, len(lines)


def region_spans(text: str, loc: Locale) -> dict[str, tuple[int, int, int, int]]:
    spans = {}
    for match in loc.doc_region_re().finditer(text):
        if match.group("slug") in spans:
            raise CatalogError(f"duplicate {loc.code} document region: {match.group('slug')}")
        spans[match.group("slug")] = (
            match.start(), match.start("body"), match.end("body"), match.end())
    return spans


def _line_patterns(loc: Locale):
    begin = re.compile(r"^<!--\s*" + loc.marker + r":begin\s+doc:[0-9a-f]+\s*-->$")
    end = re.compile(r"^<!--\s*" + loc.marker + r":end\s*-->$")
    return begin, end


def strip_regions(text: str, loc: Locale) -> str:
    """差し込み済みの領域をすべて取り除く / remove every region (nesting included)."""
    begin_re, end_re = _line_patterns(loc)
    kept: list[str] = []
    depth = 0
    for line in text.split("\n"):
        stripped = line.strip()
        if begin_re.match(stripped):
            if depth == 0:
                while kept and not kept[-1].strip():
                    kept.pop()
                kept.append("")
            depth += 1
            continue
        if end_re.match(stripped) and depth:
            depth -= 1
            continue
        if depth:
            continue
        kept.append(line)
    while kept and not kept[-1].strip():
        kept.pop()
    return "\n".join(kept) + "\n"


def apply_blocks(text: str, blocks: dict[str, list[str]], loc: Locale) -> str:
    wanted = {slug_of(heading): body for heading, body in blocks.items()}
    headings = {slug_of(heading): heading for heading in blocks}
    existing = region_spans(text, loc)
    if loc.code != "ne":
        source = text
        for language in (loc, get_locale("ne")):
            # Keep source line numbers while hiding headings inside any translation.
            source = language.doc_region_re().sub(lambda m: "\n" * m.group().count("\n"), source)
        for heading in blocks:
            section_bounds(source.split("\n"), heading, exact=True)

    for slug, (_start, _body_start, _body_end, _end) in sorted(
            existing.items(), key=lambda item: -item[1][0]):
        if slug in wanted:
            continue
        start, _bs, _be, end = existing[slug]
        text = text[: start - 1] + text[end:]

    for slug, body in wanted.items():
        body_text = "\n".join(body).strip("\n")
        if slug in existing:
            _start, body_start, body_end, _end = region_spans(text, loc)[slug]
            text = text[:body_start] + body_text + text[body_end:]
            continue
        lines = text.split("\n")
        if loc.code == "ne":
            _start, end = section_bounds(lines, headings[slug])
        else:
            source = text
            for language in (loc, get_locale("ne")):
                source = language.doc_region_re().sub(
                    lambda m: "\n" * m.group().count("\n"), source)
            _start, end = section_bounds(source.split("\n"), headings[slug], exact=True)
        while end > 0 and not lines[end - 1].strip():
            end -= 1
        head = "\n".join(lines[:end])
        tail_lines = lines[end:]
        while tail_lines and not tail_lines[0].strip():
            tail_lines.pop(0)
        tail = "\n".join(tail_lines)
        region = f"\n\n{begin_marker(loc, slug)}\n{body_text}\n{end_marker(loc)}\n"
        text = head + region + ("\n" + tail if tail.strip() else "")
        if not text.endswith("\n"):
            text += "\n"
    return text if text.endswith("\n") else text + "\n"


def apply_catalog(path: Path, write: bool, loc: Locale, reset: bool = False) -> dict:
    target_rel, blocks = parse_catalog(path, loc)
    target = COURSE_ROOT / target_rel
    if not target.is_file():
        raise CatalogError(f"{path.name}: target document not found: {target_rel}")
    original = target.read_text(encoding="utf-8")
    if reset:
        original = strip_regions(original, loc)
    remaining = strip_regions(original, loc)
    if loc.code != "ne":
        remaining = strip_regions(remaining, get_locale("ne"))
    if DEVANAGARI_RE.search(remaining):
        raise CatalogError(
            f"{path.name}: {target_rel} already contains Devanagari outside a region")
    updated = apply_blocks(original, blocks, loc)
    changed = updated != target.read_text(encoding="utf-8")
    if write and changed:
        target.write_text(updated, encoding="utf-8")
    return {"path": target_rel, "blocks": len(blocks), "changed": changed}


def catalogs(loc: Locale, only: str | None = None) -> list[Path]:
    directory = loc.catalog_dir("docs")
    paths = sorted(directory.glob(f"*.{loc.code}.md")) if directory.is_dir() else []
    if only:
        paths = [path for path in paths if only in path.name]
    return paths


def main(argv=None, default_locale: str = "ne") -> int:
    parser = argparse.ArgumentParser(description="Insert one locale's translations into documents.")
    parser.add_argument("--locale", default=default_locale, help="locale code (ne, taj)")
    parser.add_argument("--write", action="store_true", help="write the documents")
    parser.add_argument("--only", default=None, help="substring of the catalog file name")
    parser.add_argument("--reset", action="store_true",
                        help="drop every existing region before applying (repair)")
    args = parser.parse_args(argv)
    loc = get_locale(args.locale)

    problems = 0
    for catalog_path in catalogs(loc, args.only):
        try:
            report = apply_catalog(catalog_path, args.write, loc, args.reset)
        except CatalogError as error:
            print(f"[error] {error}")
            problems += 1
            continue
        state = "written" if args.write and report["changed"] else "pending"
        print(f"[{state}] {report['path']}  blocks={report['blocks']}  "
              f"changed={int(report['changed'])}")
    print(f"[done] {problems} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
