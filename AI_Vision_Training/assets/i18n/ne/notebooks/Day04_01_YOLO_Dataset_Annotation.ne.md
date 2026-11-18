<!--
Nepali anuwad / Nepali translation source for
notebooks/Day04_YOLO_Training/Day04_01_YOLO_Dataset_Annotation.ipynb
-->
# din 4 notebook 01 — Nepali anuwad

<!-- ne-cell: 36dbdec7 | after-heading -->
# din 4 notebook 01: dataset ra label (annotation)

<!-- ne-cell: 36dbdec7 -->
## sikai lakshyaharu

| Nepali |
| --- |
| 1. suparabhaijd larning ma ke-ke chahinchha bataun sakne. |
| 2. YOLO dhanchako sahi label padher arth bataun sakne. |
| 3. samanyikrit nirdeshangk aphain ganana garna sakne. |
| 4. prashikshan, pramanikaran ra parikshanko bhoomika ra chhutyaunuko karan bataun sakne. |
| 5. data chuhabat (data leakage) kina samasya ho bataun sakne. |

## yo notebookko adharabhut jankari

| bishay | biwaran |
| --- | --- |
| sikai samay (anuman) | 80 minet |
| kathinai | surubati tah |
| poorwashart | din 3 sakieko hunuparchha. |
| aawashyak laibreri | numpy, matplotlib, opencv-python, pillow, pandas |
| prayog hune kernel | aivision |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 4](../../COURSE_SYLLABUS.md#day4) |

### bujhaunuparne kaam

| Nepali |
| --- |
| aphno dataset jancheko natija |
| hataile ganana gareko YOLO dhanchako nirdeshangk |

<!-- ne-cell: 94c76861 | after-heading -->
## yo notebook kahan parchha

<!-- ne-cell: 94c76861 -->
| bishay | biwaran |
| --- | --- |
| din | din 4 |
| ajako kram | ajako notabukamadhye 1 / 3 |
| lagne samay | 80 minet |
| poorwashart | din 3 |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 4](../../COURSE_SYLLABUS.md#day4) |

dinko samayatalika `COURSE_SYLLABUS.md` ma eutai thaun ma chha. yo notebook tyasko euta bhaag matra ho.

<!-- ne-cell: audit-learning-loop | after-heading -->
### anuman garnuhos, chalaunuhos, hernuhos, byakhya garnuhos

<!-- ne-cell: audit-learning-loop -->
prashikshan, pramanikaran ra parikshanko bhoomika farak chha, ra khichaiko samuh pani chhutyainchha. mahattwapurna cell
chalaunuaghi input, kaam ra natija ek-ek bakyama lekhnuhos. pahile anuman garera chalaunuhos ra maan wa chitra
hernuhos. bandaphantako ekai matra badaler feri anuman gari chalaunuhos.

<!-- ne-cell: 5c2e0f15 | after-heading -->
## Part 0 tayari

<!-- ne-cell: 761c228b | after-heading -->
**yo detasetabare**
<!-- ne-pair: About this dataset -->

<!-- ne-cell: 761c228b -->
yo talim ma prayog hune dataset **sabai sansleshit tasbir** hun. Python le banaeka "PVC sitajasto"
tasbir hun, bastabik karakhanaka tasbir hoinan.

banaune karyakramalai **chaheko sahi uttar (class ra sthan) pahile nai thaha hunchha**. tar tyo sankhya tasbir ma
tyasai sahi hunchha bhanne chhaina. chitra banaune kram, tasbirko chheuma katinu, nirdeshangk paribartan, tasbirko
akar badalnu, ra karyakramakai bigreko bhaagle label dekhine kurabhanda sarna sakchha. tyasaile **banaiyeko ayat
tasbir ma herer jaanchne** kaam chhodn mildaina.

bastabik bigreko samanama "yo chiso kahan samma ho" bhanne kura manchhele tay garnuparchha ra bichar farak parna sakchha.
label **manchhele banaune, manchheko sahayogama banaune wa karyakramale banaune** junai bhae pani, **labelko gunastar**
tasbirko gunastar, sankhya ra model sangai natija lai asar garchha.

<!-- ne-cell: 8e303ba0 | after-heading -->
## Part 1 suparabhaijd larning

<!-- ne-cell: ebd715a4 | after-heading -->
### natijako udaharan

<!-- ne-cell: ebd715a4 -->
yo natija uhi input ma uhi aaunchha. talimko dataset sthir chha ra sankhya
`assets/yolo_dataset/dataset_summary.json` ma surakshit chhan.

<!-- ne-cell: b2fcf17e | after-heading -->
**"uttar bhaeka udaharan" baat sikne**
<!-- ne-pair: Learning from examples with answers -->

<!-- ne-cell: b2fcf17e -->
**suparabhaijd larning** le **input ra sahi uttarko jodi** dherai patak dekhaer sikaunchha.

`input: sitako tasbir` ra `sahi uttar: yo sthanama kalo thoplo chha (ayat ra class naam)`.

yo "sahi uttar" lai **label (annotation)** bhaninchha.

| shabd | arth |
|---|---|
| label / annotation | tasbirko sahi jankari |
| baunding baks | dosh baripari banaiyeko ayat |
| class label | doshko prakar (kalo thoplo, chiso, dharka) |
| sahi label file | label lai file ma rakhieko rup |

label **manchhele, sahayogasahit wa karyakramale** banaun sakinchha. yo talimko dataset ma banaune karyakramakai
label prayog bhaeko chha. junai tarikale banae pani **galat label model kai galti banchha**: manchheko kaam samay linchha,
sbatah banaiyeko ma chitra banaune wa nirdeshangk paribartanako galti misin sakchha. **tasbirko gunastar, sankhya
ra model sangai labelko gunastarale natijako uchchatam sima tay garchha.**

<!-- ne-cell: e24b5fa4 | after-heading -->
## Part 2 datasetko banabat

<!-- ne-cell: 111d802b | after-heading -->
**YOLO datasetko rachana**
<!-- ne-pair: The YOLO dataset layout -->

<!-- ne-cell: 111d802b -->
YOLO dataset tokieko rachana ma rakhinchha: `images/` bhitra `train/`, `val/`, `test/`, ra `labels/` bhitra pani
tyahi tin folder, sathai `data.yaml`.

mahattwapurna kura **tasbir ra labelko file naam uhi** hunuparchha (extension matra farak). `train_0000.png`
sang `train_0000.txt` jodinchha. `data.yaml` ma class naam ra folderko sthan lekhinchha.

<!-- ne-cell: fe231231 | after-heading -->
**`data.yaml` ko arth**
<!-- ne-pair: What `data.yaml` means -->

<!-- ne-cell: fe231231 -->
| line | arth |
|---|---|
| `path` | datasetko mul folder |
| `train` / `val` / `test` | pratyek tasbir folder (`path` baat sapeksh) |
| `names` | class kram sankhya → class naam |

> `path` pura bato (absolute) ma lekhieko chha. **folder sarda yo file feri lekhnuparchha.** tyo kram
> arko notebook (04_02) ma dekhaieko chha.

<!-- ne-cell: dafe08ab | after-heading -->
## Part 3 label file padhne

<!-- ne-cell: ce6a81f7 | after-heading -->
### ayat ra labelka paanch maan

<!-- ne-cell: ce6a81f7 | after-image:../../assets/diagrams/teach_yolo_label_fields.png -->
chitra: talim datasetko bastabik file `train_0002.png` ra tyasko ek lineko label baat banaiyeko ayat
(sansleshit tasbir). ayatale sanko dharkalai ghereko chha.

**dhyan dinuparne kura**

ek line ma kram `class_id x_center y_center width height` hunchha. **pahilo `class_id` purnank class
sankhya** ho; yo talim ma 0 = black_spot, 1 = scratch, 2 = streak. chitrako patalo dharka streak hunale
`class_id` 2 hunchha. **class sankhya samanyikrit garindain.**

**banki chaar maan (kendra x, kendra y, chaudai, uchai) matra** 0–1 bich hunchhan. ti pani piksel hoinan,
**tasbirko chaudai-uchaiko anupaat** hun. tyasaile tasbir sano garda label feri lekhnu pardaina. panchai maan
0–1 hundainan.

chitra ma dekhaieko ayat chhapieka sankhya baat yahi gananale banaiyeko ho.

```text
x1 = (x_center - width / 2) * tasbirko chaudai       x_center = (x1 + x2) / 2 / tasbirko chaudai
y1 = (y_center - height / 2) * tasbirko uchai       y_center = (y1 + y2) / 2 / tasbirko uchai
x2 = (x_center + width / 2) * tasbirko chaudai       width    = (x2 - x1) / tasbirko chaudai
y2 = (y_center + height / 2) * tasbirko uchai       height   = (y2 - y1) / tasbirko uchai
```

**sochnuhos**

- uhi ayat 640 px ra 1280 px ko tasbir ma rakhda labelko maan badlinchha?

<!-- ne-cell: clarity-label-bridge-predict | after-heading -->
#### bastabik fileharu jodne

<!-- ne-cell: clarity-label-bridge-predict -->
pahile nai bhaeko sansleshit `train_0002.png` → uhi naamko label → `data.yaml` ko `2: streak` → milaera
dekhaieko chitra jaanchnuhos. anuman: paanch manamadhye anupaat nabhaeko kun ho? pahilo matra purnank class ID ho.

<!-- ne-cell: clarity-label-bridge-interpret -->
pahilo 2 class ho; banki chaar maan matra samanyikrit nirdeshangk hun. tal milaera dekhaieko chitra ma patalo dharka
khojnuhos. sano prayog: tasbirko chaudai ra uchai dubai dobbar garda piksel nirdeshangk ra samanyikrit
nirdeshangk kasari badalinchhan?

<!-- ne-cell: c892d3b2 | after-heading -->
**ek line = ek dosh**
<!-- ne-pair: One line per defect -->

<!-- ne-cell: c892d3b2 -->
label fileko ek line ma paanch sankhya hunchhan (maan udaharanka lagi).

```text
2 0.550000 0.425000 0.300000 0.250000
class_id  x_center  y_center  width  height
(purnank)   <- yi chaar matra 0–1 ma samanyikrit ->
```

- `class_id` … purnank class sankhya. yo talim ma 0 = black_spot, 1 = scratch, 2 = streak
- banki chaar … tasbirko chaudai (x) ra uchai (y) le bhaag gareko kendra ra akar. ayat tasbirbhitra bhae 0–1

**Akar matra badalera (na kati) herda** samanyikrit nirdeshangk uhi anupatma rahanchha. **Katne (crop),
spatial warp, wa tasbir matra badaler label na milaune** kaam gare chahi samanyikrit nirdeshangk tyasai
sahi rahanchha bhanne chhaina.

khali fileko arth **"yo tasbir ma label garne dosh chhaina"** ho. tar tyo **"yo tasbir ma dosh chhaina bhanne praman"
hoina**. chhuteko wa lekhna birsieko label pani ustai khali dekhinchha. tyasaile prishthabhumi tasbir (negative
sample) prayog garnuaghi **tasbir herer jaanchnuhos**. janchieko prishthabhumi tasbirle model lai "yahan kehi
chhaina" sikn maddat garchha.

**yo talimko label niti**: lakshya tin class matra — black_spot, scratch, streak. aru butta wa dag
label garindain. label nabhaeko tasbirko arth "label garne dosh chhaina" matra ho, tyasabhanda badhi hoina.

<!-- ne-cell: 400f5185 | after-heading -->
**samanyikrit nirdeshangk pharkaune**
<!-- ne-pair: Convert normalised coordinates back -->

<!-- ne-cell: 400f5185 -->
labelko 0–1 maan lai tasbirko akarale gunan garda pikselama pharkinchha:

```text
x1 = (xc - w/2) * tasbirko chaudai
y1 = (yc - h/2) * tasbirko uchai
x2 = (xc + w/2) * tasbirko chaudai
y2 = (yc + h/2) * tasbirko uchai
```

<!-- ne-cell: 5dbe36b0 | after-heading -->
**label tasbir ma banaera jaanchne**
<!-- ne-pair: Draw the labels to inspect them -->

<!-- ne-cell: 5dbe36b0 -->
label sahi chha ki chhaina jaanchne sabaibhanda sajilo tarika **tasbir ma banaera hernu** ho.

ayatale dosh ghereko chhaina bhane karan label matra hoina. yahi kram ma jaanchnuhos.

1. **label** … tyo dosh gherne uddeshyale lagaiyo ki (lagaun birsanu, class farak parnu)
2. **nirdeshangk paribartan** … `label_to_boxes` ko ganana, x ra y satinu, `int()` ko raunding
3. **tasbirko akar** … label banaundako ra ahileko tasbirko chaudai-uchai uhi chha ki
4. **rupantaran (transform)** … sano-thulo, katai, ghumaune, khali thaun (letterbox) pharkaun birsanu

yi chaar janchepachhi matra label sudharnuhos. label sudharnuaghi yahi kram ma shangka garne bani byabaharama pani
kaam lagchha. **AI talim garnuaghi detamathi shangka garnu** nai mul niyam ho.

<!-- ne-cell: 7d972880 | after-heading -->
## Part 4 prashikshan, pramanikaran ra parikshan

<!-- ne-cell: f937aad6 | after-heading -->
### tin bhaagko bhoomika

<!-- ne-cell: f937aad6 | after-image:../../assets/diagrams/teach_split_roles.png -->
chitra: tinai bhaagko bhoomika ra yo talimko datasetko bastabik sankhya (train 64 / val 16 / test 16, karib
66.7 / 16.7 / 16.7 %).

**dhyan dinuparne kura**

bhoomika tin chhan. **prashikshan (train)** le weight tay garchha, **pramanikaran (val)** le threshold ra model kasari
chhanne tay garchha, ra **parikshan (test)** sthir garieko settingko antim mulyankanka lagi ek patak matra prayog
hunchha. chitrako sankhya yo datasetko bastabik maan ho.

threshold wa model chhanna prayog gareko data ma mulyankan garda natija ramro dekhinchha. tyasaile **parikshan
antama ek patak matra**. file naam ra hash farak bhae pani eutai khichai-satrama khichieka lagabhag uhi tasbirle bhaagharu
bich jankari chuhaunchhan.

sathai **chitra herer kun file talim ma prayog bhayo thaha hundaina**. chhutyaieko chha ki chhaina bhanne kura file wa
samuhako soochi (manifest) ra talimko setting baat janchinchha.

**sochnuhos**

- tapainko prakriyama kun ekaima bandnu sahi hunchha (miti, lat, kyamera)?

<!-- ne-cell: 108f920a | after-heading -->
**tin bhoomika**
<!-- ne-pair: The three roles -->

<!-- ne-cell: 108f920a -->
| data | bhoomika | kahile prayog |
|---|---|---|
| prashikshan (train) | model ka sankhya tay garchha | talim ma |
| pramanikaran (val) | talimko pragati herer setting chhanchha | talimakai bela |
| parikshan (test) | antim kshamata napchha. **talim ma kahilyai herindain** | talimapachhi, ek patak matra |

kina bandne? prashikshan data ma matra napieko sankhyale **nayan data ma kati sakchha** bhanne dekhaundain. model le
prashikshan tasbirka sukshma gunasamm kanth garera nayan tasbir ma lagu nahune abastha lai **obharaphiting
(overfitting)** bhaninchha.

prashikshan data ma ramro natija aunu matrale "rateko" bhanera tunggo lagdain. prashikshanko sankhyale
**nayan data ma chalchha ki chaldain** bhanne janchdain bhanne matra ho.

<!-- ne-cell: fig-teach_dataset_contact_sheet | after-heading -->
### detasetabhitr ke chha herne

<!-- ne-cell: fig-teach_dataset_contact_sheet | after-image:../../assets/diagrams/teach_dataset_contact_sheet.png -->
chitra: yo talim ma sanchchai prayog hune datasetko train / val / test baat pahilo 4-4 tasbir. ayat label file baat
banaieka chhan. sandarbha natija (bastabik file).

**dhyan dinuparne kura**

contact sheet le "dekhine rup ra label lagaune tarika" matra dekhaunchha. kun file talim ma prayog bhayo bhanne
dekhaundain. tyo bandaphantako abhilekh (file soochi, samuh, talimko setting) baat janchnuparchha.

**sochnuhos**

- yi 4 tasbir herer "talim ma prayog bhaeko chhaina" bhanna sakinchha?

<!-- ne-cell: 200e964b | after-heading -->
## Part 5 data chuhabat

<!-- ne-cell: 396d4a73 | after-heading -->
**eutai tasbir dherai bhaag ma pare ke hunchha**
<!-- ne-pair: What happens when one image appears in two splits -->

<!-- ne-cell: 396d4a73 -->
prashikshan ra parikshan dubaima **eutai tasbir** (wa lagabhag uhi) pare model le tyo tasbir **raterai** ramro
natija dinchha.

yo **thagi** jastai ho. bastabik karyasthalama tyasto tasbir aundain, tyasaile **karyasthalako kshamatako kunai
gyarenti hundaina**. yas lai **data chuhabat (data leakage)** bhaninchha.

**chuhabat hune samanya karan**

- lagatar bhidiyobat phrem nikaler chheuchhauka phrem **shuffle garepachhi** farak bhaag ma rakhnu
- eutai saman farak konabat khicher farak bhaag ma rakhnu
- eutai lat wa eutai khichai-satraka tasbir bhaagharuma bandnu

**purbagrah ra chuhabat farak kura hun.** Shuffle garnuaghi data bandda fileko kram ma niyamitata bhae
pratyek bhaagko samagri purbagrahit hunchha (**sampaling purbagrah**). yo chuhabat hoina. ulto, chheuchhauka phrem
aniyamit rupama bandda lagabhag uhi tasbir train ra test dubaima parchha, tyo **chuhabat** ho. upay
**utpadan, lat wa khichai-satralai ekai maner sangai bandnu** ho.

yo talimko datasetle **tasbirko SHA-256 hash le thyakkai dohoro** janchchha. yo jaanchle **ek bait pani namilne
(byte-identical) dohoro matra** bhetchha. piksel maan ali farak bhaeko "lagabhag uhi tasbir" wa samuh-starko
chuhabat bhetdain.

hash jaanchko natija **tin sankhya chhuttai** padhnuhos: **ganieko file sankhya** (sabai bhaagka tasbir),
**bhinna tasbir sankhya** (dohoro hataeko SHA-256 prakar), ra **eutai samagriko jodi sankhya** (dohoro jodi).
eutai jodi bhae file sankhya bhinna tasbir sankhyabhanda 1 le badhi hunchha.

<!-- ne-cell: fig-teach_leakage_split | after-heading -->
### phremaanusar bandne ki khichaianusar

<!-- ne-cell: fig-teach_leakage_split | after-image:../../assets/diagrams/teach_leakage_split.png -->
chitra: bastabik sansleshit datasetko euta tasbir ra sano piksel-maan abaj thapieko "lagabhag uhi tasbir". sthan
sarieko chhaina. phremaanusar bandda yi dui train ra test ma chhuttinchhan.

**dhyan dinuparne kura**

eutai saman, eutai khichaika tasbir talim ra parikshan ma chhuttie dekhine rup dherai najik hunchha ra kshamata bastabikabhanda
uchcha dekhinchha (leakage). bandaphant **utpadan, khichai-satr jasta samuhako ekai** ma garnuparchha. yo samagriko abaj
piksel maanko sano paribartan ho, sthan sarne hoina. Hash jaanchle ek bait pani namilne dohoro matra bhetchha.

**sochnuhos**

- kramaisang lieka photo aniyamit rupama bandda kshamata kina uchcha dekhinchha?

<!-- ne-cell: audit-teach_group_split_vs_frame_split | after-heading -->
### kod kasari padhne

<!-- ne-cell: audit-teach_group_split_vs_frame_split | after-image:../../assets/svg/teach_group_split_vs_frame_split.svg -->
chitra: eutai khichai-samuhalai bandaphantako sima ma narakhnuhos. (ganana garieko sansleshit udaharan ra yojanabaddha chitra;
model ko bastabik napieko natija hoina.)

**dhyan dinuparne kura**

udaharan: khichai A sabai train, B sabai val, C sabai test ma rakhnuhos.

**sochnuhos**

fileko dhancha pherepachhi SHA-256 farak ayo bhane ti sbatantra tasbir hun?

<!-- ne-cell: 585c7c08 | after-heading -->
## abhyas

<!-- ne-cell: a9d7688a | after-heading -->
**abhyas 1 (adharabhut): label hataile ganana garne**
<!-- ne-pair: Exercise 1 (basic): compute a label by hand -->

<!-- ne-cell: a9d7688a -->
tasbirko akar 320 × 320, doshko class black_spot (`class_id` = 0), ayat `x1=100, y1=140, x2=180, y2=200`
hunda YOLO dhanchako ek line ganana garnuhos. pahilo class sankhya, banki chaar samanyikrit sthan ra akar.

- pura bhaeko maapan: `0 0.437500 0.531250 0.250000 0.187500` sang milnuparchha

<!-- ne-cell: b82ec1c9 | after-heading -->
**abhyas 2 (madhyam): khali label ganne**
<!-- ne-pair: Exercise 2 (intermediate): count the empty labels -->

<!-- ne-cell: b82ec1c9 -->
train / val / test pratyekama **khali label (prishthabhumi tasbir) ko anupaat** ganana garnuhos.

pura bhaeko maapan: tin pratishat ek dashamalabasamm dekhaieka chhan.

<!-- ne-cell: 0fbbc7cb | after-heading -->
**abhyas 3 (baikalpik): data chuhabat bhetne**
<!-- ne-pair: Exercise 3 (optional challenge): introduce and detect leakage -->

<!-- ne-cell: 0fbbc7cb -->
janajan data chuhabat banaera bhetna sakinchha ki parikshan garnuhos. **aniwarya hoina.**

1. `images/test` baat euta tasbir chhaner `images/train` ma **pratilipi** garnuhos
2. mathiko hash jaanch cell feri chalaunuhos
3. dohoro bhetieko kura pushti garnuhos
4. pratilipi metaera pahileko abastha ma pharkaunuhos

pura bhaeko maapan: dohoro 1 bata dekhiyo ra pratilipi metaera pahileko abastha ma pharkaiyo.

<!-- ne-cell: 27c8096a | after-heading -->
#### bujhai jaanchne prashna

<!-- ne-cell: 27c8096a -->
1. suparabhaijd larning ma ke-ke chahinchha? dui kura bhannuhos.
2. label fileko ek lineka paanch maanle ke-ke janaunchhan? kun-kun samanyikrit chhan?
3. pramanikaran data ra parikshan data kina chhutyaune?
4. data chuhabat bhae "natija ramro dekhinchha tar karyasthalama chaldain" kina hunchha?
5. khali label (prishthabhumi tasbir) kina chahinchha? khali label bhae "dosh chhaina" bhanna milchha?

<!-- ne-cell: ac9204c6 | after-heading -->
## samasya parema

<!-- ne-cell: ac9204c6 -->
truti aepachhi pahile "kun cell ma", "kun line ma", "ke sandesh ayo" bhanera lekhnuhos. bujhaunuparne kaam ma pani
tyahi abhilekh rakhnuhos.

| lakshan | ke garne |
| --- | --- |
| kunai tasbir ma label file chhaina | yasko arth "label garne dosh chhaina" ho. tar dosh chhaina bhanne praman hoina. tasbir herer jaanchnuhos. |
| ayat dosh sang milen | ①label ②nirdeshangk paribartan (`label_to_boxes`) ③tasbirko akar ④sano-thulo wa katai jasta rupantaran — yahi kram ma janchepachhi label sudharnuhos. |
| `FileNotFoundError: data.yaml` | dataset banaiyeko chhaina. `python assets\scripts\prepare_datasets.py` chalaunuhos. |
| `UnicodeDecodeError` le label padhindain | label ASCII hunuparchha. editarama feri surakshit gareko bhae character encoding jaanchnuhos. |

<!-- ne-cell: 1058cec3 | after-heading -->
## sampannata janchasuchi

<!-- ne-cell: 1058cec3 -->
**aniwarya bunda matra** diieka chhan. **abhyas 3 (baikalpik) aniwarya hoina**; nagare pani pura maninchha.
samay banki bhae ma matra garnuhos.

sabai ma chinh lagepachhi yo notebook pura hunchha.

**aniwarya**

- [ ] Part 1–Part 5 padher sabai code cell chalaen
- [ ] label tasbir ma banaera janchen
- [ ] hash le dohoro janchen
- [ ] abhyas 1–2 (aniwarya) garen
- [ ] bujhai jaanchne 5 prashnako uttar dien
- [ ] notebook surakshit garen

**baikalpik**

- [ ] abhyas 3 (baikalpik): data chuhabat banaera bheten

<!-- ne-cell: 16f8af21 | after-heading -->
## thap adhyayan (baikalpik)

<!-- ne-cell: 16f8af21 -->
### sandarbha lingk

- [Ultralytics: dataset dhancha](https://docs.ultralytics.com/datasets/detect/)
- [Ultralytics: data sangkalan ra lebaling](https://docs.ultralytics.com/guides/)
- [COCO label dhancha](https://cocodataset.org/#format-data)

### thap chunauti (aniwarya hoina)

khali label euta ghataera (prishthabhumi tasbir euta dosh tasbir ma badaler) talim garnuhos ra jhuto pojitibhako
sankhya badlinchha ki hernuhos.
