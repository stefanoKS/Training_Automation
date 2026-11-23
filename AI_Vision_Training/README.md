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
### Nepali ma

kaseihin bibhagaka karmacharika lagi banaiyeko **5 din, 16 notebook** ko sbaadhyayan AI talim samagri ho.
Python, AI ra chitra prashodhanako anubhab nabhaeka manisalai lakshit garera banaiyeko chha.

| bishay | biwaran |
|---|---|
| abadhi | 2026 nobhembar 16 (som) – 20 (shukr) |
| lakshit | programing anubhab nabhaeka kaseihin bibhagaka karmachari |
| samay | 08:00–16:50 (diunsoko khana 12:00–12:50) |
| pugne lakshya | uchcha gatiko PVC sit nirikshanka lagi chahine AI ko adhar aphnai shabdama bujhaun ra chalaun sakne |
| dayara | **hapta 1 matra**. bastabik nirikshan pranali nirman hapta 2 ma hunchha. |
<!-- ne:end -->

## 0. 第7日〜第9日（自動化設備研修）/ Days 7–9 (automation course)

第1週とは別に、**第7日〜第9日**の「自動化設備の構想から試運転まで」の3日間コースがあります。第1週の16ノートブックとは独立しており、Day 1〜6の教材は変更していません。

Separately from Week 1, there is a **three-day Days 7–9 course** on automation equipment, from concept to commissioning. It is independent of the Week 1 set of 16 notebooks, and the Day 1–6 materials are unchanged.

- 時間割 / timetable: [`COURSE_SYLLABUS_DAY07_09.md`](COURSE_SYLLABUS_DAY07_09.md)
- 入口・教材一覧 / entry point and materials: [`day07_09_support/README_ja_en.md`](day07_09_support/README_ja_en.md)
- ノートブック / notebooks: [`notebooks/Day07_Automation_Concept_Mechanics/`](notebooks/Day07_Automation_Concept_Mechanics/), [`Day08_Electrical_PLC/`](notebooks/Day08_Electrical_PLC/), [`Day09_Communication_Commissioning/`](notebooks/Day09_Communication_Commissioning/)
- ワークシート / worksheets: [`day07_09_support/worksheets/`](day07_09_support/worksheets/)
- 解説PDF / explanation PDFs: [`docs/pdf/Day07_explanation_ja_en.pdf`](docs/pdf/Day07_explanation_ja_en.pdf), Day08, Day09
- 講師ガイド / instructor guides: [`docs/instructor/day07_instructor_guide.md`](docs/instructor/day07_instructor_guide.md), day08, day09
- 元PDFの正誤表 / source-PDF errata: [`docs/reference/Automation_Equipment_PDF_Errata_ja_en.md`](docs/reference/Automation_Equipment_PDF_Errata_ja_en.md)

第7日〜第9日は、実機の配線・通電・空圧・安全検証を行いません。教育用のオフライン教材です。

Days 7–9 do not perform real wiring, energisation, pneumatics or safety validation. They are offline teaching materials.

---

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
### Nepali ma

talako kram ma agadi badhnuhos.

1. [`START_HERE.md`](START_HERE.md) — computer an garne dekhi suru hune, ekadamai surubati tahaka lagi prakriya
2. [`COURSE_SYLLABUS.md`](COURSE_SYLLABUS.md) — **samayatalikako ek matra adhikarik srot**. harek dinko aniwarya samay, bachat samay ra aghillo dinasammako tayari
3. `notebooks/00_Setup/00_Environment_Setup.ipynb` — batabaran setaap ra jaanch (**paath samayabahir** garinchha)
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
### Nepali ma

sbaadhyayan dinko **360 minet** (09:00–12:00 ra 13:50–16:50) ho. tyasamadhye
**aniwarya sikai ra abhyas 270–300 minet**, banki **60–90 minet** bishram, samasya samadhan ra bujhaunama
kharch hunchha.

notebookko lagne samay **prarambhik anuman** ho. ek jana surubati prashiksharthisangako pilot ma napepachhi
matra nishchit hunchha.

**abhyas 3 (bikas) aichchhik** ho. sakieko janchasuchi ma pardaina.
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
### Nepali ma

5 dinko antya ma talaka kura garna sakne hunuhunechha.

| din | garna sakne |
|---|---|
| 1 | AI, mesin larning, dip larningko farak bujhaune. chitra sankhyako talika ho bhanera bujhaer aphain badalne. |
| 2 | Python ma nirnaya program lekhne. OpenCV le chitra padher dui-maan banaune ra pixel lai mm ma badalne. |
| 3 | sikieko YOLO chalaer natija padhne ra threshold badalda byabahar kasari badlinchha bujhaune. |
| 4 | dataset jaanchne, YOLO fine-tune garne ra parikshan data ma mulyankan garne. |
| 5 | PatchCore le anomaly detection chalaer YOLO sang tulna garne ra PVC nirikshanka lagi sipharis banaune. |
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
### Nepali ma

adhikarik kramankit prakriya [START_HERE.md](START_HERE.md) ho. Python 3.11 prayog garera paath aghi
dubai batabaran, photo ra weight tayar garnuhos. tal batabaranko saransh matra ho.

dui virtual environment banainchha. **karan aniwarya padhnuhos.**

| batabaran | prayog hune din | mukhy package |
|---|---|---|
| `.venv` | din 0–4 | numpy, matplotlib, opencv-python, torch, ultralytics |
| `.venv-anomalib` | din 5 | anomalib 2.7.0, torch, opencv-**headless** |

> **kina chhutyaune?**
>
> `anomalib` le `opencv-python-headless` chahanchha, `ultralytics` le
> `opencv-python` chahanchha. eutai batabaran ma rakhda `cv2` duibata hunchhan ra OpenCV bigranchha.
> yo adhikarik kagajatako dependency batai dekhine, chhaln nasakine dbandb ho.

Windows ko khojama "Command Prompt" (`cmd`) kholer
[START_HERE ko step 1–8](START_HERE.md) kramaisang chalaunuhos.
ZIP, OneDrive ra khali thaun bhaeko path ko byabasthapan, sakriya garne ra dubai kernel darta garne kura tyahin chha.
GPU aniwarya chhaina. GPU wheel ko sanyojan yo paribartanama janchieko chhaina.

**janchieka sanskaran:** [`requirements/tested_versions.md`](requirements/tested_versions.md)
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
### Nepali ma

kritrim chitra, chitrarekha ra dataset **Python le banainchha**. sandarbha photo ra sikieka weight paath aghi
lyainchha.

banaune adesh [START_HERE step 6](START_HERE.md) ma, ra sandarbha photo tatha weight line ra aphalain jaanch
step 7 ma chha. sangai diieka sandarbha chitra mul abhilekh bhaeka prashikshakale matra feri banaunchhan.

| natija | samagri |
|---|---|
| `assets/diagrams/` | abadharana chitra, calibration chitra ra sikai chitra |
| `assets/reference_outputs/` | bastabik chalaika natija baat baneka sandarbha chitra (srot tyahi folderko `README.md` ma) |
| `assets/normal_samples/`, `assets/defect_samples/` | samanya ra dosh namuna (sahi mask ra nirdeshank sahit) |
| `assets/yolo_dataset/` | 96 chitra (train 64 / val 16 / test 16), label, `data.yaml` |
| `assets/anomaly_dataset/pvc_sheet/` | samanya 44, asamanya 40, sahi mask |

`assets/diagrams/teach_*.png` ra `assets/reference_outputs/ref_*.png` **bitaran ma samabesh hunchhan**
(`.gitignore` ko apabad). Python nachalai pani chitra dekhin bhanera yaso garieko ho.
aru banaieka samagri (dataset, weight, sikai natija) pahilejhain Git ma rakhindain.

`generate_reference_outputs.py` ma sikai ko chalaibat surakshit natija chhaina bhane **chitra nabanai karan
dekhaer rokinchha**. sankhya banaer bharne kaam kahilyai gardaina.

> **mahattwapurna**
>
> yi **kritrim chitra** hun. bastabik PVC ko prakashik byabahar **punahutpadan gardainan**.
> bastabik karakhanako chitra ma jaanch hapta 2 pachhi matra garinchha.
> kritrim data ma paieko shuddhatalai utpadan nirikshanko shuddhata bhanera uddhrit garnu hundaina.
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
| `docs/pdf/Day01_explanation_ja_en_ne.pdf` … `Day04_…` | 各日の解説（日本語 → 英語 → ネパール語） / one booklet per day, with Nepali（第 5 日はタマン語の承認後に発行 / Day 5 follows once its Tamang text is approved） |
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
### Nepali ma

notebookko byakhya baat sbatah banaieka pustika `docs/pdf/` ma chhan. aphalain padhnaka lagi sahayak samagri
hun; abhyas bhane notabukamai garinchha.

| file | samagri |
|---|---|
| `docs/pdf/Day01_explanation_ja_en_ne.pdf` … `Day04_…` | pratyek dinko byakhya (Japani → Angreji → Nepali) |
| `docs/pdf/Week1_explanation_ja_en_ne.pdf` | 5 dinko ekai pustika |
| `docs/pdf/Setup_ja_en_ne.pdf` | tayari notebook |
| `docs/pdf/Installation_Guide_ja_en_ne.pdf` | sthapana ra samasya samadhan |
| `docs/pdf/Repository_Guide_ja_en_ne.pdf` | ripojitari ra sanskaranako parichay |
| `docs/pdf/Course_Syllabus_ja_en_ne.pdf` | samayatalika |
| `docs/pdf/README.md` | banaune tarika, ke parchha, ke pardaina, sima |

aghilla Japani–Angreji sanskaran (`*_ja_en.pdf`) pani jastako tastai rakhieka chhan, tyasaile dubai
padhna sakinchha. nayan tribhashi sanskaran banaun Chromium (Playwright) chahinchha; Japani–Angreji sanskaran
riportalyab (ReportLab) le nai banchha.

```cmd
REM PDF generation and inspection only; not needed by learners.
".\.venv\Scripts\python.exe" -m pip install -r requirements\pdf.txt
".\.venv\Scripts\python.exe" -m playwright install chromium
".\.venv\Scripts\python.exe" assets\scripts\export_explanations_pdf.py
".\.venv\Scripts\python.exe" assets\scripts\export_trilingual_pdf.py
".\.venv\Scripts\python.exe" assets\scripts\inspect_pdf_pages.py --languages ja,ne
```

* chalaiko log, stack trace, lamo tayari kod ra prashikshakaka jabaph pardainan.
* slider bhaeka thaun ma sthir chitra ra "notebook ma chalaunuhos" bhanne tippani rakhinchha.
* model download ra sikai feri garindain.
* pharakila chitra padhna sajilo hos bhanera A4 terso panama rakhinchhan.
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
### Nepali ma

tayari sakiepachhi File Explorer ma bastabik `AI_Vision_Training` kholer
thegana barama `cmd` lekher Enter thichnuhos. tyaspachhi talako adesh chalaunuhos.
wa tyahi folderko `start_training.cmd` dabal-klik garnuhos.
suru garne filele install, download wa sikai gardaina.

```cmd
.\.venv\Scripts\activate.bat
".\.venv\Scripts\python.exe" -m jupyter lab
```

sakriya garda arko Python ko Jupyter suru garne file chhaninabat jogaunchha. yo CMD bhitr matra lagu hunchha.

braujar khulepachhi `notebooks` → `00_Setup` → `00_Environment_Setup.ipynb` kram ma kholnuhos.
**din 5 ko notebook ma matra** kernel `Python 3 (AI Vision Anomalib)` ma badalnuhos.
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
### Nepali ma

sabai kod cellko suru ma talako euta chinh hunchha.

| dekhine | arth |
|---|---|
| `実行のみ / Run only` | **Shift + Enter** le tyasai chalaune. nabadalnuhos |
| `この値を変更 / Change this value` | maan badaler natija anuman garepachhi chalaune |
| `自分でコードを書く / Write your code` | khali thaun aphain bharne |
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
### Nepali ma

5 bata chhota antarakriyatmak demo chhan. **slider sarn chaliraheko kernel chahinchha.**

| thaun | ke sarne |
|---|---|
| `Day01_02` Part 3 | RGB ka tin maan |
| `Day02_02` Part 2 | loop ko step (ek-ek) |
| `Day02_03` Part 2 | OpenCV ko threshold |
| `Day03_01` Part 3 | anuman garieko chaukonako sthan (IoU) |
| `Day03_03` Part 1 | YOLO ko confidence |
| `Day05_03` Part 4 | PatchCore ko threshold (**calibration data matra**) |

> GitHub preview wa sthir HTML ma slider chaldain.
> harek demo ma **widget nachahine parameter cell** chha, jasale uhi prayog garna dinchha.
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
### Nepali ma

tayar bhaisakeko adharabhut batabaran sakriya gareko CMD ma chalaunuhos
([START_HERE](START_HERE.md) hernuhos).

```cmd
REM Check the environment.
python assets\scripts\verify_environment.py --profile all

REM Structural validation (fast).
python assets\scripts\validate_notebooks.py
```

thap jaanch ra marmataka adesh tal chhan. samanya bidyarthile sanrachanatmak janchapachhi paath ma jan sakchhan.
`--execute lightweight` ra `check_widgets.py` le notebook chalaunchhan; sanrachanatmak jaanch matra chahieko
abastha ma yi nachalaunuhos. `scaffold_notebooks.py` le notebook badalchha ra marmatakartaka lagi matra ho.

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

`assets/scripts/validate_notebooks.py --execute all` ma **model download** ra **sikai** parne hunale
dherai samay lagchha.

`check_widgets.py` le notebook chalaer `widgets.interact` prayog garne cellle widget dekhaeko chha ki chhaina
janchchha. braujarama bastabama klik garera jaanchne kaam chhuttai ho.
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
### Nepali ma

```text
AI_Vision_Training/
├── README.md                     <- yahi file
├── START_HERE.md                 <- ekadamai surubati tahako prakriya
├── COURSE_SYLLABUS.md            <- 5 dinko samayatalika
├── requirements/                 <- janchieka sanskaran
├── notebooks/                    <- 16 notebook (00_Setup ra din 1–5)
├── assets/                       <- chitra, namuna, dataset, skript, test
├── docs/                         <- PDF, prashikshak margadarshan, samasya samadhan, sandarbha
├── submissions/                  <- din anusar bujhaune kaam
└── training_results/             <- sikai ko natija (Git ma pardaina)
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
### Nepali ma

harek din `submissions/day0N/` ma talaka 4 kura rakhnuhos.

1. chalaieko notebook (`File` → `Save`)
2. `Day0N_Report_Template.md` bhareko
3. surakshit gareka chitra, CSV, JSON
4. truti ae tyasko sandesh ra prayas gareka kura

prashikshakaka namuna jabaph `docs/instructor/` ma chhan. **pahile aphain lekhnuhos.**
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
### Nepali ma

pahile talako kram ma jaanchnuhos.

1. pratyek notebookko antya ma bhaeko "samasya aunda" talika
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
### Nepali ma

| sima | karan |
|---|---|
| kritrim chitra matra | bastabik PVC chitra ajhai upalabdh chhaina |
| CPU ka lagi sano setting | talimka PC ma GPU chhaina bhanne manyata |
| sikai chitra 64 bata | ek din ma sakine matra rakhieko |
| PatchCore ko mulyankan data adha | validation ra test ma bandn |
| YOLO ra PatchCore chhuttai batabaran | OpenCV ko dbandb (mathiko khand 3) |
| PDF bhitrako chitraka akshar khojn mildaina | chitra lai image ko rupama rakhieko |
| PDF ma chalaiko log pardaina | output batabaran anusar farak parne |

mathika sabai sima janajan apanaieka ra abhilekh garieka hun; kunai pani bigrieko bhaag lukaune upay hoina.
bastabik utpadanama sambhab chha ki chhaina bhanne kura bastabik chitra, sthir kyamera ra ujyaloko dijain, ra
thaha bhaeka ramra utpadanama threshold adhyayan ma nirbhar chha — yi sabai hapta 2 ka bishay hun.
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
### Nepali ma

yo talim ma prayog hune bahy samagriko srot ra laisens
[`assets/external_samples/PROVENANCE.md`](assets/external_samples/PROVENANCE.md) ma abhilekh chha.

**mahattwapurna:** sikaika lagi prayog garda samasya chhaina, tar
**Ultralytics ka model ra kod AGPL-3.0** hun. utpadanama samabesh garnuaghi
laisens jaanch nagari agadi nabadhnuhos.
<!-- ne:end -->
