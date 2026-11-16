# नेपाली शब्दावली / Nepali terminology glossary (JA → EN → NE)

This file is the authoritative glossary for the Nepali (नेपाली, ISO 639-1 `ne`) localization of
the AI Vision Training course. Every translator and reviewer uses these approved forms so the
notebooks, the documents and the PDFs stay consistent.

## Reading order and placement rules

* 日本語 → English → नेपाली inside one Markdown cell.
* One Nepali block per idea. Do not translate the Japanese wording and the English wording
  separately into two Nepali blocks; translate the *idea* once.
* Never translate: fenced code, inline code, file names, URLs, CLI flags, Windows paths,
  environment variables, kernel names (`aivision`, `aivision-anomalib`), package names.
* Numbers, tolerances and formulas stay exactly as in the source. Use Latin (Arabic) digits
  (`100.0 ± 0.5 mm`, `125 मिनेट`) so learners can compare them with code output.
* Keep these terms in Latin script on first and later use: Python, Jupyter, JupyterLab, OpenCV,
  YOLO, PatchCore, Anomalib, NumPy, PyTorch, kernel, model, pixel, batch, epoch, IoU, AUROC,
  precision, recall, TP/FP/FN/TN, OK/NG, TEST, CALIBRATION, BGR, RGB, HSV, CMD.
* Do not use Hindi-only vocabulary. Where a Hindi word and a Nepali word differ, prefer the
  Nepali form (e.g. `कम्प्युटर` not `कंप्यूटर`, `गर्नुहोस्` not `कीजिए`, `छ`/`हुन्छ` not `है`).

## Core glossary

| 日本語 | English | नेपाली (approved) |
| --- | --- | --- |
| 人工知能 / AI | artificial intelligence | कृत्रिम बुद्धिमत्ता (AI) |
| 機械学習 | machine learning | मेसिन लर्निङ |
| 深層学習 | deep learning | डिप लर्निङ |
| 画素 / ピクセル | pixel | पिक्सेल (चित्रबिन्दु) |
| 画像 | image | तस्बिर / इमेज |
| 解像度 | resolution | रिजोल्युसन |
| 座標 | coordinate | निर्देशाङ्क |
| グレースケール | grayscale | ग्रेस्केल |
| 2 値化 | binarization / thresholding | बाइनरीकरण (थ्रेसोल्ड गर्ने) |
| しきい値 | threshold | थ्रेसहोल्ड (सीमा मान) |
| マスク | mask | मास्क |
| 輪郭 | contour | कन्टुर (बाहिरी घेरा) |
| 前景 / 背景 | foreground / background | अग्रभाग / पृष्ठभूमि |
| 分類 | classification | वर्गीकरण |
| 物体検出 | object detection | वस्तु पहिचान (डिटेक्सन) |
| セグメンテーション | segmentation | सेग्मेन्टेसन |
| 異常検知 | anomaly detection | असामान्यता पहिचान |
| 正常 / 異常 | normal / anomaly | सामान्य / असामान्य |
| バウンディングボックス | bounding box | बाउन्डिङ बक्स |
| 信頼度 | confidence | विश्वास स्कोर (कन्फिडेन्स) |
| 正解ラベル | ground truth label | सही लेबल (ग्राउन्ड ट्रुथ) |
| 学習 / 訓練 | training | प्रशिक्षण (ट्रेनिङ) |
| 推論 / 予測 | inference / prediction | अनुमान (इन्फरेन्स) |
| 評価 | evaluation | मूल्याङ्कन |
| データセット | dataset | डेटासेट |
| 学習用 / 検証用 / 試験用 | train / validation / test split | प्रशिक्षण / प्रमाणीकरण / परीक्षण भाग |
| 較正 | calibration | क्यालिब्रेसन (मापन मिलाउने) |
| 許容差 / 公差 | tolerance | सह्यता (टोलरेन्स) |
| 不良 / 欠陥 | defect | दोष (डिफेक्ट) |
| 見逃し | miss / false negative | छुट्नु (मिस) |
| 誤検出 / 誤報 | false alarm / false positive | झुटो अलार्म (फल्स पोजिटिभ) |
| 合格 / 不合格 | pass / reject (OK / NG) | पास (OK) / रिजेक्ट (NG) |
| 合成データ | synthetic data | संश्लेषित डेटा |
| 模式図 | schematic | योजनाबद्ध चित्र (स्किम्याटिक) |
| 参考出力 | reference output | सन्दर्भ नतिजा |
| 再現性 | reproducibility | पुनरुत्पादनशीलता |
| 特徴 | feature | फिचर (विशेषता) |
| 記憶 / メモリバンク | memory bank | मेमोरी ब्याङ्क |
| 最近傍 | nearest neighbour | नजिकको छिमेकी |
| パッチ | patch | प्याच (सानो टुक्रा) |
| スコアマップ | score map | स्कोर नक्सा |
| バッチ | batch | ब्याच |
| エポック | epoch | एपोक |
| 学習曲線 | learning curve | सिकाइ वक्र (कर्भ) |
| 重み | weight | वेट (तौल) |
| カーネル | kernel | कर्नेल |
| ウィジェット | widget | विजेट |
| 演習 | exercise | अभ्यास |
| ヒント | hint | सङ्केत |
| 理解度チェック | understanding questions | बुझाइ जाँच्ने प्रश्न |
| 完了チェックリスト | completion checklist | सम्पन्नता जाँचसूची |
| トラブルシューティング | troubleshooting | समस्या समाधान |
| 環境構築 | environment setup | वातावरण तयारी |
| 仮想環境 | virtual environment | भर्चुअल वातावरण |
| 端末 / コマンドプロンプト | terminal / Command Prompt | कमाण्ड प्रोम्प्ट (CMD) |
| 作業ディレクトリ | working directory | काम गर्ने फोल्डर |

## Measurement vocabulary kept numerically exact

| 日本語 | English | नेपाली |
| --- | --- | --- |
| 画素を mm に変換 | pixels to millimetres | पिक्सेललाई mm मा बदल्ने |
| 分解能（mm/画素） | resolution in mm per pixel | प्रति पिक्सेल mm मा रिजोल्युसन |
| 許容差 100.0 ± 0.5 mm | tolerance 100.0 ± 0.5 mm | सह्यता 100.0 ± 0.5 mm |
| 画像単位の評価 | image-level assessment | तस्बिर-स्तरको मूल्याङ्कन |
| 物体単位の評価 | object-level assessment | वस्तु-स्तरको मूल्याङ्कन |
| 画像スコアとマップ最大値 | image score vs map maximum | इमेज स्कोर र स्कोर नक्साको अधिकतम मान |

## Style notes

* Use `तपाईं` for the learner ("you"), `हामी` for "we".
* Use short sentences: one idea per sentence.
* Imperative instructions use `गर्नुहोस्` (`यो सेल चलाउनुहोस्`).
* Avoid the Japanese full-width colon (`：`) inside Nepali lines; use `:`.
* Never write `日本語：` or `English:` labels; the repository validator rejects them.
* When a Devanagari technical term is new, pair it once with a plain explanation:
  `थ्रेसहोल्ड (सीमा मान) — योभन्दा माथिको मानलाई दोष मानिन्छ।`

## Variants left for the native review

Two terminology alternatives remain in the delivered catalogs. Their idiomatic suitability is
pending native Nepali review; no equivalence or preference is assumed here. They are listed
instead of being silently rewritten, so the reviewer can pick one and the applier can normalise
every occurrence in a single pass afterwards.

| glossary form | alternative for review |
| --- | --- |
| ``निर्देशाङ्क`` (coordinate) | ``निर्देशांक`` |
| ``सह्यता`` (tolerance) | ``सहनशीलता`` |

``छुट्नु`` (the verb, "to be missed") and ``छुट्ने`` (its participle, used in tables and headings) are
both intended and both stay: a heading needs the participle.

## Words this pass added

| 日本語 | English | नेपाली (approved) |
| --- | --- | --- |
| 偽陽性 / 偽陰性 | false positive / false negative | झुटो अलार्म (फल्स पोजिटिभ) / छुट्ने (फल्स नेगेटिभ) |
| 偽陽性（良品を NG と判定） | false reject | गलत अस्वीकृति (फल्स रिजेक्ट) |
| 較正用 / 試験用 | calibration / test | क्यालिब्रेसन / परीक्षण |
| 見逃し率 | miss rate | छुट्ने दर |