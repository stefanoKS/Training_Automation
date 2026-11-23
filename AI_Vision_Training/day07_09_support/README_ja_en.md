# Day 7–9 自動化設備研修 / Day 7–9 Automation Course

このフォルダは、第7日〜第9日の教材の正本・生成物・検証をまとめています。第1週（Day 1–6）の教材とは独立しています。

This folder contains the canonical sources, generated outputs and verification for Days 7–9. It is independent of the Week 1 (Days 1–6) course.

## 1. コースの流れ / Course flow

| 日 / Day | テーマ / Theme | ノートブック / Notebooks |
|---|---|---|
| 7 | 自動化設備の構想・機械設計 / Automation planning and mechanical design | 07-01 要求仕様と構想 / Requirements and Concept · 07-02 機械構成と空圧 / Mechanical Architecture and Pneumatics · 07-03 シリンダ・モーター・機器選定 / Equipment Selection |
| 8 | 電気設計・センサー・PLC・ラダー制御 / Electrical design, sensors and PLC control | 08-01 電気の基礎 / Electrical Fundamentals · 08-02 センサー・I/O / Sensors and I/O · 08-03 PLC・ラダー・シーケンス / PLC, Ladder and Sequence |
| 9 | 通信・試運転・改善提案 / Communication, commissioning and proposal | 09-01 産業用ネットワーク / Industrial Networking · 09-02 試運転 / Commissioning · 09-03 自動化提案 / Automation Proposal |

公式の時間割は [`COURSE_SYLLABUS_DAY07_09.md`](../COURSE_SYLLABUS_DAY07_09.md) だけです。1日は08:00–16:50（530分）で、ノートブック01が80分、02が85分、03が135分です。

The only authoritative timetable is [`COURSE_SYLLABUS_DAY07_09.md`](../COURSE_SYLLABUS_DAY07_09.md). Each day runs 08:00–16:50 (530 min): notebook 01 is 80 min, 02 is 85 min, 03 is 135 min.

## 2. 教材の場所 / Where things are

| 種類 / Kind | 場所 / Location |
|---|---|
| 正本の講義原稿 / canonical manuscripts | [`notebooks/Day07_Automation_Concept_Mechanics/`](../notebooks/Day07_Automation_Concept_Mechanics/), [`Day08_Electrical_PLC/`](../notebooks/Day08_Electrical_PLC/), [`Day09_Communication_Commissioning/`](../notebooks/Day09_Communication_Commissioning/) |
| ノートブック / notebooks | 同じフォルダの `.ipynb`（原稿から生成 / generated from the manuscripts） |
| 図 / diagrams | [`assets/diagrams/day07/`](../assets/diagrams/day07/), [`day08/`](../assets/diagrams/day08/), [`day09/`](../assets/diagrams/day09/) |
| シミュレーション / simulations | [`simulations/`](simulations/) |
| ワークシート / worksheets | [`worksheets/`](worksheets/) |
| 講師ガイド / instructor guides | [`../docs/instructor/day07_instructor_guide.md`](../docs/instructor/day07_instructor_guide.md)、day08、day09 |
| PDF | [`../docs/pdf/Day07_explanation_ja_en.pdf`](../docs/pdf/Day07_explanation_ja_en.pdf)、Day08、Day09 |
| 元PDF / source PDF | [`../docs/reference/自動化設備製作研修_5日間_詳細版_受講者用.pdf`](../docs/reference/自動化設備製作研修_5日間_詳細版_受講者用.pdf) |
| 正誤表 / errata | [`../docs/reference/Automation_Equipment_PDF_Errata_ja_en.md`](../docs/reference/Automation_Equipment_PDF_Errata_ja_en.md) |
| 移行監査 / migration audit | [`../docs/reviews/Day07_09_PDF_Migration_Audit.md`](../docs/reviews/Day07_09_PDF_Migration_Audit.md) |
| リリースレビュー / release review | [`../docs/reviews/Day07_09_Release_Review.md`](../docs/reviews/Day07_09_Release_Review.md) |

## 3. 学習の進め方 / How to study

1. 公式時間割を確認する / check the official timetable.
2. その日のノートブック01を開く / open notebook 01 of the day.
3. 最初の「実行環境」セルを実行する / run the "executable environment" cell first.
4. 本文→図→計算→演習→理解チェック→期待結果の順に進む / explanation → figure → calculation → exercise → check → expected result.
5. ワークシートに、数値・単位・仮定・未確認事項を書く / write values, units, assumptions and open items in the worksheet.
6. 完了チェックリストを確認する / check the completion checklist.

コードはオフラインで動きます。インターネット、実機、PLCソフトウェア、空圧は不要です。

The code runs offline. No internet, real machine, PLC software or compressed air is required.

## 4. 安全境界 / Safety boundary

- 本教材は教育用です。実機の配線・通電・PLC書込み・空圧供給・シリンダ動作・安全回路の調整を指示するものではありません。
- 実機作業は、リスクアセスメント、事前承認、電気的・空圧的隔離、残留エネルギー確認、ガード、有資格者の監督、復旧手順のもとで別に行います。
- 通常のPLC制御は安全機能ではありません。非常停止・ガード・インターロック・再起動防止は、独立した安全関連システムで設計・検証します。
- 電磁弁の無通電は、シリンダの安全状態を保証しません。遮断だけでは残圧は抜けません。
- 本研修の完了に、実機の通電試験は不要です。

- This is educational material. It does not authorise real wiring, energisation, PLC download, compressed air, cylinder motion or safety-circuit adjustment.
- Real work is separate and requires a risk assessment, prior approval, electrical and pneumatic isolation, stored-energy verification, guarding, qualified supervision and recovery procedures.
- Ordinary PLC control is not a safety function. Emergency stopping, guards, interlocks and restart prevention are designed and validated in an independent safety-related system.
- A de-energised solenoid does not guarantee a safe cylinder state. Isolation alone does not release residual pressure.
- Course completion does not require an energised hardware test.

## 5. 再生成 / Regeneration

`AI_Vision_Training` フォルダで、研修用の仮想環境を使って実行します。

Run in the `AI_Vision_Training` folder with the training virtual environment.

```powershell
# 1. diagrams (SVG)
.\.venv\Scripts\python.exe day07_09_support\scripts\generate_day07_09_diagrams.py

# 2. render diagrams to PNG for inspection and PDF
.\.venv\Scripts\python.exe day07_09_support\scripts\render_diagrams.py

# 3. notebooks from the canonical manuscripts
.\.venv\Scripts\python.exe day07_09_support\scripts\build_day07_09_notebooks.py

# 4. reference outputs (offline execution; no hardware)
.\.venv\Scripts\python.exe day07_09_support\scripts\generate_reference_outputs.py

# 5. three explanation PDFs
.\.venv\Scripts\python.exe day07_09_support\scripts\export_day07_09_pdf.py

# 6. validate and render every PDF page
.\.venv\Scripts\python.exe day07_09_support\scripts\check_day07_09_pdfs.py
```

正本は `.md`、`.json`、`.py`、`.svg` です。`.ipynb` と PDF は生成物です。`.ipynb` を直接編集せず、原稿を直して再生成してください。

Canonical sources are the `.md`, `.json`, `.py` and `.svg` files. `.ipynb` and PDFs are generated. Do not edit `.ipynb` directly; edit the manuscript and regenerate.

## 6. テスト / Tests

```powershell
python -m pytest day07_09_support/tests -q
node day07_09_support/tests/run_simulation_logic_tests.js
```

テストは、元PDFの不変性、9ノートブックの実行、計算、PLC状態、通信、図、PDF、時間割、保護ベースラインを確認します。

The tests verify source-PDF immutability, nine notebook executions, calculations, PLC states, networking, diagrams, PDFs, the timetable and the protected baseline.

## 7. 主要な不変条件 / Critical invariants

次の値を変更する場合は、教材・テスト・PDF・ワークシートを同時に更新してください。

If you change these values, update the lessons, tests, PDFs and worksheets together.

- タクト **42 s/個**（420分・600個）
- 実力能力 **199.92 個/時**（240×0.85×0.98）
- 摩擦力 **19.62 N**、設計力 **39.24 N**、理論内径 **11.18 mm**
- モーター軸トルク **0.477 N·m**、出力 **60 rpm**、理想トルク **9.55 N·m**、η=0.90で **8.59 N·m**
- 電気負荷 **0.73 A**
- 回収期間 **約1.42年**（316,800円/年、投資450,000円、運用費0の仮定）
- 統一I/O: X0–X3、M0、Y0、Y1（遅延ランプ）、Y2（電磁弁）、T0
- 自己保持は `(X0 AND X2) OR M0`、直列X1
- リセットは動作開始ではない。復電時に自動再起動しない。

- Takt **42 s/piece** (420 min, 600 pieces)
- Effective capacity **199.92 pieces/h** (240 × 0.85 × 0.98)
- Friction **19.62 N**, design force **39.24 N**, theoretical bore **11.18 mm**
- Motor torque **0.477 N·m**, output **60 rpm**, ideal torque **9.55 N·m**, **8.59 N·m** at η=0.90
- Electrical load **0.73 A**
- Payback **about 1.42 years** (316,800 JPY/year, 450,000 JPY investment, zero operating cost assumption)
- Canonical I/O: X0–X3, M0, Y0, Y1 (delayed lamp), Y2 (solenoid), T0
- Self-holding is `(X0 AND X2) OR M0`, with X1 in series
- Reset is not a start; power restoration does not restart automatically.

## 8. 教材の位置づけ / Status of the material

数値例とシミュレーション結果は、明示した仮定に基づく参考値です。実機の測定値ではなく、実機の設計・安全・性能を保証するものでもありません。初学者1名でのパイロットはまだ実施していません。

Numeric examples and simulation results are reference values under stated assumptions. They are not real measurements and do not guarantee a real machine's design, safety or performance. A pilot with one beginner has not yet been conducted.
