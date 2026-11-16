# Days 1–5 clarity implementation / 第1〜5日 明確化の実装記録

## Baseline and preservation / 基準と保全

- Inspected HEAD and local main: `beda393c7fc5d0873a8f4697c46ae114c3626395`.
- Read the complete supplied 2026-11-16 review before inspecting lessons.
- Inventory: 15 lesson notebooks and one setup notebook. Audit cell indices match HEAD;
  edits identify the corresponding source passages, not shifted numeric positions.
- Pre-existing deleted second-pass agent/audit files and untracked supplied task/review files
  are user work; leave them unchanged. Setup, CMD launcher, historical reports and
  `assets/reference_outputs` are not implementation targets.
- Below, notebook names abbreviate their unique filenames under `notebooks/`.
  The initial checklist below records the inventory-time plan, not outstanding work.
  Its initial Pending states are superseded by the final disposition tables and evidence below.

## Initial findings checklist (historical) / 着手時のチェックリスト

| ID | Target notebook / heading | Issue → required change; reusable asset | Intended validation | Initial status |
|---|---|---|---|---|
| D1-01 P1 | Day01_01 / training and inference | Weights-only definition → YOLO weights vs PatchCore memory; retain train/infer figure | Adjacent bilingual two-row comparison | Pending |
| D1-02 P2 | Day01_01 / learned rule | Statistics too early → five-value first pass, optional Gaussian section; reuse nested/rule/Gaussian figures | Main/optional reading route; numbers | Pending |
| D1-03 P2 | Day01_01 / automation | Workflow vs decision method → camera-to-log chain; move brightness example | Same-good-sheet provenance | Pending |
| D1-04 P1 | Day01_02 / resolution | Pixel count vs scale → fixed-FoV worked units; new V01 | 1300/1300 and 1300/13000; no detection guarantee | Pending |
| D1-05 P1 | Day01_02 / indexing and slicing | Scattered order → construct, predict, run pixel, run slice, transfer; reuse both correct SVGs | Executed arrays and highlighted bounds | Pending |
| D1-06 P2 | Day01_02 / RGB and resizing | Interpretation too distant → RGB/grey prediction, saved resize vs optics; reuse profiles | RGB arithmetic; local contrast | Pending |
| D1-07 P2 | Day01_03 / CV output families | Duplicate visuals/tables → four families/five outputs, mask then derived area; reuse SVG/modes | One common-input table; calibration caveat | Pending |
| D2-01 P2 | Day02_01 / operators | Advanced exceptions too early → optional notes; retain assignment figure | Predict assignment/comparison; no blanket rounding | Pending |
| D2-02 P2 | Day02_01 / mass exercise | Abstract units → adjacent dimensional chain; reuse mass SVG | 3.25 m², 1137.5 cm³, 1.5925 kg; unsolved exercise | Pending |
| D2-03 P1 | Day02_02 / if, list, loop, def | Switching specifications → stable 100±0.5 main route; label independent examples | Same five measurements; failing indices 3,4 | Pending |
| D2-04 P1 | Day02_02 / approved specification | Passing bad part by altering limits → fixed 11.8–12.2 transfer example | 12.200 OK; 12.201 NG; revision authorization | Pending |
| D2-05 P1 | Day02_02 / grade_width | C outside tolerance → independent severity and acceptance | C is NG; retain public grade strings | Pending |
| D2-06 P2 | Day02_02 / validation and tests | Advanced second pass → mark required if/for/def vs guided reliability; reuse branch | Parse failure logged vs valid NG | Pending |
| D2-07 P1 | Day02_03 / BGR | No visible counterexample → deterministic strip and tuples | Actual swapped/corrected pixels | Pending |
| D2-08 P1 | Day02_03 / threshold and contours | Disconnected stages → same-mask metrics and equality truth table; reuse pipeline | Threshold equality; 12 pixels vs 6 px² | Pending |
| D2-09 P2 | Day02_03 / calibration | Equations before detail; reuse same-plane/scale visuals | Existing 475/925 px² conversions | Pending |
| D3-01 P1 | Day03_01 / box conversion | Three formats disconnected → same rectangle plus x2 edit; reuse correct SVG | Width 96, centre x144; normalized bounds | Pending |
| D3-02 P2 | Day03_01 / YOLO and pretrained | Absolute speed/class claims → forward pass + postprocessing, unreliable unrelated labels | No production-speed promise | Pending |
| D3-03 P2 | Day03_02 / result fields | Object→row bridge → field tree, actual shapes; reuse result SVG/reference | N=0 supported; historical counts labelled | Pending |
| D3-04 P1 | Day03_03 / confidence experiments | Mixed contexts → A/B/C source table, explicit fixed candidates | No imgsz/candidate-pool equivalence claim | Pending |
| D3-05 P2 | Day03_03 / evaluation | Image vs box counts → two-image worked example; link Day4 | TP image despite FN box | Pending |
| D4-01 P2 | Day04_01 / label file | File/class/image bridge → existing train_0002 line and checked overlay | Integer class 2, four normalized values | Pending |
| D4-02 P2 | Day04_01 / splitting | Overlap → one question per figure, session grouping | Hash != capture independence | Pending |
| D4-03 P1 | Day04_02 / epoch and batch | Optimizer internals first → simple 64/8 map before stage 2 SVG | Eight batches/epoch; not eight updates | Pending |
| D4-04 P2 | Day04_02 / run switch | Run vs interpret → artifact checklist, variable runtime, unique experiment names | Safe skip unchanged; archives unchanged | Pending |
| D4-05 P1 | Day04_03 / evaluation units | Unit/axes confusion → image vs box example before mAP; reuse matching figures | Numeric TP/FN, denominators and axes | Pending |
| D4-06 P1 | Day04_03 / test split | Always-test instruction → val tuning, freeze then final test | Missed images vs unmatched boxes | Pending |
| D5-01 P1 | Day05_01 / patches | Literal tiles remembered → overlap vs analogy side by side; new V13 | Schematic overlapping regions, not actual RF sizes | Pending |
| D5-02 P1 | Day05_01 / outputs | Two kinds vs three representations → scalar/map, raw/normalized/decision | Threshold uses declared image score, not map max | Pending |
| D5-03 P2 | Day05_01 / terminology | Research labels early → normal fit/calibrate/test/infer first | Optional terminology; no new dependencies | Pending |
| D5-04 P2 | Day05_02 / fitting | fit vs optimizer → state ledger; reuse frozen-backbone/stages | Unchanged weights; created memory; calibration threshold | Pending |
| D5-05 P1 | Day05_02 / numeric outputs | Formula before reading → saved-value card beside reference | Raw21.439/map21.762/normalized1.000 not probability | Pending |
| D5-06 P1 | Day05_03 / protocol | Overlapping workflows → primary six-stage flow + permissions | 6 normals × 10% permits zero sampled FP | Pending |
| D5-07 P1 | Day05_03 / panels and gallery | Three called five; TEST→CALIBRATION → retitle and print split | Three/five images correctly paired | Pending |
| D5-08 P1 | Day05_03 / holdout | Test exposed before freeze → gate evaluation and archive; written declaration | Block unacknowledged test; reused-data label | Pending |

## Initial visual checklist (historical) / 着手時の図チェックリスト

| ID | Target and design choice | Source/reuse | Intended validation | Initial status |
|---|---|---|---|---|
| V01 | Day01_02 fixed 1300-mm FoV, two sampling densities | New editable SVG + PNG | Computed units and 0.3-mm span, render | Pending |
| V02 | Day01_02 live 5×7 highlighted selection | Reuse pixel inspector and slice SVGs | Same array and stops as executed code | Pending |
| V03 | Day01_02 downsample local profile | Reuse downsample/profile images + live output | Subpixel contrast caveat; no redundant SVG | Pending |
| V04 | Day02_02 row-by-row numeric trace | Reuse loop trace + printed live trace | Exactly five rows; i3/i4 NG | Pending |
| V05 | Day02_02 parse vs tolerance two-track flow | Text flow beside existing branch visual | Invalid input logged, never called OK | Pending |
| V06 | Day02_03 swapped/correct strip | New live NumPy/OpenCV output | Channel tuples; no download | Pending |
| V07 | Day02_03 image/mask/contour | New live tiny experiment + existing pipeline | Same mask, count vs geometry | Pending |
| V08 | Day03_01 synchronized box table | Reuse correct bbox SVG + live table | x2-only experiment and normalized limits | Pending |
| V09 | Day03_02 result tree | Reuse existing result-object SVG; textual schema | Actual field shapes and table wiring | Pending |
| V10 | Day03_03 provenance table only | Existing toy/archive/live plots | Dataset, imgsz, confidence floor explicit | Pending |
| V11 | Day04_02 eight-row batch map | Live printed map; existing stage-2 SVG | 64 images, batch8, 15 passes | Pending |
| V12 | Day04_03 evaluation worked table | Existing matching/confusion SVG/PNGs | Per-image vs per-box counts and axes | Pending |
| V13 | Day05_01 disjoint analogy vs overlap | New editable schematic SVG + PNG | Grid indices/overlap mechanically checked | Pending |
| V14 | Day05_02 saved numeric annotation card | Existing reference panel, adjacent Markdown overlay key | No fabricated historical pixels/results | Pending |
| V15 | Day05_03 calibrate→freeze→test | Reuse frozen pipeline as primary; permissions table | Data roles, sampled cap, archive gate | Pending |

## Final finding dispositions / 指摘ごとの完了記録

All 35 findings have an implemented teaching change. All 19 P1 findings are addressed;
the existing correct illustrations were verified and reused, not redrawn indiscriminately.
These dispositions concern lesson implementation, not certification of new model accuracy.

| ID | Final disposition and before → after evidence |
|---|---|
| D1-01 | Implemented: weights-only account → adjacent YOLO weight updates / PatchCore frozen features and normal-memory fit comparison. |
| D1-02 | Implemented: statistics-first path → five synthetic readings and a learned toy minimum; taxonomy/Gaussian detail is optional. The minimum 198 is not a production acceptance specification. |
| D1-03 | Implemented: automation confused with AI → camera→preprocess→decision→log workflow separated from the decision method; brightness-shift example brought next to the explanation. |
| D1-04 | Implemented: pixel count treated as scale → fixed 1300-mm inspected-plane width and mm/px arithmetic; saved-image enlargement explicitly cannot recapture optical detail. |
| D1-05 | Implemented; correct assets verified/reused: scattered examples → executable 5×7 creation, pixel, reversed indices, exact 3×3 slice and 6×6 defect-image transfer. |
| D1-06 | Implemented: distant interpretation → adjacent RGB/weighted-grey prediction and resize-versus-recapture contrast, retaining measured local profiles and their limits. |
| D1-07 | Implemented: duplicate visual/table → one retained task SVG and common-input output/limitations table, four families versus five outputs, mask versus derived area. |
| D2-01 | Implemented: operator caveats interrupt first pass → negative floor division, floats and assignment expression marked optional; assignment/comparison prediction stays on main path. |
| D2-02 | Implemented: abstract formula → dimensional chain immediately beside the exercise. Existing unsolved code is unchanged; 3.25 m²→1137.5 cm³→1.5925 kg is explained outside it. |
| D2-03 | Implemented: apparently changing rules → 100.0±0.5-mm main route and same five readings; 12.0±0.2 and 12.50±0.10 are explicitly independent transfer examples. Live trace exposes difference, condition and verdict. |
| D2-04 | Implemented: widen limits to accept 12.201 → approved inclusive 11.8–12.2 remains fixed; 12.200 OK and 12.201 NG. Any legitimate revision requires separate authorization/traceability. |
| D2-05 | Implemented: severity mistaken for acceptance → C/D are explicitly NG; public grade strings retained and independent acceptance printed/tested. |
| D2-06 | Implemented: reliability internals compete with if/for/def → guided second-pass route and parse→reject/log versus valid measurement→tolerance text flow. |
| D2-07 | Implemented: only verbal BGR warning → synthetic strip, printed tuples and wrong/correct displays. Final execution verifies that imports and show helper precede this demo. |
| D2-08 | Implemented: separate images for concepts → one 7×8 source, inverse mask and contour; equality truth table and actual 12-pixel versus 6-px² measurements. Existing 2→1→18 example now distinguishes merging from noise. |
| D2-09 | Implemented; correct assets verified/reused: unit equations placed before same-plane calibration; geometric area remains distinct from foreground-pixel count. |
| D3-01 | Implemented; correct bbox SVG reused: disconnected formats → synchronized xyxy, OpenCV top-left xywh and normalized YOLO rows. x2+24 changes width/centre; invalid bounds raise ValueError. |
| D3-02 | Implemented: one-calculation/speed/class absolutes → forward pass plus postprocessing, no guaranteed production speed, COCO lacks intended defect classes but can return unrelated classes. Checkpoint/export detail is optional. |
| D3-03 | Implemented; result SVG reused: results→results[0]→boxes→row bridge with actual field shapes, zero-row case and explicitly historical saved result. |
| D3-04 | Implemented: mixed counts → A toy / B archived52 / C1 live640 / C2 live320 provenance table. C1 filters one conf=.05 candidate cache; C2 remains a separate experiment. Unknown archived settings are not silently assumed equal. |
| D3-05 | Implemented: detection counts conflated → two-image example where image TP can coexist with a missed object; explicit bridge to Day4 object matching. |
| D4-01 | Implemented: abstract annotation row → actual train_0002 label, class 2: streak, current synthetic image/overlay and checks of class integer plus four normalized fields. |
| D4-02 | Implemented: repeated generic split captions → separate questions and A/train, B/val, C/test capture-session example; differing hashes do not establish independence. |
| D4-03 | Implemented; advanced SVG retained: accumulation-first → simple 64-image/eight-batch first pass, then optional optimizer detail. 120 loader batches over 15 epochs are not asserted to be 120 optimizer updates. |
| D4-04 | Implemented: run switch without reading plan → artifact checklist, runtime caveat and RUN_NAME with exist_ok=False; original safe skip and saved training run preserved. |
| D4-05 | Implemented: mixed evaluation units → image TP=1 versus object TP=1,FN=1 before mAP; counting units, denominators and confusion-matrix axes identified. |
| D4-06 | Implemented: test as routine tuning → validation for selection, freeze, then final test; missed images separated from unmatched ground-truth boxes. |
| D5-01 | Implemented: literal disjoint tiles → early CNN-feature definition and side-by-side overlap schematic; explicitly not measured resnet18 receptive fields. |
| D5-02 | Implemented: two outputs versus three apparent outputs → scalar/map output kinds, raw/normalized representations and decision stage. Map maximum is not silently used as image score. |
| D5-03 | Implemented: research terminology first → fit/calibration/test/inference role table before optional terminology. |
| D5-04 | Implemented; stages diagram reused: training verb suggests optimizer → state ledger distinguishes unchanged weights, created memory, calibration statistics/threshold and subsequent inference. |
| D5-05 | Implemented: formula first → adjacent reading card for unchanged saved panels: raw21.439, heatmapMax21.762, normalizedImage1.000, image threshold0.50; no probability claim or fabricated inference. |
| D5-06 | Implemented; primary pipeline SVG reused: overlapping workflows → six-stage protocol, permissions and calibration counts. Six normal calibration images at 10% allow zero sampled false rejects, not a population guarantee. |
| D5-07 | Implemented: three called five and unclear split → actual three-panel title, explicit CALIBRATION gallery boundary/printed labels, separate archived five-column TEST appendix. |
| D5-08 | Implemented: answers/test before freeze → calibration controls first, required written freeze declaration, persisted state snapshot, changed-setting guards, then test. TEST_ALREADY_SEEN=True safely labels reused data; historical TEST answers are opt-in only after freeze/evaluation. |

### Proposed rewrite mapping / 改稿例との対応

| Rewrite | Applied adaptation |
|---|---|
| R01 | Day01_02 exact slice construction, selected indices, exclusive stops, executed array and edit-follow-up. |
| R02 | Day02_02 approved specification is fixed; failed measurement remains NG. |
| R03 | Day03_03 confidence provenance, shared candidate floor and separate imgsz contexts. |
| R04 | Day05_01/02 separate score kinds/scales and same-scale threshold; not probability. |
| R05 | Day04_03 and Day05_03 validation/calibration→freeze→final test chronology with reused-data qualification. |

## Final visual dispositions / 図ごとの完了記録

| ID | Disposition | Actual evidence |
|---|---|---|
| V01 | New SVG + PNG | Computed 1300-mm field, 1300/13000 px, 0.3/3-px defect span. Mark/grid explicitly schematic. Exact PNG found in Day01 PDF p36. |
| V02 | Reused + live output | Original correct pixel/slice SVGs unchanged; live highlighted 5×7 data and exact selected 3×3 array agree. |
| V03 | Reused; optional widget omitted | Existing downsample/local-profile figures and live resize suffice; no dependency-heavy or redundant dynamic widget. Subpixel contrast caveat retained. |
| V04 | Reused + live trace | Same five measurements; printed signed difference, condition and verdict, with NG at indices 3 and 4. Expected-output text identifies extra trace lines. |
| V05 | Text alternative implemented | Bilingual parse/reject/log versus tolerance flow beside existing branch visual; another static image would duplicate it. |
| V06 | Live synthetic output | BGR strip has printed [0,0,255] / [255,0,0] and wrong/correct display from the same array; no external asset. |
| V07 | Live synthetic output | One image/mask/contour sequence gives count12 versus area6; wider-region edit gives count15 versus area8. |
| V08 | Reused + live table | Correct original rectangle SVG unchanged; both coordinate rows mechanically computed, including x2 edit. |
| V09 | Reused + schema | Existing result-object SVG plus adjacent returned-object tree and shape/empty-result explanations; no duplicate SVG. |
| V10 | Table only | Toy/archive/live provenance table separates 640 and 320 candidate pools; saved metrics not regenerated. |
| V11 | New SVG + PNG + live map | Exactly eight rows of eight IDs, 0–63; simple stage before unchanged accumulation SVG. Exact PNG found in Day04 PDF p27. |
| V12 | Reused + worked table | Existing matching/confusion visuals retained; image/object example and denominators added before advanced metrics. |
| V13 | New SVG + PNG | Computed 4×4 grid/positive overlap, feature-location labels, explicit schematic limits. Exact PNG found in Day05 PDF p13. |
| V14 | Adjacent annotation card | Saved reference pixels unchanged; numeric reading order is annotated in Markdown, not painted into archived output. |
| V15 | Reused + reordered protocol | Primary frozen-pipeline SVG, permissions, calibration counts and freeze record; TEST archive gated and CALIBRATION gallery unmistakably labelled. |

Only three static diagram pairs were added. New diagrams use local drawing primitives/fonts
and no external photographs, model output, redistributed fonts or new packages.
All numeric labels derive from shared constants/loops; deterministic generation and text bounds
are tested. The original figure generator now preserves the new manifest section, and the
legacy inserter cannot restore retired panels or overwrite explicitly curated captions.

## Sources actually changed / 変更したファイル

All three lesson notebooks in each day changed; setup did not:

- Day1: [introduction](../../notebooks/Day01_AI_Fundamentals/Day01_01_Introduction_to_AI.ipynb),
  [pixels](../../notebooks/Day01_AI_Fundamentals/Day01_02_Pixels_and_Images.ipynb),
  [tasks](../../notebooks/Day01_AI_Fundamentals/Day01_03_Computer_Vision_Tasks.ipynb).
- Day2: [basics](../../notebooks/Day02_Python_OpenCV/Day02_01_Python_Basics.ipynb),
  [conditions/loops/functions](../../notebooks/Day02_Python_OpenCV/Day02_02_Conditions_Loops_Functions.ipynb),
  [OpenCV](../../notebooks/Day02_Python_OpenCV/Day02_03_OpenCV_Image_Processing.ipynb).
- Day3: [concepts](../../notebooks/Day03_YOLO_Basics/Day03_01_YOLO_Concepts.ipynb),
  [inference](../../notebooks/Day03_YOLO_Basics/Day03_02_YOLO_Inference.ipynb),
  [experiments](../../notebooks/Day03_YOLO_Basics/Day03_03_YOLO_Experiments.ipynb).
- Day4: [annotation](../../notebooks/Day04_YOLO_Training/Day04_01_YOLO_Dataset_Annotation.ipynb),
  [training](../../notebooks/Day04_YOLO_Training/Day04_02_YOLO_Training.ipynb),
  [evaluation](../../notebooks/Day04_YOLO_Training/Day04_03_YOLO_Evaluation.ipynb).
- Day5: [concepts](../../notebooks/Day05_PatchCore/Day05_01_Anomaly_Detection_Concepts.ipynb),
  [training](../../notebooks/Day05_PatchCore/Day05_02_PatchCore_Training.ipynb),
  [comparison](../../notebooks/Day05_PatchCore/Day05_03_YOLO_vs_PatchCore.ipynb).

Supporting sources and documentation:

- New [generate_clarity_figures.py](../../assets/scripts/generate_clarity_figures.py)
  and [test_clarity_review.py](../../assets/tests/test_clarity_review.py).
- Updated [generate_svg_figures.py](../../assets/scripts/generate_svg_figures.py),
  [insert_lesson_figures.py](../../assets/scripts/insert_lesson_figures.py),
  [test_visual_assets.py](../../assets/tests/test_visual_assets.py)
  and [visual_figure_manifest.md](../visual_figure_manifest.md).
- New [after-freeze instructor appendix](../instructor/day05_after_freeze_archive.md)
  and this implementation log.
- New asset pairs: `assets/svg/teach_fixed_fov_sampling.svg`,
  `assets/svg/teach_batch_first_pass.svg`, `assets/svg/teach_patch_overlap.svg`;
  matching `assets/diagrams/teach_fixed_fov_sampling_svg.png`,
  `assets/diagrams/teach_batch_first_pass_svg.png`,
  `assets/diagrams/teach_patch_overlap_svg.png`.
- Rebuilt `docs/pdf/Day01_explanation_ja_en.pdf`, `Day02_explanation_ja_en.pdf`,
  `Day03_explanation_ja_en.pdf`, `Day04_explanation_ja_en.pdf`,
  `Day05_explanation_ja_en.pdf` and `Week1_explanation_ja_en.pdf`.
  The exporter currently rebuilds even with `--check`; this was observed, not assumed
  to be a read-only command.

## Validation and final evidence / 検証と完了記録

### Commands actually executed

Course working directory: `I:\GithubProjects\Training_Automation\AI_Vision_Training`.
Runtime: existing `..\.venv\Scripts\python.exe` (Python 3.11.4).
PowerShell output encoding was set with `$env:PYTHONIOENCODING='utf-8'`.

```powershell
git --no-pager status --short
git rev-parse HEAD
& ..\.venv\Scripts\python.exe assets\scripts\generate_clarity_figures.py
& ..\.venv\Scripts\python.exe assets\scripts\validate_notebooks.py --report C:\Users\stefa\.copilot\session-state\da3b4320-e584-4c26-96e0-893ed0a3061b\files\clarity-structure.json
& ..\.venv\Scripts\python.exe -m pytest assets\tests\test_clarity_review.py assets\tests\test_notebooks.py assets\tests\test_visual_assets.py -q --tb=short
& ..\.venv\Scripts\python.exe -m pytest assets\tests -q --tb=short
& ..\.venv\Scripts\python.exe assets\scripts\export_explanations_pdf.py --check
& ..\.venv\Scripts\python.exe C:\Users\stefa\.copilot\session-state\da3b4320-e584-4c26-96e0-893ed0a3061b\files\execute_clarity_lightweight.py
git --no-pager diff --check
```

Additional executed checks used PowerShell Python here-strings:

- Repository `normalize_language_labels.clean_notebook(path, write=True)` on only the
  15 lesson notebooks; no historic reports were normalized.
- Repository `validate_notebooks.execute_notebook(..., timeout=180)` for corrected
  Day02_02/03 in the private course copy, updating `clarity-execution.json`.
- HEAD-versus-working JSON comparison of all 16 notebook-level metadata/format versions,
  original cell IDs, metadata, unsolved write-code cells and tagged intentional-error sources.
- Git protected-path checks of setup, CMD, saved reference outputs and four explicitly
  protected correct SVGs.
- PyPDF/PIL hash comparison located the three exact new PNG fallbacks in the PDFs;
  PDFium rendered those pages at scale1.4 and half-scale0.7, with printable-area checks.
  The archived five-column TEST PNG was also checked absent from the Day5 student PDF.
- Browser SVG `getBBox()` checks found no out-of-canvas text in any new SVG.
  PNGs and all six new-figure PDF previews were visually inspected.
- Pylance syntax checks passed for the new generator/test, changed SVG generator and inserter.

### Final result table

| Check | Result | Scope / qualification |
|---|---|---|
| Full existing course pytest suite plus focused regressions | **330 passed**, 4 warnings, 94.50 s | Final run after lesson, generator and test edits. Warnings are expected Agg noninteractive display notices. |
| Actual notebook structural validator | **194 passed, 0 failed** | All 16 parses, code compilation, JP-first checks, roles, required sections and local image links. |
| Actual notebook executor | **10 lightweight notebooks passed** | Setup, all Day1/2, Day03_01, Day04_01, Day05_01; original tagged setup NameError accepted by repository convention. |
| Protected behavior/content | Passed | Original notebook metadata/format, all original cell IDs, write-code exercises and intentional-error sources preserved; see deliberate role exception below. |
| New static diagrams | **3/3 passed** | Determinism, bounds, numeric/overlap checks, offline assets, browser rendering and PNG inspection. |
| PDF export/check | **6/6 passed** | Day1–5: 72/86/56/68/63 pages; combined Week1: 334 pages. Japanese text survives extraction. |
| New-figure PDF spot checks | **3/3 exact-image matches; no overflow** | Day1 p36, Day4 p27, Day5 p13; full/half previews inspected. Not a manual review of every PDF page. |
| Whitespace / protected files | Passed | `git diff --check`; setup, CMD, saved reference outputs and named correct diagrams unchanged. HEAD remains baseline SHA. |

The private execution copy used session-local `aivision` and `anomalib` kernelspec aliases
to the existing base Python, without changing user kernels. Day05_01 is conceptual/lightweight;
its pass does **not** certify the separate full Anomalib training environment.
Execution writes stayed in that copy, not learners' submissions or archived reference outputs.

One existing cell's role metadata was deliberately corrected: Day05_03 `d38ae876`
is the editable calibration fallback, now `change-value` instead of `run-only`, with matching
bilingual banner. Original tags and other original metadata remain intact. Added figure-caption
metadata protects curated explanations from the legacy inserter. Targeted teaching-block
reordering is intentional; notebook structure and original cells were not wholesale rebuilt.

### Numerical checks

- Fixed field: 1300/1300=1 mm/px; 1300/13000=0.1 mm/px.
  A 0.3-mm feature spans 0.3 or 3 px geometrically, not a guaranteed detectable defect.
- Array: `canvas[2,3]=100`, `canvas[3,2]=0`;
  `canvas[1:4,2:5]` is `[[0,0,0],[0,100,0],[0,0,0]]`, shape3×3.
  Column stop6 instead gives shape3×4.
- Mass: 2.5×1.3=3.25 m²; thickness0.35 mm gives1137.5 cm³;
  density1.4 g/cm³ gives1.5925 kg.
- Approved 12.0±0.2-mm specification: 12.200 OK, 12.201 NG;
  C-grade deviation0.6 remains NG under the separate 100±0.5-mm example.
- Inverse threshold100: values below or equal to100→255, greater→0.
  Filled 3×4 region has12 white pixels but contour area(4−1)(3−1)=6 px².
- Original box(96,72,168,132) in240×240→YOLO(.55,.425,.30,.25);
  x2+24→centre(144,102), size(96,60), YOLO(.60,.425,.40,.25).
- Label file remains `2 0.410938 0.485938 0.421875 0.034375`.
- 64 images/batch8=8 loader batches per epoch; 15 epochs=120 loader batches.
- Calibration cap: floor(6×0.10)=0 observed normal-image false rejects.
  Historical raw/map/normalized numbers are cited, not recomputed or invented.
- Freeze regression rejects empty declaration and changed thresholds/model settings;
  persisted default assessment role is `illustrative_reused_data`.

### Failures found and resolved

- First structural pass found three placement/expected-output contract failures;
  corrected figure placement and Day03_03 output heading.
- First focused suite had eight failures from obsolete visual expectations and caption
  contracts; registries now require retained/replacement SVGs, protect the TEST boundary
  and accept curated captions. Subsequent focused runs passed; final full run is330/330.
- Initial full lightweight execution found Day02_03 BGR demo before NumPy/OpenCV/show
  initialization (`NameError: np`). Moved the coherent three-cell demo after preparation,
  added ordering regression, reran affected Day2 lessons: all ten eligible executions pass.
- Initial preservation check stopped at the intentional editable-role correction;
  rerun with that single documented exception completed all16 and protected-path checks.
- Initial PDF lookup used unavailable PyMuPDF, then existing PyPDF/PDFium successfully;
  no package installed. Pylance calls requiring workspaceRoot were retried successfully.
  Browser preload warnings did not prevent DOM bounds checks or local rendering;
  independent PNG/PDF previews were inspected.
- A close feature-label/flow-label gap was spotted visually in V13 and spaced out,
  followed by regeneration, PDF rebuild and the final passing tests.

## Exact remaining verification / 未実施の確認

No finding ID or required visual disposition is left unimplemented. These verification
limits remain explicit:

1. Full execution of **Day03_02, Day03_03, Day04_02, Day04_03, Day05_02, Day05_03**
   was not performed: these are the six download/training/model-dependent categories.
   No heavy training, model download, new metric run or accuracy comparison was initiated.
   Their code compiles; relevant lightweight numeric/protocol cells have focused tests.
2. No native full Anomalib-environment certification or interactive widget click-through.
   The plain calibration fallback and protocol guards have no-model tests.
3. Full human editorial equivalence review of every Japanese/English paragraph, every PDF
   page, and a complete-beginner classroom timing/pilot remain manual follow-up.
   Automated bilingual/link checks and changed explanations/new-visual spot checks passed;
   they are not a claim of exhaustive human translation review.
4. An independent final model assessment requires a genuinely untouched partition.
   The course's already exposed examples deliberately default to reused-data illustration,
   not an untouched-test claim. No untouched dataset or new production result was fabricated.

No commits, pushes or merges. No Days6–10 work. Original audit/historic test reports,
pre-existing user changes, startup CMD and saved model metrics were left intact.
