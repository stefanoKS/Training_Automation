<!--
Nepali anuwad / Nepali translation source for
notebooks/00_Setup/00_Environment_Setup.ipynb

Each block starts with an ne-cell directive naming the notebook cell id.
CMD commands, paths, file names and licence names stay byte-identical.
-->
# din 0 notebook 00 — Nepali anuwad

<!-- ne-cell: 1ac0141f | after-heading -->
# din 0 (din 1 bhanda aghi, paath samayabahir) notebook 00: batabaran setaap

<!-- ne-cell: 1ac0141f -->
## sikai lakshyaharu

| Nepali |
| --- |
| 1. Python kasto aujar ho bhanera bujhaun sakne. |
| 2. Command Prompt (CMD) kholer adesh chalaun sakne. |
| 3. virtual environment banaera aawashyak package rakhna sakne. |
| 4. JupyterLab suru garera notebook kholna ra surakshit garna sakne. |
| 5. aphno batabaran thik chha ki chhaina aphain jaanchna sakne. |

## yo notebookko adharabhut jankari

| bishay | biwaran |
| --- | --- |
| sikai samay (anuman) | 60 minet |
| kathinai | surubati tah |
| poorwashart | kibord ra maus chalaun jannuparchha. programing jnan aawashyak chhaina. |
| aawashyak laibreri | numpy, matplotlib, pillow, pandas, opencv-python, ipykernel, jupyterlab |
| prayog hune kernel | `aivision` (adharabhut batabaran) |
| samayatalika | [`COURSE_SYLLABUS.md` tayari](../../COURSE_SYLLABUS.md#preflight) |

### bujhaunuparne kaam

| Nepali |
| --- |
| batabaran jaanch riport (yo notebookko antya ma sbatah banchha) |
| pahilo Python program chalaeko natija |

ajhai batabaran rakhieko chhaina bhane pahile [START_HERE](../../START_HERE.md) ko adhikarik prakriya Command
Prompt ma saknuhos, tyaspachhi kod cell ma januhos.

<!-- ne-cell: 3f811cde | after-heading -->
## yo notebook kahan parchha

<!-- ne-cell: 3f811cde -->
| bishay | biwaran |
| --- | --- |
| kisim | tayari (paath samayabahir) |
| lagne samay | 60 minet |
| poorwashart | chhaina |
| samayatalika | [`COURSE_SYLLABUS.md` tayari](../../COURSE_SYLLABUS.md#preflight) |

yo notebook paath samayabahir garinchha. 5 dinko 360 minetbhitra pardaina.

<!-- ne-cell: audit-learning-loop | after-heading -->
### anuman garnuhos, chalaunuhos, hernuhos, byakhya garnuhos

<!-- ne-cell: audit-learning-loop -->
variable bhaneko maanko naam ho. kernel bhaneko maan rakhne chalaune bhaag ho. mahattwapurna cell chalaunuaghi input,
kaam ra natija ek-ek bakyama lekhnuhos. pahile anuman lekhnuhos, tyaspachhi cell chalaera maan wa chitra
hernuhos. `defect_count` badhaunuaghi ra pachhiko maan badaler feri anuman garera chalaunuhos. janajan rakhieka
truti ra nasakieka abhyaska lagi lekhieko nirdeshan pachhyaunuhos.

<!-- ne-cell: 79328757 | after-heading -->
**yo notebook kasari prayog garne**
<!-- ne-pair: How to use this notebook -->

<!-- ne-cell: 79328757 -->
yo notebook **mathibat kramaisang** chalaunuhos. bichako cell chhodyo bhane pachhika cell chaldainan.

notebook ma 2 kisimaka "cell" hunchhan. dubai **badalna sakinchha**, tar kaam farak chha.

| kisim | dekhine rup | ke garchha | chalaunda |
|---|---|---|---|
| Markdown cell | akshar matra | byakhya padhne | kehi hundaina (chhapieko kagajajastai) |
| kod cell | khairo chaukon ra `In [ ]:` | program hunchha | **Shift + Enter** le tyahin chalchha |

kod cell chhaner `Shift` thicher `Enter` thichda tyo cell chalchha.

| dekhine | arth |
|---|---|
| `In [ ]:` | yo cell **ajhai chaleko chhaina** (kernel ko memory khali chha bhanne hoina) |
| `In [*]:` | chaliraheko. chaldai garda akshar dekhin pani sakchha |
| `In [7]:` | chalisakyo (yo kernel ma sataun patak chaleko) |

<!-- ne-cell: fb740ebf | after-heading -->
**pahile jannuparne kura: adesh ra Python kod farak hun**
<!-- ne-pair: First, know the difference: commands and Python code are not the same -->

<!-- ne-cell: fb740ebf -->
aba dekhi 2 kisimaka "nirdesh" aunechhan. **misae aniwarya rupama asaphal hunchha.**

**1. CMD adesh (Command Prompt ma lekhine)**

```cmd
python --version
```

yo Windows ko Command Prompt ma lekhinchha. `python` bhanne **aujar** bolaieko chha.

**2. Python kod (yo notebookko kod cell ma lekhine)**

```python
print("こんにちは")
```

yo Python bhanne **bhasha** ma lekhieko baky ho. CMD ma sidhai lekhda truti hunchha.

> notebookko kod cell ma `python -m pip install ...` jasta CMD adesh lekhnu hundaina.
> Python ko syntax truti hunchha. adhikarik installation CMD ma garinchha. Part 3 ko `%pip`
> Jupyter ka lagi matra apabad ho.

<!-- ne-cell: d68aa961 | after-heading -->
## Part 1 adharabhut shabdaharu

<!-- ne-cell: f98449a1 | after-heading -->
### skrinaka bhaag ra tinaka naam

<!-- ne-cell: f98449a1 | after-image:../../assets/diagrams/teach_setup_jupyter_ui.png -->
chitra: notebook, cell, kernel ra output ko sthan-sambandh (yojanabaddha. bastabik skrinako photo hoina).

**dhyan dinuparne kura**

cell bhaneko "akshar lekhne thaun", kernel bhaneko "hisab garne chhuttai program" ho. Markdown cell ra kod cell
dubai **sampadan garna sakinchha**. farak chalaunda garne kaam ma ho. kernel feri chhanda cellko akshar haraundain,
tar restart garda hisab garieka variable haraunchhan.

**sochnuhos**

- kernel restart garda cellko akshar ra variable madhye ke haraunchha?

<!-- ne-cell: fig-teach_setup_workflow | after-heading -->
### prakriyako samagra chitra

<!-- ne-cell: fig-teach_setup_workflow | after-image:../../assets/diagrams/teach_setup_workflow.png -->
chitra: notebook kholepachhi truti baat pharkinesammako prabah (yojanabaddha). ① cell chhanne → ② kernel chhanne →
③ chalaune → ④ output herne. truti aeko bela matra ⑤ ko punahsthapanama janchha.

**dhyan dinuparne kura**

tir "chalaune → output herne" kram ma jodieka chhan. punahsthapan (⑤) **chalaera truti aepachhi** ko bato ho.
output napadhi arko cell ma najanuhos.

**sochnuhos**

- ③ ko chalaima truti ayo bhane ④ ra ⑤ madhye kata januhunchha?

<!-- ne-cell: 198db0a3 | after-heading -->
**Python bhaneko ke ho**
<!-- ne-pair: What is Python -->

<!-- ne-cell: 198db0a3 -->
Python "computer lai kaam lagaune bhasha (programing bhasha)" madhye ek ho.

udaharanka lagi talaka kaam Python lai din sakinchha.

- hisab garne (100.3 le 100±0.5 ko dayarabhitra parchha ki pardaina nirnaya garne)
- chitra padhne (kyamerale khicheko sitako photo)
- chitrabhitrako kalo thoplo khojne
- natija lai talika wa graph banaune

Python ko phaida **padhda arth bujhine** ho. talako ek line hernuhos.

```python
width = 100.3
```

"width (chaudai) = 100.3" bhanera lagabhag anggrejimai padhna sakinchha. tapainle lekheko Python ko baky
**ek-ek line mathibat kramaisang** chalchha.

<!-- ne-cell: f4400f5e | after-heading -->
**Command Prompt (CMD) bhaneko ke ho**
<!-- ne-pair: What is Command Prompt (CMD) -->

<!-- ne-cell: f4400f5e -->
terminal bhaneko "aksharale computer lai adesh dine jhyal" ho. yo talim ma **Command Prompt (cmd.exe)**
prayog garchhaun. mausale klik garnuko satta aksharale adesh dinchhaun.

**Command Prompt kholne 2 tarika**

1. Windows ko khoj bakasama `cmd` lekher "Command Prompt" kholne.
2. File Explorer ma samagri folder kholer thegana barama `cmd` lekher Enter thichne.

kholda talako jasto line dekhinchha. yas lai **prompt** bhaninchha.

```text
C:\Users\Student>
```

`>` aghiko bhaag "ahile bhaeko folder" ho. yo dekhauna matra ho, prompt aphain taip garnu hundaina.

<!-- ne-cell: d6b93483 | after-heading -->
**virtual environment bhaneko ke ho, kina chahinchha**
<!-- ne-pair: What a virtual environment is, and why it matters -->

<!-- ne-cell: d6b93483 -->
**virtual environment** bhaneko "yo talimka lagi matra chhuttyaieko Python aujar-bakas" ho.

purai computer ma eutai aujar-bakas sajha garda talaka samasya aunchhan.

| samasya | thos udaharan |
|---|---|
| version dbandb | arko kaamka lagi purano OpenCV chahiyo, talimko OpenCV bigriyo |
| punah utpadan garna nasakine | "mero PC ma chalchha ni" bhanne abastha aaunchha |
| bigriepachhi ukasna gahro | kun package karan ho thaha hundaina |

virtual environment banae **tyahi foldarbhitra matra** package paschha.
arko kaam wa arko Python ma kunai asar pardaina. bigriyo bhane folder metaera feri banaun sakinchha.

> yo talim ma 2 bata virtual environment prayog garchhaun.
> `aivision` (adharabhut + YOLO) ra `aivision-anomalib` (PatchCore ka lagi).
> karan din 5 ko notebook ma byakhya garinchha.

<!-- ne-cell: 8b3ad3d0 | after-heading -->
**Jupyter notebook, cell ra kernel**
<!-- ne-pair: Jupyter notebook, cell and kernel -->

<!-- ne-cell: 8b3ad3d0 -->
**Jupyter notebook** bhaneko "byakhya", "chalne program" ra "natija" eutai file ma rakhieko kagajat ho.
fileko extension `.ipynb` ho.

- **cell (cell)**: notabukabhitrako euta bakas. byakhyaka lagi (Markdown) ra programaka lagi (kod) hunchhan.
- **kernel**: kod cell bastabama chalaune "Python ko mukhy bhaag".
  notebookle "kun kernel ma chalaune" samjhirahanchha.
- **variable kernel bhitra rahanchha**. cell A ma banaiyeko variable cell B ma pani prayog garna sakinchha.
  tar **kernel restart garda sabai variable haraunchhan**.

> "kernel galat chhanne" yo talimko sabaibhanda samanya samasyamadhye ek ho.
> thik kernel ho ki hoina arko cellko `sys.executable` le jaanchna sakinchha.

<!-- ne-cell: da168b9c | after-heading -->
## Part 2 installation prakriya (CMD ma chalaune)

<!-- ne-cell: f78f8416 -->
> ### ⚠️ mahattwapurna
> yo Part ka adesh **Command Prompt ma tanser** chalainchha.
> notebookko kod cell ma nalekhnuhos.

talimko PC ma batabaran pahilai rakhieko chha bhane Part 3 ko jaanch matra garnuhos.

<!-- ne-cell: 8065152f | after-heading -->
**charan 1: Python rakhieko chha ki chhaina jaanchne**
<!-- ne-pair: Step 1: check whether Python is installed -->

<!-- ne-cell: 8065152f -->
Command Prompt kholer talako adesh chalaunuhos.

```cmd
py -3.11 --version
```

apekshit natija (udaharan):

```text
Python 3.11.9
```

`Python 3.11.x` prayog garchhaun. aru series janchieko chhaina. `py` chhaina bhane
[START_HERE](../../START_HERE.md) charan 2 hernuhos.

**ramro nabhaema**

| dekhine | arth | ke garne |
|---|---|---|
| `Python was not found` | Python rakhieko chhaina | python.org baat 3.11 rakhne (talako dhyan hernuhos) |
| `Python 2.7.x` | dherai purano | 3.11 rakhne |
| Microsoft Store khulchha | Windows ko bikalp | Settings → "App execution aliases" ma `python.exe` banda garne |

python.org sanskaran rakhda dhyan dine kura:

- "**Add python.exe to PATH**" ma aniwarya chinh lagaune.
- "Install Now" thik chha.

<!-- ne-cell: 3da79c65 | after-heading -->
**charan 2: talim folder ma jane**
<!-- ne-pair: Step 2: move into the course folder -->

<!-- ne-cell: 3da79c65 -->
daunalod garieko `AI_Vision_Training` folder ma januhos.
`cd` bhaneko "change directory (folder sarne)" ho.

```cmd
cd /d "%USERPROFILE%\Documents\Training_Automation\AI_Vision_Training"
```

thik sareko chha ki chhaina jaanchnuhos.

```cmd
cd
dir
```

`cd` le ahileko thaun, `dir` le tyasabhitrako samagri dekhaunchha. ZIP wa OneDrive bhae bastabik nikalieko
thaunle badalnuhos. khali thaun bhaeko path pani quote bhitra rakhnuhos.
[START_HERE](../../START_HERE.md) charan 1 pani hernuhos.

<!-- ne-cell: e0bd50ff | after-heading -->
#### tayari prakriyako jaanch

<!-- ne-cell: e0bd50ff -->
installation ko adhikarik prakriya [START_HERE](../../START_HERE.md) charan 3–9 ho.
Python 3.11, dubai batabaran, dubai kernel, samagri, photo ra weight paath aghi tayar garinchha.
yahan feri install nagari tayar bhaisakeko abastha janchinchha. sakriya garna manahi bhaeko abastha ma quote bhitrako
virtual environment ko python.exe sidhai prayog garnuhos. CMD ma sakriya garna policy paribartan aawashyak chhaina.

<!-- ne-cell: 620ede80 | after-heading -->
#### tayari prakriyako jaanch (punah)

<!-- ne-cell: 620ede80 -->
installation ko adhikarik prakriya [START_HERE](../../START_HERE.md) charan 3–9 ho.
Python 3.11, dubai batabaran, dubai kernel, samagri, photo ra weight paath aghi tayar garinchha.
yahan feri install nagari tayar bhaisakeko abastha janchinchha. sakriya garna manahi bhaeko abastha ma quote bhitrako
virtual environment ko python.exe sidhai prayog garnuhos.

<!-- ne-cell: 319857e2 | after-heading -->
#### tayari prakriyako jaanch (tesro patak)

<!-- ne-cell: 319857e2 -->
installation ko adhikarik prakriya [START_HERE](../../START_HERE.md) charan 3–9 ho.
yahan feri install nagari tayar bhaisakeko abastha janchinchha. sakriya garna manahi bhaeko abastha ma quote bhitrako
virtual environment ko python.exe sidhai prayog garnuhos.

<!-- ne-cell: b6c87f4f | after-heading -->
**charan 6 (aichchhik): NVIDIA GPU prayog garne bhae**
<!-- ne-pair: Step 6 (optional): using an NVIDIA GPU -->

<!-- ne-cell: b6c87f4f -->
GPU aniwarya chhaina. GPU wheel ko URL, sanskaran ra driver ko sanyojan janchieko chhaina.
paribartan aawashyak bhaeko abastha ma matra prashikshak ra
[PyTorch adhikarik chayan skrin](https://pytorch.org/get-started/locally/) ma jaanchnuhos.
dodhar bhae **kehi nabadalnuhos**. adhikarik prakriya CPU ma pura garna sakinchha.

<!-- ne-cell: 60d3836e | after-heading -->
## Part 3 notabukabhitrabat rakhne tarika (%pip)

<!-- ne-cell: c3d0cb90 | after-heading -->
**`%pip` bhaneko ke ho**
<!-- ne-pair: What `%pip` is -->

<!-- ne-cell: c3d0cb90 -->
`%` baat suru hune line lai **magic command** bhaninchha, yo Jupyter ka lagi matrako nirdesh ho.
`%pip` bhaneko "yo notebookle prayog gareko kernel ma pip chalaune" bhanne ho.

```text
%pip install requests
```

yo Python ko byakaran hoina. tyasaile CMD ma lekhda chaldain.
ulto, `python -m pip install ...` notebook ma lekhda pani chaldain.

> **yo talimko niti:** installation **suru ma ek patak matra**. harek notebook chalaunda install gardainaun.
> karan 3 bata chhan.
> 1. harek patak kehi minet kurnuparchha
> 2. network nabhaeko din chaldain
> 3. batabaran bistarai badaliera karan thaha paun gahro hunchha

<!-- ne-cell: 1d7024f4 -->
talako cell **nachalaunuhos**. yo lekhne namuna matra ho. aawashyak bhaeko bela matra
`#` hataera chalaunuhos.

<!-- ne-cell: a1b2c3d4 | after-heading -->
#### talim folder ra sajha bhaag lod garne

<!-- ne-cell: a1b2c3d4 -->
arko cellle yo notebookle prayog garne thaun ra bhaag tayar garchha matra. bhitri kura bujhnu aawashyak chhaina.

<!-- ne-cell: 54340dcc | after-heading -->
## Part 4 batabaranko jaanch

<!-- ne-cell: audit-teach_code_cell_lifecycle | after-heading -->
### kod padhne tarika

<!-- ne-cell: audit-teach_code_cell_lifecycle | after-image:../../assets/svg/teach_code_cell_lifecycle.svg -->
chitra: maan cell ma hoina, kernel ma rahanchha. (hisab garieko kritrim udaharan/yojanabaddha. model ko maapan garieko
natija hoina.)

**dhyan dinuparne kura**

maan cell ma hoina, kernel ma rahanchha. input ra badaliepachhi baneko maan aunlale pachhyaunuhos.

**sochnuhos**

jodne cell matra feri chalaunda 4 kati hunchha?

<!-- ne-cell: f839cd9f | after-heading -->
**kun Python prayog bhairaheko chha jaanchne**
<!-- ne-pair: Confirm which Python you are using -->

<!-- ne-cell: f839cd9f -->
arko cell chalaunuhos. `Executable` ma `.venv` chha bhane batabaran thik chha.

yadi `C:\ProgramData\miniconda3\...` wa `C:\Python311\...` jasto
`.venv` nabhaeko dekhiyo bhane **kernel chhanot galat chha**.
tyasto abastha ma menuko `Kernel` → `Change Kernel` → `Python 3 (AI Vision)` chhannuhos.

<!-- ne-cell: c5ebf004 | after-heading -->
**aawashyak laibreri jaanchne**
<!-- ne-pair: Check the required libraries -->

<!-- ne-cell: c5ebf004 -->
`[MISSING]` dekhiyo bhane Part 2 ko charan 4 ma pharker install garnuhos.
yo cellle **install gardaina**. jaanch matra garchha.

<!-- ne-cell: 9bcfaf3c | after-heading -->
**chitra ma prayog hune phant milaunuhos**
<!-- ne-pair: Configure Japanese text in figures -->

<!-- ne-cell: 9bcfaf3c -->
Matplotlib ko purbanirdharit phantale Japani akshar dekhauna sakdain. tyasaile chitrako shirshak `□□□` jasto
dekhinchha. arko cellle Japani akshar dekhauna sakne phant khojer milaunchha. macOS wa Linux ma sbatah arko phant
chhaninchha.

<!-- ne-cell: cd8a9512 | after-heading -->
**talim folder ra samagriko thaun jaanchne**
<!-- ne-pair: Confirm the course folder and the assets -->

<!-- ne-cell: cd8a9512 -->
yo notebook tapainko prayogakarta naam wa install gareko thaun ma nirbhar gardaina.
`COURSE_SYLLABUS.md` ra `assets` folder lai chinh banaera mathitir khojdai talim folder bhettaunchha.

arko cellle `FileNotFoundError` diyo bhane `AI_Vision_Training` foldarbhitra baat JupyterLab kholnuhos
(Part 2 charan 5).

<!-- ne-cell: ea76d7d9 | after-heading -->
**sandarbha chitra ek patak matra daunalod garne**
<!-- ne-pair: Download the reference photographs once -->

<!-- ne-cell: ea76d7d9 -->
yo talimka kehi paath ma bastabik sandarbha chitra **sthaniy file** ko rupama dekhainchha. harek patak
internet baat lyaunuko satta **suru ma ek patak matra** lyaera tyaspachhi surakshit file prayog garinchha.

arko cell chalaunda `assets/scripts/download_reference_images.py` le 4 chitra
`assets/external_samples/open_reference/` ma lyaunchha. lyaieka file yi hun.

| file | ke ho | srot ra laisens |
| --- | --- | --- |
| `chelsea.png` | bastabik rangako photo (RGB ko udaharan) | scikit-image, Stefan van der Walt, CC0 1.0 |
| `camera.png` | bastabik greyscale photo | scikit-image, Lav Varshney, CC0 1.0 |
| `brick.png` | dhancha bhaeko pachhadiko photo | CC0Textures (scikit-image le prashodhan), CC0 1.0 |
| `VisA_samples.png` | audyogik anomaly detection datasetko saransh | Yang Zou adi / Amazon Science, VisA dataset CC BY 4.0 |

- lyaine **sandarbha chitra matra** ho. dataset wa model ko weight lyaindain.
- charabatai **nabadali** jastako tastai surakshit garinchha ra srot, laisens, SHA-256 `manifest.json` ra
  `ATTRIBUTION.md` ma abhilekh garinchha.
- sandarbha chitra paath ma hernaka lagi matra hun, **sikai, calibration wa parikshanko data ma prayog hundainan**.
- jati patak chalae pani thik surakshit bhaisakeka file tyasai prayog hunchhan (lyaune kaam ek patak matra).

terminal bhae adharabhut batabaran sakriya gareko CMD ma samagriko mul folder baat chalaunuhos.

```cmd
python assets\scripts\download_reference_images.py --course-root .
python assets\scripts\download_reference_images.py --course-root . --offline
```

dosro adeshale **kunai network anurodh nagari** surakshit file janchchha. file chhaina wa bigreko chha bhane skriptale
tyasko naam bhanchha ra tyahi adesh feri chalaun bhanchha; kahilyai arko chitra rakhdain.

<!-- ne-cell: 63c0e92f | after-heading -->
## Part 5 pahilo Python program

<!-- ne-cell: fig-teach_execution_state | after-heading -->
### chalaunuaghi, chaldai ra chalisakepachhiko abastha

<!-- ne-cell: fig-teach_execution_state | after-image:../../assets/diagrams/teach_execution_state.png -->
chitra: uhi 3 lineko cell lai chalaunuaghi, chaldai ra chalisakepachhi bhanera chhutyaera memoribhitrako samagrisangai
dekhaieko (yojanabaddha).

**dhyan dinuparne kura**

`In [ ]` bhaneko "yo cell ajhai chaleko chhaina", memory khali chha bhanne hoina. `In [*]` bhaneko chaliraheko, ra tyasabela
output dekhin pani sakchha. sankhya bhaneko chalisakyo. dekhaieko output ra variable ko rupama banki rahane maan farak
kura hun. aghillo chalaiko maan banki rahane abastha (stale state) ra naam nai nabhaeko abastha (NameError) dui
farak samasya hun.

**sochnuhos**

- variable paribhasha garne cell ek patak pani nachalaeko bela tyo variable prayog garne cell ma ke hunchha?

<!-- ne-cell: 7246e348 | after-heading -->
**`print()` le akshar dekhaune**
<!-- ne-pair: Displaying text with `print()` -->

<!-- ne-cell: 7246e348 -->
`print()` bhaneko "koshthakabhitrako samagri skrinama dekhaune" adesh ho.

`print` pachhiko `( )` birsie truti hunchha. akshar lekhda `"` (double quote) bhitra rakhnuparchha.

<!-- ne-cell: ee452a19 | after-heading -->
**hisab ra variable**
<!-- ne-pair: Calculating and variables -->

<!-- ne-cell: ee452a19 -->
Python kyalkuletaraka rupama pani prayog garna sakinchha. `=` bhaneko "dayanpattiko natija lai naam dine" ho.

ganitako `=` (barabar) sang arth farak chha. "`width` bhanne bakasama 100.3 rakhne" bhanera bujhnuhos.

<!-- ne-cell: d3a8869f | after-heading -->
### natijako udaharan

yo udaharan ma talako natija aaunchha (uhi input diiyo bhane uhi natija aaunchha).

`difference` lai `round(difference, 3)` le 3 dashamalabama ghumaera dekhaiekole `0.3` dekhinchha. ghumaunuaghiko
maan `0.29999999999999716` ho (0.3 lai 2 adharama thyakkai lekhna nasakine bhaekole). bistrit kura din 2 ko
notebook 01 ma samhalinchha.

<!-- ne-cell: d18c02fb | after-heading -->
**truti sandesh padhne abhyas**
<!-- ne-pair: Practice reading an error message -->

<!-- ne-cell: d18c02fb -->
janajan truti banaihalaun. truti "asaphalata" hoina "jankari" ho.
talako cell chalaunda **rato sandesh** aaunchha. yo apekshit nai ho.

padhne 3 bunda matra chhan.

1. **sabaibhanda talako line** … trutiko kisim (`NameError`, `SyntaxError` adi)
2. **tyasko mathiko line** … ke gadabad bhayo
3. **`---->` bhaeko line** … programako kati number line

<!-- ne-cell: fig-teach_nameerror_recovery | after-heading -->
### NameError baat pharkine prakriya

<!-- ne-cell: fig-teach_nameerror_recovery | after-image:../../assets/diagrams/teach_nameerror_recovery.png -->
chitra: `widht_mm` ra `width_mm` galat lekhda aune truti ra sudharne kram (yojanabaddha).

**dhyan dinuparne kura**

`NameError` bhaneko "tyo naam ajhai chhaina" bhanne ho. paribhasha garne selabhanda aghi prayog gariyo, hijje farak chha,
wa kernel restart garda variable harayo — yimadhye euta ho. mathika cell kramaisang feri chalaunu nai adharabhut
punahsthapan ho.

**sochnuhos**

- kernel restart garelagattai `width_mm` prayog garna sakinchha?

<!-- ne-cell: 852eaaf2 | after-heading -->
### truti aepachhi

<!-- ne-cell: 852eaaf2 -->
talako jasto `NameError` ayo bhane saphal bhayo.

```text
NameError: name 'sheet_width' is not defined
```

arth "`sheet_width` bhanne naam paribhashit chhaina" bhanne ho.
yo truti ae arko cell chalaera sudharnuhos.

<!-- ne-cell: acc65cdf | after-heading -->
## Part 6 chitra banaera dekhaune

<!-- ne-cell: 824933ca | after-heading -->
**sankhyako samuh nai chitra banchha**
<!-- ne-pair: An image is just a grid of numbers -->

<!-- ne-cell: 824933ca -->
chitra jadu hoina. **sankhyako talika** ho.

- euta chitra sana chaukon (**pixel**) talamathi ra chheuchhau miler rakhieko hunchha.
- pratyek pixel ma euta sankhya hunchha. 0 kalo, 255 seto.
- rang chitra ma rato, hariyo, nilo gari 3 sankhya hunchhan.

arthat Python ma sankhyako talika banayo bhane tyahi chitra banchha.
arko cell ma bastabama banainchha.

<!-- ne-cell: 68fda21f | after-heading -->
### natijako udaharan

yo udaharan ma talako natija aaunchha (uhi input diiyo bhane uhi natija aaunchha).

`...` bhaneko "banki pani uhi maanle jari chha" bhanne ho. 8 pangkti × 8 stambhaka 64 batai maan `230` chhan.

<!-- ne-cell: 66eb3a87 | after-heading -->
**Matplotlib le dekhaune**
<!-- ne-pair: Displaying with Matplotlib -->

<!-- ne-cell: 66eb3a87 -->
Jupyter bhitra `cv2.imshow()` prayog gardainaun. `cv2.imshow()` le
alag jhyal kholne hunale Jupyter ma adkin sakchha.
tyasko satta **Matplotlib** prayog garchhaun. purai talim ma yahi tarika apanainchha.

`plt.imshow()` le chitra tayar garchha, `plt.show()` le bastabama korchha.
`interpolation="nearest"` le "thulo banaunda pani sima dhamilo nabanaune" nirdesh dinchha.

yahan dekhaieko 8 × 8 ko **kritrim** chitra ho. karakhanako bastabik photo hoina.

<!-- ne-cell: 956099c4 | after-heading -->
**aphain badaler herne (nirdeshit prayog)**
<!-- ne-pair: Change it yourself (guided experiment) -->

<!-- ne-cell: 956099c4 -->
talako cellka sankhya badaler natija kasari badlinchha pahile anuman garera chalaunuhos.

1. `230` lai `120` banaune → chitra ujyalo hunchha? andhyaro?
2. `image[2:4, 5:7]` lai `image[0:2, 0:2]` banaune → kalo chaukon kata sarchha?
3. `vmin=0, vmax=255` lai `vmin=0, vmax=120` banaune → dekhai kasari badlinchha?

<!-- ne-cell: be1bb0f9 | after-heading -->
## Part 7 batabaran tayari riport

<!-- ne-cell: 06c2fc5e | after-heading -->
**riport sbatah banaune**
<!-- ne-pair: Generate the report automatically -->

<!-- ne-cell: 06c2fc5e -->
antama ahileko batabaran lai euta riportama jamma garchhaun.
`submissions/reports/environment_report.json` ma surakshit hunchha.
bujhaunda yo cellko output jastako tastai tansnuhos.

riportama Python ko executable, package ko sanskaran, pratyek package import bhayo ki bhaen, ra
talimko samagri ra sandarbha chitra puge ki pugen abhilekh hunchha. napugeko kura "chhaina" bhanera abhilekh hunchha.

<!-- ne-cell: a9e07e4c | after-heading -->
## abhyas

<!-- ne-cell: 6a2d7d09 | after-heading -->
**abhyas 1 (adharabhut): aphno naam dekhaune**
<!-- ne-pair: Exercise 1 (basic): print your name -->

<!-- ne-cell: 6a2d7d09 -->
talako cell ma Japani ra Angreji ma aphno naam ra bibhag dekhaune kod lekhnuhos.
`print()` dui line ma prayog garnuhos. chalaera natija jaanchnuhos.

sakieko adhar: output ma **aphnai naam** dekhinuparchha (namunako baky jastako tastai bhae sakieko manindain).

<!-- ne-cell: d153c5f9 | after-heading -->
**abhyas 2 (madhyam): maapan maanko nirnaya**
<!-- ne-pair: Exercise 2 (intermediate): judge a measurement -->

<!-- ne-cell: d153c5f9 -->
`measured = 99.2` lai `measured = 97.0` banaunda antim line ma `False` dekhinchha.
kun chahin "OK (manakbhitra)" hola? karan ek lineko comment ma lekhnuhos.

thap `tolerance = 0.5` lai `2.0` banaundako natija pani jaanchnuhos.

sakieko adhar: cell truti bina chalchha ra **karan ek lineko comment ma lekhieko** hunchha.

<!-- ne-cell: 6affad1b | after-heading -->
**abhyas 3 (bikas/aichchhik): chitrako "ujyalo" napne**
<!-- ne-pair: Exercise 3 (optional challenge): measure image brightness -->

<!-- ne-cell: 6affad1b -->
NumPy ko `mean()` prayog garera sampurna chitrako ausat ujyalo hisab garnuhos.
thap `base_level` lai 3 kisim (jastai 120, 180, 230) banaera ausat maan kasari badlinchha talika ma lekhnuhos.

sanket: `image.mean()` le ausat maan dinchha.

sakieko adhar: "ausat ujyalo pachhadiko maan ra andhyaro chaukonako kshetraphalale tay hunchha" jastai **niyam aphnai
shabdama lekhieko** hunchha. yo abhyas aichchhik ho.

<!-- ne-cell: a5cf6274 | after-heading -->
#### bujhai jaanch

talaka prashnako jabaph aphnai shabdama dinuhos. bujhaunuparne kaam ma lekhnuhos.
(thyakkai sahi shabdabali nabhae pani hunchha. aphno bujhai jaanchne prashna hun.)

1. virtual environment prayog nagari purai computer ma package rakhda kasta samasya aunchhan?
2. CMD ko adesh ra Python kod kasari chhutyaune?
3. `Kernel` → `Restart` garda ke haraunchha? ke banki rahanchha?
4. `[MISSING] numpy` dekhinda kun kram ma ke janchnuhunchha?
5. chitra "sankhyako talika" bhaniyo. 100 × 100 pixel ko kalo-seto chitra ma katibata sankhya hunchhan?

namuna jabaph prashikshak margadarshan (`docs/instructor/day01_instructor_guide.md`) ma chha.
pahile aphain lekhnuhos, tyaspachhi hernuhos. nakkal garnu hoina, aphnai shabdama bhannu uddeshya ho.

<!-- ne-cell: 9c31642a | after-heading -->
## samasya aunda

truti ae pahile "kun cell ma", "kun line ma", "ke sandesh ayo" bhanera tipnuhos. bujhaunuparne kaam ma pani
tyahi abhilekh rakhnuhos.

| lakshan | ke garne |
| --- | --- |
| `ModuleNotFoundError: No module named 'numpy'` | kernel farak huna sakchha. `sys.executable` ma `.venv` chha ki chhaina jancher `Kernel` → `Change Kernel` baat feri chhannuhos. |
| virtual environment sakriya garna sakien | CMD ma `dir .venv\Scripts\python.exe` jaanchnuhos, tyaspachhi `.\.venv\Scripts\activate.bat` chalaunuhos. chhaina bhane START_HERE charan 3 hernuhos. |
| `python` lekhda Microsoft Store khulchha | Settings → "App execution aliases" → `python.exe` banda garnuhos. |
| installation `Read timed out` ma rokinchha | network ko samasya. uhi adesh feri chalaunuhos. kampanima proxy chha bhane byabasthapakasang jaanchnuhos. |
| JupyterLab suru hundaina (`jupyter: command not found`) | virtual environment sakriya chha ki jaanchnuhos (`(.venv)` dekhinuparchha). chhaina bhane sakriya garera `jupyter lab` chalaunuhos. |
| `FileNotFoundError: 研修フォルダが見つかりません` | JupyterLab `AI_Vision_Training` bhitra baat suru garieko chhaina. folder ma gaera feri suru garnuhos. |
| sandarbha chitrako cell ma `取得失敗 / failed: ...` dekhinchha | dekhaieko file matra asaphal bhaeko ho. jadan jancher uhi cell feri chalaunuhos (liisakeka file jastako tastai rahanchhan). |
| sandarbha chitrako cell ma `Pillow が未導入` dekhinchha | Part 2 charan 4 (`requirements\base.txt`) chalaera uhi cell feri chalaunuhos. |
| memory apugako truti (`MemoryError`) | aru anuprayog banda garnuhos. yo talimko data sano chha, samanyatah hundaina. |

<!-- ne-cell: 98c05d2e | after-heading -->
## sakieko janchasuchi

**aniwarya: sabai kod cell + abhyas 1 ra 2. aichchhik: abhyas 3 ra "thap sikai" ko atirikt chunauti.**
abhyas 3 nagare pani yo notebook sakieko maninchha.

sabai ma chinh lagepachhi yo notebook sakinchha.

- [ ] Part 1–Part 4 ka byakhya padhen ra nabujheka shabd tipen
- [ ] sabai kod cell mathibat kramaisang chalaen
- [ ] sandarbha chitra (4 bata) lyaune cell chalaen ra `assets/external_samples/open_reference/` ma charabatai chhan
- [ ] abhyas 1 ra 2 chalaen
- [ ] `submissions/reports/environment_report.json` banyo
- [ ] kernel ko jaanch (`Kernel` → `Change Kernel`) garna sakne bhaen
- [ ] bujhai jaanchka 5 prashnako jabaph dien
- [ ] truti aeko tipot rakhen (nabhae "chhaina" lekhen)
- [ ] yo notebook surakshit garen (`Ctrl + S`)

aichchhik:

- [ ] abhyas 3 (bikas/aichchhik) garen

<!-- ne-cell: 235c801a | after-heading -->
## thap sikai (aichchhik)

<!-- ne-cell: 235c801a -->
### sandarbha lingk

- [Python adhikarik kagajat (Japani)](https://docs.python.org/ja/3/)
- [Jupyter adhikarik sait](https://jupyter.org/)
- [NumPy adhikarik kagajat](https://numpy.org/doc/)
- [Matplotlib adhikarik kagajat](https://matplotlib.org/stable/)
- [OpenCV adhikarik kagajat](https://docs.opencv.org/)

### atirikt chunauti (aniwarya hoina)

`np.zeros()` ra `np.ones()` prayog garera chitra banaera `plt.imshow()` le dekhaunuhos. `dtype` lai `uint8`
ra `float64` banaunda dekhai kasari badlinchha pani jaanchnuhos.
