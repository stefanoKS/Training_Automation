"""既存のネパール語カタログをローマ字表記へ移行する / Rewrite the Nepali catalogs in Latin letters.

The canonical source stays ``assets/i18n/ne/...``; only the script changes: Devanagari Nepali
becomes Romanized Nepali (``ne-Latn``). Structure is preserved byte for byte — directives,
``ne-pair`` comments, image anchors, tables, code fences and Latin technical tokens.

使い方 / Usage
--------------
    python assets\\scripts\\convert_nepali_to_latin.py --check      # 点検のみ / report only
    python assets\\scripts\\convert_nepali_to_latin.py --write      # 書き込み / write
    python assets\\scripts\\convert_nepali_to_latin.py --only Day04 --write
    python assets\\scripts\\convert_nepali_to_latin.py --review     # 未登録語の一覧 / unglossed words
"""

from __future__ import annotations

import argparse
import collections
import re
import sys
from pathlib import Path

from romanize_nepali import DEVANAGARI_RE, GLOSSARY, RUN_RE, romanize_text

COURSE_ROOT = Path(__file__).resolve().parents[2]
CATALOG_ROOT = COURSE_ROOT / "assets" / "i18n" / "ne"


def catalogs(only: str | None = None, scope: str = "all") -> list[Path]:
    paths: list[Path] = []
    if scope in ("all", "notebooks"):
        paths += sorted((CATALOG_ROOT / "notebooks").glob("*.ne.md"))
    if scope in ("all", "docs"):
        paths += sorted((CATALOG_ROOT / "docs").glob("*.ne.md"))
    if only:
        paths = [path for path in paths if only in path.name]
    return paths


def convert(path: Path, write: bool) -> dict:
    original = path.read_text(encoding="utf-8")
    converted = romanize_text(original)
    leftover = DEVANAGARI_RE.findall(converted)
    return {
        "path": path.relative_to(COURSE_ROOT).as_posix(),
        "changed": converted != original,
        "leftover": len(leftover),
        "chars": len(original),
        "written": write and converted != original,
        "text": converted,
    }


def review_words(paths: list[Path]) -> list[tuple[str, int, str]]:
    counts: collections.Counter = collections.Counter()
    for path in paths:
        for run in RUN_RE.findall(path.read_text(encoding="utf-8")):
            word = run.strip("।॥.,;:!?()[]\"'")
            if word and DEVANAGARI_RE.search(word) and word not in GLOSSARY:
                counts[word] += 1
    return [(word, count, romanize_text(word)) for word, count in counts.most_common()]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Romanize the Nepali catalogs.")
    parser.add_argument("--write", action="store_true", help="write the catalogs")
    parser.add_argument("--check", action="store_true", help="report only (the default)")
    parser.add_argument("--only", default=None, help="substring of the catalog file name")
    parser.add_argument("--scope", choices=("all", "notebooks", "docs"), default="all",
                        help="which catalogs to convert")
    parser.add_argument("--review", action="store_true",
                        help="list words that fall back to the rule engine")
    args = parser.parse_args(argv)

    targets = catalogs(args.only, args.scope)
    if not targets:
        print(f"[error] no catalog matched {args.only!r}")
        return 1
    if args.review:
        for word, count, roman in review_words(targets):
            print(f"{count:>4}  {word}  ->  {roman}")
        return 0

    problems = 0
    pending = 0
    for path in targets:
        result = convert(path, args.write)
        pending += int(result["changed"])
        if result["leftover"]:
            problems += 1
            print(f"[leftover] {result['path']}: {result['leftover']} Devanagari character(s) remain")
        state = "written" if result["written"] else ("pending" if result["changed"] else "unchanged")
        print(f"[{state}] {result['path']}")
        if args.write and result["changed"]:
            path.write_text(result["text"], encoding="utf-8")
    verb = "written" if args.write else "would change"
    print(f"[done] {pending} catalog(s) {verb}; {problems} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
