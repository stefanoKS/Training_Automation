<!--
Nepali anuwad / Nepali translation source for
docs/pdf/README.md
-->
# docs/pdf/README — Nepali anuwad

<!-- ne-doc: docs/pdf/README.md -->

<!-- ne-section: Explanation companions -->
### Nepali ma

yo folderka PDF **notabukakai Markdown baat sbatah banaieka** pustika hun.
chhuttai lekhieko pandulipi hoina, tyasaile notebook sudharer talako adesh feri chalaunda dubai milchha.

dui kisimaka pustika chhan.

| kisim | bhasha | banaune skript |
|---|---|---|
| `*_ja_en.pdf` | Japani → Angreji | `assets\scripts\export_explanations_pdf.py` |
| `*_ja_en_ne.pdf` | Japani → Angreji → Nepali | `assets\scripts\export_trilingual_pdf.py` |

aghilla `*_ja_en.pdf` file **jastako tastai** rakhieka chhan; nayan tribhashi sanskaranale tinalai
pratisthapan gardaina.

<!-- ne-section: ## ファイル / Files -->
### Nepali ma

| file | samagri |
|---|---|
| `Day01_explanation_ja_en_ne.pdf` … `Day05_explanation_ja_en_ne.pdf` | pratyek dinka 3 notebook (din 5 ma 3) |
| `Week1_explanation_ja_en_ne.pdf` | 5 dinakai samagri eutai pustikama |
| `Setup_ja_en_ne.pdf` | tayari notebook `00_Environment_Setup.ipynb` |
| `Installation_Guide_ja_en_ne.pdf` | `START_HERE.md` ra `docs/troubleshooting/installation.md` |
| `Repository_Guide_ja_en_ne.pdf` | `README.md` ra `requirements/tested_versions.md` |
| `Course_Syllabus_ja_en_ne.pdf` | `COURSE_SYLLABUS.md` |

pana sankhya harek patak banaunda skriptale aphain dekhaunchha.

> tesro bhasha **roman lipima lekheko Nepali** (`ne-Latn`) ho, Devanagari hoina. din 1-3 ka notebook
> ahile pani Devanagari ma chhan, tyasaile ti pustikama dui lipi bhetinchha. thap jankari:
> `assets/i18n/ne/romanization_style_guide.md`.

<!-- ne-section: ## 作り直す方法 / Regenerating -->
### Nepali ma

installation (sikai ko batabaranabhanda chhuttai):

```cmd
python -m pip install -r requirements\pdf.txt
python -m playwright install chromium
```

`playwright install chromium` le PDF chhapne Chromium khojchha. yo **PDF banaune ra jaanchne manisaka lagi
matra** ho; prashiksharthile yo chahindain.

Japani–Angreji pustika:

```cmd
python assets\scripts\export_explanations_pdf.py
```

tribhashi pustika (**yo ek adeshale sabai**) :

```cmd
python assets\scripts\export_trilingual_pdf.py
```

euta matra banaun:

```cmd
python assets\scripts\export_trilingual_pdf.py --only Day03
```

jaanch (harek pana chitra banaer, Nepali khojine abastha ma chha ki chhaina pani janchdai):

```cmd
python assets\scripts\inspect_pdf_pages.py --languages ja,ne
```

* model download, sikai ra notebook **chalaindain**. exporter le Markdown, chitra ra chhota kod cell matra
  padhchha.
* Japani phant OS ko (Windows ma Noto Sans JP / Yu Gothic / Meiryo), Nepali phant Nirmala UI
  PDF ma embed hunchha.
* chitrako srot pratyek PDF ko antim pana "srot ra sandarbha" ma chha.

<!-- ne-section: ## 何が入り、何が入らないか / What is in, and what is out -->
### Nepali ma

parchha:

* sikai lakshya, poorwashart ra byakhya (Japani → Angreji → Nepali)
* chalaunuaghi nai dekhine sthir chitra, captions, "dhyan dinuparne kura", prashnaharu
* prashiksharthile badalne chhota kod udaharan (20 line samma)
* abhyas, sanket, bujhai jaanch
* sandarbha natija (yo talim ma surakshit bhaeka natija baat baneka chitra). yojanabaddha ra kritrim datako farak
  chitrabhitrai lekhieko chha.

pardaina:

* cellko output, stack trace, lamo tayari kod, kancho JSON
* prashikshakaka jabaph (`docs/instructor/` ma chhuttai)
* slider aphain; tyasko satta sthir chitra ra "notebook ma chalaunuhos" bhanne tippani
* nachalaieko sikai wa jaanchko natija

<!-- ne-section: ## 既知の限界 / Known limitations -->
### Nepali ma

* pharakilo chitra padhna sajilo hos bhanera **A4 terso pana** ma rakhieko chha; aghillo-pachhillo panama khali
  thaun dekhinchha.
* PDF bhitraka lingk plain text hun (klik garda khuldain).
* chitrabhitrako akshar chitrakai bhaag ho, tyasaile khojn wa chhanna mildaina.
* Nepali akshar khojn milnaka lagi Nepali majjan 1.5 pt ko gunanama rakhieko chha (9, 10.5, 12, 13.5 pt).
  Chromium le any akarama shabdako bichama khali thaun haler lekhchha, jasale khoj bigarchha.
