<!--
Nepali anuwad / Nepali translation source for
notebooks/Day04_YOLO_Training/Day04_02_YOLO_Training.ipynb
-->
# din 4 notebook 02 — Nepali anuwad

<!-- ne-cell: 33aa7e73 | after-heading -->
# din 4 notebook 02: YOLO model prashikshan

<!-- ne-cell: 33aa7e73 -->
## sikai lakshyaharu

| Nepali |
| --- |
| 1. prashikshanko kram (epoch, batch, loss) bataun sakne. |
| 2. fine-tuning ko arth bataun sakne. |
| 3. CPU ma byabaharik samayabhitr prashikshan chalaun sakne. |
| 4. prashikshanko pragati padhna sakne. |
| 5. prashikshanko natija (weight, setting, maapan, lag) surakshit garna sakne. |

## yo notebookko adharabhut jankari

| bishay | biwaran |
| --- | --- |
| sikai samay (anuman) | 115 minet |
| kathinai | surubati tah |
| poorwashart | din 4 notebook 01 sakieko ra `assets/yolo_dataset` banisakeko hunuparchha. |
| aawashyak laibreri | torch, ultralytics, opencv-python, numpy, matplotlib, pandas |
| prayog hune kernel | aivision |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 4](../../COURSE_SYLLABUS.md#day4) |

### bujhaunuparne kaam

| Nepali |
| --- |
| prashikshan bhaeko weight file |
| prashikshanko lag ra maapan |
| prashikshan settingko abhilekh |

<!-- ne-cell: 7f0f9a1b | after-heading -->
## yo notebook kahan parchha

<!-- ne-cell: 7f0f9a1b -->
| bishay | biwaran |
| --- | --- |
| din | din 4 |
| ajako kram | ajako notabukamadhye 2 / 3 |
| lagne samay | 115 minet |
| poorwashart | `Day04_01_YOLO_Dataset_Annotation.ipynb`, `assets/yolo_dataset` banisakeko |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 4](../../COURSE_SYLLABUS.md#day4) |

dinko samayatalika `COURSE_SYLLABUS.md` ma eutai thaun ma chha. yo notebook tyasko euta bhaag matra ho.

<!-- ne-cell: audit-learning-loop | after-heading -->
### anuman garnuhos, chalaunuhos, hernuhos, byakhya garnuhos

<!-- ne-cell: audit-learning-loop -->
epoch bhaneko data ek pher ghumnu ho, batch bhaneko ekai patak diine tasbirko samuh ho. yas lai weight update
hune sankhya sang namisaunuhos. mahattwapurna cell chalaunuaghi input, kaam ra natija ek-ek bakyama lekhnuhos.
pahile anuman lekher chalaunuhos, ani `batch` matra badaler feri anuman gari chalaunuhos.

<!-- ne-cell: d114d800 | after-heading -->
## Part 0 tayari

<!-- ne-cell: afa3760c | after-heading -->
## Part 1 prashikshan bhaneko ke ho

<!-- ne-cell: clarity-batch-predict | after-heading -->
### pahilo charan: ek pher ra sana samuh

<!-- ne-cell: clarity-batch-predict -->
input 64 prashikshan tasbir ra batch=8 ho. natija pratyek batch ko tasbir number ho. chalaunuaghi ek pherama
kati batch hunchhan anuman garnuhos. epoch bhaneko sabai tasbir ek pher ghumnu ho.

<!-- ne-cell: clarity-batch-static | after-image:../../assets/svg/teach_batch_first_pass.svg -->
**dhyan dinuparne kura**

yo ganana garieko yojanabaddha chitra ho. harek line ek batch ho ra ath linele ek epoch banchha. weight kati patak
update hunchha bhanne kura yahan dekhaieko chhaina.

**sochnuhos**

batch=4 bhae ek pherama kati batch?

<!-- ne-cell: clarity-batch-interpret -->
8 batch le ek epoch banchha. 15 epoch hunda **data loader iteration 15 × 8 = 120 patak** hunchha.
yo "dataset sabai 120 patak padhne" bhanne hoina (dataset sabai 15 patak matra padhinchha), ra
weight 120 patak update hunchha bhanne pani hoina. batch 4 banaunda ek epoch ma kati iteration
hunchha anuman garnuhos. talako dosro charanle updateko bistrit kram bataunchha.

<!-- ne-cell: 16c0469f | after-heading -->
### dosro charan (purak): gradient jamma ra update

<!-- ne-cell: 16c0469f | after-image:../../assets/diagrams/teach_epoch_batch.png -->
chitra: 8-8 tasbir padher namamatr 8 batch ko gradient jamma garera update garne udaharan (`batch=8`, `nbs=64`).
warmup ko bela jamma hune sankhya badalin sakchha.

**dhyan dinuparne kura**

- **batch** … data loader le ekai patak padhne tasbir sankhya. yo talim ma 8. gradient yahin ganana hunchha
- **optimizer step (weight update)** … jamma bhaeko gradient le weight ek patak sarne. namamatr jamma 8
  batch ho, tar warmup ma farak parna sakchha
- **gradient jamma** … kati batch ko gradient jamma garepachhi ek patak update garne (`nbs` ÷ `batch`)
- **epoch** … sabai prashikshan tasbir ek pher ghumnu. yo talim ma 15 pher (1 epoch ko data loader iteration 8 patak)

64 ÷ 8 = 8 batch le ek epoch banchha. namamatr 8 batch ko gradient jamma garera update hunchha, tyasaile
**1 batch = 1 update hoina**. sathai prashikshanko suru ma **warmup** (learning rate ra jamma garne sankhya
bistarai lakshyatir laijane abadhi) hunchha, tyasabela sankhya 1 baat kramaisang badhchha. tyasaile "64 ÷ 8 = 8
update" bhanera gann mildaina; update sankhya prashikshak (trainer) le tay garchha.

loss le "ahile kati galti bhairaheko chha" janaunchha. sadhai ghatdai janchha bhanne chhaina — badhna pani
sakchha. prashikshan loss ghatnu matra naya tasbir ma kshamata badheko praman hoina; pramanikaran maapan ra
anuman dekhaieka tasbir sangai padhnuhos.

**sochnuhos**

- 64 prashikshan tasbir ra batch 8 hunda ek epoch ma data loader kati patak ghumchha? timadhye kati weight update
  banchha bhanne kura kele tay garchha?

<!-- ne-cell: 34a994aa | after-heading -->
**prashikshanko dohorine kram**
<!-- ne-pair: The training loop -->

<!-- ne-cell: 34a994aa -->
prashikshan chaar charanko **dohorine** kaam ho.

1. **anuman garne** — ahileko model le prashikshan tasbir ma anuman chalaunchha
2. **galti napne** — sahi uttar sang farak lai sankhya ma badalne. yas lai **loss** bhaninchha
3. **ali sudharne** — loss ghatne disha ma model ka sankhya ali sarne
4. **dohoryaune** — sabai prashikshan tasbir ek pher sakiepachhi ek **epoch** hunchha

charan 3 harek patak hundaina. kati batch ko gradient jamma garepachhi ek patak update garne bhanne settingle tay garchha
(`nbs=64`, `batch=8` ko namamatr jamma 8 batch; warmup ma farak parna sakchha).

loss ghatdai chha bhane prashikshan agadi badheko ho. tar **prashikshanko loss ghatdai jandaima bastabik kshamata badhchha
bhanne chhaina** (obharaphiting).

<!-- ne-cell: fig-teach_training_update | after-heading -->
### euta batch ma ke hunchha

<!-- ne-cell: fig-teach_training_update | after-image:../../assets/diagrams/teach_training_update.png -->
chitra: anuman → loss → gradient → update ko ek chakr, ra batch, step, epoch ganne tarika (weight ko
paribartan udaharanka lagi).

**dhyan dinuparne kura**

batch (data ekai patak padhne ekai) ra weight update hune sankhya farak hun. `nbs=64`, `batch=8` ko namamatr
jamma 8 batch ho. 64 tasbir ma data loader 8 patak ghumchha, tar warmup ma jamma sankhya pani badalin sakchha.
bastabik update sadhain ek patak ho bhanera nathani chalaieko setting ra lag jaanchnuhos.

**sochnuhos**

- 64 tasbir ra batch=8 ma kati patak loader ghumchha, ra bastabik update kun settingle tay garchha?

<!-- ne-cell: d7c70ee3 | after-heading -->
**shabdaharu ekai thaun ma**
<!-- ne-pair: The terms, all at once -->

<!-- ne-cell: d7c70ee3 -->
| shabd | arth | yo talimko maan |
|---|---|---|
| epoch | sabai prashikshan tasbir ek pher ghumnu | 15 |
| batch size | data loader le ekai patak padhne tasbir sankhya | 8 |
| gradient jamma | kati batch ko gradient jamma garepachhi ek patak update | namamatr 8 batch; warmup ma farak |
| warmup | prashikshanko suru ma learning rate ra jamma sankhya lakshyatir laijane abadhi | 3 epoch jati |
| learning rate | ek patakako sudharako akar | 0.01 baat bistarai ghatainchha |
| loss | sahi uttarasangako farak. sano bhae ramro | prashikshan ma ghatchha |
| prashikshan (train) | sankhya tay garne kaam | — |
| pramanikaran (val) | prashikshanakai bela kshamata jaanchne | harek epoch pachhi |

batch size thulo banaunda ek patakako kaam bhari hunchha. tar "thulo bhae sadhain sthir hunchha" bhann mildaina. memory
napuge sano banaunuhos ra sthir chha ki chhaina **pramanikaranko maapan** le jaanchnuhos.

<!-- ne-cell: baf19a2b | after-heading -->
**fine-tuning (thap talim)**
<!-- ne-pair: Fine-tuning -->

<!-- ne-cell: baf19a2b -->
suru dekhi prashikshan nagari **COCO ma talim bhaeko `yolo26n.pt` baat suru garinchha**. yas lai **fine-tuning**
bhaninchha.

karan: COCO ma sikeko "bastuko akar herne kshamata" PVC ko dosh ma pani kaam lagchha. thorai tasbir (64) bhae pani
akar herne tarika suru dekhi siknu pardaina.

taipani **64 tasbir dherai thorai** ho. kati chahinchha bhanne kura doshko prakar, akar, bhinnata ra ujyaloko abasthale
tay garchha. "kati bata bhae pugchha" bhanera eutai sankhya bhann sakindaina. kaam lagchha ki lagdain bhanne **pratinidhitb garne
bastabik data** ma janchinchha.

<!-- ne-cell: 16aa5ff6 | after-heading -->
## Part 2 prashikshanko tayari

<!-- ne-cell: c2cd53b9 | after-heading -->
**`data.yaml` lai ahileko sthanaanusar milaune**
<!-- ne-pair: Point `data.yaml` at the current location -->

<!-- ne-cell: c2cd53b9 -->
`data.yaml` ko `path` dataset banaundako pura bato ho. folder sarieko bhae **ahileko sthanama feri lekhna**
parchha. talako cellle `data.yaml` **ahileko talim folder anusar feri lekhchha** ra aru setting (class naam adi)
jastako tastai rakhchha.

<!-- ne-cell: a7af3b66 | after-heading -->
**tasbir ra labelko jodi antim patak jaanchne**
<!-- ne-pair: Final check that images and labels pair up -->

<!-- ne-cell: a7af3b66 -->
prashikshan suru garnuaghi **tasbir ra label ek-ek mileko chha** jaanchnuhos. yahan galti bhayo bhane prashikshan
suru bhaepachhi matra anautho natija dekhinchha.

<!-- ne-cell: bad3dfd6 | after-heading -->
## Part 3 prashikshan chalaune

<!-- ne-cell: 3261727b | after-heading -->
**yo cellko prashikshan setting**
<!-- ne-pair: The configuration in this cell -->

<!-- ne-cell: 3261727b -->
CPU ma pani byabaharik samayma sakine **sano setting** rakhieko chha.

| setting | maan | karan |
|---|---|---|
| `epochs` | 15 | dherai thorai pani hoina, parkhai pani chhoto |
| `imgsz` | 320 | mul tasbir 320 px. CPU ma pani sambhab |
| `batch` | 8 | memory ra gatiko santulan |
| `workers` | 0 | Windows notebook ma surakshit |
| `device` | `cpu` | GPU nabhae pani chalchha |
| `seed` | 2026 | natija dohoryaun |

`nbs` (gradient jamma garne ekai, purbanirdharit 64) ra `warmup_epochs` (purbanirdharit 3.0) yo cell ma
tokieka chhainan; maan surakshit `args.yaml` ma abhilekh chha. 8 batch namamatr jamma ho, warmup ma updateko
antar farak parna sakchha.

> **parkhaiko samay hardabeyaraanusar dherai farak parchha.** kehi minet ma sakin pani sakchha, 15 minetabhanda badhi lagn
> pani sakchha. **sakine samayko gyarenti chhaina.** dhilo bhae `epochs` 5 banaunuhos (prashikshanko kram uhi ho).

<!-- ne-cell: clarity-run-checklist | after-heading -->
#### chalaunuaghiko jaanch

<!-- ne-cell: clarity-run-checklist -->
natija `weights/best.pt`, `results.csv` ra `args.yaml` hun. lagne samay CPU, memory ra setting ma nirbhar chha;
chhoto samayko gyarenti chhaina. nachalaune abastha (skip) pahile jastai kayam chha. arko prayogka lagi `RUN_NAME`
farak rakhnuhos, pahileko prayog jogaun (uhi naam rakhe pani sbatah nayan folder banchha). anuman: epoch ghataeko
prayog tulna garna kun surakshit fileharu chahinchhan?

<!-- ne-cell: b271f05f | after-heading -->
**chalaune sbich**
<!-- ne-pair: The run switch -->

<!-- ne-cell: b271f05f -->
talako cell chalaunda **prashikshan suru hunchha** (lagne samay batabaran anusar farak parchha). nachalaun chahe
`RUN_TRAINING = False` banaunuhos.

**lamo prashikshan (GPU ka lagi 100 epoch) chalaindain.** udaharanko rupama string ma matra surakshit chha.

<!-- ne-cell: audit-teach_epoch_batch_step | after-heading -->
### kod kasari padhne

<!-- ne-cell: audit-teach_epoch_batch_step | after-image:../../assets/svg/teach_epoch_batch_step.svg -->
chitra: batch sankhya ra update sankhya sadhain uhi hundainan. (ganana garieko sansleshit udaharan ra yojanabaddha chitra;
model ko bastabik napieko natija hoina.)

**dhyan dinuparne kura**

batch sankhya ra update sankhya sadhain uhi hundainan. input ra paribartan bhaeko maan aunlale pachhyaunuhos.

**sochnuhos**

64 tasbir ma batch=4 banaunda ek epoch ma kati batch hunchhan?

<!-- ne-cell: 388c5d1c | after-heading -->
**prashikshanka bela skrin kasari padhne**
<!-- ne-pair: How to read the training output -->

<!-- ne-cell: 388c5d1c -->
`verbose=True` banaunda prashikshanka bela loss ka line dekhinchhan (yo talim ma shant rakhna `False` chha).
talaka stambha shirshak yo talim ma prayog hune ultralytics 8.4.211 ko trainer le dekhaune hun.

| stambha | arth |
|---|---|
| `Epoch` | kati aun pher |
| `GPU_mem` | prayog bhaeko memory (CPU ma 0 najik) |
| `box_loss` | ayatako sthanako truti. ghate sthan mildai gaeko |
| `cls_loss` | class bargikaranko truti. ghate prakar chhutyaun sakdai gaeko |
| `l1_loss` | ayatko **samanyikrit duri** (grid ekai ma badaleko kinar samma ko duri) ko L1 truti. kachcha piksel nirdeshanko ausat nirapeksh truti hoina |
| `Instances` | tyo batch ma bhaeka instance (sahi label) sankhya |
| `Size` | input tasbirko ek bhujako piksel (yo talim ma 320) |

prashikshanapachhi surakshit hune `results.csv` ma uhi samagri epoch-anusaraka stambha ma rahanchha. surakshit
chalai (`pvc_defect_quick`) ka stambha yi hun:

```text
epoch,time,train/box_loss,train/cls_loss,train/l1_loss,metrics/precision(B),metrics/recall(B),metrics/mAP50(B),metrics/mAP50-95(B),val/box_loss,val/cls_loss,val/l1_loss,lr/pg0,lr/pg1,lr/pg2
```

`metrics/...` ra `val/...` stambha harek epoch pachhi **pramanikaran data** ma ganana garieka maan hun.
prashikshanko loss matra herda nadekhine paribartan yahin dekhinchha.

> purana samagrile `dfl_loss` (Distribution Focal Loss) lai "kinarako sukshmatako truti" bhanera byakhya
> garchha. `dfl_loss` DFL prayog garne **arko banabat** ko stambha ho ra yo talimko YOLO26 ma chhaina
> (`results.csv` ma pani chhaina). sater napadhi `l1_loss` prayog garnuhos.

prashikshan loss sadhai ghatdai janchha bhanne chhaina — badhna pani sakchha. **prashikshan loss ghatnu
matra naya tasbir ma kshamata badheko praman hoina** (obharaphiting); `metrics/mAP50-95` jasta pramanikaran
mapan ra anuman dekhaieka tasbir sangai padhnuhos.

<!-- ne-cell: 90708cf6 | after-heading -->
## Part 4 prashikshanko natija surakshit garne

<!-- ne-cell: c0302cd9 | after-heading -->
### prashikshan loss ra pramanikaran loss chhuttachhuttai padhne

<!-- ne-cell: c0302cd9 | after-image:../../assets/diagrams/teach_train_val_curves.png -->
chitra: bakrako **akarako udaharan** matra ho. tapainko prashikshanko natija hoina.

**dhyan dinuparne kura**

chitrako **terso aksh epoch (kati aun pher)** ra **thado aksh loss** ho. dui line prashikshan ra pramanikaranka
hun, legend le chhutyaunuhos. prashikshan loss matra herda epoch badhaundai janda ramro bhaeko jasto dekhinchha.
chitrako dated rekha ("yahan baat obharaphiting") akar dekhauna banaiyeko udaharan ho; bastabik data ma tyahi thaun
tay hunchha bhanne hoina. **chhoto abadhiko sthirata wa briddhile matra obharaphiting bhann mildaina.**

hernuparne: "pramanikaran patti ghatn rokiyo ki", "pramanikaranko maapan (mAP50-95 adi) ajh badhdai chha ki".
bastabik tasbir ma dekhieka asaphalatako samagri pani sangai prayog garnuhos. **prashikshan loss ghatnu aphain
"ramro bhayo" bhanne praman hoina.**

**sochnuhos**

- pramanikaran loss kehi epoch sthir rahyo bhane obharaphiting bhann milchha? aru ke hernuhunchha?

<!-- ne-cell: fig-ref_train_val_curves | after-heading -->
### prashikshan lagalai dui line ma padhne

<!-- ne-cell: fig-ref_train_val_curves | after-image:../../assets/reference_outputs/ref_train_val_curves.png -->
chitra: yo talim ma sanchchai garieko chhoto prashikshan (15 epoch, CPU) ko abhilekh. bayan prashikshan ra pramanikaranko
cls loss, dayan mAP50 ra precision. surakshit garieko prashikshan lag nai ho.

**dhyan dinuparne kura**

euta manabhanda "dubai ghatdai chhan ki", "farak badhdai chha ki" bhanne kura padhnuhos. kehi epoch sthir rahanu
obharaphitingko praman hoina. loss ka stambha naam YOLO26 ko bastabik natija hun (`train/l1_loss`,
`val/l1_loss` chhan; `dfl_loss` chhaina).

**sochnuhos**

- antim 3 epoch ma mAP50 badhdai chha ki sthir chha?

<!-- ne-cell: 2a9855f8 | after-heading -->
**chaar kura surakshit garne**
<!-- ne-pair: Save four things -->

<!-- ne-cell: 2a9855f8 -->
prashikshan sakiepachhi Ultralytics le natija folder ma dherai file banaunchha. bujhaunuparne kaamka lagi yi chaar
bhae pugchha.

| prakar | file | prayog |
|---|---|---|
| weight | `weights/best.pt` | anuman ma prayog. **sabaibhanda mahattwapurna** |
| setting | `args.yaml` | kun setting ma prashikshan gariyo bhanne abhilekh |
| maapan | `results.csv` | epoch-anusar loss ra shuddhata |
| lag | `results.csv` baat banaiyeko saransh | bujhaunaka lagi |

`best.pt` **pramanikaran data (val)** ma sabaibhanda ramro bhaeko kshanako weight ho, `last.pt` antim epoch
ko. **samanyataya `best.pt` prayog garinchha.**

"sabaibhanda ramro" ko adhar Ultralytics ko **fitness** ho. yo talim ma prayog hune ultralytics 8.4.211
ko bastu pahichan ma weight `[0, 0, 0, 1]` (precision, recall, mAP50, mAP50-95 ko kram) hunchha. arthat
**fitness = mAP50-95** ra `best.pt` **pramanikaranko mAP50-95 sabaibhanda uchcha bhaeko epoch** ko weight ho.

`best.pt` chhanda pani **parikshan data herieko chhaina**. tyasaile `best.pt` chhanisakepachhi pani parikshan ma mulyankan
ek patak matra garna sakinchha.

`last.pt` antim epoch ko weight ho. prashikshanko antim abastha rakhna, `results.csv` herer arko epoch
aphain chhanna, wa `resume` garera prashikshan jari rakhna prayog hunchha.

<!-- ne-cell: f800c794 | after-heading -->
### natijako udaharan

<!-- ne-cell: f800c794 -->
yo natija yo talim ma surakshit garieko abhilekh ho (`yolo26n.pt`, 15 epoch, `imgsz=320`, `batch=8`,
seed 2026, CPU). sukshm samay ra file akar batabaran anusar farak parchha, tar chaar file baneko kura jaanchnuhos.

<!-- ne-cell: 845f2d52 | after-heading -->
**prashikshan saphal bhayo bhann milchha?**
<!-- ne-pair: Can we call this training successful? -->

<!-- ne-cell: 845f2d52 -->
loss ghatnu matra pugdain. **yo charan ma kshamata ajhai janchieko chhaina.**

arko notebook (04_03) ma **prashikshan ma prayog nabhaeka tasbir** ma kshamata napinchha. tyahan matra
"kaam lagchha / lagdain" thaha hunchha.

loss sthir bhayo bhane pani tyasaile obharaphiting bhann mildaina. nirnayaka lagi **pramanikaran maapan ko prabritti**
(`metrics/mAP50-95` adi) ra bastabik tasbir ma dekhieka asaphalata sangai prayog garnuhos. sathai kaam lagchha ki
lagdain bhanne **pratinidhitb garne bastabik data** ma janchiepachhi matra thaha hunchha.

yo charan ma "shuddhata 95%" jasto sankhya **diindain**; prashikshan data ma napieko sankhyale bastabik kshamata
dekhaundain.

<!-- ne-cell: f412c790 | after-heading -->
## abhyas

<!-- ne-cell: 4febd099 | after-heading -->
**abhyas 1 (adharabhut): 5 epoch ma prashikshan chalaune**
<!-- ne-pair: Exercise 1 (basic): train for 5 epochs -->

<!-- ne-cell: 4febd099 -->
`EPOCHS` 5 banaer prashikshan chalaunuhos ra `box_loss` ko pahilo ra antim maan abhilekh garnuhos. sathai
`metrics/mAP50-95` ko pahilo ra antim pani abhilekh garnuhos. loss matrale nirnaya garna namilne kura
pushti garnuhos.

| epoch | box_loss | mAP50-95 (val) |
|---|---|---|
| 1 | | |
| 5 | | |

- pura bhaeko maapan: dubai maan abhilekh bhaeka chhan ra loss ghatyo ki ghaten bhann sakinchha
- loss naghate wa sthir rahe pani tyasaile asaphal bhann mildaina

<!-- ne-cell: 8273b533 | after-heading -->
**abhyas 2 (madhyam): `imgsz` badaler tulna garne**
<!-- ne-pair: Exercise 2 (intermediate): compare `imgsz` -->

<!-- ne-cell: 8273b533 -->
`IMGSZ` 160 / 320 ma prashikshan garera **prashikshanko samay** ra **uhi pramanikaran maapan**
(`metrics/mAP50-95` wa precision, recall) tulna garnuhos. prashikshan loss ko antim maan input akar
pherinda arth pani pherine hunale shuddhatako tulna ma prayog garna mildaina. gati ra shuddhata madhye kun rojne
bhanne kura aphnai shabdama lekhnuhos.

- pura bhaeko maapan: dui patakako samay ra pramanikaran maapan abhilekh bhaeka chhan ra santulan (trade-off) byakhya bhaeko chha

<!-- ne-cell: 75cf3328 | after-heading -->
**abhyas 3 (baikalpik): prashikshan kina agadi nabadhne sochne**
<!-- ne-pair: Exercise 3 (optional challenge): why training might not progress -->

<!-- ne-cell: 75cf3328 -->
loss naghatne wa NaN hune chaar karan bhannuhos ra pratyekama "kasari jaanchne" lekhnuhos. **aniwarya hoina.**

pura bhaeko maapan: chaar karan ra chaar jaanchne tarika lekhieka chhan.

<!-- ne-cell: 8574a7d8 | after-heading -->
#### bujhai jaanchne prashna

<!-- ne-cell: 8574a7d8 -->
1. epoch, batch size ra optimizer step ma ke-ke farak chha?
2. loss ghatnu bhaneko ke ho? tyasle matra kshamata tay garna milchha?
3. fine-tuning garnuka dui phaida bhannuhos.
4. `best.pt` kun adharama chhaninchha? `last.pt` sang ke farak chha?
5. prashikshan sakielagattai "shuddhata 95%" bhann kina mildaina?

<!-- ne-cell: a4a1e4b0 | after-heading -->
## samasya parema

<!-- ne-cell: a4a1e4b0 -->
truti aepachhi pahile "kun cell ma", "kun line ma", "ke sandesh ayo" bhanera lekhnuhos. bujhaunuparne kaam ma pani
tyahi abhilekh rakhnuhos.

| lakshan | ke garne |
| --- | --- |
| prashikshan suru hundaina | `RUN_TRAINING = False` chha. prashikshan garna `True` banaunuhos. |
| `RuntimeError: Dataset ... not found` | `data.yaml` ko `path` purano huna sakchha. Part 2 ko cellle feri lekhnuhos. |
| `CUDA out of memory` / `OutOfMemoryError` | `BATCH` 4 ra `IMGSZ` 224 banaunuhos. CPU ma yo kam hunchha. |
| prashikshan dherai dhilo | CPU ma kehi minet dekhi darjanaun minet lagchha. `EPOCHS` 5 ra `IMGSZ` 160 banaunuhos. |
| `FileNotFoundError: yolo26n.pt` | model liieko chhaina. `assets/models/` ma file chha ki jaanchnuhos. |
| loss ghatdain | labelko galti, tasbir ra label namilnu, learning rate ko samasya huna sakchha. din 4 notebook 01 ko jaanch ma pharkanuhos. |
| prashikshan lagama `dfl_loss` chhaina | `dfl_loss` DFL prayog garne arko banabatko stambha ho. YOLO26 le `l1_loss` lekhchha. |
| ek epoch ko update sankhya milen | 1 batch = 1 update nahun sakchha. `nbs` ra `batch` ko gradient jamma tatha warmup le tay garchha. |

<!-- ne-cell: 26b4b3d5 | after-heading -->
## sampannata janchasuchi

<!-- ne-cell: 26b4b3d5 -->
**aniwarya bunda matra** diieka chhan. **abhyas 3 (baikalpik) aniwarya hoina**; nagare pani pura maninchha.
samay banki bhae ma matra garnuhos. sabai ma chinh lagepachhi yo notebook pura hunchha.

**aniwarya**

- [ ] Part 1–Part 4 padher sabai code cell chalaen
- [ ] `data.yaml` ahileko sthanaanusar feri lekhen
- [ ] tasbir ra labelko jodi janchen
- [ ] prashikshan chalaen (`RUN_TRAINING = True`)
- [ ] `best.pt` ra `results.csv` bane
- [ ] prashikshan lagako saransh surakshit garen
- [ ] abhyas 1–2 (aniwarya) garen
- [ ] bujhai jaanchne 5 prashnako uttar dien
- [ ] notebook surakshit garen

**baikalpik**

- [ ] abhyas 3 (baikalpik): prashikshan nabadhne chaar karan bhanen

<!-- ne-cell: a1c69bf9 | after-heading -->
## thap adhyayan (baikalpik)

<!-- ne-cell: a1c69bf9 -->
### sandarbha lingk

- [Ultralytics Train mod](https://docs.ultralytics.com/modes/train/)
- [Ultralytics hyperparameter](https://docs.ultralytics.com/guides/hyperparameter-tuning/)
- [PyTorch prashikshanko adhar](https://pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)

### thap chunauti (aniwarya hoina)

`BATCH` 4 ra 16 ma prashikshan garera loss ghatne "sahajata" (smoothness) tulna garnuhos.
