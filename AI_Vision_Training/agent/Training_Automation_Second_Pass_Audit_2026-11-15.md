# Training_Automation — Second-pass technical/visual audit and CMD migration

**Review date:** 2026-11-15 (JST; repository commit 2026-11-15 12:05:46 UTC)  
**Repository:** https://github.com/stefanoKS/Training_Automation  
**Branch/HEAD examined:** `main` / `47a9626bb3d87af4a883ea0bb4c4aae4d13de632`  
**Course root:** `AI_Vision_Training/`  
**Deliverable:** audit only. This report does **not** modify the repository or claim new execution results.

## 1. Executive decision

The first audit's technical defects have **largely been addressed**. The revised repository has 16 notebooks, 15 editable SVG figures with 15 raster fallbacks, corrected physical-scale and bounding-box examples, consistent synthetic geometry, and an improved calibration → freeze → test evaluation narrative. The course's own `docs/reviews/2026-11-15_audit_remediation.md` records **307 passed / 1 failed** for a local test run, with 10/10 lightweight notebook executions and no fresh heavy YOLO/PatchCore training. These are **repository-recorded** results; I did not independently run the notebook suite or a Windows CMD test in this review.

**Recommendation:** Keep the corrected numerical examples and most existing graphics. Next, perform a focused **Windows Command Prompt (`cmd.exe`) migration**, eliminate the known checkpoint-related test failure, remove duplicate SVG content, and strengthen true code-to-visual teaching in the early lessons. Do not indiscriminately recreate all diagrams, change fixed model settings, or overwrite historic reference results.

### Scope and confidence

- Inspected the latest repository tree and current commit; source-read all **16 notebook JSON files** for structure, Markdown image references, and shell instructions.
- Reviewed the main setup, syllabus, troubleshooting, package requirements, latest remediation record, generator, run-manifest helper, and audit/visual/schedule tests.
- Viewed the generated PNG renditions of **all 15 new SVGs** and reviewed their generator and figure manifest. SVG source checked for a confirmed duplicate (identical Git blob SHA).
- Did **not** execute the full toolchain locally, verify actual Windows Command Prompt behavior, perform a classroom usability test, verify all historic PNG images pixel-by-pixel, or visually render all six shipped PDF books in this pass.
- Findings labelled **confirmed** are directly grounded in files inspected. **Improvement** indicates a recommended pedagogical refinement, not a proven execution failure.

## 2. Previous audit — closure status

The latest remediation record explicitly marks TA-001–TA-011 **FIXED**, with tests or code evidence for each. This review found the corresponding revised source present. TA-012–TA-014 remain **PARTIAL** by the repository's own account.

| Earlier finding | Latest state and evidence | Current recommendation |
|---|---|---|
| TA-001 Setup/preflight conflicts | **Fixed for PowerShell**: `START_HERE.md` has 11 ordered steps, both environments before Day 1. | Convert the now-consistent *entire* workflow to CMD, do not resurrect conflicting sequences. |
| TA-002 Four-task geometry | **Fixed**: shared `spot_mask(200)`, 249-pixel mask and `(76,102,93,119)` exclusive-edge box. SVG and PNG draw from common geometry. | Keep geometry; clarify GT annotation vs detector prediction. |
| TA-003 Cross-image mm² scaling | **Fixed**: `calibrated_defects()` uses a same-image, ideal same-plane reference, 120 px / 100 mm. | Preserve explicit metrology assumptions. |
| TA-004 Biased old comparison | **Fixed in narrative**: `docs/test_report.md` now labels 17/26 vs 26/26 **SUPERSEDED / biased**; corrected workflow uses calibration→freeze→test. | Do not quote old numbers as new performance; only verify fresh results if actually rerun. |
| TA-005 Hash ≠ no leakage | **Fixed**: checker says no byte-identical duplicates, while admitting near-duplicate/session leakage. | Keep group-level split teaching. |
| TA-006 Lexical model selection | **Fixed**: `assets/helpers/training_run.py` saves an explicit run manifest and has an mtime fallback with a visible warning. | Keep run provenance and never silently select weights. |
| TA-007 Mismatched YOLO box numbers | **Fixed**: common `(96,72,168,132)` on 240×240; YOLO `0 0.550000 0.425000 0.300000 0.250000`. | Explain that exclusive-edge conventions are array/annotation context dependent. |
| TA-008 Silent tolerance rounding | **Fixed**: comparison uses unrounded difference; boundary tests exercise inclusive edges and float caveat. | Preserve test policy; explain measurement resolution separately. |
| TA-009 Pixel/mm caption/layout | **Fixed**: uncertainty is specifically ±0.5 px → ±0.25 mm in its own explanatory panel. | Keep clear that this is not guaranteed metrology accuracy. |
| TA-010 `min` threshold ≠ detectability | **Fixed**: reported as “minimum pixel below threshold,” not evidence of successful defect recognition. | Reinforce sampling and feature visibility. |
| TA-011 Wrong reference path | **Fixed**: `assets/reference_outputs/` distinguished from student-generated `submissions/`. | Keep exact paths in CMD examples. |
| TA-012 Dense diagram redesign | **Partial**: 15 new editable SVGs, still some generic six-box summaries. | Target code-aligned visuals, not more decorative flowcharts. |
| TA-013 Provenance/score variability | **Partial**: reference vs schematic vs live results are better labelled; `streak_0005` raw provenance not available for new plot. | Never fabricate fresh scores or silently replace references. |
| TA-014 Japanese/English + learner pilot | **Partial**: structural bilingual prompts added; no complete human editorial review or two-beginner classroom pilot. | Review readability against actual code output; preserve Japanese-first ordering. |

## 3. New findings — prioritized action register

| ID | Priority | Type | Location | Evidence and exact action |
|---|---|---|---|---|
| SB-01 | **P0** | Confirmed CMD incompatibility | `START_HERE.md` lines ~3–19, 27–66, 74–105, 189–219 | Main authoritative guide is **PowerShell-specific** (`Set-Location`, `$HOME`, `Get-ChildItem`, `Activate.ps1`, `Set-ExecutionPolicy`). Rewrite as one authoritative `cmd.exe` path, preserving 11-step preflight and two environments. |
| SB-02 | **P0** | Confirmed CMD incompatibility | `notebooks/00_Setup/00_Environment_Setup.ipynb` | The setup notebook teaches how to open PowerShell, shows `PS` prompt, has PowerShell fenced code blocks, installation language and an `Activate.ps1` troubleshooting item. Update Markdown, expected output, and the code cell's printable instruction. Keep real Python code and intentional NameError. |
| SB-03 | **P0** | Confirmed CMD incompatibility | `docs/troubleshooting/installation.md` lines ~17–55, 104–174, 190–291 | Proxy examples use `$env:HTTP_PROXY`/`$env:HTTPS_PROXY`; package filter uses `Select-String`; activation and comments use PowerShell syntax. Provide CMD-safe `set "VAR=value"`, `findstr /I`, `REM` or prose, `activate.bat`, and direct-python fallback. Remove irrelevant execution-policy workaround from *current* learner guidance. |
| SB-04 | **P1** | Confirmed inconsistent shell snippets | `README.md` lines ~90–109, 127–144, 194–198, 213–217, 262+; `docs/pdf/README.md`; `docs/reference_materials.md` | Convert code fences to `cmd`; replace `$HOME`; use `cd /d`; remove inline `# ...` comments from executable CMD lines. Some commands are Python-only and require no change. |
| SB-05 | **P1** | Confirmed stale setup examples | `requirements/base.txt`, `requirements/anomalib.txt`, `requirements/pdf.txt`, `requirements/yolo.txt` | Replace explanatory `PowerShell` comments and `Activate.ps1`. YOLO GPU installation comment uses Bash `\` line continuation — **not valid CMD**; use one CMD line or correct `^` continuation, after verifying wheel availability. Keep pinned versions untouched unless independently proven invalid. |
| SB-06 | **P1** | Confirmed stale generator wording | `assets/scripts/remediate_notebooks.py` line ~69; `Day01_02` troubleshooting; `Day05_02` missing-dataset message | Remediation script still rewrites `Set-ExecutionPolicy` text. Ensure running maintenance scripts cannot silently reintroduce PowerShell content. Update instructional strings, not numerical logic or library code. |
| SB-07 | **P1** | Known test failure, confirmed root cause | `assets/tests/test_schedule.py` → `_notebook_path()` and `_all_notebooks()`; related recursive notebook searches | Recursive `rglob()` includes Jupyter `.ipynb_checkpoints`, so the course test can find the real notebook plus checkpoint and assert `len(matches)==1`. Exclude checkpoint directories in discovery and test with an artificial checkpoint. **Do not delete or rewrite user checkpoints.** |
| SB-08 | **P1** | **Confirmed duplicate visual** | `assets/svg/teach_pixel_inspector.svg` and `teach_slice_walkthrough.svg`; generated PNGs; `generate_svg_figures.py` `build_figure` | Both SVG files have identical Git blob SHA **`38ab22090a0ee6a0a84debd0c1ab40d9ce997d60`** and identical rendered content. Build two truly distinct views: (A) single-pixel address/value, (B) slice bounds, selected 3×3 block and output. Add test that normalized SVG content differs. |
| SB-09 | **P1** | Publication consistency | `docs/pdf/*.pdf`, `docs/pdf/README.md`, `docs/reviews/2026-11-15_audit_remediation.md` | Remediation record states **only a Day 2 PDF sample** was rebuilt; distributed books may predate notebook/SVG edits. Re-export all six PDFs from current source if dependencies available, inspect bilingual text and every new image, report if regeneration cannot be verified. Do not claim PDF visual checks without rendering. |
| SB-10 | **P2** | Educational improvement | `teach_code_cell_lifecycle_svg.png`, `teach_yolo_result_object_svg.png`, `teach_mass_units_chain_svg.png`, `teach_patchcore_stages_svg.png`, `teach_frozen_threshold_pipeline_svg.png` | Mostly **six adjacent text boxes**, not direct illustration of a code line operating on an object. Replace selectively with one or two worked examples, arrows linking an actual input to intermediate values and code outputs. Keep useful summaries as optional recap. |
| SB-11 | **P2** | Educational improvement | `teach_cv_tasks_outputs.svg`, Day01_03 | Geometry is now correct; detection panel displays a **GT box**, not an actual model prediction, while anomaly map is schematic. Explicitly label “annotation / GT; example output not inferred” or draw separate mock prediction without implying ground truth equals model result. |
| SB-12 | **P2** | Educational improvement | `teach_detection_matching.svg`, Day04_03 | Computed IoU matrix and TP=1, FP=1, FN=1 are consistent with source. However, two overlapping predictions on one truth are not clearly labelled P1/P2 in the image; add legend/arrows linking matrix entries to matched/unmatched boxes. |
| SB-13 | **P2** | Educational improvement | `teach_epoch_batch_step.svg` and Day04_02 | 64 images/8 = eight batches is correct; optimizer steps may be affected by gradient accumulation/warmup. New SVG states this caveat, but students need a visual brace encompassing eight batches and an explicit *illustrative* update rather than assuming eight or one updates always. |
| SB-14 | **P2** | Archive hygiene | `docs/test_report.md`, `docs/implementation_report.md`, historical `agent/` files | Historical PowerShell commands and 258-test/16-notebook records should remain **dated archives**. Put a short “current CMD guide” pointer above them rather than retroactively altering evidence; do not claim historical tests ran under CMD. |
| SB-15 | **P2** | Testing gap | Windows setup instructions and any new `.cmd` launcher | No Windows CMD smoke test is recorded for this revision. Create static regression tests for current learner-facing shell snippets and a manual Windows 11 smoke checklist. If runner is Windows, actually exercise CMD. |

### No `.ps1` scripts found in the current tracked tree

The repository tree contains **no tracked `.ps1` or `.bat` startup script**. The PowerShell dependencies are primarily **Markdown/Jupyter installation instructions**, a few Python-generated instructional strings, and historical examples. Changing a filename or just rewriting `Activate.ps1` is insufficient; convert the *shell language* across those surfaces. An optional `start_training.cmd` can improve the classroom launch experience.

## 4. SVG audit — actual new visual inventory

All 15 SVG-derived PNGs were inspected visually. The current SVG renderer uses a fixed 900×590 `viewBox`, text boundaries and local native vectors; Japanese glyphs render in the provided preview PNGs. The automated bounds test is useful but does not validate factual equivalence or beginner comprehension.

| SVG name (without extension) | Current verdict | Required next step |
|---|---|---|
| `teach_code_cell_lifecycle` | Accurate values; text-rich six panels | Better depict a timeline of kernel state: `3 → 4 → 5`, restart clears memory; show arrows across actual sequence. |
| `teach_pixel_inspector` | Correct 5×7 grid, but duplicates next SVG | Focus on **one cell** and `canvas[2,3] == 100`, coordinate order and grayscale intensity, not slicing. |
| `teach_slice_walkthrough` | **Exactly identical** to pixel inspector | Make genuinely separate 3×3 slicing walkthrough, start/end indices, produced array and shape. |
| `teach_cv_tasks_outputs` | **Corrected** 249-pixel mask/GT bounding box | Distinguish GT from inferred result and explain schematic heatmap. |
| `teach_mass_units_chain` | Mathematically correct chain; answer intentionally omitted | Show unit cancellation with a dimensioned sheet, not only labels. Keep exercise unsolved. |
| `teach_if_live_trace` | `100.3 → OK`; boundary and float caveat correctly described | Show true and false branch paths, 100.5001 → NG, and condition visually. |
| `teach_opencv_pixel_pipeline` | Threshold 120 toy array and mask computed; connected region count defensible | Add small actual input/mask 2×3 tiles (currently two text arrays). |
| `teach_calibration_same_plane` | Strong: actual same-plane synthetic bars 120/100 and 60/50 | Retain; optionally annotate detected contour vs pixel count and ± uncertainty. |
| `teach_bbox_one_example` | Correct normalized YOLO numbers | Add dimension arrows and intermediate `(132,102)` centre to reduce text-only arithmetic. |
| `teach_yolo_result_object` | Attribute paths correct, but text-only | Draw nested Results/Boxes object and map one box row to plotted image and CSV output. |
| `teach_epoch_batch_step` | Correct batch count with warmup disclaimer | Draw accumulation grouping; no universal optimizer-step count. |
| `teach_detection_matching` | Correct example IoU/count logic | Label GT1/GT2/P1/P2 spatially with arrows to matched, duplicate, and missed. |
| `teach_patchcore_stages` | Correct frozen-feature / memory / inference distinction | Show a patch crop, feature vector, memory-bank nearest neighbour, raw map, and calibrated score. |
| `teach_frozen_threshold_pipeline` | Correct general six-stage process | Draw separate calibration/test lanes and a **blocked** feedback arrow, plus model freeze point. |
| `teach_group_split_vs_frame_split` | Correct distinction between near-duplicate frames and byte hash | Use two actual visually similar frame thumbnails instead of only words. |

**Key visual principle:** a figure is useful when the student can trace an input, an executed code expression, the intermediate computation, and the actual expected output. Generic boxes are fine as recaps but are not substitutes for worked evidence.

## 5. Notebook-by-notebook follow-up

| Notebook | Source correctness status | Visual / shell action |
|---|---|---|
| `00_Setup/00_Environment_Setup` | Main remaining blocker is **PowerShell-specific prose**, not NumPy/Jupyter logic. | Convert all terminal examples to CMD; revise terminal screenshots/schematic and error recovery; keep `%pip` as notebook magic. |
| `Day01_01_Introduction_to_AI` | Earlier rule-vs-learning / Gaussian caveats retained; no new SVG. | Optional exact brightness-range trace linked to mean/std variables; do not add unnecessary flowcharts. |
| `Day01_02_Pixels_and_Images` | `min` vs visibility correction present; slicing data correct. | Replace duplicate SVG with pixel inspector and slice-specific illustration; change its PowerShell troubleshooting wording. |
| `Day01_03_Computer_Vision_Tasks` | Same-defect GT geometry now consistent. | Clarify prediction-vs-ground-truth in four-task figure. |
| `Day02_01_Python_Basics` | Mass input constants preserved, exercise unsolved. | Better unit-cancellation and worked formula without spoiling exercise. |
| `Day02_02_Conditions_Loops_Functions` | Inclusive raw tolerance checks correct; tests explicitly cover float pitfalls. | Add branch visualization and trace rows; do not insert a silent epsilon. |
| `Day02_03_OpenCV_Image_Processing` | New calibrated scene fixes physical-unit mixing; contour area not pixel count. | Retain calibrated plot; show exact thresholded array on same scene. |
| `Day03_01_YOLO_Concepts` | Box coordinates now agree across code and SVG. | Add centre and normalization arrows; avoid universal edge-exclusivity claim beyond stated convention. |
| `Day03_02_YOLO_Inference` | Inference result fields as described; no new execution in this audit. | Show Results-object hierarchy and zero-box behavior. |
| `Day03_03_YOLO_Experiments` | Confidence and resizing lesson structure retained; no new SVG. | Explicit image-before/after downsampling and threshold vs image-size distinction. |
| `Day04_01_YOLO_Dataset_Annotation` | Byte-hash claim corrected, split leakage caveat retained. | Replace verbal group split with side-by-side frames and acquisition-group boundaries. |
| `Day04_02_YOLO_Training` | Training manifest added; batch/warmup distinction retained. | Use an accumulation diagram with no misleading universal update count. |
| `Day04_03_YOLO_Evaluation` | Explicit run handoff/mtime fallback; matching counts correct. | Spatial labels and matching table should cross-highlight. |
| `Day05_01_Anomaly_Detection_Concepts` | No freshly proven conceptual error in this pass; no new SVG. | Optionally overlay a simple patch location and embedding point separately. |
| `Day05_02_PatchCore_Training` | Frozen backbone/cache policy and normalization caveats preserved; full live fit not re-run. | Replace error's “PowerShell” instruction with CMD; draw true image patch → feature → memory distance. |
| `Day05_03_YOLO_vs_PatchCore` | Calibration/test separation and provenance better; no regenerated comparison run. | Show threshold freeze and distinct score scales, not a fabricated performance ranking. |

## 6. PowerShell → Windows Command Prompt migration: precise specification

### 6.1 Preferred shell policy

- **Student-facing Windows instructions:** `cmd.exe` / **コマンド プロンプト (Command Prompt)**, not PowerShell.
- Notebook code cells remain **Python**, `%pip` remains **Jupyter/IPython magic**, and Markdown historical/test records retain accurate history.
- Keep `.venv` for Days 0–4 and `.venv-anomalib` for Day 5. Both environments should be prepared before Day 1 by default, with the existing instructor-approved exception unchanged.
- Do **not** change Python library versions, the YOLO model, the Anomalib kernel, or dataset provenance purely for shell migration.
- Prefer direct `.venv\Scripts\python.exe` for reproducible commands and troubleshooting. Use `activate.bat` in interactive CMD only when teaching activation.

### 6.2 CMD replacements

| PowerShell form | CMD form | Caveat |
|---|---|---|
| `Set-Location "$HOME\Documents"` | `cd /d "%USERPROFILE%\Documents"` | `%USERPROFILE%\Documents` may be redirected to OneDrive; instruct learners to use their actual extracted folder. |
| `Get-ChildItem` | `dir` | `dir` is a CMD built-in. |
| `pwd` | `cd` | No arguments prints current CMD directory. |
| `.\.venv\Scripts\Activate.ps1` | `.\.venv\Scripts\activate.bat` | Interactive CMD works without `call`; **inside another `.cmd`/`.bat` use `call`**. |
| `.\.venv-anomalib\Scripts\Activate.ps1` | `.\.venv-anomalib\Scripts\activate.bat` | Confirm prompt and `where python` before installing. |
| `Set-ExecutionPolicy -Scope Process ...` | **Remove entirely** | CMD batch activation is not governed by PowerShell execution policy. No elevation should be required. |
| `$env:HTTP_PROXY = "..."` | `set "HTTP_PROXY=http://proxy.example.co.jp:8080"` | Example proxy only; never assume a real factory proxy exists. |
| `$env:HTTPS_PROXY = "..."` | `set "HTTPS_PROXY=http://proxy.example.co.jp:8080"` | Scope is current CMD session. |
| `python -m pip list \| Select-String "opencv"` | `python -m pip list \| findstr /I opencv` | Or use `python -m pip show opencv-python`; test package in correct environment. |
| `# comment` in terminal code block | `REM comment` or prose outside code block | `#` is not a CMD comment. Do not use trailing `#` on runnable commands. |
| PowerShell backtick `` ` `` for line continuation | One line, or `^` as the last character on a CMD line | Prefer one-line commands for absolute beginners; no trailing spaces after `^`. |
| Bash `\` continuation (YOLO requirements example) | One command on one CMD line | Also independently check GPU wheel compatibility before recommending GPU commands. |
| `deactivate` | `deactivate` | Available after CMD `activate.bat`; if not activated, skip. |
| `\`-prefixed relative executables | `".\.venv\Scripts\python.exe"` | Quotes safer for paths containing spaces; direct path avoids dependence on activation/PATH. |

### 6.3 Example: *manual* CMD setup from repository root

The following is a **proposed** sequence to implement and smoke-test on Windows, not an installation performed during this audit. It assumes Git clone under the default Documents location; ZIP/OneDrive paths require adjustment.

```cmd
cd /d "%USERPROFILE%\Documents"
git clone https://github.com/stefanoKS/Training_Automation.git
cd /d "%USERPROFILE%\Documents\Training_Automation\AI_Vision_Training"
dir
py -3.11 --version
py -3.11 -m venv .venv
.\.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements\base.txt
python -m pip install -r requirements\yolo.txt
deactivate
py -3.11 -m venv .venv-anomalib
.\.venv-anomalib\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements\anomalib.txt
deactivate
".\.venv\Scripts\python.exe" -m ipykernel install --user --name aivision --display-name "Python 3 (AI Vision)"
".\.venv-anomalib\Scripts\python.exe" -m ipykernel install --user --name aivision-anomalib --display-name "Python 3 (AI Vision Anomalib)"
".\.venv\Scripts\python.exe" assets\scripts\generate_training_assets.py
".\.venv\Scripts\python.exe" assets\scripts\prepare_datasets.py
".\.venv\Scripts\python.exe" assets\scripts\generate_teaching_diagrams.py
".\.venv\Scripts\python.exe" assets\scripts\generate_svg_figures.py
".\.venv\Scripts\python.exe" -m jupyter lab
```

Keep the existing separate photo/model preload and offline checks in START_HERE between asset generation and launch. Do not run all pip commands automatically when launching Jupyter each day.

### 6.4 Optional one-click `start_training.cmd` launcher

Place a simple launcher at `AI_Vision_Training/start_training.cmd`. Use `%~dp0` to resolve the course root even if a learner double-clicks from elsewhere. It should:

1. `@echo off`, `setlocal`, `cd /d "%~dp0"`; fail visibly if the directory is invalid.
2. Check `.venv\Scripts\python.exe` exists. If not, print Japanese and English directions to START_HERE; **do not auto-install**.
3. Start `"%~dp0.venv\Scripts\python.exe" -m jupyter lab` and propagate the real exit code.
4. Never require PowerShell, administrator rights, shell execution-policy changes or network during routine launch.
5. If a separate batch calls `activate.bat`, use `call`; prefer direct executable for launcher simplicity.
6. Prevent invisible window closure on a startup error (show a clear message and an optional `pause`).

Do **not** add a launcher that rewrites student notebooks, resets datasets, downloads model weights every day or takes over local package management.

## 7. Validation and acceptance plan for Codex

**Source and notebook regression**

1. `python assets\scripts\validate_notebooks.py` passes structural checks.
2. `python -m pytest assets\tests -q` passes *without ignoring or deleting `.ipynb_checkpoints`*. Fix the discovery predicate, and create a temporary checkpoint fixture to prevent recurrence.
3. Geometry checks remain unchanged: mask=249, GT box `(76,102,93,119)`; calibrated px/mm=1.2, contour areas 475 and 925 px²; YOLO normalized `(0.55,0.425,0.3,0.25)`; IoU=6750/15150; mass=1.5925 kg **without completing the student exercise**.
4. Verify both generated SVG and PNG for pixel-inspector vs slice-walkthrough are **different**, contain the intended respective focus, and remain referenced by the correct Markdown sections.
5. Re-run `generate_svg_figures.py` twice and verify deterministic output, identical rebuild results and no loss of Japanese glyphs. Preserve original reference-output PNG byte contents.
6. If PDF dependencies available, regenerate six course booklets and inspect rendered pages including Jupyter/CMD instructions and all 15 SVG fallback images. If not available, log **NOT RUN** rather than claiming success.

**CMD static and Windows smoke checks**

7. Search current **student-facing** docs and notebook cells for `powershell`, `Activate.ps1`, `Set-ExecutionPolicy`, `$HOME`, `$env:`, `Select-String`, `Get-ChildItem`, ` ```powershell `, and inappropriate `#` comments. Historical reports may retain old commands only if visibly dated. Check code strings and requirement comments too.
8. On actual Windows 11 `cmd.exe`: clone/ZIP path; `py -3.11 --version`; create both venvs; verify `activate.bat` and `deactivate`; verify `where python` or `python -c "import sys; print(sys.executable)"`; register both kernels; generate assets; test online preload then `--offline`; run both environment profiles; launch Jupyter from repo root, open setup notebook.
9. In a CMD batch context, test `call .\.venv\Scripts\activate.bat` returns to the caller (or avoid activation by direct venv executable). Verify spaces in the path and optional OneDrive Documents redirection, plus a missing-venv error path for `start_training.cmd`.
10. Test `set "HTTP_PROXY=..."`/`set "HTTPS_PROXY=..."` only in an isolated example environment (do not insert a fake company proxy into real settings), plus `findstr /I opencv` and `REM` syntax.
11. Run non-destructive `git diff --check`; document actual test counts and all unexecuted checks.

**Explicit non-goals:** No GPU training unless separately approved, no fabricated accuracy numbers, no deleting `.ipynb_checkpoints`, no overwriting historical evidence, no pushing/merging without explicit instruction, and no changing the bilingual Japanese-first syllabus or lesson durations.

## 8. File-change map for the next Codex pass

**Primary current documentation:** `START_HERE.md`, `README.md`, `docs/troubleshooting/installation.md`, `docs/pdf/README.md`, `docs/reference_materials.md`, `requirements/{base,yolo,anomalib,pdf}.txt`.

**Notebook instructional strings:** `notebooks/00_Setup/00_Environment_Setup.ipynb`, `notebooks/Day01_AI_Fundamentals/Day01_02_Pixels_and_Images.ipynb`, `notebooks/Day05_PatchCore/Day05_02_PatchCore_Training.ipynb`.

**Generators and tests:** `assets/scripts/remediate_notebooks.py`, `assets/scripts/generate_svg_figures.py`, `assets/tests/test_schedule.py`, `assets/tests/test_visual_assets.py`, `assets/tests/test_audit_remediation.py`, and, if necessary, a new `assets/tests/test_cmd_documentation.py`.

**Figures:** `assets/svg/teach_pixel_inspector.svg`, `assets/svg/teach_slice_walkthrough.svg`, corresponding `_svg.png` files; selectively improve the other named SVGs and regenerate from source rather than hand-editing generated fallbacks. The figure manifest should be regenerated.

**Optional new file:** `AI_Vision_Training/start_training.cmd` (no automatic installation).

**Archives that should not be silently rewritten:** `docs/test_report.md` historic section, `docs/implementation_report.md` prior runs, `docs/reviews/2026-11-15_audit_remediation.md`, `agent/` previous audit instructions, `assets/reference_outputs/*`. Add a current CMD pointer where useful; retain provenance.

## 9. Final assessment

The revised course is significantly stronger than at the first review. Its most consequential **remaining confirmed defects** are not YOLO/PatchCore mathematics but (1) current student-facing shell instructions being written for PowerShell instead of the requested CMD, (2) the checkpoint-sensitive test glob, and (3) the byte-identical pair of SVG visuals. Fix those first. Then improve the few figures that currently describe code with text instead of actually showing **input → calculation → result**. This approach best serves two students starting from zero while protecting the already-correct technical lessons.
