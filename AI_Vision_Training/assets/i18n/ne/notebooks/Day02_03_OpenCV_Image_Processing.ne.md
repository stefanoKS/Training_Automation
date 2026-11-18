<!--
Nepali anuwad / Nepali translation source for
notebooks/Day02_Python_OpenCV/Day02_03_OpenCV_Image_Processing.ipynb
-->
# din 2 notebook 03 — Nepali anuwad

<!-- ne-cell: f477b90d | after-heading -->
# din 2 notebook 03: OpenCV ra duri napne

<!-- ne-cell: f477b90d -->
## sikai lakshyaharu

| Nepali |
| --- |
| 1. OpenCV le tasbir padhna, dekhauna ra surakshit garna sakne. |
| 2. greskel ra bainarikaranako arth bataun sakne. |
| 3. kantur (contour) bheter tyasko sthan nikalna sakne. |
| 4. dui bindubichako duri pikselama ganana garna sakne. |
| 5. pikselalai milimitarama badalna ra shuddhatako sima bataun sakne. |

## yo notebookko adharabhut jankari

| bishay | biwaran |
| --- | --- |
| sikai samay (anuman) | 60 minet |
| kathinai | surubati tah |
| poorwashart | din 2 notebook 01 ra 02 sakieko hunuparchha. |
| aawashyak laibreri | opencv-python, numpy, matplotlib, pillow |
| prayog hune kernel | aivision |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 2](../../COURSE_SYLLABUS.md#day2) |

### bujhaunuparne kaam

| Nepali |
| --- |
| kinara (edge) ra kantur bheteko natija |
| piksel→mm ko natija ra napako trutibare chhoto bichar |

<!-- ne-cell: 061efcfb | after-heading -->
## yo notebook kahan parchha

<!-- ne-cell: 061efcfb -->
| bishay | biwaran |
| --- | --- |
| din | din 2 |
| ajako kram | ajako notabukamadhye 3 / 3 |
| lagne samay | 60 minet |
| poorwashart | `Day02_02_Conditions_Loops_Functions.ipynb` |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 2](../../COURSE_SYLLABUS.md#day2) |

dinko samayatalika `COURSE_SYLLABUS.md` ma eutai thaun ma chha. yo notebook tyasko euta bhaag matra ho, aphno
chhuttai samayatalika rakhdain.

<!-- ne-cell: audit-learning-loop | after-heading -->
### anuman garnuhos, chalaunuhos, hernuhos, byakhya garnuhos

<!-- ne-cell: audit-learning-loop -->
thresholdle pikselako chamak chhutyaunchha; yo kshetraphalako sart hoina. mahattwapurna cell chalaunuaghi input,
kaam ra natija ek-ek bakyama lekhnuhos. pahile anuman garera chalaunuhos ra maan wa chitra hernuhos.
ulto threshold matra badaler feri anuman gari chalaunuhos. janajan rakhieka truti ra nasakieka abhyaska
nirdeshan pachhyaunuhos.

<!-- ne-cell: be632326 | after-heading -->
## Part 0 tayari

<!-- ne-cell: e15c580c | after-heading -->
**OpenCV ko rangako kram ma dhyan dinuhos**
<!-- ne-pair: Watch out for OpenCV's colour order -->

<!-- ne-cell: e15c580c -->
OpenCV le rang **BGR** (nilo, hariyo, rato) kram ma rakhchha. `cv2.imread()` le padheko array BGR hunchha.
Matplotlib le **RGB** (rato, hariyo, nilo) kram ma dekhaunchha.

BGR array tyasai `plt.imshow()` ma dinda rato ra nilo satiera dekhinchha. **BGR array dekhaunuaghi badalnuhos.**

`cv2.cvtColor()` le **nayan array pharkaunchha**; `image_bgr` aphain badalindain.

**kahile badalnuparchha?** **BGR array** ma matra. yi pahile nai RGB hun, badalnu pardaina:

- `PIL.Image.open(...)` le kholeko tasbir (bastabik rangako sandarbha photo sahit)
- scikit-image jasta laibrerika RGB array

ulto, RGB array lai `COLOR_BGR2RGB` le badalda rang satinchha. **"yo array BGR ho ki RGB" pahile jaanchnuhos.**

yo talimabhari **dekhauna Matplotlib, prashodhan OpenCV** bhanne niyam rakhinchha. `cv2.imshow()` Jupyter ma
adkin sakne hunale prayog garindain.

<!-- ne-cell: clarity-bgr-predict | after-heading -->
#### anuman: rato kina nilo banchha?

<!-- ne-cell: clarity-bgr-predict -->
input eutai sansleshit BGR patti ho. bayan galtile RGB maner dekhaieko chha, dayan badalepachhiko. chalaunuaghi
bayan chheuko rang anuman garnuhos. yo model ko anuman wa photo hoina.

<!-- ne-cell: clarity-bgr-interpret -->
bayan chheuko uhi maan `[0,0,255]` BGR ma rato ho, RGB ma dekhaunda nilo hunchha. `cvtColor` le chyanalako kram
badalchha. bichako hariyo kina nabadaliyo byakhya garnuhos, tyaspachhi bayan patti `[0,255,255]` banaera anuman garnuhos.

<!-- ne-cell: d0b1221a | after-heading -->
## Part 1 tasbir padhne ra surakshit garne

<!-- ne-cell: a2bfa0aa | after-heading -->
**tin adharabhut kaam**
<!-- ne-pair: The three basic operations -->

<!-- ne-cell: a2bfa0aa -->
| kaam | function | pharkaune maan |
|---|---|---|
| padhne | `cv2.imread(path)` | NumPy array (BGR). asaphal bhae `None` |
| dekhaune | `plt.imshow(...)` | — |
| surakshit garne | `cv2.imwrite(path, image)` | saphal bhae `True`, asaphal bhae `False` |

> `cv2.imread` le **file nabhaema truti hoina, `None` pharkaunchha**. sadhain `None` ho ki hoina jaanchnuhos.
> nayan sikneharule sabaibhanda dherai yahi kura chhutaunchhan.

`cv2.imwrite` pani **truti hoina, `False`** pharkaun sakchha. `False` ko karan eutai hundaina.

| `False` ko karan | ke jaanchne |
|---|---|
| surakshit garne folder chhaina | pahile `output_dir.mkdir(parents=True, exist_ok=True)` chalaiyo? |
| lekhne anumati chhaina | tyo folder ma lekhna milchha? (read-only, sajha folder, administrator adhikar) |
| extension ra dhancha mildaina | `.png` / `.jpg` jasta extension le tyo dhancha rakhna sakchha? (16 bit tasbir `.jpg` ma rakhnu) |
| bato galat | nachalne akshar, atyadhik lamo bato |

<!-- ne-cell: fcc102a2 | after-heading -->
**surakshit garne**
<!-- ne-pair: Saving -->

<!-- ne-cell: fcc102a2 -->
`cv2.imwrite` le surakshit garchha. surakshit garne folder **pahile banaisaknuparchha**.

`cv2.imwrite` asaphal hunda `False` pharkaunchha (truti hoina). **pharkaeko maan sadhain jaanchnuhos**; `False`
ae folder chha ki chhaina, lekhne anumati chha ki chhaina, ra extension ra tasbir dhancha milchha ki mildaina kramaisang hernuhos.

yo talim ma **mul samagri nabigarna** natija `submissions` bhitra surakshit garinchha.

<!-- ne-cell: 7355da79 | after-heading -->
## Part 2 greskel ra bainarikaran

<!-- ne-cell: audit-teach_opencv_pixel_pipeline | after-heading -->
### kod kasari padhne

<!-- ne-cell: audit-teach_opencv_pixel_pipeline | after-image:../../assets/svg/teach_opencv_pixel_pipeline.svg -->
chitra: chamakako threshold ra kshetraphalako sart farak hun. (ganana garieko sansleshit udaharan ra yojanabaddha chitra;
model ko bastabik napieko natija hoina.)

**dhyan dinuparne kura**

chamakako threshold ra kshetraphalako sart farak hun. input ra paribartan bhaeko maan aunlale pachhyaunuhos.

**sochnuhos**

pikselako maan threshold sang thyakkai barabar hunda ulto maskama ke hunchha?

<!-- ne-cell: be0db14f | after-heading -->
### mul tasbir → mask (agrabhag) → kantur

<!-- ne-cell: be0db14f | after-image:../../assets/diagrams/teach_opencv_pipeline.png -->
chitra: uhi sansleshit tasbir prashodhan gareko bastabik natija (sansleshit tasbir, bastabik ganana). pyanal ②
`THRESH_BINARY_INV` (T=150) ko mask **aphain** ho: 150 wa kam maan bhaeka piksel seta (agrabhag), 150 bhanda
badhi bhaeka kala (prishthabhumi). pyanal ③ le tyahi maskabat nikaleko kantur mul tasbir ma rakheko dekhaunchha.

**dhyan dinuparne kura**

tinabatai pyanal **eutai** tasbir baat baneka hun. yahan mahattwapurna kura **threshold** ra `findContours` ma
diine **maskako dhrubata (polarity)** ho.

yo notebookle `cv2.THRESH_BINARY_INV` prayog garchha, tyasaile mask yasto hunchha:

| greskel maan | maskako maan | dekhine rup |
|---|---|---|
| threshold **wa kam** (`g <= T`) | 255 | seto (**agrabhag**: `findContours` le khojne piksel) |
| threshold **bhanda badhi** (`g > T`) | 0 | kalo (prishthabhumi) |

arthat **gadha dosh jati seto** dekhinchha. pyanal ② ma dekhaieko mask nai **`findContours` ma diine array** ho.
seto agrabhagako kinara pachhyaun yahi dhrubata chahinchha; ulto dhrubata diiyo (gadha piksel kalai chhodiyo) bhane
tasbirko bahiri phremalai kantur thanchha.

**sochnuhos**

- threshold badhaunda kantur badhchha ki ghatchha? yo sansleshit tasbir ma sanchchai ke hunchha, talako sweep chitra ma hernuhos.

<!-- ne-cell: clarity-mask-predict | after-heading -->
#### eutai sano tasbir: piksel → mask → kantur

<!-- ne-cell: clarity-mask-predict -->
sansleshit 7×8 tasbirko bichako 3 line × 4 stambha gadha banainchha. T=100 ko ulto bainarikaranama barabar pani seto
hunchha. anuman: seta pikselako sankhya ra piksel kendra joder banne kanturako kshetraphal barabar hunchha?

| g / piksel maan | 40 | 99 | 100 (=T) | 101 |
|---|---|---|---|---|
| ulto mask | 255 | 255 | 255 | 0 |

<!-- ne-cell: clarity-mask-interpret -->
seta piksel 3×4 = 12 bata hunchhan, tar kantur piksel kendrabich chaudai 3 × uchai 2 = 6 px² matra hunchha.
kanturako kshetraphalalai "seta pikselako sankhya" bhannu hundaina. gadha bhaagko stambha antya 6 baat 7 banaunda dubai
kati hunchhan? pachhi aune 2→1→18 ko chitra ma, thresholdle dui kshetra jodine kura ra arko abaj (noise) kshetra
dekha parne kura chhuttachhuttai padhnuhos.

<!-- ne-cell: fbc7ce1c | after-heading -->
**greskel banaune**
<!-- ne-pair: Converting to greyscale -->

<!-- ne-cell: fbc7ce1c -->
**yo abhyas jastai "gadha dosh lai chamakale bhetne" abastha** ma rangako jankari prayah prayog hundaina. chamak matra
rakhda ganana chhito ra sajilo hunchha. tar **rang aphain asamanya** (rang bigrinu, dadheko dag, bahiri padarthako rang) bhae
rang rakhnaiparchha.

`gray` dui-ayamik (uchai, chaudai) array hunchha. yo paribartan **tin chyanal (BGR) array** ma garinchha. pahile
nai ek chyanal bhaeko greskel tasbir (bastabik sandarbha photo jastai) tyasai prayog garna sakinchha, badalnu pardaina.

<!-- ne-cell: eb10df2a | after-heading -->
**bainarikaran (threshold garne)**
<!-- ne-pair: Thresholding -->

<!-- ne-cell: eb10df2a -->
bainarikaranale **threshold sang tulna garera pratyek pikselalai dui maan (0 ra 255) ma badalchha**. kun patti seto
hune bhanne kura chhanieko bidhile (`THRESH_BINARY` wa `THRESH_BINARY_INV`) tay garchha.

**threshold sang thyakkai barabar piksel "wa kam" ma parchha.** talika hernuhos.

| mul chamak | `THRESH_BINARY` | `THRESH_BINARY_INV` |
|---|---|---|
| thresaholdabhanda badhi (`g > T`) | 255 (seto) | 0 (kalo) |
| thyakkai threshold (`g == T`) | 0 (kalo) | 255 (seto) |
| thresaholdabhanda kam (`g < T`) | 0 (kalo) | 255 (seto) |

yo notebook ma **gadha dosh lai seto agrabhag** banaunu chha, tyasaile `THRESH_BINARY_INV` prayog hunchha. yasle
pachhiko "kantur khojne" kaam lai "seto bhaag khojne" bhanne saral rupama badalchha. `findContours` ma yahi seto
agrabhagako mask **aphain** diinchha.

`cv2.threshold` le **nayan array pharkaunchha**, tyasaile input `gray` (mul tasbir) badalindain. threshold
badalda mul tasbir uhi rahanchha, badaline mask matra ho.

yahan threshold **manchhele chhaneko sthir maan (150)** ho. OpenCV ma `cv2.THRESH_OTSU` (tasbir baat euta maan
sbatah) ra `cv2.adaptiveThreshold` (thaun-thaun ma farak) pani chhan, tar "yo natija thik chha ki chhaina" bhanera manchhele
jaanchne kaam sadhain banki rahanchha.

<!-- ne-cell: fdc17f13 | after-heading -->
**threshold badalda ke badlinchha**
<!-- ne-pair: What changes with the threshold -->

<!-- ne-cell: fdc17f13 -->
threshold **manchhele tay garne sankhya** ho. yahi nai tasbir prashodhanako kathinai ho.

yo bhaagko prayog **niyantrit prishthabhumima bhaeko gadha dag** ka lagi ho ra threshold **hataile chhanieko** chha.
ujyalo wa prishthabhumi farak bhae tyahi maan uttam hunchha bhanne chhaina.

- threshold **badhaunda** (jastai 200) → "gadha" thanine dayara pharakilo hunchha → prishthabhumiko asamanata pani
  agrabhagama parchha, **jhuto alarm badhchha**
- threshold **ghataunda** (jastai 60) → agrabhag ghatchha → halka dosh banki rahandain, **chhutne (miss) badhchha**

**threshold T le badaline ra nabadaline kura**

| T le badlinchha | T le badalindain |
|---|---|
| bainari mask (agrabhagako dayara) | mul tasbir ra greskel tasbir |
| agrabhagaka pikselako sankhya | calibration maan (px/mm) ra khichaiko abastha |
| kanturako sankhya ra kshetraphal | tasbirko akar (piksel sankhyako sima) |

<!-- ne-cell: fig-teach_threshold_sweep | after-heading -->
### threshold ghumaera ganne

<!-- ne-cell: fig-teach_threshold_sweep | after-image:../../assets/diagrams/teach_threshold_sweep.png -->
chitra: yo sansleshit tasbir ma threshold badalda seto agrabhag ra external contour sankhya kati hunchha
(napieka maan). tasbir chai eutai ho; badalne kura threshold matra ho.

<!-- ne-cell: fig-teach_threshold_sweep -->
**yo chitra kasari padhne.** mathiko hangama eutai grayscale tasbir chaar patak dekhaieko chha. input
badaldaina; badalne kura threshold T matra ho. `cv2.THRESH_BINARY_INV` ma **I ≤ T bhae seto (255) =
chhanieko agrabhag**, ra **I > T bhae kalo (0) = chhodine prishthabhumi**. tallo graph A le seto piksel
ganchha, graph B le `cv2.RETR_EXTERNAL` le paeka external contour ganchha. dui ota chhuttai graph ma
rakhieko chha: eutai graph ma dui wota thado aksh hald a galat padhine hunchha.

**1. T = 100 ra T = 160 le kina eutai mask dinchhan?** yo tasbirka piksel maan dherai jaso dui
samuha ma chhan: karib 40 (kalo thoplo) ra 189–218 (sheet). T 40–180 bichama rakhda I ≤ T ma parne
kalo thoplo matra ho. tyasaile T = 100 ra T = 160 duitai ma seto hune kshetra eutai 249 px ho.
**natija eutai hune karan: input eutai ho ra ti dui threshold bichama kunai piksel maan chhaina** —
threshold le farak pardaina bhanne hoina.

**2. T = 210 ma kina tasbirko dherai bhaag seto hunchha?** sheetko piksel maan 189–218 hun. T = 210
gard a tyasbhitraka dherai piksel I ≤ T kharcha. tyasaile 40,000 px madhye 36,677 px (91.7 %) seto
hunchha. tyahan chhanieko kura dosh hoina, **sheet aphai** ho.

**3. baki raheka kalo bhaag kina agrabhag ma ganieko chhaina?** I > T hune piksel 0 (kalo) nai
rahanchha. kalo bhaneko "ramro" hoina, **"nachhanieko"** ho. T = 210 ko seto kshetra bhitra raheka
sano kalo thopla T bhanda ujyalo piksel hun. ganieko kura seto piksel matra ho.

**4. seto piksel badhda pani external contour sankhya kina nabadhna sakchha?** `cv2.RETR_EXTERNAL` le
seto kshetrako **bahirako kinara** matra ganchha. seto kshetra failiera arko sang jodida dui kinara
euta hunchha. yo tasbir ma T = 200 le 12,634 px ra 320 contour, T = 210 le 36,677 px ra **49**
contour dieko thiyo. piksel badhe pani contour ghatyo. ulto, T = 190 ma prishthabhumi ko mura seto
bhaera 46 pugyo. **graph A kahilyai ghatdaina; graph B badhchha ra ghatchha.**

**5. external contour nai dosh ho?** hoina. external contour bhaneko "seto kshetrako bahirako kinara"
matra ho, dosh hunu aniwarya chhaina. prishthabhumi ko mura, reflection, dhulo ra chhaya le pani
banchha (T = 210 ko 49 contour madhye dherai mura hun). sathai euta dosh dui contour ma
chhutin sakchha, ra pwal bhaeko dosh bahirako kinara le matra ganinchha. **contour sankhya "doshko
sankhya" hoina.**

**6. PVC nirikshan ma aru kun filter chahinchha?** jastai:

| filter | ke hataunchha |
|---|---|
| nyoonatam kshetraphal / minimum area | dherai sano, noise jasto kshetra |
| akar (golopan, lamapan) / shape | mura ra dharki lai thoplo bhanda chhuttaune |
| wari-pari ko ujyalo farak / local contrast | ujyalo ko asamanata le baneka jhuto dosh |
| sthan (nirikshan kshetra) / region of interest | utpadan baahirako naksha |
| morphology | euta dosh dui ma chhutieko wa pwal bhaeko |
| calibration (px/mm) | px lai mm² ma badalna |

**sano sankhya udaharan.** yo tasbir 200 × 200 = 40,000 px ho. T = 100 ma seto 249 px, arthaat
249 ÷ 40,000 = 0.62 %. T = 210 ma 36,677 ÷ 40,000 = 91.7 %. din 2 ko calibration 2.00 px/mm
prayog garda 1 px = 0.5 mm ra 1 px² = 0.25 mm² hunchha, tyasaile 249 px = 249 × 0.25 =
**62.25 mm²**, ra 36,677 px = **9,169 mm²**. **piksel sankhya lai mapadand sang tulna garna
sakindaina**; calibration garepachhi matra mm² hunchha.

**sochnuhos ra anuman garnuhos**

- threshold badhda seto piksel badhchha ki ghatchha?
- threshold badhda external contour sankhya badhchha ki ghatchha? yo chitra ko T = 200 ra T = 210
  herera uttar dinuhos.

<!-- ne-cell: fig-camera | after-heading -->
### bastabik greskel photoma prayas garne

<!-- ne-cell: fig-camera | after-image:../../assets/external_samples/open_reference/camera.png -->
photo: bastabik greskel tasbir (scikit-image `camera`, Lav Varshney, CC0 1.0). 0–255 ko ek chyanal, yo
talimka sansleshit tasbirabhanda jatil.

**dhyan dinuparne kura**

ujyaloko asamanata, chhaya ra prishthabhumiko butta sabai 0–255 ko sankhya banchhan. yahan seto agrabhag bhaneko
"dosh" hoina, "thresaholdabhanda gadha piksel" matra ho. yo photoma utpadanako kunai dosh chhaina.

**sochnuhos**

- threshold 100 rakhda yo photoma kahan-kahan seto rahanchha? pahile anuman garera chalaunuhos.

<!-- ne-cell: fig-brick | after-heading -->
### butta bhaeko prishthabhumima ganne tarika badlinchha

<!-- ne-cell: fig-brick | after-image:../../assets/external_samples/open_reference/brick.png -->
photo: intako parkhal (CC0Textures, scikit-image le prashodhan gareko, CC0 1.0). butta dohorine prishthabhumiko
udaharan. yo samanya butta ho, dosh hoina.

**dhyan dinuparne kura**

butta dohorine prishthabhumima euta threshold tay garda **buttaka bhaagharu samuhik rupama** agrabhag banchhan.
tyasaile kantur sankhya "doshko sankhya" hoina, "gadha kshetrako sankhya" ho. samanya bhinnata pahile thaha
paunu nai dosh pahichanko surubat ho.

**sochnuhos**

- yo photoma threshold badhaundai janda seto agrabhagako kshetraphal badhchha ki ghatchha?

<!-- ne-cell: c342c62c | after-heading -->
**baikalpik abhyas: bastabik photoma thresholdko sima herne**
<!-- ne-pair: Optional: the limits of one threshold on real photographs -->

<!-- ne-cell: c342c62c -->
mathika dui photo **samanya photo** hun, doshko photo hoinan. tyasai pani euta threshold tay garda "gadha
piksel" samuhik rupama agrabhag banchha. chhaya, butta ra ujyaloko asamanata agrabhagama parne kura jaanchnuhos.
yo abhyas **baikalpik** ho (sampannata janchasuchiko aniwarya bunda hoina).

**garnuparne kaam (baikalpik)**

1. mathiko **greskel sandarbha photo** padher threshold 100 ma `THRESH_BINARY_INV` lagaunuhos.
2. kahan seto rahanchha **pahile anuman** garera chalaera jaanchnuhos.
3. tyaspachhi **butta bhaeko sandarbha photo** ma uhi kaam garera agrabhag "dosh" hoina "gadho butta" baneko dekhnuhos.

fileko naam mathiko chitrako Markdown lingk (koshthakabhitrako bato) batai lekhnuhos.

**dhyan dinuparne kura**

- agrabhagaka pikselako sankhya tasbir ra thresholdle tay garchha. **yo bhautik kshetraphal (mm²) hoina.**
- kantur sankhya "gadha kshetrako sankhya" ho, "doshko sankhya" hoina.
- ujyalo ra butta farak bhaeka tasbir lai eutai sthir thresholdle ustai byabahar garna sakindaina. tyasaile
  **samanya dekhine rup pahile thaha paunu** dosh pahichanko surubat ho.

**sochnuhos:** seto agrabhag sadhain dosh ho?

<!-- ne-cell: 4a6c53f8 | after-heading -->
#### threshold sardai mul tasbir, mask ra kantur sangai herne

<!-- ne-cell: 4a6c53f8 -->
bayanko mul tasbir threshold badalda pani badalindain. threshold T badalda bichako bainari mask badlinchha ra
dayanko kantur tyahi maskabat feri ganana hunchha. bichama dekhaieko mask `findContours` ma diieko array kai ho.

| anuman | ke herne |
|---|---|
| threshold badhaunda | seto kshetraphal badhchha? ghatchha? |
| kantur sankhya | badhchha? ghatchha? |
| threshold 0 | mask sabai seto? sabai kalo? |

widget nabhae pani talako parameter cellle uhi prayog garna dinchha.

<!-- ne-cell: 8af2cdb3 | after-heading -->
## Part 3 kantur khojne

<!-- ne-cell: 77680506 | after-heading -->
**kantur bhaneko "seto bhaagko kinara"**
<!-- ne-pair: A contour is the boundary of a white region -->

<!-- ne-cell: 77680506 -->
`cv2.findContours` le bainari tasbirko **seto bhaagko kinara (kantur)** bhetchha. pharkaune kura kinara pachhyaera
baneka binduharuko kram ho. kantur "kshetra aphain" hoina, "agrabhagaka piksel ganeko abhilekh" pani hoina.

| argument | arth |
|---|---|
| `cv2.RETR_EXTERNAL` | sabaibhanda bahiri kantur matra pharkaune |
| `cv2.CHAIN_APPROX_SIMPLE` | kanturaka bindu ghataera halka banaune |

pratyek kanturabat yi jankari painchhan.

| function | paine kura |
|---|---|
| `cv2.contourArea(c)` | kanturale ghereko akritiko kshetraphal (piksel² ekaiko jyamitiy kshetraphal) |
| `cv2.boundingRect(c)` | bahirabat gherne ayat (x, y, w, h) |
| `cv2.moments(c)` | gurutbakendra ganana garna prayog hune maan |

`cv2.contourArea` kinaraka bindubat ganana garieko **akritiko kshetraphal** ho. agrabhagaka piksel ganeko sankhya sang
sadhain mildaina (patalo akar ra kinarako byabaharale badalchha). sathai yo **piksel²** ho, mm² hoina. mm² banaun
calibration ra Part 5 ma bhanieka sart chahinchha.

<!-- ne-cell: fig-teach_contour_merge | after-heading -->
### jodinda sankhya ghatchha

<!-- ne-cell: fig-teach_contour_merge | after-image:../../assets/diagrams/teach_contour_merge.png -->
chitra: najikaka dui dosh, threshold badhaunda 2 kshetra → 1 kshetra → 18 kshetra (prishthabhumiko abaj) hune
udaharan (sansleshit tasbir, bastabik ganana).

**dhyan dinuparne kura**

kantur kshetrako **kinara** janaune binduharuko kram ho; agrabhagaka piksel wa tinako sankhya hoina. najikaka
kshetra jodinda kantur sankhya ghatchha. kshetraphalama `contourArea` (kanturako jyamitiy kshetraphal) ra agrabhagaka
piksel ganne tarika chhuttyaunuhos.

**sochnuhos**

- dui dag patalo rekhale jodie kantur sankhya ke hunchha?

<!-- ne-cell: 5a58ab0d | after-heading -->
## Part 4 dui bindubichako duri

<!-- ne-cell: 3340cb70 | after-heading -->
**pahile chitra ma sochaun**
<!-- ne-pair: Think with a picture first -->

bindu A ra B bichako duri nikalnu chha bhanaun. tasbir ma A baat B samm sidha napna gahro hunchha.

tyasaile **samakon tribhuj** banainchha.

1. tirso farak: `dx = x2 - x1`
2. thado farak: `dy = y2 - y1`
3. tirso lambai (arthat duri) paithagorasako niyamle niskanchha

yahan paine duriko ekai **px (piksel)** ho. mm ma badalna Part 5 ko calibration chahinchha.

<!-- ne-cell: fig-teach_distance_345 | after-heading -->
### dui binduko duri karna ho

<!-- ne-cell: fig-teach_distance_345 | after-image:../../assets/diagrams/teach_distance_345.png -->
chitra: dx=300, dy=400, duri=500 px bhaeko samakon tribhuj (sabai ganana garieka maan).

**dhyan dinuparne kura**

duri "dx ra dy dubaiko barg garera jodne, tyaspachhi bargamul nikalne" tarikale painchha. 3-4-5 bhaneko tyo ganana
purnank ma aune udaharan ho. px ma paieko duri lai mm banaun calibration (px/mm) chahinchha.

**sochnuhos**

- dx = 6, dy = 8 hunda duri kati px hunchha?

<!-- ne-cell: 1c601d07 | after-heading -->
**sutrako arth**
<!-- ne-pair: What the formula means -->

<!-- ne-cell: 1c601d07 -->
sutra ek lineko matra ho: `duri = √( dx² + dy² )`.

`dx²` bhaneko "dx ko barg", `√` bhaneko "bargamul". **dx ra dy dubaiko barg garne, jodne, tyaspachhi bargamul nikalne.**
Python ma `** 0.5` wa `math.sqrt` prayog garnuhos.

> "barg garne, jodne, bargamul nikalne" — yatti matra. sutra kanth garnu pardaina. **samakon tribhujako karna**
> nikalieko matra ho.

paine duriko ekai **px** ho (pikselabichako duri, bhautik lambaiko ekai hoina). mm banaun calibrationko
gunakale gunan garnuparchha.

<!-- ne-cell: daed0037 | after-heading -->
### natijako udaharan

<!-- ne-cell: 6fa3f5d0 | after-heading -->
**3-4-5 ko jaanch**
<!-- ne-pair: Verifying 3-4-5 -->

<!-- ne-cell: 6fa3f5d0 -->
`(0,0)` ra `(3,4)` bichako duri **5** ho: `3² + 4² = 9 + 16 = 25`, `√25 = 5`. ganana milyo.

<!-- ne-cell: 00f34871 | after-heading -->
## Part 5 pikselalai milimitarama badalne

<!-- ne-cell: b78a5571 | after-heading -->
### pikselalai milimitar banaune

<!-- ne-cell: b78a5571 | after-image:../../assets/diagrams/teach_pixel_to_mm.png -->
chitra: sandarbha lambai 100 px = 50.0 mm baat gunak 2.00 px/mm nikaler 200 px chaudailai 100.0 mm ma badaleko
udaharan. kinarako sthanama manieko anishchitata (±0.5 px ÷ 2.00 px/mm = ±0.25 mm) pani tyahi chitra ma chha.

**dhyan dinuparne kura**

gunak "sandarbha lambai kati px ma kati mm ho" baat niskanchha. gunak tay bhaepachhi bhaag garne matra. **ekai sadhain
lekhnuhos.** chitra ma kinarako anishchitata ±0.5 px maner ±0.25 mm ma badalieko chha. yo napako shuddhatako
gyarenti hoina.

**yo chitra eutai samatalama garieko paribartanako udaharan ho.** sandarbha lambai ra napne lambai eutai samatalama chhan,
lensako bikriti sano chha ra gunak dekhine kshetrabhari sthir chha bhanne poorwashart chha. bastabik napama
**dherai sthan ra disha** ma janchnuparchha ra bikritiko sudhar (wa kshetra-dar-kshetra calibration) pani chahinchha.

**sochnuhos**

- uhi bastabik 50.0 mm sandarbha, zoom garda 240 px ma dekhiyo. gunak kati px/mm hunchha? tyasabela uhi 1 px
  truti mm ma thulo hunchha ki sano?

<!-- ne-cell: b877b171 | after-heading -->
**calibration kina chahinchha**
<!-- ne-pair: Why calibration is necessary -->

<!-- ne-cell: b877b171 -->
tasbirko duri **piksel** ma napinchha, tar karyasthalama **milimitar** chahinchha.

uhi 100 mm ko bastu kyamera tadha hunda **sano**, najik hunda **thulo** dekhinchha. arthat "ek piksel kati mm
ho" bhanne kura **kyamera ra bastuko sthiti** le tay garchha.

tyasaile **lambai thaha bhaeko bastu** (sandarbha skel) uhi drishyama rakher piksel ra mm ko anupaat nikalinchha.
yas lai **calibration** bhaninchha.

udaharan: `px_per_mm = sandarbhako piksel lambai ÷ sandarbhako bastabik lambai (mm)` ra
`mm_per_px = sandarbhako bastabik lambai (mm) ÷ sandarbhako piksel lambai`.

<!-- ne-cell: deffde3a | after-heading -->
**calibrationko sochai dekhaune chitra**
<!-- ne-pair: The idea of calibration -->

<!-- ne-cell: deffde3a -->
talako chitrale **uhi 100 mm sandarbha** kyamerako duri anusar kati pikselama dekhinchha dekhaunchha.

- tadha: 100 mm = 120 px → **1.20 px/mm**
- najik: 100 mm = 240 px → **2.40 px/mm**

arthat calibration maan **tyahi khichaiko abastha ma matra** chalchha. kyamera sariyo bhane **feri
calibration garnaiparchha**.

**dui farak kaam namisaunuhos.**

- **sandarbha aphain dobbar lambaiko banaune** (100 mm → 200 mm): bastabik lambai badlinchha, tar gunak (px/mm) uhi rahanchha.
- **zoom garera sandarbha dekhine piksel sankhya matra dobbar banaune** (120 px → 240 px): bastabik lambai
  100 mm nai hunchha, tyasaile gunak (px/mm) dobbar hunchha.

calibrationle badalne kura "ek px kati mm ho" bhanne matra ho. kun kaam gariyo bhanera sadhain chhutyaunuhos.

<!-- ne-cell: e3c33e34 | after-heading -->
**naper herne**
<!-- ne-pair: Measure something -->

<!-- ne-cell: e3c33e34 -->
calibration maan prayog garera dui bindubichako duri mm ma nikalinchha: `duri(mm) = duri(px) × mm_per_px`.

talako cellle pahile calibration tasbirko sandarbha rekhaka dui chheu naper **100 mm mai pharkinchha ki** janchchha.
tar yo "gunak nikalekai rekhalai uhi gunakale feri napeko" matra ho, tyasaile **gananako jaanch** matra hunchha,
napako shuddhatako praman hoina.

tyasaile calibration ma naprayog garieko **thado jaanch rekha (50 mm)** pani napinchha. arko sthan, arko dishako
rekha 50 mm mai pharkiyo bhane **yo sansleshit tasbirbhitra paribartan ekanasale chaleko** sbatantra praman banchha.

**yo jaanchle bhanna sakne ra nasakne kura**

- bhanna sakne: yo tasbirbhitra eutai gunakale arko rekhalai pani sahi mm ma badalyo (**paribartanako ekanasatako jaanch**).
- bhanna nasakne: dekhine kshetrako chheu, bibhinna disha wa bibhinna duri ma pani uhi shuddhata hunchha bhanne. dubai rekha
  **eutai samatal** ma, **tasbirko akshasang samanantar** banaieka adarsh akar hun.

bastabik napama **dherai sthan ra disha** ma jaanch garinchha ra lensako bikriti tatha satahako dhalkai pani sochinchha.

<!-- ne-cell: 3c3e557c | after-heading -->
### natijako udaharan

<!-- ne-cell: 3c3e557c -->
yi dui rekha dubai sansleshit tasbir ma banaieka adarsh akar hun. truti thyakkai 0 hunuko karan piksel nirdeshangk
purnank ma diieko ra rekha tasbirko akshasang samanantar bhaeko ho. bastabik photoma piksel syampaling,
kinarako sthan anuman (subpixel) ra lens bikritile truti nimtyaunchhan.

<!-- ne-cell: 87c3a290 | after-heading -->
**eutai gunak prayog garna milne sart**
<!-- ne-pair: When one scale factor is valid -->

<!-- ne-cell: 87c3a290 -->
"eutai px/mm le purai napne" kaam yi sart pura bhae matra milchha.

| sart | napuge ke hunchha |
|---|---|
| kyamera sitako satahasang **sidha (perpendicular)** chha | tirso bhae thaun anusar skel badlinchha |
| lens bikriti sano (wa sudharieko) | tasbirko chheutir truti badhchha |
| sit samatal chha ra kyamerabat **uhi duri** ma chha | uthne wa phulne bhaag ma skel badlinchha |
| dekhine kshetrabhari gunak sthir chha | pharakilo-kon (wide) lensama chheutir skel badlinchha |

**pharakilo-kon lens bhae pani calibration garieko nap sambhab chha.** bikriti thulo bhae sudhar prayog garnuhos
(`cv2.calibrateCamera` le gunak nikaler `cv2.undistort` le sudharne) wa **kshetra-dar-kshetra calibration**
garera sthaniy gunak prayog garnuhos. namilne kura bhaneko "sudhar nagari eutai gunak purai drishyama lagaunu" ho.

arthat **calibration nagarieko tasbirko nap sahi chha bhanna mildaina**. "pikselama napen" bhanne matrale mm ko
kunai gyarenti dindain.

<!-- ne-cell: 5078b3fb | after-heading -->
## abhyas

<!-- ne-cell: audit-same-plane-intro | after-heading -->
### eutai samatalako sandarbha ra lakshya

<!-- ne-cell: audit-same-plane-intro -->
lambaiko paribartan janchepachhi, chhuttai calibration bhaeko eutai-samatalako dosh drishy prayog garinchha. nilo sandarbha
rekha threshold 80 ma agrabhagama pardaina. yo sansleshit tasbirko kodabat gunak 1.2 px/mm, sbatantra jaanch 50 mm,
kantur kshetraphal 475 / 925 px² ra agrabhagaka piksel 1508 painchha.
abhyasko sutra pura garda jaanchne ganana: 475 px² → 329.861111 mm², 925 px² → 642.361111 mm².

<!-- ne-cell: clarity-scale-equations | after-heading -->
#### pahile ekaiko sutra

<!-- ne-cell: clarity-scale-equations -->
`px_per_mm = reference_length_px / reference_length_mm`

`measured_mm = measured_px / px_per_mm`

`area_mm2 = area_px2 / (px_per_mm ** 2)`

eutai samatalako sansleshit udaharan ma 120 px / 100 mm = 1.2 px/mm, ra sbatantra 60 px le 50 mm dinchha. 475/925 px²
ka kantur karib 329.861/642.361 mm² hunchhan. anuman: gunak matra dobbar bhae badalieko kshetraphal kati hunchha?
yo napako shuddhatako pramanapatra hoina; samatal, heraiko kon ra lens bikriti pani jaanchnuhos.

<!-- ne-cell: audit-teach_calibration_same_plane | after-heading -->
### kod kasari padhne

<!-- ne-cell: audit-teach_calibration_same_plane | after-image:../../assets/svg/teach_calibration_same_plane.svg -->
chitra: sandarbha rekha ra lakshya eutai tasbir, eutai samatalama chhan. (ganana garieko sansleshit udaharan ra yojanabaddha chitra;
model ko bastabik napieko natija hoina.)

**dhyan dinuparne kura**

sandarbha rekha ra lakshya eutai tasbir, eutai samatalama chhan. input ra paribartan bhaeko maan aunlale pachhyaunuhos.

**sochnuhos**

gunak dobbar maniyo bhane uhi px² ko mm² kati guna hunchha?

<!-- ne-cell: 2e70399c | after-heading -->
**abhyas 1 (adharabhut): eutai tasbirko kantur kshetraphal mm² ma badalne**
<!-- ne-pair: Exercise 1 (basic): convert areas from the same calibrated image -->

<!-- ne-cell: 2e70399c -->
talako cell ma Part 3 ko `kept` hoina, mathiko calibration bhaeko tasbirko `calibrated_contours` prayog hunchha.
Part 3 ko `defect_multi.png` ma arko tasbir baat paieko gunak lagaunu hundaina. sanket: `area_px2` lai
`calibrated_px_per_mm ** 2` le bhaag garnuhos. kanturako jyamitiy kshetraphal ra agrabhagaka piksel sankhya
farak hun. bargakar piksel, uhi bastu-samatal, sidha herai (wa sudharieko perspective), sano lens bikriti ra
sandarbha rekhako anishchitata pani jaanchnuhos. yo adarsh sansleshit drishy ho.

**sakieko manine abastha:** dubai kanturako kshetraphal px² ra mm² dubaima dekhaieko chha.

<!-- ne-cell: 73d9d23e | after-heading -->
**abhyas 2 (madhyam): threshold badaler kantur sankhya tulna garne**
<!-- ne-pair: Exercise 2 (intermediate): compare contour counts for several thresholds -->

<!-- ne-cell: 73d9d23e -->
threshold 100 / 150 / 180 / 200 badaler **bhetieka kanturako sankhya** ra **sabaibhanda thulo kanturako kshetraphal**
talika ma rakhnuhos. kun maanle "dosh matra" samatchha? karan pani lekhnuhos.

<!-- ne-cell: e7f5ac65 | after-heading -->
**abhyas 3 (baikalpik): napako trutibare sochne**
<!-- ne-pair: Exercise 3 (optional challenge): discuss measurement error -->

<!-- ne-cell: e7f5ac65 -->
0.3 mm ko dosh 1 px/mm gunakama napne manaun.

1. 0.3 mm kati piksel hunchha?
2. **pikselako kram sankhya purnank** ho, tar kanturako gurutbakendra wa kinarako sthan **dashamalab
   (subpixel)** ma anuman garna sakinchha. yi dui kurako farak byakhya garnuhos.
3. 0.3 mm lai 3 pikselama samatna kati px/mm wa badhi chahinchha?
4. truti ghataune tin upay bhannuhos (kyamera, ujyalo, calibrationko drishtile).

**saimpaling, subpixel anuman ra anishchitata farak kura hun.** piksel kram sankhya purnank bhae pani sthanako
anuman dashamalabama nikalna sakinchha ra "0.3 px" lai nirantar maanko rupama prayog garna sakinchha. tar harek anuman sang
anishchitata (bikhandan) jodiera aaunchha.

**sakieko manine abastha:** charai uttar lekhieka chhan ra prashna 3 ma sankhya diieko chha.

<!-- ne-cell: 79f73b1f | after-heading -->
#### bujhai jaanchne prashna

<!-- ne-cell: 79f73b1f -->
1. OpenCV ko tasbir ra Matplotlib ko tasbir ma rangako kram kasari farak chha? badalna birse ke hunchha?
2. `cv2.imread` le nabhaeko file padhda truti dinchha?
3. `THRESH_BINARY` ra `THRESH_BINARY_INV` ma ke farak chha? kina dosro prayog gariyo?
4. threshold dherai badhaunda jhuto alarm badhchha ki chhutne badhchha?
5. "calibration nagarieko tasbirko nap bishbas garna mildaina" kina? kyamerako duriko udaharan dinuhos.

<!-- ne-cell: 5889e8ae | after-heading -->
## samasya parema

<!-- ne-cell: 5889e8ae -->
truti aepachhi pahile "kun cell ma", "kun line ma", "ke sandesh ayo" bhanera lekhnuhos. bujhaunuparne kaam ma pani
tyahi abhilekh rakhnuhos.

| lakshan | ke garne |
| --- | --- |
| `image_bgr` `None` hunchha | bato galat chha wa samagri banaiyeko chhaina. `ASSETS / "defect_samples" / "defect_multi.png"` jaanchnuhos. |
| `cv2.imwrite` le `False` pharkaunchha | kramaisang hernuhos: folder chhaina, lekhne anumati chhaina, extension ra dhancha mildaina, bato galat. folder `mkdir(parents=True, exist_ok=True)` le pahile banaunuhos. |
| rang anautho (rato ra nilo satieko) | BGR array ma `cv2.cvtColor(image, cv2.COLOR_BGR2RGB)` lagaun birsieko chha. ulto, pahile nai RGB bhaeko tasbir (PIL le kholeko photo) badalda pani rang satinchha. |
| `findContours` le tin maan pharkaunchha bhaninchha | tyo OpenCV 3 ko jankari ho. OpenCV 4 ma dui maan (contours, hierarchy) pharkaunchha. |
| kantur dherai / abajai abaj | `cv2.contourArea` le sana kantur phalnuhos (jastai 5 px² bhanda kam). threshold ra dhrubata (`THRESH_BINARY_INV`) pani jaanchnuhos. |
| kshetraphalako paribartan milen | kshetraphal `px_per_mm ** 2` le bhaag garinchha (lambai ghat 1, kshetraphal ghat 2). yo sutra piksel bargakar bhae ra bastu kyalibresanakai samatalama bhae matra milchha. |
| tasbirko chheutir nap sarchha (wide lens) | tyo lens bikriti ho. `cv2.calibrateCamera` ra `cv2.undistort` le sudharnuhos wa kshetra-dar-kshetra calibration garnuhos. sudhar garepachhi wide lensama pani calibration bhaeko nap sambhab chha. |
| `ModuleNotFoundError: No module named 'cv2'` | kernel galat chha wa `opencv-python` chhaina. `verify_environment.py` chalaunuhos. |

<!-- ne-cell: 9abd1567 | after-heading -->
## sampannata janchasuchi

<!-- ne-cell: 9abd1567 -->
**aniwarya** ra **baikalpik** kaam chhuttachhuttai chhan. **abhyas 3 (baikalpik)** baikalpik ho; nagare pani pura
maninchha. sabai aniwarya bundama chinh lagepachhi yo notebook pura hunchha.

**aniwarya**

- [ ] Part 1–Part 5 padher sabai code cell chalaen
- [ ] tasbir padher surakshit garne folder ma surakshit garen
- [ ] greskel ra bainarikaranako natija ankhale heren
- [ ] kantur bheter kshetraphal ra bahiri ayat dekhaen
- [ ] dui binduko duri px ma ganana garen
- [ ] px/mm ganana garera mm ma badalen
- [ ] abhyas 1–2 (aniwarya) garen
- [ ] bujhai jaanchne 5 prashnako uttar dien
- [ ] notebook surakshit garen

**baikalpik**

- [ ] bastabik sandarbha photo (greskel ra butta bhaeko) ma thresholdko sima prayas garen
- [ ] abhyas 3 (baikalpik) ka chaar prashnako uttar dien

<!-- ne-cell: d0b2693d | after-heading -->
## thap adhyayan (baikalpik)

<!-- ne-cell: d0b2693d -->
### sandarbha lingk

- [OpenCV adhikarik tutorial](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [cv2.threshold](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html)
- [cv2.findContours](https://docs.opencv.org/4.x/d3/d05/tutorial_py_table_of_contents_contours.html)
- [kyamera calibrationko sochai](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html)

### thap chunauti (aniwarya hoina)

`cv2.adaptiveThreshold` prayas garnuhos. ujyalo asaman bhaeko tasbir ma yasle sthir thresaholdabhanda ramro
natija kina din sakchha, sochnuhos.
