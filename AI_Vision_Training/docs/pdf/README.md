# 解説 PDF / Explanation companions

このフォルダの PDF は、**ノートブックの Markdown から自動で組んだ**冊子です。
別々に書いた原稿ではないので、ノートブックを直せば PDF も同じ手順で作り直せます。
The PDFs here are typeset **from the notebooks' own Markdown**. They are not a second manuscript,
so correcting a notebook and re-running the command below keeps the two in step.

## ファイル / Files

| ファイル / File | 内容 / Contents | ページ / Pages |
|---|---|---|
| `Day01_explanation_ja_en.pdf` | 第 1 日（ノートブック 01〜03） | 61 |
| `Day02_explanation_ja_en.pdf` | 第 2 日（ノートブック 01〜03） | 65 |
| `Day03_explanation_ja_en.pdf` | 第 3 日（ノートブック 01〜03） | 45 |
| `Day04_explanation_ja_en.pdf` | 第 4 日（ノートブック 01〜03） | 47 |
| `Day05_explanation_ja_en.pdf` | 第 5 日（ノートブック 01〜03） | 52 |
| `Week1_explanation_ja_en.pdf` | 5 日分をまとめたもの / all five days | 260 |

ページ数は生成のたびに `export_explanations_pdf.py` が表示します。上の表は 2026-11-13 の生成結果です。
The page counts are printed by the export script; the numbers above are from the 2026-11-13 build.

## 作り直す方法 / Regenerating

インストール（学習用の環境とは分けています / separate from the learner requirements）:

```powershell
python -m pip install -r requirements\pdf.txt
```

生成（**この 1 コマンドだけ** / this exact command is all that is needed）:

```powershell
python assets\scripts\export_explanations_pdf.py
```

点検（全ページを画像にして、空白・はみ出しを確認 / render every page and check it）:

```powershell
python assets\scripts\inspect_pdf_pages.py
```

* モデルのダウンロードはしません。学習も再実行しません。ノートブックは**実行しません**。
  No model download, no retraining, and the notebooks are **not executed**: the exporter only
  reads Markdown, figures and short code cells.
* 日本語フォントは OS のもの（Windows なら Noto Sans JP / Yu Gothic / Meiryo）を PDF に埋め込みます。
  A Japanese font installed on the machine is embedded in the PDF.
* 図の出典は各 PDF の最終ページ「出典と参照 / Sources and references」にあります。
  Figure provenance is on the last page of every PDF.

## 何が入り、何が入らないか / What is in, and what is out

入る / included

* 学習目標・前提・説明（日本語 → 英語の順）
* 実行前から見える静的図、キャプション、「気づいてほしいこと」、学習者への問い
* 学習者が書き換える短いコード例（20 行まで）
* 演習・ヒント・理解度チェック
* 参考出力（この研修で実際に保存した結果から作った図）。模式図・合成データとの区別を図の中に書いています。

入らない / excluded

* セルの実行出力、スタックトレース、長い準備コード、生の JSON
* 講師用の解答（`docs/instructor/` に別途あります / kept separately）
* 対話ウィジェットそのもの。代わりに静的図と「ノートブックで操作する」注記を置いています。
* 実行していない学習・検証の結果。数字は保存された記録がある場合にだけ載せています。

## 既知の限界 / Known limitations

* 横長の図は読みやすさのため **A4 横向きのページ**に置いています。前後のページに余白が出ます。
  Wide figures sit on landscape A4 pages so their labels stay readable; that leaves white space
  on the facing pages.
* PDF 内のリンクは文字列としてのパスです（クリックでは開きません）。
  Paths inside the PDF are plain text, not clickable links.
* 図の中の文字は図の画像に含まれています。本文のように検索・選択はできません。
  Text inside figures is part of the image and cannot be searched.
