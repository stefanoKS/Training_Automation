# Training_Automation — Days 1–5 beginner-learning and visual clarity review

**Review date:** 2026-11-16 (JST)  
**Repository:** https://github.com/stefanoKS/Training_Automation  
**Reviewed baseline:** `main` at `beda393c7fc5d0873a8f4697c46ae114c3626395` (commit dated 2026-11-15 UTC)  
**Course directory:** `AI_Vision_Training/`  
**Scope:** the 15 Day 1–5 teaching notebooks (3 notebooks per day), teaching narrative and bilingual presentation, code/figure correspondence, existing SVG text, related documentation. Environment setup is considered only where it impacts the lesson. **Review only; no repository files were modified.**

## 1. Executive assessment

The current course is considerably more sophisticated than a typical introductory notebook series. It already includes a good collection of calculated illustrations, real reference-output figures clearly identified as such, interactive demonstrations, bilingual Markdown, and safety caveats about synthetic data and unreliable model confidence. **The main remaining issue is cognitive sequencing, not a lack of total images.** A completely new programmer should learn *one idea, one input, one transformation, one output, one small experiment* before encountering advanced qualifications.

**Highest-value changes:** (1) make the Day 1 image coordinate/slicing demonstration a single executable walkthrough, (2) stabilize the example numbers and distinguish inspection specification from experiment settings in Day 2, (3) visually connect a YOLO box to the actual data returned by its API, (4) make image-level versus object-level evaluation unmistakable, and (5) separate PatchCore raw distances, scores, maps, calibration, and final test into a visible workflow. Make these improvements **without recreating the figures that are already correct**.

### What was and was not verified

- **Source-reviewed:** the 15 lesson notebook JSON files, including markdown/code cells; the current repository inventory; existing caption/figure paths and many figure descriptions; relevant review documents; selected SVG source content (pixel inspector, slicing walkthrough, box conversion, batch/update timeline).
- **Verified by inspection:** `teach_slice_walkthrough.svg` shows `canvas[1:4, 2:5]` selecting rows 1–3, columns 2–4 (shape 3×3); `teach_pixel_inspector.svg` distinguishes `canvas[2,3] = 100` and `canvas[3,2] = 0`; `teach_bbox_one_example.svg` is mathematically self-consistent; `teach_epoch_batch_step.svg` documents nominal gradient accumulation and warmup uncertainty. **Do not call these diagrams wrong.**
- **Not done:** full-resolution visual rendering and typography inspection of every existing PNG/SVG; live Windows/Jupyter classroom run; fresh model training, real-time model downloads, or proof that historical reference figures exactly match a new run. The previous repository audit records test outcomes, but this report makes **no claim of having rerun them**.
- **Location notation:** `cell 42` means zero-based `notebook.cells[42]`; re-identify by heading when editing because insertions change indices. Source file paths below are relative to `AI_Vision_Training/`.

### Priorities and definitions

- **P1 = significant teaching ambiguity or risk of learner misunderstanding** (fix first).
- **P2 = useful simplification/reordering or targeted visual upgrade**.
- **P3 = polish and optional challenges; avoid broad rewrites**.
- **Status “verified observation”** means text/code was inspected; **“recommendation”** is a proposed change, not a proved bug.

## 2. Findings by notebook (15 notebooks)

### Day 1 — fundamentals

#### Day01_01_Introduction_to_AI.ipynb (68 cells)
Path: `notebooks/Day01_AI_Fundamentals/Day01_01_Introduction_to_AI.ipynb`

**D1-01 | P1 | cells 28–30, headings “3 つの言葉の関係”, “学習と推論は別の作業” — clarify training/fitting.** The text says training determines *weights* and inference uses weights unchanged. It is a useful YOLO example, but Day 5's PatchCore **does not tune the frozen feature-extractor weights**; it builds a memory bank of normal features. Proposed concise beginner text: “学習・準備（fit）は、新しい画像を判定するための情報を作る段階です。YOLOでは重みを更新します。今回のPatchCoreではバックボーンを固定し、正常特徴を保存します。推論では保存した状態を使います。” / “Fitting prepares the information used on new images. YOLO updates model weights; this course’s PatchCore keeps the backbone fixed and stores normal features. Inference uses the prepared state.” Retain the existing training-versus-inference graphic, but add a two-row comparison immediately below it: `YOLO: labelled images → update weights → predict boxes`; `PatchCore: normal images → build memory bank → compare features`. Mark as simplified, not an exhaustive taxonomy.

**D1-02 | P2 | cells 28, 34, 37–38 — reduce jargon in the first exposure to ML.** AI/ML/DL, rule-based expert systems, Gaussian assumptions, standard deviation, estimated thresholds, and PatchCore memory-bank mechanics arrive before Python basics. The caveats are commendably careful but hard to process for a true beginner. Make the first explanation “fixed rule vs rule inferred from examples”, using five brightness values in a short table; move the Gaussian/±3σ explanation to a clearly labelled optional “why this simplified rule is not universal” section. Preserve the important warning that normal-only observations cannot measure missed defects. Existing assets `teach_ai_ml_dl_nested.png`, `teach_rule_vs_learned.png`, `teach_gaussian_vs_skewed.png` should be reused and repositioned rather than replaced.

**D1-03 | P2 | cells 20, 25, 33–35, 44 — show the actual manufacturing signal before introducing rules.** “Automation = repeating a fixed procedure” sounds mutually exclusive with AI automation until later text qualifies it. Illustrate a single pipeline `camera/measurement → numeric input → [fixed threshold OR learned rule] → OK/NG → log`. Pair two synthetic snapshots of the *same good sheet under different brightness* and show why a hardcoded threshold can fail. `teach_brightness_shift.png` already exists (cell 44); consider moving a thumbnail or linked version next to the first threshold discussion, not drawing a near-duplicate. Add an explicit distinction: automating a workflow versus choosing how its decision is made.

#### Day01_02_Pixels_and_Images.ipynb (82 cells)
Path: `notebooks/Day01_AI_Fundamentals/Day01_02_Pixels_and_Images.ipynb`

**D1-04 | P1 | cells 19, 22 — “resolution” ambiguously mixes total pixel count and physical sampling.** The glossary defines resolution in terms of pixel detail and ~300,000 pixels; the next manufacturing example uses `mm/px`, a different practical quantity. Retain both but name them: `image dimensions = width_px × height_px`, `total pixels = width × height`, `spatial scale at the inspected plane = mm/px`, `smallest *reliably resolved* detail depends on optics, contrast, noise, and sampling`. Work the existing sheet example: `1300 mm ÷ 1300 px = 1 mm/px`, `1300 mm ÷ 13000 px = 0.1 mm/px`. Clarify that a 0.3 mm feature spanning about 3 px is not a promise of reliable detection or measurement. Proposed visual **V01**: one 1300-mm field of view with two grid densities, an annotated 0.3-mm mark, and a physical ruler. It must keep *field of view fixed*, not compare unrelated camera crops.

**D1-05 | P1 | cells 39–45 and 52–53 — the slicing lesson has correct figures but the teaching sequence is scattered.** The SVGs `teach_pixel_inspector.svg` and `teach_slice_walkthrough.svg` are accurate. Students see indexing, an inspector, and a slice *before* executing the code that constructs the `5×7` canvas (cell 44). Reorder as (a) create and print `canvas` with indexed row/column headers; (b) predict `canvas[2,3]`; (c) run and inspect existing pixel SVG; (d) predict and print `canvas[1:4,2:5]` and `.shape`; (e) show existing slice SVG; (f) transfer to `sheet[60:66,100:106]`, 6 rows × 6 columns. Put the inclusive-start/exclusive-stop rule next to the code. **Avoid rewriting the correct SVG to represent `image[2:5,1:4]` unless code and caption are intentionally changed together.** Proposed visual **V02** is a small *interactive or code-produced highlighted grid* tied to the same `canvas` array (the existing static diagrams stay).

**D1-06 | P2 | cells 25–37 and 55–62 — keep colour and resizing experiments close to interpretation.** The notebook already has RGB swatches and a widget, a downsampling comparison, and a brightness profile. Add a “predict the exact selected pixel value/colour” micro-check alongside the existing RGB slider; use one labelled `RGB→weighted grey` calculation. For resize, explicitly distinguish shrinking a stored image from *capturing with a different optical field of view*. Avoid saying subpixel flaws always vanish: the current text correctly notes they may still change a pixel's brightness. Proposed visual **V03**: one dynamic original/resized pair with synchronized defect coordinate and a local pixel-profile line, if it can be generated deterministically without new external data.

#### Day01_03_Computer_Vision_Tasks.ipynb (57 cells)
Path: `notebooks/Day01_AI_Fundamentals/Day01_03_Computer_Vision_Tasks.ipynb`

**D1-07 | P2 | cells 13–15, 23–26, 32, 36, 42 — turn duplicate explanations into one common-input comparison.** `teach_cv_tasks_outputs.svg` (cell 13) and `teach_cv_tasks_outputs.png` (cell 14) are adjacent and cover the same concept; determine whether both add distinct instructional information. The four *task families* are classification, detection, segmentation, anomaly detection, while segmentation has semantic and instance variants: make this numbering explicit (“4 families / 5 shown outputs”). The long comparison tables in cells 32 and 36 overlap. Prefer one main **same source image → output shape → what it cannot answer** table, then a compact exercise with reasons. Correct the wording in cell 42 so semantic segmentation *produces a mask*, from which region counts/areas **may be calculated afterward**; areas in physical units still require calibration. Retain `teach_segmentation_modes.png` and the synthetic-versus-real attribution.

### Day 2 — Python and OpenCV

#### Day02_01_Python_Basics.ipynb (65 cells)
Path: `notebooks/Day02_Python_OpenCV/Day02_01_Python_Basics.ipynb`

**D2-01 | P2 | cells 16, 21–25, 33–34 — defer advanced numeric exceptions.** For the first introduction, the main path should be `name = number → print → calculate → compare → True/False`. Existing discussions of negative-number floor division, binary floating-point, and the `:=` assignment expression are technically nuanced but appear before the learner has mastered the essentials. Keep all warnings accessible in an “optional: precision and unusual operators” section. The `teach_assign_vs_compare.png` image is useful; beneath it, ask the learner to predict output of `width = 100.3` versus `width == 100.3`. Do not suggest that blindly rounding all boundary measurements is acceptable.

**D2-02 | P2 | cells 53–55 — replace abstract unit arithmetic with a dimensional chain.** The width/length/thickness/density exercise has an existing `teach_mass_units_chain.svg`. Make it the worked example immediately adjacent to the exercise: `1300 mm × 2500 mm = 3,250,000 mm² = 3.25 m²`; `×0.35 mm = 1,137,500 mm³ = 1137.5 cm³`; `×1.4 g/cm³ = 1592.5 g = 1.5925 kg`. Mark these as idealized computed answers, not measurements. Ask students to explain why area and volume have different exponents. This improves comprehension without another picture.

#### Day02_02_Conditions_Loops_Functions.ipynb (79 cells)
Path: `notebooks/Day02_Python_OpenCV/Day02_02_Conditions_Loops_Functions.ipynb`

**D2-03 | P1 | cells 12–17, 24–35, 37–42 — too many different numeric worlds.** The tolerance graphics use `12.0 ± 0.2 mm`; the first code works with `100.0 ± 0.5 mm`; the list/loop uses `100.0`; the stepper uses `12.50 ± 0.10 mm`; the function diagram uses `12.5`. These examples can all be valid, but a beginner must constantly recompute which numbers are applicable. Choose one primary dataset for `if → list → for → function`, e.g. `nominal=100.0`, `tolerance=0.5`, `measurements=[100.0,100.3,99.7,100.6,99.4]`, and keep a conspicuously labelled **independent transfer example** (12.50). If keeping existing figures unchanged, insert a labelled “Different demonstration — new specification” divider rather than editing diagrams to disagree with their calculations. Proposed **V04**: one *live trace table* with column `i / measurement / difference / within ±0.5 / OK or NG` that fills one row per loop iteration; existing `teach_loop_trace.png` can serve as baseline.

**D2-04 | P1 | cell 14 “changing specification” — classroom suggestion may normalize weakening acceptance criteria.** The text proposes passing `12.201 mm` by declaring a new upper bound `12.201 mm` and changing the midpoint. This is explicitly conditioned on declaration, but it can still read as instructions for modifying a quality limit to pass a bad part. Replace the primary instructional example with **fixed approved specification** `11.8 ≤ value ≤ 12.2`, `12.200 = OK`, `12.201 = NG`, and “do not round or alter the approved specification to pass a measurement.” Put formal spec-change control in an *optional* separate example requiring design/customer authorization and traceable revision. Retain the useful distinction between changing measured input and changing approved requirements.

**D2-05 | P1 | cell 20 `grade_width()` — “C (warning)” is outside tolerance.** With `tolerance=0.5`, `C` corresponds to `0.5 < abs(difference) ≤ 1.0`, i.e. already **outside the declared acceptance limit**. A first-time learner could infer C remains acceptable. Add independent columns: `severity category A/B/C/D` and `spec acceptance OK/NG` and say C is **NG under the current drawing specification**. Consider relabelling C as “out of spec (review)” and D as “out of spec (large deviation)”; avoid changing function public output gratuitously if other exercises/tests rely on it.

**D2-06 | P2 | cells 45–60 — distinguish required skills from later reliability skills.** A first-time Python student encounters `try/except`, checked functions, `assert`, and a program assembler in one notebook. Keep first-pass required route `if → for → def`; mark input validation and tests as a guided second pass with very short trace examples. Proposed **V05**: a two-track decision flow: `raw input → parse; on failure: reject/log; on success: apply tolerance`, perhaps a reused/expanded existing branch graphic.

#### Day02_03_OpenCV_Image_Processing.ipynb (74 cells)
Path: `notebooks/Day02_Python_OpenCV/Day02_03_OpenCV_Image_Processing.ipynb`

**D2-07 | P1 | cell 8 — BGR/RGB needs a visual counterexample.** The current prose is correct but students cannot see why channels matter. Add a tiny 2–3-colour test strip or single red rectangle and two side-by-side outputs: incorrectly displayed BGR and correctly converted RGB; show one pixel's `[B,G,R]` and `[R,G,B]` tuple. Use deterministic NumPy/OpenCV code, no external download. Proposed **V06**. Keep `cv2.imread`/`None` and `cv2.imwrite`/return-value advice.

**D2-08 | P1 | cells 18–24, 30, 33–35 — make mask → contour → area a continuous 3-stage experiment.** Figures `teach_opencv_pixel_pipeline.svg`, `teach_opencv_pipeline.png`, `teach_threshold_sweep.png`, `teach_contour_merge.png` are already present. Place one simple four-pixel threshold truth table *directly* next to the code, including the equality case (`g==T` is white for `THRESH_BINARY_INV`); the next cell shows exact mask; the next outlines white connected regions. Pair `count_nonzero(mask)` with `cv2.contourArea(contour)` on **the same test mask** and show why pixel count ≠ geometric contour area. Do not claim contour area is a count of white pixels. If demonstrating merging, start with 2→1, and introduce 1→many from noise as a *separate* effect so the existing 2→1→18 figure is not a causally misleading leap. Proposed **V07**: synced original, binary mask, contours with a small table of pixel/contour metrics; can use widget at existing cell 32.

**D2-09 | P2 | cells 48–62 — teach scale calibration as a unit equation first.** Use existing `teach_pixel_to_mm.png` and `teach_calibration_same_plane.svg`. Write the equation `px_per_mm = reference_length_px / reference_length_mm`, then `measured_mm = measured_px / px_per_mm`, and for a geometric contour `area_mm2 = area_px2 / (px_per_mm)^2` in one worked panel. The existing 475/925 px² example is computed and should remain. Distinguish same-plane geometry and lens distortion; this is a conceptual demo, **not** a measurement-accuracy certification. Prefer rearranging two visuals rather than creating a third generic camera diagram.

### Day 3 — YOLO concepts, inference, experiments

#### Day03_01_YOLO_Concepts.ipynb (52 cells)
Path: `notebooks/Day03_YOLO_Basics/Day03_01_YOLO_Concepts.ipynb`

**D3-01 | P1 | cells 13–17 and 26–34 — tie the correct box figure to a numerical conversion.** The three box forms (`xyxy`, OpenCV top-left `xywh`, YOLO normalized center `xc,yc,w,h`) are explained and `teach_bbox_one_example.svg` is mathematically correct. But the student should have a single annotated rectangle and *three synchronized representations* **plus one edited box experiment**. Reuse the existing figure immediately before the conversion code, then predict how `x2 += 24` affects width and center, and calculate the new YOLO line. No need to recreate the correct IoU image; its widget already demonstrates overlap. Proposed **V08**: optional slider to move `x2` while updating numeric forms and verifying `0 ≤ normalized ≤ 1` for in-bounds boxes.

**D3-02 | P2 | cells 10, 22, 36–37 — eliminate overly absolute claims.** “YOLO does one calculation” should be “a model forward pass with post-processing” and must not promise production speed without hardware benchmarking. A COCO-pretrained model lacks the labelled PVC defect classes; it **cannot reliably label these as intended defect types**, though it might emit an unrelated class. `pt`/`onnx` resume/export internals can be moved to optional technical notes after “what is pretrained?” Do not remove provenance/accuracy warnings.

#### Day03_02_YOLO_Inference.ipynb (56 cells)
Path: `notebooks/Day03_YOLO_Basics/Day03_02_YOLO_Inference.ipynb`

**D3-03 | P2 | cells 24–33, 38–40 — map the returned API object to rows and images.** Add a simple structured visual or aligned printed tree: `results (list) → results[0] → boxes.xyxy / boxes.cls / boxes.conf → table row → annotated image / CSV`. Use actual shapes `(N,4)`, `(N,)`, `(N,)`. The existing `ref_inference_boxes_table.png` is useful; label it **saved example of one historical inference**, not the expected count for every environment. The current caveat “zero predictions does not imply normal PVC” (cell 48) is correct and should be retained. Proposed **V09** should focus on object fields, not another generic photo.

#### Day03_03_YOLO_Experiments.ipynb (59 cells)
Path: `notebooks/Day03_YOLO_Basics/Day03_03_YOLO_Experiments.ipynb`

**D3-04 | P1 | cells 13–22 — three different experiment contexts are adjacent.** The toy four-candidate figure uses illustrative scores (3→1→1); a saved reference figure summarizes **52 images inferred at `conf=0.01`**; a real-image table uses `bus.jpg` at `imgsz=640`; the widget caches `bus.jpg` at `conf=0.05`, `imgsz=320`. All are individually described but are easily mistaken for outputs from the same run. Prefix every graphic with a small consistent provenance heading: **A: made-up toy examples; B: archived 52-image dataset result; C: the student's live bus inference**. Explain that a cache created at `.05` cannot recover proposals discarded below `.05`; comparisons only valid on identical image/model/preprocessing/candidate set. Proposed **V10**: an aligned “source / sample count / model input size / minimum confidence / what this figure proves” table next to existing figures. No need to regenerate archival charts.

**D3-05 | P2 | cells 34–37, 41–44 — avoid mixing image-level outcomes with individual object matches.** The existing text correctly distinguishes image-level TP/FP/FN/TN from box-level matching. Add a two-image example: one defective image with three actual boxes and two predicted ones: `image-level NG correct (TP image)` **but** `object-level one missed defect (FN box)`. This makes the different denominator intuitive. Link forward to Day 4 evaluation figures rather than introducing a redundant confusion matrix.

### Day 4 — YOLO annotation, training, evaluation

#### Day04_01_YOLO_Dataset_Annotation.ipynb (55 cells)
Path: `notebooks/Day04_YOLO_Training/Day04_01_YOLO_Dataset_Annotation.ipynb`

**D4-01 | P2 | cells 16–25 — add a tiny end-to-end label-file bridge.** Use one *existing* `train_0002.png` example with corresponding `.txt` line, `data.yaml` entry (`2: streak`) and overlaid box. Students should see that `class_id` is an integer and only `xc,yc,w,h` are normalized, all using the same example. Existing `teach_yolo_label_fields.png` already does much of this; annotation above/below and an executable `assert`/shape check may suffice. Do not imply an empty `.txt` proves an image truly defect-free; current caution is correct.

**D4-02 | P2 | cells 31–39 — data split is overexplained with adjacent overlapping visuals.** The existing split-role chart, contact sheet, leakage comparison PNG, and `teach_group_split_vs_frame_split.svg` are valuable but should each have a **different single question**: roles, appearances, near duplicates, grouping. Avoid two near-identical explanations back-to-back. Include simple example grouping `session A all train, session B all val, session C all test`; a pixel hash detects exact duplicates but does **not** establish independent capture groups. Keep current caution about group-level leakage.

#### Day04_02_YOLO_Training.ipynb (54 cells)
Path: `notebooks/Day04_YOLO_Training/Day04_02_YOLO_Training.ipynb`

**D4-03 | P1 | cells 12–16, 25–30 — the first training explanation starts with advanced optimizer internals.** New learners need to grasp `64 images / batch 8 = 8 batches per epoch`, followed by `15 epochs = 15 passes` before `nbs=64`, gradient accumulation, warmup and optimizer steps. The existing `teach_epoch_batch_step.svg` is carefully caveated and correct; use it as **stage 2**, not the very first definition of batch. Stage 1: simple 64-image, 8-row batch map with labels; Stage 2: why weight-update counts can differ from number of batches (nominal accumulation and warmup). Avoid equating `batch count = weight update count`. Keep the pinned-version `l1_loss` rather than inventing a `dfl_loss`. Proposed **V11** may be achieved by a simplified crop/callout of existing SVG, not a new model-output figure.

**D4-04 | P2 | cells 25–26, 33–42 — separate ‘run a job’ from ‘interpret a run’.** Before the CPU training switch, add an explicit checklist of files that the run will produce (`best.pt`, `results.csv`, `args.yaml`) and that enabling it can take variable time. The current explanation says CPU friendly, but actual runtime is machine-dependent. When comparing loss and mAP curves, distinguish a **schematic learning-shape example** from the archived saved run; preserve real-output provenance. For a second experiment, give runs different names/locations to avoid accidentally overwriting a baseline. Keep existing safe skip behavior.

#### Day04_03_YOLO_Evaluation.ipynb (57 cells)
Path: `notebooks/Day04_YOLO_Training/Day04_03_YOLO_Evaluation.ipynb`

**D4-05 | P1 | cells 14–18, 24–29 — explicitly split two evaluation units before mAP.** The notebook moves rapidly from precision/recall and mAP into an image-level 2×2 confusion matrix and the Ultralytics **object-level** matrix with reversed axes. All are explained, but the sequencing is demanding. Start with a concrete inspection image: `truth NG; one detection retained = image-level TP` and separately `two truth boxes, one matched = one object-level TP + one object-level FN`. Then show a **two-column comparison** `unit = image` versus `unit = box`, with denominator and axis orientation; only afterward introduce mAP and the Ultralytics matrix. Reuse `teach_image_level_confusion_matrix.png`, `teach_object_level_matching.png`, `teach_detection_matching.svg`; don't change the correct axis annotations. Proposed **V12** is a compact side-by-side numeric worked example, not another elaborate heatmap.

**D4-06 | P1 | cell 18 “Always split=test” — qualify the stage.** For the **final untouched evaluation**, yes, `split="test"` is correct; during development and parameter/model selection, use `val`. Rewrite: “Use validation for improvements and model/threshold selection. Once all choices are frozen, use test for final evaluation and do not tune against that result.” Do not imply every `model.val()` call should use test. At cell 34, distinguish **number of missed images** from **number of unmatched ground-truth boxes** when prompting students to inspect figure rows.

### Day 5 — PatchCore and comparison

#### Day05_01_Anomaly_Detection_Concepts.ipynb (55 cells)
Path: `notebooks/Day05_PatchCore/Day05_01_Anomaly_Detection_Concepts.ipynb`

**D5-01 | P1 | cells 21–30 — avoid teaching literal patch crops as the model's implementation.** The course carefully calls the `256×256 image → 16×16 tiles` example an analogy, then explains the real CNN feature maps with overlapping receptive fields. Some beginners will remember only the tile diagram. Place a **side-by-side** `analogy: disjoint tiles (not what PatchCore literally crops)` / `actual: overlapping receptive fields → feature-map locations → vectors`. Use or adapt existing `teach_patch_neighbour.png` and `teach_patchcore_stages.svg`. The first lesson should say “patch descriptor = CNN feature at a location summarizing an overlapping image region.” Proposed **V13** should visually connect overlapping image regions to the feature grid.

**D5-02 | P1 | cells 24, 36–39 — “2 outputs” heading while three distinct rows appear.** The heading says “PatchCore returns 2 outputs”, yet the table lists raw distance, postprocessed image score, and heatmap, and the following figure calls patch/image/map “three outputs”. Rephrase into a consistent **three-stage representation**: (a) `raw image score / raw anomaly map` from features (unbounded values); (b) `postprocessed image score / postprocessed anomaly map` on a calibrated scale when available; (c) `decision = image score ≥ image threshold`. Distinguish **two output kinds** (an image-level scalar and spatial map) from **raw versus postprocessed representations**; patch distances are intermediate, not a third independent API output. Give one consistent 3-row numeric example and clearly state numbers like 21.439 / 21.762 / 1.000 are **previous archived values**, not universal expectations. Preserve the technical caveat that max map value can differ from image score.

**D5-03 | P2 | cells 17–18 and 30–33 — reduce terminology before nearest neighbors.** Class labels “unsupervised”, “one-class”, and “semi-supervised” have different uses in research and will confuse zero-experience students. Keep the precise explanation but lead with a four-column picture `fit: normal images only | calibrate: labelled normal+abnormal | test: independent labelled set | infer: new image`. Mark literature terms as optional. The memory bank image `teach_memory_bank.png` already explains neighborhood; add a tiny two-vector distance example only if a student can compute it without linear algebra; avoid implying features are just physically cropped RGB squares.

#### Day05_02_PatchCore_Training.ipynb (67 cells)
Path: `notebooks/Day05_PatchCore/Day05_02_PatchCore_Training.ipynb`

**D5-04 | P2 | cells 21–31 — connect fitting to stored state.** The existing frozen-backbone/memory-bank picture and PatchCore pipeline SVG are sufficient. Instead of another diagram, add a “what happens to which object?” row after each stage: `backbone weights: unchanged`, `memory bank: created`, `threshold: chosen during calibration`, `incoming image: never used for fit`. Clarify that `fit` here is *not* 15 epochs of weight optimization as in Day 4. Keep the API pinned to the stated anomalib version and do not make unverified training claims.

**D5-05 | P1 | cells 35, 41–46, 49–51 — give the numeric reading order before the advanced formula.** The lesson correctly distinguishes `raw image score ~21.439`, `max of rendered numeric map ~21.762`, and `calibrated saved image score 1.000`; but the neighboring prose also introduces AUROC/F1, Gaussian smoothing, nine neighbors, and `post_processor`. Present the **three values as an annotated card** with arrows `original → feature scores → spatial map` and `raw image scalar → normalization → calibrated scalar → compare threshold`, then make `num_neighbors=9` and formula an optional accurate technical note (already optional in cell 46). Use the existing `ref_anomaly_panels.png`, label it a saved computation, and retain the caution that heatmap colours depend on range and that scores must not be treated as confidence probabilities. **V14** is an annotated numeric-overlay panel using an existing saved image, not a regenerated inference result.

#### Day05_03_YOLO_vs_PatchCore.ipynb (57 cells)
Path: `notebooks/Day05_PatchCore/Day05_03_YOLO_vs_PatchCore.ipynb`

**D5-06 | P1 | cells 15–16, 23–35 — draw the actual comparison protocol.** The course already has `teach_evaluation_sequence.png`, `teach_frozen_threshold_pipeline.svg`, and `teach_threshold_freeze.png`, which partially overlap. Use one as the primary 6-step teaching graphic: `manifest + same image IDs → paired predictions → calibration only: choose YOLO C and PatchCore T → freeze models/preprocessing/thresholds → test once → compare image-level TP/FP/FN/TN`. Label normal calibration count `n=6` and anomaly count `n=20`; with a 10% false-reject cap, this means **0 false rejects in the six sampled normals**, not a credible guarantee of ≤10% in production. Make that calculation a one-line learner exercise. Keep the code's actual thresholds as computed by live calibration and describe saved `0.06/0.50` as example archive settings, not universal constants. Reuse current charts rather than creating a fourth pipeline picture. Proposed **V15**: one annotated run-flow and small “data split / allowed action” color-agnostic table.

**D5-07 | P1 | cells 38–40 — misleading transition from 3 panels to 5 panels and from test to calibration.** The title at cell 38 says “five aligned columns” while the immediately displayed illustration contains **three** panels (original, map, overlay); the prose does confess it is not the five-column figure but the mismatch still disrupts learners. Retitle the first illustration to “Before comparing: how to read a three-panel heatmap” and only use “five columns” with the actual `ref_comparison_5col.png` at cell 39. After a TEST set five-column figure, cell 40 displays saved **CALIBRATION** heatmaps. Add a conspicuous bilingual boundary marker above that code: “The next gallery uses calibration images, not the three test images above”; print split role in the output. Avoid accidentally implying all displayed images came from the test set.

**D5-08 | P1 | cells 23, 26, 32, 39–42 — protect the holdout lesson.** The lesson correctly warns that seeing a saved test reference before tuning can influence later choices. Make this visible in the student workflow: either move archived 5-column test screenshots into an instructor/after-freeze appendix, or place them **after** students have recorded their frozen settings; add a required written “I did not tune after seeing test” check. If test images or predictions are already exposed during the lesson, label any later score as *illustrative/reused data*, not a fresh untouched-test estimate. Do not delete or falsify historical result images.

## 3. Visual implementation backlog (do not just add pictures)

Each request must be evaluated against the current assets first. Recommended order and visual design:

| ID | Priority | Insert near | Reuse or build | Must illustrate | Acceptance question |
|---|---|---|---|---|---|
| V01 | P1 | Day01_02 cell 19/22 | New deterministic SVG + PNG if not already represented | Same 1300-mm FoV; 1300px vs 13000px; 1 vs 0.1 mm/px, 0.3-mm mark | Does halving the FoV differ from simply scaling a saved JPEG? |
| V02 | P1 | Day01_02 cells 39–45 | Reuse 2 *correct* SVGs, add live highlighted 5×7 array code | `canvas[2,3]`; slice `[1:4,2:5]`; stop-exclusion; shape (3,3) | Which rows/cols are extracted, and why? |
| V03 | P2 | Day01_02 cell 56 | Reuse current downsample images, optional code plot | Same defect sampled at several sizes, *local* contrast and correct axis labels | Can a subpixel feature affect a pixel? |
| V04 | P1 | Day02_02 cells 24–35 | Reuse loop trace, add dynamically printed trace | Same input list/spec in if, loop, function | Which exact list entries fail and why? |
| V05 | P2 | Day02_02 cell 45 | Adapt existing branch diagram | Failed float conversion vs valid tolerance branch | What gets logged when input is invalid? |
| V06 | P1 | Day02_03 cell 8 | New tiny deterministic OpenCV demonstration | Red/blue BGR-vs-RGB swapped vs corrected | What happens if BGR is shown as RGB? |
| V07 | P1 | Day02_03 cells 19–35 | Reuse pipeline, add 3-panel code output | Same source image → INV mask → contour; count_nonzero vs contourArea | Why isn't white-pixel count equal to contour area? |
| V08 | P1 | Day03_01 cells 13–17 | Reuse correct bbox SVG + small widget or tabulation | Same rectangle as xyxy/OpenCV xywh/YOLO normalized | Which YOLO numbers change when x2 changes? |
| V09 | P2 | Day03_02 cells 24–33 | New small textual schema / diagram | result[0] fields → a row → annotations, CSV | How do you get one box's class and score? |
| V10 | P1 | Day03_03 cells 13–22 | **Table only**, no new image | A toy example vs 52 archived vs bus.jpg local experiments | Are these thresholds applied to the same candidate pool? |
| V11 | P2 | Day04_02 cells 12–15 | Reuse epoch/batch SVG (simplify first panel) | 64 images → eight batches; weight updates not same count | How many batches per epoch, not updates? |
| V12 | P1 | Day04_03 cells 24–29 | Reuse three current evaluation figures | One image-level TP with a box-level FN | Can an image be correctly NG while a box is missed? |
| V13 | P1 | Day05_01 cells 21–30 | New/modified explanatory SVG and raster fallback | Not-literal tiles vs overlapping feature receptive fields | Is a PatchCore patch a 16×16 RGB crop? |
| V14 | P1 | Day05_02 cells 41–46 | Annotate existing reference panel; do not recompute history | Raw score vs map max vs normalized score; what is thresholded | Which number gives the image-level NG decision? |
| V15 | P1 | Day05_03 cells 15–39 | Consolidate 3 existing flow images | calibrate → freeze → untouched test, with provenance | Which images may be used to tune thresholds? |

**Visual quality rules:** Actual learning question before figure; exact matching code/data immediately after; axes with units and explicit x/y, row/column and pixel origin; legible text at notebook width; not only colour-coded distinctions; JP first then EN; no screenshot of unexecuted code represented as measured output; label `[schematic / calculated synthetic / historical saved output / live execution]`; SVG source when editable, PNG fallback for PDFs and environments that cannot show SVG; calculate numeric labels from one shared source of truth; keep assets local. Use public/open photos **only** if they add a concept not already illustrated and record exact provenance/license and local offline availability; don't introduce external fetch dependencies gratuitously.

## 4. Example before/after rewrites (ready to adapt, not mandates)

### R01: slicing explanation (Day01_02)
**Replace unpaired prose with immediately runnable and inspectable values.**

**JP:** “画像は `image[y, x]` の順で取り出します。`y` は上から数える行番号、`x` は左から数える列番号です。`canvas[1:4, 2:5]` は行 1・2・3、列 2・3・4 を選びます。`4` と `5` は終点なので含みません。結果は **3 行 × 3 列** です。実行する前に `shape` を予想してください。”

**EN:** “Image arrays use `image[y, x]`: `y` is the row counted from the top and `x` the column counted from the left. `canvas[1:4, 2:5]` takes rows 1, 2, 3 and columns 2, 3, 4; the stop values 4 and 5 are excluded. The result has **3 rows and 3 columns**. Predict its `shape` before running the cell.”

### R02: production tolerance (Day02_02)
**JP:** “規格は承認済みの `11.8 mm 以上、12.2 mm 以下` に固定します。`12.200 mm` は境界を含むため OK、`12.201 mm` は NG です。コードを変えて不適合品を通してはいけません。規格変更は別の承認・改訂手続きです。”

**EN:** “Keep the approved specification fixed at **11.8–12.2 mm inclusive**. A reading of 12.200 mm is OK; 12.201 mm is NG. Do not change the code to pass an out-of-spec part. Changing the official specification requires a separate approved revision.”

### R03: Day 3 model-confidence context
**JP:** “confidence はモデルが付けたスコアです。**正しい確率そのものではありません。** しきい値を上げると、この同じ候補集合から残る検出数は増えません。別の画像や `imgsz` で再推論した結果と直接比較しないでください。”

**EN:** “Confidence is a model score, **not an automatically calibrated probability of correctness**. Increasing the threshold cannot increase the retained count **within the same cached candidate set**. Do not directly compare with a new inference on different images or `imgsz`.”

### R04: PatchCore scores (Day05_01 / Day05_02)
**JP:** “結果は **画像全体のスコア 1 つ** と **位置を示す数値マップ 1 枚** に分けて読みます。元の距離・補正後の画像スコア・マップの最大値は、同じ数値になるとは限りません。画像を OK/NG にする際は、宣言した**画像スコア**と**画像用しきい値**を比較します。ヒートマップの色は場所の手がかりであり、直接の合否判定ではありません。”

**EN:** “Read **one image-level score** and **one spatial anomaly map** separately. A raw feature distance, postprocessed image score and maximum map value need not match. For image OK/NG, compare the declared **image score** with the **image-level threshold**. Heatmap colours help localize suspicion; they are not by themselves the acceptance decision.”

### R05: final evaluation (Day04_03 / Day05_03)
**JP:** “学習用でモデルを作り、検証・較正用で設定としきい値を決めます。モデル・前処理・しきい値を固定した後に、未使用の試験用データで最終評価します。試験結果を見て設定を変更した場合、そのデータは新しい最終評価には使えません。”

**EN:** “Fit on training data. Select parameters and thresholds using validation/calibration data. After freezing the model, preprocessing and thresholds, evaluate once on untouched test data. If test feedback influences a setting change, that data can no longer justify a new untouched-test result.”

## 5. Cross-cutting editorial instructions

1. **Local bilingual layout:** for each concept use a small Japanese explanation immediately followed by semantically equivalent English, instead of a very long Japanese chapter followed by a long English duplicate. Keep both languages complete and correct. No `日本語:` / `English:` boilerplate prefixes. Keep technical identifiers and units identical in both.
2. **One numerical story per stage:** use the same sample/units through introduction, code, diagram and expected output. Any deliberate switch must start with a prominent `New independent example / 別の例` line. Never silently reuse names with different specifications and expected counts.
3. **Say exactly what a visual proves:** replace repeated generic “follow the transformed value” figure captions with a specific statement, e.g. “`canvas[2,3]=100`, but `canvas[3,2]=0`; therefore the order is row, column.”
4. **Use a short learning rhythm:** *predict one thing → run one cell → compare actual result → change one value → explain why*. Answers should be available to the instructor, not all revealed before learners attempt the task.
5. **Distinguish conceptual vs empirical:** synthetic demonstration, archived fixed reference, and live executable output cannot be casually interchanged. Calibration and test data roles must be visible in charts and tables.
6. **Do not overcorrect:** preserve accurate explanations and tested numeric examples; make the minimal reliable change. Existing figures already illustrate many topics. Preserve filenames, paths, saved historical outputs and their provenance unless a specific finding identifies a real defect.
7. **Text and grammar:** remove unnatural hybrid headings or translated metaphors (“same as three tables” without saying RGB-specific; `決める` vs `学習する` without a boundary). Prefer short declarative industrial Japanese (丁寧体/常体 used consistently within a section) and idiomatic plain English. Keep English concise, not literal Japanese sentence structure.
8. **Accessibility:** every figure gets useful alt text where supported; labels not colour-only; colour bars for heatmaps; arrows should never reverse image coordinates or switch row vs column; legibility in Jupyter and exported PDF.

## 6. Implementation plan for Codex

**Phase A — source of truth:** work from the current HEAD, map the findings to fresh headings/cells, check existing tests and scripts (`assets/scripts/generate_svg_figures.py` if present, figure-generator files, `docs/visual_figure_manifest.md`, `assets/scripts/validate_notebooks.py`, `assets/tests/`). Build a findings-to-files checklist with baseline SHA. Check every numerical worked example against live Python expressions before changing it.

**Phase B — P1 pedagogy and correctness:** implement D1-01, D1-04, D1-05, D2-03, D2-04, D2-05, D2-07, D2-08, D3-01, D3-04, D4-03, D4-05, D4-06, D5-01, D5-02, D5-05, D5-06, D5-07, D5-08. Keep changes targeted. Work per day or per notebook with small readable diffs.

**Phase C — visuals:** review V01–V15 against current assets. Reuse/relocate before generating. Build only high-value missing artifacts; diagrams derived from code use deterministic scripts; build editable SVG and local PNG PDF fallback when needed. If a visual has insufficient supporting data, omit it with reason rather than inventing results. Update figure manifest and citations.

**Phase D — P2 readability:** simplify the remaining P2 findings while leaving advanced explanations in optional sections. Do not move essential correctness warnings outside the main route.

**Phase E — verification and classroom check:** structural JSON parse of all 16 notebooks; check markdown image links, Markdown tables, diagram labels, JP/EN semantic equivalence and grammar; run locally applicable unit tests and notebook validator (respect deliberate-error cells and optional heavy model runs); compare expected-output text with actual lightweight code results; confirm deterministic visual generation; render SVG/PNG/PDF where tooling permits; visually examine critical diagrams at 100% and 50% scale; report skipped heavy work honestly. Do not download large weights, rerun expensive training, rewrite archived reference outputs, or push/commit unless explicitly instructed.

## 7. Acceptance criteria and deliverables

- All 15 day notebooks remain present, JSON-valid and runnable in their designed order; the setup notebook remains intact.
- Each P1 finding is either corrected, or accompanied by a specific documented reason it does not apply to the current HEAD; no blanket “done” without evidence.
- Student can answer from adjacent code+visual: `image[y,x]` and exclusive slice stop; accepted vs rejected tolerance; BGR vs RGB; mask vs contour area; YOLO three box formats; image vs object TP/FP/FN; 64 images/8 batch vs optimizer updates; PatchCore raw/map/postprocessed score; freeze-before-test.
- Each new figure has correct coordinates/units/provenance and JP/EN explanation; the source and exported PNG are checked together. Existing correct SVGs remain numerically correct.
- A concise modification log with findings IDs, changed paths, tests executed, failures/skips, and unfinished items. No false assurance about real-world PVC defect accuracy.

## 8. Repo references

- `AI_Vision_Training/agent/Training_Automation_Second_Pass_Audit_2026-11-15.md` — earlier second-pass review; **do not treat old findings as still broken without checking current files**.
- `AI_Vision_Training/docs/reviews/2026-11-15_audit_remediation.md` — previous fix register and test notes; historical test runs are not this review’s results.
- `AI_Vision_Training/docs/visual_figure_manifest.md` — SVG↔PNG provenance and learning questions.
- `AI_Vision_Training/docs/reference_materials.md`, `assets/external_samples/PROVENANCE.md` — external image sourcing and rights.
- `AI_Vision_Training/START_HERE.md`, `AI_Vision_Training/start_training.cmd` — current CMD-oriented user startup. This audit does **not** request another PowerShell migration.

**Decision:** prioritize *better orchestration of existing visuals* before making more. The current materials appear technically careful; the listed revisions aim to make them understandable without an instructor explaining what each figure means.
