<!--
Nepali anuwad / Nepali translation source for
notebooks/Day02_Python_OpenCV/Day02_02_Conditions_Loops_Functions.ipynb
-->
# din 2 notebook 02 — Nepali anuwad

<!-- ne-cell: 7f7e8a41 | after-heading -->
# din 2 notebook 02: sart, dohorine kaam ra function

<!-- ne-cell: 7f7e8a41 -->
## sikai lakshyaharu

| Nepali |
| --- |
| 1. `if` / `elif` / `else` le sart anusar farak kaam garna sakne. |
| 2. `for` lupale dherai maan ma eutai kaam garna sakne. |
| 3. soochi (list) banaera tattb nikalna sakne. |
| 4. parameter ra return maan bhaeko function lekhna sakne. |
| 5. apabad (exception) samater galat input sanbhalna sakne. |

## yo notebookko adharabhut jankari

| bishay | biwaran |
| --- | --- |
| sikai samay (anuman) | 115 minet |
| kathinai | surubati tah |
| poorwashart | din 2 notebook 01 sakieko hunuparchha. |
| aawashyak laibreri | numpy, matplotlib, pillow |
| prayog hune kernel | aivision |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 2](../../COURSE_SYLLABUS.md#day2) |

### bujhaunuparne kaam

| Nepali |
| --- |
| napieko maan jaanchne karyakram (dherai nap sanbhalne) |
| input jaanch bhaeko function |

<!-- ne-cell: c09bb5e1 | after-heading -->
## yo notebook kahan parchha

<!-- ne-cell: c09bb5e1 -->
| bishay | biwaran |
| --- | --- |
| din | din 2 |
| ajako kram | ajako notabukamadhye 2 / 3 |
| lagne samay | 115 minet |
| poorwashart | `Day02_01_Python_Basics.ipynb` |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 2](../../COURSE_SYLLABUS.md#day2) |

dinko samayatalika `COURSE_SYLLABUS.md` ma eutai thaun ma chha. yo notebook tyasko euta bhaag matra ho, aphno
chhuttai samayatalika rakhdain. samay thaha nabhae pahile tyahi file hernuhos.

<!-- ne-cell: audit-learning-loop | after-heading -->
### anuman garnuhos, chalaunuhos, hernuhos, byakhya garnuhos

<!-- ne-cell: audit-learning-loop -->
function le input linchha ra `return` le natija pharkaunchha. sartale saty ho ki asaty janchchha. mahattwapurna cell
chalaunuaghi input, kaam ra natija ek-ek bakyama lekhnuhos. pahile anuman lekher cell chalaunuhos ra maan wa
chitra hernuhos. napieko maan matra badaler feri anuman gari chalaunuhos. janajan rakhieka truti ra
nasakieka abhyaska nirdeshan pachhyaunuhos.

<!-- ne-cell: 59bedbb1 | after-heading -->
## Part 0 tayari

<!-- ne-cell: 7f81201b | after-heading -->
## Part 1 sart anusar bandne

<!-- ne-cell: 0c826365 | after-heading -->
**`if` le "yadi yasto bhae" lekhne**
<!-- ne-pair: Writing 'if' with `if` -->

<!-- ne-cell: 0c826365 -->
`if` ko arth ho "yadi sart pura bhayo bhane yo kaam garne".

**aniwarya dui kura**

1. sartapachhi **`:` (colon)**
2. arko lineko **indentation (lineko surubatama khali thaun)**. eutai block bhitra sabai line uti nai tal
   sarnuparchha

kati khali thaun rakhne bhanne Python ko byakaranale tokdain, tar **eutai block bhitra farak-farak matra rakhda
`IndentationError`** aaunchha. padhna sajilo hos bhanera yo talim ma sadhain **4 khali thaun** prayog garinchha (tab
prayog garindain).

<!-- ne-cell: clarity-independent-spec | after-heading -->
#### arko simako udaharan

<!-- ne-cell: clarity-independent-spec -->
pahile chitra baat 12.0±0.2 mm ko sima siknuhos. tyaspachhika mukhy kodama 100.0±0.5 mm prayog hunchha.
chitrako sankhya pachhiko kodama namisaunuhos.

<!-- ne-cell: fig-teach_tolerance_boundary | after-heading -->
### sima "bhitra" parchha ki pardaina

<!-- ne-cell: fig-teach_tolerance_boundary | after-image:../../assets/diagrams/teach_tolerance_boundary.png -->
chitra: 12.0 ± 0.2 mm ko sima ra sanchchai tulna garieka 5 maanko nirnaya. 12.200 mm sima bhitra parchha, tyasaile
OK ho.

**dhyan dinuparne kura**

mapadandama "11.8 wa badhi ra 12.2 wa kam" lekhieko chha bhane simako maan aphain pani samabesh hunchha. samabesh hune
ki nahune kura **mapadand kasari lekhieko chha** bhanne ma nirbhar chha; kodama `<=` ra `<` le tyahi janaunchhan. napako
rijolyusan ra nirnaya garnuaghi raund garne niti pani pahile nai tay garnuhos.

**sochnuhos**

- 12.2005 mm lai 3 dashamalabama raund garera nirnaya garda natija kasari badlinchha?

<!-- ne-cell: fig-teach_condition_branch | after-heading -->
### sartale kaam kasari bandchha

<!-- ne-cell: fig-teach_condition_branch | after-image:../../assets/diagrams/teach_condition_branch.png -->
chitra: napieko maan 12.14 mm lai sart 11.8 ≤ x ≤ 12.2 ma pathaunda hune kram, ra 4 maan sanchchai haler hereko
natija (yojanabaddha chitra).

**dhyan dinuparne kura**

badaline kura dekhaine akshar matra ho; sart eutai ho. simako maan 12.20 mm "bhitra" parne hunale OK hunchha.
**input maan badalnu** ra **mapadand badalnu** farak kaam hun.

**sochnuhos**

- mapadand nabadali 12.30 mm lai OK banaune upay chha?

<!-- ne-cell: 9058ead5 | after-heading -->
### sbikrit mapadand nabadali rakhnuhos

<!-- ne-cell: 9058ead5 -->
**yo arko simako udaharan ho. mukhy kod udaharanko 100.0±0.5 mm bhanda farak mapadand ho.**
mathiko chitrako sbikrit mapadand **11.8 mm wa badhi, 12.2 mm wa kam** mai sthir rakhnuhos. 12.200 mm sima
bhitra parne hunale OK, 12.201 mm NG ho. namilne saman pas banaun maan raund garne wa mapadand, sart badalne
kaam garnu hundaina. arko saman napnu ra abashyakata (mapadand) badalnu farak kura hun.

byabaharik tippani: aupacharik rupama mapadand badalna dijain wa grahakako sbikriti, sanshodhan number, lagu hune
miti ra abhilekh chahinchha. yo paath ma "maan badalnu" bhannale napieko input matra janaunchha. anuman: 12.201 ko
satta 12.200 ayo bhane ke badlinchha?

<!-- ne-cell: audit-teach_if_live_trace | after-heading -->
### kod kasari padhne

<!-- ne-cell: audit-teach_if_live_trace | after-image:../../assets/svg/teach_if_live_trace.svg -->
chitra: dekhaunaka lagi garieko raundingalai nirnayako niyam banaindain. (ganana garieko sansleshit udaharan ra
yojanabaddha chitra; model ko bastabik napieko natija hoina.)

**dhyan dinuparne kura**

dekhaunaka lagi garieko raunding nirnayako niyam hoina. input ra paribartan bhaeko maan aunlale pachhyaunuhos.

**sochnuhos**

100.5001 mm banaunda kun shakha chalchha?

<!-- ne-cell: clarity-main-spec | after-heading -->
#### mukhy udaharan: input → sart → natija

<!-- ne-cell: clarity-main-spec -->
sbikrit mapadand 100.0±0.5 mm nai sthir rakher napieko maan 100.3 mm baat OK/NG nikalnuhos. chalaunuaghi
farak ra nirnaya anuman garnuhos. chalaepachhi 100.6 banaera, mapadand nabadali NG kina ayo byakhya garnuhos.

<!-- ne-cell: f831e7cd | after-heading -->
### natijako udaharan

<!-- ne-cell: 9ca817a3 | after-heading -->
**`elif` le tin wa badhi bhaag ma bandne**
<!-- ne-pair: Splitting into three or more with `elif` -->

<!-- ne-cell: 9ca817a3 -->
tin wa badhi bhaag chahie `elif` (else if) prayog garnuhos. sart **mathibat kramaisang** janchinchha ra
**pahilo mileko kaam matra** chalchha. kram mahattwapurna chha: `if x < 10` pahile lekhiyo bhane `x = 5` kahilyai
`elif x < 20` samm pugdain.

<!-- ne-cell: clarity-severity | after-heading -->
#### shreni ra pas/phel farak hun

<!-- ne-cell: clarity-severity -->
A/B/C/D bhaneko kati tadha gaeko bhanne bargikaran ho. halako mapadand ±0.5 mm ma **A ra B OK, C ra D NG** hunchhan.
pahileko `C (warning / 注意)` bhanne natija jastako tastai rakhieko chha, tar **C mapadandabahir (jaanch aawashyak) ho
ra pathaun milne saman hoina**. anuman: 0.6 mm farak kun shrenima parchha ra pas/phel ke ho? chalaepachhi 0.5 mm
sang tulna garnuhos.

<!-- ne-cell: f86492fe | after-heading -->
### natija kasari padhne

<!-- ne-cell: f86492fe -->
harek line ma shreni ra `spec` chhuttachhuttai padhnuhos. ±0.60 farak C ho, tar NG ho. ±0.15 ra 0 A bhaera OK hun;
±2.00 D bhaera NG ho.

<!-- ne-cell: b0cf9283 | after-heading -->
## Part 2 soochi ra dohorine kaam

<!-- ne-cell: 7584722b | after-heading -->
### 5 bata nap kramaisang jaanchne

<!-- ne-cell: 7584722b | after-image:../../assets/diagrams/teach_loop_trace.png -->
chitra: yahi notebookka 5 nap (100.0, 100.3, 99.7, 100.6, 99.4) lai uhi mapadand (100.0 mm ± 0.5 mm) ma
kramaisang jancheko abhilekh. NG i=3 ra i=4 hun.

**dhyan dinuparne kura**

lup kunai naulo kura hoina. **eutai nirnaya, maan farak parer 5 patak dohoryaune** matra ho. harek patak "ahile
kun maan chha" bhanera janchnu nai sip ho. thik talako kodale **chitrakai maan ra mapadand** prayog garchha, tyasaile
natija chitrako line sang milchha.

Part 2 ko pachhillo stepper le **arko data (12.xx)** ma uhi kura dekhaunchha. maan farak bhae pani garine kaam uhi ho.

**sochnuhos**

- chitra ma NG i=3 ra i=4 hun. dubaima `|value - 100.0| = 0.6` chha ra `0.6 <= 0.5` pugdain. duibata kina?
- thik talako kod chalaunda chitrakai 5 line aaunchha? pahile anuman garnuhos.

<!-- ne-cell: 7d26f19c | after-heading -->
**soochi bhaneko maanharuko shringkhala**
<!-- ne-pair: A list is a sequence of values -->

<!-- ne-cell: 7d26f19c -->
soochi (list) le dherai maan eutai thaun ma rakhchha. `measurements = [100.0, 100.3, 99.7]` jasto lekhinchha.

| kaam | udaharan | natija |
|---|---|---|
| sankhya | `len(measurements)` | `3` |
| tattb nikalne | `measurements[0]` | `100.0` |
| antim | `measurements[-1]` | `99.7` |
| dayara | `measurements[0:2]` | `[100.0, 100.3]` |
| thapne | `measurements.append(100.1)` | antama thapinchha |
| jod | `sum(measurements)` | jamma |
| thulo | `max(measurements)` | adhikatam |

> kram sankhya 0 baat suru hunchha. `measurements[1]` bhaneko **dosro** tattb ho.

<!-- ne-cell: c534d731 | after-heading -->
### natijako udaharan

<!-- ne-cell: a0529062 | after-heading -->
**`for` le sabai tattbama eutai kaam garne**
<!-- ne-pair: Processing every element with `for` -->

<!-- ne-cell: a0529062 -->
`for` ko arth ho "suchibhitraka tattb ek-ek garera nikaler uhi kaam garne".

- lupako chal `value` harek patak **nayan chal banieko hoina**; **uhi naam lai** arko tattbasang bandhinchha (naam
  je pani rakhna sakinchha)
- soochi ma jati tattb chhan tyati patak dohorinchha
- **tal sarieko bhaag** matra dohorinchha
- farak inputle uhi natija din pani sakchha (100.0 ± 0.5 mm mapadandama 100.2 mm ra 100.4 mm dubaile `"OK"` dinchhan)

"100 bata nap ek-ek garera jaanchne" — yahi sbachalanako adharabhut dhancha ho.

<!-- ne-cell: audit-tolerance-policy | after-heading -->
### sima ra dekhaine maan

<!-- ne-cell: audit-tolerance-policy -->
adharabhut udaharanle farak naraund gari `abs(measured_mm - nominal_mm) <= tolerance_mm` le janchchha. 99.5 ra
100.5 mm OK, 100.5001 mm NG hun. dekhaine dashamalab sankhya, napne yantrako rijolyusan ra pas/phel niti
chhuttachhuttai kura hun. `2.1 - 2.0` jasta dashamalab binary ma thyakkai lekhna nasakine huna sakchha. pachhi aune
motai abhyasko raunding tyo abhyas ma matra lagu hune spasht niti ho, adharabhut udaharan ma hoina.

<!-- ne-cell: clarity-loop-predict | after-heading -->
#### uhi 5 nap pachhyaune

<!-- ne-cell: clarity-loop-predict -->
input `measurements_mm` ho; harek patak farak ganana ra mapadand tulna hunchha; natija ek line ho. anuman: NG kun
kram sankhya ma parchha? talako talika mathiko chitra sang line-dar-line milaunuhos.

<!-- ne-cell: 13daa786 | after-heading -->
### natijako udaharan

<!-- ne-cell: 13daa786 -->
chihnasahitako farak ra simabhitra chha ki chhaina bhanne line pani harek nirnayapachhi dekhainchha.

<!-- ne-cell: clarity-transfer-stepper | after-heading -->
#### arko udaharan: 12.50±0.10 mm

<!-- ne-cell: clarity-transfer-stepper -->
talako stepper matra farak mapadand ra farak nap prayog garchha. mukhy if→for→def udaharan 100.0±0.5 mm mai rahanchha.
udaharan pherda adhar maan, sahyata ra ekai feri padhnuhos.

<!-- ne-cell: bc94f88f | after-heading -->
#### lup ek-ek paila gardai herne

<!-- ne-cell: bc94f88f -->
lup bhaneko "uhi nirnaya, maan farak parer dohoryaune" matra ho. talako stepper ma **ahile kun maan herieko
chha** ek-ek garera jaanchnuhos.

| paila | ke herne |
|---|---|
| `i = 0` | pahilo nap ra sart saty bhayo ki bhaen |
| `i = 2` | \|12.38 − 12.50\| = 0.12 > 0.10 hunale NG |
| `i = 3` | \|12.92 − 12.50\| = 0.42 hunale NG. NG bhae pani tadha bhaeko farak chha |
| `i = 4` | lupako antim patak |

widget chalna nasake talako parameter cellle uhi kaam garchha.

<!-- ne-cell: 83428140 | after-heading -->
## Part 3 function (phankshan)

<!-- ne-cell: clarity-function-transfer | after-heading -->
#### chitra arko udaharan ho

<!-- ne-cell: clarity-function-transfer -->
talako chitra ma matra stepper kai 12.50±0.10 mm prayog bhaeko chha. adharabhut function le 100.0±0.5 mm prayog garchha.
pahile `judge_width(100.3)` ra `judge_width(100.6)` ko natija anuman garnuhos, tyaspachhi chitra ma lagu garnuhos.

<!-- ne-cell: c0809d54 | after-heading -->
### function bhaneko "input → niyam → natija"

<!-- ne-cell: c0809d54 | after-image:../../assets/diagrams/teach_function_io.png -->
chitra: input (napieko maan, adhar maan, sahyata) liera tokieko kram ma ganana gari euta maan pharkaune bakas.
nap 12.55, adhar 12.5, sahyata 0.1 bhae `|12.55 - 12.5| = 0.05 <= 0.10` hunale **OK**; 12.92 bhae
`0.42 > 0.10` hunale **NG** (sabai ganana garieka maan).

**dhyan dinuparne kura**

function banaepachhi eutai niyam dherai patak lekhnu pardaina. maan pherer bolaunda harek patak uhi kram chalchha. input
badalinda natija badalin pani sakchha, **uhi pani rahan sakchha** (100.2 mm ra 100.4 mm dubai `"OK"`).

**natija tinai inputle tay garchha.** sahyata nalekhie tyo bakasale uttar din sakdain.

**sochnuhos**

- chitraka dui udaharan ma natija OK ra NG kina farak bhayo? tinamadhye kun input farak thiyo?

<!-- ne-cell: 0838864d | after-heading -->
### chitrako udaharan kodale jaanchne

<!-- ne-cell: 0838864d -->
chitraka tin input tyasai `judge_width` ma pathaun sakinchha: nap 12.55, adhar maan (yahan mapadandako kendra)
12.5, sahyata 0.1. farak 0.05 hunale sahyatabhitra parchha ra natija `"OK"` aaunchha. **nap 12.92 banaunda** farak 0.42
hunchha, sahyatabhanda bahir, tyasaile uhi function le `"NG"` pharkaunchha. natija tinai inputle tay garne hunale
tinai sangai padhnuhos.

yo notebookko `judge_width` ma adhar maanko purbanirdharit 100.0 mm ra sahyatako 0.5 mm chha. tyasaile
`judge_width(12.55)` lai "100.0 ± 0.5 mm mapadandama 12.55 mm" bhanera padhchha ra NG dinchha. chitrako udaharan
chalaun `judge_width(12.55, nominal_mm=12.5, tolerance_mm=0.1)` jastai **adhar maan ra sahyata pani** pathaunuhos.

<!-- ne-cell: abe05345 | after-heading -->
**function bhaneko "naam diieko kaam"**
<!-- ne-pair: A function is a named block of processing -->

<!-- ne-cell: abe05345 -->
function le barambar prayog hune kaam lai naam dinchha.

| shabd | arth | udaharan |
|---|---|---|
| `def` | function paribhashit garchha | `def judge_width(...)` |
| parameter (aupacharik naam) | **paribhasha lekhne thaun ma** lekhine naam; bolaunda maan paunchha | paribhashako `measured_mm` |
| argument (pathaieko maan) | **bolaune thaunle** dine maan | `judge_width(100.3)` ko `100.3` |
| return maan | function le pharkaune natija | `"OK"` |
| `return` | maan pharkaera function antya garchha | `return "OK"` |

`judge_width(measured_mm=100.3)` jastai **namasahit pathaunda** kun maan kun parameter ho padhna sajilo hunchha.
tar yasle maan aphain sahi chha bhanne praman dindain.

**function prayog garne tin phaida**

1. **uhi kod barambar lekhnu pardaina**
2. **naamle arth bujhinchha** (`judge_width(100.3)` herdai bujhinchha)
3. **sudhar eutai thaun ma** (niyam badaliyo bhane function bhitra matra badalne)

<!-- ne-cell: fig-teach_definition_vs_call | after-heading -->
### paribhasha ra bolaune kaam farak

<!-- ne-cell: fig-teach_definition_vs_call | after-image:../../assets/diagrams/teach_definition_vs_call.png -->
chitra: `def` le niyamko naam matra rakhchha, bolaepachhi matra bhitrako kaam chalchha (nirnaya ganana garieka maan).

**dhyan dinuparne kura**

function paribhashit gardaima kehi chaldain. bolaunda maan pathainchha. paribhashako naam (parameter) ra bolaune
thaunko maan (argument) farak hun; kram wa naamle tini talamel garinchha.

**sochnuhos**

- function paribhashit matra garda bhitrako kaam chalchha?

<!-- ne-cell: 335a1b26 | after-heading -->
### natijako udaharan

<!-- ne-cell: 335a1b26 -->
> **maan tulna garne niti**
>
> `2.1 - 2.0` ko natija `0.10000000000000009` aaunchha. tyasai tulna garda 2.1 mm "±0.1 mm bhitra" hundahundai
> pani NG banchha. tyasaile yo abhyas ma **farak lai `round(farak, 6)` le raund garera matra** tulna garne sahamati
> rakhieko chha (mathiko kodama pani tyahi chha).
>
> yo **yo talimko abhyaska lagi banaiyeko sahamati** ho; junasukai maan ma surakshit hunchha bhanne hoina. raund garda
> simabhanda ali bahirako maan bhitra parna sakchha (jastai tallo sima 11.8 mm sang 11.7999999 mm). dashamalab sima ma
> thyakkai nirnaya chahie purnankko sano ekai (µm jastai) ma napne wa `decimal.Decimal` prayog garne
> bikalp sochnuhos. simako bhitra ra bahir dubai parikshan garnuhos ra **kati dashamalabama raund gariyo** abhilekh
> rakhnuhos.

<!-- ne-cell: 8ab30612 | after-heading -->
## Part 4 apabad sanbhalne

<!-- ne-cell: 8ab30612 -->
**yahan baat prashikshakasangai garine dosro chakra suru hunchha.** pahilo aniwarya bato if→for→def ho. input thik chha
ki chhaina bhanne ra mapadandbhitra chha ki chhaina bhanne nirnaya farak hun.

```text
kachcha input / raw input -> float ma badalne / parse
  asaphal / failure -> karan abhilekh garera asbikar garne / log reason, reject input
  saphal / success -> many sankhya / valid number -> sthir mapadand / fixed tolerance -> OK or NG
```

anuman: khali akshar NG saman ho ki napako input truti? talako natijako `rejected` ma karan hernuhos.
sano prayog: `"not-a-number"` ko satta `"100.6"` rakhda input many hunchha tar saman NG pani huna sakchha.

<!-- ne-cell: 77f645e0 | after-heading -->
**`try` / `except` le asamanya abastha sanbhalne**
<!-- ne-pair: Handling abnormal input with `try` / `except` -->

<!-- ne-cell: 77f645e0 -->
karyasthalama sadhain sahi maan aundain. khali thaun, akshar, `None`, atyadhik thulo maan aun sakchha.

`try` / `except` prayog garda **trutile rokinuaghi** nai byabastha garna sakinchha.

mahattwapurna kura: **truti lukaunu hundaina**. "jaso bhae pani `except: pass`" kahilyai nalekhnuhos.
**ke bhayo bhanera abhilekh rakhnu** nai sahi tarika ho.

<!-- ne-cell: ec5196af | after-heading -->
### natijako udaharan

<!-- ne-cell: ec5196af -->
66.7% bhaneko 6 inaputamadhye **4 bata sankhyako rupama padhna sakiyo** bhanne anupaat ho (4 ÷ 6 = 66.7%). yo
nirikshanko "recall" hoina. Recall bhaneko nachhutai bhetieka doshko anupaat (TP ÷ (TP + FN)) ho, jun din 4 pachhi
sikainchha.

<!-- ne-cell: 5eff1e70 | after-heading -->
**input jaanch bhaeko function**
<!-- ne-pair: A function with validation -->

<!-- ne-cell: 5eff1e70 -->
byabaharama function ko prabeshadbaramai maan janchinchha. yas lai **input jaanch (validation)** bhaninchha.

janchnuparne kuraka udaharan:

- sankhya ho ki (`str` wa `None` aeko chhaina?)
- sahyata dhanatmak chha ki
- yatharthaparak dayarama chha ki (jastai sitako chaudai **5,000 mm bhanda badhi** bhae napako galti; thyakkai 5,000 mm
  sbikar, 5,001 mm asbikar)

**"5,000 mm bhanda badhi" ra "5,000 mm wa badhi" farak hun.** talako kodale
`minimum_mm <= measured_mm <= maximum_mm` janchchha, tyasaile 5,000 mm pas hunchha ra 5,001 mm le `ValueError`
dinchha. simako kun patti pas hune ho, kod ra lekhai dubaima eutai banaunuhos.

<!-- ne-cell: 446e985d | after-heading -->
### natijako udaharan

<!-- ne-cell: e16cecde | after-heading -->
## Part 5 sadharan parikshan

<!-- ne-cell: 8f3eb327 | after-heading -->
**`assert` le sbatah jaanchne**
<!-- ne-pair: Automatic checks with `assert` -->

<!-- ne-cell: 8f3eb327 -->
`assert` le "yo sart pura hunuparchha" bhanera ghoshana garchha. pura bhae kehi hundaina, nabhae truti aaunchha.

```python
assert round(100.3 - 100.0, 6) <= 0.5
```

kod badalepachhi, **lekhieka parikshanko dayarama** apeksha anusar chalchha ki chaldain jaanchna sakinchha. yas lai
**regression test** bhaninchha. nalekhieka input sahi chhan ki chhainan yo parikshanle dekhaundain.

<!-- ne-cell: fa5475bf | after-heading -->
### natijako udaharan

<!-- ne-cell: 9d19737f | after-heading -->
**parikshan asaphal hunda ke hunchha**
<!-- ne-pair: What a failing test looks like -->

<!-- ne-cell: 9d19737f -->
talako cell ma **janajan galat apeksha** lekhieko chha. `AssertionError` aunechha. tyo nai sahi byabahar ho.

<!-- ne-cell: e1548d66 | after-heading -->
## Part 6 nap jaanchne karyakram pura garne

<!-- ne-cell: 172094ac | after-heading -->
**abashyakata (mapadand)**
<!-- ne-pair: Requirements -->

<!-- ne-cell: 172094ac -->
talako mapadandaanusar karyakram banaunuhos.

| bishay | maan |
|---|---|
| adhar maan (yahan mapadandako kendra) | 100.0 mm |
| sahyata | ±0.5 mm |
| input | napieka maanko soochi (akshar pani huna sakchha) |
| natija | harek napako nirnaya, OK/NG sankhya, NG anupaat, sabaibhanda naramro maan |

`adhar maan` bhaneko sima dubaitir barabar hunda "bichako maan" ho. mathillo ra tallo sima barabar nabhae dui sima
chhuttachhuttai lekhnuhos.

<!-- ne-cell: 25671959 | after-heading -->
### natijako udaharan

<!-- ne-cell: 43c80070 | after-heading -->
## abhyas

<!-- ne-cell: b7cfa925 | after-heading -->
#### abhyas 1A (adharabhut): nirnaya garne function aphain lekhne

<!-- ne-cell: b7cfa925 -->
motai jaanchne function `judge_thickness(measured, nominal=2.0, tolerance=0.1)` **aphain lekhnuhos**.
mapadand **2.00 ± 0.10 mm** ho ra `return` le `"OK"` wa `"NG"` pharkaunuparchha. `[1.95, 2.0, 2.1, 2.15]`
jancher dekhaunuhos.

**sakieko manine abastha:** 1.95 → OK, 2.0 → OK, 2.1 → OK, 2.15 → NG dekhinchha.

**sima ra raunding**

sima "bhitra" parne hunale mathillo sima thyakkai 2.1 mm **OK** ho. tar `2.1 - 2.0` ko natija
`0.10000000000000009` aune hunale tyasai tulna garda 2.1 mm NG banchha. tyasaile yo abhyas ma
**farak lai `round(measured - nominal, 6)` le raund garera** tulna garne sahamati chha (talako udaharan uttar jastai).

mapadand (2.00 ± 0.10 mm) badalindain. raunding **yo abhyaska lagi** banaiyeko sahamati ho ra simabhanda ali
bahirako maan bhitra parna sakchha.

<!-- ne-cell: cbf93b2a | after-heading -->
#### abhyas 1B (adharabhut): motaiko nirnaya ma badalne

<!-- ne-cell: cbf93b2a -->
mathiko `analyse_measurements` lai **motai 2.00 ± 0.10 mm** ko nirnaya ma prayog garnuhos.
`nominal_mm=2.0`, `tolerance_mm=0.1` toker yo data jaanchnuhos:

`["2.00", "2.05", "2.11", "1.95", "2.20"]`

**sakieko manine abastha:** kun dui NG hun ra kina, bhanera bataun sakne (2.11 ra 2.20).

<!-- ne-cell: fae217f5 | after-heading -->
**abhyas 2 (madhyam): dherai mapadand sanbhalne**
<!-- ne-pair: Exercise 2 (intermediate): support several specifications -->

<!-- ne-cell: fae217f5 -->
chaudai, motai ra lambai — tin mapadand sangai jaanchna sakne banaunuhos. mapadandalai dictionary (`dict`) ma
rakher `for` le ghumaunuhos.

| mapadand | adhar maan | sahyata |
|---|---|---|
| chaudai | 100.0 mm | ±0.5 mm |
| motai | 2.00 mm | ±0.10 mm |
| lambai | 2500.0 mm | ±2.0 mm |

**dictionary (`dict`)** le "key → maan" ka jodi rakhchha. `specifications["width"]` le chaudaiko bhaag nikalchha ra
`specifications["width"]["nominal"]` le tyasko adhar maan (100.0) dinchha. adhar maan ra sahyata napieko manakai
ekaima (yahan mm) lekhnuhos.

**sakieko manine abastha:** eutai lupale mapadandaanusar ek-ek line natija dekhaunchha.

<!-- ne-cell: 2dc30e46 | after-heading -->
#### abhyas 3 (baikalpik): asamanya maanko abhilekh rakhne

<!-- ne-cell: 2dc30e46 -->
`analyse_measurements` sudharer **asbikar garieko maan ra tyasko karan** `rejected` ma
`(maan, karan)` tuple ko rupama rakhnuhos. antama karan anusar ganer pratyek karanko sankhya dekhaunuhos.

**sakieko manine abastha:** asbikarako pratyek karan sang tyasko sankhya dekhinchha.

<!-- ne-cell: 1f203ca5 | after-heading -->
#### bujhai jaanchne prashna

<!-- ne-cell: 1f203ca5 -->
1. `if` pachhi `:` chhutyo bhane ke hunchha?
2. `elif` tinabata rakhda dosro ra tesro sart dubai saty bhae ke hunchha?
3. function lekhnuka dui phaida bhannuhos.
4. `for` lupbhitra `continue` prayog garda ke hunchha? (aphain khojnuhos.)
5. "jaso bhae pani `except: pass`" kina khataranak chha?

<!-- ne-cell: 0f28a584 | after-heading -->
## samasya parema

<!-- ne-cell: 0f28a584 -->
truti aepachhi pahile "kun cell ma", "kun line ma", "ke sandesh ayo" bhanera lekhnuhos. bujhaunuparne kaam ma pani
tyahi abhilekh rakhnuhos.

| lakshan | ke garne |
| --- | --- |
| `IndentationError: expected an indented block` | `if` pachhiko line lai block ka aru lainajattikai tal sarnuhos (yo talim ma 4 khali thaun). |
| `NameError: name 'judge_width' is not defined` | function paribhashit garne cell chalaieko chhaina. mathibat kramaisang feri chalaunuhos. |
| `AssertionError: just outside tolerance` | parikshanko apekshit maan wa function — euta galat chha. dubai `print` garera jaanchnuhos. |
| function bhitra `ValueError` aaunchha | input jaanchle kaam gareko chha. sandesh ma kun maan samasya bhaeko lekhieko hunchha. |
| lupale antim tattb janchdain | `range(len(items) - 1)` jasto lekhda dayara ek kam hunchha ra antim tattb chhutchha. `range(len(items))` le sabai kram samabesh garchha; `for value in items:` sabaibhanda sajilo ho. |

<!-- ne-cell: 22b083fc | after-heading -->
## sampannata janchasuchi

<!-- ne-cell: 22b083fc -->
**aniwarya** ra **baikalpik** kaam chhuttachhuttai rakhieka chhan. **abhyas 3 (baikalpik)** baikalpik ho; nagare pani
pura maninchha. samay banki bhae ma matra garnuhos. sabai aniwarya bundama chinh lagepachhi yo notebook pura hunchha.

**aniwarya**

- [ ] Part 1–Part 6 padher sabai code cell chalaen
- [ ] abhyas 1A, 1B ra 2 (aniwarya) garen
- [ ] `analyse_measurements` chalne kura janchen
- [ ] `assert` prayog garera parikshan lekhen
- [ ] bujhai jaanchne 5 prashnako uttar dien
- [ ] notebook surakshit garen

**baikalpik**

- [ ] abhyas 3 (baikalpik) ma asbikarako karan ganer dekhaen

<!-- ne-cell: 84120fa4 | after-heading -->
## thap adhyayan (baikalpik)

<!-- ne-cell: 84120fa4 -->
### sandarbha lingk

- [Python control flow (Japani)](https://docs.python.org/ja/3/tutorial/controlflow.html)
- [Python truti ra apabad](https://docs.python.org/ja/3/tutorial/errors.html)
- [Python built-in function](https://docs.python.org/ja/3/library/functions.html)

### thap chunauti (aniwarya hoina)

`for` ra `while` ko farak khojnuhos ra "kati patak dohorine thaha nabhaeko" kaam kunle lekhnuparne ho sochnuhos.
