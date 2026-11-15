"""Apply the 2026-11-15 audit's bounded, idempotent notebook-source corrections."""

from __future__ import annotations

import json
from pathlib import Path

from generate_svg_figures import FIGURES
from teaching_data import calibrated_defects

ROOT = Path(__file__).resolve().parents[2]
RUN_BANNER = (
    "# ▸ 実行のみ / Run only：このまま実行します。書き換えません。\n"
    "# ▸ Run only: press Shift + Enter and leave the code as it is.\n"
)


def cell(kind: str, source: str, identifier: str) -> dict:
    result = {"cell_type": kind, "id": identifier, "metadata": {},
              "source": source.splitlines(keepends=True)}
    if kind == "code":
        result.update(execution_count=None, outputs=[])
        result["metadata"]["aivision_role"] = "run-only"
    return result


def put(c: dict, source: str) -> None:
    if source == "".join(c["source"]):
        return
    c["source"] = source.splitlines(keepends=True)
    if c["cell_type"] == "code":
        c["outputs"] = []
        c["execution_count"] = None


CALIBRATION_CODE = RUN_BANNER + '''calibrated_path = ASSETS / "diagrams" / "calibrated_defects.png"
calibrated_info_path = ASSETS / "diagrams" / "calibrated_defects_ground_truth.json"
calibrated_image = cv2.imread(str(calibrated_path))
if calibrated_image is None:
    raise FileNotFoundError(f"校正付き欠陥画像がありません / missing: {calibrated_path}")
calibrated_info = json.loads(calibrated_info_path.read_text(encoding="utf-8"))
reference_points = calibrated_info["reference_points"]
calibrated_px_per_mm = distance_px(*reference_points) / calibrated_info["reference_mm"]
check_length_mm = distance_px(*calibrated_info["check_points"]) / calibrated_px_per_mm
print(f"倍率 / scale: {calibrated_px_per_mm:.3f} px/mm")
print(f"独立検査 / independent check: {check_length_mm:.3f} mm")

calibrated_gray = cv2.cvtColor(calibrated_image, cv2.COLOR_BGR2GRAY)
_, calibrated_mask = cv2.threshold(calibrated_gray, 80, 255, cv2.THRESH_BINARY_INV)
calibrated_contours, _ = cv2.findContours(
    calibrated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)
calibrated_contours = sorted(calibrated_contours, key=lambda contour: cv2.boundingRect(contour)[0])
for index, contour in enumerate(calibrated_contours, start=1):
    area_px2 = cv2.contourArea(contour)
    print(f"{index}: 輪郭面積 / contour area = {area_px2:.1f} px2")
print("前景画素数 / foreground pixels:", cv2.countNonZero(calibrated_mask))
show([cv2.cvtColor(calibrated_image, cv2.COLOR_BGR2RGB), calibrated_mask],
     ["same-plane calibrated synthetic image", "target mask (threshold 80)"])
'''


def correct_notebook(stem: str, nb: dict) -> None:
    for c in nb["cells"]:
        s = "".join(c["source"])
        if stem == "00_Environment_Setup":
            s = s.replace("第0日（第1日の朝に実施）", "第0日（第1日より前・授業時間外）")
            s = s.replace("Day 0 (done in the morning of Day 1)", "Day 0 (before Day 1, outside lesson hours)")
            s = s.replace("Set-ExecutionPolicy -Scope CurrentUser", "Set-ExecutionPolicy -Scope Process")
            s = s.replace("```python\n%pip", "```text\n%pip")
            if c["cell_type"] == "markdown" and any(key in s for key in
                    ("#### 手順 3：", "#### 手順 4：", "#### 手順 5：")):
                s = (
                    "#### 準備手順の確認 / Check the preflight sequence\n\n"
                    "インストールの正式手順は [START_HERE](../../START_HERE.md) ステップ3〜9です。\n"
                    "Python 3.11、両環境、両カーネル、素材、写真・重みを授業前に準備します。\n"
                    "ここでは再インストールせず、準備済みの状態を確認します。有効化が禁止されている場合は\n"
                    "仮想環境の python.exe を直接使います。ポリシー変更は許可された場合のみ現在の窓に限定します。\n\n"
                    "Use [START_HERE](../../START_HERE.md) Steps 3–9 as the authoritative installation sequence.\n"
                    "Prepare Python 3.11, both environments/kernels, assets, photos and weights before class.\n"
                    "Here, check the prepared state; do not reinstall. If activation is blocked, use the venv's\n"
                    "python.exe directly. Any permitted policy change is limited to the current window.\n"
                )
        elif stem == "Day01_02_Pixels_and_Images":
            s = s.replace("欠陥は残っているか / defect visible", "最小画素値が150未満 / min pixel below 150")
            s = s.replace('visible = "YES / はい"', 'below_threshold = "YES / はい"')
            s = s.replace("{visible:>24}", "{below_threshold:>24}")
        elif stem == "Day02_02_Conditions_Loops_Functions":
            s = s.replace(
                "round(measured_mm - nominal_mm, 6)   # 小数の誤差を消してから比べる / drop float noise first",
                "measured_mm - nominal_mm",
            )
        elif stem == "Day02_03_OpenCV_Image_Processing":
            s = s.replace(
                "1 px の誤差が何 mm になるかの見積もり（0.5 px ÷ 2.00 px/mm = ±0.25 mm）",
                "仮定したエッジ位置の不確かさの換算（±0.5 px ÷ 2.00 px/mm = ±0.25 mm）",
            )
            s = s.replace(
                "The same figure estimates what one pixel of error means in mm\n"
                "(0.5 px ÷ 2.00 px/mm = ±0.25 mm).",
                "The same figure converts an assumed edge-location uncertainty\n"
                "(±0.5 px ÷ 2.00 px/mm = ±0.25 mm); it is not guaranteed accuracy.",
            )
            s = s.replace(
                "1 px の誤差は、倍率の分だけ mm の誤差になります（図では 0.5 px が ±0.25 mm）。",
                "図ではエッジ位置の不確かさを ±0.5 px と仮定し、±0.25 mm に換算します。測定精度の保証ではありません。",
            )
            s = s.replace(
                "A pixel error becomes a mm error scaled by that factor (0.5 px is ±0.25 mm\n"
                "here).",
                "The assumed edge-location uncertainty ±0.5 px converts to ±0.25 mm here;\n"
                "this does not guarantee measurement accuracy.",
            )
        elif stem == "Day04_01_YOLO_Dataset_Annotation":
            s = s.replace("データ漏れはありません / no leakage detected",
                          "同一バイト列の重複ファイルは検出されませんでした / No byte-identical duplicate files detected")
            if c["cell_type"] == "code" and "No byte-identical duplicate files detected" in s:
                note = '\nprint("近似画像・再符号化・撮影群の漏れは除外できません / Near duplicates, re-encoding and session/lot leakage are not excluded.")\n'
                if note.strip() not in s:
                    s += note
        elif stem == "Day04_02_YOLO_Training":
            if c["cell_type"] == "code" and "run_dir = Path(train_model.trainer.save_dir)" in s and "save_training_run" not in s:
                s = s.replace(
                    "run_dir = Path(train_model.trainer.save_dir)",
                    'run_dir = Path(train_model.trainer.save_dir)\n'
                    '    from training_run import save_training_run\n'
                    '    training_manifest = save_training_run(COURSE_ROOT, run_dir, {\n'
                    '        "epochs": EPOCHS, "imgsz": IMGSZ, "batch": BATCH, "seed": SEED,\n'
                    '        "device": "cpu", "data": str(data_yaml_path.relative_to(COURSE_ROOT)),\n'
                    '    })\n'
                    '    print("評価へ渡す記録 / evaluation handoff:", training_manifest)',
                )
        elif stem == "Day04_03_YOLO_Evaluation":
            s = s.replace('best_weights = candidates[-1]          # 最新の学習結果 / the most recent run',
                          'from training_run import select_training_run\n'
                          'best_weights, selected_run = select_training_run(COURSE_ROOT)\n'
                          'print("評価する重み / evaluating weights:", best_weights)')
            if c["cell_type"] == "code" and "if not candidates:" in s and "model = YOLO(str(best_weights))" in s:
                start = s.index("if not candidates:")
                end = s.index("from training_run import select_training_run", start)
                s = s[:start] + s[end:]
        elif stem == "Day05_02_PatchCore_Training":
            if c["cell_type"] == "code" and "COURSE_ROOT =" in s and "TIMM_USE_OLD_CACHE" not in s:
                s = s.replace("import sys\n", 'import sys\nimport os\n'
                              'os.environ["TIMM_USE_OLD_CACHE"] = "1"\n', 1)
            if c["cell_type"] == "code" and "model = Patchcore(" in s and "check_cached_file" not in s:
                start = s.index("model = Patchcore(")
                check = (
                    "from timm.models import get_pretrained_cfg\n"
                    "from timm.models._hub import check_cached_file\n"
                    'backbone_cfg = get_pretrained_cfg("resnet18")\n'
                    "if backbone_cfg is None or not backbone_cfg.url or not check_cached_file(backbone_cfg.url):\n"
                    '    raise FileNotFoundError("resnet18 cache missing or invalid; run preload_models.py --profile anomalib before class")\n'
                )
                s = s[:start] + check + s[start:]
            if c["cell_type"] == "markdown":
                appended = (
                    "\n授業前に `preload_models.py --profile anomalib` を実行します。準備セルで\n"
                    "`TIMM_USE_OLD_CACHE=1` を設定し、検査済み URL キャッシュを優先します。\n"
                    "キャッシュが無ければ、この授業セルはエラーで止まり、自動取得しません。\n\n"
                    "Run `preload_models.py --profile anomalib` before class. Preparation sets\n"
                    "`TIMM_USE_OLD_CACHE=1` to prefer the verified URL cache. If missing, this lesson cell\n"
                    "stops with an explicit error rather than downloading automatically.\n"
                )
                s = s.replace(appended, "")
                s = s.replace(
                    "> `pre_trained=True` は、ImageNet で学習した重みを **初回だけダウンロード** します。\n"
                    "> ネットワークが必要です。取得できなかった場合は、そのことを記録して講師に相談してください。",
                    "> ImageNet の重みは授業前に `preload_models.py --profile anomalib` で取得します。\n"
                    "> 準備セルの `TIMM_USE_OLD_CACHE=1` が URL キャッシュを優先します。\n"
                    "> キャッシュが無ければこの授業セルはエラーで止まり、自動取得しません。",
                )
                s = s.replace(
                    "`pre_trained=True` **downloads ImageNet weights once**, so a network connection is needed. If it\n"
                    "fails, record it and ask the instructor.",
                    "Preload ImageNet weights before class with `preload_models.py --profile anomalib`.\n"
                    "Preparation sets `TIMM_USE_OLD_CACHE=1` to prefer the URL cache.\n"
                    "A missing/invalid cache stops this lesson cell explicitly; it does not download automatically.",
                )
                s = s.replace(
                    "`pre_trained=True` は初回に ImageNet の重みを取得します。再実行するか、管理者に相談してください。",
                    "授業前に `preload_models.py --profile anomalib` で取得・検査します。不足は講師に相談してください。",
                )
                s = s.replace("`pre_trained=True` downloads ImageNet weights once. Retry, or ask IT.",
                              "Run `preload_models.py --profile anomalib` before class; report missing cache to the instructor.")
        elif stem == "Day05_03_YOLO_vs_PatchCore":
            if c["cell_type"] == "markdown" and "固定したしきい値で、試験用を" in s:
                s += (
                    "\n**重み・前処理・正常メモリ・後処理も固定**します。試験を見てこれらを変えてはいけません。\n"
                    "同梱図の 0.06 / 0.50 は保存済み参考実行の例で、今回の実行の期待値ではありません。\n\n"
                    "**Freeze weights, preprocessing, normal memory and postprocessing too.** Do not change them\n"
                    "after inspecting test results. Supplied 0.06 / 0.50 values are saved reference-run examples,\n"
                    "not expected results for your live run.\n"
                ) if "Freeze weights, preprocessing" not in s else ""
        put(c, s)

    if stem == "Day02_03_OpenCV_Image_Processing":
        for c in nb["cells"]:
            s = "".join(c["source"])
            if c["cell_type"] == "markdown" and "#### 演習 1（基本）：輪郭の面積" in s:
                put(c, (
                    "#### 演習 1（基本）：同じ画像の輪郭面積を mm² にする\n\n"
                    "次のセルでは Part 3 の `kept` ではなく、上の校正付き画像の `calibrated_contours` を使います。\n"
                    "Part 3 の `defect_multi.png` に、別画像から得た倍率を適用してはいけません。\n"
                    "ヒント：`area_px2` を `calibrated_px_per_mm ** 2` で割ります。輪郭の幾何学的面積と\n"
                    "前景の画素数は別です。正方画素、同じ対象平面、垂直視点（または補正済みの透視）、\n"
                    "小さいレンズ歪み、基準線の不確かさを確認します。これは理想的な合成画像です。\n\n"
                    "#### Exercise 1 (basic): convert areas from the same calibrated image\n\n"
                    "Use `calibrated_contours`, not Part 3's `kept`. Do not apply a different image's scale to\n"
                    "`defect_multi.png`. Hint: divide `area_px2` by `calibrated_px_per_mm ** 2`.\n"
                    "Geometric contour area differs from foreground-pixel count. Check square pixels, the same\n"
                    "object plane, perpendicular view (or corrected perspective), limited distortion and reference\n"
                    "uncertainty. This is an ideal synthetic scene.\n\n"
                    "**できたら / Done when:** 両輪郭を px² と mm² で表示します / print both areas in px² and mm².\n"
                ))
            if c["cell_type"] == "code" and 'if "kept" in dir() and calibration_image is not None:' in s:
                put(c, s.replace('if "kept" in dir() and calibration_image is not None:',
                                 'if calibrated_image is not None:')
                    .replace("enumerate(kept,", "enumerate(calibrated_contours,")
                    .replace("area_px = cv2.contourArea", "area_px2 = cv2.contourArea")
                    .replace("{area_px:8.1f}", "{area_px2:8.1f}"))
        if not any(c.get("id") == "audit-same-plane-code" for c in nb["cells"]):
            index = next(i for i, c in enumerate(nb["cells"]) if "#### 演習 1（基本）" in "".join(c["source"]))
            _, info = calibrated_defects()
            areas = ", ".join(f"{t['area_px2']} px² → {t['area_mm2']:.6f} mm²" for t in info["targets"])
            intro = (
                "### 同じ平面の基準と対象 / Same-plane reference and targets\n\n"
                "長さの換算を確認してから、独立した校正付き欠陥画像を使います。青い基準線は\n"
                "しきい値80では前景に入りません。倍率1.2 px/mm、独立検査50 mm、輪郭面積475 / 925 px²、\n"
                f"前景画素数{sum(t['foreground_pixels'] for t in info['targets'])}が、この合成画像のコードから得られます。\n"
                f"演習の式を完成させたときの計算確認値：{areas}。\n\n"
                "After checking length conversion, use a separate same-plane calibrated defect scene.\n"
                "Blue reference/check bars are excluded by threshold 80. Computed results are 1.2 px/mm,\n"
                f"independent check 50 mm, contour areas 475 / 925 px² and "
                f"{sum(t['foreground_pixels'] for t in info['targets'])} foreground pixels.\n"
                f"After completing the exercise formula, check the computed areas: {areas}.\n"
            )
            nb["cells"][index:index] = [cell("markdown", intro, "audit-same-plane-intro"),
                                       cell("code", CALIBRATION_CODE, "audit-same-plane-code")]
        for c in nb["cells"]:
            if c.get("id") == "audit-same-plane-intro":
                put(c, "".join(c["source"]).replace("1514", "1508"))

    # Shared figure text is generated with Japanese first, then the equivalent English.
    for name, (target, anchor, jp, en, question_jp, question_en) in FIGURES.items():
        if target != stem:
            continue
        nb["cells"] = [c for c in nb["cells"] if c.get("id") != f"audit-{name}"]
        matches = [i for i, c in enumerate(nb["cells"]) if anchor in "".join(c["source"])]
        if not matches:
            raise ValueError(f"{stem}: figure anchor missing: {anchor}")
        index = matches[0]
        if "".join(nb["cells"][index]["source"]).lstrip().startswith("## Part "):
            index += 1
        source = (
            f"### コードの読み方 / Reading the code\n\n![](../../assets/svg/{name}.svg)\n\n"
            f"図：{jp}（計算した合成例・模式図。モデルの実測出力ではありません。）\n\n"
            f"Figure: {en} (computed synthetic / schematic, not measured model output.)\n\n"
            f"**気づいてほしいこと**\n\n{jp} 入力と変換後の値を指でたどってください。\n\n"
            f"**What to notice**\n\n{en} Trace the input and transformed values.\n\n"
            f"**考えてみてください / Try to answer**\n\n{question_jp}\n\n{question_en}\n"
        )
        nb["cells"].insert(index, cell("markdown", source, f"audit-{name}"))

    for c in nb["cells"]:
        if c.get("id") == "audit-same-plane-code":
            c["metadata"]["aivision_role"] = "run-only"

    if stem == "Day02_02_Conditions_Loops_Functions" and not any(c.get("id") == "audit-tolerance-policy" for c in nb["cells"]):
        index = next(i for i, c in enumerate(nb["cells"]) if "def judge(" in "".join(c["source"]))
        nb["cells"].insert(index, cell("markdown",
            "### 境界と表示 / Boundaries and display\n\n"
            "基本例は差を丸めず `abs(measured_mm - nominal_mm) <= tolerance_mm` で判定します。\n"
            "99.5 / 100.5 mm は OK、100.5001 mm は NG。表示の桁数、測定器の分解能、合否方針は別です。\n"
            "`2.1 - 2.0` のような小数は二進数で厳密に表せない場合があります。\n"
            "後の厚さ演習の丸めは、その演習だけの明示的な方針であり、基本例には使いません。\n\n"
            "The base example compares the unrounded absolute difference with an inclusive `<=`.\n"
            "99.5 / 100.5 mm are OK; 100.5001 mm is NG. Display precision, instrument resolution and acceptance\n"
            "policy are separate. Some decimals, such as `2.1 - 2.0`, are not represented exactly in binary.\n"
            "The later thickness exercise's explicit rounding convention is confined to that exercise.\n",
            "audit-tolerance-policy"))


LEARNING_LOOPS = {
    "00_Environment_Setup": ("変数は値の名前です。カーネルは値を保持する実行役です。", "A variable names a value; the kernel executes code and retains values.", "加算前後の defect_count", "defect_count before and after increment"),
    "Day01_01_Introduction_to_AI": ("学習は例から規則を決め、推論は固定した規則を使います。関数や統計はここでは予告です。", "Training fits a rule; inference applies it. Functions/statistics here are previews.", "新しい明るさの値", "a new brightness value"),
    "Day01_02_Pixels_and_Images": ("配列は数値を並べた表です。チャンネルは色ごとの表です。", "An array is a table of values; each channel is a colour's table.", "canvas の1画素", "one canvas pixel"),
    "Day01_03_Computer_Vision_Tasks": ("分類は画像の答え、検出は位置、画素分割は形、異常検知は正常との差を出します。", "Classification labels an image; detection locates, segmentation shapes, anomaly detection scores differences from normal.", "1つの欠陥の出力形式", "the output format for one defect"),
    "Day02_01_Python_Basics": ("代入は名前に値を結び付けます。= は比較ではありません。", "Assignment binds a value to a name; = is not a comparison.", "厚さだけ", "only thickness"),
    "Day02_02_Conditions_Loops_Functions": ("関数は入力を受け取り、return で結果を返します。条件は真か偽かを調べます。", "A function takes inputs and returns a result; a condition tests true or false.", "測定値だけ", "only the measured value"),
    "Day02_03_OpenCV_Image_Processing": ("しきい値は画素の明るさを分ける境目です。面積の条件とは別です。", "A threshold separates pixel intensities; it is not an area cutoff.", "反転しきい値だけ", "only the inverse threshold"),
    "Day03_01_YOLO_Concepts": ("クラスは欠陥の種類です。confidence はモデルのスコアで、正解の保証ではありません。", "A class is a defect category; confidence is a model score, not guaranteed correctness.", "x2 だけ", "only x2"),
    "Day03_02_YOLO_Inference": ("推論は保存した重みを使い、画像から結果を作ります。", "Inference uses saved weights to produce results from an image.", "confidence の表示条件だけ", "only the confidence filter"),
    "Day03_03_YOLO_Experiments": ("しきい値で四角を除く操作と、画像の縮小は別の実験です。", "Filtering boxes by score and resizing the image are separate experiments.", "confidence だけ", "only confidence"),
    "Day04_01_YOLO_Dataset_Annotation": ("学習・検証・試験は別の役割です。撮影群も分けます。", "Train, validation and test have different roles; separate acquisition groups too.", "分割の単位だけ", "only the split unit"),
    "Day04_02_YOLO_Training": ("epoch はデータを1周、batch は一度に渡す画像群です。更新回数とは区別します。", "An epoch is a pass through data; a batch is a group processed together. Distinguish optimizer updates.", "batch だけ（予測してから実行）", "only batch (predict before running)"),
    "Day04_03_YOLO_Evaluation": ("評価は固定したモデルと判定条件を未使用画像で調べます。", "Evaluation checks a frozen model and rule on unused images.", "模式例の IoU 条件だけ", "only the schematic IoU cutoff"),
    "Day05_01_Anomaly_Detection_Concepts": ("特徴は画像から計算する数値です。正常メモリは特徴の見本です。", "Features are values computed from images; normal memory stores feature examples.", "模式例の新しい特徴だけ", "only a schematic new feature"),
    "Day05_02_PatchCore_Training": ("バックボーンは固定した特徴抽出器です。正常メモリと較正値はデータから作ります。", "The backbone is a frozen feature extractor; data determine normal memory and calibration.", "較正用の条件だけ（試験は調整に使わない）", "only a calibration setting (never tune on test)"),
    "Day05_03_YOLO_vs_PatchCore": ("較正は判定条件を決める工程です。試験は固定後に別データで確認する工程です。", "Calibration selects the rule; test checks it on different data after freezing.", "較正用スライダーだけ", "only the calibration slider"),
}


def main() -> int:
    paths = sorted((ROOT / "notebooks").glob("*/*.ipynb"))
    if len(paths) != 16:
        raise ValueError(f"Expected 16 lesson notebooks, found {len(paths)}")
    for path in paths:
        nb = json.loads(path.read_text(encoding="utf-8"))
        correct_notebook(path.stem, nb)
        if not any(c.get("id") == "audit-learning-loop" for c in nb["cells"]):
            jp, en, change_jp, change_en = LEARNING_LOOPS[path.stem]
            nb["cells"].insert(2, cell("markdown",
                "### 予想して、実行して、説明する / Predict, run, inspect, explain\n\n"
                f"{jp} 重要なセルの前に、入力・操作・出力を一文ずつ説明してください。\n"
                f"予想を書いて実行し、値または図を観察します。{change_jp}を変え、もう一度予想して実行します。\n"
                "意図的なエラーと未完成の演習は、その指示に従って取り組みます。\n\n"
                f"{en} Before an important cell, describe its input, operation and output in one sentence each.\n"
                f"Predict, run, inspect the values/image and explain why. Change {change_en}, predict and rerun.\n"
                "Follow the instructions for deliberately erroneous cells and unsolved exercises.\n",
                "audit-learning-loop"))
        new_text = json.dumps(nb, ensure_ascii=False, indent=1) + "\n"
        if path.read_text(encoding="utf-8") != new_text:
            path.write_text(new_text, encoding="utf-8")
            print("Updated:", path.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
