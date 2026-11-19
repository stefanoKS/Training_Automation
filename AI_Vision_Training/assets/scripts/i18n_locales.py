"""学習資料の言語設定 / the locales the course can carry.

Every locale is described once, here, so the insertion tools, the coverage checker and the PDF
exporter all read the same facts: which marker wraps a translated region, which BCP 47 tag the PDF
declares, which script the text is written in, and whether the variety has been confirmed with the
trainees.

Two locales exist today:

``ne``
    ローマ字表記のネパール語 (``ne-Latn``). Legacy: kept for rollback only, **not** learner-facing
    after the Tamang migration. Written in Latin letters, validated against the Romanized Nepali
    lexicon.

``taj``
    Tamang, provisionally **Eastern Tamang in Devanagari (``taj-Deva``)**. Tamang is a
    Tibeto-Burman language of Nepal; it is **not** Nepali (Indo-Aryan) and not a script variant of
    it. ``Western Tamang`` is a separate language (``tdg``) and must not be mixed in. The variety and
    script stay **unconfirmed** until the trainees' preference is established, so every ``taj``
    catalog is marked provisional and its review status is what decides whether it may be shown.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

COURSE_ROOT = Path(__file__).resolve().parents[2]
I18N_ROOT = COURSE_ROOT / "assets" / "i18n"

DEVANAGARI_RE = re.compile(r"[\u0900-\u097f]")
LEGACY_REGION_RE = re.compile(
    r"^[ \t]*<!--[ \t]*ne:begin[ \t]+[^\n]*?-->[ \t]*\n"
    r".*?^[ \t]*<!--[ \t]*ne:end[ \t]*-->[ \t]*(?:\n|$)", re.M | re.S)


def without_legacy(text: str) -> str:
    return LEGACY_REGION_RE.sub("\n", text)


def has_devanagari_letters(text: str) -> bool:
    return any(character.isalpha() and DEVANAGARI_RE.fullmatch(character) for character in text)


@dataclass(frozen=True)
class Locale:
    code: str                 # catalog folder and marker name, e.g. "taj"
    tag: str                  # BCP 47 tag for the PDF text layer, e.g. "taj-Deva"
    label: str                # human-readable name used in reports
    script: str               # "devanagari" or "romanized"
    confirmed: bool           # has the variety/script been confirmed with the trainees?
    variety: str              # which variety the catalog claims to hold
    learner_facing: bool      # may this locale appear in a learner-facing booklet?
    note: str = ""

    @property
    def marker(self) -> str:
        return self.code

    @property
    def catalog_root(self) -> Path:
        return I18N_ROOT / self.code

    def catalog_dir(self, kind: str) -> Path:
        return self.catalog_root / kind

    def region_re(self) -> re.Pattern:
        return re.compile(
            r"\n<!--\s*" + self.code + r":begin\s+(?P<anchor>[^\s]+)\s*-->\n"
            r"(?P<body>.*?)\n<!--\s*" + self.code + r":end\s*-->\n", re.S)

    def cell_directive_re(self) -> re.Pattern:
        return re.compile(r"^<!--\s*" + self.code + r"-cell:\s*([A-Za-z0-9_\-]+)\s*"
                          r"(?:\|\s*([^\s]+)\s*)?-->$")

    def pending_directive_re(self) -> re.Pattern:
        return re.compile(r"^<!--\s*" + self.code + r"-pending:\s*([A-Za-z0-9_\-]+)\s*"
                          r"(?:\|\s*(.+?)\s*)?-->$")

    def doc_pending_directive_re(self) -> re.Pattern:
        """文書の pending は見出し行をキーにする / document pending lines are keyed by heading."""
        return re.compile(r"^<!--\s*" + self.code + r"-pending:\s*(?P<key>.+?)\s*\|\s*"
                          r"(?P<reason>.+?)\s*-->$")

    def status_directive_re(self) -> re.Pattern:
        return re.compile(r"^<!--\s*" + self.code + r"-status:\s*([A-Za-z0-9_\-]+)\s+"
                          r"(approved|draft)\s*-->$")

    def doc_status_directive_re(self) -> re.Pattern:
        return re.compile(r"^<!--\s*" + self.code
                          + r"-status:\s*(?P<key>.+?)\s*\|\s*(?P<status>approved|draft)\s*-->$")

    def doc_re(self) -> re.Pattern:
        return re.compile(r"^<!--\s*" + self.code + r"-doc:\s*(?P<path>[^\s]+)\s*-->$")

    def section_directive_re(self) -> re.Pattern:
        return re.compile(r"^<!--\s*" + self.code + r"-section:\s*(?P<heading>.+?)\s*-->$")

    def doc_region_re(self) -> re.Pattern:
        return re.compile(
            r"\n<!--\s*" + self.code + r":begin\s+doc:(?P<slug>[0-9a-f]+)\s*-->\n"
            r"(?P<body>.*?)\n<!--\s*" + self.code + r":end\s*-->\n", re.S)

    def pdf_suffix(self) -> str:
        return f"ja_en_{self.code}"


LOCALES: dict[str, Locale] = {
    "ne": Locale(
        code="ne",
        tag="ne-Latn",
        label="Romanized Nepali (legacy)",
        script="romanized",
        confirmed=True,
        variety="Nepali, Latin transliteration",
        learner_facing=False,
        note="Kept for rollback only after the Tamang migration; never presented as Tamang.",
    ),
    "taj": Locale(
        code="taj",
        tag="taj-Deva",
        label="Tamang (provisional Eastern Tamang, Devanagari)",
        script="devanagari",
        confirmed=False,
        variety="Eastern Tamang, Devanagari; Western Tamang (tdg) is a separate language",
        learner_facing=True,
        note="UNCONFIRMED variety and script: confirm with the trainees before classroom use.",
    ),
}


def locale(code: str) -> Locale:
    try:
        return LOCALES[code]
    except KeyError as error:
        raise SystemExit(f"unknown locale {code!r}; known: {', '.join(sorted(LOCALES))}") from error
