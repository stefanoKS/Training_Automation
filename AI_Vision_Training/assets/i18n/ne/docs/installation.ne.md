<!--
Nepali anuwad / Nepali translation source for
docs/troubleshooting/installation.md

Sections are keyed on a distinctive part of their heading line.
-->
# installation troubleshooting — Nepali anuwad

<!-- ne-doc: docs/troubleshooting/installation.md -->

<!-- ne-section: Installation troubleshooting -->
### Nepali ma

setup garda aljhiyo bhane yo prakriya-pustika hernuhos.
**mathibat kramaisang** jaanchnuhos. adhikarik tayari prakriya
[START_HERE](../../START_HERE.md) ho.

<!-- ne-section: ## 0. -->
### Nepali ma

kehi anautho lagyo bhane pahile batabaran jaanchnuhos.

File Explorer ma bastabik samagri folder kholer thegana barama `cmd` lekher Enter thichnuhos.
talaka adesh tyahi Command Prompt ma chalaunuhos. ahileko thaun `cd` le, bhitri samagri `dir` le
dekhaunchha. ZIP wa OneDrive bhae pani bastabik nikaleko thaun prayog garnuhos.

```cmd
.\.venv\Scripts\activate.bat
where python
python -c "import sys; print(sys.executable)"
python assets\scripts\verify_environment.py --profile all
```

din 5 ma nayan CMD jhyalama `.venv-anomalib` sakriya garera uhi jaanch garnuhos.
yo jaanchle chalaeko batabaran matra herchha.

dekhaiko arth yasari padhnuhos.

| dekhine | arth | ke garne |
|---|---|---|
| `Virtual env : YES / はい` | virtual environment sakriya chha | thik chha |
| `Virtual env : NO` | **virtual environment sakriya chhaina** | talako khand 1 |
| `[MISSING] numpy ...` | package napug | talako khand 3 |
| `[MISS] ... assets` | samagri baneko chhaina | talako khand 6 |
| `READY` | tayar chha | agadi badhnuhos |

<!-- ne-section: ## 1. -->
### Nepali ma

samagri folderko CMD ma `dir .venv\Scripts\python.exe` chalaunuhos.
chhaina bhane [START_HERE step 3](../../START_HERE.md) ko banaune prakriyama pharkanuhos.
chha bhane `.\.venv\Scripts\activate.bat` le sakriya garnuhos. saphal bhae `(.venv)` dekhinchha.
execution policy wa prashasak adhikar paribartan aawashyak chhaina. sansthako bandej bhae IT sang sodhnuhos.

sakriya nagari chalaune tarika pani chha. tyas abastha ma `deactivate` aawashyak chhaina.

```cmd
".\.venv\Scripts\python.exe" assets\scripts\verify_environment.py --profile all
".\.venv-anomalib\Scripts\python.exe" assets\scripts\verify_environment.py --profile all
```

<!-- ne-section: ## 2. -->
### Nepali ma

**karan:** Windows ko "app execution alias" le `python.exe` lai agadi chhekchha.

**ke garne:**

1. Windows Settings kholnuhos
2. "Apps" → "App execution aliases"
3. `python.exe` ra `python3.exe` **banda** garnuhos
4. Command Prompt **banda garera feri kholnuhos**

tyaspachhi pani namile Python PATH ma chhaina.
[python.org](https://www.python.org/downloads/) ko installer chalaer pahilo skrinama
"**Add python.exe to PATH**" ma chinh lagaer "Install Now" thichnuhos.

<!-- ne-section: ## 3. `ModuleNotFoundError: No module named 'numpy'` -->
### Nepali ma

**karan 2 bata chhan:**

<!-- ne-section: ### 3.1 -->
### Nepali ma

notebookle arko Python prayog gariraheko chha.

**ke garne:**

1. notebookko mathi-dayanko kernel naam ma klik garnuhos
2. `Python 3 (AI Vision)` chhannuhos
3. `Kernel` → `Restart Kernel and Run All Cells` garnuhos

**jaanch:** arko cellko output ma `.venv` chha ki hernuhos.

```python
import sys
print(sys.executable)
```

<!-- ne-section: ### 3.2 -->
### Nepali ma

```cmd
.\.venv\Scripts\activate.bat
python -m pip install -r requirements\base.txt
python -m ipykernel install --user --name aivision --display-name "Python 3 (AI Vision)"
```

`ipykernel install` birsiyo bhane Jupyter baat batabaran dekhindain. **aniwarya rupama chalaunuhos.**

<!-- ne-section: ## 4. -->
### Nepali ma

**karan:** network ko kshanik asaphalata, wa kampaniko proxy.

**ke garne:**

1. **uhi adesh feri chalaunuhos** (sabaibhanda prabhabakari)
2. tyaspachhi pani nabhae proxy milaunuhos

talaka thegana **kalpanik udaharan** hun, kampaniko bastabik setting hoina. IT le pushti gareko maanle
badaler matra chalaunuhos. `set` le yo CMD jhyal ra tyas baat suru garieka programama matra asar garchha.
jhyal banda gare setting haraunchha. pahileko thik setting lai udaharanko maanle nabadalnuhos.

```cmd
set "HTTP_PROXY=http://proxy.example.co.jp:8080"
set "HTTPS_PROXY=http://proxy.example.co.jp:8080"
python -m pip install -r requirements\base.txt
```

proxy ko thegana suchana pranali bibhagasang sodhnuhos.

3. kampaniko mirror chha bhane `--index-url` dinuhos:

talako mirror pani udaharan ho. bastabik URL IT sang sodhnuhos.

```cmd
python -m pip install -r requirements\base.txt --index-url https://pypi.example.co.jp/simple
```

<!-- ne-section: ## 5. -->
### Nepali ma

**lakshan:** rang ulto dekhinchha, `cv2` asthir hunchha, `findContours` ko natija farak aaunchha.

**karan:** `opencv-python` ra `opencv-python-headless` **chhuttai package** hun, tar dubaile `cv2`
dinchhan. **eutai batabaran ma dubai rakhda bigranchha.**

**jaanch:**

```cmd
.\.venv\Scripts\activate.bat
python -m pip list | findstr /I opencv
```

**ek line matra** dekhinu thik ho. dui line dekhiyo bhane bigreko chha.

**ke garne:**

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

dui batabaran namisaunuhos. install garnuaghi prompt (`(.venv)` wa `(.venv-anomalib)`) ma kun
batabaran chaliraheko chha aniwarya jaanchnuhos.

<!-- ne-section: ## 6. -->
### Nepali ma

**lakshan:** `FileNotFoundError`, `画像がありません`, `data.yaml がありません`.

**ke garne:**

```cmd
.\.venv\Scripts\activate.bat
python assets\scripts\generate_training_assets.py
python assets\scripts\prepare_datasets.py
```

samanyatah pahileko data nai punah prayog hunchha. janajan feri banaune ho bhane matra prashikshakasang sallah
garnuhos.

<!-- ne-section: ### 6.1 -->
### Nepali ma

**lakshan:** `assets/external_samples/open_reference/` ma 4 bata pugeka chhainan, wa
"参考画像がそろっていません / reference images are incomplete" dekhinchha.

**ke garne:**

```cmd
.\.venv\Scripts\activate.bat
python assets\scripts\download_reference_images.py --course-root .
```

- lyaine **sandarbha chitra 4 bata matra** hun (`chelsea.png`, `camera.png`, `brick.png`,
  `VisA_samples.png`).
- jati patak chalae pani thik surakshit bhaisakeka file tyasai prayog hunchhan (lyaune kaam ek patak matra).
- asaphal bhaeko fileko naam dekhinchha. **arko chitrale nabadalnuhos.** jadan jancher uhi adesh feri
  chalaunuhos.
- network prayog nagari surakshit file matra jaanchna sakinchha.

```cmd
python assets\scripts\download_reference_images.py --course-root . --offline
```

<!-- ne-section: ## 7. -->
### Nepali ma

paath aghi line ra aphalain jaanch garne kaam [START_HERE.md](../../START_HERE.md) ko step 7 ho.
`preload_models.py` le YOLO ko weight ra bus ko udaharan, ra Anomalib ko resnet18 cache janchchha.
`--offline` le network ma jodindain ra napug bhaeko kura trutika rupama bataunchha.

**lakshan:** `URLError`, `TimeoutError`, `yolo26n.pt` lina sakien.

**ke garne (yahi kram ma):**

1. **uhi cell feri chalaunuhos**
2. braujarabat linuhos:

```text
https://github.com/ultralytics/assets/releases
```

`yolo26n.pt` (karib 5 MB) daunalod garera `assets\models\` ma rakhnuhos.

3. kampaniko proxy chha bhane byabasthapakasang jaanchnuhos

**lina nasakeko bela mildojuldo natija banaunu hundaina.**
truti jastako tastai abhilekh garera prashikshakasang sallah garnuhos.

<!-- ne-section: ## 8. -->
### Nepali ma

din 5 ko notebook **`aivision-anomalib` kernel** ma chalaunuhos.
`anomalib` `.venv` ma **chhaina** (janajan chhutyaieko).

**ke garne:**

ajhai banaiyeko chhaina bhane [START_HERE step 4–5](../../START_HERE.md) chalaunuhos.
pahileko batabaran sudharn sakriya nagari tyasko Python sidhai din sakinchha.

```cmd
".\.venv-anomalib\Scripts\python.exe" -m pip install -r requirements\anomalib.txt
".\.venv-anomalib\Scripts\python.exe" -m ipykernel install --user --name aivision-anomalib --display-name "Python 3 (AI Vision Anomalib)"
```

<!-- ne-section: ## 9. `OSError: Error loading -->
### Nepali ma

**karan:** `torch==2.10.0` ko Windows wheel yo batabaran ma import huna saken.

**ke garne:**

```cmd
".\.venv-anomalib\Scripts\python.exe" -m pip uninstall -y torch torchvision
".\.venv-anomalib\Scripts\python.exe" -m pip install torch==2.15.0 torchvision==0.29.2
```

tyaspachhi pani nabhae Microsoft Visual C++ Redistributable feri rakhnuhos.

<!-- ne-section: ## 10. -->
### Nepali ma

**lakshan:** `MemoryError`, `CUDA out of memory`, PC atyadhik dhilo hunchha.

| abastha | ke garne |
|---|---|
| YOLO ko sikai | `BATCH` 8 → 4, `IMGSZ` 320 → 224 |
| PatchCore ko sikai | `train_batch_size` ra `eval_batch_size` 4 banaune |
| notebook samanya | aru anuprayog banda garne |

<!-- ne-section: ## 11. -->
### Nepali ma

slider **chaliraheko kernel** ma matra chalchha. GitHub preview wa sthir HTML ma chaldain. tyo bigreko hoina.

| lakshan | karan | ke garne |
|---|---|---|
| kehi dekhindain | `ipywidgets` chhaina | `python -m pip install -r requirements\base.txt` chalaer kernel restart garne |
| `ipywidgets が見つかりません` dekhinchha | uhi | talako "parameter cell" ma uhi prayog garna sakinchha |
| slider dekhinchha tar chitra badalindain | kernel purano chha | **Kernel → Restart & Run All** |
| aghillo chitra thapindai janchha | output metieko chhaina | tyo cellko output metaer feri chalaune |

`ipywidgets` **aniwarya chhaina**. harek demo ma widget nachahine "parameter cell" tayar chha.
samay kam bhae tyahi prayog garnuhos.

<!-- ne-section: ## 12. -->
### Nepali ma

talaka 4 kura tiper prashikshakalai bhannuhos. yi bhae samasya chhito samadhan hunchha.

1. **kun notebookko kun cell** (`In [ ]` ko number bhae pani hunchha)
2. **truti sandesh** (antim 3 line kapi)
3. `python assets\scripts\verify_environment.py --profile all` ko output
4. **pahile prayas gareka kura** ra tinako natija

CMD ko `where python` ra dubai batabaranko chhuttai jaanch natija pani sanlagn garnuhos.
proxy ko praman (credential) wa gopy jankari natansnuhos.
