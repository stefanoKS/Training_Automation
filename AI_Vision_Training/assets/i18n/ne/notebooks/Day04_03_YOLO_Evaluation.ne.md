<!--
Nepali anuwad / Nepali translation source for
notebooks/Day04_YOLO_Training/Day04_03_YOLO_Evaluation.ipynb
-->
# din 4 notebook 03 — Nepali anuwad

<!-- ne-cell: 7bb5e95c | after-heading -->
# din 4 notebook 03: prashikshan bhaeko model ko mulyankan

<!-- ne-cell: 7bb5e95c -->
## sikai lakshyaharu

| Nepali |
| --- |
| 1. prashikshan ma prayog nabhaeka tasbir ma kshamata napna sakne. |
| 2. precision ra recall ko arth bataun sakne. |
| 3. confusion matrix padhna sakne. |
| 4. saphal ra asaphal pahichanka udaharan abhilekh garna sakne. |
| 5. dataset sudharne sujhab din sakne. |

## yo notebookko adharabhut jankari

| bishay | biwaran |
| --- | --- |
| sikai samay (anuman) | 95 minet |
| kathinai | surubati tah |
| poorwashart | din 4 notebook 02 ko prashikshan sakieko ra `weights/best.pt` bhaeko hunuparchha. |
| aawashyak laibreri | torch, ultralytics, opencv-python, numpy, matplotlib, pandas |
| prayog hune kernel | aivision |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 4](../../COURSE_SYLLABUS.md#day4) |

### bujhaunuparne kaam

| Nepali |
| --- |
| mulyankan maapan (precision / recall / mAP) |
| asaphal udaharanka tasbir |
| sudharaka sujhab |

<!-- ne-cell: 09eb408e | after-heading -->
## yo notebook kahan parchha

<!-- ne-cell: 09eb408e -->
| bishay | biwaran |
| --- | --- |
| din | din 4 |
| ajako kram | ajako notabukamadhye 3 / 3 |
| lagne samay | 95 minet |
| poorwashart | `Day04_02_YOLO_Training.ipynb` ko prashikshan bhaeko model |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 4](../../COURSE_SYLLABUS.md#day4) |

dinko samayatalika `COURSE_SYLLABUS.md` ma eutai thaun ma chha. yo notebook tyasko euta bhaag matra ho.

<!-- ne-cell: audit-learning-loop | after-heading -->
### anuman garnuhos, chalaunuhos, hernuhos, byakhya garnuhos

<!-- ne-cell: audit-learning-loop -->
mulyankanle sthir garieko model ra nirnaya niyam lai nadekhieka tasbir ma janchchha. mahattwapurna cell chalaunuaghi
input, kaam ra natija ek-ek bakyama lekhnuhos. pahile anuman garera chalaunuhos ra maan wa chitra hernuhos.
udaharan chitrako IoU sart matra badaler feri anuman gari chalaunuhos.

<!-- ne-cell: a79775e7 | after-heading -->
## Part 0 tayari

<!-- ne-cell: 264f61b9 | after-heading -->
**prashikshan bhaeko weight khojne**
<!-- ne-pair: Find the trained weights -->

<!-- ne-cell: 264f61b9 -->
prashikshan bhaeko model `training_results/day04/.../weights/best.pt` ma chha. nabhetie pahile prashikshan
(04_02) chalaunuhos.

**prashikshan nagareko model ko mulyankan garna sakindaina.** sankhya banaera rakhnu hundaina.

<!-- ne-cell: b264ae84 | after-heading -->
## Part 1 mulyankanka maapan

<!-- ne-cell: clarity-evaluation-units | after-heading -->
### pahile ganne ekai tay garne

<!-- ne-cell: clarity-evaluation-units -->
uhi sansleshit udaharan: ek asamanya tasbir ma sahi ayat 2 bata, anuman 1 bata ra ek-ek milne jodi 1 ho.
anuman: tasbir sahi rupama NG bhaniyo bhane pani dosh chhutna sakchha?

| drishti | yahan ganieko | recall ko har | chitrako aksh |
|---|---|---|---|
| tasbir | TP=1, FN=0 | asamanya tasbir 1 | tasbir 2×2: line=sahi, stambha=anuman |
| ayat | TP=1, FN=1, FP=0 | sahi ayat 2 | Ultralytics: line=anuman, stambha=sahi |

tasbir recall = 1/1, bastu recall = 1/2 ho. prishthabhumiko line-stambha bhaeko bastu myatriksama TN tasbir
ganindain. talaka sahi chitra ekaianusar padhnuhos. sano prayog: uhi tasbir ma anuman 0 banaunda dubai FN kati?

<!-- ne-cell: 968ad99b | after-heading -->
**precision ra recall**
<!-- ne-pair: Precision and recall -->

<!-- ne-cell: 968ad99b -->
dui maapanle **farak kura napchhan**.

```text
precision = sahi pahichanko sankhya ÷ pahichan garieko kul sankhya
          -> "pahichan gareka madhye kati bastabik?"

recall    = sahi pahichanko sankhya ÷ bastabik doshko kul sankhya
          -> "bastabik doshamadhye kati samatyaun?"
```

| maapan | kam bhae ke hunchha |
|---|---|
| precision kam | **jhuto alarm dherai**. kamadar thakchhan, line rokinchha |
| recall kam | **chhutne dherai**. bigreko saman pathainchha |

**uthi pahichanko soochi, uthi sahi uttar, uthi milaune niyam (IoU adi) ra uthi pachhi-prashodhan** prayog garda
matra threshold badhaunda **recall badhdain** (uhi rahanchha wa ghatchha) bhanne kura nishchayaka sath bhanna sakinchha.
threshold badalda anuman feri chaldain bhane pahichan aphai badalina sakne hunale yo nishchayata lagu hundaina.
precision samanyataya badhchha, tar **sadhain badhchha bhanne chhaina**; score ko kram anusar ghatna pani sakchha ra dubai nabadalin
pani sakchhan (din 3 ma dekheko 3 → 1 → 1 udaharan). bastabik paribartan pramanikaran data ma jaanchnuhos.

<!-- ne-cell: c479853d | after-heading -->
**mAP ke ho**
<!-- ne-pair: What mAP is -->

<!-- ne-cell: c479853d -->
**mAP** (mean Average Precision) le precision ra recall miler baneko maapan ho. paribhasha yahi kram ma banchha.

1. pahichan lai confidence ko uchcha baat nimn kram ma rakher ek-ek gardai precision ra recall ganana gari
   **precision–recall bakr** banainchha.
2. tyo bakramuniko kshetraphal **AP** (Average Precision) ho (ek class ko).
3. Class-dar-class AP ko ausat **mAP** ho.
4. IoU ko adhar badaler uhi ganana feri garinchha.

( karyakramma precision–recall bakr lai interpolate garera kshetraphal nikalchha. ahile "precision ra recall
lai ek sankhya ma mileko maapan" bhanne bujhai pugchha. )

YOLO ko prashikshan lagama `mAP50` ra `mAP50-95` dekhinchhan.

- `mAP50` … IoU 0.50 wa badhi lai "milyo" manda ko mAP
- `mAP50-95` … IoU 0.50, 0.55, …, 0.95 gari 10 tharama mAP ganana garera ausat

utpadanako karyasthalama **mAP bhanda precision / recall bujhna sajilo** hunchha. "kati pratishat chhutchha" bhanne kurako
karyasthalama arth hunchha.

<!-- ne-cell: 6bcff7a5 | after-heading -->
## Part 2 parikshan data ma mulyankan

<!-- ne-cell: 612e7d6a | after-heading -->
#### pramanikaran ma chhaner sthir garepachhi parikshan

<!-- ne-cell: 612e7d6a -->
sudhar tatha model ra threshold chhanot `split="val"` ma garinchha. model, purb-prashodhan ra threshold sthir
garepachhi matra prayog nabhaeko `split="test"` ma antim mulyankan garinchha. parikshan herer setting badaliyo bhane
nayan antim mulyankanka lagi arko prayog nabhaeko data chahinchha.

talako cell tyo antim charanko udaharan ho. **chalepachhi pahile ghoshana magchha, ra khali chhodepachhi
rokinchha.** "parikshan hernuaghi setting sthir garen" bhanne kura aphnai shabda ma lekhnuhos ra
`TEST_ALREADY_SEEN` jaanchnuhos. parikshan tasbir wa natija pahile nai herisaknu bhaeko chha bhane `True` nai
rakhnuhos; tyo natija **punar prayog garieko datako udaharan mulyankan** ho, swatantra antim natija hoina.
nahereko awastha ma matra `False` banaunuhos. ajhai chhanot gardai hunuhunchha bhane nachalai val ma
pharkanuhos. prashikshan `train` ko angk antim mulyankan hundaina.

<!-- ne-cell: 0fe77594 | after-heading -->
### natijako udaharan

<!-- ne-cell: 0fe77594 -->
Class-dar-class sahi sankhya (`black_spot` 5, `scratch` 7, `streak` 6) yo talimko parikshan datale tay garne
maan hun. precision pachhika sankhya yo talim ma surakshit garieko abhilekhaka hun (`best.pt`,
`split="test"`, `imgsz=320`, seed 2026). sukshma sankhya batabaran anusar farak parchha; prabritti ra thulo-sanoko
sambandh padhnuhos.

<!-- ne-cell: cdbaa1cb | after-heading -->
**sankhya kasari padhne**
<!-- ne-pair: How to read these numbers -->

<!-- ne-cell: cdbaa1cb -->
64 prashikshan tasbir ma talim bhaeko model ho. sankhya **uchcha nahun pani sakchha**. tyo **sambhab natija** ho;
thorai data ma bastabik kshamata simit hunchha.

| herne tarika | sambhabit karan (anuman) | jaanchne tarika |
|---|---|---|
| recall kam | dosh halka wa sano, prashikshan udaharan thorai, threshold dherai uchcha | chhuteka tasbir hernuhos. threshold **pramanikaran data** ma matra sarnuhos |
| precision kam | prishthabhumiko bhinnata prashikshan ma kam, buttalai dosh thannu | jhuto alarmka tasbir hernuhos. prishthabhumi tasbir badhaune kura sochnuhos |
| dubai kam | kam prashikshan, labelko galti, prashikshan ra parikshan tasbirko dekhine rupako farak (domain shift) | label, khichaiko abastha ra pramanikaranko prabritti jaanchnuhos |

**threshold samayojan pramanikaran data ma garinchha.** parikshan datako natija herepachhi tyahi parikshan data ma
samayojan garda tyo data aba "prayog nabhaeko" rahandain.

**"ramro sankhya naaunjel prashikshan dohoryaune" tarika galat** ho. sankhya naramro hunuko karan data,
label ra khichaiko abastha ma khojnuhos. karan eutai nahun pani sakchha.

<!-- ne-cell: b116fb65 | after-heading -->
## Part 3 confusion matrix (milan talika)

<!-- ne-cell: b116fb65 -->
tasbir chhutne sankhya ra namileka sahi ayatako sankhya farak hun. chitrako harek line ma ekai jaanchnuhos.

<!-- ne-cell: audit-teach_detection_matching | after-heading -->
### kod kasari padhne

<!-- ne-cell: audit-teach_detection_matching | after-image:../../assets/svg/teach_detection_matching.svg -->
chitra: eutai class ka ayat ek-ek garera milainchha. (ganana garieko sansleshit udaharan ra yojanabaddha chitra; model ko
bastabik napieko natija hoina.)

**dhyan dinuparne kura**

eutai class ka ayat ek-ek garera milainchha. input ra paribartan bhaeko maan aunlale pachhyaunuhos.

**sochnuhos**

euta sahi ayatama dui anuman obharalyap bhae dubai TP hun?

<!-- ne-cell: 0c5dc209 | after-heading -->
### confusion matrix kasari padhne

<!-- ne-cell: 0c5dc209 | after-image:../../assets/diagrams/teach_image_level_confusion_matrix.png -->
chitra: tasbir-starko confusion matrix. line "bastabik", stambha "anuman". ganne ekai ek tasbir ho.
(sankhya udaharanka lagi)

**dhyan dinuparne kura**

yo **tasbir-star** ko ganana ho. euta tasbir ma dherai dosh bhae pani ek patak matra ganinchha. yo chitra ma bastabik
NG ra anuman NG (TP) 28 tasbir, bastabik NG ra anuman OK (FN, chhutnu) 9 tasbir, bastabik OK ra anuman NG
(FP, jhuto alarm) 6 tasbir, bastabik OK ra anuman OK (TN) 57 tasbir chhan.

bastu-starko precision/recall (mAP adi) bhanda yo farak sankhya ho, tyasaile misaer tulna garnu hundaina.
yo chitrako akshako disha (line=bastabik, stambha=anuman) lai tal aune Ultralytics ko bastu-star chitra ma
lagu nagarnuhos; tyahan disha ulto chha. harek chitrako aksh label jaanchnuhos.

**sochnuhos**

- euta tasbir ma dui dosh bhae bastu-star ma kati patak ganinchha?

<!-- ne-cell: 826acaec | after-heading -->
### tasbir-starko TP, FP, FN ra TN

<!-- ne-cell: 826acaec | after-image:../../assets/diagrams/teach_image_level_confusion.png -->
chitra: harek tasbirko chaar natija (sansleshit tasbir; bastabik model ko natija hoina). ekai ek tasbir.

**dhyan dinuparne kura**

tasbirko nirnaya "lakshya class ko pahichan kamtima ek bata tokieko adhar pura garchha ki" bhannele NG wa OK
tay garchha. yo chitrako udaharan ma "confidence threshold wa badhi bhaeko pahichan ek bhae pani NG" ho. **tyo nirnaya
ra tasbir ma bhaeko sahi label chhuttachhuttai tayar garera** matra TP, FP, FN, TN gannuhos. anumanko bela sahi
label prayog garna mildaina, tyasaile nirnayako niyam pahile nai tay garinchha.

chhutnu (FN) bhaneko "bastabama NG hundahundai OK bhanieko" tasbir sankhya ho. utpadanama pahile yahi herinchha.
jhuto alarm (FP) bhaneko "bastabama OK hundahundai NG bhanieko" sankhya ho. **rang matra herer nirnaya nagarnuhos.**
TP ra TN dubai "milyo" hun, tar arth ulto chha.

bastu pahichan ma prishthabhumilai ganna milne **TN** mann sakindaina. yi chaar ganne tarika **tasbir-star** ko
mulyankan ma matra prayog hunchha.

**sochnuhos**

- yo confusion matrix baat recall ra precision ganana garnuhos.

<!-- ne-cell: fig-teach_object_level_matching | after-heading -->
### bastu-star ma ek-ek milaune

<!-- ne-cell: fig-teach_object_level_matching | after-image:../../assets/diagrams/teach_object_level_matching.png -->
chitra: bastu-starko milan. sahi ayat ra anumanko ayat IoU le ek-ek milainchha; namileko anuman FP ganinchha
(nirdeshangk udaharanka lagi).

**dhyan dinuparne kura**

bastu-star ma lakshya class, IoU (yo talim ma 0.5 wa badhi), confidence ra ek-ek milaune niyam pahile tay
garinchha. namileko anuman FP, namileko sahi ayat FN ho. tasbir-starko OK/NG arkai ganana ho, jastai "lakshya class
ko pahichan ek wa badhi bhae NG".

**sochnuhos**

- eutai ayat dui patak anuman gariyo bhane bastu-star ma kasari ganinchha?

<!-- ne-cell: bdd2037d | after-heading -->
**Ultralytics ko confusion matrix kasari padhne**
<!-- ne-pair: How to read the Ultralytics confusion matrix -->

<!-- ne-cell: bdd2037d -->
mulyangkanapachhi Ultralytics le lekhne `confusion_matrix.png` **bastu-star** ko talika ho. yo talim ma
prayog hune ultralytics 8.4.211 ko chitra ma **terso aksh sahi (True)** ra **thado aksh anuman (Predicted)**
hunchha (sadhain chitrako aksh label padhnuhos). euta khandale "sahi class yo thiyo ra anuman yo class bhayo" bhanne
sankhya dekhaunchha.

|  | sahi: black_spot | sahi: scratch | sahi: prishthabhumi |
|---|---|---|---|
| anuman: black_spot | sahi pahichan | class farak | **jhuto pahichan (FP)** |
| anuman: scratch | class farak | sahi pahichan | **jhuto pahichan (FP)** |
| anuman: prishthabhumi | **chhutnu (FN)** | **chhutnu (FN)** | (ganindain) |

- **prishthabhumiko stambha** … milne sahi ayat nabhaeko anuman. arthat **FP**
- **prishthabhumiko line** … milne anuman nabhaeko sahi ayat. arthat **FN**
- tal-dayanko khand (prishthabhumi ra prishthabhumi) bastu pahichan ma **ganna milne TN hundaina**; kehi nabhaeko kshetra pani
  gannuparne hunchha. tyasaile yo talika ma TN chhaina.

aghillo chitrako tasbir-star TP/FP/FN/TN sang **ganne ekai ra akshako disha dubai farak chhan**. misaunu hundaina.
yo talimko model sang tin class chhan, tyasaile mulyankan chitra ma `streak` ka line ra stambha pani dekhinchhan.

<!-- ne-cell: 8a71da19 | after-heading -->
### dui confusion matrix chhutyaera padhne

<!-- ne-cell: 8a71da19 -->
tasbir-starko mulyankan ma harek tasbir lai OK wa NG ma bargikaran garera TP, FP, FN, TN ganinchha. NG nirnaya
"lakshya class ko pahichan kamtima ek bata tokieko adhar (jastai confidence threshold) pura garnu" le garinchha
ra tasbir ma bhaeko sahi label sang **chhuttai** tulna garinchha.

bastu pahichanko mulyankan ma anumanko ayat ra sahi ayat milainchha. milaune kaam **class milnu, IoU,
confidence ko byabahar ra ek-ek milaune** niyamle garinchha. tyasabela namileko anuman FP, namileko sahi ayat
FN ho. purai prishthabhumilai ganna milne TN mann sakindaina. line-stambhako disha chitra anusar farak parchha, tyasaile
**aksh label jancher** padhnuhos.

<!-- ne-cell: 4607c1f7 | after-heading -->
## Part 4 saphal ra asaphal udaharan

<!-- ne-cell: 1838c3de | after-heading -->
**aphnai ankhale jaanchne**
<!-- ne-pair: Check with your own eyes -->

<!-- ne-cell: 1838c3de -->
sankhya matrale karyasthalama chalchha ki chaldain bhanne thaha hundaina. **tasbir hernuhos.**

talako cellle parikshan dataka tasbir ma anuman banaunchha. **hariyo** anuman, **rato** sahi label (label) ho.
namileka tasbir khojnuhos.

<!-- ne-cell: fig-ref_detections_label_vs_pred | after-heading -->
### sahi label ra anuman eutai kram ma herne

<!-- ne-cell: fig-ref_detections_label_vs_pred | after-image:../../assets/reference_outputs/ref_detections_label_vs_pred.png -->
chitra: eutai batch ka 8 tasbir, sahi label (bayan) ra anuman (dayan) ma rakhieko bastabik natija. sahi label yo
talimko banaune skriptale doshko abhilekhabat banaeka ayat hun, anuman talim bhaeko model ka.

**dhyan dinuparne kura**

dayan nabhai bayan matra bhaeko tasbir chhutne (FN) ko ummedabar ho. ulto, dayan matra thapieko ayat FP ho ki
hoina milaune niyam (class, IoU, confidence) le tay garchha. dekhine rup matrale tunggo lagdain.

**sochnuhos**

- kati tasbir ma chhutnu (FN) chha? tyo dosh anumanko stambha ma kasto dekhinchha?

<!-- ne-cell: 17e80b20 | after-heading -->
**asaphalataka prakar**
<!-- ne-pair: Types of failure -->

<!-- ne-cell: 17e80b20 -->
herda asaphalataka prakar dekhinchhan. talako talikako "sambhabit karan" **anuman** ho. tasbir ra label herer
ek-ek garera jaanchnuhos.

| prakar | lakshan | sambhabit karan (anuman) | jaanchne tarika |
|---|---|---|---|
| chhutnu | rato ayat matra chha (milne anuman chhaina) | dosh halka, dherai sano, prashikshan udaharan thorai, threshold uchcha | tyo tasbirko label ra dekhine rup jaanchnuhos; threshold pramanikaran data ma sarnuhos |
| jhuto pahichan | hariyo ayat matra chha (milne sahi label chhaina) | prishthabhumiko bhinnata kam, buttalai dosh thannu | milaune niyam (class, IoU, confidence) lagaepachhi matra nirnaya garnuhos |
| sthan namilnu | ayat adha matra milchha (IoU kam) | label lagaune tarika asthir, mildo akarako bhram | label ra nirdeshangk paribartan jaanchnuhos. **threshold sarda ayatako sthan sardain** |
| Class galti | chisolai kalo thoplo thannu | dekhine rup milnu, udaharanko asamanata | confusion matrix ma class-bichako bhram jaanchnuhos |

<!-- ne-cell: 64c7855e | after-heading -->
**obharaphiting ra nahun sakne abastha**
<!-- ne-pair: Overfitting, and what else can look like it -->

<!-- ne-cell: 64c7855e -->
prashikshan data ma kshamata uchcha ra nadekhieko data ma kshamata kam hune abastha lai **obharaphiting** bhaninchha. tar
parikshan datako kshamata kam hunuko karan obharaphiting matra hoina.

| sambhabana | jaanchne tarika |
|---|---|
| obharaphiting | pramanikaranko loss ra maapan ko prabritti hernuhos (prashikshan ghatdai janchha, pramanikaran ghatna rokinchha) |
| kam prashikshan (underfitting) | prashikshan data ma pani kshamata kam chha ki hernuhos |
| labelko galti | asaphal tasbirko label tasbir ma banaera jaanchnuhos |
| khichaiko abastha farak | prashikshan ra parikshan tasbirko ujyalo, prishthabhumi ra kon sangai rakher hernuhos |
| prashikshan ra parikshan tasbirko dekhine rup farak (domain shift) | pratinidhitb garne bastabik data ma mulyankan garnuhos |

upay euta matra hoina. data badhaunu upayogi hunchha, tar **sadhain sabaibhanda prabhabakari hunchha bhanne chhaina**.
labelko galti sudharnu badhi kaam lagn sakchha.

yo talimko 64 tasbir obharaphiting sajilai hune abasthamadhye ek ho. **ramro sankhya naaunu galti hoina.**

<!-- ne-cell: f152c1d1 | after-heading -->
## Part 5 din 5 sang sajha tasbir ma abhilekh

<!-- ne-cell: 29056356 | after-heading -->
**arko tasbir setama pani kina abhilekh garne**
<!-- ne-pair: Why record results on another image set -->

din 5 ma **YOLO ra PatchCore lai eutai tasbir ma tulna** garinchha. tyaska lagi yahan **tulnaka lagi
banaiyeko tasbir set** ma YOLO ko natija abhilekh garinchha. lakshya
`assets/anomaly_dataset/pvc_sheet/test/` ho. yi tasbir **prashikshan ma prayog bhaeka chhainan**.

tulnaka lagi banaiyeko set ma 52 tasbir chhan. din 5 notebook 02 le yaslai **calibration** ra **test**
gari 26/26 ma bandaphant garchha. niyam sthir chha (`val_split_mode="from_test"`, anupat 0.5,
`seed=2026`), ra **yo Part le pahile nai tay garera `submissions/day04/shared_set_split.json` ma
surakshit garchha**. din 5 le haatama bhaeko anomalib ko bandaphant yo abhilekh sang milchha ki
jaanchera matra agadi badhchha.

kram mahatwapurna chha. **sthir garnuaghi testko score banaunu hudaina** — yo bhaagko uddeshya tyahi ho.

| kahile / when | ke garne / what |
|---|---|
| sthir garnuaghi / before the freeze | calibration ka 26 tasbir matra mulyankan garera `yolo_predictions_on_shared_set.json` ma surakshit garne |
| sthir garepachhi / after the freeze | Part 5 ko `shared-sealed-test` cell le test ka 26 tasbir **ek patak matra** mulyankan garera chhuttai file ma sealed garne |

threshold tay garna paune calibration ko score le matra ho. **test ko score sthir nagare samma
hundaina.** nahereko kuralai threshold ma prayog garna sakindaina.

> Part 2 ko `split="test"` mulyankan sang **yo data farak ho**. Part 2 `assets/yolo_dataset` ko test
> bandaphant ho; yahan `assets/anomaly_dataset/pvc_sheet/test` ko tulnaka lagi set ho. duilai milaera
> nishkarsh nikaalnu hundaina.

<!-- ne-cell: shared-sealed-test-intro | after-heading -->
**sthir garepachhi ek patak matra**
<!-- ne-pair: Once, after the freeze -->

din 5 notebook 03 ma dui threshold sthir garepachhi, talako cell **ek patak matra** chalaunuhos.
test ka 26 tasbir yahin pahilo patak mulyankan bhaera
`submissions/day04/yolo_predictions_sealed_test.json` ma sealed hunchhan.

talako kura madhye kunai chhaina bhane yo cell **mulyankan nagari rokinchha**. bhaeko sealed file pani
badaldaina.

- sthir abhilekh `submissions/day05/comparison_freeze_record.json` ra tyasko ghoshana
- sthir abhilekh ma lekheko bandaphant ra yo Part ma tay gareko bandaphant ko milan
- sthir abhilekh ma lekheko YOLO weight ra yahan load bhaeko weight ko milan

**kernel YOLO batabaran mai** rakhera chalaunuhos. anomalib batabaran ma `ultralytics` chhaina,
tyasaile yo cell chaldaina. kernel feri suru gareko bhane Part 5 ko bandaphant cell baat feri
chalaunuhos. model feri prashikshan gareko bhane **yo arko experiment** ho; sealed garnuaghi din 5 ko
sthir charan baat feri garnuhos.

<!-- ne-cell: ba368ee2 | after-heading -->
## abhyas

<!-- ne-cell: 68c27e48 | after-heading -->
**abhyas 1 (adharabhut): precision ra recall abhilekh garne**
<!-- ne-pair: Exercise 1 (basic): record precision and recall -->

<!-- ne-cell: 68c27e48 -->
Part 2 ko natija talako talika ma lekhnuhos.

| maapan | maan | karyasthalama arth |
|---|---|---|
| precision | | |
| recall | | |
| mAP50 | | |

- pura bhaeko maapan: tin maan abhilekh bhaeka chhan ra precision ra recall aphnai shabdama byakhya garna sakinchha

<!-- ne-cell: 83c679ee | after-heading -->
**abhyas 2 (madhyam): asaphal udaharan surakshit garne**
<!-- ne-pair: Exercise 2 (intermediate): save failure examples -->

<!-- ne-cell: 83c679ee -->
Part 4 ka tasbir baat **chhutnu** ra **jhuto pahichan** khojer bhetieka `submissions/day04/` ma surakshit
garnuhos. file naam ma `miss_` / `false_alarm_` rakhnuhos.

yo chalaima kunai ek (wa dubai) prakarko **ek pani nahun** sakchha. tyasto abastha ma **khojeko dayara ra sankhya**
lekher "bhetien" abhilekh garnuhos. nabhaeko asaphalata banaunu hundaina.

- khojeko dayara: parikshanka 16 tasbiramadhye Part 4 ma dekhaieka 6 (seed 1)
- ganieko sankhya: chhutnu 0, jhuto pahichan 0 (lagu hune abastha ma)

- pura bhaeko maapan: dui file chhan, wa "bhetien" dayara ra sangkhyasahit abhilekh bhaeko chha
- pura bhaeko maapan: bhetieka harek asaphalatako karanabare anuman lekhieko chha

<!-- ne-cell: cf0ad36e | after-heading -->
**abhyas 3 (baikalpik): sudharako yojana lekhne**
<!-- ne-pair: Exercise 3 (optional challenge): write an improvement plan -->

<!-- ne-cell: cf0ad36e -->
asaphalataka prakarka adharama **aba ke garne** bhanera prathamikatako kram ma tin kura lekhnuhos. pratyekama
"kina yasle kaam garchha" ra "kasari jaanchne" pani lekhnuhos.

data badhaunu bikalpamadhye ek ho, tar **sadhain pahilo prathamikata hundaina**. labelko galti sudharnu badhi kaam
lagn sakchha. **aniwarya hoina.**

| prathamikata | garnuparne kaam | kina kaam garchha | kasari jaanchne |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

pura bhaeko maapan: tin kaam, karan ra jaanchne tarika lekhieka chhan.

<!-- ne-cell: e1f991d3 | after-heading -->
#### bujhai jaanchne prashna

<!-- ne-cell: e1f991d3 -->
1. precision ra recall le kramaisang ke napchhan?
2. recall kam bhae karyasthalama kasto samasya hunchha?
3. tasbir-starko confusion matrix ra Ultralytics ko bastu-starko matrix ma line ra stambhale ke janaunchhan?
   `background` ko stambha ra linele kramaisang ke ganchhan?
4. parikshan datako kshamata kam hunda obharaphitingabahek aru ke karan huna sakchha? kasari jaanchne?
5. `split="test"` ma kina mulyankan garne? `split="train"` kina namilne ho?

<!-- ne-cell: 440278a7 | after-heading -->
## samasya parema

<!-- ne-cell: 440278a7 -->
truti aepachhi pahile "kun cell ma", "kun line ma", "ke sandesh ayo" bhanera lekhnuhos. bujhaunuparne kaam ma pani
tyahi abhilekh rakhnuhos.

| lakshan | ke garne |
| --- | --- |
| `FileNotFoundError` prashikshan bhaeko weight bhetien | pahile 04_02 ko prashikshan chalaunuhos. `training_results/day04/` jaanchnuhos. |
| `model.val()` le truti dinchha | `data.yaml` ko `path` purano huna sakchha. 04_02 ko Part 2 feri chalaunuhos. |
| sabai maapan 0 hunchha | parikshan label khali wa class sankhya namileko huna sakchha. 04_01 ko jaanch ma pharkanuhos. |
| confusion matrix ko chitra chhaina | mulyankan `plots=True` rakher feri chalaunuhos. prashikshan dohoryaunu pardaina. |
| matrix ko terso-thado thaha bhaen | chitrako aksh label padhnuhos. yo sanskaranako Ultralytics chitra ma terso sahi (True), thado anuman (Predicted) ho. |
| sajha tasbir set chhaina | `python assets\scripts\prepare_datasets.py --only anomaly` chalaunuhos. |

<!-- ne-cell: 9b6959aa | after-heading -->
## sampannata janchasuchi

<!-- ne-cell: 9b6959aa -->
**aniwarya bunda matra** diieka chhan. **abhyas 3 (baikalpik) aniwarya hoina**; nagare pani pura maninchha.
sabai ma chinh lagepachhi yo notebook pura hunchha.

**aniwarya**

- [ ] Part 1–Part 5 padher sthir garnuaghi ka sabai code cell chalaen
- [ ] `split="test"` ma mulyankan garen
- [ ] confusion matrix janchen
- [ ] saphal ra asaphal udaharan tasbir ma heren
- [ ] `yolo_predictions_on_shared_set.json` surakshit garen (calibration matra)
- [ ] sthir garepachhi `shared-sealed-test` ek patak matra chalaen
- [ ] abhyas 1–2 (aniwarya) garen
- [ ] bujhai jaanchne 5 prashnako uttar dien
- [ ] notebook surakshit garen

**baikalpik**

- [ ] abhyas 3 (baikalpik): sudharaka tin kaam prathamikatasahit lekhen

<!-- ne-cell: 24754a39 | after-heading -->
## thap adhyayan (baikalpik)

<!-- ne-cell: 24754a39 -->
### sandarbha lingk

- [Ultralytics Val mod](https://docs.ultralytics.com/modes/val/)
- [confusion matrix kasari padhne](https://scikit-learn.org/stable/modules/model_evaluation.html#confusion-matrix)
- [precision ra recall](https://scikit-learn.org/stable/modules/model_evaluation.html#precision-recall-f-measure-metrics)

### thap chunauti (aniwarya hoina)

`conf` 0.1 ra 0.6 rakher `model.val()` chalaunuhos ra precision ra recall ko paribartan tulna garnuhos.
