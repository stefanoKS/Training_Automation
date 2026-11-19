"""ネパール語の翻訳をノートブックへ差し込む（互換ラッパー）/ legacy Nepali entry point.

The engine now lives in ``apply_translations.py`` and takes a ``--locale``. This module keeps the
Nepali-specific names the rest of the course imports, bound to the ``ne`` locale, so existing
callers and the historical commands keep working unchanged::

    python assets\\scripts\\apply_nepali_translations.py            # dry run
    python assets\\scripts\\apply_nepali_translations.py --write    # write

Nepali (``ne-Latn``) is legacy material after the Tamang migration: it is kept for rollback and is
**not** learner-facing. Tamang lives in ``assets/i18n/taj/`` and is applied with
``apply_translations.py --locale taj``.
"""

from __future__ import annotations

from functools import partial

import apply_translations as _generic
from course_notebooks import course_notebooks  # noqa: F401  (re-exported for callers/tests)
from i18n_locales import DEVANAGARI_RE, locale as _locale  # noqa: F401  (re-exported)
from romanize_nepali import looks_like_nepali_latin  # noqa: F401  (re-exported)

COURSE_ROOT = _generic.COURSE_ROOT
LOCALE = _locale("ne")
CATALOG_DIR = LOCALE.catalog_dir("notebooks")

REGION_RE = LOCALE.region_re()
DIRECTIVE_RE = LOCALE.cell_directive_re()
BEGIN = "<!-- ne:begin {anchor} -->"
END = "<!-- ne:end -->"
FORBIDDEN_LABELS = _generic.FORBIDDEN_LABELS
VALID_ANCHORS = _generic.VALID_ANCHORS
IMAGE_RE = _generic.IMAGE_RE
CAPTION_RE = _generic.CAPTION_RE
CatalogError = _generic.CatalogError

valid_anchor = _generic.valid_anchor
image_captions = _generic.image_captions
parse_regions = partial(_generic.parse_regions, loc=LOCALE)
strip_regions = partial(_generic.strip_regions, loc=LOCALE)
apply_blocks = partial(_generic.apply_blocks, loc=LOCALE)
parse_catalog = partial(_generic.parse_catalog, loc=LOCALE)
apply_catalog = partial(_generic.apply_catalog, loc=LOCALE)
catalogs = partial(_generic.catalogs, LOCALE)


def main(argv=None) -> int:
    return _generic.main(argv, default_locale="ne")


if __name__ == "__main__":
    raise SystemExit(main())
