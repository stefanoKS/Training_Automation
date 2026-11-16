# Day 2–5 targeted follow-up implementation / 対象修正の実装記録

Date: 2026-11-16. Authority: [follow-up audit](Training_Automation_Day02-Day05_Followup_Audit_2026-11-16.md), read completely before editing.

## Baseline and minimal plan

- Confirmed `main`, HEAD `9852b1949bd1180de801d52a5adb748dc963e00a`, exactly the audited baseline.
- Initial worktree: only the supplied audit was untracked; it already existed at the required path and was not changed. No newer commit had resolved A01–A06.
- Read current cell IDs, neighbouring code and Day 5 figure/map producers before editing.
- Plan: replace premature TEST evidence and prevent reinsertion; apply A02–A06 bilingual alignments; retain A07–A12's correct material; validate source/provenance, lightweight execution and affected PDFs.
- No push, merge, publish, commit, dependency installation or environment/setup change.

## A01–A12 dispositions and exact notebook anchors

Paths below are relative to the course root through their links. All pre-existing IDs and metadata were retained.

| Item | Disposition | Exact path / cell IDs and implementation |
|---|---|---|
| A01 | FIXED | [Day05_01](../../notebooks/Day05_PatchCore/Day05_01_Anomaly_Detection_Concepts.ipynb), `5c642a4a`: additionally found the same TEST-derived worked scores here; replaced them with a nonnumeric description of the two output roles. [Day05_02](../../notebooks/Day05_PatchCore/Day05_02_PatchCore_Training.ipynb), `clarity-score-card`, `fig-ref_anomaly_panels`: replaced early TEST panel/card with a transparently calculated synthetic toy. Retained the original cell ID despite the different image filename. TEST-map writer `39a9c510` remains unchanged and is not a learner display. Original TEST panel, truth/score reading and historical values now appear only in the [after-freeze instructor appendix](../instructor/day05_after_freeze_archive.md), opened by the existing Day05_03 gate. |
| A02 | FIXED | [Day02_03](../../notebooks/Day02_Python_OpenCV/Day02_03_OpenCV_Image_Processing.ipynb), `4a6c53f8`: used the audit's exact JP and EN replacements. Original left input is invariant; middle mask changes with T; right contours are recomputed from that mask. No live-code/figure change. |
| A03 | FIXED | [Day02_01](../../notebooks/Day02_Python_OpenCV/Day02_01_Python_Basics.ipynb), `fig-teach_assign_vs_compare`: added immediate four-line code cell `followup-assignment-live` (two bilingual role-banner lines plus `width = 100.3` and `print(width == 100.3)`). Changing only width to 100.4 changes True to False. Existing specification example `9ff42d85` follows unchanged; prompt explicitly distinguishes equality from tolerance acceptance. |
| A04 | FIXED | [Day05_03](../../notebooks/Day05_PatchCore/Day05_03_YOLO_vs_PatchCore.ipynb), `3d343aab`: corrected both languages to the earlier calibration slider. Added that settings revised after inspecting TEST need a new untouched holdout and cannot be reported as the original final test score. Slider not moved. |
| A05 | FIXED | [Day02_01](../../notebooks/Day02_Python_OpenCV/Day02_01_Python_Basics.ipynb), `acfe495e`: brief bilingual stored-number-approximation note immediately beside the unchanged recorded decimal. Retained `fig-teach_units_conversion` and deferred detailed lesson. `1b60ce34` explains that 1e-9 is chosen toy numerical tolerance, not a manufacturing criterion; `50c7ee88` and matching expected output `31fc6d72` now say “toy numerical tolerance”, not “safe comparison”. Arithmetic unchanged. |
| A06 | FIXED | [Day05_02](../../notebooks/Day05_PatchCore/Day05_02_PatchCore_Training.ipynb), `c452bff7`, directly before code `6c5c2682`: bilingual bridge explains `engine.test()` is the library method name; supplied `datamodule.val_dataloader()` determines CALIBRATION data, not held-out TEST. API call and split unchanged. |
| A07 | RETAINED | [Day02_02](../../notebooks/Day02_Python_OpenCV/Day02_02_Conditions_Loops_Functions.ipynb), `clarity-independent-spec`, `clarity-main-spec`, `clarity-transfer-stepper`, `clarity-function-transfer`: existing main/transfer banners and correct numbers/verdicts retained. No classroom evidence justifying optional expansion. |
| A08 | RETAINED | [Day03_03](../../notebooks/Day03_YOLO_Basics/Day03_03_YOLO_Experiments.ipynb), `clarity-experiment-provenance`: A/B/C1/C2 inputs, resolutions and candidate sets remain separate; no optional rewrite or figure change. |
| A09 | RETAINED | [Day04_02](../../notebooks/Day04_YOLO_Training/Day04_02_YOLO_Training.ipynb), actual first-pass cell `clarity-batch-static` (audit describes it as clarity-batch-first-pass), extension `16c0469f`: existing 64/8 = 8-batch SVG, Stage 2 accumulation/warmup detail, loss and checkpoint material unchanged. |
| A10 | PASS / RETAINED | [Day04_03](../../notebooks/Day04_YOLO_Training/Day04_03_YOLO_Evaluation.ipynb), `clarity-evaluation-units`: successful image-vs-object example, figures and axis conventions unchanged. |
| A11 | PASS / RETAINED | [Day05_01](../../notebooks/Day05_PatchCore/Day05_01_Anomaly_Detection_Concepts.ipynb), `clarity-patch-overlap`: approved analogy/overlapping-support explanation and original SVG/PNG unchanged. |
| A12 | PASS / PRESERVED | [Day05_03](../../notebooks/Day05_PatchCore/Day05_03_YOLO_vs_PatchCore.ipynb), `clarity-freeze-record`, `clarity-archive-gate`, `clarity-calibration-boundary` and test-scoring code: declaration, TEST_ALREADY_SEEN, assessment role, frozen-setting comparisons and archive opt-in guards unchanged. A01/A04 supply the cross-notebook/text fixes only. |

## Figure provenance and generation

- No saved calibration numeric maps, score CSV or original checkpoint were available locally. Chose the explicitly permitted synthetic option rather than fabricating calibration inference.
- **One new PNG:** [teach_numeric_map_toy.png](../../assets/reference_outputs/teach_numeric_map_toy.png). Fixed 5×5 distance grid: ones, centre 6, four direct neighbours 2. Edge-padded 3×3 mean has maximum 2.000; chosen weight gives raw scalar `6 × 0.8 = 4.800`; chosen transform gives `clip((4.8 − 4)/8 + 0.5, 0, 1) = 0.600`. These are teaching constants, not fitted statistics or an implementation of PatchCore. Both figure and card say so in JP/EN; no TEST numbers reused.
- [generate_reference_outputs.py](../../assets/scripts/generate_reference_outputs.py): added pure `toy_numeric_map()` and its renderer; repeated generation is byte-identical. Existing anomaly/comparison TEST PNGs are preserved when present. Reconstructing a missing anomaly archive requires a TEST image path and matching TEST score row.
- [insert_lesson_figures.py](../../assets/scripts/insert_lesson_figures.py): removed the early TEST-panel registry entry; future lesson insertion cannot restore it. Existing five-column TEST entry was already retired.
- Updated [visual manifest](../visual_figure_manifest.md) with **every Day 5 static/runtime figure's source role**, including external VisA, synthetic diagrams, calibration distribution, live calibration overlays and both TEST archives. `ref_score_distribution.png` is CALIBRATION by its producer's explicit partition filter; `ref_` alone is not a provenance claim.
- Updated [reference-output documentation](../../assets/reference_outputs/README.md) and the image allowlist in the course `.gitignore`. No other PNG/SVG was regenerated. All seven original reference PNG SHA-256 hashes match the pre-edit snapshot.
- Original archive SHA-256:
  - `ref_anomaly_panels.png`: `5e55dd456029af0663f1727f7e2cdba1c7f7d574f9d942a796185b11c29ebad8`
  - `ref_comparison_5col.png`: `9c2296614a9779fbbfc85d852755ad498e17d6a006855ebab3bf9adfc28a193d`

## Before/after teaching checks

- A01: early “保存例21.439 / archived 21.439” and raw21.439/map21.762/saved1.000 TEST card → nonnumeric output-role overview plus **合成おもちゃ / calculated synthetic toy**, 4.800/2.000/0.600. Historical TEST card remains in the after-freeze appendix, not learner PDFs.
- A02: “3 枚は同じしきい値 / three panels all come from one threshold” → “左の元画像は、しきい値を変えても変わりません。 / The left-hand original stays unchanged when the threshold T changes.” Both complete replacement paragraphs match A02 exactly.
- A03: `width` prediction followed by unrelated tolerance code → immediate matching executable equality example, then the original tolerance code.
- A04: “次の節のスライダー / slider in the next section” → “前の較正用スライダー / earlier calibration slider”, with the same fresh-holdout restriction in both languages.
- A05: unexplained `0.29999999999999716` → adjacent “保存した数の近似 / stored-number approximation” note; “安全な比較 / safe comparison” → “数値許容差のおもちゃ / toy numerical tolerance”, explicitly not a manufacturing acceptance criterion.
- A06: method/data-role bridge added: “ライブラリのメソッド名 / library method name”, loader selects CALIBRATION, not held-out TEST. No code change.

## Validation actually performed

Used the existing repository `.venv\Scripts\python.exe`; installed nothing.

| Check | Actual result |
|---|---|
| Initial targeted repro, before notebook/generator corrections | **6 failed, 1 passed**, 10 deselected. Confirmed A01 also affected Day05_01. |
| Focused clarity/provenance/visual tests | **95 passed, 0 failed, 0 skipped**; 4 existing noninteractive Matplotlib warnings. |
| `python -m pytest assets\tests -q`, final run | **345 passed, 0 failed, 0 skipped**, 4 existing Matplotlib warnings; 124.25 seconds. Includes source, split/freeze, diagram, notebook, documentation and PDF regressions. |
| PDF-specific suite | **35 passed, 0 failed, 0 skipped**. Further strengthened toy-pixel-identity/early-answer selection: **5 passed**, 47 deselected, then final full suite above. |
| Documentation rules after adding this log | **28 passed, 0 failed, 0 skipped** (`test_language_labels.py`, `test_cmd_documentation.py`). |
| `validate_notebooks.py --execute none` | **194 passed, 0 failed, 0 skipped**, all 16 course/setup notebooks structurally valid; no missing images or syntax/banner failures. |
| Baseline JSON comparison | All **1,075 existing cell IDs**, all notebook/cell metadata and all original code cells except the optional demonstration's printed label unchanged. Exactly one new ID. **47 unanswered write-code exercise cells** and **one deliberate-exception cell** unchanged. |
| Lightweight in-memory notebook execution | **3 passed, 0 failed**: Day02_01 (17 code cells, 1.7 s), Day02_03 (22, 4.0 s), Day05_01 (12, 3.5 s). No unexpected errors. Used existing `python3` venv kernel in memory; source kernelspecs/outputs not rewritten. |
| Heavy YOLO/PatchCore training/full Day05_02/03 execution | **NOT RUN / SKIPPED**, not counted as passed. No new model results claimed. |
| Pylance syntax checks / `git diff --check` | Passed for changed generator/provenance/PDF test code and whitespace. |

Source regressions cover all three pre-freeze Day 5 notebooks, old TEST names/scores/labels, source-role filtering with mixed calibration/TEST fixtures, rejection of mismatched archive sources, repeated archive/toy generation, complete figure classification, preservation of freeze guards and prevention of early-panel reinsertion.

### PDF acceptance

- Rebuilt only [Day02](../pdf/Day02_explanation_ja_en.pdf) (**86 pages**), [Day05](../pdf/Day05_explanation_ja_en.pdf) (**63**) and [Week1](../pdf/Week1_explanation_ja_en.pdf) (**334**).
- PDF regressions compare decoded embedded image pixels: **neither archived TEST PNG occurs anywhere** in learner Day05/Week1; the new toy occurs unchanged, not silently substituted. Day 5 text contains none of the archived test-only scores/image labels.
- Rendered/geometry-checked 13 unique PDF pages. Visually inspected Day02 pp. **14, 18, 24, 69**; Day05 pp. **35, 38, 39, 55**; Week1 pp. **309, 310, 326**. JP/EN text, numeric card, mini-code and landscape figure titles are legible, with no clipping or missing glyphs observed. Checked pages had no out-of-bounds characters or blank-page flags.
- Notebook/figure/appendix image targets resolve; checked PDF internal outline destinations are valid. Existing export convention renders ordinary Markdown links as text, not live external hyperlinks; no link-rendering change was made.
- **Approved Day 1 is unchanged:** all three source notebooks and standalone Day01 PDF retain their original SHA-256 hashes. The rebuilt Week1 Day 1 overview/lessons retain identical extracted text, embedded image pixels and page dimensions across **67 pages** (pp. 14–80; page-number footer excluded from comparison).

## Scope and limitations

No Day 1 notebook, Day 1-only source asset/text, Setup notebook, launcher or CMD installation procedure was modified. Days 3/4 notebooks, figures and standalone PDFs are untouched. Original measurement definitions, specification numbers, calibration/test partitions and research evidence remain intact.

Historical model checkpoints/numeric arrays were absent, so historical inference values (including the preserved calibration distribution) were **not independently recomputed**. Their existing provenance and original pixels are retained, not newly certified. No classroom trial, fresh holdout assessment or heavy-model training was performed. The after-freeze appendix remains a teaching-workflow gate, not filesystem access control.
