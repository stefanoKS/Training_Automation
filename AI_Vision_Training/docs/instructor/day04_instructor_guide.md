# 第4日 講師ガイド / Day 4 Instructor Guide

**YOLO モデルの準備と学習 / Preparing and training a YOLO model**

---

## 午前（08:00–09:00）／ Morning session

### 学習目標 / Learning goals

1. 教師あり学習に必要なもの（入力＋正解）を言える
2. YOLO ラベルの 5 つの数値を読める
3. 学習・検証・試験の役割と、分離する理由を説明できる
4. データ漏れがなぜ危険かを説明できる
5. epoch / batch / loss を説明できる

### 説明する概念 / Key concepts

| 概念 / Concept | 説明の要点 / Key message |
|---|---|
| 注釈 | 人間が作る正解。**質が AI の上限を決める** |
| 正規化座標 | 画像サイズで割った 0〜1 の値。サイズが変わっても使える |
| データ分割 | train で学び、val で選び、**test は最後に 1 回だけ** |
| データ漏れ | 同じ画像が train と test にあると **丸暗記** で高得点。現場では無意味 |
| epoch | 全学習画像を 1 周 |
| batch | 一度に処理する枚数。大きいほど重く、安定 |
| loss | 正解との差。下がれば学習が進んでいる |
| ファインチューニング | 学習済みモデルを自分のデータで追加学習 |

### 実演 / Demonstration（10 分程度）

1. `data.yaml` と `labels/train/train_0001.txt` を開いて見せる
2. ラベルを画像に描いた図（ノートブック 01 の点検セル）を見せる
3. **わざとデータ漏れを作り**、ハッシュ検査が検出することを見せる

Show `data.yaml`, one label file, the drawn labels, then deliberately copy a test image
into train and let the hash check catch it.

### よくある誤解 / Common beginner misunderstandings

| 誤解 / Misunderstanding | 実際 / Reality |
|---|---|
| 「画像が多ければ良い」 | **偏りが無いこと** のほうが大事 |
| 「学習データで 99 % なら優秀」 | 丸暗記の可能性。**試験データで測る** |
| 「ラベルは自動で付く」 | 人手。1 枚数十秒〜数分 |
| 「空のラベルは不要」 | 背景画像として **偽陽性を減らす** |
| 「エポックは多いほど良い」 | 過学習する。val の loss を見る |

### 受講者に投げかける質問 / Questions to ask

1. 「学習用と試験用に同じ画像が入っていたら、何が起きますか？」
2. 「なぜ背景（欠陥なし）の画像が必要なのですか？」
3. 「ラベルを間違えると、AI はどうなりますか？」

### 午前の課題説明 / Explaining the morning assignment

ノートブック 01 の全 Part と演習（座標の手計算・空ラベルの集計・データ漏れの検出）。

---

## 午後（12:50–13:50）／ Afternoon session

### 午前の振り返り / What to review

1. ラベルの 5 つの数値（言わせる）
2. train / val / test の役割
3. データ漏れの危険性

### 期待される結果 / Expected results

| ノートブック / Notebook | 午後終了時の到達 / By end of day |
|---|---|
| 01 Dataset Annotation | 全 Part、ラベルの点検、漏れ検査 |
| 02 Training | **学習が完走**し、`best.pt` と `results.csv` が生成される |
| 03 Evaluation | `split="test"` の評価、混同行列、失敗例、共通画像の JSON |

**学習時間はハードウェアで大きく変わります。** 「終了時間は保証できない」と
最初に明言してください。遅い受講者には `EPOCHS=5`、`IMGSZ=160` を案内します。

State up front that runtime depends on hardware and cannot be guaranteed. For slow
machines, use `EPOCHS=5` and `IMGSZ=160`.

参考実測（CPU）: precision 0.872 / recall 0.889 / mAP50 0.918 / mAP50-95 0.609。

Reference measurement on CPU: precision 0.872, recall 0.889, mAP50 0.918, mAP50-95 0.609.

### よくあるエラー / Common errors

| 症状 / Symptom | 原因 / Cause | 説明の仕方 / How to explain |
|---|---|---|
| 学習が始まらない | `RUN_TRAINING = False` | セルの値を確認させる |
| `Dataset not found` | `data.yaml` の `path` が古い | Part 2 の書き直しセルを再実行 |
| `FileNotFoundError: best.pt` | 学習未完了 | 学習を最後まで実行 |
| 損失が下がらない | ラベル誤り・画像とラベルの不一致 | 01 の点検に戻る |
| 評価が 0 になる | 試験ラベルが空・クラス数不一致 | `data.yaml` の `names` を確認 |

### 次に導入する概念 / Next concepts to introduce

第 5 日は「**正解ラベルが無い** 世界」に入ります。
今日「ラベルを作るのが大変だ」と感じたことが、異常検知が必要になる理由です。

Day 5 enters a world without labels. The pain of annotating today is exactly why
anomaly detection exists.

### 午後の課題説明 / Afternoon assignment briefing

1. ノートブック 02 の学習と Part 4（保存）
2. ノートブック 03 の全 Part（評価・混同行列・失敗例・改善提案）
3. 提出物：`best.pt`、`results.csv`、学習ログの要約、評価指標、失敗例の画像、改善提案

---

## 評価ルーブリック / Assessment rubric

| 観点 / Criterion | Level 0 | Level 1 | Level 2 | Level 3 |
|---|---|---|---|---|
| データセットの理解 | 未着手 | 構造を写すだけ | 形式を説明 | 自分で点検できる |
| 学習の実行 | 未実行 | 助けを借りて実行 | 一人で実行 | パラメータの影響を説明 |
| 学習ログの読解 | 未着手 | 数値を見るだけ | loss の意味を説明 | 学習の可否を判断できる |
| 評価の実行 | 未実行 | 実行のみ | `split="test"` を理解 | 指標を現場の言葉で説明 |
| 失敗の分析 | なし | 1 例挙げる | 原因を分類 | 改善の優先順位を提案 |
| データ漏れの理解 | なし | 用語のみ | 危険性を説明 | 自分で検出できる |

---

## 理解度チェックの解答例 / Model answers

**（受講者には渡さないでください / do not hand these to learners）**

### ノートブック 01

1. **入力（画像）と正解（注釈）**。教師あり学習はこのペアから学ぶ。
2. クラス番号、中心 x、中心 y、幅、高さ（すべて 0〜1 に正規化）。
3. val は学習中に設定を選ぶため、test は **最終評価のために取っておく**。
   test で調整すると、もう「未知のデータ」ではなくなる。
4. 漏れがあると **丸暗記** で成績が良くなる。実際のラインには同じ画像が流れてこないので、
   現場の性能は保証されない。
5. モデルが **「ここには何も無い」を学ぶ** ため。無いと、模様をすべて欠陥と判定しがち。

### ノートブック 02

1. **epoch** は全学習画像を 1 周すること、**batch** は一度に処理する枚数。
2. 予測が正解に近づいている（誤差が減っている）ということ。
3. ① 少ない画像で済む ② 学習が速く進む（形の見方を一から覚え直さなくてよい）。
4. `best.pt` は **検証データで最良だった時点**、`last.pt` は最後。**ふつう `best.pt`** を使う。
5. 学習データの数字は **丸暗記の度合い** を測っている。未知データの性能ではない。

### ノートブック 03

1. precision は **検出したもののうち本物の割合**、recall は **本物のうち捕まえた割合**。
2. 見逃しが増える → **不良品を出荷してしまう**。
3. **見逃し（偽陰性）が多い**。正解が異常なのに background と予測された数が多い。
4. **データを増やす（多様性を上げる）** のが最も効く。次に過学習を抑える（学習を止める、
   モデルを小さくする）。
5. `split="test"` は学習に使っていないデータ。`split="train"` は丸暗記の成績で、
   実力を示さない。