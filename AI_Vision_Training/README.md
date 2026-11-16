# 広島化成 第1週 AI・マシンビジョン研修 / Hiroshima Kasei Week 1 AI & Machine Vision Training

化成品（Kaseihin）部門の方を対象とした、**5 日間・16 ノートブック**の
自習型 AI 研修教材です。Python も AI も画像処理も未経験の方を前提に作っています。

A five-day, **16-notebook** self-study AI course for the Kaseihin (化成品)
department, written for people with **no prior experience** in Python, AI or image processing.

| 項目 / Item | 内容 / Details |
|---|---|
| 期間 / Period | 2026 年 11 月 16 日（月）〜 20 日（金） / 16-20 November 2026 |
| 対象 / Audience | プログラミング未経験の化成品部門スタッフ / Kaseihin staff with no programming background |
| 時間 / Hours | 08:00–16:50（昼休み 12:00–12:50） / with lunch 12:00-12:50 |
| 到達点 / Outcome | 高速塩ビシート検査のための AI の基礎を、自分のことばで説明し、実際に動かせること / explain and run the AI foundations needed for high-speed PVC sheet inspection |
| 範囲 / Scope | **第 1 週のみ**。実際の検査システム構築は第 2 週で行います。 / **Week 1 only**; the real inspection system is Week 2. |

---

<!-- ne:begin doc:142d737232 -->
### नेपालीमा

कासेइहिन विभागका कर्मचारीका लागि बनाइएको **५ दिन, १६ नोटबुक** को स्वअध्ययन AI तालिम सामग्री हो।
Python, AI र चित्र प्रशोधनको अनुभव नभएका मानिसलाई लक्षित गरेर बनाइएको छ।

| विषय | विवरण |
|---|---|
| अवधि | 2026 नोभेम्बर 16 (सोम) – 20 (शुक्र) |
| लक्षित | प्रोग्रामिङ अनुभव नभएका कासेइहिन विभागका कर्मचारी |
| समय | 08:00–16:50 (दिउँसोको खाना 12:00–12:50) |
| पुग्ने लक्ष्य | उच्च गतिको PVC सिट निरीक्षणका लागि चाहिने AI को आधार आफ्नै शब्दमा बुझाउन र चलाउन सक्ने |
| दायरा | **हप्ता १ मात्र**। वास्तविक निरीक्षण प्रणाली निर्माण हप्ता २ मा हुन्छ। |
<!-- ne:end -->

## 1. 最初に読むもの / Read this first

次の順番で進めてください。

1. [`START_HERE.md`](START_HERE.md) — パソコンの電源を入れるところから始める、超初心者向け手順
2. [`COURSE_SYLLABUS.md`](COURSE_SYLLABUS.md) — **時間割の唯一の正**。各日の必須時間・予備時間・前日までの準備
3. `notebooks/00_Setup/00_Environment_Setup.ipynb` — 環境のセットアップと確認（**授業時間の外** に行います）

Follow this order: `START_HERE.md` (from switching the PC on), then `COURSE_SYLLABUS.md` (the
**single source of truth** for the timetable, including preflight), then the setup notebook —
which is done **outside the lesson hours**.

---

<!-- ne:begin doc:967583ec4e -->
### नेपालीमा

तलको क्रममा अगाडि बढ्नुहोस्।

1. [`START_HERE.md`](START_HERE.md) — कम्प्युटर अन गर्नेदेखि सुरु हुने, एकदमै सुरुवाती तहका लागि प्रक्रिया
2. [`COURSE_SYLLABUS.md`](COURSE_SYLLABUS.md) — **समयतालिकाको एक मात्र आधिकारिक स्रोत**। हरेक दिनको अनिवार्य समय, बचत समय र अघिल्लो दिनसम्मको तयारी
3. `notebooks/00_Setup/00_Environment_Setup.ipynb` — वातावरण सेटअप र जाँच (**पाठ समयबाहिर** गरिन्छ)
<!-- ne:end -->

## 1.1 時間の考え方 / How the time adds up

自習は 1 日 **360 分**（09:00–12:00 と 13:50–16:50）です。そのうち
**必須の学習・演習は 270〜300 分**、残りの **60〜90 分** は休憩・トラブル対応・提出に使います。

Self-study gives **360 minutes** a day. **270-300 minutes** are required lesson and exercise work;
the remaining **60-90 minutes** are explicitly budgeted for breaks, troubleshooting and submission.

ノートブックの所要時間は **暫定値** です。初学者 1 名とのパイロットで測るまで確定しません。
The notebook durations are **provisional** until measured in a pilot with one beginner.

**演習 3（発展）は任意** です。完了チェックリストには入っていません。
**Exercise 3 (challenge) is optional** and is never part of the completion checklist.

---

<!-- ne:begin doc:b50dcca840 -->
### नेपालीमा

स्वअध्ययन दिनको **360 मिनेट** (09:00–12:00 र 13:50–16:50) हो। त्यसमध्ये
**अनिवार्य सिकाइ र अभ्यास 270–300 मिनेट**, बाँकी **60–90 मिनेट** विश्राम, समस्या समाधान र बुझाउनमा
खर्च हुन्छ।

नोटबुकको लाग्ने समय **प्रारम्भिक अनुमान** हो। एक जना सुरुवाती प्रशिक्षार्थीसँगको pilot मा नापेपछि
मात्र निश्चित हुन्छ।

**अभ्यास 3 (विकास) ऐच्छिक** हो। सकिएको जाँचसूचीमा पर्दैन।
<!-- ne:end -->

## 2. この研修で身につくこと / What you will be able to do

5 日間の終わりに、次のことができるようになります。

| 日 / Day | できるようになること / You will be able to |
|---|---|
| 1 | AI・機械学習・深層学習の違いを説明する。画像が数値の表であることを説明し、自分で書き換える。 / Explain AI vs ML vs DL; explain that an image is a table of numbers and modify one. |
| 2 | Python で判定プログラムを書く。OpenCV で画像を読み、2 値化し、ピクセルを mm に換算する。 / Write a judgement program; read and threshold an image; convert pixels to mm. |
| 3 | 学習済み YOLO を動かし、検出結果を読み、しきい値を変えて挙動を説明する。 / Run a pretrained YOLO, read its results, explain threshold effects. |
| 4 | データセットを点検し、YOLO をファインチューニングし、試験データで評価する。 / Inspect a dataset, fine-tune YOLO, evaluate on held-out data. |
| 5 | PatchCore で異常検知を実行し、YOLO と比較して、塩ビ検査への推奨を作る。 / Run PatchCore anomaly detection, compare it with YOLO, and recommend an approach for PVC. |

---

<!-- ne:begin doc:c46af914d7 -->
### नेपालीमा

५ दिनको अन्त्यमा तलका कुरा गर्न सक्ने हुनुहुनेछ।

| दिन | गर्न सक्ने |
|---|---|
| 1 | AI, मेसिन लर्निङ, डिप लर्निङको फरक बुझाउने। चित्र सङ्ख्याको तालिका हो भनेर बुझाएर आफैं बदल्ने। |
| 2 | Python मा निर्णय प्रोग्राम लेख्ने। OpenCV ले चित्र पढेर दुई-मान बनाउने र pixel लाई mm मा बदल्ने। |
| 3 | सिकिएको YOLO चलाएर नतिजा पढ्ने र threshold बदल्दा व्यवहार कसरी बदलिन्छ बुझाउने। |
| 4 | डेटासेट जाँच्ने, YOLO fine-tune गर्ने र परीक्षण डेटामा मूल्याङ्कन गर्ने। |
| 5 | PatchCore ले anomaly detection चलाएर YOLO सँग तुलना गर्ने र PVC निरीक्षणका लागि सिफारिस बनाउने। |
<!-- ne:end -->

## 3. インストール / Installation

正式な番号付き手順は [START_HERE.md](START_HERE.md) です。Python 3.11 を使い、授業前に
両環境・写真・重みを準備します。以下は環境の概要です。

The authoritative numbered sequence is [START_HERE.md](START_HERE.md). Use Python 3.11 and
prepare both environments, photos and weights before class. The following is an environment overview.

2 つの仮想環境を作ります。**理由を必ず読んでください。**

| 環境 / Environment | 使う日 / Used on | 主なパッケージ / Main packages |
|---|---|---|
| `.venv` | 第 0〜4 日 / Days 0-4 | numpy, matplotlib, opencv-python, torch, ultralytics |
| `.venv-anomalib` | 第 5 日 / Day 5 | anomalib 2.7.0, torch, opencv-**headless** |

> **なぜ分けるのか / Why two environments?**
>
> `anomalib` は `opencv-python-headless` を要求し、`ultralytics` は
> `opencv-python` を要求します。同じ環境に入れると `cv2` が二重になり、OpenCV が壊れます。
> これは公式ドキュメントの依存関係から確認できる、避けられない衝突です。
>
> `anomalib` requires `opencv-python-headless` while `ultralytics` requires
> `opencv-python`. Installing both into one environment gives two `cv2` distributions and breaks
> OpenCV. This is an unavoidable conflict visible in the official dependency metadata.

Windows の検索で「コマンド プロンプト」（`cmd`）を開き、
[START_HERE のステップ1〜8](START_HERE.md) を順番に実行してください。
ZIP・OneDrive・空白を含むパスの扱い、有効化、両カーネルの登録もそこにまとめています。
GPU は必須ではありません。GPU 用ホイールの組み合わせはこの変更では未検証です。

Open **Command Prompt** (`cmd`) from Windows Search and follow
[START_HERE Steps 1–8](START_HERE.md) in order. That single sequence covers ZIP/OneDrive paths,
spaces, activation and both kernels. A GPU is not required; GPU wheel combinations are not
verified by this change.

**検証済みのバージョン / Verified versions:** [`requirements/tested_versions.md`](requirements/tested_versions.md)

---

<!-- ne:begin doc:54c624e7ef -->
### नेपालीमा

आधिकारिक क्रमांकित प्रक्रिया [START_HERE.md](START_HERE.md) हो। Python 3.11 प्रयोग गरेर पाठ अघि
दुवै वातावरण, फोटो र weight तयार गर्नुहोस्। तल वातावरणको सारांश मात्र हो।

दुई virtual environment बनाइन्छ। **कारण अनिवार्य पढ्नुहोस्।**

| वातावरण | प्रयोग हुने दिन | मुख्य package |
|---|---|---|
| `.venv` | दिन 0–4 | numpy, matplotlib, opencv-python, torch, ultralytics |
| `.venv-anomalib` | दिन 5 | anomalib 2.7.0, torch, opencv-**headless** |

> **किन छुट्याउने?**
>
> `anomalib` ले `opencv-python-headless` चाहन्छ, `ultralytics` ले
> `opencv-python` चाहन्छ। एउटै वातावरणमा राख्दा `cv2` दुईवटा हुन्छन् र OpenCV बिग्रन्छ।
> यो आधिकारिक कागजातको dependency बाटै देखिने, छल्न नसकिने द्वन्द्व हो।

Windows को खोजमा "Command Prompt" (`cmd`) खोलेर
[START_HERE को स्टेप 1–8](START_HERE.md) क्रमैसँग चलाउनुहोस्।
ZIP, OneDrive र खाली ठाउँ भएको path को व्यवस्थापन, सक्रिय गर्ने र दुवै kernel दर्ता गर्ने कुरा त्यहीँ छ।
GPU अनिवार्य छैन। GPU wheel को संयोजन यो परिवर्तनमा जाँचिएको छैन।

**जाँचिएका संस्करण:** [`requirements/tested_versions.md`](requirements/tested_versions.md)
<!-- ne:end -->

## 4. 素材（データ）の生成 / Generating the assets

合成画像・図・データセットは **Python で生成** します。参考写真と学習済み重みは授業前に取得します。

Synthetic images, diagrams and datasets are **generated locally by Python**.
Reference photographs and pretrained weights must be downloaded before class.

生成コマンドは [START_HERE ステップ6](START_HERE.md)、
参考写真・重みの取得とオフライン検査はステップ7を使います。
同梱の参考図は、元の保存記録がある講師だけが再生成します。

Use [START_HERE Step 6](START_HERE.md) for generation and Step 7 for photo/weight preloading
and offline checks. Only instructors with the original saved records rebuild reference figures.

| 出力 / Output | 中身 / Contents |
|---|---|
| `assets/diagrams/` | 概念図・校正用画像・教材図 / concept diagrams, a calibration image and the teaching diagrams |
| `assets/reference_outputs/` | 実際の実行結果から作った参考図（出所は同フォルダの `README.md`） / figures built from real saved runs |
| `assets/normal_samples/`, `assets/defect_samples/` | 正常例・欠陥例（正解マスクと座標付き） / normal and defective examples with masks and coordinates |
| `assets/yolo_dataset/` | 96 枚（train 64 / val 16 / test 16）、ラベル、`data.yaml` |
| `assets/anomaly_dataset/pvc_sheet/` | 正常 44 枚、異常 40 枚、正解マスク / 44 normal, 40 abnormal, ground-truth masks |

`assets/diagrams/teach_*.png` と `assets/reference_outputs/ref_*.png` は **配布物に含まれます**
（`.gitignore` の例外）。Python を実行しなくても図が見えるようにするためです。
それ以外の生成物（データセット・重み・学習結果）は従来どおり Git に入れません。

The `assets/diagrams/teach_*.png` and `assets/reference_outputs/ref_*.png` files **ship with the
repository** (exceptions in `.gitignore`) so that the essential figures are readable without
running Python. Everything else — datasets, weights, training outputs — stays out of Git.

`generate_reference_outputs.py` は、教材の実行で保存された結果が無い場合は**図を作らずに
理由を表示して止まります**。数値を創作して埋めることはありません。

`generate_reference_outputs.py` stops and prints why if the saved results are missing. It never
invents numbers to fill a gap.

> **重要 / Important**
>
> これらは **合成画像** です。実際の塩ビの光学的な振る舞いを再現したものでは
> **ありません**。実際の工場画像での検証は第 2 週以降に行います。
> 合成データで得られた精度を、製品の検査精度として引用してはいけません。
>
> These are **synthetic images**. They do NOT reproduce the optical behaviour of the
> factory's PVC material. Real images are required for a meaningful feasibility check in Week 2.
> Never quote accuracy obtained on synthetic data as a product inspection accuracy.

---

<!-- ne:begin doc:61b91bc04f -->
### नेपालीमा

कृत्रिम चित्र, चित्ररेखा र डेटासेट **Python ले बनाइन्छ**। सन्दर्भ फोटो र सिकिएका weight पाठ अघि
ल्याइन्छ।

बनाउने आदेश [START_HERE स्टेप 6](START_HERE.md) मा, र सन्दर्भ फोटो तथा weight लिने र अफलाइन जाँच
स्टेप 7 मा छ। सँगै दिइएका सन्दर्भ चित्र मूल अभिलेख भएका प्रशिक्षकले मात्र फेरि बनाउँछन्।

| नतिजा | सामग्री |
|---|---|
| `assets/diagrams/` | अवधारणा चित्र, क्यालिब्रेसन चित्र र सिकाइ चित्र |
| `assets/reference_outputs/` | वास्तविक चलाइका नतिजाबाट बनेका सन्दर्भ चित्र (स्रोत त्यही फोल्डरको `README.md` मा) |
| `assets/normal_samples/`, `assets/defect_samples/` | सामान्य र दोष नमुना (सही mask र निर्देशांक सहित) |
| `assets/yolo_dataset/` | 96 चित्र (train 64 / val 16 / test 16), लेबल, `data.yaml` |
| `assets/anomaly_dataset/pvc_sheet/` | सामान्य 44, असामान्य 40, सही mask |

`assets/diagrams/teach_*.png` र `assets/reference_outputs/ref_*.png` **वितरणमा समावेश हुन्छन्**
(`.gitignore` को अपवाद)। Python नचलाई पनि चित्र देखिन भनेर यसो गरिएको हो।
अरू बनाइएका सामग्री (डेटासेट, weight, सिकाइ नतिजा) पहिलेझैं Git मा राखिँदैन।

`generate_reference_outputs.py` मा सिकाइको चलाइबाट सुरक्षित नतिजा छैन भने **चित्र नबनाई कारण
देखाएर रोकिन्छ**। सङ्ख्या बनाएर भर्ने काम कहिल्यै गर्दैन।

> **महत्त्वपूर्ण**
>
> यी **कृत्रिम चित्र** हुन्। वास्तविक PVC को प्रकाशिक व्यवहार **पुनःउत्पादन गर्दैनन्**।
> वास्तविक कारखानाको चित्रमा जाँच हप्ता २ पछि मात्र गरिन्छ।
> कृत्रिम डेटामा पाइएको शुद्धतालाई उत्पादन निरीक्षणको शुद्धता भनेर उद्धृत गर्नु हुँदैन।
<!-- ne:end -->

## 4.1 解説 PDF / Explanation PDFs

ノートブックの説明から自動で組んだ冊子を `docs/pdf/` に置いています。オフラインで読むための
副教材で、演習はノートブックで行います。

Companion booklets typeset from the notebooks' own Markdown live in `docs/pdf/`. They are for
offline reading; the exercises are still done in Jupyter.

| ファイル / File | 内容 / Contents |
|---|---|
| `docs/pdf/Day01_explanation_ja_en.pdf` … `Day05_…` | 各日の解説（日本語 → 英語） / one booklet per day |
| `docs/pdf/Week1_explanation_ja_en.pdf` | 5 日分をまとめたもの / all five days |
| `docs/pdf/Day01_explanation_ja_en_ne.pdf` … `Day05_…` | 各日の解説（日本語 → 英語 → ネパール語） / one booklet per day, with Nepali |
| `docs/pdf/Week1_explanation_ja_en_ne.pdf` | 5 日分をまとめた三言語版 / all five days, trilingual |
| `docs/pdf/Setup_ja_en_ne.pdf`, `Installation_Guide_ja_en_ne.pdf`, `Repository_Guide_ja_en_ne.pdf`, `Course_Syllabus_ja_en_ne.pdf` | 準備ノートブック・導入・リポジトリ案内・シラバスの三言語版 / the setup notebook, installation, repository guide and syllabus in three languages |
| `docs/pdf/README.md` | 作り方・含まれるもの・限界 / how to rebuild, what is in, limitations |

```cmd
REM PDF generation and inspection only; not needed by learners.
".\.venv\Scripts\python.exe" -m pip install -r requirements\pdf.txt
".\.venv\Scripts\python.exe" -m playwright install chromium
".\.venv\Scripts\python.exe" assets\scripts\export_explanations_pdf.py
".\.venv\Scripts\python.exe" assets\scripts\export_trilingual_pdf.py
".\.venv\Scripts\python.exe" assets\scripts\inspect_pdf_pages.py --languages ja,ne
```

* 実行ログ・スタックトレース・長い準備コード・講師用の解答は入りません。
* 対話ウィジェットは、静的図＋「ノートブックで操作する」注記に置き換えています。
* モデルのダウンロードも学習のやり直しも行いません。
* 横長の図は読みやすさのため A4 横向きのページに置いています。
* ネパール語版は Chromium の PDF 出力で組んでいます。ReportLab はデーヴァナーガリーの本文を
  検索できない形でしか書けないためで、**元の日本語＋英語版は書き換えていません。**

The exporter includes no execution logs, no stack traces, no long setup code and no instructor
answer keys; widgets become a static figure plus a note. It downloads nothing and retrains nothing.
Wide figures sit on landscape A4 pages so their labels stay readable. The Nepali booklets are
typeset through Chromium's PDF engine, because ReportLab cannot keep Devanagari searchable; the
original Japanese + English booklets are left untouched.

---

<!-- ne:begin doc:baaae668d6 -->
### नेपालीमा

नोटबुकको व्याख्याबाट स्वतः बनाइएका पुस्तिका `docs/pdf/` मा छन्। अफलाइन पढ्नका लागि सहायक सामग्री
हुन्; अभ्यास भने नोटबुकमै गरिन्छ।

| फाइल | सामग्री |
|---|---|
| `docs/pdf/Day01_explanation_ja_en_ne.pdf` … `Day05_…` | प्रत्येक दिनको व्याख्या (जापानी → अङ्ग्रेजी → नेपाली) |
| `docs/pdf/Week1_explanation_ja_en_ne.pdf` | ५ दिनको एकै पुस्तिका |
| `docs/pdf/Setup_ja_en_ne.pdf` | तयारी नोटबुक |
| `docs/pdf/Installation_Guide_ja_en_ne.pdf` | स्थापना र समस्या समाधान |
| `docs/pdf/Repository_Guide_ja_en_ne.pdf` | रिपोजिटरी र संस्करणको परिचय |
| `docs/pdf/Course_Syllabus_ja_en_ne.pdf` | समयतालिका |
| `docs/pdf/README.md` | बनाउने तरिका, के पर्छ, के पर्दैन, सीमा |

अघिल्ला जापानी–अङ्ग्रेजी संस्करण (`*_ja_en.pdf`) पनि जस्ताको तस्तै राखिएका छन्, त्यसैले दुवै
पढ्न सकिन्छ। नयाँ त्रिभाषी संस्करण बनाउन Chromium (Playwright) चाहिन्छ; जापानी–अङ्ग्रेजी संस्करण
रिपोर्टल्याब (ReportLab) ले नै बन्छ।

```cmd
REM PDF generation and inspection only; not needed by learners.
".\.venv\Scripts\python.exe" -m pip install -r requirements\pdf.txt
".\.venv\Scripts\python.exe" -m playwright install chromium
".\.venv\Scripts\python.exe" assets\scripts\export_explanations_pdf.py
".\.venv\Scripts\python.exe" assets\scripts\export_trilingual_pdf.py
".\.venv\Scripts\python.exe" assets\scripts\inspect_pdf_pages.py --languages ja,ne
```

* चलाइको log, stack trace, लामो तयारी कोड र प्रशिक्षकका जवाफ पर्दैनन्।
* slider भएका ठाउँमा स्थिर चित्र र "नोटबुकमा चलाउनुहोस्" भन्ने टिप्पणी राखिन्छ।
* model download र सिकाइ फेरि गरिँदैन।
* फराकिला चित्र पढ्न सजिलो होस् भनेर A4 तेर्सो पानामा राखिन्छन्।
<!-- ne:end -->

## 5. 起動 / Starting JupyterLab

準備完了後、エクスプローラーで実際の `AI_Vision_Training` を開き、
アドレス欄に `cmd` と入力して Enter。次を実行します。
または同じフォルダの `start_training.cmd` をダブルクリックします。
起動用ファイルはインストール・ダウンロード・学習を行いません。

After preflight, open your actual `AI_Vision_Training` folder in File Explorer, type `cmd`
in its address bar and press Enter, then run the following. Alternatively double-click
`start_training.cmd` there. The launcher never installs, downloads or trains.

```cmd
.\.venv\Scripts\activate.bat
".\.venv\Scripts\python.exe" -m jupyter lab
```

有効化は別の Python の Jupyter 起動ファイルが選ばれるのを防ぎます。この CMD 内だけ有効です。
Activation prevents selecting another Python's Jupyter executable; it affects this CMD only.

ブラウザが開いたら、`notebooks` → `00_Setup` → `00_Environment_Setup.ipynb`
の順に開きます。**第 5 日のノートブックだけは、カーネルを
`Python 3 (AI Vision Anomalib)` に切り替えてください。**

Open `notebooks` -> `00_Setup` -> `00_Environment_Setup.ipynb`. For the **Day 5
notebooks only**, switch the kernel to `Python 3 (AI Vision Anomalib)`.

<!-- ne:begin doc:83b7690592 -->
### नेपालीमा

तयारी सकिएपछि File Explorer मा वास्तविक `AI_Vision_Training` खोलेर
ठेगाना बारमा `cmd` लेखेर Enter थिच्नुहोस्। त्यसपछि तलको आदेश चलाउनुहोस्।
वा त्यही फोल्डरको `start_training.cmd` डबल-क्लिक गर्नुहोस्।
सुरु गर्ने फाइलले install, download वा सिकाइ गर्दैन।

```cmd
.\.venv\Scripts\activate.bat
".\.venv\Scripts\python.exe" -m jupyter lab
```

सक्रिय गर्दा अर्को Python को Jupyter सुरु गर्ने फाइल छानिनबाट जोगाउँछ। यो CMD भित्र मात्र लागू हुन्छ।

ब्राउजर खुलेपछि `notebooks` → `00_Setup` → `00_Environment_Setup.ipynb` क्रममा खोल्नुहोस्।
**दिन ५ को नोटबुकमा मात्र** kernel `Python 3 (AI Vision Anomalib)` मा बदल्नुहोस्।
<!-- ne:end -->

### 5.1 セルの指示 / Cell instructions

すべてのコードセルの先頭に、次のどれかが付きます。
Every code cell starts with one of these banners.

| 表示 / Banner | 意味 / Meaning |
|---|---|
| `実行のみ / Run only` | **Shift + Enter** でそのまま実行。書き換えない / run it, do not edit |
| `この値を変更 / Change this value` | 値を変えて、結果を予想してから実行 / change the value, predict, then run |
| `自分でコードを書く / Write your code` | 空欄を自分で埋める / fill in the blanks |

<!-- ne:begin doc:a3941da5af -->
### नेपालीमा

सबै कोड सेलको सुरुमा तलको एउटा चिन्ह हुन्छ।

| देखिने | अर्थ |
|---|---|
| `実行のみ / Run only` | **Shift + Enter** ले त्यसै चलाउने। नबदल्नुहोस् |
| `この値を変更 / Change this value` | मान बदलेर नतिजा अनुमान गरेपछि चलाउने |
| `自分でコードを書く / Write your code` | खाली ठाउँ आफैं भर्ने |
<!-- ne:end -->

### 5.2 対話デモ / Interactive demos

5 つの短い対話デモがあります。**スライダーを動かすには、生きているカーネルが必要** です。

There are five short interactive demos. **Moving a slider requires a live kernel.**

| 場所 / Where | 何を動かすか / What you move |
|---|---|
| `Day01_02` Part 3 | RGB の 3 つの値 / the three RGB values |
| `Day02_02` Part 2 | ループのステップ（1 つずつ）/ the loop step |
| `Day02_03` Part 2 | OpenCV のしきい値 / the OpenCV threshold |
| `Day03_01` Part 3 | 予測の四角の位置（IoU）/ the predicted box position (IoU) |
| `Day03_03` Part 1 | YOLO の confidence / the YOLO confidence |
| `Day05_03` Part 4 | PatchCore のしきい値（**較正用データのみ**）/ the PatchCore threshold (calibration data only) |

> GitHub のプレビューや静的な HTML では、スライダーは動きません。
> どのデモにも **ウィジェットを使わないパラメータセル** が付いていて、同じ実験ができます。
>
> Sliders do **not** run in GitHub previews or static HTML. Every demo has a **parameter cell that
> needs no widget**, and it runs the same experiment.

---

<!-- ne:begin doc:049571f7e7 -->
### नेपालीमा

५ वटा छोटा अन्तरक्रियात्मक demo छन्। **slider सार्न चलिरहेको kernel चाहिन्छ।**

| ठाउँ | के सार्ने |
|---|---|
| `Day01_02` Part 3 | RGB का तीन मान |
| `Day02_02` Part 2 | loop को step (एक-एक) |
| `Day02_03` Part 2 | OpenCV को threshold |
| `Day03_01` Part 3 | अनुमान गरिएको चौकोणको स्थान (IoU) |
| `Day03_03` Part 1 | YOLO को confidence |
| `Day05_03` Part 4 | PatchCore को threshold (**क्यालिब्रेसन डेटा मात्र**) |

> GitHub preview वा स्थिर HTML मा slider चल्दैन।
> हरेक demo मा **widget नचाहिने parameter सेल** छ, जसले उही प्रयोग गर्न दिन्छ।
<!-- ne:end -->

## 6. 検証とテスト / Validation and tests

準備済みの基本環境を有効化した CMD で実行します（[START_HERE](START_HERE.md)）。
Run in CMD with the prepared base environment activated (see [START_HERE](START_HERE.md)).

```cmd
REM Check the environment.
python assets\scripts\verify_environment.py --profile all

REM Structural validation (fast).
python assets\scripts\validate_notebooks.py

REM Execute the lightweight notebooks.
python assets\scripts\validate_notebooks.py --execute lightweight

REM Automated asset and dataset tests.
python -m pytest assets\tests -v

REM Check language labels without writing.
python assets\scripts\normalize_language_labels.py --check

REM Re-apply cell instruction banners (maintainers only; writes notebooks).
python assets\scripts\scaffold_notebooks.py

REM Check widget rendering.
python assets\scripts\check_widgets.py
```

`assets/scripts/validate_notebooks.py --execute all` は **モデルのダウンロード** と
**学習** を含むため、長時間かかります。
`--execute all` includes model downloads and training, so it takes a long time.

`check_widgets.py` はノートブックを実行して、`widgets.interact` を使うセルが
ウィジェット表示（`application/vnd.jupyter.widget-view+json`）を出したかを確認します。
ブラウザで実際にクリックする確認は別です。
`check_widgets.py` executes a notebook and checks that the cells using `widgets.interact` emitted a
widget view. Clicking the controls in a browser is a separate, manual check.

---

<!-- ne:begin doc:80f7f4299b -->
### नेपालीमा

तयार भइसकेको आधारभूत वातावरण सक्रिय गरेको CMD मा चलाउनुहोस्
([START_HERE](START_HERE.md) हेर्नुहोस्)।

```cmd
REM Check the environment.
python assets\scripts\verify_environment.py --profile all

REM Structural validation (fast).
python assets\scripts\validate_notebooks.py
```

थप जाँच र मर्मतका आदेश तल छन्। सामान्य विद्यार्थीले संरचनात्मक जाँचपछि पाठमा जान सक्छन्।
`--execute lightweight` र `check_widgets.py` ले नोटबुक चलाउँछन्; संरचनात्मक जाँच मात्र चाहिएको
अवस्थामा यी नचलाउनुहोस्। `scaffold_notebooks.py` ले नोटबुक बदल्छ र मर्मतकर्ताका लागि मात्र हो।

```cmd
REM Execute the lightweight notebooks.
python assets\scripts\validate_notebooks.py --execute lightweight

REM Automated asset and dataset tests.
python -m pytest assets\tests -v

REM Check language labels without writing.
python assets\scripts\normalize_language_labels.py --check

REM Re-apply cell instruction banners (maintainers only; writes notebooks).
python assets\scripts\scaffold_notebooks.py

REM Check widget rendering.
python assets\scripts\check_widgets.py
```

`assets/scripts/validate_notebooks.py --execute all` मा **model download** र **सिकाइ** पर्ने हुनाले
धेरै समय लाग्छ।

`check_widgets.py` ले नोटबुक चलाएर `widgets.interact` प्रयोग गर्ने सेलले widget देखाएको छ कि छैन
जाँच्छ। ब्राउजरमा वास्तवमा क्लिक गरेर जाँच्ने काम छुट्टै हो।
<!-- ne:end -->

## 7. フォルダ構成 / Project structure

```text
AI_Vision_Training/
├── README.md                     <- このファイル / this file
├── START_HERE.md                 <- 超初心者向け手順 / absolute beginner guide
├── COURSE_SYLLABUS.md            <- 5 日間の時間割 / five-day timetable
├── requirements/                 <- 検証済みバージョン / verified versions
│   ├── base.txt, yolo.txt, anomalib.txt
│   └── tested_versions.md
├── notebooks/
│   ├── 00_Setup/                 <- 環境セットアップ
│   ├── Day01_AI_Fundamentals/    <- 3 冊 / 3 notebooks
│   ├── Day02_Python_OpenCV/      <- 3 冊
│   ├── Day03_YOLO_Basics/        <- 3 冊
│   ├── Day04_YOLO_Training/      <- 3 冊
│   └── Day05_PatchCore/          <- 3 冊
├── assets/
│   ├── diagrams/                 <- 生成された概念図 / generated diagrams
│   ├── reference_outputs/        <- 実際の実行結果から作った参考図 / figures from real runs
│   ├── normal_samples/           <- 正常例 / normal examples
│   ├── defect_samples/           <- 欠陥例 / defect examples
│   ├── yolo_dataset/             <- YOLO データセット / YOLO dataset
│   ├── anomaly_dataset/          <- PatchCore データセット / PatchCore dataset
│   ├── external_samples/         <- 外部由来素材と出所 / external assets and provenance
│   ├── scripts/                  <- 生成・検証スクリプト / generation and validation scripts
│   └── tests/                    <- pytest
├── docs/
│   ├── pdf/                      <- 解説 PDF と再生成手順 / explanation PDFs and how to rebuild
│   ├── instructor/               <- 講師用ガイド（各日）/ instructor guides (per day)
│   ├── troubleshooting/          <- トラブル対処 / troubleshooting
│   └── reference_materials.md    <- 公式ドキュメントへのリンク / official links
├── submissions/                  <- 提出物（日別）/ submission folders (per day)
└── training_results/             <- 学習出力（Git 管理外）/ training outputs (git-ignored)
```

---

<!-- ne:begin doc:0e875b8266 -->
### नेपालीमा

```text
AI_Vision_Training/
├── README.md                     <- यही फाइल
├── START_HERE.md                 <- एकदमै सुरुवाती तहको प्रक्रिया
├── COURSE_SYLLABUS.md            <- ५ दिनको समयतालिका
├── requirements/                 <- जाँचिएका संस्करण
├── notebooks/                    <- 16 नोटबुक (00_Setup र दिन 1–5)
├── assets/                       <- चित्र, नमुना, डेटासेट, स्क्रिप्ट, test
├── docs/                         <- PDF, प्रशिक्षक मार्गदर्शन, समस्या समाधान, सन्दर्भ
├── submissions/                  <- दिनअनुसार बुझाउने काम
└── training_results/             <- सिकाइको नतिजा (Git मा पर्दैन)
```
<!-- ne:end -->

## 8. 提出物 / Submissions

毎日、`submissions/day0N/` に次の 4 つを保存してください。

1. 実行済みのノートブック（`File` → `Save`）
2. `Day0N_Report_Template.md` を埋めたもの
3. 保存した画像・CSV・JSON
4. エラーが出た場合はそのメッセージと、試したこと

Each day, leave four things in `submissions/day0N/`: the executed notebook, the filled
report template, the saved images/CSVs/JSONs, and — if you hit an error — the message plus what you
tried.

講師用の解答例は `docs/instructor/` にあります。**先に自分で書いてください。**
Model answers live in `docs/instructor/`. **Write your own answer first.**

---

<!-- ne:begin doc:c3842ba36e -->
### नेपालीमा

हरेक दिन `submissions/day0N/` मा तलका ४ कुरा राख्नुहोस्।

1. चलाइएको नोटबुक (`File` → `Save`)
2. `Day0N_Report_Template.md` भरेको
3. सुरक्षित गरेका चित्र, CSV, JSON
4. त्रुटि आए त्यसको सन्देश र प्रयास गरेका कुरा

प्रशिक्षकका नमुना जवाफ `docs/instructor/` मा छन्। **पहिले आफैं लेख्नुहोस्।**
<!-- ne:end -->

## 9. 困ったとき / When something goes wrong

まず次の順番で確認してください。

1. 各ノートブック末尾の「困ったときは / Troubleshooting」表
2. [`docs/troubleshooting/installation.md`](docs/troubleshooting/installation.md)
3. `python assets\scripts\verify_environment.py --profile all`

Check the troubleshooting table at the end of each notebook, then
`docs/troubleshooting/installation.md`, then run the environment verifier.

---

<!-- ne:begin doc:e1bc74c9a8 -->
### नेपालीमा

पहिले तलको क्रममा जाँच्नुहोस्।

1. प्रत्येक नोटबुकको अन्त्यमा भएको "समस्या आउँदा" तालिका
2. [`docs/troubleshooting/installation.md`](docs/troubleshooting/installation.md)
3. `python assets\scripts\verify_environment.py --profile all`
<!-- ne:end -->

## 10. 既知の制限 / Known limitations

| 制限 / Limitation | 理由 / Reason |
|---|---|
| 合成画像のみ / synthetic data only | 実際の塩ビ画像はまだ提供されていない / no real PVC images available yet |
| CPU 前提の小さな設定 / small CPU-oriented configuration | 研修 PC に GPU が無いことを前提 / assumes training PCs without a GPU |
| 学習画像 64 枚 / 64 training images | 1 日で終わる分量に抑えている / keeps the exercise within one day |
| PatchCore の評価データは半数 / half of the eval data | 検証と試験に分けるため / split into validation and test |
| YOLO と PatchCore は別環境 / two environments | OpenCV の衝突（上記 3 節）/ the OpenCV conflict described in section 3 |
| PDF の図内文字は検索できない / figure text in the PDFs is not searchable | 図は画像として埋め込んでいる / figures are embedded as images |
| PDF に実行ログは入らない / no execution logs in the PDFs | 出力は環境ごとに変わるため / outputs differ per machine |

Every limitation above is deliberate and documented; none of them is a workaround for a
failing component. Real production feasibility requires real images, a fixed camera and lighting
design, and a threshold study on known-good production — all of which are Week 2 topics.

---

<!-- ne:begin doc:0c5d782eec -->
### नेपालीमा

| सीमा | कारण |
|---|---|
| कृत्रिम चित्र मात्र | वास्तविक PVC चित्र अझै उपलब्ध छैन |
| CPU का लागि सानो सेटिङ | तालिमका PC मा GPU छैन भन्ने मान्यता |
| सिकाइ चित्र 64 वटा | एक दिनमा सकिने मात्रा राखिएको |
| PatchCore को मूल्याङ्कन डेटा आधा | validation र test मा बाँड्न |
| YOLO र PatchCore छुट्टै वातावरण | OpenCV को द्वन्द्व (माथिको खण्ड 3) |
| PDF भित्रको चित्रका अक्षर खोज्न मिल्दैन | चित्रलाई image को रूपमा राखिएको |
| PDF मा चलाइको log पर्दैन | output वातावरणअनुसार फरक पर्ने |

माथिका सबै सीमा जानाजान अपनाइएका र अभिलेख गरिएका हुन्; कुनै पनि बिग्रिएको भाग लुकाउने उपाय होइन।
वास्तविक उत्पादनमा सम्भव छ कि छैन भन्ने कुरा वास्तविक चित्र, स्थिर क्यामेरा र उज्यालोको डिजाइन, र
थाहा भएका राम्रा उत्पादनमा threshold अध्ययनमा निर्भर छ — यी सबै हप्ता २ का विषय हुन्।
<!-- ne:end -->

## 11. ライセンスと出所 / Licensing and provenance

この研修で使う外部素材の出所とライセンスは
[`assets/external_samples/PROVENANCE.md`](assets/external_samples/PROVENANCE.md) に記録しています。

**重要 / Important:** 学習目的での利用は問題ありませんが、
**Ultralytics のモデルとコードは AGPL-3.0** です。製品への組み込みは、
ライセンスの確認なしに行わないでください。

Provenance and licences of external assets are recorded in
`assets/external_samples/PROVENANCE.md`. Educational use is fine, but **Ultralytics code and released
models are AGPL-3.0** — do not embed them in a product without a licence review.

<!-- ne:begin doc:94dd206991 -->
### नेपालीमा

यो तालिममा प्रयोग हुने बाह्य सामग्रीको स्रोत र लाइसेन्स
[`assets/external_samples/PROVENANCE.md`](assets/external_samples/PROVENANCE.md) मा अभिलेख छ।

**महत्त्वपूर्ण:** सिकाइका लागि प्रयोग गर्दा समस्या छैन, तर
**Ultralytics का model र कोड AGPL-3.0** हुन्। उत्पादनमा समावेश गर्नुअघि
लाइसेन्स जाँच नगरी अगाडि नबढ्नुहोस्।
<!-- ne:end -->
