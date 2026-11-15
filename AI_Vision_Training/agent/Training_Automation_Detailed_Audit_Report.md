# Training_Automation — Detailed Audit and Remediation Specification

**Date:** 2026-11-15 (Japan time)  
**Repository:** https://github.com/stefanoKS/Training_Automation  
**Branch inspected:** `main`  
**Root:** `AI_Vision_Training/`  
**Git tree observed:** `b8c496f8c0c96ff027adb148669d3c29e56e9b03`  
**Scope:** Day 0 setup + Day 1–5, all 16 notebooks; instructional text; generated diagrams; reference outputs; installation and validation documentation.

> **Evidence and scope:** This document expands an inspection of the notebook source, selected diagrams inspected visually, the diagram-generation source, and repository documents. The current tree contains 16 notebooks and 55 PNG files under `assets/diagrams/`. Existing repository reports say 16/16 notebooks were executed and 258 tests passed in an earlier run; **those reports are not a fresh independent execution by this audit**. Do not interpret uninspected image pixels, current training accuracy, or exact runtime behavior as verified by this audit. Reproduce and verify findings before changing code where noted.

## 0. Executive summary

### Educational objective
Two students with no programming background should be able to explain **what enters each important code cell, what each line changes, why the output is what it is, and how the output changes when they edit an input**. Visuals should be correct and traceable to actual code, not merely attractive. All teaching explanations should appear in the order **Japanese, then English**, without `日本語:` / `English:` prefixes, and work offline after setup.

### Overall result
- Strong foundation: bilingual explanations; guided experiments; topic-specific notebooks; an unusually large set of purpose-built diagrams; explicit caveats for held-out evaluation and synthetic imagery.
- Highest-value fixes: setup workflow contradiction; one **geometrically inconsistent** four-task comparison diagram; a **physically unjustified** conversion from pixels to mm² between unrelated synthetic images; outdated comparison documentation; incorrect implication from a duplicate-file checker; easier tracing of Python code into visuals.
- Avoid blanket redesign. Retain accurate diagrams such as `teach_array_indexing.png`, `teach_iou_rects.png`, the image-level confusion matrix, the memory-bank schematic, and the threshold-freeze explanation. Simplify or supplement only as needed.
- Prefer **code-authored SVG** for vectors, coordinates, flowcharts, data structures, unit diagrams and mathematical annotations. Continue using PNG/JPEG for real inspection images, actual model heatmaps, actual model predictions and existing reproducible reference outputs. Do not fabricate results.

## 1. Evidence-based correction register

The following findings are ordered by severity. `P0` means fix before the training; `P1` means fix for beginner comprehension; `P2` is polish/robustness. File paths are relative to `AI_Vision_Training/` unless noted.

### TA-001 — P0 — Conflicting setup/preflight instructions
**Affected:** `START_HERE.md`, `COURSE_SYLLABUS.md`, `notebooks/00_Setup/00_Environment_Setup.ipynb`, possibly `README.md` and instructor preflight guide.

**Observed:** `COURSE_SYLLABUS.md` says to finish both kernels and preflight before Day 1; `START_HERE.md` requires both kernels at its Day 1 readiness check, but does not install `.venv-anomalib` until a later section describing it as optional until after Day 4. `START_HERE.md` also has two sections both labelled Step 7 and places asset generation after a readiness check that expects an image. The setup notebook labels itself as Day 0 done in the morning of Day 1, whereas the syllabus separates preflight from the 5-day program.

**Required fix:** Pick one authoritative sequence that matches course logistics: download/clone → Python 3.11 environment → base + YOLO packages → separate anomalib environment → register both kernels → generate assets/datasets → preload offline reference samples and model weights → verify environments → launch Jupyter → readiness checklist → lessons. If an after-Day-4 installation path remains, make it a clearly labelled **alternative** with different readiness criteria; do not describe it as the default. Make numbering unique and ensure no check precedes its prerequisites. Distinguish setup exercise from install preflight.

**Acceptance:** First-time student can follow `START_HERE.md` linearly on a clean Windows 11 PC; every checked artifact has been created; `COURSE_SYLLABUS.md` and setup notebook agree; no duplicate numbered steps. No unexpected admin privileges or machine-wide PowerShell policy changes when a process-scoped alternative suffices.

### TA-002 — P0 — Same-defect comparison visual uses different defect geometry
**Affected:** `assets/scripts/generate_teaching_diagrams.py` → `teach_cv_tasks_outputs()`, generated `assets/diagrams/teach_cv_tasks_outputs.png`, `notebooks/Day01_AI_Fundamentals/Day01_03_Computer_Vision_Tasks.ipynb`.

**Observed:** The source image is generated by `_pvc_sheet(200, defect="spot", seed=44)`, whose spot mask is circular with radius `size * 0.045` = **9 px**. `teach_cv_tasks_outputs()` independently draws a segmentation region with radius **22 px** at approximately the same centre; the drawn detection box is derived from this larger region. The figure describes all four outputs as the same defect. The segmentation panel therefore overstates the defect footprint.

**Required fix:** Compute a single ground-truth mask and bounding rectangle from exactly the same pixel geometry as the source synthetic defect. Reuse it for segmentation and a perfect-box **ground-truth** illustration. If the intention is to show imperfect model predictions, draw predicted vs truth separately and state that an inaccurate mask/bounding box is deliberate. If stating `score=0.93` or `confidence=0.87`, mark those as **illustrative, not actual model outputs**. Include legible labels for each method's output and supervision type.

**Acceptance:** Automated test comparing the source image's dark-defect footprint and target mask/box within appropriate labelled tolerance; diagram labels never imply an invented model score is real; screenshot visually confirms same geometry in all panels.

### TA-003 — P0 — Cross-image physical scale used for contour area
**Affected:** `notebooks/Day02_Python_OpenCV/Day02_03_OpenCV_Image_Processing.ipynb` Part 5, Exercise 1; `assets/scripts/generate_training_assets.py` as needed.

**Observed:** Scale is computed from separately generated `assets/diagrams/calibration_image.png` / `calibration_ground_truth.json` and later used in an exercise to convert contours detected on `assets/defect_samples/defect_multi.png` to mm². Their shared world scale is not established. The formula `area_mm2 = area_px2 / (px_per_mm ** 2)` is conditionally correct; its *application to a different synthetic image* is not supported.

**Required fix:** Prefer a **new calibrated sample** in which a known 50/100 mm reference marker and defects share the same synthetic camera geometry and image plane. Calculate scale on that image, detect contours there, and compare with an independently generated known-size validation feature. Alternatively, if reusing the old asset for arithmetic practice, state prominently that the scale is an arbitrary assumption, not a physical measurement. Keep the existing independent 50 mm validation concept. Explain that real camera calibration must consider perspective, distortion, variation across the field, and uncertainty.

**Acceptance:** One image (or documented shared calibrated acquisition) supplies both reference length and contours; expected units and values match executable code; a test checks length and area conversion; no unqualified production-scale claim.

### TA-004 — P0 — Historical biased comparison is still the prominent report
**Affected:** `docs/test_report.md` Section 5.4 and limitations, `docs/implementation_report.md` references, `assets/reference_outputs/README.md` if necessary; latest `Day05_03_YOLO_vs_PatchCore.ipynb`.

**Observed:** The test report still foregrounds historical 26-image results (YOLO 17/26, PatchCore 26/26) while acknowledging the PatchCore threshold was tuned on the evaluation data itself. Day 5 Notebook 03 now uses calibration → freeze thresholds → evaluate test, writing `submissions/day05/comparison_test_results.json` and `.csv`. These distinct methods must not be conflated. The existing five-column reference also states a frozen comparison run with an illustrative case where `streak_0005` is a PatchCore miss.

**Required fix:** Move historical figures into a clearly labelled **superseded/biased comparison** section with dates and reasons. Main summary should point to a valid *recorded run* of the updated method only if source files and provenance are available; otherwise show methodology and a script that generates numbers from current persisted results after execution. Never claim a rerun occurred without actually running it. Preserve old values in an archival section to avoid destroying traceability. Verify fresh calibration/test counts and explain that synthetic results are not factory performance.

**Acceptance:** A reader cannot mistake historical contaminated results for current validation; every performance number is tagged with dataset partition, method, run metadata, and timestamp or explicitly marked historical.

### TA-005 — P1 — Exact-hash duplicate checker overclaims no leakage
**Affected:** `notebooks/Day04_YOLO_Training/Day04_01_YOLO_Dataset_Annotation.ipynb` Part 5; `teach_leakage_split.png` wording; `assets/scripts/generate_teaching_diagrams.py`.

**Observed:** The script hashes bytes with SHA-256. If no hash collision/duplicate is found, it prints `データ漏れはありません / no leakage detected`. Byte hashing cannot detect nearly identical frames, different encodings of identical pixels, repeated subjects, lot/session leakage, or correlated capture conditions. The diagram refers to a ±1 **intensity** perturbation; the phrase “sub-pixel noise” is misleading because pixels were not spatially shifted.

**Required fix:** Print `同一バイト列の画像は検出されませんでした / No byte-identical duplicate files detected`. Add `This does not rule out near duplicates or session/lot leakage.` Show image-level vs session-level split; explain separate perceptual-hash/SSIM and group-ID checks as enhancements, not guarantees. Replace `sub-pixel noise` with `±1 intensity-level noise`.

**Acceptance:** No test or output asserts zero data leakage merely from SHA; grouped split demonstration distinguishes exact duplicates, near duplicates, and dataset leakage by acquisition group.

### TA-006 — P1 — YOLO evaluation chooses model by pathname
**Affected:** `notebooks/Day04_YOLO_Training/Day04_03_YOLO_Evaluation.ipynb`, code cell selecting `best_weights`.

**Observed:** It gathers `*/weights/best.pt`, calls `sorted(...)`, and selects `candidates[-1]` while describing it as the latest run. Alphabetical path order does not guarantee recency or correctness.

**Required fix:** Prefer a persisted explicit output path/manifest from the Day 4 training notebook. Otherwise sort by `stat().st_mtime` while explaining that a chosen run ID is more reliable. Display chosen path, training parameters, and a clear warning if multiple candidates exist. Do not silently evaluate the wrong model.

**Acceptance:** Test with two controlled filenames and reversed timestamps; chosen file is correct per documented selection policy; message reveals file being used.

### TA-007 — P1 — Diagrams and code use different box values
**Affected:** `notebooks/Day03_YOLO_Basics/Day03_01_YOLO_Concepts.ipynb`; `teach_bbox_coords.png`; `assets/scripts/generate_teaching_diagrams.py`.

**Observed:** A diagram shows corners `(84,108)` and `(132,152)` on a 240×240 image. The nearby code computes using `(96,72)` and `(168,132)` on a 240×240 image. Each can be valid independently, but for a first-time student it obscures the link between diagram, equation and output.

**Required fix:** Make a single worked example with constants for image size, corner coordinates, centre, width and height, with `xyxy`, `xywh` and normalized YOLO `class_id xc yc w h`. Use exact example values in figure, code and explanatory text; preserve additional examples only when explicitly labelled separately. Include off-by-one/boundary conventions where relevant.

**Acceptance:** Tests recompute figure annotations from the source constants; student can manually verify all values with a calculator.

### TA-008 — P1 — Borderline tolerance evaluation obscured by silent rounding
**Affected:** `notebooks/Day02_Python_OpenCV/Day02_02_Conditions_Loops_Functions.ipynb` (the `judge()` example that rounds a difference to 6 decimals); related tolerance examples.

**Observed:** The code computes `difference = round(measured_mm - nominal_mm, 6)` before comparing to a limit, described as dropping floating-point noise. Rounding may affect which side of a limit a near-boundary value falls on, and hides the policy choice.

**Required fix:** Separate *measurement resolution*, *display formatting*, *floating-point tolerance*, and *acceptance criteria*. For the introductory rule use `abs(measured_mm - nominal_mm) <= tolerance_mm` with a documented boundary policy and suitable controlled examples; if exact decimal behavior is essential, consider `Decimal` and state why. Do not silently alter the acceptance rule across notebooks. Add a targeted boundary test for `99.5`, `100.5`, just within, just outside, and float representation examples.

**Acceptance:** Code, diagrams, text and tests agree at boundaries; no unsupported implication that rounding is always safe.

### TA-009 — P1 — Pixel-to-mm diagram readability and uncertainty label
**Affected:** `teach_pixel_to_mm.png` and generator; Day 2 Notebook 03.

**Observed:** Text overlaps the blue sheet's bottom edge. The prose refers to a “one-pixel error” while the numerical example assumes a **±0.5 pixel** edge-location uncertainty and yields **±0.25 mm** at 2 px/mm.

**Required fix:** Redraw as four clean, separate panels: (1) known reference; (2) derive px/mm and mm/px; (3) measure target; (4) propagate pixel location uncertainty. Label uncertainty and assumptions explicitly. Avoid claims of universal measurement accuracy.

**Acceptance:** Figure readable at notebook width; all calculations reproducible; source and target on same plane.

### TA-010 — P1 — Binary visibility criterion is too weak
**Affected:** `notebooks/Day01_AI_Fundamentals/Day01_02_Pixels_and_Images.ipynb`, resizing experiment.

**Observed:** A table infers `defect visible = YES/NO` using the global minimum pixel value after resizing (`darkest < 150`). This tests a thresholded intensity statistic, **not** whether the defect's shape is resolved, spatially locatable, or reliably detectable. It can be useful if accurately labelled.

**Required fix:** Rename to `minimum pixel below test threshold` / `最小画素値がしきい値未満か`, optionally add a separate spatial defect-location/contrast demonstration and discussion of downsampling filters. Distinguish sensing, model detection and human visual perception. The sample images and code output must still agree.

**Acceptance:** No statement equates one global min-pixel test with demonstrated defect detectability.

### TA-011 — P1 — Report/sample paths and setup documentation must converge
**Affected:** `COURSE_SYLLABUS.md` and setup/troubleshooting docs.

**Observed:** The syllabus references `submissions/reference_results/` as a fallback, but the committed reference figures are under `assets/reference_outputs/`. Confirm any additional expected submissions folders before changing.

**Required fix:** Use one canonical, existing directory for instructor-provided reference outputs. Document the distinction between real precomputed reference outputs and student-produced submission results; maintain offline availability.

**Acceptance:** All examples resolve locally; no broken fallback path.

### TA-012 — P2 — Complex diagrams are dense at notebook width
**Affected:** `teach_epoch_batch.png`, `teach_training_update.png`, `ref_comparison_5col.png`, `teach_threshold_freeze.png`, other diagrams with embedded 6–8 pt labels.

**Observed:** Many figures combine Japanese and English, variable definitions, graphs and captions on one wide canvas. They are accurate enough to retain, but text can become small in a normal Jupyter cell.

**Required fix:** Split dense material into overview and detailed figures, use larger type and label hierarchy, and move detailed paragraphs into adjacent Markdown rather than crowding an SVG. Preserve actual numeric output as raster where it is an empirical figure. For the five-column comparison, provide 3-row overview plus **one enlarged annotated disagreement** panel.

**Acceptance:** All essential figure annotations readable at ~900 px display width; use scalable SVG labels whenever possible; no overlap/clipping at exported PDF dimensions.

### TA-013 — P2 — Reference results and stochastic variability
**Affected:** Day 3–5 reference images and explanatory text.

**Observed:** Several figures display a specific reference run's learned thresholds, e.g. YOLO `0.06` and PatchCore `0.50`; training results can vary by installed environment and stochasticity. Existing language often says “recorded run”, which is correct and should be preserved.

**Required fix:** Label every source-dependent number as `illustrative`, `saved reference run`, or `student's current run` as appropriate. Never use a reference-run threshold as an unlabelled hardcoded expectation. Avoid making comparative quality claims from synthetic, small-sample scores.

**Acceptance:** Source/provenance label displayed beside all non-universal metrics and thresholds.

### TA-014 — P2 — Language and execution-state consistency
**Affected:** all notebooks, especially setup and Day 1–2.

**Observed:** The bilingual structure is generally good, but novice accessibility still varies: code comments and function arguments are sometimes introduced before their fundamentals. Repeated code-banner pairs should not become a wall of redundant English text.

**Required fix:** Run a bilingual clarity pass on all 16 notebooks, preserving Japanese-first then English. Use short declarative sentences; define `variable`, `array`, `channel`, `function`, `return`, `class`, `confidence`, `epoch`, `batch`, `threshold`, `training`, `inference`, `calibration` on first meaningful use. Identify intentional learner mistakes, not accidental code defects. Do not change intended exercises into supplied solutions.

**Acceptance:** Every notebook has a concrete goal, prerequisite, code↔visual alignment, an output interpretation, a *predict → run → explain → modify* question, troubleshooting and checklist; terms consistent across JP/EN.

---

## 2. Notebook-by-notebook teaching changes

Below, **Fix** denotes a confirmed or plausibly testable problem. **Improve** denotes a pedagogical recommendation, not an assertion of incorrectness. Paths are `notebooks/<folder>/<file>.ipynb`.

| Notebook | What is good / preserve | Fix / improve | SVG or instructional asset target |
|---|---|---|---|
| `00_Setup/00_Environment_Setup.ipynb` | Explains PowerShell vs notebook cell, environment, kernel, intentional NameError, first pixels | **Fix** its Day 0 scheduling description against preflight; **improve** visual link from run button to cell status and variable state | `teach_code_cell_lifecycle.svg`, `teach_actual_course_folders.svg` (real repo paths) |
| `Day01_AI_Fundamentals/Day01_01_Introduction_to_AI.ipynb` | AI/ML/DL, rules versus learned thresholds, Gaussian caveat, lighting shift | **Improve** examples that introduce advanced `def`, arrays and statistics before Python basics; explain only as preview | `teach_brightness_learning_trace.svg`: 200 values → mean/std → ±3σ → new value → judgement |
| `Day01_AI_Fundamentals/Day01_02_Pixels_and_Images.ipynb` | Shape, indexing, RGB channels, slicing, image construction | **Fix** global-min proxy wording (TA-010); **improve** exact array trace | `teach_pixel_inspector.svg`, `teach_slice_walkthrough.svg` and tested raster resize profile |
| `Day01_AI_Fundamentals/Day01_03_Computer_Vision_Tasks.ipynb` | Four CV tasks, segmentation modes, normal/abnormal | **Fix** source spot/mask mismatch (TA-002), clarify actual vs schematic scores | `teach_cv_tasks_outputs.svg` backed by same mask/box as image |
| `Day02_Python_OpenCV/Day02_01_Python_Basics.ipynb` | Arithmetic, strings, assignment vs equality, tracebacks | **Improve** density problem: size and dimensional conversions add cognitive load | `teach_mass_units_chain.svg`: mm³ → cm³ → g → kg, using exercise values |
| `Day02_Python_OpenCV/Day02_02_Conditions_Loops_Functions.ipynb` | Conditions, loop stepper, function IO, assert and exception exercises | **Fix/clarify** silent rounding at tolerance boundary (TA-008); **improve** function call/state trace | `teach_if_live_trace.svg`, `teach_loop_iteration_trace.svg` |
| `Day02_Python_OpenCV/Day02_03_OpenCV_Image_Processing.ipynb` | BGR/gray/threshold/contours, 3–4–5 distance, calibration limitations | **Fix** cross-image scale (TA-003); **improve** threshold graph complexity and mm uncertainty layout | `teach_opencv_pixel_pipeline.svg`, `teach_calibration_same_plane.svg` |
| `Day03_YOLO_Basics/Day03_01_YOLO_Concepts.ipynb` | Confidence, IoU and normalized labels | **Fix** mismatched box values (TA-007); label `xyxy` vs `(x,y,width,height)` clearly | `teach_bbox_one_example.svg`, `teach_iou_cases.svg` |
| `Day03_YOLO_Basics/Day03_02_YOLO_Inference.ipynb` | Real YOLO inference and saved boxes/CSV | **Improve** the structure of Ultralytics `Results` and `Boxes`; avoid obscure result access | `teach_yolo_result_object.svg` with `cls`, `conf`, `xyxy`, `.plot()` and CSV |
| `Day03_YOLO_Basics/Day03_03_YOLO_Experiments.ipynb` | Confidence sweeps, false alarms/misses, resizing studies | **Improve** separation of detector confidence filtering versus image downsampling / reprocessing | `teach_confidence_filter_vs_resize.svg` |
| `Day04_YOLO_Training/Day04_01_YOLO_Dataset_Annotation.ipynb` | Good label-field diagram, dataset splits and leakage section | **Fix** overclaiming hash conclusion (TA-005); group split semantics | `teach_group_split_vs_frame_split.svg` |
| `Day04_YOLO_Training/Day04_02_YOLO_Training.ipynb` | Useful training parameters, actual loss columns and accumulation description | **Improve** readability of `epoch`, `batch`, optimizer update, train vs validation loss | `teach_epoch_batch_step.svg`, `teach_training_forward_backward.svg` |
| `Day04_YOLO_Training/Day04_03_YOLO_Evaluation.ipynb` | Distinguishes image-level vs object-level metrics | **Fix** model selection policy (TA-006); **improve** TP/FP/FN matching steps | `teach_detection_matching.svg` |
| `Day05_PatchCore/Day05_01_Anomaly_Detection_Concepts.ipynb` | Good normal-only concept and nearest-neighbour illustrations | **Improve** clarify 2D feature space is illustrative, not image x/y space | `teach_patch_to_feature_vector.svg` |
| `Day05_PatchCore/Day05_02_PatchCore_Training.ipynb` | Frozen pretrained backbone vs stored normal features; score/map distinctions | **Improve** explicitly separate fit of memory, fitted calibration/postprocessor, and threshold; avoid implying score always 0–1 | `teach_patchcore_stages.svg` |
| `Day05_PatchCore/Day05_03_YOLO_vs_PatchCore.ipynb` | Updated holdout method and matching images; excellent error-analysis opportunity | **Fix** associated historical reporting (TA-004); **improve** the narrow 5-column result and sample-size caveats | `teach_frozen_threshold_pipeline.svg`, `teach_streak_false_negative_case.svg` |

**Important:** The names listed are specifications for new or revised assets, **not evidence that those files currently exist**. Codex should avoid redundant duplicates if a corrected existing diagram already fulfills the same teaching purpose.

## 3. Detailed SVG briefs and data-integrity contracts

SVG is appropriate where a precise vector can be programmatically built and checked. Embed Japanese and English in each image only where legible. Prefer separate small JP/EN caption lines to very small dual-language text. Do not embed external fonts, links, remote images, scripts or network resources in SVG. Keep it self-contained and local. Use explicit `viewBox`, test in JupyterLab and in PDF conversion. Recommended SVG source directory: `assets/svg/`; retain or generate PNG fallback under `assets/diagrams/` if the course's renderer needs it. Source figures should carry a clear provenance label: `schematic`, `computed synthetic`, or `saved model output`.

### V01 — Python execution state (P1; setup + Day 2)
- **Panels:** (a) code, (b) before/after variable-memory values, (c) stdout, (d) what happens on the next run.
- **Worked example:** `defect_count = 3`, then `defect_count = defect_count + 1` yields `4`; `print(defect_count)` prints 4.
- **Student prompt:** What happens if you re-run only the increment cell, and what happens after Restart Kernel + Run All?
- **Truth contract:** Document that notebook kernel state persists across cell runs and can differ from visual execution order.

### V02 — Pixel explorer and slice visual (P1; Day 1 Notebook 02)
- **Panels:** fixed 5×7 array, zero-indexed `(row, column)` axes, selected pixel `canvas[2,3]`, 3×3 slice `[1:4, 2:5]`, selected output.
- **Truth contract:** Row is y, column is x; slice end is exclusive; `shape = (height,width)`; selected values must be derived from a real NumPy array.
- **Additional optional panel:** Same RGB pixel shown as `[R,G,B]` and as weighted grayscale. Clarify false-color channel views vs numeric values.

### V03 — Four CV task outputs (P0; Day 1 Notebook 03)
- **Panels:** same actual generated sample: classification label, detection rectangle, segmentation mask, anomaly heatmap.
- **Truth contract:** Underlying source geometry identical across panels; if mask/heatmap synthetic, explicitly label as schematic and derive mask location from source defect. Invented confidences must be labelled illustrative.
- **Supplement:** a thin second row `needs image label / box label / pixel mask / normal samples` to teach training differences without oversimplifying.

### V04 — Numerical units and industrial mass (P1; Day 2 Notebook 01)
- **Panels:** length(mm), width(mm), thickness(mm) → volume(mm³) → volume(cm³) → density(g/cm³) → mass(g) → mass(kg).
- **Truth contract:** Convert mm³ to cm³ by dividing by 1,000; grams to kg by dividing by 1,000; do not confuse sheet area and sheet volume. Derive example numeric labels directly from exercise constants; test against Python.

### V05 — Tolerance and boolean path (P1; Day 2 Notebook 02)
- **Panels:** measured, nominal, signed/absolute deviation, `<= tolerance` decision, `if`/`else` path.
- **Truth contract:** `100.5` and `99.5` are on the boundary and accepted for nominal 100.0 ±0.5; `100.5001` outside unless an explicit measurement-resolution policy says otherwise.

### V06 — Threshold-to-contour pipeline (P1; Day 2 Notebook 03)
- **Panels:** source BGR → grayscale → inverse threshold → binary mask → contours → area count.
- **Truth contract:** With `cv2.THRESH_BINARY_INV`, pixels satisfying the OpenCV inverse-threshold condition are shown as foreground white; numbers come from the same actual NumPy arrays. Count contours separately from foreground pixels.
- **Graphs:** separate charts for foreground pixel count and connected-region count, both keyed to the same selected threshold.

### V07 — Calibrated measurement (P0; Day 2 Notebook 03)
- **Panels:** a reference bar and defects on the same physical plane → compute px/mm → compute mm/px → measure target → independent validation line → uncertainty.
- **Truth contract:** With 120 px = 100 mm, `px_per_mm = 1.2`, `mm_per_px = 0.833333...`; match any different actual generated calibration sample used. Never use an unrelated sample's scale without an explicit assumption.
- **Warnings:** perspective, distortion and mm/px uncertainty are not removed by a single scalar.

### V08 — Bounding-box coordinate formats (P1; Day 3 Notebook 01)
- **Panels:** one exact rectangle, corner `(x1,y1,x2,y2)`, centre `(xc,yc)`, width/height, normalized YOLO label.
- **Truth contract:** `xc=(x1+x2)/(2W)`, `yc=(y1+y2)/(2H)`, `w=(x2-x1)/W`, `h=(y2-y1)/H`, class ID is integer and is not normalized. Test all displayed values against source constants.

### V09 — Ultralytics result object (P1; Day 3 Notebook 02)
- **Panels:** input image → YOLO weights → `Results` → `boxes.cls`, `boxes.conf`, `boxes.xyxy` → annotated image and CSV table.
- **Truth contract:** The displayed field structure is tied to the tested Ultralytics version; `boxes.xyxy` is corner coordinates in original-image pixels, and confidence is not a guarantee of correctness. Use a saved example from an actual inference run where feasible.

### V10 — Epochs, batches and updates (P1; Day 4 Notebook 02)
- **Panels:** 64 sample tiles divided into 8 batches of 8 → forward/loss/backprop → accumulate gradients → optimizer step.
- **Truth contract:** Distinguish batch size, number of batches, optimizer updates and epoch. If showing nbs=64 and nominal gradient accumulation over 8 batches, label it as **this course configuration** and verify actual training settings; explain warmup and last partial batch caveats rather than claiming universal equality.

### V11 — Ground-truth/prediction matching (P1; Day 4 Notebook 03)
- **Panels:** GT boxes and predicted boxes → same-class IoU matrix → matching policy/threshold → matched TP, unmatched predictions FP, unmatched GT FN → metric formulas.
- **Truth contract:** Include confidence and matching thresholds; object-level matching is different from image-level OK/NG confusion. Check matrix and outcome against a small deterministic test case.

### V12 — PatchCore's feature flow (P1; Day 5)
- **Panels:** normal images → pretrained frozen backbone → patch embeddings → subsampled memory bank; test image → patch embedding → nearest stored feature → patch distance → anomaly map/image score → calibration.
- **Truth contract:** 2D feature scatter is a projection/schematic, not the original x/y image coordinate. Explain separately that image score and interpolated map maximum need not equal one another; postprocessed scores are 0–1 only under fitted normalization conditions.

### V13 — Calibrate/freeze/test split (P1; Day 5 Notebook 03)
- **Panels:** split by acquisition group → train / calibration / untouched test → freeze weights/preprocessing/rule/threshold → evaluate and report.
- **Truth contract:** No arrow from test data back to thresholds; every scored test record has partition provenance. Thresholds shown as `0.06`/`0.50` must be tagged as **saved reference run**, not universal defaults.

### V14 — One enlarged disagreement case (P1; Day 5 Notebook 03)
- **Panels:** original `streak_0005`; GT mask; YOLO prediction; PatchCore map; threshold comparison; image-level verdict.
- **Truth contract:** Use actual saved source/run result for any real output; only claim PatchCore false negative when reference data confirms `score 0.464 < 0.50`, YOLO NG, GT NG in that exact saved run. Add a note that results change with model and training environment.

## 4. Visual design conventions (mandatory)

1. **Traceability:** Each explanatory diagram has a declared source: example code cell, generator function, dataset image, exact constants, and provenance. The same sample should be visible before and after its transformation.
2. **Readable typography:** A student at standard Jupyter width (approximately 850–1000 px) should read the essential numbers without zoom. Avoid embedding long paragraphs in figures. Put detailed Japanese-first/English-second explanation in Markdown below.
3. **Color semantics:** Keep one consistent palette, e.g. blue=input/reference, amber=operation/uncertainty, green=correct/OK, red=error/NG, violet=model score. Also show labels/shapes so meaning does not depend on color alone.
4. **One key question per diagram:** Prediction before execution, actual code output after, explanation, then change only one parameter and repeat.
5. **Image provenance:** Caption each figure `schematic`, `computed synthetic data`, `original external reference with source/licence`, or `saved real model output`, whichever applies. Do not call a generated mask “ground truth” unless it matches the actual synthetic defect generation.
6. **JP then EN:** Natural, short Japanese first, then equivalent natural English. No `日本語:` or `English:` prefixes. Units always attached to numbers.
7. **SVG engineering:** Valid standalone XML, `viewBox`, no external dependencies, scripts, font files or remote image URLs; avoid text clipping, use native vector text where editable. If raster embedded, include local image provenance and ensure offline rendering.
8. **Preservation:** Do not replace already correct reusable figures unnecessarily. Do not re-render actual model output as an invented AI-generated picture.

## 5. Required validations and tests

### Existing checks to run after changes
Use repo-provided tools, assessing which require local data and which are lightweight. Do not claim anything that has not been executed:

```powershell
python assets\scripts\generate_training_assets.py
python assets\scripts\prepare_datasets.py
python assets\scripts\generate_teaching_diagrams.py
python assets\scripts\validate_notebooks.py
python -m pytest assets\tests -q
```

If dependencies and time permit, run the `--execute lightweight` validator, then separately the training/anomalib paths on the documented tested environment. Do not automatically run expensive 100-epoch GPU examples. Do not overwrite archived reference outputs as if they represent newly validated models. Record exact environment versions, command, execution date and outcome in the final implementation summary.

### New automated tests
- Validate all new SVGs with an XML parser; test internal references and no prohibited external resources.
- Confirm each referenced SVG/PNG exists relative to its notebook and is Git-tracked for offline students.
- Confirm no figure text extends beyond the SVG viewBox / fallback PNG frame; optionally rasterize and inspect representative files manually.
- Check spot mask/detection box geometry against `_pvc_sheet` actual generated spot.
- Verify coordinate and label math from the worked examples, including normalisation, class ID, IoU, array indexing and area/length units.
- Verify no calibration from an unrelated image is silently applied to another's contours.
- Verify 16 notebook files parse and code cells compile; preserve deliberate-error lesson metadata.
- Unit test duplicate-check language; report byte-duplicate detection only, and test near-duplicate case does not falsely assert no leakage.
- Unit test deterministic model selection when two training runs exist.
- Check no figure/result uses a held-out test partition for threshold selection.
- Check Japanese/English pairs, notebook learning objectives, output interpretation, visual questions and current code values.
- Check PDF export/import rendering of SVGs and fallback PNG assets, including Japanese fonts.

## 6. Recommended implementation sequence and completion requirements

| Phase | Target | Completion condition |
|---|---|---|
| Phase 0 | Baseline inventory | Confirm current HEAD, notebook count, diagram references, known baseline tests; create a bounded change plan |
| Phase 1 | P0 correctness fixes | TA-001 through TA-004 fixed, rerendered, tested, documented |
| Phase 2 | P1 code/documentation consistency | TA-005 through TA-011 resolved; all examples now use matching numbers and terms |
| Phase 3 | SVG assets | Implement the nonduplicative high-priority V01–V14 briefs, prioritizing Day 0–2 and exact code traces |
| Phase 4 | Bilingual and classroom review | Natural Japanese-first + English explanations, no premature concepts, visual interpretation tasks per major concept |
| Phase 5 | Validation | Structural/asset tests pass; execution checks reported honestly; clean git diff; manifest of newly created figures |

**Definition of done:**
- Student can start from `START_HERE.md` with no contradictory steps or missing prerequisite assets.
- Every edited lesson has a clear code → data → intermediate values → output → experiment connection.
- Every numerical graphic is either generated from its actual source data or explicitly called a schematic.
- All P0 technical errors are corrected; old biased results are not passed off as current.
- Visual tests, mathematical checks, bilingual quality checks, and documented execution results exist.
- Existing beginner exercises, answer-hiding conventions, instructor syllabus and submission structure remain intact.
- No push or destructive cleanup without the repo owner's approval; all work reviewable as a branch/diff.

## 7. Notes for reviewers

- **Confirmed mistakes** above are supported by source/visual inspection; **recommended graphics** are teaching improvements and must not be described as detected code failures.
- Some diagrams are **already correct**: `teach_iou_rects.png` shows 6750/(9900+12000−6750) ≈ 0.4455, `teach_array_indexing.png` demonstrates exclusive-end slicing accurately, and existing evaluation figures have useful caveats. Preserve these unless detailed tests reveal an actual issue.
- `teach_score_levels.png` explicitly warns that a PatchCore image score is not merely the maximum of the displayed map; keep this nuance.
- The reference output `ref_anomaly_panels.png` distinguishes raw patch distance maps from normalized scores; preserve this distinction when redrawing.
- Interpret `100% understanding` as a **design aspiration evaluated by teach-back exercises**, not a measurable guarantee that every student will understand without instructor help.

---

**Repository review status:** Report and implementation specification only. No modifications to the user's GitHub repository or local working copy have been made as part of producing these files.
