# Day 4 / Day 5 fixes and Romanized Nepali pilot — implementation log

**Repository:** `stefanoKS/Training_Automation`
**Starting commit:** `83423d81573098a5653f5415ae7c6a17fbf9d6e0`
**Scope delivered:** Day 4 and Day 5 notebooks (technical/pedagogical fixes plus a safe evaluation
workflow), all 12 learner documents and the six Day 4/5 notebook catalogues migrated to **Romanized
Nepali** (`ne-Latn`), the trilingual PDF exporter refactored to carry explicit language provenance,
and the ten trilingual PDFs rebuilt. Days 1–3 notebook catalogues stay in Devanagari until this
pilot is approved (pilot decision recorded with the requester).

## Method

* **Notebook fixes** were made against the actual source and the pinned library
  (`ultralytics==8.4.211`, `anomalib`), not against remembered API behaviour. Each change below
  states what was wrong.
* **Romanization** is not a blind `str.replace`. `assets/scripts/romanize_nepali.py` holds the
  published spelling rules (final-schwa deletion, `व`→`b`, `ी`/`ू`→`i`/`u`, postposition spacing)
  plus a reviewed `GLOSSARY` of the words this course uses. `assets/scripts/convert_nepali_to_latin.py`
  applies it, is idempotent, and reports every word that falls back to the rule engine so a reviewer
  can see the queue. The output is real Nepali grammar in Latin letters; English text is rejected by
  `looks_like_nepali_latin()` (vocabulary + English-function-word guard), never accepted because it
  happens to contain Latin letters.
* No image, SVG, checkpoint, model or dataset byte was regenerated or edited.

## Phase 1 — Day 4

### `Day04_01_YOLO_Dataset_Annotation.ipynb`

| Cell | Change |
|---|---|
| `ef0229c6` | The duplicate check now reports **three separate numbers**: `files_scanned`, `unique_hashes` (`distinct images`) and `duplicate_pairs`. Previously `len(seen)` was printed as "images checked", which is the number of distinct hashes, not files. |
| `aa01b7fd` | Exercise 3 runs inside `tempfile.TemporaryDirectory()` on a throw-away copy of `images/`. `demonstrate_leakage()` refuses to overwrite an existing target, uses `try/finally`, verifies the fixture is restored, and the cell asserts the live dataset is unchanged. An interrupted cell can no longer leave `leak_test.png` inside `assets/yolo_dataset`. |
| `396d4a73` | Explains the three counts in JA/EN/Romanized Nepali and why one duplicate pair makes the file count one higher than the distinct count. |
| `c892d3b2` | Adds the requested sentence: resizing without cropping preserves normalised geometry; a crop, spatial warp, or an annotation not updated with the image does not. |

### `Day04_02_YOLO_Training.ipynb`

| Cell | Change |
|---|---|
| `clarity-batch-interpret` | `15 × 8 = 120` is now named **data-loader iterations**, explicitly not 120 dataset reads (the dataset is read 15 times) and not 120 weight updates. All three languages updated. |
| `16c0469f` | Loss is described as usually falling but not monotonically; a falling training loss alone does not show generalisation. The epoch bullet also states the 8 loader iterations per epoch. |
| `388c5d1c` | `l1_loss` is described as L1 on **normalised box distances** (edge distances in grid units), matching `F.l1_loss(pred_dist, target_ltrb)` in the pinned package's DFL-free path (`loss_names = ("box_loss","cls_loss","l1_loss")`, `reg_max <= 1`). The falling-loss paragraph now separates training loss, overfitting and validation metrics. |

### `Day04_03_YOLO_Evaluation.ipynb`

| Cell | Change |
|---|---|
| `612e7d6a` | States that the next cell stops until a freeze declaration is recorded, and defines the two honest labels (illustrative/reused-data vs declared untouched). |
| `0865c09d` | Runnable gate: `FREEZE_DECLARATION` (empty by default → `ValueError`), `TEST_ALREADY_SEEN=True` by default, `assessment_role` printed, and `submissions/day04/test_evaluation_record.json` written with weights, split, settings, declaration and metrics. Run-All can no longer silently present a test score as independent. |
| `968ad99b` | The "recall cannot increase" statement is now explicitly conditional on a fixed detection list, fixed truth, fixed matching and fixed postprocessing. |
| `c479853d` | One bracketed note that implementations interpolate the PR curve before integrating, so the beginner definition stays honest without becoming a lecture. |

## Phase 2 — Day 5

### `Day05_01_Anomaly_Detection_Concepts.ipynb`

| Cell | Change |
|---|---|
| `74117d66` | No longer scans `test/` or prints its normal/abnormal breakdown before the freeze. It shows normal training images and the synthetic teaching samples in `assets/defect_samples/`, and says plainly that the evaluation composition stays hidden. |
| `ef2014d3` | JA/EN/Romanized note explaining what the cell shows and why a preview would turn the later assessment into reused data. |

### `Day05_02_PatchCore_Training.ipynb`

| Cell | Change |
|---|---|
| `82f543da` | Scores **calibration only** (`datamodule.val_dataloader()`); no test prediction before the freeze. |
| `1c4cd018` | Writes a calibration-only `patchcore_predictions.json` (`scored_partitions`, `test_scored: false`); no test class counts are printed. |
| `39a9c510` | Numeric maps are written for calibration images only; the test maps moved to the sealed stage. |
| `748dffdf` | JA/EN/Romanized text updated to match. |
| `clarity-sealed-test` / `clarity-sealed-test-scoring` (new) | Post-freeze stage. Requires `submissions/day05/comparison_freeze_record.json`, verifies the frozen model, split and declaration against the live notebook, and scores test **once**, writing `patchcore_test_predictions.json` plus the test numeric maps. Re-running prints a reproducibility notice instead of silently re-scoring. |

### `Day05_03_YOLO_vs_PatchCore.ipynb`

| Cell | Change |
|---|---|
| `39ee7a27` | Rejects a PatchCore artifact that already contains test rows (`test_scored` or `partition == "test"`), so a stale pre-freeze file cannot be reused. |
| `be4aa133` | Artifact table now lists the calibration-only file and the sealed test file. |
| `d26eb085` | Strict calibration coverage: unique IDs per method, complete manifest coverage, no unknown IDs, no non-calibration rows, `ValueError` otherwise. An explicit `ALLOW_PARTIAL_COMPARISON = False` flag keeps a labelled, non-final exploratory branch for teaching (it prints **EXPLORATORY, NOT FINAL** and records exclusions). |
| `cccf0ff7` | Builds the calibration frame only, rejects duplicate IDs instead of `drop_duplicates`, checks truth agreement and row counts. Test scores are not read yet. |
| `clarity-sealed-test-read` / `clarity-load-sealed-test` (new, after `clarity-freeze-record`) | Reads the sealed test predictions, verifies schema, model, score convention, frozen threshold, unique IDs, complete test coverage and truth agreement, then builds `test_frame`. It never re-scores. |
| `clarity-freeze-record` (unchanged behaviour) | Still records declaration, assessment role, thresholds, model, postprocessor, score convention and split. |

## Phase 3 — Romanized Nepali (`ne-Latn`)

### New and changed tooling

| File | Purpose |
|---|---|
| `assets/scripts/romanize_nepali.py` | Spelling rules, reviewed `GLOSSARY`, `looks_like_nepali_latin()` (positive detection: Nepali markers plus an English-function-word guard), `nepali` marker set derived from the glossary so the two cannot drift. |
| `assets/scripts/convert_nepali_to_latin.py` | `--check`, `--write`, `--only`, `--scope {all,notebooks,docs}`, `--review`. Idempotent; reports any leftover Devanagari. |
| `assets/scripts/apply_nepali_translations.py` | Accepts a block only when it is Devanagari Nepali **or** Romanized Nepali; caption prefixes now include `chitra:`/`Chitra:`/`tasbir:`. |
| `assets/scripts/apply_nepali_docs.py` | Same block validation for documents. |
| `assets/scripts/check_nepali_coverage.py` | Per-block script classification (`devanagari`/`romanized`/`unverified`), per-catalog all-or-nothing script, unverified-block failures, Latin Hindi guard. |
| `assets/i18n/ne/romanization_style_guide.md` | 40-term approved glossary, spelling rules, review checklist. |

### Catalogs migrated (18)

* Notebooks: `Day04_01`, `Day04_02`, `Day04_03`, `Day05_01`, `Day05_02`, `Day05_03`.
* Documents (12): `START_HERE`, `README`, `COURSE_SYLLABUS`, `installation`, `reference_materials`,
  `pdf/README`, `tested_versions`, and the five report templates.

Days 1–3 notebook catalogs remain Devanagari and are reported as such, rather than being silently
half-converted.

### Exporter (`assets/scripts/export_trilingual_pdf.py`)

* `glyph_language()` now decides only Japanese vs English; **Nepali comes from provenance**:
  `nepali_lines()` collects the line ranges inside `ne:` regions and every renderer receives that
  context. Romanized Nepali can no longer be misclassified as English.
* `markdown_cell_html(..., force_language="ne")` renders figure notes and Nepali captions with their
  own language; captions keep their image (`caption_languages`).
* Every Nepali element carries `lang="ne-Latn"`: headings, paragraphs, notes, list items, table
  cells, figure captions and TOC entries. Japanese uses `lang="ja"`, English `lang="en"`.
* `notebook_title()` reads the Nepali title from the region, not from Devanagari glyphs.
* CSS: `.ne` inherits the body stack (Latin first, Devanagari fallback for Days 1–3); the built-in
  cover, about page, day metadata and document labels are Romanized Nepali.
* `check_devanagari_font()` became `check_fonts(page, needs_devanagari)`: the Latin probe must
  resolve to a real font for every booklet; the Devanagari probe runs only when the HTML still
  contains Devanagari. A Latin-only booklet no longer requires a Devanagari font.
* PDF metadata subject now names the Romanized Nepali third language.

## Phase 4 — PDFs rebuilt

| File | Pages | Size |
|---|---|---|
| `Day01_explanation_ja_en_ne.pdf` | 95 | 8,151 KB |
| `Day02_explanation_ja_en_ne.pdf` | 112 | 4,862 KB |
| `Day03_explanation_ja_en_ne.pdf` | 75 | 3,934 KB |
| `Day04_explanation_ja_en_ne.pdf` | 88 | 5,420 KB |
| `Day05_explanation_ja_en_ne.pdf` | 86 | 6,955 KB |
| `Week1_explanation_ja_en_ne.pdf` | 445 | 24,289 KB |
| `Setup_ja_en_ne.pdf` | 39 | 1,738 KB |
| `Installation_Guide_ja_en_ne.pdf` | 23 | 634 KB |
| `Repository_Guide_ja_en_ne.pdf` | 23 | 682 KB |
| `Course_Syllabus_ja_en_ne.pdf` | 20 | 536 KB |

Text-layer check (extracted with pypdfium2):

| PDF | Devanagari characters | Romanized markers |
|---|---|---|
| Day04 | 0 | 254 |
| Day05 | 0 | 283 |
| Installation_Guide | 0 | 66 |
| Course_Syllabus | 0 | 28 |
| Setup | Devanagari present (`00_Setup` is not migrated yet) | 39 |
| Week1 | 103,493 (Days 1–3 only) | 579 |

Rendered pages inspected with pypdfium2 (reproducible with
`python assets\scripts\inspect_pdf_pages.py`): `Day04` p1/p3 (front matter, TOC) and p20 (table and
prose), `Day05` p41 (figure page), `Course_Syllabus` p4, `Installation_Guide` p7. Captions stay under
their own image, the Nepali question follows the caption, TOC page numbers pair with the body, and
command lines wrap without overflow.

## Machine-checked change inventory

Comparing each notebook against `HEAD` (cell ids, code-cell source, metadata, outputs,
`execution_count`):

```
Day04_01  added=[]                      removed=[]  changed code cells=[ef0229c6, aa01b7fd]
Day04_02  added=[]                      removed=[]  changed code cells=[]
Day04_03  added=[]                      removed=[]  changed code cells=[0865c09d]
Day05_01  added=[]                      removed=[]  changed code cells=[74117d66]
Day05_02  added=[clarity-sealed-test, clarity-sealed-test-scoring]
                                               changed code cells=[82f543da, 1c4cd018, 39a9c510]
Day05_03  added=[clarity-sealed-test-read, clarity-load-sealed-test]
                                               changed code cells=[39ee7a27, d26eb085, cccf0ff7]
```

No cell id was removed, no `execution_count` or saved output changed, and no code cell changed outside
the list above. Day 1–3 notebooks, every PNG/SVG, every checkpoint and every dataset file are
byte-identical to `HEAD` (`git status` shows no modified figure or model path).

## Tests and acceptance gates

| Command | Result |
|---|---|
| `python assets\scripts\validate_notebooks.py --execute none` | `passed=194 failed=0 skipped=0`, `RESULT: OK` |
| `python -m pytest assets\tests -q` | **419 passed**, 0 failed, 0 deselected (baseline at the starting commit: 404 passed) |
| `convert_nepali_to_latin.py --check` (Day 4/5 notebooks, all docs) | `0 catalog(s) would change` |
| `apply_nepali_translations.py` / `apply_nepali_docs.py` (dry run) | `0 cells would change` / `0 documents would change` |
| `check_nepali_coverage.py --strict` | `0 missing`, `0 unverified`, `12/12` documents, 391 Romanized / 756 Devanagari regions |
| `git diff --check` | no whitespace errors |

New or strengthened tests:

* `test_audit_remediation.py`: three-count hash report, live dataset untouched, cleanup after an
  injected failure, refusal to overwrite a learner file, Day 4 test gate stops without a declaration.
* `test_evaluation_provenance.py`: only the sealed cell touches `test_dataloader()`; the freeze
  record precedes the sealed read; the sealed loader verifies model, score convention and threshold;
  strict comparison rejects duplicate IDs and incomplete calibration coverage.
* `test_trilingual_layout.py`: Romanized Nepali is tagged from provenance (`lang="ne-Latn"`), English
  is never tagged Nepali, a Romanized caption is grouped with its image, font preflight fails on
  `LastResort`.
* `test_nepali_localization.py`: Devanagari booklets keep searchable Devanagari; the migrated
  booklets carry Romanized prose and no Devanagari.

## Known limitations

1. **Native review is still required.** Automated tests prove structure, coverage and script; they
   cannot certify idiomatic fluency. The `--review` word list and the style-guide checklist are the
   hand-off for a Nepali reviewer.
2. **Days 1–3 notebooks and `00_Setup` are still Devanagari** (pilot decision). The Week1 booklet,
   the Day 1–3 booklets and the Setup booklet therefore mix scripts until those catalogs are migrated
   with the same command.
3. `Week1_explanation_ja_en_ne.pdf` was rebuilt because the exporter changed; its Days 1–3 content is
   unchanged apart from the Romanized front matter.
4. The Day 5 sealed stage needs the fitted model still loaded in the Notebook 02 kernel. If the kernel
   was restarted, the cell stops with an explicit message telling the learner to re-run Part 3 rather
   than silently producing a different model.
5. No push, merge or release was performed.
