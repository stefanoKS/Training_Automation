"""ネパール語の翻訳を Markdown 文書へ差し込む / Insert approved Nepali text into the documents.

The notebook applier (``apply_nepali_translations.py``) works on cell ids. Documents have no cell
ids, so this script keys each block on the **exact heading line** of the section it belongs to and
appends the Nepali block at the end of that section.

カタログの書き方 / catalog format
--------------------------------
One sidecar file per document under ``assets/i18n/ne/docs/``::

    <!-- ne-doc: START_HERE.md -->
    <!-- ne-section: ## 3. 仮想環境を作る -->
    ## ३. virtual environment बनाउने
    …

The first directive names the target file (relative to the course root). Every ``ne-section`` line
must match an existing heading line byte for byte; an unmatched heading is an error, so a heading
rename cannot silently drop a translation.

差し込みの仕組み / how insertion stays idempotent
-------------------------------------------------
Each block is wrapped in a marker pair that names the section::

    <!-- ne:begin doc:3f4c1a == --> … <!-- ne:end -->

Re-running a catalog rewrites only the body inside an existing region. Command blocks, numbers and
paths inside the Nepali text are copied from the original; nothing else in the document changes.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

COURSE_ROOT = Path(__file__).resolve().parents[2]
CATALOG_DIR = COURSE_ROOT / "assets" / "i18n" / "ne" / "docs"

BEGIN = "<!-- ne:begin doc:{slug} -->"
END = "<!-- ne:end -->"
REGION_RE = re.compile(
    r"\n<!--\s*ne:begin\s+doc:(?P<slug>[0-9a-f]+)\s*-->\n"
    r"(?P<body>.*?)\n<!--\s*ne:end\s*-->\n", re.S)
DOC_RE = re.compile(r"^<!--\s*ne-doc:\s*(?P<path>[^\s]+)\s*-->$")
SECTION_RE = re.compile(r"^<!--\s*ne-section:\s*(?P<heading>.+?)\s*-->$")
DEVANAGARI_RE = re.compile(r"[\u0900-\u097f]")
FORBIDDEN_LABELS = ("日本語：", "日本語:", "English:", "English：")


class CatalogError(SystemExit):
    pass


def slug_of(heading: str) -> str:
    return hashlib.sha1(heading.strip().encode("utf-8")).hexdigest()[:10]


def parse_catalog(path: Path) -> tuple[str, dict[str, list[str]]]:
    """副ファイルを、見出し行ごとのブロックにする / parse one sidecar file."""
    target = None
    blocks: dict[str, list[str]] = {}
    current = None
    buffer: list[str] = []
    in_comment = False

    def flush() -> None:
        nonlocal current, buffer
        if current is None:
            return
        body = "\n".join(buffer).strip("\n")
        if not body.strip():
            raise CatalogError(f"{path.name}: empty Nepali block for {current!r}")
        if not DEVANAGARI_RE.search(body):
            raise CatalogError(f"{path.name}: block {current!r} has no Devanagari text")
        for label in FORBIDDEN_LABELS:
            if label in body:
                raise CatalogError(f"{path.name}: block {current!r} has the forbidden label {label}")
        if current in blocks:
            raise CatalogError(f"{path.name}: two blocks for the same heading {current!r}")
        blocks[current] = buffer
        current, buffer = None, []

    for line in path.read_text(encoding="utf-8").splitlines():
        doc_match = DOC_RE.match(line.strip())
        if doc_match and current is None:
            target = doc_match.group("path")
            continue
        section_match = SECTION_RE.match(line.strip())
        if section_match:
            flush()
            current = section_match.group("heading")
            buffer = []
            continue
        if current is None:
            stripped = line.strip()
            if in_comment:
                in_comment = not stripped.endswith("-->")
                continue
            if stripped.startswith("<!--"):
                in_comment = not stripped.endswith("-->")
                continue
            if stripped and not stripped.startswith("#"):
                raise CatalogError(f"{path.name}: text before the first ne-section: {line!r}")
            continue
        buffer.append(line)
    flush()

    if target is None:
        raise CatalogError(f"{path.name}: no '<!-- ne-doc: ... -->' target line")
    return target, blocks


def section_bounds(lines: list[str], heading: str) -> tuple[int, int]:
    """見出し行と、その節の見出し直後の本文の終わり / heading index and the end of its own prose.

    ``heading`` is a substring that has to match exactly one heading line, so a catalog stays
    readable (``## 4.`` or a few words) without copying long bilingual headings verbatim.
    The block is inserted before the next heading of *any* level, so a section that contains
    subsections keeps its Nepali summary directly under its own prose instead of after them.
    """
    if heading.strip().startswith("#"):
        matches = [i for i, line in enumerate(lines) if line.startswith(heading.strip())]
    else:
        matches = [i for i, line in enumerate(lines)
                   if line.startswith("#") and heading.strip() in line]
    if not matches:
        raise CatalogError(f"heading not found: {heading!r}")
    if len(matches) > 1:
        raise CatalogError(f"heading {heading!r} matches {len(matches)} headings; be more specific")
    start = matches[0]
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("#"):
            return start, index
    return start, len(lines)


def region_spans(text: str) -> dict[str, tuple[int, int, int, int]]:
    """領域ごとの (全体開始, 本文開始, 本文終了, 全体終了) / spans of the existing regions."""
    spans = {}
    for match in REGION_RE.finditer(text):
        spans[match.group("slug")] = (
            match.start(), match.start("body"), match.end("body"), match.end())
    return spans


BEGIN_LINE_RE = re.compile(r"^<!--\s*ne:begin\s+doc:[0-9a-f]+\s*-->$")
END_LINE_RE = re.compile(r"^<!--\s*ne:end\s*-->$")


def strip_regions(text: str) -> str:
    """差し込み済みの領域をすべて取り除く / remove every Nepali region (nesting included)."""
    kept: list[str] = []
    depth = 0
    for line in text.split("\n"):
        stripped = line.strip()
        if BEGIN_LINE_RE.match(stripped):
            if depth == 0:
                while kept and not kept[-1].strip():
                    kept.pop()
                kept.append("")
            depth += 1
            continue
        if END_LINE_RE.match(stripped) and depth:
            depth -= 1
            continue
        if depth:
            continue
        kept.append(line)
    while kept and not kept[-1].strip():
        kept.pop()
    return "\n".join(kept) + "\n"


def apply_blocks(text: str, blocks: dict[str, list[str]]) -> str:
    wanted = {slug_of(heading): body for heading, body in blocks.items()}
    headings = {slug_of(heading): heading for heading in blocks}
    existing = region_spans(text)

    for slug, (_start, _body_start, _body_end, _end) in sorted(
            existing.items(), key=lambda item: -item[1][0]):
        if slug in wanted:
            continue
        start, _bs, _be, end = existing[slug]
        text = text[: start - 1] + text[end:]

    for slug, body in wanted.items():
        body_text = "\n".join(body).strip("\n")
        if slug in existing:
            _start, body_start, body_end, _end = region_spans(text)[slug]
            text = text[:body_start] + body_text + text[body_end:]
            continue
        lines = text.split("\n")
        _start, end = section_bounds(lines, headings[slug])
        while end > 0 and not lines[end - 1].strip():
            end -= 1
        head = "\n".join(lines[:end])
        tail_lines = lines[end:]
        while tail_lines and not tail_lines[0].strip():
            tail_lines.pop(0)
        tail = "\n".join(tail_lines)
        region = f"\n\n{BEGIN.format(slug=slug)}\n{body_text}\n{END}\n"
        text = head + region + ("\n" + tail if tail.strip() else "")
        if not text.endswith("\n"):
            text += "\n"
    return text if text.endswith("\n") else text + "\n"


def apply_catalog(path: Path, write: bool, reset: bool = False) -> dict:
    target_rel, blocks = parse_catalog(path)
    target = COURSE_ROOT / target_rel
    if not target.is_file():
        raise CatalogError(f"{path.name}: target document not found: {target_rel}")
    original = target.read_text(encoding="utf-8")
    if reset:
        original = strip_regions(original)
    untracked = DEVANAGARI_RE.search(strip_regions(original))
    if untracked:
        raise CatalogError(
            f"{path.name}: {target_rel} already contains Devanagari outside a region")
    updated = apply_blocks(original, blocks)
    changed = updated != target.read_text(encoding="utf-8")
    if write and changed:
        target.write_text(updated, encoding="utf-8")
    return {"path": target_rel, "blocks": len(blocks), "changed": changed}


def catalogs(only: str | None = None) -> list[Path]:
    paths = sorted(CATALOG_DIR.glob("*.ne.md")) if CATALOG_DIR.is_dir() else []
    if only:
        paths = [path for path in paths if only in path.name]
    return paths


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Insert Nepali translations into documents.")
    parser.add_argument("--write", action="store_true", help="write the documents")
    parser.add_argument("--only", default=None, help="substring of the catalog file name")
    parser.add_argument("--reset", action="store_true",
                        help="drop every existing region before applying (repair)")
    args = parser.parse_args(argv)

    problems = 0
    for catalog_path in catalogs(args.only):
        try:
            report = apply_catalog(catalog_path, args.write, args.reset)
        except CatalogError as error:
            print(f"[error] {error}")
            problems += 1
            continue
        state = "written" if args.write and report["changed"] else "pending"
        print(f"[{state}] {report['path']}  blocks={report['blocks']}  "
              f"changed={int(report['changed'])}")
    verb = "written" if args.write else "would change"
    print(f"[done] {len(catalogs(args.only)) - problems} document(s); {problems} problem(s)" if
          not args.write else f"[done] {verb}; {problems} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
