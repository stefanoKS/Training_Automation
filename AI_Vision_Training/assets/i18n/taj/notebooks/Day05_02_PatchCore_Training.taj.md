<!--
locale: taj
bcp47: taj-Deva
variety: Eastern Tamang, Devanagari; Western Tamang (tdg) is a separate language
script: devanagari
provenance: none (no translation produced yet)
review: pending-native-review
reviewer: (none)
note: every block below is recorded as pending. Nothing here has been translated, so
note: nothing here can be mistaken for a finished translation; the production gate
note: keeps failing until a Tamang reviewer supplies and approves the text.
-->
# Day05_02_PatchCore_Training — Tamang (provisional Eastern Tamang, Devanagari)

<!-- taj-pending: 43cbc7ba/unit:day-5-notebook-02-training-patchcore | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 43cbc7ba/unit:initialise-patchcore-through-the | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 43cbc7ba/unit:explain-the-dataset-layout-used | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 43cbc7ba/unit:fit-the-model-on-normal-images-o | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 43cbc7ba/unit:obtain-anomaly-scores-and-heatma | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 43cbc7ba/unit:save-results-and-reason-about-th | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 43cbc7ba/row:duration | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 43cbc7ba/row:difficulty | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 43cbc7ba/row:prerequisites | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 43cbc7ba/row:libraries | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 43cbc7ba/row:kernel | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 43cbc7ba/row:timetable | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 43cbc7ba/unit:notebook-facts | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 43cbc7ba/unit:training-results-metrics | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 43cbc7ba/unit:heatmap-images | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 43cbc7ba/unit:a-table-of-per-image-anomaly-sco | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 43cbc7ba/unit:numeric-maps-calibration-maps-ca | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 01bf2bc9/row:day | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 01bf2bc9/row:today | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 01bf2bc9/row:duration | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 01bf2bc9/row:prerequisites | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 01bf2bc9/row:timetable | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 01bf2bc9/unit:where-this-notebook-sits | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: audit-learning-loop/unit:predict-run-inspect-explain | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 75d078b0/unit:preparation | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 2fa75b5a/unit:confirm-the-kernel | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 8f419564/row:anomalib-data-folder | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 8f419564/row:anomalib-models-patchcore | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 8f419564/row:anomalib-engine-engine | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 8f419564/unit:the-api-used-here-pinned-version | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 08e2ac7d/unit:the-data-layout | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: bc41a079/unit:only-normal-images-are-used-for-training | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: afbdd116/row:normal-dir | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: afbdd116/row:normal-test-dir | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: afbdd116/row:abnormal-dir | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: afbdd116/row:mask-dir | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: afbdd116/row:val-split-mode-val-split-ratio | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: afbdd116/row:num-workers | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: afbdd116/unit:building-the-datamodule | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: c7f73514/unit:verify-training-data-contains-no-anomalies | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 9e971153/unit:initialising-the-model | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: f6b40399/row:backbone | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: f6b40399/row:layers | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: f6b40399/row:pre-trained | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: f6b40399/row:coreset-sampling-ratio | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: f6b40399/row:num-neighbors | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: f6b40399/unit:choosing-the-backbone | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: audit-teach_patchcore_stages/unit:reading-the-code-caption | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: audit-teach_patchcore_stages/unit:what-to-notice | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: audit-teach_patchcore_stages/unit:try-to-answer | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 90a03498/unit:fitting-the-model | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: bf3d12fb/unit:one-pass-is-enough-for-patchcore-s-fit | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: fig-teach_backbone_vs_memory/unit:only-the-memory-bank-changes-caption | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: fig-teach_backbone_vs_memory/unit:what-to-notice | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: fig-teach_backbone_vs_memory/unit:try-to-answer | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: f5f00936/unit:why-the-progress-display-is-switched-off | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-fit-state/row:extraction | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-fit-state/row:fit | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-fit-state/row:calibration | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-fit-state/row:inference | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-fit-state/unit:which-state-changed | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 29df63e7/unit:what-was-saved | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 9aac8b7e/unit:evaluating | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: c452bff7/row:image-auroc | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: c452bff7/row:image-f1score | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: c452bff7/row:pixel-auroc | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: c452bff7/row:pixel-f1score | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: c452bff7/unit:the-four-metrics | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: ba5da1ef/unit:expected-output | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: f4d5f377/unit:when-the-numbers-look-too-good | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: f4d5f377/unit:never-quote-this-course-s-numbers-as-the-inspection-accuracy | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 28cb22c6/unit:scores-and-heatmaps | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 8cfeab62/unit:original-score-map-and-overlay-caption | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 8cfeab62/unit:what-to-notice | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 8cfeab62/unit:try-to-answer | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-score-card/row:raw-image-scalar | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-score-card/row:location-clue-map | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-score-card/row:decision-vs-threshold | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-score-card/unit:read-the-numbers-in-this-order | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: fig-ref_anomaly_panels/unit:calculated-synthetic-toy-numeric-map-caption | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: fig-ref_anomaly_panels/unit:what-to-notice | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: fig-ref_anomaly_panels/unit:try-to-answer | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: cefba6c0/row:pred-score | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: cefba6c0/row:pred-label | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: cefba6c0/row:anomaly-map | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: cefba6c0/row:gt-label | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: cefba6c0/row:image-path | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: cefba6c0/unit:look-at-results-image-by-image | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 11a17ecf/unit:caution-when-reading-the-numbers | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 748dffdf/unit:save-the-heatmaps-as-images | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: b8ec6f1a/unit:how-to-read-a-heatmap | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-sealed-test/row:step-1 | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-sealed-test/row:step-2 | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-sealed-test/row:step-3 | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-sealed-test/row:step-4 | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-sealed-test/row:step-5 | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-sealed-test/row:step-6 | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-sealed-test/unit:the-order-has-six-steps | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-sealed-test/row:scoring-before-freeze | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-sealed-test/row:run-all-stops | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-sealed-test/row:freeze-record-missing | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-sealed-test/row:calibration-images-unmatched | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-sealed-test/row:kernel-restarted | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-sealed-test/unit:common-situations | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-sealed-test/unit:freeze-record | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-sealed-test/unit:recover-step-1 | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-sealed-test/unit:recover-step-2 | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-sealed-test/unit:recover-step-3 | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-sealed-test/unit:recover-after-a-kernel-restart | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: d5e2bc6d/unit:exercises | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 09b10a38/unit:exercise-1-basic-record-the-metrics | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 93a1ccd3/unit:exercise-2-intermediate-change-a-setting-and-compare-on-cali | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 1fd52dc9/unit:exercise-3-optional-challenge-add-normal-variation | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: c81c8cac/unit:understanding-questions | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 2da75241/row:no-module-named-anomalib | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 2da75241/row:folder-object-attribute | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 2da75241/row:mismatch-error | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 2da75241/row:backbone-download | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 2da75241/row:training-slow | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 2da75241/row:out-of-memory | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 2da75241/unit:troubleshooting | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 483ecbb0/unit:completion-checklist | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: d02d8a44/unit:optional | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: d02d8a44/unit:reference-links | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: d02d8a44/unit:not-mandatory | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
