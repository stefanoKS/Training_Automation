<!--
Nepali anuwad / Nepali translation source for
notebooks/Day01_AI_Fundamentals/Day01_02_Pixels_and_Images.ipynb

Each block starts with an ne-cell directive naming the notebook cell id.
Do not translate code, file names, URLs or kernel names.
-->
# din 1 notebook 02 — Nepali anuwad

<!-- ne-cell: 324ebd08 | after-heading -->
# din 1 notebook 02: dijital chitra bujhne

<!-- ne-cell: 324ebd08 -->
## sikai lakshyaharu

| Nepali |
| --- |
| 1. dijital chitra "sankhyako talika" ho bhanera bujhaun sakne. |
| 2. pixel sankhya, resolution, chaudai ra uchaiko sambandh bataun sakne. |
| 3. RGB ra greyscale ko farak bataun sakne. |
| 4. NumPy array le chitra banaera badalna sakne. |
| 5. resolution ghataunda jankari haraunchha bhanne kura aphain jancher dekhauna sakne. |

## yo notebookko adharabhut jankari

| bishay | biwaran |
| --- | --- |
| sikai samay (anuman) | 110 minet |
| kathinai | surubati tah |
| poorwashart | din 1 notebook 01 sakieko hunuparchha. |
| aawashyak laibreri | numpy, matplotlib, pillow |
| prayog hune kernel | aivision |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 1](../../COURSE_SYLLABUS.md#day1) |

### bujhaunuparne kaam

| Nepali |
| --- |
| chitra banaune/badalne abhyasko natija |
| resolution ghataunda haraune janakaribare aphno bichar |

<!-- ne-cell: efc6b5ea | after-heading -->
## yo notebook kahan parchha

<!-- ne-cell: efc6b5ea -->
| bishay | biwaran |
| --- | --- |
| din | din 1 |
| ajako kram | ajako notabukamadhye 2 / 3 |
| lagne samay | 110 minet |
| poorwashart | `Day01_01_Introduction_to_AI.ipynb` |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 1](../../COURSE_SYLLABUS.md#day1) |

dinko samayatalika `COURSE_SYLLABUS.md` ma eutai thaun ma chha. yo notebook tyasko euta bhaag matra ho, aphno
chhuttai samayatalika rakhdain. samay thaha nabhae pahile tyahi file hernuhos.

<!-- ne-cell: audit-learning-loop | after-heading -->
### anuman garnuhos, chalaunuhos, hernuhos, byakhya garnuhos

<!-- ne-cell: audit-learning-loop -->
array bhaneko sankhya milaera rakhieko talika ho. channel bhaneko rangaanusarako chhuttai talika ho. mahattwapurna cell
chalaunuaghi input, kaam ra natija ek-ek bakyama lekhnuhos.
pahile anuman lekhnuhos, tyaspachhi cell chalaera maan wa chitra hernuhos. canvas ko euta pixel badaler feri
anuman garera chalaunuhos. janajan rakhieka truti ra nasakieka abhyaska lagi lekhieko nirdeshan pachhyaunuhos.

<!-- ne-cell: ed9b3d3c | after-heading -->
## Part 0 tayari

<!-- ne-cell: 328beddc | after-heading -->
**chitra ma prayog hune phant milaunuhos**
<!-- ne-pair: Configure Japanese text in figures -->

<!-- ne-cell: 328beddc -->
Matplotlib ko purbanirdharit phantale Japani akshar dekhauna sakdain. tyasaile chitrako shirshak `□□□` jasto
dekhinchha. arko cellle Japani akshar dekhauna sakne phant khojer milaunchha. macOS wa Linux ma sbatah arko phant
chhaninchha.

<!-- ne-cell: 6bf89cef | after-heading -->
## Part 1 pixel bhaneko ke ho

<!-- ne-cell: e4ad5e50 | after-heading -->
### pixel ra nirdeshank

<!-- ne-cell: e4ad5e50 | after-image:../../assets/diagrams/diagram_pixel_grid.png -->
chitra: 8×8 pixel ko udaharan (8-bit, 1 channel). euta khand euta pixel ho, ra pratyekama 0–255 ko euta
maan hunchha.

**dhyan dinuparne kura**

yo chitra **8-bit, 1 channel (greyscale)** ko udaharan ho. euta khandama sankhya **euta** matra hunchha, ra
thulo bhae tyo badhi ujyalo dekhinchha. padhne tarika mathi-bayanbat dayantir, pangkti-pangkti ho. sthan
"pangkti y, stambha x" kram ma diinchha, `image[y, x]` bhanera lekhinchha. x dayantir, y talatir badhchha, tyasaile
ganitako graphabhanda mathi-tal ulto hunchha. **RGB rangako chitra ma uhi khandama R, G, B tinabata maan hunchhan**
(yo chitrako tin guna sankhya).

**sochnuhos**

- yo chitrako mathi-bayanko pixel lai pangkti ra stambha numberle kasari lekhnuhunchha? RGB rangako chitra bhae tyo
  khandama katibata sankhya hunchhan?

<!-- ne-cell: 610c3045 | after-heading -->
**pixel (chitrabindu)**
<!-- ne-pair: Pixel -->

<!-- ne-cell: 610c3045 -->
dijital chitra sana chaukon **talamathi ra chheuchhau milaera rakhieko** hunchha.
yo euta chaukonalai **pixel (chitrabindu)** bhaninchha.

yo notebook ma **8-bit chitra** prayog garchhaun. 8-bit greyscale chitra ma pratyek pixel ma
**euta sankhya** hunchha.

- `0` = kalo
- `255` = seto
- bichako maan = khairo

0–255 kina bhane ek pixel lai 8 bit (2 ko 8 ghat = 256 tarika) le dekhainchha.
**0 dekhi 255 samm 256 tah matra** hunchha bhanne samjhanuhos. 16-bit chitrajasta ajh sukshma tah bhaeka
dhancha pani hunchhan.

bhandaran hune sankhyako sankhya chitrako kisimaanusar farak parchha.

| kisim | prati pixel sankhya | sankhyako jamma |
|---|---|---|
| 8-bit greyscale | 1 | uchai × chaudai |
| 8-bit RGB rang | 3 | uchai × chaudai × 3 |

talako chitra hernuhos. bayan 8×8 pixel ko chitra, dayan tyas lai thulo banaera sankhya dekhaieko chha.

<!-- ne-cell: c69e86d8 | after-heading -->
**sankhya ra ujyaloko sambandh**
<!-- ne-pair: The relationship between numbers and brightness -->

<!-- ne-cell: c69e86d8 -->
talako chitrale 0–255 ko maan bastabama kati ujyalo dekhinchha bhanera dekhaunchha.
sankhya thulo hunda setotir najik hunchha.

<!-- ne-cell: 0f48e9a7 | after-heading -->
## Part 2 chaudai, uchai ra resolution

<!-- ne-cell: efef174f | after-heading -->
#### chitrako akar ra bastabik napako sambandh

<!-- ne-cell: efef174f -->
| matra | arth | udaharan |
|---|---|---|
| chitrako ayam | chaudai×uchai (px) | 640×480 px |
| jamma pixel sankhya | chaudai × uchai | 307,200 pixels |
| napine satahako maapan | euta pixel le dhakne lambai | mm/px |
| intensity | pixel ko ujyalo | 8-bit: 0–255 |

"resolution" matra bhanda ke bujhine aspasht hunchha. jamma pixel sankhya ra mm/px chhutyaunuhos.
bastabama sukshma biwaran chhutyaun sakinchha ki sakindaina bhanne kura prakashiki, contrast, noise ra
sampling ma pani bhar parchha.

<!-- ne-cell: clarity-fixed-fov | after-heading -->
### uhi drishyakshetra ma pixel sankhya badalne

<!-- ne-cell: clarity-fixed-fov | after-image:../../assets/svg/teach_fixed_fov_sampling.svg -->
**sochnuhos**

anuman: 1300 mm chaudai 13000 pixel le khichda 0.3 mm kati pixel ma parchha?

**dhyan dinuparne kura**

yo hisab garieko kritrim udaharan ho. `1300/1300=1 mm/px`, `1300/13000=0.1 mm/px`.
karib 3 pixel ma pani patta lagaune ra napne bishbasaniyata gyarenti hundaina. surakshit JPEG lai thulo
banaunda khichaiko jankari thapindain. drishyakshetra adha banaera feri khichne kaam surakshit chitra sano banaune
kamabhanda chhuttai ho.

<!-- ne-cell: f984e55f | after-heading -->
### natijako udaharan

<!-- ne-cell: f984e55f -->
yo udaharan ma talako natija aaunchha (uhi input diiyo bhane uhi natija aaunchha). label kodale chhapne
Japani aksharamai dekhinchha.

yo greyscale chitraka lagi 64 bhaneko uchai × chaudai ho; 307,200 ra 2,073,600 ti dui kyamera akaraka
lagi uhi gunanaphal hun. uhi akarako rang chitra ma tin guna badhi maan bhandaran hunchha.

<!-- ne-cell: 6d88b3b1 | after-heading -->
**resolution ra dekhine doshko akar**
<!-- ne-pair: Resolution and the smallest visible defect -->

<!-- ne-cell: 6d88b3b1 -->
yo utpadan nirikshan ma nirnayak kura ho.

sitako chaudai 1,300 mm lai chaudai 1,300 pixel ko kyamerale khichyaun bhanaun. tab **1 pixel = 1 mm** hunchha.
0.3 mm ko dosh **ek pixel bhanda sano** hunchha, tyasaile akar ra sthan sthir rupama nirnaya garna sakindaina.
taipani baraparako bhanda ujyalo dherai farak bhae tyo pixel ko maan badlinchha. "nadekhine" hoina "akarako rupama
resolved nahune" bhanera bujhnu thik hunchha.

chaudai 13,000 pixel le khichda 1 pixel = 0.1 mm hunchha, ra 0.3 mm ko dosh **3 pixel** ma parchha.

chahine pixel ghanatb talako sutrale anuman garinchha.

```text
prati mm chahine pixel = doshka lagi chahine pixel ÷ doshko akar [mm]
```

0.3 mm ko dosh 3 pixel ma dekhauna chahanubhayo bhane prati mm 3 ÷ 0.3 = **10 pixel** chahinchha.
chaudai 1,300 mm bhae 1,300 × 10 = **13,000 pixel** hunchha.

yahan "3 pixel" **yo talimka lagi chhanieko lakshya maan** ho. kati pixel bhae pakka bhetinchha bhanne kura
lensako kshamata, contrast, dhamilopan, noise ra nirnaya garne tarikama nirbhar garchha.
"3 pixel bhae sadhain bhetinchha" bhanne gyarenti hoina.

> "AI ko shuddhata kam chha" bhannuaghi **tyo dosh chitramai dekhinchha ki dekhindain** bhanera
> janchnu aawashyak chha.

<!-- ne-cell: 389b5529 | after-heading -->
## Part 3 RGB ra greyscale

<!-- ne-cell: 77008bda | after-heading -->
### euta chitra bhaneko tinabata talika

<!-- ne-cell: 77008bda | after-image:../../assets/diagrams/teach_rgb_channels.png -->
chitra: uhi chitra lai R, G, B channel ma chhutyaieko. tinabata talikale uhi pixel sthanalai farak-farak
sankhyale dekhaunchhan.

**dhyan dinuparne kura**

rang chitra (uchai, chaudai, 3) akarako array ho. 3 bhaneko R, G, B ka tinabata talika, pratyekama 0–255 ko
maan. **uhi euta pixel** R talika ma ratoko tibrata, G talika ma hariyoko tibrata, B talika ma niloko
tibrata bhaera baschha. euta channel matra dekhaunda tyo tibrata ujyaloko rupama dekhinchha (rang dekhindain).
tinabata milaepachhi matra mul rang banchha. tinabatai uhi bhae khairo hunchha. thik talako bastabik photoko cell pani uhi
kram (uchai × chaudai × 3) ma surakshit chha.

**sochnuhos**

- R=200, G=60, B=60 bhaeko pixel kasto rang dekhinchha? R talika matra dekhaunda tyo pixel ujyalo dekhinchha
  ki andhyaro?

<!-- ne-cell: fig-chelsea | after-heading -->
### bastabik photoma pani 1 pixel = 3 sankhya

<!-- ne-cell: fig-chelsea | after-image:../../assets/external_samples/open_reference/chelsea.png -->
photo: skyan garieko bastabik tasbir (scikit-image `chelsea`, Stefan van der Walt, CC0 1.0). talako
byakhya ma bhaeka RGB talika sang **uhi kram** (uchai × chaudai × 3) ma surakshit chha. karakhanako PVC chitra
hoina, rangako banabat hernaka lagi matra udaharan ho.

**dhyan dinuparne kura**

yo photoma pani prati pixel R, G, B ka tinabata purnank (0–255) matra hunchhan. "photo bhaekole bishesh
sanyantra" bhanne kura chhaina. dekhaunda ti tin sankhya lai prakashaka tin adharabhut rang milaera dekhaieko matra ho.

**sochnuhos**

- yo photoko euta pixel ko maan (34, 139, 34) thiyo bhane dekhine rangama rato, hariyo, nilomadhye kun baliyo hunchha?

<!-- ne-cell: a067440a | after-heading -->
**rang chitra bhaneko tinabata talika**
<!-- ne-pair: A colour image is three tables -->

<!-- ne-cell: a067440a -->
rang chitra ma **rato, hariyo, nilo** tin sankhyale euta pixel dekhainchha.
arthat prati pixel tin sankhya.

```text
pixel (pangkti y=2, stambha x=3) = rato 210, hariyo 205, nilo 190
```

tinabatai uhi bhae khairo hunchha. tyasaile **greyscale (kalo-seto)** ma prati pixel 1 sankhya matra pugchha.

| kisim | prati pixel sankhya | array ko akar |
|---|---|---|
| greyscale | 1 | (uchai, chaudai) |
| RGB rang | 3 | (uchai, chaudai, 3) |

NumPy ma rang chitra `shape = (uchai, chaudai, 3)` bhaeko array hunchha.
`3` bhaneko "rato, hariyo, nilo" ho. **yo kram (RGB) samjhanuhos.**
OpenCV ma **BGR** (nilo, hariyo, rato) kram hunchha, tyasaile dhyan dinuhos (din 2 ma samhalinechha).

<!-- ne-cell: c0f7ec40 | after-heading -->
### natijako udaharan

<!-- ne-cell: c0f7ec40 -->
yo udaharan ma talako natija aaunchha (uhi input diiyo bhane uhi natija aaunchha). label kodale chhapne
Japani aksharamai dekhinchha.

`(3, 4, 3)` bhaneko uchai 3, chaudai 4 ra prati pixel tin rang maan. `画素 (0,0)` bhaneko pangkti 0, stambha 0 —
Part 4 ma byakhya garieko `image[y, x]` kram.

<!-- ne-cell: 710f8ada | after-heading -->
**greyscale ma badalne**
<!-- ne-pair: Converting to greyscale -->

<!-- ne-cell: 710f8ada -->
RGB baat greyscale ma badalnu bhaneko tin maanko **bharit ausat** ho.
manisako ankha hariyoprati sanbedanashil hunchha, tyasaile hariyoko bhar thulo chha.

```text
khairo = 0.299 × rato + 0.587 × hariyo + 0.114 × nilo
```

yo sutra kanth garnu aawashyak chhaina. "tin sankhya lai eutai ma milaieko chha" bhanera bujhe pugchha.

<!-- ne-cell: fed2a6d9 | after-heading -->
### natijako udaharan

<!-- ne-cell: fed2a6d9 -->
yo udaharan ma talako natija aaunchha (uhi input diiyo bhane uhi natija aaunchha). label kodale chhapne
Japani aksharamai dekhinchha.

lambai 3 bhaeko antim aksh haraeko chha: prati pixel tin rang maan euta ujyalo maan banyo. shuddh rato, hariyo
ra nilo pixel ko ujyalo farak parchha, kinabhane bhar farak chha.

<!-- ne-cell: dda7bd81 | after-heading -->
#### aphain rang banaera hernuhos

<!-- ne-cell: dda7bd81 -->
`R`, `G`, `B` tin sankhya sarda rang badlinchha. **sarnuaghi kasto rang banchha anuman garnuhos.**

| anuman | jaanchne maan |
|---|---|
| kahile khairo hunchha? | tinabatai uhi sankhya |
| kahile pahenlo hunchha? | R ra G thulo, B = 0 |
| kahile kalo hunchha? | tinabatai 0 |

talako "parameter cell" le widget nabhae pani uhi prayog garna sakinchha.

anuman: RGB=(255,0,0) bhane rato ho. bharit khairo
`0.299×255 + 0.587×0 + 0.114×0 = 76.245` (8-bit dekhaima karib 76) hunchha.
talako parameter cell ma R matra 255→0 banaera anuman sang tulna garnuhos.

<!-- ne-cell: 11c4e389 | after-heading -->
## Part 4 chitrako nirdeshank

<!-- ne-cell: a54f4513 | after-heading -->
**mulabindu mathi-bayan, y talatir**
<!-- ne-pair: The origin is top-left, and y increases downward -->

<!-- ne-cell: a54f4513 -->
ganitako graphabhanda **ulto** hunchha. dhyan dinuhos.

- mulabindu `(0, 0)` **mathi-bayan** ko pixel
- `x` **dayan** tir badhchha
- `y` **tal** tir badhchha

NumPy array pani uhi ho. `image[y, x]` kram ma lekhinchha. **`x` ra `y` ko kram ulto** hunchha,
tyasaile suru ma abashy galti hunchha. shant bhaera jaanchnuhos.

<!-- ne-cell: fig-teach_array_indexing | after-heading -->
### array ko index ra slice

<!-- ne-cell: fig-teach_array_indexing | after-image:../../assets/diagrams/teach_array_indexing.png -->
chitra: `image[1:4]` le chhanne pangkti. pangkti index 1, 2, 3 bhaneko mathibat dosrodekhi chautho pangkti
samm (yojanabaddha).

**dhyan dinuparne kura**

chitrako index 0 baat suru hunchha. `image[1:4]` bhaneko "pahilodekhi tesro pangkti" hoina, "pangkti index
1, 2, 3", arthat mathibat dosrodekhi chautho pangkti. `image[1:4, 2:5]` jastai pangkti ra stambha sangai
lekhinchha.

**sochnuhos**

- mathibat pahilo pangkti matra chhanna kasari lekhnuhunchha?

<!-- ne-cell: clarity-pixel-predict | after-heading -->
#### euta pixel anuman garne

<!-- ne-cell: clarity-pixel-predict -->
input mathiko 5×7 array ho, kaam `canvas[2,3]`, natija euta maan. kram `image[y,x]` ho.
chalaunuaghi `canvas[3,2]` sang uhi ho ki hoina anuman garnuhos. chalaepachhi talako chitra ma thegana jaanchnuhos.

<!-- ne-cell: audit-teach_pixel_inspector | after-heading -->
### kod padhne tarika

<!-- ne-cell: audit-teach_pixel_inspector | after-image:../../assets/svg/teach_pixel_inspector.svg -->
chitra: 5 pangkti 7 stambhako canvas[2,3] ko maan 100 ho. pahilo index pangkti y, dosro stambha x ho.
(hisab garieko kritrim udaharan/yojanabaddha. model ko maapan garieko natija hoina.)

**dhyan dinuparne kura**

5 pangkti 7 stambhako canvas[2,3] ko maan 100 ho. pahilo index pangkti y, dosro stambha x ho. nilo gherako
euta pixel ra index ultyaera lekhieko maan tulna garnuhos.

**sochnuhos**

canvas[2, 3] ra canvas[3, 2] uhi hun?

<!-- ne-cell: clarity-slice-predict | after-heading -->
#### slice anuman garne

<!-- ne-cell: clarity-slice-predict -->
input uhi `canvas` ho. `canvas[1:4,2:5]` le pangkti 1, 2, 3 ra stambha 2, 3, 4 chhanchha.
suru samabesh hunchha, antya 4 ra 5 samabesh hundaina. chalaunuaghi natijako `shape` anuman garnuhos.

<!-- ne-cell: audit-teach_slice_walkthrough | after-heading -->
### kod padhne tarika

<!-- ne-cell: audit-teach_slice_walkthrough | after-image:../../assets/svg/teach_slice_walkthrough.svg -->
chitra: canvas[1:4,2:5] le 3 pangkti 3 stambha nikalchha. antya 4 ra 5 samabesh hundaina.
(hisab garieko kritrim udaharan/yojanabaddha. model ko maapan garieko natija hoina.)

**dhyan dinuparne kura**

pangkti 1–3 ra stambha 2–4 lai dayanko array ma pachhyaunuhos. bichako matra 100 chha, ra shape (3,3) ho.

**sochnuhos**

[1:4, 2:5] ko stambhako antya 6 banaunda shape kasto hunchha?

<!-- ne-cell: clarity-slice-followup -->
natija 3×3 ho ra bichako matra 100 chha. stambhako antya 5 baat 6 banaunda kati stambha hunchhan?
talako chitrako mul 3×3 sang tulna garera antya feri pahileko banaepachhi agadi badhnuhos.

<!-- ne-cell: 0ef08f98 | after-heading -->
### natijako udaharan

pangkti ra stambha hedar bhaeko 5×7 talikale thegana janchchhaun. mul chaar kunako maan jastako tastai chha.
`canvas[2,3]=100`, `canvas[3,2]=0`, slice `[[0,0,0],[0,100,0],[0,0,0]]` ho.
aba yahi niyam 6×6 ko andhyaro kshetra ma sarnuhos. 6 pangkti kina hunchha pahile byakhya garnuhos.

<!-- ne-cell: fef0e737 | after-heading -->
## Part 5 chitra banaera badalne

<!-- ne-cell: e313b7d9 | after-heading -->
**sitajasto dekhine chitra banaune**
<!-- ne-pair: Build a sheet-like image -->

<!-- ne-cell: e313b7d9 -->
aba bastabama "PVC sitajasto" chitra banaera kaam garchhaun.
bastabik karakhanako chitra hoina, tar ujyaloko asamanata ra noise ko soch abhyas garna sakinchha.

charan 3 bata chhan.

1. sabai thaun ujyalo khairo (`210`) le bharne
2. bistarai badaline asamanata thapne
3. sukshma noise thapne

<!-- ne-cell: d6f4780d | after-heading -->
### natijako udaharan

yo udaharan ma talako natija aaunchha (seed sthir chha. antim angk NumPy ko sanskaranaanusar farak parna sakchha).

maanharu 210 baraparai rahanchhan, kinabhane adhar khairoma shading ra noise jodinda tyahi dayarama parchha; `uint8`
bhaneko pratyek maan 0 dekhi 255 sammako purnankko rupama bhandaran hunchha.

<!-- ne-cell: 159783f0 | after-heading -->
**pixel badaler dosh banaune**
<!-- ne-pair: Modify pixels to create a defect -->

<!-- ne-cell: 159783f0 -->
pixel ko maan badalda tyo bhaagko dekhine rup badlinchha. yo udaharan ma mul maan (210 asapas) bhanda sano `40`
rakhiekole tyo bhaag **andhyaro** hunchha. yo "dosh" ko sabaibhanda sano udaharan ho.

talako cellle 6×6 pixel ko andhyaro chaukon banaunchha. `sheet[60:66, 100:106]` bhaneko
"pangkti y 60–65, stambha x 100–105" bhanne ho. **pahile pangkti (y), tyaspachhi stambha (x)** lekhinchha.
Part 4 ko chitra "array ko index ra slice" ko uhi niyam ho. tyo chitra ma `canvas[1:4, 2:5]` prayog bhaeko
thiyo. yo cellle `sheet[60:66, 100:106]` prayog garchha. suru ra antya matra farak ho, niyam uhi ho. antyako
maan **samabesh hundaina**, tyasaile 6 pangkti × 6 stambha hunchha (7 hoina).

<!-- ne-cell: 4b00fec6 | after-heading -->
## Part 6 thulo/sano banaunda haraune jankari

<!-- ne-cell: eff2d8cf | after-heading -->
### sano banaunda sukshma biwaran ra contrast haraunchha

<!-- ne-cell: eff2d8cf | after-image:../../assets/diagrams/teach_downsample_defect.png -->
chitra: uhi kritrim chitra lai 480 px, 120 px ra 30 px ma sano banaeko natija (Pillow ko BILINEAR
interpolation le bastabamai hisab gareko chitra).

**dhyan dinuparne kura**

30 px samm sano banaunda patalo chot 1 pixel bhanda sano hunchha. **chot haraundain.** chitra ma tirchho rekha
ajhai dekhinchha. tar rekhako sukshma biwaran haraunchha ra baraparasangako ujyaloko farak pani sano hunchha, tyasaile
akar ra sthan thyakkai padhna gahro hunchha. sampurna chitrako standard deviation jasto euta statistic le
hoina, **chotako sthan ra pachhadiko farak** herer nirnaya garnuhos.

**sochnuhos**

- 0.3 mm ko chot 3 pixel ma dekhauna prati mm kati pixel chahinchha?

<!-- ne-cell: be892bb2 | after-heading -->
**sano banaunda ke hunchha**
<!-- ne-pair: What happens when you shrink an image -->

<!-- ne-cell: be892bb2 -->
chitra sano banaunda **pixel ghatchha**, tyasaile jankari haraunchha.
bistrit rupama bhanne ho bhane chheuchhauka pixel milaera euta banainchha (yo notebook ma BILINEAR interpolation).

sano dosh sano banaunda akarako sukshma biwaran haraunchha ra baraparasangako ujyaloko farak pani sano hunchha.
tyasko natija bhettaun ra napna gahro hunchha. haraunchha bhanne chahin pakka hoina.
yo utpadan nirikshan ma dherai mahattwapurna hunchha.

yahan surakshit garieko uhi chitra sano banainchha. prakashiki badaler arko drishyakshetra khichne kaam hoina.
sano dosh 1 pixel bhanda kam bhae pani pixel ko ujyaloma asar garna sakchha.

<!-- ne-cell: fig-teach_resize_profile | after-heading -->
### uhi kshetra lai 3 resolution ma tulna garne

<!-- ne-cell: fig-teach_resize_profile | after-image:../../assets/diagrams/teach_resize_profile.png -->
chitra: yo udaharanko kritrim chitra sano banaunda dosh baat jane katchhedako ujyalo (maapan garieko maan).
terso aksh sthan, thado aksh 0–255 ko pixel maan ho.

**dhyan dinuparne kura**

yo chitrale **yo udaharan ma napieko maan** dekhaunchha. "sano banaunda sadhain kam gahiro ra pharakilo hunchha"
bhanne niyam hoina. interpolation ko tarika, doshko akar ra pachhadisangako farakle badalchha. thado akshako ikai ra
katchhed kahan baat liiyo jaanchnuhos.

**sochnuhos**

- sano banae pani andhyaropanako nyoonatam maan khasai nabadaline abastha kasto hola?

<!-- ne-cell: 28884f36 | after-heading -->
**sano banaunda dosh kahan samma rahanchha**
<!-- ne-pair: How much of the defect survives? -->

<!-- ne-cell: 28884f36 -->
talako cellle harek resolution ma "sabaibhanda andhyaro pixel" janchchha.
yo udaharan ma sano banaundai janda sabaibhanda andhyaro pixel ko maan pachhadiko najik pugchha. tar yo euta sankhyale
matra "dekhinchha/dekhindain" tay gardaina. bastabik nirikshan ma chotako sthan ra pachhadiko farak, noise ko matra ra
nirnaya garne tarika sangai janchinchha.

<!-- ne-cell: 23b71a6c | after-heading -->
### natijako udaharan

yo udaharan ma talako natija aaunchha (seed sthir chha. antim angk NumPy ko sanskaranaanusar farak parna sakchha).
label kodale chhapne Japani aksharamai dekhinchha.

yahan "YES" bhaneko 150 bhanda andhyaro pixel banki rahyo bhanne matra ho; yo sabaibhanda andhyaro pixel ko jaanch
ho, chinh sajilai bhetinchha bhanne praman hoina. chitra sano hundai janda sabaibhanda andhyaro maan 40 baat 171
pugchha, tar `teach_downsample_defect.png` (Part 6) ko 30 px chitra ma chinh ajhai dekhinchha bhanne kura dhyan
dinuhos.

<!-- ne-cell: f9071fc7 | after-heading -->
## Part 7 anuman garepachhi chalaune

<!-- ne-cell: e6e142e9 | after-heading -->
**natija anuman garnuhos**
<!-- ne-pair: Predict the result -->

<!-- ne-cell: e6e142e9 -->
talako cellle `predict_me` bhanne chitra banaunchha. **chalaunuaghi**
notama talaka 3 kura lekhnuhos.

1. chitra kasto rang dekhinchha
2. kata gadha bhaag banchha
3. sampurna ausat ujyalo kati jati hola

lekhisakepachhi chalaera anuman sang tulna garnuhos.

<!-- ne-cell: 46ee1d4a | after-heading -->
**tyasto kina bhayo**
<!-- ne-pair: Why it looks like that -->

<!-- ne-cell: 46ee1d4a -->
bayan bhaag rato dekhinuko karan ratoko maan matra `230` banaiyo. dayanko gadha bhaag ma tinabatai maan `60`
banaiyekole khairo ho.

yo "anuman garepachhi chalaune" abhyas aundo 5 dinabhari kaam lagchha.
**anuman namileko kshan nai sabaibhanda dherai sikine kshan** ho.

<!-- ne-cell: 50a7a817 | after-heading -->
## abhyas

<!-- ne-cell: c13aea22 | after-heading -->
**abhyas 1 (adharabhut): aphnai chitra banaune**
<!-- ne-pair: Exercise 1 (basic): make your own image -->

100×100 ko greyscale chitra banaera bichako 20×20 pixel `30` banaunuhos.
tyaspachhi `plt.imshow()` le dekhaunuhos.

**sakieko thanne adhar:** dekhaieko chitrako bichama euta andhyaro chaukon dekhinchha.

<!-- ne-cell: b8228fc7 | after-heading -->
**abhyas 2 (madhyam): rang badalne**
<!-- ne-pair: Exercise 2 (intermediate): change colours -->

abhyas 1 ko chitra lai **rang** banaera bichako chaukon "rato khalako khairo" banaunuhos.
tyaspachhi hariyo ra nilo ansh 0 banaera dekhaunuhos. yo **rato matra bhaeko RGB chitra** ho.
ratoko tibrata ujyaloko rupama dekhinchha, tyasaile ujyalo pachhadi rato ra `30` ko chaukon andhyaro rato
dekhinchha.

**sakieko thanne adhar:** rato matra rakhieko chitra ma kun pixel ujyalo dekhinchha (ratoko maan thulo bhaeko
pixel) bhanera bujhaun sakne.

<!-- ne-cell: 6850a83e | after-heading -->
**abhyas 3 (bikas/aichchhik): resolution ra doshko sambandh byakhya garne**
<!-- ne-pair: Exercise 3 (optional challenge): relate resolution to detectability -->

Part 6 ko natija prayog garera "chaudai 1,300 mm ko sitama 0.3 mm ko dosh bhettaun tersotir kati pixel
chahinchha" hisab garnuhos. karan pani lekhnuhos.

sanket: euta dosh 3 pixel ma dekhauna chahanchhaun bhanera mannuhos. yi 3 pixel yo talimka lagi chhanieko lakshya
maan hun. prakashiki, contrast, dhamilopan ra noise le chahine pixel sankhya badalchha.

**sakieko thanne adhar:** chahine pixel sankhya ra tyasko adhar (prati mm pixel sankhya, 3 pixel bhanne
lakshya maan) dubai lekhnuhos.

<!-- ne-cell: b41ca058 | after-heading -->
#### bujhai jaanch

1. 640×480 ko rang chitra ma katibata sankhya hunchhan? hisabako sutra pani lekhnuhos.
2. chitrako nirdeshankama `(0, 0)` kahan parchha? ganitako graphabhanda kasari farak chha?
3. RGB ka tinabatai maan 120 bhae tyo pixel kasto rang hunchha?
4. resolution ghataunda sano doshko dekhine rup kasari badlinchha? karan pani lekhnuhos.
5. "pixel badalne" kaam utpadan line ma ke sang barabar hunchha?

namuna jabaph: `docs/instructor/day01_instructor_guide.md`.

<!-- ne-cell: caac07dd | after-heading -->
## samasya aunda

truti ae pahile "kun cell ma", "kun line ma", "ke sandesh ayo" bhanera tipnuhos. bujhaunuparne kaam ma pani
tyahi abhilekh rakhnuhos.

| lakshan | ke garne |
| --- | --- |
| `FileNotFoundError` le chitra padhna sakien | samagri baneko chhaina. adharabhut batabaran sakriya gareko CMD ma samagriko mul folder baat `python assets\scripts\generate_training_assets.py` ek patak chalaunuhos. |
| `TypeError: Invalid shape ... for image data` | `imshow` lai diieko array ko ayam galat chha. khairo 2 ayam, rang 3 ayam hunchha. |
| khairo chitra purai kalo/seto dekhinchha | intensity dekhaune scale ko samasya ho. `vmin=0, vmax=255` dinuhos. nadie maanko dayara sbatah tankinchha. |
| `IndexError: index 200 is out of bounds` | nirdeshank chitrako bahir chha. `shape` jaanchnuhos (`shape[0]` uchai, `shape[1]` chaudai). |
| rang anautho (rato ra nilo ulto dekhinchha) | channel ko kramko samasya ho. OpenCV BGR kram prayog garchha, `cv2.cvtColor(image, cv2.COLOR_BGR2RGB)` le badalnuhos (din 2). `vmin`/`vmax` le yo mildaina. |
| sano banaunda chot dekhna gahro hunchha | pixel milaine hunale sukshma biwaran ra contrast haraunchha. chotako sthan ra pachhadiko farak sano banaunuaghi ra pachhi tulna garnuhos. |

<!-- ne-cell: 5254066a | after-heading -->
## sakieko janchasuchi

**aniwarya** bastuharu suchibaddh chhan. sabai ma chinh lagepachhi yo notebook sakinchha.

- [ ] Part 1–Part 7 padhen
- [ ] sabai kod cell chalaen
- [ ] anuman lekher matra Part 7 chalaen
- [ ] abhyas 1–2 (aniwarya) garen
- [ ] resolution ra doshko akarako sambandh bujhaun sakchhu
- [ ] bujhai jaanchka 5 prashnako jabaph dien
- [ ] notebook surakshit garen

**aichchhik (sakieko sartama pardaina):** abhyas 3 ra "thap sikai" ko atirikt chunauti.

<!-- ne-cell: 669d9fb1 | after-heading -->
## thap sikai (aichchhik)

<!-- ne-cell: 669d9fb1 -->
### sandarbha lingk

- [NumPy array ko adhar](https://numpy.org/doc/stable/user/basics.creation.html)
- [Matplotlib imshow](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html)
- [Pillow ko resize](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize)
- [dijital chitrako adhar (OpenCV tutorial)](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)

### atirikt chunauti (aniwarya hoina)

`Image.resize` ko `Image.BILINEAR` lai `Image.NEAREST` banaera Part 6 ko talika feri banaunuhos.
natija kasari badaliyo? karan ke ho? chot harayo, ki dekhna gahro matra bhayo?
