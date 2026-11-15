# CMD 移行と再点検 / CMD migration and second-pass verification

実施日 / Date: **2026-11-15**. 対象 / Baseline:
`main`, `47a9626bb3d87af4a883ea0bb4c4aae4d13de632`.

この記録は今回の実行結果です。過去の実行結果を置き換えるものではありません。
This records this pass, not a rewrite of earlier runs.
The [implementation brief](../../agent/CODEX_Second_Pass_CMD_Migration_Implementation.txt)
and [second-pass audit](../../agent/Training_Automation_Second_Pass_Audit_2026-11-15.md)
were available and read. The checkout matched the audited revision.

## 1. 実装したこと / Implemented changes

- 現在のWindows向け手順をCMDに統一し、準備の正本を [START_HERE](../../START_HERE.md) に集約しました。
  Current directions use CMD, quoted Windows paths, `cd /d`, `dir`, `activate.bat`,
  session-local proxy examples, `findstr`, and standalone `REM` comments.
  The eleven steps, default two-environment preflight and instructor-approved delayed
  Anomalib exception remain. No package specifier, model architecture or timetable changed.
- チェックポイントを削除せず、正式な6フォルダだけからノートブックを取得します。
  Shared discovery ignores checkpoint paths and unrelated learner folders. A real duplicate
  lesson still fails the original uniqueness assertion.
- 1画素の参照とスライスを別の図にし、元配列と抽出配列の値を検証しました。
  Pixel inspection selects exactly `canvas[2,3]=100`; slicing shows the separate
  `[[0,0,0],[0,100,0],[0,0,0]]` result and stop-exclusive bounds.
- 実行状態、OpenCVの画素、GTと予測の区別、対応づけのラベルも改善しました。
  Additional SVG changes show executable kernel transitions, actual thresholded pixel
  tiles, explicit GT/annotation provenance, and spatial GT1/GT2/P1/P2 labels.
- 残っていた図と本文の食い違いを修正しました。
  Legacy loop diagrams now compare raw values; the separate thickness exercise's rounding
  convention is explicitly scoped. Batch/update figures and captions describe nominal
  accumulation, not universal updates per epoch. Leakage uses intensity noise, not spatial
  “sub-pixel” displacement; its crowded title area was separated.
- 起動用CMDと6冊のPDFを更新しました。学習や推論の新しい成績は作っていません。
  The launcher only starts Jupyter. All six books were rebuilt without executing notebooks
  or training models. Historical outputs retain their original provenance.

### 実機検査で見つかった追加の原因 / Additional observed launch defect

単に正しいPythonで `-m jupyter lab` を実行しても、Jupyterの子コマンドが
別環境のPATHから選ばれる場合がありました。
An initial real CMD smoke selected the host's unrelated Miniconda `jupyter-lab.exe`,
which failed with a `fastjsonschema` import error. No global installation was repaired.

手動手順では起動直前に基本環境を有効化し、ランチャーでは `setlocal` 内だけで
自分のScriptsをPATHの先頭に置きます。
Manual startup now activates the base environment first. The launcher prepends its own
Scripts directory inside `setlocal`, preserving the requested direct-interpreter launch.
Real manual and launcher startup then both passed. The launcher regression checks that
its own Jupyter entrypoint wins over the inherited PATH.

## 2. 検証結果 / Executed validation

検証には既存のリポジトリルートの `.venv`（CPython 3.11.4）を使いました。
教材直下の2環境は存在せず、新規インストールは行っていません。
Validation used the existing repository-root `.venv`, not newly installed course-local
environments. This is not a clean classroom-PC certification.

Commands below ran from the course root using `..\.venv\Scripts\python.exe`.

| 確認 / Check | 今回の結果 / Actual result |
|---|---|
| Baseline `assets\scripts\validate_notebooks.py` | **194 passed, 0 failed, 0 skipped** |
| Baseline `-m pytest assets\tests -q` | **307 passed, 1 failed**, 183.68 s; reproduced checkpoint collision |
| Final `-m pytest assets\tests -q` | **319 passed, 0 failed, 0 skipped**, 197.47 s |
| Final static notebook validator | **194 passed, 0 failed, 0 skipped**; all 16 notebooks |
| `normalize_language_labels.py --check` | **CLEAN**, files=0, lines=0 |
| Isolated `validate_notebooks.py --execute lightweight` | **204 passed, 0 failed, 6 skipped**, including **10 executed notebooks** |
| Focused CMD/launcher tests | **9 passed** on real Windows CMD |
| Focused numerical/caption/visual regressions | **44 passed** after legacy-figure fixes |
| Final combined CMD/numerical/caption checks | **53 passed**, 7.02 s, after the final notebook wording changes |
| Changed Python sources | **16 parsed**; Pylance syntax checks also passed on the new discovery/CMD tests and changed figure generators |
| SVG regeneration | All **15 SVGs**, fallbacks and manifest generated; **31 files byte-identical across two further reruns** |
| Protected files | **74/74 SHA-256 hashes unchanged** |
| Notebook metadata and outputs | All 16 notebook/kernel metadata preserved; only two code-message cells differ |
| Requirement specifiers | All non-comment requirement entries unchanged |
| `git diff --check` | Passed; generated PDFs correctly marked binary |

全319件の実行後に、Day04のMarkdown説明を名目上の勾配累積とwarmupに合わせて補足しました。
その後、関連53件・静的194件・言語チェックを再実行し、Day04とWeek1のPDFを再生成・再検査しました。
The 319-test full run preceded the final Markdown-only Day04 wording clarification.
The final 53 focused tests, 194 static checks and language check passed afterward;
Day04 and Week1 PDFs were then rebuilt and all PDF pages rechecked.

軽量実行は教材の一時コピーで行い、提出先もそのコピー内です。
Lightweight execution used an isolated course copy with a space-containing path and private
kernel aliases; both aliases used the existing base interpreter. Day05_01's NumPy-only
execution is **not** validation of an installed Anomalib environment.
The six skipped execution categories were Day03_02/03 (download/inference),
Day04_02/03 (training/evaluation), and Day05_02/03 (Anomalib).
The 204 total comprises 194 static checks plus ten successful executions.

初期のランチャーテストにはCMD引用符のテスト側不具合があり、修正して再実行しました。
The first launcher test attempt had four subprocess-quoting harness failures; these were
fixed and all nine CMD tests passed. A temporary setup PDF initially had a leading blank
page because the sampling harness retained a cover-dependent PageBreak; removing that
sample-only initial break produced 24 clean pages. Neither was hidden as a successful run.

## 3. 実際のCMD検査 / Real CMD smoke

すべて `cmd.exe /d /c` の子プロセス内で行い、システム設定は変更していません。
These checks ran in actual CMD child processes, without global policy, PATH, proxy or
administrator changes:

- `cd /d`, `dir`, `py -3.11 --version`; activation, `where python`, `sys.executable`, deactivation.
- Fictional `set "HTTP_PROXY=..."` / `set "HTTPS_PROXY=..."` and `pip list | findstr /I opencv`.
- Training-asset, dataset, teaching-diagram and SVG generation in the isolated copy; no clean/force option.
- Reference downloader with already cached inputs, followed by its offline check.
- YOLO model preload in offline mode; **no new model download**.
- Base-interpreter `verify_environment.py --profile all`: **READY**, exit 0.
  It explicitly excluded the separate Anomalib environment; this was not two-environment readiness.
- Missing environment and missing Jupyter: visible bilingual failure, exit 1.
  Isolated stub success and exit 23: correct course working directory and propagated exit code.
- Real JupyterLab startup by manual activation and by the updated launcher:
  localhost HTTP contents API responded with the expected course files; both private kernel names
  were visible. Both servers shut down through the API and exited 0.

実際のサーバー検査では、一時教材フォルダの `.venv` を既存の基本環境への
ジャンクションにしました。新規の重い環境を複製・インストールしたわけではありません。
The real server check used a session-only junction to the existing base environment inside
the spaced course path. Private kernel specs did not replace user registrations.
The initial unactivated `jupyter kernelspec list` result was not accepted as proof: it used
the unrelated dispatcher. Direct API inspection confirmed that public `aivision` and
`aivision-anomalib` registrations were absent.

**未実施 / NOT RUN:** fresh creation/install of the two course environments,
course-local Anomalib activation, Anomalib offline model preload and its independent
`verify_environment.py --profile all`, permanent user kernel registration,
new YOLO/PatchCore inference or training, GPU verification, real production-image evaluation.

## 4. 16冊の内容点検 / Notebook-by-notebook recheck

本文と図の対応、既存の数値テスト、軽量実行、静的画像を確認しました。
The focused review covered every notebook's audit topics and current linked figures.
It is not a native-speaker classroom usability sign-off.

| ノートブック / Notebook | 確認した内容 / Checked |
|---|---|
| 00_Environment_Setup | CMD vs Python vs `%pip`; intentional NameError and kernel-state loop preserved |
| Day01_01_Introduction_to_AI | Rule/learned distinction, strict Gaussian caveats, synthetic examples |
| Day01_02_Pixels_and_Images | Distinct pixel/slice values and shapes; visibility heuristic is not proof; CMD recovery |
| Day01_03_Computer_Vision_Tasks | True 249-pixel mask and exclusive `(76,102,93,119)` box; annotation vs schematic output |
| Day02_01_Python_Basics | Units, binary floats, separate later thickness-rounding convention; unsolved mass exercise |
| Day02_02_Conditions_Loops_Functions | Inclusive raw tolerance; loop values and displayed decisions agree without pre-comparison rounding |
| Day02_03_OpenCV_Image_Processing | Same-image 1.2 px/mm calibration; 475/925 px² contour areas distinct from 1508 foreground pixels |
| Day03_01_YOLO_Concepts | One `(96,72,168,132)` box, 240×240 normalisation, integer class ID and coordinate conventions |
| Day03_02_YOLO_Inference | Results/Boxes and CSV mapping; confidence is not calibrated truth; no fresh inference claim |
| Day03_03_YOLO_Experiments | Confidence filtering and resolution limitations, reference-output provenance |
| Day04_01_YOLO_Dataset_Annotation | Group leakage vs byte hashes; intensity-only near duplicates; annotation labels |
| Day04_02_YOLO_Training | Nominal accumulation/warmup throughout captions and figures; training settings and manifest logic retained |
| Day04_03_YOLO_Evaluation | Weight selection/provenance and one-to-one matching; matrix `[[1,3480/3720],[0,0]]`, TP1/FP1/FN1 |
| Day05_01_Anomaly_Detection_Concepts | Frozen backbone, normal-only fitted memory, image-score/map distinction |
| Day05_02_PatchCore_Training | Normal-memory fitting and separate calibration; only missing-dataset message changed |
| Day05_03_YOLO_vs_PatchCore | Frozen settings before untouched test; saved reference thresholds are not production claims |

日程は変更せず、シラバスに残っていた重み名だけを `yolo26n.pt` に合わせました。
Only the stale syllabus model prerequisite was corrected; durations and schedules were retained.
Optional redesigns of the remaining nine SVGs (for example a nested Results tree or separate
calibration/test lanes) were deferred; their existing source-aware schematics remain.

## 5. PDFと画像 / PDF and visual inspection

| 配布PDF / Distributed PDF | ページ / Pages | 抽出した日本語文字 / Japanese characters |
|---|---:|---:|
| [Day01](../pdf/Day01_explanation_ja_en.pdf) | 73 | 22438 |
| [Day02](../pdf/Day02_explanation_ja_en.pdf) | 82 | 21790 |
| [Day03](../pdf/Day03_explanation_ja_en.pdf) | 56 | 16088 |
| [Day04](../pdf/Day04_explanation_ja_en.pdf) | 66 | 18125 |
| [Day05](../pdf/Day05_explanation_ja_en.pdf) | 63 | 19335 |
| [Week1](../pdf/Week1_explanation_ja_en.pdf) | 329 | 96223 |

- 配布6冊の**全669ページ**を描画し、空白・用紙外の文字を自動検査しました。検出は0件です。
  All 669 distributed pages were rendered; no blank-page or text-boundary failures were detected.
  Every page contained extractable Japanese. These checks do not prove every label is readable at print size.
- 準備ノートブックは配布6冊に入らないため、一時的な**24ページ**の検査用PDFを作成しました。
  The temporary setup sample also had no blank/overflow failures. Its CMD explanation pages
  and lifecycle figure were visually opened; no seventh distributed booklet was added.
- 15枚のSVGはソースの安全性・寸法テストを通し、全フォールバックを目視しました。
  All 15 fallbacks were viewed in contact sheets, with the six changed ones also opened individually.
  Pixel hashes verified the actual embedded images: 14 in daily books, lifecycle in the setup sample.
- 修正した旧図5枚も個別に開き、PDF内の同一画素とページを確認しました。
  Legacy corrected figures were visually reviewed individually and in rendered PDF pages:
  Day02 pp.13/38 (units/loop), Day04 pp.19/27/30 (leakage/epoch/update).
- 現在の文書・ノートブックから参照される**81種類の静的画像**をデコードし、14枚の一覧で確認しました。
  All 81 unique current linked raster images were decoded and viewed in contact sheets.
  Dense historical reference figures were not re-created or claimed as new results.
  Visual review focused on the figures and selected CMD pages, not a line-by-line human reading of all 693 rendered pages.

## 6. 変更ファイル / Exact changed files

以下は今回の実装分です。パスは教材ルートからの相対表記です。
The following inventory excludes the user's pre-existing agent-file deletions and new brief/audit.

### 手順とノートブック / CMD documentation and notebooks

- [START_HERE.md](../../START_HERE.md), [README.md](../../README.md), [COURSE_SYLLABUS.md](../../COURSE_SYLLABUS.md)
- [docs/troubleshooting/installation.md](../troubleshooting/installation.md), [docs/reference_materials.md](../reference_materials.md)
- [docs/pdf/README.md](../pdf/README.md)
- [docs/test_report.md](../test_report.md), [docs/implementation_report.md](../implementation_report.md): current pointers only; historic results retained
- [This new implementation record](2026-11-15_cmd_migration.md)
- Requirements usage comments only: [base.txt](../../requirements/base.txt), [yolo.txt](../../requirements/yolo.txt),
  [anomalib.txt](../../requirements/anomalib.txt), [pdf.txt](../../requirements/pdf.txt)
- [00_Environment_Setup.ipynb](../../notebooks/00_Setup/00_Environment_Setup.ipynb)
- [Day01_02_Pixels_and_Images.ipynb](../../notebooks/Day01_AI_Fundamentals/Day01_02_Pixels_and_Images.ipynb)
- [Day04_01_YOLO_Dataset_Annotation.ipynb](../../notebooks/Day04_YOLO_Training/Day04_01_YOLO_Dataset_Annotation.ipynb)
- [Day04_02_YOLO_Training.ipynb](../../notebooks/Day04_YOLO_Training/Day04_02_YOLO_Training.ipynb)
- [Day05_02_PatchCore_Training.ipynb](../../notebooks/Day05_PatchCore/Day05_02_PatchCore_Training.ipynb)

### ソースとテスト / Sources and tests

Under [assets/scripts](../../assets/scripts):
[course_notebooks.py](../../assets/scripts/course_notebooks.py) (new),
[check_widgets.py](../../assets/scripts/check_widgets.py),
[export_explanations_pdf.py](../../assets/scripts/export_explanations_pdf.py),
[generate_svg_figures.py](../../assets/scripts/generate_svg_figures.py),
[generate_teaching_diagrams.py](../../assets/scripts/generate_teaching_diagrams.py),
[insert_lesson_figures.py](../../assets/scripts/insert_lesson_figures.py),
[normalize_language_labels.py](../../assets/scripts/normalize_language_labels.py),
[remediate_notebooks.py](../../assets/scripts/remediate_notebooks.py),
[scaffold_notebooks.py](../../assets/scripts/scaffold_notebooks.py),
[teaching_data.py](../../assets/scripts/teaching_data.py).

Under [assets/tests](../../assets/tests):
[test_cmd_documentation.py](../../assets/tests/test_cmd_documentation.py) (new),
[test_audit_remediation.py](../../assets/tests/test_audit_remediation.py),
[test_evaluation_provenance.py](../../assets/tests/test_evaluation_provenance.py),
[test_language_labels.py](../../assets/tests/test_language_labels.py),
[test_schedule.py](../../assets/tests/test_schedule.py),
[test_visual_assets.py](../../assets/tests/test_visual_assets.py).

### 生成図 / Generated figures

各行のSVGとPNGを変更しました。他の9組も再生成しましたが、バイトは変わっていません。
Both files in each row changed; the other nine regenerated pairs are byte-identical.

| SVG | PNG fallback |
|---|---|
| [teach_pixel_inspector.svg](../../assets/svg/teach_pixel_inspector.svg) | [PNG](../../assets/diagrams/teach_pixel_inspector_svg.png) |
| [teach_slice_walkthrough.svg](../../assets/svg/teach_slice_walkthrough.svg) | [PNG](../../assets/diagrams/teach_slice_walkthrough_svg.png) |
| [teach_code_cell_lifecycle.svg](../../assets/svg/teach_code_cell_lifecycle.svg) | [PNG](../../assets/diagrams/teach_code_cell_lifecycle_svg.png) |
| [teach_opencv_pixel_pipeline.svg](../../assets/svg/teach_opencv_pixel_pipeline.svg) | [PNG](../../assets/diagrams/teach_opencv_pixel_pipeline_svg.png) |
| [teach_cv_tasks_outputs.svg](../../assets/svg/teach_cv_tasks_outputs.svg) | [PNG](../../assets/diagrams/teach_cv_tasks_outputs_svg.png) |
| [teach_detection_matching.svg](../../assets/svg/teach_detection_matching.svg) | [PNG](../../assets/diagrams/teach_detection_matching_svg.png) |

Also [docs/visual_figure_manifest.md](../visual_figure_manifest.md) and five generated legacy PNGs:
[teach_loop_trace.png](../../assets/diagrams/teach_loop_trace.png),
[teach_units_conversion.png](../../assets/diagrams/teach_units_conversion.png),
[teach_epoch_batch.png](../../assets/diagrams/teach_epoch_batch.png),
[teach_training_update.png](../../assets/diagrams/teach_training_update.png),
[teach_leakage_split.png](../../assets/diagrams/teach_leakage_split.png).

### 起動とPDF / Launcher and PDFs

[start_training.cmd](../../start_training.cmd) (new); the six PDF files linked in section 5;
[docs/pdf/.gitattributes](../pdf/.gitattributes) (new).
ReportLab's mostly ASCII PDF output had been misclassified as text by Git, causing spurious
whitespace errors and enormous diffs. The directory-local binary rule fixes classification
without rewriting generated PDF bytes or hiding source whitespace errors.

## 7. 教室PCでの手動確認 / Manual classroom Windows smoke procedure

未完了のチェックを実機で行ってください。インストール手順は複製せず、
[START_HERE](../../START_HERE.md) の11ステップを使います。
Complete this checklist on an actual learner PC using the authoritative guide:

1. [ ] Windows SearchまたはエクスプローラーからCMDを開き、実際の教材パスへ `cd /d`。
   Check `dir` and `py -3.11 --version`; include a space-containing or redirected Documents path.
2. [ ] 教材直下の両環境をそれぞれ有効化し、`where python` と `sys.executable`、終了後の
   `deactivate` を確認。Verify both environments independently; do not treat the base READY as Day 5 readiness.
3. [ ] 両カーネルを登録して選択し、ノートブック内の `sys.executable` を確認。
   Verify each real kernel, cached photos/weights, both offline profiles and each interpreter's environment check.
4. [ ] 手動起動とダブルクリック起動で教材フォルダが開き、Day01の図と日本語、ウィジェット、
   保存が機能すること。Check manual and double-click launch, browser display, Day 5 kernel selection,
   saving, and shutdown. Confirm no server is left running.
5. [ ] 新しい空の一時フォルダにランチャーだけをコピーして環境不足の表示を確認。
   Test the missing/broken-environment case only in a disposable copy, never by renaming or deleting learner environments.
6. [ ] 日本語母語話者と初心者が、説明・問い・図を両言語で確認。
   Human bilingual review, print-size/PDF legibility and corporate-network behaviour remain required.
   Do not copy fictional proxy addresses into actual company configuration.

## 8. 保持したもの / Preservation

チェックポイント、提出物、モデル、学習結果、参考PNG、ライセンス素材の74ファイルは
開始時と同じハッシュです。解答の空欄、意図的エラー、カーネル名を保持しました。
All 74 protected files match their initial SHA-256 hashes. Learner placeholders, deliberate
errors, kernel names, output cells, package pins, dataset seeds and training configurations
were not changed. The two changed code cells contain only printed/setup guidance or a
missing-dataset error message.

開始時からあった `agent/` 内の2件の削除と、新しい依頼・監査ファイルはそのままです。
The user's pre-existing two agent-file deletions and two untracked input files remain as found.
The dated prior audit/remediation record was not rewritten. No commit, push, merge or PR was made.
