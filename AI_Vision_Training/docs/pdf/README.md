# 解説 PDF / Explanation companions

このフォルダの PDF は、**ノートブックの Markdown から自動で組んだ**冊子です。
別々に書いた原稿ではないので、ノートブックを直せば PDF も同じ手順で作り直せます。
The PDFs here are typeset **from the notebooks' own Markdown**. They are not a second manuscript,
so correcting a notebook and re-running the command below keeps the two in step.

2 種類あります。`*_ja_en.pdf` は 2026-11-15 に作った日本語＋英語版、`*_ja_en_ne.pdf` は
ネパール語を加えた三言語版です。**前者は書き換えていません。** 両方そのまま読めます。
There are two generations: the Japanese + English booklets from 2026-11-15, and the
tri-language booklets that add Nepali. The earlier files are left **untouched**, so both are
readable.

<!-- ne:begin doc:35ca32f23d -->
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
<!-- ne:end -->

## ファイル / Files

日本語＋英語 / Japanese and English:

| ファイル / File | 内容 / Contents | ページ / Pages |
|---|---|---|
| `Day01_explanation_ja_en.pdf` | 第 1 日（ノートブック 01〜03） | 72 |
| `Day02_explanation_ja_en.pdf` | 第 2 日（ノートブック 01〜03） | 88 |
| `Day03_explanation_ja_en.pdf` | 第 3 日（ノートブック 01〜03） | 56 |
| `Day04_explanation_ja_en.pdf` | 第 4 日（ノートブック 01〜03） | 70 |
| `Day05_explanation_ja_en.pdf` | 第 5 日（ノートブック 01〜03） | 65 |
| `Week1_explanation_ja_en.pdf` | 5 日分をまとめたもの / all five days | 340 |

日本語＋英語版のうち、2026-11-19 に作り直したのは `Day02`・`Day04`・`Day05`・`Week1` です
（Day 2 の図、Day 4・Day 5 の手順の説明が変わったため）。`Day01`・`Day03` は 2026-11-16 の版を
そのまま残しています。
Of the Japanese + English booklets, `Day02`, `Day04`, `Day05` and `Week1` were rebuilt on 2026-11-19
(the Day 2 figure and the Day 4/5 workflow text changed); `Day01` and `Day03` still ship the
2026-11-16 files unchanged.

日本語＋英語＋ネパール語 / Japanese, English and Nepali:

> 第 3 の言語は **ローマ字表記のネパール語**（Nepali written with Latin letters, BCP 47 `ne-Latn`）です。
> デーヴァナーガリー文字ではありません。16 冊のノートブックと 12 の学習者向け文書はすべてローマ字
> 表記に移行済みなので、どの冊子にもデーヴァナーガリーは入りません。詳しくは
> [`assets/i18n/ne/romanization_style_guide.md`](../../assets/i18n/ne/romanization_style_guide.md)。
> The third language is **Nepali written with Latin letters** (`ne-Latn`), not Devanagari.
> All 16 notebooks and 12 learner documents have been migrated, so no booklet mixes scripts.

| ファイル / File | 内容 / Contents | ページ / Pages |
|---|---|---|
| `Day01_explanation_ja_en_ne.pdf` | 第 1 日（ノートブック 01〜03） | 98 |
| `Day02_explanation_ja_en_ne.pdf` | 第 2 日（ノートブック 01〜03） | 115 |
| `Day03_explanation_ja_en_ne.pdf` | 第 3 日（ノートブック 01〜03） | 77 |
| `Day04_explanation_ja_en_ne.pdf` | 第 4 日（ノートブック 01〜03） | 90 |
| `Day05_explanation_ja_en_ne.pdf` | 第 5 日（ノートブック 01〜03） | 92 |
| `Week1_explanation_ja_en_ne.pdf` | 5 日分をまとめたもの / all five days | 460 |
| `Setup_ja_en_ne.pdf` | 準備ノートブック `00_Environment_Setup.ipynb` | 41 |
| `Installation_Guide_ja_en_ne.pdf` | `START_HERE.md` と `docs/troubleshooting/installation.md` | 23 |
| `Repository_Guide_ja_en_ne.pdf` | `README.md` と `requirements/tested_versions.md` | 23 |
| `Course_Syllabus_ja_en_ne.pdf` | `COURSE_SYLLABUS.md` | 21 |

ページ数は生成のたびにスクリプトが表示します。下の表は 2026-11-19（ローマ字ネパール語への移行と
Day 2・Day 5 の修正の後）の生成結果です。
The page counts are printed by the exporter on every run. Both tables are from the 2026-11-19 rebuild,
after the migration to Romanized Nepali and the Day 2 / Day 5 corrections. That rebuild is recorded in
[Final_Romanized_Nepali_Day02_Day05_Implementation_Log.md](../reviews/Final_Romanized_Nepali_Day02_Day05_Implementation_Log.md).

準備ノートブックは日本語＋英語版の 6 冊に含みません。三言語版では `Setup_ja_en_ne.pdf` として
独立した 1 冊にしています。
Setup is not part of the six Japanese + English books; the tri-language generation ships it as its
own booklet, `Setup_ja_en_ne.pdf`.

<!-- ne:begin doc:724f15e073 -->
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

> tesro bhasha **roman lipima lekheko Nepali** (`ne-Latn`) ho, Devanagari hoina. sabai 16 wata
> notebook ra 12 wata shiksharthi file roman lipima chhan, tyasaile kunai pustikama Devanagari
> bhetindaina. thap jankari: `assets/i18n/ne/romanization_style_guide.md`.
<!-- ne:end -->

## 作り直す方法 / Regenerating

インストール（学習用の環境とは分けています / separate from the learner requirements）:

コマンド プロンプトで教材ルートから実行します。環境の準備は [START_HERE](../../START_HERE.md)。
Run in Command Prompt from the course root; prepare the environment via [START_HERE](../../START_HERE.md).

```cmd
python -m pip install -r requirements\pdf.txt
python -m playwright install chromium
```

生成（**日本語＋英語 / Japanese + English**）:

```cmd
python assets\scripts\export_explanations_pdf.py
```

生成（**三言語 / tri-language** — 1 コマンドで 10 冊 / one command, ten booklets）:

```cmd
python assets\scripts\export_trilingual_pdf.py
```

1 冊だけ / a single booklet:

```cmd
python assets\scripts\export_trilingual_pdf.py --only Day03
```

点検（全ページを画像にして、空白・はみ出し・ネパール語の検索可否を確認 / render every page and check blank pages, overflow and that Nepali stays searchable）:

```cmd
python assets\scripts\inspect_pdf_pages.py --languages ja,ne
```

* モデルのダウンロードはしません。学習も再実行しません。ノートブックは**実行しません**。
  No model download, no retraining, and the notebooks are **not executed**: the exporter only
  reads Markdown, figures and short code cells.
* 日本語フォントは OS のもの（Windows なら Noto Sans JP / Yu Gothic / Meiryo）を PDF に埋め込みます。
  A Japanese font installed on the machine is embedded in the PDF.
* ネパール語（ローマ字表記）も Chromium の PDF 出力で組んでいます。日本語・英語・ネパール語を
  1 つの組版で扱い、本文が**選択・検索できる**状態を保つためです。
  The Nepali (Romanized) text is typeset through Chromium's PDF engine as well, so the three languages
  share one typesetter and the text layer stays **selectable and searchable**. (The exporter was
  introduced when the third language was Devanagari, which ReportLab could only write as private-use
  code points; Chromium keeps both shapes and text correct, and it still does so for `ne-Latn`.)
* 図の出典は各 PDF の最終ページ「出典と参照 / Sources and references」にあります。
  Figure provenance is on the last page of every PDF.

<!-- ne:begin doc:459440aadc -->
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
<!-- ne:end -->

## 何が入り、何が入らないか / What is in, and what is out

入る / included

* 学習目標・前提・説明（日本語 → 英語 → ネパール語の順。三言語版のみネパール語）
* 実行前から見える静的図、キャプション、「気づいてほしいこと」、学習者への問い
* 学習者が書き換える短いコード例（20 行まで）
* 演習・ヒント・理解度チェック
* 参考出力（この研修で実際に保存した結果から作った図）。模式図・合成データとの区別を図の中に書いています。

入らない / excluded

* セルの実行出力、スタックトレース、長い準備コード、生の JSON
* 講師用の解答（`docs/instructor/` に別途あります / kept separately）
* 対話ウィジェットそのもの。代わりに静的図と「ノートブックで操作する」注記を置いています。
* 実行していない学習・検証の結果。数字は保存された記録がある場合にだけ載せています。

<!-- ne:begin doc:f63342958e -->
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
<!-- ne:end -->

## 既知の限界 / Known limitations

* 横長の図は読みやすさのため **A4 横向きのページ**に置いています。前後のページに余白が出ます。
  Wide figures sit on landscape A4 pages so their labels stay readable; that leaves white space
  on the facing pages.
* PDF 内のリンクは文字列としてのパスです（クリックでは開きません）。
  Paths inside the PDF are plain text, not clickable links.
* 図の中の文字は図の画像に含まれています。本文のように検索・選択はできません。
  Text inside figures is part of the image and cannot be searched.
* 三言語版のネパール語は **1.5 pt の倍数の大きさ**（9 / 10.5 / 12 / 13.5 pt）で組んでいます。
  Chromium の PDF 出力は他の大きさだとデーヴァナーガリーの単語の途中に空白を書き込み、PDF 内検索が
  できなくなります。`inspect_pdf_pages.py --languages ja,ne` がこの崩れを検出します。
  The Nepali type in the tri-language booklets is set at **multiples of 1.5 pt** (9 / 10.5 / 12 /
  13.5 pt). At other sizes Chromium's PDF writer inserts a space inside Devanagari words, which
  breaks in-PDF search; `inspect_pdf_pages.py --languages ja,ne` detects that regression.

<!-- ne:begin doc:aa0695c08e -->
### Nepali ma

* pharakilo chitra padhna sajilo hos bhanera **A4 terso pana** ma rakhieko chha; aghillo-pachhillo panama khali
  thaun dekhinchha.
* PDF bhitraka lingk plain text hun (klik garda khuldain).
* chitrabhitrako akshar chitrakai bhaag ho, tyasaile khojn wa chhanna mildaina.
* Nepali akshar khojn milnaka lagi Nepali majjan 1.5 pt ko gunanama rakhieko chha (9, 10.5, 12, 13.5 pt).
  Chromium le any akarama shabdako bichama khali thaun haler lekhchha, jasale khoj bigarchha.
<!-- ne:end -->

## タマン語（taj）版 / The Tamang (taj) booklets

第 3 の言語をタマン語に置き換える準備として、書き出しスクリプトに `--locale taj` を追加しました。
出力名は `*_ja_en_taj.pdf`、PDF のテキスト層の言語タグは `taj-Deva` です。日本語と英語の冊子、
および既存の `*_ja_en.pdf` はこの変更の影響を受けません。

**現時点では、タマン語の冊子は 1 冊も作られません。** これは意図した動作です。タマン語の翻訳は
すべて `assets/i18n/taj/` で `pending`（未翻訳）として記録されており、
`check_localization_coverage.py --locale taj --strict` の本番ゲートが通るまで、書き出しスクリプトは
終了コード 2 で停止します。機械翻訳やネパール語の流用でゲートを開くことはできません。

The exporter now accepts `--locale taj`: the booklets would be named `*_ja_en_taj.pdf` and the PDF
text layer would declare `taj-Deva`. The Japanese/English booklets and the existing `*_ja_en.pdf`
files are unaffected.

**No Tamang booklet is produced today, by design.** Every Tamang block is recorded as `pending` in
`assets/i18n/taj/`, and `export_trilingual_pdf.py --locale taj` exits with status 2 until
`check_localization_coverage.py --locale taj --strict` passes. Neither machine output nor copied
Nepali can open that gate.

### 有効にする条件 / What has to happen first

1. 受講者と話し合って**変種と文字**を確定する（暫定: 東部タマン語・デーヴァナーガリー `taj-Deva`）。
2. タマン語の話者が各ブロックを翻訳し、`<!-- taj-status: <cell id> approved -->` で承認する。
3. `python assets\scripts\apply_translations.py --locale taj --write` と
   `python assets\scripts\apply_docs.py --locale taj --write` で差し込む。
4. `python assets\scripts\check_localization_coverage.py --locale taj --strict` が通る。
5. `python assets\scripts\export_trilingual_pdf.py --locale taj` で冊子を作り、
   `python assets\scripts\inspect_pdf_pages.py --languages ja,en,taj` で崩れを点検する。

1. Agree the variety and script with the trainees (provisional: Eastern Tamang, Devanagari,
   `taj-Deva`). 2. A Tamang speaker translates each block and approves it with
   `<!-- taj-status: <cell id> approved -->`. 3. Insert with the two `--locale taj --write` commands.
   4. Pass the strict coverage gate. 5. Build and inspect with the commands above.

既存の `*_ja_en_ne.pdf` は**ロールバック用の旧版**として残します。タマン語版が承認されるまで、
学習者に配る第 3 の言語はどちらも「未承認」です。
The existing `*_ja_en_ne.pdf` files stay as **legacy rollback material**; until a Tamang booklet is
approved, neither third language is classroom-ready.
