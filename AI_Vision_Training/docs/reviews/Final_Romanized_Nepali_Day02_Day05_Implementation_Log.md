# Final Romanized Nepali, Day 2 figure, and Day 5 evaluation safeguards — implementation log

Date: 2026-11-19
Course root: `AI_Vision_Training/`
Author: AI assistant (Copilot SDK in VS Code) on behalf of stefanoKS

This log separates **source inspection**, **automated execution**, **PDF rendering inspection** and
**human language review**. No claim here is a native-speaker certification of the Nepali wording.

---

## 1. Git commit before implementation

| Item | Value |
|---|---|
| Baseline SHA | `7beb09789e16e93a7c34e34e0397d0c055dc14de` |
| Baseline subject | `Implement Day 4/Day 5 fixes and Romanized Nepali pilot; add detailed implementation log and audit report` |
| Branch | `main` (local, not pushed) |
| Uncommitted changes at start | none (`git status --porcelain` empty) |

The SHA matched the "last reviewed commit" in the request, so no additional commits had to be
absorbed before starting.

## 2. Git commit after implementation

**Not committed.** The work stays in the working tree; nothing was pushed, merged or published.
`git status` lists **59 modified files** plus four new untracked paths (see §3); `git diff --stat`
reports 7 080 insertions and 6 299 deletions.

---

## 3. Complete changed-file list

### Romanized Nepali (`ne-Latn`)

| File | Change |
|---|---|
| `assets/i18n/ne/notebooks/00_Environment_Setup.ne.md` | Devanagari → Romanized |
| `assets/i18n/ne/notebooks/Day01_01_Introduction_to_AI.ne.md` | Devanagari → Romanized |
| `assets/i18n/ne/notebooks/Day01_02_Pixels_and_Images.ne.md` | Devanagari → Romanized |
| `assets/i18n/ne/notebooks/Day01_03_Computer_Vision_Tasks.ne.md` | Devanagari → Romanized |
| `assets/i18n/ne/notebooks/Day02_01_Python_Basics.ne.md` | Devanagari → Romanized |
| `assets/i18n/ne/notebooks/Day02_02_Conditions_Loops_Functions.ne.md` | Devanagari → Romanized |
| `assets/i18n/ne/notebooks/Day02_03_OpenCV_Image_Processing.ne.md` | Devanagari → Romanized; Day 2 figure block rewritten |
| `assets/i18n/ne/notebooks/Day03_01_YOLO_Concepts.ne.md` | Devanagari → Romanized |
| `assets/i18n/ne/notebooks/Day03_02_YOLO_Inference.ne.md` | Devanagari → Romanized |
| `assets/i18n/ne/notebooks/Day03_03_YOLO_Experiments.ne.md` | Devanagari → Romanized |
| `assets/i18n/ne/notebooks/Day04_0{1,2,3}*.ne.md` | Reviewed spellings applied (no re-translation) |
| `assets/i18n/ne/notebooks/Day05_0{1,2,3}*.ne.md` | Reviewed spellings applied; Day 5 navigation/provenance blocks rewritten |
| `assets/scripts/romanize_nepali.py` | Glossary 360 → 441 entries; duplicate keys removed; `_rule_romanize` split out; `glossary_respellings` + `apply_glossary_spellings` added |
| `assets/scripts/convert_nepali_to_latin.py` | Applies the glossary respelling pass to already-Latin catalogs |
| `assets/scripts/check_nepali_coverage.py` | `karna` dropped from the Hindi marker list (it is the Nepali hypotenuse) |
| `assets/i18n/ne/romanization_style_guide.md` | Rules 9 and 10, respelling safety note, three new glossary rows |
| `notebooks/**/**.ipynb` (16 files) | Nepali regions only; cell ids, code, metadata, outputs, execution counts untouched |
| `assets/i18n/ne/docs/pdf_README.ne.md`, `docs/pdf/README.md` | Removed the now-false "Day 1–3 are still Devanagari" claim; page counts refreshed |

### Day 2 figure

| File | Change |
|---|---|
| `assets/scripts/generate_teaching_diagrams.py` | `teach_threshold_sweep()` redesigned (4 panels + two separate graphs) |
| `assets/diagrams/teach_threshold_sweep.png` | Regenerated — the only image regenerated in this task |
| `notebooks/Day02_Python_OpenCV/Day02_03_OpenCV_Image_Processing.ipynb` | Cell `fig-teach_threshold_sweep` rewritten (JA / EN / ne-Latn) |
| `docs/visual_figure_manifest.md` | New section: asset, deterministic source, provenance, source-checked values |

### Day 5 evaluation

| File | Change |
|---|---|
| `assets/helpers/experiment_identity.py` | **New.** Fingerprints, identity, sealed validation, atomic write |
| `notebooks/Day05_PatchCore/Day05_02_PatchCore_Training.ipynb` | `clarity-sealed-test` (navigation), `clarity-sealed-test-scoring` (rewritten), `daed190f`, `1c4cd018`, `82f543da`, `39a9c510` |
| `notebooks/Day05_PatchCore/Day05_03_YOLO_vs_PatchCore.ipynb` | `clarity-freeze-record`, `clarity-sealed-test-read`, `clarity-load-sealed-test` |

### PDF regeneration

| File | Pages before → after (2026-11-16 → 2026-11-19) |
|---|---|
| `docs/pdf/Setup_ja_en_ne.pdf` | 39 → **41** |
| `docs/pdf/Day01_explanation_ja_en_ne.pdf` | 95 → **98** |
| `docs/pdf/Day02_explanation_ja_en_ne.pdf` | 112 → **115** |
| `docs/pdf/Day03_explanation_ja_en_ne.pdf` | 75 → **77** |
| `docs/pdf/Day04_explanation_ja_en_ne.pdf` | 88 → **88** |
| `docs/pdf/Day05_explanation_ja_en_ne.pdf` | 86 → **88** |
| `docs/pdf/Week1_explanation_ja_en_ne.pdf` | 445 → **455** |
| `docs/pdf/Installation_Guide_ja_en_ne.pdf` | 23 → **23** |
| `docs/pdf/Repository_Guide_ja_en_ne.pdf` | 23 → **23** |
| `docs/pdf/Course_Syllabus_ja_en_ne.pdf` | 20 → **20** |
| `docs/pdf/Day02_explanation_ja_en.pdf` | 86 → **88** (required: Day 2 figure) |
| `docs/pdf/Day05_explanation_ja_en.pdf` | 63 → **64** (required: Day 5 JA/EN navigation text) |
| `docs/pdf/Week1_explanation_ja_en.pdf` | 334 → **338** (required: Day 2 figure + Day 5 navigation) |
| `assets/scripts/export_explanations_pdf.py` | **Bug fix** — the JA/EN typesetter now strips the Nepali regions |

`docs/pdf/Day01_explanation_ja_en.pdf` (72), `Day03_explanation_ja_en.pdf` (56) and
`Day04_explanation_ja_en.pdf` (68) were **not** rebuilt and are byte-identical to the baseline.

### Tests

| File | Change |
|---|---|
| `assets/tests/test_experiment_identity.py` | **New** — 22 tests, cases 1–11 |
| `assets/tests/test_day02_threshold_figure.py` | **New** — 16 tests |
| `assets/tests/test_nepali_localization.py` | All 16 catalogs + 12 documents Romanized; idempotency over all 16; JA/EN preservation; bilingual booklets must stay Nepali-free |
| `assets/tests/test_trilingual_layout.py` | Figure-caption signature no longer collides when one figure is reused in two lessons |
| `assets/tests/test_evaluation_provenance.py` | Sealed-loader assertions follow the checks into `validate_sealed` |
| `assets/tests/test_clarity_review.py` | Freeze fixture now writes the fitted-state record |

---

## 4. Romanization summary

```
python assets\scripts\convert_nepali_to_latin.py --scope notebooks --check   # before: 10 pending
python assets\scripts\convert_nepali_to_latin.py --scope notebooks --write
python assets\scripts\convert_nepali_to_latin.py --scope notebooks --check   # after:  0 pending
```

| Metric | Value |
|---|---|
| Notebook catalogs | 16 / 16 Romanized (`catalog_script` = `romanized` for every file) |
| Nepali regions in notebooks | **1 148**, of which **0** Devanagari |
| Learner documents with Nepali | **12 / 12**, all Romanized |
| Markdown cells carrying Nepali | 655 / 802 (147 documented exemptions) |
| Nepali characters in notebooks | 330 524 |
| Glossary entries | 360 → **441** |

The engine (`romanize_word`) was not rewritten; the reviewed spellings live in `GLOSSARY`, which is
the mechanism the style guide documents.

---

## 5. Translation quality issues identified and corrected

Each item below was found by reading the `--review` word list (2 281 unglossed words) and the
converted text against the Japanese, the English and the Devanagari original.

| # | Problem | Why it was wrong | Fix |
|---|---|---|---|
| 1 | `-एर` converbs came out as `banaer`, `chalaer`, `padher`, `rakher`… | The letter rules stop at the final `र`; no Nepali speaker writes `banaer` | 24 glossary entries ending in `-era` (`banaera`, `chalaera`, `padhera`, `rakhera`, …) |
| 2 | Words ending in a consonant cluster became `bhitr`, `kshetr`, `kendr`, `gann`, `nikaln` | Rule 4 drops the final vowel; with a cluster that leaves an unreadable word | 54 glossary entries (`bhitra`, `kshetra`, `kendra`, `sutra`, `ganna`, `bhanna`, `napna`, `nikalna`, …) plus 12 compounds in `-bhitra` |
| 3 | Same word, two spellings in `GLOSSARY` (`अभ्यास`, `मात्र`, `पूरा`, `मूल्याङ्कन`, `प्रमाणीकरण`, `संश्लेषित`) | Violates the style guide's "one idea, one spelling"; the value silently depended on dict order | 26 duplicate keys removed; the effective value was kept, so no output changed |
| 4 | Genitive sometimes joined, sometimes spaced (`score ko` vs `tasbirko`) | Rule 5 says `को` stays attached | `scoreko`, `maapanko`, `sikaiko`, `heatmapko` |
| 5 | `कर्ण` (hypotenuse) → `karna` collided with the Hindi "करना" detector | The coverage checker failed on a correct Nepali word | The Latin marker list no longer flags `karna`; the Devanagari `करना` check stays |
| 6 | Latin catalogs could not pick up new glossary spellings | `romanize_text` only touches Devanagari, so Day 4–5 would drift | `apply_glossary_spellings` + `glossary_respellings` (189 safe pairs), with three guards: a rule output produced by two glossary words is skipped (`हुन`/`हुन्`), short forms (`ab`, `bat`, `man`) are skipped, and `path` is never touched |
| 7 | Two `after-heading` blocks became all-English after the migration (`**Jupyter notebook, cell, kernel**`, `**class label**`) | The "is this Nepal" check correctly refused them | Rewritten as `**Jupyter notebook, cell ra kernel**` and `**class label (barga ko naam)**` |

**Deliberately accepted, not corrected:** the rule engine still yields `utpadanako`, `tinabata`,
`pikselama`. They are consistent across all 16 catalogs and are recorded as accepted in the style
guide's review checklist. **They need a native or advanced Nepali reviewer**; automated conversion
cannot certify fluency.

---

## 6. Day 2 threshold figure — before / after

### Original problem

`teach_threshold_sweep()` drew the foreground-pixel count and the "region" count on **one shared
plot with two vertical axes**, showed only the three binary masks (no input image), and called the
contours "領域 / regions".

### Why it was incorrect or confusing

* A dual axis invites the reader to compare two unrelated quantities; the two lines cross and imply a
  relationship that does not exist.
* Without the input image, the reader cannot see that the input never changes and only `T` moves.
* "Regions" hides the actual OpenCV call. The count is `cv2.RETR_EXTERNAL`, i.e. **outer boundaries**,
  which is not a defect count and not a connected-component analysis.

### Exact modification

`assets/scripts/generate_teaching_diagrams.py`:

* **Top row:** grayscale input + `T = 100`, `T = 160`, `T = 210`, each labelled
  `THRESH_BINARY_INV`, with `white = selected foreground (I ≤ T)` / `black = ignored background
  (I > T)` written above the row and the pixel/contour counts under each mask.
* **Bottom row:** two separate graphs — **A** = white foreground pixels vs `T`, **B** = external
  contours (`cv2.findContours(..., cv2.RETR_EXTERNAL, ...)`) vs `T`. No twin axis.
* The 19 thresholds 40–220 (step 10) and the synthetic input `_pvc_sheet(200, "spot", seed=52)` are
  unchanged.

The notebook cell `fig-teach_threshold_sweep` was rewritten in Japanese, English and Romanized Nepali
to answer the six required questions, give a small numerical example, and keep the prediction
exercise. A "what to notice" list was kept because the visual-asset test requires every figure to
carry one.

### Numerical verification

`36677` matched the reference exactly, so the input and the counting method are the same. The spot is
the disc of `teaching_data.spot_mask` (radius 9 px, `< r²`), which contains **249** pixels, not 250 —
the earlier note was off by one. **The computed value is used; nothing was adjusted to hit 250.**

| T | white px | external contours |
|---|---|---|
| 40–180 | 249 | 1 |
| 190 | 302 | 46 |
| 200 | 12 634 | 320 |
| 210 | 36 677 | 49 |
| 220 | 40 000 | 1 |

### How the fix was tested

* `assets/tests/test_day02_threshold_figure.py` recomputes `cv2.threshold` + `cv2.findContours` and
  compares against `_threshold_sweep` for six thresholds; asserts the pixel count never falls, the
  contour count does; asserts `RETR_EXTERNAL < RETR_LIST` at T = 210; rebuilds the PNG twice and
  compares bytes against the shipped file.
* The explanation is checked for the six answers, the three numbers, the calibration example, the
  "input never changes" statement, and the explicit "the contour count is not the number of defects"
  in both languages.

---

## 7. Day 5 navigation changes

### Original problem

`clarity-sealed-test` told learners to run "the last cell of this notebook". The scoring cell is
`clarity-sealed-test-scoring`, which sits **before** the remaining exercises and the report cells, so
"last cell" is wrong and can be read as "run everything, then this".

### Exact modification

`clarity-sealed-test` now carries a four-step table (notebook filename, what to do), a plain-text
flow diagram inside a fenced block (no new PNG/SVG), and a "common situations" table:

| Step | Notebook | Action |
|---|---|---|
| 1 | `Day05_02_PatchCore_Training.ipynb` | fit, score calibration, save; do **not** score test |
| 2 | `Day05_03_YOLO_vs_PatchCore.ipynb` | compare on calibration, select both thresholds, record the freeze |
| 3 | `Day05_02_PatchCore_Training.ipynb` | run **only** `clarity-sealed-test-scoring` |
| 4 | `Day05_03_YOLO_vs_PatchCore.ipynb` | load the seal, verify provenance, finish the comparison |

The same table answers the required questions: why scoring before the freeze is prohibited, why
*Run All* deliberately stops, what a freeze record is, what to do when a required file is missing, and
what to do after a kernel restart. `clarity-sealed-test-read` in Notebook 03 now names the cell and
states the same order. Two comments and one error message that said "the last cell" were changed to
the cell name (`82f543da`, `39a9c510`, `clarity-load-sealed-test`). No other instruction mentions a
"last cell".

### How the fix was tested

`test_evaluation_provenance.py::test_day05_02_scores_the_test_partition_only_after_the_freeze` still
proves that only `clarity-sealed-test-scoring` touches `test_dataloader()`; the layout is additionally
reviewed on Day 5 pages 55–56 of the tri-language booklet and the rebuilt JA/EN booklet (the string
`最後のセル` no longer appears in `Day05_explanation_ja_en.pdf`).

---

## 8. Day 5 provenance mechanism

### Original problem

```python
if sealed_path.is_file():
    print("already scored")
else:
    compute_test_predictions()
```

Repeated scoring was prevented, but nothing tied the existing file to the **current** frozen
experiment, so a result from another fit, another split or other thresholds could be reused.

### Design

`assets/helpers/experiment_identity.py` (new, importable from both notebooks):

* `fitted_state(model)` — SHA-256 over every tensor of `model.model.state_dict()` plus
  `memory_bank`, in name order, with each tensor's **name, shape, dtype and bytes**.
* `postprocessor_state(model)` — `enable_normalization`, `image_min/max`, `pixel_min/max`,
  `adaptive_threshold`.
* `dataset_identity(manifest)` — dataset name, seed, image size, split settings, counts and a digest
  of the partition lists.
* `base_identity(...)` → `experiment_id`; `frozen_identity(base, yolo_threshold=…,
  patchcore_threshold=…)` → the frozen `experiment_id`.
* `validate_sealed(...)` — schema, experiment identity (naming the failing part), thresholds,
  assessment role, partition set, duplicate ids, full test-partition coverage, field presence and
  types.
* `write_json_atomic(...)` — temp file in the same directory, `fsync`, `os.replace`; a failure leaves
  the previous file and no `*.tmp`.

Not used as identity: class names alone, `id()`, timestamps, paths or random UUIDs.

### Wiring

| Where | What happens |
|---|---|
| `Day05_02` / `daed190f` (right after the fit) | `FITTED_STATE` / `POSTPROCESSOR_STATE`, `manifest["experiment"]`, `split_manifest.json` and `patchcore_fitted_state.json` written atomically |
| `Day05_02` / `1c4cd018` | the calibration payload carries the same `experiment` |
| `Day05_03` / `clarity-freeze-record` | verifies the fitted record against the manifest **and** the calibration payload, then stores `experiment`, `model_fingerprint`, `experiment_id` |
| `Day05_02` / `clarity-sealed-test-scoring` | freeze record → kernel model fingerprint → freeze identity → (existing seal | score once) |
| `Day05_03` / `clarity-load-sealed-test` | full `validate_sealed` before the table is built; prints "Existing sealed predictions match this frozen experiment." only on success |

Scoring writes the numeric maps into `submission_dir/maps_pending`, validates the payload, publishes
the JSON atomically and only then moves the maps into `maps/`. A failure before publication leaves
the previous files and no partial seal.

### How the fix was tested

`assets/tests/test_experiment_identity.py` (22 tests) covers cases 1–11 with synthetic fixtures and no
model fitting: valid seal, reuse, other fitted model, other split, other thresholds, missing images,
duplicate ids, wrong types, missing field, older schema, reused-data role retained, and a write that
fails at `os.replace` (previous file intact, no leftover temp file). Case 8 (kernel restarted) is a
runtime message in `clarity-sealed-test-scoring`; case 9 (no freeze declaration) is still covered by
`test_clarity_review.py`.

---

## 9. PDF files regenerated

```
python assets\scripts\export_trilingual_pdf.py
python assets\scripts\export_explanations_pdf.py --only Day02
python assets\scripts\export_explanations_pdf.py --only Day05
python assets\scripts\export_explanations_pdf.py --only Week1
```

**Deviation, stated openly:** the request named only `Day02_explanation_ja_en.pdf` and
`Week1_explanation_ja_en.pdf` for the bilingual rebuild. `Day05_explanation_ja_en.pdf` was rebuilt as
well because the Japanese/English navigation text of Day 5 changed (§7); leaving it would have shipped
the outdated "last cell" wording in one of the six booklets. `Day01`, `Day03` and `Day04` were **not**
rebuilt.

**Bug found and fixed while rebuilding:** `export_explanations_pdf.py` had no Nepali handling. While
the third language was Devanagari the typesetter silently dropped the glyphs; with `ne-Latn` it printed
the region body **and** the `<!-- ne:begin … -->` markers. `strip_nepali()` now removes regions and
markers, is applied to the notebook title and to every Markdown cell, and is idempotent.

---

## 10. PDF page counts

| File | Pages |
|---|---|
| `Setup_ja_en_ne.pdf` | 41 |
| `Day01_explanation_ja_en_ne.pdf` | 98 |
| `Day02_explanation_ja_en_ne.pdf` | 115 |
| `Day03_explanation_ja_en_ne.pdf` | 77 |
| `Day04_explanation_ja_en_ne.pdf` | 88 |
| `Day05_explanation_ja_en_ne.pdf` | 88 |
| `Week1_explanation_ja_en_ne.pdf` | 455 |
| `Installation_Guide_ja_en_ne.pdf` | 23 |
| `Repository_Guide_ja_en_ne.pdf` | 23 |
| `Course_Syllabus_ja_en_ne.pdf` | 20 |
| `Day02_explanation_ja_en.pdf` | 88 |
| `Day05_explanation_ja_en.pdf` | 64 |
| `Week1_explanation_ja_en.pdf` | 338 |

## 11. Pages visually inspected

Rendered with `assets\scripts\inspect_pdf_pages.py` (PNG per page) and viewed directly.

| Booklet | Pages viewed | What was checked |
|---|---|---|
| `Day02_explanation_ja_en_ne.pdf` | 1 (cover), 3 (TOC), 85 (new figure), 86 (six answers + table) | cover text in three languages, TOC bookmarks, figure readable at print size, caption → figure adjacency, table borders, no overflow, selectable text |
| `Day05_explanation_ja_en_ne.pdf` | 55, 56 (four steps + situations), 77 (freeze + sealed read) | table split across a page break, ASCII flow diagram alignment, Nepali paragraph rendering, no clipping |
| `Setup_ja_en_ne.pdf` | contact sheet 1 (pages 1–12) | cover, "about", TOC, learning-objective tables, figure pages |
| `Day01_explanation_ja_en_ne.pdf` | contact sheet 2 (pages 13–24) | three-language body text, code blocks, tables, figure/heading pairing |
| `Day02_explanation_ja_en.pdf` | 66 (figure), 67 (answers) | bilingual booklet carries no Nepali or markers |
| `Day03`, `Day04`, `Week1` (tri-language) | not page-by-page; automated checks only | see §12 |

Automated render checks (`inspect_pdf_pages.py`) reported for every regenerated booklet:
**no blank pages, no text outside the printable area, no split words in the text layer**.

**Honest scope statement:** six representative pages plus three contact sheets were inspected by eye.
The remaining ~1 000 pages were checked only by the automated render/text checks; they were **not**
visually reviewed page by page.

---

## 12. Actual automated test results

```
python -m pytest assets\tests -q
495 passed, 4 warnings in 462.43s
```

Baseline at `7beb097` on the same machine, before any change: `357 passed, 62 skipped`
(the 62 skips were the optional PDF tooling, which was installed for this task).

```
python assets\scripts\convert_nepali_to_latin.py --scope notebooks --check
[done] 0 catalog(s) would change; 0 problem(s)

python assets\scripts\apply_nepali_translations.py
[done] 0 cells would change; 0 problem(s)

python assets\scripts\apply_nepali_docs.py
[done] written; 0 problem(s)          (second run: 0 changed)

python assets\scripts\check_nepali_coverage.py --strict
[done] 655/802 markdown cells with Nepali (81.7 %), 147 exempt, 0 missing, 330,524 Nepali characters
[done] 1148 Romanized and 0 Devanagari Nepali regions
[done] 12/12 documents with Nepali regions          (exit 0)

python assets\scripts\validate_notebooks.py --execute none
passed=194 failed=0 skipped=0
RESULT: OK

git diff --check
(no output)
```

Notebook execution (`--execute all`) was **not** run: Day 5 needs anomalib 2.7.0, lightning and the
resnet18 cache, which this analysis machine does not have (it has anomalib 1.1.0dev without
lightning). All Day 5 logic is therefore covered by unit tests with synthetic fixtures instead of a
full training run.

---

## 13. Files verified unchanged

Verified by hashing every notebook's protected parts before and after (`cell id`, code source,
metadata, outputs, execution count, notebook metadata):

* **16 / 16 notebooks**: no cell added, removed or re-ordered; no cell id changed; no notebook
  metadata changed.
* **Setup and Day 1–4**: **zero** code cells changed (byte-identical).
* **Day 5**: exactly **7** code cells changed, all authorised by §7 and §8:
  `daed190f`, `1c4cd018`, `82f543da` (comment only), `39a9c510` (comment only),
  `clarity-sealed-test-scoring`, `clarity-freeze-record`, `clarity-load-sealed-test`.
* Images: only `assets/diagrams/teach_threshold_sweep.png` changed. `git status` lists no other PNG,
  SVG, reference output or dataset file.
* Models and datasets: untouched (`assets/models`, `assets/anomaly_dataset`, `assets/yolo_dataset`,
  `training_results`, `results` are not in the change list).
* `start_training.cmd`, `requirements/*.txt`, kernel installation and Python environment setup:
  untouched.
* `docs/pdf/Day01_explanation_ja_en.pdf`, `Day03_…`, `Day04_…`: byte-identical to the baseline.
* Day 4–5 catalogs changed **only** through the reviewed respellings listed in §5 (word-level diff:
  `bhitr→bhitra`, `banaer→banaera`, `kshetr→kshetra`, …); no sentence was re-translated.

---

## 14. Known limitations

1. **No native-speaker sign-off.** The wording is machine-transliterated plus hand-reviewed
   spellings; a Nepali reviewer must still read the 16 catalogs before the class.
2. **Accepted rule-engine spellings** (`utpadanako`, `tinabata`, `pikselama`) remain; they are
   consistent but not ideal.
3. **Sentence-initial capitals** are not introduced (the catalogs start sentences in lower case,
   matching the existing Day 4–5 style).
4. **Day 5 was not executed end-to-end** here (missing anomalib 2.7.0 / lightning / resnet18 cache).
   The new cells compile (`validate_notebooks`) and their logic is unit-tested, but the first real
   classroom run is the first true integration test of the fingerprint against a real PatchCore.
5. **TOC entries concatenate the three languages on one line** (`第2日 … Day 2 … din 2 …`). This is
   pre-existing exporter behaviour — the baseline Day 4 booklet shows the same — and was left alone
   because the request forbids changing the general language layout of the booklets.
6. **Figure captions are typeset twice** for diagrams that carry their own caption inside the PNG,
   because the Markdown caption sits under the image. Pre-existing; not changed.
7. **PDF inspection was sampled** (§11), not exhaustive.
8. **`path` is excluded from the respelling pass** because it is a YAML key in the YOLO lessons; if a
   future glossary entry needs it, the guard must be revisited.

---

## 15. Issues requiring human review

| Item | Who | Why |
|---|---|---|
| All 16 Nepali catalogs | Nepali reviewer | Fluency, register and grammatical gender cannot be certified automatically |
| `nan`, `barg`, `mathi-bayan` style terms in the Day 2 answers | Nepali reviewer | Check the technical register is natural for factory operators |
| Day 5 first classroom run | Instructor | Confirms the fingerprint matches a real fitted PatchCore and the 4-step order works in practice |
| Pre-existing TOC concatenation (§14.5) | Owner | A layout change is out of scope here |
| Whether `Day05_explanation_ja_en.pdf` should have been rebuilt (§9) | Owner | Deliberate deviation, taken to avoid shipping outdated navigation text |

---

## Acceptance gates

| Gate | Result | Evidence |
|---|---|---|
| **A — Translation** | **PASS** | 16/16 catalogs and 12/12 documents Romanized; 1 148 regions, 0 Devanagari; `check_nepali_coverage --strict` exits 0 |
| **B — Original content** | **PASS** | Cell ids / code / metadata / outputs identical; 7 authorised Day 5 code cells; JA/EN preservation tests |
| **C — Day 2 figure** | **PASS** | Two separate graphs, input panel, `RETR_EXTERNAL` counts, six answers, 249/249/36 677 verified |
| **D — Day 5 navigation** | **PASS** | 4-step order in Notebook 02 and 03; no "last cell" left; bilingual Day 5 booklet rebuilt |
| **E — Day 5 provenance** | **PASS** | `validate_sealed` runs before any reuse; 22 unit tests, cases 1–11 |
| **F — Evaluation integrity** | **PASS** | Test scored once, after the freeze; `declared_untouched_test` / `illustrative_reused_data` preserved |
| **G — PDF** | **PASS (sampled)** | 13 booklets rebuilt, page counts recorded, 6 pages + 3 contact sheets inspected, automated render checks clean |
| **H — Regression** | **PASS** | 495 passed, 0 failed, 0 skipped; `validate_notebooks` OK; `git diff --check` clean |
| **I — Idempotency** | **PASS** | Converter, notebook applier and doc applier all report zero changes on a second run |

**Ready for classroom use?** Yes for the Japanese/English material and the Day 5 protocol. The
Romanized Nepali is ready for a supervised pilot; it should not be presented as reviewed Nepali until
a Nepali speaker signs off §15.