<!--
Nepali anuwad / Nepali translation source for
COURSE_SYLLABUS.md

Times, notebook names and command lines are copied unchanged from the table above each block.
-->
# COURSE_SYLLABUS — Nepali anuwad

<!-- ne-doc: COURSE_SYLLABUS.md -->

<!-- ne-section: COURSE SYLLABUS -->
### Nepali ma

**hirosima kasei, kaseihin bibhag — hapta 1 AI ra mesin bhijan talim**

**abadhi:** 2026 nobhembar 16 (somabar) – nobhembar 20 (shukrabar) · **kaam garne samay:** 08:00–16:50

yo file **samayatalikako ek matra adhikarik srot** ho. pratyek notebookle "ajako kati numberko
notebook" matra bataunchha; kunai notebookle dinabhariko samayatalika aphain rakhdain.

<!-- ne-section: ## 1. 1 日のリズム -->
### Nepali ma

| samay | minet | kaam | kasale |
|---|---|---|---|
| 08:00–09:00 | 60 | prashikshakako byakhya ra pradarshan | prashikshak |
| 09:00–12:00 | 180 | **sbaadhyayan 1** (talako talika hernuhos) | prashiksharthi |
| 12:00–12:50 | 50 | diunsoko khana | — |
| 12:50–13:50 | 60 | bihanako punarabalokan ra diunsoko byakhya | prashikshak |
| 13:50–16:50 | 180 | **sbaadhyayan 2** (talako talika hernuhos) | prashiksharthi |

yi samay sthir hun, sarindainan.

sbaadhyayan dinko **360 minet** (180 + 180) ho. tyo 360 minet yasari bandinchha.

| bhaag | anuman | ke ka lagi |
|---|---|---|
| aniwarya sikai ra abhyas | **270–300 minet** | talikaka `必須` pangktiko jod |
| bishram, samasya samadhan, bujhaune | **60–90 minet** | talikaka `休憩` `予備` `提出` pangktiko jod |

aniwarya ra bachat bhaagko jod sadhain 360 minet hunuparchha. dinko talika badalepachhi jod 360 minet bhaeko
jaanchnuhos (`python -m pytest assets/tests/test_schedule.py` le sbatah janchchha).

<!-- ne-section: ### 時間割の記号 -->
### Nepali ma

| kisim | arth |
|---|---|
| `必須` aniwarya | sabaile garnuparne. sakieko janchasuchi ma parchha |
| `任意` aichchhik | samay banki bhae matra. janchasuchi ma pardaina |
| `休憩` bishram | skrinabat alag hune |
| `予備` bachat | dhilai bhartaune, samasya samadhan, punahsthapana |
| `提出` bujhaune | bujhaunuparne kaam banaer surakshit garne |

> lagne samay **prarambhik anuman** ho. ek jana surubati prashiksharthisangako pilot ma napepachhi matra
> nishchit hunchha.

<!-- ne-section: ## 2. 研修前の準備 -->
### Nepali ma

tayari paath samayabahir saknuparchha. **paath samayabhitr tayariko samay lukaieko chhaina.**

kramankit adhikarik prakriya [START_HERE.md](START_HERE.md) ho. Python 3.11, dubai batabaran,
samagri banaune, photo ra weight aghi line, ra dubai batabaranko jaanch din 1 bhanda aghi saknuparchha. talako
talika samayko anuman matra ho; dosro installation prakriya hoina.

`00_Environment_Setup.ipynb` **tayarika lagi** banaiyeko notebook ho. 5 dinko 360 minetabhitr pardaina.

| kram | kaam | anuman | jaanch |
|---|---|---|---|
| 1 | bidyarthiko folder chhanne | 5 minet | bastabik thaun tipne |
| 2 | Python batabaran banaune | 20 minet | `python assets\scripts\verify_environment.py --profile base` |
| 3 | dubai kernel darta garne | 10 minet | `jupyter kernelspec list` ma `aivision` ra `aivision-anomalib` |
| 4 | dataset banaune | 10 minet | `python assets\scripts\prepare_datasets.py` |
| 5 | photo ra weight pahile lyaune | 10 minet | `START_HERE.md` step 7 ka aphalain jaanch |
| 6 | `00_Environment_Setup.ipynb` pura garne | 60 minet | Part 7 ko riport `submissions/day00/` ma |
| 7 | din 1 ko tayari jaanch | 10 minet | talaka charai sart pura |

<!-- ne-section: ### 第1日の準備確認 -->
### Nepali ma

| jaanch | pas hune sart |
|---|---|
| kernel | "Python 3 (AI Vision)" ra "Python 3 (AI Vision Anomalib)" dubai soochi ma dekhinchhan |
| laibreri | dubai batabaran ma `verify_environment.py --profile all` ko exit code 0, samagri ma napug chhaina |
| chitra | `Day01_02` ko Part 1 le euta chitra dekhauna sakchha |
| phant | chitrako shirshakama `□` dekhindain |

<!-- ne-section: ### 準備が終わらなかった場合 -->
### Nepali ma

lukaunu hundaina; talako euta chhannuhos. **tayari paath samayabhitr sarda tyo dinko aniwarya sikai
ataundain.**

| abastha | yojana |
|---|---|
| kunai pani PC ma batabaran chaldain | prashikshakako PC ma batabaran dekhaune; prashiksharthile kagajama abalokan ra anuman ma dhyan dine. chalaunai parne aniwarya bhaag bholipalt 08:00–09:00 ma sarne. |
| kehi janako matra chalchha | chalne ra nachalne milaer 2 janako samuh banaune. nachalnele "anuman → chheuko manisako natija herne → ek bakyama byakhya" garne. |
| model download matra asaphal | din 3 pachhi `assets/reference_outputs/` ko **sandarbha natija** padher agadi badhne. prashiksharthiko aphnai natija (`submissions/`) sang chhutyaer rakhne. |

sandarbha natija **tapainko PC ma napieko natija hoina**. ti sankhya aphno natijaka rupama bujhaunu hundaina.

<!-- ne-section: ## 3. 第1日 -->
### Nepali ma

**aniwarya 300 minet / bachat 60 minet** (bishram 30 minet, punahsthapana 30 minet)

bihan ra diunsoko talika mathi diieko chha. yas dinka notebook:

| kram | notebook | lagne samay | poorwashart |
|---|---|---|---|
| 1 | `Day01_01_Introduction_to_AI.ipynb` | 115 minet | `00_Environment_Setup.ipynb` |
| 2 | `Day01_02_Pixels_and_Images.ipynb` | 110 minet | `Day01_01` |
| 3 | `Day01_03_Computer_Vision_Tasks.ipynb` | 65 minet | `Day01_02` |

**aichchhik:** `Day01_01` ko "thap sikai" ma bhaeka ujyalobahekaka lakshan (rang, kshetraphal) ka prayog.

**kary:** AI ra chitra pahichanko byakhya, Python le prashodhan gareko chitrako natija, ra PVC nirikshan ma
kaam lagn sakne tarikako sujhab.

**din 1 ko samayatalika** (`必須` = aniwarya, `休憩` = bishram, `提出` = bujhaune):

| samay | minet | kisim | kaam |
|---|---|---|---|
| 09:00–09:10 | 10 | aniwarya | tayari jaanch |
| 09:10–09:50 | 40 | aniwarya | `Day01_01` Part 0–2 |
| 09:50–10:30 | 40 | aniwarya | `Day01_01` Part 3–4 |
| 10:30–10:45 | 15 | bishram | skrinabat alag hune |
| 10:45–11:20 | 35 | aniwarya | `Day01_01` Part 5–6 + abhyas 1 |
| 11:20–12:00 | 40 | aniwarya | `Day01_02` Part 0–2 |
| 13:50–14:30 | 40 | aniwarya | `Day01_02` Part 3–5 |
| 14:30–15:00 | 30 | aniwarya | `Day01_02` Part 6–7 + abhyas |
| 15:00–15:15 | 15 | bishram | skrinabat alag hune |
| 15:15–15:50 | 35 | aniwarya | `Day01_03` Part 0–3 |
| 15:50–16:20 | 30 | aniwarya | `Day01_03` Part 4–6 + abhyas |
| 16:20–16:50 | 30 | bujhaune | bujhai jaanch, bujhaune kaam ra punahsthapana |

<!-- ne-section: ## 4. 第2日 -->
### Nepali ma

**aniwarya 300 minet / bachat 60 minet** (bishram 30 minet, punahsthapana 30 minet)

| kram | notebook | lagne samay | poorwashart |
|---|---|---|---|
| 1 | `Day02_01_Python_Basics.ipynb` | 125 minet | din 1 |
| 2 | `Day02_02_Conditions_Loops_Functions.ipynb` | 115 minet | `Day02_01` |
| 3 | `Day02_03_OpenCV_Image_Processing.ipynb` | 60 minet | `Day02_02` |

**din 2 ko samayatalika:**

| samay | minet | kisim | kaam |
|---|---|---|---|
| 09:00–09:10 | 10 | aniwarya | `Day02_01` Part 1, din 1 dohor‍yaune |
| 09:10–09:50 | 40 | aniwarya | `Day02_01` Part 2–3 |
| 09:50–10:30 | 40 | aniwarya | `Day02_01` Part 4–5 |
| 10:30–10:45 | 15 | bishram | skrinabat alag hune |
| 10:45–11:20 | 35 | aniwarya | `Day02_01` Part 6 + abhyas |
| 11:20–12:00 | 40 | aniwarya | `Day02_02` Part 0–2 |
| 13:50–14:35 | 45 | aniwarya | `Day02_02` Part 3–4, pahilo function lekhne |
| 14:35–15:05 | 30 | aniwarya | `Day02_02` Part 5–6 + abhyas |
| 15:05–15:20 | 15 | bishram | skrinabat alag hune |
| 15:20–16:00 | 40 | aniwarya | `Day02_03` Part 0–2 |
| 16:00–16:20 | 20 | aniwarya | `Day02_03` Part 3–5 |
| 16:20–16:50 | 30 | bujhaune | bujhai jaanch, bujhaune kaam ra punahsthapana |

**aichchhik:** `Day02_03` ko thap sikai ma morphology ko prayog.
**kary:** kamtima 5 maapan ma OK/NG chhutyaune program, OpenCV ko natija, pixel baat mm ma rupantaran
ra trutibare bichar bujhaunuhos.

<!-- ne-section: ## 5. 第3日 -->
### Nepali ma

**aniwarya 275 minet / bachat 85 minet** (bishram 30 minet, punahsthapana 30 minet, bujhaune 25 minet)

| kram | notebook | lagne samay | poorwashart |
|---|---|---|---|
| 1 | `Day03_01_YOLO_Concepts.ipynb` | 80 minet | din 2 |
| 2 | `Day03_02_YOLO_Inference.ipynb` | 85 minet | `Day03_01`, `yolo26n.pt` daunalod bhaisakeko |
| 3 | `Day03_03_YOLO_Experiments.ipynb` | 110 minet | `Day03_02` |

**din 3 ko samayatalika:**

| samay | minet | kisim | kaam |
|---|---|---|---|
| 09:00–09:40 | 40 | aniwarya | `Day03_01` Part 0–2 |
| 09:40–10:20 | 40 | aniwarya | `Day03_01` Part 3–4 + abhyas |
| 10:20–10:35 | 15 | bishram | skrinabat alag hune |
| 10:35–11:20 | 45 | aniwarya | `Day03_02` Part 0–3, model kholne samayasahit |
| 11:20–12:00 | 40 | aniwarya | `Day03_02` Part 4–5 + abhyas |
| 13:50–14:30 | 40 | aniwarya | `Day03_03` Part 0–2 |
| 14:30–15:10 | 40 | aniwarya | `Day03_03` Part 3–4 |
| 15:10–15:25 | 15 | bishram | skrinabat alag hune |
| 15:25–15:55 | 30 | aniwarya | `Day03_03` Part 5 + abhyas |
| 15:55–16:25 | 30 | bachat | download asaphal wa dhilo PC ko punahsthapana |
| 16:25–16:50 | 25 | bujhaune | bujhaune kaam surakshit garne |

**aichchhik:** `Day03_03` ko thap sikai ma `imgsz=1280` bhanda thulo maanko prayog.
**kary:** anumanko natija, baunding baksako chitra, threshold prayogko talika ra euta asaphalatako bishleshan.

<!-- ne-section: ## 6. 第4日 -->
### Nepali ma

**aniwarya 290 minet / bachat 70 minet** (bishram 35 minet, bujhaune 35 minet)

| kram | notebook | lagne samay | poorwashart |
|---|---|---|---|
| 1 | `Day04_01_YOLO_Dataset_Annotation.ipynb` | 80 minet | din 3 |
| 2 | `Day04_02_YOLO_Training.ipynb` | 115 minet | `Day04_01`, `assets/yolo_dataset` banisakeko |
| 3 | `Day04_03_YOLO_Evaluation.ipynb` | 95 minet | `Day04_02` ko sikieko model |

**din 4 ko samayatalika:** CPU ma sikai lai kehi minet lagchha. 11:15–12:00 ko samayamai parkhai
samabesh chha; tyasabela Part 4 padhnuhos.

| samay | minet | kisim | kaam |
|---|---|---|---|
| 09:00–09:40 | 40 | aniwarya | `Day04_01` Part 0–2 |
| 09:40–10:20 | 40 | aniwarya | `Day04_01` Part 3–5 + abhyas |
| 10:20–10:35 | 15 | bishram | skrinabat alag hune |
| 10:35–11:15 | 40 | aniwarya | `Day04_02` Part 0–2 |
| 11:15–12:00 | 45 | aniwarya | `Day04_02` Part 3, sikai suru garera Part 4 padhne |
| 13:50–14:20 | 30 | aniwarya | `Day04_02` Part 4 + abhyas |
| 14:20–14:55 | 35 | aniwarya | `Day04_03` Part 0–2 |
| 14:55–15:15 | 20 | bishram | skrinabat alag hune |
| 15:15–15:50 | 35 | aniwarya | `Day04_03` Part 3–4 |
| 15:50–16:15 | 25 | aniwarya | `Day04_03` Part 5 + abhyas |
| 16:15–16:50 | 35 | bujhaune | bujhaune kaam surakshit garne |

**aichchhik:** `Day04_02` ko thap sikai ma `epochs=20` ko prayog.
**kary:** dataset jaanch, sikai ra mulyankanko natija, euta saphal ra euta asaphal udaharan tatha arko sudhar.

<!-- ne-section: ## 7. 第5日 -->
### Nepali ma

**aniwarya 300 minet / bachat 60 minet** (bishram 35 minet, bujhaune 25 minet)

| kram | notebook | lagne samay | poorwashart |
|---|---|---|---|
| 1 | `Day05_01_Anomaly_Detection_Concepts.ipynb` | 70 minet | din 4 |
| 2 | `Day05_02_PatchCore_Training.ipynb` | 130 minet | `Day05_01`, `aivision-anomalib` kernel |
| 3 | `Day05_03_YOLO_vs_PatchCore.ipynb` | 100 minet | `Day04_03` ra `Day05_02` ka surakshit natija |

calibration ra parikshan chhutyaer rakhnuhos. parikshan data herer threshold milaunu hundaina.

**din 5 ko samayatalika:** CPU ma PatchCore `fit` ko parkhai 11:10–12:00 bhitrai samabesh chha.

| samay | minet | kisim | kaam |
|---|---|---|---|
| 09:00–09:35 | 35 | aniwarya | `Day05_01` Part 0–2 |
| 09:35–10:10 | 35 | aniwarya | `Day05_01` Part 3–5 + abhyas |
| 10:10–10:30 | 20 | bishram | skrinabat alag hune |
| 10:30–11:10 | 40 | aniwarya | `Day05_02` Part 0–2 |
| 11:10–12:00 | 50 | aniwarya | `Day05_02` Part 3–4, fit ra mulyankan |
| 13:50–14:30 | 40 | aniwarya | `Day05_02` Part 5 + abhyas |
| 14:30–15:15 | 45 | aniwarya | `Day05_03` Part 0–3 |
| 15:15–15:30 | 15 | bishram | skrinabat alag hune |
| 15:30–16:00 | 30 | aniwarya | `Day05_03` Part 4–5 + abhyas |
| 16:00–16:25 | 25 | aniwarya | paanch dinko prashikshakasang punarabalokan |
| 16:25–16:50 | 25 | bujhaune | bujhaune kaam surakshit garne |

**aichchhik:** `Day05_03` ko thap sikai ma validation data ma thresholdka 3 maan jaanchne kaam.
**kary:** PatchCore ko natija, heatmap, tulna talika ra karanasahit PVC ka lagi sipharis.

<!-- ne-section: ## 8. ノートブックの共通構成 -->
### Nepali ma

16 batai notebookko banabat uhi chha. alamalie yahi kram samjhanuhos.

| bhaag | samagri |
|---|---|
| shirshak | sikai lakshya, lagne samay, poorwashart, ajako kram, bujhaunuparne kaam |
| tayari | talim folder patta lagaune, laibreri jaanch, Japani phant milaune (ekai patak chalaune) |
| abadharana | Japani → Angreji kram ma byakhya. **pahile chitra** dekhainchha |
| pradarshan | udaharan herne → euta badaler anuman → chalaune → tulna → ek bakyama byakhya → kod padhne |
| nirdeshit prayog | sankhya badaler natija anuman garne (aichchhik slider sahit) |
| abhyas | adharabhut (aniwarya), madhyam (aniwarya), bikas (aichchhik) |
| bujhai jaanch | 3–5 prashna |
| samasya | samanya galti ra samadhan, punahsthapanako kram |
| sakieko janchasuchi | **aniwarya** bastu matra. aichchhik kaam soochi ma pardaina |
| thap sikai | aichchhik bikas matra |

<!-- ne-section: ### セルの指示 -->
### Nepali ma

harek kod cellko suru ma talako euta chinh aniwarya hunchha.

| dekhine | arth |
|---|---|
| `実行のみ / Run only` | chhaner **Shift + Enter**. nabadalnuhos |
| `この値を変更 / Change this value` | maan badaler natijako paribartan anuman garepachhi chalaunuhos |
| `自分でコードを書く / Write your code` | khali thaun aphain bharnuhos |

**uchcha tahako tayari:** Part 0 ka cell ma folder patta lagaune, phant milaune ra dekhaune function matra
chhan. bhitri kura bujhnu aawashyak chhaina. ekai patak chalaunuhos.

<!-- ne-section: ## 9. 評価 -->
### Nepali ma

harek din 4 tahama aphain mulyankan garnuhos. **lakshya tah 2 wa mathi** ho.

| tah | abastha |
|---|---|
| 0 | nasakieko |
| 1 | thulo sahayog bhae ma sakieko |
| 2 | alikati sahayogama sakieko |
| 3 | eklai saker natija bujhaun sakne |

tah 3 ma "chalyo" matra pugdain. **"kina tyasto hunchha" arulai bujhaun sakne** hunuparchha.

mulyankan **aniwarya** bastuma matra garinchha. aichchhik bikas kaam nagare pani angk ghataindain.

<!-- ne-section: ## 10. 第 2 週へのつながり -->
### Nepali ma

hapta 1 **adhar** ho. bastabik nirikshan pranali hapta 2 ma samhalinchha.

| hapta 2 ko samagri |
|---|
| PVC ka bastabik nirikshan abashyakatako byabasthapan |
| kyamera, lens ra ujyaloko chhanot (0.3 mm dekhauna kati pixel chahinchha) |
| khichaiko sart dijain ra calibration |
| bastabik chitrako data sankalan ra lebaling |
| pranaliko banabat ra uchcha gatiko prashodhan |
| nirikshan prototype banaune ra mulyankan garne |

hapta 1 ma "kritrim datako shuddhata utpadanako shuddhata hoina" bhanera dohoryaieko karan hapta 2 ma
bastabik data sang imanadarisath samana garnu ho.
