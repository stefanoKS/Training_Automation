# 研修シラバス / COURSE SYLLABUS

**広島化成 化成品部門 第1週 AI・マシンビジョン研修**
**Hiroshima Kasei, Kaseihin Department — Week 1 AI & Machine Vision Training**

**期間 / Period:** 2026 年 11 月 16 日（月）〜 11 月 20 日（金）
16–20 November 2026 · **作業時間 / Working hours:** 08:00–16:50

---

## 1. 毎日の時間割 / Daily timetable

**日本語：** すべての日が同じリズムで進みます。この形を覚えてください。

**English:** Every day follows the same rhythm.

| 時刻 / Time | 内容 / Activity | 誰が / Who |
|---|---|---|
| 08:00–09:00 | 講師による説明と実演 / Instructor explanation and demonstration | 講師 / instructor |
| 09:00–12:00 | **自習**：Jupyter ノートブックを進める / **Self-study** with the notebooks | 受講者 / learner |
| 12:00–12:50 | 昼休み / Lunch break | — |
| 12:50–13:50 | 講師による午前の振り返りと午後の説明 / Morning review and afternoon briefing | 講師 / instructor |
| 13:50–16:50 | **自習**：演習・課題・提出物 / **Self-study**: exercises, assignments, submission | 受講者 / learner |

**日本語：** 自習時間（合計 6 時間）は **講師が横にいません**。
だからノートブックには、自分だけで進められるだけの説明を入れてあります。

**English:** During the six hours of self-study the instructor is not available. The notebooks
therefore contain enough explanation to keep going without help.

**日本語：** つまずいたときの順番：① ノートブック末尾のトラブル表 → ②
`docs/troubleshooting/installation.md` → ③ `python assets\scripts\verify_environment.py --profile all`
→ ④ 講師に相談（12:50 以降、またはメモを残す）。

**English:** When stuck: (1) the troubleshooting table at the end of the notebook, (2)
`docs/troubleshooting/installation.md`, (3) the environment verifier, (4) the instructor.

---

## 2. 5 日間の流れ / The five days

### 第1日（11/16）AI の基礎 / Day 1 — AI fundamentals

**日本語：** プログラミングをほとんど書かず、**概念と画像の仕組み** を学びます。

| ノートブック / Notebook | 主な内容 / Content | 目安 / Time |
|---|---|---|
| `Day01_01_Introduction_to_AI.ipynb` | プログラム・自動化・AI・機械学習・深層学習、学習と推論、AI が間違える理由 | 90 分 |
| `Day01_02_Pixels_and_Images.ipynb` | 画素・解像度・RGB・グレースケール・NumPy 配列・座標・拡大縮小 | 90 分 |
| `Day01_03_Computer_Vision_Tasks.ipynb` | 分類・検出・セグメンテーション・異常検知の違いと製造応用 | 90 分 |

**English:** Almost no programming: **concepts and how images work**. Notebook 01 covers programs,
automation, AI/ML/DL, training versus inference and why AI fails. Notebook 02 covers pixels,
resolution, RGB, greyscale, NumPy arrays, coordinates and resizing. Notebook 03 compares
classification, detection, segmentation and anomaly detection.

**課題 / Assignment:** AI と画像認識の説明、画像を Python で加工した結果、
PVC 検査に使えそうな手法の提案。

---

### 第2日（11/17）Python と OpenCV / Day 2 — Python and OpenCV

| ノートブック / Notebook | 主な内容 / Content | 目安 / Time |
|---|---|---|
| `Day02_01_Python_Basics.ipynb` | `print`・変数・数値・文字列・計算・比較・真偽値・エラー | 90 分 |
| `Day02_02_Conditions_Loops_Functions.ipynb` | `if`/`elif`/`else`・`for`・リスト・関数・例外・テスト | 100 分 |
| `Day02_03_OpenCV_Image_Processing.ipynb` | 読み込み・表示・保存・グレー・2値化・輪郭・距離・px→mm | 120 分 |

**English:** Day 2 moves from the language itself to image processing: reading, displaying and
saving images, greyscale, thresholding, contours, the distance between two points and the
pixel-to-millimetre calibration.

**課題 / Assignment:** OK/NG 判定プログラム（5 つ以上の測定値）、OpenCV の処理結果、
ピクセル→mm の換算結果と誤差の考察。

---

### 第3日（11/18）YOLO の基礎 / Day 3 — YOLO basics

| ノートブック / Notebook | 主な内容 / Content | 目安 / Time |
|---|---|---|
| `Day03_01_YOLO_Concepts.ipynb` | YOLO・バウンディングボックス・クラス・confidence・IoU・事前学習 | 90 分 |
| `Day03_02_YOLO_Inference.ipynb` | モデル読み込み・推論・結果の取り出し・保存 | 100 分 |
| `Day03_03_YOLO_Experiments.ipynb` | しきい値・座標・偽陽性/偽陰性・解像度の影響 | 120 分 |

**English:** Day 3 uses a real pretrained model. Students see that a COCO model runs correctly but
**cannot** find PVC defects, which motivates Day 4.

**課題 / Assignment:** 推論結果、バウンディングボックスの可視化、しきい値実験の表、
失敗例の分析。

---

### 第4日（11/19）YOLO の学習 / Day 4 — Training YOLO

| ノートブック / Notebook | 主な内容 / Content | 目安 / Time |
|---|---|---|
| `Day04_01_YOLO_Dataset_Annotation.ipynb` | 教師あり学習・注釈・YOLO 形式・正規化座標・データ分割・データ漏れ | 100 分 |
| `Day04_02_YOLO_Training.ipynb` | epoch・batch・学習率・損失・ファインチューニング・学習実行・保存 | 150 分 |
| `Day04_03_YOLO_Evaluation.ipynb` | 試験データでの評価・precision/recall・混同行列・失敗例・改善 | 140 分 |

**English:** Day 4 is the heaviest day: the dataset is inspected, a nano YOLO model is fine-tuned on
the synthetic dataset, and evaluated on a held-out split.

**課題 / Assignment:** データセットの点検、学習結果、評価結果、成功例と失敗例、
次に改善する点。

---

### 第5日（11/20）PatchCore と比較 / Day 5 — PatchCore and comparison

| ノートブック / Notebook | 主な内容 / Content | 目安 / Time |
|---|---|---|
| `Day05_01_Anomaly_Detection_Concepts.ipynb` | 異常検知・正常/異常・パッチ・特徴・最近傍・異常スコア | 100 分 |
| `Day05_02_PatchCore_Training.ipynb` | Anomalib・データ構成・PatchCore・fit・推論・ヒートマップ | 150 分 |
| `Day05_03_YOLO_vs_PatchCore.ipynb` | 出力の違い・同じ画像での比較・しきい値・推奨の作成 | 140 分 |

**English:** Day 5 introduces learning from normal images only, trains a real PatchCore model and
then compares it with YOLO on a shared held-out set.

**課題 / Assignment:** PatchCore の学習結果、ヒートマップ、比較表、
PVC 検査への推薦（判断と理由）。

---

## 3. ノートブックの共通構成 / Structure of every notebook

**日本語：** 16 冊すべてが同じ構成です。迷ったら、この順番を思い出してください。

**English:** All 16 notebooks share one structure.

| 記号 / Section | 内容 / Content |
|---|---|
| ヘッダ / Header | 学習目標・所要時間・前提条件・必要なライブラリ・提出物 |
| 準備 / Preparation | 研修フォルダの検出・ライブラリ確認・日本語フォント設定 |
| 概念説明 / Concept | 日本語 → 英語の順で説明 |
| 実演 / Demonstration | 問題 → 考え方 → コード → 出力 → 意味 |
| 誘導実験 / Guided experiment | 数値を変えて結果を予想する |
| 演習 / Exercises | 基本・中級・発展の 3 つ |
| 理解度チェック / Questions | 3〜5 問 |
| トラブル / Troubleshooting | よくある失敗と対処 |
| 完了チェックリスト / Checklist | 終わったかの確認 |
| さらに学ぶ / Further learning | 任意の発展 |

---

## 4. 評価 / Assessment

**日本語：** 各日、4 段階で自己評価します。**目標はレベル 2 以上** です。

| レベル / Level | 状態 / State |
|---|---|
| 0 | 未完了 / not completed |
| 1 | 大きな助けがあって完了 / completed with significant assistance |
| 2 | 少しの助けで完了 / completed with minor assistance |
| 3 | 一人で完了し、結果を説明できる / completed independently and can explain the result |

**English:** Self-assess each day on this four-level scale. **Level 2 or above is the target.**

**日本語：** レベル 3 は「動いた」だけでは足りません。**「なぜそうなるか」を人に説明できる** ことが条件です。

**English:** Level 3 is not "it ran". It requires being able to **explain why**.

---

## 5. 第 2 週へのつながり / What Week 2 covers

**日本語：** 第 1 週は **基礎** です。実際の検査システムは第 2 週で扱います。

| 第 2 週の内容 / Week 2 content |
|---|
| PVC 固有の検査要件の整理 / the actual PVC inspection requirements |
| カメラ・レンズ・照明の選定（0.3 mm を写すには何画素必要か） / camera, lens and lighting selection |
| 撮影条件の設計と校正 / imaging setup and calibration |
| 実画像でのデータ収集と注釈 / collecting and annotating real images |
| システム構成と高速処理 / system integration and throughput |
| 検査プロトタイプの試作と評価 / building and evaluating the prototype |

**English:** Week 1 builds the foundation. Week 2 covers the real PVC requirements, camera and
lighting selection (how many pixels are needed for 0.3 mm), the imaging setup and its calibration,
real data collection, system integration and throughput, and finally the prototype.

**日本語：** 第 1 週で「合成データの精度は製品の精度ではない」と繰り返しているのは、
第 2 週で実データに向き合うためです。

**English:** Week 1 repeatedly states that synthetic accuracy is not product accuracy, precisely so
that Week 2 can confront real data honestly.
