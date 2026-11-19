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
# Day05_01_Anomaly_Detection_Concepts — Tamang (provisional Eastern Tamang, Devanagari)

<!-- taj-pending: a62c030b/unit:day-5-notebook-01-introduction-to-anomaly-detection | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: a62c030b/unit:explain-what-anomaly-detection-d | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: a62c030b/unit:distinguish-normal-from-abnormal | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: a62c030b/unit:explain-how-this-differs-from-su | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: a62c030b/unit:explain-patches-features-and-ano | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: a62c030b/unit:explain-patchcore-using-an-analo | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: a62c030b/row:duration | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: a62c030b/row:difficulty | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: a62c030b/row:prerequisites | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: a62c030b/row:libraries | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: a62c030b/row:kernel | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: a62c030b/row:timetable | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: a62c030b/unit:notebook-facts | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: a62c030b/unit:your-explanation-of-how-anomaly | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: a62c030b/unit:notes-on-how-to-read-an-anomaly | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: b071950f/row:day | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: b071950f/row:today | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: b071950f/row:duration | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: b071950f/row:prerequisites | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: b071950f/row:timetable | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: b071950f/unit:where-this-notebook-sits | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: audit-learning-loop/unit:predict-run-inspect-explain | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 73b2d2a4/unit:preparation | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 68ece906/unit:what-anomaly-detection-is | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 154bde87/row:needs-for-fitting | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 154bde87/row:output | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 154bde87/row:weak-at | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 154bde87/unit:finding-not-like-usual | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: fig-teach_normal_variation/unit:normal-variation-versus-a-defect-caption | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: fig-teach_normal_variation/unit:what-to-notice | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: fig-teach_normal_variation/unit:try-to-answer | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: ef2014d3/unit:normal-and-abnormal-samples | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: d5d90ce4/unit:supervised-versus-unsupervised | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: fig-VisA_samples/unit:why-collecting-only-normal-samples-is-hard-caption | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: fig-VisA_samples/unit:what-to-notice | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: fig-VisA_samples/unit:try-to-answer | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-patch-data-roles/row:only | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-patch-data-roles/unit:read-the-data-roles-before-terminology | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 5e60e191/row:supervised | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 5e60e191/row:unsupervised | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 5e60e191/row:normal-only | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 5e60e191/unit:optional-research-terminology | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: cf09f7d8/unit:patches-and-features | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-patch-overlap/unit:compare-the-analogy-with-the-actual-mechanism | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: clarity-patch-overlap/unit:what-to-notice | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 429f99e1/unit:a-patch-is-a-small-piece-of-the-image | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: f6726637/unit:what-a-feature-is | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 33f893ee/unit:distance-to-the-nearest-neighbour | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: a85f80ca/unit:expected-output | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: c4d6ab80/unit:how-to-read-the-plot | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 47e11e57/unit:the-patchcore-idea | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: e9df232d/unit:patch-feature-position-nearest-neighbour-score-caption | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: e9df232d/unit:what-to-notice | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: e9df232d/unit:try-to-answer | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: c474e947/unit:why-a-memory-bank | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: fig-teach_memory_bank/unit:the-memory-bank-and-the-nearest-neighbour-caption | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: fig-teach_memory_bank/unit:what-to-notice | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: fig-teach_memory_bank/unit:try-to-answer | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 1aba9655/unit:anomaly-scores-and-heatmaps | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 5c642a4a/row:representation | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 5c642a4a/row:postprocessed | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 5c642a4a/row:decision | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 5c642a4a/unit:two-output-kinds-read-in-three-stages | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: fig-teach_score_levels/unit:intermediate-distances-and-two-output-kinds-caption | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: fig-teach_score_levels/unit:what-to-notice | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: fig-teach_score_levels/unit:try-to-answer | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 1f601e75/unit:turning-a-score-into-ok-ng-with-a-threshold | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 1784ecb1/unit:what-patchcore-cannot-do | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 2b8faacc/unit:exercises | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 074c9203/unit:exercise-1-basic-explain-it-in-your-own-words | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 0cf76dd2/row:low | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 0cf76dd2/row:medium | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 0cf76dd2/row:high | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 0cf76dd2/unit:exercise-2-intermediate-move-the-threshold | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 3c808d08/unit:exercise-3-optional-challenge-how-would-you-use-this-for-pvc | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 93412cb6/unit:understanding-questions | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 2fb637f4/row:normal-images-missing | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 2fb637f4/row:points-overlap | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 2fb637f4/row:distance-meaning | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 2fb637f4/row:threshold-choice | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 2fb637f4/row:score-range | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: 2fb637f4/unit:troubleshooting | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: f1c0d7cd/unit:completion-checklist | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: ea343d35/unit:optional | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: ea343d35/unit:reference-links | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
<!-- taj-pending: ea343d35/unit:not-mandatory | no dependable reference translation is available in this environment; a native/advanced Tamang reviewer must supply and sign off the text -->
