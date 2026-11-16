<!--
नेपाली अनुवाद / Nepali translation source for
docs/troubleshooting/installation.md

Sections are keyed on a distinctive part of their heading line.
-->
# installation troubleshooting — नेपाली अनुवाद

<!-- ne-doc: docs/troubleshooting/installation.md -->

<!-- ne-section: Installation troubleshooting -->
### नेपालीमा

setup गर्दा अल्झियो भने यो प्रक्रिया-पुस्तिका हेर्नुहोस्।
**माथिबाट क्रमैसँग** जाँच्नुहोस्। आधिकारिक तयारी प्रक्रिया
[START_HERE](../../START_HERE.md) हो।

<!-- ne-section: ## 0. -->
### नेपालीमा

केही अनौठो लाग्यो भने पहिले वातावरण जाँच्नुहोस्।

File Explorer मा वास्तविक सामग्री फोल्डर खोलेर ठेगाना बारमा `cmd` लेखेर Enter थिच्नुहोस्।
तलका आदेश त्यही Command Prompt मा चलाउनुहोस्। अहिलेको ठाउँ `cd` ले, भित्री सामग्री `dir` ले
देखाउँछ। ZIP वा OneDrive भए पनि वास्तविक निकालेको ठाउँ प्रयोग गर्नुहोस्।

```cmd
.\.venv\Scripts\activate.bat
where python
python -c "import sys; print(sys.executable)"
python assets\scripts\verify_environment.py --profile all
```

दिन ५ मा नयाँ CMD झ्यालमा `.venv-anomalib` सक्रिय गरेर उही जाँच गर्नुहोस्।
यो जाँचले चलाएको वातावरण मात्र हेर्छ।

देखाइको अर्थ यसरी पढ्नुहोस्।

| देखिने | अर्थ | के गर्ने |
|---|---|---|
| `Virtual env : YES / はい` | virtual environment सक्रिय छ | ठीक छ |
| `Virtual env : NO` | **virtual environment सक्रिय छैन** | तलको खण्ड 1 |
| `[MISSING] numpy ...` | package नपुग | तलको खण्ड 3 |
| `[MISS] ... assets` | सामग्री बनेको छैन | तलको खण्ड 6 |
| `READY` | तयार छ | अगाडि बढ्नुहोस् |

<!-- ne-section: ## 1. -->
### नेपालीमा

सामग्री फोल्डरको CMD मा `dir .venv\Scripts\python.exe` चलाउनुहोस्।
छैन भने [START_HERE स्टेप 3](../../START_HERE.md) को बनाउने प्रक्रियामा फर्कनुहोस्।
छ भने `.\.venv\Scripts\activate.bat` ले सक्रिय गर्नुहोस्। सफल भए `(.venv)` देखिन्छ।
execution policy वा प्रशासक अधिकार परिवर्तन आवश्यक छैन। संस्थाको बन्देज भए IT सँग सोध्नुहोस्।

सक्रिय नगरी चलाउने तरिका पनि छ। त्यस अवस्थामा `deactivate` आवश्यक छैन।

```cmd
".\.venv\Scripts\python.exe" assets\scripts\verify_environment.py --profile all
".\.venv-anomalib\Scripts\python.exe" assets\scripts\verify_environment.py --profile all
```

<!-- ne-section: ## 2. -->
### नेपालीमा

**कारण:** Windows को "app execution alias" ले `python.exe` लाई अगाडि छेक्छ।

**के गर्ने:**

1. Windows Settings खोल्नुहोस्
2. "Apps" → "App execution aliases"
3. `python.exe` र `python3.exe` **बन्द** गर्नुहोस्
4. Command Prompt **बन्द गरेर फेरि खोल्नुहोस्**

त्यसपछि पनि नमिले Python PATH मा छैन।
[python.org](https://www.python.org/downloads/) को installer चलाएर पहिलो स्क्रिनमा
"**Add python.exe to PATH**" मा चिन्ह लगाएर "Install Now" थिच्नुहोस्।

<!-- ne-section: ## 3. `ModuleNotFoundError: No module named 'numpy'` -->
### नेपालीमा

**कारण २ वटा छन्:**

<!-- ne-section: ### 3.1 -->
### नेपालीमा

नोटबुकले अर्को Python प्रयोग गरिरहेको छ।

**के गर्ने:**

1. नोटबुकको माथि-दायाँको kernel नाममा क्लिक गर्नुहोस्
2. `Python 3 (AI Vision)` छान्नुहोस्
3. `Kernel` → `Restart Kernel and Run All Cells` गर्नुहोस्

**जाँच:** अर्को सेलको output मा `.venv` छ कि हेर्नुहोस्।

```python
import sys
print(sys.executable)
```

<!-- ne-section: ### 3.2 -->
### नेपालीमा

```cmd
.\.venv\Scripts\activate.bat
python -m pip install -r requirements\base.txt
python -m ipykernel install --user --name aivision --display-name "Python 3 (AI Vision)"
```

`ipykernel install` बिर्सियो भने Jupyter बाट वातावरण देखिँदैन। **अनिवार्य रूपमा चलाउनुहोस्।**

<!-- ne-section: ## 4. -->
### नेपालीमा

**कारण:** network को क्षणिक असफलता, वा कम्पनीको proxy।

**के गर्ने:**

1. **उही आदेश फेरि चलाउनुहोस्** (सबैभन्दा प्रभावकारी)
2. त्यसपछि पनि नभए proxy मिलाउनुहोस्

तलका ठेगाना **काल्पनिक उदाहरण** हुन्, कम्पनीको वास्तविक सेटिङ होइन। IT ले पुष्टि गरेको मानले
बदलेर मात्र चलाउनुहोस्। `set` ले यो CMD झ्याल र त्यसबाट सुरु गरिएका प्रोग्राममा मात्र असर गर्छ।
झ्याल बन्द गरे सेटिङ हराउँछ। पहिलेको ठीक सेटिङलाई उदाहरणको मानले नबदल्नुहोस्।

```cmd
set "HTTP_PROXY=http://proxy.example.co.jp:8080"
set "HTTPS_PROXY=http://proxy.example.co.jp:8080"
python -m pip install -r requirements\base.txt
```

proxy को ठेगाना सूचना प्रणाली विभागसँग सोध्नुहोस्।

3. कम्पनीको mirror छ भने `--index-url` दिनुहोस्:

तलको mirror पनि उदाहरण हो। वास्तविक URL IT सँग सोध्नुहोस्।

```cmd
python -m pip install -r requirements\base.txt --index-url https://pypi.example.co.jp/simple
```

<!-- ne-section: ## 5. -->
### नेपालीमा

**लक्षण:** रङ उल्टो देखिन्छ, `cv2` अस्थिर हुन्छ, `findContours` को नतिजा फरक आउँछ।

**कारण:** `opencv-python` र `opencv-python-headless` **छुट्टै package** हुन्, तर दुवैले `cv2`
दिन्छन्। **एउटै वातावरणमा दुवै राख्दा बिग्रन्छ।**

**जाँच:**

```cmd
.\.venv\Scripts\activate.bat
python -m pip list | findstr /I opencv
```

**एक लाइन मात्र** देखिनु ठीक हो। दुई लाइन देखियो भने बिग्रेको छ।

**के गर्ने:**

```cmd
REM .venv (Days 0-4); direct interpreter, no activation needed.
".\.venv\Scripts\python.exe" -m pip uninstall -y opencv-python opencv-python-headless opencv-contrib-python
".\.venv\Scripts\python.exe" -m pip install opencv-python==4.12.0.88
```

```cmd
REM .venv-anomalib (Day 5); direct interpreter, no activation needed.
".\.venv-anomalib\Scripts\python.exe" -m pip uninstall -y opencv-python opencv-python-headless opencv-contrib-python
".\.venv-anomalib\Scripts\python.exe" -m pip install opencv-python-headless==4.12.0.88
```

दुई वातावरण नमिसाउनुहोस्। install गर्नुअघि prompt (`(.venv)` वा `(.venv-anomalib)`) मा कुन
वातावरण चलिरहेको छ अनिवार्य जाँच्नुहोस्।

<!-- ne-section: ## 6. -->
### नेपालीमा

**लक्षण:** `FileNotFoundError`, `画像がありません`, `data.yaml がありません`।

**के गर्ने:**

```cmd
.\.venv\Scripts\activate.bat
python assets\scripts\generate_training_assets.py
python assets\scripts\prepare_datasets.py
```

सामान्यतः पहिलेको डेटा नै पुनः प्रयोग हुन्छ। जानाजान फेरि बनाउने हो भने मात्र प्रशिक्षकसँग सल्लाह
गर्नुहोस्।

<!-- ne-section: ### 6.1 -->
### नेपालीमा

**लक्षण:** `assets/external_samples/open_reference/` मा ४ वटा पुगेका छैनन्, वा
"参考画像がそろっていません / reference images are incomplete" देखिन्छ।

**के गर्ने:**

```cmd
.\.venv\Scripts\activate.bat
python assets\scripts\download_reference_images.py --course-root .
```

- ल्याइने **सन्दर्भ चित्र ४ वटा मात्र** हुन् (`chelsea.png`, `camera.png`, `brick.png`,
  `VisA_samples.png`)।
- जति पटक चलाए पनि ठीक सुरक्षित भइसकेका फाइल त्यसै प्रयोग हुन्छन् (ल्याउने काम एक पटक मात्र)।
- असफल भएको फाइलको नाम देखिन्छ। **अर्को चित्रले नबदल्नुहोस्।** जडान जाँचेर उही आदेश फेरि
  चलाउनुहोस्।
- network प्रयोग नगरी सुरक्षित फाइल मात्र जाँच्न सकिन्छ।

```cmd
python assets\scripts\download_reference_images.py --course-root . --offline
```

<!-- ne-section: ## 7. -->
### नेपालीमा

पाठ अघि लिने र अफलाइन जाँच गर्ने काम [START_HERE.md](../../START_HERE.md) को स्टेप 7 हो।
`preload_models.py` ले YOLO को weight र bus को उदाहरण, र Anomalib को resnet18 cache जाँच्छ।
`--offline` ले network मा जोडिँदैन र नपुग भएको कुरा त्रुटिका रूपमा बताउँछ।

**लक्षण:** `URLError`, `TimeoutError`, `yolo26n.pt` लिन सकिएन।

**के गर्ने (यही क्रममा):**

1. **उही सेल फेरि चलाउनुहोस्**
2. ब्राउजरबाट लिनुहोस्:

```text
https://github.com/ultralytics/assets/releases
```

`yolo26n.pt` (करिब 5 MB) डाउनलोड गरेर `assets\models\` मा राख्नुहोस्।

3. कम्पनीको proxy छ भने व्यवस्थापकसँग जाँच्नुहोस्

**लिन नसकेको बेला मिल्दोजुल्दो नतिजा बनाउनु हुँदैन।**
त्रुटि जस्ताको तस्तै अभिलेख गरेर प्रशिक्षकसँग सल्लाह गर्नुहोस्।

<!-- ne-section: ## 8. -->
### नेपालीमा

दिन ५ को नोटबुक **`aivision-anomalib` kernel** मा चलाउनुहोस्।
`anomalib` `.venv` मा **छैन** (जानाजान छुट्याइएको)।

**के गर्ने:**

अझै बनाइएको छैन भने [START_HERE स्टेप 4–5](../../START_HERE.md) चलाउनुहोस्।
पहिलेको वातावरण सुधार्न सक्रिय नगरी त्यसको Python सिधै दिन सकिन्छ।

```cmd
".\.venv-anomalib\Scripts\python.exe" -m pip install -r requirements\anomalib.txt
".\.venv-anomalib\Scripts\python.exe" -m ipykernel install --user --name aivision-anomalib --display-name "Python 3 (AI Vision Anomalib)"
```

<!-- ne-section: ## 9. `OSError: Error loading -->
### नेपालीमा

**कारण:** `torch==2.10.0` को Windows wheel यो वातावरणमा import हुन सकेन।

**के गर्ने:**

```cmd
".\.venv-anomalib\Scripts\python.exe" -m pip uninstall -y torch torchvision
".\.venv-anomalib\Scripts\python.exe" -m pip install torch==2.15.0 torchvision==0.29.2
```

त्यसपछि पनि नभए Microsoft Visual C++ Redistributable फेरि राख्नुहोस्।

<!-- ne-section: ## 10. -->
### नेपालीमा

**लक्षण:** `MemoryError`, `CUDA out of memory`, PC अत्यधिक ढिलो हुन्छ।

| अवस्था | के गर्ने |
|---|---|
| YOLO को सिकाइ | `BATCH` 8 → 4, `IMGSZ` 320 → 224 |
| PatchCore को सिकाइ | `train_batch_size` र `eval_batch_size` 4 बनाउने |
| नोटबुक सामान्य | अरू अनुप्रयोग बन्द गर्ने |

<!-- ne-section: ## 11. -->
### नेपालीमा

slider **चलिरहेको kernel** मा मात्र चल्छ। GitHub preview वा स्थिर HTML मा चल्दैन। त्यो बिग्रेको होइन।

| लक्षण | कारण | के गर्ने |
|---|---|---|
| केही देखिँदैन | `ipywidgets` छैन | `python -m pip install -r requirements\base.txt` चलाएर kernel restart गर्ने |
| `ipywidgets が見つかりません` देखिन्छ | उही | तलको "parameter सेल" मा उही प्रयोग गर्न सकिन्छ |
| slider देखिन्छ तर चित्र बदलिँदैन | kernel पुरानो छ | **Kernel → Restart & Run All** |
| अघिल्लो चित्र थपिँदै जान्छ | output मेटिएको छैन | त्यो सेलको output मेटाएर फेरि चलाउने |

`ipywidgets` **अनिवार्य छैन**। हरेक demo मा widget नचाहिने "parameter सेल" तयार छ।
समय कम भए त्यही प्रयोग गर्नुहोस्।

<!-- ne-section: ## 12. -->
### नेपालीमा

तलका ४ कुरा टिपेर प्रशिक्षकलाई भन्नुहोस्। यी भए समस्या छिटो समाधान हुन्छ।

1. **कुन नोटबुकको कुन सेल** (`In [ ]` को नम्बर भए पनि हुन्छ)
2. **त्रुटि सन्देश** (अन्तिम ३ लाइन कपी)
3. `python assets\scripts\verify_environment.py --profile all` को output
4. **पहिले प्रयास गरेका कुरा** र तिनको नतिजा

CMD को `where python` र दुवै वातावरणको छुट्टै जाँच नतिजा पनि संलग्न गर्नुहोस्।
proxy को प्रमाण (credential) वा गोप्य जानकारी नटाँस्नुहोस्।
