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
| 到達点 / Outcome | 高速 PVC シート検査のための AI の基礎を、自分のことばで説明し、実際に動かせること / explain and run the AI foundations needed for high-speed PVC sheet inspection |
| 範囲 / Scope | **第 1 週のみ**。実際の検査システム構築は第 2 週で行います。 / **Week 1 only**; the real inspection system is Week 2. |

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

## 2. この研修で身につくこと / What you will be able to do

5 日間の終わりに、次のことができるようになります。

| 日 / Day | できるようになること / You will be able to |
|---|---|
| 1 | AI・機械学習・深層学習の違いを説明する。画像が数値の表であることを説明し、自分で書き換える。 / Explain AI vs ML vs DL; explain that an image is a table of numbers and modify one. |
| 2 | Python で判定プログラムを書く。OpenCV で画像を読み、2 値化し、ピクセルを mm に換算する。 / Write a judgement program; read and threshold an image; convert pixels to mm. |
| 3 | 学習済み YOLO を動かし、検出結果を読み、しきい値を変えて挙動を説明する。 / Run a pretrained YOLO, read its results, explain threshold effects. |
| 4 | データセットを点検し、YOLO をファインチューニングし、試験データで評価する。 / Inspect a dataset, fine-tune YOLO, evaluate on held-out data. |
| 5 | PatchCore で異常検知を実行し、YOLO と比較して、PVC 検査への推奨を作る。 / Run PatchCore anomaly detection, compare it with YOLO, and recommend an approach for PVC. |

---

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

### 3.1 基本環境（第 0〜4 日）/ Base environment (Days 0-4)

```powershell
cd "$HOME\Documents\AI_Vision_Training"
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements\base.txt
python -m pip install -r requirements\yolo.txt
python -m ipykernel install --user --name aivision --display-name "Python 3 (AI Vision)"
```

### 3.2 Anomalib 環境（第 5 日）/ Anomalib environment (Day 5)

```powershell
deactivate
py -3.11 -m venv .venv-anomalib
.\.venv-anomalib\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements\anomalib.txt
python -m ipykernel install --user --name aivision-anomalib --display-name "Python 3 (AI Vision Anomalib)"
```

GPU が無くても、この研修はすべて動きます。GPU がある場合の手順は
`requirements/yolo.txt` のコメントを見てください。
Everything works without a GPU. GPU instructions are in the comments of
`requirements/yolo.txt`.

**検証済みのバージョン / Verified versions:** [`requirements/tested_versions.md`](requirements/tested_versions.md)

---

## 4. 素材（データ）の生成 / Generating the assets

合成画像・図・データセットは **Python で生成** します。参考写真と学習済み重みは授業前に取得します。

Synthetic images, diagrams and datasets are **generated locally by Python**.
Reference photographs and pretrained weights must be downloaded before class.

```powershell
# 基本環境に戻る / return to the base environment
deactivate
.\.venv\Scripts\Activate.ps1
# 図とサンプル画像 / concept diagrams and sample images
python assets\scripts\generate_training_assets.py

# 追加の教材図（ノートブックから Markdown で直接参照する静的な図）
# the additional teaching diagrams referenced directly from notebook Markdown
python assets\scripts\generate_teaching_diagrams.py
python assets\scripts\generate_svg_figures.py

# 参考図は同梱済み。再生成は元の保存記録がある講師だけが行います。
# Reference figures ship with the course; only instructors with saved sources rebuild them.

# YOLO 用データセットと PatchCore 用データセット / the two datasets
python assets\scripts\prepare_datasets.py
```

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
> これらは **合成画像** です。実際の PVC の光学的な振る舞いを再現したものでは
> **ありません**。実際の工場画像での検証は第 2 週以降に行います。
> 合成データで得られた精度を、製品の検査精度として引用してはいけません。
>
> These are **synthetic images**. They do NOT reproduce the optical behaviour of the
> factory's PVC material. Real images are required for a meaningful feasibility check in Week 2.
> Never quote accuracy obtained on synthetic data as a product inspection accuracy.

---

## 4.1 解説 PDF / Explanation PDFs

ノートブックの説明から自動で組んだ冊子を `docs/pdf/` に置いています。オフラインで読むための
副教材で、演習はノートブックで行います。

Companion booklets typeset from the notebooks' own Markdown live in `docs/pdf/`. They are for
offline reading; the exercises are still done in Jupyter.

| ファイル / File | 内容 / Contents |
|---|---|
| `docs/pdf/Day01_explanation_ja_en.pdf` … `Day05_…` | 各日の解説（日本語 → 英語） / one booklet per day |
| `docs/pdf/Week1_explanation_ja_en.pdf` | 5 日分をまとめたもの / all five days |
| `docs/pdf/README.md` | 作り方・含まれるもの・限界 / how to rebuild, what is in, limitations |

```powershell
python -m pip install -r requirements\pdf.txt          # 生成・点検用（学習には不要）
python assets\scripts\export_explanations_pdf.py        # 6 つの PDF を作り直す
python assets\scripts\inspect_pdf_pages.py              # 全ページを画像にして点検
```

* 実行ログ・スタックトレース・長い準備コード・講師用の解答は入りません。
* 対話ウィジェットは、静的図＋「ノートブックで操作する」注記に置き換えています。
* モデルのダウンロードも学習のやり直しも行いません。
* 横長の図は読みやすさのため A4 横向きのページに置いています。

The exporter includes no execution logs, no stack traces, no long setup code and no instructor
answer keys; widgets become a static figure plus a note. It downloads nothing and retrains nothing.
Wide figures sit on landscape A4 pages so their labels stay readable.

---

## 5. 起動 / Starting JupyterLab

```powershell
cd "$HOME\Documents\AI_Vision_Training"
.\.venv\Scripts\Activate.ps1
jupyter lab
```

ブラウザが開いたら、`notebooks` → `00_Setup` → `00_Environment_Setup.ipynb`
の順に開きます。**第 5 日のノートブックだけは、カーネルを
`Python 3 (AI Vision Anomalib)` に切り替えてください。**

Open `notebooks` -> `00_Setup` -> `00_Environment_Setup.ipynb`. For the **Day 5
notebooks only**, switch the kernel to `Python 3 (AI Vision Anomalib)`.

### 5.1 セルの指示 / Cell instructions

すべてのコードセルの先頭に、次のどれかが付きます。
Every code cell starts with one of these banners.

| 表示 / Banner | 意味 / Meaning |
|---|---|
| `実行のみ / Run only` | **Shift + Enter** でそのまま実行。書き換えない / run it, do not edit |
| `この値を変更 / Change this value` | 値を変えて、結果を予想してから実行 / change the value, predict, then run |
| `自分でコードを書く / Write your code` | 空欄を自分で埋める / fill in the blanks |

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

## 6. 検証とテスト / Validation and tests

```powershell
# 環境の確認 / check the environment
python assets\scripts\verify_environment.py --profile all

# ノートブックの構造検証（速い）/ structural validation (fast)
python assets\scripts\validate_notebooks.py

# 軽いノートブックを実際に実行して検証 / actually execute the lightweight notebooks
python assets\scripts\validate_notebooks.py --execute lightweight

# アセットとデータセットの自動テスト / automated asset and dataset tests
python -m pytest assets\tests -v

# 言語ラベルが残っていないか（CI 向け。書き換えません）
# check that no repetitive language label came back (read-only)
python assets\scripts\normalize_language_labels.py --check

# 指示バナーを付け直す（何度実行しても同じ結果 / idempotent）
# re-apply the cell instruction banners
python assets\scripts\scaffold_notebooks.py

# 対話デモが本当に「表示」されるか / check that the interactive demos really render
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

## 9. 困ったとき / When something goes wrong

まず次の順番で確認してください。

1. 各ノートブック末尾の「困ったときは / Troubleshooting」表
2. [`docs/troubleshooting/installation.md`](docs/troubleshooting/installation.md)
3. `python assets\scripts\verify_environment.py --profile all`

Check the troubleshooting table at the end of each notebook, then
`docs/troubleshooting/installation.md`, then run the environment verifier.

---

## 10. 既知の制限 / Known limitations

| 制限 / Limitation | 理由 / Reason |
|---|---|
| 合成画像のみ / synthetic data only | 実際の PVC 画像はまだ提供されていない / no real PVC images available yet |
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

## 11. ライセンスと出所 / Licensing and provenance

この研修で使う外部素材の出所とライセンスは
[`assets/external_samples/PROVENANCE.md`](assets/external_samples/PROVENANCE.md) に記録しています。

**重要 / Important:** 学習目的での利用は問題ありませんが、
**Ultralytics のモデルとコードは AGPL-3.0** です。製品への組み込みは、
ライセンスの確認なしに行わないでください。

Provenance and licences of external assets are recorded in
`assets/external_samples/PROVENANCE.md`. Educational use is fine, but **Ultralytics code and released
models are AGPL-3.0** — do not embed them in a product without a licence review.
