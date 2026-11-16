<!--
नेपाली अनुवाद / Nepali translation source for
README.md

Commands, paths, versions and file names stay byte-identical.
-->
# README — नेपाली अनुवाद

<!-- ne-doc: README.md -->

<!-- ne-section: Hiroshima Kasei Week 1 -->
### नेपालीमा

कासेइहिन विभागका कर्मचारीका लागि बनाइएको **५ दिन, १६ नोटबुक** को स्वअध्ययन AI तालिम सामग्री हो।
Python, AI र चित्र प्रशोधनको अनुभव नभएका मानिसलाई लक्षित गरेर बनाइएको छ।

| विषय | विवरण |
|---|---|
| अवधि | 2026 नोभेम्बर 16 (सोम) – 20 (शुक्र) |
| लक्षित | प्रोग्रामिङ अनुभव नभएका कासेइहिन विभागका कर्मचारी |
| समय | 08:00–16:50 (दिउँसोको खाना 12:00–12:50) |
| पुग्ने लक्ष्य | उच्च गतिको PVC सिट निरीक्षणका लागि चाहिने AI को आधार आफ्नै शब्दमा बुझाउन र चलाउन सक्ने |
| दायरा | **हप्ता १ मात्र**। वास्तविक निरीक्षण प्रणाली निर्माण हप्ता २ मा हुन्छ। |

<!-- ne-section: ## 1. 最初に読むもの -->
### नेपालीमा

तलको क्रममा अगाडि बढ्नुहोस्।

1. [`START_HERE.md`](START_HERE.md) — कम्प्युटर अन गर्नेदेखि सुरु हुने, एकदमै सुरुवाती तहका लागि प्रक्रिया
2. [`COURSE_SYLLABUS.md`](COURSE_SYLLABUS.md) — **समयतालिकाको एक मात्र आधिकारिक स्रोत**। हरेक दिनको अनिवार्य समय, बचत समय र अघिल्लो दिनसम्मको तयारी
3. `notebooks/00_Setup/00_Environment_Setup.ipynb` — वातावरण सेटअप र जाँच (**पाठ समयबाहिर** गरिन्छ)

<!-- ne-section: ## 1.1 時間の考え方 -->
### नेपालीमा

स्वअध्ययन दिनको **360 मिनेट** (09:00–12:00 र 13:50–16:50) हो। त्यसमध्ये
**अनिवार्य सिकाइ र अभ्यास 270–300 मिनेट**, बाँकी **60–90 मिनेट** विश्राम, समस्या समाधान र बुझाउनमा
खर्च हुन्छ।

नोटबुकको लाग्ने समय **प्रारम्भिक अनुमान** हो। एक जना सुरुवाती प्रशिक्षार्थीसँगको pilot मा नापेपछि
मात्र निश्चित हुन्छ।

**अभ्यास 3 (विकास) ऐच्छिक** हो। सकिएको जाँचसूचीमा पर्दैन।

<!-- ne-section: ## 2. この研修で身につくこと -->
### नेपालीमा

५ दिनको अन्त्यमा तलका कुरा गर्न सक्ने हुनुहुनेछ।

| दिन | गर्न सक्ने |
|---|---|
| 1 | AI, मेसिन लर्निङ, डिप लर्निङको फरक बुझाउने। चित्र सङ्ख्याको तालिका हो भनेर बुझाएर आफैं बदल्ने। |
| 2 | Python मा निर्णय प्रोग्राम लेख्ने। OpenCV ले चित्र पढेर दुई-मान बनाउने र pixel लाई mm मा बदल्ने। |
| 3 | सिकिएको YOLO चलाएर नतिजा पढ्ने र threshold बदल्दा व्यवहार कसरी बदलिन्छ बुझाउने। |
| 4 | डेटासेट जाँच्ने, YOLO fine-tune गर्ने र परीक्षण डेटामा मूल्याङ्कन गर्ने। |
| 5 | PatchCore ले anomaly detection चलाएर YOLO सँग तुलना गर्ने र PVC निरीक्षणका लागि सिफारिस बनाउने। |

<!-- ne-section: ## 3. インストール -->
### नेपालीमा

आधिकारिक क्रमांकित प्रक्रिया [START_HERE.md](START_HERE.md) हो। Python 3.11 प्रयोग गरेर पाठ अघि
दुवै वातावरण, फोटो र weight तयार गर्नुहोस्। तल वातावरणको सारांश मात्र हो।

दुई virtual environment बनाइन्छ। **कारण अनिवार्य पढ्नुहोस्।**

| वातावरण | प्रयोग हुने दिन | मुख्य package |
|---|---|---|
| `.venv` | दिन 0–4 | numpy, matplotlib, opencv-python, torch, ultralytics |
| `.venv-anomalib` | दिन 5 | anomalib 2.7.0, torch, opencv-**headless** |

> **किन छुट्याउने?**
>
> `anomalib` ले `opencv-python-headless` चाहन्छ, `ultralytics` ले
> `opencv-python` चाहन्छ। एउटै वातावरणमा राख्दा `cv2` दुईवटा हुन्छन् र OpenCV बिग्रन्छ।
> यो आधिकारिक कागजातको dependency बाटै देखिने, छल्न नसकिने द्वन्द्व हो।

Windows को खोजमा "Command Prompt" (`cmd`) खोलेर
[START_HERE को स्टेप 1–8](START_HERE.md) क्रमैसँग चलाउनुहोस्।
ZIP, OneDrive र खाली ठाउँ भएको path को व्यवस्थापन, सक्रिय गर्ने र दुवै kernel दर्ता गर्ने कुरा त्यहीँ छ।
GPU अनिवार्य छैन। GPU wheel को संयोजन यो परिवर्तनमा जाँचिएको छैन।

**जाँचिएका संस्करण:** [`requirements/tested_versions.md`](requirements/tested_versions.md)

<!-- ne-section: ## 4. 素材（データ）の生成 -->
### नेपालीमा

कृत्रिम चित्र, चित्ररेखा र डेटासेट **Python ले बनाइन्छ**। सन्दर्भ फोटो र सिकिएका weight पाठ अघि
ल्याइन्छ।

बनाउने आदेश [START_HERE स्टेप 6](START_HERE.md) मा, र सन्दर्भ फोटो तथा weight लिने र अफलाइन जाँच
स्टेप 7 मा छ। सँगै दिइएका सन्दर्भ चित्र मूल अभिलेख भएका प्रशिक्षकले मात्र फेरि बनाउँछन्।

| नतिजा | सामग्री |
|---|---|
| `assets/diagrams/` | अवधारणा चित्र, क्यालिब्रेसन चित्र र सिकाइ चित्र |
| `assets/reference_outputs/` | वास्तविक चलाइका नतिजाबाट बनेका सन्दर्भ चित्र (स्रोत त्यही फोल्डरको `README.md` मा) |
| `assets/normal_samples/`, `assets/defect_samples/` | सामान्य र दोष नमुना (सही mask र निर्देशांक सहित) |
| `assets/yolo_dataset/` | 96 चित्र (train 64 / val 16 / test 16), लेबल, `data.yaml` |
| `assets/anomaly_dataset/pvc_sheet/` | सामान्य 44, असामान्य 40, सही mask |

`assets/diagrams/teach_*.png` र `assets/reference_outputs/ref_*.png` **वितरणमा समावेश हुन्छन्**
(`.gitignore` को अपवाद)। Python नचलाई पनि चित्र देखिन भनेर यसो गरिएको हो।
अरू बनाइएका सामग्री (डेटासेट, weight, सिकाइ नतिजा) पहिलेझैं Git मा राखिँदैन।

`generate_reference_outputs.py` मा सिकाइको चलाइबाट सुरक्षित नतिजा छैन भने **चित्र नबनाई कारण
देखाएर रोकिन्छ**। सङ्ख्या बनाएर भर्ने काम कहिल्यै गर्दैन।

> **महत्त्वपूर्ण**
>
> यी **कृत्रिम चित्र** हुन्। वास्तविक PVC को प्रकाशिक व्यवहार **पुनःउत्पादन गर्दैनन्**।
> वास्तविक कारखानाको चित्रमा जाँच हप्ता २ पछि मात्र गरिन्छ।
> कृत्रिम डेटामा पाइएको शुद्धतालाई उत्पादन निरीक्षणको शुद्धता भनेर उद्धृत गर्नु हुँदैन।

<!-- ne-section: ## 4.1 解説 PDF -->
### नेपालीमा

नोटबुकको व्याख्याबाट स्वतः बनाइएका पुस्तिका `docs/pdf/` मा छन्। अफलाइन पढ्नका लागि सहायक सामग्री
हुन्; अभ्यास भने नोटबुकमै गरिन्छ।

| फाइल | सामग्री |
|---|---|
| `docs/pdf/Day01_explanation_ja_en_ne.pdf` … `Day05_…` | प्रत्येक दिनको व्याख्या (जापानी → अङ्ग्रेजी → नेपाली) |
| `docs/pdf/Week1_explanation_ja_en_ne.pdf` | ५ दिनको एकै पुस्तिका |
| `docs/pdf/Setup_ja_en_ne.pdf` | तयारी नोटबुक |
| `docs/pdf/Installation_Guide_ja_en_ne.pdf` | स्थापना र समस्या समाधान |
| `docs/pdf/Repository_Guide_ja_en_ne.pdf` | रिपोजिटरी र संस्करणको परिचय |
| `docs/pdf/Course_Syllabus_ja_en_ne.pdf` | समयतालिका |
| `docs/pdf/README.md` | बनाउने तरिका, के पर्छ, के पर्दैन, सीमा |

अघिल्ला जापानी–अङ्ग्रेजी संस्करण (`*_ja_en.pdf`) पनि जस्ताको तस्तै राखिएका छन्, त्यसैले दुवै
पढ्न सकिन्छ। नयाँ त्रिभाषी संस्करण बनाउन Chromium (Playwright) चाहिन्छ; जापानी–अङ्ग्रेजी संस्करण
रिपोर्टल्याब (ReportLab) ले नै बन्छ।

```cmd
REM PDF generation and inspection only; not needed by learners.
".\.venv\Scripts\python.exe" -m pip install -r requirements\pdf.txt
".\.venv\Scripts\python.exe" -m playwright install chromium
".\.venv\Scripts\python.exe" assets\scripts\export_explanations_pdf.py
".\.venv\Scripts\python.exe" assets\scripts\export_trilingual_pdf.py
".\.venv\Scripts\python.exe" assets\scripts\inspect_pdf_pages.py --languages ja,ne
```

* चलाइको log, stack trace, लामो तयारी कोड र प्रशिक्षकका जवाफ पर्दैनन्।
* slider भएका ठाउँमा स्थिर चित्र र "नोटबुकमा चलाउनुहोस्" भन्ने टिप्पणी राखिन्छ।
* model download र सिकाइ फेरि गरिँदैन।
* फराकिला चित्र पढ्न सजिलो होस् भनेर A4 तेर्सो पानामा राखिन्छन्।

<!-- ne-section: ## 5. 起動 -->
### नेपालीमा

तयारी सकिएपछि File Explorer मा वास्तविक `AI_Vision_Training` खोलेर
ठेगाना बारमा `cmd` लेखेर Enter थिच्नुहोस्। त्यसपछि तलको आदेश चलाउनुहोस्।
वा त्यही फोल्डरको `start_training.cmd` डबल-क्लिक गर्नुहोस्।
सुरु गर्ने फाइलले install, download वा सिकाइ गर्दैन।

```cmd
.\.venv\Scripts\activate.bat
".\.venv\Scripts\python.exe" -m jupyter lab
```

सक्रिय गर्दा अर्को Python को Jupyter सुरु गर्ने फाइल छानिनबाट जोगाउँछ। यो CMD भित्र मात्र लागू हुन्छ।

ब्राउजर खुलेपछि `notebooks` → `00_Setup` → `00_Environment_Setup.ipynb` क्रममा खोल्नुहोस्।
**दिन ५ को नोटबुकमा मात्र** kernel `Python 3 (AI Vision Anomalib)` मा बदल्नुहोस्।

<!-- ne-section: ### 5.1 セルの指示 -->
### नेपालीमा

सबै कोड सेलको सुरुमा तलको एउटा चिन्ह हुन्छ।

| देखिने | अर्थ |
|---|---|
| `実行のみ / Run only` | **Shift + Enter** ले त्यसै चलाउने। नबदल्नुहोस् |
| `この値を変更 / Change this value` | मान बदलेर नतिजा अनुमान गरेपछि चलाउने |
| `自分でコードを書く / Write your code` | खाली ठाउँ आफैं भर्ने |

<!-- ne-section: ### 5.2 対話デモ -->
### नेपालीमा

५ वटा छोटा अन्तरक्रियात्मक demo छन्। **slider सार्न चलिरहेको kernel चाहिन्छ।**

| ठाउँ | के सार्ने |
|---|---|
| `Day01_02` Part 3 | RGB का तीन मान |
| `Day02_02` Part 2 | loop को step (एक-एक) |
| `Day02_03` Part 2 | OpenCV को threshold |
| `Day03_01` Part 3 | अनुमान गरिएको चौकोणको स्थान (IoU) |
| `Day03_03` Part 1 | YOLO को confidence |
| `Day05_03` Part 4 | PatchCore को threshold (**क्यालिब्रेसन डेटा मात्र**) |

> GitHub preview वा स्थिर HTML मा slider चल्दैन।
> हरेक demo मा **widget नचाहिने parameter सेल** छ, जसले उही प्रयोग गर्न दिन्छ।

<!-- ne-section: ## 6. 検証とテスト -->
### नेपालीमा

तयार भइसकेको आधारभूत वातावरण सक्रिय गरेको CMD मा चलाउनुहोस्
([START_HERE](START_HERE.md) हेर्नुहोस्)।

```cmd
REM Check the environment.
python assets\scripts\verify_environment.py --profile all

REM Structural validation (fast).
python assets\scripts\validate_notebooks.py
```

थप जाँच र मर्मतका आदेश तल छन्। सामान्य विद्यार्थीले संरचनात्मक जाँचपछि पाठमा जान सक्छन्।
`--execute lightweight` र `check_widgets.py` ले नोटबुक चलाउँछन्; संरचनात्मक जाँच मात्र चाहिएको
अवस्थामा यी नचलाउनुहोस्। `scaffold_notebooks.py` ले नोटबुक बदल्छ र मर्मतकर्ताका लागि मात्र हो।

```cmd
REM Execute the lightweight notebooks.
python assets\scripts\validate_notebooks.py --execute lightweight

REM Automated asset and dataset tests.
python -m pytest assets\tests -v

REM Check language labels without writing.
python assets\scripts\normalize_language_labels.py --check

REM Re-apply cell instruction banners (maintainers only; writes notebooks).
python assets\scripts\scaffold_notebooks.py

REM Check widget rendering.
python assets\scripts\check_widgets.py
```

`assets/scripts/validate_notebooks.py --execute all` मा **model download** र **सिकाइ** पर्ने हुनाले
धेरै समय लाग्छ।

`check_widgets.py` ले नोटबुक चलाएर `widgets.interact` प्रयोग गर्ने सेलले widget देखाएको छ कि छैन
जाँच्छ। ब्राउजरमा वास्तवमा क्लिक गरेर जाँच्ने काम छुट्टै हो।

<!-- ne-section: ## 7. フォルダ構成 -->
### नेपालीमा

```text
AI_Vision_Training/
├── README.md                     <- यही फाइल
├── START_HERE.md                 <- एकदमै सुरुवाती तहको प्रक्रिया
├── COURSE_SYLLABUS.md            <- ५ दिनको समयतालिका
├── requirements/                 <- जाँचिएका संस्करण
├── notebooks/                    <- 16 नोटबुक (00_Setup र दिन 1–5)
├── assets/                       <- चित्र, नमुना, डेटासेट, स्क्रिप्ट, test
├── docs/                         <- PDF, प्रशिक्षक मार्गदर्शन, समस्या समाधान, सन्दर्भ
├── submissions/                  <- दिनअनुसार बुझाउने काम
└── training_results/             <- सिकाइको नतिजा (Git मा पर्दैन)
```

<!-- ne-section: ## 8. 提出物 -->
### नेपालीमा

हरेक दिन `submissions/day0N/` मा तलका ४ कुरा राख्नुहोस्।

1. चलाइएको नोटबुक (`File` → `Save`)
2. `Day0N_Report_Template.md` भरेको
3. सुरक्षित गरेका चित्र, CSV, JSON
4. त्रुटि आए त्यसको सन्देश र प्रयास गरेका कुरा

प्रशिक्षकका नमुना जवाफ `docs/instructor/` मा छन्। **पहिले आफैं लेख्नुहोस्।**

<!-- ne-section: ## 9. 困ったとき -->
### नेपालीमा

पहिले तलको क्रममा जाँच्नुहोस्।

1. प्रत्येक नोटबुकको अन्त्यमा भएको "समस्या आउँदा" तालिका
2. [`docs/troubleshooting/installation.md`](docs/troubleshooting/installation.md)
3. `python assets\scripts\verify_environment.py --profile all`

<!-- ne-section: ## 10. 既知の制限 -->
### नेपालीमा

| सीमा | कारण |
|---|---|
| कृत्रिम चित्र मात्र | वास्तविक PVC चित्र अझै उपलब्ध छैन |
| CPU का लागि सानो सेटिङ | तालिमका PC मा GPU छैन भन्ने मान्यता |
| सिकाइ चित्र 64 वटा | एक दिनमा सकिने मात्रा राखिएको |
| PatchCore को मूल्याङ्कन डेटा आधा | validation र test मा बाँड्न |
| YOLO र PatchCore छुट्टै वातावरण | OpenCV को द्वन्द्व (माथिको खण्ड 3) |
| PDF भित्रको चित्रका अक्षर खोज्न मिल्दैन | चित्रलाई image को रूपमा राखिएको |
| PDF मा चलाइको log पर्दैन | output वातावरणअनुसार फरक पर्ने |

माथिका सबै सीमा जानाजान अपनाइएका र अभिलेख गरिएका हुन्; कुनै पनि बिग्रिएको भाग लुकाउने उपाय होइन।
वास्तविक उत्पादनमा सम्भव छ कि छैन भन्ने कुरा वास्तविक चित्र, स्थिर क्यामेरा र उज्यालोको डिजाइन, र
थाहा भएका राम्रा उत्पादनमा threshold अध्ययनमा निर्भर छ — यी सबै हप्ता २ का विषय हुन्।

<!-- ne-section: ## 11. ライセンスと出所 -->
### नेपालीमा

यो तालिममा प्रयोग हुने बाह्य सामग्रीको स्रोत र लाइसेन्स
[`assets/external_samples/PROVENANCE.md`](assets/external_samples/PROVENANCE.md) मा अभिलेख छ।

**महत्त्वपूर्ण:** सिकाइका लागि प्रयोग गर्दा समस्या छैन, तर
**Ultralytics का model र कोड AGPL-3.0** हुन्। उत्पादनमा समावेश गर्नुअघि
लाइसेन्स जाँच नगरी अगाडि नबढ्नुहोस्।
