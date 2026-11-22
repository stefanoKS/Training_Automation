# 第7〜9日 出典とライセンス / Day 7–9 Sources and Licenses

最終確認日 / Last checked: **2026-11-22**（この日付でURLと概要を確認 / URLs and summaries checked on this date）

本教材の説明・図・シミュレータは**オリジナルの教育用著作物**です。以下の資料は、技術的な記述を確認するために参照した出典です。規格の本文・図表を転載していません。
The explanations, diagrams and simulations in this course are **original educational work**. The sources below were consulted to verify technical statements. No standard text or figures are reproduced.

## 1. 参照した出典 / Consulted sources

| 分類 / class | 出典 / source | URL | 使い方 / how it is used |
|---|---|---|---|
| PLC言語 / PLC languages | IEC 61131-3:2025 | https://webstore.iec.ch/en/publication/68533 | ラダーがIECで定義される言語の一つであることの確認 / confirms LD is one language defined in IEC |
| PLC / PLC | Mitsubishi Electric FA | https://www.mitsubishielectric.com/fa/ | デバイス表記とマニュアル確認の必要性 / device naming and manual verification |
| 機械安全 / machinery safety | ISO 12100:2010 | https://www.iso.org/standard/51528.html | リスクアセスメントの位置づけ / role of risk assessment |
| 機械安全 / machinery safety | ISO 13849-1:2023 | https://www.iso.org/standard/73481.html | 安全関連の設計概念 / safety-related design concepts |
| 機械安全 / machinery safety | ISO 13850:2015 | https://www.iso.org/standard/59970.html | 非常停止の扱い / emergency-stop treatment |
| 電気安全 / electrical | IEC 60204-1:2016+A1:2021 | https://webstore.iec.ch/en/publication/71256 | 機械の電気設備の一般的枠組み / general electrical equipment framework |
| マシンビジョン / vision | EMVA GenICam | https://www.emva.org/standards-technology/genicam/ | GenICamが共通のソフト枠組みであること / GenICam as a generic software framework |
| マシンビジョン / vision | Basler documentation | https://docs.baslerweb.com/ | トリガ・露光・ラインスキャンの一般説明 / general trigger, exposure and line-scan explanations |
| 通信 / communications | OPC Foundation reference | https://reference.opcfoundation.org/ | OPC UAの一般的説明 / general OPC UA description |
| 通信 / communications | Modbus specifications | https://www.modbus.org/modbus-specifications | Modbus TCPの一般的説明 / general Modbus TCP description |
| AI / AI | Ultralytics YOLO detect docs | https://docs.ultralytics.com/tasks/detect/ | 物体検出の出力（クラス・枠・信頼度） / detection outputs |
| AI / AI | Anomalib PatchCore (lib-v2.7.0) | https://anomalib.readthedocs.io/en/lib-v2.7.0/markdown/guides/reference/models/image/patchcore.html | PatchCoreの異常スコアとメモリバンク / anomaly score and memory bank |

**版・適用範囲は変わります。 / Editions and applicability change.** 本教材は特定の版の要件を断定しません。実務では最新の公式資料と有資格のレビューを確認してください。
This course does not assert the requirements of any specific edition. In practice, confirm current official documents and obtain competent review.

## 2. 図 / Diagrams

- 36点のSVG（`assets/diagrams/day07|day08|day09/`）はすべて本教材のために新規作成しました。 / All 36 SVGs were created for this course.
- 生成スクリプト: `day07_09_support/scripts/generate_day07_09_diagrams.py`（`svgkit.py` を使用）。 / Generator scripts are listed.
- SVGは編集可能で、`<title>` と `<desc>`、日英ラベルを持ちます。 / SVGs are editable with title, desc and bilingual labels.
- 外部画像・写真・アイコン素材は使用していません。 / No external images, photographs or icon assets are used.

## 3. シミュレータ / Simulations

- `simulations/*.html` は本教材のために新規作成したオフライン教材です。 / The six HTML simulators were written for this course.
- 外部JavaScriptライブラリ、CDN、ネットワーク通信はありません。 / No external JS libraries, CDNs or network calls.
- 外部フォントは埋め込まず、OSの日本語フォントを参照するCSS指定のみです。 / No external fonts are embedded; CSS references system Japanese fonts.

## 4. PDF / PDFs

- PDFはReportLabで、教材原稿（Markdown）から生成しています。 / PDFs are built with ReportLab from the Markdown manuscripts.
- 日本語表示には、作成環境にインストール済みのフォント（Meiryo等）を**PDF生成時のみ**使用します。フォントファイル自体は再配布しません。 / A locally installed Japanese font is used **only during generation**; the font file is not redistributed.
- SVG図はブラウザ（Chrome/Edge）で描画しPNG化してPDFに埋め込みます。 / SVGs are rendered in a local browser, rasterised and embedded.
- ページ画像（`docs/pdf/_pages/`）は点検用で、リポジトリには含めません（`.gitignore`）。 / Page renders are for inspection and are not committed.

## 5. データ / Data

- 数値例（ローラ径、速度、画素数、遅延など）はすべて**仮定**です。 / All numeric examples are hypothetical.
- 検査結果・ロット・画像IDは架空です。 / Inspection results, lots and image IDs are fictional.
- 実在の工場、装置、ネットワーク、顧客データは含みません。 / No real factory, equipment, network or customer data is included.

## 6. 著作権と利用 / Copyright and use

- 本教材の文章・図・シミュレータは、リポジトリの利用条件に従います。 / Text, diagrams and simulators follow the repository's terms.
- 引用した規格・製品名は各権利者の商標または著作物です。 / Quoted standards and product names belong to their owners.
- 規格の本文、図表、有料文書の転載は行っていません。 / No standard text, figures or paid documents are reproduced.
- 画像の利用権が確認できない写真は使用していません。 / No photographs with unverified rights are used.

## 7. 免責 / Disclaimer

本教材は教育用の概念説明です。実機の設計・製作・設置・運転・保守・安全認証を代替しません。実際の機械安全は、危険源・要求性能・適用規格・選定機器・有資格のレビューに基づいて決定されます。
This is conceptual training material. It does not replace real design, construction, installation, operation, maintenance or safety certification. Real machinery safety depends on hazards, required performance, applicable standards, selected equipment and competent review.
