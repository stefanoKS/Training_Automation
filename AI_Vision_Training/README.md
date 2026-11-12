# 広島化成 第1週 AI・マシンビジョン研修 / Hiroshima Kasei Week 1 AI & Machine Vision Training

**日本語：** 化成品（Kaseihin）部門の方を対象とした、**5 日間・16 ノートブック**の
自習型 AI 研修教材です。Python も AI も画像処理も未経験の方を前提に作っています。

**English:** A five-day, **16-notebook** self-study AI course for the Kaseihin (化成品)
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

**日本語：** 次の順番で進めてください。

1. [`START_HERE.md`](START_HERE.md) — パソコンの電源を入れるところから始める、超初心者向け手順
2. [`COURSE_SYLLABUS.md`](COURSE_SYLLABUS.md) — 5 日間の時間割
3. `notebooks/00_Setup/00_Environment_Setup.ipynb` — 環境のセットアップと確認

**English:** Follow this order: `START_HERE.md` (from switching the PC on), then
`COURSE_SYLLABUS.md` (the five-day timetable), then the setup notebook.

---

## 2. この研修で身につくこと / What you will be able to do

**日本語：** 5 日間の終わりに、次のことができるようになります。

| 日 / Day | できるようになること / You will be able to |
|---|---|
| 1 | AI・機械学習・深層学習の違いを説明する。画像が数値の表であることを説明し、自分で書き換える。 / Explain AI vs ML vs DL; explain that an image is a table of numbers and modify one. |
| 2 | Python で判定プログラムを書く。OpenCV で画像を読み、2 値化し、ピクセルを mm に換算する。 / Write a judgement program; read and threshold an image; convert pixels to mm. |
| 3 | 学習済み YOLO を動かし、検出結果を読み、しきい値を変えて挙動を説明する。 / Run a pretrained YOLO, read its results, explain threshold effects. |
| 4 | データセットを点検し、YOLO をファインチューニングし、試験データで評価する。 / Inspect a dataset, fine-tune YOLO, evaluate on held-out data. |
| 5 | PatchCore で異常検知を実行し、YOLO と比較して、PVC 検査への推奨を作る。 / Run PatchCore anomaly detection, compare it with YOLO, and recommend an approach for PVC. |

---

## 3. インストール / Installation

**日本語：** 2 つの仮想環境を作ります。**理由を必ず読んでください。**

| 環境 / Environment | 使う日 / Used on | 主なパッケージ / Main packages |
|---|---|---|
| `.venv` | 第 0〜4 日 / Days 0-4 | numpy, matplotlib, opencv-python, torch, ultralytics |
| `.venv-anomalib` | 第 5 日 / Day 5 | anomalib 2.7.0, torch, opencv-**headless** |

> **なぜ分けるのか / Why two environments?**
>
> **日本語：** `anomalib` は `opencv-python-headless` を要求し、`ultralytics` は
> `opencv-python` を要求します。同じ環境に入れると `cv2` が二重になり、OpenCV が壊れます。
> これは公式ドキュメントの依存関係から確認できる、避けられない衝突です。
>
> **English:** `anomalib` requires `opencv-python-headless` while `ultralytics` requires
> `opencv-python`. Installing both into one environment gives two `cv2` distributions and breaks
> OpenCV. This is an unavoidable conflict visible in the official dependency metadata.

### 3.1 基本環境（第 0〜4 日）/ Base environment (Days 0-4)

```powershell
cd "$HOME\Documents\AI_Vision_Training"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements\base.txt
python -m pip install -r requirements\yolo.txt
python -m ipykernel install --user --name aivision --display-name "Python 3 (AI Vision)"
```

### 3.2 Anomalib 環境（第 5 日）/ Anomalib environment (Day 5)

```powershell
python -m venv .venv-anomalib
.\.venv-anomalib\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements\anomalib.txt
python -m ipykernel install --user --name aivision-anomalib --display-name "Python 3 (AI Vision Anomalib)"
```

**日本語：** GPU が無くても、この研修はすべて動きます。GPU がある場合の手順は
`requirements/yolo.txt` のコメントを見てください。
**English:** Everything works without a GPU. GPU instructions are in the comments of
`requirements/yolo.txt`.

**検証済みのバージョン / Verified versions:** [`requirements/tested_versions.md`](requirements/tested_versions.md)

---

## 4. 素材（データ）の生成 / Generating the assets

**日本語：** 画像・図・データセットはすべて **Python で生成** します。ダウンロード不要です。

**English:** All images, diagrams and datasets are **generated locally by Python**; nothing is
downloaded.

```powershell
# 図とサンプル画像 / diagrams and sample images
python assets\scripts\generate_training_assets.py

# YOLO 用データセットと PatchCore 用データセット / the two datasets
python assets\scripts\prepare_datasets.py
```

| 出力 / Output | 中身 / Contents |
|---|---|
| `assets/diagrams/` | 15 枚の概念図と校正用画像 / 15 concept diagrams plus a calibration image |
| `assets/normal_samples/`, `assets/defect_samples/` | 正常例・欠陥例（正解マスクと座標付き） / normal and defective examples with masks and coordinates |
| `assets/yolo_dataset/` | 96 枚（train 64 / val 16 / test 16）、ラベル、`data.yaml` |
| `assets/anomaly_dataset/pvc_sheet/` | 正常 44 枚、異常 40 枚、正解マスク / 44 normal, 40 abnormal, ground-truth masks |

> **重要 / Important**
>
> **日本語：** これらは **合成画像** です。実際の PVC の光学的な振る舞いを再現したものでは
> **ありません**。実際の工場画像での検証は第 2 週以降に行います。
> 合成データで得られた精度を、製品の検査精度として引用してはいけません。
>
> **English:** These are **synthetic images**. They do NOT reproduce the optical behaviour of the
> factory's PVC material. Real images are required for a meaningful feasibility check in Week 2.
> Never quote accuracy obtained on synthetic data as a product inspection accuracy.

---

## 5. 起動 / Starting JupyterLab

```powershell
cd "$HOME\Documents\AI_Vision_Training"
.\.venv\Scripts\Activate.ps1
jupyter lab
```

**日本語：** ブラウザが開いたら、`notebooks` → `00_Setup` → `00_Environment_Setup.ipynb`
の順に開きます。**第 5 日のノートブックだけは、カーネルを
`Python 3 (AI Vision Anomalib)` に切り替えてください。**

**English:** Open `notebooks` -> `00_Setup` -> `00_Environment_Setup.ipynb`. For the **Day 5
notebooks only**, switch the kernel to `Python 3 (AI Vision Anomalib)`.

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
```

`assets/scripts/validate_notebooks.py --execute all` は **モデルのダウンロード** と
**学習** を含むため、長時間かかります。
`--execute all` includes model downloads and training, so it takes a long time.

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
│   ├── normal_samples/           <- 正常例 / normal examples
│   ├── defect_samples/           <- 欠陥例 / defect examples
│   ├── yolo_dataset/             <- YOLO データセット / YOLO dataset
│   ├── anomaly_dataset/          <- PatchCore データセット / PatchCore dataset
│   ├── external_samples/         <- 外部由来素材と出所 / external assets and provenance
│   ├── scripts/                  <- 生成・検証スクリプト / generation and validation scripts
│   └── tests/                    <- pytest
├── docs/
│   ├── instructor/               <- 講師用ガイド（各日）/ instructor guides (per day)
│   ├── troubleshooting/          <- トラブル対処 / troubleshooting
│   └── reference_materials.md    <- 公式ドキュメントへのリンク / official links
├── submissions/                  <- 提出物（日別）/ submission folders (per day)
└── training_results/             <- 学習出力（Git 管理外）/ training outputs (git-ignored)
```

---

## 8. 提出物 / Submissions

**日本語：** 毎日、`submissions/day0N/` に次の 4 つを保存してください。

1. 実行済みのノートブック（`File` → `Save`）
2. `Day0N_Report_Template.md` を埋めたもの
3. 保存した画像・CSV・JSON
4. エラーが出た場合はそのメッセージと、試したこと

**English:** Each day, leave four things in `submissions/day0N/`: the executed notebook, the filled
report template, the saved images/CSVs/JSONs, and — if you hit an error — the message plus what you
tried.

**日本語：** 講師用の解答例は `docs/instructor/` にあります。**先に自分で書いてください。**
**English:** Model answers live in `docs/instructor/`. **Write your own answer first.**

---

## 9. 困ったとき / When something goes wrong

**日本語：** まず次の順番で確認してください。

1. 各ノートブック末尾の「困ったときは / Troubleshooting」表
2. [`docs/troubleshooting/installation.md`](docs/troubleshooting/installation.md)
3. `python assets\scripts\verify_environment.py --profile all`

**English:** Check the troubleshooting table at the end of each notebook, then
`docs/troubleshooting/installation.md`, then run the environment verifier.

---

## 10. 既知の制限 / Known limitations

**日本語：**

| 制限 / Limitation | 理由 / Reason |
|---|---|
| 合成画像のみ / synthetic data only | 実際の PVC 画像はまだ提供されていない / no real PVC images available yet |
| CPU 前提の小さな設定 / small CPU-oriented configuration | 研修 PC に GPU が無いことを前提 / assumes training PCs without a GPU |
| 学習画像 64 枚 / 64 training images | 1 日で終わる分量に抑えている / keeps the exercise within one day |
| PatchCore の評価データは半数 / half of the eval data | 検証と試験に分けるため / split into validation and test |
| YOLO と PatchCore は別環境 / two environments | OpenCV の衝突（上記 3 節）/ the OpenCV conflict described in section 3 |

**English:** Every limitation above is deliberate and documented; none of them is a workaround for a
failing component. Real production feasibility requires real images, a fixed camera and lighting
design, and a threshold study on known-good production — all of which are Week 2 topics.

---

## 11. ライセンスと出所 / Licensing and provenance

**日本語：** この研修で使う外部素材の出所とライセンスは
[`assets/external_samples/PROVENANCE.md`](assets/external_samples/PROVENANCE.md) に記録しています。

**重要 / Important:** 学習目的での利用は問題ありませんが、
**Ultralytics のモデルとコードは AGPL-3.0** です。製品への組み込みは、
ライセンスの確認なしに行わないでください。

**English:** Provenance and licences of external assets are recorded in
`assets/external_samples/PROVENANCE.md`. Educational use is fine, but **Ultralytics code and released
models are AGPL-3.0** — do not embed them in a product without a licence review.
