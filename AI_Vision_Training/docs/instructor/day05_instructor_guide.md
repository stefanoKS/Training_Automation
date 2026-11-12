# 第5日 講師ガイド / Day 5 Instructor Guide

**PatchCore 異常検知と YOLO との比較 / PatchCore anomaly detection and comparison with YOLO**

---

## 午前（08:00–09:00）／ Morning session

### 学習目標 / Learning goals

1. 異常検知が「正常だけ」で学ぶことを説明できる
2. パッチ・特徴・メモリバンク・最近傍距離の関係を説明できる
3. 異常スコアをしきい値で OK/NG に変える流れを説明できる
4. PatchCore の限界（種類が分からない・正常のばらつきを誤検知）を言える
5. YOLO と PatchCore の出力の違いを説明できる

### 説明する概念 / Key concepts

| 概念 / Concept | 説明の要点 / Key message |
|---|---|
| 異常検知 | 正常の見え方を学び、そこからの外れを数値化する |
| 正常のみ学習 | ラベル作成が不要。**現場の最大の利点** |
| パッチ | 画像の小片。異常は **局所** に起きる |
| 特徴 | パッチを数値の並びにしたもの（見た目の「住所」） |
| メモリバンク | 正常パッチの特徴を保存したもの（コアセットに間引き） |
| 異常スコア | 一番近い正常パッチまでの距離 |
| ヒートマップ | 画素ごとの異常の度合い。**種類は分からない** |

### 実演 / Demonstration（10 分程度）

**日本語：**

1. 正常画像 3 枚と異常画像 3 枚を見せ、**違いを言葉にさせる**（意外と難しい）
2. 「この違いをルールで書けますか？」と問いかける → 書けないことを確認
3. ノートブック 01 の最近傍距離の散布図を見せる
4. PatchCore の 4 ステップ図を見せる

**English:** Show three normal and three abnormal images and ask learners to describe the difference
in words. They will struggle — that is the point. Then show the nearest-neighbour scatter and the
four-step diagram.

### よくある誤解 / Common beginner misunderstandings

| 誤解 / Misunderstanding | 実際 / Reality |
|---|---|
| 「異常検知は何でも見つける」 | 正常に似た欠陥は見逃す |
| 「異常スコアが高い＝不良」 | 正常なばらつきを異常と言うことがある |
| 「学習＝ネットワークを賢くする」 | 特徴を計算して保存するだけ。重みは更新しない |
| 「エポックを増やせば精度が上がる」 | PatchCore は 1 回で完了。増やしても無意味 |
| 「YOLO と AUROC を比べられる」 | 測っているものが違う |

### 受講者に投げかける質問 / Questions to ask

1. 「正常品のばらつきを、どこまで学習データに入れるべきですか？」
2. 「異常スコア 0.6 が出ました。不良ですか？」
3. 「YOLO と PatchCore、現場ではどちらを先に使いますか？」

### 午前の課題説明 / Explaining the morning assignment

ノートブック 01 の全 Part と演習 1〜3。

**日本語：** 第 5 日のノートブック 02・03 は **`aivision-anomalib` カーネル** です。
午前中に、カーネルが一覧に出るか確認させてください。

**English:** Notebooks 02 and 03 need the `aivision-anomalib` kernel. Verify during the morning that
it appears in the kernel list.

---

## 午後（12:50–13:50）／ Afternoon session

### 午前の振り返り / What to review

1. 「正常だけ」で学ぶ利点と代償（言わせる）
2. 異常スコア → しきい値 → OK/NG の流れ
3. PatchCore で **できないこと** 3 つ

### 期待される結果 / Expected results

| ノートブック / Notebook | 午後終了時の到達 / By end of day |
|---|---|
| 01 Concepts | 全 Part、散布図の読み取り |
| 02 PatchCore Training | fit 完了、4 指標、ヒートマップ、JSON 保存 |
| 03 YOLO vs PatchCore | 共通画像での比較表、限界の説明、推奨の作成 |

**日本語：** 参考実測（CPU, resnet18）:
`image_AUROC 1.000 / image_F1 0.974 / pixel_AUROC 0.984 / pixel_F1 0.386`。
**pixel_F1 が低いのは異常** ではなく、**画素単位の一致が厳しい** ためです。説明できるようにしてください。

**English:** Reference values on CPU with ResNet-18: image_AUROC 1.000, image_F1 0.974,
pixel_AUROC 0.984, pixel_F1 0.386. The low pixel_F1 is not a fault — pixel-level agreement is simply
demanding.

### よくあるエラー / Common errors

| 症状 / Symptom | 原因 / Cause | 説明の仕方 / How to explain |
|---|---|---|
| `No module named 'anomalib'` | カーネル違い | 右上で `AI Vision Anomalib` を選ぶ |
| `RecursionError` | Lightning の経過表示 | 教材は表示を切ってある。再実行 |
| `AttributeError: 'Folder' object has no attribute 'val_data'` | `val_split_mode="none"` | `from_test` を指定 |
| `MisMatchError` | 異常画像とマスクの対応ずれ | ファイル名を確認 |
| 比較で共通画像 0 枚 | JSON のパス形式 | `test/` の除去を確認 |
| `precision/recall` が `nan` | TP+FP または TP+FN が 0 | データとしきい値を確認 |

### 次に導入する概念 / Next concepts to introduce（第2週へ）

**日本語：** 第 1 週の締めくくりとして、次の 3 つを伝えてください。

1. **合成データの精度は製品の精度ではない**
2. 実際の PVC では、色ムラ・照明ムラ・反射が加わる
3. 第 2 週で、カメラ・照明・校正・実画像の収集に取り組む

**English:** Close Week 1 with three messages: synthetic accuracy is not product accuracy; real PVC
adds mottling, uneven lighting and reflections; Week 2 tackles camera, lighting, calibration and real
data collection.

### 午後の課題説明 / Afternoon assignment briefing

1. ノートブック 02 の全 Part（学習・評価・スコア・ヒートマップ・保存）
2. ノートブック 03 の全 Part（比較・限界・推奨）
3. 提出物：PatchCore の指標、ヒートマップ、比較表、
   **PVC 検査への推奨（判断と理由）**

**日本語：** 推奨には **必ず根拠の数字を引用させる** でください。「なんとなく」を許さないのが
第 1 週の到達点です。

**English:** Require every recommendation to cite a concrete number. That is the standard Week 1
should reach.

---

## 評価ルーブリック / Assessment rubric

| 観点 / Criterion | Level 0 | Level 1 | Level 2 | Level 3 |
|---|---|---|---|---|
| 異常検知の概念 | 未着手 | 用語のみ | 正常のみ学習を説明 | 利点と代償を説明 |
| パッチ・特徴・スコア | 未着手 | 図の写し | 流れを説明 | 比喩で人に説明できる |
| PatchCore の実行 | 未実行 | 助けを借りて実行 | 一人で実行 | パラメータの影響を説明 |
| ヒートマップの解釈 | 未着手 | 見るだけ | 明るい場所を説明 | 誤検知の原因を推測 |
| 比較の妥当性 | なし | 表を写す | 出力の違いを説明 | 比較の限界を指摘できる |
| 推奨の作成 | なし | 手法名のみ | 理由付き | 数字を引用し順序まで提案 |

---

## 理解度チェックの解答例 / Model answers

**（受講者には渡さないでください / do not hand these to learners）**

### ノートブック 01

1. **不要。** 正常品の見え方だけを学び、そこからの外れを測るため。ラベル作成の手間が最大の利点。
2. 異常は **画像全体ではなく局所** に起きるから。小片ごとに比べたほうが敏感。
3. **正常パッチの特徴**（代表的なものを間引いたコアセット）。
4. スコアは **正常からの距離** であり、正常なばらつき（色ムラ・模様）でも高くなる。
   しきい値と学習データの範囲で決まる。
5. 正常なばらつきを異常と判定し、**偽陽性が増える**。現場が検査を信用しなくなる。

### ノートブック 02

1. **異常画像を「正常」として覚えてしまい、二度と検出できなくなる** から。
2. 正常画像をバックボーンに通して **特徴を計算し、メモリバンクに保存** する。
   **重みは更新しない。**
3. `image_AUROC` は **画像単位で OK/NG を分ける力**、`pixel_AUROC` は **画素単位で異常領域を
   当てる力**。
4. しきい値を **検証データで決め、成績を試験データで測る** ため（同じデータで両方はできない）。
5. **合成画像は実際より簡単** で、実際の PVC の光学的条件（ムラ・反射）を含まないから。

### ノートブック 03

1. mAP は **四角とクラス** を必要とし、AUROC は **スコア** を必要とする。測っている対象が違う。
2. それぞれの手法に **正解ラベル付きデータで決めたしきい値**。
3. **正常に近い見た目の欠陥**（低コントラスト・正常のばらつきに似たもの）。
4. **学習していない種類の欠陥**、小さすぎる欠陥、学習時と分布が違う画像。
5. 意見が分かれる。**まず異常検知で網をかけ、確定した不良は YOLO で種類と位置を記録する**
   という順序が現実的。理由として、ラベルの無い未知欠陥に対応でき、種類の記録は YOLO が得意。