# 第7〜9日 実装前監査 / Day 7–9 Pre-Implementation Audit

記録日 / Recorded: 2026-11-22 (Asia/Tokyo)
作成 / Author: implementation agent (GPT Sol role), reviewed by no production engineer yet.

この文書は **Checkgate G0** の記録です。実装を始める前にリポジトリの実状態を確認し、保護対象の基準値を記録しました。
This document is the **Checkgate G0** record: the repository was inspected before any Day 7–9 file was created, and a baseline of protected content was recorded.

## 1. リポジトリ基準状態 / Repository baseline

| 項目 / Item | 値 / Value |
|---|---|
| ブランチ / Branch | `main` |
| HEAD | `0d30045b663104867ec77da9ac55e34714527695` |
| HEAD 件名 / Subject | `Add Day 6 materials: Agents and Harnesses notebook and markdown, along with submission guidelines` |
| リモート / Remote | `origin https://github.com/stefanoKS/Training_Automation.git` |
| 未コミット変更 / Uncommitted changes | なし / none (`git status --porcelain` 空 / empty) |
| 追跡ファイル数 / Tracked files | 387 |
| 取得 / Fetched | 取得しませんでした（指示により破壊的操作と通信を避けました）。リモート状態は未確認です。 / Not fetched; remote state unverified by instruction. |

`git fetch` は実行していません。したがって「リモートと同一か」は確認していません。ローカルの `main` と HEAD のみを基準とします。
No `git fetch` was run, so equality with the remote was **not** verified. Only local `main` and HEAD form the baseline.

## 2. 既存構造の確認 / Existing structure observed

- ノートブック階層は `AI_Vision_Training/notebooks/DayNN_Topic/` 形式です。
- Day 6 は 5 本の Markdown 原稿から 5 本の `.ipynb` を生成する方式です（`day06_support/scripts/build_day06_notebooks.py`）。
  - セルはすべて `markdown`（実行セルなし）。
  - `## ` 見出しでセルを分割。
  - メタデータに `day06_source_sha256` と `day06_source` を保持し、原稿との不一致を検出。
  - セル ID は `f"{name.lower()[:16]}-{index:02}"` 形式。
- PDF は `day06_support/scripts/export_day06_pdf.py` が ReportLab + Playwright(Chrome) で A4 に組み、SVG を PNG 化して貼り付けます。原稿ハッシュが一致しないと中断します。
- 図は `assets/diagrams/day06/D06-NN.svg` に編集可能 SVG として格納され、`<title>`/`<desc>` と日英ラベルを持ちます。
- テストは `day06_support/tests/test_day06_contracts.py` が pytest で契約（存在・日英・図・PDF・保護パス）を検証します。
- 先生用資料は `docs/instructor/`、PDF は `docs/pdf/`、レビューは `docs/reviews/` にあります。

## 3. 保護対象の基準値 / Protected baseline

`git ls-files AI_Vision_Training` の全 387 ファイルについて `git hash-object` を記録しました。
Hashes for all 387 tracked files were recorded with `git hash-object`.

- 記録ファイル / Manifest: `AI_Vision_Training/day07_09_support/reference_data/protected_baseline_hashes.txt`
- 形式 / Format: `<sha1>  <path>`（`git hash-object` と同一 / identical to `git hash-object`）

代表値 / Examples:

| ファイル / File | SHA-1 |
|---|---|
| `AI_Vision_Training/.gitignore` | `52559db4a3e787afbc4541de95b0a9618b5c5e83` |
| `AI_Vision_Training/COURSE_SYLLABUS.md` | `ce1276e775861fdc8b6cea0161bb3591672e4d8c` |
| `AI_Vision_Training/COURSE_SYLLABUS_DAY06.md` | `136e789d6e3bb0cbcace1b6c117eed787b9c8001` |
| `AI_Vision_Training/README.md` | `a45bad87b35a42b58d0ce2fce36440ae5651c041` |
| `AI_Vision_Training/START_HERE.md` | `7e7c1d359ff2ca2403e2038f49e920a3f67fa7c5` |

保護対象 / Protected: 既存のノートブック、Markdown 原稿、図、PDF、翻訳、データセット、重み、先生用資料、既存テスト、第1週と第6日の時間割、ノートブック探索・翻訳・出力の既存基盤。
Existing notebooks, manuscripts, diagrams, PDFs, translations, datasets, weights, instructor guides, existing tests, Week 1 and Day 6 syllabi, and the existing discovery/translation/export infrastructure.

## 4. 追加予定の新規パス / Intended new-file scope

以下だけを新規に作ります（既存ファイルは変更しません）。
Only the following will be created; no existing file is modified.

```
AI_Vision_Training/
├── COURSE_SYLLABUS_DAY07_09.md
├── notebooks/Day07_Machine_Fundamentals/  (3 .md + 3 .ipynb)
├── notebooks/Day08_PLC_Control/           (3 .md + 3 .ipynb)
├── notebooks/Day09_System_Integration/    (3 .md + 3 .ipynb)
├── assets/diagrams/day07..day09/          (12 + 12 + 12 SVG)
├── day07_09_support/
│   ├── README_ja_en.md
│   ├── SOURCES_AND_LICENSES.md
│   ├── examples/ simulations/ worksheets/ reference_data/ scripts/ tests/
├── docs/instructor/day07..day09_instructor_guide.md
├── docs/pdf/Day07..Day09_explanation_ja_en.pdf
└── docs/reviews/Day07_09_PreImplementation_Audit.md, Day07_09_Final_Review.md
```

`week2/` は作りません。`notebooks/` 以外の最上位学習階層も作りません。
No `week2/` tree and no new top-level learning hierarchy outside `notebooks/`.

## 5. 既存の Day 7–9 材料の有無 / Pre-existing Day 7–9 material

確認結果 / Result: なし / none.
`notebooks/Day07_*`, `notebooks/Day08_*`, `notebooks/Day09_*`, `assets/diagrams/day07..09`, `day07_09_support`, `COURSE_SYLLABUS_DAY07_09.md`, `docs/instructor/day07..09*`, `docs/pdf/Day07..09*` は HEAD に存在しませんでした。
None of these paths existed at HEAD, so there is no prior work to extend.

## 6. 意図的な仮定 / Explicitly fictional assumptions

- 中心事例は「連続塩ビシート検査機（教育用の概念モデル）」です。実機の仕様ではありません。
- 数値例（ロール径・速度・画素数など）はすべて仮定値で、各所で「仮定 / hypothetical」と明記します。
- PLC は「Mitsubishi MELSEC 風の架空ラック」として説明し、実機の CPU・アドレス・タイマ時定数を断定しません。
- 安全機能は「別途設計・検証される独立した安全系」として扱い、本教材から展開可能な安全プログラムは作りません。

## 7. Checkgate G0 の結論 / G0 conclusion

- リポジトリ状態を把握した / understood.
- 保護ファイルの基準値を記録した / recorded.
- 追加パスは既存と衝突しない / no conflict.
- Day 1–6 は未変更のまま / untouched.

**G0: PASS**（この時点 / at this point）. 最終確認は `Day07_09_Final_Review.md` で再実行します。
Final re-verification is repeated in `Day07_09_Final_Review.md`.
