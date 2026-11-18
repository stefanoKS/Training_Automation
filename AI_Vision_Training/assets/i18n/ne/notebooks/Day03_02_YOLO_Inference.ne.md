<!--
Nepali anuwad / Nepali translation source for
notebooks/Day03_YOLO_Basics/Day03_02_YOLO_Inference.ipynb
-->
# din 3 notebook 02 — Nepali anuwad

<!-- ne-cell: 9dd6a5e7 | after-heading -->
# din 3 notebook 02: pahilo YOLO anuman

<!-- ne-cell: 9dd6a5e7 -->
## sikai lakshyaharu

| Nepali |
| --- |
| 1. Ultralytics sthapana bhaeko chha ki chhaina jaanchna sakne. |
| 2. pretrained model padher tasbir ma anuman chalaun sakne. |
| 3. pahichanko natija (ayat, class, confidence) nikalna sakne. |
| 4. natija tasbirko rupama surakshit garna sakne. |
| 5. daunalod asaphal hunda ke garne bataun sakne. |

## yo notebookko adharabhut jankari

| bishay | biwaran |
| --- | --- |
| sikai samay (anuman) | 85 minet |
| kathinai | surubati tah |
| poorwashart | din 3 notebook 01 sakieko hunuparchha. pahilo patak matra intaranet chahinchha. |
| aawashyak laibreri | torch, torchvision, ultralytics, opencv-python, numpy, matplotlib |
| prayog hune kernel | aivision |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 3](../../COURSE_SYLLABUS.md#day3) |

### bujhaunuparne kaam

| Nepali |
| --- |
| tippani lagaieko tasbir (surakshit gareko file) |
| pahichanko natijako talika |

<!-- ne-cell: 8b3be722 | after-heading -->
## yo notebook kahan parchha

<!-- ne-cell: 8b3be722 -->
| bishay | biwaran |
| --- | --- |
| din | din 3 |
| ajako kram | ajako notabukamadhye 2 / 3 |
| lagne samay | 85 minet |
| poorwashart | `Day03_01_YOLO_Concepts.ipynb`, `yolo11n.pt` daunalod sakieko |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 3](../../COURSE_SYLLABUS.md#day3) |

dinko samayatalika `COURSE_SYLLABUS.md` ma eutai thaun ma chha. yo notebook tyasko euta bhaag matra ho.

<!-- ne-cell: audit-learning-loop | after-heading -->
### anuman garnuhos, chalaunuhos, hernuhos, byakhya garnuhos

<!-- ne-cell: audit-learning-loop -->
anumanle surakshit garieko weight prayog garera tasbir baat natija banaunchha. mahattwapurna cell chalaunuaghi input,
kaam ra natija ek-ek bakyama lekhnuhos. pahile anuman garera chalaunuhos ra maan wa chitra hernuhos.
confidence dekhaune sart matra badaler feri anuman gari chalaunuhos. janajan rakhieka truti ra nasakieka abhyaska
nirdeshan pachhyaunuhos.

<!-- ne-cell: f4b54286 | after-heading -->
## Part 0 tayari

<!-- ne-cell: 60086395 | after-heading -->
## Part 1 Ultralytics jaanchne

<!-- ne-cell: audit-teach_yolo_result_object | after-heading -->
### kod kasari padhne

<!-- ne-cell: audit-teach_yolo_result_object | after-image:../../assets/svg/teach_yolo_result_object.svg -->
chitra: confidence model ko score ho, sahi hune gyarenti hoina. (ganana garieko sansleshit udaharan ra yojanabaddha
chitra; model ko bastabik napieko natija hoina.)

**dhyan dinuparne kura**

confidence model ko score ho, sahi hune gyarenti hoina. input ra paribartan bhaeko maan aunlale pachhyaunuhos.

**sochnuhos**

pahichan shunya bhae talika ma kati line hunchhan?

<!-- ne-cell: 907c6b68 | after-heading -->
**pustakalay ra GPU ko abastha herne**
<!-- ne-pair: Look at the library and the GPU -->

<!-- ne-cell: 907c6b68 -->
pahile chahine sadhan sabai chhan ki chhaina janchaun.

`torch.cuda.is_available()` le `False` die pani **samasya chhaina**. yo talimko adharabhut bhaag CPU ma chalchha.

<!-- ne-cell: b514e5ac | after-heading -->
**yo notebook ma prayog hune model ra tasbirko srot**
<!-- ne-pair: Where the model and the image come from -->

<!-- ne-cell: b514e5ac -->
yo notebook ma dui kura prayog hunchhan.

| prakar | bishay | srot |
|---|---|---|
| model | `yolo26n.pt` (nano model) | Ultralytics ko adhikarik release `ultralytics/assets` ko `v8.4.0`. COCO ka 80 class ma pahile nai talim bhaeko |
| tasbir | `bus.jpg` | sthapana garieko `ultralytics` package (8.4.211) sangai aune `ultralytics/assets/bus.jpg` |

**srot ra laisensabare**

- "COCO ma pahile nai talim bhaeko" bhannale **model kun data ma talim bhayo** bhanne matra ho. sangai aune photo
  COCO kai tasbir ho bhanne hoina.
- package ko AGPL-3.0 **package bitaranko sart** ho. sangai aune harek photoko adhikarako praman hoina (package
  ma `bus.jpg` ra `zidane.jpg` ko chhuttai laisens suchana chhaina).
- yo talim ma chalne ki nachalne jaanchna sangai aune tasbir jastako tastai prayog garinchha. **photo feri bitaran
  garne wa utpadanama rakhne bhae prayogakarta aphainle adhikar janchnuparchha.**
- bistrit biwaran `assets/external_samples/PROVENANCE.md` ma chha.

> yo tasbir "bas ra manis" ko photo ho. **PVC ko dosh hoina.** pretrained model "thik chalchha" bhanera jaanchne
> tayari-parikshan matra ho.

<!-- ne-cell: b1bde3f5 | after-heading -->
## Part 2 model padhne

<!-- ne-cell: ced84bb3 | after-heading -->
**pahilo patak matra daunalod hunchha**
<!-- ne-pair: Downloaded once, cached afterwards -->

model file (karib 5 MB) **pahilo patak matra** daunalod hunchha. dosro patakadekhi `assets/models/` baat padhinchha,
tyasaile intaranet nabhae pani chalchha.

**daunalod asaphal hunda ke garne**

1. tyahi cell feri chalaunuhos (samanyataya asthayi samasya hunchha)
2. braujarama `https://github.com/ultralytics/assets/releases` kholer `yolo26n.pt` hataile daunalod gari
   `assets/models/` ma rakhnuhos
3. kampaniko proxy chha bhane byabasthapakasang sodhnuhos

> **daunalod huna nasake "jasto dekhine natija" banaunu hundaina.** truti jastako tastai abhilekh garera
> prashikshakasang sallah linuhos.

<!-- ne-cell: 16326241 | after-heading -->
### natijako udaharan

<!-- ne-cell: 16326241 -->
yo natija uhi model file bhae ma uhi aaunchha. model adyabadhik garda class sankhya wa naamko kram badalin sakchha.

<!-- ne-cell: c1293292 | after-heading -->
**janchnuparne kura**
<!-- ne-pair: What to verify here -->

<!-- ne-cell: c1293292 -->
class soochi ma `black_spot` ra `scratch` **chhainan** bhanera pakka garnuhos. din 4 ma nayan talim kina chahinchha
bhanne karan yahi ho.

<!-- ne-cell: de1be408 | after-heading -->
## Part 3 anuman chalaune

<!-- ne-cell: cf0e60bc | after-heading -->
### pahichanko natija "ayataharuko soochi" ho

<!-- ne-cell: cf0e60bc | after-image:../../assets/diagrams/diagram_detection.png -->
chitra: pahichanle ke pharkaunchha (yojanabaddha chitra, bastabik anumanko natija hoina, udaharanka lagi banaiyeko data).
ayat Ultralytics ko `result.boxes.xyxy` dhanchama (`x1, y1, x2, y2`) pharkinchha, ra confidence model le dieko
score ho, sahi hune sambhabana hoina. bastabik natija talako cellle tapainko computer ma banaunchha.

**dhyan dinuparne kura**

pahichanle eutai uttar pharkaundain. **ayat, class ra confidence ko jodi jati pani** pharkaun sakchha; shunya pani
huna sakchha. talako cell chalaunda tapainko tasbirko bastabik soochi dekhinchha.

**sochnuhos**

- pahichan shunya bhannu "kehi asamanya chhaina" bhanne arth ho?

<!-- ne-cell: 674b1102 | after-heading -->
**tasbir padher anuman garne**
<!-- ne-pair: Load an image and predict -->

<!-- ne-cell: 674b1102 -->
`model.predict()` ka mukhy argument:

| argument | arth | udaharan |
|---|---|---|
| `source` | tasbirko bato | `"image.jpg"` |
| `conf` | yasabhanda kam bhaeka pahichan **anumanakai bela phalinchha** | `0.25` |
| `imgsz` | input akar (sano bhae chhito) | `640` |
| `verbose` | lag dekhaune ki nadekhaune | `False` |

pharkaune maan "natijako soochi" ho. euta tasbir bhae `results[0]` ma tyo tasbirko natija hunchha.

`conf` le phaleka ummedabar, **pachhi threshold ghatae pani pharker aundainan**. "kam threshold ma ek patak anuman
garera pachhi chhanne" tarika ra harek patak `conf` badaler feri anuman garne tarika farak hun. din 3 notebook 03 ma
bistrit herinchha.

<!-- ne-cell: 1a88508f | after-heading -->
**ke-ke dekhiyo**
<!-- ne-pair: What you should see -->

<!-- ne-cell: 1a88508f -->
tasbir ma **euta bas ra kehi manis** chhan. harekama ayat banchha ra class naam sang confidence dekhinchha. yo talimko
abhilekhama `bus 0.88` `person 0.87` jasto dekhiyo. maan model, tasbir ra `conf` anusar badlinchha.

yahan mahattwapurna kura **model le talim lieka class pharkaun sakchha** bhanne pushti ho. PVC ko dosh pahichan
ajhai sambhab chhaina.

**pahichan shunya bhae ke?** yahan shunya bhannale **"tokieka class (COCO ka 80 prakar) ma banki pahichan shunya"**
bhanne matra ho. "yo tasbir ma dosh chhaina" bhanne praman hoina.

shunya hunuka dherai karan huna sakchhan.

- yo tasbir ma COCO ka class sanchchai chhainan
- `conf` thresholdle sabai ummedabar phaleko
- anuman aphain asaphal bhaeko (bato galat, tasbir padhna nasakine adi)

ulto, threshold ghataunda **COCO class ko rupama galat pahichan pani aun sakchha** (jastai prishthabhumiko buttalai
`stop sign` bhanera). COCO pretrained model PVC ko doshabare arthapurna nirnaya din banaiyeko hoina. tyasaile shunya lai
"OK" bhanera napadhi, **kun data ma talim bhaeko model ho, kun threshold ma chalaiyo, tasbir ma ke chha** bhanne kura
sangai padhnuhos.

<!-- ne-cell: 75c3644d | after-heading -->
## Part 4 natija nikalne

<!-- ne-cell: clarity-result-tree | after-heading -->
### pharkieko bastubat talikako ek line samma

<!-- ne-cell: clarity-result-tree -->
input aghillo anumanko `results` ho; natija harek pahichanko talika, chitra ra CSV ho. anuman: N=0 bhae
talika ma kati line hunchhan?

`results` (soochi / prati tasbir euta) → `results[0]` = pahilo tasbirko result → `boxes.xyxy` (N,4),
`boxes.cls` (N,), `boxes.conf` (N,) → talikako line → CSV, ra `result.plot()` le BGR chitra.

eutai `i` ma tinai gun milaunuhos. tal dekhaieko surakshit chitra pahileko ek patakako anuman ho, yo patakako N ko
gyarenti hoina. chalaepachhi pahilo line lai uhi numberko ayatasang milaunuhos. sano prayog: confidence philtar
badhaunda talikako line sankhya ke hunchha?

<!-- ne-cell: 541f0482 | after-heading -->
**ayat, class ra confidence sankhyako rupama nikalne**
<!-- ne-pair: Pull out boxes, classes and confidences -->

<!-- ne-cell: 541f0482 -->
tasbir ma banaera matra abhilekh wa nirnayaka lagi pugdain. **sankhya** ko rupama nikalnuparchha.

| gun | samagri | akar |
|---|---|---|
| `result.boxes.xyxy` | dui-bindu shailiko nirdeshangk | (N, 4) |
| `result.boxes.cls` | class kram sankhya | (N,) |
| `result.boxes.conf` | confidence | (N,) |
| `result.boxes.data` | mathika sabai miler 6 stambhako talika | (N, 6) |
| `result.names` | kram sankhya → class naam ko dictionary | dict |

`boxes.data` ka 6 stambha bayanbat **`x1, y1, x2, y2, confidence, class kram sankhya`** hun. yi 6 bhaepachhi
talika wa CSV banaun sakinchha.

<!-- ne-cell: fig-ref_inference_boxes_table | after-heading -->
### surakshit garieko udaharan: tasbirko number ra talikako line

<!-- ne-cell: fig-ref_inference_boxes_table | after-image:../../assets/reference_outputs/ref_inference_boxes_table.png -->
chitra: yo talim ma sanchchai surakshit garieka 5 pahichan ma number lagaera uhi numberka talika line sang rakhieko.
sandarbha natija (bastabik natija).

**dhyan dinuparne kura**

yo talika ra chitra eutai patakako anumanko natija ho (`yolo26n.pt`, conf=0.25, imgsz=640 ko abhilekh).
photo ultralytics package sangai aune namuna tasbir ho, COCO ma talim bhaeko model chinaun prayog bhaeko.
photoko srot ra adhikar package ko laisensabhanda chhuttai janchnuparchha (`assets/external_samples/PROVENANCE.md`).
yo PVC ko dosh hoina.

**sochnuhos**

- yo talikako confidence sahi pahichan hune sambhabana ho?

pahile surakshit garieko ek patakako anuman ho; ahileko natija sankhya batabaran anusar farak hunchha.

<!-- ne-cell: 18b85475 | after-heading -->
### natijako udaharan

<!-- ne-cell: 18b85475 -->
yo natija yo talim ma surakshit garieko abhilekh ho (`yolo26n.pt`, `conf=0.25`, `imgsz=640`). sukshma sankhya
batabaran anusar farak parchha, tar prabritti ra thulo-sanoko sambandh padhnuhos.

<!-- ne-cell: 37628bc4 | after-heading -->
## Part 5 natija surakshit garne

<!-- ne-cell: 4635e510 | after-heading -->
**tasbir ra talika surakshit garne**
<!-- ne-pair: Save the image and the table -->

<!-- ne-cell: 4635e510 -->
bujhaunuparne kaamka rupama dui kura surakshit garinchha.

1. tippani lagaieko tasbir → `submissions/day03/`
2. pahichan natijako talika (CSV) → `submissions/day03/`

surakshit garne thaun **talim folder baat sapeksh bato** le tay garinchha. tapainko prayogakarta naam wa sthapana
thaun ma nirbhar hundaina.

<!-- ne-cell: 7886dfe4 | after-heading -->
**`utf-8-sig` kina lagaune**
<!-- ne-pair: Why `utf-8-sig` -->

<!-- ne-cell: 7886dfe4 -->
CSV Excel ma kholda `utf-8` matra bhae Japani akshar bigran sakchha. `utf-8-sig` lagaunda Excel ma pani thik
dekhinchha. Nepali aksharako hakama pani yahi karanle `utf-8-sig` upayogi hunchha.

<!-- ne-cell: a82596f0 | after-heading -->
## abhyas

<!-- ne-cell: fbd218e2 | after-heading -->
**abhyas 1 (adharabhut): confidence ka adharama kram ma rakhne**
<!-- ne-pair: Exercise 1 (basic): sort by confidence -->

<!-- ne-cell: fbd218e2 -->
pahichanko natija confidence ko **badhi baat ghati** kram ma milaera mathilla 3 bata dekhaunuhos.

sanket: `table.sort_values(by="confidence", ascending=False)`

pura bhaeko maapan: pahilo lineko confidence tapainko talika ma sabaibhanda thulo ho. class naam ra maan harek patak
farak huna sakchha, abhilekhako `bus 0.88` sang milnaiparchha bhanne chhaina.

<!-- ne-cell: 744ed2c5 | after-heading -->
**abhyas 2 (madhyam): `zidane.jpg` ma pani anuman chalaune**
<!-- ne-pair: Exercise 2 (intermediate): run it on `zidane.jpg` too -->

<!-- ne-cell: 744ed2c5 -->
Ultralytics sangai `zidane.jpg` pani aaunchha. uhi kram ma anuman chalaera **bhetieka class ra sankhya** dekhaunuhos.

pura bhaeko maapan: aphnai natija baat kati `person` bhetiyo ra aru ke bhetiyo bhanera bataun sakne.

<!-- ne-cell: 5759f10e | after-heading -->
**abhyas 3 (baikalpik): PVC ko tasbir ma lagaera herne**
<!-- ne-pair: Exercise 3 (optional challenge): try it on a PVC-like image -->

<!-- ne-cell: 5759f10e -->
`assets/defect_samples/defect_multi.png` ma anuman chalaunuhos. **ke banki rahyo? kehi banki rahen bhane
tyasko arth ke ho?**

din 1 ra din 3 notebook 01 ma sikeka karan prayog garera tin line ma byakhya garnuhos.

pura bhaeko maapan: banki raheka pahichan (bhae) ra kehi narahanuko karan class paribhasha, kshetra, akar ra khichaiko
abasthako drishtile byakhya gareko chha, ra shunya lai "samanya" wa "dosh chhaina bhanne sahi uttar" lekheko chhaina.

<!-- ne-cell: d60cb985 | after-heading -->
#### bujhai jaanchne prashna

<!-- ne-cell: d60cb985 -->
1. `model.predict()` le ke pharkaunchha? euta tasbir hunda kahan herne?
2. `conf` ghataunda banki pahichanko sankhya ke hunchha? sadhain badhchha? tyasko satta ke badhchha?
3. pahichanko natija baat "class naam" kasari nikalne?
4. model daunalod asaphal bhae tapain ke garnuhunchha?
5. sangai aune `bus.jpg` ra `zidane.jpg` prayog garnuka phaida ra dhyan dinuparne kura bhannuhos.

<!-- ne-cell: 3417c856 | after-heading -->
## samasya parema

<!-- ne-cell: 3417c856 -->
truti aepachhi pahile "kun cell ma", "kun line ma", "ke sandesh ayo" bhanera lekhnuhos. bujhaunuparne kaam ma pani
tyahi abhilekh rakhnuhos.

| lakshan | ke garne |
| --- | --- |
| `ModuleNotFoundError: No module named 'ultralytics'` | kernel galat chha wa `ultralytics` chhaina. `requirements\yolo.txt` jaanchnuhos. |
| `URLError` / `TimeoutError` le daunalod hundaina | feri chalaunuhos. sudhar nabhae releases pejabat hataile daunalod gari `assets/models/` ma rakhnuhos. |
| `RuntimeError: ... CUDA ...` | CPU sanskaranako torch chha ki jaanchnuhos. GPU nabhai CUDA tokda asaphal hunchha. |
| pahichan sankhya shunya | `conf` ghataunuhos (jastai 0.10) wa tasbir ma sanchchai bastu chha ki jaanchnuhos. |
| tasbir dekhindain | `result.plot()` BGR pharkaunchha. `cv2.cvtColor(..., cv2.COLOR_BGR2RGB)` birsieko chha ki jaanchnuhos. |
| dherai dhilo chalchha | CPU ma euta tasbir ma kehi sekend lagchha. `imgsz=320` rakhda chhito hunchha. |

<!-- ne-cell: 3f7ce62e | after-heading -->
## sampannata janchasuchi

<!-- ne-cell: 3f7ce62e -->
**aniwarya** bhaneko talako "aniwarya" soochi matra ho. **abhyas 3 ra thap chunauti baikalpik** hun; nagare pani pura
maninchha. samay banki bhae ma matra garnuhos.

**aniwarya**

- [ ] Part 1–Part 5 padher sabai code cell chalaen
- [ ] model daunalod bhaera `assets/models/` ma surakshit bhayo
- [ ] tippani lagaieko tasbir surakshit garen
- [ ] pahichan natijako talika CSV ma surakshit garen
- [ ] abhyas 1 ra 2 (aniwarya) garen
- [ ] class soochi ma `black_spot` chhaina bhanera pakka garen
- [ ] bujhai jaanchne 5 prashnako uttar dien
- [ ] notebook surakshit garen

**baikalpik**

- [ ] abhyas 3 (baikalpik): PVC tasbir ma natija jancher karan tin line ma lekhen
- [ ] thap chunauti: `imgsz` badaler pahichan sankhya ra samay tulna garen

<!-- ne-cell: bceb7c93 | after-heading -->
## thap adhyayan (baikalpik)

<!-- ne-cell: bceb7c93 -->
### sandarbha lingk

- [Ultralytics Predict mod](https://docs.ultralytics.com/modes/predict/)
- [Ultralytics model ko soochi](https://docs.ultralytics.com/models/)
- [COCO dataset](https://cocodataset.org/)

### thap chunauti (aniwarya hoina)

`imgsz` lai 320 / 640 / 1280 badaler pahichan sankhya ra chalne samayko paribartan talika ma rakhnuhos.
