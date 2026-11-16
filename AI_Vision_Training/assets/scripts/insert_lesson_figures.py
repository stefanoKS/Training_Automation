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
from course_notebooks import course_notebooks

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
        folder="diagrams",
        image="teach_setup_workflow.png",
        title_ja="手順の全体像",
        title_en="the five steps at a glance",
        caption_ja="図：ノートブックを開いてから、エラーから戻るまでの流れ（模式図）。① セルを選ぶ → ② カーネルを選ぶ → ③ 実行する → ④ 出力を見る。エラーが出たときだけ ⑤ の復旧へ分かれます。",
        caption_en="Figure: the flow from opening a notebook to recovering from an error (schematic). ① choose a cell → ② choose the kernel → ③ run it → ④ read the output; only when an error appears do you branch to ⑤ recovery.",
        notice_ja="矢印は「実行 → 出力を見る」の順につながっています。復旧（⑤）は、**実行してエラーが出た後**の分かれ道です。出力を読まないまま次のセルへ進まないでください。",
        notice_en="The arrows follow run → read the output. Recovery (⑤) is a branch taken **after** a run produced an error. Do not move on without reading the output.",
        question_ja="③ の実行でエラーが出たとき、④ と ⑤ のどちらへ進みますか。",
        question_en="When ③ produces an error, do you go to ④ or to ⑤?",
    ),
    dict(
        notebook="Day01_01_Introduction_to_AI",
        anchor="3 つの言葉の関係",
        folder="diagrams",
        image="teach_train_vs_inference.png",
        title_ja="学習と推論は別の作業",
        title_en="training and inference are different jobs",
        caption_ja="図：学習（fitting）と推論（applying）の違い（模式図）。学習はモデルの重みを例から決める作業、推論はその重みをそのまま使って新しい画像を判定する作業です。",
        caption_en="Figure: training (fitting) versus inference (applying) — a schematic. Training determines the weights from examples; inference uses those weights unchanged to judge new images.",
        notice_ja="回数や速さは**典型的な例**であって、定義ではありません。学習をやり直すことも、推論をまとめて大量に行うこともあります。推論で変わるのは判定だけで、重みは変わりません。しきい値は重みとは別に決める値で、変えても重みは更新されません。",
        notice_en="Frequency and speed are **typical examples**, not definitions: you can retrain, and you can run batch inference. Inference changes decisions, not weights. The threshold is chosen separately from the weights, so changing it updates no weight.",
        question_ja="しきい値を変えたとき、学習し直す必要はありますか。",
        question_en="When you change the threshold, do you need to retrain?",
    ),
    dict(
        notebook="Day02_02_Conditions_Loops_Functions",
        anchor="もし〜なら」を書く",
        folder="diagrams",
        image="teach_condition_branch.png",
        title_ja="条件で処理を分ける流れ",
        title_en="how a condition splits the work",
        caption_ja="図：測定値 12.14 mm を条件 11.8 ≤ x ≤ 12.2 に通したときの流れと、4 つの値を実際に当てはめた結果（模式図）。",
        caption_en="Figure: one measurement (12.14 mm) passed through the condition 11.8 ≤ x ≤ 12.2, and four real values applied to it (schematic).",
        notice_ja="分かれるのは表示する文字だけで、条件は 1 つです。境界値 12.20 mm は「以内」なのでOK になります。**入力値を変える**のと、**規格を変える**のは別の操作です。",
        notice_en="Only the message differs; there is one condition. The boundary 12.20 mm is inside the limit, so it passes. **Changing the input** and **changing the specification** are different actions.",
        question_ja="規格を変えずに 12.30 mm を OK にする方法はありますか。",
        question_en="Without changing the specification, can 12.30 mm be made to pass?",
    ),
    dict(
        notebook="Day03_01_YOLO_Concepts",
        anchor="バウンディングボックス / Bounding boxes",
        folder="diagrams",
        image="teach_bbox_coords.png",
        title_ja="四角を画像の上で読む",
        title_en="reading a box on the image",
        caption_ja="図：同じ 1 つの欠陥の四角を、画素の数（左）と画像サイズで割った値（右）で表したもの。座標は計算して図に描いています。",
        caption_en="Figure: one defect box written as pixel counts (left) and as fractions of the image size (right). The coordinates are computed and drawn, not sketched.",
        notice_ja="左は画素の xyxy、右は画像サイズで割った cx, cy, w, h で、**同じ箱**です。画像全体の縮小・拡大では 0〜1 の値は意味を保ちますが、切り抜き（crop）や余白の追加（letterbox）では座標が変わります。API ごとに形式が違うので名前を確認します（Ultralytics の `xyxy`、OpenCV の `boundingRect` は xywh）。",
        notice_en="The left is pixel xyxy; the right is cx, cy, w, h divided by the image size — **the same box**. Resizing the whole image keeps the 0–1 values meaningful, but cropping or letterbox padding changes the coordinates. Formats differ by API (Ultralytics `xyxy`; OpenCV `boundingRect` is xywh).",
        question_ja="画像の左半分だけを切り抜いたとき、もとの cx = 0.6 の箱はどうなりますか。",
        question_en="If you crop the left half of the image, what happens to a box with cx = 0.6?",
    ),
    dict(
        notebook="Day03_03_YOLO_Experiments",
        anchor="confidence のしきい値 / The confidence threshold",
        folder="diagrams",
        image="teach_confidence_filter.png",
        title_ja="しきい値で残る数が変わる",
        title_en="the threshold changes how many are kept",
        caption_ja="図：同じ 1 回の推論で得た 4 つの候補を、しきい値 0.25・0.50・0.75 で絞った結果（合成画像・例示用の値）。",
        caption_en="Figure: the same four candidates from one inference pass, filtered at 0.25, 0.50 and 0.75 (synthetic image, illustrative values).",
        notice_ja="残る数は 3 → 1 → 1 です。しきい値を上げても**数が変わらない**ことがある、というのがこの図の要点です。捨てた候補は「存在しない」のではなく「採用しない」だけです。",
        notice_en="The counts are 3 → 1 → 1: raising the threshold can leave the count unchanged. Discarded candidates are not nonexistent; they are simply not retained.",
        question_ja="0.50 と 0.75 で残る数が同じなのはなぜですか。",
        question_en="Why is the count the same at 0.50 and 0.75?",
    ),
    dict(
        notebook="Day03_03_YOLO_Experiments",
        anchor="confidence のしきい値 / The confidence threshold",
        folder="reference_outputs",
        image="ref_confidence_counts.png",
        title_ja="実際の結果で数える",
        title_en="counted on the real results",
        caption_ja="図：この研修で実際に保存した推論結果（52 枚）のうち、候補が残った 42 枚について、しきい値を変えたときに NG と判定される枚数を数えたもの。右は画像ごとの最大 confidence。参考出力（実際の結果）。",
        caption_en="Figure: among the 52 images actually saved by this course, the 42 that kept a candidate, counted as NG at each threshold. Right: each image's highest confidence. Reference output — real results.",
        notice_ja="推論は conf = 0.01 で 1 回だけ行いました。**検出が 1 件も残らなかった 10 枚**は候補が無いので、どのしきい値でも NG になりません（保存されている 0 は「弱い検出」ではなく目印の値です）。0.01 で 42 枚、0.25 で 28 枚、0.50 で 23 枚、0.75 で 13 枚です。",
        notice_en="Inference ran once at conf = 0.01. The **10 images that kept no box** have no candidate, so no threshold turns them into NG; their stored 0 is a sentinel, not a weak detection. Counts: 42 at 0.01, 28 at 0.25, 23 at 0.50, 13 at 0.75.",
        question_ja="しきい値を 0.01 から 0.25 に上げると NG は何枚減りますか。減った画像を「欠陥なし」と断定できますか。",
        question_en="Raising the threshold from 0.01 to 0.25 removes how many NG calls — and can you call those images defect-free?",
    ),
    dict(
        notebook="Day03_03_YOLO_Experiments",
        anchor="解像度と小さな物体 / Resolution and small objects",
        folder="diagrams",
        image="teach_resolution_effect.png",
        title_ja="解像度が欠陥の見え方を決める",
        title_en="resolution decides how a defect looks",
        caption_ja="図：同じ合成画像を縮小したときの、欠陥の見え方と中心画素の差（計算値）。",
        caption_en="Figure: how the defect looks, and the computed difference at the centre pixel, as one synthetic image is shrunk.",
        notice_ja="1 画素より小さい欠陥でも、その画素の明るさは変わり得ます。ただし形や位置を安定して判断できるとは限りません。視野・補間・残ったコントラストを分けて読みます。",
        notice_en="A defect smaller than one pixel can still change that pixel's intensity, but its shape and position may not be reliably resolved. Read field of view, resampling and the remaining contrast separately.",
        question_ja="0.5 px の欠陥でも、しきい値で検出できる場合があるのはなぜですか。",
        question_en="Why can a 0.5 px defect still be detected by a threshold?",
    ),
    dict(
        notebook="Day04_02_YOLO_Training",
        anchor="read training and validation loss separately",
        folder="reference_outputs",
        image="ref_train_val_curves.png",
        title_ja="学習ログを 2 本の線で読む",
        title_en="reading the training log as two lines",
        caption_ja="図：この研修で実際に行った短い学習（15 epoch, CPU）の記録。左は学習・検証の cls 損失、右は mAP50 と precision。保存された学習ログそのものです。",
        caption_en="Figure: the short training run actually performed in this course (15 epochs, CPU). Left: train and val cls loss. Right: mAP50 and precision. This is the saved log.",
        notice_ja="読むのは絶対値より「両方が下がり続けるか」「差が開き続けないか」です。数 epoch の横ばいだけで過学習とは言えません。損失の列名は YOLO26 の実際の出力です（`train/l1_loss`・`val/l1_loss` があり、`dfl_loss` はありません）。",
        notice_en="Read whether both curves keep falling and whether the gap keeps widening, not a single value. A few flat epochs are not proof of overfitting. The loss columns are YOLO26's actual outputs (`train/l1_loss`, `val/l1_loss`; there is no `dfl_loss`).",
        question_ja="最後の 3 epoch で、mAP50 は上がっていますか、横ばいですか。",
        question_en="In the last three epochs, is mAP50 rising or flat?",
    ),
    dict(
        notebook="Day04_03_YOLO_Evaluation",
        anchor="画像単位の TP・FP・FN・TN / image-level TP, FP, FN and TN",
        folder="diagrams",
        image="teach_object_level_matching.png",
        title_ja="物体単位の対応づけ",
        title_en="matching objects one to one",
        caption_ja="図：物体単位の対応づけ。正解の四角と予測の四角を IoU で 1 対 1 に対応させ、対応しない予測を FP として数えます（座標は例示用）。",
        caption_en="Figure: object-level matching. Truth and predicted boxes are paired one to one by IoU; a prediction with no partner counts as a false positive (illustrative coordinates).",
        notice_ja="物体単位では、対象クラス・IoU（この研修では 0.5 以上）・confidence・1 対 1 の対応づけのルールを先に決めます。対応しない予測は FP、対応しない正解は FN です。画像単位の OK/NG は別の計算で、「対象クラスの検出が 1 つ以上あれば NG」のように決めます。",
        notice_en="Object level needs a stated policy: target class, IoU, confidence and one-to-one assignment. An unmatched prediction is an FP; an unmatched ground-truth object is an FN. The image-level OK/NG decision is a separate rule, for example \"NG if at least one target-class detection is retained\".",
        question_ja="同じ箱が 2 回予測されたら、物体単位ではどう数えますか。",
        question_en="If the same box is predicted twice, how is it counted at object level?",
    ),
    dict(
        notebook="Day04_03_YOLO_Evaluation",
        anchor="自分の目で確認する",
        folder="reference_outputs",
        image="ref_detections_label_vs_pred.png",
        title_ja="正解と予測を同じ並びで見る",
        title_en="truth and prediction in the same order",
        caption_ja="図：同じバッチの 8 枚を、正解（左）と予測（右）で並べた実際の出力。正解はこの研修の生成スクリプトが欠陥記録から作った四角、予測は学習したモデルの四角です。",
        caption_en="Figure: the eight images of one batch as ground truth (left) and prediction (right). The labels come from this course's generator using the defect records; the predictions come from the trained model.",
        notice_ja="右に無くて左にある画像が見逃し（FN）の候補です。逆に右だけに増えた四角は、対応づけのルール（クラス・IoU・confidence）で FP かどうかを決めます。見た目だけで断定しません。",
        notice_en="Images with a left box but no right box are miss (FN) candidates. An extra box on the right is judged by the matching rule (class, IoU, confidence) before calling it an FP; appearance alone does not settle it.",
        question_ja="見逃し（FN）は何枚ありますか。その画像の欠陥は予測の列でどう見えていますか。",
        question_en="How many images contain a miss (FN), and how does that defect look in the prediction column?",
    ),
    dict(
        notebook="Day05_03_YOLO_vs_PatchCore",
        anchor="Choose the thresholds on the calibration partition",
        folder="reference_outputs",
        image="ref_score_distribution.png",
        title_ja="較正用データの分布",
        title_en="the distribution on calibration data",
        caption_ja="図：較正用（validation）データだけのスコア分布と、そこから決めたしきい値 0.50（保存値の 0〜1 スケール）。試験用データは含みません。",
        caption_en="Figure: the score distribution on the calibration (validation) partition only, with the threshold 0.50 chosen there, on the saved 0–1 scale. The test partition is not included.",
        notice_ja="スコアは anomalib 2.7.0 の後処理で `clip((生の値 − しきい値) ÷ (較正の最大 − 最小) + 0.5, 0, 1)` に変換されており、**学習したしきい値が 0.5** になります。較正は正常 6 枚・異常 20 枚です。6 枚で誤報 0 件は「本番でも 0 件」の保証ではありません。",
        notice_en="anomalib 2.7.0's post-processing maps the score with `clip((raw − threshold) / (cal_max − cal_min) + 0.5, 0, 1)`, so the **learned threshold becomes 0.5**. Calibration holds 6 normal and 20 abnormal images; zero false alarms in six does not guarantee zero in production.",
        question_ja="しきい値を 0.60 にすると、この較正データでは見逃しが何枚増えますか。",
        question_en="At a threshold of 0.60, how many misses appear on this calibration data?",
    ),
    dict(
        notebook="00_Environment_Setup",
        anchor="Jupyter ノートブック・セル・カーネル",
        folder="diagrams",
        image="teach_setup_jupyter_ui.png",
        title_ja="画面の部品と名前",
        title_en="the parts of the screen and their names",
        caption_ja="図：ノートブック・セル・カーネル・出力の位置関係（模式図。実際の画面写真ではありません）。",
        caption_en="Figure: where the notebook, the cells, the kernel and the output sit (schematic, not a screenshot).",
        notice_ja="セルは「文字を書く場所」、カーネルは「計算する別のプログラム」です。Markdown セルもコードセルも**編集はできます**。違うのは実行したときの働きです。カーネルを選び直してもセルの文字は消えませんが、再起動すると計算した変数は消えます。",
        notice_en="A cell is where the text lives; the kernel is a separate program that computes. Both Markdown and code cells **can be edited**; what differs is what running them does. Choosing another kernel keeps your text, while a restart discards the variables.",
        question_ja="カーネルを再起動したとき、消えるのはセルの文字と変数のどちらですか。",
        question_en="After a kernel restart, which disappears: the cell text or the variables?",
    ),
    dict(
        notebook="00_Environment_Setup",
        anchor="Part 5　最初の Python プログラム",
        folder="diagrams",
        image="teach_execution_state.png",
        title_ja="実行前・実行中・実行後の状態",
        title_en="before, during and after a run",
        caption_ja="図：同じ 3 行のセルを、実行前・実行中・実行後に分けて、メモリの中身と一緒に示したもの（模式図）。",
        caption_en="Figure: the same three-line cell before, during and after a run, together with what is in memory (schematic).",
        notice_ja="`In [ ]` は「このセルをまだ実行していない」という意味で、メモリが空という意味ではありません。`In [*]` は実行中で、その間に出力が流れることもあります。数字は実行済みです。表示された出力と、変数として残る値は別物です。前の実行の値が残る状態（stale state）と、名前がまだ無い状態（NameError）は、別の困りごとです。",
        notice_en="`In [ ]` means \"this cell has not run yet\"; it does **not** mean an empty memory. `In [*]` means running, and output may stream meanwhile. A number means finished. Displayed output and the values kept in variables are different things. Leftover state from an earlier run and a name that has never existed (NameError) are two different problems.",
        question_ja="変数を定義したセルをまだ一度も実行していないとき、その変数を使うセルでは何が起きますか。",
        question_en="If the cell that defines a variable has never been run, what happens in a cell that uses that variable?",
    ),
    dict(
        notebook="00_Environment_Setup",
        anchor="エラーメッセージを読む練習",
        folder="diagrams",
        image="teach_nameerror_recovery.png",
        title_ja="NameError から戻る手順",
        title_en="recovering from a NameError",
        caption_ja="図：`widht_mm` と `width_mm` を書き間違えたときのエラーと、直す順番（模式図）。",
        caption_en="Figure: the error you get when `widht_mm` and `width_mm` are mixed up, and the order for fixing it (schematic).",
        notice_ja="`NameError` は「その名前がまだ無い」という意味です。定義したセルより先に使った、綴りが違う、カーネルを再起動して変数が消えた、のどれかです。上のセルから順に実行し直すのが基本の復旧です。",
        notice_en="`NameError` means the name does not exist yet: it was used before the cell that defines it, the spelling differs, or a kernel restart removed the variables. The basic recovery is to run the cells again from the top.",
        question_ja="カーネルを再起動した直後、`width_mm` は使えますか。",
        question_en="Immediately after a kernel restart, can you use `width_mm`?",
    ),
    dict(
        notebook="Day01_01_Introduction_to_AI",
        anchor="自動化＝同じ手順を機械に繰り返させる",
        folder="diagrams",
        image="teach_inspection_roles.png",
        title_ja="検査の 4 つの段階（簡略化した流れ）",
        title_en="the four stages of inspection (a simplified pipeline)",
        caption_ja="図：検査を「撮る → 画素値から寸法・特徴を取り出す → 決める → 動かす」の 4 段階に分けた簡略図（模式図）。AI が使える範囲の境界を示したものではありません。",
        caption_en="Figure: inspection split into four stages — capture → extract dimensions and features from pixel values → decide → act (schematic). It is not a boundary of where AI can be used.",
        notice_ja="この 4 段階は**説明のための簡略化**です。AI は「決める」だけでなく、寸法や特徴の推定、領域の抽出にも使えます。画素にはすでに数値が入っているので、「画素が数値になる」のではなく「画素値から寸法・特徴を取り出す」と考えます。撮像が悪いと、モデルを変えても救えないことが多いのも事実です。",
        notice_en="This is a **simplified explanation**. AI can help with estimating dimensions and features or extracting regions, not only with deciding. A pixel already holds numbers, so we extract dimensions and features from pixel values rather than \"turning pixels into numbers\". Poor imaging often cannot be rescued by a different model.",
        question_ja="4 段階のうち、AI を使えるのは ③ だけですか。",
        question_en="Is ③ the only stage where AI can be used?",
    ),
    dict(
        notebook="Day01_01_Introduction_to_AI",
        anchor="3 つの言葉の関係",
        folder="diagrams",
        image="teach_ai_ml_dl_nested.png",
        title_ja="AI・機械学習・深層学習の入れ子",
        title_en="how the three words nest",
        caption_ja="図：AI ⊃ 機械学習 ⊃ 深層学習 の包含関係と、それぞれの例（模式図）。",
        caption_en="Figure: AI ⊃ machine learning ⊃ deep learning, with an example of each (schematic).",
        notice_ja="入れ子は 深層学習 ⊂ 機械学習 ⊂ AI のままです。人が書いた if 文だけの判定は「普通の自動化」で、AI とは呼びません。ルールベースの AI には、専門家の知識をif 文の形で書いたエキスパートシステムもあります。機械学習かどうかを分けるのは「ルールを人が書いたか、例から決めたか」です。決定木のように、学習した結果をif 文で書ける場合もあります。",
        notice_en="The nesting stays deep learning ⊂ machine learning ⊂ AI. A decision written as a hand-made if-statement is ordinary automation, not AI. Rule-based AI includes expert systems, where an expert's knowledge is written as if-rules. What separates machine learning is whether a person wrote the rule or the examples determined it; a learned decision tree can itself be written as if-rules.",
        question_ja="「幅が 100±0.5 mm なら OK」という if 文は、AI・機械学習・普通の自動化のどれですか。",
        question_en="The rule \"width within 100 ± 0.5 mm is OK\" written as an if-statement is which of AI, machine learning, ordinary automation?",
    ),
    dict(
        notebook="Day01_01_Introduction_to_AI",
        anchor="しきい値をデータから決める",
        before=True,
        folder="diagrams",
        image="teach_gaussian_vs_skewed.png",
        title_ja="左右対称と正規分布は同じではない",
        title_en="symmetric is not the same as Gaussian",
        caption_ja="図：左右対称だが正規分布ではない分布（左）と、正規分布（右）の比較（模式図）。",
        caption_en="Figure: a symmetric distribution that is not Gaussian (left) next to a Gaussian distribution (right) — schematic.",
        notice_ja="左右対称であることは、正規分布であることを意味しません。正規分布では、母平均 μ から母標準偏差 σ の 3 倍以内に約 99.73% の値が入ります。ただし、限られた正常画像から推定した平均・標準偏差では、実際の割合はこの値と一致するとは限りません。",
        notice_en="Symmetry alone does not make a distribution Gaussian. For a Gaussian distribution about 99.73 % of values lie within three population standard deviations of the population mean. With a mean and standard deviation estimated from a few normal images, the observed proportion need not match that number.",
        question_ja="この左右対称な分布で、μ±3σ の外側が 0.27% より多くなるのはなぜですか。",
        question_en="Why can the outside of μ ± 3σ hold more than 0.27 % in this symmetric distribution?",
    ),
    dict(
        notebook="Day01_02_Pixels_and_Images",
        anchor="原点は左上、y は下向き",
        folder="diagrams",
        image="teach_array_indexing.png",
        title_ja="配列の添字とスライス",
        title_en="indexing and slicing an array",
        caption_ja="図：`image[1:4]` が選ぶ行。行インデックス 1・2・3 は、上から 2〜4 行目です（模式図）。",
        caption_en="Figure: the rows selected by `image[1:4]`. Row indices 1, 2 and 3 are the second to fourth rows from the top (schematic).",
        notice_ja="画像の添字は 0 から始まります。`image[1:4]` は「1 行目から 3 行目」ではなく「行インデックス 1・2・3」、つまり上から 2〜4 行目です。`image[1:4, 2:5]` のように行と列を並べて指定します。",
        notice_en="Image indices start at 0. `image[1:4]` means row indices 1, 2 and 3 — the second to fourth rows — not \"rows 1 to 3\". Rows and columns are written together, as in `image[1:4, 2:5]`.",
        question_ja="上から 1 行目だけを選ぶには、どう書きますか。",
        question_en="How do you select only the first row from the top?",
    ),
    dict(
        notebook="Day01_02_Pixels_and_Images",
        anchor="縮小すると何が起きるか",
        folder="diagrams",
        image="teach_resize_profile.png",
        title_ja="同じ領域を 3 つの解像度で比べる",
        title_en="one region at three resolutions",
        caption_ja="図：この例の合成画像を縮小したときの、欠陥を通る断面の明るさ（実測値）。横軸は位置、縦軸は 0〜255 の画素値です。",
        caption_en="Figure: measured brightness along a profile through the defect when this synthetic image is shrunk. The horizontal axis is position; the vertical axis is the pixel value, 0–255.",
        notice_ja="この図が示すのは**この例で測った値**です。「縮小すると必ず浅く広くなる」という規則ではありません。補間の方法、欠陥の大きさ、背景との差で変わります。縦軸の単位と、どこを断面にしたかを確認してください。",
        notice_en="The figure shows **the values measured in this example**, not a rule that shrinking always makes a defect shallower and wider: the resampling method, the defect size and the contrast with the background all matter. Check the axis unit and where the profile was taken.",
        question_ja="縮小しても暗さの最小値がほとんど変わらないのは、どんなときだと思いますか。",
        question_en="When would the darkest value barely change even after downsampling?",
    ),
    dict(
        notebook="Day01_03_Computer_Vision_Tasks",
        anchor="セマンティックセグメンテーション",
        folder="diagrams",
        image="teach_segmentation_modes.png",
        title_ja="意味とインスタンスの違い",
        title_en="semantic versus instance",
        caption_ja="図：同じ 2 つの欠陥を、意味セグメンテーション（1 つのクラスにまとめる）とインスタンスセグメンテーション（1 つずつ番号を付ける）で表したもの（合成画像）。",
        caption_en="Figure: the same two defects under semantic segmentation (one class) and instance segmentation (numbered one by one) — synthetic image.",
        notice_ja="セマンティックセグメンテーションは画素ごとのクラスを返すので、同じクラスの領域が離れていても数えられます。区別が必要なのは**接している個体**です。その場合はインスタンスセグメンテーションを使います。",
        notice_en="Semantic segmentation returns a class per pixel, so separated regions of the same class can still be counted. What needs a different method is **touching instances**, which is what instance segmentation separates.",
        question_ja="接していない 2 つの黒い汚れは、セマンティックセグメンテーションで 2 つとして数えられますか。",
        question_en="Can two separated dark marks be counted as two with semantic segmentation?",
    ),
    dict(
        notebook="Day02_01_Python_Basics",
        anchor="数値の種類と四則演算",
        folder="diagrams",
        image="teach_units_conversion.png",
        title_ja="寸法と単位換算",
        title_en="dimensions and unit conversion",
        caption_ja="図：単位の換算と、コンピュータの中の数の表し方（模式図）。上段が物理単位、下段が 2 進数の近似と丸めの方針です。",
        caption_en="Figure: unit conversion and how a computer stores numbers (schematic). The upper row is physical units; the lower row is binary approximation and rounding policy.",
        notice_ja="3 つを分けて考えます。① 物理単位（mm・px）の換算、② 2 進数で表せない数の近似（0.1 + 0.2 は 0.3 にならない）、③ 規格の判定でどこを四捨五入するか。②は計算の性質、③は会社のルールです。",
        notice_en="Keep three things apart: ① physical unit conversion (mm, px); ② approximation of numbers that have no exact binary form (`0.1 + 0.2` is not `0.3`); ③ where the inspection rounds before comparing with the limit. ② is a property of arithmetic; ③ is a company rule.",
        question_ja="0.1 + 0.2 が 0.3 にならないのは、単位の換算のせいですか、数の表し方のせいですか。",
        question_en="Is `0.1 + 0.2 != 0.3` caused by unit conversion or by how numbers are stored?",
    ),
    dict(
        notebook="Day02_01_Python_Basics",
        anchor="比較演算子",
        folder="diagrams",
        image="teach_assign_vs_compare.png",
        title_ja="`=` と `==` は別の操作",
        title_en="`=` and `==` are different operations",
        caption_ja="図：代入（値を入れる）と比較（真偽を聞く）の違いと、実際に計算した 4 つの結果。",
        caption_en="Figure: assignment (store a value) versus comparison (ask for a truth value), with four computed answers.",
        notice_ja="`=` は「右側の値を名前につける」文で、それ自体は値を表示しません（値を返すのは `:=` の代入式です）。`==` は「等しいか」を判定して True / False を返します。",
        notice_en="`=` binds the value on the right to a name and displays nothing by itself (the assignment expression `:=` is the form that returns a value). `==` compares and returns True or False.",
        question_ja="`a = 5` を実行しても何も表示されないのはなぜですか。",
        question_en="Why does running `a = 5` display nothing?",
    ),
    dict(
        notebook="Day02_01_Python_Basics",
        anchor="よく出るエラー 4 種類",
        folder="diagrams",
        image="teach_traceback_annotated.png",
        title_ja="traceback の読み方",
        title_en="how to read a traceback",
        caption_ja="図：0 で割ったときの traceback を、どこを読むかの順番つきで示したもの（模式図）。",
        caption_en="Figure: a division-by-zero traceback, annotated with the order to read it (schematic).",
        notice_ja="この例は**Python の普通の数値の割り算**を 0 で割ったときのエラーです。言語や数値の種類によっては例外にならず、`inf` や `nan` になることもあります（NumPy の配列演算など）。「どの言語でも必ず失敗する」とは限りません。",
        notice_en="This example is an error from dividing ordinary Python numbers by zero. Other languages, or other numeric types such as NumPy array arithmetic, may return `inf` or `nan` instead of raising, so it is not true that \"every language fails\".",
        question_ja="NumPy で `1.0 / 0.0` を計算すると、例外と `inf` のどちらになりますか。",
        question_en="With NumPy, does `1.0 / 0.0` raise an exception or produce `inf`?",
    ),
    dict(
        notebook="Day02_02_Conditions_Loops_Functions",
        anchor="`if` で「もし〜なら」を書く",
        folder="diagrams",
        image="teach_tolerance_boundary.png",
        title_ja="規格の境界は「含む」か",
        title_en="are the bounds inclusive",
        caption_ja="図：12.0 ± 0.2 mm の境界と、実際に比較した 5 つの値の判定。境界 12.200 mm は「以内」なので OK。",
        caption_en="Figure: the bounds of 12.0 ± 0.2 mm and the verdict for five compared values; 12.200 mm is inside because the bounds are inclusive.",
        notice_ja="規格が「11.8 以上 12.2 以下」と書かれているとき、境界そのものは含みます（以内）。含めるか含めないかは**規格の書き方**で決まり、プログラムでは `<=` と `<` が対応します。測定値の分解能と、判定前の丸めの方針も先に決めておきます。",
        notice_en="When the limit reads \"11.8 or more and 12.2 or less\", the boundary itself is included. Whether it is included is decided by **how the specification is written**, and `<=` versus `<` expresses that. Decide the measurement resolution and the rounding policy before judging.",
        question_ja="12.2005 mm を小数 3 桁に丸めてから判定すると、結果はどう変わりますか。",
        question_en="If 12.2005 mm is rounded to three decimals before judging, how does the result change?",
    ),
    dict(
        notebook="Day02_02_Conditions_Loops_Functions",
        anchor="関数は「名前を付けた処理」",
        folder="diagrams",
        image="teach_definition_vs_call.png",
        title_ja="定義とよび出し",
        title_en="defining versus calling",
        caption_ja="図：`def` で決めただけでは何も判定されず、呼び出したときに初めて中身が動くこと（判定は計算値）。",
        caption_en="Figure: `def` only names the rule; the body runs when you call it (verdicts computed).",
        notice_ja="関数を定義しただけでは何も実行されません。呼び出すときに値を渡します。定義側の名前（引数）と、呼ぶ側の値（実引数）は別物で、順番か名前で対応します。",
        notice_en="Defining a function runs nothing. Values are supplied at the call. The names in the definition (parameters) and the values at the call (arguments) are different things, matched by position or by name.",
        question_ja="関数を定義しただけで、中身は実行されますか。",
        question_en="Does defining a function run its body?",
    ),
    dict(
        notebook="Day02_03_OpenCV_Image_Processing",
        anchor="しきい値を変えると何が変わるか",
        folder="diagrams",
        image="teach_threshold_sweep.png",
        title_ja="しきい値を掃引して数える",
        title_en="sweeping the threshold and counting",
        caption_ja="図：この合成画像でしきい値を変えたときの、前景の画素数と輪郭数（実測値）。",
        caption_en="Figure: foreground pixel count and contour count measured on this synthetic image as the threshold changes.",
        notice_ja="縦軸は**画素数**で、mm² に換算した面積ではありません。曲線の形は画像と欠陥で変わります。しきい値を変えても輪郭数が変わらない範囲があることも読み取ってください。",
        notice_en="The vertical axis counts **pixels**, not a calibrated area in mm². The shape of the curve depends on the image and the defect; notice also the ranges where the contour count does not change at all.",
        question_ja="しきい値を上げると、前景の画素数は増えますか、減りますか。",
        question_en="As the threshold rises, does the foreground pixel count grow or shrink?",
    ),
    dict(
        notebook="Day02_03_OpenCV_Image_Processing",
        anchor="輪郭とは、白い領域のかたまり",
        folder="diagrams",
        image="teach_contour_merge.png",
        title_ja="つながると数が減る",
        title_en="merging reduces the count",
        caption_ja="図：近い 2 つの欠陥が、しきい値を上げると 2 領域 → 1 領域 → 18 領域と変わる例（合成画像・実際の計算）。",
        caption_en="Figure: two nearby defects go from 2 regions to 1 (merged) to 18 (background noise) as the threshold rises (synthetic, computed).",
        notice_ja="輪郭は領域の**境界**を表す点の列で、前景画素そのものでも画素数でもありません。近い領域がつながると輪郭数は減ります。面積は `contourArea`（輪郭の幾何学的な面積）と、前景画素を数える方法を区別します。",
        notice_en="A contour is the **boundary** of a region — a sequence of points — not the foreground pixels or their count. Nearby regions that merge reduce the contour count. For area, distinguish `contourArea` (geometric area of the contour) from counting foreground pixels.",
        question_ja="2 つの汚れが 1 本の線でつながると、輪郭数はどうなりますか。",
        question_en="If two marks are joined by a thin line, what happens to the contour count?",
    ),
    dict(
        notebook="Day02_03_OpenCV_Image_Processing",
        anchor="まず図で考えましょう",
        folder="diagrams",
        image="teach_distance_345.png",
        title_ja="2 点の距離は斜辺",
        title_en="the distance is a hypotenuse",
        caption_ja="図：dx=300, dy=400, 距離=500 px の直角三角形（すべて計算値）。",
        caption_en="Figure: a right triangle with dx = 300, dy = 400 and a distance of 500 px (all computed).",
        notice_ja="距離は「dx と dy をそれぞれ 2 乗して足し、その平方根」で求めます。3-4-5 は、その計算が整数になる例です。px で求めた距離を mm にするには校正（px/mm）が必要です。",
        notice_en="Distance is found by squaring dx and dy, adding them, then taking the square root. 3-4-5 is a case where that calculation gives whole numbers. A distance measured in px needs calibration (px per mm) to become millimetres.",
        question_ja="dx = 6, dy = 8 のとき、距離は何 px ですか。",
        question_en="With dx = 6 and dy = 8, what is the distance in px?",
    ),
    dict(
        notebook="Day03_01_YOLO_Concepts",
        anchor="確からしさ（confidence）",
        folder="diagrams",
        image="teach_score_vs_correctness.png",
        title_ja="confidence と正しさは別",
        title_en="confidence is not correctness",
        caption_ja="図：5 つの検出の confidence と、正解と比べた正しさ（値は例示用）。",
        caption_en="Figure: confidence against correctness for five detections (illustrative values).",
        notice_ja="confidence が高い検出でも間違っていることがあり、低い検出でも正しいことがあります。confidence はモデルが出したスコアで、正解でも「正しい確率」でもありません。正しさは正解ラベルと対応づけのルールで確かめます。",
        notice_en="A high-confidence detection can be wrong and a low-confidence one can be right. Confidence is a score produced by the model: it is neither ground truth nor a probability of being correct. Correctness is checked against ground truth with a stated matching rule.",
        question_ja="しきい値 0.60 で残る検出のうち、正しくないのはどれですか。",
        question_en="At a threshold of 0.60, which of the surviving detections are wrong?",
    ),
    dict(
        notebook="Day03_02_YOLO_Inference",
        anchor="四角・クラス・confidence を数値で取り出す",
        folder="reference_outputs",
        image="ref_inference_boxes_table.png",
        title_ja="画像の番号と表の行",
        title_en="the numbers on the image and the rows in the table",
        caption_ja="図：この研修で実際に保存した検出（5 件）に番号を振り、同じ番号の表の行と並べたもの。参考出力（実際の結果）。",
        caption_en="Figure: the five detections actually saved by this course, numbered, next to the matching table rows. Reference output — real results.",
        notice_ja="この表と図は同一の 1 回の推論結果です（`yolo26n.pt`、conf=0.25、imgsz=640 の記録）。写真は ultralytics パッケージに同梱のサンプル画像で、COCO で学習したモデルの予習用です。写真の出所と権利はパッケージのライセンスとは別に確認が必要です（`assets/external_samples/PROVENANCE.md`）。塩ビの欠陥ではありません。",
        notice_en="The table and the figure come from one inference pass (`yolo26n.pt`, conf = 0.25, imgsz = 640). The photograph is a sample bundled with the ultralytics package, used to introduce a model pretrained on COCO. Its provenance and rights need checking separately from the package licence (`assets/external_samples/PROVENANCE.md`). It is not a PVC defect.",
        question_ja="この表の confidence は、正しい検出である確率ですか。",
        question_en="Is the confidence in this table a probability of being a correct detection?",
    ),
    dict(
        notebook="Day03_03_YOLO_Experiments",
        anchor="confidence と正しさは別物",
        folder="diagrams",
        image="teach_score_vs_correctness.png",
        title_ja="失敗の型を confidence で分ける",
        title_en="sorting failures by confidence",
        caption_ja="図：confidence と正しさを並べ、しきい値の上・下で失敗がどう分かれるかを見る図（値は例示用）。",
        caption_en="Figure: confidence against correctness, showing how failures split above and below the threshold (illustrative values).",
        notice_ja="しきい値を下げると「低い confidence の正しい検出」が助かり、同時に「低い confidence の誤検出」も入ります。片方だけを消すことはできません。",
        notice_en="Lowering the threshold rescues correct low-confidence detections **and** admits wrong low-confidence ones. You cannot remove only one side.",
        question_ja="この 5 件で、しきい値を 0.30 にすると誤検出は何件残りますか。",
        question_en="At a threshold of 0.30, how many wrong detections remain among these five?",
    ),
    dict(
        notebook="Day04_01_YOLO_Dataset_Annotation",
        anchor="3 つの役割",
        folder="diagrams",
        image="teach_dataset_contact_sheet.png",
        title_ja="データセットの中身を見る",
        title_en="look inside the dataset",
        caption_ja="図：この研修で実際に使うデータセットの train / val / test の先頭 4 枚ずつ。四角はラベルファイルから描いたもの。参考出力（実際のファイル）。",
        caption_en="Figure: the first four images of each split of the dataset this course actually uses; boxes are drawn from the label files. Reference output — real files.",
        notice_ja="コンタクトシートで分かるのは「見た目とラベルの付け方」です。どのファイルが学習に使われたかは分かりません。それは分割の記録（ファイル一覧・グループ・学習設定）で確かめます。",
        notice_en="A contact sheet shows appearance and labels; it cannot show which files trained the model. Establish that from the split records — file lists, groups and the training configuration.",
        question_ja="この 4 枚を見て「学習に使っていない」と言えますか。",
        question_en="Can you tell from these four thumbnails that they were not used for training?",
    ),
    dict(
        notebook="Day04_01_YOLO_Dataset_Annotation",
        anchor="同じ画像が複数の分割に入ると、何が起きるか",
        folder="diagrams",
        image="teach_leakage_split.png",
        title_ja="フレームで分ける／撮影で分ける",
        title_en="split by frame or by capture",
        caption_ja="図：実際の合成データセット画像 1 枚と、小さな画素値ノイズを加えた「ほぼ同じ画像」。位置はずらしていません。フレームで分けると、この 2 枚が train と test に分かれてしまいます。",
        caption_en="Figure: one synthetic dataset image and a copy with small pixel-intensity noise, not a spatial shift — two frames that a frame-level split would put on opposite sides.",
        notice_ja="同じ製品・同じ撮影回の画像が学習と試験に分かれると、見た目が近すぎて性能が実際より高く出ます（leakage）。分割は**製品・撮影回などのグループ単位**で行います。この教材のノイズは画素値の小さな変化で、位置をずらすものではありません。ハッシュ検査で見つかるのは 1 バイトも違わない重複だけです。",
        notice_en="If images of the same product or the same capture session land in both training and test, they look too alike and performance is overstated (leakage). Split by **group**, such as product or session. The noise in this course is a small change in pixel intensity, not a sub-pixel shift. A hash check finds only byte-identical duplicates.",
        question_ja="連番の連続写真をランダムに分けると、なぜ性能が高く出ますか。",
        question_en="Why does randomly splitting consecutive frames overstate performance?",
    ),
    dict(
        notebook="Day04_02_YOLO_Training",
        anchor="学習の繰り返し",
        folder="diagrams",
        image="teach_training_update.png",
        title_ja="1 つの batch で起きること",
        title_en="what one batch does",
        caption_ja="図：予測 → 損失 → 勾配 → 更新 の 1 サイクルと、batch・step・epoch の数え方（重みの変化は例示用）。",
        caption_en="Figure: one cycle of forward → loss → backward → update, and how batch, step and epoch are counted (weight changes illustrative).",
        notice_ja="バッチ（データをまとめて読む単位）と、重みの更新回数は別です。`nbs=64`・`batch=8` の名目累積は8バッチです。64枚は8回のデータローダ反復になりますが、warmup 中は累積数も変わり得ます。実際の更新回数を常に1回と決めつけず、実行設定とログを確認します。",
        notice_en="A batch and an optimizer update are different units. With `nbs=64` and `batch=8`, nominal accumulation is 8 batches. A pass over 64 images gives 8 loader iterations, but warmup can also change the accumulation count. Do not promise exactly one update; check the run settings and logs.",
        question_ja="64枚・batch=8 の反復数と、実際の更新回数を決める設定は何ですか。",
        question_en="For 64 images and batch=8, how many loader iterations occur, and which settings determine actual updates?",
    ),
    dict(
        notebook="Day05_01_Anomaly_Detection_Concepts",
        anchor="「いつもと違う」を見つける",
        folder="diagrams",
        image="teach_normal_variation.png",
        title_ja="正常のばらつきと欠陥",
        title_en="normal variation versus a defect",
        caption_ja="図：正常 4 枚（照明ムラとノイズで少しずつ違う）と、欠陥のある 1 枚の平均値の比較（合成画像・計算値）。",
        caption_en="Figure: four good parts that differ through lighting and noise, compared with one defective part by mean value (synthetic, computed).",
        notice_ja="明るさのムラ、模様、位置のずれなど、正常でもばらつきます。全体の明るさ 1 つでは説明できない差があることを先に知っておくと、異常マップの読み方が変わります。",
        notice_en="Normal parts still vary in brightness, texture and position. Knowing that one global brightness value cannot describe those differences changes how you read an anomaly map.",
        question_ja="全体の明るさが同じ 2 枚でも、異常と判定され方が変わるのはなぜですか。",
        question_en="Why can two images with the same overall brightness be judged differently?",
    ),
    dict(
        notebook="Day05_01_Anomaly_Detection_Concepts",
        anchor="なぜ「記憶」なのか",
        folder="diagrams",
        image="teach_memory_bank.png",
        title_ja="メモリバンクと最近傍",
        title_en="the memory bank and the nearest neighbour",
        caption_ja="図：正常パッチの特徴を貯めたメモリバンクと、2 つのクエリからの距離（2 次元の模式図）。",
        caption_en="Figure: a memory bank of normal-patch features and the distance from two queries (a 2-D schematic).",
        notice_ja="メモリバンクには正常画像の特徴を保存します。正常でない画像が混ざると、スコアが下がって見逃しが増える**可能性**があります（必ず永久に検出できなくなる、という保証ではありません）。混ざったら取り除いて作り直し、別の画像で確かめます。",
        notice_en="The memory bank stores features of normal images. A contaminated example can lower scores and **increase** misses; it does not guarantee permanent failure. Remove it, rebuild the bank and verify with held-out images.",
        question_ja="異常画像が 1 枚混ざったとき、最初に確かめるべきことは何ですか。",
        question_en="If one abnormal image slipped in, what should you check first?",
    ),
    dict(
        notebook="Day05_01_Anomaly_Detection_Concepts",
        anchor="2 種類の出力",
        folder="diagrams",
        image="teach_score_levels.png",
        title_ja="パッチ・画像・マップは別の出力",
        title_en="patch, image and map are three outputs",
        caption_ja="図：パッチごとのスコア → 画像 1 枚のスコア → 空間マップ。3 つを分けて読む（値は例示用）。",
        caption_en="Figure: per-patch scores → one image score → the spatial map, read separately (illustrative values).",
        notice_ja="この図の「最大」「平均」は**説明用のおもちゃの集約**です。この研修の設定では、最大のパッチ距離に近傍の正常特徴（9 点）の重みを掛けて画像スコアにし、表示するマップは補間と平滑化を経ます。だから画像スコアとマップの最大値は一致しません。",
        notice_en="The max and mean here are **toy aggregations for explanation**. In this course's configuration the image score weights the largest patch distance with its 9 nearest normal features, and the displayed map is interpolated and smoothed — so the image score and the map maximum need not match.",
        question_ja="画像スコアを決めるのに、マップ全体の平均は使っていますか。",
        question_en="Does the image score use the mean of the whole map?",
    ),
    dict(
        notebook="Day05_02_PatchCore_Training",
        anchor="PatchCore の「学習」は 1 回だけ",
        folder="diagrams",
        image="teach_backbone_vs_memory.png",
        title_ja="変わるのはメモリバンクだけ",
        title_en="only the memory bank changes",
        caption_ja="図：重みを更新しないバックボーンと、データで決まるメモリバンク（模式図）。",
        caption_en="Figure: a frozen backbone and a memory bank determined by the data (schematic).",
        notice_ja="ResNet-18 の重みは更新されません（凍結）。データで決まるのはメモリバンクで、その後に較正で決まる後処理（正規化の統計としきい値）も保存される状態の一部です。`max_epochs=1` で足りるのは、この手順が 1 周で終わる作りだからです。",
        notice_en="No ResNet-18 weight is updated (they are frozen). The data determines the memory bank, and the post-processing fitted later on calibration (normalisation statistics and the threshold) is also stored state. `max_epochs=1` is enough because this fitting procedure needs one pass.",
        question_ja="正常画像を増やしたとき、変わるのはバックボーン・メモリバンク・しきい値のどれですか。",
        question_en="If you add normal images, which changes: the backbone, the memory bank or the threshold?",
    ),
    dict(
        notebook="Day05_03_YOLO_vs_PatchCore",
        anchor="しきい値を動かしてよいのは、較正用データだけ",
        folder="diagrams",
        image="teach_threshold_freeze.png",
        title_ja="較正で決めて、固定する",
        title_en="choose on calibration, then freeze",
        caption_ja="図：較正用データでしきい値を決めて固定する流れ（模式図）。この研修の固定値は YOLO 0.06、PatchCore 0.50 です。",
        caption_en="Figure: choosing a threshold on calibration data, then freezing it (schematic). This course froze YOLO at 0.06 and PatchCore at 0.50.",
        notice_ja="固定した後に試験用データを見て動かすと、その数字はもう「未使用データでの成績」ではありません。較正用データは正常 6 枚・異常 20 枚なので、割合は 1/6 刻みでしか動きません。",
        notice_en="If you move the threshold after seeing the test data, those numbers are no longer a result on untouched data. Calibration holds 6 normal images, so a false-reject rate can only move in steps of 1/6.",
        question_ja="較正用の正常が 6 枚のとき、誤報率 10% 以下にするには誤報が何件以下である必要がありますか。",
        question_en="With six normal calibration images, how many false alarms are allowed for a false-reject rate of at most 10 %?",
    ),
    dict(
        notebook="Day01_02_Pixels_and_Images",
        anchor="1 枚の画像は 3 枚の表",
        folder="external_samples/open_reference",
        image="chelsea.png",
        title_ja="実写写真でも、1 画素は 3 つの数",
        title_en="in a real photograph, one pixel is still three numbers",
        caption_ja="写真：スキャンした実写（scikit-image `chelsea`、Stefan van der Walt、CC0 1.0）。下の説明の RGB の表と**同じ並び**（高さ × 幅 × 3）で保存されています。工場の塩ビの画像ではなく、色の仕組みを見るための例です。",
        caption_en="Photograph: a scanned real photo (scikit-image `chelsea`, Stefan van der Walt, CC0 1.0). It is stored in the **same layout** as the RGB arrays below (height × width × 3). This is an example for colour, not a factory PVC image.",
        notice_ja="この写真も、1 画素につき R・G・B の 3 つの整数（0〜255）を持つだけです。「写真だから特別な仕組み」はありません。表示するときに、その 3 つの数を光の三原色として混ぜているだけです。",
        notice_en="This photograph also stores three integers (0–255) per pixel: R, G and B. Nothing special happens \"because it is a photo\"; the display mixes those three numbers as red, green and blue light.",
        question_ja="この写真の 1 画素の値が (34, 139, 34) だったとき、表示される色は赤・緑・青のどれが強い色ですか。",
        question_en="If one pixel of this photo were (34, 139, 34), which of red, green and blue would dominate the displayed colour?",
    ),
    dict(
        notebook="Day01_03_Computer_Vision_Tasks",
        anchor="Part 5　製造での使い分け",
        folder="external_samples/open_reference",
        image="VisA_samples.png",
        title_ja="実在の産業向け異常検知データの例",
        title_en="a real industrial anomaly-detection dataset",
        caption_ja="図：VisA データセットの概要（Yang Zou ほか / Amazon Science、VisA データセットは CC BY 4.0）。回路基板・部品・カプセルなど、**工業製品の実写**が並びます。この研修の塩ビ製品ではなく、この研修のモデルの出力でもありません。",
        caption_en="Figure: the VisA overview (Yang Zou et al. / Amazon Science; VisA dataset, CC BY 4.0). Real photographs of industrial objects — circuit boards, parts, capsules. These are not this course's PVC products and not outputs of its models.",
        notice_ja="欠陥の見え方は製品ごとに違います。明るさの平均 1 つでは表せない差（形・模様・位置）が、どの製品にもあります。",
        notice_en="What counts as an anomaly differs by product. In every product there are differences — shape, pattern, position — that one average brightness value cannot describe.",
        question_ja="この中で、画像全体の平均の明るさを比べるだけでは見つけにくい欠陥はどれだと思いますか。",
        question_en="Which of these defects do you think a whole-image average brightness comparison would miss most easily?",
    ),
    dict(
        notebook="Day02_03_OpenCV_Image_Processing",
        anchor="しきい値を掃引して数える",
        folder="external_samples/open_reference",
        image="camera.png",
        title_ja="実写のグレースケール画像で試す",
        title_en="try it on a real greyscale photograph",
        caption_ja="写真：実写のグレースケール画像（scikit-image `camera`、Lav Varshney、CC0 1.0）。0〜255 の 1 チャンネルで、この研修の合成画像より複雑です。",
        caption_en="Photograph: a real greyscale image (scikit-image `camera`, Lav Varshney, CC0 1.0). One channel, 0–255, and more complex than this course's synthetic images.",
        notice_ja="照明のムラ、影、背景の模様が、すべて 0〜255 の数になっています。白い前景として残った部分は「欠陥」ではなく、単に『しきい値より暗い画素』です。この画像に製造上の欠陥はありません。",
        notice_en="Uneven lighting, shadows and background texture all become numbers between 0 and 255. White foreground here does not mean \"defect\"; it means \"darker than the threshold\". There is no manufacturing defect in this photograph.",
        question_ja="しきい値を 100 にすると、この写真で白く残るのはどんな場所だと思いますか。予想してから実行してください。",
        question_en="At a threshold of 100, which parts of this photo do you expect to stay white? Predict before you run it.",
    ),
    dict(
        notebook="Day02_03_OpenCV_Image_Processing",
        anchor="しきい値を掃引して数える",
        folder="external_samples/open_reference",
        image="brick.png",
        title_ja="模様のある背景では、数え方が変わる",
        title_en="repeated texture changes what you count",
        caption_ja="写真：レンガ壁の実写（CC0Textures を scikit-image が加工、CC0 1.0）。同じ模様がくり返される背景の例です。正常な模様で、欠陥ではありません。",
        caption_en="Photograph: a real brick wall (CC0Textures, processed by scikit-image; CC0 1.0). An example of a background with a repeating pattern. The pattern is normal, not a defect.",
        notice_ja="同じ模様がくり返される背景では、しきい値を 1 つ決めると**模様の一部がまとめて**前景になります。輪郭の数は『欠陥の数』ではなく『暗い領域の数』です。正常なばらつきを先に知ることが、欠陥検出の出発点になります。",
        notice_en="With a repeating background, one threshold turns **whole parts of the pattern** into foreground. The contour count is then \"number of dark regions\", not \"number of defects\". Knowing the normal variation first is the starting point for defect detection.",
        question_ja="この写真のしきい値を上げていくと、白い前景の面積は増えますか、減りますか。",
        question_en="As you raise the threshold on this photo, does the white foreground grow or shrink?",
    ),
    dict(
        notebook="Day05_01_Anomaly_Detection_Concepts",
        anchor="Part 2　教師ありと教師なし",
        folder="external_samples/open_reference",
        image="VisA_samples.png",
        title_ja="正常だけを集める難しさ",
        title_en="why collecting only normal samples is hard",
        caption_ja="図：VisA データセットの概要（Yang Zou ほか / Amazon Science、VisA データセットは CC BY 4.0）。正常・異常の両方を人が見分けて集めた、実在の産業データです。この研修の塩ビ製品ではありません。",
        caption_en="Figure: the VisA overview (Yang Zou et al. / Amazon Science; VisA dataset, CC BY 4.0). A real industrial dataset where people separated normal and abnormal examples. Not this course's PVC products.",
        notice_ja="異常検知は正常画像だけで学習できますが、**しきい値を決める較正**と**性能を測る評価**には、正常・異常のラベルが付いた別の画像が必要です。この研修でも、較正用に 26 枚、評価用に 26 枚を分けて使います。",
        notice_en="Anomaly detection can be fitted on normal images only, but **choosing a threshold** and **measuring performance** need labelled normal and abnormal images from a separate set. This course uses 26 images for calibration and 26 for evaluation.",
        question_ja="正常画像だけでは測れない数字は、見逃し率と誤報率のどちらですか。",
        question_en="With normal images only, which can you not measure: the miss rate or the false-alarm rate?",
    ),
]


def _notebook(stem: str) -> Path:
    matches = course_notebooks(NOTEBOOK_DIR, f"{stem}.ipynb")
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
    if cell.get("metadata", {}).get("aivision_caption") == "clarity-review-2026-11-16":
        return False
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
