"""実際に保存された実行結果から、教材用の参考図を作ります。

Build the teaching figures that come from **saved runs of this course**, not from imagination:
a real training log, the real validation scores, the real anomalib visualisations and the real
YOLO detections. Every figure says inside itself where the numbers came from.

方針 / Rules
------------
* 数値を創作しません。入力ファイルが無ければ **作らずに失敗** し、理由を表示します。
  Nothing is invented. If a source file is missing the figure is not produced and the reason is
  printed, so nobody can mistake a placeholder for a measurement.
* 高価な処理（モデルの学習・再推論）はしません。保存済みの出力を読むだけです。
  No training and no costly re-inference: the script reads what the course already saved.
  例外は YOLO の枠を描くための 1 回の推論で、これはローカルの重みだけで完結します。
  The one exception is a short YOLO pass used to draw boxes; it uses local weights only and
  never downloads anything (`weights_only` local checkpoint, `imgsz` fixed).
* 出力は ``assets/reference_outputs/`` です。
  Output goes to ``assets/reference_outputs/``.

使い方 / Usage
--------------
    python assets\\scripts\\generate_reference_outputs.py
    python assets\\scripts\\generate_reference_outputs.py --only comparison

入力 / Inputs（すべて研修の実行で生成される / all produced by running the course）
--------------------------------------------------------------------------
``submissions/day05/patchcore_scores.csv``        PatchCore scores per image and partition
``submissions/day05/comparison_test_results.json`` frozen thresholds and the test summary
``submissions/day04/yolo_predictions_on_shared_set.json`` YOLO confidence per image
``submissions/day04/best.pt``                      YOLO weights from Day 4
``training_results/day04/pvc_defect_quick/results.csv`` one row per training epoch
``training_results/day04/test_evaluation/val_batch0_{labels,pred}.jpg`` truth and prediction
``training_results/day05/Patchcore/pvc_sheet/latest/images/test/**/*.png`` anomalib output
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm, patches
from mpl_toolkits.axes_grid1 import make_axes_locatable
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_training_assets import configure_matplotlib  # noqa: E402

DPI = 140
INK = "#24292f"
MUTED = "#57606a"
ACCENT = "#1f6feb"
LINE = "#d0d7de"
OK = "#1a7f37"
WARN = "#9a6700"
BAD = "#a40e26"

PROVENANCE_TEST = ("参考出力：この研修で実際に保存された実行結果（2026-11-12, CPU のみ）/ "
                   "Reference output: actually saved run of this course (12 Nov 2026, CPU only)")


class MissingSource(RuntimeError):
    """入力が無いので図を作らない / a source file is missing, so nothing is drawn."""


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _require(path: Path) -> Path:
    if not path.exists():
        raise MissingSource(f"missing source: {path}")
    return path


def _save(fig, path: Path) -> Path:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[reference] {path.name}")
    return path


def _note(fig, text: str, y: float = -0.02) -> None:
    fig.text(0.5, y, text, ha="center", va="top", fontsize=8, color=MUTED)


def _read_scores(root: Path) -> list[dict]:
    path = _require(root / "submissions" / "day05" / "patchcore_scores.csv")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


# ---------------------------------------------------------------------------
# Day 4: 実際の学習曲線 / the actual training curves
# ---------------------------------------------------------------------------


def ref_train_val_curves(root: Path, out_dir: Path) -> Path:
    path = _require(root / "training_results" / "day04" / "pvc_defect_quick" / "results.csv")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = [row for row in csv.DictReader(handle) if row.get("epoch")]
    if not rows:
        raise MissingSource(f"no epoch rows in {path}")

    epoch = np.array([int(float(r["epoch"])) for r in rows])
    train_cls = np.array([float(r["train/cls_loss"]) for r in rows])
    val_cls = np.array([float(r["val/cls_loss"]) for r in rows])
    map50 = np.array([float(r["metrics/mAP50(B)"]) for r in rows])
    precision = np.array([float(r["metrics/precision(B)"]) for r in rows])

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 3.9))
    ax = axes[0]
    ax.plot(epoch, train_cls, color=ACCENT, linewidth=1.8, label="学習 / train cls loss")
    ax.plot(epoch, val_cls, color=WARN, linewidth=1.8, label="検証 / val cls loss")
    ax.set_xlabel("epoch（データ全体を何周したか / passes over the data）", fontsize=8.5)
    ax.set_ylabel("損失 / loss（小さいほど良い / lower is better）", fontsize=8.5)
    ax.set_title("① 損失 / loss", fontsize=9)
    ax.tick_params(labelsize=7.5)
    ax.legend(fontsize=7.6)
    ax.grid(alpha=0.25)
    gap = val_cls[-1] - train_cls[-1]
    ax.annotate(f"最後の差 / final gap = {gap:+.2f}",
                xy=(epoch[-1], val_cls[-1]), textcoords="offset points", xytext=(-105, 30),
                fontsize=7.4, color=MUTED,
                arrowprops=dict(arrowstyle="->", color=MUTED, linewidth=1))

    ax2 = axes[1]
    ax2.plot(epoch, map50, color=OK, linewidth=1.8, label="mAP50")
    ax2.plot(epoch, precision, color=MUTED, linewidth=1.4, label="precision")
    ax2.set_ylim(0, 1.02)
    ax2.set_xlabel("epoch", fontsize=8.5)
    ax2.set_ylabel("0〜1（高いほど良い / higher is better）", fontsize=8.5)
    ax2.set_title("② 精度の指標 / quality metrics", fontsize=9)
    ax2.tick_params(labelsize=7.5)
    ax2.legend(fontsize=7.6)
    ax2.grid(alpha=0.25)

    fig.suptitle(f"この研修で実際に行った学習の記録 / the actual training log of this course "
                 f"（{len(epoch)} epoch の CPU での試行 / a short CPU run）", fontsize=10)
    _note(fig, "図：" + PROVENANCE_TEST + " — source: training_results/day04/pvc_defect_quick/results.csv"
               "（本番の学習ではなく、この回の短い試行の記録です / a short trial run, not a production training）\n"
               "検証の損失が学習の損失より低いこともあります（学習時だけ画像を加工して難しくするため）。"
               "見るのは絶対値より「両方が下がり続けるか」「差が開き続けないか」です / "
               "The validation loss can sit below the training loss because training adds augmentation; "
               "watch both curves and the gap, not a single number.")
    return _save(fig, out_dir / "ref_train_val_curves.png")


# ---------------------------------------------------------------------------
# Day 5: 較正用データのスコア分布としきい値 / calibration scores and the threshold
# ---------------------------------------------------------------------------


def ref_score_distribution(root: Path, out_dir: Path) -> Path:
    rows = [r for r in _read_scores(root) if r.get("partition") == "calibration"]
    if not rows:
        raise MissingSource("no calibration rows in submissions/day05/patchcore_scores.csv")

    normal = np.array([float(r["score"]) for r in rows if r["truly_abnormal"].strip() == "False"])
    abnormal = np.array([float(r["score"]) for r in rows if r["truly_abnormal"].strip() == "True"])

    threshold = None
    summary_path = root / "submissions" / "day05" / "comparison_test_results.json"
    if summary_path.exists():
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        for row_ in summary.get("calibration", []):
            if row_.get("method") == "PatchCore":
                threshold = float(row_["threshold"])

    fig, ax = plt.subplots(figsize=(10.4, 4.4))
    rng = np.random.default_rng(0)
    ax.scatter(normal, np.full_like(normal, 1.0) + rng.uniform(-0.06, 0.06, normal.size),
               s=46, color=ACCENT, marker="o", label=f"正常品 / normal (n={normal.size})")
    ax.scatter(abnormal, np.full_like(abnormal, 0.0) + rng.uniform(-0.06, 0.06, abnormal.size),
               s=46, color=BAD, marker="x", label=f"異常品 / abnormal (n={abnormal.size})")
    ax.set_yticks([0.0, 1.0])
    ax.set_yticklabels(["異常品 / abnormal", "正常品 / normal"], fontsize=8.5)
    ax.set_ylim(-0.45, 1.45)
    ax.set_xlim(0, 1.02)
    ax.set_xlabel("画像単位の異常スコア（較正用データの min/max で 0〜1 に正規化）/ "
                  "image-level score, normalised on the calibration partition", fontsize=8.5)
    ax.tick_params(labelsize=7.5)
    ax.grid(axis="x", alpha=0.25)

    if threshold is not None:
        ax.axvline(threshold, color=OK, linewidth=2)
        ax.text(threshold + 0.012, 1.35, f"しきい値 / threshold = {threshold:.2f}",
                fontsize=8.5, color=OK)
        missed = int((abnormal < threshold).sum())
        false_alarm = int((normal >= threshold).sum())
        ax.text(0.02, -0.36,
                f"この線より左の異常品は見逃し / abnormal left of the line = {missed} 枚、"
                f"右の正常品は誤報 / normal right of it = {false_alarm} 枚",
                fontsize=8, color=INK)
    else:
        ax.text(0.02, 1.35, "しきい値がまだ保存されていません / no frozen threshold saved yet",
                fontsize=8.5, color=MUTED)

    ax.set_title("較正用（validation）データだけを使った分布 / distribution on the calibration partition only",
                 fontsize=10)
    _note(fig, "図：" + PROVENANCE_TEST + " — 試験用データは含みません / test partition not shown here")
    return _save(fig, out_dir / "ref_score_distribution.png")


# ---------------------------------------------------------------------------
# Day 3: 実際の confidence と残る件数 / real confidences and how many survive
# ---------------------------------------------------------------------------


def ref_confidence_counts(root: Path, out_dir: Path) -> Path:
    path = _require(root / "submissions" / "day04" / "yolo_predictions_on_shared_set.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    images = payload.get("images", [])
    if not images:
        raise MissingSource(f"no per-image entries in {path}")

    max_conf = np.array([float(row["yolo_max_conf"]) for row in images])
    is_abnormal = np.array([row.get("true_label") == "bad" for row in images])
    thresholds = np.round(np.arange(0.0, 1.001, 0.01), 2)
    # NG と判定される枚数 = その画像の最大 confidence がしきい値以上の枚数
    # An image is called NG when its highest confidence reaches the threshold.
    ng_counts = np.array([int((max_conf >= t).sum()) for t in thresholds])

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.1))
    ax = axes[0]
    ax.step(thresholds, ng_counts, where="post", color=ACCENT, linewidth=2)
    ax.set_xlabel("しきい値 / threshold", fontsize=8.5)
    ax.set_ylabel("NG と判定される枚数 / images called NG", fontsize=8.5)
    ax.set_title(f"① 実際の最大 confidence から数えた件数（全 {max_conf.size} 枚）", fontsize=9)
    ax.tick_params(labelsize=7.5)
    ax.grid(alpha=0.25)
    for t in (0.01, 0.25, 0.5, 0.75):
        count = int((max_conf >= t).sum())
        ax.plot([t], [count], marker="o", color=WARN, markersize=5)
        ax.annotate(f"{t:.2f}→{count}", (t, count), textcoords="offset points",
                    xytext=(4, 6), fontsize=7.4, color=WARN)

    ax2 = axes[1]
    bins = np.linspace(0, 1, 21)
    ax2.hist(max_conf[~is_abnormal], bins=bins, color=ACCENT, alpha=0.75,
             label=f"正常品 / normal (n={int((~is_abnormal).sum())})")
    ax2.hist(max_conf[is_abnormal], bins=bins, color=BAD, alpha=0.65,
             label=f"異常品 / abnormal (n={int(is_abnormal.sum())})")
    ax2.set_xlabel("画像ごとの最大 confidence / highest confidence in the image", fontsize=8.5)
    ax2.set_ylabel("枚数 / number of images", fontsize=8.5)
    ax2.set_title("② 落とした検出だけでなく、残った最大値も見る", fontsize=9)
    ax2.tick_params(labelsize=7.5)
    ax2.legend(fontsize=7.6)
    ax2.grid(alpha=0.25)

    fig.suptitle(f"実際の推論結果での confidence の効き方（{payload.get('imgsz', '?')} px, "
                 f"推論は conf={payload.get('min_inference_conf', '?')} で 1 回だけ）", fontsize=10)
    _note(fig, "図：" + PROVENANCE_TEST + " — source: submissions/day04/yolo_predictions_on_shared_set.json"
              + "（しきい値を変えても推論はやり直していません / no re-inference）")
    return _save(fig, out_dir / "ref_confidence_counts.png")


# ---------------------------------------------------------------------------
# Day 4: 正解と予測を並べる / truth and prediction side by side
# ---------------------------------------------------------------------------


def ref_detections_label_vs_pred(root: Path, out_dir: Path) -> Path:
    folder = root / "training_results" / "day04" / "test_evaluation"
    truth = Image.open(_require(folder / "val_batch0_labels.jpg")).convert("RGB")
    pred = Image.open(_require(folder / "val_batch0_pred.jpg")).convert("RGB")

    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.3))
    axes[0].imshow(truth)
    axes[0].set_title("① 正解ラベル / ground truth\n（人が付けた四角 / boxes drawn by a person）", fontsize=9)
    axes[1].imshow(pred)
    axes[1].set_title("② モデルの予測 / prediction\n（同じ画像・同じ学習済み重み / same images and weights）",
                      fontsize=9)
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])

    fig.suptitle("同じ 16 枚を、正解と予測で並べる / the same batch seen as truth and as prediction",
                 fontsize=10)
    _note(fig, "図：" + PROVENANCE_TEST
               + " — source: training_results/day04/test_evaluation/val_batch0_{labels,pred}.jpg")
    return _save(fig, out_dir / "ref_detections_label_vs_pred.png")


# ---------------------------------------------------------------------------
# Day 5: 元画像・異常マップ・重ね表示 / original, anomaly map and overlay
# ---------------------------------------------------------------------------


def _anomalib_panels(root: Path) -> list[Path]:
    folder = root / "training_results" / "day05" / "Patchcore" / "pvc_sheet" / "latest" / "images" / "test"
    panel_paths = sorted(folder.rglob("*.png")) if folder.exists() else []
    if not panel_paths:
        raise MissingSource(f"no anomalib visualisations under {folder}")
    return panel_paths


def _split_panels(path: Path) -> list[np.ndarray]:
    image = np.asarray(Image.open(path).convert("RGB"))
    width = image.shape[1] // 4
    # 各パネル上部の「Image」「Gt Mask」という見出し帯を落とす（列見出しは図の側で付ける）
    # drop the per-panel banner strip; the column titles are added by the figure itself
    band = int(round(image.shape[0] * 0.17))   # 見出し帯は上から約 17% / the banner sits in the top 17%
    return [image[band:, i * width:(i + 1) * width] for i in range(4)]


def ref_anomaly_panels(root: Path, out_dir: Path) -> Path:
    panels = _split_panels(_anomalib_panels(root)[0])
    original, overlay = panels[0], panels[2]

    fig, axes = plt.subplots(1, 3, figsize=(12.2, 4.0))
    axes[0].imshow(original)
    axes[0].set_title("① 元の画像 / original", fontsize=8.8)

    axes[1].imshow(overlay)
    axes[1].set_title("② 異常マップ / anomaly map", fontsize=8.8)

    axes[2].imshow(overlay)
    axes[2].set_title("③ 同じ図に目盛り / with a scale", fontsize=8.8)
    cax = make_axes_locatable(axes[2]).append_axes("right", size="6%", pad=0.06)
    cbar = fig.colorbar(cm.ScalarMappable(cmap="jet", norm=plt.Normalize(0, 1)), cax=cax)
    cbar.set_label("正規化スコア / normalised score", fontsize=7.4)
    cbar.ax.tick_params(labelsize=7)

    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])

    fig.suptitle("元画像・異常マップ・重ね表示（同じ 1 枚の実際の出力）/ "
                 "original, anomaly map and overlay for one real image", fontsize=10)
    _note(fig, "図：" + PROVENANCE_TEST
               + " — source: training_results/day05/Patchcore/pvc_sheet/latest/images/test/\n"
                 "色の目盛りは 0〜1 に正規化したスコアです。0 が「学習した正常の範囲」、1 がこの較正での最大に対応します。")
    return _save(fig, out_dir / "ref_anomaly_panels.png")


# ---------------------------------------------------------------------------
# Day 5: 5 つの列で同じ画像を比べる / five aligned columns for the same images
# ---------------------------------------------------------------------------


def _yolo_boxes(weights: Path, image_path: Path, conf: float, imgsz: int) -> list[tuple]:
    from ultralytics import YOLO

    model = YOLO(str(weights))
    result = model.predict(source=str(image_path), conf=conf, imgsz=imgsz, verbose=False,
                           device="cpu")[0]
    boxes = []
    names = result.names
    for box in result.boxes:
        x1, y1, x2, y2 = (float(v) for v in box.xyxy[0].tolist())
        boxes.append((x1, y1, x2, y2, float(box.conf[0]), names[int(box.cls[0])]))
    return boxes


def ref_comparison_5col(root: Path, out_dir: Path) -> Path:
    from ultralytics import YOLO  # noqa: F401  (fail early and clearly if it is missing)

    scores = {row["image"].replace("\\", "/"): row for row in _read_scores(root)}
    summary = json.loads(_require(root / "submissions" / "day05" / "comparison_test_results.json")
                         .read_text(encoding="utf-8"))
    thresholds = {row["method"]: float(row["threshold"]) for row in summary.get("test", [])}
    yolo_thr = thresholds.get("YOLO", 0.06)
    patch_thr = thresholds.get("PatchCore", 0.5)

    dataset_root = root / "assets" / "anomaly_dataset" / "pvc_sheet"
    weights = _require(root / "submissions" / "day04" / "best.pt")
    image_size = json.loads((root / "submissions" / "day05" / "split_manifest.json")
                            .read_text(encoding="utf-8"))["image_size"]

    wanted = ["test/black_spot/black_spot_0000.png", "test/good/good_test_0000.png"]
    images_root = (root / "training_results" / "day05" / "Patchcore" / "pvc_sheet"
                   / "latest" / "images")
    panel_files = {p.relative_to(images_root).as_posix(): p for p in _anomalib_panels(root)}

    rows = []
    for key in wanted:
        vis = panel_files.get(key)
        if vis is None:
            raise MissingSource(f"no anomalib visualisation for {key}")
        panels = _split_panels(vis)
        image_path = _require(dataset_root / key)
        boxes = _yolo_boxes(weights, image_path, conf=yolo_thr, imgsz=image_size)
        score_row = scores.get(key)
        if score_row is None:
            raise MissingSource(f"no saved PatchCore score for {key}")
        rows.append({
            "key": key,
            "original": np.asarray(Image.open(image_path).convert("RGB")),
            "overlay": panels[2],
            "gt": panels[1],
            "boxes": boxes,
            "score": float(score_row["score"]),
            "truly_abnormal": score_row["truly_abnormal"].strip() == "True",
        })

    fig, axes = plt.subplots(len(rows), 5, figsize=(13.2, 3.4 * len(rows)),
                             gridspec_kw={"width_ratios": [1, 1, 1, 1, 1.05]})
    if len(rows) == 1:
        axes = np.array([axes])
    titles = ["① 元画像 / original", "② YOLO の四角 / YOLO boxes",
              "③ PatchCore の異常マップ / anomaly map", "④ 正解マスク / ground truth",
              "⑤ 画像単位の判定 / image-level decision"]

    for r, row_ in enumerate(rows):
        axes[r, 0].imshow(row_["original"])
        axes[r, 1].imshow(row_["original"])
        for x1, y1, x2, y2, conf, name in row_["boxes"]:
            axes[r, 1].add_patch(patches.Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False,
                                                   edgecolor=WARN, linewidth=1.8))
            axes[r, 1].text(x1, max(8, y1 - 5), f"{name} {conf:.2f}", fontsize=6.6, color=WARN)
        axes[r, 2].imshow(row_["overlay"])
        axes[r, 3].imshow(row_["gt"])

        yolo_ng = any(conf >= yolo_thr for *_, conf, _ in row_["boxes"])
        patch_ng = row_["score"] >= patch_thr
        axes[r, 4].axis("off")
        lines = [
            f"YOLO: {'NG' if yolo_ng else 'OK'}",
            f"  検出 {len(row_['boxes'])} 件 (conf ≥ {yolo_thr:.2f})",
            "",
            f"PatchCore: {'NG' if patch_ng else 'OK'}",
            f"  score {row_['score']:.2f} (≥ {patch_thr:.2f})",
            "",
            f"正解 / truth: {'NG' if row_['truly_abnormal'] else 'OK'}",
        ]
        axes[r, 4].text(0.02, 0.95, "\n".join(lines), fontsize=8, va="top", color=INK,
                        family="monospace")
        agreement = (yolo_ng == patch_ng == row_["truly_abnormal"])
        axes[r, 4].text(0.02, 0.06, "3 者が一致 / all agree" if agreement
                        else "一致しない：どこで食い違ったかを見る\nnot all agree: say where",
                        fontsize=7.6, color=OK if agreement else BAD, va="bottom")

        for c in range(4):
            axes[r, c].set_xticks([])
            axes[r, c].set_yticks([])
        if r == 0:
            for c in range(5):
                axes[r, c].set_title(titles[c], fontsize=8.4)

    fig.suptitle("同じ画像を 5 つの列で並べる（試験用データ・しきい値は固定済み）/ "
                 "the same images in five aligned columns (test partition, frozen thresholds)",
                 fontsize=10)
    _note(fig, "図：" + PROVENANCE_TEST + " — 試しに 2 枚だけを示しています。全 26 枚の集計はノートブックで計算します。\n"
               "Source: anomalib visualisations + submissions/day04/best.pt + "
               "submissions/day05/patchcore_scores.csv. Ground truth is panel ④, never used for tuning.")
    return _save(fig, out_dir / "ref_comparison_5col.png")


# ---------------------------------------------------------------------------
# registry
# ---------------------------------------------------------------------------

OUTPUTS = {
    "ref_train_val_curves.png": ref_train_val_curves,
    "ref_score_distribution.png": ref_score_distribution,
    "ref_confidence_counts.png": ref_confidence_counts,
    "ref_detections_label_vs_pred.png": ref_detections_label_vs_pred,
    "ref_anomaly_panels.png": ref_anomaly_panels,
    "ref_comparison_5col.png": ref_comparison_5col,
}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build teaching figures from saved course runs.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--only", default=None, help="substring of a single output key")
    args = parser.parse_args(argv)

    family = configure_matplotlib()
    print(f"[font] using: {family}")
    plt.rcParams["font.family"] = [family, "DejaVu Sans"]
    plt.rcParams["font.monospace"] = [family, "DejaVu Sans Mono", "monospace"]
    plt.rcParams["axes.unicode_minus"] = False

    root = args.root.resolve()
    out_dir = root / "assets" / "reference_outputs"
    failures = []
    for name, func in OUTPUTS.items():
        if args.only and args.only not in name:
            continue
        try:
            func(root, out_dir)
        except MissingSource as error:
            failures.append(name)
            print(f"[skipped] {name}: {error}")
    if failures:
        print("\n未作成 / not produced: " + ", ".join(failures))
        print("理由は上に表示しています。図は作り話で埋めません。"
              "/ reasons above. Nothing is invented to fill the gap.")
        return 1
    print("\nDone. Reference outputs are written to assets/reference_outputs/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
