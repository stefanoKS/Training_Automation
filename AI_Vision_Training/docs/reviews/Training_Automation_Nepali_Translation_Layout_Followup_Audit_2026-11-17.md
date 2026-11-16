# Training_Automation — Nepali Translation and Trilingual Layout Follow-up Audit

**Reviewed repository:** `https://github.com/stefanoKS/Training_Automation`  
**Commit:** `8857204b2d9d0e34a5befbad73e00da98ff5fcd7` (2026-11-16 20:28:56 UTC / 2026-11-17 JST)  
**Scope:** 16 Jupyter notebooks, Nepali catalog/coverage scripts, learner documentation, trilingual PDF exporter and tests.  
**Method:** Live GitHub source inspection, systematic scan of the 16 notebook JSON files, selected JP/EN/NE semantic spot checks, and reading the repository's own implementation/validation log. **No GitHub changes were made. The committed PDFs could not be independently downloaded and rasterized in this environment**, so page-level rendering claims remain project-reported.

## Executive judgment

**Translation coverage: good. Content is broadly usable. Layout: targeted corrections required before final PDF sign-off.**

The implementation has a strong architecture: Nepali sidecar catalogs, idempotent injection, preserved code and cell metadata, a separate Chromium PDF exporter, a terminology guide, and regression tests. The existing figures were reused unchanged. However, the choice to place Nepali headings immediately after the first heading and Nepali explanations at the end of the original Markdown cells introduces reproducible layout/reading-order problems, and the PDF exporter does not fully correct them.

### Positive findings directly supported by the repo

- 16 notebooks contain Nepali translation regions. The repository log reports **653 translated of 800 Markdown cells**, with **147 intentionally exempt**. An independent source inspection showed **146 divider/separator cells and one exercise placeholder** among untranslated Markdown cells; no ordinary explanatory Markdown cell was left untranslated.
- 12 learner-facing text documents contain Nepali regions, including `START_HERE.md`, `README.md`, `COURSE_SYLLABUS.md`, `docs/troubleshooting/installation.md`, version notes and five report templates.
- All **10 trilingual PDF artifacts** exist in the repository, including five day-by-day PDFs, Week1, Setup, Installation Guide, Repository Guide, and Course Syllabus.
- Sampling included Day 2 BGR/RGB explanation, Day 3 confidence versus correctness, Day 4 object-level FP/FN and Day 5 calibration/TEST freeze. Their Nepali wording preserves the essential rules and illustrative quantities. This is a **spot check**, not an exhaustive native-language editorial review.
- The repository implementation log **reports 375 passing tests**, no zero-translation coverage, 1,035 pages of new trilingual PDFs, and 1,714 rendered pages with zero blank/overflow flags. This audit did **not** rerun those tests or render those PDFs.
- Reported original code cells, outputs, cell IDs, and the existing Japanese/English PDFs were preserved.

## Findings, priority, evidence, and recommended fix

### L01 — P1 — JP/NE and EN headings split inside 222 candidate cells

**Evidence (source inspected):** The notebook injection strategy uses `<!-- ne:begin after-heading -->` to add a Nepali Markdown heading immediately after the leading Japanese heading. Some existing cells put the English heading after the entire Japanese explanation. A source scan found **641 `after-heading` cells**, with **222 candidates** containing a later English heading after the inserted Nepali heading. Examples were manually checked:

- `notebooks/00_Setup/00_Environment_Setup.ipynb`, cell `79328757` — `このノートブックの使い方` / `यो नोटबुक कसरी प्रयोग गर्ने` appears before the Japanese body; `How to use this notebook` occurs later, before the English body.
- `notebooks/Day02_Python_OpenCV/Day02_03_OpenCV_Image_Processing.ipynb`, cell `e15c580c` — OpenCV's BGR/RGB lesson has the same ordering.
- `notebooks/Day05_PatchCore/Day05_03_YOLO_vs_PatchCore.ipynb`, cell `3d343aab` — freeze/TEST subsection has a Japanese heading, then Nepali heading, later English heading.

**PDF impact:** `assets/scripts/export_trilingual_pdf.py::markdown_cell_html` merges only *adjacent* same-level headings. Because an English heading can occur after substantive paragraphs, it is processed independently. This yields an English-only heading, possibly with an empty Japanese span, and an additional TOC entry, rather than one JP/EN/NE heading. In Jupyter, the reading hierarchy also looks inconsistent.

**Fix:** Avoid broad moving/retranslation of the protected Japanese/English text. Add deliberate heading-pair metadata or a cell-local semantic grouping pass in the *trilingual exporter* that recognizes the same JP/EN/NE concept even when the headings are split by original paragraph layout. Emit **one trilingual PDF heading / TOC entry**, suppressing only the duplicate heading rendering, never the English explanatory paragraph. For the notebook UI, normalize *only Nepali region placement / heading level* where necessary so a new Nepali heading does not artificially subdivide Japanese and English content. Provide before/after demonstrations on the cited cells. Do not blindly merge two genuinely distinct section headings in one cell.

**Acceptance:** no duplicate or blank-language PDF heading for the 222 candidate cases; TOC has each semantic section once; preserved JA/EN prose and all original code.

### L02 — P1 — Nepali figure captions and teaching questions are separated from their figures

**Evidence (source inspected):** Of **85 Markdown cells containing static image references**, **84** have Nepali image-related explanation/caption in a trailing `<!-- ne:begin end -->` region instead of immediately after the image. The exporter collects captions only from the first **three immediately subsequent lines** beginning `図`, `Figure`, `चित्र`, or `चित्रमा`.

Confirmed examples:

- Setup notebook, cell `f98449a1`: `teach_setup_jupyter_ui.png`, JP/EN caption directly under figure, Nepali caption and question after all other paragraphs.
- Day 2 OpenCV, cell `audit-teach_opencv_pixel_pipeline`: `teach_opencv_pixel_pipeline.svg`; Nepali `चित्र:` is stored at cell end.
- Day 5 YOLO/PatchCore, cell `fig-teach_threshold_freeze`: `teach_threshold_freeze.png`; Nepali caption at the end.

**Impact:** a beginner who reads Nepali may need to scroll away from the figure to understand it; the PDF's image+caption block does **not** automatically include the Nepali caption.

**Fix:** Extend catalog anchors (for example `after-image` or a safe, stable anchor by image path) or implement an explicit PDF semantic extraction of the corresponding Nepali `चित्र:` caption. Place JP, EN and NE captions immediately next to the same image, followed by appropriately aligned `What to notice / ध्यान दिनुपर्ने कुरा` and questions. Handle multiple images and multiple captions in a cell; do not treat every Nepali paragraph as a caption. No image regeneration or editing is authorized.

**Acceptance:** spot-check the cited figures and all 85 image-bearing cells for correctly matched captions; no missing or duplicated captions, reference evidence and TEST-gating intact.

### L03 — P2 — Learner documents are Nepali *section summaries*, not complete paragraph equivalents

**Evidence:** The localization implementation log explicitly states that `START_HERE.md`, `README.md`, `COURSE_SYLLABUS.md` and `docs/troubleshooting/installation.md` are translated *by section*, often as a summary with a translated table. This differs from the near cell-for-cell notebook translation.

**Assessment:** The Nepali `START_HERE.md` excerpts inspected contain actual reproducible Windows CMD commands and proper preparation sequence; this is good. The source makes no guarantee that **all** important exceptional cases from the JA/EN instructions also appear in Nepali.

**Fix:** Perform a task-by-task parity audit of the installation and navigation paths. Ensure Nepali-only readers can follow download/ZIP vs Git, Windows quoted paths, `.venv` and `.venv-anomalib`, kernel selection, network preloading, offline checks, Windows CMD syntax, fallback executable paths, troubleshooting, and report submission. Do not translate command tokens or invent new shell commands. Original full paragraphs need not be duplicated verbatim, but **every actionable step, warning and branch must be present**.

**Acceptance:** a complete Nepali-only setup walkthrough (preferably a novice dry run) with the same commands and checkpoints as JA/EN.

### L04 — P2 — Layout/typeface verification is machine- and size-dependent

**Evidence:** The new Chromium exporter uses the OS font stack `Nirmala UI / Noto Sans Devanagari / Mangal`, the CSS switch `font-feature-settings: "abvm" 0`, and fixed Nepali sizes (mostly multiples of 1.5 pt) to maintain searchable PDF text. The implementation log reports acceptable results on the author's environment.

**Risk, not a confirmed rendered defect:** a different Windows machine, missing fallback fonts, future text/caption changes or new CSS may introduce missing conjunct marks, clipping or unsplittable/awkward lines. Existing `test_nepali_localization.py` checks coverage and PDF presence/text extraction, but not one-to-one heading grouping, figure-adjacent Nepali captions, or human legibility.

**Fix:** Fail clearly when a suitable Devanagari font is unavailable; verify text and appearance on the actual deployment machine. For each of Setup, Installation, Day02, Day04, Day05 and Week1, render a documented page sample (cover, TOC, long tables, figures, code, Devanagari combinations, mixed JP/EN/NE), visually inspect and keep reproducible screenshots. Keep the PDF export separate from model/assets generation.

### L05 — P3 — Terminology and script conventions need a final Nepalese editorial pass

The implementation log records variations such as `निर्देशाङ्क` vs `निर्देशांक` and `सह्यता` vs `सहनशीलता`. These are primarily consistency concerns, not proven conceptual mistakes. A Nepali language reviewer should check the glossary, compound forms, natural instructions, and technical terms for factory staff. Source spot checks did **not** uncover a clear reversal of the major Day 2–5 technical principles. Do not claim 100% translation correctness based on automated tests.

### L06 — P3 — PDF exporter documentation naming mismatch

The header of `assets/scripts/export_trilingual_pdf.py` says `Setup_explanation_ja_en_ne.pdf`; the implemented `DOC_JOBS` naming and committed artifact use `Setup_ja_en_ne.pdf`. Align documentation to the actual filename. No need to rename a shipped PDF.

## Why existing tests missed the layout problems

`assets/tests/test_nepali_localization.py` verifies translation coverage, forbidden Hindi/placeholder tokens, idempotency, original content preservation, PDFs existing, and searchable Devanagari. It does **not** verify that the three language headings form one conceptual heading, that the TOC contains no duplicates, or that the Nepali figure caption appears within the same visual figure block. Page-wide "no overflow" checks are insufficient to prove conceptual alignment.

## Minimal recommended Codex implementation

1. Correct **L01** in the PDF semantic heading parser, plus targeted Jupyter anchor placement if needed.
2. Correct **L02** in figure-caption association / Nepali injection anchors without touching any PNG/SVG.
3. Add tests for both issues, with fixtures from Setup, Day02 and Day05 and checks for TOC uniqueness and caption adjacency.
4. Check **L03** actionable parity and report only true Nepali omissions. Preserve all CMD commands.
5. Require sample rendered screenshots in the implementation log. Keep real model/test artifacts and old JA/EN PDFs untouched.
6. Optional small L05/L06 consistency fixes.

## Final verdict

**The three-language course is usable, and the translations are a strong foundation, but the trilingual visual hierarchy is not yet ready for final sign-off.** Fix the heading and caption placements, validate key installation steps, and inspect representative PDF pages. Do not redo the original diagrams, training, or entire translation.

**Limit of this audit:** GitHub returned notebook, Markdown and Python sources and the reported test log, but direct binary PDF download/rasterization was unavailable in this environment. Claims about the exact finished page appearance are therefore conditional on independent rendering; the documented heading and caption failures are visible from source logic alone.
