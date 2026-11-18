<!--
Nepali anuwad / Nepali translation source for
notebooks/Day03_YOLO_Basics/Day03_03_YOLO_Experiments.ipynb
-->
# din 3 notebook 03 — Nepali anuwad

<!-- ne-cell: 60315362 | after-heading -->
# din 3 notebook 03: pahichanko natija padhne

<!-- ne-cell: 60315362 -->
## sikai lakshyaharu

| Nepali |
| --- |
| 1. confidence ko threshold badaler natija tulna garna sakne. |
| 2. pahichanko natijako nirdeshangk padher arth bataun sakne. |
| 3. bastabik tasbir ma jhuto pojitibh ra jhuto negetibh dekhauna sakne. |
| 4. tasbirko akar ghataunda kina pahichan gumchha bataun sakne. |
| 5. prayogko natija talika ma rakher riport garna sakne. |

## yo notebookko adharabhut jankari

| bishay | biwaran |
| --- | --- |
| sikai samay (anuman) | 110 minet |
| kathinai | surubati tah |
| poorwashart | din 3 notebook 01 ra 02 sakieko hunuparchha. |
| aawashyak laibreri | torch, ultralytics, opencv-python, numpy, matplotlib, pandas |
| prayog hune kernel | aivision |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 3](../../COURSE_SYLLABUS.md#day3) |

### bujhaunuparne kaam

| Nepali |
| --- |
| threshold anusar pahichan sankhyako talika |
| kamtima euta anishchit pahichanko punarabalokan abhilekh |

<!-- ne-cell: 5fdd18cf | after-heading -->
## yo notebook kahan parchha

<!-- ne-cell: 5fdd18cf -->
| bishay | biwaran |
| --- | --- |
| din | din 3 |
| ajako kram | ajako notabukamadhye 3 / 3 |
| lagne samay | 110 minet |
| poorwashart | `Day03_02_YOLO_Inference.ipynb` |
| ajako samayatalika | [`COURSE_SYLLABUS.md` din 3](../../COURSE_SYLLABUS.md#day3) |

dinko samayatalika `COURSE_SYLLABUS.md` ma eutai thaun ma chha. yo notebook tyasko euta bhaag matra ho.

<!-- ne-cell: audit-learning-loop | after-heading -->
### anuman garnuhos, chalaunuhos, hernuhos, byakhya garnuhos

<!-- ne-cell: audit-learning-loop -->
thresholdle ayat chhanne kaam ra tasbir sano banaune kaam farak prayog hun. mahattwapurna cell chalaunuaghi
input, kaam ra natija ek-ek bakyama lekhnuhos. pahile anuman garera chalaunuhos ra maan wa chitra hernuhos.
confidence matra badaler feri anuman gari chalaunuhos. janajan rakhieka truti ra nasakieka abhyaska nirdeshan
pachhyaunuhos.

<!-- ne-cell: ddb249df | after-heading -->
## Part 0 tayari

<!-- ne-cell: e00d64c2 | after-heading -->
## Part 1 confidence ko threshold

<!-- ne-cell: clarity-experiment-provenance | after-heading -->
### yo bhaagko srot chhutyaune

<!-- ne-cell: clarity-experiment-provenance -->
harek chitra wa talikaaghi A/B/C hernuhos. tasbir, model, purb-prashodhan ra ummedabarako samuh uhi nabhae
ganeko sankhya lai "thresholdko matra asar" bhanera tulna garna mildaina. `imgsz` bhaneko model ma diine tasbirko
akar ho.

| sandarbha | input sankhya | imgsz | anumanko tallo sima | ke thaha hunchha |
|---|---|---|---|---|
| A banaiyeko udaharan | 4 ummedabar | lagu hundaina | lagu hundaina | sthir samuh chhanne kaam |
| B surakshit 52 tasbir | 52 tasbir, 42 ma ummedabar | abhilekh jaanchnuhos | 0.01 | tyo surakshit chalaima matra |
| C1 aphnai bus anuman | 1 tasbir | 640 | 0.05 | uhi cache bhitrako tulna |
| C2 aphnai bus widget | 1 tasbir | 320 | 0.05 | C1 bhanda farak prayog |

confidence model ko score ho, sahi hune sambhabana aphain hoina. uhi ummedabar samuhama threshold badhaunda banki
sankhya badhdain. tallo simabhanda kam bhaeka ummedabar feri pharkaun sakindaina.

<!-- ne-cell: fig-teach_confidence_filter | after-heading -->
### thresholdle banki sankhya badalchha

<!-- ne-cell: fig-teach_confidence_filter | after-image:../../assets/diagrams/teach_confidence_filter.png -->
**A: banaieka 4 ummedabar**

chitra: eutai patakako anuman baat aeka 4 ummedabaralai 0.25, 0.50 ra 0.75 thresholdle chhanda aeko natija
(sansleshit tasbir, udaharanka lagi banaieka maan).

**dhyan dinuparne kura**

banki sankhya 3 → 1 → 1 ho. threshold badhaunda **sankhya nabadalin** pani sakchha — yahi chitrako mukhy kura ho.
phalieka ummedabar "abasthit chhainan" bhanne hoina, "sbikar garien" bhanne matra ho.

**sochnuhos**

- 0.50 ra 0.75 ma banki sankhya uhi kina hunchha?

<!-- ne-cell: fig-ref_confidence_counts | after-heading -->
### bastabik natija ma ganne

<!-- ne-cell: fig-ref_confidence_counts | after-image:../../assets/reference_outputs/ref_confidence_counts.png -->
**B: surakshit 52 tasbirko anuman**

chitra: yo talim ma sanchchai surakshit garieka 52 tasbirko anumanamadhye ummedabar banki raheka 42 tasbir ma,
threshold badalda NG thaharine tasbirko sankhya. dayan pratyek tasbirko adhikatam confidence. sandarbha natija.

**dhyan dinuparne kura**

anuman conf = 0.01 ma ek patak matra gariyo. **pahichan shunya banki raheka 10 tasbir** ma ummedabar nai chhainan,
tyasaile kunai thresholdle tinalai NG banaundain (surakshit 0 bhaneko "kamajor pahichan" hoina, chinh maan matra ho).
0.01 ma 42, 0.25 ma 28, 0.50 ma 23, 0.75 ma 13 tasbir.

**sochnuhos**

- threshold 0.01 baat 0.25 banaunda kati tasbir NG baat hatchhan? hateka tasbir lai "dosh chhaina" bhanna milchha?

<!-- ne-cell: 9082bf2f | after-heading -->
### pahichanle "ayataharuko soochi" pharkaunchha

<!-- ne-cell: 9082bf2f | after-image:../../assets/diagrams/diagram_detection.png -->
chitra: pahichanle ke pharkaunchha (yojanabaddha chitra). yo notebook 02 kai **eutai pahichan udaharan dohoryaieko**
chitra ho, chaar pyanalako chitra hoina. talako prayogle bastabik ayat ra sankhya badalchha.

**dhyan dinuparne kura**

model le dherai ummedabar dinchha, ra thresholdle tinamadhye "rakhne ki phalne" matra tay garchha. **model le
dekheka ummedabar aphain badalindainan.** threshold badhaunda banki sankhya **badhna sakdain**, tar **nabadalin pani
sakchha**. tyasaile "sankhya 0" ko arth "kehi asamanya chhaina" hoina.

**sochnuhos**

- threshold 0.9 banaunda banki sankhya sadhain 0 hunchha? kahile 0 hundaina?

<!-- ne-cell: 2abea6c2 | after-heading -->
**thresholdle "kasalai pahichan manne" tay garchha**
<!-- ne-pair: A threshold decides what counts as a detection -->

<!-- ne-cell: 2abea6c2 -->
model le dherai ummedabar dinchha. tinamadhye **confidence threshold wa badhi bhaeka matra sbikar** garinchha.

| threshold | natija |
|---|---|
| 0.90 | atyadhik uchcha scoreka pahichan matra. **chhutne (miss) badhna sakchha** |
| 0.25 | prayah prayog hune purbanirdharit maan |
| 0.05 | lagabhag sabai banki. **jhuto alarm badhna sakchha** |

uhi ummedabar samuhama threshold badhaunda **banki sankhya badhdain**, tar **ghatna pani sakdain** (yo talimko
chitra ma 0.50 ra 0.75 dubaima 1 bata banki thiyo). threshold ghataunda phalieka ummedabar pharker aunchhan; ti
"thienan" hoina, **phalieka** thie. kun threshold ma kati banki rahanchha bhanne kura data ra score ma nirbhar chha.

threshold **model le hoina, manchhele tay garne** sankhya ho. "chhutaunu hundaina" ki "jhuto alarm ghataunu
parchha" bhanne kurale badalnuparne maan farak parchha.

<!-- ne-cell: d87d261f | after-heading -->
### natijako udaharan — C1 surakshit udaharan

<!-- ne-cell: d87d261f -->
yo natija yo talim ma surakshit garieko abhilekh ho (`yolo26n.pt`, `imgsz=640`, `bus.jpg`). sukshma sankhya
batabaran anusar farak parchha, prabritti ra thulo-sanoko sambandh padhnuhos.

yo talika ma 0.25, 0.40 ra 0.60 sabai ma 5 bata chhan. **threshold badhaunda sankhya nabadaline** udaharan ho.
`max_conf` 0.000 hunu bhaneko banki pahichan shunya hunda adhikatam maan nabhaeko **dekhaiko maan** ho; kamajor pahichan
thiyo bhanne hoina.

ahileko C1 le sthir ummedabar prayog garchha. yo purano punah-anuman talikakai sankhya aaunchha bhanne chhaina.

<!-- ne-cell: 8aa62c20 | after-heading -->
**dhyan dinuparne kura**
<!-- ne-pair: What you should notice -->

<!-- ne-cell: 8aa62c20 -->
yo abhilekhit chalaima threshold 0.90 banaunda **basako pahichan (confidence 0.881) pani harayo**, kinabhane
0.881 < 0.90.

**"threshold badhaunu = kadai garnu" bhannale sahi pahichan pani phalnu** ho. kati banki rahanchha ra kun pahichan haraunchha
bhanne kura abhilekhit score ma nirbhar chha. 0.90 bhanda mathi ek pani nabhae sankhya 0 hunchha.

<!-- ne-cell: f0a405bf | after-heading -->
#### pahichan rakhne wa phalne sima herne

<!-- ne-cell: f0a405bf -->
**C2: aphnai bus tasbir, imgsz=320**

**anuman ek patak matra** chalchha; natija lai thresholdle chhanchha. threshold sarda feri anuman chaldain.

> yo cache **conf=0.05** ma banaiyeko chha. 0.05 bhanda kam ummedabar anumanakai bela phalieka hunale
> **yo soochi ma chhainan** ("abasthit chhaina" hoina, "yahan prayog garna mildaina"). tyasaile 0.05 bhanda kam
> threshold chhanna mildaina.

yo bhaagko sandarbha chitrale surakshit 52 tasbiramadhye **anumanko tallo sima 0.01 ma pahichan banki raheka 42
tasbir** ganchha. banki 10 ma "kamajor pahichan" thien; **ek pani ayat banki thien**. 0.01 bhanda kam ummedabar
abhilekhama nabhaeko hunale prayog garna sakindaina.

| anuman | ke herne |
|---|---|
| threshold badhaunda | banki pahichan kati? |
| 0.9 banaunda | banki sankhya badlinchha? |
| banki sankhya 0 | "kehi asamanya chhaina" kai arth ho? |

widget nabhae pani talako parameter cellle uhi prayog garna dinchha.

<!-- ne-cell: f9b7ab5c | after-heading -->
## Part 2 nirdeshangk padhne

<!-- ne-cell: 9890093b | after-heading -->
**nirdeshangk baat ke thaha hunchha**
<!-- ne-pair: What coordinates tell you -->

<!-- ne-cell: 9890093b -->
nirdeshangk padhda yi kura thaha hunchhan.

- bastuko **sthan** (tasbirko kahan)
- **ayatale dekhaune bistar** (chaudai, uchai). yo bastuko anumanit dayara ho, **doshko thyakkai nap hoina**
- tasbirko chheusang jodieko chha ki chhaina (**bichaima katieko** huna sakchha)
- eutai sthanama dherai pahichan chha ki chhaina (**dohoro pahichan**)

ayat model le "yahan bastu chha" bhanera anuman gareko dayara ho. doshko bastabik nap (mm) wa kshetraphal nikalna
calibration (din 2) ra napne tarika thik chha ki chhaina bhanne jaanch chhuttai chahinchha.

<!-- ne-cell: e502c791 | after-heading -->
**akar anupaat ma dekhaune**
<!-- ne-pair: Express size as a ratio -->

<!-- ne-cell: e502c791 -->
bastabik pikselama tulna garda tasbirko akar badalie arth bujhna gahro hunchha. **tasbirko tulna ma pratishat**
ma herda tasbirko akar badalie pani tulna garna sakinchha.

tar anupaatle tulna garna milne kura **dekhine kshetra (field of view) ra katieko bhaag uhi bhae** matra ho.
kyamerako duri, zoom wa katai badaliyo bhane uhi doshko anupaat pani badlinchha. dekhine kshetra farak bhaeka
tasbir tulna garda tyo farak abhilekh garnuhos.

<!-- ne-cell: d87bb599 | after-heading -->
## Part 3 tasbir pherer tulna garne

<!-- ne-cell: caae9118 | after-heading -->
## Part 4 jhuto pojitibh ra jhuto negetibh

<!-- ne-cell: 92bbe170 | after-heading -->
**tasbir-starka chaar abastha**
<!-- ne-pair: The four image-level outcomes -->

<!-- ne-cell: 92bbe170 -->
euta tasbir lai **OK ki NG** bhanera nirnaya garda natija yi charamadhye ek hunchha.

| tasbir-starko nirnaya | bastabama dosh chha | bastabama samanya chha |
|---|---|---|
| **NG bhaniyo** | sahi pahichan (true positive) | **jhuto pojitibh** (false positive, jhuto alarm) |
| **OK bhaniyo** | **jhuto negetibh** (false negative, chhutnu) | sahi (true negative) |

**utpadan nirikshan ma jhuto negetibh (chhutnu) bishesh gambhir** hunchha, kinabhane bigreko saman pathainchha.
arkotir jhuto pojitibh dherai bhae line barambar rokiera kamadar thakchhan.

tyasaile **kun kura kati sbikar garne** pahile nai tay garnuparchha.

**bastu pahichan ma yi chaar sidhai ganna mildaina.** anuman garieko ayat ra sahi ayat milaunuparchha; namileko anuman FP,
namileko sahi bastu FN ho. purai prishthabhumilai TN ganer rakhna mildaina (bastu-starko mulyankan din 4 ma aaunchha).

<!-- ne-cell: 73de97ad | after-heading -->
**confidence ra sahi hunu farak kura**
<!-- ne-pair: Confidence and correctness are different -->

<!-- ne-cell: 73de97ad -->
yi dui **dubai hunchhan**.

- **kam confidence bhaeko pahichan sahi huna sakchha** — sano ra dekhna gahro, tar bastabik
- **uchcha confidence bhaeko pahichan galat huna sakchha** — model dekhine rupale thagieko

tyasaile "confidence badhi chha, tyasaile thik chha" bhanna mildaina. sathai **kam confidence bhaneko "shangkaspad" matra ho,
galat bhanera tunggo lageko hoina**. **tasbir herer janchnu** nai yo talim ma ra byabaharama pani adhar ho.

<!-- ne-cell: fig-teach_score_vs_correctness | after-heading -->
### asaphalatako prakar confidence le chhutyaune

<!-- ne-cell: fig-teach_score_vs_correctness | after-image:../../assets/diagrams/teach_score_vs_correctness.png -->
chitra: confidence ra sahi hunulai sangai rakher, threshold mathi-tal asaphalata kasari bandinchha dekhaune chitra
(maan udaharanka lagi).

**dhyan dinaparne kura**

threshold ghataunda "kam confidence bhaeko sahi pahichan" joginchha, sangai "kam confidence bhaeko galat pahichan" pani
bhitra parchha. euta patti matra hataun sakindaina.

**sochnuhos**

- yi 5 madhye threshold 0.30 banaunda kati galat pahichan banki rahanchhan?

<!-- ne-cell: 4a886707 | after-heading -->
**anishchit pahichan abhilekh garne**
<!-- ne-pair: Record an uncertain detection -->

<!-- ne-cell: 4a886707 -->
talako cellle `bus.jpg` ko natija baat **kam confidence bhaeka pahichan** soochi ma rakhchha. kam bhae jati "shangkaspad"
ummedabar hun.

abhyas ma yimadhye euta chhaner **tasbir sang tulna gari** "sahi / galat / nirnaya garna sakindaina" madhye euta
abhilekh garnuhos. tyaspachhi **kina kam bhayo** (dherai sano, lukeko, dekhine rup milne) bhanera **anuman** lekhnuhos.
tasbir herer pani nirnaya garna nasakine huna sakchha; tyas abastha ma "nirnaya garna sakindaina" lekhnuhos.

<!-- ne-cell: d3580c9b | after-heading -->
## Part 5 rijolyusan ra sana bastu

<!-- ne-cell: fig-teach_resolution_effect | after-heading -->
### rijolyusanale dosh kasari dekhinchha tay garchha

<!-- ne-cell: fig-teach_resolution_effect | after-image:../../assets/diagrams/teach_resolution_effect.png -->
chitra: uhi sansleshit tasbir sano banaunda dosh kasari dekhinchha ra kendrako pikselama kati farak parchha (ganana garieka maan).

**dhyan dinaparne kura**

ek pikselabhanda sano doshle pani tyo pikselako chamak badalna sakchha. tar akar ra sthan bharapardo rupama thamyaun
sakinchha bhanne chhaina. dekhine kshetra, interpolation ra banki raheko contrast chhuttachhuttai padhnuhos.

**sochnuhos**

- 0.5 px ko dosh pani thresholdle bhetna saknuko karan ke ho?

<!-- ne-cell: 860a5fd3 | after-heading -->
**tasbir sano banaunda pahichan gahro hunchha**
<!-- ne-pair: Shrinking an image makes detection harder -->

<!-- ne-cell: 860a5fd3 -->
model le input lai tokieko akar (`imgsz`, purbanirdharit 640) ma badaler prashodhan garchha. mul tasbir sano
bhae **sana bastu kehi pikselama matra banki rahanchhan**.

din 1 ma dekhejastai ek pikselabhanda sano doshle pani pikselako chamakama asar garna sakchha. tar tyasko
**akar ra sthan bharapardo rupama thamyaun gahro** hunchha. sano banaunda sukshma biwaran ra baraparasangako chamakako
farak (contrast) pani haraunchha.

arkotir **sano banaundaima sadhain 0 hundaina**. banki sankhya tasbir, bastu ra threshold ma nirbhar chha. talako
cellle tasbir janajan sano banaera anuman chalaunchha ra pahichan sankhya kasari badlinchha herchha.

**fileko rupama sbikar hunu** ra **model le sanchchai prashodhan garne rijolyusan** farak kura hun. thulo tasbir
truti nagari din sakinchha, tar `imgsz` anusar bhitrai sano banainchha, tyasaile sukshma biwaran haraunchha.

<!-- ne-cell: 1937768a | after-heading -->
**sankhya kina ghatchha**
<!-- ne-pair: Why the count drops -->

<!-- ne-cell: 1937768a -->
sano banaunda manisako chaudai darjanaun pikselabat kehi pikselama jharchha. model le "manisako akar" chinna
gahro hunchha. 0 hunchha ki hundaina bhanne kura tasbir ra threshold ma nirbhar chha.

PVC ko 0.3 mm dosh ma **ajh kathin** hunchha. dekhine kshetrako tulna ma dosh kehi pikselama matra banki bhae
chamakako farak dekhie pani akar ra sthan sthir hundaina. tyas abastha ma AI ko kshamata hoina,
**khichaiko rijolyusan (dekhine kshetra ra pixel pitch)** badhaune wa tasbir tukra-tukra garera khichne kura sochnuparchha.

<!-- ne-cell: clarity-image-box-transfer | after-heading -->
### tasbir ra ayatako ekai namisaune

<!-- ne-cell: clarity-image-box-transfer -->
dui sansleshit tasbir ma anuman garnuhos. A ma dosh 3 bata chhan ra sahi milne anuman 2 bata. B samanya chha,
anuman 0 bata. tasbir-ekaima A=TP ra B=TN; ayat-ekaima A ma TP=2 ra FN=1 chha. samanya B ma ayat-ekaiko
TN banaindain. yo kura din 4 ko mulyankan notebookko "ganne ekai" sang jodinchha.

sano prayog: A ma anuman ek bhae tasbir-starko recall ra bastu-starko recall madhye kun badlinchha?

<!-- ne-cell: 1e45eae2 | after-heading -->
## abhyas

<!-- ne-cell: 23ef30f5 | after-heading -->
**abhyas 1 (adharabhut): thresholdko talika banaune**
<!-- ne-pair: Exercise 1 (basic): build the threshold table -->

<!-- ne-cell: 23ef30f5 -->
Part 1 ko talika `zidane.jpg` ma pani feri banaunuhos. threshold 0.05–0.90 ma pahichan sankhyako paribartan
abhilekh garnuhos.

pura bhaeko maapan: 7 lineko talika banyo, threshold badhaunda pahichan sankhya nabadhne kura pushti bhayo, ra
sankhya 0 bhaeko threshold abhilekh gariyo. **kunai threshold ma 0 bhaen bhane tyahi kura abhilekh gare pani pura maninchha.**

<!-- ne-cell: 48325aa1 | after-heading -->
**abhyas 2 (madhyam): euta anishchit pahichan punarabalokan garne**
<!-- ne-pair: Exercise 2 (intermediate): review one uncertain detection -->

<!-- ne-cell: 48325aa1 -->
mathiko "kam confidence ko soochi" baat euta chhaner abhilekh garnuhos.

| bishay | lekhne |
|---|---|
| class | |
| confidence | |
| akar (chaudai×uchai) | |
| tasbir sang tulna garda nirnaya (sahi / galat / nirnaya garna sakindaina) | |
| kam hunuko karanabare anuman (anuman ho bhanera spasht lekhnuhos) | |

pura bhaeko maapan: panchai mahal bhariyo, "tasbir sang tulna garda nirnaya" tasbir wa sahi label ma adharit chha, ra
kam hunuko karan **anuman** ko rupama lekhieko chha.

<!-- ne-cell: 2aedccfa | after-heading -->
**abhyas 3 (baikalpik): PVC nirikshanka lagi chahine rijolyusan sujhaune**
<!-- ne-pair: Exercise 3 (optional challenge): propose the resolution needed for PVC -->

<!-- ne-cell: 2aedccfa -->
chaudai 1,300 mm bhaeko sitama 0.3 mm ko dosh **kamtima 3 piksel** ma samatnu chha bhanaun.

1. tirso disha ma chahine piksel sankhya ganana garnuhos.
2. tyo tasbir YOLO ma tyasai din sakinchha? fileko rupama sbikar hunu ra model le sanchchai prashodhan garne
   rijolyusan farak hun. ke upay garnuhunchha?
3. Part 5 ko natija lai adhar maner "tasbir sano banaera anuman chalaune" tarikako samasya byakhya garnuhos.

pura bhaeko maapan: chahine piksel sankhya (13,000 piksel) ganana garieko chha, `imgsz` badhaune ra obharalyapasahit
tailama bandne dubai kura ullekh chhan, ra sano banaunda parne asar byakhya garieko chha.

<!-- ne-cell: cc0a4b24 | after-heading -->
#### bujhai jaanchne prashna

<!-- ne-cell: cc0a4b24 -->
1. abhilekhit `bus.jpg` ko chalaima threshold 0.90 banaunda sahi pahichan pani kina harayo?
2. jhuto pojitibh ra jhuto negetibh karyasthalako bhashama byakhya garnuhos.
3. "confidence badhi chha, tyasaile sahi chha" bhanna kina mildaina?
4. tasbir sano banaunda pahichan ghatne dui karan bhannuhos.
5. PVC nirikshan ma "chhutne" ra "jhuto alarm" madhye kun pahile ghataunuparchha? tapainko bichar ra karan lekhnuhos.

<!-- ne-cell: 36d302d7 | after-heading -->
## samasya parema

<!-- ne-cell: 36d302d7 -->
truti aepachhi pahile "kun cell ma", "kun line ma", "ke sandesh ayo" bhanera lekhnuhos. bujhaunuparne kaam ma pani
tyahi abhilekh rakhnuhos.

| lakshan | ke garne |
| --- | --- |
| talika khali hunchha | `conf` dherai uchcha huna sakchha. 0.05 samm ghataera jaanchnuhos. |
| `model` paribhashit chhaina | Part 0 ko model padhne cell chalaunuhos. |
| sano banaeko tasbir ma truti | `int()` le purnank banainchha, tar atyadhik sano bhae 0 hunchha. `scale` 0.10 bhanda kam narakhnuhos. |
| CSV Excel ma bigranchha | `encoding="utf-8-sig"` lagaera surakshit garnuhos. |
| harek patak daunalod suru hunchha | `assets/models/` ma file chha ki jaanchnuhos. chhaina bhane hataile rakhnuhos. |

<!-- ne-cell: e3887914 | after-heading -->
## sampannata janchasuchi

<!-- ne-cell: e3887914 -->
**aniwarya** bhaneko talako "aniwarya" soochi matra ho. **abhyas 3 ra thap chunauti baikalpik** hun; nagare pani pura
maninchha. samay banki bhae ma matra garnuhos.

**aniwarya**

- [ ] Part 1–Part 5 padher sabai code cell chalaen
- [ ] threshold anusar pahichan sankhyako talika banaen
- [ ] nirdeshangk baat chaudai, uchai ra anupaat nikalen
- [ ] rijolyusan ghataunda pahichan sankhya ma parne asar heren
- [ ] abhyas 1 ra 2 (aniwarya) garen
- [ ] kamtima euta anishchit pahichan punarabalokan gari nirnaya ra anuman abhilekh garen
- [ ] bujhai jaanchne 5 prashnako uttar dien
- [ ] notebook surakshit garen

**baikalpik**

- [ ] abhyas 3 (baikalpik): chahine rijolyusan ganana garera `imgsz` ra tailing sochen
- [ ] thap chunauti: NMS ko `iou` threshold badaler dohoro pahichan janchen

<!-- ne-cell: 987dc9d2 | after-heading -->
## thap adhyayan (baikalpik)

<!-- ne-cell: 987dc9d2 -->
### sandarbha lingk

- [Ultralytics Predict mod](https://docs.ultralytics.com/modes/predict/)
- [Ultralytics mulyankan (val) mod](https://docs.ultralytics.com/modes/val/)
- [COCO mulyankan maapanko sochai](https://cocodataset.org/#detection-eval)

### thap chunauti (aniwarya hoina)

`iou` threshold (`model.predict(..., iou=...)`) badalda dohoro pahichan kasari badlinchha khojnuhos.
