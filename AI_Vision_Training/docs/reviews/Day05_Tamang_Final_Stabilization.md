# Day 5 and Tamang final stabilization

Fetched `origin main` before editing. Its tip and the previously reviewed baseline
were both `357a89c`. The initial working tree was clean. The work is on
`stabilize/day5-tamang-final`; no push or merge was performed. Implementation
commits: `dd3dc52` (localization), `9ef2179` (Day 5), and `37e9744`
(rollback PDFs), followed by this report.

## Confirmed defects and corrections

| Area | Finding and correction |
|---|---|
| Day 5 freeze | An existing seal did not prevent recreation when the freeze JSON was missing. Either seal now blocks that write; an identical frozen record can be reused without rewriting it. |
| Day 5 archive | The assessment role could change after a YOLO-only seal. Either seal now prevents a late change. |
| Day 5 holdout | The pre-freeze summary displayed a total from which the TEST count could be derived. It no longer displays that total. The course distinguishes folder metadata from embargoed TEST labels, scores and metrics. |
| Day 5 recovery | The restart snippet depended on live kernel variables. The replacement shows how to restore the environment and checkpoint and verify the frozen fitted fingerprint and postprocessing state without calling `fit`. |
| Tamang coverage | Document coverage applied one aggregate state and could never reach per-section approval. Live JA/EN heading keys (qualified by parent headings when needed) replace partial keys from the rollback catalogs. The audit checks the catalog target, inserted anchors and text, explicit review decisions, reviewer identity, provenance, review date, script, and variety. |
| Tamang PDF | The day-job list holds tuples, not dictionaries. Both job types now use the same verified locale selection. The Tamang path drops legacy Nepali regions and uses approved source blocks for the third language; built-in labels without approved Tamang resources remain JA/EN. |

## Changed files

- [Day 5 notebooks](../../notebooks/Day05_PatchCore/),
  [Day 4/5 contract tests](../../assets/tests/test_day04_day05_contracts.py), and
  [clarity regression tests](../../assets/tests/test_clarity_review.py).
- [Pinned integration tests](../../assets/tests/test_day05_anomalib27_integration.py).
- [Coverage checker](../../assets/scripts/check_localization_coverage.py),
  [document inserter](../../assets/scripts/apply_docs.py),
  [notebook inserter](../../assets/scripts/apply_translations.py),
  [locale definitions](../../assets/scripts/i18n_locales.py), and
  [PDF exporter](../../assets/scripts/export_trilingual_pdf.py).
- [Localization tests](../../assets/tests/test_tamang_localization.py),
  [PDF fixture tests](../../assets/tests/test_tamang_pdf_renderer.py),
  and [pending-only Tamang catalogs and inventory](../../assets/i18n/taj/).
- [PDF index](../pdf/README.md) and the two rebuilt JA/EN/Nepali rollback companions:
  [Day 5](../pdf/Day05_explanation_ja_en_ne.pdf) and [Week 1](../pdf/Week1_explanation_ja_en_ne.pdf).

| Notebook | Modified cell IDs |
|---|---|
| Day05_01 | `b071950f`, `ef2014d3`, `74117d66` |
| Day05_02 | `43cbc7ba`, `01bf2bc9`, `83008bb8`, `f1a28c15`, `befc72c6`, `ba5da1ef`, `748dffdf`, `39a9c510`, `clarity-sealed-test`, `clarity-sealed-test-scoring` |
| Day05_03 | `1e496b72`, `d8230d25`, `clarity-freeze-prompt`, `clarity-freeze-record`, `clarity-load-sealed-test`, `9747ac10`, `clarity-archive-gate` |

The bilingual six-step navigation in Day05_03 points learners to the notebook, kernel,
and cell ID for each calibration, freeze, seal, and comparison. A rejected freeze
rerun retains the original frozen record in memory as well as on disk.

## Verification

| Gate | Executed result |
|---|---|
| Day 4/5 contracts, clarity, and provenance | 110 passed, 1 skipped (the base interpreter lacks `anomalib.post_processing`). |
| Tamang and rollback localization | 137 passed in the focused insertion/coverage and PDF fixture run. The separate legacy PDF layout regression run passed all 30 cases selected with the existing Tamang renderer checks. |
| Full pytest suite | `python -m pytest -q -rs`: 605 passed, 10 skipped, 4 non-interactive Matplotlib warnings (486.43 s). Nine tests require Anomalib 2.7.0 (base has 1.1.0dev) and one requires `anomalib.post_processing`. All ten passed separately using the pinned environment. |
| Notebook structure and code syntax | `python assets/scripts/validate_notebooks.py --execute none`: 194 passed, 0 failed. |
| Real model integration | 9 passed in 222.90 s with Anomalib 2.7.0 and Ultralytics 8.0.187 in separate CPU interpreters. Run the integration module with the Anomalib interpreter and set `DAY05_YOLO_PYTHON` to the separate YOLO interpreter. |
| Localization regeneration | Pending catalog generation wrote zero files on rerun; Tamang and Nepali notebook/document insertion dry runs reported zero changes and zero problems; the legacy coverage gate passed. |
| Preservation | No tracked changes to datasets, model files, submissions, results, figures, requirements, original Nepali catalogs, or `start_training.cmd`. The Day 5 and Week 1 rollback companions were rebuilt so their recovery headings and TOC page numbers match the updated notebooks (92 and 460 pages). Other PDFs were not changed. |
| Whitespace | `git diff --check 357a89c` passed. |

**Day 5 is ready for the synthetic classroom workflow.** Genuine YOLO inference,
checkpoint recovery without refitting, real PatchCore scoring and the sealed final
comparison ran in isolated directories. The test read all 26 genuine NPZ files and
verified image IDs, labels, shapes, values, and sealed digests; interruption before
seal publication rolled back, and a retry succeeded without rescoring an existing
seal. The runtime evidence verifies workflow and provenance, not model accuracy or
fitness for production inspection.

## Tamang readiness

**BLOCKED for classroom release.** The production gate returned exit `1`: zero
approvals, 656 pending notebook cells (147 exemptions) and 161 pending sections across
12 documents. The catalogs still say `pending-native-review`; trainees have not yet
confirmed the provisional Eastern Tamang variety and Devanagari script. No production
translations or approvals were added. The script check cannot establish linguistic
authenticity or independently authenticate a reviewer.

The approved-language test used isolated temporary fixtures, not a bypass of the
production gate. The real Chromium export produced a four-page day booklet and a
four-page document booklet. Tests checked matching TOC pagination, bookmarks,
Devanagari font resources, searchable Unicode, JA/EN text, figure embedding and no
legacy Nepali in the rendered fixture. A rasterized teaching page was also inspected
for shaped text, the three-language heading, split diagram, caption, and code. No
production Tamang PDF was generated.
