# Training_Automation — Day 4 / Day 5 teaching and localization follow-up audit

**Repository:** https://github.com/stefanoKS/Training_Automation  
**Source reviewed:** `main` at `83423d81573098a5653f5415ae7c6a17fbf9d6e0`  
**Coverage:** Six Day 4 and Day 5 Jupyter notebooks, the Romanized Nepali migration surface (16 notebook catalogs + 12 document catalogs), trilingual PDF exporter and layout tests.  
**Method:** Live GitHub source inspection, selected JP/EN/Nepali text checks, code/lesson consistency and saved PDF-page screenshot inspection. Not an independent full notebook/model execution or 999-page human visual inspection.

## Summary judgment

**Most explanations are sound.** Keep the proven pedagogy, images, synthetic-versus-measured distinctions, comparison methodology and current preservation tests. Make targeted improvements in holdout discipline, deterministic failure checks and instructional precision. Then implement **Romanized Nepali (Nepali written in Latin/Roman letters)** globally, NOT English replacement and NOT mere unreviewed mechanical transliteration.

## Confirmed findings

### P1-01 — Day 5 final TEST is scored and saved before freeze

- `notebooks/Day05_PatchCore/Day05_02_PatchCore_Training.ipynb`, cell `82f543da` runs `engine.predict(...)` for BOTH `val_dataloader()` and `test_dataloader()`; cell `1c4cd018` saves normal/abnormal truths, test scores and predicted labels into `submissions/day05/patchcore_predictions.json` and prints test partition class counts.
- Only afterward, `notebooks/Day05_PatchCore/Day05_03_YOLO_vs_PatchCore.ipynb`, cell `clarity-freeze-record`, records the freeze declaration and `TEST_ALREADY_SEEN` state. Its cell `cccf0ff7` already displays test normal/abnormal counts.
- **Precise interpretation:** Precomputation is not necessarily statistical leakage if values are genuinely unseen and never used for selection, but the learner-accessible artifact and displayed test labels conflict with the stronger lesson 'test is untouched until freeze'. The output files also make an unintentional peek easy.
- **Fix:** Prefer a real two-stage workflow: compute/store calibration predictions only; freeze exact model/weight/preprocessor/memory/postprocessor/score convention/thresholds; then score TEST once and build comparison. Because Day 4 YOLO and Day 5 anomalib run in separate virtual environments, design an explicit cross-environment handoff with checkpoints/instructions. Do not silently break the existing launcher. If strict deferment cannot be automated, mark earlier test predictions and any test-labelled score as *precomputed holdout* and force `assessment_role='illustrative_reused_data'` unless defensibly proven untouched; never claim formal final assessment. Avoid printing TEST class counts before freeze in strict flow.

### P1-02 — Day 4 final-test evaluation too easy to execute prematurely

- `notebooks/Day04_YOLO_Training/Day04_03_YOLO_Evaluation.ipynb`, cell `612e7d6a` warns the learner to freeze before TEST, but immediately succeeding code cell `0865c09d` unconditionally runs `model.val(..., split="test", ...)` when the student executes it. Later cells and exercises encourage changes and exploration.
- **Fix:** Add an explicit, novice-friendly gate (recorded freeze + decision warning + strict/not-strict result labeling), or reorder the test section behind final calibration, while keeping the deliberate teaching example available. Do not pretend a boolean typed by a student proves test was unseen. Reuse after test must be labelled exploratory/illustrative. If model training occurs again after examining TEST, its result needs a fresh holdout for independent assessment.

### P2-03 — Day 5 comparison silently loses duplicate/incomplete images

- `Day05_03_YOLO_vs_PatchCore.ipynb`, cell `d26eb085` reports missing YOLO/PatchCore predictions but proceeds on `shared_images`; cell `cccf0ff7` calls `.drop_duplicates("image")` (keeps first and masks invalid input) then `inner` joins. It checks truth consistency but does not independently reject duplicate IDs or partition mismatches before use.
- **Fix:** For a formal comparison, require exactly one row per ID per method, complete manifest coverage for calibration/test, matching partition + ground truth, and no overlap across splits. Raise clear bilingual/romanized-Nepali error on mismatch. For deliberate partial exploration, allow `ALLOW_PARTIAL_COMPARISON=True` in an explicitly *non-final* branch and report exclusion by partition, class and method. Never relabel a partial-case comparison as final.

### P2-04 — Day 4 duplicate demo leaves training file on interruption

- `Day04_01_YOLO_Dataset_Annotation.ipynb`, cell `aa01b7fd` copies a test image to `images/train/leak_test.png`, checks hashes, then unlinks it. An interruption/exception between copy and unlink leaves altered training data, contaminating later exercises.
- `ef0229c6` prints `len(seen)` as 'images checked' but `seen` is a dictionary indexed by content hash; after duplication this is the number of **unique hashes**, not images scanned.
- **Fix:** Use `try/finally` and avoid overwriting an existing target, verify cleanup, optionally use a temporary isolated fixture rather than live course data, and distinguish `files_scanned`, `unique_hashes`, `duplicate_pairs`. Make rerunning after an interrupted exercise safe.

### P2-05 — Tighten technical wording with minimal edits

- `Day04_02_YOLO_Training.ipynb`, `clarity-batch-interpret`: 8 minibatches per epoch × 15 epochs = 120 **loader iterations**, not '120 full reads of the dataset'. Japanese/English already mostly distinguish it, while Nepali says 'डेटा 120 पटक पढाइ' which is prone to misreading. Make all three versions precise.
- `Day04_02`, `16c0469f`: 'loss goes down as learning progresses' is a useful beginner heuristic, not guaranteed monotonic nor proof of generalization; ensure follow-up interpretation emphasizes validation and output images. `388c5d1c` accurately says training-loss decrease alone is not proof.
- `Day04_02`, `388c5d1c`: describe YOLO26 `l1_loss` carefully as L1 regression on **normalized box distances**, not a generic unqualified mean of raw pixel coordinate errors. Ultralytics official configuration reference describes the DFL-free YOLO26 replacement; verify against pinned 8.4.211 rather than today's latest package. The `dfl_loss`/`l1_loss` distinction is otherwise correctly recognized.
- `Day04_03_YOLO_Evaluation.ipynb`, `968ad99b`: 'raising a detection-confidence threshold cannot increase recall' should explicitly assume a fixed set of detections and fixed matching/IoU; avoid stating it as an unconditional property of arbitrary rerun postprocessing.
- `Day04_03`, `c479853d`: pedagogical 'AP is area under PR curve' is fine for beginners but the actual implementation uses interpolation and details; if revised, keep it brief and distinguish actual mAP50/mAP50-95 from image-level recall.
- `Day05_01_Anomaly_Detection_Concepts.ipynb`, `1f601e75`: the statement that compared anomaly scores are 0–1 is valid only under enabled, fitted postprocessing; retain its important caveat. Distinguish calibration-set threshold selection from postprocessor score normalization and from a true probability.
- `Day05_02`, `c452bff7`: `engine.test(model, dataloaders=datamodule.val_dataloader())` is a library method evaluated **on CALIBRATION**, not held-out TEST. The current explanation correctly states this. Preserve it.

### P2-06 — Edge-case handling of calibration threshold candidates

- `Day05_03`, cell `935ef5b9`, chooses YOLO candidates from inference-confidence floor to about 0.99 and PatchCore candidates from 0.00 through 1.00, with strict false-reject constraint. The search grid cannot always express an all-OK classifier if a normal score equals 1.00 (using `>=` at exactly 1.00) or exceeds the last YOLO candidate; it may assert no feasible threshold even when a deliberately over-range threshold could meet the constraint with zero recall. **This is a demonstrable edge-case risk, not evidence that the supplied classroom data fails.**
- Test with toy arrays containing ties/endpoints, zero positives, zero normals, all equal scores and a missing method. Decide and document whether 'no feasible candidate' is intentional or use an explicit boundary sentinel / safe fallback without pretending good detection.

### P3-07 — Current multilingual visual layout largely fixed

- The latest trilingual exporter groups paired headings, matches Nepali captions to exact images and reports rendered layout tests. Saved screenshot `docs/reviews/nepali_layout_evidence/pdf-Day04_explanation-p039.png` shows a wide diagram with JP/EN text and a nearby Nepali caption/question; `pdf-Day05_explanation-p073.png` similarly groups the calibration plot and text. The text is dense but readable in inspected samples.
- Do not broadly reorganize all lessons. When migrating to Latin letters, retain semantic JP→EN→Romanized Nepali order, captions grouped under each picture and one semantic heading per concept/TOC entry. Reinspect page breaks, fonts, table widths and copyable command lines.

## Romanized Nepali migration — global scope

**Meaning:** Same Nepali sentences written in Latin (Roman) letters, e.g. `Yo notebook kasari prayog garne?`, rather than Devanagari `यो नोटबुक कसरी प्रयोग गर्ने?`. It is not a new English translation, and a naive letter-by-letter transliteration is insufficient. Standardize readable everyday Nepali spelling with reviewer approval, and retain technical tokens such as `YOLO`, `PatchCore`, `train`, `val`, `test`, `image_AUROC`, `F1Score`, `.venv`, `python`, `cmd`, model paths and mathematical operators verbatim.

**Change all learner-facing Nepali**, not only Day 4/5: the **16 notebook sidecars and 12 documentation sidecars**, applied regions in notebooks and documents, cover/TOC/captions/visual notes, and the **10 trilingual PDFs**. Keep existing Day 1–3 Japanese/English and code unchanged, and do not regenerate any figure/image.

**Important implementation blocker:** Current code often assumes Nepali == Devanagari:

- `assets/scripts/apply_nepali_translations.py`: `parse_catalog()` rejects blocks without `DEVANAGARI_RE`; current conflict detection and heading anchors also use the script.
- `assets/scripts/apply_nepali_docs.py`: document catalog parser similarly requires Devanagari.
- `assets/scripts/check_nepali_coverage.py`: counts script characters and blocks.
- `assets/scripts/export_trilingual_pdf.py`: `script_class()`, `semantic_headings()`, notebook title extraction, caption CSS, `check_devanagari_font()`, PDF text checks and TOC rely on Devanagari detection. Latin-letter Nepali would be mislabeled as English, losing the correct PDF language grouping.
- `assets/tests/test_nepali_localization.py` and `test_trilingual_layout.py`: check for Devanagari text. Those tests must be **replaced with appropriate positive romanized-Nepali checks**, not simply disabled.

**Recommended architecture:** Keep ISO language `ne` and add explicit script tag `ne-Latn` in metadata/data markers rather than guessing from glyphs. Distinguish `en` and `ne-Latn` by provenance (sidecar block or explicit heading attributes), not regex on Latin letters. Use semantic `<span lang="ne-Latn" class="ne">` markup and reliable heading-pair/image anchors. Render with a legible Latin font without requiring Devanagari fonts. Retain a canonical transliteration style guide and reviewer-signoff checklist, and preserve the old Devanagari version in Git history; do not ship both scripts as though both are required if user asked for replacement.

**Source notes:** Official Anomalib v2.7.0 reference: https://anomalib.readthedocs.io/en/lib-v2.7.0/markdown/guides/reference/post_processing/index.html . Official Ultralytics YOLO26 config: https://docs.ultralytics.com/usage/cfg . Verify package-specific API behavior against pinned versions.

## Acceptance plan

1. 100% of six Day 4/5 notebooks reviewed; change only warranted scientific/pedagogical mistakes or unsafe learner workflows.
2. Holdout state and artifact provenance are consistent in text and code; no final result silently uses prematurely inspected TEST.
3. Strict paired comparison raises on duplicates, missing IDs, manifest misalignment or truth disagreement; optional incomplete exploration must clearly disclaim it.
4. Leakage demo always cleans up even on an exception; image-scanned count is correct.
5. All 16 notebooks and 12 documents receive **human-readable Romanized Nepali** via canonical sidecars; strip-regions preservation and idempotent regeneration pass.
6. PDF language identity uses explicit metadata; headings/TOC/images/figure captions and `lang=ne-Latn` work with all-Latin Nepali. No Devanagari-font requirement. Language coverage tests positively detect actual romanized prose rather than passing English duplicate placeholders.
7. Regenerate ten existing trilingual PDFs under their established names; DO NOT rewrite six Japanese/English original PDFs unless a separate approved Day4/5 Japanese/English educational fix necessitates rebuilding affected Day4/Day5/Week1 bilingual editions, in which case record all hashes and exact reasons.
8. Inspect actual rendered PDF samples (Day4/Day5/Week1 plus setup/install) and compare known figure placement and test-figure gating.
9. Test generation routines run in temporary directories so teaching assets are not overwritten. Jupyter structural tests + targeted numeric/holdout tests + full pytest; report deselections transparently. No fictitious 100% language correctness claim.
10. Produce a change log with each modified notebook cell ID, translation catalog, reference figure, PDF name and observed test output; no push unless authorized.
