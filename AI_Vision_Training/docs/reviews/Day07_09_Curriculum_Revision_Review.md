# 第7日〜第9日 カリキュラム改訂 実装・検証報告 / Day 7–9 Curriculum Revision: Implementation and Verification Report

> 実装日 / implementation date: 2026-11-24
> 開始コミット / starting commit: `643ab47f98cc14520b9d8c65078a82dd2e602d2d`（`643ab47`）
> 最終状態 / final state: **未コミットの作業ツリー**（コミット・プッシュは指示がないため行っていません） / **uncommitted working tree** (no commit or push was performed)

## 1. 開始時の状態 / starting state

- ブランチ `main`、作業ツリーはクリーン（開始時点）。 / Branch `main`, clean working tree at the start.
- 元PDF `docs/reference/自動化設備製作研修_5日間_詳細版_受講者用.pdf` の SHA-256 は `3380c2b67e148cd9a71b0f9071963744f3b0acba7491b309708b0f31183707ae`、51ページ。改訂後も同じ値で51ページであることを確認。 / Unchanged hash and page count after the revision.
- 既存の Day 7〜9 テストは 39 passed / 1 failed。失敗は Day 1〜6 保護ベースライン（`Day01_01_Introduction_to_AI.ipynb`）の不一致。原因は**この作業と無関係な外部プロセスによる同日 13:32 の書き換え**（Nepali 挿入ブロックの消失、`LastWriteTime` 13:32:03）。 / The pre-existing suite had one failure in the Day 1–6 baseline, caused by an external rewrite of a Day 1 notebook, not by this change.
- 同じ環境で別のエージェントプロセス（`codex`）が稼働していたため、Day 1〜6 のファイルには一切触れていません。 / Another agent process was running in the shared environment, so no Day 1–6 file was edited.

**Day 1 ノートブックの扱い / treatment of the Day 1 notebook**

外部で書き換えられていた `notebooks/Day01_AI_Fundamentals/Day01_01_Introduction_to_AI.ipynb` を、HEAD（開始コミット）の内容に復元しました。復元前の内容は
`<session-state>/files/external-change-backup/Day01_01_Introduction_to_AI.ipynb.modified` に保存しています。
The externally modified Day 1 notebook was restored to the HEAD content. The modified copy is kept in the session-state backup folder shown above.

理由：保護ベースライン（`protected_baseline_hashes.txt`）と HEAD が一致しており、外部変更は Day 5 Tamang/Nepali 実装の一部を削除するものだったため。復元により Day 1〜6 の保護テストは通過します。
Rationale: HEAD and the recorded baseline agreed, and the external change had removed part of the Day 5 Tamang/Nepali content. Restoring it makes the Day 1–6 protection test pass again.

## 2. 経営要求の要約 / summary of the management requirements

| 日 / Day | 要求 / Requirement | 実装 / Implementation |
|---|---|---|
| 7 | 稼働率不要 / no availability | 稼働率・OEE・実力能力の計算を必須教材から削除。 / Availability, OEE and effective-capacity models removed from required content. |
| 7 | セル不要 / no manufacturing cells | セル生産の項目を削除。 / Cell organisation excluded. |
| 7 | 演習は簡単な部分だけ / only simple exercises | 各ノートブック1〜2問、直後に解答。 / One or two questions per notebook, answers immediately after. |
| 7 | 能力・効果金額の計算 / capacity and economic effect | 07-01 に集約。タクト42秒、240個/時、316,800円/年、1.42年・1.69年。 / Centralised in 07-01 with the stated numbers. |
| 7 | シリンダ・モーター・その他アクチュエータ / actuators | 07-02 で空圧・油圧・電気と用途を整理。 / Pneumatic, hydraulic and electric power and applications in 07-02. |
| 7 | 油圧・空圧・電気の動力 / power sources | 油圧を新設。 / A dedicated hydraulic section was added. |
| 7 | 選定に必要な仕様 / selection specifications | 07-03 で16項目の仕様と計算。 / Sixteen specifications and the calculations in 07-03. |
| 8 | 電圧の役割 100/200/24/12/5V | 08-01 §5。 / 08-01 section 5. |
| 8 | 制御盤の機器の役割 / panel components | 08-01 §6、18機器。 / 08-01 section 6, eighteen devices. |
| 8 | IN/OUT / inputs and outputs | 08-02 §4。 / 08-02 section 4. |
| 8 | センサーの選定・種類 / sensors | 08-02 §5–§6、10段階の選定手順。 / 08-02 sections 5-6 with a ten-step workflow. |
| 8 | PNP・NPNとPLC選定 / NPN/PNP and PLC selection | 08-02 §7–§8、電流経路と入力共通。 / 08-02 sections 7-8 with current paths and input commons. |
| 8 | ラダーとは / ladder from zero | 08-03 §5–§6。 / 08-03 sections 5-6. |
| 8 | 自己保持とインターロック | 08-03 §7–§9（再起動防止を含む）。 / 08-03 sections 7-9, including restart prevention. |
| 8 | 消費電力 / power consumption | 08-01 §7–§8。 / 08-01 sections 7-8. |
| 9 | 20ページ目以降不要 / no page 20 onward | **19ページ**に再構成（表紙・目次・付録込み）。 / Rebuilt to **19 pages** including cover, contents and appendices. |
| 9 | AIカメラ自作に向けて / towards a custom AI camera | 09-03 で構成・手順・判定。 / Architecture, workflow and decision in 09-03. |
| 9 | カメラと環境 / camera and environment | 09-01・09-02。 / 09-01 and 09-02. |

## 3. 旧カリキュラムとの比較 / old-to-new comparison

| 旧 / Old | 新 / New |
|---|---|
| 07-01 要求仕様と構想（ECRS、3案比較、稼働率込み能力、受入基準） | 07-01 生産能力と効果金額（タクト、必要能力、理論能力、純効果、回収期間） |
| 07-02 機械構成と空圧（5機能、BOM、側荷重） | 07-02 動力とアクチュエータ（空圧・油圧・電気、単動/複動、グリッパ、真空） |
| 07-03 シリンダ・モーター選定（BOM、版管理、カタログ探索） | 07-03 選定の仕様と計算（16仕様、押し/引き、摩擦、トルク、実務例） |
| 08-01 電気の基礎とDC24V | 08-01 電気の基礎・電圧の使い分け・制御盤の機器 |
| 08-02 センサー・I/O・電気インターフェース | 08-02 センサーの種類・選定・入出力・NPN/PNP |
| 08-03 PLC・ラダー・シーケンス（状態機械、異常マトリクス） | 08-03 PLCとラダー・自己保持・インターロック（再起動防止を分離） |
| 09-01 産業用ネットワーク（サブネット、TCP/UDP、Modbus） | 09-01 カメラ・レンズ・撮像条件の基礎 |
| 09-02 試運転（ゲート、試験マトリクス、引継ぎ） | 09-02 照明・反射・撮像環境 |
| 09-03 自動化提案（24項目、10分発表、費用対効果） | 09-03 AI検査カメラの構成と自作の流れ（構成・手順・判定・チェックリスト） |

`Day09_Communication_Commissioning` は削除し、`Day09_AI_Camera_Imaging` を新設しました。旧教材は Git 履歴から復元できます。 / The old Day 9 folder was removed and `Day09_AI_Camera_Imaging` created; the old material remains recoverable from Git history.

## 4. 技術的な修正 / technical corrections

1. **自己保持と再起動防止の混同**：基本のシールイン（`M0 = X1 AND (X0 OR M0)`）と、アーム・立ち上がり検出・STOP優先・位置確認・リセット分離を含む拡張ロジックを別々に提示。シミュレータとテストの挙動を一致させました。 / Basic seal-in and the extended restart-prevention logic are now separate; simulator and tests agree.
2. **物理NC接点の扱い**：物理NCのSTOPをON許可として使う説明を維持し、「NCスイッチは必ずNC論理接点」という規則を否定。 / The physical NC stop used as an ON permission is kept; the false rule about NC instructions is rejected.
3. **同時指令の扱い**：相互に打ち消すだけの回路がスキャン順に依存することを明示し、同時要求は「両方OFF（拒否）」という決定的な設計に。 / Cross-linked interlocks are shown to depend on scan order; simultaneous requests are deterministically rejected.
4. **NPN/PNP**：電流経路（PNP: +24V→センサー→PLC→0V、NPN: +24V→PLC→センサー→0V）と入力共通（0V/+24V）を図とテストで固定。PLC全体を「NPN型」と呼べないことを明示。 / Current paths and input commons are fixed in text, figure and tests; "an NPN PLC" is explicitly rejected.
5. **保護機器**：遮断器・漏電遮断器・ヒューズ・サーマルリレーの守る範囲を分離。サーマルは短絡保護ではないと明示。 / Protective-device coverage is separated; the overload relay is not short-circuit protection.
6. **用語**：フィルタレギュレータとFRLユニットの混同、本質安全防爆の誤用、潤滑の条件性を修正。 / Filter regulator versus FRL, misuse of "intrinsically safe", and conditional lubrication corrected.
7. **油圧**：専用節を新設し、「油圧は常に強い・速い・効率がよい」という断定を否定。 / A dedicated hydraulic section was added, rejecting the claim that hydraulics are always stronger, faster or more efficient.
8. **カメラ**：「4ピクセルなら検出可能」「カメラFPS＝検査FPS」「グローバルならぶれない」を否定。 / "Four pixels is enough", "camera FPS equals inspection FPS" and "a global shutter has no blur" are rejected.
9. **検査判定**：OK/NG/無効（INVALID）を分離し、無効をOKにしないことをモデル・テスト・表で保証。 / OK, NG and INVALID are separated, with INVALID never treated as OK in model, table and tests.
10. **PDFの過剰な長さ**：Day 7 は58→45ページ、Day 8 は60→48ページ。 / Day 7 58→45 pages, Day 8 60→48 pages.

## 5. 図の変更 / diagram changes

- 旧：Day 7 = 9、Day 8 = 11、Day 9 = 9（計29、うち Day 9 はネットワーク・試運転・提案）。
- 新：Day 7 = 14（D07-01〜14）、Day 8 = 14（D08-01〜14）、Day 9 = 11（D09-01〜11）。計 **39**。
- すべて自作の編集可能なSVGで、日英ラベルを持ち、`title`/`desc` を備えます。PNGは点検用とPDF用に Inkscape で描画。
- 旧 Day 9 の図（ネットワーク・試運転）は削除し、古いPNG（`D09-12.png`、`sim_commissioning.png`）も削除。
- 各図はマニフェストと教材本文の両方から参照されていることをテストで確認。

- Old: 9 / 11 / 9 (29, Day 9 about networking, commissioning and proposals). New: 14 / 14 / 11 (39).
- Every figure is an original editable SVG with Japanese and English labels plus `title`/`desc`; PNGs are rendered with Inkscape for inspection and the PDF.
- Old Day 9 figures and stale PNGs (`D09-12.png`, `sim_commissioning.png`) were removed.
- Tests confirm each figure is referenced both by the manifest and by a manuscript.

## 6. 変更・作成・削除したファイル / files changed, created and removed

### 6.1 作成 / created

- `notebooks/Day07_Automation_Concept_Mechanics/Day07_01_Capacity_And_Effect.md`（+`.ipynb`）
- `notebooks/Day07_Automation_Concept_Mechanics/Day07_02_Power_And_Actuators.md`（+`.ipynb`）
- `notebooks/Day07_Automation_Concept_Mechanics/Day07_03_Selection_Specifications.md`（+`.ipynb`）
- `notebooks/Day09_AI_Camera_Imaging/Day09_01_Camera_Fundamentals.md`（+`.ipynb`）
- `notebooks/Day09_AI_Camera_Imaging/Day09_02_Lighting_and_Imaging_Environment.md`（+`.ipynb`）
- `notebooks/Day09_AI_Camera_Imaging/Day09_03_AI_Camera_System.md`（+`.ipynb`）
- `day07_09_support/worksheets/Glossary_day09_ja_en.md`
- `day07_09_support/worksheets/Day07_09_Assessment_Rubric_ja_en.md`（旧版を置換して再作成 / recreated after removal of the old rubric）
- 本報告書 / this report

### 6.2 削除 / removed

- `notebooks/Day07_Automation_Concept_Mechanics/Day07_01_Requirements.{md,ipynb}`
- `notebooks/Day07_Automation_Concept_Mechanics/Day07_02_Mechanical_Architecture.{md,ipynb}`
- `notebooks/Day07_Automation_Concept_Mechanics/Day07_03_Equipment_Selection.{md,ipynb}`
- `notebooks/Day09_Communication_Commissioning/`（6ファイル / six files）
- `day07_09_support/reference_data/diagram_png/day09/D09-12.png`
- `day07_09_support/simulations/fallback/sim_commissioning.png`

### 6.3 主要な更新 / main updates

- 教材原稿 / manuscripts: `Day08_01_Electrical_Fundamentals.md`、`Day08_02_Sensors_and_IO.md`、`Day08_03_Ladder_Sequence.md`
- 基盤 / infrastructure: `lesson_manifest.json`、`curriculum_source_map.csv`、`examples/automation_models.py`、`scripts/{build_day07_09_notebooks,generate_day07_09_diagrams,render_diagrams,export_day07_09_pdf,check_day07_09_pdfs,generate_reference_outputs,run_notebook_cells}.py`
- 図 / figures: `assets/diagrams/day07/*.svg`（14）、`day08/*.svg`（14）、`day09/*.svg`（11）、`reference_data/diagram_png/**`
- 補助教材 / support: ワークシート6点、評価ルーブリック、公式カード3点、用語集2点、講師ガイド3点
- ナビゲーション / navigation: `COURSE_SYLLABUS_DAY07_09.md`、`README.md`、`START_HERE.md`、`day07_09_support/README_ja_en.md`、`SOURCES_AND_LICENSES.md`、`docs/pdf/README.md`
- シミュレータ / simulator: `simulations/sim_plc_sequence.html`、`tests/run_simulation_logic_tests.js`
- テスト / tests: `tests/test_day07_09_course.py`
- 生成物 / generated: `.ipynb` 9点、`reference_outputs.json`、PDF 3点、`docs/pdf/_pages/**`

## 7. 最終PDFのページ数 / final PDF page counts

| PDF | ページ / pages | 画像 / images | 備考 / note |
|---|---:|---:|---|
| `Day07_explanation_ja_en.pdf` | **45** | 16 | 旧58ページ / was 58 |
| `Day08_explanation_ja_en.pdf` | **48** | 14 | 旧60ページ / was 60 |
| `Day09_explanation_ja_en.pdf` | **19** | 11 | 上限19 / limit 19（表紙・目次・付録込み / including cover, contents and appendices） |

第9日の19ページは、余白12 mm、本文8.8 pt、表7.8 pt以上、目次を表紙ページに統合、付録Aを公式カードの前半、付録Bを短縮版用語集とすることで達成しています。図は紙面では小さくなるため、講師は `assets/diagrams/day09/` のSVG/PNGを投影してください。
Day 9 reaches 19 pages with 12 mm margins, an 8.8 pt body and table text of at least 7.8 pt, the contents merged onto the cover page, the first half of the formula card as Appendix A, and the compact glossary. Figures are small on paper; instructors should project the SVG/PNG files.

## 8. 実行したコマンドと結果 / commands executed and results

```powershell
cd AI_Vision_Training
.\.venv\Scripts\python.exe day07_09_support\scripts\generate_day07_09_diagrams.py   # 39 SVG
.\.venv\Scripts\python.exe day07_09_support\scripts\render_diagrams.py              # 39 PNG (Inkscape)
.\.venv\Scripts\python.exe day07_09_support\scripts\build_day07_09_notebooks.py     # 9 notebooks
.\.venv\Scripts\python.exe day07_09_support\scripts\build_day07_09_notebooks.py --check
.\.venv\Scripts\python.exe day07_09_support\scripts\generate_reference_outputs.py
.\.venv\Scripts\python.exe day07_09_support\scripts\run_notebook_cells.py
.\.venv\Scripts\python.exe day07_09_support\scripts\export_day07_09_pdf.py
.\.venv\Scripts\python.exe day07_09_support\scripts\check_day07_09_pdfs.py
.\.venv\Scripts\python.exe -m pytest day07_09_support\tests\test_day07_09_course.py -q
node day07_09_support\tests\run_simulation_logic_tests.js
.\.venv\Scripts\python.exe -m pytest day06_support\tests assets\tests\test_notebooks.py assets\tests\test_schedule.py -q
```

| 実行 / Run | 結果 / Result |
|---|---|
| 図の生成 / diagram generation | 39 SVG written, no clipping assertions tripped |
| PNG描画 / PNG rendering | 39 rendered with Inkscape |
| ノートブック生成 / notebook build | 9 built; `--check` reports "All nine notebooks match their canonical sources" |
| セル実行 / cell execution | 9 notebooks OK (Day 7 = 0 code cells) |
| 参考出力 / reference outputs | 9 lessons captured (Day 7 = 0 cells) |
| PDF生成 / PDF export | Day07 45 pages, Day08 48, Day09 19 (limit 19) |
| PDF点検 / PDF checks | 全ページ描画・構造チェック通過 / all pages rendered; structural checks passed |
| Day 7〜9 テスト / tests | **53 passed** |
| シミュレータ論理テスト / simulator logic | **SIMULATION LOGIC TESTS PASSED (20 checks)** |
| Day 1〜6 回帰 / regression | **110 passed, 2 failed**（下記 §11 / see section 11） |

## 9. 独立レビュー / independent discipline reviews

自動テストが通ることと、内容が正しいことは別です。次の観点で本文・図・数値を読み直し、見つけた問題を修正しました。

Passing tests does not prove correctness. The text, figures and numbers were re-read from each discipline and the findings were fixed.

### A. 機械 / mechanical

- 質量 kg と力 N を全節で区別（D07-13）。 / Mass and force separated everywhere.
- 押し側・引き側の受圧面積と、ロッド径がボア以上になる入力の拒否。 / Effective areas on both sides; a rod diameter not smaller than the bore is rejected.
- 摩擦・余裕係数・静摩擦の扱いを「仮定」と明示。 / Friction, margin factor and static friction labelled as assumptions.
- 減速機効率とモーター効率を分離。 / Reducer efficiency separated from motor efficiency.
- 修正：07-01 で「効果金額」の説明に稼働率が混ざっていた箇所を削除。 / Fixed: the availability factor leaking into the Day 7 effect explanation was removed.

### B. 電気 / electrical

- AC/DC、電圧の使い分け、保護機器の範囲、W/VA、突入電流を確認。 / AC/DC, voltage use, protective coverage, W/VA and inrush checked.
- 修正：0.80 A / 19.2 W / 1.00 A の電源計算を、旧 0.73 A の例から置き換え。 / Fixed: the power budget was replaced with 0.80 A / 19.2 W / 1.00 A.
- 修正：`Y0` を電磁弁に使う誤りを検出するよう `validate_io` の対象を修正（テスト側の誤りも修正）。 / Fixed: `validate_io` now flags a solenoid on `Y0`; the test that used the wrong address was corrected.

### C. PLC制御 / PLC control

- スキャン順依存、STOP優先、リセットと起動の分離、位置確認を確認。 / Scan order, STOP precedence, reset versus start, position confirmation checked.
- 修正：基本回路の「STOP許可が戻るとRUNが戻る」挙動を、図・本文・テストの3か所で一致させた。 / Fixed: the basic-circuit restart behaviour is consistent in figure, text and test.
- 修正：`PusherSequence` のFAULT復帰はSTART非保持とリセット立ち上がりを要求することを、本文のネットワークと一致させた。 / Fixed: fault recovery requires START released and a reset edge, matching the ladder description.

### D. マシンビジョン / machine vision

- 0.125 mm/px、4 px、1 mm、8 px、0.125 ms、8,000 line/s、33.33 mm を再計算。 / Recomputed.
- 「ピクセル数＝検出保証」を否定し、検証データと撮像条件を要求。 / Pixel count is not a detection guarantee; validation data and imaging conditions are required.
- 修正：09-01 から「サブネット計算など」の記述を削除（廃止した単元の用語がPDFに残らないように）。 / Fixed: removed a leftover subnet reference from 09-01 so obsolete terminology does not appear in the PDF.

### E. 教育・可読性 / education and readability

- 第7日は計算を紙と電卓で行い、実行セルを持たない。 / Day 7 is paper and calculator work with no executable cells.
- 演習は各ノートブック1〜2問、直後に解答。 / One or two exercises per notebook, with answers immediately after.
- 第9日のPDFは紙面が小さいため、講師投影用のSVG/PNGを明記。 / Because the Day 9 PDF is compact, the report and the PDF README point instructors to the SVG/PNG for projection.

### F. リポジトリ整合 / repository integrity

- 生成物はすべて原稿から再生成。`.ipynb` と PDF を直接編集していない。 / All artefacts regenerated from the sources; no `.ipynb` or PDF was hand-edited.
- 旧 Day 9 教材と旧 Day 7 原稿は削除し、ナビゲーションからも排除。 / The old Day 9 course and old Day 7 manuscripts are removed and no longer referenced.
- 元PDFは不変（ハッシュと51ページを確認）。 / The source PDF is unchanged (hash and 51 pages verified).

## 10. 検証中に発見して修正した問題 / issues found and corrected during verification

| 問題 / Issue | 対応 / Action |
|---|---|
| Day 9 PDFが29→20→19ページと上限を超えた / Day 9 exceeded the limit | 本文の圧縮、演習の統合、付録の統合、目次の表紙統合、余白と文字サイズの調整で19ページに。 / Content compaction, merged exercises, merged appendices, contents on the cover, adjusted margins and type sizes. |
| 図の生成スクリプトで `svg.text` の引数誤りと幅超過 / generator argument and width errors | 修正し、全39図がクリッピング検査を通ることを確認。 / Fixed; all 39 figures pass the clipping assertions. |
| ラダーのコイル記号が「(( ))」に見えた / coil symbol looked like two parentheses | 角丸のコイル形状に変更。 / Redrawn as a rounded coil symbol. |
| D08-12 のネットワーク説明が接点ラベルと重なった / overlapping labels | 行間と説明位置を調整。 / Row spacing and label positions adjusted. |
| `validate_io` のテストが誤ったアドレスを検査 / the I/O test checked the wrong address | テストを修正（Y0に電磁弁を割り当てた場合を検査）。 / Test corrected. |
| ソースマップの1行が新しい分類と矛盾 / one source-map row contradicted its disposition | 分類を `REPLACED_WITH_CORRECTED_CONTENT` に修正。 / Disposition corrected. |
| 保護ベースラインの失敗 / protected-baseline failure | 外部変更をHEADへ復元（上記 §1）。 / External change restored to HEAD (section 1). |

## 11. 残存する制約と未検証事項 / remaining limitations and unverified items

1. **Day 1〜6 の2件のテスト失敗（本作業と無関係）**：`assets/tests/test_notebooks.py` の2件が失敗します。原因は `notebooks/Day02_Python_OpenCV/Day02_03_OpenCV_Image_Processing.ipynb` が参照する `assets/diagrams/calibrated_defects.png` と `calibrated_defects_ground_truth.json` が存在しないことです。両ファイルは Git 管理下になく、開始コミット時点でも存在しませんでした。Day 1〜6 の内容を変更して回避することは避け、**未修正のまま報告**します。 / Two pre-existing failures remain in the Day 2 notebook asset check: two referenced Day 2 assets are not tracked and were absent at the starting commit. They were not worked around by editing Day 1–6 content.
2. **メーカー固有の値は未検証**：三菱・オムロン等の端子番号、機種互換、カメラ・レンズ・照明のカタログ値は引用していません。汎用の概念例のみです。実機では公式マニュアルで確認してください。 / No manufacturer terminal numbers, model compatibility or catalogue values are asserted; only generic conceptual examples are used.
3. **実機検証は未実施**：本教材のコードは実機のPLC出力・モーター・電磁弁・カメラ・設備を動かしません。シミュレーション結果は実機の測定値ではありません。 / No hardware validation was performed; simulation output is not a measurement.
4. **初心者パイロットは未実施**：時間配分（80/85/135分）は計画値であり、実測ではありません。 / The durations are planned, not measured in a beginner pilot.
5. **PDFの目視点検は代表ページ**：全ページを画像化し、空白・構造・文字化け・リンク・HTML混入を自動確認しました。目視では Day 7（p.8）、Day 8（p.12）、Day 9（p.1–4, 14, 19）を確認しています。全ページの目視確認は未完です。 / Every page was rendered and checked automatically; visual inspection covered representative pages (listed). Full page-by-page visual inspection is not complete.
6. **第9日PDFの図は小さい**：19ページ上限のため図は66 mm高に制限しています。投影用のSVG/PNGを使用してください。 / Day 9 figures are capped at 66 mm high because of the 19-page limit; use the SVG/PNG for projection.
7. **共有環境**: 作業中に別プロセスの書き換えが観測されました。今後も同じ環境で作業する場合は、コミット前に `git status` を再確認してください。 / Concurrent external modification was observed; re-check `git status` before committing.

## 12. 受け入れマトリクス / acceptance matrix

| ID | 要求 / Requirement | 状態 / Status | 根拠 / Evidence |
|---|---|---|---|
| D7-01 | 稼働率の削除 / availability removed | **PASS** | Day 7 原稿に稼働率の計算式なし。`test_no_availability_or_oee_model_remains`。 / No availability formula; test passes. |
| D7-02 | 実行セルなし / no executable cells | **PASS** | `test_notebook_structure_and_bilingual_content`（Day 7 = 0 code cells）。 |
| D7-03 | 能力の説明 / capacity | **PASS** | 42秒/個、85.71個/時、240個/時、480個/時をテスト。 / Tested. |
| D7-04 | 効果金額 / economic effect | **PASS** | 316,800円、266,800円、1.42年、1.69年をテスト。 / Tested. |
| D7-05 | 動力 / power sources | **PASS** | 07-02 §5–§7（空圧・油圧・電気）。 / Sections present. |
| D7-06 | アクチュエータ / actuators | **PASS** | 07-02 §4・§8（直線・回転・把持・クランプ・昇降・押出し・位置決め・搬送、グリッパ、真空）。 |
| D7-07 | 選定仕様 / selection specifications | **PASS** | 07-03 §4（16項目、単位付き）。 / Sixteen specifications with units. |
| D7-08 | 計算の検証 / calculations | **PASS** | 157.08 N、131.95 N、19.62 N、39.24 N、11.18 mm、0.477/9.55/8.59 N·m をテスト。 |
| D8-01 | 電圧 / voltages | **PASS** | 08-01 §5。 / Section present. |
| D8-02 | 盤の機器 / components | **PASS** | 08-01 §6（18機器、D08-03〜05）。 / Eighteen devices with figures. |
| D8-03 | I/O | **PASS** | 08-02 §4、D08-06。 / Section and figure. |
| D8-04 | センサー / sensors | **PASS** | 08-02 §5–§6、D08-07・D08-08。 |
| D8-05 | NPN/PNP | **PASS** | 08-02 §7–§9、D08-09、`test_npn_pnp_compatibility`。 |
| D8-06 | ラダー / ladder | **PASS** | 08-03 §5–§6、D08-10。 |
| D8-07 | 自己保持 / self-holding | **PASS** | 08-03 §7、D08-11、`test_basic_seal_in_and_extended_gate`。 |
| D8-08 | 再起動防止 / restart prevention | **PASS** | 08-03 §8、D08-12、`test_start_gate_*`、`test_pusher_sequence_*`、シミュレータ20チェック。 |
| D8-09 | インターロック / interlocks | **PASS** | 08-03 §9、D08-13、`test_interlocks`。 |
| D8-10 | 電力計算 / power | **PASS** | 0.80 A、19.2 W、1.00 A、3.6 W、0.8 kWh、24円をテスト。 |
| D9-01 | 範囲の置換 / scope replaced | **PASS** | `Day09_Communication_Commissioning` 削除、ナビゲーションから排除、Day 9 PDFにネットワーク用語なし。 / Folder removed, navigation clean, no networking terms in the PDF. |
| D9-02 | カメラ / cameras | **PASS** | 09-01 §4–§10。 / Sections present. |
| D9-03 | 光学 / optics | **PASS** | 0.125 mm/px、4 px、レンズ選定要素をテスト。 |
| D9-04 | 露光とぶれ / exposure and blur | **PASS** | 1 mm、8 px、0.125 ms、シャッター比較をテスト。 |
| D9-05 | エリア/ライン / area vs line | **PASS** | 8,000 line/s、エンコーダ同期、D09-10。 |
| D9-06 | 照明 / lighting | **PASS** | 09-02 §5、D09-06、6種類の表。 |
| D9-07 | 環境 / environment | **PASS** | 09-02 §7–§9、D09-07。 |
| D9-08 | AIカメラ構成 / architecture | **PASS** | 09-03 §4–§7、D09-09・D09-11。 |
| D9-09 | 19ページ以内 / page limit | **PASS** | 19ページ、テストとエクスポータの両方で上限を検査。 |
| QA-01 | 日本語 / Japanese | **PASS（範囲限定 / scoped）** | 全原稿を読み直し、単位・用語・文体を統一。ネイティブ校正は未実施。 / Re-read and unified; no native-speaker proofread. |
| QA-02 | 英語 / English | **PASS（範囲限定 / scoped）** | 日本語と同内容の英語を併記。専門家校正は未実施。 / Equivalent English in every unit; no professional proofread. |
| QA-03 | 図 / diagrams | **PASS** | 39図、日英ラベル、`title`/`desc`、クリッピング検査、PNG 20 KB以上。 |
| QA-04 | 演習の削減 / exercises | **PASS** | 各ノートブック1〜2問、ワークシートは最大3問。 / One or two per notebook, at most three per worksheet. |
| QA-05 | ノートブック生成 / notebooks | **PASS** | 9点生成、`--check`一致。 |
| QA-06 | PDF生成 / PDFs | **PASS（目視は代表ページ / visual inspection of representative pages）** | 3点生成、全ページ自動点検、代表ページを目視。 / All three exported, all pages checked automatically, representative pages inspected visually. |
| QA-07 | テスト / tests | **PASS** | 53 passed（Day 7〜9）。 / 53 passed for Days 7-9. |
| QA-08 | 参照 / references | **PASS（現行資料のみ / current material only）** | 現行教材の画像リンク・図参照・ナビゲーションをテスト。 / Links and references in the current material are tested. |
| QA-09 | Day 1〜6 保護 / protected content | **PASS（Day 7〜9 テスト内 / within the Day 7-9 suite）** | 保護ハッシュ320件以上が一致。Day 1〜6 の別スイートに既存の2件失敗あり（§11）。 / All protected hashes match; two unrelated failures remain in another suite. |
| QA-10 | 元PDF / source PDF | **PASS** | SHA-256 `3380c2b6…3707ae`、51ページ。 |
| QA-11 | 安全 / safety | **PASS** | 実機検証の主張なし。全教材に安全境界を明記。 / No claim of real-machine validation; safety boundaries stated throughout. |

**未実施（NOT VERIFIED）：** 実機でのPLC・カメラ・照明の動作確認、初心者パイロット、メーカー資料との突合、全PDFページの目視。
**NOT VERIFIED:** real-machine PLC, camera and lighting behaviour, a beginner pilot, cross-checks against manufacturer documents, and page-by-page visual inspection of every PDF page.

## 13. 次の推奨作業 / recommended next steps

1. 実機を使わない範囲で、初心者3〜5名のパイロットを実施し、時間配分と演習量を測る。 / Run a 3–5 person beginner pilot without hardware to measure durations and exercise load.
2. 第9日PDFの図を投影で確認し、必要なら図を2点に統合して紙面を広げる。 / Review the Day 9 figures under projection and merge figures if more paper space is needed.
3. Day 2 の未追跡アセット（`calibrated_defects.png` と ground truth）の扱いを、Day 1〜6 の担当者と決める。 / Decide the Day 2 missing-asset issue with the Day 1–6 owner.
4. 実機演示を行う場合は、リスクアセスメントと承認のうえで、別途実施する。 / Any real demonstration must be separately approved and risk-assessed.
