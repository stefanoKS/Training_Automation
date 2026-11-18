<!--
Nepali anuwad / Nepali translation source for
notebooks/Day01_AI_Fundamentals/Day01_01_Introduction_to_AI.ipynb

Each block starts with an ne-cell directive naming the notebook cell id.
Do not translate code, file names, URLs or kernel names.
-->
# din 1 notebook 01 — Nepali anuwad

<!-- ne-cell: 21e8248a | after-heading -->
# din 1 notebook 01: AI bhaneko ke ho

<!-- ne-cell: 21e8248a -->
## sikai lakshyaharu

| Nepali |
| --- |
| 1. computer program bhaneko ke ho bhanera bujhaun sakne. |
| 2. sbachalan (automation) ra AI bichako farak bataun sakne. |
| 3. AI, mesin larning ra dip larningabichako sambandh bataun sakne. |
| 4. "siknu" ra "anuman garnu" (training / inference) bichako farak bataun sakne. |
| 5. utpadanako udaharan baat AI le kina galti garchha bhanera bujhaun sakne. |

## yo notebookko adharabhut jankari

| bishay | biwaran |
| --- | --- |
| sikai samay (anuman) | 115 minet |
| kathinai | surubati tah |
| poorwashart | `00_Environment_Setup.ipynb` sakieko hunuparchha. |
| aawashyak laibreri | numpy, matplotlib, pillow |
| prayog hune kernel | aivision |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 1](../../COURSE_SYLLABUS.md#day1) |

### bujhaunuparne kaam

| Nepali |
| --- |
| yo notebook chalaera aeko natija |
| abhyas 1–3 ka jabaph |
| bujhai jaanchka prashnaharuko jabaph |

<!-- ne-cell: f42a60b5 | after-heading -->
## yo notebook kahan parchha

<!-- ne-cell: f42a60b5 -->
| bishay | biwaran |
| --- | --- |
| din | din 1 |
| ajako kram | ajako notabukamadhye 1 / 3 |
| lagne samay | 115 minet |
| poorwashart | `00_Environment_Setup.ipynb` |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 1](../../COURSE_SYLLABUS.md#day1) |

dinko samayatalika `COURSE_SYLLABUS.md` ma eutai thaun ma chha. yo notebook tyasko euta bhaag matra ho, aphno
chhuttai samayatalika rakhdain. samay thaha nabhae pahile tyahi file hernuhos.

<!-- ne-cell: audit-learning-loop | after-heading -->
### anuman garnuhos, chalaunuhos, hernuhos, byakhya garnuhos

<!-- ne-cell: audit-learning-loop -->
sikaile udaharan baat niyam tay garchha; anumanle tay bhaisakeko niyam prayog garchha. yahan dekhine function ra
statistics bhane pachhi aune kurako purbabalokan matra hun. mahattwapurna cell chalaunuaghi input, kaam ra natija
ek-ek bakyama lekhnuhos. pahile anuman lekhnuhos, tyaspachhi cell chalaera maan wa chitra hernuhos ra kina tyasto
bhayo bhanera byakhya garnuhos. nayan brightness maan rakher feri anuman garnuhos ra chalaunuhos. janajan
rakhieka truti ra nasakieka abhyaska lagi lekhieko nirdeshan pachhyaunuhos.

<!-- ne-cell: 7b2d8b77 | after-heading -->
## Part 0 tayari

<!-- ne-cell: 247d7a3d | after-heading -->
**yo notebookko batabaran jaanchnuhos**
<!-- ne-pair: Check the environment for this notebook -->

<!-- ne-cell: 247d7a3d -->
pahile talim folder khojnuhos, tyaspachhi aawashyak laibreri jaanchnuhos. truti ae
`docs/troubleshooting/installation.md` hernuhos.

<!-- ne-cell: 458db013 | after-heading -->
**chitra ma prayog hune phant milaunuhos**
<!-- ne-pair: Configure Japanese text in figures -->

<!-- ne-cell: 458db013 -->
Matplotlib ko purbanirdharit phantale Japani akshar dekhauna sakdain. tyasaile chitrako shirshak `□□□` jasto
dekhinchha. arko cellle Japani akshar dekhauna sakne phant khojer milaunchha. macOS wa Linux ma sbatah arko phant
chhaninchha.

<!-- ne-cell: e5f6279e | after-heading -->
## Part 1 computer program bhaneko ke ho

<!-- ne-cell: 678fd258 | after-heading -->
**program bhaneko "nirdeshan-pustika" ho**
<!-- ne-pair: A program is a set of instructions -->

<!-- ne-cell: 678fd258 -->
program bhaneko computer lai diine **nirdeshan-pustika** ho. "yo kram ma, yo hisab garnu" bhanera
bistarai lekhieko hunchha.

computerle lekhieko kura thyakkai ra chhito chalaunchha. tyasko phaida bhaneko **thakdain ra alamalindain** bhanne ho.

uhi jabaph aunuko karan **uhi maapan maan ra uhi setting diinu** ho. yo udaharanko programale diieko sankhya lai
manakasang tulna matra garchha, utpadan napne kaam gardaina. maapan maan aphain sahi chha ki chhaina bhanne kura
kyamera, ujyalo ra maapan yantrako pakshko kura ho, tyo chhuttai janchnuparchha.

utpadanako udaharan heraun. sitako chaudai naper manakbhitra chha ki chhaina bhanera nirnaya garne kaam.

1. maapan maan padhne
2. manak maan 100.0 mm sangko farak hisab garne
3. farak ±0.5 mm bhitra chha bhane "OK", natra "NG"
4. natija abhilekh garne

yi 4 charan **manisale tay gareka niyam** hun. programale tinalai tyasai gari chalaunchha.

<!-- ne-cell: b2dfbcca | after-heading -->
**bastabama lekher heraun**
<!-- ne-pair: Let us write it -->

<!-- ne-cell: b2dfbcca -->
talako cellle mathika 4 charan lai tyasai gari Python ma lekheko chha. `def` bhaneko "function (kaamko samuh)
paribhashit garne" bhanne ho. ahile "`judge_width` naamle yi 4 charan lai eutai banaeko chha" bhanera bujhnuhos.

<!-- ne-cell: 836a01e2 | after-heading -->
### natijako udaharan

<!-- ne-cell: 836a01e2 -->
yo udaharan ma talako natija aaunchha (uhi input diiyo bhane uhi natija aaunchha). label bhane kodale chhapne
Japani aksharamai dekhinchha.

100.3 ra 99.7 ±0.5 mm ko simabhitrai parchhan; 100.6 ra 99.4 simabhanda alikati bahir; 103.2 dherai bahir.
nirnaya thyakkai chha, tar diieko maapan jati ramro chha tyati matra ramro hunchha.

<!-- ne-cell: b042214d | after-heading -->
**yo programale garne ra nagarne kaam**
<!-- ne-pair: What this program does, and does not do -->

<!-- ne-cell: b042214d -->
yo program **diieko maapan maanko nirnaya** ma thyakkai chha. chhito chha ra thakdain.
tar napne kaam kyamera, ujyalo ra maapan yantrako ho. nirnaya sahi bhae pani maapan maan galat bhayo bhane natija
galat hunchha.

aba chaudaijasto euta sankhyale lekhna gahro hune kaam heraun.

| kaam | manisale niyam lekhda hune samasya |
|---|---|
| sitako satahama "kalo thoplo" khojne | "kalo" lai sankhya ma lekhnuparchha. threshold ujyalosangai badlinchha |
| chot ra samanya dhancha chhutyaune | shabdama lekher sakindaina |
| "sadhainbhanda farak" khojne | "sadhain" lai sankhya ma paribhashit garna gahro |

yahan chhutyaunuparne kura **niyam kasale tay garchha** bhanne ho.

- manisale tay garchha: "maapan 99.5 mm bhanda kam bhae NG". yo samanya sbachalan (niyam ma adharit) ho.
- datale tay garchha: samanya utpadanaka udaharan baat threshold ra nirnaya garne tarika hisab garne. yo
  mesin larning ho.

kalo thoplojasto saral dosh ujyalo sthir rakhda "andhyaro pixel lai thresholdle chhutyaune" samanya
image processing le pani samhalna sakinchha. din 2 ma tyo prayas garnechhaun. dekhine tarika yati badlinchha ki
threshold manisale tay garna gahro hunchha, tyatibela udaharan baat tay garne tarika euta bikalp banchha. AI
prayog garne prakriya pani programakai rupama chalchha.

<!-- ne-cell: 2bbf0b0b | after-heading -->
## Part 2 sbachalan bhaneko ke ho

<!-- ne-cell: 28db0d04 | after-heading -->
**sbachalan = uhi prakriya mesinalai dohoryaun lagaunu**
<!-- ne-pair: Automation = letting a machine repeat a fixed procedure -->

<!-- ne-cell: 28db0d04 -->
sbachalan bhaneko **tay bhaisakeko prakriya mesinalai dohoryaun lagaunu** ho. nirnayako niyam manisale lekheko
wa udaharan baat paieko dubai huna sakchha. mesinale chhanieko prakriya dohoryaunchha.

utpadan lineko udaharan:

- kanbeyarale utpadan bokne (sbachalan)
- nishchit samayma kyamerako shatar thichne (sbachalan)
- maapan maan manakbhitra chha ki chhaina nirnaya garne (sbachalan. niyam mathi lekhejastai)

sbachalan niyam **spasht lekhna sakine** kaam ma dherai baliyo hunchha.

AI prayog garne prakriya pani computer ma euta programakai rupama chalchha. farak **nirnayako niyam manisale
lekhne ho ki datale tay garne ho** bhanne ma matra ho.

<!-- ne-cell: fig-teach_inspection_roles | after-heading -->
### nirikshanka 4 charan (saral banaiyeko prabah)

<!-- ne-cell: fig-teach_inspection_roles | after-image:../../assets/diagrams/teach_inspection_roles.png -->
chitra: nirikshan lai "khichne → pixel maan baat nap ra lakshan nikalne → nirnaya garne → chalaune" gari 4 charan ma
bandieko saral chitra (yojanabaddha). yo AI prayog garna sakine kshetrako sima dekhaune chitra hoina.

**dhyan dinuparne kura**

yi 4 charan **byakhyaka lagi saral banaieka** hun. AI le "nirnaya garne" matra hoina, nap ra lakshan anuman
garne, kshetra chhutyaune kaam pani garna sakchha. pixel bhitra pahilai sankhya hunchha, tyasaile "pixel sankhya
banaune" hoina "pixel maan baat nap ra lakshan nikalne" bhanera bujhnuhos. khichai naramro bhayo bhane model
pherer pani dherai jaso abastha ma ukasna sakindaina.

**sochnuhos**

- 4 charanamadhye AI prayog garna sakine ③ matra ho?

<!-- ne-cell: 7d23eed7 | after-heading -->
**dohorine kaam aphain heraun**
<!-- ne-pair: See the repetition -->

<!-- ne-cell: 7d23eed7 -->
din ma 10,000 pana nirikshan garnuparchha bhanaun. mathiko function 10,000 patak bolae,
manisalai kehi ghanta lagne kaam 1 sekendamai sakinchha.

talako cellle 1,000 maapan maan sbatah nirnaya garera NG ko sankhya ganchha. `for` bhaneko "dohoryaune" bhanne ho.

<!-- ne-cell: 3a7aa970 | after-heading -->
### natijako udaharan

<!-- ne-cell: 3a7aa970 -->
yo udaharan ma talako natija aaunchha (seed sthir rakhieko chha, tyasaile uhi batabaran ma uhi natija aaunchha).
label kodale chhapne Japani aksharamai dekhinchha.

yahan sabai utpadan ramra chhan, tyasaile 90 NG sabai galat asbikriti (false reject) hun. yo chalaima doshka
namuna chhainan, tyasaile chhutne dar dekhauna sakindaina.

<!-- ne-cell: 943e94e6 | after-heading -->
### ujyalo badalinda ramra utpadan NG hunchhan

<!-- ne-cell: 943e94e6 | after-image:../../assets/diagrams/teach_brightness_shift.png -->
chitra: ramra utpadanako brightness bitaran (nilo) ra ujyalo farak pareko dinko bitaran (pahenlo). rato
rekha sikieko tallo sima ho.

**dhyan dinuparne kura**

sikai bhaeko "nilo bitaran" baat matra ho. ujyalo kam hunda uhi ramra utpadan pahenlo bitaran ma sarchhan, rato
rekhabhanda tal parchhan ra NG bhaninchha. yo **galat asbikriti (false reject)** ho. Model bigreko hoina.
**sikai bhaeko belako sartabhanda farak sart** karan ho.

yahan "sart" bhannale ujyaloko matra bujhnuhos. utpadan line ma talaka sart badalinda chitrako dekhine tarika
ra scoreko bitaran sarna sakchha.

| badalin sakne sart | udaharan |
|---|---|
| ujyaloko matra ra rangako tapakram | phlorosent pherer LED rakhiyo, beluka bhayo |
| kyamerako exposure ra gain | auto-exposure le kaam gar‍yo |
| lens, duri, kon | jig pheriyo, lens mail bhayo |
| pachhadiko drishy ra parabartan | r‍yak sariyo, kabhar hataiyo |

kun sartale kati asar garchha bhanne kura paribartanako kisim ra kaam ma nirbhar hunchha. sart badaliyo bhane nirnaya
abashy badlinchha bhanne niyam chhaina. tyasaile "score" matra hoina, **tyo din ke, kun sartama khichiyo** pani
abhilekh garnuhos.

**sochnuhos**

- yo chitrako jasto kura nadohorin utpadan line ma ke abhilekh rakhnuparla?

<!-- ne-cell: b80511ca | after-heading -->
**manisale niyam tay garna nasakne bela**
<!-- ne-pair: When a person can no longer fix the rule -->

<!-- ne-cell: b80511ca -->
chaudaiko nirnaya **chaudai bhanne euta sankhya** bhaeko hunale sajilo bhayo. tar utpadan line ma yasto anurodh
aaunchha.

> "sitako satahama kahilekahin sano kalo thoplo parchha. yo sbatah patta lagaun chahanchhu."

"kalo thoplo" ko niyam sankhya ma lekhna khojda yasta samasya aunchhan.

- ujyalo 100 bhanda kam → ujyalo kam bhaeko din sabai NG hunchha
- byas 3 mm bhanda badhi → 1 mm ko thoplo chhutchha
- akar golo → chot chhutchha

sart thapdai janda niyam jatil banchha, ra tyo **line anusar farak** parchha. ujyalo ra kyamera sthir rakher
sadharan threshold ra contour le pugne pani hunchha (din 2 ma janchnechhaun). napugne abastha bhane dekhine
tarika yati badlinchha ki **manisale threshold tay garna nasakne** bela ho. tyatibela ramra utpadanaka
udaharan baat dayara wa nirnaya tay garne tarika (mesin larning) euta bikalp banchha.

<!-- ne-cell: 74f143d9 | after-heading -->
## Part 3 AI, mesin larning, dip larning

<!-- ne-cell: 1e0f9b0e | after-heading -->
#### pahile tinabata shabd matra

<!-- ne-cell: 1e0f9b0e -->
AI bauddhik kaamko samuhik naam ho, mesin larning udaharan baat niyam nikalne tarika ho, ra dip larning
bahu-tah nyural netabark prayog garne mesin larning ho.
ahile "manisale tay gareko niyam" ra "udaharan baat tay bhaeko niyam" chhutyaun sake pugchha.
bigya pranali (expert system) jasta bistrit bargikaran pachhi aune aichchhik khandama chha.

<!-- ne-cell: fig-teach_ai_ml_dl_nested | after-heading -->
### AI, mesin larning, dip larning kasari bhitra-bhitra parchhan

<!-- ne-cell: fig-teach_ai_ml_dl_nested | after-image:../../assets/diagrams/teach_ai_ml_dl_nested.png -->
chitra: AI ⊃ mesin larning ⊃ dip larning bhanne samabesh sambandh ra pratyekako euta udaharan (yojanabaddha).

**dhyan dinuparne kura**

samabesh  dip larning ⊂ mesin larning ⊂ AI jastai rahanchha. manisale lekheko if baky matra bhaeko nirnaya
"samanya sbachalan" ho, tyas lai AI bhandainaun. niyam ma adharit AI ma bigyako jnan if bakyko rupama
lekhieko expert system pani parchha. mesin larning ho ki hoina bhanne chhutyaune kura "niyam manisale lekhyo ki
udaharanle tay gar‍yo" bhanne ho. decision tree jasta kehi abastha ma sikieko natija if bakyko rupama pani
lekhna sakinchha.

**sochnuhos**

- "chaudai 100±0.5 mm bhitra chha bhane OK" bhanne if baky AI, mesin larning, samanya sbachalanamadhye kun ho?

<!-- ne-cell: fig-teach_train_vs_inference | after-heading -->
### sikai/tayari ra anuman

<!-- ne-cell: fig-teach_train_vs_inference | after-image:../../assets/diagrams/teach_train_vs_inference.png -->
**dhyan dinuparne kura**

sikai/tayari (fit) bhaneko nayan chitrako nirnaya garna chahine jankari banaune charan ho. chitra ma "bajan update"
bhanieko YOLO ko udaharan ho. yo patakako PatchCore le backbone sthir rakher samanya lakshan surakshit garchha.
anumanle surakshit abastha nabadali prayog garchha. threshold chhanne kaam chhuttai calibration kaam ho.

| tarika | input → tayari → anuman |
|---|---|
| YOLO | label bhaeka chitra → bajan update → bakas anuman |
| PatchCore | samanya chitra → samanya memory banaune → lakshan tulna |

yo saral banaiyeko tulna ho. **sochnuhos**

anuman: threshold matra badalda bajan badlinchha? talako udaharan chalaera
euta input badalnuhos. nirnaya ra surakshit abastha lai chhutyaera byakhya garnuhos.

<!-- ne-cell: d0b8452e | after-heading -->
## Part 4 niyam ra sikaiko farak

<!-- ne-cell: 6671ed4e | after-heading -->
### niyam lekhine nirikshan ra udaharan baat sikine nirikshan

<!-- ne-cell: 6671ed4e | after-image:../../assets/diagrams/teach_rule_vs_learned.png -->
chitra: mathillo pangkti niyamle lekhna sakine nirikshan, tallo pangkti udaharan baat sikne nirikshan.

**dhyan dinuparne kura**

mathillo pangktima manisale "99.5 mm bhanda kam bhae NG" bhanera tay garchha. tallo pangktima threshold manisale
tay gardaina. ramra utpadanaka udaharan diinchha ra **dayara wa nirnaya ma prayog hune sankhya data baat tay
garinchha**. tar "ke herne" (yo saral udaharan ma ujyalo) bhane yahan manisale nai chhaneko chha.

**sochnuhos**

- tapainko prakriyama ahile "niyam" ko rupama lekhna sakine nirikshan kun ho? ujyalojasto "herne thaun"
  aphain chhanna saknuhunchha?

<!-- ne-cell: clarity-workflow-rule | after-heading -->
#### sbachalan ra nirnaya garne tarika

<!-- ne-cell: clarity-workflow-rule -->
kyamera/maapan → sankhya input →〔sthir niyam wa udaharan baat paieko niyam〕→ OK/NG → log.
sbachalan bhaneko prabah dohoryaunu ho, AI apanaunu bhaneko tyabhitrako nirnaya garne tarika chhannu ho.

<!-- ne-cell: 10d61c4a | after-heading -->
#### uhi 5 maan lai dui tarikale nirnaya garne

<!-- ne-cell: 10d61c4a -->
kritrim brightness maan `[198,202,204,206,210]` prayog garnuhos. manisale sthir gareko tallo sima 200 ra
samanya udaharan baat paieko nyoonatam 198 tulna garnuhos. **nyoonatam maan sikne khelauna matra ho, yo
PatchCore hoina.**
anuman: 198 ko nirnaya dui tarikama uhi hunchha? sthir niyam ra udaharan baat paieko sankhyako farak hernuhos.
samanya udaharan matra bhaera dosh chhuteko sankhya napna sakindaina.

<!-- ne-cell: clarity-five-brightness-followup -->
198 matra sthir tallo sima ma NG hunchha, udaharan baat paieko sima ma sabai OK hunchhan.
sano prayog: samanya udaharanko 198 lai 196 banaunda paine tallo sima kati hola? nayan dosh pani pas hune
sambhabana chha?

<!-- ne-cell: clarity-optional-statistics | after-heading -->
### aichchhik: statistics baat samanya dayara anuman garne

<!-- ne-cell: clarity-optional-statistics -->
pahilo patakama chitrako akar ra "samanya udaharan matrale chhuteko dosh ganna sakindaina" bhanne kura matra janche pugchha.
ausat, standard deviation ra normal distribution ko hisab dosro patakako thap ho. pachhika abhyas ma prayog hune
tayari kod kramaisang chalaun sakinchha.

<!-- ne-cell: e6d3e3e3 | after-heading -->
### natijako udaharan

<!-- ne-cell: e6d3e3e3 -->
yo udaharan ma talako natija aaunchha (seed sthir chha. antim angk NumPy ko sanskaranaanusar farak parna sakchha).
label kodale chhapne Japani aksharamai dekhinchha.

phailabat hernuhos: standard deviation karib 3.5 bhaeko hunale arko charan ma prayog hune ausat ± 3σ ko dayara
karib 21 brightness tah pharakilo hunchha.

<!-- ne-cell: fig-teach_gaussian_vs_skewed | after-heading -->
### dubaitir saman ra normal distribution uhi kura hoina

<!-- ne-cell: fig-teach_gaussian_vs_skewed | after-image:../../assets/diagrams/teach_gaussian_vs_skewed.png -->
chitra: dubaitir saman tar normal distribution nabhaeko bitaran (bayan) ra normal distribution (dayan) ko
tulna (yojanabaddha).

**dhyan dinuparne kura**

dubaitir saman hunuko arth normal distribution hunu hoina. normal distribution ma janasankhya ausat μ baat
janasankhya standard deviation σ ko 3 gunbhitra karib 99.73% maan parchha. tar simit samanya chitra baat anuman
garieko ausat ra standard deviation bhaekole bastabik anupaat yo sankhya sang milnaiparchha bhanne chhaina.

**sochnuhos**

- yo dubaitir saman bitaran ma μ±3σ bahir 0.27% bhanda badhi kina parna sakchha?

<!-- ne-cell: cffec913 | after-heading -->
**threshold data baat tay garne**
<!-- ne-pair: Determine the threshold from data -->

<!-- ne-cell: cffec913 -->
ramra utpadanako maan **normal distribution (dubaitir saman ghanti akarako bitaran)** pachhyaunda janasankhyako karib
**99.73 %** maan "janasankhya ausat ± 3 × janasankhya standard deviation" bhitra parchha. **yo 99.73 % normal
distribution bhanne manyatamathiko gun ho.** dubaitir saman hunu matrale normal distribution bhanna mildaina.
puchchharako akar farak bhae uhi ±3σ bhitra parne anupaat farak parchha (mathiko chitra hernuhos).

yo talim ma simit sankhyaka samanya chitra baat ausat ra standard deviation **anuman** garchhaun.
tyasaile bastabik anupaat 99.73 % sang milnaiparchha bhanne chhaina. yo anuman bhaekole najikako maan matra ho.

```text
tallo sima = ausat - 3 × standard deviation
mathillo sima = ausat + 3 × standard deviation
```

yo dayaralai **samanya dayara** bhannechhaun. yo yahanko udaharan ma **sikai** ko natija ho.

samanya utpadanako data matra bhaera "dosh chhuteko sankhya" ganna sakindaina. ganna sakine "ramra utpadanalai NG
bhanieko sankhya (galat asbikriti)" matra ho. chhuteko ganna dosh label bhaeka chitra chahinchha.

<!-- ne-cell: e14bfbfe | after-heading -->
### natijako udaharan

<!-- ne-cell: e14bfbfe -->
yo udaharan ma talako natija aaunchha (seed sthir chha. antim angk NumPy ko sanskaranaanusar farak parna sakchha).
label kodale chhapne Japani aksharamai dekhinchha.

sikieko dayarako najikaka dui maan sbikarinchhan, dherai bahiraka dui asbikarinchhan. nirnayale ramra
namunabat sikieka dui sankhya matra prayog garchha.

<!-- ne-cell: 8a380704 | after-heading -->
**"sikiyo" bhannuko arth ke ho**
<!-- ne-pair: What 'trained' actually means -->

<!-- ne-cell: 8a380704 -->
yo udaharan ma data baat tay bhaeko kura `mean_brightness` ra `std_brightness` bhanne
**dui sankhya** hun. yi dui nai "sikaiko natija" hun.
purna dip larning ma yi sankhya lakhaundekhi karodaun hunchhan. tar **sochne tarika uhi** ho.

- **sikai (training)**: data herer model bhitraka sankhya (bajan, parameter) tay garne
- **anuman (inference)**: sikaile tay gareka sankhya tyasai prayog garera nayan datako nirnaya garne

kati samay lagchha ra kati patak chalchha bhanne **paribhasha hoina, samanya udaharan matra** ho. sikai jati patak pani
dohoryaun sakinchha, ra batch inference jastai dherai ekaipatak chalaune pani hunchha. anuman mahango ra samay lagne
model pani hunchhan.

chhutyaunuparne dui kura:

- **model ko bajan**: sikaile tay garchha, anuman ma badalindain
- **nirnayako threshold**: utpadan line ma badalna sakinchha. badalda bajan badalindain, tar **nirikshan pranali
  samagrale garne pathaune nirnaya badlinchha**

> "threshold badalen tar sikieko model badalien" bhanne lagchha bhane, chaleko kura yi duimadhye euta matra ho.

<!-- ne-cell: clarity-optional-taxonomy | after-heading -->
### aichchhik: shabdaharuko bistrit bargikaran

<!-- ne-cell: clarity-optional-taxonomy -->
#### tin shabdako sambandh
yi tin alag-alag prabidhi hoinan, **bhitra-bhitra parne (thulo-sano sambandh)** ho.

```text
kritrim bauddhikata AI
 └── mesin larning Machine Learning
      └── dip larning Deep Learning
```

| shabd | arth (saral) | utpadanama udaharan |
|---|---|---|
| kritrim bauddhikata AI | manisako bauddhik kaam computerle garne sochako samuhik naam | "manisako ankhale gardai aeko nirikshan mesinale garne" |
| mesin larning ML | udaharan baat niyam bhettaera nirnaya ma prayog hune sankhya data baat tay garne | 500 ramra utpadanako chitra baat "samanya dayara" sikne |
| dip larning DL | bahu-tah nyural netabark prayog garne mesin larning | chitra baat dosh bhettaune (YOLO, PatchCore adi) |

arthat dip larning mesin larningko ek kisim ho, ra mesin larning AI ko ek kisim ho.
"AI" bhanda tyo aniwarya dip larning nai ho bhanne hundaina.

AI ma sikai nagarne pani chhan. bigyako jnanalai "yadi yasto bhae yasto" bhanne niyamko rupama dherai lekher
tinalai joder anuman garne tarikalai **niyam ma adharit AI (expert system)** bhaninchha.
tar chaudaiko nirnayako euta if baky matra **samanya sbachalan** ho, tyas lai matra AI bhandainaun.
niyam joder nirnaya banaiyeko chha ki chhaina bhanne kura chhutyaune adhar ho.

mahattwapurna kura **niyam kasari paiyo** bhanne ho. manisale lekhyo bhane niyam ma adharit, udaharanle tay gar‍yo
bhane mesin larning. sikieko decision tree pachhi if bakyko rupama lekhna sakinchha. taipani ti niyam data baat
tay bhaeka, arthat mesin larningko natija hun.

yo talim ma prayog hune PatchCore le sikieko dip lakshan nikalne bhaag (sikieko bajan prayog garne ansh) ra
samanya chitraka lakshan jamma garieko memory baink (sikaile banaune ansh) jodchha.

<!-- ne-cell: 656d0ff1 | after-heading -->
## Part 5 sikai data ra AI le galti garne karan

<!-- ne-cell: d17a6856 | after-heading -->
**sikai data ekatarphi bhae AI pani ekatarphi hunchha**
<!-- ne-pair: Biased training data makes a biased model -->

<!-- ne-cell: d17a6856 -->
mathiko sikaile "ramra utpadan 200" matra prayog gar‍yo. yadi ti 200 bata
**phlorosent kam bhaeko din khichieka photo matra** thie bhane ke hunthyo?

sikieko samanya dayara "andhyarotir" sarchha. tyaspachhi ujyalo din khichieko **ramro utpadan** pani
NG bhaninchha. yo **galat asbikriti (false reject)** ho.

ulto, samanya dayara dherai pharakilo bhayo bhane **sanchchaiko dosh** chhutna sajilo hunchha. yo
**galat sbikriti (false negative)** ho.

kun lai badhi mahattb dine bhanne **tyo nirikshanko abashyakata** le tay garchha. doshayukt utpadan bajarama
janai nahune prakriyama chhutne (false negative) ghataunalai pahilo prathamikata diinchha. arkatir chhutne
ghataun threshold kada banaunda ramra utpadanako galat nirnaya (false reject) badhchha, ra line rokine wa
punahkam garne kharch badhchha. dubai sbikary chhainan bhane tyo nirikshanko abashyakata ahileko tarikale pura
bhaeko chhaina bhanne bujhnuparchha.

<!-- ne-cell: 218477f8 | after-heading -->
### natijako udaharan

<!-- ne-cell: 218477f8 -->
yo udaharan ma talako natija aaunchha (seed sthir chha. antim angk NumPy ko sanskaranaanusar farak parna sakchha).
label kodale chhapne Japani aksharamai dekhinchha.

maan 206.0 purna rupama ramro utpadan ho; sikieko dayara andhyaro dinko data baat matra baneko hunale
tyo asbikar bhayo.

<!-- ne-cell: 1d1e4928 | after-heading -->
**AI le galti garne karan (saransh)**
<!-- ne-pair: Why AI makes mistakes (summary) -->

<!-- ne-cell: 1d1e4928 -->
karan mukhyatah 5 bata chhan.

1. **sikai data apug** — ramra utpadan 5 batale samanya phailabat dekhauna dherai jaso pugdain
2. **sikai data ekatarphi** — andhyaro din matra, euta kisim matra
3. **sikai data ma jabaph (label) ko galti** — dosh nadekher "samanya" bhanera label lagaunu
4. **utpadan ra sikaiko sart farak** — ujyalo, lens, duri, gati badaliyo
5. **chitramai nadekhine wa chhutyaun nasakine farak** — 0.3 mm ko dosh resolution kam bhaera metiyo,
   wa contrast noise bhitra harayo

panchaun karan AI ko hoina, **kyamera, ujyalo ra prakashiki (optics)** ko samasya ho. yo hapta 2 ma
samhalinechha.

<!-- ne-cell: 6adce078 | after-heading -->
## Part 6 nirdeshit prayog

<!-- ne-cell: b66a97de | after-heading -->
**maan badaler natijako paribartan anuman garnuhos**
<!-- ne-pair: Change parameters and predict what happens -->

<!-- ne-cell: b66a97de -->
talako cell ma 4 bata niyantran chhan. **chalaunuaghi** natija anuman garnuhos.

| niyantran | badaler herne maan | anuman garne kura |
|---|---|---|
| `k` (kati gun standard deviation) | 1, 2, 3, 4 | NG ko sankhya badhchha? ghatchha? |
| `good_mean` (ramra utpadanako ausat) | 190, 205, 215 | sikaiko natija ke hunchha? |
| `n_good` (sikai chitra sankhya) | 10, 200, 2000 | sikieko dayara sthir hunchha? |
| `seed` (random sankhyako suru bindu) | 7, 1, 2, 3 | uhi setting ma pani natija farak parchha? |

`seed` badalda **sikaika lagi data feri liinchha** (jaanchko data sthir rahanchha).
`n_good` sano hunda harek patak feri linda sikieko dayara sarchha. sikai chitra sankhyako asar herda
`seed` kehi bata tarikale prayas garera **dayara kati phailinchha** bhanne tulna garnuhos.

<!-- ne-cell: 117ecad5 | after-heading -->
**dhyan dinuparne kura**
<!-- ne-pair: What you should notice -->

<!-- ne-cell: 117ecad5 -->
yo cell ma `seed` sthir chha, tyasaile **uhi settingle jati patak chalae pani uhi natija** aaunchha.
`n_good = 10` rakher `seed` 7 → 1 → 2 → 3 badalda sikieko samanya dayara sarne dekhinchha.
`n_good = 2000` banaunda `seed` badale pani dayara khasai sardain.

**sikai data kam bhae sikaiko natija sthir hundaina** bhanne kura yahi ho.
yo "harek chalaima badlinchha" hoina, "**arko** 10 bata jamma gare natija badlinchha" bhanne ho.
din 4 ra din 5 ma samhaline purna model ma pani yahi hunchha.

<!-- ne-cell: 4edd22fb | after-heading -->
## abhyas

<!-- ne-cell: 0e8f4450 | after-heading -->
#### abhyas 1 (adharabhut): diieko function chalaera natija anuman garne

<!-- ne-cell: 0e8f4450 -->
talako cell ma **pahilai lekhieko function** `judge_thickness` chha. function lekhne tarika din 2 ma siknechhaun.
aj **nabadali chalaera** natija anuman garnuhos.

| anuman | maan |
|---|---|
| manakbhitra | 1.95, 2.0, 2.1 |
| manakabahir | 2.15 |

**sakieko thanne adhar:** charabatai maanka lagi anuman ra natija tulna garera mileko sankhya lekhnuhos.
namileko maan bhae tyo ra karan pani lekhnuhos. charabatai mile "sabai milyo" lekhe pugchha.

> aphnai function lekhne abhyas **din 2 notebook 02 ko abhyas 1** ma chha.

<!-- ne-cell: 3bf0f138 | after-heading -->
**abhyas 2 (madhyam): samanya dayara pharakilo/sanghuro banaune**
<!-- ne-pair: Exercise 2 (intermediate): widen or narrow the normal range -->

<!-- ne-cell: 3bf0f138 -->
Part 6 ma `k` lai 1 dekhi 4 samm badaler ramra utpadan NG bhanieko sankhya (galat asbikriti) talika ma
lekhnuhos. tyaspachhi dui prashnako jabaph dinuhos.

1. `k` thulo banaunda galat asbikriti kasari badlinchha?
2. uhi kaamle **chhutne (false negative)** kasari badlinchha bhanera sochnuhos.

yo abhyasko jaanch data **sabai ramra utpadan** hun. tyasaile ganna sakine galat asbikriti matra ho,
chhuteko sankhya napna sakindaina. 2 ko jabaph "aba dekhi huna sakne kura" ko rupama lekhnuhos.

**sakieko thanne adhar:** 4 pangktiko talika ra dui jabaph lekhnuhos. chhuteko sankhya napejhain
nalekhnuhos.

<!-- ne-cell: c6260d3b | after-heading -->
**abhyas 3 (bikas/aichchhik): niyamle lekhine ra udaharanle tay garne bhaag chhutyaune**
<!-- ne-pair: Exercise 3 (optional challenge): separate what a rule can decide from what examples decide -->

<!-- ne-cell: c6260d3b -->
"chaudaiko nirnaya" niyamle lekhna sakiyo. "kalo thoplo patta lagaune" ma threshold manisale tay garna
nasakne huna sakchha. karan aphno utpadan lineko shabdama 3 pangktibhitra lekhnuhos. tyaspachhi niyamle lekhna
sakine bhaag ra udaharan baat tay garnu ramro hune bhaag talako talika ma chhutyaera lekhnuhos.

**sakieko thanne adhar:** niyamle lekhine kaam ra udaharan baat tay garnu ramro hune kaam dubaitir kamtima
3/3 bata lekhnuhos.

<!-- ne-cell: 82dd44f4 | after-heading -->
#### bujhai jaanch

<!-- ne-cell: 82dd44f4 -->
talaka prashnako jabaph aphnai shabdama dinuhos.

1. "manisale niyam lekhne prakriya" ra "data baat niyam tay garne prakriya" ko farak aphno karyasthalako
   kaam lai udaharan banaera bujhaunuhos.
2. mesin larning ra dip larningamadhye kun pharakilo abadharana ho? karan pani lekhnuhos.
3. sikai ra anumanko farak "ke tay garne" ra "ke lagu garne" bhanne drishtile bujhaunuhos.
   samay ra datako matralai tyasko samanya udaharanko rupama ullekh garnuhos.
4. ramra utpadanako photo matrale sikeko model le bastabik line ma galat nirnaya garne dui karan lekhnuhos.
5. galat asbikriti ra chhutnemadhye kun lai badhi mahattb dine bhanne kasale tay garchha? aphno prakriyalai
   udaharan banaera lekhnuhos.

namuna jabaph `docs/instructor/day01_instructor_guide.md` ma chhan.
ti padhnuaghi aphnai jabaph lekhnuhos.

<!-- ne-cell: d40c2add | after-heading -->
## samasya aunda

<!-- ne-cell: d40c2add -->
truti ae pahile "kun cell ma", "kun line ma", "ke sandesh ayo" bhanera tipnuhos. bujhaunuparne kaam ma pani
tyahi abhilekh rakhnuhos.

| lakshan | ke garne |
| --- | --- |
| `ModuleNotFoundError: No module named 'numpy'` | kernel farak chha. `sys.executable` jaanchnuhos, tyaspachhi `Kernel` → `Change Kernel` → `Python 3 (AI Vision)` chhannuhos. |
| sankhya udaharanabhanda alikati farak (dashamalabako antim angk) | `seed` sthir rakhieka udaharan uhi batabaran ma uhi maan dinchhan. NumPy ko sanskaran farak bhae antim angk badalin sakchha. |
| NG ko sankhya jasta ganana udaharanabhanda farak | `seed`, `n_good`, `k` ko maan jaanchnuhos. yi tin farak bhae ganana pani farak parchha. |
| `NameError: name '...' is not defined` | aghillo cell chalaieko chhaina. mathibat kramaisang feri chalaunuhos. |
| `TypeError: 'list' object is not callable` | chalako naam ma `list` wa `sum` jasta built-in naam prayog garda hunchha. arko naam rakhnuhos. |
| memory apug (`MemoryError`) | yo abhyas ma samanyatah hundaina. `n_good` ma atyadhik thulo maan rakhieko bhae ghataunuhos. |

<!-- ne-cell: 99832686 | after-heading -->
## sakieko janchasuchi

<!-- ne-cell: 99832686 -->
**aniwarya** bastuharu matra suchibaddh chhan. sabai ma chinh lagepachhi yo notebook sakinchha.

- [ ] Part 1–Part 6 ka byakhya padhen
- [ ] sabai kod cell mathibat kramaisang chalaen
- [ ] abhyas 1–2 (aniwarya) garen
- [ ] nirdeshit prayog ma `k`, `n_good`, `seed` badaler heren
- [ ] bujhai jaanchka 5 prashnako jabaph dien
- [ ] galat asbikriti ra chhutne farak aphnai shabdama bujhaun sakchhu
- [ ] trutiko abhilekh rakhen (nabhae "chhaina" lekhen)
- [ ] yo notebook surakshit garen

**aichchhik (sakieko sartama pardaina):** abhyas 3 ra "thap sikai" ko atirikt chunauti. samay banki bhae matra
garnuhos.

<!-- ne-cell: 9c628291 | after-heading -->
## thap sikai (aichchhik)

<!-- ne-cell: 9c628291 -->
### sandarbha lingk

- [Python adhikarik tutorial (Japani)](https://docs.python.org/ja/3/tutorial/)
- [scikit-learn: mesin larningko soch](https://scikit-learn.org/stable/getting_started.html)
- [NumPy random generator](https://numpy.org/doc/stable/reference/random/generator.html)
- [hirosima kasei sandarbha samagri](../../docs/reference_materials.md)

### atirikt chunauti (aniwarya hoina)

`good_std` lai 1.0 ra 10.0 banaera sikieko samanya dayarako "chaudai" kasari badlinchha hernuhos.
dayara pharakilo hunda ke chhutna sajilo hunchha?

yo prayog ma pani ramra utpadan matra prayog bhaekole chhuteko sankhya napna sakindaina.
"dayara pharakilo banaunda kasto dosh banki rahan sajilo hunchha" bhanera shabdama jabaph dinuhos.
