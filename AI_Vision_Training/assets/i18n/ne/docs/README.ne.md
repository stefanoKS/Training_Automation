<!--
Nepali anuwad / Nepali translation source for
README.md

Commands, paths, versions and file names stay byte-identical.
-->
# README — Nepali anuwad

<!-- ne-doc: README.md -->

<!-- ne-section: Hiroshima Kasei Week 1 -->
### Nepali ma

kaseihin bibhagaka karmacharika lagi banaiyeko **5 din, 16 notebook** ko sbaadhyayan AI talim samagri ho.
Python, AI ra chitra prashodhanako anubhab nabhaeka manisalai lakshit garera banaiyeko chha.

| bishay | biwaran |
|---|---|
| abadhi | 2026 nobhembar 16 (som) – 20 (shukr) |
| lakshit | programing anubhab nabhaeka kaseihin bibhagaka karmachari |
| samay | 08:00–16:50 (diunsoko khana 12:00–12:50) |
| pugne lakshya | uchcha gatiko PVC sit nirikshanka lagi chahine AI ko adhar aphnai shabdama bujhaun ra chalaun sakne |
| dayara | **hapta 1 matra**. bastabik nirikshan pranali nirman hapta 2 ma hunchha. |

<!-- ne-section: ## 1. 最初に読むもの -->
### Nepali ma

talako kram ma agadi badhnuhos.

1. [`START_HERE.md`](START_HERE.md) — computer an garne dekhi suru hune, ekadamai surubati tahaka lagi prakriya
2. [`COURSE_SYLLABUS.md`](COURSE_SYLLABUS.md) — **samayatalikako ek matra adhikarik srot**. harek dinko aniwarya samay, bachat samay ra aghillo dinasammako tayari
3. `notebooks/00_Setup/00_Environment_Setup.ipynb` — batabaran setaap ra jaanch (**paath samayabahir** garinchha)

<!-- ne-section: ## 1.1 時間の考え方 -->
### Nepali ma

sbaadhyayan dinko **360 minet** (09:00–12:00 ra 13:50–16:50) ho. tyasamadhye
**aniwarya sikai ra abhyas 270–300 minet**, banki **60–90 minet** bishram, samasya samadhan ra bujhaunama
kharch hunchha.

notebookko lagne samay **prarambhik anuman** ho. ek jana surubati prashiksharthisangako pilot ma napepachhi
matra nishchit hunchha.

**abhyas 3 (bikas) aichchhik** ho. sakieko janchasuchi ma pardaina.

<!-- ne-section: ## 2. この研修で身につくこと -->
### Nepali ma

5 dinko antya ma talaka kura garna sakne hunuhunechha.

| din | garna sakne |
|---|---|
| 1 | AI, mesin larning, dip larningko farak bujhaune. chitra sankhyako talika ho bhanera bujhaer aphain badalne. |
| 2 | Python ma nirnaya program lekhne. OpenCV le chitra padher dui-maan banaune ra pixel lai mm ma badalne. |
| 3 | sikieko YOLO chalaer natija padhne ra threshold badalda byabahar kasari badlinchha bujhaune. |
| 4 | dataset jaanchne, YOLO fine-tune garne ra parikshan data ma mulyankan garne. |
| 5 | PatchCore le anomaly detection chalaer YOLO sang tulna garne ra PVC nirikshanka lagi sipharis banaune. |

<!-- ne-section: ## 3. インストール -->
### Nepali ma

adhikarik kramankit prakriya [START_HERE.md](START_HERE.md) ho. Python 3.11 prayog garera paath aghi
dubai batabaran, photo ra weight tayar garnuhos. tal batabaranko saransh matra ho.

dui virtual environment banainchha. **karan aniwarya padhnuhos.**

| batabaran | prayog hune din | mukhy package |
|---|---|---|
| `.venv` | din 0–4 | numpy, matplotlib, opencv-python, torch, ultralytics |
| `.venv-anomalib` | din 5 | anomalib 2.7.0, torch, opencv-**headless** |

> **kina chhutyaune?**
>
> `anomalib` le `opencv-python-headless` chahanchha, `ultralytics` le
> `opencv-python` chahanchha. eutai batabaran ma rakhda `cv2` duibata hunchhan ra OpenCV bigranchha.
> yo adhikarik kagajatako dependency batai dekhine, chhaln nasakine dbandb ho.

Windows ko khojama "Command Prompt" (`cmd`) kholer
[START_HERE ko step 1–8](START_HERE.md) kramaisang chalaunuhos.
ZIP, OneDrive ra khali thaun bhaeko path ko byabasthapan, sakriya garne ra dubai kernel darta garne kura tyahin chha.
GPU aniwarya chhaina. GPU wheel ko sanyojan yo paribartanama janchieko chhaina.

**janchieka sanskaran:** [`requirements/tested_versions.md`](requirements/tested_versions.md)

<!-- ne-section: ## 4. 素材（データ）の生成 -->
### Nepali ma

kritrim chitra, chitrarekha ra dataset **Python le banainchha**. sandarbha photo ra sikieka weight paath aghi
lyainchha.

banaune adesh [START_HERE step 6](START_HERE.md) ma, ra sandarbha photo tatha weight line ra aphalain jaanch
step 7 ma chha. sangai diieka sandarbha chitra mul abhilekh bhaeka prashikshakale matra feri banaunchhan.

| natija | samagri |
|---|---|
| `assets/diagrams/` | abadharana chitra, calibration chitra ra sikai chitra |
| `assets/reference_outputs/` | bastabik chalaika natija baat baneka sandarbha chitra (srot tyahi folderko `README.md` ma) |
| `assets/normal_samples/`, `assets/defect_samples/` | samanya ra dosh namuna (sahi mask ra nirdeshank sahit) |
| `assets/yolo_dataset/` | 96 chitra (train 64 / val 16 / test 16), label, `data.yaml` |
| `assets/anomaly_dataset/pvc_sheet/` | samanya 44, asamanya 40, sahi mask |

`assets/diagrams/teach_*.png` ra `assets/reference_outputs/ref_*.png` **bitaran ma samabesh hunchhan**
(`.gitignore` ko apabad). Python nachalai pani chitra dekhin bhanera yaso garieko ho.
aru banaieka samagri (dataset, weight, sikai natija) pahilejhain Git ma rakhindain.

`generate_reference_outputs.py` ma sikai ko chalaibat surakshit natija chhaina bhane **chitra nabanai karan
dekhaer rokinchha**. sankhya banaer bharne kaam kahilyai gardaina.

> **mahattwapurna**
>
> yi **kritrim chitra** hun. bastabik PVC ko prakashik byabahar **punahutpadan gardainan**.
> bastabik karakhanako chitra ma jaanch hapta 2 pachhi matra garinchha.
> kritrim data ma paieko shuddhatalai utpadan nirikshanko shuddhata bhanera uddhrit garnu hundaina.

<!-- ne-section: ## 4.1 解説 PDF -->
### Nepali ma

notebookko byakhya baat sbatah banaieka pustika `docs/pdf/` ma chhan. aphalain padhnaka lagi sahayak samagri
hun; abhyas bhane notabukamai garinchha.

| file | samagri |
|---|---|
| `docs/pdf/Day01_explanation_ja_en_ne.pdf` … `Day04_…` | pratyek dinko byakhya (Japani → Angreji → Nepali) |
| `docs/pdf/Week1_explanation_ja_en_ne.pdf` | 5 dinko ekai pustika |
| `docs/pdf/Setup_ja_en_ne.pdf` | tayari notebook |
| `docs/pdf/Installation_Guide_ja_en_ne.pdf` | sthapana ra samasya samadhan |
| `docs/pdf/Repository_Guide_ja_en_ne.pdf` | ripojitari ra sanskaranako parichay |
| `docs/pdf/Course_Syllabus_ja_en_ne.pdf` | samayatalika |
| `docs/pdf/README.md` | banaune tarika, ke parchha, ke pardaina, sima |

aghilla Japani–Angreji sanskaran (`*_ja_en.pdf`) pani jastako tastai rakhieka chhan, tyasaile dubai
padhna sakinchha. nayan tribhashi sanskaran banaun Chromium (Playwright) chahinchha; Japani–Angreji sanskaran
riportalyab (ReportLab) le nai banchha.

```cmd
REM PDF generation and inspection only; not needed by learners.
".\.venv\Scripts\python.exe" -m pip install -r requirements\pdf.txt
".\.venv\Scripts\python.exe" -m playwright install chromium
".\.venv\Scripts\python.exe" assets\scripts\export_explanations_pdf.py
".\.venv\Scripts\python.exe" assets\scripts\export_trilingual_pdf.py
".\.venv\Scripts\python.exe" assets\scripts\inspect_pdf_pages.py --languages ja,ne
```

* chalaiko log, stack trace, lamo tayari kod ra prashikshakaka jabaph pardainan.
* slider bhaeka thaun ma sthir chitra ra "notebook ma chalaunuhos" bhanne tippani rakhinchha.
* model download ra sikai feri garindain.
* pharakila chitra padhna sajilo hos bhanera A4 terso panama rakhinchhan.

<!-- ne-section: ## 5. 起動 -->
### Nepali ma

tayari sakiepachhi File Explorer ma bastabik `AI_Vision_Training` kholer
thegana barama `cmd` lekher Enter thichnuhos. tyaspachhi talako adesh chalaunuhos.
wa tyahi folderko `start_training.cmd` dabal-klik garnuhos.
suru garne filele install, download wa sikai gardaina.

```cmd
.\.venv\Scripts\activate.bat
".\.venv\Scripts\python.exe" -m jupyter lab
```

sakriya garda arko Python ko Jupyter suru garne file chhaninabat jogaunchha. yo CMD bhitr matra lagu hunchha.

braujar khulepachhi `notebooks` → `00_Setup` → `00_Environment_Setup.ipynb` kram ma kholnuhos.
**din 5 ko notebook ma matra** kernel `Python 3 (AI Vision Anomalib)` ma badalnuhos.

<!-- ne-section: ### 5.1 セルの指示 -->
### Nepali ma

sabai kod cellko suru ma talako euta chinh hunchha.

| dekhine | arth |
|---|---|
| `実行のみ / Run only` | **Shift + Enter** le tyasai chalaune. nabadalnuhos |
| `この値を変更 / Change this value` | maan badaler natija anuman garepachhi chalaune |
| `自分でコードを書く / Write your code` | khali thaun aphain bharne |

<!-- ne-section: ### 5.2 対話デモ -->
### Nepali ma

5 bata chhota antarakriyatmak demo chhan. **slider sarn chaliraheko kernel chahinchha.**

| thaun | ke sarne |
|---|---|
| `Day01_02` Part 3 | RGB ka tin maan |
| `Day02_02` Part 2 | loop ko step (ek-ek) |
| `Day02_03` Part 2 | OpenCV ko threshold |
| `Day03_01` Part 3 | anuman garieko chaukonako sthan (IoU) |
| `Day03_03` Part 1 | YOLO ko confidence |
| `Day05_03` Part 4 | PatchCore ko threshold (**calibration data matra**) |

> GitHub preview wa sthir HTML ma slider chaldain.
> harek demo ma **widget nachahine parameter cell** chha, jasale uhi prayog garna dinchha.

<!-- ne-section: ## 6. 検証とテスト -->
### Nepali ma

tayar bhaisakeko adharabhut batabaran sakriya gareko CMD ma chalaunuhos
([START_HERE](START_HERE.md) hernuhos).

```cmd
REM Check the environment.
python assets\scripts\verify_environment.py --profile all

REM Structural validation (fast).
python assets\scripts\validate_notebooks.py
```

thap jaanch ra marmataka adesh tal chhan. samanya bidyarthile sanrachanatmak janchapachhi paath ma jan sakchhan.
`--execute lightweight` ra `check_widgets.py` le notebook chalaunchhan; sanrachanatmak jaanch matra chahieko
abastha ma yi nachalaunuhos. `scaffold_notebooks.py` le notebook badalchha ra marmatakartaka lagi matra ho.

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

`assets/scripts/validate_notebooks.py --execute all` ma **model download** ra **sikai** parne hunale
dherai samay lagchha.

`check_widgets.py` le notebook chalaer `widgets.interact` prayog garne cellle widget dekhaeko chha ki chhaina
janchchha. braujarama bastabama klik garera jaanchne kaam chhuttai ho.

<!-- ne-section: ## 7. フォルダ構成 -->
### Nepali ma

```text
AI_Vision_Training/
├── README.md                     <- yahi file
├── START_HERE.md                 <- ekadamai surubati tahako prakriya
├── COURSE_SYLLABUS.md            <- 5 dinko samayatalika
├── requirements/                 <- janchieka sanskaran
├── notebooks/                    <- 16 notebook (00_Setup ra din 1–5)
├── assets/                       <- chitra, namuna, dataset, skript, test
├── docs/                         <- PDF, prashikshak margadarshan, samasya samadhan, sandarbha
├── submissions/                  <- din anusar bujhaune kaam
└── training_results/             <- sikai ko natija (Git ma pardaina)
```

<!-- ne-section: ## 8. 提出物 -->
### Nepali ma

harek din `submissions/day0N/` ma talaka 4 kura rakhnuhos.

1. chalaieko notebook (`File` → `Save`)
2. `Day0N_Report_Template.md` bhareko
3. surakshit gareka chitra, CSV, JSON
4. truti ae tyasko sandesh ra prayas gareka kura

prashikshakaka namuna jabaph `docs/instructor/` ma chhan. **pahile aphain lekhnuhos.**

<!-- ne-section: ## 9. 困ったとき -->
### Nepali ma

pahile talako kram ma jaanchnuhos.

1. pratyek notebookko antya ma bhaeko "samasya aunda" talika
2. [`docs/troubleshooting/installation.md`](docs/troubleshooting/installation.md)
3. `python assets\scripts\verify_environment.py --profile all`

<!-- ne-section: ## 10. 既知の制限 -->
### Nepali ma

| sima | karan |
|---|---|
| kritrim chitra matra | bastabik PVC chitra ajhai upalabdh chhaina |
| CPU ka lagi sano setting | talimka PC ma GPU chhaina bhanne manyata |
| sikai chitra 64 bata | ek din ma sakine matra rakhieko |
| PatchCore ko mulyankan data adha | validation ra test ma bandn |
| YOLO ra PatchCore chhuttai batabaran | OpenCV ko dbandb (mathiko khand 3) |
| PDF bhitrako chitraka akshar khojn mildaina | chitra lai image ko rupama rakhieko |
| PDF ma chalaiko log pardaina | output batabaran anusar farak parne |

mathika sabai sima janajan apanaieka ra abhilekh garieka hun; kunai pani bigrieko bhaag lukaune upay hoina.
bastabik utpadanama sambhab chha ki chhaina bhanne kura bastabik chitra, sthir kyamera ra ujyaloko dijain, ra
thaha bhaeka ramra utpadanama threshold adhyayan ma nirbhar chha — yi sabai hapta 2 ka bishay hun.

<!-- ne-section: ## 11. ライセンスと出所 -->
### Nepali ma

yo talim ma prayog hune bahy samagriko srot ra laisens
[`assets/external_samples/PROVENANCE.md`](assets/external_samples/PROVENANCE.md) ma abhilekh chha.

**mahattwapurna:** sikaika lagi prayog garda samasya chhaina, tar
**Ultralytics ka model ra kod AGPL-3.0** hun. utpadanama samabesh garnuaghi
laisens jaanch nagari agadi nabadhnuhos.
