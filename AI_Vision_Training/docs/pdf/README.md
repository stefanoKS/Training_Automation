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
### नेपालीमा

यो फोल्डरका PDF **नोटबुककै Markdown बाट स्वतः बनाइएका** पुस्तिका हुन्।
छुट्टै लेखिएको पाण्डुलिपि होइन, त्यसैले नोटबुक सुधारेर तलको आदेश फेरि चलाउँदा दुवै मिल्छ।

दुई किसिमका पुस्तिका छन्।

| किसिम | भाषा | बनाउने स्क्रिप्ट |
|---|---|---|
| `*_ja_en.pdf` | जापानी → अङ्ग्रेजी | `assets\scripts\export_explanations_pdf.py` |
| `*_ja_en_ne.pdf` | जापानी → अङ्ग्रेजी → नेपाली | `assets\scripts\export_trilingual_pdf.py` |

अघिल्ला `*_ja_en.pdf` फाइल **जस्ताको तस्तै** राखिएका छन्; नयाँ त्रिभाषी संस्करणले तिनलाई
प्रतिस्थापन गर्दैन।
<!-- ne:end -->

## ファイル / Files

日本語＋英語 / Japanese and English:

| ファイル / File | 内容 / Contents | ページ / Pages |
|---|---|---|
| `Day01_explanation_ja_en.pdf` | 第 1 日（ノートブック 01〜03） | 72 |
| `Day02_explanation_ja_en.pdf` | 第 2 日（ノートブック 01〜03） | 86 |
| `Day03_explanation_ja_en.pdf` | 第 3 日（ノートブック 01〜03） | 56 |
| `Day04_explanation_ja_en.pdf` | 第 4 日（ノートブック 01〜03） | 68 |
| `Day05_explanation_ja_en.pdf` | 第 5 日（ノートブック 01〜03） | 63 |
| `Week1_explanation_ja_en.pdf` | 5 日分をまとめたもの / all five days | 334 |

日本語＋英語＋ネパール語 / Japanese, English and Nepali:

| ファイル / File | 内容 / Contents | ページ / Pages |
|---|---|---|
| `Day01_explanation_ja_en_ne.pdf` | 第 1 日（ノートブック 01〜03） | 101 |
| `Day02_explanation_ja_en_ne.pdf` | 第 2 日（ノートブック 01〜03） | 116 |
| `Day03_explanation_ja_en_ne.pdf` | 第 3 日（ノートブック 01〜03） | 79 |
| `Day04_explanation_ja_en_ne.pdf` | 第 4 日（ノートブック 01〜03） | 88 |
| `Day05_explanation_ja_en_ne.pdf` | 第 5 日（ノートブック 01〜03） | 88 |
| `Week1_explanation_ja_en_ne.pdf` | 5 日分をまとめたもの / all five days | 460 |
| `Setup_ja_en_ne.pdf` | 準備ノートブック `00_Environment_Setup.ipynb` | 41 |
| `Installation_Guide_ja_en_ne.pdf` | `START_HERE.md` と `docs/troubleshooting/installation.md` | 23 |
| `Repository_Guide_ja_en_ne.pdf` | `README.md` と `requirements/tested_versions.md` | 23 |
| `Course_Syllabus_ja_en_ne.pdf` | `COURSE_SYLLABUS.md` | 17 |

ページ数は生成のたびにスクリプトが表示します。日本語＋英語版の表は 2026-11-15 の生成結果、
三言語版は 2026-11-16 の生成結果です。
全679ページの描画検査と図の点検範囲は [今回の検証記録](../reviews/2026-11-15_cmd_migration.md) にあります。
The page counts are printed by the exporter on every run. The Japanese + English table is from the
2026-11-15 rebuild; the tri-language table from 2026-11-16. All 679 pages of the first generation were
rendered; see the [verification record](../reviews/2026-11-15_cmd_migration.md) for that scope. The
tri-language generation is recorded in
[Nepali_Localization_And_PDF_Implementation_2026-11-16.md](../reviews/Nepali_Localization_And_PDF_Implementation_2026-11-16.md).

準備ノートブックは日本語＋英語版の 6 冊に含みません。三言語版では `Setup_ja_en_ne.pdf` として
独立した 1 冊にしています。
Setup is not part of the six Japanese + English books; the tri-language generation ships it as its
own booklet, `Setup_ja_en_ne.pdf`.

<!-- ne:begin doc:724f15e073 -->
### नेपालीमा

| फाइल | सामग्री |
|---|---|
| `Day01_explanation_ja_en_ne.pdf` … `Day05_explanation_ja_en_ne.pdf` | प्रत्येक दिनका ३ नोटबुक (दिन ५ मा ३) |
| `Week1_explanation_ja_en_ne.pdf` | ५ दिनकै सामग्री एउटै पुस्तिकामा |
| `Setup_ja_en_ne.pdf` | तयारी नोटबुक `00_Environment_Setup.ipynb` |
| `Installation_Guide_ja_en_ne.pdf` | `START_HERE.md` र `docs/troubleshooting/installation.md` |
| `Repository_Guide_ja_en_ne.pdf` | `README.md` र `requirements/tested_versions.md` |
| `Course_Syllabus_ja_en_ne.pdf` | `COURSE_SYLLABUS.md` |

पाना सङ्ख्या हरेक पटक बनाउँदा स्क्रिप्टले आफैं देखाउँछ।
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
* ネパール語は Chromium の PDF 出力で組んでいます。ReportLab では文字の見た目は作れても本文が
  私用領域の符号になり、**検索できません**。Chromium は字形も本文も正しく保ちます。
  The Devanagari text is typeset through Chromium's PDF engine: ReportLab shapes it visually but
  writes private-use code points, so the text cannot be searched. Chromium keeps both the shapes and
  the text layer correct.
* 図の出典は各 PDF の最終ページ「出典と参照 / Sources and references」にあります。
  Figure provenance is on the last page of every PDF.

<!-- ne:begin doc:459440aadc -->
### नेपालीमा

installation (सिकाइको वातावरणभन्दा छुट्टै):

```cmd
python -m pip install -r requirements\pdf.txt
python -m playwright install chromium
```

`playwright install chromium` ले PDF छाप्ने Chromium खोज्छ। यो **PDF बनाउने र जाँच्ने मानिसका लागि
मात्र** हो; प्रशिक्षार्थीले यो चाहिँदैन।

जापानी–अङ्ग्रेजी पुस्तिका:

```cmd
python assets\scripts\export_explanations_pdf.py
```

त्रिभाषी पुस्तिका (**यो एक आदेशले सबै**) :

```cmd
python assets\scripts\export_trilingual_pdf.py
```

एउटा मात्र बनाउन:

```cmd
python assets\scripts\export_trilingual_pdf.py --only Day03
```

जाँच (हरेक पाना चित्र बनाएर, नेपाली खोजिने अवस्थामा छ कि छैन पनि जाँच्दै):

```cmd
python assets\scripts\inspect_pdf_pages.py --languages ja,ne
```

* model download, सिकाइ र नोटबुक **चलाइँदैन**। exporter ले Markdown, चित्र र छोटा कोड सेल मात्र
  पढ्छ।
* जापानी फन्ट OS को (Windows मा Noto Sans JP / Yu Gothic / Meiryo), नेपाली फन्ट Nirmala UI
  PDF मा embed हुन्छ।
* चित्रको स्रोत प्रत्येक PDF को अन्तिम पाना "स्रोत र सन्दर्भ" मा छ।
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
### नेपालीमा

पर्छ:

* सिकाइ लक्ष्य, पूर्वशर्त र व्याख्या (जापानी → अङ्ग्रेजी → नेपाली)
* चलाउनुअघि नै देखिने स्थिर चित्र, captions, "ध्यान दिनुपर्ने कुरा", प्रश्नहरू
* प्रशिक्षार्थीले बदल्ने छोटा कोड उदाहरण (20 लाइनसम्म)
* अभ्यास, सङ्केत, बुझाइ जाँच
* सन्दर्भ नतिजा (यो तालिममा सुरक्षित भएका नतिजाबाट बनेका चित्र)। योजनाबद्ध र कृत्रिम डेटाको फरक
  चित्रभित्रै लेखिएको छ।

पर्दैन:

* सेलको output, stack trace, लामो तयारी कोड, काँचो JSON
* प्रशिक्षकका जवाफ (`docs/instructor/` मा छुट्टै)
* slider आफैं; त्यसको सट्टा स्थिर चित्र र "नोटबुकमा चलाउनुहोस्" भन्ने टिप्पणी
* नचलाइएको सिकाइ वा जाँचको नतिजा
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
### नेपालीमा

* फराकिलो चित्र पढ्न सजिलो होस् भनेर **A4 तेर्सो पाना** मा राखिएको छ; अघिल्लो-पछिल्लो पानामा खाली
  ठाउँ देखिन्छ।
* PDF भित्रका लिङ्क plain text हुन् (क्लिक गर्दा खुल्दैन)।
* चित्रभित्रको अक्षर चित्रकै भाग हो, त्यसैले खोज्न वा छान्न मिल्दैन।
* नेपाली अक्षर खोज्न मिल्नका लागि नेपाली मज्जन 1.5 pt को गुणनमा राखिएको छ (9, 10.5, 12, 13.5 pt)।
  Chromium ले अन्य आकारमा शब्दको बीचमा खाली ठाउँ हालेर लेख्छ, जसले खोज बिगार्छ।
<!-- ne:end -->
