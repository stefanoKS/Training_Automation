# Day 7–9 PDF移行監査 / Day 7–9 PDF migration audit

**実施日 / Date:** 2026-11-23
**対象リポジトリ / Repository:** `https://github.com/stefanoKS/Training_Automation`
**対象 / Scope:** `AI_Vision_Training/` の Day 7–9 を、元PDF由来の3日間コースへ置換 / replace Days 7–9 with a three-day course derived from the source PDF
**状態 / Status:** 実装・検証の作業記録。最終判定は [`Day07_09_Release_Review.md`](Day07_09_Release_Review.md) を参照。
Working record of implementation and verification. See the release review for the final assessment.

---

## G0 — リポジトリ基準 / repository baseline

| 項目 / Item | 結果 / Result |
|---|---|
| 開始コミット / starting commit | `879824c802c3a35a45074ce4017c296e58332630` |
| ブランチ / branch | `main` |
| `origin/main` | 同じSHA（`git fetch` 後）/ same SHA after fetch |
| 作業ツリー / working tree | 開始時はクリーン / clean at start |
| 元PDF / source PDF | `docs/reference/自動化設備製作研修_5日間_詳細版_受講者用.pdf` |
| 元PDF SHA-256 | `3380c2b67e148cd9a71b0f9071963744f3b0acba7491b309708b0f31183707ae` |
| 元PDFページ数 / pages | 51 |
| 元PDFの変更 / modification | なし / none |
| 旧Day 7–9の棚卸し / old Day 7–9 inventory | 3フォルダ、18ファイル（`.md`/`.ipynb`）、旧テスト1、旧図36、旧シミュレーション6、旧レビュー2、旧ガイド3、旧ワークシート8 |
| 共有依存 / shared dependencies | `assets/scripts/course_notebooks.py` はDay 1–5のみを対象にしており、Day 7–9は含まない。変更不要と判断。 / targets Days 1–5 only; no change needed. |

**旧コース / old course**

- `notebooks/Day07_Machine_Fundamentals/`
- `notebooks/Day08_PLC_Control/`
- `notebooks/Day09_System_Integration/`

**置換後 / replacement**

- `notebooks/Day07_Automation_Concept_Mechanics/`
- `notebooks/Day08_Electrical_PLC/`
- `notebooks/Day09_Communication_Commissioning/`

**保護範囲 / protected scope:** Day 1–6のノートブック、データ、モデル、評価、ローカライズ、Day 6 LLM、図、PDF、元PDF。新しい保護ベースラインは `day07_09_support/reference_data/protected_baseline_hashes.txt` に保存。

Days 1–6 notebooks, data, models, evaluation, localisation, Day 6 LLM, diagrams, PDFs and the source PDF. The new baseline is `protected_baseline_hashes.txt`.

---

## G1 — 元PDFのカバレッジ / source PDF coverage

### 抽出と描画 / extraction and rendering

- 全51ページのテキストを `pypdfium2` で抽出: `reference_data/pdf_extract/source_text.txt`
- 全51ページをPNGに描画: `reference_data/pdf_extract/pages/page-001.png` 〜 `page-051.png`
- 図・回路・数式・表・手順のページは、テキストだけでなく画像で確認。
- 自己保持（p.31）、順序制御（p.32）、空圧（p.14）、NPN/PNP（p.25）、I/O（p.27）、ゲート（p.41）を重点的に確認。

- Extracted text for all 51 pages with `pypdfium2`.
- Rendered all 51 pages to PNG.
- Pages with diagrams, circuits, formulas, tables and procedures were checked as images, not text only.
- Focus pages: p.31 self-holding, p.32 sequence, p.14 pneumatics, p.25 NPN/PNP, p.27 I/O, p.41 gates.

### トレーサビリティ / traceability

`day07_09_support/curriculum_source_map.csv` は51行。全ページに明示的な処分がある。

The CSV has 51 rows and an explicit disposition for every page.

| 状態 / Status | 件数 / Count |
|---|---:|
| REQUIRED | 37 |
| REPLACED_WITH_CORRECTED_CONTENT | 7 |
| INCORPORATED_ELSEWHERE | 4 |
| SUPPLEMENTARY | 3 |
| REFERENCE_ONLY | 0 |

| 必須/任意 / Required or optional | 件数 / Count |
|---|---:|
| required | 50 |
| optional | 1 |

**主な置換 / main replacements**

- p.14 空圧の直列ブロック図 → 機能的な空圧回路図（D07-07）を追加。
- p.25 NPN/PNP → 入力共通端子を含む電流経路図（D08-06）に置換。
- p.27 I/O表 → 統一I/O表（Y1は遅延ランプ専用、Y2が電磁弁）に置換。
- p.31 自己保持 → 並列保持接点を含む正しい回路（D08-08）に置換。
- p.32 順序制御 → 8状態の状態機械（D08-09）に置換。
- p.41 試運転ゲート → G0–G6の段階ゲート（D09-06）に置換。G5は任意。

---

## G2 — 技術的修正 / engineering corrections

| 項目 / Item | 修正 / Correction | 証拠 / Evidence |
|---|---|---|
| p.31 自己保持 / self-holding | 並列保持接点を追加。`(X0 AND X2) OR M0`、直列X1。X2は開始時のみ。 / parallel hold added; X2 only at start | D08-08, `sim-selfhold`, tests |
| p.32 順序 / sequence | IDLE–COMPLETE–FAULTの8状態、位置確認、F001/F003、F002 | D08-09, D08-11, simulator tests |
| Y1の重複 / Y1 reuse | Y1=遅延ランプ、Y2=電磁弁。アドレスと端子を分離。 / fixed | canonical I/O, `validate_io`, test |
| シリンダ / cylinder | 11.18 mmを理論下限と明記。カタログ候補と分離。実型式なし。 / theoretical bound separated | `test_mechanical_numbers`, notebook |
| モーター / motor | 9.55 N·mを理想値、η=0.90を追加仮定、8.59 N·m | `test_motor_numbers`, notebook |
| 電気 / electrical | 0.73 Aは定常合計。電源選定の承認ではない。突入・定格低下・電線・端子・保護を別記。 / not an approval | `test_electrical_load_numbers` |
| NPN/PNP | 共通端子を含む閉回路。2線式の漏れ電流。 / common included | D08-06, compatibility cell |
| 安全・試運転 / safety, commissioning | G5は任意。未実施はBLOCKED/NOT TESTED。リセットは開始ではない。 / G5 optional; reset is not start | `test_fault_reset...`, matrix |
| PDFレイアウト / layout | IPv4を`<nobr>`で保護、列幅を文字幅から計算、生HTMLを除去。 / IP and tables fixed | `check_day07_09_pdfs.py` |

詳細は [`../reference/Automation_Equipment_PDF_Errata_ja_en.md`](../reference/Automation_Equipment_PDF_Errata_ja_en.md)。

---

## G3 — ノートブック / notebooks

| ノートブック / Notebook | 実行セル / executable cells | 全体セル / cells | 主な図 / diagrams |
|---|---:|---:|---|
| Day07_01_Requirements | 3 | 7 | D07-01〜05 |
| Day07_02_Mechanical_Architecture | 4 | 9 | D07-06〜08 |
| Day07_03_Equipment_Selection | 7 | 15 | D07-09 |
| Day08_01_Electrical_Fundamentals | 4 | 9 | D08-01〜04 |
| Day08_02_Sensors_and_IO | 4 | 9 | D08-05〜07 |
| Day08_03_Ladder_Sequence | 7 | 15 | D08-08〜11 |
| Day09_01_Industrial_Networking | 4 | 9 | D09-01〜05 |
| Day09_02_Commissioning | 5 | 11 | D09-06〜07 |
| Day09_03_Automation_Proposal | 4 | 9 | D09-08〜09 |

**方式 / approach**

- 正本は `.md`。`python exec` フェンスだけをコードセルへ変換。その他のフェンスは説明用としてMarkdownに残す。
- `lesson_manifest.json` が順序・時間・図・PDFページを所有。
- ノートブックは、マニフェスト、原稿、`automation_models.py`、参照SVG、生成スクリプトの**結合フィンガープリント**を持つ。
- `--check` で古いノートブックを検出。

- Canonical `.md`; only `python exec` fences become code cells; other fences stay Markdown.
- The manifest owns order, time, figures and PDF pages.
- Each notebook stores a combined fingerprint of manifest, manuscript, model, referenced SVGs and generator.
- `--check` detects stale notebooks.

**実行結果 / execution:** 9/9 notebooks execute offline; see G7 and the release review for the exact command and output.

---

## G4 — 図とシミュレーション / diagrams and simulations

- 29個の自作SVG（Day 7: 9、Day 8: 11、Day 9: 9）。すべて `<title>`、`<desc>`、日英ラベル、キャプションを持つ。
- InkscapeでPNGに描画し、1.6倍で目視確認。
- 旧36図のうち、新しい学習目標に合わないカメラ・AI系の図は削除。
- Pythonシミュレーション（`automation_models.py`）と、オフラインHTMLシミュレータ（`sim_plc_sequence.html`）。
- HTMLのロジックはNodeで14チェック。ブラウザなしで検証。

- 29 original SVGs (Day 7: 9, Day 8: 11, Day 9: 9), all with title, desc, bilingual labels and caption.
- Rendered with Inkscape and reviewed at 1.6x.
- Removed the old camera/AI diagrams that no longer serve the replacement syllabus.
- Python simulation and offline HTML simulator.
- HTML logic is tested with Node (14 checks) without a browser.

**既知の制約 / known constraint:** 図は概念図であり、製作図・安全設計図・規格準拠の証明ではない。 / conceptual only.

---

## G5 — 教材 / teaching materials

- 学生ワークシート（Day 7/8/9）、解答キー（Day 7/8/9）、コース評価ルーブリック。
- 講師ガイド（Day 7/8/9）: 16項目、正確な時間割、準備、実演、誤解、解答、安全、オフライン代替、評価。
- 用語集（日英）。
- 時間割は `COURSE_SYLLABUS_DAY07_09.md` のみ。80/85/135分、合計530分。

- Student worksheets, answer keys and a course rubric.
- Instructor guides with 16 sections, exact timetable, preparation, demonstration, misconceptions, answers, safety, offline alternatives and assessment.
- Bilingual glossary.
- The syllabus is the single timetable source: 80/85/135 min, 530 min total.

**未実施 / not performed:** 初学者1名でのパイロット。所要時間は設計値であり、経験的に証明されていない。 / no beginner pilot; durations are design values.

---

## G6 — PDF / PDFs

| PDF | ページ / pages | 画像 / images | サイズ / bytes |
|---|---:|---:|---:|
| Day07_explanation_ja_en.pdf | 58 | 10 | 2,804,758 |
| Day08_explanation_ja_en.pdf | 60 | 12 | 2,845,013 |
| Day09_explanation_ja_en.pdf | 57 | 9 | 2,352,920 |

- 目次、ページ番号、選択可能テキスト、日英、公式カード、用語集、参考文献。
- 全ページをPNGに描画（`docs/pdf/_pages/Day0N/`）。
- テキスト検査: `??`、生HTML、壊れたIPv4、Markdownリンク残りがないこと。
- コンタクトシートでレイアウトを確認。図・表・コード・用語集のページを重点確認。

- TOC, page numbers, selectable text, Japanese and English, formula cards, glossary, references.
- Every page rendered to PNG.
- Text checks: no `??`, raw HTML, broken IPv4 or raw Markdown links.
- Contact sheets reviewed, with figure/table/code/glossary pages checked closely.

**既知の制約 / known constraint:** 図の細部は画面拡大が必要な場合がある。 / some figure detail needs zoom. 用語集が長く、PDF全体のページ数が多い。 / the glossary makes the PDFs long.

**修正した問題 / fixed problems:** 表の列幅、IPv4の改行、生HTML、図のラベル重なり（D07-06、D07-07、D08-06、D08-08、D08-09）。

---

## G7 — 回帰とクリーンアップ / regression and cleanup

**削除 / removed**

- 旧Day 7–9の3フォルダ（18ノートブック関連ファイル）。
- 旧シミュレーション6個と旧フォールバック6個。
- 旧テスト `test_day07_09_contracts.py`。
- 旧スクリプト `engineering_examples.py`、`inspect_day07_09_pdf.py`、`render_simulation_fallbacks.py`。
- 旧サンプル3個。
- 旧レビュー2個（`Day07_09_Final_Review.md`、`Day07_09_PreImplementation_Audit.md`）。
- 旧SVG 7個（D07-10〜12、D08-12、D09-10〜12）。

- Old Day 7–9 folders (18 notebook-related files).
- Six old simulations and six old fallbacks.
- Old contract test.
- Old scripts and sample documents.
- Two old review documents.
- Seven old SVGs.

**保持 / kept:** Day 1–6の教材、データ、モデル、ローカライズ、図、PDF、元PDF。 / Days 1–6 materials and the source PDF.

**新しいテスト / new tests:** `day07_09_support/tests/test_day07_09_course.py`。元PDF、9ノートブックの実行、独立計算、PLC、通信、図、HTML、PDF、時間割、保護ベースラインを検証。 / verifies source, nine notebook executions, calculations, PLC, networking, diagrams, HTML, PDFs, timetable and protected baseline.

**保護ベースライン / protected baseline:** Day 1–6と元PDFを対象に再生成。`git hash-object` で比較するため、コミット後も意味を持つ。作業ツリーが汚れていることを要求しない。 / regenerated for Days 1–6 and the source PDF; compares `git hash-object`, so it remains meaningful after commit and does not require a dirty tree.

---

## G8 — 最終レビュー / final review

最終的なPASS/FAIL/NOT VERIFIED、テストの実出力、未検証事項は [`Day07_09_Release_Review.md`](Day07_09_Release_Review.md) に記録する。この監査は、その根拠となる実装記録である。

The final PASS/FAIL/NOT VERIFIED assessment, actual test output and unverified items are in the release review. This audit is the implementation record behind it.

---

## 残っている制約 / remaining constraints

1. 実機の通電・空圧・安全検証は未実施。 / no real energisation, pneumatics or safety validation.
2. メーカー型式・圧力損失・負荷率・実摩擦・実センサー応答は未確認。 / manufacturer models, pressure loss, load factor, real friction and sensor response are unverified.
3. 初学者パイロットは未実施。 / no beginner pilot.
4. PDFの図の細部は、画面拡大が必要な場合がある。 / some PDF figure detail requires zoom.
5. 実ネットワーク設定は変更していない。 / no real network changes.
