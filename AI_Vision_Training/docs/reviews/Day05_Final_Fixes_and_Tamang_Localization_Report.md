# Day 5 最終修正・タマン語ローカライズ レポート / Day 5 final fixes and Tamang localization

Date: 2026-11-19
Course root: `AI_Vision_Training/`
Branch: `feature/day05-final-fixes-and-tamang-localization` (local only — nothing pushed or merged)
Author: AI assistant (Copilot SDK in VS Code) on behalf of stefanoKS

This report separates **executed evidence**, **source inspection**, and **things that were not run**.
Where something is BLOCKED it says so instead of claiming PASS.

---

## A. Baseline

| Item | Value |
|---|---|
| HEAD when the work started | `61f8ff6` (main), working tree had one accidental kernelspec edit in `Day01_01` |
| That edit | VS Code rewrote `kernelspec` to `python3`; `test_notebook_kernel_is_one_of_the_course_kernels` failed because of it. Restored with `git checkout --`; it is not part of any commit |
| Report read first | `docs/reviews/Day04_Day05_Final_Stabilization_Report.md` |
| Tests collected at HEAD | 509 (`pytest --collect-only`) |
| Baseline behavioural reference | the previous report's measured baseline: 495 passed |
| Baseline generators | `apply_nepali_translations.py` 0 changes, `check_nepali_coverage.py --strict` exit 0, `validate_notebooks.py --execute none` 194 passed |

I did **not** re-run the full suite at the pristine commit before editing; the first full run happened
after the technical fixes. That run was **520 passed, 2 failed, 1 skipped**, and both failures were
mine (a fixture that no longer satisfied the new weight-digest contract, and the accidental
kernelspec). Both were fixed; the causes are named in §C.

Toolchain measured on this machine (not assumed):

| Environment | Python | torch | ultralytics | anomalib | lightning |
|---|---|---|---|---|---|
| base (`C:\Users\stefa\miniconda3`) | 3.11.4 | 2.0.1+cpu | 8.0.187 | 1.1.0dev (**no** `anomalib.post_processing`) | absent |
| `.venv-anomalib` (created for this work, git-ignored) | 3.11.4 | **2.15.0+cpu** | absent (by design) | **2.7.0** | **2.6.6** |

---

## B. Patch plan — cells and files

### Notebook cells changed

| Notebook | Cell id | Change |
|---|---|---|
| `Day05_02` | `f1a28c15` | no longer prints the test count or the label distribution; prints train, calibration and the evaluation-folder total, and says the test side stays hidden until the freeze |
| `Day05_02` | `6c5c2682` | JA/EN wording: test is scored after the freeze by Day 4 N03 and by Part 5 of this notebook; N03 never runs TEST inference |
| `Day05_02` | `8853ba93` | the calibration payload is re-published with `write_json_atomic` (was a plain `write_text`) |
| `Day05_02` | `39a9c510` | the print no longer claims the test maps appear in Notebook 03 |
| `Day05_02` | `1c4cd018` | threshold read from `CALIBRATED_POSTPROCESSOR["adaptive_threshold"]`, not `model.post_processor.adaptive_threshold` |
| `Day05_02` | `clarity-sealed-test-scoring` | restart message rewritten (checkpoint reload + fingerprint; a refit is a new experiment); stale maps quarantined; maps digested; seal validated again after the map block; maps moved, verified, then the JSON published last |
| `Day05_02` | `clarity-sealed-test` | recovery snippet added (verified against the real runtime); JA/EN table fixed |
| `Day04_03` | `f7f5833b` | records `WEIGHTS_PATH` and `WEIGHTS_SHA256` before any inference |
| `Day04_03` | `552d3581` | the calibration payload carries `weights_sha256` |
| `Day04_03` | `shared-sealed-test` | existing seal fully validated (schema/identity/role/thresholds/IDs/duplicates/partition/coverage/split digest/weight digest) and never re-scored; new seal records the weight digest |
| `Day04_03` | `shared-sealed-test-intro` | JA/EN text now says the frozen weights are checked by path **and** SHA-256 |
| `Day05_03` | `39ee7a27` | verifies the YOLO weights by content before anything is paired |
| `Day05_03` | `clarity-freeze-record` | freeze record immutable once either seal exists; identical rerun is a no-op; changed settings raise; weight digest verified |
| `Day05_03` | `clarity-load-sealed-test` | numeric-map set verified against the seal's digest, reported (not silently used) |
| `Day05_03` | `9747ac10` | weight digest cross-check, `numeric_maps` status recorded, CSV published atomically with a BOM |

### Files added

```
AI_Vision_Training/assets/helpers/experiment_identity.py   (extended)
AI_Vision_Training/assets/scripts/i18n_locales.py
AI_Vision_Training/assets/scripts/apply_translations.py
AI_Vision_Training/assets/scripts/apply_docs.py
AI_Vision_Training/assets/scripts/check_localization_coverage.py
AI_Vision_Training/assets/i18n/taj/README.md
AI_Vision_Training/assets/i18n/taj/terminology.md
AI_Vision_Training/assets/i18n/taj/coverage_inventory.json
AI_Vision_Training/assets/i18n/taj/notebooks/*.taj.md        (16)
AI_Vision_Training/assets/i18n/taj/docs/*.taj.md              (12)
AI_Vision_Training/assets/tests/test_day05_anomalib27_integration.py
AI_Vision_Training/assets/tests/test_tamang_localization.py
AI_Vision_Training/assets/tests/test_tamang_pdf_renderer.py
```

### Files modified (other than the notebooks)

```
assets/scripts/apply_nepali_translations.py     → thin wrapper over apply_translations.py (locale ne)
assets/scripts/apply_nepali_docs.py             → thin wrapper over apply_docs.py (locale ne)
assets/scripts/export_trilingual_pdf.py         → --locale {ne,taj}, taj-Deva tag, gate, suffix
assets/i18n/ne/notebooks/Day04_03_…ne.md        → one line: weights checked by path and SHA-256
assets/tests/test_day04_day05_contracts.py      → new groups F–J
assets/tests/test_experiment_identity.py        → CASE 12/13 + real-anomalib accessor test
assets/tests/test_clarity_review.py             → freeze fixture now carries real weights + digest
docs/instructor/day05_instructor_guide.md       → test numbers come from the two sealed scorings
docs/pdf/README.md                              → Tamang booklets section, page counts
docs/pdf/Day04_explanation_ja_en_ne.pdf         → rebuilt (90 pages)
docs/pdf/Day05_explanation_ja_en_ne.pdf         → rebuilt (90 pages)
docs/pdf/Week1_explanation_ja_en_ne.pdf         → rebuilt (459 pages)
```

Untouched, verified with `git diff --stat` against the pre-work commit: `assets/anomaly_dataset`,
`assets/yolo_dataset`, `assets/defect_samples`, `assets/diagrams`, `assets/svg`, `results/`,
`submissions/`, `requirements/`, `start_training.cmd`, `docs/pdf/*_ja_en.pdf`, and every
`*_ja_en_ne.pdf` other than the three rebuilt above.

---

## C. Technical corrections and the tests that prove them

| # | Correction | Evidence |
|---|---|---|
| 1 | Test label distribution hidden before the freeze | `test_the_datamodule_cell_hides_the_test_composition`; Notebook 01's promise is unchanged |
| 2 | Freeze record immutable once a seal exists | `test_the_freeze_record_is_immutable_once_a_seal_exists` (identical rerun → byte-identical record and seal, "Identical freeze record"; changed declaration → `RuntimeError` "immutable", nothing written) |
| 3 | Existing YOLO seal fully validated | `test_an_invalid_existing_yolo_seal_is_rejected_and_test_is_not_re_scored` — six mutations (role, threshold, coverage, duplicate, partition, schema); each raises, the file stays byte-identical, `model.predict` is never called again. `test_a_valid_existing_yolo_seal_is_accepted_without_re_scoring` covers the happy path |
| 4 | Canonical PostProcessor accessor | `test_the_threshold_comes_from_the_canonical_helper` (source no longer contains the stale accessor) + `test_the_canonical_helper_reads_the_pinned_anomalib_postprocessor` (real `anomalib.post_processing.PostProcessor`; skipped in the base env) + §D |
| 5 | Restart message and recovery | `test_the_restart_message_matches_the_documented_recovery`; `test_checkpoint_recovery_accepts_only_the_frozen_bytes`; real checkpoint recovery in §D |
| 6 | YOLO weights by SHA-256 | `test_the_yolo_weight_contents_are_frozen_and_verified` (payload digest == file digest == freeze digest; retraining blocks sealing); `test_file_digest_helpers_name_what_changed`; `test_the_yolo_weights_digest_is_the_real_file_digest` (§D) |
| 7 | Interruption recovery / map publication | `test_stale_maps_are_quarantined_and_the_seal_records_the_published_set`, `test_a_rejected_map_publish_leaves_no_seal_behind`, `test_a_map_digest_mismatch_is_not_presented_as_this_experiments_output`, `test_case10_a_failed_write_publishes_nothing` |
| 8 | JA/EN wording | `test_the_wording_puts_test_inference_in_day4_and_day5_02`, `test_the_six_step_table_names_the_right_owners`, `test_the_sealing_sections_name_their_notebooks` |
| 9 | Isolation / thresholds / denominators / six steps | `test_the_prefreeze_export_holds_calibration_rows_only` (the model never sees a test image), `test_end_to_end_from_the_split_to_the_final_comparison` (`TP+FP+FN+TN == n_images`, CSV role column), `test_a_partial_calibration_cannot_be_frozen`, plus the threshold tests already in `test_experiment_identity.py` |
| 10 | Pinned anomalib integration | §D — PASS in `.venv-anomalib`, **BLOCKED** in the base environment (reported as a skip, never as a pass) |

Two failures from the first full run, and why they happened:

* `test_freeze_requires_written_declaration_and_persists_reused_data_status` — the fixture's
  `yolo_data` had no weight digest. The fixture was updated to create a real `weights/best.pt` and
  record its digest; the test's own assertions are unchanged.
* `test_notebook_kernel_is_one_of_the_course_kernels[Day01_01…]` — the accidental VS Code kernelspec
  edit. Restored.

No existing assertion was weakened. The only tests deleted were a too-strict six-step check I had
just written; it was replaced by two narrower ones.

---

## D. Genuine `anomalib==2.7.0` evidence

Environment created for this work: `.venv-anomalib` with `torch==2.15.0`, `torchvision==0.29.2`,
`anomalib==2.7.0`, `lightning==2.6.6` (the pins in `requirements/anomalib.txt`).

`python -m pytest assets/tests/test_day05_anomalib27_integration.py` in that interpreter →
**6 passed in 34 s**. What it actually did, with the real library:

| Check | Result |
|---|---|
| `anomalib.Folder` (`val_split_mode="from_test"`, ratio 0.5, seed 2026) vs `shared_set_split.py` | **identical**: 32 / 26 / 26, no differences |
| `Patchcore` + `Engine.fit` on CPU | ran (1 epoch, resnet18) |
| `model.post_processor.adaptive_threshold` on the real object | **does not exist** → the old accessor was a real bug |
| `postprocessor_state(model)["adaptive_threshold"]` | finite float (9.752996…) recorded in `patchcore_predictions.json` |
| fitted fingerprint before/after calibration scoring | unchanged |
| `fitted_state` stability within the process | stable |
| checkpoint written by `Engine.fit` | `day05/Patchcore/pvc_sheet/{latest,v0}/weights/lightning/model.ckpt` |
| `Patchcore.load_from_checkpoint` + `recover_fitted_model` | loads, fingerprint matches the fit → recovery is real, not documented-only |
| test scoring | 26 images, once, after the freeze; scores within 0-1 |
| final comparison | `n_images == 26`, `TP+FP+FN+TN == 26`, `numeric_maps.verified == True`, weight digest present |

The YOLO half of that integration stays duck-typed because `ultralytics` cannot be installed next to
anomalib (`cv2` collision documented in `requirements/anomalib.txt`). That limitation is stated, not
hidden.

In the base environment the same module is **skipped** with the reason "anomalib 2.x is required …
(BLOCKED, not PASS)". The full base suite therefore reports `2 skipped`, one of which is this module.

---

## E. Tamang inventory and review status

`python assets/scripts/check_localization_coverage.py --locale taj --strict --inventory assets/i18n/taj/coverage_inventory.json`

| Bucket | Count |
|---|---|
| Notebook markdown cells with a region | 0 |
| … recorded as **pending** (no dependable translation) | **656** |
| … intentionally **exempt** (separators, empty scaffolding, "write your code here") | 147 |
| … **missing** (neither translated, pending nor exempt) | **0** |
| Document sections recorded as pending | **154** across 12 documents |
| **approved** notebook blocks | **0** |
| **draft** notebook blocks | **0** |
| Gate result | **BLOCKED** (exit 1) |

The 656 pending cells are exactly the 656 cells the legacy Nepali pass translated
(`test_the_pending_inventory_covers_every_cell_the_nepali_pass_translated`), so replacing the language
did not silently drop teaching content.

Every catalog carries provenance:

```
locale: taj
bcp47: taj-Deva
variety: Eastern Tamang, Devanagari; Western Tamang (tdg) is a separate language
script: devanagari
provenance: none (no translation produced yet)
review: pending-native-review
reviewer: (none)
```

**No Tamang learner-facing text was produced.** No Nepali was copied into the taj catalogs, no English
was relabelled, and nothing was machine-translated into place. The reason is stated in
`assets/i18n/taj/README.md`: no dependable reference material was reachable (Kathmandu University
ILPRL/TMT was not accessible from this environment, and nothing from it was copied), and no
native/advanced Tamang speaker is available to this session. The blocks stay pending rather than
become fabricated text.

---

## F. Localization design decisions

* **Locale = `taj`, tag `taj-Deva`, variety "Eastern Tamang", confirmed = False.** Tamang is
  Tibeto-Burman; Nepali is Indo-Aryan. Same script, different language — which is exactly why a script
  test can never prove Tamang. Western Tamang (`tdg`) is a separate language and is named as such so
  it cannot be mixed in later by accident.
* **Markers:** `<!-- taj:begin … -->` / `<!-- taj:end -->`, directives `taj-cell`, `taj-section`,
  `taj-status`, `taj-pending`. They never collide with the legacy `ne:` markers, so a rollback can
  keep both (proved by `test_nepali_and_tamang_regions_do_not_collide`).
* **Four states, not two:** `approved` (reviewer signed), `draft` (text exists, unreviewed),
  `pending` (recorded as untranslated), `exempt`. `missing` exists as a defect state so a forgotten
  cell can never hide.
* **The gate has three independent locks:** every required block approved, every catalog header
  `review: approved`, and a confirmed variety/script. A translator finishing the text is therefore not
  enough on its own — the trainees' variety decision is a separate gate.
* **Language-aware tools:** `apply_translations.py` / `apply_docs.py` take `--locale`, support dry-run
  (default), `--write`, `--only`, and are idempotent. The two `apply_nepali_*` scripts are now thin
  wrappers, so the historical commands still behave identically (0 changes on the real corpus).
* **Order of languages in a learner-facing block:** JA → EN → Tamang. The legacy Nepali stays in the
  repository as rollback material and is `learner_facing = False`.

---

## G. PDFs

### Booklets rebuilt

| File | Pages | Why |
|---|---|---|
| `Day04_explanation_ja_en_ne.pdf` | 90 | Part 5 intro text changed (weights by content) |
| `Day05_explanation_ja_en_ne.pdf` | 90 | six-step wording, restart/recovery section, map wording |
| `Week1_explanation_ja_en_ne.pdf` | 459 | aggregates the four previous days |

`Day01`, `Day02`, `Day03`, `Course_Syllabus`, `Setup`, `Installation_Guide`, `Repository_Guide` and
every `*_ja_en.pdf` were **not** rebuilt (no source change for them).

### Rendering checked, not assumed

`python assets/scripts/inspect_pdf_pages.py --pdf … --languages ja,ne`:

```
Day04 … pages=90  Nepali text layer: no split words, the PDF stays searchable
Day05 … pages=90  no blank pages, no text outside the printable area
Week1 … pages=459  no blank pages, no text outside the printable area
```

Pages rendered and inspected by eye: `Day05` **56** (six-step table, common-situations table, updated
kernel-restart row) and **57** (English six-step table, recovery snippet, Romanized Nepali table).

### `*_ja_en_taj.pdf`

`export_trilingual_pdf.py --locale taj` exists, writes `*_ja_en_taj.pdf`, sets the text-layer tag to
`taj-Deva`, reads the terminology from `assets/i18n/taj/`, and **refuses to build** while the gate
fails:

```
[gate] BLOCKED — taj-Deva booklets are not built: the localization gate fails.
   - 656 notebook cells are recorded as pending
   …
exit status 2
```

So no Tamang booklet exists today, and none can be produced from unreviewed content. What *was*
verified is the rendering path a Taj booklet will use — Devanagari through the same Chromium/HarfBuzz
pipe, as **searchable Unicode** (`तामाङ भाषा` found in the text layer), with tables, images, links and
a forced page break surviving (`test_tamang_pdf_renderer.py`, 4 passed). That fixture is a rendering
sample, not a translation of lesson content.

---

## H. Test matrix

| Suite / command | Environment | Result |
|---|---|---|
| `python -m pytest assets/tests -q` | base | **579 passed, 2 skipped, 4 warnings** (two consecutive full runs: 482.72 s and 480.40 s) |
| `assets/tests/test_day05_anomalib27_integration.py` | `.venv-anomalib` (anomalib 2.7.0) | **6 passed, 34 s** |
| `assets/tests/test_day05_anomalib27_integration.py` | base | **BLOCKED** (module-level skip: no `anomalib.post_processing`) |
| `assets/scripts/validate_notebooks.py --execute none` | base | **194 passed, 0 failed** |
| `apply_nepali_translations.py` (dry run) | base | **0 cells would change** |
| `apply_nepali_docs.py` (dry run) | base | **0 documents would change** |
| `check_nepali_coverage.py --strict` | base | **656/803 (81.7 %), 147 exempt, 0 missing, 1149 Romanized, 0 Devanagari, 12/12 documents**; exit 0 |
| `check_localization_coverage.py --locale taj --strict` | base | **BLOCKED**, exit 1 (656 pending, 154 pending sections, unverified variety) |
| `check_localization_coverage.py --locale taj --emit-pending-catalogs` (second run) | base | **0 would be written** (idempotent) |
| `export_trilingual_pdf.py --locale taj` | base | **BLOCKED**, exit 2, no file written |
| `export_trilingual_pdf.py --only Day04/Day05/Week1` | base | PASS (90 / 90 / 459 pages) |
| `inspect_pdf_pages.py` on the three rebuilt booklets | base | PASS (no blank pages, no overflow, no split words) |
| `git diff --check` | base | clean |

The base suite's two skips are: the anomalib-2 integration module (BLOCKED, as above) and one
pre-existing conditional skip.

---

## I. Remaining risks

1. **No Tamang text, no native review.** The catalogs are honest scaffolding. Until a Tamang speaker
   translates and signs each block, and the trainees confirm the variety and script, the gate stays
   closed and no learner-facing Tamang exists.
2. **Locale still provisional.** `taj-Deva` is a starting point, not a decision. If the trainees use
   Tamyig or Western Tamang, the catalogs must be redone — the locale registry makes that a change of
   one entry, not a rename of files.
3. **One classroom run is still the first full rehearsal.** The real anomalib run here used the real
   dataset on this machine; a different machine or a different anomalib build can still change the
   split, and the notebooks stop loudly rather than mixing partitions.
4. **Weight digests need the weights file present.** `clarity-freeze-record` and `shared-sealed-test`
   verify the contents on disk; a learner who deleted `best.pt` gets a stop, not a silent pass. This is
   intended, but it is a new failure mode to mention in class.
5. **Freeze immutability compares the whole canonical record.** Anything volatile added to that record
   in future (a timestamp, a temp path) would make an identical rerun fail loudly. That is the safe
   direction, but it must be kept in mind.
6. **Maps remain derived artefacts.** They are now digested and quarantined, and the JSON stays
   authoritative, but a map set can still be deleted by hand without affecting the result.
7. **PDF page counts move with the text.** The numbers in `docs/pdf/README.md` were updated; the
   inspector prints the truth on every rebuild.

---

## J. Readiness decisions

**Day 5 (technical): READY WITH CONDITIONS.** The four defects fixed here are covered by tests that
execute the real cells, and the PatchCore half now has genuine `anomalib==2.7.0` evidence. The
conditions are: one real classroom rehearsal on the pinned environment; the YOLO half of the
integration remains duck-typed because `ultralytics` cannot share the environment.

**Tamang localization: NOT READY (BLOCKED).** Zero approved blocks, zero drafts, 656 notebook cells and
154 document sections recorded as pending, the variety and script unconfirmed, and no `*_ja_en_taj.pdf`
produced. This is the honest state, not a partial success.
