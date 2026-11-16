# Nepali translation/layout fix implementation log

## Baseline and boundaries

- Read the complete [supplied follow-up audit](Training_Automation_Nepali_Translation_Layout_Followup_Audit_2026-11-17.md) before implementation.
- Initial/current HEAD: `8857204b2d9d0e34a5befbad73e00da98ff5fcd7`, exactly the report baseline. No newer commit needed reconciliation.
- Initial worktree: clean except for the user-supplied, untracked audit.
- Inspected all 16 shipped nbformat 4.5 notebooks, the six cited cells, localization catalogs/appliers, the trilingual exporter and relevant tests before implementation. The notebook checkpoint copy is not a shipped course notebook.
- No original teaching image was regenerated, edited or translated. No model or notebook kernel was run. No dependency was installed; no launcher/setup file was changed. No commit, push or merge was performed.
- Review screenshots below are inspection evidence, not new course figures.

## Changes and rationale

### Corresponding headings

The original inventory contained 641 `after-heading` translations. Explicitly paired 222 non-title Japanese/English headings belonging to the same concept; one of these pairs was already adjacent. Notebook title handling remains separate.

Each affected Nepali sidecar now uses a bold translation label and an explicit `<!-- ne-pair: English heading -->` declaration. The exporter emits one semantic JA/EN/NE heading at the original Japanese heading, suppressing only its explicitly identified English counterpart. Japanese/English body paragraphs retain their original order and content. Unrelated adjacent headings remain separate; fenced code comments are not headings.

The three cited heading cases are H4. They become single semantic headings but remain outside the printed H1-H3 TOC under the existing policy. Eligible headings have a single TOC entry. Printed TOC regression tests check complete trilingual text and actual body page numbers, including repeated heading labels.

### Existing images, captions and visual explanations

Audited all 85 image-bearing Markdown cells. Each now has an `after-image:<exact original Markdown target>` Nepali anchor. The applier validates missing/duplicate targets and is idempotent. A two-image fixture checks that captions cannot cross-associate.

The exporter places the corresponding Japanese, English and leading Nepali caption beneath the same existing image, followed by its Nepali visual notice/question. It reads complete wrapped caption paragraphs; it does not promote arbitrary later Nepali lesson paragraphs to captions. Existing A/B labels are preserved.

Landscape figure groups use the 175 mm available figure area within the existing 180 mm landscape content height, leaving room for their vertical margins. Flex layout keeps captions/notes unshrunk and fits the original image, with its aspect ratio preserved, into the remaining space. This replaces an overly conservative 80 mm image cap that made some original labels unnecessarily small. A fixed 110 mm trial split six long explanations; the final fitting layout kept all 85 image/explanation groups together in the focused PDF probe and regression test. No image bytes changed.

Day 5 archived TEST-only figures retain their original gating/provenance. Bilingual and trilingual Day05/Week1 PDF tests check that those archived image bytes are absent from student-facing PDFs.

### TOC, fonts and general-document export

- TOC page digits occupy a fixed-width column. Heading lookup uses complete trilingual signatures in body order, not incidental English mentions.
- Missing body markers/headings and changes in two-pass pagination fail explicitly.
- The transparent body sentinel reserves 1 pt of height. A zero-height sentinel was observed in the preceding TOC page's text layer; a two-page rendered regression now verifies that body lookup cannot mistake a TOC occurrence for the real heading.
- General-document `doc:<id>` localization regions render without being incorrectly validated as notebook anchors; a regression covers the installation-guide failure found during rebuilding.
- Chromium resolved the Nepali sample to **Nirmala UI**, PostScript `NirmalaUI`. The installed font cmap covered all 65 distinct Devanagari code points inventoried from notebook/document catalogs.
- The temporary font probe is placed onscreen and laid out after `document.fonts.ready` before asking Chromium for its resolved fonts, avoiding an observed empty-usage timing race.
- A missing Devanagari-capable resolved font produces a diagnostic instead of accepting generic fallback.
- Preserved the existing `font-feature-settings: "abvm" 0` shaping/searchability rule and established Nepali font-size conventions.
- Corrected the exporter docstring to `Setup_ja_en_ne.pdf`; no distributed file was renamed.

### Nepali-only learner walkthrough

Compared each requested original Japanese/English document, with Nepali regions stripped, against its Nepali sidecar. This was an actionable-instruction audit, not a fresh installation or native-speaker usability trial.

| Document | Conditions/commands/warnings checked | Outcome |
|---|---|---|
| [START_HERE.md](../../START_HERE.md) | ZIP versus clone; course-root selection; File Explorer `cmd`; redirected Documents/OneDrive; quoted paths; Python 3.11; `.venv`/`.venv-anomalib`; activation failure; kernels; preloading; offline checks | Existing Nepali instructions cover these branches; unchanged. |
| [README.md](../../README.md) | Course entry points; launcher/manual paths; maintenance commands; notebook validation; PDFs; reporting and repository structure | Added missing actionable maintenance/PDF commands and corrected Nepali references to the actual ten PDF filenames. |
| [COURSE_SYLLABUS.md](../../COURSE_SYLLABUS.md) | Preflight tasks; every timetable window/duration/lesson; required/optional work; report submissions | Added missing timetable rows, preflight checks, optional assignments and deliverables; corrected two recovery-summary distinctions to match the original meaning. |
| [installation troubleshooting](../troubleshooting/installation.md) | Python/path/kernel problems; two environments; activation recovery using explicit interpreter paths; download/offline and other troubleshooting branches | Already present in Nepali; unchanged. |
| [tested versions](../../requirements/tested_versions.md) | Python 3.11 and pinned requirements; base/anomalib environment separation; compatibility warnings and recovery branches | Already present in Nepali; unchanged. |

Literal commands, paths, version requirements and link targets were retained in the corresponding translations. CMD parity tests cover START_HERE, README and installation troubleshooting; a separate test compares syllabus timetable windows, minutes and ordered lesson references. No PowerShell syntax was introduced into CMD examples.

The glossary records `निर्देशाङ्क` / `निर्देशांक` and `सह्यता` / `सहनशीलता` as alternatives awaiting native reviewer adjudication. It does not assert an unverified preferred spelling or interchangeability.

## Exact implementation paths

All paths below are relative to `AI_Vision_Training`.

### Scripts, tests and learner documents

```text
assets\scripts\apply_nepali_translations.py
assets\scripts\check_nepali_coverage.py
assets\scripts\export_trilingual_pdf.py
assets\tests\test_nepali_localization.py
assets\tests\test_pdf_exports.py
assets\tests\test_trilingual_layout.py
assets\i18n\ne\docs\README.ne.md
assets\i18n\ne\docs\COURSE_SYLLABUS.ne.md
assets\i18n\ne\terminology.md
README.md
COURSE_SYLLABUS.md
```

### Notebook and matching sidecar paths

Only Nepali Markdown regions changed: 307 Markdown cells across these 16 notebooks. All original cell IDs, all 276 complete code-cell JSON objects, notebook/cell metadata and non-Nepali Markdown content were preserved.

| Notebook | Matching sidecar |
|---|---|
| `notebooks\00_Setup\00_Environment_Setup.ipynb` | `assets\i18n\ne\notebooks\00_Environment_Setup.ne.md` |
| `notebooks\Day01_AI_Fundamentals\Day01_01_Introduction_to_AI.ipynb` | `assets\i18n\ne\notebooks\Day01_01_Introduction_to_AI.ne.md` |
| `notebooks\Day01_AI_Fundamentals\Day01_02_Pixels_and_Images.ipynb` | `assets\i18n\ne\notebooks\Day01_02_Pixels_and_Images.ne.md` |
| `notebooks\Day01_AI_Fundamentals\Day01_03_Computer_Vision_Tasks.ipynb` | `assets\i18n\ne\notebooks\Day01_03_Computer_Vision_Tasks.ne.md` |
| `notebooks\Day02_Python_OpenCV\Day02_01_Python_Basics.ipynb` | `assets\i18n\ne\notebooks\Day02_01_Python_Basics.ne.md` |
| `notebooks\Day02_Python_OpenCV\Day02_02_Conditions_Loops_Functions.ipynb` | `assets\i18n\ne\notebooks\Day02_02_Conditions_Loops_Functions.ne.md` |
| `notebooks\Day02_Python_OpenCV\Day02_03_OpenCV_Image_Processing.ipynb` | `assets\i18n\ne\notebooks\Day02_03_OpenCV_Image_Processing.ne.md` |
| `notebooks\Day03_YOLO_Basics\Day03_01_YOLO_Concepts.ipynb` | `assets\i18n\ne\notebooks\Day03_01_YOLO_Concepts.ne.md` |
| `notebooks\Day03_YOLO_Basics\Day03_02_YOLO_Inference.ipynb` | `assets\i18n\ne\notebooks\Day03_02_YOLO_Inference.ne.md` |
| `notebooks\Day03_YOLO_Basics\Day03_03_YOLO_Experiments.ipynb` | `assets\i18n\ne\notebooks\Day03_03_YOLO_Experiments.ne.md` |
| `notebooks\Day04_YOLO_Training\Day04_01_YOLO_Dataset_Annotation.ipynb` | `assets\i18n\ne\notebooks\Day04_01_YOLO_Dataset_Annotation.ne.md` |
| `notebooks\Day04_YOLO_Training\Day04_02_YOLO_Training.ipynb` | `assets\i18n\ne\notebooks\Day04_02_YOLO_Training.ne.md` |
| `notebooks\Day04_YOLO_Training\Day04_03_YOLO_Evaluation.ipynb` | `assets\i18n\ne\notebooks\Day04_03_YOLO_Evaluation.ne.md` |
| `notebooks\Day05_PatchCore\Day05_01_Anomaly_Detection_Concepts.ipynb` | `assets\i18n\ne\notebooks\Day05_01_Anomaly_Detection_Concepts.ne.md` |
| `notebooks\Day05_PatchCore\Day05_02_PatchCore_Training.ipynb` | `assets\i18n\ne\notebooks\Day05_02_PatchCore_Training.ne.md` |
| `notebooks\Day05_PatchCore\Day05_03_YOLO_vs_PatchCore.ipynb` | `assets\i18n\ne\notebooks\Day05_03_YOLO_vs_PatchCore.ne.md` |

### PDF artifacts and evidence

```text
docs\pdf\Day01_explanation_ja_en_ne.pdf
docs\pdf\Day02_explanation_ja_en_ne.pdf
docs\pdf\Day03_explanation_ja_en_ne.pdf
docs\pdf\Day04_explanation_ja_en_ne.pdf
docs\pdf\Day05_explanation_ja_en_ne.pdf
docs\pdf\Week1_explanation_ja_en_ne.pdf
docs\pdf\Setup_ja_en_ne.pdf
docs\pdf\Installation_Guide_ja_en_ne.pdf
docs\pdf\Repository_Guide_ja_en_ne.pdf
docs\pdf\Course_Syllabus_ja_en_ne.pdf
docs\reviews\Nepali_Translation_Layout_Fix_Implementation_Log.md
docs\reviews\nepali_layout_evidence\
```

The supplied audit is an input, not an implementation change. Seven older review files were observed deleted later in the session; those unrelated deletions were neither made nor restored by this task:

```text
docs\reviews\2026-11-15_audit_remediation.md
docs\reviews\2026-11-15_cmd_migration.md
docs\reviews\Day01-Day05_Clarity_Implementation_Log.md
docs\reviews\Day01-Day05_Teaching_Clarity_Review_2026-11-16.md
docs\reviews\Day02-Day05_Followup_Implementation_Log_2026-11-16.md
docs\reviews\Nepali_Localization_And_PDF_Implementation_2026-11-16.md
docs\reviews\Training_Automation_Day02-Day05_Followup_Audit_2026-11-16.md
```

## Validation results

| Check | Actual result |
|---|---|
| Notebook applier, default dry-run mode | All 16 catalogs; 0 cells would change; 0 problems. |
| Document applier, default dry-run mode | All 12 catalogs; 0 changes; 0 problems. |
| Strict Nepali coverage | 653/800 Markdown cells translated, 147 exemptions, 0 missing; 12/12 documents. |
| `validate_notebooks.py --execute none` | **194 passed, 0 failed, 0 skipped**; no kernel/model execution. |
| Full `assets\tests` suite with the exclusions below | **391 passed, 13 deselected, 4 warnings**, in 512.03 seconds. |
| Focused semantic/layout suite before the full run | 17 passed, 6 distributed-TOC cases deselected; all 23 cases subsequently included in the passing full run. |
| Pylance syntax checks | No syntax errors in the modified localization/export scripts or the new layout regression file. |
| Final preservation comparison | 16 complete stripped notebook JSON objects and 513 protected hashes match; 276 complete code cells unchanged; exactly 307 Markdown cells changed. |
| Five learner documents, original-language comparison | Original Japanese/English content matches after stripping Nepali regions. |
| `git diff --check` | Passed; Git emitted only LF-to-CRLF working-copy notices. |
| Final PDF inspection | **999 pages** across all ten PDFs; 0 blank-page, printable-area overflow or broken-Nepali heuristic flags. |

The four pytest warnings came from two existing noninteractive Matplotlib array/demo tests (`test_executed_slice_uses_the_illustrated_canvas_and_exclusive_stops` and `test_live_bgr_counterexample_and_same_mask_geometry`). Their Agg `show()` calls cannot display a window; they did not save or replace any teaching image. These numerical/example checks are distinct from the explicitly deselected image-generator tests.

The final PDF inspection used the existing `inspect_pdf_pages.py --languages ja,ne --scale 0.8`, with explicit `--pdf` arguments for the ten trilingual files only. Every page was rasterized; full raster/contact-sheet output was kept in the session inspection directory, not mixed into teaching assets. [The compact scan report](nepali_layout_evidence/pdf-inspection.json) contains per-file hashes, page counts and all flags. Installation/Repository Guide p.4 are original Japanese/English TOC continuations without Nepali; this is a language-presence notice, not blank/tofu output or a missing body translation.

| Final artifact in `docs\pdf` | Pages | TOC entries located and checked across both render passes |
|---|---:|---:|
| [Day01_explanation_ja_en_ne.pdf](../pdf/Day01_explanation_ja_en_ne.pdf) | 95 | 94 |
| [Day02_explanation_ja_en_ne.pdf](../pdf/Day02_explanation_ja_en_ne.pdf) | 111 | 98 |
| [Day03_explanation_ja_en_ne.pdf](../pdf/Day03_explanation_ja_en_ne.pdf) | 75 | 83 |
| [Day04_explanation_ja_en_ne.pdf](../pdf/Day04_explanation_ja_en_ne.pdf) | 87 | 89 |
| [Day05_explanation_ja_en_ne.pdf](../pdf/Day05_explanation_ja_en_ne.pdf) | 85 | 89 |
| [Week1_explanation_ja_en_ne.pdf](../pdf/Week1_explanation_ja_en_ne.pdf) | 442 | 458 |
| [Setup_ja_en_ne.pdf](../pdf/Setup_ja_en_ne.pdf) | 39 | 31 |
| [Installation_Guide_ja_en_ne.pdf](../pdf/Installation_Guide_ja_en_ne.pdf) | 23 | 33 |
| [Repository_Guide_ja_en_ne.pdf](../pdf/Repository_Guide_ja_en_ne.pdf) | 23 | 33 |
| [Course_Syllabus_ja_en_ne.pdf](../pdf/Course_Syllabus_ja_en_ne.pdf) | 19 | 26 |

### Agreed image-generation exclusions

The user explicitly selected **"Skip only image-generation tests and document exact exclusions."** No test configuration was changed. The following 11 functions account for 13 deselected test instances, including the parameterized diagram-generator cases:

```text
test_clarity_review.py::test_new_diagrams_are_deterministic_offline_and_text_stays_inside_canvas
test_evaluation_provenance.py::test_prefreeze_toy_is_calculated_without_any_saved_data
test_evaluation_provenance.py::test_score_distribution_uses_only_calibration_even_when_test_rows_exist
test_audit_remediation.py::test_four_tasks_use_the_source_spot_geometry
test_audit_remediation.py::test_bbox_diagram_and_executed_notebook_use_one_example
test_audit_remediation.py::test_matching_diagram_matrix_and_one_to_one_counts
test_audit_remediation.py::test_legacy_figures_do_not_reintroduce_rounding_or_universal_update_counts
test_audit_remediation.py::test_pixel_and_slice_figures_are_distinct_and_match_the_executed_array
test_assets.py::test_generator_is_deterministic
test_assets.py::test_defective_render_produces_requested_defects
test_datasets.py::test_dataset_is_reproducible
```

These are generator/diagram/plot tests, including generators that only construct images in memory or have saving monkeypatched. Static image inspections, image provenance/gating checks, tests that reject inputs before drawing, and the empty-generator manifest-preservation test remain enabled. PDF rendering/raster inspection is permitted and is not course-image regeneration.

Reproducible commands from the course root (existing Python 3.11 environment; no installation):

```bat
..\.venv\Scripts\python.exe assets\scripts\apply_nepali_translations.py
..\.venv\Scripts\python.exe assets\scripts\apply_nepali_docs.py
..\.venv\Scripts\python.exe assets\scripts\check_nepali_coverage.py --strict
..\.venv\Scripts\python.exe assets\scripts\validate_notebooks.py --execute none
..\.venv\Scripts\python.exe -m pytest assets\tests -q -k "not (test_new_diagrams_are_deterministic_offline_and_text_stays_inside_canvas or test_prefreeze_toy_is_calculated_without_any_saved_data or test_four_tasks_use_the_source_spot_geometry or test_bbox_diagram_and_executed_notebook_use_one_example or test_matching_diagram_matrix_and_one_to_one_counts or test_legacy_figures_do_not_reintroduce_rounding_or_universal_update_counts or test_pixel_and_slice_figures_are_distinct_and_match_the_executed_array or test_score_distribution_uses_only_calibration_even_when_test_rows_exist or test_generator_is_deterministic or test_defective_render_produces_requested_defects or test_dataset_is_reproducible)"
..\.venv\Scripts\python.exe assets\scripts\export_trilingual_pdf.py
```

The appliers' default mode is the dry run; they do not have a `--dry-run` flag.

## Notebook/HTML before-and-after evidence

Rendered with Jupyter's Markdown renderer (`nbconvert`/Mistune) and local Chromium, without a kernel. External HTTP(S) requests were blocked. "Before" cells came from HEAD; "after" cells came from the localized working notebooks.

| Reproduction | Before | After | Final exporter HTML |
|---|---|---|---|
| Setup heading `79328757` | [before](nepali_layout_evidence/html-79328757-before.png) | [after](nepali_layout_evidence/html-79328757-after.png) | [HTML](nepali_layout_evidence/exporter-79328757.png) |
| Day02 heading `e15c580c` | [before](nepali_layout_evidence/html-e15c580c-before.png) | [after](nepali_layout_evidence/html-e15c580c-after.png) | [HTML](nepali_layout_evidence/exporter-e15c580c.png) |
| Day05 heading `3d343aab` | [before](nepali_layout_evidence/html-3d343aab-before.png) | [after](nepali_layout_evidence/html-3d343aab-after.png) | [HTML](nepali_layout_evidence/exporter-3d343aab.png) |
| Setup image `f98449a1` | [before](nepali_layout_evidence/html-f98449a1-before.png) | [after](nepali_layout_evidence/html-f98449a1-after.png) | [HTML](nepali_layout_evidence/exporter-f98449a1.png) |
| Day02 image `audit-teach_opencv_pixel_pipeline` | [before](nepali_layout_evidence/html-audit-teach_opencv_pixel_pipeline-before.png) | [after](nepali_layout_evidence/html-audit-teach_opencv_pixel_pipeline-after.png) | [HTML](nepali_layout_evidence/exporter-audit-teach_opencv_pixel_pipeline.png) |
| Day05 image `fig-teach_threshold_freeze` | [before](nepali_layout_evidence/html-fig-teach_threshold_freeze-before.png) | [after](nepali_layout_evidence/html-fig-teach_threshold_freeze-after.png) | [HTML](nepali_layout_evidence/exporter-fig-teach_threshold_freeze.png) |

All six after-notebook views and six exporter HTML views were visually checked: the Nepali heading translation does not create an extra notebook subsection; each cited image has the correct three-language captions and nearby Nepali notice/question. The exporter shows one corresponding semantic heading. No missing-glyph boxes were observed in these samples.

## Final PDF page-by-page visual notes

**Actually visually inspected: 40 individual final PDF pages**, listed below, rendered at scale 1.5. This is not a full human visual audit of the 999 pages. No missing-glyph boxes or clipped Devanagari marks were observed in these samples. [The machine-readable sample index](nepali_layout_evidence/visual-page-selections.json) records the selection reasons.

| PDF | Page / raster reference | Observation, fix or retained limitation |
|---|---|---|
| Setup | [1](nepali_layout_evidence/pdf-Setup-p001.png) | Cover: Japanese/English/Nepali titles fit; no visible tofu. |
| Setup | [3](nepali_layout_evidence/pdf-Setup-p003.png) | TOC: wrapped trilingual entries retain a separate, aligned page-number column. |
| Setup | [4](nepali_layout_evidence/pdf-Setup-p004.png) | Last TOC page: final labels/digits remain within the page. |
| Setup | [7](nepali_layout_evidence/pdf-Setup-p007.png) | `79328757`: one corresponding three-language heading, then original body tables. Retained minor issue: the Nepali table header sits at the foot of this page, with its rows on p.8. |
| Setup | [8](nepali_layout_evidence/pdf-Setup-p008.png) | Table continuation and Nepali CMD-versus-Python explanation are readable. The narrow first column wraps “Markdown”; no text is clipped. |
| Setup | [10](nepali_layout_evidence/pdf-Setup-p010.png) | `f98449a1`: original Jupyter figure, JP/EN/NE captions and Nepali notice/question share the landscape page; labels remain readable after fitting. |
| Installation | [1](nepali_layout_evidence/pdf-Installation_Guide-p001.png) | Cover: Devanagari title and body fit. |
| Installation | [3](nepali_layout_evidence/pdf-Installation_Guide-p003.png) | TOC: long troubleshooting headings and page digits align. Source wrapper/title entries are preserved. |
| Installation | [4](nepali_layout_evidence/pdf-Installation_Guide-p004.png) | Last TOC page is Japanese/English-only, as its source labels are; no glyph-rendering fault. |
| Installation | [6](nepali_layout_evidence/pdf-Installation_Guide-p006.png) | Nepali ZIP/OneDrive/quoted-path and Python 3.11 instructions are present; literal CMD commands remain legible. |
| Installation | [7](nepali_layout_evidence/pdf-Installation_Guide-p007.png) | Nepali `.venv`/`.venv-anomalib` commands, direct-interpreter recovery and activation warnings fit without clipping. |
| Installation | [8](nepali_layout_evidence/pdf-Installation_Guide-p008.png) | Both kernel registration commands and Nepali asset-generation warnings are visible. Wrapped command continuations are distinguished; no command was executed during this review. |
| Installation | [9](nepali_layout_evidence/pdf-Installation_Guide-p009.png) | Nepali photo/model preloading, offline checks and two-environment verification commands are legible; license/output-location distinctions remain present. |
| Installation | [10](nepali_layout_evidence/pdf-Installation_Guide-p010.png) | Nepali Jupyter launch/kernel choices, launcher limitations, preflight checklist and report path remain readable. |
| Installation | [13](nepali_layout_evidence/pdf-Installation_Guide-p013.png) | Nepali environment diagnostics and activation-failure recovery include both explicit interpreter paths; no clipped code block. |
| Day02 | [1](nepali_layout_evidence/pdf-Day02_explanation-p001.png) | Cover: trilingual titles and Devanagari marks fit. |
| Day02 | [3](nepali_layout_evidence/pdf-Day02_explanation-p003.png) | First TOC page: wrapped long entries and digits remain separated. |
| Day02 | [5](nepali_layout_evidence/pdf-Day02_explanation-p005.png) | True last TOC page: final notebook entries and three-digit page numbers fit. The optional-photographs heading already embeds English in its original Japanese heading; that protected wording remains within one grouped entry, not a second TOC entry. |
| Day02 | [72](nepali_layout_evidence/pdf-Day02_explanation-p072.png) | `e15c580c`: one JP/EN/NE colour-order heading above preserved Japanese/English explanations and code examples. |
| Day02 | [73](nepali_layout_evidence/pdf-Day02_explanation-p073.png) | Nepali colour-order explanation, conjuncts and inline code are readable. The next table continues onto p.74. |
| Day02 | [74](nepali_layout_evidence/pdf-Day02_explanation-p074.png) | JP/EN/NE table cells and code values fit. Retained general table-pagination limitation: continuation pages do not repeat every table header. |
| Day02 | [76](nepali_layout_evidence/pdf-Day02_explanation-p076.png) | Existing pixel-pipeline SVG fallback, all captions and Nepali notice/question share the page. No picture or threshold value was changed. |
| Day04 | [1](nepali_layout_evidence/pdf-Day04_explanation-p001.png) | Cover: no visible missing glyphs. |
| Day04 | [3](nepali_layout_evidence/pdf-Day04_explanation-p003.png) | TOC: long lesson labels and digits are aligned. |
| Day04 | [5](nepali_layout_evidence/pdf-Day04_explanation-p005.png) | Last TOC page: final evaluation entries/digits fit. |
| Day04 | [7](nepali_layout_evidence/pdf-Day04_explanation-p007.png) | Nepali objectives, notebook metadata and deliverable tables are readable; long words stay inside cells. |
| Day04 | [15](nepali_layout_evidence/pdf-Day04_explanation-p015.png) | Label-format code blocks and corresponding Nepali explanation retain all five values and warnings; no clipped code. |
| Day04 | [39](nepali_layout_evidence/pdf-Day04_explanation-p039.png) | Existing training-update diagram is larger than the interim 80 mm version; JP/EN/NE captions and complete Nepali question remain together. |
| Day05 | [1](nepali_layout_evidence/pdf-Day05_explanation-p001.png) | Cover: long Nepali title fits. |
| Day05 | [3](nepali_layout_evidence/pdf-Day05_explanation-p003.png) | TOC: long PatchCore labels wrap without colliding with digits. |
| Day05 | [5](nepali_layout_evidence/pdf-Day05_explanation-p005.png) | Last TOC page: archive/provenance section labels remain; automated image-byte gating separately confirms archived TEST figures are absent from student-facing output. |
| Day05 | [73](nepali_layout_evidence/pdf-Day05_explanation-p073.png) | Existing calibration/freeze figure, three captions and Nepali notice/question share the page. Retained minor formatting issue: the wrapped final question clause is an adjacent paragraph rather than an indented bullet continuation; no words are lost or moved away from the image. |
| Day05 | [74](nepali_layout_evidence/pdf-Day05_explanation-p074.png) | `3d343aab`: one grouped JP/EN/NE freeze/test heading, with the original Japanese body following. |
| Day05 | [75](nepali_layout_evidence/pdf-Day05_explanation-p075.png) | Original English and Nepali freeze instructions and saved-example blocks continue legibly; examples/protocol are unchanged. |
| Week1 | [1](nepali_layout_evidence/pdf-Week1_explanation-p001.png) | Combined-volume cover: no visible clipping/tofu. |
| Week1 | [3](nepali_layout_evidence/pdf-Week1_explanation-p003.png) | TOC opening: long day/notebook labels retain aligned digits. |
| Week1 | [15](nepali_layout_evidence/pdf-Week1_explanation-p015.png) | Actual last TOC page: three-digit page numbers, wrapped labels and final entries fit. |
| Week1 | [176](nepali_layout_evidence/pdf-Week1_explanation-p176.png) | Pixel-pipeline image/caption/notice/question grouping also holds in the combined volume. |
| Week1 | [430](nepali_layout_evidence/pdf-Week1_explanation-p430.png) | Freeze/test semantic heading remains grouped in the combined volume. |
| Week1 | [431](nepali_layout_evidence/pdf-Week1_explanation-p431.png) | Continuation text and saved-example blocks remain readable; no model was run to produce them. |

## Preservation and remaining limitations

- [Preservation evidence](nepali_layout_evidence/preservation.json) records the HEAD, all notebook/cell counts, the protected-file count and original bilingual PDF SHA256 values.
- All 16 notebook JSON objects match the original after stripping only Nepali regions. This includes complete code cells, IDs, comments, outputs, execution counts, metadata, exercise templates, role banners, guards and protocol logic.
- All 513 snapshotted protected file hashes match, including original PNG/SVG/reference images, models, dataset/results files, launcher, bilingual exporter and the six original `*_ja_en.pdf` files.
- The five requested learner documents match their original Japanese/English text after stripping Nepali regions.
- A native Nepali reviewer remains the final authority on idiom, teaching clarity and glossary alternatives.
- No fresh beginner installation, pip installation, external download or model/photo preloading was executed. Static Nepali-only branch coverage and command parity do **not** substitute for a fresh novice setup trial; that practical sign-off remains outstanding under the no-install/no-model-execution constraints.
- Image-generation tests were excluded by explicit user choice; no claim is made that those generators were retested.
- Minor retained layout limitations are documented against the actual pages above: table-header/continuation pagination, a narrow table column and one wrapped question clause. Original bilingual heading wording can also repeat English inside a single grouped label; it was not silently rewritten.
- Automated page scans and the explicitly enumerated raster samples are not a full human visual audit of every distributed page.
