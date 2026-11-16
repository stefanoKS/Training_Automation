<!--
नेपाली अनुवाद / Nepali translation source for
START_HERE.md

Each block is keyed on the exact heading line it belongs to; the Nepali text is appended at the end
of that section. Commands, paths and file names stay byte-identical.
-->
# START_HERE — नेपाली अनुवाद

<!-- ne-doc: START_HERE.md -->

<!-- ne-section: ## ステップ 1　取得してフォルダを開く / Download and open the folder -->
### नेपालीमा

यो Windows 11 / Command Prompt (cmd.exe) को **आधिकारिक तयारी प्रक्रिया** हो। दिन १ भन्दा अघि, पाठ
समयबाहिर माथिबाट क्रमैसँग पूरा गर्नुहोस्। installation सकिएपछि तयारी नोटबुक खोल्नुहोस्।

Windows को खोजमा "Command Prompt" वा `cmd` खोलेर सुरु गर्नुहोस्। File Explorer मा फोल्डर खोलेर
ठेगाना बारमा `cmd` लेखेर Enter थिच्दा पनि खुल्छ। प्रशासक (Administrator) बन्नु आवश्यक छैन।

GitHub को Code → Download ZIP निकाल्नुहोस्, वा Git छ भने तलको आदेश चलाउनुहोस्।

```cmd
cd /d "%USERPROFILE%\Documents"
git clone https://github.com/stefanoKS/Training_Automation.git
cd /d "%USERPROFILE%\Documents\Training_Automation\AI_Vision_Training"
dir
```

ZIP भए निकालेको `AI_Vision_Training` फोल्डरमा जानुहोस्। अबका सबै आदेश `README.md` र `requirements`
भएको यही फोल्डरमा चलाउनुहोस्।

Documents OneDrive जस्तो अन्य ठाउँमा सारिएको छ भने वास्तविक निकालेको ठाउँ प्रयोग गर्नुहोस्।
`cd /d "<actual extracted AI_Vision_Training path>"` मा <> भित्रको भाग उदाहरण मात्र हो; जस्ताको
तस्तै नचलाई वास्तविक path ले बदल्नुहोस्। उदाहरण:

```cmd
cd /d "D:\Training Materials\Training_Automation\AI_Vision_Training"
dir
cd
```

`dir` ले भित्री सामग्री देखाउँछ, argument नभएको `cd` ले अहिलेको ठाउँ देखाउँछ। खाली ठाउँ भएको path पनि
quote भित्र राख्नुहोस्।

<!-- ne-section: ## ステップ 2　Python 3.11 を確認する / Check Python 3.11 -->
### नेपालीमा

```cmd
py -3.11 --version
```

जाँचिएको series **Python 3.11** हो। 3.12 जस्ता अन्य series जाँचिएका छैनन्।
विस्तृत कुरा [tested_versions.md](requirements/tested_versions.md) मा छ।
`py` छैन भने python.org बाट Python 3.11 राखेर Add python.exe to PATH छान्नुहोस् र Command Prompt फेरि
खोल्नुहोस्। `python --version` ले 3.11 देखायो भने अबका `py -3.11` लाई `python` ले बदल्न सकिन्छ।

<!-- ne-section: ## ステップ 3　基本環境を作る / Create the base environment -->
### नेपालीमा

virtual environment भनेको तालिमका लागि छुट्ट्याइएको औजार-बाकस हो। अर्को कामको Python सँग मिसिँदैन।

```cmd
py -3.11 -m venv .venv
.\.venv\Scripts\activate.bat
where python
python -c "import sys; print(sys.executable)"
python -m pip install --upgrade pip
python -m pip install -r requirements\base.txt
python -m pip install -r requirements\yolo.txt
```

देखिएको Python को पहिलो ठेगाना यही फोल्डरको `.venv\Scripts\python.exe` हो कि जाँच्नुहोस्।
सक्रिय (activate) गर्न नसकिए `python` को सट्टा `".\.venv\Scripts\python.exe"` प्रयोग गर्नुहोस्।
उदाहरण: `".\.venv\Scripts\python.exe" -m pip install -r requirements\base.txt`।
CMD सक्रिय गर्न execution policy परिवर्तन आवश्यक छैन। संस्थाको बन्देज छ भने प्रशिक्षक/IT सँग सोध्नुहोस्।

<!-- ne-section: ## ステップ 4　Anomalib 環境を作る / Create the Anomalib environment -->
### नेपालीमा

दिन ५ मा अर्को औजार-बाकस प्रयोग गरिन्छ। **मानक प्रक्रियामा दिन १ भन्दा अघि दुवै तयार गरिन्छ।**

```cmd
deactivate
py -3.11 -m venv .venv-anomalib
.\.venv-anomalib\Scripts\activate.bat
where python
python -c "import sys; print(sys.executable)"
python -m pip install --upgrade pip
python -m pip install -r requirements\anomalib.txt
deactivate
```

सक्रिय नगरी सिधै Python प्रयोग गरिरहेको छ भने `deactivate` आवश्यक छैन। दिन ५ का लागि `python` को सट्टा
`".\.venv-anomalib\Scripts\python.exe"` प्रयोग गर्नुहोस्।

<!-- ne-section: ## ステップ 5　両方のカーネルを登録する / Register both kernels -->
### नेपालीमा

kernel भनेको नोटबुकको कोड चलाउने Python हो।

```cmd
".\.venv\Scripts\python.exe" -m ipykernel install --user --name aivision --display-name "Python 3 (AI Vision)"
".\.venv-anomalib\Scripts\python.exe" -m ipykernel install --user --name aivision-anomalib --display-name "Python 3 (AI Vision Anomalib)"
```

<!-- ne-section: ## ステップ 6　教材とデータを作る / Generate teaching assets and datasets -->
### नेपालीमा

यहाँबाट सक्रिय नगरी **आधारभूत वातावरण `.venv` को Python सिधै** दिनुहोस्। `--force` वा `--clean`
आवश्यक छैन। बुझाइसकेका काम वा सुरक्षित model नतिजा फेरि बनाइँदैन।

```cmd
".\.venv\Scripts\python.exe" assets\scripts\generate_training_assets.py
".\.venv\Scripts\python.exe" assets\scripts\prepare_datasets.py
".\.venv\Scripts\python.exe" assets\scripts\generate_teaching_diagrams.py
".\.venv\Scripts\python.exe" assets\scripts\generate_svg_figures.py
```

<!-- ne-section: ## ステップ 7　オフライン授業の素材を先に取得する / Preload offline lesson inputs -->
### नेपालीमा

सन्दर्भ फोटो लाइसेन्स भएका मूल फाइल हुन्। कृत्रिम चित्र वा कारखानाको मापन नतिजा होइनन्।
model को weight पनि पाठ अघि ल्याइन्छ। पहिलो पटक network चाहिन्छ।

```cmd
".\.venv\Scripts\python.exe" assets\scripts\download_reference_images.py --course-root .
".\.venv\Scripts\python.exe" assets\scripts\preload_models.py --profile yolo
".\.venv-anomalib\Scripts\python.exe" assets\scripts\preload_models.py --profile anomalib
".\.venv\Scripts\python.exe" assets\scripts\download_reference_images.py --course-root . --offline
".\.venv\Scripts\python.exe" assets\scripts\preload_models.py --profile yolo --offline
".\.venv-anomalib\Scripts\python.exe" assets\scripts\preload_models.py --profile anomalib --offline
```

weight को वितरण र प्रयोगका सर्त दिने निकाय (Ultralytics / timm / torchvision) बाट जाँच्नुहोस्।
लिन असफल भए पाठ अघि प्रशिक्षकलाई खबर गर्नुहोस्। दिइएका सन्दर्भ नतिजा `assets/reference_outputs/`
मा छन्; प्रशिक्षार्थीले चलाएर सुरक्षित गर्ने नतिजा `submissions/` मा जान्छ।

<!-- ne-section: ## ステップ 8　環境と教材を確認する / Verify environments and assets -->
### नेपालीमा

`--profile all` ले **चलाइएको वातावरण मात्र** जाँच्छ। दुवैमा चलाउनुहोस्।

```cmd
".\.venv\Scripts\python.exe" assets\scripts\verify_environment.py --profile all
".\.venv-anomalib\Scripts\python.exe" assets\scripts\verify_environment.py --profile all
".\.venv\Scripts\python.exe" assets\scripts\validate_notebooks.py
".\.venv\Scripts\python.exe" -m jupyter kernelspec list
```

exit code 0 सँगै देखाइएको सामग्रीको सूचीमा कुनै नपुग भाग नभएको पनि जाँच्नुहोस्।

<!-- ne-section: ## ステップ 9　JupyterLab を起動する / Launch JupyterLab -->
### नेपालीमा

आधारभूत वातावरण सक्रिय गरेपछि मात्र सुरु गर्नुहोस्। अर्को Python को `jupyter-lab` छानिनबाट जोगाउँछ।
परिवर्तन यो CMD झ्यालमा मात्र लागू हुन्छ।

```cmd
.\.venv\Scripts\activate.bat
".\.venv\Scripts\python.exe" -m jupyter lab
```

दैनिक सुरु गर्न यही फोल्डरको `start_training.cmd` डबल-क्लिक गरे पनि उही हुन्छ।
यो सुरु गर्ने फाइलले तयार भइसकेको वातावरण प्रयोग गर्छ मात्र; install, सामग्री लिने वा train गर्ने काम
गर्दैन।

ब्राउजर नखुले देखाइएको localhost URL खोल्नुहोस्। `notebooks` → `00_Setup` →
`00_Environment_Setup.ipynb` खोलेर `Python 3 (AI Vision)` छान्नुहोस्। दिन ५ मा मात्र
`Python 3 (AI Vision Anomalib)` छानिन्छ।

<!-- ne-section: ## ステップ 10　準備完了を確認する / Complete preflight -->
### नेपालीमा

दिन १ भन्दा अघि तयारी नोटबुक माथिबाट क्रमैसँग चलाउनुहोस्। जानाजान राखिएको त्रुटिको अभ्यास व्याख्याअनुसार
सुधार्नुहोस्। दिन १ को 09:00–09:10 तयार भइसकेको अवस्था पुनः जाँच्ने समय हो, installation को समय होइन।

- [ ] दुवै kernel छान्न सकिन्छ
- [ ] दुवै वातावरणको जाँच सफल भयो, सामग्रीमा कुनै नपुग छैन
- [ ] अफलाइन फोटो र weight को जाँच सफल भयो
- [ ] Day01_02 Part 1 मा चित्र देखिन्छ
- [ ] चित्रको जापानी अक्षर वर्गमा परिणत भएको छैन
- [ ] `submissions/day00/` मा तयारी रिपोर्ट सुरक्षित गरियो

समयमै नभ्याए [COURSE_SYLLABUS.md](COURSE_SYLLABUS.md) को पुनःस्थापन प्रक्रिया प्रयोग गर्नुहोस्।

<!-- ne-section: ## ステップ 11　授業を始める / Start lessons -->
### नेपालीमा

सेल छानेर Shift+Enter, सुरक्षित गर्न Ctrl+S। सेल माथिबाट क्रमैसँग चलाउनुहोस्।
मान kernel मा रहन्छ। क्रम बिर्सियो भने Kernel → Restart Kernel and Run All Cells प्रयोग गर्नुहोस्।
भोलिको दिन स्टेप 1 को फोल्डरमा गएर स्टेप 9 बाट सुरु गर्नुहोस्। वातावरण फेरि बनाइँदैन।
सक्दा सुरक्षित गरेर ब्राउजर बन्द गर्नुहोस्, र Command Prompt मा Ctrl+C थिचेर रोकिएको पुष्टि गर्नुहोस्।

<!-- ne-section: ### 例外：第4日後の Anomalib 準備 / Alternative: Anomalib setup after Day 4 -->
### नेपालीमा

प्रशिक्षकले स्पष्ट अनुमति दिएको अवस्थामा मात्र स्टेप 4 र Anomalib को दर्ता, weight लिने र जाँच दिन ४
पछि सार्न सकिन्छ। त्यस अवस्थामा दिन १ को जाँच आधारभूत वातावरणमा मात्र हुन्छ र **पूरै तालिम तयार छ**
भन्न मिल्दैन। दिन ५ अघि बाँकी काम पूरा गर्नुहोस्। यो मानक दुवै-वातावरण जाँचसूचीभन्दा छुट्टै अपवाद हो।

<!-- ne-section: ### 困ったとき / Troubleshooting -->
### नेपालीमा

| लक्षण | के गर्ने |
|---|---|
| `python` / `py` छैन | स्टेप 2। PATH र app execution aliases जाँच्नुहोस् |
| package नपुग | सही वातावरणमा requirements राख्नुहोस् |
| kernel फरक छ | Python सेलमा `import sys; print(sys.executable)` जाँच्नुहोस् |
| सक्रिय गर्न मनाही छ | स्टेप 3 को सिधै चलाउने तरिका प्रयोग गर्नुहोस् |
| weight छैन | स्टेप 7 फेरि चलाएर असफलता अभिलेख गर्नुहोस् |

Command Prompt को `python -m pip` र नोटबुकका लागि मात्रको Jupyter `%pip` फरक कुरा हुन्।
पाठ चलिरहँदा स्वतः install गरिँदैन। विस्तृत कुरा
[installation.md](docs/troubleshooting/installation.md) मा छ।
