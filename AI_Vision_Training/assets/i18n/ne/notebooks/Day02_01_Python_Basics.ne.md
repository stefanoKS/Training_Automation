<!--
Nepali anuwad / Nepali translation source for
notebooks/Day02_Python_OpenCV/Day02_01_Python_Basics.ipynb

Each block starts with an ne-cell directive naming the notebook cell id.
Do not translate code, file names, URLs or kernel names.
-->
# din 2 notebook 01 — Nepali anuwad

<!-- ne-cell: 79dc91db | after-heading -->
# din 2 notebook 01: Python parichay

<!-- ne-cell: 79dc91db -->
## sikai lakshyaharu

| Nepali |
| --- |
| 1. `print()` prayog garera maan dekhauna sakne. |
| 2. chal (variable) ma sankhya ra akshar (text) rakhna sakne. |
| 3. chaar adharabhut ganit ra tulna garne sanchalak (operator) prayog garna sakne. |
| 4. True / False ko arth bataun sakne. |
| 5. truti sandesh (error message) padher aphain sudhar garna sakne. |

## yo notebookko adharabhut jankari

| bishay | biwaran |
| --- | --- |
| sikai samay (anuman) | 125 minet |
| kathinai | surubati tah |
| poorwashart | din 1 sakieko hunuparchha. |
| aawashyak laibreri | numpy, matplotlib, pillow |
| prayog hune kernel | aivision |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 2](../../COURSE_SYLLABUS.md#day2) |

### bujhaunuparne kaam

| Nepali |
| --- |
| abhyas 1–3 ka karyakram |
| truti abhilekh (error log) |

<!-- ne-cell: fcc49434 | after-heading -->
## yo notebook kahan parchha

<!-- ne-cell: fcc49434 -->
| bishay | biwaran |
| --- | --- |
| din | din 2 |
| ajako kram | ajako notabukamadhye 1 / 3 |
| lagne samay | 125 minet |
| poorwashart | din 1 |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 2](../../COURSE_SYLLABUS.md#day2) |

dinko samayatalika `COURSE_SYLLABUS.md` ma eutai thaun ma chha. yo notebook tyasko euta bhaag matra ho, aphno
chhuttai samayatalika rakhdain. samay thaha nabhae pahile tyahi file hernuhos.

<!-- ne-cell: audit-learning-loop | after-heading -->
### anuman garnuhos, chalaunuhos, hernuhos, byakhya garnuhos

<!-- ne-cell: audit-learning-loop -->
maan rakhne kaamle naam lai euta maan sang bandhchha. `=` tulna hoina. mahattwapurna cell chalaunuaghi input, kaam ra
natija ek-ek bakyama lekhnuhos. pahile anuman lekhnuhos, tyaspachhi cell chalaera maan wa chitra hernuhos.
eutai kura matra badalnuhos, feri anuman garera chalaunuhos. janajan rakhieka truti ra nasakieka abhyaska
lagi lekhieko nirdeshan pachhyaunuhos.

<!-- ne-cell: 289d22f2 | after-heading -->
## Part 0 tayari

<!-- ne-cell: f2e7dc76 | after-heading -->
## Part 1 maan dekhaune

<!-- ne-cell: 4c543e1a | after-heading -->
**`print()` ko adhar**
<!-- ne-pair: The basics of `print()` -->

<!-- ne-cell: 4c543e1a -->
`print()` le koshthakabhitrako maan skrinama dekhaunchha. mathiko kod udaharan hernuhos.

tesro line jastai `"..."` ra sankhya kamale chhutyaera rakhda, ti **euta khali thaunle chhutyaera** ekai laharama
dekhinchhan.

| lekhne tarika | dekhine natija |
|---|---|
| `print("abc")` | `abc` |
| `print(100.3)` | `100.3` |
| `print("abc", 100.3)` | `abc 100.3` |
| `print("abc" + "def")` | `abcdef` (jodinchha) |
| `print("abc" + 100.3)` | **truti** (akshar ra sankhya jodna mildaina) |

<!-- ne-cell: 864e596f | after-heading -->
### natijako udaharan

<!-- ne-cell: e18478f8 | after-heading -->
## Part 2 chal (variables)

<!-- ne-cell: 56698643 | after-heading -->
### chalama maan pugne kram

<!-- ne-cell: 56698643 | after-image:../../assets/diagrams/teach_variable_trace.png -->
chitra: tin lineko kod ra pratyek line sakinda chalama raheko maan. tesro linele `100.7 < 101.0` bhanne
sart tulna garchha; sart pugeko hunale `is_ok` ko maan `True` hunchha. yasko arth 100.7 bhanne sankhya aphain
"sahi" ho bhanne chahin hoina.

**dhyan dinuparne kura**

`=` ko arth "barabar" hoina. yasko arth **"dayanpattiko hisab garera bayanpattiko naam ma rakhne"** ho. dosro
linele `width_mm` lai dayanpatti padhchha, tyaspachhi nayan maan rakhchha.

tesro lineko `True` le **tyahan lekhieko sart (`width_mm < 101.0`) pura bhayo** bhanne matra janaunchha. sartalai
`width_mm < 100.0` banaunubhayo bhane tyahi 100.7 le `False` dinchha. `True` / `False` le "sahi / galat" hoina,
"sart pugyo / pugen" bhanne jabaph dinchha.

**sochnuhos**

- tesro line sakinda `width_mm` ko maan kati hunchha? ra `is_ok` `True` hunuko karan kun sart pura hunu ho?

<!-- ne-cell: 710318fa | after-heading -->
**chal bhaneko naam bhaeko bakas**
<!-- ne-pair: A variable is a named box -->

<!-- ne-cell: 710318fa -->
chal (variable) bhaneko maan rakhne **naam bhaeko bakas** ho. mathiko `sheet_width = 100.3` lekhieko kodale
"`sheet_width` bhanne bakasama `100.3` rakhne" bhanne arth dinchha. yo ganitako `=` (barabar) hoina.

**chalako naam rakhne niyam**

- Angreji akshar, angk ra `_` (underscore) prayog garna painchha
- angkabat suru garna paindain
- thula ra sana akshar farak maninchha (`Width` ra `width` beglai hun)
- surakshit shabd (`if`, `for`, `class` adi) prayog garna paindain

**ramro naamka udaharan:** `sheet_width`, `measured_thickness`, `defect_count`
**naramro naamka udaharan:** `a`, `x1`, `data2` — pachhi padhda arth thaha hundaina.

<!-- ne-cell: 2702d72d | after-heading -->
### natijako udaharan

<!-- ne-cell: 397ef12e | after-heading -->
## Part 3 sankhya ra ganana

<!-- ne-cell: 9fb383b4 | after-heading -->
**sankhyaka prakar ra chaar ganit**
<!-- ne-pair: Number types and the four operations -->

<!-- ne-cell: 9fb383b4 -->
Python ma mukhyatah dui prakarka sankhya hunchhan.

| prakar | udaharan | kahan prayog hunchha |
|---|---|---|
| purnank `int` | `3`, `-12`, `0` | ganne sankhya, piksel sankhya, kram sankhya |
| dashamalab `float` | `100.3`, `0.05`, `2.0` | napieko maan, anupaat, samay |

**sanchalak (operators)**

| chinh | arth | udaharan | natija |
|---|---|---|---|
| `+` | jodne | `100.0 + 0.3` | `100.3` |
| `-` | ghataune | `100.0 - 0.3` | `99.7` |
| `*` | gunan | `1.2 * 100` | `120.0` |
| `/` | bhaag | `120 / 1.2` | `100.0` |
| `//` | talatir raund garne bhaag (bhagaphal talatir) | `7 // 2` | `3` |
| `%` | bhaagko shesh | `7 % 2` | `1` |
| `**` | ghat (power) | `2 ** 3` | `8` |

> `/` ko natija sadhain dashamalab hunchha. `4 / 2` ko natija `2.0` ho (`2` hoina).

<!-- ne-cell: fig-teach_units_conversion | after-heading -->
### nap ra ekai paribartan

<!-- ne-cell: fig-teach_units_conversion | after-image:../../assets/diagrams/teach_units_conversion.png -->
chitra: ekai paribartan ra kampyuterbhitra sankhya kasari rakhinchha (yojanabaddha chitra). mathillo lahar bhautik
ekai ho, tallo lahar 2-adharit (binary) anuman ra raund garne niti ho.

**dhyan dinuparne kura**

tin kura chhuttaera sochnuhos. ① bhautik ekai (mm, px) ko paribartan, ② binary ma thyakkai lekhna nasakine
sankhyako anuman (`0.1 + 0.2` le `0.3` dindain), ③ nirikshan ma kahan raund garne. ② ganitako gun ho, ③
kampaniko niyam ho.

**sochnuhos**

- `0.1 + 0.2` le `0.3` nadinuko karan ekai paribartan ho ki sankhya bhandaran garne tarika?

<!-- ne-cell: acfe495e | after-heading -->
### natijako udaharan

<!-- ne-cell: acfe495e -->
lamo dashamalab bhaneko rakhieko sankhyako anumanko parinam ho. yasko bistrit byakhya pachhi "baikalpik:
parishuddhata ra bishesh sanchalak" bhaag ma aaunchha. yo ekai wa nirikshan-mapadand badalne karan hoina.

<!-- ne-cell: 8464d545 | after-heading -->
**akshar (string)**
<!-- ne-pair: Strings -->

<!-- ne-cell: 8464d545 -->
aksharako lahar (string) bhaneko `"..."` bhitra rakhieko aksharaharuko kram ho. `'...'` pani uhi ho. mathiko
`product_name = "PVC sheet"` jasto lekhai tyasaiko udaharan ho.

**prayah prayog hune kaam**

| kaam | udaharan | natija |
|---|---|---|
| jodne | `"PVC" + " sheet"` | `PVC sheet` |
| dohoryaune | `"ab" * 3` | `ababab` |
| lambai | `len("PVC")` | `3` |
| ansh nikalne | `"PVC sheet"[0:3]` | `PVC` |
| thulo akshar banaune | `"pvc".upper()` | `PVC` |

> kram sankhya **0 baat** suru hunchha. `[0:3]` ko arth "0 aundekhi 3 aun aghi samma" ho.

<!-- ne-cell: a1b4171f | after-heading -->
### natijako udaharan

<!-- ne-cell: fd0785c0 | after-heading -->
## Part 4 tulna ra saty/asaty maan

<!-- ne-cell: 1bde6236 | after-heading -->
**tulna garne sanchalak**
<!-- ne-pair: Comparison operators -->

<!-- ne-cell: 1bde6236 -->
tulna garda natija `True` wa `False` aaunchha. yi dui lai **saty/asaty maan (boolean)** bhaninchha.

`True` ko arth "**tyo sart pura bhayo**", `False` ko arth "**tyo sart pura bhaen**" ho. yo "sahi / galat"
bhanne nirnaya hoina. sart namiler `False` aunu programako truti pani nahun sakchha; tyasko arth maanle sart
pura garen bhanne matra ho.

| chinh | arth | udaharan | natija |
|---|---|---|---|
| `==` | barabar | `100.0 == 100.0` | `True` |
| `!=` | barabar hoina | `1 != 2` | `True` |
| `<` | sano | `1 < 2` | `True` |
| `<=` | sano wa barabar | `2 <= 2` | `True` |
| `>` | thulo | `1 > 2` | `False` |
| `>=` | thulo wa barabar | `2 >= 3` | `False` |

> **`=` ra `==` farak hun**. `=` le maan rakhchha, `==` le tulna garchha. nayan sikneharule sabaibhanda dherai
> yahi thaun ma galti garchhan.

<!-- ne-cell: fig-teach_assign_vs_compare | after-heading -->
### `=` ra `==` farak kaam hun

<!-- ne-cell: fig-teach_assign_vs_compare | after-image:../../assets/diagrams/teach_assign_vs_compare.png -->
chitra: maan rakhne (`=`) ra saty/asaty sodhne (`==`) ko farak, ra sanchchai ganana garieka chaar natija.

**dhyan dinuparne kura**

`=` bhaneko "dayanpattiko maan lai naam ma bandhne" baky ho; yasle aphain kehi dekhaundain. `==` le "barabar chha
ki chhaina" jancher True / False dinchha.

**sochnuhos**

- `a = 5` chalaunda kehi pani nadekhinuko karan ke ho?

chalaunuaghi anuman: `width = 100.3` le maan dekhaunchha? tyaspachhi `print(width == 100.3)` le ke garchha?
`width` matra 100.4 banaera tulnako True/False byakhya garnuhos.

talako chhoto cellle barabari matra janchchha. tyaspachhiko purano udaharanle arko prashna sodhchha: "farak mapadandbhitra
chha ki chhaina?"

<!-- ne-cell: 6892283a | after-heading -->
### natijako udaharan

<!-- ne-cell: d919c78b | after-heading -->
## Part 5 kibordabat maan line

<!-- ne-cell: e9217fc0 | after-heading -->
**`input()` ko prayog ra dhyan dinuparne kura**
<!-- ne-pair: How `input()` works, and its warnings -->

<!-- ne-cell: e9217fc0 -->
`input()` le kibordabat ek line padhchha. yasle **sadhain akshar (`str`)** pharkaunchha. mathiko kod udaharan hernuhos.

sankhyako rupama prayog garna **paribartan (conversion) garnaiparchha**. tyo paribartan asaphal huna sakchha. tyasaile
mathiko udaharanle `try` / `except` bhitra `float(text)` rakhchha.

`float("abc")` le `ValueError` dinchha. `input()` baat aeko maan **sadhain paribartan hunchha bhanne thannu hundaina**.

**yo talim ma `input()` prayog nagarne karan**

| karan | byakhya |
|---|---|
| sbatah chalaun mildaina | notebook ekaipatak chalaunda inputko pratikshama rokinchha |
| diieko maan notebook ma basdain | ke rakhnubhayo bhanne skrinama matra dekhinchha. pachhi uhi natija dohoryaun aphain lekhnuparchha |
| galti input ma kamajor | angk bahek aru lekhda `float()` le `ValueError` dinchha (mathiko `try` / `except` jasto upay chahinchha) |

tyasaile maan **selabhitrai lekher** chalaunuhos. maan badaler jati patak pani prayas garna saknuhunchha.

<!-- ne-cell: 2713acd6 | after-heading -->
## Part 6 truti ra dibaging

<!-- ne-cell: 0f6a8f0a | after-heading -->
**prayah dekhine paanch truti**
<!-- ne-pair: The five errors you will meet most -->

<!-- ne-cell: 0f6a8f0a -->
truti "asaphalata" hoina, "jankari" ho. namaile karan bataunchha.

| truti | arth | prayah hune karan |
|---|---|---|
| `SyntaxError` | byakaran milen | `if x > 1` ma `:` chhutnu, koshthak naband hunu |
| `NameError` | tyo naam paribhashit chhaina | chalako naam ma taip galti, aghillo cell nachalaieko |
| `TypeError` | prakar milen | `"abc" + 100` (akshar ra sankhya) |
| `ValueError` | maan milen | `float("abc")` (sankhya nabhaeko akshar) |
| `IndexError` | dayarabahir | 3 bata tattb bhaeko soochi ma `[10]` le pugna khojnu |

**truti sandesh padhne tin charan**

1. **antim line**: trutiko prakar (`NameError` adi)
2. **tyasko mathiko line**: ke garna khojda asaphal bhayo
3. **`---->` bhaeko line**: programako kati number line (Jupyter ma `line 3` adi)

<!-- ne-cell: fig-teach_traceback_annotated | after-heading -->
### traceback kasari padhne

<!-- ne-cell: fig-teach_traceback_annotated | after-image:../../assets/diagrams/teach_traceback_annotated.png -->
chitra: 0 le bhaag garda aune traceback, kun kram ma padhne bhanera chinh lagaieko (yojanabaddha chitra).

**dhyan dinuparne kura**

yo udaharan **Python ka sadharan sankhya lai** 0 le bhaag garda aune truti ho. bhasha wa sankhyako prakar
farak bhae (jastai NumPy ko array ganana) truti naai `inf` wa `nan` pani aun sakchha. "junasukai bhashama sadhain
asaphal hunchha" bhanne hoina.

**sochnuhos**

- NumPy ma `1.0 / 0.0` ganana garda truti aaunchha ki `inf` aaunchha?

<!-- ne-cell: 7ed0594d | after-heading -->
### natijako udaharan

<!-- ne-cell: 90a7e4fa | after-heading -->
**dibag garne kram**
<!-- ne-pair: A debugging procedure -->

<!-- ne-cell: 90a7e4fa -->
truti aepachhi yahi kram ma jaanchnuhos.

1. **kun cell** ma bhayo bhanera hernuhos (`In [ ]` ko number)
2. sandeshko **antim line** padhnuhos
3. **aghilla cellharu chalaiyo ki** jaanchnuhos
4. shangka lageko maan **`print()` garnuhos** — yo sabaibhanda bharapardo tarika ho
5. sudharepachhi **tyo cell ra tyasko natija prayog garne cellharu** feri chalaunuhos. kati samm asar parchha thaha
   nabhae **kernel punah suru garera aawashyak cellharu mathibat kramaisang chalaunuhos**

**euta cell matra sudharer feri chalaunda purano natija rahirahanchha.** notebookle mathibat talasamm abastha banaunchha,
tyasaile function wa chal sudharda pahile nai ganana bhaisakeko purano natija skrinama tyasai rahanchha. purano ra
nayan natija misinda karan chhutyaun sakindaina.

<!-- ne-cell: clarity-optional-operators | after-heading -->
### baikalpik: parishuddhata ra bishesh sanchalak

<!-- ne-cell: clarity-optional-operators -->
pahilo charan ma naam → sankhya → print → ganana → tulna → True/False abhyas garnuhos. talaka kura dosro
patakama padhne purak tippani hun. sima najikako napieko maan lai sochabicharabina raund garera pas banaunu
hundaina. aawashyak rijolyusan ra nirnaya niti pahile nai toknuhos.

<!-- ne-cell: 1b60ce34 | after-heading -->
**dashamalab ganana ma truti aaunchha**
<!-- ne-pair: Floating-point rounding error -->

<!-- ne-cell: 1b60ce34 -->
mathiko natija ma `0.29999999999999716` dekhnubhayo? `100.3 - 100.0` ko ganitiy uttar `0.3` ho, tar Python
le `0.3` dekhaundain.

yo Python ko bigreko gun hoina. **computerle dashamalab sankhya 2-adharit (0 ra 1 ko kram) ma rakhchha**, tyasaile
yasto hunchha. 0.1 ra 0.3 dubailai 2-adharitama simit angkale thyakkai lekhna sakindaina.

**yo ekaiko kurabhanda farak ho.** yo truti mm wa cm ko kura hoina; "eutai sankhya kun dhanchama rakhieko chha"
bhanne kura ho. sankhya ma ekaiko jankari hundaina. mm ma napeko thaner cm ma ganana garda pani karyakramale
truti dindain.

**utpadan nirikshan ma yasko byabahar (yo talimko niti)**

1. napieko maanko **rijolyusan** toknuhos (jastai 0.001 mm samm padhne, wa 1 pixel = 0.05 mm).
2. sima tulna ma **ghoshit mapadandako sima** (jastai 11.8 mm wa badhi ra 12.2 mm wa kam) tyasai prayog garnuhos.
   pas banaun mapadand pharakilo banaunu hundaina.
3. raund garne niti **pahile nai toker abhilekh garnuhos**. yo talimka abhyas ma `round(farak, 6)` prayog hunchha.
4. asamanatako chinhale truti hataundain. raund garepachhi simabhanda ali bahirako maan bhitra parna sakchha. sima
   najik raund niti ra napako anishchitata sangai jaanchnuhos.

talako `1e-9` bhaneko aphain chhanieko sangkhyatmak sahyatasang garine euta khelauna-tulna ho. yo utpadanako
pas/phel mapadand hoina.

<!-- ne-cell: 31fc6d72 | after-heading -->
### natijako udaharan

<!-- ne-cell: clarity-floor-notes | after-heading -->
#### rinatmak sankhyako bhaag ra assignment expression

<!-- ne-cell: clarity-floor-notes -->
> `//` bhaneko **talatir raund garne bhaag (floor division)** ho. yasle purnank bhaag matra nikaldain, bhagaphalalai
> **talatir (rinatmak anantatatir)** raund garchha. `7 // 2` ko natija `3` ho, tar `-7 // 2` ko natija `-4` hunchha
> (`-3` hoina). `//` dashamalabama pani chalchha: `7.0 // 2` ko natija `3.0` ho. purnank chahie `int()` le badalnuhos.

`:=` bhaneko maan pani pharkaune uchcha-stariy assignment expression ho. yo paath ma prayog garindain.

<!-- ne-cell: cc676dcd | after-heading -->
## abhyas

<!-- ne-cell: 7d48e791 | after-heading -->
**abhyas 1 (adharabhut): aphno parichay dekhaune**
<!-- ne-pair: Exercise 1 (basic): print an introduction -->

<!-- ne-cell: 7d48e791 -->
chalama "naam", "bibhag" ra "ajako sikai lakshya" rakher `print()` le 3 line dekhaunuhos. euta line Nepali ma
ra dui line Angreji ma rakhnuhos.

**sakieko manine abastha:** natija ma namunako akshar hoina, tapainko aphnai bastabik jankari dekhinuparchha.

<!-- ne-cell: audit-teach_mass_units_chain | after-heading -->
### kod kasari padhne

<!-- ne-cell: audit-teach_mass_units_chain | after-image:../../assets/svg/teach_mass_units_chain.svg -->
chitra: kshetraphal ra ayatan chhutyaunuhos. uttar aphain ganana garnuhos. (ganana garieko sansleshit udaharan ra
yojanabaddha chitra; model ko bastabik napieko natija hoina.)

**dhyan dinuparne kura**

kshetraphal ra ayatan farak hun. uttar aphain ganana garnuhos. input ra paribartan bhaeko maan aunlale dekhaundai
pachhyaunuhos.

**sochnuhos**

motai matra dobbar banaunda kshetraphal ra taul kasari badlinchha?

<!-- ne-cell: clarity-mass-chain | after-heading -->
#### ekaiko shringkhala (adarsh ganana)

<!-- ne-cell: clarity-mass-chain -->
mathiko chitrakai input prayog bhaeko chha. yi napieka natija hoinan. pahile kshetraphal kina dui lambaiko gunan ra
ayatan kina tin lambaiko gunan hunchha, anuman garnuhos.

`1300 mm × 2500 mm = 3,250,000 mm² = 3.25 m²`

`3,250,000 mm² × 0.35 mm = 1,137,500 mm³ = 1137.5 cm³`

`1137.5 cm³ × 1.4 g/cm³ = 1592.5 g = 1.5925 kg`

abhyaska khali thaun aphain bharnuhos. sano prayog: motai matra dobbar banaunda kshetraphal ra taul ke hunchha?

<!-- ne-cell: 3ab12dde | after-heading -->
**abhyas 2 (madhyam): chaudai, lambai ra kshetraphal ganana**
<!-- ne-pair: Exercise 2 (intermediate): compute width, length and area -->

<!-- ne-cell: 3ab12dde -->
chaudai 1,300 mm ra lambai 2,500 mm bhaeko sit chha.

1. kshetraphal mm² ma dekhaunuhos
2. kshetraphal m² ma badaler dekhaunuhos (1 m² = 1,000,000 mm²)
3. prati sit 0.35 mm motai ra 1.4 g/cm³ ghanatb maner taul kg ma anuman garnuhos

sanket: taul = ayatan × ghanatb. pahile mm lai cm ma badalnuhos.

**sakieko manine abastha:** tinai maan ekaisahit dekhaieka chhan.

<!-- ne-cell: 1ccd85ef | after-heading -->
#### abhyas 3 (baikalpik): truti sudharne

<!-- ne-cell: 1ccd85ef -->
talako cell ma **janajan tinabata galti** bhaeko karyakram chha. pahile tyasai chalaera **truti sandesh** padhnuhos.

tyaspachhi "uttar lekhne" cell ma **sahi sudharieko karyakram** lekhnuhos. sudharepachhi karan ke thiyo bhanera
comment ma lekhnuhos.

**sakieko manine abastha:** uttar cellle OK/NG dekhaunchha ra tinabata karan comment lekhieka chhan.

<!-- ne-cell: 95857ac2 | after-heading -->
#### bujhai jaanchne prashna

<!-- ne-cell: 95857ac2 -->
1. `=` ra `==` ko farak byakhya garnuhos.
2. `100.3 - 100.0` le `0.3` nadinuko karan ke ho?
3. `a` akshar ra `b` sankhya hunda `print(a, b)` ra `print(a + b)` ma ke farak chha?
4. `NameError` dekhda pahile ke janchnuhunchha?
5. chalako naam `x1` nabhai `measured_width_mm` rakhda ke phaida hunchha?

<!-- ne-cell: b791fe79 | after-heading -->
## samasya parema

<!-- ne-cell: b791fe79 -->
truti aepachhi pahile "kun cell ma", "kun line ma", "ke sandesh ayo" bhanera lekhnuhos. bujhaunuparne kaam ma pani
tyahi abhilekh rakhnuhos.

| lakshan | ke garne |
| --- | --- |
| `SyntaxError: invalid syntax` | prayah `:` chhutnu, koshthak naband hunu wa purna-chaudaiko (full-width) khali thaun hunu karan ho. line number jaanchnuhos. |
| `NameError: name 'x' is not defined` | chalako naamko hijje wa aghillo cell nachalaieko hunu karan ho. |
| `IndentationError` | lineko surubatako khali thaun mileko chhaina. eutai block bhitra sabai line uti nai tal sarnuhos (yo talim ma 4 khali thaun). tab ra space misaunu hundaina. |
| `TypeError: can only concatenate str (not "int") to str` | akshar ra sankhya `+` le jodna khojieko chha. `print("a", 1)` wa f-string prayog garnuhos. |
| natija `0.29999999999999716` aaunchha | yo dashamalabako truti ho, bigreko ganana hoina. dekhauna `round()` le raund garnuhos; tulna "tokieko angkama raund garepachhi" wa "sahyatasahitako asamanata" le garnuhos. raund niti pahile nai toker abhilekh garnuhos. |
| Japani akshar `??` wa `□□` dekhinchha | kansolako character code ko samasya huna sakchha. notebook ma samanyatah yasto hundaina. |

<!-- ne-cell: 6111fb35 | after-heading -->
## sampannata janchasuchi

<!-- ne-cell: 6111fb35 -->
**aniwarya** ra **baikalpik** kaam chhuttachhuttai rakhieka chhan. **abhyas 3 (baikalpik)** baikalpik ho; nagare pani
pura maninchha. samay banki bhae ma matra garnuhos.

sabai aniwarya bundama chinh lagepachhi yo notebook pura hunchha.

**aniwarya**

- [ ] Part 1–Part 6 padher sabai code cell chalaen
- [ ] abhyas 1–2 (aniwarya) garen
- [ ] `=` ra `==` ko farak byakhya garna sakchhu
- [ ] bujhai jaanchne 5 prashnako uttar dien
- [ ] truti abhilekh rakhen
- [ ] notebook surakshit garen

**baikalpik**

- [ ] abhyas 3 (baikalpik) ka tinabata galti aphain sudharen

<!-- ne-cell: f428ef26 | after-heading -->
## thap adhyayan (baikalpik)

<!-- ne-cell: f428ef26 -->
### sandarbha lingk

- [Python adhikarik tutorial (Japani)](https://docs.python.org/ja/3/tutorial/)
- [Python ka built-in prakar](https://docs.python.org/ja/3/library/stdtypes.html)
- [Floating point gananako gun](https://docs.python.org/ja/3/tutorial/floatingpoint.html)

### thap chunauti (aniwarya hoina)

`print(f"{0.1:.20f}")` chalaera 0.1 bhitri rupama kasari rakhieko chha hernuhos.
