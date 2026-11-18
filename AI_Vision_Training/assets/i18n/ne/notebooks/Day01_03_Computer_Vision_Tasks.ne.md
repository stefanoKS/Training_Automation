<!--
Nepali anuwad / Nepali translation source for
notebooks/Day01_AI_Fundamentals/Day01_03_Computer_Vision_Tasks.ipynb

Each block starts with an ne-cell directive naming the notebook cell id.
Do not translate code, file names, URLs or kernel names.
-->
# din 1 notebook 03 — Nepali anuwad

<!-- ne-cell: 85059ad2 | after-heading -->
# din 1 notebook 03: computer bhijan AI ka kisimaharu

<!-- ne-cell: 85059ad2 -->
## sikai lakshyaharu

| Nepali |
| --- |
| 1. image classification, object detection, segmentation ra anomaly detection ko farak bujhaun sakne. |
| 2. pratyekako natija ke hunchha bhanna sakne. |
| 3. utpadan nirikshan ma kun kahan prayog garne bhanera sujhab din sakne. |
| 4. pratyekako phaida ra sima bujhaun sakne. |

## yo notebookko adharabhut jankari

| bishay | biwaran |
| --- | --- |
| sikai samay (anuman) | 65 minet |
| kathinai | surubati tah |
| poorwashart | din 1 notebook 01 ra 02 sakieko hunuparchha. |
| aawashyak laibreri | numpy, matplotlib, pillow |
| prayog hune kernel | aivision |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 1](../../COURSE_SYLLABUS.md#day1) |

### bujhaunuparne kaam

| Nepali |
| --- |
| 4 kaamko farak bujhaune talika |
| PVC nirikshanka lagi sujhab (abhyas 3) |

<!-- ne-cell: 31addddb | after-heading -->
## yo notebook kahan parchha

<!-- ne-cell: 31addddb -->
| bishay | biwaran |
| --- | --- |
| din | din 1 |
| ajako kram | ajako notabukamadhye 3 / 3 |
| lagne samay | 65 minet |
| poorwashart | `Day01_02_Pixels_and_Images.ipynb` |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 1](../../COURSE_SYLLABUS.md#day1) |

dinko samayatalika `COURSE_SYLLABUS.md` ma eutai thaun ma chha. yo notebook tyasko euta bhaag matra ho, aphno
chhuttai samayatalika rakhdain. samay thaha nabhae pahile tyahi file hernuhos.

<!-- ne-cell: audit-learning-loop | after-heading -->
### anuman garnuhos, chalaunuhos, hernuhos, byakhya garnuhos

<!-- ne-cell: audit-learning-loop -->
classification le chitrako jabaph, detection le sthan, segmentation le akar, anomaly detection le
samanyasangako farak dinchha. mahattwapurna cell chalaunuaghi input, kaam ra natija ek-ek bakyama lekhnuhos.
pahile anuman lekhnuhos, tyaspachhi cell chalaera maan wa chitra hernuhos. euta doshko natija dhancha badaler
feri anuman garera chalaunuhos. janajan rakhieka truti ra nasakieka abhyaska lagi lekhieko nirdeshan
pachhyaunuhos.

<!-- ne-cell: d436d9c5 -->
> ### ⚠️ yo notebookka chitrabare
>
> yo notebook ma dekhine "detection natija" ra "heatmap" **abadharana chitra** hun.
> AI le bastabamai anuman gareko hoina. chitramathi **manisale koreka** byakhyaka chitra hun.
> bastabik AI anuman din 3 pachhi garinechha.

<!-- ne-cell: 25ce99d9 | after-heading -->
## Part 0 tayari

<!-- ne-cell: 4aa1c309 | after-heading -->
**chitra ma prayog hune phant milaunuhos**
<!-- ne-pair: Configure Japanese text in figures -->

<!-- ne-cell: 4aa1c309 -->
Matplotlib ko purbanirdharit phantale Japani akshar dekhauna sakdain. tyasaile chitrako shirshak `□□□` jasto
dekhinchha. arko cellle Japani akshar dekhauna sakne phant khojer milaunchha. macOS wa Linux ma sbatah arko phant
chhaninchha.

<!-- ne-cell: 6c945e72 | after-heading -->
## Part 1 image classification (chitrako bargikaran)

<!-- ne-cell: audit-teach_cv_tasks_outputs | after-heading -->
### kod padhne tarika

<!-- ne-cell: audit-teach_cv_tasks_outputs | after-image:../../assets/svg/teach_cv_tasks_outputs.svg -->
chitra: uhi mask baat chaukon nikalinchha. (hisab garieko kritrim udaharan/yojanabaddha. model ko maapan garieko
natija hoina.)

**dhyan dinuparne kura**

uhi mask baat chaukon nikalinchha. input ra badaliepachhiko maan aunlale pachhyaunuhos.

**sochnuhos**

mask ko pixel sankhya ra chaukonako kshetraphal barabar hunchha?

<!-- ne-cell: d7f165e1 | after-heading -->
### 4 paribar, 5 natija udaharan

<!-- ne-cell: d7f165e1 -->
classification, detection, segmentation ra anomaly detection gari 4 paribar hun.
segmentation ma semantic ra instance gari 2 tarika bhaekole pachhika udaharan ma 5 natija dekhainchha.
mathiko uhi kritrim kalo thoploko chitra ma sthan pharkaune tarika kun hola anuman garnuhos. yo
bastabik anuman natija hoina.

<!-- ne-cell: ed68e4b2 | after-heading -->
**classification bhaneko "euta chitra ma euta jabaph"**
<!-- ne-pair: Classification gives one answer per image -->

<!-- ne-cell: ed68e4b2 -->
yo udaharanko image classification le **euta chitraka lagi euta label** pharkaune kaam ho
(euta chitra ma euta class dine, single-label classification).

```text
input: sitako euta chitra
natija: OK wa NG (+ tyasko bishbasaniyata)
```

**phaida:** banabat saral chha, lagu garna sajilo chha. euta chitra ma euta label die pugne hunale pixel-pichchhe
rang bharnubhanda sahi jabaphako data banaun sajilo hunchha.

**kami:** **kahan** bigreko ho thaha hundaina. "NG" bhanchha matra,
"dayantir 3 mm ko kalo thoplo chha" bhanera bataundain.
chahine datako matra dekhine tarikako phailabat, class sankhya ra chahieko shuddhatama nirbhar hunchha.
"classification ma sadhain sabaibhanda kam data pugchha" bhanna sakindaina.

<!-- ne-cell: 803b0934 | after-heading -->
## Part 2 object detection (bastu pahichan)

<!-- ne-cell: 7390e751 | after-heading -->
**detection bhaneko "kahan ke kati"**
<!-- ne-pair: Detection answers where, what and how many -->

<!-- ne-cell: 7390e751 -->
object detection le **doshko sthanalai charakon dhancha (bounding box) le gherer**
kisim ra bishbasaniyata pharkaunchha.

```text
input: sitako euta chitra
natija: [x1, y1, x2, y2] ko chaukon + kisim (kalo thoplo/chot/dharka) + bishbasaniyata
```

**phaida:** sthan ra sankhya thaha hunchha. doshko abhilekh ra line rokne nirnaya ma prayog garna sakinchha.

**kami:** **tay garieka class naam matra pharkaun sakchha**. sikai nabhaeko kisimako dosh janieka class
madhye euta ma thichiera parchha, wa bishbasaniyata kam raher chhutchha. sathai chaukonale gherne hunale tirchho chotama
atirikt kshetra pani parchha.

<!-- ne-cell: c5f9e59d | after-heading -->
## Part 3 segmentation (kshetra bibhajan)

<!-- ne-cell: 02bee1e7 | after-heading -->
**semantic segmentation (pixel-pichchhe classification)**
<!-- ne-pair: Semantic segmentation (classifying each pixel) -->

<!-- ne-cell: 02bee1e7 -->
segmentation le **pixel-pichchhe** "yo dosh ho wa hoina" pharkaunchha.
mask chitra (seto = dosh, kalo = samanya) natija ho.

**phaida:** doshko **kshetraphal** thaha hunchha. "0.5 mm² bhanda thulo dosh NG" jastai simasahit nirnaya garna
sakinchha. lamo-patalo chotako akar pani jastako tastai dekhauna sakinchha.

**kami:** sahi jabaphako data (mask) banaun **samay lagchha**.
euta chitraka lagi pixel-ekaima rang bharne kaam chahinchha.

kshetraphal mm² ma hisab garna **calibration** chahinchha. 1 pixel kati mm ho pahile tay nagareko bhae pixel
sankhyako kshetraphalalai mm² ko manakasang tulna garnuparne hunchha, ra nirnaya bigranchha (din 2 pachhi samhalinechha).

<!-- ne-cell: fig-teach_segmentation_modes | after-heading -->
### semantic ra instance ko farak

<!-- ne-cell: fig-teach_segmentation_modes | after-image:../../assets/diagrams/teach_segmentation_modes.png -->
chitra: uhi dui dosh lai semantic segmentation (eutai class ma milaune) ra instance segmentation
(ek-ek ma number lagaune) ma dekhaieko (kritrim chitra).

**dhyan dinuparne kura**

semantic segmentation le pixel-pichchhe class pharkaune hunale eutai class ka tadha-tadha kshetra pani
ganna sakinchha. chhuttyaunu parne kura **ek-arkalai chhoeka bastu** hun. tyasto abastha ma instance
segmentation prayog garinchha.

**sochnuhos**

- nachhoeka dui kalo dag semantic segmentation le duibata bhanera ganna sakinchha?

<!-- ne-cell: c5df01d0 | after-heading -->
**instance segmentation (bastugat kshetra bibhajan)**
<!-- ne-pair: Instance segmentation -->

<!-- ne-cell: c5df01d0 -->
semantic segmentation le "sabai milaera dosh" bhanne garchha, tar
instance segmentation le **pratyek dosh chhutyaunchha**.

```text
semantic:  dosh 3 bata → euta mask (3 kshetra)
instance:  dosh 3 bata → mask 1, mask 2, mask 3 (pratyek farak rang)
```

semantic mask ma pani **tadha raheka kshetra** connected component ko rupama ganna sakinchha.
ganna nasakine **chhoera baseka dosh** hun. dui dosh ek pixel matra chhoe pani
semantic mask ma eutai kshetra ma miler janchhan, chhutyaun sakindaina.
yahi nai instance segmentation sangko sancho farak ho.

tadha bhaeka doshko sankhya ganna matra chahinchha bhane segmentation ra connected component ganer pugchha.
chhoera baseka dosh pani ek-ek gari chhutyaun chahieko bela instance segmentation chahinchha.

<!-- ne-cell: 7ea5662a | after-heading -->
## Part 4 anomaly detection (asamanyata pahichan)

<!-- ne-cell: 9e24e09a | after-heading -->
**anomaly detection le "sadhainbhanda farak" khojchha**
<!-- ne-pair: Anomaly detection looks for 'not like usual' -->

<!-- ne-cell: 9e24e09a -->
yo talim ma prayog hune PatchCore jasto anomaly detection le **ramra utpadanako chitra matra** baat
"samanya bhaneko ke ho" sikchha, ra tyasabhanda farak bhaag lai **anomaly score** ko rupama sankhya ma pharkaunchha.

```text
input: sitako euta chitra
natija: anomaly score (sankhya) + asamanya sthan dekhaune heatmap
```

**phaida:** sikai ma **doshko kisim sikaunu naparne** kura sabaibhanda thulo phaida ho.
"kalo thoplo", "chot" bhanera label lagaeka asamanya chitra jamma garnu naparne, ramra utpadan matrale
sikai hunchha. label bhaeka asamanya chitra sikai ma hoina, **threshold calibration ra mulyankan** ma
prayog garinchha.

**kami:** **kasto dosh ho thaha hundaina**. sathai "samanya phailabat" lai asamanya bhanera nirnaya garna sakchha
(rangako asamanata, dhancha, ujyaloko asamanata adi).

heatmap le **sthanako sanket** pharkaunchha, tar doshko kisim wa thyakkai akar thaha hundaina.

> din 5 ma PatchCore bhanne anomaly detection tarika bastabama chalaunechhaun.

<!-- ne-cell: 2db70af1 | after-heading -->
#### uhi input ma ke pharkinchha

<!-- ne-cell: 2db70af1 -->
mathiko kritrim sitalai sajha input banaera tulna garchhaun.

| paribar | natijako rup | yasle matra jabaph din nasakne kura |
|---|---|---|
| classification | euta chitra ma euta label | sthan wa kshetraphal |
| detection | N chaukon + class + score | thyakkai akar |
| segmentation | H×W pixel mask, instance bhae dherai | mm² ka lagi calibration chahinchha |
| anomaly detection | euta score + sthan naksa | doshko class naam |

<!-- ne-cell: 620867ac | after-heading -->
## Part 5 utpadanama kun kahan prayog garne

<!-- ne-cell: fig-VisA_samples | after-heading -->
### bastabik audyogik anomaly detection datasetko udaharan

<!-- ne-cell: fig-VisA_samples | after-image:../../assets/external_samples/open_reference/VisA_samples.png -->
chitra: VisA datasetko saransh (Yang Zou adi / Amazon Science, VisA dataset CC BY 4.0). sarkit bord,
part, kyapsulajasta **audyogik utpadanaka bastabik tasbir** chhan. yo talimko PVC utpadan hoina, ra yo
talimka model ko natija pani hoina.

**dhyan dinuparne kura**

dosh kasto dekhinchha bhanne kura utpadanaanusar farak parchha. ujyaloko ausat eutale dekhauna nasakne farak
(akar, dhancha, sthan) harek utpadanama hunchha.

**sochnuhos**

- yimadhye sampurna chitrako ausat ujyalo tulna garda bhettaun sabaibhanda gahro hune dosh kun hola?

<!-- ne-cell: b3725e7f | after-heading -->
#### prashna baat tarika chhanne sano abhyas

<!-- ne-cell: b3725e7f -->
"NG ho ki hoina matra", "sthan ra sankhya", "pixel kshetra", "najaneko asamanyata" — pratyekaka lagi
mathiko talika baat tarika chhaner karan ek bakyama lekhnuhos. chhoera baseka 2 dosh chhuttachhuttai samhalne ho
bhane kun tarika chhannuhunchha?

<!-- ne-cell: 120c9c28 | after-heading -->
## Part 6 banaiyeko namuna chitrale jaanchne

<!-- ne-cell: 05049adb | after-heading -->
**kritrim sitako dosh herne**
<!-- ne-pair: Look at the synthetic defects -->

<!-- ne-cell: 05049adb -->
tayar bhaisakeko kritrim chitra herer 4 kaamle ke pharkaunchha bhanera sochnuhos.
yo chitra **hamile Python le koreko** ho, bastabik karakhanako chitra hoina.

<!-- ne-cell: 68e42818 | after-heading -->
### natijako udaharan

yo natija `assets/defect_samples/defects.json` ma surakshit sahi jabaphako data baat banainchha
(uhi samagri bhae uhi natija). shirshak kodale chhapne Japani aksharamai dekhinchha.

tin class `scratch`, `streak` ra `black_spot` hun; chaar sankhya [x1, y1, x2, y2] ko rupama pixel
ekaima chaukon hun.

<!-- ne-cell: c2fe0d8c | after-heading -->
**4 kaamko natija (segmentation 2 kisim)**
<!-- ne-pair: What would each task return here -->

<!-- ne-cell: c2fe0d8c -->
mathiko chitraka lagi 4 kaamle talako natija pharkaunchhan. segmentation ma matra semantic (class anusar) ra
instance (bastu anusar) gari 2 kisim dekhaieko chha.

| kaam | pharkine kura |
|---|---|
| image classification | "NG" (euta chitra ma euta label) |
| object detection | 3 chaukon ra pratyekako class naam (scratch / streak / black_spot) |
| semantic segmentation | dosh class ko mask (tadha 3 kshetra). sankhya ra pixel kshetraphal pachhi hisab garinchha |
| instance segmentation | dosh anusar chhuttieka 3 mask. kshetraphal pachhi hisab garinchha |
| anomaly detection | euta score (jastai 0.87) ra sthan dekhaune heatmap |

mm² ma badalna uhi bastu satahama napako calibration chahinchha.

<!-- ne-cell: e881aa20 | after-heading -->
## abhyas

<!-- ne-cell: 16e4bbfc | after-heading -->
**abhyas 1 (adharabhut): 4 kaam aphnai shabdama bujhaune**
<!-- ne-pair: Exercise 1 (basic): explain the four tasks in your own words -->

<!-- ne-cell: 16e4bbfc -->
talako cell ma 4 kaam ek-ek pangktima bujhaunuhos.
"natija ke ho" ra "kahile prayog garne" samabesh garnuhos.

**sakieko thanne adhar:** 4 pangktimadhye pratyekama natijako rup ra utpadanama thos prayog lekhieko chha.

<!-- ne-cell: 1cd0cf63 | after-heading -->
**abhyas 2 (madhyam): karyasthalako prashnako jabaph dine**
<!-- ne-pair: Exercise 2 (intermediate): answer shop-floor questions -->

<!-- ne-cell: 1cd0cf63 -->
talaka 3 prashnaka lagi kun kaam chhanne ra kina, lekhnuhos.

1. "yo rol pathaun sakinchha? jasari bhae pani chhutaunu hundaina."
2. "yo mahina kalo thoplo katibata thiyo ganna chahanchhu."
3. "chotako kshetraphal 1 mm² bhanda badhi bhae NG banaun chahanchhu."

**sakieko thanne adhar:** harek prashna ma (1) chhanieko kaam, (2) tyasko natijale abashyakata kasari pura garchha,
(3) tyo chhanotama banki rahane samjhauta (garna nasakine kura, thapine jhanjhat wa jhuta chetabani) lekhnuhos.

<!-- ne-cell: b0601286 | after-heading -->
**abhyas 3 (bikas/aichchhik): PVC nirikshanka lagi sujhab**
<!-- ne-pair: Exercise 3 (optional challenge): propose an approach for PVC inspection -->

<!-- ne-cell: b0601286 -->
chaudai 1,300 mm, dosh 0.3 mm, uchcha gatiko nirantar utpadan bhanne sartama
**pahile kun kaam prayas garnuparla** bhanera sujhab dinuhos. talaka drishtikon samabesh garnuhos.

- pahile prayas garne kaam ra tyasko karan
- chahine data (ke, kati bata jati)
- ramro nahune sambhabana badhi bhaeko bunda
- hapta 2 ma janchnuparne kura (kyamera, ujyalo, gati)

**sakieko thanne adhar:** pahilo kaam, data yojana, jokhim ra hapta 2 ma janchnuparne kura pratyek lekhnuhos.

<!-- ne-cell: 55e10325 | after-heading -->
#### bujhai jaanch

1. image classification ra object detection ko natijako farak bujhaunuhos.
2. semantic ra instance segmentation ma ke farak chha?
3. yo talimko anomaly detection (PatchCore) ma sikai ma doshko kisim sikaunu kina naparne ho?
   tyasko satta ke thaha hundaina?
4. karyasthalama "kshetraphalale nirnaya garna chahanchhu" bhaniyo bhane kun kaam chhannuhunchha? ke tayar garnuparchha?
5. 4 kamamadhye sahi jabaphako data (label) banaun sabaibhanda gahro kun ho? karan pani lekhnuhos.

namuna jabaph: `docs/instructor/day01_instructor_guide.md`.

<!-- ne-cell: ab02a78c | after-heading -->
## samasya aunda

truti ae pahile "kun cell ma", "kun line ma", "ke sandesh ayo" bhanera tipnuhos. bujhaunuparne kaam ma pani
tyahi abhilekh rakhnuhos.

| lakshan | ke garne |
| --- | --- |
| samagri chitra dekhindain | `python assets\scripts\generate_training_assets.py` chalaera samagri banaunuhos. |
| `json.decoder.JSONDecodeError` | `defects.json` bigreko chha. samagri banaune skript `--clean` sahit feri chalaunuhos. |
| chitrako bishayabastu AI ko natijabhanda farak dekhinchha | tapainko bujhai thik chha. yo notebookka chitra abadharana chitra hun, AI ko anuman hoina. |
| `KeyError: 'bbox'` | `defects.json` ko dhancha purano huna sakchha. samagri feri banaunuhos. |

<!-- ne-cell: 022c2c2b | after-heading -->
## sakieko janchasuchi

**aniwarya** bastuharu suchibaddh chhan. sabai ma chinh lagepachhi yo notebook sakinchha.

- [ ] Part 1–Part 6 ka byakhya padhen
- [ ] sabai kod cell chalaen
- [ ] abadharana chitra AI ko anuman hoina bhanne bujhen
- [ ] abhyas 1–2 (aniwarya) garen
- [ ] 4 kaamko farak arulai bujhaun sakchhu
- [ ] bujhai jaanchka 5 prashnako jabaph dien
- [ ] notebook surakshit garen

**aichchhik (sakieko sartama pardaina):** abhyas 3 ra "thap sikai" ko atirikt chunauti.

<!-- ne-cell: 45684e7a | after-heading -->
## thap sikai (aichchhik)

<!-- ne-cell: 45684e7a -->
### sandarbha lingk

- [Ultralytics: object detection ko kaam](https://docs.ultralytics.com/tasks/detect/)
- [Ultralytics: segmentation](https://docs.ultralytics.com/tasks/segment/)
- [Anomalib kagajat](https://anomalib.readthedocs.io/)
- [OpenCV image processing tutorial](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)

### atirikt chunauti (aniwarya hoina)

"anomaly detection" ra "object detection" dubai prayog garne ho bhane kun kram ma prayog garda bigreko
utpadan eutai pani najane hunchha, sochnuhos.
