# 監査対応記録 / Audit remediation record

## 結論 / Summary

TA-001〜TA-011 のコード・説明・図の不一致を修正しました。16 冊に予測 → 実行 →
観察 → 説明 → 1 条件を変更する学習手順を追加し、編集可能な SVG 15 枚と PDF 用 PNG
15 枚を作成しました。演習の未完成コード、意図的なエラー、保存済みの参考出力は維持しています。
重い学習は再実行していません。全テストは **307 合格・1 不合格**で、不合格は作業前から存在する
チェックポイントとの名前衝突です。初学者による授業試行と全面的な言語校正は未完了です。

The P0/P1 source corrections are implemented; P2 classroom/readability certification remains
partial. Changes are local and uncommitted: no push, PR, merge or heavy training was performed.
This record describes this amendment, not a repetition of historical training runs.

## 基準と保全 / Baseline and preservation

- Checkout inspected: `main`, HEAD `b8c496f8c0c96ff027adb148669d3c29e56e9b03`;
  16 notebooks and 55 existing teaching PNGs.
- Initial tests: **192 passed, 8 failed, 67 skipped**. Missing generated/offline assets and
  optional PDF dependencies accounted for most failures. The checkpoint collision described below
  also existed before this work.
- The pre-existing root `.gitignore`, supplied `agent/` files, user checkpoints, training results
  and cached data were not removed or rewritten.
- The independent audit was not modified. Historical biased results remain explicitly archived,
  not erased or replaced with fabricated measurements.
- All saved reference-output PNGs remain byte-for-byte unchanged. Of the original 55 teaching
  PNGs, only the four listed below are changed; 51 otherwise-correct originals were preserved.
- New SVGs and PDF fallbacks are not ignored and are ready for review/commit. They are not
  represented as already committed. Downloaded/generated classroom data remain intentionally ignored.

## 指摘ごとの対応 / Finding register

`FIXED` means the identified source defect is corrected and covered by the checks below.
It does not certify a clean installation on every classroom PC or a new model-training run.

| Finding | Status | Change and evidence | Remaining limits |
|---|---|---|---|
| TA-001: conflicting setup/preflight | **FIXED** | [START_HERE](../../START_HERE.md) is the authoritative numbered PowerShell sequence: both environments/kernels, local assets and downloads, verification, then lessons. Setup and syllabus agree on pre-course preparation. Restricted activation alternatives avoid machine-wide policy changes. | This host was not rebuilt from scratch. The complete pinned course Anomalib environment was not installed and exercised. |
| TA-002: same-defect geometry | **FIXED** | [Shared geometry](../../assets/scripts/teaching_data.py) drives the source image, strict radius-9 mask, exclusive-edge box and schematic heatmap centre. Mask = 249 pixels; box = `(76,102,93,119)`. Both [PNG generator](../../assets/scripts/generate_teaching_diagrams.py) and [SVG generator](../../assets/scripts/generate_svg_figures.py) use it. Labels distinguish ground truth and schematic output; invented confidence values were removed. | No model prediction is claimed by this teaching example. |
| TA-003: cross-image physical scale | **FIXED** | [Asset generator](../../assets/scripts/generate_training_assets.py) supplies an ideal same-plane calibrated defect image. Day02_03 introduces it separately, leaving earlier processing exercises intact. A 120 px/100 mm reference gives 1.2 px/mm; independent 60 px/50 mm check passes. Exercise code uses its own contours and remains unsolved. | Ideal synthetic geometry does not establish real metrology accuracy. Assumptions and reference uncertainty are stated. |
| TA-004: biased historical comparison | **FIXED** | [Test report](../test_report.md), [implementation report](../implementation_report.md), reference README and Day05_03 separate the main calibration → freeze → untouched-test method from the dated **SUPERSEDED / biased** 17/26 versus 26/26 archive. Regression checks cover calibration-only selection and frozen model/preprocessing/threshold semantics. | No corrected live comparison was rerun. Historical/reference numbers are not new test results or factory performance estimates. |
| TA-005: exact-hash leakage claim | **FIXED** | Day04_01 now says no **byte-identical** duplicate files were found, not that leakage is excluded. Near-duplicates, re-encoding and session/lot leakage are explicit limits. The group/frame SVG contrasts split units. Legacy diagram wording uses intensity-level noise, not sub-pixel motion. | Hash equality alone is not a perceptual or acquisition-group audit. |
| TA-006: model chosen by lexical pathname | **FIXED** | Day04_02 saves an explicit run manifest through [training_run](../../assets/helpers/training_run.py). Day04_03 uses it first; missing recorded weights fail explicitly. Legacy fallback sorts by modification time with a deterministic path tie-break and prints candidates, selected path and available settings. Tests reverse lexical and timestamp order. | Helper and notebook wiring were tested; a new YOLO fit was not run. |
| TA-007: mismatched box example | **FIXED** | Diagram, formulas and Day03_01 use a 240×240 image and `(96,72,168,132)`: centre `(132,102)`, size `(72,60)`, YOLO row `0 0.550000 0.425000 0.300000 0.250000`. Class ID stays integer. Numerical tests verify all conversions. | Other explicitly separate examples retain their own values. |
| TA-008: rounding changes tolerance acceptance | **FIXED** | Base `judge()` and dependent `judge_width()` compare the unrounded difference inclusively. Boundary 99.5/100.5 passes; 100.5001 and 100.5000001 fail. Formatting and binary-float caveats are separate. | The later thickness exercise's separately documented rounding policy was intentionally preserved. |
| TA-009: conversion layout/uncertainty | **FIXED** | The corrected legacy PNG separates reference, conversion, measurement and uncertainty panels. Day02_03 describes **assumed edge-location uncertainty ±0.5 px → ±0.25 mm at 2 px/mm**, not unrestricted one-pixel error or guaranteed accuracy. Caption wording is tested. | This is a single assumed edge-location uncertainty, not a complete instrument uncertainty budget. |
| TA-010: minimum pixel described as visible defect | **FIXED** | Day01_02 labels the numeric result “min pixel below threshold” and explicitly separates it from visual/model detection. Existing same-image before/after views, shared scale and zoom are retained. The notebook executed successfully. | The heuristic does not prove defect location, resolution or detectability. |
| TA-011: readiness/reference paths | **FIXED** | Setup, README, syllabus, troubleshooting and affected instructor guides use actual [supplied references](../../assets/reference_outputs/README.md), distinct from generated student submissions. Asset generation/download precedes readiness checks. YOLO and ResNet18 have explicit preflight/offline checks. | Cache checks used the installed environments described below; classroom machines still need their own preflight. |
| TA-012: dense figures | **PARTIAL** | Fifteen simpler editable figures provide lifecycle, units, batch/epoch/step, matching and frozen-pipeline scaffolds. All 15 passed browser text-bound checks; a real calibration figure was inspected in the PDF. Accurate legacy figures and empirical maps were preserved. | Not every legacy dense figure was redesigned. The five-column reference panel was not altered. Full beginner readability testing remains pending. |
| TA-013: reference provenance/variability | **PARTIAL** | Reference images and notebook notes distinguish saved teaching references, computed synthetic/schematic examples and student live runs. Model score is not truth probability; displayed confidence/threshold values are not promised rerun outcomes. | Original raw run files sufficient to verify `streak_0005` were unavailable. The optional numeric false-negative SVG was deliberately omitted. No new training/provenance certification is claimed. |
| TA-014: language/execution-state consistency | **PARTIAL** | All 16 notebooks received Japanese-first learning-loop prompts and structural/bilingual checks. New figures have paired captions, notice prompts and prediction questions. Exercises, optional/required status and deliberate error cells were preserved. Ten lightweight notebooks executed successfully. | A human Japanese/English editorial review and two-beginner classroom pilot are still needed. Six download/training/Anomalib categories were not executed. No guarantee of individual comprehension is made. |

## 数値の根拠 / Computed checks

The [regression tests](../../assets/tests/test_audit_remediation.py) check numerical behavior,
not merely whether labels exist.

- Calibrated geometric contour areas: **475 and 925 px²**, giving
  **329.861111 and 642.361111 mm²** at 1.2 px/mm.
  Total foreground count is **1508 pixels**, not the sum of geometric contour areas.
  Reference/check bars are excluded by the threshold.
- Mass-chain exercise constants remain 1300×2500×0.35 mm and 1.4 g/cm³:
  the computed value is **1.5925 kg**. The exercise code is not filled in.
- Retained IoU example: `6750 / 15150 ≈ 0.4455`.
- The matching SVG's two-GT/two-prediction matrix is
  `[[1, 3480/3720], [0, 0]]`; one-to-one matching gives **TP=1, FP=1, FN=1**.
  Image-level decision gives **TP=1**, a different counting unit.
- The 64-image/batch-8 example gives eight batches, not necessarily eight optimizer updates;
  accumulation and warmup are explicitly separated.

## 実行した検証 / Executed validation

Environment: Windows host (the platform API reported Windows 10), CPython **3.11.4**, CPU.
Base runtime included Torch **2.15.0+cpu**, torchvision **0.29.2+cpu**, OpenCV **4.12.0**
and Ultralytics **8.4.211**. This is not a freshly certified Windows 11 installation.
Separate existing Anomalib-environment cache checks used timm **1.0.21** and
Torch **2.9.0+cu126**; no PatchCore fit was performed.

Commands below are relative to the course root, using the repository base environment.

| Executed check | Result |
|---|---|
| `python assets\scripts\generate_training_assets.py` and `python assets\scripts\prepare_datasets.py` | Synthetic assets/datasets generated. |
| Existing reference-image downloader and offline verification | Four licensed originals present; credits/manifest retained. |
| `python assets\scripts\generate_teaching_diagrams.py` | Four corrected outputs retained; otherwise-correct tracked PNGs restored to original bytes after renderer-only changes. Final four-task output regenerated separately after coordinate-boundary alignment. |
| `python assets\scripts\generate_svg_figures.py` | **15 SVGs + 15 PNG fallbacks + figure manifest** generated successfully. |
| `python assets\scripts\validate_notebooks.py` | **194 passed, 0 failed**. |
| `python -m pytest assets\tests -q` | **307 passed, 1 failed**, 178.83 seconds. The only failure is the pre-existing checkpoint collision below. |
| Final focused tests: audit remediation, evaluation provenance, notebook structure, visual assets | **133 passed**, after final caption and pixel-boundary corrections. |
| Validator `--execute lightweight` in an isolated course copy with private kernelspecs | **10/10 executed successfully**, no unexpected errors; six other categories skipped. Private aliases did not replace user kernels. |
| YOLO preflight/offline check | Local YOLO weights and bus sample usable without download. |
| ResNet18 preflight/offline cache check | URL cache verified with timm; Day05_02 selects old-cache policy before imports and fails explicitly if cache is missing. |
| Pylance Python syntax checks | No syntax errors in changed/new Python code checked, including final run-manifest and model-preload helpers. |
| Chromium SVG DOM/text-bound inspection | All **15** standalone SVGs: no clipped/overlapping text at notebook-scale viewBox; screenshot inspected at 900 px. |
| `python assets\scripts\export_explanations_pdf.py --only Day02 --out <sample-folder>` | **82 pages**, **21,790 Japanese characters**, no blank pages. Page **77**, containing the actual same-plane calibration figure, rendered and inspected. |
| `git diff --check` | Passed. |

### 既知の不合格 / Known pre-existing failure

`test_schedule.py::test_referenced_notebooks_and_parts_exist[day1]` finds both the real
Day01_01 notebook and the user's existing `.ipynb_checkpoints/...-checkpoint.ipynb`.
The helper recursively matches both filenames. The checkpoint was already present at baseline.
It was neither deleted nor hidden by weakening the test. Thus the complete local suite is
**not reported as fully passing**.

### 軽量実行の範囲 / Lightweight execution scope

Executed: Setup; all three Day 1 notebooks; all three Day 2 notebooks; Day03_01;
Day04_01; Day05_01. The repository validator governs intentional errors/exercises.
The private Day05_01 “anomalib” alias used base Python because that concepts notebook is NumPy-only;
this does not validate the full Anomalib kernel.

Skipped: Day03_02/03 model inference/experiments; Day04_02/03 live training/evaluation;
Day05_02 PatchCore training; Day05_03 live comparison. Offline cache checks are separate evidence,
not substitutes for these executions.

## 変更ファイル / Changed files

All links below are relative to this report. Generated student submissions and downloaded caches
are not course-source changes.

### ノートブック / Notebooks: 16

- [Setup](../../notebooks/00_Setup/00_Environment_Setup.ipynb)
- [Day01_01](../../notebooks/Day01_AI_Fundamentals/Day01_01_Introduction_to_AI.ipynb)
- [Day01_02](../../notebooks/Day01_AI_Fundamentals/Day01_02_Pixels_and_Images.ipynb)
- [Day01_03](../../notebooks/Day01_AI_Fundamentals/Day01_03_Computer_Vision_Tasks.ipynb)
- [Day02_01](../../notebooks/Day02_Python_OpenCV/Day02_01_Python_Basics.ipynb)
- [Day02_02](../../notebooks/Day02_Python_OpenCV/Day02_02_Conditions_Loops_Functions.ipynb)
- [Day02_03](../../notebooks/Day02_Python_OpenCV/Day02_03_OpenCV_Image_Processing.ipynb)
- [Day03_01](../../notebooks/Day03_YOLO_Basics/Day03_01_YOLO_Concepts.ipynb)
- [Day03_02](../../notebooks/Day03_YOLO_Basics/Day03_02_YOLO_Inference.ipynb)
- [Day03_03](../../notebooks/Day03_YOLO_Basics/Day03_03_YOLO_Experiments.ipynb)
- [Day04_01](../../notebooks/Day04_YOLO_Training/Day04_01_YOLO_Dataset_Annotation.ipynb)
- [Day04_02](../../notebooks/Day04_YOLO_Training/Day04_02_YOLO_Training.ipynb)
- [Day04_03](../../notebooks/Day04_YOLO_Training/Day04_03_YOLO_Evaluation.ipynb)
- [Day05_01](../../notebooks/Day05_PatchCore/Day05_01_Anomaly_Detection_Concepts.ipynb)
- [Day05_02](../../notebooks/Day05_PatchCore/Day05_02_PatchCore_Training.ipynb)
- [Day05_03](../../notebooks/Day05_PatchCore/Day05_03_YOLO_vs_PatchCore.ipynb)

### ソース・テスト / Source and tests

- New: [teaching_data](../../assets/scripts/teaching_data.py),
  [training_run](../../assets/helpers/training_run.py),
  [preload_models](../../assets/scripts/preload_models.py),
  [SVG generator](../../assets/scripts/generate_svg_figures.py),
  [bounded notebook updater](../../assets/scripts/remediate_notebooks.py),
  [audit regression tests](../../assets/tests/test_audit_remediation.py).
- Updated: [training asset generator](../../assets/scripts/generate_training_assets.py),
  [legacy diagram generator](../../assets/scripts/generate_teaching_diagrams.py),
  [PDF exporter](../../assets/scripts/export_explanations_pdf.py),
  [visual-asset tests](../../assets/tests/test_visual_assets.py).

### 図 / Figures

- New: **15 editable SVGs** in [assets/svg](../../assets/svg/) and **15 `_svg.png`
  fallbacks** in [assets/diagrams](../../assets/diagrams/).
  [Figure manifest](../visual_figure_manifest.md) lists every figure, target notebook section,
  source/provenance, computed values, learning question and preview path.
- Corrected existing PNGs: [four-task geometry](../../assets/diagrams/teach_cv_tasks_outputs.png),
  [box coordinates](../../assets/diagrams/teach_bbox_coords.png),
  [pixel/mm layout](../../assets/diagrams/teach_pixel_to_mm.png),
  [leakage wording](../../assets/diagrams/teach_leakage_split.png).
- SVGs contain native editable text/shapes, a 900×590 viewBox and no external scripts/images/fonts.
  PNG fallback generation uses installed Japanese fonts; no font binaries are distributed.
  PDF export explicitly resolves the fallback and errors if it is missing.

### 文書 / Documentation

- [START_HERE](../../START_HERE.md), [README](../../README.md),
  [syllabus](../../COURSE_SYLLABUS.md), [course .gitignore](../../.gitignore).
- [Installation troubleshooting](../troubleshooting/installation.md);
  instructor guides for [Day 1](../instructor/day01_instructor_guide.md),
  [Day 2](../instructor/day02_instructor_guide.md),
  [Day 4](../instructor/day04_instructor_guide.md),
  [Day 5](../instructor/day05_instructor_guide.md).
- [Reference-output README](../../assets/reference_outputs/README.md),
  [test report](../test_report.md), [implementation report](../implementation_report.md),
  [figure manifest](../visual_figure_manifest.md), and this remediation record.

## 開き方と未検証項目 / Opening materials and remaining work

Students should start with [START_HERE](../../START_HERE.md), complete the preflight outside
mandatory lesson hours, launch JupyterLab from the course root, and open the notebooks in syllabus
order. Use `aivision` for the base course and the documented `anomalib` kernel for Day 5.
Do not infer readiness from this machine's private validation aliases.

Before classroom delivery: run preflight on each Windows 11 PC, validate the actual pinned Anomalib
environment, execute the deliberately skipped live-model notebooks when resources permit, and
perform a human bilingual/beginner pilot. No new YOLO/PatchCore accuracy claims are warranted yet.
Only the Day 2 PDF sample was rebuilt in this amendment; any previously distributed booklets should
be regenerated from the updated notebook sources before use.
