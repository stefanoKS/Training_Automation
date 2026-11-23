# Day 7–9 リリースレビュー / Day 7–9 release review

**日付 / Date:** 2026-11-23
**リポジトリ / Repository:** `https://github.com/stefanoKS/Training_Automation`
**対象 / Scope:** `AI_Vision_Training/` の Day 7–9 を、元PDF由来の3日間コースへ完全置換 / full replacement of Days 7–9 with a three-day course derived from the source PDF
**レビュー種別 / Review type:** 実装・検証・引継ぎ / implementation, verification and handover

> このレビューは、実装者が自分の成果を自己評価したものです。独立した第三者レビューや、実機・安全・初学者パイロットの検証を置き換えるものではありません。
> This is the implementer's self-assessment. It does not replace an independent review, real-machine validation, safety validation or a beginner pilot.

---

## 1. リポジトリの状態 / Repository state

| 項目 / Item | 値 / Value |
|---|---|
| 開始コミット / starting commit | `879824c802c3a35a45074ce4017c296e58332630` |
| ブランチ / branch | `main` |
| 終了状態 / ending state | 作業ツリーに変更あり。**コミット・プッシュなし** / working-tree changes, **no commit or push** |
| `origin/main` | 開始時と同じSHA / same SHA as the start |
| 変更数 / changed paths | 232（modified 59、deleted 46、untracked 127） / 232 changed (59 modified, 46 deleted, 127 untracked) |
| 完全な一覧 / complete inventory | [`Day07_09_Change_Inventory.txt`](Day07_09_Change_Inventory.txt)（232行 / 232 lines） |
| 破壊的Git操作 / destructive git operations | なし（force-push、履歴書換え、resetなし） / none |

作業ツリーは意図的に未コミットです。コミットは別途の承認が必要です。 / The tree is intentionally uncommitted; a commit requires separate authorisation.

---

## 2. 元PDFの検証 / Source verification

| 項目 / Item | 結果 / Result |
|---|---|
| パス / path | `docs/reference/自動化設備製作研修_5日間_詳細版_受講者用.pdf` |
| SHA-256 | `3380c2b67e148cd9a71b0f9071963744f3b0acba7491b309708b0f31183707ae` |
| 期待値との一致 / expected match | **一致 / matches** |
| ページ数 / pages | **51** |
| 変更 / modification | **なし / none**（テストでハッシュを検証 / hash tested） |
| テキスト抽出 / text extraction | 全51ページ / all 51 pages → `reference_data/pdf_extract/source_text.txt` |
| 画像描画 / page rendering | 全51ページ / all 51 pages → `reference_data/pdf_extract/pages/` |
| トレーサビリティ / traceability | `curriculum_source_map.csv` 51行 / 51 rows |

**カバレッジ結果 / coverage result:** 51/51ページに明示的な処分。REQUIRED 37、REPLACED_WITH_CORRECTED_CONTENT 7、INCORPORATED_ELSEWHERE 4、SUPPLEMENTARY 3、REFERENCE_ONLY 0。必須50、任意1。
Every page has a disposition: 37 REQUIRED, 7 REPLACED_WITH_CORRECTED_CONTENT, 4 INCORPORATED_ELSEWHERE, 3 SUPPLEMENTARY, 0 REFERENCE_ONLY; 50 required, 1 optional.

---

## 3. カリキュラム実装 / Curriculum implementation

9つのノートブックは、`lesson_manifest.json` の順序・時間・図・PDFページに従います。`.md` が正本、`.ipynb` は生成物です。

The nine notebooks follow the manifest's order, time, figures and PDF pages. `.md` is canonical; `.ipynb` is generated.

### Day 7

| ノート / Notebook | 元PDF / pages | 主な学習目標 / objectives | 実行セル / executable exercises | 図 / diagrams | 提出物 / deliverables | PDF章 / PDF section |
|---|---|---|---|---|---|---|
| Day07_01_Requirements | 4–11 | 自動化と機械化、8段階、ECRS、観測、タクト/サイクル/実力能力、3案比較、要求仕様、受入基準、構想安全 | `capacity`, `capacity-sweep`, `option-score`（3） | D07-01〜05 | 課題文、能力計算、3案比較、初期リスク、要求仕様 | 第7日 01 |
| Day07_02_Mechanical_Architecture | 12–14, 16 | 5機能、空圧/電動、空圧回路、推力、速度制御、位置検出、ガイド、側荷重、残留エネルギー | `setup`, `pneumatic-force`, `air-use`, `side-load-moment`（4） | D07-06〜08 | 機械構成図、空圧BOM、推力計算、エネルギー表 | 第7日 02 |
| Day07_03_Equipment_Selection | 15, 17–20, 47 | 力/摩擦、理論内径、ロッド側、カタログ、モーター/減速機、効率、BOM、版管理、メーカー資料 | `setup`, `cylinder-calculator`, `cylinder-validation`, `bore-curve`, `motor-calculator`, `motor-curve`, `bom-hash`（7） | D07-09 | シリンダ計算書、モーター計算書、BOM、候補比較 | 第7日 03 |

### Day 8

| ノート / Notebook | 元PDF / pages | 主な学習目標 / objectives | 実行セル / executable exercises | 図 / diagrams | 提出物 / deliverables | PDF章 / PDF section |
|---|---|---|---|---|---|---|
| Day08_01_Electrical_Fundamentals | 21–23 | V/I/R/P、オームの法則、DC/AC、DC24V、電源、突入/定格低下、スイッチ/リレー、PLC出力、保護、接地、絶縁、信号と電力 | `setup`, `supply-margin`, `load-budget`, `ohms-law`（4） | D08-01〜04 | 負荷計算、電源確認項目、電圧降下、信号/電力経路 | 第8日 01 |
| Day08_02_Sensors_and_IO | 24–29, 48 | センサー方式、アナログ/デジタル、NPN/PNPと入力共通、PLC入力/出力、電磁弁、サージ、統一I/O、配線、通電前確認 | `setup`, `sensor-compatibility`, `io-table`, `io-validation`（4） | D08-05〜07 | 電気機器表、センサー表、I/O表、互換性、配線図 | 第8日 02 |
| Day08_03_Ladder_Sequence | 30–33 | PLCスキャン、接点、物理/論理、自己保持、タイマー、状態、位置確認、タイムアウト、異常、リセット、復電 | `setup`, `sim-selfhold`, `sim-timer`, `sim-sequence`, `sim-faults`, `sim-reset`, `sim-invalid`（7） | D08-08〜11 | 自己保持説明、状態表、I/Oトレース、異常マトリクス、試験証跡 | 第8日 03 |

### Day 9

| ノート / Notebook | 元PDF / pages | 主な学習目標 / objectives | 実行セル / executable exercises | 図 / diagrams | 提出物 / deliverables | PDF章 / PDF section |
|---|---|---|---|---|---|---|
| Day09_01_Industrial_Networking | 34–38, 49 | LAN、IP、/24・/25、ネットワーク/ブロードキャスト、GW、TCP/UDP、ポート、産業用Ethernet、Modbus TCP、記録、切り分け | `setup`, `subnet-basic`, `subnet-pairs`, `ip-allocation`（4） | D09-01〜05 | IP割当、構成図、通信仕様、切り分け | 第9日 01 |
| Day09_02_Commissioning | 39–43, 50 | 組立/検査、隔離、オフライン、段階ゲート、正常/異常試験、故障履歴、復旧、保全、引継ぎ、変更管理 | `setup`, `commissioning-matrix`, `fault-trace`, `test-record`, `change-history`（5） | D09-06〜07 | ゲート表、試験マトリクス、不具合、変更履歴、引継ぎ | 第9日 02 |
| Day09_03_Automation_Proposal | 9, 44–46, 51 | 24項目の提案、能力/機械/電気/PLC/通信/試験/リスク/費用、10分発表、次のステップ | `setup`, `payback-calculator`, `payback-sensitivity`, `proposal-check`（4） | D09-08〜09 | 最終提案、コスト要約、発表 | 第9日 03 |

**生成と検証 / generation and verification:** 結合フィンガープリント（マニフェスト、原稿、`automation_models.py`、参照SVG、生成スクリプト）を各ノートブックに保存。`--check` で古いノートブックを検出。9/9がオフラインで実行。 / Combined fingerprint stored in each notebook; `--check` detects stale files; 9/9 execute offline.

---

## 4. 技術的修正 / Technical corrections

詳細は [`../reference/Automation_Equipment_PDF_Errata_ja_en.md`](../reference/Automation_Equipment_PDF_Errata_ja_en.md)。

### 4.1 p.31 自己保持 / self-holding

元PDFの図には**並列保持接点がない**。STARTを離すとRUNが消える。新教材は `(X0 AND X2) OR M0`、直列X1の正しいラングを示す。X2は開始時だけ必要で、保持枝には入れない。シミュレーションでSTART解放後もRUNが続くことを確認。

The source lacks the **parallel holding contact**, so RUN drops when START is released. The replacement shows `(X0 AND X2) OR M0` with X1 in series. X2 is needed only at start and is not in the hold branch. Simulation confirms RUN survives START release.

**Evidence:** D08-08, `sim-selfhold`, `test_start_release_self_holding_and_stop`, `test_notebook_structure...`.

### 4.2 p.32 順序確認 / sequence confirmation

元PDFは指令と位置確認が明確に分かれていない。新教材は IDLE、READY、EXTEND、WAIT_EXTENDED、RETRACT、WAIT_RETRACTED、COMPLETE、FAULT の8状態。F001（前進端未確認）、F003（後退端未確認）、F002（前後端同時ON）。3秒は訓練用の仮値。

The source does not clearly separate commands from position confirmation. The replacement uses eight states and F001/F003/F002. The 3 s value is a training assumption.

**Evidence:** D08-09, D08-11, `normal_cycle`, `sensor_stuck_off`, `motion_slow`, `sensor_conflict`.

### 4.3 Y1の重複 / Y1 inconsistency

Y1を遅延ランプ専用、Y2を前進電磁弁に固定。`validate_io()` がY1の電磁弁流用とX1の正常状態の誤りを検出。 / Y1 is the delayed lamp only; Y2 is the solenoid. `validate_io()` detects misuse.

**Evidence:** canonical I/O, `io-table`, `io-validation`, `test_canonical_io_is_unambiguous`.

### 4.4 シリンダ / cylinder

8 kg、μ=0.25、factor 2、0.4 MPa → 19.62 N、39.24 N、**11.18 mm**。11.18 mmは理論下限であり、カタログ選定ではない。実型式は割り当てず、16 mmは比較用の仮候補。ロッド側の有効面積を明示。

8 kg, μ=0.25, factor 2, 0.4 MPa → 19.62 N, 39.24 N, **11.18 mm**. The bore is a theoretical lower bound, not a catalogue selection. No real part number is assigned; 16 mm is a comparison candidate. Rod-side area is explicit.

**Evidence:** D07-09, `cylinder-calculator`, `test_mechanical_numbers`.

### 4.5 モーター / motor

60 W、1200 rpm → **0.477 N·m**。20:1 → **60 rpm**、理想 **9.55 N·m**。η=0.90（追加仮定）→ **8.59 N·m**。0.90は実機の効率ではないと明記。

60 W at 1200 rpm → **0.477 N·m**; 20:1 → **60 rpm**, ideal **9.55 N·m**; η=0.90 (added assumption) → **8.59 N·m**. The efficiency is explicitly a teaching value.

**Evidence:** `motor-calculator`, `motor-curve`, `test_motor_numbers`.

### 4.6 電気インターフェース / electrical interfaces

0.73 Aは定常合計であり、電源選定の承認ではない。突入、定格低下、電線、端子、保護を別に確認。NPN/PNPは入力共通端子を含む閉回路で説明。2線式の漏れ電流も扱う。

0.73 A is a steady-state sum, not approval of a supply. Inrush, derating, wiring, terminals and protection are separate. NPN/PNP is explained as a closed circuit including the input common; two-wire leakage is included.

**Evidence:** D08-06, `load-budget`, `sensor-compatibility`, `test_electrical_load_numbers`.

### 4.7 安全・試運転 / safety and commissioning

G5（通電試験）は課程の必須ではない。未実施は **BLOCKED** または **NOT TESTED**。リセットは動作開始ではない。復電時に保持ビットや押しっぱなしのSTARTで自動再起動しない。通常PLCは安全機能ではない。

G5 (energised testing) is not required. Unperformed tests are **BLOCKED** or **NOT TESTED**. Reset is not a start. Power restoration does not restart from a retained bit or held START. Ordinary PLC is not a safety function.

**Evidence:** D08-11, D09-06, D09-07, `test_fault_reset_never_starts_motion`, `test_power_restore_with_held_start_and_new_start`, commissioning matrix T11/T12 BLOCKED.

### 4.8 PDFレイアウト / PDF layout

- IPv4を`<nobr>`で保護し、抽出テストで分割を検出。 / IPv4 protected with `<nobr>` and extraction test.
- 表の列幅を文字幅から計算。 / table widths computed from text width.
- 生HTMLを除去。 / raw HTML stripped.
- D07-06、D07-07、D08-06、D08-08、D08-09のラベル重なりを修正。 / fixed overlapping labels.

**Evidence:** `check_day07_09_pdfs.py`、`no_broken_ip`、`no_html_tag`、図の再描画。

---

## 5. 作成・変更・削除したファイル / Files created, modified and deleted

完全な一覧は [`Day07_09_Change_Inventory.txt`](Day07_09_Change_Inventory.txt)（232行）。

Complete inventory: `Day07_09_Change_Inventory.txt` (232 entries).

### 作成 / created

- 9ノートブックの正本 `.md` と生成 `.ipynb`（`notebooks/Day07_Automation_Concept_Mechanics/`, `Day08_Electrical_PLC/`, `Day09_Communication_Commissioning/`）。
- 29個のSVG（`assets/diagrams/day07/` 9、`day08/` 11、`day09/` 9）。
- `day07_09_support/` の `lesson_manifest.json`、`curriculum_source_map.csv`、`examples/automation_models.py`、新しい図・ノートブック・PDF・参照出力・ベースライン生成スクリプト、PDF検査、保護ベースライン生成。
- `simulations/sim_plc_sequence.html` とフォールバックPNG 2個。
- ワークシート3、解答キー3、評価ルーブリック、用語集（再生成）。
- 講師ガイド3（再生成）。
- 正誤表、移行監査、本レビュー、変更一覧。

- Nine canonical `.md` and generated `.ipynb` files.
- 29 SVGs.
- Manifest, source map, `automation_models.py`, new generation/validation scripts, reference outputs and baseline builder.
- Offline simulator and two fallback images.
- Three worksheets, three answer keys, rubric and glossary (regenerated).
- Three instructor guides (regenerated).
- Errata, audit, this review and the inventory.

### 変更 / modified

- `COURSE_SYLLABUS_DAY07_09.md`（3日間の公式時間割 / official three-day timetable）
- `README.md`、`START_HERE.md`、`docs/reference_materials.md`、`docs/pdf/README.md`（狭いナビゲーション更新 / narrow navigation updates）
- `docs/pdf/Day07/08/09_explanation_ja_en.pdf`（再生成 / regenerated）
- `day06_support/tests/test_day06_contracts.py`（Day 6保護テストを、Day 7–9の正規移行を妨げない形に限定 / narrowed so the authorised Day 7–9 migration does not fail it, while still checking all Day 6 changes)

### 削除 / deleted

- 旧 `notebooks/Day07_Machine_Fundamentals/`、`Day08_PLC_Control/`、`Day09_System_Integration/`（18ファイル / 18 files）。
- 旧シミュレーション6 + フォールバック6。
- 旧テスト `test_day07_09_contracts.py`。
- 旧スクリプト `engineering_examples.py`、`inspect_day07_09_pdf.py`、`render_simulation_fallbacks.py`。
- 旧サンプル3。
- 旧レビュー2。
- 旧SVG 7（D07-10〜12、D08-12、D09-10〜12）。

**削除理由 / why removed:** 旧教材はカメラ・AI・画像処理中心で、元PDFの機械・電気・PLC・通信・試運転の学習目標と一致しない。重複する有効コースを残さないため。Git履歴には残る。
The old course centred on cameras, AI and image processing and did not match the source PDF's mechanical, electrical, PLC, network and commissioning objectives. Removing it prevents two active Day 7–9 courses. Git history preserves it.

---

## 6. テスト証跡 / Testing evidence

実行環境 / environment: Windows, repository virtual environment (Python 3.11), Inkscape for SVG rasterisation, Node.js for the HTML logic tests.

### 6.1 Day 7–9 suite

```text
python -m pytest day07_09_support/tests/test_day07_09_course.py -q
```

**結果 / result:** `40 passed`（本レビュー作成後に再実行 / rerun after this file exists）。内訳: 元PDF、9ノートブックの構造と実行、独立計算、PLC、通信、図、HTML、PDF、時間割、保護ベースライン。

`40 passed`. Covers the source PDF, nine notebook structures and executions, independent calculations, PLC, networking, diagrams, HTML, PDFs, timetable and protected baseline.

### 6.2 ノートブック実行 / notebook execution

```text
python day07_09_support/scripts/run_notebook_cells.py
```

**結果 / result:** 9/9 `OK`、終了コード0。各ノートブック3–7個のコードセル（合計42セル）。オフライン、実機なし。

9/9 OK, exit code 0. Three to seven code cells per notebook (42 total). Offline, no hardware.

### 6.3 HTMLシミュレータ / HTML simulator

```text
node day07_09_support/tests/run_simulation_logic_tests.js
```

**結果 / result:** `SIMULATION LOGIC TESTS PASSED (14 checks)`。START、解放、STOP、2999/3000、タイムアウト、矛盾、リセット、復電、繰返し、不正遷移。

14 checks covering START, release, STOP, 2999/3000, timeout, conflict, reset, power restore, repeat and invalid transitions.

### 6.4 PDF / PDFs

```text
python day07_09_support/scripts/check_day07_09_pdfs.py
```

**結果 / result:** 構造チェック合格。

```text
Day07: 58 pages, 10 images, 2,804,758 bytes, render OK
Day08: 60 pages, 12 images, 2,845,013 bytes, render OK
Day09: 57 pages, 9 images, 2,352,920 bytes, render OK
PDF structural checks passed
```

目次、日英、用語集、参考文献、生HTMLなし、壊れたIPv4なし、全ページ非空白、画像数を確認。 / TOC, both languages, glossary, references, no raw HTML, no broken IPv4, no blank pages, image counts.

**SHA-256**

- Day07: `6FC8A3807D1FEC01C4028EEBD3C4F470F13DE7B5D35AC9D70C04DEB71BA3591A`
- Day08: `92DEF75B0CCF15E0F0A76FD17BE1E6AD723138AD364303CDE71021C72EC83094`
- Day09: `0FA6B4B46A1B773807B9134A180A956A5DE340146F269C9C00470DB512FE2801`

### 6.5 図 / diagrams

29/29 SVGがXMLとして有効、`<title>`/`<desc>`あり、日英ラベルあり、ノートブックから参照、PNGが20 KB超、旧図が残っていないことをテスト。 / 29 SVGs valid, titled, described, bilingual, referenced, rasterised and no obsolete figures.

### 6.6 リポジトリ回帰 / repository regression

**Day 6:**

```text
python -m pytest day06_support/tests -q
11 passed in 4.61s
```

**Day 1–6 サブセット / subset:**

```text
python -m pytest assets/tests/test_notebooks.py assets/tests/test_pdf_exports.py \
  assets/tests/test_schedule.py assets/tests/test_assets.py \
  assets/tests/test_visual_assets.py assets/tests/test_day04_day05_contracts.py -q
256 passed, 3 failed
```

**3件の失敗 / three failures:**

1. `test_notebooks.py::test_no_notebook_references_missing_assets` — Day02_03が `calibrated_defects.png` と `calibrated_defects_ground_truth.json` を参照するが、両ファイルはコミット `879824c` にも存在しない。 / Day02_03 references two files that do not exist in `879824c` either.
2. `test_notebooks.py::test_structural_checks_pass` — 同じ欠落資産が原因。 / same missing assets.
3. `test_day04_day05_contracts.py::test_the_repository_holds_no_generated_comparison_artifacts` — `submissions/comparison_test_results.json` が作業ツリーに存在するが、このファイルは `879824c` に存在せず、Day 7–9の変更でもない。 / the file is not in `879824c` and is not a Day 7–9 change.

これらは**変更前から存在する、Day 7–9と無関係な失敗**です。Day 1–6の教材・データ・モデル・PDFを変更して回避していません。 / These are **pre-existing failures unrelated to Day 7–9**. They were not hidden by modifying protected Day 1–6 content.

### 6.7 保護ベースライン / protected baseline

```text
python day07_09_support/scripts/build_protected_baseline.py
Wrote 310 protected entries
```

`test_protected_days_1_to_6_baseline` は `git hash-object` で310ファイルを比較し、合格。元PDF、Day 1–6のノートブック、Day 6サポート、データ・モデル、図、PDF、講師ガイドを含む。作業ツリーの汚れを要求しない。

The test compares 310 files with `git hash-object` and passes. It covers the source PDF, Day 1–6 notebooks, Day 6 support, data/models, diagrams, PDFs and instructor guides. It does not require a dirty tree.

### 6.8 未実施の試験 / tests not performed

- 実機の通電・空圧・動作・安全機能の試験。 / real energisation, pneumatic, motion and safety tests.
- メーカーの選定プログラムや実カタログとの照合。 / manufacturer selection tools and real catalogues.
- 実ネットワークでの通信試験。 / real-network communication tests.
- 初学者1名でのパイロット。 / beginner pilot.
- 独立した第三者レビュー。 / independent third-party review.

---

## 7. 目視検査 / Visual inspection

- **PDF:** 全ページをPNGに描画（`docs/pdf/_pages/Day07`, `Day08`, `Day09`）。表紙・目次・各ノートブック冒頭・図ページ・表ページ・コード/出力ページ・用語集・参考文献を、コンタクトシートと原寸で確認。
- **図:** 29個すべてをInkscapeで1.6倍に描画し、ラベルの欠落・重なり・クリップ・日本語文字化け・矢印方向を確認。D07-06、D07-07、D08-06、D08-08、D08-09は修正後に再確認。
- **確認した問題 / problems found:** 表の列幅が狭く語が不自然に折れる、IPv4が表で分割される、D07-06の部品重なり、D07-07のラベル重複、D08-06のパネル副題と+24Vの重なり、D08-08の保持枝の線切れ、D08-09の状態ボックスとタイムアウト線の交差。
- **修正 / fixed:** 列幅を文字幅から計算、`<nobr>`、図の座標・ラベル・線の再設計。
- **残る制約 / remaining limitation:** 全テキストページを100%倍で1ページずつ読む作業は完了していない。全ページの描画・非空白・抽出・図ページの目視は完了しているが、長い本文ページの微細な組版（孤行・句読点の位置など）は抜き取り確認にとどまる。 / A 100% page-by-page reading of every text page was not completed. Rendering, non-blank checks, extraction and figure-page review are complete; fine typography on long text pages was sampled, not exhaustively read.

**判定 / assessment:** 既知のレイアウト破綻は残っていない。図表ページは実用上読める。本文ページの完全な目視校正は未完了であり、独立校正を推奨する。 / No known layout breakage remains and figure/table pages are usable. Full visual proofreading of text pages is incomplete; independent proofreading is recommended.

---

## 8. 既知の制約 / Known limitations

| 分類 / Category | 状態 / Status |
|---|---|
| 数値計算 / numerical behaviour | 42 s、199.92、19.62 N、39.24 N、11.18 mm、0.477 N·m、60 rpm、9.55 N·m、8.59 N·m、0.73 A、316,800円、1.42年、/24・/25を独立計算とテストで確認。**検証済み / verified** |
| シミュレーション / simulation | PLC状態、タイマー境界、タイムアウト、矛盾、リセット、復電、繰返しを決定論的に確認。**検証済み（モデル内） / verified in the model** |
| メーカー依存 / manufacturer-dependent | 実シリンダ圧力、負荷率、許容モーメント、実効率、弁の無通電位置、圧力損失、センサー応答。**未検証 / not verified** |
| 実機 / real hardware | 通電、空圧、動作、異常、安全機能。**未実施 / not performed** |
| 安全認証 / safety certification | リスクアセスメント、PL/SIL、規格適合、保護方策の妥当性。**未実施 / not performed** |
| 実ネットワーク / real network | IP、VLAN、ルーティング、FW、ポート。**未変更・未検証 / unchanged, not verified** |
| 初学者パイロット / beginner pilot | 80/85/135分の実測、理解度、つまずき。**未実施 / not performed** |
| 独立レビュー / independent review | 第三者による技術・安全・教育レビュー。**未実施 / not performed** |
| PDF本文の完全校正 / full PDF proofreading | 全ページ描画・抽出・図ページ目視は完了。本文の100%目視校正は未完了。 / full rendering and extraction done; 100% text proofreading incomplete |
| Day 1–6の既存失敗 / pre-existing Day 1–6 failures | 3件。Day 7–9と無関係。 / three, unrelated |

**重要 / important:** 数値とシミュレーションのPASSは、実機のPASSでも安全機能の検証でもありません。 / Numerical and simulation passes are not hardware passes or safety validation.

---

## 9. 最終受入マトリクス / Final acceptance matrix

| ゲート / Gate | 判定 / Status | 根拠 / Evidence | 残り / Remaining |
|---|---|---|---|
| G0 リポジトリ基準 / baseline | **PASS** | 開始SHA、クリーンな開始、PDFハッシュ、旧ファイル棚卸し、保護範囲 | なし / none |
| G1 PDFカバレッジ / coverage | **PASS** | 51/51ページ、テキスト+画像、51行のマップ | なし |
| G2 技術修正 / corrections | **PASS** | p.31、p.32、Y1、シリンダ、モーター、電気、安全、PDF | 実機依存の未確認は残る / hardware-dependent items remain |
| G3 ノートブック / notebooks | **PASS** | 9/9、42コードセル、フィンガープリント、オフライン実行 | なし |
| G4 図・シミュレーション / visuals | **PASS** | 29 SVG、Inkscape描画、14 Nodeチェック、Pythonモデル | 図の細部は拡大が必要な場合 / some detail needs zoom |
| G5 教材 / teaching materials | **PASS** | ワークシート3、解答3、ルーブリック、ガイド3、用語集、時間割 | 初学者パイロット未実施 / no pilot |
| G6 PDF品質 / PDF quality | **PASS（制約付き）/ PASS with limitation** | 3 PDF、構造チェック合格、全ページ描画、図表ページ目視 | 本文の完全目視校正は未完了 / full text proofreading incomplete |
| G7 回帰・清掃 / regression and cleanup | **PASS（既知の例外）/ PASS with noted exceptions** | Day 7–9 40 passed、Day 6 11 passed、旧教材削除、保護310件 | Day 1–6の既存3失敗 / three pre-existing failures |
| G8 最終工学レビュー / final review | **PASS** | 計算、状態機械、I/O、図、安全文言、トレーサビリティを再確認 | 実機・安全・独立レビューは未実施 / hardware, safety and independent review not performed |

**総合 / overall:** 教育用のDay 7–9コースとしては**リリース可能 / releaseable for educational use**。実機の設計・製作・安全検証に使うには、追加の実機確認と有資格レビューが必要。 / Releaseable as an educational course; real design, build and safety validation require additional hardware work and qualified review.

---

## 10. 引継ぎ / Handover

### 10.1 正本 / canonical files

| 内容 / Content | 正本 / canonical |
|---|---|
| コース順序・時間・図・PDFページ / order, time, figures, PDF pages | `day07_09_support/lesson_manifest.json` |
| 講義本文 / lesson text | `notebooks/Day07_Automation_Concept_Mechanics/*.md`, `Day08_Electrical_PLC/*.md`, `Day09_Communication_Commissioning/*.md` |
| 計算・PLC・通信モデル / calculations, PLC, network | `day07_09_support/examples/automation_models.py` |
| 図 / diagrams | `assets/diagrams/day07|day08|day09/*.svg`（生成元は `scripts/generate_day07_09_diagrams.py`） |
| 時間割 / timetable | `COURSE_SYLLABUS_DAY07_09.md` |
| 元PDF対応 / source mapping | `day07_09_support/curriculum_source_map.csv` |
| 正誤 / errata | `docs/reference/Automation_Equipment_PDF_Errata_ja_en.md` |
| 保護範囲 / protected scope | `day07_09_support/reference_data/protected_baseline_hashes.txt` |

### 10.2 再生成 / regeneration

```powershell
cd AI_Vision_Training
.\.venv\Scripts\python.exe day07_09_support\scripts\generate_day07_09_diagrams.py
.\.venv\Scripts\python.exe day07_09_support\scripts\render_diagrams.py
.\.venv\Scripts\python.exe day07_09_support\scripts\build_day07_09_notebooks.py
.\.venv\Scripts\python.exe day07_09_support\scripts\generate_reference_outputs.py
.\.venv\Scripts\python.exe day07_09_support\scripts\export_day07_09_pdf.py
.\.venv\Scripts\python.exe day07_09_support\scripts\check_day07_09_pdfs.py
.\.venv\Scripts\python.exe day07_09_support\scripts\build_protected_baseline.py
```

`.ipynb` とPDFは直接編集しない。`.md`、マニフェスト、モデル、SVGを直して再生成する。 / Do not edit `.ipynb` or PDFs directly; edit the canonical sources and regenerate.

### 10.3 テスト / tests

```powershell
python -m pytest day07_09_support/tests/test_day07_09_course.py -q
python -m pytest day06_support/tests -q
node day07_09_support/tests/run_simulation_logic_tests.js
```

### 10.4 壊してはいけない不変条件 / invariants not to break

1. 元PDFのSHA-256と51ページ。 / source PDF hash and 51 pages.
2. タクト42 s、実力能力199.92、摩擦力19.62 N、設計力39.24 N、理論内径11.18 mm。
3. モーター0.477 N·m、60 rpm、9.55 N·m、η=0.90で8.59 N·m。
4. 電気負荷0.73 A（定常合計、承認ではない）。
5. 回収1.42年（316,800円/年、450,000円、運用費0の仮定）。
6. 統一I/O: X0–X3、M0、Y0、Y1（遅延ランプ）、Y2（電磁弁）、T0。
7. 自己保持 `(X0 AND X2) OR M0`、直列X1。X2を保持枝に入れない。
8. リセットは動作開始ではない。復電時に自動再起動しない。
9. BLOCKED / NOT TESTEDをPASSにしない。
10. 通常のPLC制御を安全機能として扱わない。
11. Day 1–6と元PDFを変更しない（保護ベースライン310件）。

### 10.5 保護範囲 / protected areas

- `notebooks/Day01_*` 〜 `Day06_*`、`notebooks/00_Setup`
- `day06_support/`
- `assets/`（Day 1–6のデータ・モデル・図・i18nを含む。Day 7–9の図は除く）
- `docs/pdf/Day01–06`、`Week1`、`Course_Syllabus` など
- `docs/instructor/day01–06`
- `docs/reference/` の元PDF
- `requirements/`
- `COURSE_SYLLABUS.md`、`COURSE_SYLLABUS_DAY06.md`

Day 7–9を変更するときは、保護ベースラインを再生成しない限り、Day 1–6のテストを変更しない。 / When changing Day 7–9, do not modify Day 1–6 tests unless you also regenerate the protected baseline and document the reason.

### 10.6 次の作業 / next work

1. 独立した技術・安全レビュー。 / independent technical and safety review.
2. 実機での圧力・負荷・センサー・弁・ネットワーク確認。 / real pressure, load, sensor, valve and network checks.
3. 初学者1名でのパイロットと所要時間の実測。 / beginner pilot and timing measurement.
4. PDF本文の完全な目視校正。 / full visual proofreading of PDF text.
5. Day 1–6の既存3失敗の扱いを、Day 1–6の担当者と決める。 / decide the three pre-existing Day 1–6 failures with the Day 1–6 owner.
6. コミット・プッシュは、承認後に実施する。 / commit and push only after approval.
