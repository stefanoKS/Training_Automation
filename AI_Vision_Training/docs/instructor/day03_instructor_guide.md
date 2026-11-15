# 第3日 講師ガイド / Day 3 Instructor Guide

**YOLO 物体検出の基礎 / YOLO object detection basics**

---

## 午前（08:00–09:00）／ Morning session

### 学習目標 / Learning goals

1. 物体検出の出力（四角・クラス・confidence）を説明できる
2. YOLO 形式の正規化座標を計算できる
3. IoU を手計算できる
4. 事前学習モデルが塩ビ欠陥を検出できない理由を 4 つ言える

### 説明する概念 / Key concepts

| 概念 / Concept | 説明の要点 / Key message |
|---|---|
| バウンディングボックス | `xyxy`（Ultralytics の boxes）・`xywh`（`cv2.boundingRect`）・`xc,yc,w,h` の正規化（YOLO のラベル）を区別する。正規化座標は**画像全体のリサイズ**には強いが、crop と letterbox では基準が変わる |
| クラス | 学習した種類だけ。**COCO の 80 クラスに欠陥は無い** |
| confidence | モデルが出したスコア。**正しい確率ではない。0.50 も五分五分ではない。高い≠正しい** |
| IoU | 重なりの面積 ÷ 2 つの枠を合わせた領域の面積（重なりは 1 回だけ数える）。0.5 以上を「当たり」とする慣習 |
| 事前学習 | 他のデータで学習済み。**ファインチューニングの出発点** |
| 重みファイル | `.pt` は学習のチェックポイント、`.onnx` は書き出した計算グラフ＋パラメータ |

### 実演 / Demonstration（10 分程度）

**必ず「うまくいかない例」を見せてください。**

1. `bus.jpg` に YOLO をかけ、バスと人が検出されることを見せる（**動く**）
2. 同じモデルを `defect_multi.png` にかけ、何も残らないことを見せる（**動かない**）。
   ただし残った検出が 0 件でも、それは「欠陥が無い」証拠ではありません。
   しきい値を下げると COCO のクラスとして誤った検出が出ることもあります。
3. 「なぜ動かないか」を受講者に考えさせる
4. 4 つの理由（クラス定義／分野／大きさと撮影条件／正解データが無い）を板書

Show both sides: the model works on `bus.jpg` and returns nothing meaningful on the PVC-like image.
Zero retained detections is not evidence that no defect exists, and lowering the threshold can
produce spurious COCO classes. Let learners explain why before you list the four reasons.

### 教材画像の出所 / Provenance of the course images

`bus.jpg` と `zidane.jpg` は `ultralytics` パッケージに同梱された公式サンプルです。
モデルは COCO で事前学習されていますが、**写真が COCO 由来という意味ではありません**。
パッケージの AGPL-3.0 はパッケージの配布条件で、写真 1 枚ずつの権利を保証するものではありません。
「教育目的なら自由に使える」と説明しないでください。再配布や製品利用の判断は利用者側が行います。
くわしくは `assets/external_samples/PROVENANCE.md`。

`bus.jpg` and `zidane.jpg` are the official samples bundled with the `ultralytics` package. The
model is pretrained on COCO, which does not make the photographs COCO images. The package
AGPL-3.0 licence covers the package distribution, not each photograph's rights. Do not tell
learners that educational use makes the photographs free to reuse; redistribution and product use
are the user's own decision. See `assets/external_samples/PROVENANCE.md`.

### よくある誤解 / Common beginner misunderstandings

| 誤解 / Misunderstanding | 実際 / Reality |
|---|---|
| 「AI は何でも見つける」 | 学習したクラスだけ |
| 「confidence が高い＝正しい」 | モデルが出したスコアにすぎない。堂々と間違える |
| 「confidence 0.50 は五分五分の確率」 | スコアの中間というだけで、正しさの確率ではない |
| 「IoU 1.0 でないと失敗」 | 0.5 以上を当たりとするのが一般的 |
| 「IoU 0.3 は枠の 30 % の重なり」 | 2 つの枠を合わせた領域（和集合）の 30 % |
| 「モデルを入れれば検査できる」 | **データと学習が無ければ何もできない** |
| 「正規化座標は 0〜255」 | **0〜1**。割り忘れると 1 を超える |
| 「0 件＝異常なし」 | **違う**。設定したクラスで残らなかっただけ。しきい値・失敗の可能性もある |
| 「低い confidence＝失敗」 | 疑わしいだけ。画像と見比べて正しい・間違い・判断できないを決める |

### 受講者に投げかける質問 / Questions to ask

1. 「confidence 0.9 の検出でも間違うことがあるのはなぜですか？」
2. 「IoU 0.3 のとき、重なりの面積は何の 30 % ですか？」
3. 「もし 80 クラスに `scratch` を足せるとしたら、何が必要ですか？」

### 午前の課題説明 / Explaining the morning assignment

ノートブック 01 の全 Part と演習 1〜2（座標計算・IoU の手計算）。演習 3 は任意（発展・任意）。

Notebook 01: all Parts plus Exercises 1-2 (coordinate conversion, hand-computed IoU).
Exercise 3 is optional.

---

## 午後（12:50–13:50）／ Afternoon session

### 午前の振り返り / What to review

1. YOLO 形式の 5 つの数値の意味（言わせる）
2. IoU の式と 0.5 の慣習
3. 事前学習モデルで塩ビ欠陥が検出できない 4 つの理由

### 期待される結果 / Expected results

| ノートブック / Notebook | 午後終了時の到達 / By end of day |
|---|---|
| 01 Concepts | 全 Part、IoU の手計算一致（演習 3 は任意） |
| 02 Inference | モデル取得、注釈画像と CSV の保存、演習 1〜2（演習 3 は任意） |
| 03 Experiments | しきい値の表、座標の読み取り、不確かな検出 1 件の見直し |

**02 の最初の実行だけは講師が見届けてください。** モデルのダウンロードで
つまずく受講者が必ず出ます（`assets/models/` に置く手順を案内）。

Supervise the first run of Notebook 02. Some learners will hit the model download;
walk them through placing `yolo26n.pt` in `assets/models/`.

### よくあるエラー / Common errors

| 症状 / Symptom | 原因 / Cause | 説明の仕方 / How to explain |
|---|---|---|
| `URLError` / `TimeoutError` | ダウンロード失敗 | 再実行 → 手動取得 → 情報システムへ |
| 色が反転して表示される | `plot()` は BGR | `cvtColor(..., COLOR_BGR2RGB)` |
| `ModuleNotFoundError: ultralytics` | カーネル違い | 右上のカーネル名を確認 |
| 検出数 0 | `conf` が高すぎる／画像に物体が無い／推論の失敗 | `conf=0.05` で試す。**0 件を「異常なし」と説明しない** |
| 動作が遅い | CPU 実行 | 正常。`imgsz=320` で速くなる |

### 次に導入する概念 / Next concepts to introduce

第 4 日は「**このモデルに、自分たちの欠陥を覚えさせる**」話です。
今日見た「検出できない理由」が、そのまま第 4 日の作業項目になります。

Day 4 teaches the model your own defects. Today's four reasons become tomorrow's
checklist.

### 午後の課題説明 / Afternoon assignment briefing

1. ノートブック 02 の全 Part（推論・結果の取り出し・保存）と演習 1〜2
2. ノートブック 03 の Part 1〜Part 5（しきい値・座標・4 つの場合・不確かな検出の見直し・解像度）と演習 1〜2
3. 演習 3（どちらのノートブックも発展・任意）
4. 提出物：推論結果の画像、検出結果の CSV、しきい値の表、不確かな検出の見直し記録

Notebooks 02 and 03: all Parts plus Exercises 1-2. Exercise 3 in both notebooks is optional.
Deliverables: the annotated image, the detection CSV, the threshold table and the review record for
one uncertain detection.

---

## 評価ルーブリック / Assessment rubric

| 観点 / Criterion | Level 0 | Level 1 | Level 2 | Level 3 |
|---|---|---|---|---|
| 検出の出力の理解 | 未着手 | 用語のみ | 3 要素を説明 | 現場での意味まで説明 |
| 座標変換 | 未着手 | 写しのみ | 計算できる | 逆変換もできる |
| IoU | 未着手 | 式の暗記 | 手計算できる | 0.5 の意味を説明 |
| 推論の実行 | 未実行 | 助けを借りて実行 | 一人で実行・保存 | パラメータの影響を説明 |
| 失敗の分析 | なし | 1 つ挙げる | 画像と見比べて判断し、仮説を書く | 改善案まで提案 |
| 塩ビへの理解 | なし | 「無理」だけ | 理由を 2 つ | 理由 4 つと対策 |

---

## 理解度チェックの解答例 / Model answers

**（受講者には渡さないでください / do not hand these to learners）**

### ノートブック 01

1. **バウンディングボックス（位置）、クラス（種類）、confidence（スコア）**。
2. **必ずしも正しくない。** confidence はモデルが出したスコアで、正しい確率ではない。
   見た目に騙されることがあり、0.9 を「90 % の確率で正しい」と読むことはできない。
3. **重なりが、2 つの枠を合わせた領域（和集合）の約 30 %。**
   予測の枠の 30 %、正解の枠の 30 % という意味ではない。
4. 例：① COCO に欠陥クラスが無い（クラス定義の違い） ② 写している分野が違う
   ③ 大きさ・撮影条件が違う ④ 正解データで学習していない。
5. **学習は計算時間とデータが必要。推論は学習済みモデルに画像を通すだけ。**
   この研修の記録では、第 4 日のファインチューニング（15 エポック、CPU）が約 90 秒。

### ノートブック 02

1. **結果のリスト**。1 枚なら `results[0]`。
2. **残る数は増えますが、必ず増えるとは限りません**（同じ候補集合なら、しきい値を下げて減ることはない）。
   その代わり **偽陽性（誤検出）が増え**、「疑わしい候補」も残ります。
3. `box.cls` を `int()` にし、`result.names[その番号]` で名前を引く。
4. ① 同じセルを再実行 ② releases から手動取得して `assets/models/` に置く ③ 情報システムに相談。
5. **利点**：ネットワーク不要・再現できる・全員が同じファイルを使える。
   **注意**：塩ビの欠陥ではないこと、COCO のクラスしか出ないこと、
   同梱写真 1 枚ずつの権利表示は無いこと（パッケージの AGPL-3.0 はパッケージの配布条件で、
   写真の権利を保証するものではない）。「COCO で事前学習済み」はモデルの学習データの話で、
   写真の出所とは別。

### ノートブック 03

1. **記録した実行では、正しい検出も confidence 0.881 程度で、0.90 未満に集まっていた** から。
   しきい値を 0.90 にするとバスまで消えた。ただしこれは記録されたスコア次第で、
   0.90 より上に 1 件も無ければ結果は 0 件になる。
2. **偽陰性**＝本当の欠陥を見逃すこと。**偽陽性**＝正常品を不良と判定すること。
3. confidence は「学習した見た目にどれくらい似ているか」というモデルのスコアで、
   **正解かどうかとは別**。低いスコアは「疑わしい」であって「間違い」ではない。
4. ① 物体が数ピクセルになり、形が分からなくなる ② 入力が `imgsz` に縮小され、細部が失われる。
5. 意見が分かれる。**見逃しを先に減らす**のが原則だが、誤報が多すぎると現場が検査を
   信用しなくなり、結局見逃しが増える。**両方を測りながら決める** のが正解。