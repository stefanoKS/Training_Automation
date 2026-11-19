"""ネパール語の翻訳を文書へ差し込む（互換ラッパー）/ legacy Nepali document entry point.

The engine now lives in ``apply_docs.py`` and takes a ``--locale``; this module binds the old names to
the ``ne`` locale so existing callers keep working::

    python assets\\scripts\\apply_nepali_docs.py            # dry run
    python assets\\scripts\\apply_nepali_docs.py --write    # write
"""

from __future__ import annotations

from functools import partial

import apply_docs as _generic
from i18n_locales import DEVANAGARI_RE, locale as _locale  # noqa: F401  (re-exported)

COURSE_ROOT = _generic.COURSE_ROOT
LOCALE = _locale("ne")
CATALOG_DIR = LOCALE.catalog_dir("docs")
REGION_RE = LOCALE.doc_region_re()
BEGIN = "<!-- ne:begin doc:{slug} -->"
END = "<!-- ne:end -->"
FORBIDDEN_LABELS = _generic.FORBIDDEN_LABELS
CatalogError = _generic.CatalogError

slug_of = _generic.slug_of
section_bounds = _generic.section_bounds
strip_regions = partial(_generic.strip_regions, loc=LOCALE)
apply_blocks = partial(_generic.apply_blocks, loc=LOCALE)
parse_catalog = partial(_generic.parse_catalog, loc=LOCALE)
apply_catalog = partial(_generic.apply_catalog, loc=LOCALE)
catalogs = partial(_generic.catalogs, LOCALE)


def main(argv=None) -> int:
    return _generic.main(argv, default_locale="ne")


if __name__ == "__main__":
    raise SystemExit(main())
