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
        anchor="画面のどこを押すか / which part of the screen to use",
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
        title_ja="実際の出力で確かめる", title_en="checking with a real output",
        caption_ja="図：この研修で実際に保存した PatchCore の出力 1 枚。元画像・異常マップ・"
                   "目盛り付きの重ね表示を同じ順で並べています。",
        caption_en="Figure: one PatchCore output actually saved by this course — the original image, "
                   "the anomaly map, and the same map with a scale.",
        notice_ja="重ね表示の色は**スコアの大きさ**であって、傷の濃さではありません。"
                  "目盛りは 0〜1 で、0 が「学習した正常の範囲」、1 がこの較正での最大です。"
                  "マップが広がっている＝異常の範囲が広い、とは限らないことにも注意してください。",
        notice_en="The colour shows the **score**, not how dark the mark is. The scale is 0–1, where "
                  "0 is the learned normal range and 1 is the maximum seen in this calibration. A "
                  "wide blob does not always mean a wide defect.",
        question_ja="元画像の欠陥の位置と、異常マップで最も明るい場所は一致していますか。"
                    "一致しない場合、何が原因と考えられますか。",
        question_en="Does the brightest spot in the anomaly map sit on the defect? If not, what could "
                    "explain the difference?",
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
        caption_ja="図：同じ 2 枚（試験用）を 5 つの列で並べた実際の結果。元画像・YOLO の四角・"
                   "PatchCore の異常マップ・正解マスク・画像単位の判定です。しきい値は固定済みで、"
                   "この図のために動かしていません。",
        caption_en="Figure: two test images in five aligned columns — original, YOLO boxes, PatchCore "
                   "anomaly map, ground-truth mask and the image-level decision. Thresholds were "
                   "already frozen and were not moved to make this figure.",
        notice_ja="1 行目は 3 者が一致しています（NG）。2 行目も一致しています（OK）。"
                  "列を増やす目的は「どちらが良さそうか」ではなく、"
                  "**どこで食い違うか**を見つけることです。正解マスク（④）は判定には使っていません。",
        notice_en="Row 1: all three agree (NG). Row 2: all three agree (OK). The columns exist to show "
                  "**where the methods disagree**, not which looks better. The ground-truth mask (④) "
                  "was never used for tuning.",
        question_ja="あなたの実行結果でも、この 2 枚は同じ判定になりましたか。"
                    "違った場合、最初に疑うべき原因は何ですか。",
        question_en="Did the same two images get the same decisions in your own run? If not, what is "
                    "the first cause to suspect?",
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


def _insert(nb: dict, entry: dict, after: int | None = None) -> int | None:
    """見出しセルの直後に差し込む / insert right after the heading cell.

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
    for index, cell in enumerate(nb["cells"]):
        if cell["cell_type"] != "markdown":
            continue
        if anchor not in "".join(cell["source"]):
            continue
        nb["cells"].insert(index + 1, {
            "cell_type": "markdown",
            "id": _cell_id(entry),
            "metadata": {},
            "source": _markdown(entry).splitlines(keepends=True),
        })
        return index + 1
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
        for entry in entries:
            if entry["image"] in present:
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
        if changed and not args.check:
            path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{stem}: inserted={changed} (already present={len(entries) - changed})")
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
