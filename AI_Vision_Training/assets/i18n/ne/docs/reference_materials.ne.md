<!--
नेपाली अनुवाद / Nepali translation source for
docs/reference_materials.md

The link tables above each block are the authoritative list; the Nepali block explains how to use
them. URLs are never translated.
-->
# reference_materials — नेपाली अनुवाद

<!-- ne-doc: docs/reference_materials.md -->

<!-- ne-section: Reference materials -->
### नेपालीमा

यो तालिममा हेरिएका आधिकारिक कागजात र थप सिकाइका सामग्री हुन्।
**सधैं आधिकारिक कागजातलाई प्राथमिकता दिनुहोस्।** blog लेख पुरानो हुन सक्छ।

<!-- ne-section: ## 0. -->
### नेपालीमा

| विषय | ठाउँ | कसरी प्रयोग गर्ने |
|---|---|---|
| दिन 1–5 को व्याख्या PDF | `docs/pdf/Day0N_explanation_ja_ne.pdf` (वा पहिलेको `*_ja_en.pdf`) | नोटबुकको व्याख्या जस्ताको तस्तै बनाइएको पुस्तिका। अफलाइन पढ्न |
| हप्ता १ को सारांश PDF | `docs/pdf/Week1_explanation_ja_ne.pdf` | दोहोर्याउन र छाप्न |
| PDF फेरि बनाउने तरिका | `docs/pdf/README.md` | `python assets\scripts\export_trilingual_pdf.py` |
| चित्रको स्रोत | `assets/reference_outputs/README.md` | मापन गरिएका चित्र र योजनाबद्ध चित्रको फरक |

PDF नोटबुकको Markdown बाट स्वतः बन्छ, त्यसैले नोटबुक सुधारेपछि उही आदेशले दुवै मिलाउन सकिन्छ।
export ले नोटबुक चलाउँदैन र model डाउनलोड गर्दैन।

<!-- ne-section: ## 1. コア（必須） -->
### नेपालीमा

पहिले यही तालिकाका लिङ्क पढ्नुहोस्। Python, Jupyter, NumPy, Matplotlib, Pillow र pandas का
आधिकारिक कागजात हुन्। जापानी अनुवाद भएका पृष्ठ पनि छन्; अङ्ग्रेजी मूलसँग मिलाएर हेर्दा राम्रो हुन्छ।

<!-- ne-section: ## 2. OpenCV -->
### नेपालीमा

दिन २ मा सम्हालिने कुरा माथिका ५ लिङ्कले लगभग सबै ढाक्छन्।
`cv2.findContours` ले **OpenCV 4 मा दुई** मान (contours, hierarchy) फर्काउँछ।
OpenCV 3 का लेख (तीन मान फर्काउने) सँग नमिसाउनुहोस्।

<!-- ne-section: ## 3. PyTorch -->
### नेपालीमा

दिन 4–5 मा model भित्र के हुन्छ बुझ्न यी लिङ्क उपयोगी छन्। तर यो तालिममा PyTorch को कोड
आफैं लेख्नु पर्दैन; ultralytics र anomalib ले सम्हाल्छन्।

<!-- ne-section: ## 4. Ultralytics YOLO -->
### नेपालीमा

दिन 3–4 मा प्रयोग हुने YOLO का आधिकारिक पृष्ठ हुन्। predict, train, val का विकल्प र
नतिजाको अर्थ यहीँबाट जाँच्नुहोस्। **Ultralytics का model र कोड AGPL-3.0** हुन्;
उत्पादनमा राख्नुअघि लाइसेन्स जाँच्नुहोस्।

<!-- ne-section: ## 5. Anomalib -->
### नेपालीमा

दिन ५ को PatchCore का आधिकारिक कागजात हुन्। संस्करण 2.7.0 प्रयोग भएको छ; पुरानो संस्करणको
लेख हेर्दा API फरक हुन सक्छ भन्ने ध्यान दिनुहोस्।

<!-- ne-section: ## 6. データセットと評価の考え方 -->
### नेपालीमा

डेटासेटको बनावट, train/val/test को बाँडफाँट र मापन (precision, recall, AUROC) को अर्थ बुझ्न
यी लिङ्क हेर्नुहोस्। मापनको नाम जस्ताको तस्तै राख्नुहोस्; नेपाली अनुवाद गर्दा अर्थ नबिग्रियोस्।

<!-- ne-section: ## 7. ライセンスの確認 -->
### नेपालीमा

सामग्री प्रयोग गर्नुअघि लाइसेन्स जाँच्नुहोस्। सिकाइमा प्रयोग गर्नु र उत्पादनमा राख्नु फरक कुरा हो।
यो तालिममा प्रयोग भएका बाह्य सामग्रीको स्रोत
[`assets/external_samples/PROVENANCE.md`](../assets/external_samples/PROVENANCE.md) मा अभिलेख छ।

<!-- ne-section: ## 8. 実写の参考画像 -->
### नेपालीमा

सन्दर्भ फोटो लाइसेन्स भएका मूल फाइल हुन्, कारखानाको मापन नतिजा होइनन्। ती **सिकाइ, क्यालिब्रेसन वा
परीक्षणको डेटामा प्रयोग हुँदैनन्**। लिने र जाँच्ने तरिका
[START_HERE.md](../START_HERE.md) को स्टेप 7 मा छ।
