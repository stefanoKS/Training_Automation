# 第5日 講師ガイド / Day 5 Instructor Guide

**PatchCore 異常検知と YOLO との比較 / PatchCore anomaly detection and comparison with YOLO**

### 監査対応の確認 / Audit-remediation checks

主手順は較正 → 全設定固定 → 未使用試験です。しきい値だけでなく重み・前処理・
正常メモリ・後処理も固定します。旧17/26対26/26は **SUPERSEDED / biased**。
同梱参考図の0.06 / 0.50は保存実行の例であり、受講者の再実行を保証しません。
streak_0005 の元の数値記録がない場合、新しい数値付き拡大図を作りません。

Use calibration → freeze all settings → untouched test. Freeze weights, preprocessing, normal
memory and postprocessing as well as thresholds. Historical 17/26 versus 26/26 is
**SUPERSEDED / biased**. Supplied 0.06 / 0.50 values are saved-run examples, not guaranteed reruns.
Do not create a new numeric streak_0005 zoom without the original numerical records.

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
| 正常画像のみ学習 | fit にラベルが要らない。**現場の最大の利点**。ただし較正と評価にはラベル付き画像が必要 |
| パッチ | 特徴マップの 1 つの位置。入力の **重なり合う範囲** をまとめたもの（画素の切り出しではない） |
| 特徴 | パッチを数値の並びにしたもの（見た目の「住所」） |
| メモリバンク | 正常パッチの特徴を保存したもの（コアセットに間引き） |
| 異常スコア | 一番近い正常特徴までの距離を、較正用データの統計で 0〜1 に変換した値。**生の距離は 0〜1 ではない** |
| ヒートマップ | 画素ごとの異常の度合い。**種類は分からない**。色は表示範囲とカラーマップで決まる |

用語は **「正常画像のみを使って学習する異常検知 / anomaly detection fitted using normal images only」**
で統一してください。文献の one-class・semi-supervised は「呼び名が複数ある」とだけ説明し、
fit（正常画像だけで合わせる）と、較正・評価（ラベル付き画像でしきい値を決め誤りを測る）を
分けて話します。「ラベルがまったく不要」と言わせないでください。

Use **"anomaly detection fitted using normal images only"** throughout. Mention one-class and
semi-supervised only as other names in the literature, and separate fitting (normal images only)
from calibration and evaluation (labelled images give the threshold and the error counts). Never
let anyone say labels are entirely unnecessary.

### 実演 / Demonstration（10 分程度）

1. 正常画像 3 枚と異常画像 3 枚を見せ、**違いを言葉にさせる**（意外と難しい）
2. 「この違いをルールで書けますか？」と問いかける → 書けないことを確認
3. ノートブック 01 の最近傍距離の散布図を見せる
4. PatchCore の 4 ステップ図を見せる

Show three normal and three abnormal images and ask learners to describe the difference
in words. They will struggle — that is the point. Then show the nearest-neighbour scatter and the
four-step diagram.

### よくある誤解 / Common beginner misunderstandings

| 誤解 / Misunderstanding | 実際 / Reality |
|---|---|
| 「異常検知は何でも見つける」 | 正常に似た欠陥は見逃す |
| 「異常スコアが高い＝不良」 | スコアは正常からの隔たり。しきい値で決めた判定は間違うことがある |
| 「学習＝ネットワークを賢くする」 | 特徴を計算して保存するだけ。重みは更新しない |
| 「エポックを増やせば精度が上がる」 | この合わせ方は 1 回で足りる。データを変えたら fit と較正をやり直す |
| 「YOLO と AUROC を比べられる」 | 測っているものが違う。比べるのは同じ正解に対する画像単位の判定 |
| 「画像スコア＝ヒートマップの最大値」 | この設定では重み付きの値と補間・平滑化したマップなので別の数（保存例 21.439 と 21.762、後処理後 1.000） |
| 「train に異常が混ざると、その欠陥は二度と検出できない」 | スコアが下がり見逃しの危険が増える。混入画像を除いてメモリバンクを作り直し、較正・評価用画像で確かめる |

### 受講者に投げかける質問 / Questions to ask

1. 「正常品のばらつきを、どこまで学習データに入れるべきですか？」
2. 「異常スコア 0.6 が出ました。不良ですか？」
3. 「YOLO と PatchCore、現場ではどちらを先に使いますか？」

### 午前の課題説明 / Explaining the morning assignment

ノートブック 01 の Part 0〜5 と演習 1〜2（必須）。**演習 3（発展・任意）** に取り組むかどうかは
任意です。
ノートブック 02 も演習 1〜2 が必須です（**重いバックボーン自体は任意** で、CPU が厳しければ別の設定で
同じ比較をしてかまいません）。ノートブック 03 の演習 1〜2 は必須、演習 3（発展・任意）は任意です。

Notebooks 01, Parts 0-5 and exercises 1-2 (required). **Exercise 3 (optional challenge)** is not
required. Notebook 02 also requires exercises 1-2 (**the heavier backbone itself is optional**; on a
slow CPU the same comparison may use another setting). In Notebook 03, exercises 1-2 are required and
Exercise 3 (optional challenge) is optional.

第 5 日のノートブック 02・03 は **`aivision-anomalib` カーネル** です。
午前中に、カーネルが一覧に出るか確認させてください。

Notebooks 02 and 03 need the `aivision-anomalib` kernel. Verify during the morning that
it appears in the kernel list.

---

## 教室での実行順 / The classroom order (six steps)

`Day05_02` は **2 回** 開きます。`Day04_03` も **固定後にもう一度** 開きます。試験用のスコアは、
しきい値を固定するまで 1 つも作りません。

`Day05_02` is opened **twice**, and `Day04_03` is reopened **once after the freeze**. No test score
exists before the thresholds are frozen.

| # | ノートブック（環境）/ Notebook (env) | すること / What happens |
|---|---|---|
| 1 | `Day04_03`（YOLO） | 比較用セットの分割を決め、較正用 26 枚だけを採点する / decide the shared split, score the 26 calibration images only |
| 2 | `Day05_02`（anomalib） | fit し、分割が第 4 日と一致することを確かめ、較正用を採点する / fit, verify the split against Day 4, score calibration |
| 3 | `Day05_03`（anomalib） | 較正用で 2 つのしきい値を決め、固定を記録する / choose both thresholds on calibration, record the freeze |
| 4 | `Day04_03`（YOLO） | `shared-sealed-test` だけを実行し、試験用 26 枚を 1 回採点して封印する / run only `shared-sealed-test` and seal the 26 test images once |
| 5 | `Day05_02`（anomalib） | `clarity-sealed-test-scoring` だけを実行し、試験用 26 枚を 1 回採点して封印する / run only `clarity-sealed-test-scoring` and seal them once |
| 6 | `Day05_03`（anomalib） | 2 つの封印を読み、身元を確かめて最終比較を出す / load both seals, verify provenance, produce the comparison |

**「すべて実行 / Run All」は封印セルで止まります。** これは故障ではなく、固定を飛ばせないための仕様です。
各封印は固定記録と照合されます（学習した状態の指紋・分割・しきい値・評価の役割）。役割を書き換えた
記録や、fit し直したモデルは拒否されます。分割は第 4 日が推論より前に決め、第 5 日が anomalib の
実際の分割と照合します。食い違えば止まります。

"Run All" stops at the sealing cell **by design**: the freeze cannot be skipped. Each seal is checked
against the freeze record — the fitted fingerprint, the split, the thresholds and the assessment role.
A relabelled role or a refitted model is rejected. The split is decided by Day 4 before any
inference and verified against the installed anomalib by Day 5; a mismatch stops the notebook.

## 比較の較正（重要） / How the comparison is calibrated (important)

> **受講者向けの説明はノートブックにあります。この節は講師用です。**
> The learner-facing explanation is in the notebook; this section is for the instructor.

以前の版では、PatchCore のしきい値を「正常スコアの最大と異常スコアの最小の中央」で決め、
**同じデータで成績を出して** いました。これは「答えを見てから採点する」のと同じで、
受講者に教えてはいけない手順です。現在は次の 2 段階です。

The earlier version chose the PatchCore threshold as the midpoint between the maximum normal score
and the minimum abnormal score, **and then scored the same data** — marking your own exam. Do not
teach that. The current workflow has two steps:

| 段階 / Step | データ / Data | 何をするか / What happens |
|---|---|---|
| 1. 較正 / calibration | `calibration`（anomalib の val 分割）/ the anomalib validation split | 2 つのしきい値を、共通の目的関数で決める / choose both thresholds with one shared objective |
| 2. 評価 / evaluation | `test`（較正に使っていない残り）/ the untouched remainder | しきい値を **固定** して 1 回だけ成績を出す / freeze and score once |

**目的関数 / objective:** 正常品の誤報率（false reject rate）≤ 10% の条件で、再現率（recall）を最大にする。
等しい再現率なら、しきい値が高い方（誤報の余裕が大きい方）を選びます。
maximise recall subject to a false-reject rate of at most 10%; among equal recall, take the higher
threshold.

**必ず伝えること / Always say this:**

- 較正用は 26 枚（正常 6・異常 20）。**正常 6 枚では誤報率 10% は「誤報 0 枚」** と同じです。
  これは **この研修の目標値（教室での基準）** で、生産での誤報率を保証する数字ではありません。
  記録された実行（2026-11）では、両手法とも較正で recall 1.0（20/20）・FP 0（0/6）になりました。
- 試験用は別の 26 枚（正常 6・異常 20）。記録された実行では YOLO が 20/20、PatchCore が 19/20 でした。
  **較正で完璧だった PatchCore が、試験で 1 件見逃した** — これが一般化の差であり、
  この研修で一番伝えたい事実です。しきい値 0.06 と 0.50 は **この 1 回の実行の値** です。
- 件数は分母と一緒に言ってください（20/20、19/20、0/6）。件数だけでは率は伝わりません。
- 数値は環境とシードで変わります。**この数字を製品の精度として引用させないでください。**

- The calibration partition is 26 images (6 normal, 20 abnormal). **With 6 normal images a 10% cap
  means zero false alarms.** That 10% is a **classroom objective**, not a production guarantee. In
  the recorded run (2026-11) both methods reached recall 1.0 (20/20) with 0 false alarms (0/6) on
  calibration.
- The test partition is a different 26 images (6 normal, 20 abnormal). In the recorded run YOLO
  scored 20/20 and PatchCore 19/20 — **the method that looked perfect on calibration missed one
  defect on test**. That gap is the most important fact in this course. The thresholds 0.06 and 0.50
  belong to **that one recorded run**.
- Always quote the denominator with the count (20/20, 19/20, 0/6); a bare count does not convey a
  rate.
- Numbers depend on the machine and the seed. **Never let anyone quote them as product accuracy.**

`submissions/day05/comparison_test_results.json` に、分割・モデル・しきい値・目的関数・
スコアの定義がすべて入っています。古い `yolo_vs_patchcore.csv` は
`superseded`（旧方式）として残してあります。**上書きしないでください。**

`submissions/day05/comparison_test_results.json` records the split, the model, the thresholds, the
objective and the score convention. The old `yolo_vs_patchcore.csv` is kept as `superseded`;
**do not overwrite it**.

### スコアの読み方（講師用） / Reading the scores (instructor notes)

- 画像スコアは **最大のパッチ距離 × 近傍 9 個から作る重み** です。表示するマップは、その距離を
  **画像サイズに補間し平滑化** したものです。**画像スコア＝マップの最大値ではありません。**
  保存した `black_spot_0000` では、生の画像スコア **21.439**、表示したマップの最大値 **21.762**、
  後処理後のスコア **1.000** で、3 つとも違う数です。
- 生の距離は 0〜1 に収まりません（この実行では約 9〜21）。0〜1 になるのは、**較正用データの統計で
  変換したあとのスコア** です。
- anomalib 2.7.0 の変換式は `clip((raw - threshold) / (max - min) + 0.5, 0, 1)` です。
  `min`・`max`・`threshold` は **較正用（validation）分割** から求めます。`max - min = 0` の
  ときはしきい値との比較で 1 / 0.5 / 0 に落とし、統計が無い（NaN の）ときは生の値をそのまま返します。
  この式のため、**較正で決めたしきい値は 0〜1 の目盛りで 0.5** になります。
  画像用と画素用の統計は **別々** です。
- 「`pred_score` はいつも 0〜1」と言わないでください。後処理が無効、または統計が未 fit のときは
  0〜1 になりません。
- ヒートマップの色は **カラーマップと表示範囲** で決まります。比較するときは表示範囲を固定し、
  カラーバーを付け、範囲外がクリップされることを伝えてください。

- The image score is **the largest patch distance multiplied by a weight from its 9 nearest
  features**; the displayed map is those distances **interpolated and smoothed**. **The image
  score is not the map maximum.** For the saved `black_spot_0000`: raw image score **21.439**,
  displayed map maximum **21.762**, post-processed score **1.000** — three different numbers.
- Raw distances are not bounded to 0-1 (about 9-21 in this run). Only the **score rescaled with
  calibration statistics** is on 0-1.
- Anomalib 2.7.0 normalises with `clip((raw - threshold) / (max - min) + 0.5, 0, 1)`, where the
  `min`, `max` and `threshold` come from the **calibration (validation)** partition. A degenerate
  range falls back to 1 / 0.5 / 0 by comparison with the threshold, and missing (NaN) statistics
  leave the raw value untouched. This is why **the calibrated threshold sits at 0.5 on the 0-1
  scale**. Image-level and pixel-level statistics are fitted separately.
- Never say "`pred_score` is always 0-1". With postprocessing disabled or unfitted it is not.
- Heatmap colours come from the **colormap and the display range**. Fix the range when comparing,
  show a colourbar, and say that values outside the range are clipped.

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

参考実測（CPU, resnet18, `image_size=256`, seed 2026 の **較正用 = validation** データ）:
`image_AUROC 1.0000 / image_F1Score 0.9744 / pixel_AUROC 0.9851 / pixel_F1Score 0.4307`。
この 4 つは **較正用データ** の値で、試験用の値はノートブック 03 で出します。
**pixel_F1 が低いのは異常** ではなく、**画素単位の一致が厳しい** ためです。説明できるようにしてください。

Reference values on CPU with ResNet-18 (`image_size=256`, seed 2026) **on the calibration
(validation) partition**: image_AUROC 1.0000, image_F1Score 0.9744, pixel_AUROC 0.9851,
pixel_F1Score 0.4307. These four are **calibration** numbers; the test numbers appear in Notebook 03.
The low pixel_F1 is not a fault — pixel-level agreement is simply demanding.

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

第 1 週の締めくくりとして、次の 3 つを伝えてください。

1. **合成データの精度は製品の精度ではない**
2. 実際の塩ビでは、色ムラ・照明ムラ・反射が加わる
3. 第 2 週で、カメラ・照明・校正・実画像の収集に取り組む

Close Week 1 with three messages: synthetic accuracy is not product accuracy; real PVC
adds mottling, uneven lighting and reflections; Week 2 tackles camera, lighting, calibration and real
data collection.

### 午後の課題説明 / Afternoon assignment briefing

1. ノートブック 02 の全 Part（学習・評価・スコア・ヒートマップ・保存）
2. ノートブック 03 の全 Part（比較・限界・推奨）
3. 提出物：PatchCore の指標、ヒートマップ、比較表、
   **塩ビ検査への推奨（判断と理由）**

推奨には、**判断の根拠となる数値を必ず示すように指導してください。** 「なんとなく」を許さないのが
第 1 週の到達点です。

Require every recommendation to cite a concrete number. That is the standard Week 1
should reach.

### 比較の 4 つの限界（受講者に必ず言わせる） / The four limits of the comparison

ノートブック 03 の Part 5 に 4 項目のリストがあります。口頭でも次の 4 つを確認してください。

1. **合成画像と実画像の差** — 合成は欠陥がはっきりし、背景のばらつきが小さい。
2. **少ないサンプルによる不確かさ** — 正常 6 枚・異常 20 枚。1 枚で率が動く。
3. **学習とラベルの予算が違う** — YOLO はラベル付き欠陥画像、PatchCore は正常画像のみ。
4. **解像度・前処理・運用しきい値への依存** — 入力サイズ、前処理、しきい値で結果が変わる。

5 列の比較図では **一致しない行は 1 つだけ** です。PatchCore が見逃した `streak_0005` の行
（YOLO NG・PatchCore OK（スコア 0.464 < 0.50）・正解 NG の **PatchCore の見逃し 1 件**）だけで、
ほかの行は 3 者一致です。「2 つの手法が一致したか」ではなく、**それぞれの判定を正解と突き合わせる**
ことを強調してください。

Notebook 03 Part 5 lists four limits; confirm all four orally: synthetic-to-real gap; small-sample
uncertainty; differing training and label budgets; dependence on resolution, preprocessing and the
operating threshold. In the five-column figure **exactly one row disagrees** — the image PatchCore
missed, `streak_0005` (YOLO NG, PatchCore OK with score 0.464 < 0.50, truth NG), which is the single
PatchCore miss — while every other row agrees across all three. Stress that each method's decision is
checked **against the ground truth**, not just against the other method.

---

## 評価ルーブリック / Assessment rubric

| 観点 / Criterion | Level 0 | Level 1 | Level 2 | Level 3 |
|---|---|---|---|---|
| 異常検知の概念 | 未着手 | 用語のみ | 正常のみ学習を説明 | 利点と代償を説明 |
| パッチ・特徴・スコア | 未着手 | 図の写し | 流れを説明 | 比喩で人に説明できる |
| PatchCore の実行 | 未実行 | 助けを借りて実行 | 一人で実行 | パラメータの影響を説明 |
| ヒートマップの解釈 | 未着手 | 見るだけ | 表示範囲と色の意味を説明 | 誤検知の原因を推測 |
| 比較の妥当性 | なし | 表を写す | 出力の違いを説明 | 比較の限界を指摘できる |
| 推奨の作成 | なし | 手法名のみ | 理由付き | 数字を引用し順序まで提案 |

---

## 理解度チェックの解答例 / Model answers

**（受講者には渡さないでください / do not hand these to learners）**

### ノートブック 01

1. **fit には不要。** 正常品の見え方だけを学び、そこからの外れを測るため。ラベル作成の手間が
   最大の利点。ただし **較正（しきい値）と評価には** 正常・異常のラベル付き画像が要る。
   文献では one-class・semi-supervised などと呼ぶことも添える。
2. 異常は **画像全体ではなく局所** に起きるから。小片ごとに比べたほうが敏感。ただし大域的・
   構造的な異常は局所の比較だけでは捉えにくい。
3. **正常パッチの特徴**（代表的なものを間引いたコアセット）。
4. スコアは **正常からの距離** であり、正常なばらつき（色ムラ・模様）でも高くなる。
   しきい値と学習データの範囲で決まる。したがって **しきい値を通した結果は予測** で、間違うことがある。
5. 正常なばらつきを異常と判定し、**誤報（偽陽性）が増える**。現場が検査を信用しなくなる。

### ノートブック 02

1. **異常画像を「正常」として覚えてしまい、同じような見え方の異常のスコアが下がって見逃しが
   増える** から。「二度と検出できない」と断定はできない（コアセットの選ばれ方、特徴の近傍、
   位置や周囲の見え方、しきい値で変わる）。混入画像を除いてメモリバンクを作り直し、
   較正用・評価用の画像で確かめる。
2. 正常画像をバックボーンに通して **特徴を計算し、メモリバンクに保存** する。
   **重みは更新しない。** データで決まるのはメモリバンクと、そのあとの較正（しきい値と
   正規化の統計）。
3. `image_AUROC` は **画像単位で OK/NG を分ける力**、`pixel_AUROC` は **画素単位で異常領域を
   当てる力**。**AUROC 1.0 は「この 26 枚で順位が完璧」** という意味で、どのしきい値でも完璧、
   という意味ではない。見逃しと誤報の件数は別に数える。
4. しきい値を **検証データで決め、成績を試験データで測る** ため（同じデータで両方はできない）。
   分かれる比率は `val_split_ratio=0.5` で決まる（`from_test` だけでは決まらない）。
5. **合成画像は実際より簡単** で、実際の塩ビの光学的条件（ムラ・反射）を含まないから。
   較正用は正常 6 枚・異常 20 枚しかなく、その枚数で測った数字は生産の性能にならない。

### ノートブック 03

1. mAP は **四角とクラス** を必要とし、AUROC は **スコア** を必要とする。測っている対象が違う。
2. それぞれの手法に **正解ラベル付きデータで決めたしきい値（判定規則）**。そのうえで
   **2 つの手法どうしの一致ではなく、それぞれの判定を同じ正解と突き合わせる**。
   しきい値の数値そのものは直接比べられない。
3. **正常に近い見た目の欠陥**（低コントラスト・正常のばらつきに似たもの）。記録された実行では
   試験用の `streak_0005` を 1 件見逃した（0.464 < 0.50）。
4. **学習していない種類の欠陥**、小さすぎる欠陥、学習時と分布が違う画像。
5. 意見が分かれる。**まず異常検知で網をかけ、確定した不良は YOLO で種類と位置を記録する**
   という順序が現実的。理由として、ラベルの無い未知欠陥に対応でき、種類の記録は YOLO が得意。
   ただし **組み合わせれば必ず補完するわけではなく**、計算時間と新しい誤りの組み合わせが増える。