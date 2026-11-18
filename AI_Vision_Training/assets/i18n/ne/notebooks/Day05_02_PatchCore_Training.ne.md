<!--
Nepali anuwad / Nepali translation source for
notebooks/Day05_PatchCore/Day05_02_PatchCore_Training.ipynb
-->
# din 5 notebook 02 — Nepali anuwad

<!-- ne-cell: 43cbc7ba | after-heading -->
# din 5 notebook 02: PatchCore ko talim

<!-- ne-cell: 43cbc7ba -->
## sikai lakshyaharu

| Nepali |
| --- |
| 1. Anomalib ko API prayog garera PatchCore suru garna sakne. |
| 2. asamanyata pahichanko data banabat bataun sakne. |
| 3. samanya tasbir matra prayog garera fit garna sakne. |
| 4. score ra heatmap nikalna sakne. |
| 5. natija surakshit garera thresaholdabare sochn sakne. |

## yo notebookko adharabhut jankari

| bishay | biwaran |
| --- | --- |
| sikai samay (anuman) | 130 minet |
| kathinai | surubati tah |
| poorwashart | din 5 notebook 01 sakieko ra `aivision-anomalib` kernel chhanieko hunuparchha. |
| aawashyak laibreri | anomalib 2.7.0, torch, torchvision, opencv-python-headless, numpy, matplotlib, pandas |
| prayog hune kernel | `aivision-anomalib` (**yahi kernel prayog garnaiparchha**) |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 5](../../COURSE_SYLLABUS.md#day5) |

### bujhaunuparne kaam

| Nepali |
| --- |
| talimko natija (maapan) |
| heatmap tasbir |
| tasbir-dar-tasbir score ko talika |
| tasbir-dar-tasbir sangkhyatmak naksa (maps/*.npz) |

> yo notebook lai **`aivision-anomalib` kernel aawashyak** parchha. hapta 1 ma dui alag batabaran rakhieka chhan kinabhane
> Anomalib lai `opencv-python-headless` chahinchha ra Ultralytics lai `opencv-python`; dubai eutai batabaran ma rakhda
> OpenCV bigranchha.

<!-- ne-cell: 01bf2bc9 | after-heading -->
## yo notebook kahan parchha

<!-- ne-cell: 01bf2bc9 -->
| bishay | biwaran |
| --- | --- |
| din | din 5 |
| ajako kram | ajako notabukamadhye 2 / 3 |
| lagne samay | 130 minet |
| poorwashart | `Day05_01_Anomaly_Detection_Concepts.ipynb`, `aivision-anomalib` kernel |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 5](../../COURSE_SYLLABUS.md#day5) |

dinko samayatalika `COURSE_SYLLABUS.md` ma eutai thaun ma chha. yo notebook tyasko euta bhaag matra ho.

<!-- ne-cell: audit-learning-loop | after-heading -->
### anuman garnuhos, chalaunuhos, hernuhos, byakhya garnuhos

<!-- ne-cell: audit-learning-loop -->
backbone sthir feature nikalne bhaag ho. samanya memory ra calibration maan data baat banchha. mahattwapurna cell
chalaunuaghi input, kaam ra natija ek-ek bakyama lekhnuhos. pahile anuman garera chalaunuhos. calibrationko
sart matra badaler (parikshan data samayojanama prayog nagarnuhos) feri anuman gari chalaunuhos.

<!-- ne-cell: 75d078b0 | after-heading -->
## Part 0 tayari

<!-- ne-cell: 2fa75b5a | after-heading -->
**kernel jaanchne**
<!-- ne-pair: Confirm the kernel -->

<!-- ne-cell: 2fa75b5a -->
yo notebook **`aivision-anomalib` kernel** ma chalaunuhos. arko kernel bhae
`ModuleNotFoundError: No module named 'anomalib'` aaunchha.

tyasto bhae menubat `Kernel` → `Change Kernel` → `Python 3 (AI Vision Anomalib)` chhaner
**notebook suru dekhi feri chalaunuhos**.

<!-- ne-cell: 8f419564 | after-heading -->
**prayog hune API (sanskaran sthir)**
<!-- ne-pair: The API used here (pinned version) -->

<!-- ne-cell: 8f419564 -->
Anomalib ma **2.x** ma API dherai badaliyo. 1.x ko namuna kod sarda chaldain.

yo talim ma **Anomalib 2.7.0** ma janchieko chha. prayog hune tin class matra hun.

| class | bhoomika |
|---|---|
| `anomalib.data.Folder` | folder banabat baat data padhne |
| `anomalib.models.Patchcore` | PatchCore model aphain |
| `anomalib.engine.Engine` | talim, mulyankan ra anuman chalaune |

<!-- ne-cell: 08e2ac7d | after-heading -->
## Part 1 datako banabat

<!-- ne-cell: bc41a079 | after-heading -->
**talim ma samanya matra prayog garne**
<!-- ne-pair: Only normal images are used for training -->

<!-- ne-cell: bc41a079 -->
prayog hune folder banabat yasto chha: `assets/anomaly_dataset/pvc_sheet/` bhitra `train/good/` (talim,
samanya matra), `test/good/` (mulyankan, samanya), `test/black_spot/`, `test/scratch/`,
`test/streak/`, `test/irregular_mark/` (mulyankan, asamanya), ra
`ground_truth/<prakar>/xxx_mask.png` (sahi mask, mulyankanka lagi).

**`train/` ma euta pani asamanya tasbir chhaina.** yahi PatchCore ko poorwashart ho.

<!-- ne-cell: afbdd116 | after-heading -->
**data module banaune**
<!-- ne-pair: Building the datamodule -->

<!-- ne-cell: afbdd116 -->
`Folder` lai kun folder ke ho bhanera batainchha.

| argument | arth |
|---|---|
| `normal_dir` | talim ma prayog hune samanya tasbirko folder |
| `normal_test_dir` | mulyankan ma prayog hune samanya tasbirko folder |
| `abnormal_dir` | mulyankan ma prayog hune asamanya tasbirko folder (soochi) |
| `mask_dir` | sahi maskako folder (soochi) |
| `val_split_mode` / `val_split_ratio` | mulyankan data pramanikaran ra parikshan ma bandne tarika ra anupaat |
| `num_workers` | Windows ma 0 surakshit |

`val_split_mode="from_test"` le **mulyankan folder lai "pramanikaran (calibration)" ra "parikshan" ma
bandne tarika** matra bataunchha. **adha-adha hunu `val_split_ratio=0.5` tokieko hunale** ho; `from_test`
matrale anupaat tay gardaina. uddeshya: **threshold pramanikaran (yo talim ma calibration bhaninchha) ma tay
garne ra natija parikshan ma napne**.

<!-- ne-cell: c7f73514 | after-heading -->
**talim data ma asamanya chhaina bhanne pushti garne**
<!-- ne-pair: Verify training data contains no anomalies -->

<!-- ne-cell: c7f73514 -->
yahan **abashy jaanchnuhos**. `train` ma asamanya tasbir misiyo bhane tyo asamanyata "samanyako namuna"
baner memory bank ma parchha. phalasbarup **ustai dekhine asamanyatako score ghatchha ra chhutne badhchha**.

tar "misiepachhi tyo dosh kahilyai bhetindain" bhanera tunggo lagdain. coreset kasari chhaniyo, featureko chhimek,
sthan ra baraparako dekhine rup, ra thresholdle natija badalchha. **bhanna sakine kura "chhutne jokhim badhchha" samm**
ho.

sabaibhanda bharapardo upay: **misieko tasbir hataera memory bank feri banaune, ra chhutyaera rakhieka
calibration ra mulyankan tasbir ma jaanchne**.

<!-- ne-cell: 9e971153 | after-heading -->
## Part 2 model suru garne

<!-- ne-cell: f6b40399 | after-heading -->
**backbone kasari chhanne**
<!-- ne-pair: Choosing the backbone -->

<!-- ne-cell: f6b40399 -->
`Patchcore` ka mukhy argument:

| argument | arth | yo talimko maan |
|---|---|---|
| `backbone` | feature ganana garne netabark | `resnet18` (CPU ka lagi halka) |
| `layers` | kun tahako feature prayog garne | `["layer2", "layer3"]` |
| `pre_trained` | talim bhaeko weight prayog garne ki | `True` |
| `coreset_sampling_ratio` | memory bank ma rakhine anupaat | `0.1` (10 %) |
| `num_neighbors` | duri ganana ma prayog hune chhimeki sankhya | `9` |

patrako purbanirdharit `wide_resnet50_2` ho, tar yo talimko CPU batabaran ma ganana lamo lagne hunale
purbanirdharit rupama `resnet18` prayog garinchha. **kun ramro hunchha bhanne kura data ra samayle tay garchha.**
nirnaya garda **uhi calibration (pramanikaran) data ma maapan ra samay naper** tulna garnuhos (abhyas 2).
"resnet18 sadhain ali naramro" wa "wide_resnet50_2 sadhain dherai dhilo" bhanera nathaannuhos.

> ImageNet ko weight kakshaaghi `preload_models.py --profile anomalib` le liinchha. tayari cellko
> `TIMM_USE_OLD_CACHE=1` le URL cache lai prathamikata dinchha. cache chhaina bhane yo paathko cell trutisahit
> rokinchha ra aphain daunalod gardaina.

<!-- ne-cell: audit-teach_patchcore_stages | after-heading -->
### kod kasari padhne

<!-- ne-cell: audit-teach_patchcore_stages | after-image:../../assets/svg/teach_patchcore_stages.svg -->
chitra: tasbirko nirdeshangk ra feature spes chhutyaunuhos. (ganana garieko sansleshit udaharan ra yojanabaddha chitra;
model ko bastabik napieko natija hoina.)

**dhyan dinuparne kura**

tasbirko nirdeshangk ra feature spes chhutyaunuhos. input ra paribartan bhaeko maan aunlale pachhyaunuhos.

**sochnuhos**

samanya memory ma asamanyata halda duriko nirnaya kasari badalin sakchha?

<!-- ne-cell: 90a03498 | after-heading -->
## Part 3 fit garne

<!-- ne-cell: bf3d12fb | after-heading -->
**PatchCore ko "talim" ek patakale pugchha**
<!-- ne-pair: One pass is enough for PatchCore's fit -->

<!-- ne-cell: bf3d12fb -->
PatchCore ko talimle **neural network ko weight update gardaina**. garine kaam dui matra ho:

1. samanya tasbir backbone ma haler **feature ganana garne**
2. ti feature **memory bank ma surakshit garne** (coreset le chhotyaer)

**CNN ko weight sthir (frozen)** rahanchha; datale tay garne kura **memory bank** ho. sathai tyaspachhiko
**calibration (threshold ra samanyikaranako tathyangk)** pani datale tay garchha. surakshit hune abastha yahi
"memory bank + calibration tathyangk" ho.

uhi tasbir baat uhi feature aune hunale **yo fit tarikama ek patak (`max_epochs=1`) pugchha**. "jati patak
dohoryae pani sadhain arthahin" bhanne hoina; **data badaliyo bhane feri fit garne ra calibration pani feri garne.**
yo din 4 ko YOLO sangko thulo farak ho.

<!-- ne-cell: fig-teach_backbone_vs_memory | after-heading -->
### badaline kura memory bank matra

<!-- ne-cell: fig-teach_backbone_vs_memory | after-image:../../assets/diagrams/teach_backbone_vs_memory.png -->
chitra: weight update nahune backbone ra datale tay garne memory bank (yojanabaddha chitra).

**dhyan dinaparne kura**

ResNet-18 ko weight update hundaina (frozen). datale tay garne kura memory bank ho, ra pachhi calibrationle
tay garne pachhi-prashodhan (samanyikaranako tathyangk ra threshold) pani surakshit abasthako bhaag ho. `max_epochs=1`
pugnuko karan yo kram ek pheramai sakine banabat ho.

**sochnuhos**

samanya tasbir thapda ke badlinchha: backbone, memory bank ki threshold?

<!-- ne-cell: f5f00936 | after-heading -->
**pragati dekhaune subidha aphain banda garne karan**
<!-- ne-pair: Why the progress display is switched off -->

<!-- ne-cell: f5f00936 -->
Lightning ko dherai sajabat bhaeko pragati dekhaune subidhale Windows ko Jupyter ma kahilekahin
`RecursionError` din sakchha. yo talim ma **tyo dekhaune subidha banda garera** aphain suru-antyako sandesh
dekhainchha. talim aphainma kunai paribartan hundaina.

<!-- ne-cell: clarity-fit-state | after-heading -->
### kun abastha badaliyo

<!-- ne-cell: clarity-fit-state -->
| charan | bastu ra paribartan |
|---|---|
| feature nikalne | backbone weight: sthir |
| fit | samanya memory: banainchha |
| calibration | samanyikaran tathyangk ra tasbir threshold: chhaner sthir garinchha |
| anuman | nayan tasbir: nirnaya matra; fit ma thapindain |

din 4 ko 15 epoch ko weight anukulanabhanda yo farak ho. anuman: samanya tasbir thapda ke feri banaunuparchha?
talako surakshit garne thaun ma memory model ko abasthabhitr parne kura jaanchnuhos ra surakshit sankhya lai
yo patakako chalaibat chhutyaunuhos.

<!-- ne-cell: 29df63e7 | after-heading -->
**surakshit bhaeko kura**
<!-- ne-pair: What was saved -->

<!-- ne-cell: 29df63e7 -->
`engine.fit()` le model ko abastha `training_results/day05/` muni surakshit garchha.
**memory bank ko samagri tyahi surakshit phailabhitr hunchha.**

<!-- ne-cell: 9aac8b7e | after-heading -->
## Part 4 mulyankan garne

<!-- ne-cell: c452bff7 | after-heading -->
**chaar maapan**
<!-- ne-pair: The four metrics -->

<!-- ne-cell: c452bff7 -->
Anomalib le chaar maapan pharkaunchha. **yo bhaag calibration (validation) data ma matra ganana garinchha.**
parikshan datako maapan threshold sthir garepachhi din 5 notebook 03 ma ek patak matra nikalinchha.

| maapan | arth |
|---|---|
| `image_AUROC` | tasbir-star ma OK/NG chhutyaune kshamata (1.0 sarbottam) |
| `image_F1Score` | tasbir-starko precision ra recall ko santulit ausat |
| `pixel_AUROC` | piksel-star ma asamanya kshetra bhetne kshamata |
| `pixel_F1Score` | piksel-starko santulit ausat |

**AUROC** le "threshold natoki samanya ra asamanya lai kati ramro kram ma rakhna sakiyo" dekhaunchha. 0.5
aniyamit, 1.0 purna kram. tar **AUROC 1.0 bhae "junasukai threshold ma purna" bhanne hoina**; **yo
calibration data ma kram purna thiyo** bhanne matra ho. bastabik nirnaya chhanieko euta thresholdle garchha,
tyasaile **chhutne ra jhuto alarmko sankhya chhuttai ganinchha**.

calibration data ma samanya 6 ra asamanya 20 tasbir chhan. **yo sankhyale napna sakne shuddhatako sima chha.**

yahan `engine.test()` pustakalayako method naam ho. diieko `datamodule.val_dataloader()` le kun tasbir
mulyankan hune tay garne hunale yo CALIBRATION ho, prayog nabhaeko antim TEST mulyankan hoina.

<!-- ne-cell: ba5da1ef | after-heading -->
### natijako udaharan

<!-- ne-cell: ba5da1ef -->
yo natija yo talim ma surakshit garieko abhilekh ho (model, data bandaphant ra seed lekhama chha). sukshma sankhya
batabaran anusar farak parchha; prabritti ra thulo-sanoko sambandh padhnuhos. yi **calibration** ka sankhya hun
(ResNet-18, `image_size=256`, seed 2026); parikshanka sankhya notebook 03 ma matra aunchhan.

<!-- ne-cell: f4d5f377 | after-heading -->
**sankhya dherai ramro dekhinda shangka garne kura**
<!-- ne-pair: When the numbers look too good -->

<!-- ne-cell: f4d5f377 -->
sansleshit tasbir **bastabik karakhanaka tasbirabhanda sajilo** hunchha. dosh spasht hunchha ra prishthabhumiko bhinnata
pani sano hunchha, tyasaile `image_AUROC` 1.0 najik pugchha.

**yo "bastabik kshamata" hoina.** bastabik PVC ma rangako asamanata, ujyaloko asamanata ra parabartan thapinchhan
ra uhi sankhya aundain. sathai calibration ma samanya 6 ra asamanya 20 tasbir matra chhan, tyasaile
**yo sankhya ma napieko maan utpadanako kshamata hundaina**.

yo talimko sankhya lai **utpadanako nirikshan shuddhata bhanera uddhrit garnu hundaina.**

<!-- ne-cell: 28cb22c6 | after-heading -->
## Part 5 score ra heatmap

<!-- ne-cell: 8cfeab62 | after-heading -->
### mul tasbir, score naksa ra milaera dekhaieko chitra

<!-- ne-cell: 8cfeab62 | after-image:../../assets/diagrams/teach_score_map_overlay.png -->
chitra: **byakhyaka lagi banaiyeko sansleshit yojanabaddha chitra** (halka dandajasto akar) ho. yo bastabik
PatchCore ko natija hoina. milaera rakhne tarika dekhauna uhi tasbir lai uhi rang-maapan (0.0–0.4) ma tin
rupama rakhieko chha.

**dhyan dinuparne kura**

tulna garda **dekhaine dayara (vmin ra vmax) sthir** rakhnuhos. harek tasbirle aphnai dayara chhanda
samanya samanama pani adhikatam maan sabaibhanda chamkilo rangama dekhinchha ra tulna arthahin hunchha. yo notebookko
heatmaple **sabai tasbir ma uhi 0–1 dayara** prayog garchha ra **rang-patti (colourbar)** rakhchha
(`MAP_VMIN`, `MAP_VMAX`). rang **colormap ra dekhaine dayarale** tay garne hunale **rang-patti herer arth
bujhnuhos** ra chamkilo bhaag matra dekher NG nathaannuhos. dayarabahiraka maan kinarako rangama katinchhan
(**clipping**).

**sochnuhos**

- dekhaine dayara tasbir-dar-tasbir badalda dui naksa tulna garna kina mildaina?

<!-- ne-cell: clarity-score-card | after-heading -->
### sankhya padhne kram

<!-- ne-cell: clarity-score-card -->
talako chitra ganana garieko sansleshit khelauna ho. calibration/parikshan tasbir wa model ko natija
prayog bhaeko chhaina. anuman: khelaunako pas/phel kun linele tay garchha?

| input → kaam → maan | prayog |
|---|---|
| duriko adhikatam 6 × manieko weight 0.8 = 4.800 | khelaunako kachcha tasbir score |
| duriko grid → 3×3 ausat → naksako adhikatam 2.000 | sthan dekhaune sanket |
| clip((4.8 − 4) / 8 + 0.5, 0, 1) = 0.600 | manieko tasbir threshold 0.50 sang tulna: NG |

5×5 duri grid ma sabai 1, kendrama 6 ra mathi-tal-bayan-dayan 2 chhan. kinara dohoryaer 3×3 ausat ganana
garinchha. weight 0.8, kendra 4, dayara 8 ra threshold 0.50 byakhyaka lagi chhanieka maan hun, calibrationle
nikaleka tathyangk hoinan. yo bastabik PatchCore gananako punarutpadan hoina, farak sankhyaka bhoomikako
byakhya matra ho. 0.600 sambhabana hoina. kachcha maan lai 0.50 sang tulna garnu hundaina. dekhaine vmax matra
badalda nirnaya badlinchha?

<!-- ne-cell: fig-ref_anomaly_panels | after-heading -->
### sansleshit khelaunako sangkhyatmak naksa

<!-- ne-cell: fig-ref_anomaly_panels | after-image:../../assets/reference_outputs/teach_numeric_map_toy.png -->
chitra: khelaunako input, 3×3 ausat naksa ra uhi maanko milaera dekhaieko chitra. yo
`generate_reference_outputs.toy_numeric_map` ko sthir array baat ganana garinchha. bastabik calibration/TEST
data wa anumanko natija hoina.

**dhyan dinuparne kura**

kachcha tasbir score 4.800, masino banaiyeko naksako adhikatam 2.000 ra badalepachhiko tasbir score 0.600 farak kura
hun. uhi maapan ko tasbir threshold sang tulna garine kura antim maan matra ho. bastabik ganana pachhiko kod
ra calibration tathyangkale garchha.

**sochnuhos**

- naksako adhikatam maan ra tasbir score kina mildaina?

<!-- ne-cell: cefba6c0 | after-heading -->
**ek-ek tasbirko natija herne**
<!-- ne-pair: Look at results image by image -->

<!-- ne-cell: cefba6c0 -->
`engine.predict()` le tasbir-dar-tasbir natija pharkaunchha.

| gun | samagri |
|---|---|
| `pred_score` | score. **pachhi-prashodhan sakriya ra tathyangk fit bhaeko abastha ma matra 0–1** |
| `pred_label` | thresholdle tay gareko OK/NG |
| `anomaly_map` | piksel-dar-piksel asamanyatako matra (pachhi-prashodhanale 0–1 ma badaleko) |
| `gt_label` | sahi uttar (asamanya ho ki hoina) |
| `image_path` | tasbirko bato |

`pred_score` 0–1 hunuko sart: **samanyikaran (`enable_normalization=True`) sakriya chha ra calibration
data baat nyoonatam/adhikatam tathyangk bharieko chha**. tathyangk chhaina (NaN) bhane Anomalib le **kachcha duri tyasai
pharkaunchha**, jun 0–1 ma simit hundaina. "sadhain 0–1 mai pharkinchha" bhanera nathaannuhos.

<!-- ne-cell: 11a17ecf | after-heading -->
**sankhya herda dhyan dinuparne kura**
<!-- ne-pair: Caution when reading the numbers -->

<!-- ne-cell: 11a17ecf -->
`pred_label` Anomalib le **calibration data ma tay gareko threshold** anusarako nirnaya ho. threshold
`post_processor` ma rahanchha ra `model.post_processor` baat herna sakinchha. tasbir score ra piksel naksaka
threshold **chhuttachhuttai** tay hunchhan.

yo threshold **sansleshit dataka lagi** ho. bastabik sanchalanama **ramro bhanera thaha bhaeka saman matra
chalaera score ko bitaran napne ra threshold feri tay garne** aawashyak hunchha. tar **samanya saman matra bhae
"chhutne (recall)" napna sakindaina**; samanya samanale napine kura **jhuto alarm (samanya samanalai NG bhanne
dar)** samm ho. chhutne pani napna **asamanya label bhaeko calibration data** chahinchha (din 5 notebook 03
le tyahi garchha).

> **baikalpik biwaran: score samanyikaranako sutra (anomalib 2.7.0)**
> tasbir score ra piksel naksa chhuttachhuttai tathyangkale
> `clip((raw - threshold) / (max - min) + 0.5, 0, 1)` ma badalinchhan. `min`, `max` ra `threshold`
> **calibration (validation) bhaag** baat nikalieka hun. `max - min = 0` hunda threshold sang tulna
> garera `1 / 0.5 / 0` ma jharinchha. tathyangk chhaina (NaN) bhane nabadali kachcha maan pharkainchha. yahi sutraka karan
> **calibration ma tay garieko threshold 0–1 maapan ma 0.5** ma parchha.

<!-- ne-cell: 748dffdf | after-heading -->
**heatmap ra sangkhyatmak naksa surakshit garne**
<!-- ne-pair: Save the heatmaps as images -->

<!-- ne-cell: 748dffdf -->
din 5 notebook 03 ma YOLO ko natijasangai dekhauna heatmap lai tasbir fileko rupama surakshit garinchha.

- **milaera dekhaieko tasbir (`heatmaps/`)** **calibration data** baat banchha. threshold sthir garnuaghi
  ankhale herna milne calibration matra ho.
- **sangkhyatmak naksa (`maps/*.npz`)** calibration tasbirka lagi matra, pachhi samagrika chitra feri banaun
  sakine gari surakshit garinchha. mulyankan (test) tasbirka sangkhyatmak naksa sthir garepachhi antim
  "sealed" cell le ek patak matra banauchha.

<!-- ne-cell: b8ec6f1a | after-heading -->
**heatmap kasari padhne**
<!-- ne-pair: How to read a heatmap -->

<!-- ne-cell: b8ec6f1a -->
rang **dekhaine dayara ra colormap** le tay garchha. yo bhaagka chitra pachhi-prashodhit maan hunale **0–1 ko sthir
dayara** ma dekhainchha, jahan 0.5 calibration ma tay garieko piksel threshold ho. dayarabhanda bahiraka maan
kinarako rangama katinchhan (clipping). **rang-pattibat sankhya jaanchnuhos**.

- **NG tasbir ma** pani dosh chamkilo binduko rupama nadekhin sakchha; pharakilo ra halka dekhin pani sakchha, wa naksa
  gadhai rahan sakchha.
- **OK tasbir ma** pani asaman bhaag ali chamkilo dekhin sakchha.

tyasaile **chamkilo bindu chha ki chhaina bhanera nirnaya nagarnuhos**. nirnaya tasbir score ra thresholdle garchha;
heatmap "kahan heriraheko chha" jaanchna prayog hunchha. OK tasbir ma chamkilo kshetra dekhiyo bhane tyo
**"samanya bhinnatalai asamanya thanieko"** huna sakchha; tyo bhinnata talim data ma thapnuparchha.

<!-- ne-cell: d5e2bc6d | after-heading -->
## abhyas

<!-- ne-cell: clarity-sealed-test | after-heading -->
**Part 5: sthir garepachhi sealed testko mulyankan**

<!-- ne-cell: clarity-sealed-test -->
**chalne kram chha charan ko ho.** test data mulyankan hune charan 4 ra 5 ma, eka-eka patak matra ho.

| charan / step | notebook (batabaran) / notebook (env) | garnuparne kaam / what to do |
|---|---|---|
| 1 | `Day04_03_YOLO_Evaluation.ipynb` (YOLO) | tulnaka lagi setko bandaphant tay garera **calibration ka 26 tasbir matra** mulyankan garne ra surakshit garne |
| 2 | `Day05_02_PatchCore_Training.ipynb` (anomalib, yo notebook) | PatchCore fit garne, bandaphant din 4 sang milchha ki jaanchne, ani **calibration matra** mulyankan garera surakshit garne |
| 3 | `Day05_03_YOLO_vs_PatchCore.ipynb` (anomalib) | calibration ma tulna garne, dui threshold chhannne, ra sthir gareko ghoshana abhilekh garne |
| 4 | `Day04_03_YOLO_Evaluation.ipynb` (YOLO) | **`shared-sealed-test` cell matra** chalaune: test ka 26 tasbir ek patak mulyankan garera sealed garne |
| 5 | `Day05_02_PatchCore_Training.ipynb` (anomalib, yo notebook) | **`clarity-sealed-test-scoring` cell matra** chalaune: test ka 26 tasbir ek patak mulyankan garera sealed garne |
| 6 | `Day05_03_YOLO_vs_PatchCore.ipynb` (anomalib) | dui seal padhne, parichay jaanchne, ra antim tulna pura garne |

```text
1  Day04_03 (YOLO)     bandaphant → calibration mulyankan → surakshit
2  Day05_02 (anomalib) fit → bandaphant jaanch → calibration mulyankan → surakshit
3  Day05_03 (anomalib) calibration ma tulna → dui threshold sthir
4  Day04_03 (YOLO)     shared-sealed-test matra → sealed
5  Day05_02 (anomalib) clarity-sealed-test-scoring matra → sealed
6  Day05_03 (anomalib) dui seal → antim tulna
```

| abastha / situation | ke hunchha / what happens | ke garnu / what to do |
|---|---|---|
| sthir garnuaghi test mulyankan garyo bhane | threshold test ko natijama milauna sakinchha, ra "nahereko data ko natija" rahndaina. tyasaile talako sealed cell sthir abhilekh nabhae **chalna rokinchha.** | charan 1–3 pura garera matra charan 5 chalaunuhos. |
| "sabai chalaunuhos / Run All" bichma rokiyo | janajan rokieko ho. yo notebook charan 2 ra 5 ma gari dui patak kholinchha. pahilo "Run All" `clarity-sealed-test-scoring` ma rokinu nai sahi ho. | rokieko karan padhera mathiko 6 charan ek-ek garnuhos. |
| `comparison_freeze_record.json` chhaina | sthir gareko ghoshana ahile abhilekh bhaeko chhaina. | charan 3 (`Day05_03` ko `clarity-freeze-record`) chalaunuhos. |
| calibration ka tasbir pura chhainan | dui tarika eutai tasbir ma tulna sakidaina, tyasaile sthir nai huna sakdaina. | charan 1 ra 2 feri chalaera calibration ka anuman pura garnuhos. |
| kernel feri suru gariyo | talim gareko model haraeko chha, tyasaile mulyankan garna mildaina. feri fit garda memory bank badlinchha ra **tyo uhi experiment ko nirantarta hoina** (fingerprint badlinchha). | mulyankan garnuaghi kernel feri suru nagarnuhos. badhyata bhayera feri fit garne bhae `training_results/day05/.../*.ckpt` ko surakshit checkpoint padhera fingerprint milchha ki jaanchnuhos. na milae **naya experiment** ho. charan 3 ko sthir baat feri garnuhos ra parikshan ek patak herisakeko hunale `TEST_ALREADY_SEEN=True` nai rakhnuhos. |

**sthir abhilekh (`submissions/day05/comparison_freeze_record.json`) bhaneko** test hernuaghi "yo setting le
mulyankan garne" bhanera tay gareko praman ho. tyasma model, purb-prashodhan, threshold ra experiment ko
fingerprint hunchha. test mulyankan garepachhi yo abhilekh badalda natijako artha badlinchha, tyasaile
nabadalnuhos.

<!-- ne-cell: 09b10a38 | after-heading -->
**abhyas 1 (adharabhut): maapan abhilekh garne**
<!-- ne-pair: Exercise 1 (basic): record the metrics -->

<!-- ne-cell: 09b10a38 -->
Part 4 ka chaar maapan talika ma lekhnuhos. `image_AUROC` ra `pixel_AUROC` ko farak pani ek line ma
byakhya garnuhos.

<!-- ne-cell: 93a1ccd3 | after-heading -->
**abhyas 2 (madhyam): setting badaler calibration data ma tulna garne**
<!-- ne-pair: Exercise 2 (intermediate): change a setting and compare on calibration -->

<!-- ne-cell: 93a1ccd3 -->
`backbone="wide_resnet50_2"` badaler **calibration (pramanikaran) data ma** maapan ra lagne samay naper
`resnet18` sang tulna garnuhos. CPU matra bhaeko batabaran ma `wide_resnet50_2` dherai dhilo bhae **arko setting**
(jastai `layers=["layer3"]`, wa `coreset_sampling_ratio` badaler) ma uhi tulna garna saknuhunchha. **bhari
backbone prayog garnu baikalpik** ho. yo abhyasko uddeshya "uhi calibration data ma maapan ra samay naper
tulna gari abhilekh garnu" ho.

- tulna **uhi calibration data** ma `image_AUROC` jasta maapan ra **napieko samay** baat garnuhos.
- antim ma chhanieko eutai setting mulyankan garna parikshan bhaag jogaer rakhnuhos.
- abhilekhama **bhaag (calibration), model (backbone) ra chalaiko pahichan** aniwarya lekhnuhos.

<!-- ne-cell: 1fd52dc9 | after-heading -->
**abhyas 3 (baikalpik): samanya samanako bhinnata badhaune**
<!-- ne-pair: Exercise 3 (optional challenge): add normal variation -->

<!-- ne-cell: 1fd52dc9 -->
`assets/scripts/pvc_synth.py` prayog garera **ujyaloko asamanata badhaieka samanya tasbir** 10 bata thap
banaera `train/good/` ma rakhnuhos. tyaspachhi feri fit garera **calibration data (uhi sthir set) ma
samanya score ko adhikatam maan** ghatyo ki jaanchnuhos.

<!-- ne-cell: c81c8cac | after-heading -->
#### bujhai jaanchne prashna

<!-- ne-cell: c81c8cac -->
1. `train` ma asamanya tasbir kina rakhnu hundaina?
2. PatchCore ko "talim" le ke garchha? weight update hunchha?
3. `image_AUROC` ra `pixel_AUROC` le ke napchhan?
4. `val_split_mode="from_test"` kina prayog gariyo?
5. `image_AUROC` 1.0 bhae pani utpadanako nirikshan shuddhata bhanera kina uddhrit garna hundaina?

<!-- ne-cell: 2da75241 | after-heading -->
## samasya parema

<!-- ne-cell: 2da75241 -->
truti aepachhi pahile "kun cell ma", "kun line ma", "ke sandesh ayo" bhanera lekhnuhos.

| lakshan | ke garne |
| --- | --- |
| `ModuleNotFoundError: No module named 'anomalib'` | kernel galat chha. `Kernel` → `Change Kernel` → `Python 3 (AI Vision Anomalib)` chhannuhos. |
| `AttributeError: 'Folder' object has no attribute 'val_data'` | `val_split_mode="none"` rakhda aaunchha. `from_test` wa `from_train` toknuhos. |
| `MisMatchError` aaunchha | asamanya tasbir ra maskako jodi milen. `ground_truth/<prakar>/` ka file naam jaanchnuhos. |
| backbone daunalod asaphal | kakshaaghi `preload_models.py --profile anomalib` le liera janchinchha. kami bhae prashikshakasang sodhnuhos. |
| talim anautho rupama dhilo | `wide_resnet50_2` CPU ma dherai dhilo hunchha. `resnet18` prayog garnuhos. |
| memory apug hunchha | `train_batch_size` ra `eval_batch_size` 4 banaunuhos. |

<!-- ne-cell: 483ecbb0 | after-heading -->
## sampannata janchasuchi

<!-- ne-cell: 483ecbb0 -->
**aniwarya bunda matra** diieka chhan. **abhyas 3 (baikalpik) aniwarya hoina**; nagare pani pura maninchha.
sabai ma chinh lagepachhi yo notebook pura hunchha.

**aniwarya**

- [ ] `aivision-anomalib` kernel ma chalaen
- [ ] `train` ma samanya matra chha bhanera janchen
- [ ] PatchCore ko fit chalaen
- [ ] chaar maapan abhilekh garen
- [ ] heatmap heren
- [ ] score soochi ra anuman JSON surakshit garen
- [ ] abhyas 1–2 (aniwarya) garen
- [ ] bujhai jaanchne 5 prashnako uttar dien
- [ ] notebook surakshit garen

<!-- ne-cell: d02d8a44 | after-heading -->
## thap adhyayan (baikalpik)

<!-- ne-cell: d02d8a44 -->
### sandarbha lingk

- [Anomalib kagajat](https://anomalib.readthedocs.io/)
- [Anomalib: Folder data module](https://anomalib.readthedocs.io/en/latest/markdown/guides/reference/data/image/folder.html)
- [PatchCore patr](https://arxiv.org/abs/2106.08265)
- [torchvision ko model soochi](https://pytorch.org/vision/stable/models.html)

### thap chunauti (aniwarya hoina)

`coreset_sampling_ratio` 0.01 ra 0.5 ma prayas garera memory prayog ra maapan ko paribartan tulna garnuhos.
