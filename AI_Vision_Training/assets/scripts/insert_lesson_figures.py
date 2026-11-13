"""教材図をノートブックの Markdown に差し込みます（何度実行しても増えません）。

Insert the teaching figures into notebook Markdown cells **before** the code they explain, so a
learner sees the picture without starting a kernel. Every figure gets
a bilingual caption, a "what to notice" statement and one short question.

方針 / Rules
------------
* 画像は**リポジトリ内の相対パス**で参照します。ノートブックを開いた時点で表示されます。
  Images are referenced with repository-relative paths and appear before any execution.
* すでに同じ画像を参照しているノートブックは変更しません（冪等）。
  A notebook that already references the image is left untouched.
* コードセル・出力・セル ID・メタデータは変更しません。
  Code cells, outputs, cell ids and metadata are not touched.

使い方 / Usage
--------------
    python assets\\scripts\\insert_lesson_figures.py            # 適用 / apply
    python assets\\scripts\\insert_lesson_figures.py --check    # 確認のみ / check only
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

COURSE_ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK_DIR = COURSE_ROOT / "notebooks"
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")

# ---------------------------------------------------------------------------
# 差し込む図の一覧 / what goes where
# ---------------------------------------------------------------------------
#
# notebook    : notebook stem
# anchor      : substring of the Markdown heading the figure is placed **after**
# image       : file name inside assets/diagrams or assets/reference_outputs
# folder      : "diagrams" or "reference_outputs"
# caption_*   : what the figure is / 図の説明
# notice_*    : what the learner should notice / 気づいてほしいこと
# question_*  : one prediction or interpretation question / 学習者への問い
#
FIGURES = [
    dict(
        notebook="00_Environment_Setup",
        anchor="画面の部品と名前 / the parts of the screen and their names",
        folder="diagrams", image="teach_setup_workflow.png",
        title_ja="手順の全体像", title_en="the five steps at a glance",
        caption_ja="図：ノートブックを開いてから、エラーから戻るまでの 5 つの手順。どこを押すかと、"
                   "そこで何が見えるかを並べています（模式図）。",
        caption_en="Figure: the five steps from opening a notebook to recovering from an error, "
                   "with the control to use and what you should see (schematic).",
        notice_ja="② カーネルと ③ 実行は別の操作です。カーネルを選ばないまま実行すると、"
                  "「カーネルが見つかりません」というエラーになります。"
                  "また ⑤ で最初に読むのは、赤い文字の**一番下の行**です。",
        notice_en="Choosing the kernel (②) and running a cell (③) are separate actions. Running "
                  "without a kernel gives a \"no kernel\" error. In step ⑤ the first thing to read "
                  "is the **last line** of the red text.",
        question_ja="③ の実行を押したのに何も起きないとき、② の表示はどうなっているはずですか。",
        question_en="If pressing run in ③ does nothing, what should the kernel label in ② look like?",
    ),
    dict(
        notebook="Day01_01_Introduction_to_AI",
        anchor="3 つの言葉の関係",
        folder="diagrams", image="teach_train_vs_inference.png",
        title_ja="学習と推論は別の作業", title_en="training and inference are different jobs",
        caption_ja="図：学習（training）と推論（inference）の違い。学習は 1 回だけで時間がかかり、"
                   "推論は部品ごとに何度でも行えて速い、という役割の違いです（模式図）。",
        caption_en="Figure: training versus inference. Training happens once and is slow; inference "
                   "runs on every part and is fast (schematic).",
        notice_ja="重み（weights）は学習で決まり、推論では**変わりません**。"
                  "現場で毎日動くのは推論のほうです。モデルを良くしたいときは、"
                  "推論ではなく学習をやり直します。",
        notice_en="The weights are fixed by training and **do not change** during inference. What "
                  "runs in the factory is inference. To make the model better you retrain; you do "
                  "not tune the inference.",
        question_ja="1 日に 1000 個の部品を検査するとしたら、学習と推論はそれぞれ何回行われますか。",
        question_en="For 1000 parts a day, how many training and how many inference runs happen?",
    ),
    dict(
        notebook="Day02_02_Conditions_Loops_Functions",
        anchor="もし〜なら」を書く",
        folder="diagrams", image="teach_condition_branch.png",
        title_ja="条件で処理を分ける流れ", title_en="how a condition splits the work",
        caption_ja="図：測定値 12.14 mm を条件 11.8 ≤ x ≤ 12.2 に通したときの流れと、"
                   "4 つの値を実際に当てはめた結果（模式図）。",
        caption_en="Figure: one measurement (12.14 mm) passed through the condition 11.8 ≤ x ≤ 12.2, "
                   "and four real values applied to it (schematic).",
        notice_ja="分かれるのは「表示する文字」だけで、条件そのものは 1 つです。"
                  "境界値 12.20 mm は「以内」なので OK になります。"
                  "`<` と `<=` の 1 文字で結果が変わることに注意してください。",
        notice_en="Only the message differs; the condition is one expression. The boundary 12.20 mm "
                  "is inside the spec because it is \"within\". A single character, `<` versus `<=`, "
                  "changes the answer.",
        question_ja="11.74 mm が OK になる規格はどう書けばよいですか。",
        question_en="How would you write the spec so that 11.74 mm passes?",
    ),
    dict(
        notebook="Day03_01_YOLO_Concepts",
        anchor="バウンディングボックス / Bounding boxes",
        folder="diagrams", image="teach_bbox_coords.png",
        title_ja="四角を画像の上で読む", title_en="reading a box on the image",
        caption_ja="図：同じ 1 つの欠陥の四角を、画素の数（左）と画像サイズで割った値（右）で表したもの。"
                   "座標は計算して図に描いています。",
        caption_en="Figure: one defect box written as pixel counts (left) and as fractions of the "
                   "image size (right). The coordinates are computed and drawn, not sketched.",
        notice_ja="左の 4 つの数（x1, y1, x2, y2）と右の 4 つの数（cx, cy, w, h）は**同じ箱**です。"
                  "0〜1 の値は「画像のどこか」を表すので、画像を縮小しても同じ意味になります。",
        notice_en="The four pixel numbers (x1, y1, x2, y2) and the four fractions (cx, cy, w, h) "
                  "describe **the same box**. The 0–1 values say \"where in the image\", so they keep "
                  "their meaning when the image is resized.",
        question_ja="右の cx=0.450 から、この箱の中心は画像の横幅の何割の位置にあると言えますか。",
        question_en="From cx = 0.450, where is the centre of the box as a fraction of the image width?",
    ),
    dict(
        notebook="Day03_03_YOLO_Experiments",
        anchor="confidence のしきい値 / The confidence threshold",
        folder="diagrams", image="teach_confidence_filter.png",
        title_ja="しきい値で残る数が変わる", title_en="the threshold changes how many are kept",
        caption_ja="図：同じ 1 回の推論で得た 4 つの検出を、しきい値 0.25・0.50・0.75 で"
                   "絞り込んだ結果（合成画像・例示用の値）。",
        caption_en="Figure: the same four detections from one inference, filtered at 0.25, 0.50 and "
                   "0.75 (synthetic image, illustrative scores).",
        notice_ja="推論は 1 回だけで、しきい値を変えても**やり直していません**。"
                  "変わるのは「残すか捨てるか」だけです。しきい値を上げると残る数は減り、"
                  "同時に、本当の欠陥も落としやすくなります。",
        notice_en="Inference ran once; changing the threshold does **not** run it again. Only the "
                  "keep/drop decision changes. Raising the threshold keeps fewer boxes — and drops "
                  "real defects too.",
        question_ja="しきい値を 0.90 にすると、この 4 つのうち何個が残りますか。"
                    "そのとき本当の欠陥は残りますか。",
        question_en="At 0.90, how many of the four survive — and is the real defect still among them?",
    ),
    dict(
        notebook="Day03_03_YOLO_Experiments",
        anchor="confidence のしきい値 / The confidence threshold",
        folder="reference_outputs", image="ref_confidence_counts.png",
        title_ja="実際の結果で数える", title_en="counted on the real results",
        caption_ja="図：この研修で実際に保存した推論結果（52 枚）を使い、しきい値を変えたときに"
                   "NG と判定される枚数を数えたもの。右は画像ごとの最大 confidence の分布です。"
                   "参考出力（実際の結果）。",
        caption_en="Figure: using the 52 images actually saved by this course, how many are called NG "
                   "at each threshold. Right: the distribution of each image's highest confidence. "
                   "Reference output — real results.",
        notice_ja="推論は conf=0.01 で 1 回だけ行い、しきい値は後から動かしています。"
                  "正常品でも 0.01〜0.1 の検出が残るため、しきい値を 0 にすると全数 NG になります。"
                  "「検出がある」と「欠陥がある」は別だということが、この形で見えます。",
        notice_en="Inference ran once at conf = 0.01; the threshold is applied afterwards. Some normal "
                  "parts still have a weak detection near 0.01, so a threshold of 0 calls everything "
                  "NG. \"A detection exists\" is not the same as \"a defect exists\".",
        question_ja="この図で、しきい値を 0.50 から 0.75 に上げると NG は何枚減りますか。"
                    "減った分は正しい削除だと言い切れますか。",
        question_en="Raising the threshold from 0.50 to 0.75 removes how many NG calls? Can you claim "
                    "those removals were all correct?",
    ),
    dict(
        notebook="Day03_03_YOLO_Experiments",
        anchor="解像度と小さな物体 / Resolution and small objects",
        folder="diagrams", image="teach_resolution_effect.png",
        title_ja="解像度が欠陥の見え方を決める", title_en="resolution decides how a defect looks",
        caption_ja="図：同じ合成画像を 640→320→160→80 px に縮小し、欠陥の位置を等倍で表示したもの。"
                   "Δ は「欠陥あり」と「欠陥なし」の中心画素の差（計算値）。",
        caption_en="Figure: one synthetic image shrunk 640 → 320 → 160 → 80 px, zoomed at the defect. "
                   "Δ is the computed difference at the centre pixel with and without the defect.",
        notice_ja="画素数が減ると、欠陥の直径は 4.0 → 2.0 → 1.0 → 0.5 px になり、"
                  "明るさの差も 45 → 38 → 17 → 7 と小さくなります。"
                  "**撮影する時点で解像度を決めてしまうと、あとからモデルを変えても戻せません。**",
        notice_en="As pixels are removed the defect goes 4.0 → 2.0 → 1.0 → 0.5 px and the difference "
                  "falls 45 → 38 → 17 → 7. **Resolution is decided when you take the picture; no "
                  "later model change brings it back.**",
        question_ja="0.2 mm の欠陥を見つけるには、1 mm あたり何画素必要ですか。"
                    "この図の 4 つの条件のうち、どれが条件を満たしますか。",
        question_en="To find a 0.2 mm defect, how many pixels per millimetre do you need, and which "
                    "of the four conditions here satisfies it?",
    ),
    dict(
        notebook="Day04_02_YOLO_Training",
        anchor="read training and validation loss separately",
        folder="reference_outputs", image="ref_train_val_curves.png",
        title_ja="学習ログを 2 本の線で読む", title_en="reading the training log as two lines",
        caption_ja="図：この研修で実際に行った短い学習（15 epoch, CPU）の記録。左が損失、右が精度の指標。"
                   "合成ではなく、保存された学習ログそのものです。",
        caption_en="Figure: the short training run actually performed in this course (15 epochs, CPU). "
                   "Left: loss. Right: quality metrics. This is the saved log, not a synthetic curve.",
        notice_ja="2 本の線を別々に見ます。学習の損失だけが下がり続けて検証が下がらない状態が"
                  "「覚えすぎ（overfitting）」です。ここでは両方が下がっていますが、"
                  "検証の損失が学習より低いこともあります（学習時だけ画像を加工して難しくするため）。",
        notice_en="Read the two lines separately. Training loss falling while validation loss stops "
                  "falling is overfitting. Here both fall; the validation loss can sit below the "
                  "training loss because training adds augmentation.",
        question_ja="このログの最後の 3 epoch で、mAP50 は上がっていますか、横ばいですか。"
                    "学習をあと 15 epoch 続ける価値はありそうですか。",
        question_en="In the last three epochs, is mAP50 rising or flat? Would 15 more epochs be worth it?",
    ),
    dict(
        notebook="Day04_03_YOLO_Evaluation",
        anchor="画像単位の TP・FP・FN・TN / image-level TP, FP, FN and TN",
        folder="diagrams", image="teach_object_level_matching.png",
        title_ja="物体単位の対応づけ", title_en="matching objects one to one",
        caption_ja="図：物体単位の対応づけ。正解の四角と予測の四角を IoU で 1 対 1 に対応させ、"
                   "対応しない予測を FP として数えます（座標は例示用）。",
        caption_en="Figure: object-level matching. Truth and predicted boxes are paired one to one by "
                  "IoU; a prediction with no partner counts as a false positive (illustrative coordinates).",
        notice_ja="**物体単位**の数え方と、**画像単位**の OK/NG は別の計算です。"
                  "物体単位では「どの箱がどの箱に対応したか」を先に決め、"
                  "画像単位では「その画像に 1 つでも当てはまれば NG」のように決めます。"
                  "同じデータでも、数え方を混ぜると数字の意味が変わります。",
        notice_en="**Object-level** counting and the **image-level** OK/NG decision are different "
                  "calculations. Object level first pairs boxes; image level asks whether any box "
                  "matches. Mixing the two changes what the number means.",
        question_ja="P2（conf 0.61）は物体単位では FP です。この画像の画像単位の判定は OK と NG の"
                    "どちらになりますか。理由も言ってください。",
        question_en="P2 (conf 0.61) is an object-level FP. What is this image's image-level decision, "
                    "OK or NG, and why?",
    ),
    dict(
        notebook="Day04_03_YOLO_Evaluation",
        anchor="自分の目で確認する",
        folder="reference_outputs", image="ref_detections_label_vs_pred.png",
        title_ja="正解と予測を同じ並びで見る", title_en="truth and prediction in the same order",
        caption_ja="図：同じ 8 枚を、正解（左）と予測（右）で並べた実際の出力。"
                   "正解は人が付けた四角、予測は学習したモデルの四角です。",
        caption_en="Figure: the same eight images as ground truth (left) and prediction (right). "
                   "The left boxes were drawn by a person; the right boxes by the trained model.",
        notice_ja="右の列で**四角が無いのに左にある**画像を探してください。それが見逃し（FN）です。"
                  "逆に、右だけに増えている四角は誤検出（FP）です。"
                  "数字の表より先に、この 2 列を見比べるほうが失敗の種類が分かります。",
        notice_en="Find the images where the left column has a box and the right does not — those are "
                  "misses (FN). Extra boxes on the right are false positives (FP). Comparing these two "
                  "columns reveals failure types faster than the metrics table.",
        question_ja="見逃し（FN）は何枚ありますか。その画像の欠陥は、予測の列でどう見えていますか。",
        question_en="How many images contain a miss (FN), and how does the defect look in the "
                    "prediction column?",
    ),
    dict(
        notebook="Day05_02_PatchCore_Training",
        anchor="original, score map and overlay",
        folder="reference_outputs", image="ref_anomaly_panels.png",
        title_ja="実際の数値マップで確かめる", title_en="checking with the real numeric map",
        caption_ja="図：この研修で保存した PatchCore の生のパッチ距離マップ（`submissions/day05/maps/` の数値）。"
                   "元画像・数値マップ・同じ数値の重ね表示・数値の読み方を並べています。"
                   "描画済みの画像を切り抜いたものではありません。",
        caption_en="Figure: the raw patch-distance map saved by this course (the numbers in "
                   "`submissions/day05/maps/`) — original, numeric map, an overlay of the same values, "
                   "and how to read them. Nothing is cropped from a rendered picture.",
        notice_ja="左の 3 枚は**同じ数値**から描いています。色の目盛りは正規化前の距離（0〜マップの最大）で、"
                  "右のパネルの「画像スコア」はその最大値を較正用データで 0〜1 に直した別の数です。"
                  "**マップの色と画像スコアは別の数**だと分けて読んでください。",
        notice_en="The three left panels are drawn from the **same numbers**. The colour scale is the raw "
                  "distance (0 to the map maximum), while the image score on the right is that maximum "
                  "rescaled 0–1 with calibration statistics. **The colours and the image score are "
                  "different numbers.**",
        question_ja="右の「マップの最大値」と「画像スコア」は、なぜ同じ値にならないのですか。",
        question_en="Why are the map maximum and the image score on the right not the same number?",
    ),
    dict(
        notebook="Day05_03_YOLO_vs_PatchCore",
        anchor="Choose the thresholds on the calibration partition",
        folder="reference_outputs", image="ref_score_distribution.png",
        title_ja="較正用データの分布", title_en="the distribution on calibration data",
        caption_ja="図：この研修で実際に保存した**較正用（validation）データだけ**のスコア分布と、"
                   "そこから決めたしきい値 0.50。試験用データは含めていません。",
        caption_en="Figure: the score distribution on the **calibration (validation) partition only**, "
                   "as actually saved by this course, with the threshold 0.50 chosen from it. The test "
                   "partition is not included.",
        notice_ja="この線は「正常品の誤報を一定以下に抑えつつ、見逃しを最小にする」という 1 つの決め方で"
                  "選んでいます。較正で 0 件の見逃しでも、試験で 0 件になるとは限りません。"
                  "**線を動かしてよいのは、この図のデータだけ**です。",
        notice_en="The line comes from one rule: keep false alarms on good parts under a limit while "
                  "minimising misses. Zero misses in calibration does not promise zero on test. "
                  "**Only this figure's data may be used to move the line.**",
        question_ja="しきい値を 0.60 に上げると、この較正用データでは見逃しが何枚増え、誤報は何枚減りますか。",
        question_en="Raising the threshold to 0.60 adds how many misses and removes how many false "
                    "alarms on this calibration data?",
    ),
    dict(
        notebook="Day05_03_YOLO_vs_PatchCore",
        anchor="five aligned columns for the same image",
        folder="reference_outputs", image="ref_comparison_5col.png",
        title_ja="実際の 5 列の比較", title_en="the real five-column comparison",
        caption_ja="図：同じ 3 枚（試験用）を 5 つの列で並べた実際の結果。元画像・YOLO の四角・"
                   "PatchCore の数値マップ・正解マスク・画像単位の判定です。しきい値は固定済みで、"
                   "この図のために動かしていません。",
        caption_en="Figure: three test images in five aligned columns — original, YOLO boxes, "
                   "PatchCore's numeric map, ground-truth mask and the image-level decision. "
                   "Thresholds were already frozen and were not moved to make this figure.",
        notice_ja="1 行目は 3 者が食い違っています（YOLO は NG、PatchCore は OK、正解は NG）。"
                  "2 行目・3 行目は一致しています。列を増やす目的は「どちらが良さそうか」ではなく、"
                  "**どこで食い違うか**を見つけることです。正解マスク（④）は判定には使っていません。",
        notice_en="Row 1 is a disagreement (YOLO NG, PatchCore OK, truth NG); rows 2 and 3 agree. "
                  "The columns exist to show **where the methods disagree**, not which looks better. "
                  "The ground-truth mask (④) was never used for tuning.",
        question_ja="あなたの実行結果でも、1 行目の画像は同じ判定になりましたか。"
                    "違った場合、最初に疑うべき原因は何ですか。",
        question_en="Did the first image get the same decisions in your own run? If not, what is "
                    "the first cause to suspect?",
    ),
    # ------------------------------------------------------------------
    # the explanations that were text only / 文章だけだった説明に図を付ける
    # ------------------------------------------------------------------
    dict(
        notebook="00_Environment_Setup",
        anchor="Jupyter ノートブック・セル・カーネル",
        folder="diagrams", image="teach_setup_jupyter_ui.png",
        title_ja="画面の部品と名前", title_en="the parts of the screen and their names",
        caption_ja="図：ノートブック・セル・カーネル・出力の位置関係（模式図。実際の画面写真ではありません）。",
        caption_en="Figure: where the notebook, the cells, the kernel and the output sit "
                   "(schematic, not a screenshot).",
        notice_ja="セルは「文字を書く場所」、カーネルは「計算する別のプログラム」です。"
                  "だからカーネルを選び直しても、セルの文字は消えません。逆にカーネルを再起動すると、"
                  "計算した値（変数）だけが消えます。",
        notice_en="A cell is where the text lives; the kernel is a separate program that computes. "
                  "Choosing another kernel keeps your text; restarting the kernel throws away the "
                  "computed values (the variables).",
        question_ja="カーネルを再起動したとき、消えるのはセルの文字と変数のどちらですか。",
        question_en="After a kernel restart, which disappears: the cell text or the variables?",
    ),
    dict(
        notebook="00_Environment_Setup",
        anchor="Part 5　最初の Python プログラム",
        folder="diagrams", image="teach_execution_state.png",
        title_ja="実行前・実行中・実行後の状態", title_en="before, during and after a run",
        caption_ja="図：同じ 3 行のセルを、実行前・実行中・実行後に分けて、メモリの中身と一緒に示したもの（模式図）。",
        caption_en="Figure: the same three-line cell before, during and after a run, together with "
                   "what is in memory (schematic).",
        notice_ja="`In [ ]` は「まだ実行していない」、`In [*]` は「実行中」、`In [3]` は「3 番目に実行した」という意味です。"
                  "実行が終わると `width_mm` はメモリに残り、次のセルから使えます。",
        notice_en="`In [ ]` means not run yet, `In [*]` means running, `In [3]` means it was the "
                  "third run. When it finishes, `width_mm` stays in memory and the next cell can use it.",
        question_ja="1 行目のセルだけを実行して、2 行目のセルを実行したらどうなりますか。",
        question_en="If you run only the first cell and then run the second cell, what happens?",
    ),
    dict(
        notebook="00_Environment_Setup",
        anchor="エラーメッセージを読む練習",
        folder="diagrams", image="teach_nameerror_recovery.png",
        title_ja="NameError から戻る手順", title_en="recovering from a NameError",
        caption_ja="図：`widht_mm` と `width_mm` を書き間違えたときのエラーと、直す順番（模式図）。",
        caption_en="Figure: the error you get when `widht_mm` and `width_mm` are mixed up, and the "
                   "order for fixing it (schematic).",
        notice_ja="エラーの**一番下の行**に理由（`name 'width_mm' is not defined`）が書いてあります。"
                  "その上に「どのセルの何行目か」があります。2 回実行しても消えません。名前をそろえるまで同じです。",
        notice_en="The **last line** gives the reason (`name 'width_mm' is not defined`); above it "
                  "is the cell and line number. Running again does not help until the names match.",
        question_ja="`print(width_mm)` を実行する前に、どのセルを実行しておく必要がありますか。",
        question_en="Which cell must have been run before `print(width_mm)` can work?",
    ),
    dict(
        notebook="Day01_01_Introduction_to_AI",
        anchor="自動化＝同じ手順を機械に繰り返させる",
        folder="diagrams", image="teach_inspection_roles.png",
        title_ja="検査システムの 4 つの役割", title_en="the four roles in an inspection system",
        caption_ja="図：検査を自動化するときの「撮る・測る・決める・動かす」の 4 つの役割と、"
                   "AI が受け持つ範囲（模式図）。",
        caption_en="Figure: the four roles of an automated inspection — capture, measure, decide, "
                   "act — and the part AI covers (schematic).",
        notice_ja="AI が受け持つのは ③「決める」だけです。①撮る・②測る・④動かす が決まっていないと、"
                  "③ を良くしても検査全体は良くなりません。数で書ける判定は if 文のままにします。",
        notice_en="AI only covers ③ decide. If capture, measure and act are not fixed, a better ③ "
                  "does not make a better inspection. Decisions you can write as numbers stay as "
                  "if-statements.",
        question_ja="この 4 つのうち、いま自分の工程で決まっていないのはどれですか。",
        question_en="Which of the four is not yet decided in your own line today?",
    ),
    dict(
        notebook="Day01_01_Introduction_to_AI",
        anchor="3 つの言葉の関係",
        folder="diagrams", image="teach_ai_ml_dl_nested.png",
        title_ja="AI・機械学習・深層学習の入れ子", title_en="how the three words nest",
        caption_ja="図：AI ⊃ 機械学習 ⊃ 深層学習 の包含関係と、それぞれの例（模式図）。",
        caption_en="Figure: AI ⊃ machine learning ⊃ deep learning, with an example of each "
                   "(schematic).",
        notice_ja="**すべての AI が機械学習ではありません。** 人が書いた if 文も AI の一部ですが、"
                  "機械学習ではありません。この研修で使う YOLO と PatchCore は、いちばん内側の深層学習です。",
        notice_en="**Not all AI is machine learning.** An if-statement a person wrote can count as AI "
                  "but is not machine learning. YOLO and PatchCore sit in the innermost ring.",
        question_ja="「幅が 99.5 mm 未満なら NG」という if 文は、3 つのどれに入りますか。",
        question_en="Where does the rule “NG if width < 99.5 mm” belong: AI, machine learning or "
                    "deep learning?",
    ),
    dict(
        notebook="Day01_01_Introduction_to_AI",
        anchor="しきい値をデータから決める",
        before=True,
        folder="diagrams", image="teach_gaussian_vs_skewed.png",
        title_ja="±3σ が使えるのは、どんな分布か", title_en="when the ±3σ rule applies",
        caption_ja="図：左右対称の分布と、右に裾を引く分布に、同じ「平均 ± 3σ」を当てはめた結果"
                   "（合成データ。入る割合は計算値）。",
        caption_en="Figure: the same “mean ± 3σ” rule applied to a symmetric and to a right-skewed "
                   "distribution (synthetic data; the coverage is computed).",
        notice_ja="99.7 % は**正規分布（左右対称）のときの性質**です。右のように裾を引く分布では、"
                  "同じ ±3σ でも入る割合が変わります。「99.7 %」と書く前に、ヒストグラムの形を確かめてください。",
        notice_en="99.7 % is a property of the **normal (symmetric) distribution**. For a skewed one "
                  "the same ±3σ rule covers a different share. Look at the histogram before quoting 99.7 %.",
        question_ja="この右の分布で「平均 ± 3σ の外は異常」と決めると、どんな見逃し・誤報が起きますか。",
        question_en="If you call everything outside mean ± 3σ abnormal on the right-hand "
                    "distribution, what misses and false alarms follow?",
    ),
    dict(
        notebook="Day01_02_Pixels_and_Images",
        anchor="原点は左上、y は下向き",
        folder="diagrams", image="teach_array_indexing.png",
        title_ja="配列の添字とスライス", title_en="indexing and slicing an array",
        caption_ja="図：6 行 7 列の配列を画像として見たときの添字（行 = y、列 = x）と、"
                   "`image[1:4, 2:5]` で切り出される範囲（実際に計算した値）。",
        caption_en="Figure: a 6×7 array seen as an image — index = row (y) then column (x) — and the "
                   "block `image[1:4, 2:5]` takes out (values computed).",
        notice_ja="添字の順番は **`image[y, x]`（行 → 列）** です。`x, y` の順ではありません。"
                  "スライスの終わりの値は**含みません**（`1:4` は 1・2・3 行目）。",
        notice_en="The order is **`image[y, x]` — row, then column**, not x then y. A slice stops "
                  "**one short** of its end value (`1:4` is rows 1, 2, 3).",
        question_ja="`image[0:2, 0:3]` は何行何列のまとまりになりますか。",
        question_en="How many rows and columns does `image[0:2, 0:3]` give you?",
    ),
    dict(
        notebook="Day01_02_Pixels_and_Images",
        anchor="縮小すると何が起きるか",
        folder="diagrams", image="teach_resize_profile.png",
        title_ja="同じ領域を 3 つの解像度で比べる", title_en="one region at three resolutions",
        caption_ja="図：同じ合成画像・同じ領域を 320 / 160 / 80 px で切り出し、断面の明るさを"
                   "同じ軸で比べたもの（落ち込みの深さは計算値）。",
        caption_en="Figure: the same synthetic image and region at 320 / 160 / 80 px, with the "
                   "cross-section profiles drawn on one axis (depths computed).",
        notice_ja="解像度が下がると、断面の落ち込みは深いままではなく**浅く広がります**。"
                  "同じ欠陥でも、測る解像度が変われば「コントラスト」の数字が変わります。",
        notice_en="As the resolution falls, the dip in the profile gets **shallower and wider**. The "
                  "same defect gives a different contrast number at a different resolution.",
        question_ja="3 つの解像度のうち、いちばん大きな落ち込みを示すのはどれですか。その理由は？",
        question_en="Which of the three shows the deepest dip, and why?",
    ),
    dict(
        notebook="Day01_03_Computer_Vision_Tasks",
        anchor="セマンティックセグメンテーション",
        folder="diagrams", image="teach_segmentation_modes.png",
        title_ja="意味とインスタンスの違い", title_en="semantic versus instance",
        caption_ja="図：同じ 2 つの欠陥を、意味セグメンテーション（1 つのクラスにまとめる）と"
                   "インスタンスセグメンテーション（1 つずつ番号を付ける）で表したもの（合成画像）。",
        caption_en="Figure: the same two defects under semantic segmentation (one class) and "
                   "instance segmentation (numbered one by one) — synthetic image.",
        notice_ja="意味セグメンテーションでは、2 つの欠陥は**区別できません**。"
                  "「何個あるか」を数えたいときは、インスタンスセグメンテーションか検出が必要です。",
        notice_en="Semantic segmentation **cannot tell the two defects apart**. If you need a count, "
                  "you need instance segmentation or detection.",
        question_ja="「1 枚に欠陥が何個あるか」を数えたいとき、どちらの出力が必要ですか。",
        question_en="To count how many defects are on a part, which output do you need?",
    ),
    dict(
        notebook="Day02_01_Python_Basics",
        anchor="数値の種類と四則演算",
        folder="diagrams", image="teach_units_conversion.png",
        title_ja="寸法と単位換算", title_en="dimensions and unit conversion",
        caption_ja="図：300 mm × 200 mm のシートを、cm・m・µm・面積で書き直したもの（すべて計算値）。",
        caption_en="Figure: a 300 mm × 200 mm sheet written in cm, m, µm and area (all computed).",
        notice_ja="Python は単位を持ちません。だから `0.1 + 0.2` は `0.3` と等しくならず、"
                  "単位を間違えても計算は成功します。**変数名と表の見出しに単位を書く**のが対策です。",
        notice_en="Python has no units: `0.1 + 0.2` is not equal to `0.3`, and a unit mistake leaves "
                  "the arithmetic valid. Put the unit in the name and in the column heading.",
        question_ja="200 mm を µm で表すといくつですか。また mm² を cm² にするには何で割りますか。",
        question_en="What is 200 mm in µm, and what do you divide by to turn mm² into cm²?",
    ),
    dict(
        notebook="Day02_01_Python_Basics",
        anchor="比較演算子",
        folder="diagrams", image="teach_assign_vs_compare.png",
        title_ja="`=` と `==` は別の操作", title_en="`=` and `==` are different operations",
        caption_ja="図：代入（値を入れる）と比較（真偽を聞く）の違いと、実際に計算した 4 つの結果。",
        caption_en="Figure: assignment (store a value) versus comparison (ask for a truth value), "
                   "with four computed answers.",
        notice_ja="`a = 5` は値を入れます。`a == 5` は質問して `True` を返します。"
                  "`if a = 5:` と書くと SyntaxError になります。これは書き間違いを見つけるための仕組みです。",
        notice_en="`a = 5` stores a value; `a == 5` asks a question and returns `True`. "
                  "`if a = 5:` is a SyntaxError — a designed guard against a typo.",
        question_ja="`a == 6` の結果は `True` と `False` のどちらですか。",
        question_en="Does `a == 6` return `True` or `False`?",
    ),
    dict(
        notebook="Day02_01_Python_Basics",
        anchor="よく出るエラー 4 種類",
        folder="diagrams", image="teach_traceback_annotated.png",
        title_ja="traceback の読み方", title_en="how to read a traceback",
        caption_ja="図：0 で割ったときの traceback を、どこを読むかの順番つきで示したもの（模式図）。",
        caption_en="Figure: a division-by-zero traceback, annotated with the order to read it "
                   "(schematic).",
        notice_ja="読む順番は ① 一番下の行（理由）→ ② どのセル・どの行か → ③ その行の中身、です。"
                  "① を読まずに上から読むと、時間がかかります。",
        notice_en="Read ① the last line (the reason) → ② the cell and line → ③ the line itself. "
                  "Reading top-down first wastes time.",
        question_ja="`ZeroDivisionError` が出たとき、最初に確かめる変数はどれですか。",
        question_en="When a `ZeroDivisionError` appears, which variable do you check first?",
    ),
    dict(
        notebook="Day02_02_Conditions_Loops_Functions",
        anchor="`if` で「もし〜なら」を書く",
        folder="diagrams", image="teach_tolerance_boundary.png",
        title_ja="規格の境界は「含む」か", title_en="are the bounds inclusive",
        caption_ja="図：12.0 ± 0.2 mm の境界と、実際に比較した 5 つの値の判定。境界 12.200 mm は「以内」なので OK。",
        caption_en="Figure: the bounds of 12.0 ± 0.2 mm and the verdict for five compared values; "
                   "12.200 mm is inside because the bounds are inclusive.",
        notice_ja="`<=` と `<` の 1 文字で、境界の値の判定が変わります。"
                  "そして 12.20 mm は「OK」ですが、`0.1 + 0.2` のような計算を経た値は誤差を持つので、"
                  "比べる前に `round()` でそろえます。",
        notice_en="One character (`<=` versus `<`) changes the verdict at the boundary. Also, a value "
                  "that went through arithmetic such as `0.1 + 0.2` carries error, so round before comparing.",
        question_ja="12.201 mm を OK にしたいとき、条件はどう書き換えますか。",
        question_en="How would you rewrite the condition so that 12.201 mm passes?",
    ),
    dict(
        notebook="Day02_02_Conditions_Loops_Functions",
        anchor="関数は「名前を付けた処理」",
        folder="diagrams", image="teach_definition_vs_call.png",
        title_ja="定義とよび出し", title_en="defining versus calling",
        caption_ja="図：`def` で決めただけでは何も判定されず、呼び出したときに初めて中身が動くこと（判定は計算値）。",
        caption_en="Figure: `def` only names the rule; the body runs when you call it (verdicts "
                   "computed).",
        notice_ja="`def` を書いただけでは 1 件も判定していません。呼び出しの行が来て初めて中の処理が動きます。"
                  "引数の名前を指定して渡すと、順番を間違えにくくなります。",
        notice_en="Writing `def` judges nothing; the body runs when a call happens. Naming the "
                  "argument when you call makes the order impossible to get wrong.",
        question_ja="`judge()` を 3 回呼ぶと、`def` の中の行は何回実行されますか。",
        question_en="If you call `judge()` three times, how many times does the body run?",
    ),
    dict(
        notebook="Day02_03_OpenCV_Image_Processing",
        anchor="しきい値を変えると何が変わるか",
        folder="diagrams", image="teach_threshold_sweep.png",
        title_ja="しきい値を掃引して数える", title_en="sweeping the threshold and counting",
        caption_ja="図：同じ 1 枚を 19 通りのしきい値で 2 値化し、前景の画素数と連結領域の数を"
                   "同時に描いたもの（合成画像・実際の計算）。",
        caption_en="Figure: one image thresholded 19 ways, plotting the foreground pixel count and "
                   "the number of connected regions (synthetic, computed).",
        notice_ja="しきい値を上げると、前景の面積は増え、領域の数は増えてから減ります。"
                  "だから面積や個数を比べるときは、**必ずしきい値を書きます**。",
        notice_en="Raising the threshold grows the area; the region count rises and then falls. So an "
                  "area or a count **must** be reported with its threshold.",
        question_ja="しきい値 200 で数えた領域の数を、しきい値を書かずに報告すると何が起きますか。",
        question_en="What goes wrong if you report the region count at threshold 200 without "
                    "saying which threshold?",
    ),
    dict(
        notebook="Day02_03_OpenCV_Image_Processing",
        anchor="輪郭とは、白い領域のかたまり",
        folder="diagrams", image="teach_contour_merge.png",
        title_ja="つながると数が減る", title_en="merging reduces the count",
        caption_ja="図：近い 2 つの欠陥が、しきい値を上げると 2 領域 → 1 領域 → 18 領域と変わる例"
                   "（合成画像・実際の計算）。",
        caption_en="Figure: two nearby defects go from 2 regions to 1 (merged) to 18 (background "
                   "noise) as the threshold rises (synthetic, computed).",
        notice_ja="領域の数は**単調に増えません**。間の薄いムラが前景に入ると 1 つに**つながり**、"
                  "さらに上げると背景のムラで急に増えます。数だけを見て「欠陥が増えた」と判断しないでください。",
        notice_en="The count is **not monotonic**: a faint bridge merges two regions into one, then "
                  "background noise multiplies them. A change in count is not a change in defects.",
        question_ja="第 1 の図（2 領域）と第 2 の図（1 領域）で、実際の欠陥の数は変わっていますか。",
        question_en="Between the first panel (2 regions) and the second (1 region), did the number "
                    "of real defects change?",
    ),
    dict(
        notebook="Day02_03_OpenCV_Image_Processing",
        anchor="まず図で考えましょう",
        folder="diagrams", image="teach_distance_345.png",
        title_ja="2 点の距離は斜辺", title_en="the distance is a hypotenuse",
        caption_ja="図：dx=300, dy=400, 距離=500 px の直角三角形（すべて計算値）。",
        caption_en="Figure: a right triangle with dx = 300, dy = 400 and a distance of 500 px "
                   "(all computed).",
        notice_ja="距離は `sqrt(dx² + dy²)` で、Python では `np.hypot(dx, dy)` と書けます。"
                  "画素の距離に単位はありません。mm にするには、別に倍率を掛けます。",
        notice_en="The distance is `sqrt(dx² + dy²)`, or `np.hypot(dx, dy)` in Python. It is in "
                  "pixels and has no physical unit until you multiply by a scale.",
        question_ja="dx=60, dy=80 のとき距離はいくつですか。",
        question_en="What is the distance when dx = 60 and dy = 80?",
    ),
    dict(
        notebook="Day03_01_YOLO_Concepts",
        anchor="確からしさ（confidence）",
        folder="diagrams", image="teach_score_vs_correctness.png",
        title_ja="confidence と正しさは別", title_en="confidence is not correctness",
        caption_ja="図：5 つの検出の confidence と、正解と比べた正しさ（値は例示用）。",
        caption_en="Figure: confidence against correctness for five detections (illustrative values).",
        notice_ja="confidence が高い検出でも間違っていることがあり、低い検出でも正しいことがあります。"
                  "confidence はモデル自身の自信であって、正解ではありません。",
        notice_en="A high-confidence detection can be wrong and a low-confidence one can be right. "
                  "Confidence is the model's own certainty, not ground truth.",
        question_ja="しきい値 0.60 で残る検出のうち、正しくないのはどれですか。",
        question_en="At a threshold of 0.60, which of the surviving detections are wrong?",
    ),
    dict(
        notebook="Day03_02_YOLO_Inference",
        anchor="四角・クラス・confidence を数値で取り出す",
        folder="reference_outputs", image="ref_inference_boxes_table.png",
        title_ja="画像の番号と表の行", title_en="the numbers on the image and the rows in the table",
        caption_ja="図：この研修で実際に保存した検出（5 件）に番号を振り、同じ番号の表の行と並べたもの。"
                   "参考出力（実際の結果）。",
        caption_en="Figure: the five detections actually saved by this course, numbered, next to the "
                   "matching table rows. Reference output — real results.",
        notice_ja="四角の番号と表の行番号は**同じデータ**です。番号が合わないときは、"
                  "保存する前に表を並べ替えたかどうかを疑ってください。表には座標が 4 つ入っているので、"
                  "あとから四角を描き直せます。",
        notice_en="The numbers and the rows come from the **same list**. If they disagree, check "
                  "whether the table was sorted before saving. Four coordinates per row let you "
                  "redraw the boxes later.",
        question_ja="表の 2 行目（person, 0.87）の四角は、画像のどのあたりにありますか。",
        question_en="Where on the image is the box for row 2 (person, 0.87)?",
    ),
    dict(
        notebook="Day03_03_YOLO_Experiments",
        anchor="confidence と正しさは別物",
        folder="diagrams", image="teach_score_vs_correctness.png",
        title_ja="失敗の型を confidence で分ける", title_en="sorting failures by confidence",
        caption_ja="図：confidence と正しさを並べ、しきい値の上・下で失敗がどう分かれるかを見る図"
                   "（値は例示用）。",
        caption_en="Figure: confidence against correctness, showing how failures split above and "
                   "below the threshold (illustrative values).",
        notice_ja="しきい値を下げると「低い confidence の正しい検出」が助かり、"
                  "同時に「低い confidence の誤検出」も入ります。片方だけを消すことはできません。",
        notice_en="Lowering the threshold rescues correct low-confidence detections **and** admits "
                  "wrong low-confidence ones. You cannot remove only one side.",
        question_ja="この 5 件で、しきい値を 0.30 にすると誤検出は何件残りますか。",
        question_en="At a threshold of 0.30, how many wrong detections remain among these five?",
    ),
    dict(
        notebook="Day04_01_YOLO_Dataset_Annotation",
        anchor="3 つの役割",
        folder="diagrams", image="teach_dataset_contact_sheet.png",
        title_ja="データセットの中身を見る", title_en="look inside the dataset",
        caption_ja="図：この研修で実際に使うデータセットの train / val / test の先頭 4 枚ずつ。"
                   "四角はラベルファイルから描いたもの。参考出力（実際のファイル）。",
        caption_en="Figure: the first four images of each split of the dataset this course actually "
                   "uses; boxes are drawn from the label files. Reference output — real files.",
        notice_ja="行ごとに撮り方も欠陥の種類も違います。**枚数と四角の数は別物**です（1 枚に複数の欠陥があり得る）。"
                  "val と test は、学習に使っていないことを目で確かめられる枚数にしてあります。",
        notice_en="Each row looks different, and **images and boxes are different counts** (one image "
                  "can hold several defects). Validation and test are large enough to see that they "
                  "were not trained on.",
        question_ja="train の 4 枚には、四角が全部でいくつありますか。",
        question_en="How many boxes in total are on the four training images shown?",
    ),
    dict(
        notebook="Day04_01_YOLO_Dataset_Annotation",
        anchor="同じ画像が複数の分割に入ると、何が起きるか",
        folder="diagrams", image="teach_leakage_split.png",
        title_ja="フレームで分ける／撮影で分ける", title_en="split by frame or by capture",
        caption_ja="図：実際のデータセット画像 1 枚と、それに 1 画素未満のノイズを加えた「ほぼ同じ画像」。"
                   "フレームで分けると、この 2 枚が train と test に分かれてしまいます。",
        caption_en="Figure: one real dataset image and a copy with sub-pixel noise — two frames that "
                   "a frame-level split would put on opposite sides.",
        notice_ja="ファイル名もハッシュも違うので、名前や md5 の照合では見つかりません。"
                  "**同じ照明・同じ製品・同じ時刻**の画像は、まとめて片側に置いてください。",
        notice_en="Different names and hashes hide the leak from name or md5 checks. Keep images "
                  "from **one lighting setup, one part, one session** on the same side.",
        question_ja="この 2 枚が train と test に分かれたとき、test の成績は実際より良く見えますか、悪く見えますか。",
        question_en="If these two land in train and test, does the test score look better or worse "
                    "than reality?",
    ),
    dict(
        notebook="Day04_02_YOLO_Training",
        anchor="学習の繰り返し",
        folder="diagrams", image="teach_training_update.png",
        title_ja="1 つの batch で起きること", title_en="what one batch does",
        caption_ja="図：予測 → 損失 → 勾配 → 更新 の 1 サイクルと、batch・step・epoch の数え方"
                   "（重みの変化は例示用）。",
        caption_en="Figure: one cycle of forward → loss → backward → update, and how batch, step and "
                   "epoch are counted (weight changes illustrative).",
        notice_ja="1 step で重みはほんの少ししか動きません。だから何度も繰り返します。"
                  "**推論では ① だけを行い、重みは動かしません。**",
        notice_en="One step moves the weights only slightly, which is why the loop repeats. "
                  "**Inference runs only ① and leaves the weights alone.**",
        question_ja="学習画像が 64 枚、batch が 8 枚のとき、1 epoch は何 step ですか。",
        question_en="With 64 training images and a batch of 8, how many steps are in one epoch?",
    ),
    dict(
        notebook="Day05_01_Anomaly_Detection_Concepts",
        anchor="「いつもと違う」を見つける",
        folder="diagrams", image="teach_normal_variation.png",
        title_ja="正常のばらつきと欠陥", title_en="normal variation versus a defect",
        caption_ja="図：正常 4 枚（照明ムラとノイズで少しずつ違う）と、欠陥のある 1 枚の平均値の比較"
                   "（合成画像・計算値）。",
        caption_en="Figure: four good parts that differ through lighting and noise, compared with one "
                   "defective part by mean value (synthetic, computed).",
        notice_ja="正常品どうしでも平均値は動きます。異常検知は「いつもと違う」を測る方法で、"
                  "「決まった範囲の外」を測る規格判定とは別物です。",
        notice_en="Good parts differ from each other too. Anomaly detection measures “unlike the "
                  "others”; a spec measures “outside a fixed limit”. They are different questions.",
        question_ja="この 5 枚のうち、異常検知のスコアがいちばん高くなるのはどれだと思いますか。",
        question_en="Which of these five would get the highest anomaly score, and why?",
    ),
    dict(
        notebook="Day05_01_Anomaly_Detection_Concepts",
        anchor="なぜ「記憶」なのか",
        folder="diagrams", image="teach_memory_bank.png",
        title_ja="メモリバンクと最近傍", title_en="the memory bank and the nearest neighbour",
        caption_ja="図：正常パッチの特徴を貯めたメモリバンクと、2 つのクエリからの距離（2 次元の模式図）。",
        caption_en="Figure: a memory bank of normal-patch features and the distance from two queries "
                   "(a 2-D schematic).",
        notice_ja="覚えているのは**正常だけ**です。異常の見本は要りません。"
                  "スコアは「最も近い正常パッチまでの距離」なので、大きいほど「いつもと違う」と言えます。",
        notice_en="Only **normal** patches are stored; no defect examples are needed. The score is "
                  "the distance to the nearest normal patch, so larger means “less like usual”.",
        question_ja="メモリバンクに異常パッチを入れてしまうと、何が起きますか。",
        question_en="What happens if an abnormal patch gets into the memory bank?",
    ),
    dict(
        notebook="Day05_01_Anomaly_Detection_Concepts",
        anchor="2 種類の出力",
        folder="diagrams", image="teach_score_levels.png",
        title_ja="パッチ・画像・マップは別の出力", title_en="patch, image and map are three outputs",
        caption_ja="図：パッチごとのスコア → 画像 1 枚のスコア → 空間マップ。3 つを分けて読む（値は例示用）。",
        caption_en="Figure: per-patch scores → one image score → the spatial map, read separately "
                   "(illustrative values).",
        notice_ja="画像スコアは「マップの最大値」などの 1 つの数で、しきい値と比べるのはこの数です。"
                  "マップは「どこが高いか」を示す図で、広がっていても画像スコアは上がりません。",
        notice_en="The image score is a single number (for example the map maximum) and it is what "
                  "you compare with the threshold. The map shows *where*; a wide map does not raise "
                  "the image score by itself.",
        question_ja="この図の画像スコア（最大）はいくつで、しきい値 0.50 での判定は OK と NG のどちらですか。",
        question_en="What is the image score (max) here, and is the verdict at 0.50 OK or NG?",
    ),
    dict(
        notebook="Day05_02_PatchCore_Training",
        anchor="PatchCore の「学習」は 1 回だけ",
        folder="diagrams", image="teach_backbone_vs_memory.png",
        title_ja="変わるのはメモリバンクだけ", title_en="only the memory bank changes",
        caption_ja="図：重みを更新しないバックボーンと、データで決まるメモリバンク（模式図）。",
        caption_en="Figure: a frozen backbone and a memory bank determined by the data (schematic).",
        notice_ja="ResNet-18 の重みは 1 つも更新されません。`max_epochs=1` で十分なのはこのためです。"
                  "モデルを良くしたいときは、epoch ではなく**正常画像**を増やす・そろえます。",
        notice_en="No ResNet-18 weight is updated, which is why `max_epochs=1` is enough. To improve "
                  "the model you add or tidy the **normal images**, not the epochs.",
        question_ja="正常画像を 32 枚から 50 枚に増やすと、変わるのはバックボーンとメモリバンクのどちらですか。",
        question_en="If you go from 32 to 50 normal images, which changes: the backbone or the memory "
                    "bank?",
    ),
    dict(
        notebook="Day05_03_YOLO_vs_PatchCore",
        anchor="Part 2　保存された結果を読み込む",
        folder="diagrams", image="teach_evaluation_sequence.png",
        title_ja="評価の順番", title_en="the order of evaluation",
        caption_ja="図：分割 → 学習 → 較正 → 固定 → 評価 → 報告 の順番と、順番を入れ替えたときに"
                   "数字の意味が変わること（模式図）。",
        caption_en="Figure: split → fit → calibrate → freeze → evaluate → report, and how reordering "
                   "changes what the numbers mean (schematic).",
        notice_ja="④ の後にしきい値を動かすと、⑤ の数字は「試験の成績」ではなくなります。"
                  "このノートブックは ⑤ を 1 回だけ行います。",
        notice_en="Moving the threshold after ④ turns ⑤ into something other than a test result. "
                  "This notebook evaluates ⑤ exactly once.",
        question_ja="試験の数字を見てからしきい値を直したとき、その数字を「試験の成績」と呼べますか。",
        question_en="If you adjust the threshold after seeing the test numbers, can you still call "
                    "them a test result?",
    ),
    dict(
        notebook="Day05_03_YOLO_vs_PatchCore",
        anchor="しきい値を動かしてよいのは、較正用データだけ",
        folder="diagrams", image="teach_threshold_freeze.png",
        title_ja="較正で決めて、固定する", title_en="choose on calibration, then freeze",
        caption_ja="図：較正用データのスコアと、候補ごとの見逃し・誤報。緑の線が固定したしきい値"
                   "（値は例示用。この研修の固定値は YOLO 0.06、PatchCore 0.50）。",
        caption_en="Figure: calibration scores with the misses and false alarms at each candidate; "
                   "the green line is the frozen threshold (illustrative values; this course froze "
                   "YOLO at 0.06 and PatchCore at 0.50).",
        notice_ja="誤報（FP）と見逃し（FN）は**同時にしか動かないわけではありません**。"
                  "分布に隙間があれば、両方を 0 にできるしきい値が存在します。"
                  "この研修の較正用データでは、0.50 で両方 0 になりました。"
                  "隙間が無いデータでは、どちらかを犠牲にするしかありません。",
        notice_en="False alarms and misses do **not** always move together: when the two distributions "
                  "have a gap, a threshold exists that gives zero for both — as 0.50 did on this "
                  "course's calibration data. Without a gap you must trade one for the other.",
        question_ja="しきい値を 0.70 にすると、PatchCore の見逃しは何枚になりますか。",
        question_en="At a threshold of 0.70, how many PatchCore misses are there?",
    ),
]


def _notebook(stem: str) -> Path:
    matches = sorted(NOTEBOOK_DIR.rglob(f"{stem}.ipynb"))
    if len(matches) != 1:
        raise SystemExit(f"{stem}: expected exactly one notebook, found {len(matches)}")
    return matches[0]


def _cell_id(entry: dict) -> str:
    """セル ID は画像名から決める（何度実行しても同じ）/ deterministic cell id from the image name."""
    return "fig-" + Path(entry["image"]).stem


def _markdown(entry: dict) -> str:
    target = f"../../assets/{entry['folder']}/{entry['image']}"
    return (
        f"### {entry['title_ja']} / {entry['title_en']}\n\n"
        f"![]({target})\n\n"
        f"{entry['caption_ja']}\n\n"
        f"{entry['caption_en']}\n\n"
        f"**気づいてほしいこと**\n\n"
        f"{entry['notice_ja']}\n\n"
        f"**What to notice**\n\n"
        f"{entry['notice_en']}\n\n"
        f"**考えてみてください / Try to answer**\n\n"
        f"- {entry['question_ja']}\n"
        f"- {entry['question_en']}\n"
    )


def _referenced_images(nb: dict) -> set[str]:
    found = set()
    for cell in nb["cells"]:
        if cell["cell_type"] != "markdown":
            continue
        for target in IMAGE_RE.findall("".join(cell["source"])):
            found.add(Path(target).name)
    return found


def _owned(cell: dict, entry: dict) -> bool:
    """このスクリプトが書いたセルか / whether this script wrote the cell."""
    if cell.get("id") == _cell_id(entry):
        return True
    source = "".join(cell["source"])
    return (not cell.get("metadata")
            and source.startswith("### ")
            and "気づいてほしいこと" in source
            and "What to notice" in source)


def _find(nb: dict, image: str) -> int | None:
    for index, cell in enumerate(nb["cells"]):
        if cell["cell_type"] != "markdown":
            continue
        if image in IMAGE_RE.findall("".join(cell["source"])) or any(
            Path(target).name == image for target in IMAGE_RE.findall("".join(cell["source"]))
        ):
            return index
    return None


def _update(nb: dict, entry: dict) -> bool:
    """既にある図の説明を最新にする（重複は作らない）。"""
    index = _find(nb, entry["image"])
    if index is None:
        return False
    cell = nb["cells"][index]
    if not _owned(cell, entry):
        return False                       # 手書きのセルは触らない / never rewrite hand-written cells
    block = _markdown(entry)
    if "".join(cell["source"]) == block:
        return False
    cell["source"] = block.splitlines(keepends=True)
    return True


def _insert(nb: dict, entry: dict, after: int | None = None) -> int | None:
    """見出しセルの直後（``before`` なら直前）に差し込む / insert after (or before) the heading cell.

    ``after`` が与えられたときは、その位置の直後に入れます（同じ見出しに複数の図を並べるため）。
    ``after`` lets a second figure follow the first one instead of jumping ahead of it.
    """
    if after is not None:
        nb["cells"].insert(after + 1, {
            "cell_type": "markdown",
            "id": _cell_id(entry),
            "metadata": {},
            "source": _markdown(entry).splitlines(keepends=True),
        })
        return after + 1

    anchor = entry["anchor"]
    before = bool(entry.get("before"))
    for index, cell in enumerate(nb["cells"]):
        if cell["cell_type"] != "markdown":
            continue
        if anchor not in "".join(cell["source"]):
            continue
        position = index if before else index + 1
        nb["cells"].insert(position, {
            "cell_type": "markdown",
            "id": _cell_id(entry),
            "metadata": {},
            "source": _markdown(entry).splitlines(keepends=True),
        })
        return position
    return None


def _remove(nb: dict, images: set[str]) -> int:
    """このスクリプトが入れたセルを取り除く / drop cells this script inserted."""
    kept, removed = [], 0
    for cell in nb["cells"]:
        if cell["cell_type"] == "markdown" and not cell.get("metadata"):
            targets = {Path(t).name for t in IMAGE_RE.findall("".join(cell["source"]))}
            if targets and targets <= images:
                removed += 1
                continue
        kept.append(cell)
    nb["cells"] = kept
    return removed


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Insert teaching figures into notebook Markdown.")
    parser.add_argument("--check", action="store_true", help="report only; write nothing")
    parser.add_argument("--remove", action="store_true", help="remove the cells this script inserted")
    args = parser.parse_args(argv)

    images = {entry["image"] for entry in FIGURES}
    changed_total = 0
    problems = []
    per_notebook: dict[str, list[dict]] = {}
    for entry in FIGURES:
        per_notebook.setdefault(entry["notebook"], []).append(entry)

    for stem, entries in per_notebook.items():
        path = _notebook(stem)
        nb = json.loads(path.read_text(encoding="utf-8"))
        if args.remove:
            removed = 0 if args.check else _remove(nb, images)
            if not args.check:
                path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"{stem}: removed={removed}")
            continue

        present = _referenced_images(nb)
        cursor: dict[str, int] = {}
        changed = 0
        updated = 0
        for entry in entries:
            if entry["image"] in present:
                if _update(nb, entry):
                    updated += 1
                continue
            if not (COURSE_ROOT / "assets" / entry["folder"] / entry["image"]).is_file():
                problems.append(f"{stem}: missing asset {entry['folder']}/{entry['image']}")
                continue
            position = _insert(nb, entry, after=cursor.get(entry["anchor"]))
            if position is None:
                problems.append(f"{stem}: anchor not found -> {entry['anchor']!r}")
                continue
            cursor[entry["anchor"]] = position
            present.add(entry["image"])
            changed += 1
        if (changed or updated) and not args.check:
            path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{stem}: inserted={changed} updated={updated} "
              f"(already present={len(entries) - changed})")
        changed_total += changed

    if problems:
        print("\n問題 / problems:")
        for problem in problems:
            print("  -", problem)
        return 1
    print(f"\n{'would insert' if args.check else 'inserted'}: {changed_total} figure block(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
