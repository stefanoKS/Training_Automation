<!--
Nepali anuwad / Nepali translation source for
notebooks/Day03_YOLO_Basics/Day03_01_YOLO_Concepts.ipynb
-->
# din 3 notebook 01 — Nepali anuwad

<!-- ne-cell: fa4f448a | after-heading -->
# din 3 notebook 01: YOLO bujhne

<!-- ne-cell: fa4f448a -->
## sikai lakshyaharu

| Nepali |
| --- |
| 1. bastu pahichan garne model le ke garchha bataun sakne. |
| 2. baunding baks ra nirdeshangk lekhne tarika bataun sakne. |
| 3. bishbas score (confidence) ko arth bataun sakne. |
| 4. IoU hataile ganana garna sakne. |
| 5. pahile nai talim bhaeko model le PVC ko dosh kina bhetna nasakchha bataun sakne. |

## yo notebookko adharabhut jankari

| bishay | biwaran |
| --- | --- |
| sikai samay (anuman) | 80 minet |
| kathinai | surubati tah |
| poorwashart | din 1 ra din 2 sakieko hunuparchha. |
| aawashyak laibreri | numpy, matplotlib, pillow |
| prayog hune kernel | aivision |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 3](../../COURSE_SYLLABUS.md#day3) |

### bujhaunuparne kaam

| Nepali |
| --- |
| IoU hataile ganana gareko natija |
| YOLO dhanchako nirdeshangk ganana |

<!-- ne-cell: fig-teach_score_vs_correctness | after-heading -->
### confidence ra sahi hunu farak kura hun

<!-- ne-cell: fig-teach_score_vs_correctness | after-image:../../assets/diagrams/teach_score_vs_correctness.png -->
chitra: 5 bata pahichanko confidence ra sahi uttar sang tulna garda kati sahi bhayo (maan udaharanka lagi matra).

**dhyan dinuparne kura**

confidence badhi bhaeko pahichan pani galat huna sakchha, ra kam bhaeko pani sahi huna sakchha. confidence bhaneko model
le dieko score ho; yo sahi uttar pani hoina, "sahi hune sambhabana" pani hoina. sahi chha ki chhaina bhanne kura sahi
label sang tokieko niyam anusar milaera janchinchha.

**sochnuhos**

- threshold 0.60 ma banki rahane pahichanamadhye kun-kun galat chhan?

<!-- ne-cell: audit-learning-loop | after-heading -->
### anuman garnuhos, chalaunuhos, hernuhos, byakhya garnuhos

<!-- ne-cell: audit-learning-loop -->
class bhaneko doshko prakar ho. confidence model ko score ho, sahi hune gyarenti hoina. mahattwapurna cell
chalaunuaghi input, kaam ra natija ek-ek bakyama lekhnuhos. pahile anuman garera chalaunuhos ra maan wa chitra
hernuhos. `x2` matra badaler feri anuman gari chalaunuhos. janajan rakhieka truti ra nasakieka abhyaska
nirdeshan pachhyaunuhos.

<!-- ne-cell: 65c518c5 | after-heading -->
## yo notebook kahan parchha

<!-- ne-cell: 65c518c5 -->
| bishay | biwaran |
| --- | --- |
| din | din 3 |
| ajako kram | ajako notabukamadhye 1 / 3 |
| lagne samay | 80 minet |
| poorwashart | din 2 |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 3](../../COURSE_SYLLABUS.md#day3) |

dinko samayatalika `COURSE_SYLLABUS.md` ma eutai thaun ma chha. yo notebook tyasko euta bhaag matra ho.

<!-- ne-cell: f78a487c | after-heading -->
## Part 0 tayari

<!-- ne-cell: 6e36b163 | after-heading -->
#### YOLO ke ho

<!-- ne-cell: 6e36b163 -->
YOLO (You Only Look Once) bhaneko tasbir baat ayat, talim lieka class ra score anuman garne bastu-pahichan
model ho. model ko forward pass ra postprocessing miler natija banchha; "ekai patakako ganana matra" bhanne hoina.
utpadan lineko gatima samay pugchha ki pugdain bhanne kura bastabik yantra, tasbirko akar, purb-prashodhan ra
pachhi-prashodhan sahit naper matra thaha hunchha.

<!-- ne-cell: 3423fdc1 | after-heading -->
## Part 1 baunding baks

<!-- ne-cell: fig-teach_bbox_coords | after-heading -->
### tasbir ma ayat padhne

<!-- ne-cell: fig-teach_bbox_coords | after-image:../../assets/diagrams/teach_bbox_coords.png -->
chitra: eutai doshko ayatalai bayan piksel sankhyale ra dayan tasbirko akarale bhaag gareko maanle dekhaieko chha.
nirdeshangk ganana garera chitra ma rakhieka hun.

**dhyan dinuparne kura**

bayan pikselako xyxy ra dayan tasbirko akarale bhaag gareko cx, cy, w, h — **eutai baks** ho. purai tasbir
sano-thulo garda 0–1 ka maan arthapurna rahanchhan, tar katda (crop) wa khali thaun thapda (letterbox) nirdeshangk
badalinchhan. API-anusar dhancha farak hunchha, naam jaanchnuhos (Ultralytics ko `xyxy`, OpenCV ko
`boundingRect` xywh ho).

**sochnuhos**

- tasbirko bayan adha bhaag matra katda, pahile cx = 0.6 bhaeko baks ke hunchha?

<!-- ne-cell: 9bff031a | after-heading -->
**ayatale gherne, chaar sankhya**
<!-- ne-pair: A rectangle is four numbers -->

<!-- ne-cell: 9bff031a -->
baunding baksale dosh lai ayatale gherchha. baks chaar sankhyale lekhinchha, ra ti sankhyako kram
(**nirdeshangkko dhancha**) API-anusar tokieko hunchha.

| dhancha | chaar sankhya | kahan prayog hunchha |
|---|---|---|
| `xyxy` | `x1, y1, x2, y2` (mathi-bayan ra tal-dayan) | Ultralytics ko `result.boxes.xyxy`, chitra banaune laibreri |
| `xywh` | `x, y, w, h` (mathi-bayan ra chaudai, uchai) | `cv2.boundingRect()` (OpenCV ko kantur baripariko ayat) |
| `xc, yc, w, h` (samanyikrit) | kendra ra akaralai tasbirko akarale bhaag gareko 0–1 maan | YOLO ko label file (sahi label) |

uhi "chaar sankhya" bhae pani `xyxy`, `xywh` ra YOLO label ma **arth ra kram farak** hunchha. function bolaunda
kun dhancha pharkinchha sadhain jaanchnuhos.

YOLO label **kendra-shaili** ma hunchha ra **tasbirko chaudai-uchaile bhaag gareko 0–1 maan** (samanyikrit) hunchha.
purai tasbir eutai anupaat ma sano-thulo garda yi maan uhi rahanchhan. tar tasbirko bhaag katda (crop) wa anupaat
jogaun khali thaun thapda (letterbox) adhar banne phrem badlinchha, tyasaile tyasai prayog garna mildaina. phrem
badaliyo bhane nayan phremako chaudai-uchaile feri ganana garnuhos.

<!-- ne-cell: aaf95ec6 | after-heading -->
**nirdeshangk paribartan aphain ganana garne**
<!-- ne-pair: Do the conversion yourself -->

<!-- ne-cell: aaf95ec6 -->
piksel nirdeshangk `(x1, y1, x2, y2)` baat YOLO dhanchama badalna chaar line pugchha:

```text
xc = (x1 + x2) / 2 / tasbirko chaudai
yc = (y1 + y2) / 2 / tasbirko uchai
w  = (x2 - x1)     / tasbirko chaudai
h  = (y2 - y1)     / tasbirko uchai
```

bhaag garna birse maan 1 bhanda badhi hunchha. **0–1 dayarabhitra chha ki chhaina sadhain jaanchnuhos.**

yi chaar linele **mul tasbirko purai chaudai ra uchai** prayog garchhan. katepachhi (crop) wa letterbox ko khali
thaun thapepachhi nayan tasbirko chaudai-uchaile feri ganana garnuhos. puranai maan prayog garda baks sarchha.

<!-- ne-cell: audit-teach_bbox_one_example | after-heading -->
### kod kasari padhne

<!-- ne-cell: audit-teach_bbox_one_example | after-image:../../assets/svg/teach_bbox_one_example.svg -->
chitra: class_id purnank ho ra samanyikrit garindain. (ganana garieko sansleshit udaharan ra yojanabaddha chitra;
model ko bastabik napieko natija hoina.)

**dhyan dinuparne kura**

class_id purnank ho ra samanyikrit garindain. input ra paribartan bhaeko maan aunlale pachhyaunuhos.

**sochnuhos**

`x2` matra 24 px badhaunda kendra ra chaudai kasari badlinchha?

<!-- ne-cell: 06fb8c28 | after-heading -->
### natijako udaharan

<!-- ne-cell: clarity-bbox-predict | after-heading -->
#### uhi ayat tin dhanchama padhne

<!-- ne-cell: clarity-bbox-predict -->
input 240×240 tasbir ma pahile nai dekhaieko `(96,72,168,132)` ho. talako cellle tin dhanchako talika dekhaunchha.
anuman: dayan chheu `x2` matra 24 px badhaunda chaudai ra kendra x kati px badhchha? y ka maan badalinchhan?

<!-- ne-cell: clarity-bbox-interpret -->
chaudai 72 baat 96, kendra x 132 baat 144 hunchha. YOLO ko xc ra w matra badalinchhan; yc ra h uhi rahanchhan.
24 ko satta 12 rakher anuman garnuhos ra badaleko ayat mul chitrako ayatabhanda kina farak chha byakhya garnuhos.

<!-- ne-cell: ea7a5e4f | after-heading -->
## Part 2 class ra bishbas score

<!-- ne-cell: 2b02787b | after-heading -->
**class label (barga ko naam)**
<!-- ne-pair: Class label -->

<!-- ne-cell: 2b02787b -->
**class** bhaneko "prakar" ho. YOLO le pahichan talim lieka prakaramadhye euta ma rakhchha.

samanya pahile nai talim bhaeko model (COCO dataset) le 80 prakar jandachha. jastai `person`, `car`, `bus`,
`dog`, `bottle` …

yas ma **`black_spot` (kalo thoplo) wa `scratch` (chiso) chhainan**. tyasaile PVC ko dosh bhetna sakdain.

<!-- ne-cell: 797f53b6 | after-heading -->
**bishbas score (confidence)**
<!-- ne-pair: Confidence -->

<!-- ne-cell: 797f53b6 -->
**confidence** model le pratyek ummedabaralai dieko **score** ho. yo 0–1 bichako maan hunchha.

| maan | kasari padhne |
|---|---|
| 0.95 | score uchcha (model le baliyo samarthan gareko) |
| 0.50 | madhyam score |
| 0.10 | score nyoon |

**yo score "sahi hune sambhabana" hoina.** 0.8 lai "80% sambhabanale sahi" bhanera padhna mildaina, 0.50 pani
"adha-adha sambhabana" hoina. scorele talim lieko class ko dekhine rupasang kati milchha bhanne kura model le
sankhya ma badaleko ho. **score uchcha bhae pani sahi hunchha bhanne chhaina, ra kam bhae pani sahi pahichan hunchha.** sahi chha ki
chhaina bhanne kura sahi label sang tokieko niyam (jastai IoU kunai threshold wa badhi) le janchinchha.

<!-- ne-cell: dd8128d0 | after-heading -->
## Part 3 IoU (obharalyapako matra)

<!-- ne-cell: d097f138 | after-heading -->
### pratichchhed, sanyog ra IoU

<!-- ne-cell: d097f138 | after-image:../../assets/diagrams/teach_iou_rects.png -->
chitra: A (sahi uttar) ra B (anuman) ka ayat sanchchai milaera pratichchhed (obharalyapako kshetraphal) ra sanyog (dui
ayat miler banne kshetra; obharalyap ek patak matra ganinchha) ganana garieko. yo chitra ma 6,750 ÷ 15,150 ≒ 0.45 ho.

**dhyan dinuparne kura**

IoU le "obharalyapako matra" euta sankhya ma badalchha. 0 najik hunda obharalyap kam, 1 najik hunda thyakkai
mileko. yo **kshetraphalako anupaat** hunale ekai hundaina. sanyog dui kshetraphal joder matra paindain; obharalyap
dui patak naganna ek patak matra ganinchha.

**sochnuhos**

- IoU 0.3 hunda pratichchhed "anumanko ayat" ko 30% ho, "sahi ayat" ko 30% ho, ki aru kunai kurako 30%?

<!-- ne-cell: 4dd6c2de | after-heading -->
**IoU bhaneko "dui ayatako obharalyapako matra"**
<!-- ne-pair: IoU measures how much two boxes overlap -->

<!-- ne-cell: 4dd6c2de -->
**IoU** le anuman garieko baks ra sahi baks **kati obharalyap chhan** bhanne kura 0–1 ma dekhaunchha.

```text
IoU = pratichchhedako kshetraphal ÷ dui ayat miler banne kshetraphal (obharalyap ek patak matra)
```

"dui ayat miler banne kshetra" nai **sanyog** ho. dui kshetraphal tyasai jodda obharalyap dui patak ganinchha,
tyasaile obharalyap ek patak matra ganine gari jodaghatau garinchha.

- `IoU = 1.0` … thyakkai milyo
- `IoU = 0.5` … thikai milyo
- `IoU = 0.0` … kehi pani obharalyap chhaina

`IoU = 0.3` ko arth "pratichchhedako kshetraphal **dui ayat miler banne kshetrako** 30%" ho. anumanko ayatako
30% wa sahi ayatako 30% hoina.

samanyataya `IoU >= 0.5` lai "sahi pahichan" maninchha. tar yo **chalan** ho, prayog anusar farak parchha.

<!-- ne-cell: 7805f6a4 | after-heading -->
### natijako udaharan

<!-- ne-cell: 5cde7a67 | after-heading -->
**hataile ganana garera jaanchne**
<!-- ne-pair: Verify by hand -->

<!-- ne-cell: 5cde7a67 -->
"ali sareko" abastha hataile ganana garaun.

- sahi: `(100,100)` dekhi `(200,200)` → kshetraphal **10,000**
- anuman: `(110,110)` dekhi `(210,210)` → kshetraphal **10,000**
- pratichchhed: `(110,110)` dekhi `(200,200)` → 90 × 90 = **8,100**
- sanyog: 10,000 + 10,000 − 8,100 = **11,900**
- IoU = 8,100 ÷ 11,900 ≒ **0.681**

<!-- ne-cell: 27c2070a | after-heading -->
**ayat sarer pratichchhed, sanyog ra IoU herne**
<!-- ne-pair: Move a box and watch the intersection, the union and IoU -->

<!-- ne-cell: 27c2070a -->
`offset_x` ra `offset_y` matra sarinchhan. sarne **anumanko ayat** ho.

| anuman | ke herne |
|---|---|
| sarai 0 | IoU kati? |
| sarai badhaune | pratichchhed ra sanyog ke hunchha? |
| kehi obharalyap nahune | IoU kati? |

widget nabhae pani talako parameter cellle uhi prayog garna dinchha.

<!-- ne-cell: 5ae021d1 | after-heading -->
## Part 4 pahile nai talim bhaeko model ra weight file

<!-- ne-cell: 112b5bfa | after-heading -->
**"talim bhaisakeko" model lyaune**
<!-- ne-pair: Starting from something already trained -->

suru dekhi talim garna dherai tasbir ra lamo ganana samay chahinchha. kati chahinchha bhanne kura model, data ra computer anusar
dherai farak parchha. tyasaile **pahile nai dherai tasbir ma talim bhaeko model** prayog garinchha. yas lai
**pahile nai talim bhaeko model (pretrained model)** bhaninchha.

**weight file** bhaneko tyo talimko natija rakhieko file ho.

| shabd | arth |
|---|---|
| pretrained model | aru data ma pahile nai talim bhaeko model |
| weight | talimle tay gareka sankhyaharuko samuh |
| anuman (inference) | talim bhaeko model le nayan tasbir jaanchne kaam |
| fine-tuning | pretrained model lai aphnai data ma thap talim garne |

din 4 ma garine kaam **fine-tuning** ho. COCO ma sikeko "bastuko akar herne kshamata" udharo liera PVC ko
dosh sikainchha. yo talimko abhilekhama din 4 ko fine-tuning (15 epoch, CPU) karib 90 sekendama sakiyo
(`training_results/day04/pvc_defect_quick/results.csv` ko `time` stambha, antim line 89.7 sekend),
kinabhane yo talimko dataset sano chha. tasbir wa epoch badhaunda samay pani badhchha.

<!-- ne-cell: clarity-optional-weight-formats | after-heading -->
#### baikalpik: checkpoint ra export

<!-- ne-cell: clarity-optional-weight-formats -->
pahilo anumanapachhi padhne prabidhik thap jankari.

| file | bhitra ke hunchha |
|---|---|
| `.pt` (PyTorch) | **talimko checkpoint**: model ko banabat, talimle tay gareka parameter ra talimko abastha |
| `.onnx` (ONNX) | **export garieko ganana graph ra parameter**: talimko abastha hoina, arko batabaran ma chalaun banaiyeko dhancha |

`.pt` lai `.onnx` ma export garda talimko abhilekh (epoch sankhya, optimizer ko abastha) sardain.
"talim jari rakhna milne file" ra "arko batabaran ma chalaune file" farak kura hun.

<!-- ne-cell: c82b89d9 | after-heading -->
#### COCO model ra PVC dosh class

<!-- ne-cell: c82b89d9 -->
COCO pretrained model sang yo samagrika `black_spot` / `scratch` / `streak` dosh class chhainan. tyasaile
chaheko doshko naam bishbasaka sath rakhna sakindaina. kehi nadekhaune bhanne pani chhaina; sambandh nabhaeko class pharkaun
sakchha. pahichan shunya hunu pani "PVC samanya chha" bhanne praman hoina. din 4 ma yahi talimka labelle model talim garinchha.

<!-- ne-cell: 0b071006 | after-heading -->
## abhyas

<!-- ne-cell: 00ad41f6 | after-heading -->
**abhyas 1 (adharabhut): YOLO dhanchama badalne**
<!-- ne-pair: Exercise 1 (basic): convert to YOLO format -->

<!-- ne-cell: 00ad41f6 -->
tasbirko akar 640 × 480 ra baks `x1=320, y1=200, x2=400, y2=260` hunda YOLO dhanchaka chaar maan ganana garnuhos.

pura bhaeko maapan: charai maan 0–1 dayarabhitra chhan ra 6 dashamalabasamm dekhaieka chhan.

<!-- ne-cell: cc2d6cd5 | after-heading -->
**abhyas 2 (madhyam): IoU hataile ganana garera jaanchne**
<!-- ne-pair: Exercise 2 (intermediate): a hand calculation of IoU -->

<!-- ne-cell: cc2d6cd5 -->
sahi `(50, 50, 150, 150)` ra anuman `(100, 50, 200, 150)` ko IoU **kagajama** ganana garepachhi talako cellle jaanchnuhos.
pratichchhedako kshetraphal dui ayat miler banne kshetrako kati ansh ho, sochnuhos.

pura bhaeko maapan: kagajako maan ra `iou(...)` ko maan milnuparchha (0.333).

<!-- ne-cell: 50f63c6d | after-heading -->
**abhyas 3 (baikalpik): din 4 ma ke sikaunuparchha bhanera yojana banaune**
<!-- ne-pair: Exercise 3 (optional challenge): plan what Day 4 must teach the model -->

<!-- ne-cell: 50f63c6d -->
pretrained model le PVC ko dosh kina bhetna sakdain bhanne chaar karanka adharama din 4 ma ke tayar garnuparchha bhanera
byabasthit garnuhos.

| bishay | tapainko uttar |
|---|---|
| class ko naam | |
| prati tasbir doshko sankhya (anuman) | |
| chahine tasbir sankhya (prashikshanka lagi) | |
| sahi labelko dhancha | |

pura bhaeko maapan: talika bharieko chha ra label dhanchako mahalama YOLO ko kendra dhancha
(`class_id x_center y_center width height`) lekhieko chha.

<!-- ne-cell: 69ca863c | after-heading -->
#### bujhai jaanchne prashna

<!-- ne-cell: 69ca863c -->
1. YOLO ko natija ma ke-ke hunchha? tin kura bhannuhos.
2. confidence 0.9 bhaeko pahichan sadhain sahi hunchha? karan pani lekhnuhos.
3. IoU 0.3 hunda pratichchhed "kasako" 30% ho?
4. pretrained model le PVC ko dosh kina bhetna sakdain, dui karan bhannuhos.
5. "anuman" ra "prashikshan" bichako farak samayko drishtile bataunuhos.

<!-- ne-cell: 67d928a3 | after-heading -->
## samasya parema

<!-- ne-cell: 67d928a3 -->
truti aepachhi pahile "kun cell ma", "kun line ma", "ke sandesh ayo" bhanera lekhnuhos. bujhaunuparne kaam ma pani
tyahi abhilekh rakhnuhos.

| lakshan | ke garne |
| --- | --- |
| YOLO dhanchako maan 1 bhanda badhi hunchha | tasbirko chaudai-uchaile bhaag garna birsieko chha. `/ image_width` jaanchnuhos. |
| IoU rinatmak aaunchha | obharalyap nabhae 0 hunuparchha. `max(0.0, ...)` lekhna birsieko chha ki jaanchnuhos. |
| `confidence` ra sambhabana misaunchhu | confidence model le dieko score ho, sahi hune sambhabana hoina. sahi chha ki chhaina sahi label sang tulna garera jaanchnuhos. |
| sankhya notako udaharanabhanda ali farak aaunchha | prayah raund gareko dashamalab sankhya farak hunchha. `round()` ma lekhieko angk jaanchnuhos. |

<!-- ne-cell: 60e5ea71 | after-heading -->
## sampannata janchasuchi

<!-- ne-cell: 60e5ea71 -->
**aniwarya** bhaneko talako "aniwarya" soochi matra ho. **abhyas 3 ra thap chunauti baikalpik** hun; nagare pani pura
maninchha. samay banki bhae ma matra garnuhos.

**aniwarya**

- [ ] Part 1–Part 4 padher sabai code cell chalaen
- [ ] YOLO dhanchako nirdeshangk aphain ganana garen
- [ ] IoU hataile ganana garera kodasang milaen
- [ ] abhyas 1 ra 2 (aniwarya) garen
- [ ] bujhai jaanchne 5 prashnako uttar dien
- [ ] notebook surakshit garen

**baikalpik**

- [ ] abhyas 3 (baikalpik): din 4 ka tayarika bunda byabasthit garen
- [ ] thap chunauti: COCO ka 80 class madhye utpadan nirikshan ma kaam lagne kunai chha ki heren

<!-- ne-cell: f9c29d7d | after-heading -->
## thap adhyayan (baikalpik)

<!-- ne-cell: f9c29d7d -->
### sandarbha lingk

- [Ultralytics kagajat](https://docs.ultralytics.com/)
- [Ultralytics: bastu pahichan kary](https://docs.ultralytics.com/tasks/detect/)
- [COCO datasetka class ko soochi](https://cocodataset.org/#explore)

### thap chunauti (aniwarya hoina)

COCO ka 80 class ko soochi herer utpadan nirikshan ma kaam lagne class chha ki chhaina khojnuhos.
