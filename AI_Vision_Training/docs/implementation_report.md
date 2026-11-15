# 実装・検証レポート / Implementation and validation report

## 追補 2026-11-15 / Audit remediation amendment

今回の変更・実行した検査は [監査対応記録](reviews/2026-11-15_audit_remediation.md)、
図の出典は [図の一覧](visual_figure_manifest.md) を参照してください。以下の過去の実行記録は
今回の再実行を意味しません。旧26枚比較は **SUPERSEDED / biased**（しきい値を同じデータで調整）。
現在は Day05_03 の較正 → 全設定固定 → 未使用試験を主手順とします。

See the [remediation record](reviews/2026-11-15_audit_remediation.md) for this amendment's checks,
and the [figure manifest](visual_figure_manifest.md) for sources. Historical execution records below
are not new reruns. The old 26-image comparison is **SUPERSEDED / biased** (threshold tuned on the
same data). The main method is now Day05_03: calibration → freeze all settings → untouched test.

**実施日 / Date:** 2026 年 11 月 13 日（初版）/ 14 日（改訂）/ 13 November 2026 (first issue), 14 November 2026 (revision)
**作業ディレクトリ / Working directory:** `C:\Users\14413\Documents\Training_Automation`
**教材ルート / Course root:** `C:\Users\14413\Documents\Training_Automation\AI_Vision_Training`
**検証環境 / Environment:** Windows 11 (64-bit), CPython 3.11.4, CPU only

このレポートは **実際に実行した確認** と **ソースを読んだだけの確認** と
**教室での確認がまだ必要な項目** を分けて書きます。

This report separates **checks that were actually executed**, **source-only checks**, and
**items that still need classroom validation**.

---

## 改訂（2026-11-14）：Day 1–5 校正パス / Revision: Day 1–5 correction pass

**基準リビジョン / Base revision:** `4628ebf1f0f2a4f05c4866a4a318540188d2906e`
（`day1-5_review.md` の 82 件の指摘にもとづく校正。未コミット / uncommitted）
**実施日 / Date:** 2026 年 11 月 14 日 / 14 November 2026

### 現行の数値（ノートブックから集計）/ Current figures, counted from the notebooks

| 項目 / Item | 値 / Value |
|---|---|
| ノートブック / notebooks | 16（Setup 1 ＋ Day 1〜5 各 3） |
| Markdown セル / markdown cells | 725（うち「実行結果の例」を含むセル 43） |
| コードセル / code cells | 263（すべて `metadata.aivision_role` と指示バナーあり） |
| Markdown の画像参照 / Markdown image references | 70 |
| 参照されている画像ファイル / unique image files | 66（`assets/diagrams` 55、`assets/reference_outputs` 7、`assets/external_samples/open_reference` 4） |
| Git 追跡 / tracked by git | 62（教材図と参考出力） |
| Git 対象外（設置時に取得）/ gitignored, downloaded at installation | 4（CC0 3 枚＋VisA 概要 1 枚） |

以下の §1〜§12 は **前回（2026-11-13）の実装時点の記録** です。図の枚数・テスト件数などは
当時の値であり、現在の検証結果ではありません。

Sections §1–§12 below record the **previous (13 November 2026) implementation**. Their figure
counts and test totals describe that revision, not the checks listed here.

### この改訂で直したこと / What this revision corrected

- 82 件の指摘（G01–G07、D101–D118、D201–D215、D301–D309、D401–D414、D501–D515、S01–S04）を
  ノートブック・講師ガイド・図の生成コード・参考出力の生成コードに反映。
- 誤った説明の代表例：AI が「決める」段階だけに限られる、左右対称＝正規分布、
  縮小するとキズが消える、YOLO ラベルの 5 値すべてが 0〜1、batch = 重み更新 1 回、
  `dfl_loss` の提示、`best.pt` の古い fitness 式、PatchCore の画像スコア = マップ最大値、
  しきい値 0 で全数 NG、テスト用データを固定前に表示、較正から報告への近道。
- 図を **生成コードから作り直し**（`generate_teaching_diagrams.py`）。矢印・軸・単位・
  コントラスト・キャプションの折り返しを修正し、模式図・合成データの明記を維持。
- 参考出力を **保存済みの数値から作り直し**（`generate_reference_outputs.py`）。
  confidence の下限 0.01（52 枚中 42 枚が候補あり）、PatchCore の
  生スコア 21.439 / 表示マップ最大 21.762 / 後処理後 1.000 を図に明記。
- 実写の参考画像 4 枚を **設置時に一度だけ取得**する仕組みを追加
  （`assets/scripts/download_reference_images.py`、Setup のセル、`ATTRIBUTION.md`・`manifest.json`）。
- 英語のみだった完了条件・表の本文を日本語と対にして整理し、
  「数値は環境によって変わります」という定型文を、決定論的な出力と記録済み実行で分けた。

### この改訂で実際に実行した確認 / Checks actually executed in this revision

| 確認 / Check | 結果 / Result |
|---|---|
| `validate_notebooks.py`（構造・二言語・図の配置） | ✅ `passed=194 failed=0` |
| `python -m pytest assets\tests -q` | ✅ **264 passed**（PDF 33 件を含む） |
| `insert_lesson_figures.py` を 2 回実行 | ✅ 2 回目は `inserted=0 updated=0`（冪等） |
| `generate_teaching_diagrams.py` で全図を再生成 | ✅ グリフ欠落なし。主要図を目視 |
| `generate_reference_outputs.py` で参考図を再生成 | ✅ 7 枚（保存済み CSV/JSON/NPZ から） |
| 画像インストーラ（空の一時フォルダ） | ✅ 4 枚取得、SHA-256 一致、`--offline` 成功、破損ファイルを拒否、復旧成功 |
| 解説 PDF の再出力 | ✅ Day01 66 ページ、Day02 74、Day03 50、Day04 59、Day05 58、Week1 297 |
| PDF のページ画像点検（Day01・Day05 全ページ） | ✅ 空白ページ 0、印刷範囲外の文字 0、表・二言語順序を目視 |
| ノートブックの再実行（学習・PatchCore の再 fit） | ❌ **未実施**（下記の限界を参照） |

### 残っている限界 / Remaining limitations

1. **ノートブックの全実行はしていません。** 変更したセルのうち、コードを変えたものは
   単体の Python スニペットで確認しましたが、Day04_02 の学習と Day05_02 の PatchCore fit は
   再実行していません（再学習は不要と判断）。
2. `submissions/day05/` の保存済み JSON（`split_manifest.json`・`patchcore_predictions.json`・
   `comparison_test_results.json`）は **前回の実行の産物** で、`score_convention` の文が
   古いままです。ノートブック側は修正済みで、Day05_02 を再実行すると新しい文で上書きされます。
3. `submissions/day05/heatmaps/` の画像も前回の産物（テスト用画像の重ね表示）です。
   Day05_03 は較正用の重ね表示として説明するため、Day05_02 を再実行するまでは
   保存済み画像と説明が一致しません。
4. 教室での実測（所要時間・ブラウザでのスライダー操作・初学者 1 名のパイロット）は未実施です。
5. 実写の参考写真は CC0/CC BY の 4 枚のみで、工場の実写や校正用の実写は含みません
   （校正の実写は今後の撮影待ち）。

---

## 0. 作業したルート / Which copy was edited

| 項目 / Item | 値 / Value |
|---|---|
| 作業したコピー / copy edited | `C:\Users\14413\Documents\Training_Automation\AI_Vision_Training`（このセッションのワークスペース） |
| 元リポジトリ / original repository | 同じツリー。**別コピーは編集していません** / the same tree; **no second copy was edited** |
| 同期 / synchronisation | していません / none |
| push / publish | していません / none |
| pull / reset / clean | していません / none |

仮想環境（`.venv`, `.venv-anomalib`）、モデルの重み（`assets/models`）、学習結果
（`training_results/`）は従来どおり Git の対象外です。

Virtual environments, model weights and training outputs remain out of Git.

---

## 1. 言語表記の整理 / Language presentation

**変更 / What changed**

- Markdown から `日本語：` / `English:`（太字・見出し・引用・箇条書きの各形）を **削除**。
  本文は日本語 → 英語の順序を保ったまま残しました。
- 英語見出しが英語段落の **後ろ** にあった 13〜19 箇所／ノートブックを、段落の前へ移動。
  二言語見出し（`学習目標 / Learning objectives`）と重複する英語見出しは削除。
- 対象は 16 ノートブックの Markdown セル 644 個と、教材 18 個の `.md`。
  コードセル・出力・セル ID・メタデータ・添付は触っていません。

**再現手段 / How it is reproducible**

```powershell
python assets\scripts\normalize_language_labels.py          # 適用 / apply
python assets\scripts\normalize_language_labels.py --check  # 確認のみ / check only
```

**検証 / Validation (実際に実行 / executed)**

| 確認 / Check | 結果 / Result |
|---|---|
| リポジトリ全体でラベル 0 件 / no labels left | ✅ `files=0 lines=0 RESULT: CLEAN` |
| 冪等性（2 回目で差分なし） / idempotent | ✅ 全セルで 2 回目 = 1 回目 |
| fixture テスト / fixture tests | ✅ `test_language_labels.py` 17 件（太字・コロン違い・コードフェンス・引用・インラインコード・URL・表・`日本語フォント`・`English` を語として使う文・見出し移動・重複見出し・冪等性） |

---

## 2. 時間割と必須課題 / Pacing and required work

**変更 / What changed**

- `COURSE_SYLLABUS.md` を **時間割の唯一の正** にしました。各日、09:00–12:00 と
  13:50–16:50 を **15 分単位で実際の Part に割り当て**、`必須 / 任意 / 休憩 / 予備 / 提出` を明記。
- 各日の `必須` 合計は 275〜300 分、`休憩＋予備＋提出` は 60〜85 分、**合計は必ず 360 分**。
- ノートブックは 1 日の時間割を **持たなくなりました**。かわりに
  「この日の順番・所要時間・前提・シラバスへのリンク」だけを持つ 1 セルに置き換えました。
- 存在しない Part への参照（例：`Day03_01` の Part 4〜6、`04_02` の Part 5）を削除。
- 前提整備（環境 2 つ・カーネル・データセット・モデル）を **第1日より前** に分離し、
  第1日の準備確認 4 項目と、準備未完了時の **3 つの回復案** を明記。
- 演習 3 を **任意**、完了チェックリストは **必須のみ**（`演習 1〜2`）に変更。

**検証 / Validation (実際に実行 / executed)** — `assets/tests/test_schedule.py`

| 確認 / Check | 結果 |
|---|---|
| 各日の合計 = 360 分 | ✅ 5/5 |
| 必須 270〜300 分 / 予備 60〜90 分 | ✅ 5/5 |
| 時間の隙間・重複なし（分単位の連続性） | ✅ 5/5 |
| 参照した `DayNN_NN` と `Part N` が実在 | ✅ 5/5 |
| ノートブックの所要時間 = シラバス | ✅ 16/16 |
| どのノートブックも 1 日の時間割を持たない | ✅ 16/16 |

**未検証 / Not verified:** 初学者 1 名でのパイロット。所要時間はすべて **暫定値** です。

---

## 3. 初学者向けの足場 / Beginner scaffolding

- すべてのコードセル（262 個）に、日本語 → 英語の指示バナーを付けました。
  `実行のみ / Run only`（178）、`この値を変更 / Change this value`（37）、
  `自分でコードを書く / Write your code`（47）。
- Part 0 の「フォルダ探索」「日本語フォント探索」の長いセルを、共通モジュール
  `assets/helpers/aivision.py` を呼ぶ **短いセル** に置き換え（18→15 行、50→7 行）。
  Part 0 のコードは `tags: ["advanced-prep"]` を付け、「実行するだけでよい」と明記。
- **第1日の演習 1 を、関数を書く課題から「用意された関数を実行して予想する」課題へ変更**。
  関数を書く課題は **第2日ノートブック02 の演習 1** に移しました。

**検証 / Validation (実際に実行 / executed)** — `validate_notebooks.py`
すべてのコードセルに `metadata.aivision_role` と一致するバナーがあること（194 件すべて合格）。

---

## 4. 実行前から見える図 / Visuals before execution

- 教材図 21 枚を `assets/diagrams/` に生成し、**Git の例外規則で配布物に含めました**
  （`.gitignore` の `!assets/diagrams/...` 21 行）。データセット・重み・出力は除外のまま。
- 14 の概念ノートブックに **Markdown 画像参照** を追加。ノートブックを開いた時点で、
  Python を 1 行も実行せずに図が見えます。各図には「気づいてほしいこと / What to notice」と
  学習者への問いを付けました。
- 生成スクリプトは `assets/scripts/generate_teaching_diagrams.py`（matplotlib のみ、
  AI 生成画像は不使用）。模式図・合成データ・保存済み出力は **図の中にその旨を明記**。
  色だけで OK/NG を伝えないよう、文字と形を併用しています。

**検証 / Validation (実際に実行 / executed)**

| 確認 / Check | 結果 |
|---|---|
| 図のファイルが存在 / files exist | ✅ 20/20（`teach_*`） |
| Markdown 参照がノートブックのフォルダから解決 | ✅ 全件 |
| 参照されている図が `git check-ignore` で無視されない | ✅ 全件 |
| 教材でない図・データセットは無視されたまま | ✅ `calibration_image.png`, `diagram_classification.png`, `anomaly_dataset/...` |
| 図が同じ Part のコードより前にある | ✅ 全件 |
| 6 枚の図を実際に開いて目視（日本語、ラベル、切り取り） | ✅ Jupyter 画面図・明るさ分布・IoU・パッチ近傍・スコア重ね・混同行列 |

**限界 / Limitations:** 目視したのは 6 枚です。残り 15 枚は「生成成功・参照解決・
図中に模式図/合成の明記がある」ことまでを自動で確認しています。

---

## 5. 対話デモ（5 つ＋ループステッパー）/ Interactive demos

| # | 場所 / Where | 何を動かすか / Control | 静的例 / Static example | フォールバック / Fallback |
|---|---|---|---|---|
| 1 | `Day01_02` Part 3 | RGB の 3 つの値 | `teach_rgb_channels.png` | あり / yes |
| 2 | `Day02_02` Part 2 | 5 つの測定値のループステップ | `teach_loop_trace.png` | あり / yes |
| 3 | `Day02_03` Part 2 | OpenCV しきい値（元画像・マスク・輪郭を同時） | `teach_opencv_pipeline.png` | あり / yes |
| 4 | `Day03_01` Part 3 | 予測の四角の位置（交差・合計・IoU） | `teach_iou_rects.png` | あり / yes |
| 5 | `Day03_03` Part 1 | YOLO confidence（**推論は 0.05 で 1 回だけ**） | `diagram_detection.png` | あり / yes |
| 6 | `Day05_03` Part 4 | PatchCore しきい値（**較正用データのみ**、FP/FN 表示） | `teach_score_map_overlay.png` | あり / yes |

- 重い処理は再実行しません。YOLO は最小 confidence で 1 回だけ推論して結果を保持し、
  スライダーは **その結果を絞り込むだけ**（選択できる下限は 0.05、それ未満は存在しない旨を表示）。
- PatchCore のスライダーは **試験用スコアを読み込みません**。動かしても最終表は汚れません。
- すべて `continuous_update=False`（重い描画）または軽量描画のみ。出力は毎回消去。

**検証 / Validation (実際に実行 / executed)** — `assets/scripts/check_widgets.py`

```text
Day01_02_Pixels_and_Images: widget cells=1 rendered=1 fallback=0
Day02_02_Conditions_Loops_Functions: widget cells=1 rendered=1 fallback=0
Day02_03_OpenCV_Image_Processing: widget cells=1 rendered=1 fallback=0
Day03_01_YOLO_Concepts: widget cells=1 rendered=1 fallback=0
Day03_03_YOLO_Experiments: widget cells=1 rendered=1 fallback=0
Day05_03_YOLO_vs_PatchCore: widget cells=1 rendered=1 fallback=0
```

**未検証 / Not verified:** ブラウザ（JupyterLab）での **実際のクリック操作**。
JupyterLab サーバーを起動していないため、確認したのは「ウィジェット表示
（`application/vnd.jupyter.widget-view+json`）が出たこと」までです。
フォールバック経路は、`ipywidgets` を入れる前の実行で 10 ノートブックすべて成功しています。

---

## 6. 比較と較正 / Comparison and calibration

**以前の問題 / What was wrong:** Day05_03 は「正常スコア最大と異常スコア最小の中央」を
PatchCore のしきい値にし、**同じ結合データで評価** していました。警告文だけでは不十分でした。

**現在の流れ / The current workflow**

1. **分割の記録**（`submissions/day05/split_manifest.json`, `schema_version: 2`）
   — anomalib `Folder(val_split_mode="from_test", val_split_ratio=0.5, seed=...)` が実際に作った
   分割を、画像パスで書き出します。学習 32 枚 / 較正 26 枚 / 試験 26 枚。
   重なりは 0（assert で強制）、YOLO 学習画像との重なりも 0。
   anomalib 既定の `PostProcessor`（`enable_normalization=True`）は **検証（較正）分割** の
   min/max で正規化することを確認し、その旨を manifest と `score_convention` に記録。
2. **YOLO 側**は `conf=0.01` で 1 回だけ推論し、全 52 枚の最大 confidence を保存
   （`schema_version: 2`, `min_inference_conf: 0.01`）。しきい値は後から 0.01 以上で選べます。
3. **較正**（`calibration` 26 枚）で 2 つのしきい値を **共通の目的関数** で決定：
   **正常品の誤報率 ≤ 10% の条件で recall を最大**（同点はしきい値の高い方）。
4. しきい値を **固定** し、`test` 26 枚で **1 回だけ** 評価。
   画像単位で TP/FP/FN/TN、recall、誤報率、precision、分母を表示。`nan` は 0 と区別して表示。
5. 結果は `submissions/day05/comparison_test_results.json` に、分割・モデル・目的関数・
   スコア定義・モデル識別子と一緒に保存。旧 `yolo_vs_patchcore.csv` は
   `superseded` として **上書きせず** 残しています。
6. 古い形式のファイル（`schema_version != 2`）は理由を表示して **停止** します。
   片方の結果が無い画像は、**除外した枚数とファイル名を表示** します（黙って inner join しない）。

**実際に実行した結果 / Results actually obtained（2026-11-13, seed 2026）**

```
calibration (n=26: normal 6, abnormal 20)
method     threshold  recall  false_reject_rate  TP  FP  FN  TN
YOLO           0.06    1.000              0.000   20   0   0   6
PatchCore      0.50    1.000              0.000   20   0   0   6

test (n=26: normal 6, abnormal 20) — thresholds frozen
method     threshold  TP  FP  FN  TN  recall  false_reject_rate
YOLO           0.06    20   0   0   6   1.000              0.000
PatchCore      0.50    19   0   1   6   0.950              0.000

coverage: 52 images with both results, 0 excluded
```

**読み方 / How to read it:** 較正では両方 1.000 でしたが、**試験では PatchCore が 1 件見逃しました**。
これは「較正で完璧＝現場で完璧ではない」という、この研修で一番伝えたい事実です。
正常 6 枚では誤報率 10% は「誤報 0 枚」を意味するため、しきい値の根拠は弱いことも
ノートブックと講師ガイドの両方に書いてあります。

**検証 / Validation (実際に実行 / executed)** — `assets/tests/test_evaluation_provenance.py`

- 旧式（正常最大＋異常最小の中央）が **復活していない** こと（禁止文字列 3 種）
- 較正用・試験用の分離、`schema_version`、`superseded` マーク、除外枚数の表示
- `choose_threshold()` を **実際に実行** して、FP 上限内で recall 最大のしきい値を選ぶこと、
  正常品が 0 枚なら `None` を返すこと
- PatchCore が **正常のみ** で fit していること、正規化が試験データで fit されないこと

---

## 7. 実行した確認の一覧 / Everything that was run

| # | コマンド / Command | 結果 / Result |
|---|---|---|
| 1 | `python assets\scripts\normalize_language_labels.py --check` | ✅ CLEAN |
| 2 | `python assets\scripts\scaffold_notebooks.py`（2 回） | ✅ 2 回目は `changed=0`（冪等） |
| 3 | `python assets\scripts\validate_notebooks.py` | ✅ **194 passed, 0 failed** |
| 4 | `python -m pytest assets\tests -q` | ✅ **208 passed** |
| 5 | `python assets\scripts\generate_teaching_diagrams.py` | ✅ 20 図、グリフ欠落警告 0 |
| 6 | `python assets\scripts\validate_notebooks.py --execute lightweight` | ✅ 10/10 実行成功（新しいカーネルから） |
| 7 | `python assets\scripts\check_widgets.py` | ✅ 6/6 がウィジェット表示 |
| 8 | Day04_03 を nbclient で実行 | ✅ 16.4 秒、予期しないエラー 0 |
| 9 | Day03_02 を nbclient で実行 | ✅ 8.3 秒、エラー 0 |
| 10 | Day03_03 を nbclient で実行（`check_widgets` 経由） | ✅ エラー 0 |
| 11 | Day05_02 を nbclient で実行（`aivision-anomalib`） | ✅ 45〜47 秒、エラー 0（PatchCore fit を含む） |
| 12 | Day05_03 を nbclient で実行（`aivision-anomalib`） | ✅ 3.5 秒、エラー 0 |
| 13 | `git check-ignore` による図の配布可否 | ✅ 教材図 21 枚は追跡、それ以外は無視 |
| 14 | 生成図 6 枚の目視確認 | ✅ |

**実行していないもの / Not executed**

- `validate_notebooks.py --execute all`（Day04_02 の学習を含む全実行）
- ブラウザでの JupyterLab 操作（サーバー未起動）
- 初学者 1 名でのパイロット（時間測定）

---

## 8. 依存関係の提案 / Proposed dependency changes

| パッケージ / Package | 変更 / Change | 理由 / Why | 検証した環境 / Verified in |
|---|---|---|---|
| `ipywidgets` | **追加 `==8.1.9`** | 5 つの対話デモに必要。jupyterlab 4.6.6 / ipykernel 7.4.0 と同時に動作を確認 | `.venv` と `.venv-anomalib` の **両方** に導入し、6 デモの表示とノートブック実行を確認 |
| `jupyterlab_widgets` | 追加（依存で自動、3.0.17） | Lab 4 でウィジェット表示に必要 | 同上 |
| `widgetsnbextension` | 追加（依存で自動、4.0.16） | 同上 | 同上 |

`ipywidgets` は **任意** です。無くても各ノートブックのパラメータセルで同じ実験ができ、
そのことは実際に（導入前の実行で）10 ノートブックを実行して確認しました。
他の pin（numpy / opencv / torch / ultralytics / anomalib など）は **変更していません**。

`ipywidgets` is optional; without it the parameter cells run the same experiments — verified by
executing the 10 lightweight notebooks before installing it. No other pin was changed.

---

## 9. 教室での確認が必要なこと / Still needs classroom validation

1. **所要時間の実測**（初学者 1 名のパイロット）。現在の分は設計値です。
2. **ブラウザでのスライダー操作**（描画は確認済み、操作は未確認）。
3. **Day04_02 の学習を含む全実行**（CPU 時間が長いため未実施）。
4. **古い比較結果の扱い**: `submissions/day05/yolo_vs_patchcore.csv` は旧方式の産物として
   残しています。教室で「これは今の方法の結果ではない」と説明してください。
5. **副教材**: 画面操作の短い録画は未作成です（要件どおり必須ではありません）。

---

# 追補（視覚教材と解説 PDF）/ Update: visuals and explanation PDFs

**実施日 / Date:** 2026 年 11 月 13 日 / 13 November 2026
**作業したコピー / Copy edited:** `C:\Users\14413\Documents\Training_Automation\AI_Vision_Training`
（1 つのコピーのみ。pull / reset / clean / push はしていません / one copy only; nothing pulled, reset,
cleaned or pushed）

## 10. 何が足りなかったか / What the first pass left out

最初の実装は、図 20 枚・対話デモ 6 つ・較正の修正まで到達していましたが、次の 5 点が
要件に対して不足していました。**すべて今回の追補で対応しました。**

| # | 不足していたこと / Gap | 追補での対応 / What was added |
|---|---|---|
| 1 | 必須トピックの図が 9 つ無い（学習と推論、条件、四角の座標、confidence、解像度、物体単位の対応、スコア分布、5 列比較、セットアップ手順） | 概念図 7 枚を新規生成、実測図 6 枚を新規生成 |
| 2 | 「実行しないと見えない図」が 17 箇所あった | 各トピックに実行前から見える静的図を用意（対応表は §11） |
| 3 | 解説 PDF が 1 冊も無かった | 日別 5 冊＋週まとめ 1 冊を生成（§12） |
| 4 | 図が実測か合成かの区別が、生成スクリプト任せだった | 実測図を `assets/reference_outputs/` に分離し、図の中と README に出所を明記 |
| 5 | 新しい図を配布物に含める規則が無かった | `.gitignore` の例外を 13 行追加（教材図 7＋参考図 6） |

## 11. 視覚カバレッジ / Visual coverage by notebook

「実行前から見える図」だけを数えています。備考の「コード表示のみ」は、ノートブックの
コードが画像を表示している箇所で、同じ概念には静的図を別に用意したものです。

Only figures visible **before execution** are counted. "code-only" means the notebook also draws an
image from code; a static figure for the same idea exists separately.

| ノートブック / Notebook | 静的図 / static figures | 主な図 / main assets | 教育上の狙い / why |
|---|---|---|---|
| `00_Environment_Setup` | 2 | `teach_setup_jupyter_ui`, `teach_setup_workflow` | 画面のどこを押すか、エラーからどう戻るか |
| `Day01_01_Introduction_to_AI` | 3 | `teach_rule_vs_learned`, `teach_brightness_shift`, `teach_train_vs_inference` | 決まった規則と例から学ぶことの違い、学習と推論の役割 |
| `Day01_02_Pixels_and_Images` | 3 | `diagram_pixel_grid`, `teach_rgb_channels`, `teach_downsample_defect` | 画素・座標・RGB・解像度の結び付き |
| `Day01_03_Computer_Vision_Tasks` | 1 | `teach_cv_tasks_outputs` | 4 つのタスクの出力の違い（分類・検出・セグメンテーション・異常検知） |
| `Day02_01_Python_Basics` | 1 | `teach_variable_trace` | 変数の値が実行の各段で変わること |
| `Day02_02_Conditions_Loops_Functions` | 3 | `teach_condition_branch`, `teach_loop_trace`, `teach_function_io` | 条件で分かれる流れ、5 件のループ、入力→処理→出力 |
| `Day02_03_OpenCV_Image_Processing` | 2 | `teach_opencv_pipeline`, `teach_pixel_to_mm` | 元画像→グレー→2 値化→輪郭、px→mm の計算 |
| `Day03_01_YOLO_Concepts` | 2 | `teach_bbox_coords`, `teach_iou_rects` | 四角を 4 つ／5 つの数で読む、交差・合計・IoU |
| `Day03_02_YOLO_Inference` | 1 | `diagram_detection` | 検出の出力が「四角の一覧」であること |
| `Day03_03_YOLO_Experiments` | 4 | `teach_confidence_filter`, `ref_confidence_counts`, `teach_resolution_effect`, `diagram_detection` | しきい値で残る数が変わる（模式図＋実測）、解像度と小さな物体 |
| `Day04_01_YOLO_Dataset_Annotation` | 2 | `teach_yolo_label_fields`, `teach_split_roles` | ラベルの 5 つの値、train/val/test と漏れ（leakage） |
| `Day04_02_YOLO_Training` | 3 | `teach_epoch_batch`, `teach_train_val_curves`, `ref_train_val_curves` | batch と epoch、曲線の読み方（模式＋実測） |
| `Day04_03_YOLO_Evaluation` | 4 | `teach_image_level_confusion`, `teach_image_level_confusion_matrix`, `teach_object_level_matching`, `ref_detections_label_vs_pred` | 画像単位と物体単位を混ぜない、正解と予測の並置 |
| `Day05_01_Anomaly_Detection_Concepts` | 1 | `teach_patch_neighbour` | パッチ→特徴→記憶→最近傍→スコア |
| `Day05_02_PatchCore_Training` | 2 | `ref_anomaly_panels`, (`teach_score_map_overlay` は Day05_03 と共用) | 元画像・異常マップ・目盛り付き重ね表示（実測） |
| `Day05_03_YOLO_vs_PatchCore` | 3 | `ref_score_distribution`, `ref_comparison_5col`, `teach_score_map_overlay` | 較正データの分布としきい値、5 列比較 |

**コード表示のみだった図 / figures that used to appear only after running code**（17 箇所）は、
すべて静的図で代替できることを `test_visual_assets.py::test_every_code_only_diagram_has_a_static_equivalent`
で確認しています。例: `diagram_control_flow`（条件）→ `teach_condition_branch`、
`diagram_dataset_split` → `teach_split_roles`、`diagram_patchcore_concept` → `teach_patch_neighbour`。

**重複させなかったもの / deliberately not duplicated:** `diagram_classification` / `diagram_segmentation`
などは `teach_cv_tasks_outputs` が 1 枚で同じ比較を示すため、本文の図は増やしていません。

## 12. 実測図と模式図の分離 / Measured figures versus schematics

| 種類 / Kind | 置き場所 / Where | 作り方 / How | 図の中の表示 / label inside |
|---|---|---|---|
| 模式図・合成データ / schematic, synthetic | `assets/diagrams/teach_*.png` | `generate_teaching_diagrams.py`（matplotlib のみ、座標と値を計算） | 「模式図 / schematic」「合成 / synthetic」 |
| 実際の実行結果 / measured | `assets/reference_outputs/ref_*.png` | `generate_reference_outputs.py`（保存済みのログ・スコア・出力を読む） | 「参考出力 / Reference output」＋出典ファイル名 |

`generate_reference_outputs.py` は入力が無ければ**図を作らずに失敗**します（`MissingSource`）。
学習のやり直しや大量の再推論はしません。唯一の例外は YOLO の四角を描くための短い推論で、
ローカルの重みと固定 `imgsz` だけを使います。

## 13. 解説 PDF / Explanation PDFs

**作ったもの / Produced**（`docs/pdf/`）

| ファイル | ページ | 日本語文字（抽出） |
|---|---|---|
| `Day01_explanation_ja_en.pdf` | 47 | 14,028 |
| `Day02_explanation_ja_en.pdf` | 50 | 12,030 |
| `Day03_explanation_ja_en.pdf` | 40 | 10,940 |
| `Day04_explanation_ja_en.pdf` | 42 | 11,099 |
| `Day05_explanation_ja_en.pdf` | 43 | 11,838 |
| `Week1_explanation_ja_en.pdf` | 214 | 58,100 |

**再生成の 1 コマンド / the one regeneration command**

```powershell
python assets\scripts\export_explanations_pdf.py
```

（初回のみ `python -m pip install -r requirements\pdf.txt`。学習者用の `base.txt` とは分離）

**方針 / Design**

- 原稿は**ノートブックの Markdown そのもの**から組むので、説明が 2 か所に分かれて食い違うことがありません。
- 目次（ページ番号付き）・A4・日本語フォント埋め込み・ページ番号・キャプションを実装。
- 図とキャプションは `KeepTogether` で同じページに置きます。横長の図は A4 横向きページに置き、
  文字が潰れないようにしました（縦向きだと 9 pt が 5 pt 以下になります）。
- 含めないもの: セル出力（ログ・スタックトレース）、20 行を超えるコード、`advanced-prep` タグのセル、
  `%pip`／`pip install` を含むセル、`docs/instructor/` を指す行（講師用解答）、生の JSON。
- 対話ウィジェットのセルは、コードを出さずに
  「この節はノートブック上での対話操作です。PDF では前の静的図で代わりに示しています。」に置換。
- 出力の節（`実行結果の例`）は、本文が無ければ
  「ノートブックで実行すると表示されます」という注記に置換（推測で出力を書かない）。
- モデルのダウンロード・学習・ノートブックの実行は**しません**（Markdown と保存済み画像のみ）。

## 14. 追補で実行した確認 / Checks run for this update

| # | コマンド / Command | 結果 / Result |
|---|---|---|
| 1 | `python assets\scripts\generate_teaching_diagrams.py` | ✅ 27 図（新規 7 を含む）、グリフ欠落警告 0 |
| 2 | `python assets\scripts\generate_reference_outputs.py` | ✅ 6 図（すべて保存済みの実行結果から） |
| 3 | `python assets\scripts\insert_lesson_figures.py`（2 回） | ✅ 13 箇所を差し込み、2 回目は 0 件（冪等） |
| 4 | `python assets\scripts\validate_notebooks.py` | ✅ 全ノートブック合格（図が Part のコードより前、日英順、画像解決） |
| 5 | `python -m pytest assets\tests -q` | ✅ **258 passed**（追補前 208、+50） |
| 6 | `python assets\scripts\export_explanations_pdf.py` | ✅ 6 PDF、ページ数と日本語文字数を表示 |
| 7 | `python assets\scripts\inspect_pdf_pages.py` | ✅ 全 436 ページを描画。空白ページ 0、印刷範囲外の文字 0 |
| 8 | PDF の目視（コンタクトシート） | ✅ 下記の範囲を実際に開いて確認 |

**目視したページ / pages inspected by eye:** Day01 全 47 ページ、Day02 全 50、Day03 全 40、
Day04 全 42、Day05 全 43（4〜12 ページずつのコンタクトシートで全ページ）。
Week1 は同一内容の再掲のため、冒頭・中間・末尾のシートを確認し、残りは
`inspect_pdf_pages.py` の自動判定（空白・はみ出し）に委ねました。

**数えた結果 / counts:** 図の参照は 16 ノートブックで **37 箇所・35 種類**
（`assets/diagrams` 31 + `assets/reference_outputs` 6）。`teach_*.png` は 27 枚すべて、
`ref_*.png` は 6 枚すべてが、どこかのノートブックから参照されています。

## 15. 追補の限界 / Limits of this update

1. **PDF の文字は図の中では検索できません**（図は画像として埋め込み）。
2. **横長ページで余白が出ます**（読みやすさを優先した結果）。
3. **Week1 PDF の全 214 ページは目視していません**（日別 PDF と同一内容の再掲のため）。
4. **実際の学習・推論は再実行していません**。参考図は 2026-11-12 の保存済み結果に基づきます。
5. **所要時間の実測は未実施**（初学者パイロット待ち）。
6. `generate_reference_outputs.py` は、`submissions/` と `training_results/` が無い環境では
   図を作れません（その場合は理由を表示して停止します）。
