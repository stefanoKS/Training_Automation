<!--
Nepali anuwad / Nepali translation source for
docs/reference_materials.md

The link tables above each block are the authoritative list; the Nepali block explains how to use
them. URLs are never translated.
-->
# reference_materials — Nepali anuwad

<!-- ne-doc: docs/reference_materials.md -->

<!-- ne-section: Reference materials -->
### Nepali ma

yo talim ma herieka adhikarik kagajat ra thap sikaika samagri hun.
**sadhain adhikarik kagajatalai prathamikata dinuhos.** blog lekh purano huna sakchha.

<!-- ne-section: ## 0. -->
### Nepali ma

| bishay | thaun | kasari prayog garne |
|---|---|---|
| din 1–5 ko byakhya PDF | `docs/pdf/Day0N_explanation_ja_ne.pdf` (wa pahileko `*_ja_en.pdf`) | notebookko byakhya jastako tastai banaiyeko pustika. aphalain padhna |
| hapta 1 ko saransh PDF | `docs/pdf/Week1_explanation_ja_ne.pdf` | dohoryaun ra chhapn |
| PDF feri banaune tarika | `docs/pdf/README.md` | `python assets\scripts\export_trilingual_pdf.py` |
| chitrako srot | `assets/reference_outputs/README.md` | maapan garieka chitra ra yojanabaddha chitrako farak |

PDF notebookko Markdown baat sbatah banchha, tyasaile notebook sudharepachhi uhi adeshale dubai milauna sakinchha.
export le notebook chalaundain ra model daunalod gardaina.

<!-- ne-section: ## 1. コア（必須） -->
### Nepali ma

pahile yahi talikaka lingk padhnuhos. Python, Jupyter, NumPy, Matplotlib, Pillow ra pandas ka
adhikarik kagajat hun. Japani anuwad bhaeka prishth pani chhan; Angreji mulasang milaer herda ramro hunchha.

<!-- ne-section: ## 2. OpenCV -->
### Nepali ma

din 2 ma samhaline kura mathika 5 lingkale lagabhag sabai dhakchhan.
`cv2.findContours` le **OpenCV 4 ma dui** maan (contours, hierarchy) pharkaunchha.
OpenCV 3 ka lekh (tin maan pharkaune) sang namisaunuhos.

<!-- ne-section: ## 3. PyTorch -->
### Nepali ma

din 4–5 ma model bhitr ke hunchha bujhn yi lingk upayogi chhan. tar yo talim ma PyTorch ko kod
aphain lekhnu pardaina; ultralytics ra anomalib le samhalchhan.

<!-- ne-section: ## 4. Ultralytics YOLO -->
### Nepali ma

din 3–4 ma prayog hune YOLO ka adhikarik prishth hun. predict, train, val ka bikalp ra
natijako arth yahinbat jaanchnuhos. **Ultralytics ka model ra kod AGPL-3.0** hun;
utpadanama rakhnuaghi laisens jaanchnuhos.

<!-- ne-section: ## 5. Anomalib -->
### Nepali ma

din 5 ko PatchCore ka adhikarik kagajat hun. sanskaran 2.7.0 prayog bhaeko chha; purano sanskaranako
lekh herda API farak huna sakchha bhanne dhyan dinuhos.

<!-- ne-section: ## 6. データセットと評価の考え方 -->
### Nepali ma

datasetko banabat, train/val/test ko bandaphant ra maapan (precision, recall, AUROC) ko arth bujhn
yi lingk hernuhos. maapan ko naam jastako tastai rakhnuhos; Nepali anuwad garda arth nabigriyos.

<!-- ne-section: ## 7. ライセンスの確認 -->
### Nepali ma

samagri prayog garnuaghi laisens jaanchnuhos. sikai ma prayog garnu ra utpadanama rakhnu farak kura ho.
yo talim ma prayog bhaeka bahy samagriko srot
[`assets/external_samples/PROVENANCE.md`](../assets/external_samples/PROVENANCE.md) ma abhilekh chha.

<!-- ne-section: ## 8. 実写の参考画像 -->
### Nepali ma

sandarbha photo laisens bhaeka mul file hun, karakhanako maapan natija hoinan. ti **sikai, calibration wa
parikshanko data ma prayog hundainan**. line ra jaanchne tarika
[START_HERE.md](../START_HERE.md) ko step 7 ma chha.
