# 第3日 講師ガイド / Day 3 Instructor Guide

**YOLO 物体検出の基礎 / YOLO object detection basics**

---

## 午前（08:00–09:00）／ Morning session

### 学習目標 / Learning goals

1. 物体検出の出力（四角・クラス・confidence）を説明できる
2. YOLO 形式の正規化座標を計算できる
3. IoU を手計算できる
4. 事前学習モデルが PVC 欠陥を検出できない理由を 4 つ言える

### 説明する概念 / Key concepts

| 概念 / Concept | 説明の要点 / Key message |
|---|---|
| バウンディングボックス | 2 点方式（x1,y1,x2,y2）と中心方式（xc,yc,w,h）。YOLO は **中心＋正規化** |
| クラス | 学習した種類だけ。**COCO の 80 クラスに欠陥は無い** |
| confidence | モデルの自己評価。**確率ではない。高い≠正しい** |
| IoU | 重なり ÷ 合計。0.5 以上を「当たり」とする慣習 |
| 事前学習 | 他のデータで学習済み。**ファインチューニングの出発点** |
| 重みファイル | `.pt`。学習で決まった数値の集まり |

### 実演 / Demonstration（10 分程度）

**日本語：** **必ず「うまくいかない例」を見せてください。**

1. `bus.jpg` に YOLO をかけ、バスと人が検出されることを見せる（**動く**）
2. 同じモデルを `defect_multi.png` にかけ、何も出ないことを見せる（**動かない**）
3. 「なぜ動かないか」を受講者に考えさせる
4. 4 つの理由（クラスが無い／見た目／大きさ／正解データが無い）を板書

**English:** Show both sides: the model works on `bus.jpg` and does nothing on the PVC-like image.
Let learners explain why before you list the four reasons.

### よくある誤解 / Common beginner misunderstandings

| 誤解 / Misunderstanding | 実際 / Reality |
|---|---|
| 「AI は何でも見つける」 | 学習したクラスだけ |
| 「confidence が高い＝正しい」 | 自己評価にすぎない。堂々と間違える |
| 「IoU 1.0 でないと失敗」 | 0.5 以上を当たりとするのが一般的 |
| 「モデルを入れれば検査できる」 | **データと学習が無ければ何もできない** |
| 「正規化座標は 0〜255」 | **0〜1**。割り忘れると 1 を超える |

### 受講者に投げかける質問 / Questions to ask

1. 「confidence 0.9 の検出でも間違うことがあるのはなぜですか？」
2. 「IoU 0.3 の検出は、現場で使えますか？」
3. 「もし 80 クラスに `scratch` を足せるとしたら、何が必要ですか？」

### 午前の課題説明 / Explaining the morning assignment

ノートブック 01 の全 Part と演習 1〜3（座標計算・IoU の手計算）。

---

## 午後（12:50–13:50）／ Afternoon session

### 午前の振り返り / What to review

1. YOLO 形式の 5 つの数値の意味（言わせる）
2. IoU の式と 0.5 の慣習
3. 事前学習モデルで PVC 欠陥が検出できない 4 つの理由

### 期待される結果 / Expected results

| ノートブック / Notebook | 午後終了時の到達 / By end of day |
|---|---|
| 01 Concepts | 全 Part、IoU の手計算一致 |
| 02 Inference | モデル取得、注釈画像と CSV の保存 |
| 03 Experiments | しきい値の表、座標の読み取り、失敗例 1 件 |

**日本語：** **02 の最初の実行だけは講師が見届けてください。** モデルのダウンロードで
つまずく受講者が必ず出ます（`assets/models/` に置く手順を案内）。

**English:** Supervise the first run of Notebook 02. Some learners will hit the model download;
walk them through placing `yolo26n.pt` in `assets/models/`.

### よくあるエラー / Common errors

| 症状 / Symptom | 原因 / Cause | 説明の仕方 / How to explain |
|---|---|---|
| `URLError` / `TimeoutError` | ダウンロード失敗 | 再実行 → 手動取得 → 情報システムへ |
| 色が反転して表示される | `plot()` は BGR | `cvtColor(..., COLOR_BGR2RGB)` |
| `ModuleNotFoundError: ultralytics` | カーネル違い | 右上のカーネル名を確認 |
| 検出数 0 | `conf` が高すぎる／画像に物体が無い | `conf=0.05` で試す |
| 動作が遅い | CPU 実行 | 正常。`imgsz=320` で速くなる |

### 次に導入する概念 / Next concepts to introduce

**日本語：** 第 4 日は「**このモデルに、自分たちの欠陥を覚えさせる**」話です。
今日見た「検出できない理由」が、そのまま第 4 日の作業項目になります。

**English:** Day 4 teaches the model your own defects. Today's four reasons become tomorrow's
checklist.

### 午後の課題説明 / Afternoon assignment briefing

1. ノートブック 02 の全 Part（推論・結果の取り出し・保存）
2. ノートブック 03 の Part 1〜Part 4（しきい値・座標・失敗例）
3. 提出物：推論結果の画像、検出結果の CSV、しきい値の表、失敗例の記録

---

## 評価ルーブリック / Assessment rubric

| 観点 / Criterion | Level 0 | Level 1 | Level 2 | Level 3 |
|---|---|---|---|---|
| 検出の出力の理解 | 未着手 | 用語のみ | 3 要素を説明 | 現場での意味まで説明 |
| 座標変換 | 未着手 | 写しのみ | 計算できる | 逆変換もできる |
| IoU | 未着手 | 式の暗記 | 手計算できる | 0.5 の意味を説明 |
| 推論の実行 | 未実行 | 助けを借りて実行 | 一人で実行・保存 | パラメータの影響を説明 |
| 失敗の分析 | なし | 1 つ挙げる | 原因を推測 | 改善案まで提案 |
| PVC への理解 | なし | 「無理」だけ | 理由を 2 つ | 理由 4 つと対策 |

---

## 理解度チェックの解答例 / Model answers

**（受講者には渡さないでください / do not hand these to learners）**

### ノートブック 01

1. **バウンディングボックス（位置）、クラス（種類）、confidence（確からしさ）**。
2. **必ずしも正しくない。** confidence はモデルの自己評価で、見た目に騙されることがある。
3. 予測と正解の重なりが **約 30 %** しかない。半分も合っていない。
4. 例：① COCO に欠陥クラスが無い ② 見た目・大きさが学習した物体と違いすぎる
   ③ 正解データで学習していない。
5. **学習は遅くデータが必要。推論は速く 1 枚で足りる。**

### ノートブック 02

1. **結果のリスト**。1 枚なら `results[0]`。
2. **検出数が増える。** その代わり **偽陽性（誤検出）が増える**。
3. `box.cls` を `int()` にし、`result.names[その番号]` で名前を引く。
4. ① 同じセルを再実行 ② releases から手動取得して `assets/models/` に置く ③ 情報システムに相談。
5. **利点**：ネットワーク不要・再現できる・出所が明確。**注意**：PVC の欠陥ではないこと、
   AGPL-3.0 であること、COCO のクラスしか出ないこと。

### ノートブック 03

1. **正しい検出も confidence 0.88 程度で、0.9 未満に集まる** から。しきい値を 0.9 にすると
   バスまで消える。
2. **偽陰性**＝本当の欠陥を見逃すこと。**偽陽性**＝正常品を不良と判定すること。
3. confidence は「学習した見た目にどれくらい似ているか」であり、**正解かどうかとは別**。
4. ① 物体が数ピクセルになり、形が分からなくなる ② 入力が縮小され、細部が失われる。
5. 意見が分かれる。**見逃しを先に減らす**のが原則だが、誤報が多すぎると現場が検査を
   信用しなくなり、結局見逃しが増える。**両方を測りながら決める** のが正解。