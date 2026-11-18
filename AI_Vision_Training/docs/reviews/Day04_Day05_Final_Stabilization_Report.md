# Day 4・Day 5 最終安定化レポート / Final stabilization report — Day 4 and Day 5

Date: 2026-11-19
Course root: `AI_Vision_Training/`
Author: AI assistant (Copilot SDK in VS Code) on behalf of stefanoKS

This report separates **real execution evidence**, **source inspection**, **synthetic-but-real-code
tests**, and **prior implementation logs**. Where something was not executed, it says so.

---

## A. HEAD and baseline comparison

| Item | Value |
|---|---|
| Reviewed HEAD (in the request) | `16d20b1d4ce772104fd34ad66007583269312654` |
| HEAD when this work started | `16d20b1d4ce772104fd34ad66007583269312654` |
| Difference | none — the working tree was clean and no newer commit had to be absorbed |
| Branch | `main` (local; nothing pushed or merged) |
| Baseline test suite | `python -m pytest assets/tests -q` → **495 passed, 4 warnings, 465.83 s** |
| Baseline evaluator scripts | `apply_nepali_translations.py` 0 changes, `check_nepali_coverage.py --strict` exit 0, `validate_notebooks.py --execute none` 194 passed |

Toolchain on this machine (measured, not assumed):

| Environment | Python | torch | ultralytics | anomalib | lightning |
|---|---|---|---|---|---|
| base (`C:\Users\stefa\miniconda3`) | 3.11.4 | 2.0.1+cpu | 8.0.187 | 1.1.0dev (**no PostProcessor class**) | absent |
| `.venv` (course YOLO env) | 3.11.4 | **2.15.0** | **8.4.211** | absent | absent |
| pinned Anomalib env (`.venv-anomalib`) | — | — | — | **not installed** | — |

The pinned Day 5 runtime (`anomalib==2.7.0`, `lightning==2.6.6`) is **not available on this machine**.
See §N.

---

## B. Findings

### B1. Confirmed defects (fixed)

| # | Layer | Defect | Root cause |
|---|---|---|---|
| D1 | Day 4 / P1 | The pre-freeze shared-set step inferred on **all 52** images of `assets/anomaly_dataset/pvc_sheet/test/` and printed `frame.groupby("true_label")["yolo_max_conf"].agg(["count","min","max"])` over calibration **and** final-test images | the split existed only inside Day 5's `datamodule`, which runs later, so the Day 4 summary could not separate the halves |
| D2 | Day 4 / P1 | `submissions/day04/yolo_predictions_on_shared_set.json` contained a per-image score for **every** image, readable before any freeze | same root cause: the split did not exist yet, so nothing could be withheld |
| D3 | Day 5 / P1 | `comparison_is_final` was computed but never enforced: `clarity-freeze-record` and the result writer accepted a partial calibration comparison | the flag was informational only |
| D4 | Day 5 / P1 | `validate_sealed` accepted any of the two valid assessment roles without comparing it to the freeze record, and `clarity-archive-gate` rewrote `freeze_record["assessment_role"]` after a seal existed | a role was validated as a *value*, never as *the frozen experiment's role* |
| D5 | Day 5 / P2 | The experiment identity captured `postprocessor_state(model)` **before** calibration was scored, so the normalisation statistics and threshold that decide the scores were not part of the fingerprint | the manifest is written in Part 3, but the PostProcessor is fitted in Part 4 |
| D6 | Day 5 / P2 | `postprocessor_state` probed `adaptive_threshold`, which anomalib 2.x does not expose (it keeps `_image_threshold`); unfitted `image_min/max` are `NaN`, which is not valid JSON | attribute names were assumed, not checked against the library |
| D7 | Day 5 / P2 | The sealed JSON was published **before** the numeric maps, and the maps were moved without checking count or file-name collisions | publication order and map identity were untested |
| D8 | Day 5 / P2 | The kernel-restart guidance told learners to refit and continue as if it were the same experiment | refitting produces a different memory bank and therefore a different fingerprint |
| D9 | Docs | Day 5 navigation said "4 ステップ" and "3 つのファイル" after the workflow grew | stale instructions |
| D10 | PDF tooling | `export_trilingual_pdf.locate_headings` required the JA+EN+ne heading text to be contiguous; a long heading that crosses a page boundary has the running header/footer interleaved and the Day 5 booklet failed to build | the lookup assumed one uninterrupted string |

### B2. Already-fixed issues verified, not rewritten

| # | Item | Evidence |
|---|---|---|
| V1 | `normalise_image_id` accepts `test/good/a.png` and `good/a.png` | `test_image_ids_from_both_conventions_agree`; the prefix mismatch reported in the request is FIXED in the reviewed source |
| V2 | PatchCore is scored on calibration only, once | `test_day05_02_scores_the_test_partition_only_after_the_freeze` |
| V3 | Atomic JSON publication (`write_json_atomic`) | `test_case10_a_failed_write_publishes_nothing` |
| V4 | The old comparison is labelled `superseded`, never overwritten | `test_old_results_are_marked_superseded` |
| V5 | Day 4's `model.val(split="test")` (cell `0865c09d`) is a **different dataset** (`assets/yolo_dataset`) from the shared anomaly set | cell `612e7d6a` and the new Part 5 text now say so explicitly; no code change was needed |
| V6 | Seeded, recorded split with overlap and content-hash checks | `daed190f` kept its `assert not shared` and digest checks |

### B3. Optional improvements taken (small, justified by a defect above)

* The shared-set split is now **produced before any inference** and cross-checked by Day 5 (D1/D2).
* Application date of the frozen model identity now includes the **post-calibration** PostProcessor
  statistics (D5/D6).
* Maps are published first and the JSON last as the completion marker, with a one-to-one check (D7).

### B4. Unverified concerns

* The pinned `anomalib==2.7.0` was never executed here. The corrected PostProcessor attribute names
  were checked against the public `anomalib` 2.0.0 source, not against 2.7.0 on this machine.
* No native Nepali speaker has reviewed the wording.

---

## C. Affected notebook cells (exact IDs)

| Notebook | Cell | Change |
|---|---|---|
| `Day04_03_YOLO_Evaluation.ipynb` | `29056356` (markdown) | Part 5 rewritten: split-first, calibration-only, sealed test |
| | `f7f5833b` (code) | builds `shared_set_split.json` **before** inference, scores calibration only |
| | `552d3581` (code) | exports schema 3 with `scored_partitions: ["calibration"]`, `test_scored: false`, split digest; prints calibration-only statistics |
| | `shared-sealed-test-intro` (markdown, **new**) | explains the post-freeze step |
| | `shared-sealed-test` (code, **new**) | verifies the freeze record and split, scores the 26 test images once, seals them |
| | `9b6959aa` (markdown) | completion checklist updated |
| `Day05_02_PatchCore_Training.ipynb` | `daed190f` (code) | verifies the Day 4 split against the live `datamodule`; records `shared_split` (verified, digest) in the manifest; schema 2 → 3 |
| | `1c4cd018` (code) | asserts the fitted model is unchanged by calibration scoring; captures the **post-calibration** PostProcessor state; writes `patchcore_calibrated_state.json`; schema 2 → 3 |
| | `clarity-sealed-test-scoring` (code) | rebuilds the expected identity from the current fitted state + PostProcessor; passes the frozen assessment role; publishes maps first (count and name checks) and the JSON last |
| | `clarity-sealed-test` (markdown) | six-step protocol (JA/EN/ne) |
| `Day05_03_YOLO_vs_PatchCore.ipynb` | `39ee7a27` (code) | per-file schema 3; requires `shared_split.verified`; rejects any non-calibration row or mismatched split digest |
| | `be4aa133` (markdown) | "three calibration files" |
| | `clarity-freeze-record` (code) | **blocks** when `comparison_is_final` is false; reads the post-calibration record; checks fitted fingerprint and dataset/model consistency |
| | `clarity-sealed-test-read` (markdown) | both seals, provenance, six steps |
| | `clarity-load-sealed-test` (code) | validates **both** seals (identity, split, thresholds, role, coverage, duplicates, types); requires identical test image sets and agreeing ground truth |
| | `9747ac10` (code) | blocks on a partial comparison; writes `assessment_role` and `assessment_is_final` into JSON **and** CSV; atomic write |
| | `clarity-archive-gate` (code) | never rewrites a sealed role; records a downgrade (with reason) only before a seal exists |

---

## D. Root cause per confirmed defect

* **D1/D2** — the 52 comparison images are partitioned *inside* `anomalib.Folder`
  (`val_split_mode="from_test"`, `val_split_ratio=0.5`, `seed=2026`), which only exists in the Day 5
  kernel. Day 4 therefore had no notion of "calibration" and exported everything.
* **D3** — `comparison_is_final` was assigned in `d26eb085` and read nowhere.
* **D4** — `validate_sealed` checked `role in {…}`, and the archive gate mutated the record afterwards.
* **D5** — `postprocessor_state(model)` was called in Part 3; `engine.test()` / `engine.predict()`
  fit the PostProcessor in Part 4.
* **D6** — `POSTPROCESSOR_KEYS` was a flat tuple of assumed names; `_scalar` passed `NaN` through.
* **D7** — publication was `write_json_atomic → move maps`, with no count/name check.
* **D8** — the guidance conflated "re-run the cells" with "same experiment".
* **D10** — `locate_headings` used `body.find(ja+en+ne)`; Chromium extracts the running header between
  the second and third line of a heading that crosses a page break.

---

## E. Proposed fix versus implemented fix

| # | Proposed | Implemented |
|---|---|---|
| D1/D2 | Option A "generate the deterministic shared split manifest before any shared-set inference and export calibration only" | new helper `assets/helpers/shared_set_split.py` reproduces anomalib's rule with `torch.randperm`; Day 4 writes `submissions/day04/shared_set_split.json` first, scores **calibration only**, and Day 5 fails loudly if the installed anomalib disagrees. Chosen over Option B (two-stage only in Day 5) because it keeps the course order Day 4 → Day 5 and needs no new environment |
| D3 | Option A (block the freeze) | implemented; the message names the missing images, the reason and the cells to re-run |
| D4 | compare the expected role explicitly inside `validate_sealed` | `validate_sealed`/`validate_yolo_sealed` take `expected_role` (required) and fail on any mismatch, in either direction |
| D5/D6 | fingerprint the fitted PostProcessor | post-calibration state recorded and frozen; alias lookup (`adaptive_threshold` → `image_threshold` → `_image_threshold`); non-finite values recorded as `null` |
| D7 | JSON authoritative, maps best-effort; publish in a safe order | maps validated (one per image, unique names) and published first; JSON last; a failed map publish rolls back |
| D8 | honest recovery | checkpoint reload + fingerprint check; refit means a **new** experiment and `TEST_ALREADY_SEEN=True` |
| D10 | — | `locate_headings` searches one language at a time |

---

## F. Files modified

Modified:

```
AI_Vision_Training/COURSE_SYLLABUS.md
AI_Vision_Training/assets/helpers/experiment_identity.py
AI_Vision_Training/assets/i18n/ne/docs/COURSE_SYLLABUS.ne.md
AI_Vision_Training/assets/i18n/ne/notebooks/Day04_03_YOLO_Evaluation.ne.md
AI_Vision_Training/assets/i18n/ne/notebooks/Day05_02_PatchCore_Training.ne.md
AI_Vision_Training/assets/i18n/ne/notebooks/Day05_03_YOLO_vs_PatchCore.ne.md
AI_Vision_Training/assets/scripts/export_trilingual_pdf.py
AI_Vision_Training/assets/tests/test_clarity_review.py
AI_Vision_Training/assets/tests/test_experiment_identity.py
AI_Vision_Training/docs/instructor/day04_instructor_guide.md
AI_Vision_Training/docs/instructor/day05_instructor_guide.md
AI_Vision_Training/docs/pdf/README.md
AI_Vision_Training/notebooks/Day04_YOLO_Training/Day04_03_YOLO_Evaluation.ipynb
AI_Vision_Training/notebooks/Day05_PatchCore/Day05_02_PatchCore_Training.ipynb
AI_Vision_Training/notebooks/Day05_PatchCore/Day05_03_YOLO_vs_PatchCore.ipynb
AI_Vision_Training/docs/pdf/{Course_Syllabus,Day04_explanation_ja_en,Day04_explanation_ja_en_ne,
                             Day05_explanation_ja_en,Day05_explanation_ja_en_ne,
                             Week1_explanation_ja_en,Week1_explanation_ja_en_ne}.pdf
```

Added:

```
AI_Vision_Training/assets/helpers/shared_set_split.py
AI_Vision_Training/assets/tests/test_day04_day05_contracts.py
AI_Vision_Training/docs/reviews/Day04_Day05_Final_Stabilization_Report.md   (this report)
```

Untouched (verified by `git status`): Setup, Day 1–3 notebooks, Day 5 Notebook 01, every PNG/SVG, the
`assets/anomaly_dataset` and `assets/yolo_dataset` trees, `training_results/`, `results/`,
`start_training.cmd`, `requirements/*`.

---

## G. Tests actually run

```
python -m pytest assets/tests -q
```

| Moment | Result |
|---|---|
| Baseline (before any change) | **495 passed, 4 warnings, 465.83 s** |
| After the change | **509 passed, 0 failed, 4 warnings, 468.36 s** |

New test file `assets/tests/test_day04_day05_contracts.py` (9 tests) executes the **real notebook
cells** — only the model and the engine are duck-typed stand-ins:

| Test | What it proves |
|---|---|
| `test_the_shared_split_is_deterministic_and_label_aware` | identical output on repeat; counts 32 / 26 / 26; no overlaps |
| `test_the_archived_test_images_land_in_the_test_partition` | the archived run recorded `black_spot_0000` and `streak_0005` as TEST (see `docs/instructor/day05_after_freeze_archive.md`); the reproduced split agrees — independent corroboration that the rule matches anomalib |
| `test_the_prefreeze_export_holds_calibration_rows_only` | the model is never shown a test image before the freeze; the pre-freeze file holds calibration rows only |
| `test_end_to_end_from_the_split_to_the_final_comparison` | Day 4 split → Day 4 calibration export → Notebook 02 calibration producer → Notebook 03 pairing/thresholds/freeze → Day 4 seal → Notebook 02 seal → Notebook 03 pairing → final JSON/CSV; a second sealing run re-uses the seal instead of re-scoring; `TP+FP+FN+TN == n_images` |
| `test_relabelling_the_role_after_the_seal_is_rejected` | editing `assessment_role` after sealing fails with "assessment role differs" |
| `test_a_partial_calibration_cannot_be_frozen` | `comparison_is_final=False` blocks the freeze and writes nothing |
| `test_a_rejected_map_publish_leaves_no_seal_behind` | a map set that does not pair one-to-one with the images publishes nothing |
| `test_the_archive_gate_cannot_relabel_a_sealed_role` | the downgrade is recorded only before a seal; afterwards the record is untouched |
| `test_the_repository_holds_no_generated_comparison_artifacts` | no fabricated result ships in `submissions/` |

Added to `test_experiment_identity.py`: mismatched role, reused→untouched, missing role,
`validate_yolo_sealed` (happy path + wrong threshold), and anomalib-2.x PostProcessor attribute names
including `NaN` → `null`.

Existing assertions were not weakened. Two call sites of `validate_sealed` and the freeze fixture in
`test_clarity_review.py` were updated because the signature and the preconditions intentionally
changed (`expected_role` is now required; the freeze needs `comparison_is_final` and the
post-calibration record).

---

## H. Cross-notebook artifact compatibility

| Artifact | Producer | Consumer | Schema | Verified |
|---|---|---|---|---|
| `submissions/day04/shared_set_split.json` | Day04_03 `f7f5833b` | Day05_02 `daed190f` | 1 | integration test |
| `submissions/day04/yolo_predictions_on_shared_set.json` | Day04_03 `552d3581` | Day05_03 `39ee7a27` | **2 → 3** | integration test (calibration only, digest match) |
| `submissions/day04/yolo_predictions_sealed_test.json` | Day04_03 `shared-sealed-test` | Day05_03 `clarity-load-sealed-test` | 1 (new) | integration test |
| `submissions/day05/split_manifest.json` | Day05_02 `daed190f` | Day05_03 | **2 → 3** (`shared_split.verified`) | integration test |
| `submissions/day05/patchcore_predictions.json` | Day05_02 `1c4cd018` | Day05_03 | **2 → 3** | integration test |
| `submissions/day05/patchcore_calibrated_state.json` | Day05_02 `1c4cd018` | Day05_03 `clarity-freeze-record` | 1 (new) | integration test |
| `submissions/day05/comparison_freeze_record.json` | Day05_03 `clarity-freeze-record` | Day04_03 seal, Day05_02 seal | unchanged + `assessment_role` mandatory | integration test |
| `submissions/day05/patchcore_test_predictions.json` | Day05_02 `clarity-sealed-test-scoring` | Day05_03 | `SEALED_SCHEMA` = 3 | integration test |
| `submissions/day05/comparison_test_results.json/.csv` | Day05_03 `9747ac10` | learner | **2 → 3** (+`assessment_role`, `assessment_is_final`, CSV column) | integration test |

Stale files are rejected with a named reason (schema version), never reinterpreted. Older Day 4/5
artifacts from a previous course run are therefore **rejected**, not silently upgraded — the notebooks
tell the learner to re-run Day 4 Notebook 03 and Day 5 Notebook 02.

---

## I. Dataset-leakage verification

Traced order (source inspection + integration test):

1. `assets/anomaly_dataset/pvc_sheet/dataset_layout.json` fixes `seed = 2026`; the split is
   deterministic.
2. **Day 4** (`f7f5833b`) computes `{patchcore_train: 32, calibration: 26, test: 26}` with
   `torch.Generator().manual_seed(2026)` per label group and writes it **before** any `model.predict`.
3. Day 4 scores **only** the 26 calibration images. The integration test asserts that the set of paths
   passed to `model.predict` equals the calibration set exactly.
4. **Day 5 Notebook 02** builds the same split with `anomalib.Folder` and compares the three partitions;
   a mismatch stops the notebook with the differing file names.
5. Thresholds are chosen in Notebook 03 from `calibration_frame` only (`choose_threshold`).
6. Test scores do not exist until the freeze record exists; both seals are checked against the frozen
   identity before use.
7. `yolo_training_overlap` (content-hash comparison against `assets/yolo_dataset`) is unchanged, and
   the file-name overlap check between `patchcore_train` and the evaluation partitions still asserts.

Day 4's own `split="test"` evaluation (cell `0865c09d`) was reviewed: it uses
`assets/yolo_dataset`, a different dataset, is not used to choose any Day 5 threshold, and its result
is labelled with `TEST_ALREADY_SEEN` / `assessment_role`. Part 5 now states explicitly that the two
datasets must not be blended.

---

## J. Model-fingerprint verification

| Check | Result |
|---|---|
| Fingerprint stability and sensitivity (synthetic tensors) | PASS — `test_fitted_fingerprint_is_stable_and_changes_with_the_fitted_bytes` |
| Real |PyTorch| tensors through `fitted_state` | PASS — the integration test uses a real `torch.arange` buffer behind the same attributes |
| PostProcessor attribute names against the library | **corrected**: anomalib 2.0.0 `PostProcessor` exposes `enable_normalization`, `image_min`, `image_max`, `pixel_min`, `pixel_max` buffers and `_image_threshold`; it does **not** expose `adaptive_threshold` |
| PostProcessor state after calibration scoring | now captured (`patchcore_calibrated_state.json`) and frozen |
| Real PatchCore fit + fingerprint on the pinned runtime | **NOT RUN** — `anomalib==2.7.0` / `lightning` are not installed here (see §N) |

The fingerprint therefore covers: memory-bank and state-dict bytes, dataset partitions, seed, model
configuration, score convention, thresholds, and the fitted PostProcessor statistics. It does not
claim runtime verification against 2.7.0.

---

## K. Japanese / English / Romanized Nepali review

Scope: the six Day 4–5 notebooks and the two revised documents (syllabus, both instructor guides).

* The three changed/new Day 4 cells and the three revised Day 5 cells carry JA, EN and `ne-Latn`
  content; the Nepali lives in the sidecars and was applied with `apply_nepali_translations.py`
  (second run: **0 changes** → idempotent).
* `check_nepali_coverage.py --strict`: **656/803 markdown cells with Nepali (81.7 %), 147 exempt,
  0 missing, 334,018 Nepali characters; 1 149 Romanized and 0 Devanagari regions; 12/12 documents.**
* Terminology is unchanged except where the workflow needed it; the Nepali says `chha charan`
  (six steps) to match the new protocol.
* Every language states the same rule set: split before inference, calibration only before the freeze,
  one sealed scoring per method after it, never tune on test, a refit is a new experiment.
* The "Run All" wording now says the sealing cells **stop by design** (it never claims that Run All
  completes the workflow).
* **A native Nepali reviewer is still required.** No claim of linguistic certification is made here.

---

## L. PDFs regenerated and pages inspected

Rebuilt (only the booklets whose source text changed):

| File | Pages |
|---|---|
| `docs/pdf/Day04_explanation_ja_en_ne.pdf` | 88 → **90** |
| `docs/pdf/Day04_explanation_ja_en.pdf` | 68 → **70** |
| `docs/pdf/Day05_explanation_ja_en_ne.pdf` | 88 → **89** |
| `docs/pdf/Day05_explanation_ja_en.pdf` | 64 → **65** |
| `docs/pdf/Week1_explanation_ja_en_ne.pdf` | 455 → **458** |
| `docs/pdf/Week1_explanation_ja_en.pdf` | 338 → **340** |
| `docs/pdf/Course_Syllabus_ja_en_ne.pdf` | 20 → **21** |

`Day01`, `Day03`, `Day04` untouched booklets and `Setup`, `Installation_Guide`, `Repository_Guide`
were **not** rebuilt (no source change).

Pages rendered and inspected by eye:

| Booklet | Page | What was checked |
|---|---|---|
| `Day04_explanation_ja_en_ne.pdf` | 47 | training-loop / evaluation explanation still intact |
| | **81, 82** | the new Part 5: JA/EN/ne text, the two tables, the quotes; no clipping, tables intact |
| | 88 | completion checklist |
| `Day05_explanation_ja_en_ne.pdf` | **56, 57** | six-step table split across a page break, ASCII flow, "common situations" table, Nepali paragraphs |
| | **78** | sealed-prediction section (both seals, provenance) |
| | 80 | "Expected output" for the frozen comparison |
| `Day04_explanation_ja_en.pdf` | **64** | bilingual booklet: no Nepali, no `<!-- ne: -->` markers |
| `Day05_explanation_ja_en.pdf` | **43** | bilingual six-step section |
| `Week1_explanation_ja_en_ne.pdf` | **365** | the Day 4 shared-set section inside the week booklet |
| `Course_Syllabus_ja_en_ne.pdf` | **15** | Day 4/5 timetable rows and the six-step note |

No image file was regenerated or modified.

**Pre-existing PDF defect observed and left alone:** raw HTML anchors (`<a id="day5"></a>`) leak into
the syllabus text layer on pages 8, 10, 11, 13 and 15. The same leak exists in the previous
`Course_Syllabus_ja_en_ne.pdf` (checked against `HEAD`), so it is not caused by this work; fixing the
document exporter's anchor handling is outside the Day 4–5 scope.

---

## M. Acceptance gates

| Gate | Result | Evidence |
|---|---|---|
| 1. All confirmed Day 4 shared-test leaks fixed | **PASS** | B1 D1/D2; integration test asserts no test image reaches the model pre-freeze |
| 2. Threshold selection only accesses calibration | **PASS** | `935ef5b9` uses `calibration_frame`; test-set rows rejected in `39ee7a27` |
| 3. Day 4 / Day 5 file schemas compatible | **PASS** | §H; integration test |
| 4. No partial comparison labelled final | **PASS** | D3; `assessment_is_final` in JSON and the freeze gate |
| 5. Sealed identity and assessment roles agree | **PASS** | D4; three dedicated tests |
| 6. Old sealed results never silently reused | **PASS** | `validate_sealed` names the differing part; a re-run re-uses, never re-scores |
| 7. Final metrics use correctly aligned test IDs | **PASS** | join by normalised image ID; identical image sets enforced |
| 8. Fingerprint verified against the actual runtime | **CONDITIONAL** | source-level correction of the anomalib 2.x attributes; no 2.7.0 runtime here |
| 9. Failure scenarios preserve existing results | **PASS** | atomic JSON; map publish checks; previous seal untouched |
| 10. JA / EN / ne-Latn agree | **PASS (with caveat)** | §K; human Nepali review outstanding |
| 11. Affected PDFs rebuilt and inspected | **PASS (sampled)** | §L |
| 12. Regression tests pass | **PASS** | §G |
| 13. Unrelated notebooks, diagrams, datasets untouched | **PASS** | §F; `git status` |
| 14. Remaining limitations documented | **PASS** | §N |

---

## N. Remaining limitations

1. **No real Anomalib execution.** `anomalib==2.7.0` with `lightning` is not installed on this machine
   (the base environment has `anomalib 1.1.0dev`, which has no `PostProcessor` class). Day 5 was
   therefore **not** executed end-to-end with a real PatchCore fit. The end-to-end evidence in this
   report comes from executing the real notebook cells with a real `torch` buffer and duck-typed
   model/engine stand-ins. The first classroom run remains the first true integration test of the
   fingerprint against a real PatchCore.
2. **Split reproduction risk.** `shared_set_split.py` reproduces anomalib's `from_test` rule. Two
   independent signals support it (torch 2.0.1 and 2.15.0 produce the same digest; the archived TEST
   images `black_spot_0000` and `streak_0005` land in the reproduced TEST partition), and Day 5 aborts
   with the differing file names if the installed anomalib disagrees. A disagreement blocks the course
   rather than silently mixing partitions.
3. **Nepali not certified.** Machine-assisted transliteration plus hand-reviewed spellings; a Nepali
   speaker must read the five changed blocks before the class.
4. **Archived artifacts kept as-is.** `ref_confidence_counts.png` and the archived TEST panels were
   produced from the pre-change all-image file. They are labelled archived and were not regenerated.
5. **Maps are best-effort.** The JSON scores are authoritative; a failed map publish publishes no seal,
   but a map write that succeeds before a JSON write failure leaves inert maps behind.
6. **Pre-existing syllabus anchor leak** (§L).
7. **"Run All" stops by design.** The Day 4 and Day 5 notebooks are each opened twice; an automated
   full-notebook execution cannot complete them in one pass. `validate_notebooks.py --execute all`
   remains unsuitable for these two notebooks.

---

## O. Recommended final classroom workflow

Environment: steps 1, 4 in the **YOLO** kernel; steps 2, 3, 5, 6 in the **anomalib** kernel.

| # | Notebook | Cell(s) | Action |
|---|---|---|---|
| 0 | `Day04_01`, `Day04_02` | all | annotate the dataset, train YOLO |
| 1 | `Day04_03_YOLO_Evaluation.ipynb` | Part 2–4, then Part 5 `f7f5833b`, `552d3581` | evaluate on the YOLO dataset's test split; then decide the shared split and score **calibration only** |
| | | `shared-sealed-test` | **stops** — the freeze does not exist yet |
| 2 | `Day05_01`, then `Day05_02_PatchCore_Training.ipynb` | Part 0–4 (`…daed190f`, `1c4cd018`) | fit PatchCore, verify the split against Day 4, score calibration |
| | | Part 5 `clarity-sealed-test-scoring` | **stops** — the freeze does not exist yet |
| 3 | `Day05_03_YOLO_vs_PatchCore.ipynb` | `39ee7a27` → `935ef5b9`, then `clarity-freeze-record` | pair calibration by image ID, choose both thresholds, record the freeze |
| 4 | `Day04_03_YOLO_Evaluation.ipynb` (YOLO kernel) | `shared-sealed-test` | seal the 26 YOLO test scores |
| 5 | `Day05_02_PatchCore_Training.ipynb` | `clarity-sealed-test-scoring` | seal the 26 PatchCore test scores |
| 6 | `Day05_03_YOLO_vs_PatchCore.ipynb` | `clarity-load-sealed-test` → `9747ac10` | verify both seals, produce the final comparison, save JSON + CSV |
| 7 | `Day05_03` | `clarity-archive-gate` (`SHOW_ARCHIVED_TEST = True`) | only after the final comparison; the archived panels are labelled as such |

If anything changes after step 3, the model or the split is a **new experiment**: redo the freeze and
keep `TEST_ALREADY_SEEN=True`.

---

## Reference: exact commands used

```
python -m pytest assets/tests -q
python assets/scripts/apply_nepali_translations.py --write      # then a dry run: 0 changes
python assets/scripts/apply_nepali_docs.py --write              # then a dry run: 0 changes
python assets/scripts/check_nepali_coverage.py --strict
python assets/scripts/validate_notebooks.py --execute none      # 194 passed, 0 failed
python assets/scripts/export_trilingual_pdf.py --only Day04|Day05|Week1|Syllabus
python assets/scripts/export_explanations_pdf.py --only Day04|Day05|Week1
```
