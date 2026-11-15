"""言語ラベルの整理 / Remove repetitive language labels.

このスクリプトは教材の Markdown から ``日本語：`` / ``English:`` のような
「言語ラベルだけ」の接頭辞を取り除きます。日本語と英語の本文はそのまま残し、
日本語 → 英語の順序も保ちます。

This script strips standalone language labels such as ``日本語：`` / ``English:``
from course Markdown while keeping every Japanese and English paragraph, in the
original Japanese-then-English order.

対象 / Scope
------------
* ``.ipynb`` の Markdown セルだけ / Markdown cells of ``.ipynb`` files only
* 受講者向け・講師向けの ``.md`` 文書 / learner and instructor ``.md`` documents

触らないもの / Never touched
---------------------------
* コードセル、実行結果、セル ID、メタデータ、添付ファイル
  code cells, saved outputs, cell ids, metadata, attachments
* フェンス付きコードブロック、インラインコード、数式、URL、HTML 属性
  fenced code blocks, inline code, math, URLs, HTML attributes
* ``日本語フォント`` のような意味のある語 / meaningful terms such as
  ``日本語フォント`` (the pattern only matches a *line-leading label*)

使い方 / Usage
--------------
    python assets\\scripts\\normalize_language_labels.py --check
    python assets\\scripts\\normalize_language_labels.py
    python assets\\scripts\\normalize_language_labels.py --root . --json

``--check`` は書き換えず、必要な変更があるときだけ終了コード 1 を返します。
``--check`` never writes; it exits with 1 when a change would be required.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import nbformat
from course_notebooks import course_notebooks

# ---------------------------------------------------------------------------
# 正規表現 / patterns
# ---------------------------------------------------------------------------

JP_RE = re.compile(r"[\u3040-\u30ff\u4e00-\u9fff\u3005\u3006]")

# ``` または ~~~ で始まるフェンス / a fenced code block delimiter
FENCE_RE = re.compile(r"^\s{0,3}(?P<fence>`{3,}|~{3,})")

HEADING_RE = re.compile(r"^(?P<hashes>#{1,6})(?P<spacing>[ \t]+)(?P<body>.*)$")

# 行頭の「> 」「- 」「1. 」など / line-leading quote or list markers
PREFIX_RE = re.compile(r"^(?P<prefix>[ \t]*(?:>[ \t]*)*(?:[-*+][ \t]+|\d+[.)][ \t]+)?)(?P<body>.*)$")

# ``**日本語：**`` / ``**English**：`` / ``日本語：``
LABEL_RE = re.compile(
    r"(?:\*\*(?:日本語|English)[ \t]*[：:]\*\*)"      # **日本語：**
    r"|(?:\*\*(?:日本語|English)\*\*[ \t]*[：:])"     # **日本語**：
    r"|(?:(?:日本語|English)[ \t]*[：:])"             # 日本語：
)

LABEL_ONLY_RE = re.compile(r"^[ \t]*(?:" + LABEL_RE.pattern + r")[ \t]*$")

ENGLISH_WORD = "English"


@dataclass
class Change:
    """1 ファイル分の変更内容 / change report for one file."""

    path: str
    cells_changed: int = 0
    lines_changed: int = 0
    removed_label_lines: int = 0
    heading_labels_removed: int = 0
    english_headings_moved: int = 0
    english_headings_dropped: int = 0
    details: list[str] = field(default_factory=list)

    @property
    def changed(self) -> bool:
        return bool(self.cells_changed or self.lines_changed)

    def as_dict(self) -> dict:
        return {
            "path": self.path,
            "cells_changed": self.cells_changed,
            "lines_changed": self.lines_changed,
            "removed_label_lines": self.removed_label_lines,
            "heading_labels_removed": self.heading_labels_removed,
            "english_headings_moved": self.english_headings_moved,
            "english_headings_dropped": self.english_headings_dropped,
        }


# ---------------------------------------------------------------------------
# Markdown 変換 / markdown transformation
# ---------------------------------------------------------------------------


def _strip_label(body: str) -> tuple[str, bool] | None:
    """行頭の言語ラベルを取り除く / strip a leading language label.

    Returns ``(remainder, was_english)`` or ``None`` when there is no label.
    """
    match = LABEL_RE.match(body)
    if not match:
        return None
    label = match.group(0)
    remainder = body[match.end():]
    # ラベルの直後の空白だけを落とす / drop only the spaces right after the label
    remainder = remainder.lstrip(" \t")
    return remainder, ENGLISH_WORD in label


def _strip_heading_label(body: str) -> tuple[str, bool] | None:
    match = LABEL_RE.match(body.lstrip(" \t"))
    if not match:
        return None
    label = match.group(0)
    remainder = body.lstrip(" \t")[match.end():].strip(" \t")
    return remainder, ENGLISH_WORD in label


def _collapse_blank_runs(lines: list[str], max_blank: int = 1) -> list[str]:
    """削除で生じた余分な空行を詰める。フェンス内は触らない。

    Squash blank-line runs created by removing a label, but never inside a fenced
    code block where blank lines are part of the example.
    """
    result: list[str] = []
    blanks = 0
    in_fence = False
    fence_char = ""
    for line in lines:
        fence = FENCE_RE.match(line)
        if fence:
            char = fence.group("fence")[0]
            if not in_fence:
                in_fence, fence_char = True, char
            elif char == fence_char:
                in_fence, fence_char = False, ""
            result.append(line)
            blanks = 0
            continue
        if in_fence:
            result.append(line)
            continue
        if line.strip():
            blanks = 0
            result.append(line)
            continue
        blanks += 1
        if blanks <= max_blank:
            result.append(line)
    return result


def _heading_split(line: str) -> tuple[str, str] | None:
    match = HEADING_RE.match(line)
    if not match:
        return None
    return match.group("hashes"), match.group("body").strip()


def _relocate_english_headings(lines: list[str], english_headings: set[int]) -> tuple[list[str], int, int]:
    """英語見出しが英語段落の後に来ていたら、段落の前に移す。

    Moves an English heading that ended up *after* its English paragraph back in
    front of that paragraph, so every section reads ``heading`` → ``body``.  A
    heading that merely repeats the English half of a bilingual heading such as
    ``#### 理解度チェック / Understanding questions`` is dropped instead.

    Returns ``(lines, moved, dropped)``.
    """
    moved = 0
    dropped = 0
    for index in sorted(english_headings, reverse=True):
        if index >= len(lines):
            continue
        last_japanese = None
        for k in range(index - 1, -1, -1):
            if lines[k].strip() and JP_RE.search(lines[k]):
                last_japanese = k
                break
        if last_japanese is None:
            continue

        # 二言語見出しの英語側と重複していたら削除 / drop a duplicate of "JA / EN"
        split = _heading_split(lines[index])
        closest_heading = None
        for k in range(last_japanese, -1, -1):
            candidate = _heading_split(lines[k])
            if candidate is not None:
                closest_heading = candidate
                break
        if (closest_heading is not None and split is not None
                and JP_RE.search(closest_heading[1]) and "/" in closest_heading[1]):
            english_half = closest_heading[1].split("/", 1)[1].strip()
            if english_half.casefold() == split[1].casefold():
                lines.pop(index)
                dropped += 1
                continue

        between = [k for k in range(last_japanese + 1, index) if lines[k].strip()]
        if not between or any(JP_RE.search(lines[k]) for k in between):
            continue
        insert_at = last_japanese + 1
        while insert_at < index and not lines[insert_at].strip():
            insert_at += 1
        heading = lines.pop(index)
        lines.insert(insert_at, heading)
        moved += 1
    return lines, moved, dropped


def clean_markdown_text(text: str, stats: Change | None = None) -> str:
    """Markdown 文字列から言語ラベルを取り除く / clean one markdown string."""
    stats = stats if stats is not None else Change(path="<memory>")
    lines = text.split("\n")
    out: list[str] = []
    english_headings: set[int] = set()
    in_fence = False
    fence_char = ""

    for raw in lines:
        fence = FENCE_RE.match(raw)
        if fence:
            char = fence.group("fence")[0]
            if not in_fence:
                in_fence, fence_char = True, char
            elif char == fence_char:
                in_fence, fence_char = False, ""
            out.append(raw)
            continue
        if in_fence:
            out.append(raw)
            continue

        # --- 見出し / heading -------------------------------------------------
        heading = HEADING_RE.match(raw)
        if heading:
            stripped = _strip_heading_label(heading.group("body"))
            if stripped is not None:
                title, was_english = stripped
                stats.heading_labels_removed += 1
                stats.lines_changed += 1
                if not title:
                    continue
                new_line = f"{heading.group('hashes')} {title}"
                out.append(new_line)
                if was_english:
                    english_headings.add(len(out) - 1)
                continue
            out.append(raw)
            continue

        # --- 本文 / paragraph ---------------------------------------------------
        prefix = PREFIX_RE.match(raw)
        body = prefix.group("body") if prefix else raw
        leading = prefix.group("prefix") if prefix else ""
        stripped = _strip_label(body)
        if stripped is not None:
            remainder, was_english = stripped
            stats.lines_changed += 1
            if not remainder:
                # 言語ラベルだけの段落は削除 / a label-only paragraph disappears
                stats.removed_label_lines += 1
                continue
            out.append(leading + remainder)
            if was_english:
                stats.details.append(f"english-body: {remainder[:60]}")
            continue

        out.append(raw)

    out, moved, dropped = _relocate_english_headings(out, english_headings)
    out = _collapse_blank_runs(out)
    stats.english_headings_moved += moved
    stats.english_headings_dropped += dropped
    return "\n".join(out)


def clean_markdown_lines(text: str) -> str:
    return clean_markdown_text(text)


# ---------------------------------------------------------------------------
# ノートブック / notebooks
# ---------------------------------------------------------------------------


def _source_to_text(source) -> str:
    return "".join(source) if isinstance(source, list) else source


def _text_to_source(text: str) -> list[str]:
    if not text:
        return []
    parts = text.split("\n")
    return [line + "\n" for line in parts[:-1]] + ([parts[-1]] if parts[-1] else [])


def clean_notebook(path: Path, write: bool = True) -> Change:
    """Markdown セルだけを整理する / clean markdown cells of one notebook."""
    record = Change(path=str(path))
    notebook = nbformat.read(str(path), as_version=4)
    for index, cell in enumerate(notebook.cells):
        if cell.get("cell_type") != "markdown":
            continue
        original = _source_to_text(cell.get("source", ""))
        cleaned = clean_markdown_text(original, record)
        if cleaned != original:
            record.cells_changed += 1
            cell["source"] = _text_to_source(cleaned)
            record.details.append(f"cell {index}")
    if write and record.changed:
        nbformat.write(notebook, str(path))
    return record


def clean_markdown_file(path: Path, write: bool = True) -> Change:
    record = Change(path=str(path))
    original = path.read_text(encoding="utf-8")
    cleaned = clean_markdown_text(original, record)
    if cleaned != original:
        record.cells_changed = 1
        if write:
            path.write_text(cleaned, encoding="utf-8", newline="\n")
    return record


# ---------------------------------------------------------------------------
# 対象の収集 / discovery
# ---------------------------------------------------------------------------

DOC_GLOBS = (
    "*.md",
    "docs/**/*.md",
    "submissions/**/*.md",
    "requirements/**/*.md",
    "assets/**/*.md",
)


def iter_targets(root: Path) -> list[Path]:
    targets: list[Path] = []
    notebooks = root / "notebooks"
    if notebooks.is_dir():
        targets.extend(course_notebooks(notebooks))
    for pattern in DOC_GLOBS:
        targets.extend(sorted(root.glob(pattern)))
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in targets:
        resolved = path.resolve()
        if resolved in seen:
            continue
        if any(part in {".git", ".venv", ".venv-anomalib", "__pycache__", ".pytest_cache",
                        ".ipynb_checkpoints"}
               for part in resolved.parts):
            continue
        seen.add(resolved)
        unique.append(path)
    return unique


def run(root: Path, write: bool = True) -> list[Change]:
    changes: list[Change] = []
    for path in iter_targets(root):
        if path.suffix == ".ipynb":
            changes.append(clean_notebook(path, write=write))
        elif path.suffix == ".md":
            changes.append(clean_markdown_file(path, write=write))
    return changes


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Remove repetitive Japanese/English language labels.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--check", action="store_true", help="report only; never write")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    changes = run(root, write=not args.check)
    touched = [c for c in changes if c.changed]

    if args.json:
        print(json.dumps([c.as_dict() for c in touched], indent=2, ensure_ascii=False))
    else:
        for record in touched:
            relative = Path(record.path).resolve().relative_to(root) if Path(record.path).exists() else record.path
            print(f"{relative}: cells={record.cells_changed} lines={record.lines_changed} "
                  f"label_lines={record.removed_label_lines} headings={record.heading_labels_removed} "
                  f"moved={record.english_headings_moved} dropped={record.english_headings_dropped}")
        total_lines = sum(c.lines_changed for c in touched)
        print("-" * 70)
        print(f"files={len(touched)} lines={total_lines}")
        if args.check:
            print("RESULT:", "CHANGES NEEDED" if touched else "CLEAN")
        else:
            print("RESULT:", "UPDATED" if touched else "ALREADY CLEAN")
    if args.check and touched:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
