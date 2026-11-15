# 検証レポート / Test and validation report

> **2026-11-15 の追補:** 最新の変更・検査は
> [監査対応記録](reviews/2026-11-15_audit_remediation.md) を参照してください。
> コードも変更したため、以下の過去の「16 冊実行成功」は今回の版の実行検証ではありません。
>
> **15 November 2026 amendment:** See the
> [remediation record](reviews/2026-11-15_audit_remediation.md) for current checks.
> Code changed in this amendment; the historical “16 notebooks executed” below does not certify this revision.

> **このレポートは 2026 年 11 月 12 日時点の記録です。**
> その後の変更（言語ラベルの整理、時間割の一本化、教材図の追加、対話デモ、比較の較正手順）は
> [`implementation_report.md`](implementation_report.md) に記載しています。
> このファイルは **履歴として残します**。数字を現在の状態として引用しないでください。
>
> **This report records the state on 12 November 2026.** Later changes (language-label cleanup,
> the single authoritative timetable, the added teaching diagrams, the interactive demos and the
> calibration-first comparison) are described in [`implementation_report.md`](implementation_report.md).
> This file is **kept as history**; do not quote its numbers as the current state.

このファイルは「**実際に実行して確認した**」結果だけを記録します。
実行していないものは「未検証」と明記します。

This file records **only results that were actually executed**. Anything not run is
marked as unverified.

**検証日 / Date:** 2026 年 11 月 12 日 / 12 November 2026
**検証環境 / Environment:** Windows 11 (64-bit), CPython 3.11.4, CPU only (no GPU)

---

## 1. 結論 / Verdict

| 項目 / Item | 結果 / Result |
|---|---|
| ノートブックの本数 / notebooks | **16 / 16 作成済み** |
| 構造検証 / structural validation | **194 件すべて合格 / 194 passed, 0 failed**（2026-11-13 再実行） |
| 実行検証 / execution validation | **16 / 16 実行成功**（初回検証。追補はコードセルを変更していません） |
| 自動テスト / automated tests | **258 passed**（2026-11-13 再実行） |
| 未検証項目 / unverified | 下表のとおり / see the list below |

追補（視覚教材と PDF）の内容は [`implementation_report.md`](implementation_report.md) の §10〜§15 に
あります。追補ではコードセルを変更していないため、実行検証の結果はそのまま有効です。

The visual-material and PDF update is described in §10–§15 of
[`implementation_report.md`](implementation_report.md). It changed no code cell, so the execution
results above still hold.

「未検証：なし」は、**16 冊すべてを実際に最後まで実行した** という意味です。
GPU を使う設定（`device=0`）だけは、GPU が無いため実行していません（後述）。

"No unverified items" means **all 16 notebooks were executed end to end**. The only
exception is the GPU configuration (`device=0`), which cannot be run on a machine without a GPU
(see section 7).

---

## 2. 実行したコマンド / Commands that were run

```powershell
# 環境確認 / environment check
python assets\scripts\verify_environment.py --profile all

# 素材生成 / asset generation
python assets\scripts\generate_training_assets.py
python assets\scripts\prepare_datasets.py --force

# 構造検証 + 全ノートブック実行 / structural validation + full execution
python assets\scripts\validate_notebooks.py --execute all `
    --report submissions\reports\validation_report.json

# 自動テスト / automated tests
python -m pytest assets\tests -v
```

---

## 3. ノートブック実行結果 / Notebook execution results

16 冊すべてを、**上から順に最後まで実行** しました。

All 16 notebooks were executed **from top to bottom, to completion**.

| # | ノートブック / Notebook | カーネル / Kernel | 実行時間 / Time | 結果 / Result |
|---|---|---|---|---|
| 1 | 00_Environment_Setup | aivision | 2.9 s | PASS |
| 2 | Day01_01_Introduction_to_AI | aivision | 1.9 s | PASS |
| 3 | Day01_02_Pixels_and_Images | aivision | 3.1 s | PASS |
| 4 | Day01_03_Computer_Vision_Tasks | aivision | 2.7 s | PASS |
| 5 | Day02_01_Python_Basics | aivision | 1.6 s | PASS |
| 6 | Day02_02_Conditions_Loops_Functions | aivision | 2.0 s | PASS |
| 7 | Day02_03_OpenCV_Image_Processing | aivision | 2.9 s | PASS |
| 8 | Day03_01_YOLO_Concepts | aivision | 2.4 s | PASS |
| 9 | Day03_02_YOLO_Inference | aivision | 8.5 s | PASS |
| 10 | Day03_03_YOLO_Experiments | aivision | 8.6 s | PASS |
| 11 | Day04_01_YOLO_Dataset_Annotation | aivision | 2.8 s | PASS |
| 12 | **Day04_02_YOLO_Training** | aivision | **102.1 s** | PASS |
| 13 | Day04_03_YOLO_Evaluation | aivision | 12.5 s | PASS |
| 14 | Day05_01_Anomaly_Detection_Concepts | aivision | 2.7 s | PASS |
| 15 | **Day05_02_PatchCore_Training** | aivision-anomalib | **42.0 s** | PASS |
| 16 | Day05_03_YOLO_vs_PatchCore | aivision-anomalib | 2.7 s | PASS |

合計は約 **3 分 20 秒**。学習を含む 2 冊が大半を占めます。
Total about **3 min 20 s**, dominated by the two notebooks that actually train.

### 3.1 意図的なエラーセルの扱い / Handling of the deliberate-error cell

セットアップノートブックには、**わざと `NameError` を起こすセル** があります
（エラーメッセージの読み方を学ぶため）。このセルには `raises-exception` タグを付けてあり、
検証ツールはそのセルだけエラーを許します。**それ以外のセルでエラーが出れば失敗** として扱います。

The setup notebook contains a cell that **deliberately raises `NameError`** (to teach how
to read error messages). It is tagged `raises-exception`, and the validator tolerates errors only
there. **An error anywhere else fails the run.**

---

## 4. 自動テストの結果 / Automated test results

`python -m pytest assets\tests -v` の結果です。

Result of `python -m pytest assets\tests -v`.

```text
258 passed in 54.63s
```

| ファイル / File | 主な検証内容 / What is checked |
|---|---|
| `test_assets.py` | 15 枚の図の存在と可読サイズ、校正画像と記録値の一致、欠陥マスクとバウンディングボックスの一致、生成の再現性、YOLO 座標の正規化 |
| `test_datasets.py` | データ構造、`data.yaml` の必須キー、画像とラベルの 1 対 1 対応、ラベルの値域（0〜1）、ボックスが画像内、**分割間のデータ漏れ 0 件**、学習データが**正常のみ**、マスクの存在と内容 |
| `test_notebooks.py` | 16 冊の存在、日本語→英語の順序、必須セクション、演習 3 つ、コードの構文、禁止パターン（`cv2.imshow`・絶対パス）、参照アセットの実在 |
| `test_visual_assets.py` | 実行前から見える図（必須トピック 13 ノートブック分）、図の解決、Git 追跡、図ごとの「気づいてほしいこと」と問い、参考出力の出所、差し込みの冪等性、コード表示のみの図に対する静的代替 |
| `test_pdf_exports.py` | 6 つの PDF の存在とページ数、日本語文字の抽出、目次・出典ページ、空白ページ 0、ウィジェットがコードとして漏れていないこと、横長ページの使用、再生成コマンドの記載 |
| `test_language_labels.py` | `日本語：` / `English:` が戻っていないこと（17 件の fixture） |
| `test_schedule.py` | 各日の時間割が 360 分で連続していること、参照した Part の実在 |
| `test_evaluation_provenance.py` | 較正用と試験用の分離、旧方式の復活禁止、しきい値決定関数の動作 |

特に重要なのは次の 2 つです。

1. **データ漏れが 0 件**（train / val / test で画像ハッシュが重複しない）
2. **PatchCore の学習データが正常のみ**（異常画像が 1 枚でも混ざればテストが落ちる）

Two checks matter most:

1. **zero data leakage** (no image hash appears in two splits)
2. **PatchCore training data is normal-only** (a single abnormal image fails the test)

---

## 5. AI 機能の検証 / Verification of the AI functionality

「本物の AI が動いたか」を、実際の出力で確認しました。**作った数字はありません。**

"Did real AI actually run?" was confirmed from real output. **No numbers were invented.**

### 5.1 YOLO 推論 / YOLO inference

| 項目 / Item | 結果 / Result |
|---|---|
| モデル / Model | `yolo26n.pt`（初回に自動取得、`assets/models/` にキャッシュ / auto-downloaded once, cached） |
| 画像 / Image | Ultralytics 同梱の `bus.jpg` |
| 検出 / Detections | 5 件（`bus` 0.881、`person` 0.872 / 0.861 / 0.846 / 0.656） |
| クラス数 / Classes | 80（`black_spot` は **含まれない** ことを確認 / confirmed absent） |

PVC 風画像（`defect_multi.png`）では検出 0 件でした。これも **期待どおり** です
（COCO クラスに欠陥が無いため）。

On the PVC-like image (`defect_multi.png`) there were zero detections — also **expected**,
because COCO has no defect classes.

### 5.2 YOLO 学習と評価 / YOLO training and evaluation

実際にファインチューニングし、**学習に使っていない** 試験データで評価しました。

| 項目 / Item | 値 / Value |
|---|---|
| 学習設定 / config | `epochs=15`, `imgsz=320`, `batch=8`, `device=cpu`, `seed=2026` |
| 学習時間 / training time | 約 2.3 分 / about 2.3 minutes |
| 生成物 / artifacts | `best.pt`, `last.pt`, `args.yaml`, `results.csv` すべて生成を確認 |
| precision | **0.872** |
| recall | **0.889** |
| mAP50 | **0.918** |
| mAP50-95 | **0.609** |

### 5.3 PatchCore 学習と推論 / PatchCore fit and inference

Anomalib 2.7.0 の **本物の PatchCore** を CPU で学習させ、推論しました。

| 項目 / Item | 値 / Value |
|---|---|
| モデル / Model | `Patchcore(backbone="resnet18", layers=["layer2","layer3"], coreset_sampling_ratio=0.1, num_neighbors=9)` |
| 学習 / fit | 正常画像のみ（32 枚）で完了 / completed using normal images only |
| fit 時間 / fit time | 約 42 秒 / about 42 seconds |
| image_AUROC | **1.000** |
| image_F1Score | **0.974** |
| pixel_AUROC | **0.984** |
| pixel_F1Score | **0.386** |
| 正常スコア最大 / max normal score | 0.356 |
| 異常スコア最小 / min abnormal score | 0.473 |

正常品の最大スコア（0.356）と異常品の最小スコア（0.473）の間にしきい値を置けば
分離できました。**これは合成画像だからです。** 実際の PVC ではここまで分離しません。

A threshold between the maximum normal score (0.356) and the minimum abnormal score
(0.473) separates the two groups — **because the images are synthetic**. Real PVC will not separate
this cleanly.

### 5.4 YOLO と PatchCore の比較 / YOLO versus PatchCore

**現在の主手順：較正 → 固定 → 試験。** Day05_03 で較正データだけからしきい値を選び、
重み・前処理・メモリ・後処理も固定して、未使用の試験データを評価します。
保存先は `submissions/day05/comparison_test_results.json` と CSV です。
この改訂では学習・比較を再実行していません。元の JSON、分割記録、重みがないため、
同梱参考図の数値は**保存実行の例**であり、今回検証した最新成績ではありません。

**Current main protocol: calibrate → freeze → test.** Day05_03 chooses thresholds using
calibration only, freezes weights, preprocessing, memory and postprocessing too, then evaluates
untouched test data. Outputs are `submissions/day05/comparison_test_results.json` and CSV.
No training/comparison was rerun for this amendment. Without the source JSON, split record and weights,
numbers in supplied reference figures are **saved-run examples**, not freshly verified results.

再生成には Day04_02 → Day04_03 → Day05_02 → Day05_03 を実行し、保存記録と版を添付します。
異常を陽性とすると、TP=異常をNG、FP=正常をNG、FN=異常をOK、TN=正常をOK。
少数の合成画像、異なるラベル・学習予算の比較であり、工場の検査精度を示しません。

To regenerate, run Day04_02 → Day04_03 → Day05_02 → Day05_03 and retain records and versions.
With anomaly as positive: TP=abnormal called NG, FP=normal called NG, FN=abnormal called OK,
TN=normal called OK. The tiny synthetic sample and unequal labelling/training budgets do not
establish factory inspection performance.

#### SUPERSEDED / biased — 旧比較の記録 / Historical comparison archive (2026-11-15)

以下は旧方式の26枚の記録です。2026-11-15に主成績としての利用を取り下げました。
PatchCore のしきい値を同じ比較データから選んだためです。追跡のため数値を残します。

The following historical 26-image record was superseded on 2026-11-15 because PatchCore's
threshold was selected from that same comparison set. Values are retained for traceability.

| 手法 / Method | precision | recall | 正解 / correct | accuracy |
|---|---|---|---|---|
| YOLO | 1.000 | 0.550 | 17 / 26 | 0.654 |
| PatchCore | 1.000 | 1.000 | 26 / 26 | 1.000 |

**この表は公平ではありません。** PatchCore のしきい値は、この比較データ自身から
決めているため楽観的です。ノートブック内にもその旨を明記しています。

**This table is not fair.** The PatchCore threshold was derived from the comparison set
itself, so its numbers are optimistic. The notebook states this explicitly.

---

## 6. ライブラリのバージョン / Library versions

詳細は [`requirements/tested_versions.md`](../requirements/tested_versions.md)。

Full detail in `requirements/tested_versions.md`.

| 環境 / Env | 主要パッケージ / Key packages |
|---|---|
| `.venv` | numpy 2.2.6, matplotlib 3.11.2, pillow 13.0.0, pandas 3.1.1, **opencv-python 4.12.0.88**, **torch 2.15.0 (CPU)**, torchvision 0.29.2, **ultralytics 8.4.211** |
| `.venv-anomalib` | **anomalib 2.7.0**, torch 2.15.0 (CPU), torchvision 0.29.2, lightning 2.6.6, **opencv-python-headless 4.12.0.88** |

---

## 7. 実行できなかった・未検証の項目 / Not executed or unverified

正直に記載します。

Listed honestly.

| 項目 / Item | 状態 / Status | 理由 / Reason |
|---|---|---|
| GPU 学習（`device=0`, `epochs=100`） | **未実行 / not executed** | 検証環境に GPU が無い / no GPU available. コードはノートブック内に **文字列例として** 保持 / kept as a string example only |
| `torch==2.10.0` | **実行不可 / cannot run** | `c10.dll` の読み込みに失敗 / DLL load failure. `2.15.0` で代替 / replaced by 2.15.0 |
| 実工場画像での検査 / real factory images | **未検証 / not verified** | 画像が提供されていない / no images supplied. 第 2 週の課題 / Week 2 task |
| 0.3 mm 欠陥の実際の撮像 / imaging a real 0.3 mm defect | **未検証 / not verified** | 光学系が未確定 / optics not yet defined |
| Windows 以外の OS / operating systems other than Windows | **未検証 / not verified** | 検証は Windows 11 のみ / Windows 11 only |
| Python 3.12 | **未検証 / not verified** | 3.11.4 のみで検証 / verified on 3.11.4 only |

---

## 8. 残っている制限 / Remaining limitations

1. **データはすべて合成** — 実際の PVC の光学的挙動を再現していない
2. **学習画像は 64 枚** — 過学習が起きやすい条件。数字は低めに出る
3. **PatchCore の評価データは 26 枚** — 検証と試験に半分ずつ分けているため
4. **旧比較は撤回済み** — 同じデータでしきい値を調整した楽観的な記録（5.4 のアーカイブ）
5. **旧 YOLO recall 0.55 は最新成績ではない** — 現在の成績は固定した未使用試験の保存記録から報告する
6. **コンソール出力は英字のみ** — Windows の文字コード（cp932）対策。日本語はノートブックと `docs` にある

1. **All data is synthetic** — the optical behaviour of real PVC is not reproduced
2. **64 training images** — a setting where overfitting is likely; scores stay modest
3. **26 evaluation images for PatchCore** — the evaluation data is split into validation and test
4. **Comparison fairness** — PatchCore's threshold comes from the comparison set and is optimistic
5. **YOLO recall 0.55 on the shared set** — training at 320 px versus comparison images at 256 px,
   plus a distribution difference
6. **Console output is ASCII only** — a Windows codepage (cp932) safeguard; the Japanese text lives in
   the notebooks and in `docs/`

---

## 9. 推奨する追加作業 / Recommended follow-up

| 優先 / Priority | 作業 / Action | 理由 / Reason |
|---|---|---|
| 1 | 実画像を **許可を得て** 収集する / collect real images with permission | 合成データの精度は製品精度ではない / synthetic accuracy is not product accuracy |
| 2 | 照明・カメラ・距離を固定し **校正** する / fix and calibrate the optics | 0.3 mm を何画素で写すかが全てを決める / pixel size decides everything |
| 3 | 正常品の **ばらつき** を意図的に集める / collect normal variation deliberately | 偽陽性を減らす唯一の方法 / the only way to reduce false alarms |
| 4 | しきい値の決め方を **規程化** する / define a threshold procedure | 評価データから決めると楽観的になる / deriving it from evaluation data is optimistic |
| 5 | 社内データでの **AGPL-3.0 の扱い** を確認する / review AGPL-3.0 internally | YOLO の製品組み込みには確認が必要 / embedding YOLO needs review |
