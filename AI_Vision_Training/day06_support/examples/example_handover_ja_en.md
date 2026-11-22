# 架空の引き継ぎ / Simulated handover

**SIMULATION / 架空:** これは実装や試験が行われた証拠ではありません。/ This does not claim implementation or real test execution.

| 項目 / Item | 日本語 | English |
|---|---|---|
| 元の仕様 / Approved requirements | [承認用仕様](inspection_app_spec_ja_en.md)を参照 | See [approved sample specification](inspection_app_spec_ja_en.md) |
| 完了と報告された内容 / Reported progress | 日本語入力欄、必須検査、ローカル保存、一覧、絞り込み | Japanese form, validation, local save, list and filters |
| 残作業 / Outstanding | CSV出力と保存失敗表示、受入確認 | CSV export and error display, acceptance review |
| 変更ファイル / Changed files | 架空の例：`day06_app/form`, `day06_app/store`。実ファイルは未作成 | Fictional example: `day06_app/form`, `day06_app/store`; no such files were created |
| 試験 / Test evidence | 未提示。成功を主張しない | None supplied; no claim of pass |
| 既知の問題 / Known issue | CSVボタンがない | CSV button absent |
| 禁止 / Protected scope | 第1〜5日、実データ、本番システムには触れない | Do not touch Days 1–5, real data or production systems |
| 次にすること / Next step | 現状を調べ、CSVだけの計画を出し、承認後に修正、保存の回帰確認を報告 | Inspect existing state, propose CSV-only plan, obtain approval, fix and report save regression checks |

受け取ったエージェントは「完了と報告された内容」を事実として扱う前に、実際のファイルと動作を確認してください。/ The receiving agent must inspect files and behavior before treating reported progress as verified fact.
