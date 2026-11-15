# 研修シラバス / COURSE SYLLABUS

**広島化成 化成品部門 第1週 AI・マシンビジョン研修**
**Hiroshima Kasei, Kaseihin Department — Week 1 AI & Machine Vision Training**

**期間 / Period:** 2026 年 11 月 16 日（月）〜 11 月 20 日（金）
16–20 November 2026 · **作業時間 / Working hours:** 08:00–16:50

このファイルは **時間割の唯一の正** です。各ノートブックは「この日の何冊目か」だけを示し、
1 日の時間割を自分で持つことはありません。

This file is the **single source of truth for the timetable**. Each notebook only states its
position in the day; no notebook keeps its own copy of the full-day schedule.

---

## 1. 1 日のリズム / The daily rhythm

| 時刻 / Time | 分 / min | 内容 / Activity | 誰が / Who |
|---|---|---|---|
| 08:00–09:00 | 60 | 講師による説明と実演 / Instructor explanation and demonstration | 講師 / instructor |
| 09:00–12:00 | 180 | **自習 1**（下の時間割を参照）/ **Self-study block 1** (see the timetable below) | 受講者 / learner |
| 12:00–12:50 | 50 | 昼休み / Lunch break | — |
| 12:50–13:50 | 60 | 午前の振り返りと午後の説明 / Morning review and afternoon briefing | 講師 / instructor |
| 13:50–16:50 | 180 | **自習 2**（下の時間割を参照）/ **Self-study block 2** (see the timetable below) | 受講者 / learner |

固定の時間です。動かしません。
These times are fixed and are not moved.

自習は 1 日 **360 分**（180 + 180）です。その 360 分を次のように配分します。
Self-study gives **360 minutes** per day (180 + 180). Those 360 minutes are budgeted like this.

| 区分 / Bucket | 目安 / Budget | 内容 / What it is for |
|---|---|---|
| 必須の学習・演習 / required lesson and exercise work | **270〜300 分** | 時間割の `必須` 行の合計 / the sum of the `必須` rows |
| 休憩・トラブル対応・提出 / breaks, troubleshooting, submission | **60〜90 分** | 時間割の `休憩` `予備` `提出` 行の合計 / the sum of the `休憩` `予備` `提出` rows |

必須と予備の合計は必ず 360 分になります。1 日の表を書き換えたら、合計が 360 分であることを
確認してください（`python -m pytest assets/tests/test_schedule.py` が自動で確認します）。

The required and buffer rows must always add up to 360 minutes. After editing a day, re-check the
total — `python -m pytest assets/tests/test_schedule.py` does this automatically.

### 時間割の記号 / Reading the timetable

| 種別 / Type | 意味 / Meaning |
|---|---|
| `必須` / required | 全員が行う。完了チェックリストの対象 / everyone does it; part of the completion checklist |
| `任意` / optional | 時間が余ったときだけ。チェックリストの対象外 / only with spare time; never in the checklist |
| `休憩` / break | 画面から離れる / step away from the screen |
| `予備` / buffer | 遅れの取り戻し、トラブル対応、回復手順 / catching up, troubleshooting, recovery |
| `提出` / submission | 提出物の作成と保存 / writing and saving the deliverables |

> 所要時間は **暫定値** です。初学者 1 名とのパイロットで測るまで確定しません。
>
> All durations are **provisional** until measured in a pilot with one beginner.

---

## 2. 研修前の準備（第1日より前）/ Preflight, before Day 1

準備は授業時間の外で終わらせます。**授業時間に準備時間を隠していません。**
Preflight happens outside the lesson hours. Setup time is **not** hidden inside the lesson budget.

番号付きの正式手順は [START_HERE.md](START_HERE.md) です。Python 3.11、両環境、
素材生成、写真・重みの事前取得、両環境の検査を第1日前に完了します。下表は時間の見積もりです。

Follow the authoritative numbered sequence in [START_HERE.md](START_HERE.md): Python 3.11,
both environments, generated assets, preloaded photos/weights, and verification in both environments
before Day 1. The table below estimates time; it is not a second installation sequence.

| # | やること / Task | 目安 / Time | 確認方法 / How to check |
|---|---|---|---|
| 1 | 受講者用フォルダを決める / choose the learner folder | 5 分 | — |
| 2 | Python 環境を作る / create the Python environment | 20 分 | `python assets\scripts\verify_environment.py --profile base` |
| 3 | Jupyter のカーネルを 2 つ登録する / register both kernels | 10 分 | `jupyter kernelspec list` に `aivision` と `aivision-anomalib` |
| 4 | データセットを作る / build the datasets | 10 分 | `python assets\scripts\prepare_datasets.py` |
| 5 | 写真・モデルの重みを取得する / preload photos and weights | 10 分 | `START_HERE.md` ステップ7のオフライン検査 / Step 7 offline checks |
| 6 | `00_Environment_Setup.ipynb` を通す / run the setup notebook | 60 分 | Part 7 のレポートが `submissions/day00/` に保存される |
| 7 | 第1日の準備確認 / Day 1 readiness check | 10 分 | 下の表の 4 項目すべてにチェック |

`00_Environment_Setup.ipynb` は **準備用** のノートブックです。5 日間の 360 分には含めません。
`00_Environment_Setup.ipynb` is a **preparatory** notebook and is not part of any day's 360 minutes.

### 第1日の準備確認 / Day 1 readiness check

| チェック / Check | 合格の条件 / Passes when |
|---|---|
| カーネル / kernels | 「Python 3 (AI Vision)」と「Python 3 (AI Vision Anomalib)」の両方が一覧に出る |
| ライブラリ / libraries | 両環境で `verify_environment.py --profile all` が 0、素材の不足なし / exit 0 in both environments, no missing assets |
| 画像 / images | `Day01_02` の Part 1 が画像を 1 枚表示できる |
| フォント / font | 図のタイトルに `□` が出ない |

### 準備が終わらなかった場合 / If preflight is not finished

ごまかさずに、次のどれかを選びます。**準備を授業時間に持ち込むと、その日の必須学習が入りません。**
Do not pretend: pick one of these. **Carrying setup into lesson time means the required work no
longer fits.**

| 状況 / Situation | 対応 / Plan |
|---|---|
| 環境が 1 台も動かない / no environment works | 講師の PC で環境を見せ、受講者は紙の観察記録と予想に集中する。実行が要る必須部分は翌朝 08:00–09:00 に回収する。 |
| 一部の受講者だけ動く / some machines work | 動く人と 2 人 1 組にする。動かない人は「予想 → 隣の人の結果を見る → 一文で説明」を行う。 |
| モデルのダウンロードだけ失敗 / only the model download fails | 第3日以降は `assets/reference_outputs/` の **参考結果** を使って読み進める。受講者の実行結果（`submissions/`）と区別する。 |

参考結果は「実際に測った結果」ではありません。数字を自分の結果として提出してはいけません。
Reference results are **not** measurements taken on your machine. Never submit them as your own.

---

<a id="day1"></a>
## 3. 第1日（11/16）AI の基礎 / Day 1 — AI fundamentals

**必須 300 分 / 予備 60 分**（休憩 30 分、回復 30 分）
**required 300 min / buffer 60 min** (30 min breaks, 30 min recovery)

### 午前の自習 / Morning self-study（09:00–12:00）

| 時刻 / Time | 分 / min | 種別 / Type | 内容 / Content |
|---|---|---|---|
| 09:00–09:10 | 10 | 必須 | 第1日の準備確認 / Day 1 readiness check |
| 09:10–09:50 | 40 | 必須 | `Day01_01` Part 0–2 |
| 09:50–10:30 | 40 | 必須 | `Day01_01` Part 3–4 |
| 10:30–10:45 | 15 | 休憩 | 休憩 / break |
| 10:45–11:20 | 35 | 必須 | `Day01_01` Part 5–6 + 演習 1 |
| 11:20–12:00 | 40 | 必須 | `Day01_02` Part 0–2 |

### 午後の自習 / Afternoon self-study（13:50–16:50）

| 時刻 / Time | 分 / min | 種別 / Type | 内容 / Content |
|---|---|---|---|
| 13:50–14:30 | 40 | 必須 | `Day01_02` Part 3–5 |
| 14:30–15:00 | 30 | 必須 | `Day01_02` Part 6–7 + 演習 |
| 15:00–15:15 | 15 | 休憩 | 休憩 / break |
| 15:15–15:50 | 35 | 必須 | `Day01_03` Part 0–3 |
| 15:50–16:20 | 30 | 必須 | `Day01_03` Part 4–6 + 演習 |
| 16:20–16:50 | 30 | 提出 | 理解度チェック・提出物・回復 / questions, submission, recovery |

**この日のノートブック / Notebooks today**

| 順番 / # | ノートブック / Notebook | 所要 / Duration | 前提 / Prerequisites |
|---|---|---|---|
| 1 | `Day01_01_Introduction_to_AI.ipynb` | 115 分 | `00_Environment_Setup.ipynb` |
| 2 | `Day01_02_Pixels_and_Images.ipynb` | 110 分 | `Day01_01` |
| 3 | `Day01_03_Computer_Vision_Tasks.ipynb` | 65 分 | `Day01_02` |

**任意 / Optional:** `Day01_01` の「さらに学ぶ」にある明るさ以外の特徴（色・面積）の実験。
**任意 / Optional:** the colour and area experiments under "さらに学ぶ" in `Day01_01`.

**課題 / Assignment:** AI と画像認識の説明、画像を Python で加工した結果、
PVC 検査に使えそうな手法の提案。
Explain AI and image recognition, show one image you modified in Python, and propose a method that
could work for PVC inspection.

---

<a id="day2"></a>
## 4. 第2日（11/17）Python と OpenCV / Day 2 — Python and OpenCV

**必須 300 分 / 予備 60 分**（休憩 30 分、回復 30 分）
**required 300 min / buffer 60 min** (30 min breaks, 30 min recovery)

### 午前の自習 / Morning self-study（09:00–12:00）

| 時刻 / Time | 分 / min | 種別 / Type | 内容 / Content |
|---|---|---|---|
| 09:00–09:10 | 10 | 必須 | `Day02_01` Part 1（前日の復習）/ recap of Day 1 |
| 09:10–09:50 | 40 | 必須 | `Day02_01` Part 2–3 |
| 09:50–10:30 | 40 | 必須 | `Day02_01` Part 4–5 |
| 10:30–10:45 | 15 | 休憩 | 休憩 / break |
| 10:45–11:20 | 35 | 必須 | `Day02_01` Part 6 + 演習 |
| 11:20–12:00 | 40 | 必須 | `Day02_02` Part 0–2 |

### 午後の自習 / Afternoon self-study（13:50–16:50）

| 時刻 / Time | 分 / min | 種別 / Type | 内容 / Content |
|---|---|---|---|
| 13:50–14:35 | 45 | 必須 | `Day02_02` Part 3–4（**関数を初めて書く** / first function） |
| 14:35–15:05 | 30 | 必須 | `Day02_02` Part 5–6 + 演習 |
| 15:05–15:20 | 15 | 休憩 | 休憩 / break |
| 15:20–16:00 | 40 | 必須 | `Day02_03` Part 0–2 |
| 16:00–16:20 | 20 | 必須 | `Day02_03` Part 3–5 |
| 16:20–16:50 | 30 | 提出 | 理解度チェック・提出物・回復 / questions, submission, recovery |

**この日のノートブック / Notebooks today**

| 順番 / # | ノートブック / Notebook | 所要 / Duration | 前提 / Prerequisites |
|---|---|---|---|
| 1 | `Day02_01_Python_Basics.ipynb` | 125 分 | 第1日 / Day 1 |
| 2 | `Day02_02_Conditions_Loops_Functions.ipynb` | 115 分 | `Day02_01` |
| 3 | `Day02_03_OpenCV_Image_Processing.ipynb` | 60 分 | `Day02_02` |

**任意 / Optional:** `Day02_03` の「さらに学ぶ」にあるモルフォロジー処理。
**任意 / Optional:** the morphology experiment under "さらに学ぶ" in `Day02_03`.

**課題 / Assignment:** OK/NG 判定プログラム（5 つ以上の測定値）、OpenCV の処理結果、
ピクセル→mm の換算結果と誤差の考察。
An OK/NG judgement program over at least five measurements, the OpenCV processing results, and the
pixel-to-mm conversion with its error.

---

<a id="day3"></a>
## 5. 第3日（11/18）YOLO の基礎 / Day 3 — YOLO basics

**必須 275 分 / 予備 85 分**（休憩 30 分、回復 30 分、提出 25 分）
**required 275 min / buffer 85 min** (30 min breaks, 30 min recovery, 25 min submission)

### 午前の自習 / Morning self-study（09:00–12:00）

| 時刻 / Time | 分 / min | 種別 / Type | 内容 / Content |
|---|---|---|---|
| 09:00–09:40 | 40 | 必須 | `Day03_01` Part 0–2 |
| 09:40–10:20 | 40 | 必須 | `Day03_01` Part 3–4 + 演習 |
| 10:20–10:35 | 15 | 休憩 | 休憩 / break |
| 10:35–11:20 | 45 | 必須 | `Day03_02` Part 0–3（モデル読み込みを含む / includes loading the model） |
| 11:20–12:00 | 40 | 必須 | `Day03_02` Part 4–5 + 演習 |

### 午後の自習 / Afternoon self-study（13:50–16:50）

| 時刻 / Time | 分 / min | 種別 / Type | 内容 / Content |
|---|---|---|---|
| 13:50–14:30 | 40 | 必須 | `Day03_03` Part 0–2 |
| 14:30–15:10 | 40 | 必須 | `Day03_03` Part 3–4 |
| 15:10–15:25 | 15 | 休憩 | 休憩 / break |
| 15:25–15:55 | 30 | 必須 | `Day03_03` Part 5 + 演習 |
| 15:55–16:25 | 30 | 予備 | ダウンロード失敗・遅い PC の回復 / recovery for download or slow-machine problems |
| 16:25–16:50 | 25 | 提出 | 提出物 / submission |

**この日のノートブック / Notebooks today**

| 順番 / # | ノートブック / Notebook | 所要 / Duration | 前提 / Prerequisites |
|---|---|---|---|
| 1 | `Day03_01_YOLO_Concepts.ipynb` | 80 分 | 第2日 / Day 2 |
| 2 | `Day03_02_YOLO_Inference.ipynb` | 85 分 | `Day03_01`、`yolo11n.pt` のダウンロード完了 |
| 3 | `Day03_03_YOLO_Experiments.ipynb` | 110 分 | `Day03_02` |

**任意 / Optional:** `Day03_03` の「さらに学ぶ」にある `imgsz` を 1280 より大きくする実験。
**任意 / Optional:** the experiment above `imgsz=1280` under "さらに学ぶ" in `Day03_03`.

**課題 / Assignment:** 推論結果、バウンディングボックスの可視化、しきい値実験の表、
失敗例の分析。
Inference results, the rendered bounding boxes, the threshold experiment table and an analysis of
one failure.

---

<a id="day4"></a>
## 6. 第4日（11/19）YOLO の学習 / Day 4 — Training YOLO

**必須 290 分 / 予備 70 分**（休憩 35 分、提出 35 分）
**required 290 min / buffer 70 min** (35 min breaks, 35 min submission)

学習は CPU で数分かかります。待ち時間は 11:15–12:00 の枠に入れてあり、その間も手は止めません。
Training takes several minutes on CPU. The waiting time sits inside the 11:15–12:00 slot, and the
learner keeps working during it.

### 午前の自習 / Morning self-study（09:00–12:00）

| 時刻 / Time | 分 / min | 種別 / Type | 内容 / Content |
|---|---|---|---|
| 09:00–09:40 | 40 | 必須 | `Day04_01` Part 0–2 |
| 09:40–10:20 | 40 | 必須 | `Day04_01` Part 3–5 + 演習 |
| 10:20–10:35 | 15 | 休憩 | 休憩 / break |
| 10:35–11:15 | 40 | 必須 | `Day04_02` Part 0–2 |
| 11:15–12:00 | 45 | 必須 | `Day04_02` Part 3（学習を開始し、待つ間に Part 4 を読む / start training, read Part 4 while it runs） |

### 午後の自習 / Afternoon self-study（13:50–16:50）

| 時刻 / Time | 分 / min | 種別 / Type | 内容 / Content |
|---|---|---|---|
| 13:50–14:20 | 30 | 必須 | `Day04_02` Part 4 + 演習 |
| 14:20–14:55 | 35 | 必須 | `Day04_03` Part 0–2 |
| 14:55–15:15 | 20 | 休憩 | 休憩 / break |
| 15:15–15:50 | 35 | 必須 | `Day04_03` Part 3–4 |
| 15:50–16:15 | 25 | 必須 | `Day04_03` Part 5 + 演習 |
| 16:15–16:50 | 35 | 提出 | 提出物 / submission |

**この日のノートブック / Notebooks today**

| 順番 / # | ノートブック / Notebook | 所要 / Duration | 前提 / Prerequisites |
|---|---|---|---|
| 1 | `Day04_01_YOLO_Dataset_Annotation.ipynb` | 80 分 | 第3日 / Day 3 |
| 2 | `Day04_02_YOLO_Training.ipynb` | 115 分 | `Day04_01`、`assets/yolo_dataset` 生成済み |
| 3 | `Day04_03_YOLO_Evaluation.ipynb` | 95 分 | `Day04_02` の学習済みモデル |

**任意 / Optional:** `Day04_02` の「さらに学ぶ」にある `epochs` を 20 に増やす実験。
**任意 / Optional:** the `epochs=20` experiment under "さらに学ぶ" in `Day04_02`.

**課題 / Assignment:** データセットの点検、学習結果、評価結果、成功例と失敗例、
次に改善する点。
The dataset check, the training result, the evaluation, one success and one failure, and the next
improvement.

---

<a id="day5"></a>
## 7. 第5日（11/20）PatchCore と比較 / Day 5 — PatchCore and comparison

**必須 300 分 / 予備 60 分**（休憩 35 分、提出 25 分）
**required 300 min / buffer 60 min** (35 min breaks, 25 min submission)

PatchCore の `fit` は CPU で数分かかります。11:10–12:00 の枠に待ち時間を含めています。
PatchCore's `fit` takes several minutes on CPU; the 11:10–12:00 slot includes that wait.

### 午前の自習 / Morning self-study（09:00–12:00）

| 時刻 / Time | 分 / min | 種別 / Type | 内容 / Content |
|---|---|---|---|
| 09:00–09:35 | 35 | 必須 | `Day05_01` Part 0–2 |
| 09:35–10:10 | 35 | 必須 | `Day05_01` Part 3–5 + 演習 |
| 10:10–10:30 | 20 | 休憩 | 休憩 / break |
| 10:30–11:10 | 40 | 必須 | `Day05_02` Part 0–2 |
| 11:10–12:00 | 50 | 必須 | `Day05_02` Part 3–4（fit と評価 / fit and evaluation） |

### 午後の自習 / Afternoon self-study（13:50–16:50）

| 時刻 / Time | 分 / min | 種別 / Type | 内容 / Content |
|---|---|---|---|
| 13:50–14:30 | 40 | 必須 | `Day05_02` Part 5 + 演習 |
| 14:30–15:15 | 45 | 必須 | `Day05_03` Part 0–3 |
| 15:15–15:30 | 15 | 休憩 | 休憩 / break |
| 15:30–16:00 | 30 | 必須 | `Day05_03` Part 4–5 + 演習 |
| 16:00–16:25 | 25 | 必須 | 5 日間の振り返り（講師のまとめ / instructor wrap-up） |
| 16:25–16:50 | 25 | 提出 | 提出物 / submission |

**この日のノートブック / Notebooks today**

| 順番 / # | ノートブック / Notebook | 所要 / Duration | 前提 / Prerequisites |
|---|---|---|---|
| 1 | `Day05_01_Anomaly_Detection_Concepts.ipynb` | 70 分 | 第4日 / Day 4 |
| 2 | `Day05_02_PatchCore_Training.ipynb` | 130 分 | `Day05_01`、`aivision-anomalib` カーネル |
| 3 | `Day05_03_YOLO_vs_PatchCore.ipynb` | 100 分 | `Day04_03` と `Day05_02` の保存済み結果 |

**任意 / Optional:** `Day05_03` の「さらに学ぶ」にある、検証データでしきい値を 3 通り試す作業。
**任意 / Optional:** the three-way validation threshold sweep under "さらに学ぶ" in `Day05_03`.

**課題 / Assignment:** PatchCore の学習結果、ヒートマップ、比較表、
PVC 検査への推薦（判断と理由）。
The PatchCore result, the heatmaps, the comparison table and a recommendation for PVC with reasons.

---

## 8. ノートブックの共通構成 / Structure of every notebook

16 冊すべてが同じ構成です。迷ったら、この順番を思い出してください。
All 16 notebooks share one structure.

| 記号 / Section | 内容 / Content |
|---|---|
| ヘッダ / Header | 学習目標・所要時間・前提条件・この日の順番・提出物 |
| 準備 / Preparation | 研修フォルダの検出・ライブラリ確認・日本語フォント設定（まとめて実行 / run as a block） |
| 概念説明 / Concept | 日本語 → 英語の順で説明。**最初に図** を見せる / Japanese then English, visual first |
| 実演 / Demonstration | 例を見る → 1 つ変えて予想する → 実行する → 比べる → 一文で説明する → コードを読む |
| 誘導実験 / Guided experiment | 数値を変えて結果を予想する（任意の対話スライダーを含む） |
| 演習 / Exercises | 基本（必須）・中級（必須）・発展（任意） |
| 理解度チェック / Questions | 3〜5 問 |
| トラブル / Troubleshooting | よくある失敗と対処、回復手順 |
| 完了チェックリスト / Checklist | **必須** の項目だけ。任意の課題はチェックリストに入れない |
| さらに学ぶ / Further learning | 任意の発展 / optional only |

### セルの指示 / Cell instructions

コードセルの先頭に、必ず次のどれかが付きます。
Every code cell starts with one of these three banners.

| 表示 / Banner | 意味 / Meaning |
|---|---|
| `実行のみ / Run only` | 選んで **Shift + Enter**。書き換えない / just run it, do not edit |
| `この値を変更 / Change this value` | 値を変えて、結果の変化を予想してから実行する / change the value, predict, then run |
| `自分でコードを書く / Write your code` | 空欄を自分で埋める / fill in the blanks yourself |

**上級準備 / advanced preparation:** Part 0 のセルは、フォルダ検出・フォント設定・表示用の
関数だけです。中身を理解する必要はありません。まとめて実行してください。
The Part 0 cells only locate the folder, configure the Japanese font and define display helpers. You
do not need to understand them; run them as one block.

---

## 9. 評価 / Assessment

各日、4 段階で自己評価します。**目標はレベル 2 以上** です。
Self-assess each day on this four-level scale. **Level 2 or above is the target.**

| レベル / Level | 状態 / State |
|---|---|
| 0 | 未完了 / not completed |
| 1 | 大きな助けがあれば完了 / completed with substantial help |
| 2 | 少しの助けで完了 / completed with minor assistance |
| 3 | 一人で完了し、結果を説明できる / completed independently and can explain the result |

レベル 3 は「動いた」だけでは足りません。**「なぜそうなるか」を人に説明できる** ことが条件です。
Level 3 is not "it ran". It requires being able to **explain why**.

評価は **必須** の項目だけで行います。任意の発展課題が未実施でも減点しません。
Assessment uses **required** items only. An unfinished optional extension is not penalised.

---

## 10. 第 2 週へのつながり / What Week 2 covers

第 1 週は **基礎** です。実際の検査システムは第 2 週で扱います。
Week 1 is the **foundation**; the real inspection system is covered in Week 2.

| 第 2 週の内容 / Week 2 content |
|---|
| PVC 固有の検査要件の整理 / the actual PVC inspection requirements |
| カメラ・レンズ・照明の選定（0.3 mm を写すには何画素必要か） / camera, lens and lighting selection |
| 撮影条件の設計と校正 / imaging setup and calibration |
| 実画像でのデータ収集と注釈 / collecting and annotating real images |
| システム構成と高速処理 / system integration and throughput |
| 検査プロトタイプの試作と評価 / building and evaluating the prototype |

第 1 週で「合成データの精度は製品の精度ではない」と繰り返しているのは、
第 2 週で実データに向き合うためです。
Week 1 repeatedly states that synthetic accuracy is not product accuracy, precisely so that Week 2
can confront real data honestly.
