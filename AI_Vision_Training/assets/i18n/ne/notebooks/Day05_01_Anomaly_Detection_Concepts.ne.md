<!--
Nepali anuwad / Nepali translation source for
notebooks/Day05_PatchCore/Day05_01_Anomaly_Detection_Concepts.ipynb
-->
# din 5 notebook 01 — Nepali anuwad

<!-- ne-cell: a62c030b | after-heading -->
# din 5 notebook 01: asamanyata pahichanko sochai

<!-- ne-cell: a62c030b -->
## sikai lakshyaharu

| Nepali |
| --- |
| 1. asamanyata pahichanle ke garchha bataun sakne. |
| 2. samanya ra asamanya namuna chhutyaun sakne. |
| 3. suparabhaijd larningasangako farak bataun sakne. |
| 4. pyach, feature ra score ko sambandh bataun sakne. |
| 5. PatchCore ko sochai drishtant prayog garera bataun sakne. |

## yo notebookko adharabhut jankari

| bishay | biwaran |
| --- | --- |
| sikai samay (anuman) | 70 minet |
| kathinai | surubati tah |
| poorwashart | din 4 sakieko hunuparchha. |
| aawashyak laibreri | numpy, matplotlib, pillow, opencv-python |
| prayog hune kernel | aivision |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 5](../../COURSE_SYLLABUS.md#day5) |

### bujhaunuparne kaam

| Nepali |
| --- |
| asamanyata pahichan ra bastu pahichanko farakko byakhya |
| score kasari padhne bhanne abhilekh |

<!-- ne-cell: b071950f | after-heading -->
## yo notebook kahan parchha

<!-- ne-cell: b071950f -->
| bishay | biwaran |
| --- | --- |
| din | din 5 |
| ajako kram | ajako notabukamadhye 1 / 3 |
| lagne samay | 70 minet |
| poorwashart | din 4 |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 5](../../COURSE_SYLLABUS.md#day5) |

dinko samayatalika `COURSE_SYLLABUS.md` ma eutai thaun ma chha. yo notebook tyasko euta bhaag matra ho.

<!-- ne-cell: audit-learning-loop | after-heading -->
### anuman garnuhos, chalaunuhos, hernuhos, byakhya garnuhos

<!-- ne-cell: audit-learning-loop -->
feature bhaneko tasbir baat ganana garine sankhya ho. samanya memory (memory bank) featureka namuna rakhne thaun
ho. mahattwapurna cell chalaunuaghi input, kaam ra natija ek-ek bakyama lekhnuhos. pahile anuman garera chalaunuhos
ra maan wa chitra hernuhos. udaharan chitrako nayan feature matra badaler feri anuman gari chalaunuhos.

<!-- ne-cell: 73b2d2a4 | after-heading -->
## Part 0 tayari

<!-- ne-cell: 68ece906 | after-heading -->
## Part 1 asamanyata pahichan ke ho

<!-- ne-cell: 154bde87 | after-heading -->
**"rojabhanda farak" bhetne**
<!-- ne-pair: Finding 'not like usual' -->

<!-- ne-cell: 154bde87 -->
**asamanyata pahichan** le **samanya bhaneko ke ho** sikchha ra tyas baat **namilne bhaag** bhetchha. yo talim ma
yas lai **samanya tasbir matra prayog garera talim garine asamanyata pahichan** bhaninchha.

```text
fit (talim): samanya bhanera pushti bhaeka tasbir matra dekhaune (doshko label prayog hundaina)
anuman: nayan tasbir rakhieka samanya feature baat kati tadha chha bhanne sankhya pharkaune
calibration: samanya/asamanya label bhaeka arko tasbir setama threshold tay garne
mulyankan: ajh arko setama chhutne ra jhuto alarm ganne
```

din 3 ra din 4 ko YOLO sangko farak yahi ho.

| | YOLO (bastu pahichan) | PatchCore (asamanyata pahichan) |
|---|---|---|
| talim ma chahine | doshko sthan ra prakarko label | **samanya bhanera pushti bhaeka tasbir matra** |
| natija | ayat + class + confidence | **score + heatmap** |
| kamajori | talim nalieko prakar | kun dosh ho bhanne pahichan |

sahityama yo tarikalai one-class, semi-supervised, normal-only adi dherai naamle bhaninchha. naam patraanusar
farak bhae pani **yo talim ma garine kram eutai** ho: samanya tasbir ma matra model fit garne, label bhaeka
calibration tasbir ma threshold tay garne, ra arko mulyankan setama galti napne. "label katti pani
chahindain" bhanne hoina; **fit charan ma matra chahindain**.

<!-- ne-cell: fig-teach_normal_variation | after-heading -->
### samanya bhinnata ra dosh

<!-- ne-cell: fig-teach_normal_variation | after-image:../../assets/diagrams/teach_normal_variation.png -->
chitra: samanya 4 tasbir (ujyaloko asamanata ra abajale ali-ali farak) ra dosh bhaeko 1 tasbirko ausat maanko
tulna (sansleshit tasbir, ganana garieka maan).

**dhyan dinaparne kura**

ujyaloko asamanata, butta, sthanako sarai jasta kurale samanya tasbir ma pani bhinnata aaunchha. euta
samagra chamakale tyo bhinnata byakhya garna sakdain bhanne kura pahile thaha pae asamanyata naksa padhne tarika
nai badlinchha.

**sochnuhos**

- samagra chamak uhi bhaeka dui tasbir pani asamanya bhanieko natija farak kina huna sakchha?

<!-- ne-cell: ef2014d3 | after-heading -->
**samanya ra asamanya namuna**
<!-- ne-pair: Normal and abnormal samples -->

<!-- ne-cell: ef2014d3 -->
- **samanya namuna** … samasya nabhaeko samanako tasbir
- **asamanya namuna** … dosh bhaeko samanako tasbir

karyasthalama **samanya saman dherai hunchha ra jamma garna sajilo hunchha**, kinabhane bigreko saman "kahilekahin
matra" aaunchha. asamanyata pahichanle yahi gun prayog garchha.

**talako cell le ke dekhaunchha.** samanya prashikshan tasbir ra `assets/defect_samples/` ka sansleshit
(shikshan) dosh namuna matra. mulyankan folder (`test/`) ma pachhiko notebook le calibration ra test ma
chhutyaune tasbir milieka hunchhan, tyasaile tyasko sankhya ra bhitri biwaran threshold sthir garnuaghi
dekhaindain. yahan pahile dekhaune ho bhane pachhiko mulyankan "punar prayog garieko data" banchha.

<!-- ne-cell: d5d90ce4 | after-heading -->
## Part 2 suparabhaijd ra anasuparabhaijd

<!-- ne-cell: fig-VisA_samples | after-heading -->
### samanya matra jamma garna gahro kina

<!-- ne-cell: fig-VisA_samples | after-image:../../assets/external_samples/open_reference/VisA_samples.png -->
chitra: VisA datasetko saransh (Yang Zou adi / Amazon Science; VisA dataset CC BY 4.0). samanya ra asamanya
dubai manchhele chhutyaera jamma gareko bastabik audyogik data. yo talimko PVC saman hoina.

**dhyan dinaparne kura**

asamanyata pahichan samanya tasbir ma matra fit garna sakinchha, tar **threshold tay garne calibration** ra
**kshamata napne mulyankan** ka lagi samanya ra asamanya label bhaeka arka tasbir chahinchha. yo talim ma pani
calibrationka lagi 26 ra mulyankanka lagi 26 tasbir chhutyaieka chhan.

**sochnuhos**

- samanya tasbir matra bhae kun kura napna sakindaina: chhutne dar ki jhuto alarm dar?

<!-- ne-cell: clarity-patch-data-roles | after-heading -->
### shabdabalibhanda pahile datako bhoomika padhne

<!-- ne-cell: clarity-patch-data-roles -->
| fit / tayari | calibration | parikshan | anuman (sanchalan) |
|---|---|---|---|
| samanya tasbir matra | samanya + asamanya sahi labelle samayojan | sthir garepachhi matra prayog hune chhuttai label set | nayan tasbir jaanchne |

anuman: threshold chhanne tasbir kun stambha ma parchha? talako sahityik shabdabali baikalpik purak ho.

<!-- ne-cell: 5e60e191 | after-heading -->
**baikalpik: sahityama prayog hune shabd**
<!-- ne-pair: Sorting out the terms -->

<!-- ne-cell: 5e60e191 -->
| talimko prakar | data | udaharan |
|---|---|---|
| suparabhaijd | input + sahi uttar | YOLO (din 4) |
| anasuparabhaijd | input matra | clustering |
| samanya tasbir matra | samanya bhanera pushti bhaeka tasbir matra | **PatchCore** |

PatchCore **samanya tasbir matra prayog garera talim garine asamanyata pahichan** ho. sahityama one-class wa
semi-supervised bhanie pani **yo talim ma "samanya tasbir matra" bhanera ekai shabd prayog** garinchha.

karyasthalako phaida spasht chha: **"dosh lai naam dier ayatale gherne" kaam chahindain**. tyo kaam ma prati tasbir
darjanaun sekendadekhi kehi minet lagchha ra manchheanusar nirnaya farak parchha. tar threshold tay garne calibration
ra kshamata napne mulyankanka lagi samanya-asamanya label bhaeka tasbir chahinchha.

<!-- ne-cell: cf09f7d8 | after-heading -->
## Part 3 pyach ra feature

<!-- ne-cell: clarity-patch-overlap | after-heading -->
### drishtant ra bastabik kaam sangai tulna garne

<!-- ne-cell: clarity-patch-overlap | after-image:../../assets/svg/teach_patch_overlap.svg -->
pahile samjhanuparne paribhasha: pyach diskriptar bhaneko obharalyap hune tasbirko bhaag lai saranshit garne
**CNN feature naksako euta sthanako sankhya-shringkhala** ho.

anuman: chheuchhauka feature sthanaharule uhi mul pikselako asar paun sakchhan?

**dhyan dinuparne kura**

yo yojanabaddha chitra ho. dayanko bhaagko akar ra feature sankhya byakhyaka lagi matra hun, resnet18 ko
bastabik receptive field ko nap hoina. bayanko RGB katieko tukra memory bank ma tyasai rakhindain.
talako grid kod pani drishtant matra ho. sano prayog: grid 8→4 banaunda dekhaine tail badlinchha, tar model
ko setting badlinchha?

<!-- ne-cell: 429f99e1 | after-heading -->
**pyach = tasbirko sano tukra**
<!-- ne-pair: A patch is a small piece of the image -->

<!-- ne-cell: 429f99e1 -->
PatchCore le tasbir lai **sana bhaag (pyach)** ma bander sochchha. talako chitra tyo sochaiko
**saralikrit drishtant** ho.

```text
(drishtant) 256 × 256 tasbir → 16 × 16 grid → euta bhaag = 16 × 16 piksel
```

**bastabik model yasari chaldain.** yo talimko model le talim bhaeko CNN (resnet18) ko bichako tah
(`layer2`, `layer3`) ka **feature naksa** prayog garchha. feature naksako euta sthanale input tasbirko
**obharalyap hune pharakilo kshetra** saransh garchha. tyasaile:

- euta "pyach" pikselalai 16 × 16 ma katieko tukra hoina
- grid kati sukshma hunchha bhanne kura backbone, prayog hune tah ra purb-prashodhan (input akar) le tay garchha
- euta sthanale samhalne kshetra obharalyap hune hunale sthan sankhya ra piksel sankhyako sambandh sidha chhaina

bander hernuko karan uhi ho: **dherai asamanyata sthaniy rupama hunchhan**, tyasaile sthaniy bhaag lai samanya sang
tulna garda bhetna sajilo hunchha. tar **tasbirabhariko chamak paribartan, buttako sarai, akar bigranu** jasta
pharakilo dayaraka asamanyata (global wa sanrachanagat) sthaniy tulnale matra thamyaun gahro huna sakchha.

<!-- ne-cell: f6726637 | after-heading -->
**feature ke ho**
<!-- ne-pair: What a feature is -->

<!-- ne-cell: f6726637 -->
**feature** bhaneko tasbirko euta bhaag lai **sankhyako shringkhala** ma badaleko kura ho.

```text
tasbirko euta sthan → [0.14, 0.73, 0.08, ...] (sayaundekhi hajaraun sankhya)
```

dekhine rup uhi bhae sankhyako shringkhala pani mildo hunchha. **"dekhine rup" lai "sankhyako thegana" ma
badaleko** bhanera sochda bujhna sajilo hunchha.

feature ganana garne bhaag (**backbone**) dherai tasbir ma pahile nai talim bhaeko model baat liinchha (jastai ImageNet
ma talim bhaeko ResNet). **yo talim ma backbone ko weight talim garindain (sthir rakhinchha).**

<!-- ne-cell: 33f893ee | after-heading -->
**najikako chhimekisangako duri**
<!-- ne-pair: Distance to the nearest neighbour -->

<!-- ne-cell: 33f893ee -->
nayan sthanako feature **samanya featureko samuh (memory bank)** baat kati tadha chha napinchha.

```text
nayan feature → memory bank bhitra sabaibhanda najikako samanya feature khojne
          → tyo duri "samanyabhanda kati farak chha" bhanne sankhya banchha
```

- duri **sano** … rakhieka samanya feature sang **najik** (dekhine rup milchha)
- duri **thulo** … rakhieka samanya feature baat **tadha** (dekhine rup mildaina)

**duri "praman" ho, "uttar" hoina.** duri sano hunda samanya sang milne sambandh matra hunchha; duri aphain
"samanya" bhanne label hoina. OK/NG nikalna **threshold** chahinchha ra thresholdle gareko nirnaya **galat huna
sakchha**.

sathai **kachcha duri 0–1 dayarama simit hundaina**. yo talim ma surakshit kachcha duri karib 9–21 dayarama thiyo.
0–1 hune kura pachhi calibration datako tathyangkale badaleko **score** ho. dui kura chhutyaera padhnuhos
(Part 5 ma bistrit).

<!-- ne-cell: a85f80ca | after-heading -->
### natijako udaharan

<!-- ne-cell: a85f80ca -->
yo udaharan ma natija yasto aaunchha (random seed 3 ma sthir garieko hunale uhi input ma uhi natija aaunchha).
Japani aksharako chaudaile stambhako sthan badalin sakchha, sankhya bhane uhi rahanchha.

<!-- ne-cell: c4d6ab80 | after-heading -->
**graph kasari padhne**
<!-- ne-pair: How to read the plot -->

<!-- ne-cell: c4d6ab80 -->
nilo bindu **samanya pyach**, × chinh **nayan pyach** ho.

- samanya pyachko **samuhabhitr** bhaeko × ko duri sano hunchha, tyo **rakhieka samanya feature sang najik** chha
- samuhabat **tadha** bhaeko × ko duri thulo hunchha, **samanyabhanda farak huna sakne shangka** hunchha

duri **praman** ho, tyasaile matra OK/NG tay hundaina. **threshold** bhaepachhi matra nirnaya banchha. bastabik
PatchCore ma yo 2 ayam **sayaundekhi hajaraun ayam** hunchha. **ayam badhe pani sochai uhi** rahanchha.

<!-- ne-cell: 47e11e57 | after-heading -->
## Part 4 PatchCore ko sochai

<!-- ne-cell: e9df232d | after-heading -->
### pyach → feature sthan → najikako chhimeki → score

<!-- ne-cell: e9df232d | after-image:../../assets/diagrams/teach_patch_neighbour.png -->
chitra: euta sthanako feature nikaler sabaibhanda najikako samanya phicharasangako duri lai score banaune kram. ③ ko
2-ayam bindu **feature spesako drishtant** ho.

**dhyan dinaparne kura**

③ **byakhyaka lagi banaiyeko 2-ayam yojanabaddha chitra** ho. binduharu **feature spes** ko drishtant hun,
piksel tyasai milaera rakhieko hoina. bastabik "pyach" pikselabat naobharalyap hune tailama katieko hoina;
**CNN feature naksako euta sthan** le input tasbirko **obharalyap hune kshetra** saransh garchha. bastabik
model le sayaun ayamako bhitri pratinidhitb prayog garchha. samjhanuparne kura eutai sambandh ho: rakhieka samanya
feature baat jati tadha, tyo dekhine rup samanyabhanda tyati farak. **"thulo = asamanya" threshold tay garepachhi
matra** lagu hunchha; duri thulo bhae pani thresaholdabhanda kam bhae nirnaya OK nai hunchha.

**sochnuhos**

- samanya binduko samuhako thik chheuma kberi (×) rakhda duri kati jati hunchha?

<!-- ne-cell: c474e947 | after-heading -->
**kina "memory" bhaninchha**
<!-- ne-pair: Why a memory bank -->

<!-- ne-cell: c474e947 -->
PatchCore le samanya pyachka feature **tyasai surakshit (samjhana)** garchha ra harek patak "sabaibhanda najikako samanya
pyachasangako duri" ganana garchha.

yo **daksh nirikshakako tarikasang najik** chha: "yo butta pahile dekheko chhu. tyo chahin dekheko chhaina."

daksh nirikshakale "ramro saman kasto hunchha" dimagama rakhchhan ra nayan kura bhetchhan. PatchCore le tyahi kura
sankhyako samuhabat garchha.

dhyan dinuparne kura: samanya pyachko sankhya dherai hune hunale **pratinidhitb garne kehi matra rakhne
(coreset)** upay chha. `coreset_sampling_ratio` le tyo anupaat tay garchha.

<!-- ne-cell: fig-teach_memory_bank | after-heading -->
### memory bank ra najikako chhimeki

<!-- ne-cell: fig-teach_memory_bank | after-image:../../assets/diagrams/teach_memory_bank.png -->
chitra: samanya pyachka feature jamma garieko memory bank ra dui kberibatako duri (2-ayam yojanabaddha chitra).

**dhyan dinaparne kura**

memory bank ma samanya tasbirka feature surakshit hunchhan. samanya nabhaeko tasbir misiyo bhane score ghater
chhutne badhna **sakchha** (sadhainbhari pahichanai hundaina bhanne gyarenti hoina). misieko bhetie hataera feri banaunuhos
ra arko tasbir ma jaanchnuhos.

**sochnuhos**

- euta asamanya tasbir misiyo bhane pahile ke janchnuparchha?

<!-- ne-cell: 1aba9655 | after-heading -->
## Part 5 score ra heatmap

<!-- ne-cell: 5c642a4a | after-heading -->
#### dui prakarko natija, tin charan ma padhne

<!-- ne-cell: 5c642a4a -->
natijaka prakar dui hun: **tasbirabhariko euta score** ra **euta sthanik naksa**. pyach duri bichako maan
ho, alag tesro API natija hoina.

| charan | tasbir score | sthanik naksa |
|---|---|---|
| 1 kachcha rup | sabaibhanda thulo pyach duri ma chhimekiko weight | bichako maan bharer masino banaiyeko duri |
| 2 kyalibresanapachhi | calibration tathyangkale samanyikrit | arko tathyangkale samanyikrit |
| 3 nirnaya | ghoshit tasbir score ≥ uhi maapan ko tasbir threshold | sthan dekhaune sanket matra; tasbir nirnayako bikalp hoina |

yo talikale prashodhanako bhoomika dekhaunchha, kunai tasbirko natija hoina. pachhi-prashodhan sakriya ra calibration
tathyangk fit bhaeko abastha ma matra 0–1 maapan prayog garna milchha. kachcha maan 0–1 ma simit hundaina ra tasbir
score ra naksako adhikatam maan pani mildaina. 0–1 bhae pani tyo sambhabana hoina. tasbir score ko ganana ra naksako
bharne/masino banaune kaam farak prashodhan hun.

anuman: tasbir score uhi maapan ko tasbir threshold wa badhi bhayo bhane? naksako rang matra badalda pas/phel
badlinchha?

<!-- ne-cell: fig-teach_score_levels | after-heading -->
### bichako duri ra dui prakarko natija

<!-- ne-cell: fig-teach_score_levels | after-image:../../assets/diagrams/teach_score_levels.png -->
chitra: pyach-dar-pyach score → tasbirko euta score → sthanik naksa. bichako maan ra natija chhutyaune
(maan udaharanka lagi).

**dhyan dinaparne kura**

yo chitrako "adhikatam" ra "ausat" **byakhyaka lagi banaiyeko khelauna sankshep** ho. yo talimko setting ma sabaibhanda
thulo pyach duri ma chheuchhauka samanya feature (9 bindu) ko weight gunan garera tasbir score banainchha, ra dekhaine
naksa bharne ra masino banaune prakriyabat janchha. tyasaile tasbir score ra naksako adhikatam maan mildaina.

**sochnuhos**

- tasbir score tay garna naksabhariko ausat prayog bhaeko chha?

<!-- ne-cell: 1f601e75 | after-heading -->
**thresholdle OK/NG tay garne**
<!-- ne-pair: Turning a score into OK/NG with a threshold -->

<!-- ne-cell: 1f601e75 -->
score **sankhya** ho. OK/NG banaun **threshold** chahinchha.

```text
score < threshold  →  OK
score >= threshold →  NG
```

threshold **ghataunda** NG badhchha (chhutne ghatchha, jhuto alarm badhchha). **badhaunda** OK badhchha (jhuto alarm ghatchha,
chhutne badhchha). yo din 3 ma dekheko confidence thresaholdakai uhi dhancha ho.

threshold sang tulna garine kura **calibrationle 0–1 ma badalepachhiko score** ho, kachcha duri hoina. sathai
**threshold baat niskeko natija "anuman"** ho; sahi uttar sang tulna nagaresamm tyo sahi chha ki chhaina thaha hundaina.
threshold calibration data ma tay garnuhos ra parikshan data ma nasarnuhos (din 5 notebook 03).

<!-- ne-cell: 1784ecb1 | after-heading -->
**PatchCore le garna nasakne kaam**
<!-- ne-pair: What PatchCore cannot do -->

<!-- ne-cell: 1784ecb1 -->
badhi bishbas nagarnuhos. yi kurako gyarenti chhaina.

1. **sabai dosh bhetne** — "samanya sang milne dosh" chhutchha
2. **doshko prakar bhanne** — "kalo thoplo" ki "chiso" bhanna sakdain
3. **samanya bhinnatalai asamanya nabhanne** — rangako asamanata, butta ra ujyaloko asamanata asamanya thanne
   sambhabana dherai hunchha

tesro kura bishesh mahattwapurna chha. **samanya samanako bhinnata talim data ma kati sametne** bhanne kurale
byabaharama kaam lagchha ki lagdain tay garchha.

<!-- ne-cell: 2b8faacc | after-heading -->
## abhyas

<!-- ne-cell: 074c9203 | after-heading -->
**abhyas 1 (adharabhut): aphnai shabdama byakhya garne**
<!-- ne-pair: Exercise 1 (basic): explain it in your own words -->

<!-- ne-cell: 074c9203 -->
talaka tin kura pratyek dui lainabhitr byakhya garnuhos.

1. asamanyata pahichan ra bastu pahichanko farak
2. memory bank ke ho
3. score ke ho

<!-- ne-cell: 0cf76dd2 | after-heading -->
**abhyas 2 (madhyam): threshold sarne**
<!-- ne-pair: Exercise 2 (intermediate): move the threshold -->

<!-- ne-cell: 0cf76dd2 -->
talako talika bharnuhos (andajale bhae pani hunchha).

| threshold | NG sankhya | chhutne | jhuto alarm |
|---|---|---|---|
| kam (0.2) | | | |
| madhyam (0.5) | | | |
| uchcha (0.8) | | | |

<!-- ne-cell: 3c808d08 | after-heading -->
**abhyas 3 (baikalpik): PVC nirikshan ma kasari prayog garne**
<!-- ne-pair: Exercise 3 (optional challenge): how would you use this for PVC -->

<!-- ne-cell: 3c808d08 -->
chaudai 1,300 mm, 0.3 mm dosh ra uchcha gati bhanne abastha ma asamanyata pahichan **kun charan ma, kun uddeshyale**
rakhne sujhab dinuhos.

- YOLO ra asamanyata pahichan **dubai** prayog garne bhae kram ke hunchha?
- asamanyata pahichan matra kina pugdain?
- pahile kun data jamma garnuparchha?

<!-- ne-cell: 93412cb6 | after-heading -->
#### bujhai jaanchne prashna

<!-- ne-cell: 93412cb6 -->
1. asamanyata pahichanko talim ma doshko label chahinchha? karan pani lekhnuhos.
2. tasbir lai pyach ma kina bandne?
3. "memory bank" le ke surakshit garchha?
4. score uchcha = sadhain bigreko saman, bhanna kina mildaina?
5. samanya samanako bhinnata (rangako asamanata adi) talim data ma narakhda kasto samasya aaunchha?

<!-- ne-cell: 2fb637f4 | after-heading -->
## samasya parema

<!-- ne-cell: 2fb637f4 -->
truti aepachhi pahile "kun cell ma", "kun line ma", "ke sandesh ayo" bhanera lekhnuhos. bujhaunuparne kaam ma pani
tyahi abhilekh rakhnuhos.

| lakshan | ke garne |
| --- | --- |
| samanya tasbir dekhindain | `python assets\scripts\prepare_datasets.py --only anomaly` le data banaunuhos. |
| graphaka bindu obharalyap bhaera dekhindain | samanya pyach 120 bata chhan. `alpha` ghataunuhos wa `s` sano banaunuhos. |
| "duri" ko arth bujhien | yasle bahu-ayami sankhyako farak lai euta sankhya ma badalchha. 2-ayam udaharan ma jaanchnuhos. |
| threshold kasari tay garne thaha bhaen | samanya tasbir matra bhae jhuto alarm napna sakinchha, chhutne hoina. samanya-asamanya label bhaeko calibration data ma jhuto rijekt darko sima tay garera recall adhikatam banaunuhos. din 5 notebook 02 ma garinchha. |
| score 0–1 ma aundain | samanyikaranako tathyangk chhaina (NaN) bhane Anomalib le kachcha duri pharkaunchha. calibration data ma pachhi-prashodhan fit bhaeko chha ki jaanchnuhos. |

<!-- ne-cell: f1c0d7cd | after-heading -->
## sampannata janchasuchi

<!-- ne-cell: f1c0d7cd -->
**aniwarya bunda matra** diieka chhan. **abhyas 3 (baikalpik) aniwarya hoina**; nagare pani pura maninchha.
sabai ma chinh lagepachhi yo notebook pura hunchha.

**aniwarya**

- [ ] Part 1–Part 5 padher sabai code cell chalaen
- [ ] samanya ra asamanya tasbirko sankhya janchen
- [ ] pyach bandaphantako chitra heren
- [ ] najikako chhimeki duriko graph heren
- [ ] abhyas 1–2 (aniwarya) garen
- [ ] bujhai jaanchne 5 prashnako uttar dien
- [ ] notebook surakshit garen

<!-- ne-cell: ea343d35 | after-heading -->
## thap adhyayan (baikalpik)

<!-- ne-cell: ea343d35 -->
### sandarbha lingk

- [Anomalib kagajat](https://anomalib.readthedocs.io/)
- [PatchCore patr (Roth et al., 2022)](https://arxiv.org/abs/2106.08265)
- [MVTec AD dataset](https://www.mvtec.com/company/research/datasets/mvtec-ad)

### thap chunauti (aniwarya hoina)

PatchCore patrako chitra 1 herer memory bank kahan chha khojnuhos.
