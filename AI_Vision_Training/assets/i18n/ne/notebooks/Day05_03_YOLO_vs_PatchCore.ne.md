<!--
Nepali anuwad / Nepali translation source for
notebooks/Day05_PatchCore/Day05_03_YOLO_vs_PatchCore.ipynb
-->
# din 5 notebook 03 — Nepali anuwad

<!-- ne-cell: ba87b991 | after-heading -->
# din 5 notebook 03: YOLO ra PatchCore ko tulna

<!-- ne-cell: ba87b991 -->
## sikai lakshyaharu

| Nepali |
| --- |
| 1. dui bidhiko natijako farak byabasthit garna sakne. |
| 2. eutai tasbir setama dubaiko natija sangai rakhna sakne. |
| 3. eutai adharama OK/NG tulna garda dhyan dinuparne kura bataun sakne. |
| 4. dubaiko phaida ra kamajori utpadanako drishtile bataun sakne. |
| 5. PVC nirikshan ma kun, kun kram ma prayog garne sujhab din sakne. |

## yo notebookko adharabhut jankari

| bishay | biwaran |
| --- | --- |
| sikai samay (anuman) | 100 minet |
| kathinai | surubati tah |
| poorwashart | din 4 notebook 03 ra din 5 notebook 02 chalaisakeko ra natija `submissions` ma surakshit bhaeko hunuparchha. |
| aawashyak laibreri | pandas, numpy, matplotlib, pillow |
| prayog hune kernel | `aivision-anomalib` (YOLO ko natija file baat padhinchha) |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 5](../../COURSE_SYLLABUS.md#day5) |

### bujhaunuparne kaam

| Nepali |
| --- |
| tulnako talika |
| sangai rakhieka natija tasbir |
| PVC nirikshanka lagi sipharis (nirnaya ra karan) |

> YOLO ra PatchCore dui farak batabaran ma chhan, tyasaile yo notebookle dubai model lod nagari **surakshit natija**
> tulna garchha. yo janajan garieko dijain ho ra `requirements/tested_versions.md` ma lekhieko chha.

<!-- ne-cell: 1e496b72 | after-heading -->
## yo notebook kahan parchha

<!-- ne-cell: 1e496b72 -->
| bishay | biwaran |
| --- | --- |
| din | din 5 |
| ajako kram | ajako notabukamadhye 3 / 3 |
| lagne samay | 100 minet |
| poorwashart | `Day04_03` ra `Day05_02` ka surakshit natija |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 5](../../COURSE_SYLLABUS.md#day5) |

dinko samayatalika `COURSE_SYLLABUS.md` ma eutai thaun ma chha. yo notebook tyasko euta bhaag matra ho.

<!-- ne-cell: audit-learning-loop | after-heading -->
### anuman garnuhos, chalaunuhos, hernuhos, byakhya garnuhos

<!-- ne-cell: audit-learning-loop -->
calibrationle nirnayako niyam tay garne charan ho. parikshanle sthir garepachhi arko data ma jaanchne charan ho.
mahattwapurna cell chalaunuaghi input, kaam ra natija ek-ek bakyama lekhnuhos. pahile anuman garera chalaunuhos;
calibrationko slider matra badaler feri anuman gari chalaunuhos.

<!-- ne-cell: b1dbfcbd | after-heading -->
## Part 0 tayari

<!-- ne-cell: c92bae7e | after-heading -->
## Part 1 natijako farak samjhane

<!-- ne-cell: 404278ad | after-heading -->
**jo milauna sakindaina, tyas lai uhi dhanchama narakhne**
<!-- ne-pair: Do not pretend different things are the same -->

<!-- ne-cell: 404278ad -->
dui bidhile **farak kura pharkaunchhan**.

| | YOLO | PatchCore |
|---|---|---|
| mukhy natija | ayat + class + confidence | score + heatmap |
| "kun dosh" | **thaha hunchha** | thaha hundaina |
| "kahan" | ayatako sthan | heatmap ko chamkilo thaun |
| talim ma chahine | doshko label | samanya bhanera pushti bhaeka tasbir |

tyasaile **mAP ra AUROC sidhai tulna garnu hundaina**; ti farak kura napchhan.

tulna garna milne kura **uhi sahi labelka adharama dubai bidhile tasbir-star ma dieko OK/NG nirnaya** ho.
tyaska lagi **harek bidhiko nirnaya niyam (threshold) ghoshana garera dubailai uhi sahi uttar sang bhidaunuparchha**.
dui bidhi apasama milchhan ki mildainan matra herda **dubai uhi tarikale galat bhaeko abastha** chhutchha.

<!-- ne-cell: c1bfc258 | after-heading -->
## Part 2 surakshit natija padhne

<!-- ne-cell: fig-teach_evaluation_sequence | after-heading -->
### tulnako mukhy kram

<!-- ne-cell: fig-teach_evaluation_sequence | after-image:../../assets/svg/teach_frozen_threshold_pipeline.svg -->
chitra: sthir garnuaghiko calibration ra sthir garepachhiko parikshan chhutyaune yojanabaddha chitra. yo paath ma yas lai
chha charan ma milainchha.

1. bibhajan manifest ra uhi tasbir ID jaanchne
2. dubai model ko anuman ID le milaune
3. calibration ma matra YOLO ko C ra PatchCore ko T chhanne
4. model, purb-prashodhan, samanya memory, pachhi-prashodhan ra threshold abhilekh gari sthir garne
5. prayog nabhaeko test ek patak mulyankan garne
6. uhi tasbir-ekaima TP/FP/FN/TN tulna garne

| bhaag | anumati hune kaam |
|---|---|
| fit | YOLO ko weight ra PatchCore ko samanya memory banaune |
| calibration | setting ra threshold chhanne |
| parikshan | sthir garepachhiko mulyankan matra; samayojan nishedh |

calibration surakshit udaharan ma samanya n=6 ra asamanya n=20 chhan.

anuman: jhuto alarm darko sima 10% bhae samanya 6 tasbir ma kati batasamm? `floor(6×0.10)=0` ho. yo
utpadanama 10% bhanda kam hunchha bhanne gyarenti hoina. sangai aune chitraka 0.06/0.50 surakshit udaharan hun;
yo patakako threshold calibration kodale ganana gareko maan baat aaunchha.

<!-- ne-cell: be4aa133 | after-heading -->
**tin file padhne**
<!-- ne-pair: Read the three files -->

<!-- ne-cell: be4aa133 -->
| file | banaeko thaun | bhitr ke chha |
|---|---|---|
| `submissions/day05/split_manifest.json` | din 5 notebook 02 | **bibhajanako abhilekh**: kun tasbir talim, calibration wa parikshan ho |
| `submissions/day04/yolo_predictions_on_shared_set.json` | din 4 notebook 03 | sabai tasbirko YOLO pahichan (confidence sahit) |
| `submissions/day05/patchcore_predictions.json` | din 5 notebook 02 | **calibration matra** ko PatchCore score (test hoina) |
| `submissions/day05/patchcore_test_predictions.json` | din 5 notebook 02 ko antim "sealed" cell | **sthir garepachhi ek patak** matra baneko test score |

**bibhajanako abhilekh nabhaeko natija prayog garindain.** kun data ma threshold tay gariyo thaha nabhaeko sankhya
tulnako adhar bann sakdain. purano dhanchako file bhae karan dekhaer rokinchha.

<!-- ne-cell: 415b6d88 | after-heading -->
**frame banaune**
<!-- ne-pair: Turn them into frames -->

<!-- ne-cell: 415b6d88 -->
`image` stambha dubai bidhi ma eutai tarikale (`prakar/phailanam.png`) milainchha. namilae eutai tasbir lai dui
bidhi sang jodn sakindaina.

<!-- ne-cell: ff4aa9d1 | after-heading -->
## Part 3 eutai tasbir ma sangai rakhne

<!-- ne-cell: a0a1bf15 | after-heading -->
**dubai bidhiko natija bhaeka tasbir matra prayog garne**
<!-- ne-pair: Use only images where both methods produced a result -->

<!-- ne-cell: a0a1bf15 -->
ek bidhiko matra natija bhaeko tasbir **tulna garna sakindaina**. chupachap phalda "anukul tasbir matrako
tulna" banchha. tyasaile pahile **kati tasbir mile ra kati chhute** ganer dekhainchha.

<!-- ne-cell: 38cb927e | after-heading -->
**bhaag anusar chhutyaune**
<!-- ne-pair: Split the images into their roles -->

<!-- ne-cell: 38cb927e -->
| bhaag | ke ka lagi | kahile herna milchha |
|---|---|---|
| `patchcore_train` | PatchCore ko talim (samanya matra) | talimakai bela matra |
| `calibration` | **threshold ra nirnaya niyam tay garne** | jati patak pani herna milchha |
| `test` | antama ek patak natija nikalne | **model, purb-prashodhan ra threshold sthir garepachhi** |

herna milchha ki mildaina bhanne kura **"jankari kasari prayog bhayo"** le tay garchha. parikshan data herer
threshold wa purb-prashodhan badaliyo bhane tyo data "ajhai nadekhieko data" rahandain. sthir gareko setting ma
uhi mulyankan feri chalaun hunchha (tyo punarutpadanako jaanch ho).

yo talimka sandarbha chitra **surakshit garieko ek patakako chalaibat baneka prakashit natija** hun. ti chitra ma
parikshanka udaharan herepachhi setting badaliyo bhane tapainko parikshan data aba prayog nabhaeko bhann mildaina.
nayan antim natijaka lagi **nayan prayog nabhaeko data** chahinchha.

<!-- ne-cell: 904252da | after-heading -->
## Part 4 eutai adharama OK/NG nikalne

<!-- ne-cell: d8230d25 | after-heading -->
**threshold "calibration" ma tay garne**
<!-- ne-pair: Choose the thresholds on the calibration partition -->

<!-- ne-cell: d8230d25 -->
aghillo sanskaranama samanya score ko adhikatam ra asamanya score ko nyoonatam baat threshold tay garera
**uhi data ma natija nikalieko** thiyo. tyo "uttar herepachhi angk dinu" jastai ho ra sankhya ramro dekhinchha.
tyo hataiyo.

ahile dui charan chhan.

1. **calibration** ma dui threshold tay garne. uddeshya eutai: **samanya samanako jhuto rijekt dar
   (false reject rate) 10% wa kam rakher recall adhikatam banaune.** yo 10% **yo talimko lakshya** ho.
   calibration ma samanya saman 6 matra bhaeko hunale 10% ko arth "jhuto alarm 0" ho.
   **utpadanako jhuto alarm darko gyarenti garne sankhya hoina.**
2. tay gareko maan **sthir** garera **parikshan** ma ek patak matra natija nikalne.

| bidhi | nirnaya niyam | tay garne maan |
|---|---|---|
| YOLO | `confidence ≥ C` bhaeko pahichan ek wa badhi bhae NG | `C` |
| PatchCore | `score ≥ T` bhae NG | `T` |

dui threshold **tyasai tulna garna mildaina**; napine kura farak chha (YOLO ma confidence, PatchCore ma
calibrationle samanyikrit score). sanyogale uhi sankhya aun sakchha, tar tyasko arth "uhi kura" hoina.
tulna garine kura sankhya hoina, **uhi sahi uttarka adharama tasbir-starko OK/NG nirnaya** ho.

<!-- ne-cell: fig-ref_score_distribution | after-heading -->
### calibration datako bitaran

<!-- ne-cell: fig-ref_score_distribution | after-image:../../assets/reference_outputs/ref_score_distribution.png -->
chitra: calibration (validation) datako matra score bitaran ra tyasaibat tay garieko threshold 0.50
(surakshit 0–1 maapan ma). parikshan data samabesh chhaina.

**dhyan dinaparne kura**

score anomalib 2.7.0 ko pachhi-prashodhanale
`clip((kachcha maan − threshold) ÷ (calibrationko adhikatam − nyoonatam) + 0.5, 0, 1)` ma badaleko chha,
tyasaile **talim bhaeko threshold 0.5** hunchha. calibration ma samanya 6 ra asamanya 20 tasbir chhan;
6 ma jhuto alarm 0 hunu "utpadanama pani 0" ko gyarenti hoina.

**sochnuhos**

- threshold 0.60 banaunda yo calibration data ma kati tasbir chhutne badhchha?

<!-- ne-cell: audit-teach_frozen_threshold_pipeline | after-heading -->
### sthir garnuaghiko antim jaanch

<!-- ne-cell: audit-teach_frozen_threshold_pipeline -->
suruko mukhy kram ma pharker calibration ma matra chhanieka dui maan ra model manifest milaunuhos.
parikshan herer setting badaliyo bhane nayan antim mulyankanka lagi nayan prayog nabhaeko data chahinchha.

<!-- ne-cell: c818bf0a | after-heading -->
**threshold sarn milne calibration data ma matra**
<!-- ne-pair: You may move thresholds on the calibration data only -->

<!-- ne-cell: c818bf0a -->
talako slider le **calibration data** ko score bitaran matra prayog garchha. parikshanko score lod garieko chhaina.
**calibration ma jati patak prayas gare pani pachhiko parikshan talika badalindain.**

tar **parikshanko natija herisakepachhi** calibrationko slider sarer feri chhanda pani tyo nirnaya
"parikshanko natija thaha bhaeko manchhele" gareko hunchha. **nayan antim natijaka lagi nayan prayog nabhaeko
data chahinchha.**

jhuto alarm (FP) ra chhutnu (FN) **sadhain uhi disha ma sardainan**. threshold badhaunda chhutne badhchha ra jhuto
alarm ghatchha. **dubai ekaichoti 0 huna pani sakchhan** — samanya samanako adhikatam skorabhanda asamanya samanako
nyoonatam score badhi bhae (bitaran ma khali thaun bhae). yo talim ma surakshit chalaima calibration data ma tyo
khali thaun bhaeko hunale PatchCore 0.50 ma **calibrationka 26 tasbir (samanya 6, asamanya 20) ma**
chhutnu 0 ra jhuto alarm 0 bhayo. **yo ek patakako abhilekhit chalaiko maan** ho, junasukai batabaran ma uhi hundaina.
sathai **threshold sarda sankhya nabadaline khand** pani hunchha (tyo bichama parne tasbir nabhaekole). khali
thaun nabhaeko data ma euta patti tyagnaiparchha.

<!-- ne-cell: fig-teach_threshold_freeze | after-heading -->
### calibration ma tay garera sthir garne

<!-- ne-cell: fig-teach_threshold_freeze | after-image:../../assets/diagrams/teach_threshold_freeze.png -->
chitra: calibration data ma threshold tay garera sthir garne kram (yojanabaddha chitra). chitrako YOLO 0.06 ra
PatchCore 0.50 surakshit purana udaharan hun; yo patakako maan calibration kodale tay garchha.

**dhyan dinuparne kura**

sthir garepachhi parikshan data herer sarda tyo sankhya aba "prayog nabhaeko datako natija" rahandain.
calibration ma samanya 6 ra asamanya 20 tasbir bhaeko hunale anupaat 1/6 ko pailama matra sarchha.

**sochnuhos**

- calibration ma samanya 6 tasbir hunda jhuto alarm dar 10% wa kam rakhna jhuto alarm kati batasamm
  huna milchha?

<!-- ne-cell: clarity-freeze-prompt | after-heading -->
#### aniwarya: sthir gareko ra prayog nabhaeko kura abhilekh garne

<!-- ne-cell: clarity-freeze-prompt -->
calibrationka prayog sakepachhi talako ghoshana aphnai shabdama bharnuhos:
"parikshan hernuaghi setting sthir garen ra parikshan herepachhi samayojan garne chhaina." model, purb-prashodhan ra
thresholdko abhilekh jaanchnuhos. parikshan tasbir wa natija pahile herisaknubhaeko chha bhane
`TEST_ALREADY_SEEN=True` nai rakhnuhos; tyo natija **punah prayog garieko datako udaharan mulyankan**
ho. nahereko abastha ma matra False banaunuhos. khali chhode parikshan mulyankan chaln sakdain.

<!-- ne-cell: clarity-slider-before-freeze -->
calibration slider hernaka lagi matra ho, apanaine dui maan badaldain. uddeshyaanusarako maan calibration
chhanot garne cell feri chalaer jaanchnuhos. yo abalokanapachhi sthir garnuhos ra sthir abhilekhako
`assessment_role` bujhaunuparne kaam ma samabesh garnuhos.

<!-- ne-cell: clarity-sealed-test-read | after-heading -->
**sealed test prediction padhne**

<!-- ne-cell: clarity-sealed-test-read -->
test score sthir abhilekh gariepachhi din 5 notebook 02 ko antim cell le ek patak matra mulyankan garera
`submissions/day05/patchcore_test_predictions.json` ma sealed garera rakheko hun. yo cell tyo sealed file
padhchha ra **bibhajan abhilekh, model ra threshold milchha ki** jaanchera matra talika banaunchha.
namilyo bhane rokinchha. yahan feri mulyankan garindaina.

<!-- ne-cell: 3d343aab | after-heading -->
**sthir garieko thresholdle parikshan ek patak matra mulyankan garne**
<!-- ne-pair: Score the test partition once, with the frozen thresholds -->

<!-- ne-cell: 3d343aab -->
threshold calibration data ma tay garera **yahan sthir** gariyo. aba parikshanko sankhya herer threshold
sarnubhayo bhane tyo talika "uttar herer angk dieko talika" banchha. sarn man lage aghillo calibration
slider **calibration data** ma prayog garnuhos. parikshan pahile nai herisaknubhaeko bhae badalieko settingka
lagi **arko prayog nabhaeko data** chahinchha; uhi parikshan ma feri garieko mulyankan lai mul antim parikshan
natijako rupama dekhaunu hundaina.

**weight, purb-prashodhan, samanya memory ra pachhi-prashodhan pani sthir** garinchha. parikshan herer yi badalnu
hundaina. sangai aune chitraka 0.06 / 0.50 surakshit sandarbha chalaika udaharan hun, yo patakako chalaiko apekshit
maan hoina.

<!-- ne-cell: ec601269 | after-heading -->
### natijako udaharan

<!-- ne-cell: ec601269 -->
yo natija yo talim ma surakshit garieko abhilekh ho (model, data bibhajan ra seed lekhama chha). sukshm sankhya
batabaran anusar farak parchha; prabritti ra thulo-sanoko sambandh padhnuhos. `x` raheko thaun tapainko batabaranle
tay garne maan ho.

surakshit chalaile talaka dui threshold sthir gar‍yo. pahilo khandalai **calibration** (threshold chhanieko
thaun) ra dosrolai **ek patakako parikshan mulyankan** padhnuhos.

<!-- ne-cell: aa3a7737 | after-heading -->
## Part 5 natija sangai herne

<!-- ne-cell: bf9157ac | after-heading -->
### tulna garnuaghi: tin pyanal kasari padhne

<!-- ne-cell: bf9157ac | after-image:../../assets/diagrams/teach_score_map_overlay.png -->
yo yojanabaddha chitra **tin pyanal** ko chha: mul tasbir, asamanyata naksa ra milaer dekhaieko chitra.
yo bastabik model ko natija pani hoina ra paanch-stambha tulna pani hoina.

anuman: rangako dayara matra badaliyo bhane score badlinchha? sthanako sanket padhna rang-patti hernuhos.

<!-- ne-cell: fig-ref_comparison_5col | after-heading -->
### sthir garepachhiko parishisht: surakshit TEST ka paanch stambha

<!-- ne-cell: fig-ref_comparison_5col -->
talako baikalpik cellle matra surakshit TEST ko chitra dekhaunchha. pahilo prayog nabhaeko parikshan sakunjel
False rakhnuhos. dekhaisakepachhi yo data ma feri chhanieko setting lai "prayog nabhaeko parikshanko natija"
bhann mildaina.

<!-- ne-cell: clarity-calibration-boundary | after-heading -->
### yahan baat CALIBRATION

<!-- ne-cell: clarity-calibration-boundary -->
talako gallery calibration tasbirko ho, mathiko surakshit TEST ka tin tasbirabhanda farak. diskako folder
naam `test/` le hoina, bibhajan manifest le bhoomika tay garchha.

<!-- ne-cell: 29824f9c | after-heading -->
#### tulnako byakhya

<!-- ne-cell: 29824f9c -->
heatmaple sthan dekhaunchha, YOLO le talim lieka class ko sanket dinchha. milaer prayog garda phaida hunchha
bhanne gyarenti chhaina; gati ra galti naper nirnaya garnuhos. surakshit TEST ka thos asaphal udaharan sthir
garepachhiko baikalpik parishishtama matra chhan. sansleshit ra bastabikko farak, thorai data, labelko bajet, ra
rijolyusan, purb-prashodhan tatha threshold ma nirbharata riport garnuhos.

<!-- ne-cell: bb4b29d3 | after-heading -->
## abhyas

<!-- ne-cell: 38937c33 | after-heading -->
**abhyas 1 (adharabhut): tulnako talika pura garne**
<!-- ne-pair: Exercise 1 (basic): complete the comparison table -->

<!-- ne-cell: 38937c33 -->
talako talika aphnai natijale bharnuhos.

| bishay | YOLO | PatchCore |
|---|---|---|
| talim ma chahine tasbir | | |
| talim ma chahine label | | |
| natija | | |
| doshko prakar thaha hunchha? | | |
| sthan thaha hunchha? | | |
| chhutne (FN) sankhya | | |
| jhuto alarm (FP) sankhya | | |

<!-- ne-cell: b9498efe | after-heading -->
**abhyas 2 (madhyam): calibration data ma threshold sarne**
<!-- ne-pair: Exercise 2 (intermediate): move the threshold on the calibration data -->

<!-- ne-cell: b9498efe -->
PatchCore ko threshold 0.30 / 0.50 / 0.80 badaler **chhutnu (FN) ra jhuto alarm (FP)** kasari badlinchha
**tin lineko talika** ma rakhnuhos. **threshold badalna calibration data matra prayog garnuhos.**
parikshan data ma tyahi garda tyo talika "uttar herer angk dieko" banchha.

| threshold | chhutnu FN (har: asamanya 20) | jhuto alarm FP (har: samanya 6) |
|---|---|---|
| 0.30 | | |
| 0.50 | | |
| 0.80 | | |

**sakieko manine abastha:** tin lineko talika banyo ra FN ra FP biparit disha ma sarchhan (kahilekahin
ekaichoti nasarn pani sakchhan) bhanera ek bakyama lekhiyo. sankhya nabadaline line bhae karan pani lekhnuhos.

<!-- ne-cell: 09fc3b55 | after-heading -->
**abhyas 3 (baikalpik): PVC nirikshanka lagi sipharis banaune**
<!-- ne-pair: Exercise 3 (optional challenge): build a recommendation for PVC -->

<!-- ne-cell: 09fc3b55 -->
talako dhanchama **tapainko sipharis** lekhnuhos. adharaka rupama yi 5 din ma paeka sankhya wa abalokan
aniwarya uddhrit garnuhos.

| bishay | tapainko sipharis |
|---|---|
| pahilo charan ma prayog garne bidhi | |
| tyasko karan | |
| dosro charan ma thapne bidhi | |
| chhutne ghataun ke garne | |
| jhuto alarm ghataun ke garne | |
| hapta 2 ma janchnuparne kura | |

<!-- ne-cell: 9a48e17c | after-heading -->
#### bujhai jaanchne prashna

<!-- ne-cell: 9a48e17c -->
1. YOLO ko mAP ra PatchCore ko AUROC sidhai tulna garna kina mildaina?
2. tasbir-star ma tulna garna dubailai ke chahinchha?
3. PatchCore le kasto dosh chhutaun sakchha?
4. YOLO le kasto dosh chhutaun sakchha?
5. tapainko karyasthalama kun pahile prayas garnuhunchha? karan pani lekhnuhos.

<!-- ne-cell: 30e783b7 | after-heading -->
## samasya parema

<!-- ne-cell: 30e783b7 -->
truti aepachhi pahile "kun cell ma", "kun line ma", "ke sandesh ayo" bhanera lekhnuhos.

| lakshan | ke garne |
| --- | --- |
| `yolo_predictions_on_shared_set.json` chhaina | din 4 notebook 03 ko Part 5 chalaunuhos. |
| `patchcore_predictions.json` chhaina | din 5 notebook 02 ko Part 5 chalaunuhos. |
| sajha tasbir 0 hunchha | batoko dhancha farak huna sakchha. `image` stambhako suruko `test/` hataieko chha ki jaanchnuhos. |
| precision wa recall `nan` hunchha | TP + FP wa TP + FN shuny chha. asamanya tasbir ek pani chhaina, wa ek pani pahichan bhaeko chhaina. |

<!-- ne-cell: dca7b3f3 | after-heading -->
## sampannata janchasuchi

<!-- ne-cell: dca7b3f3 -->
**aniwarya bunda matra** diieka chhan. **abhyas 3 (baikalpik) aniwarya hoina**; nagare pani pura maninchha.
sabai ma chinh lagepachhi yo notebook pura hunchha.

**aniwarya**

- [ ] Part 1–Part 5 padher sabai code cell chalaen
- [ ] dui natija file padhna saken
- [ ] sajha tasbir ma tulnako talika banaen
- [ ] threshold sarer FN / FP ko paribartan heren
- [ ] tulnaka chaar sima byakhya garna sakchhu
- [ ] abhyas 1–2 (aniwarya) garen
- [ ] bujhai jaanchne 5 prashnako uttar dien
- [ ] notebook surakshit garen

<!-- ne-cell: e39fff93 | after-heading -->
## thap adhyayan (baikalpik)

<!-- ne-cell: e39fff93 -->
### sandarbha lingk

- [Anomalib kagajat](https://anomalib.readthedocs.io/)
- [Ultralytics mulyankan mod](https://docs.ultralytics.com/modes/val/)
- [MVTec AD benchamark](https://paperswithcode.com/sota/anomaly-detection-on-mvtec-ad)

### thap chunauti (aniwarya hoina)

uhi tasbir ma YOLO le pahichan gareko sthan ra PatchCore ko heatmap ko sabaibhanda chamkilo bindubich kati
duri chha, tin tasbir ma napnuhos.
