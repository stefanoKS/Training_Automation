# 第6日 実装・検証報告 / Day 6 implementation and verification report

## 1. 基準 / Repository baseline

- 開始ブランチ / Starting branch: `main`.
- 開始HEAD / Starting HEAD: `3443340e98b958d3d5245c6e8ed3f8eb5f17a8cf`.
- 開始時の作業ツリー / Initial worktree: clean.
- 第1週の保護対象として追跡済みファイル330件のSHA-256を、変更前にセッション領域へ記録。最終確認は下記。/ SHA-256 baseline for 330 tracked Week 1 files recorded outside the repository before modification; final comparison below.
- 現在の作業ツリー / Final worktree: untracked additions only in `AI_Vision_Training/week2/day06/`; no tracked file diff.

## 2. 成果物 / Deliverables (all added files)

| ファイル / File | 用途 / Purpose |
|---|---|
| `README_ja_en.md` | 読み方と独立した生成手順 / reading order and independent build |
| `DAY06_SYLLABUS_ja_en.md` | 唯一の時間割 / sole timetable |
| `lessons/Day06_01_LLM_Agent_Harness.md`, `.ipynb` | モデル、支援、エージェント、ハーネス / concepts and architecture |
| `lessons/Day06_02_Ideas_and_Requirements.md`, `.ipynb` | 問題、アイデア、要件、継続事例 / requirements and case study |
| `lessons/Day06_03_Prompting_and_Agents.md`, `.ipynb` | 指示、計画、監督、修正 / prompting, planning and corrections |
| `lessons/Day06_04_Testing_and_Handover.md`, `.ipynb` | 受入、安全、引き継ぎ / verification, safety and handover |
| `assets/SOURCES_AND_LICENSES.md` | 図の目録と出典 / figure manifest and sources |
| `assets/diagrams/D06-01.svg` | 技術から監督への移行 / training transition |
| `assets/diagrams/D06-02.svg` | YOLO・PatchCore・LLM / three model flows |
| `assets/diagrams/D06-03.svg` | モデル・アシスタント・エージェント・ハーネス / component distinctions |
| `assets/diagrams/D06-04.svg` | 権限とツールの循環 / permission-checked execution |
| `assets/diagrams/D06-05.svg` | 問題から受入まで / idea-to-software process |
| `assets/diagrams/D06-06.svg` | 悪い・良い指示 / prompt comparison |
| `assets/diagrams/D06-07.svg` | 要件の分類 / requirements structure |
| `assets/diagrams/D06-08.svg` | 架空の日本語画面 / fictional Japanese UI |
| `assets/diagrams/D06-09.svg` | 人・ChatGPT・実装担当 / three-participant workflow |
| `assets/diagrams/D06-10.svg` | 会話の段階 / conversation timeline |
| `assets/diagrams/D06-11.svg` | 品質ゲート / quality gates |
| `assets/diagrams/D06-12.svg` | 見た目・動作・受入 / three evidence types |
| `assets/diagrams/D06-13.svg` | 次の担当への引き継ぎ / handover |
| `assets/diagrams/D06-14.svg` | 機密と設備の隔離 / privacy and operational safety |
| `examples/inspection_app_spec_ja_en.md` | 継続例の承認用仕様 / approved sample spec |
| `examples/example_agent_prompts_ja_en.md` | 6種類の対訳指示 / six bilingual prompt templates |
| `examples/example_agent_conversation_ja_en.md` | 架空の会話の流れ / simulated conversation |
| `examples/example_test_cases_ja_en.md` | 受入チェックの計画 / planned acceptance checks |
| `examples/example_handover_ja_en.md` | 架空の引き継ぎ / simulated handover |
| `instructor/day06_instructor_guide_ja_en.md` | 午前・午後、代替実演、解答 / sessions, offline fallback, answers |
| `worksheets/Day06_Student_Worksheet_ja_en.md` | 最終提出 / final student submission |
| `worksheets/Day06_Assessment_Rubric_ja_en.md` | 講師用評価表 / instructor rubric |
| `scripts/build_day06_notebooks.py` | Markdown原稿からコードセルなしのノートブックを生成 / build notebooks |
| `scripts/export_day06_pdf.py` | 4冊から独立したA4 PDFを生成 / export PDF from notebooks |
| `tests/test_day06_contracts.py` | 第6日だけの構造・内容・PDF・保護範囲の検証 / isolated contracts |
| `pdf/Day06_explanation_ja_en.pdf` | 日本語・英語の図入り解説 / illustrated bilingual companion |
| `DAY06_IMPLEMENTATION_REPORT.md` | 本報告 / this report |

各SVGは本教材用のオリジナル作品です。図ごとの対応章・目的・出典は[図目録](assets/SOURCES_AND_LICENSES.md)を参照。14図ともXML解析、ローカル参照、PDFへの掲載を確認。/ All 14 figures are original course artwork; the [manifest](assets/SOURCES_AND_LICENSES.md) maps each to its objective and lesson. XML structure, local links and PDF inclusion were checked.

## 3. 授業の構成と言語 / Course and language review

01（70分）はLLM/画像AIと権限、02（95分）は問題と要件、03（80分）は実装前の計画と修正、04（55分）は受入と安全を扱います。講師120分・必須学習300分・休憩30分・提出30分・昼食50分で530分です。演習は紙だけで進められ、学生用コードセルはありません。

01 (70 min) covers models and permission; 02 (95 min) defines a problem and specification; 03 (80 min) plans and corrects; 04 (55 min) verifies and hands over. The schedule totals 530 min including 120 instructor, 300 required learning, 30 breaks, 30 submission and 50 lunch. All activities can be done on paper without code.

各節は日本語→英語→図や例→問いの順とし、架空の `PVC-EX-001`、`PVC-EX-002` と同じCSV列を照合しました。製品用語は[公式資料](assets/SOURCES_AND_LICENSES.md)で確認。学習者本人を交えた日本語の校正・所要時間の試行は未実施です。

Sections pair Japanese then English, followed by a figure or example and reflection. Fictional lot IDs and CSV columns were checked across the case study. Product terminology was checked against [official sources](assets/SOURCES_AND_LICENSES.md). A beginner pilot and native-language editorial review have not yet been performed.

## 4. 実際の検証 / Actual validation

- `python AI_Vision_Training\week2\day06\scripts\build_day06_notebooks.py` — 4冊を生成。/ Built four notebooks.
- `python AI_Vision_Training\week2\day06\scripts\export_day06_pdf.py` — 4冊から生成。/ Exported from all four notebooks.
- `python -m pytest AI_Vision_Training\week2\day06\tests\test_day06_contracts.py -q` — **10 passed** (final run).
- PDFはA4の22ページで全章が正しい順序、図は16配置（14種類）です。PDFiumで全4章の代表ページと大きな表・図のページを画像化して目視確認。日本語の本文と図ラベルが表示され、テキストを抽出できます。/ The A4 PDF has 22 pages, correct chapter order and 16 figure placements (14 unique figures). Representative pages from all four modules, including large tables/figures, were rasterized with PDFium and visually inspected. Japanese prose and figure text render; PDF text is extractable.
- 一度のImageMagickによるSVG画像化では日本語が欠字になったため、PDF出力をChrome/Edgeの表示で画像化する方式へ修正し、再生成・再確認しました。/ Initial ImageMagick SVG conversion produced missing Japanese glyphs; exporter now uses Chrome/Edge rendering and the PDF was rebuilt and checked.

## 5. 保護対象 / Protected files and working tree

開始時の330件の追跡済み第1週ファイルとSHA-256を比較し、**変更0件**。`git diff --name-status`は空で、`git status --short --untracked-files=all`の追加物はすべて第6日ディレクトリ内。既存PDFと既存翻訳は一切再生成していません。

All 330 baseline protected tracked files match their original SHA-256 values; **zero changed**. Tracked diff is empty; all new files are isolated under Day 6. Existing PDFs and translations were not regenerated.

## 6. 制限と判定 / Limitations and readiness

図はノートブックでは編集可能なSVG、PDFではフォント互換性を保つため画像として埋め込み、図中の文字はPDFテキスト検索対象ではありません（図の説明と本文は検索可能）。教材作成機でPDFを再生成するにはPythonのReportLab、Pillow、PlaywrightとChromeまたはEdgeが必要です。使用するAI製品の画面・利用権限は環境で異なります。初学者との試行と講師による最終確認が残ります。

SVGs stay editable in the notebooks; the PDF embeds rasterized figures to preserve Japanese glyphs, so text inside figures is not searchable (captions and body text are). Regeneration needs ReportLab, Pillow, Playwright and local Chrome or Edge on the authoring machine. Product interfaces and permissions vary. A beginner pilot and instructor review remain outstanding.

**READY FOR INSTRUCTOR REVIEW.**
