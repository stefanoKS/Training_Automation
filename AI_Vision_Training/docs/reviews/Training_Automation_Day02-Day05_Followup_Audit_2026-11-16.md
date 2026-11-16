# Training_Automation — Follow-up teaching and visual audit (Days 2–5 only)

**Audit date:** 2026-11-16 (JST)  
**Repository:** https://github.com/stefanoKS/Training_Automation  
**Reviewed branch / commit:** `main` / `9852b1949bd1180de801d52a5adb748dc963e00a` (2026-11-16 10:44:54 UTC)  
**Comparison baseline:** `beda393c7fc5d0873a8f4697c46ae114c3626395`  
**Root:** `AI_Vision_Training/`  
**STRICT SCOPE:** Day 2, Day 3, Day 4 and Day 5 notebooks. **Day 1 is approved: do not modify Day 1 content, assets solely associated with Day 1, or its notebook.** Setup and CMD launcher are also out of scope. This report is an inspection, not a repository change.

## 1. Overall judgment

The new revision is a substantial improvement. All 12 Day 2–5 notebooks have been modified. The initial clarity implementation correctly addressed much of the previous backlog: consistent/titled tolerance examples; BGR→RGB before/after; a tiny grayscale→mask→contour experiment with foreground pixels distinguished from contour area; synchronized bounding-box formats; provenance-separated confidence experiments; a first-pass batch diagram; image versus object evaluation; an overlapping-patch schematic; and a freeze record for YOLO/PatchCore comparisons.

The repository's `docs/reviews/Day01-Day05_Clarity_Implementation_Log.md` **reports** 330 pytest passes, 194 structural-validation passes, 10 lightweight notebook executions, and six successful PDF builds. These are project-recorded results, **not** independent test executions in this follow-up. I fetched current notebook sources and selected SVG sources. I did **not** execute YOLO/PatchCore training, render every figure, or perform a fresh classroom walkthrough. Preserve the already-correct code, numerical examples, diagrams, and output files.

**Decision:** Targeted corrections rather than another wholesale rewrite. One finding (A01) is a meaningful **teaching evaluation-integrity issue**. Several smaller text/code cross-reference issues can be corrected with minimal edits. No evidence in this source review requires regenerating the three new SVG diagrams.

## 2. Prioritized findings (remaining only)

### A01 — P1 — Day 5 exposes test examples before the freeze (confirmed source-level contradiction)

**Notebook:** `notebooks/Day05_PatchCore/Day05_02_PatchCore_Training.ipynb`  
**Anchors:** Markdown cells with IDs `clarity-score-card`, `fig-ref_anomaly_panels`; code cell saving `*_map.npz` in Part 5.  
**Related builder:** `assets/scripts/generate_reference_outputs.py`, function `ref_anomaly_panels`.

**Evidence:** The Day 5 Notebook 02 code builds numeric-map files by looping through `predictions_by_partition["test"]` and storing `submissions/day05/maps/*_map.npz`. `ref_anomaly_panels` reads those maps, selects e.g. `black_spot_0000`, and produces `assets/reference_outputs/ref_anomaly_panels.png` with ground-truth label, raw map and anomaly scores. Notebook 02 displays this PNG plus its worked numbers (`raw image score = 21.439`, `map maximum = 21.762`, `normalized image score = 1.000`) **before** the freeze declaration in Day 5 Notebook 03. The implementation correctly gated `ref_comparison_5col.png` in Notebook 03, but overlooked this earlier test-derived panel. This is **premature exposure of the held-out test set to the learner**, not proof that the model's fit itself used test data.

**Fix:** Remove the test-derived panel and its corresponding `21.439/21.762/1.000` reading card from the *pre-freeze student path*. Replace it with (preferred) a numerically grounded **CALIBRATION-only** illustration and a matching simple card, or use a clearly tagged synthetic toy with no actual test information. Preserve the existing test panel unchanged in an **after-freeze instructor appendix** such as `docs/instructor/day05_after_freeze_archive.md`, with provenance. If a calibration numeric-map asset is generated, derive it from `predictions_by_partition["calibration"]`, give it a distinct name and noncolliding output path, and compute labels from the actual saved data rather than substituting invented numbers. Never relabel a TEST result as CALIBRATION. Ensure any static PDF/Week1 output does not expose the archived test panel before the test gate.

**Add regression:** A test that scans **all student-facing, pre-freeze Day 5 notebooks (01/02/03)** for references to test-derived reference panels and known test-only numbers/labels; validate the newly chosen calibration/synthetic panel's provenance and the gate for the archived panel. Audit all other `ref_` figures used before freezing to ensure they are not test-derived. Document exact classification of each figure.

**Why it matters:** Students cannot learn the difference between a truly untouched test and an already-inspected test when a worked test answer is shown early.

### A02 — P1 — Day 2 OpenCV threshold narrative contradicts the live figure behavior

**Notebook:** `notebooks/Day02_Python_OpenCV/Day02_03_OpenCV_Image_Processing.ipynb`  
**Anchor:** Markdown cell ID `4a6c53f8`, "しきい値を動かして、元画像・マスク・輪郭を同時に見る" (at roughly index 36).

**Existing wording:** `3 枚は同じしきい値から作られます。片方だけが変わることはありません。` / `The three panels all come from one threshold value; they cannot change independently.`

**Problem:** Panel 1 is the **original image**, so it does not depend on the threshold. Panels 2 and 3 are computed **from it** using the threshold. The notebook already states this correctly elsewhere ("元画像とグレースケール画像" do not change with T). The quoted caption incorrectly implies all three panels change together.

**Replace, JP:** `左の元画像は、しきい値を変えても変わりません。しきい値 T を変えると、中央の2値化マスクが変わり、右の輪郭表示もそのマスクから再計算されます。中央に表示したマスクは findContours に渡した配列と同じです。`

**Replace, EN:** `The left-hand original stays unchanged when the threshold T changes. Changing T updates the binary mask in the middle; the contour display on the right is then recomputed from that mask. The displayed mask is exactly the array passed to findContours.`

**Visual:** No new image necessary; the existing three-panel live output is already a good demonstration. Optionally label the panels `fixed input`, `changes with T`, `recomputed from mask`.

### A03 — P2 — Day 2 assignment/comparison question does not match the next runnable cell

**Notebook:** `notebooks/Day02_Python_OpenCV/Day02_01_Python_Basics.ipynb`  
**Anchors:** Markdown ID `fig-teach_assign_vs_compare` (index ~31); code cell immediately after (index ~32).

**Evidence:** The added question asks learners to predict `width = 100.3` followed by `print(width == 100.3)`, then change `width` to `100.4`. The **next runnable code** instead creates `measured_mm`, `nominal_mm`, `tolerance_mm` and evaluates `abs(difference) <= tolerance_mm`; it contains no `width` or `print(width == 100.3)`.

**Fix:** Add one tiny runnable **code cell immediately after the exact question** using the same `width` name, or change the question to predict what the actual following code does. If adding a cell, keep it 2–4 lines long and explicitly instruct what one value the learner changes. Keep the existing production tolerance comparison later and distinguish boolean equality from tolerance acceptance.

**Visual:** Reuse `teach_assign_vs_compare.png`. No new static figure.

### A04 — P2 — Day 5 points forward to a slider that is now earlier

**Notebook:** `notebooks/Day05_PatchCore/Day05_03_YOLO_vs_PatchCore.ipynb`  
**Anchor:** Markdown cell ID `3d343aab`, "固定したしきい値で、試験用を1回だけ評価する", immediately before test-scoring code.

**Problem:** Japanese/English instruction still says `次の節のスライダー` / `the slider in the next section`, while the calibration slider and parameter cell were moved **before** the freeze declaration, to cells near indexes 32–33. The correct sequence is now calibration exploration → freeze declaration → test.

**Fix:** Replace with `前の較正用スライダー` / `the earlier calibration slider`, and add an explicit constraint: *if the test was already inspected, a revised setting needs a new untouched holdout and must not be presented as the original final test score*. No new image needed.

### A05 — P2 — Advanced floating-point lesson still leaks into the first-pass main path

**Notebook:** `notebooks/Day02_Python_OpenCV/Day02_01_Python_Basics.ipynb`  
**Anchors:** `fig-teach_units_conversion` (index ~22), code and expected output at 23–24; optional detail moved to `clarity-optional-operators` (index ~47).

**Problem:** Codex correctly moved the detailed floating-point explanation and negative-floor-division material into a second-pass section, but the **earlier main-route figure** still mixes physical units, binary representability and rounding policy, and the example immediately prints `0.29999999999999716`. A zero-programming-experience learner is shown the very surprise that the explanation is deferred until much later. That is not numerically wrong, but the sequencing is still unnecessarily demanding.

**Fix options (pick the smallest):** (1) Explain the printed decimal in one very short bilingual note immediately next to the output (`This is a stored-number approximation; learn the details in Optional...`), then leave the detailed visual for later; OR (2) move/retitle the mixed-unit figure and float example into the optional section, leaving a basic unit-conversion introduction in the main path. Avoid duplicate figures and preserve the exact recorded output. Also change `安全な比較 / safe comparison` on the optional `1e-9` example to **"toy comparison with a chosen numerical tolerance — not a manufacturing acceptance criterion"**, because `1e-9` is not a universal engineering tolerance.

### A06 — P2 — Day 5's method name `engine.test(...)` and dataset role need one plain-language bridge

**Notebook:** `notebooks/Day05_PatchCore/Day05_02_PatchCore_Training.ipynb`  
**Anchor:** code calling `engine.test(model=model, dataloaders=datamodule.val_dataloader())` and the text "4つの指標".

**Risk:** Beginners may read the method name `test` and assume it evaluates the held-out TEST set, even though the supplied loader is `val_dataloader()` and the notebook correctly uses it for calibration metrics.

**Fix:** Directly before this cell add a one- or two-sentence JP/EN note: *"Here `.test()` is the library method name; `val_dataloader()` determines which images are evaluated. Therefore this is CALIBRATION, not the final TEST."* Use two different colors/labels or a tiny text table if desired. Do not rename the library method or change the split.

### A07 — P3 — Day 2 independent measurement examples are now labelled but still numerically dense

**Notebook:** `notebooks/Day02_Python_OpenCV/Day02_02_Conditions_Loops_Functions.ipynb`  
**Anchors:** `clarity-independent-spec`, `clarity-main-spec`, `clarity-transfer-stepper`, `clarity-function-transfer`.

**Status:** **Mostly fixed; not a bug.** The main `100.0 ± 0.5 mm` route and the separate `12.0 ± 0.2`/`12.50 ± 0.10` examples are labelled. For classroom simplicity, consider a compact one-line "current example" band at the start of each transition (main versus transfer), rather than adding new diagrams or changing numbers. Preserve the correct boundary verdict and rule that grade C/D is NG under the approved specification.

### A08 — P3 — Day 3 experiments are properly separated, but the provenance explanation is fairly dense

**Notebook:** `notebooks/Day03_YOLO_Basics/Day03_03_YOLO_Experiments.ipynb`  
**Anchor:** `clarity-experiment-provenance` and its A/B/C1/C2 descriptions.

**Status:** **Technically improved and not a correctness error.** Different datasets, archived results and live 640/320 inference cases are now distinguished. If a classroom trial suggests confusion, make a one-row "which example am I looking at?" cue above each result, and move detailed archival provenance into an optional section. Do **not** combine counts from different candidate sets or portray old cached scores as this run's predictions. Reuse current confidence visuals; no more graphics needed.

### A09 — P3 — Day 4 training material is correct but dense for the first exposure

**Notebook:** `notebooks/Day04_YOLO_Training/Day04_02_YOLO_Training.ipynb`  
**Anchors:** `clarity-batch-first-pass` diagram, follow-on accumulation diagram, loss columns and best/last checkpoint explanation.

**Status:** The new 64-image / eight-batch SVG and distinction from optimizer updates are **correct by SVG text inspection**. Do not regenerate it. A first-time student should answer `64 ÷ 8 = 8 batches per epoch` before opening the optional `nbs`, warmup and optimizer-step detail. The existing text largely does this; only clarify/label "advanced after first run" if necessary.

### A10 — P3 — Day 4 evaluation: retain the successful image-vs-object example

**Notebook:** `notebooks/Day04_YOLO_Training/Day04_03_YOLO_Evaluation.ipynb`  
**Anchor:** `clarity-evaluation-units`.

**Status:** **Pass.** The example where a single image is correctly NG but one of two objects is missed is the right teaching fix. Keep the figure and unit labels. No new image or mathematical correction recommended. Do not change confusion-matrix axis conventions without checking the actual versioned library output.

### A11 — P3 — Day 5 patch overlap explanation and diagrams are sufficiently correct

**Notebook:** `notebooks/Day05_PatchCore/Day05_01_Anomaly_Detection_Concepts.ipynb`  
**Anchor:** `clarity-patch-overlap`, `assets/svg/teach_patch_overlap.svg`.

**Status:** **Pass.** SVG explicitly labels independent tiles as an analogy and CNN feature regions as overlapping. It does not claim actual receptive-field dimensions. The patch → features → bank → nearest neighbor → score visual story is now sufficient for a beginner overview. No new image needed.

### A12 — P3 — Day 5 comparison after freeze is mostly sound; preserve the guards

**Notebook:** `notebooks/Day05_PatchCore/Day05_03_YOLO_vs_PatchCore.ipynb`  
**Anchors:** `clarity-freeze-record`, test-scoring cell, `clarity-archive-gate`, `clarity-calibration-boundary`.

**Status:** **Pass with A04 text fix and A01 cross-notebook fix.** Required declaration, `TEST_ALREADY_SEEN`, saved assessment role, frozen-setting checks, and archived TEST gate are useful. Do not loosen or remove them. `TEST_ALREADY_SEEN=False` remains a student declaration, not proof of an untouched dataset; keep the output labels appropriately qualified.

## 3. Visual disposition — what to keep / improve

| Visual or lesson | Assessment | Action |
|---|---|---|
| Day 2 BGR before/after live strip | Good; matches channel-order rule | KEEP |
| Day 2 tiny inverse mask and contour area (12 pixels vs 6 px²) | Good; concrete computed comparison | KEEP |
| Day 2 original / mask / contours three panels | Good graphic, misleading accompanying sentence | EDIT CAPTION ONLY (A02) |
| Day 2 assignment-vs-comparison image | Good, but question refers to absent next-cell code | ADD MATCHING MINI-CELL (A03) |
| Day 3 box `xyxy` / `xywh` / normalized center | Correct synchronised sample | KEEP |
| Day 3 confidence toy/archived/live separation | Source-labelled; optional simplification | KEEP, optionally streamline |
| Day 4 first epoch/8-batch SVG | Correct labels 0–63, batches 1–8 | KEEP |
| Day 4 image-level vs object-level example | Good distinction | KEEP |
| Day 5 overlapping-CNN-regions SVG | Correctly marked as schematic | KEEP |
| Day 5 `ref_anomaly_panels.png` in Notebook 02 | Derived from saved TEST maps; shown before freeze | MOVE TO AFTER-FREEZE ARCHIVE; replace learner figure (A01) |
| Day 5 frozen-threshold protocol and hidden TEST panel | Proper safeguard in Notebook 03 | KEEP; fix stray forward pointer (A04) |

**Important:** More static images are **not** the main need in this new version. The outstanding improvement is precise placement, sequencing, provenance and one tiny executable example. Do not add illustrations merely to increase the image count.

## 4. Recommended Codex order and acceptance criteria

1. **A01 first:** establish which Day 5 assets expose TEST versus CALIBRATION. Move/replace the premature TEST panel and its numeric card. Update lesson, generator/reference manifest, archived instructor guide and relevant PDF exports only as needed. Add a regression that prevents reintroduction across all Day 5 pre-freeze notebook content.
2. **A02 and A04:** fix the two verifiable sequencing/caption contradictions. Do not alter correct working processing code.
3. **A03 and A05:** align the beginner prompt with a runnable variable example and defer/minimize floating-point distractions.
4. **A06:** explain `engine.test` versus `val_dataloader` with the smallest bilingual annotation.
5. **A07–A12:** leave as is unless a local classroom/presentation review establishes a specific need. Keep existing confirmed visuals.
6. Regenerate only affected Day 2–5 PDFs (and the combined Week1 PDF if needed to reflect the edits). Do not edit the approved Day 1 notebooks. Do not falsify fresh model scores or overwrite original archived figures.

**Verification to require from Codex (report actual results only):**

- Inspect working tree and repository HEAD first; never silently overwrite newer work.
- Execute source/structure checks, focused tests, then all affordable offline tests. Preserve writing exercises and intentional-error cells.
- When possible, execute the changed lightweight Day 2 lesson(s); report **skipped** heavy GPU/CPU training as skipped, not passed.
- Re-run local figure provenance checks and validate that Day 5 student-facing pre-freeze figures are calibration/synthetic only. The archived test panel must be inaccessible before freeze in the normal student workflow.
- Check Japanese/English text for the specific edited segments and all new figure captions.
- Check the rendered PDF pages around all changed material (no clipping, correct Japanese, no premature TEST example).
- Finish with an implementation log containing before/after excerpts, affected paths, tests actually executed, and unresolved limitations.

## 5. Scope enforcement

**DO NOT touch:** `notebooks/Day01_AI_Fundamentals/*`, Day 1-only teaching assets, environment setup, `start_training.cmd`, or previous source-review documents. Do not open Day 1 for improvements. Reading Day 1 metadata only to validate cross-day references is optional; changing its approved content is forbidden. Existing 15-notebook lessons should remain available. No new download dependency should be introduced for these limited fixes.

**Source links:**
- Updated commit: https://github.com/stefanoKS/Training_Automation/commit/9852b1949bd1180de801d52a5adb748dc963e00a
- Implementation log: https://github.com/stefanoKS/Training_Automation/blob/main/AI_Vision_Training/docs/reviews/Day01-Day05_Clarity_Implementation_Log.md
- Day 5 numeric map builder: https://github.com/stefanoKS/Training_Automation/blob/main/AI_Vision_Training/assets/scripts/generate_reference_outputs.py

**Confidence limits:** This is a direct source-level inspection of the latest repo and the relevant SVG text/geometry descriptions. I did not clone or execute the repository locally, run heavy models, or view every rendered PDF page; repository-recorded tests are reported as such, not independently certified.
