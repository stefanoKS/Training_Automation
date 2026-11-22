# 架空アプリの受入表 / Acceptance checks for a fictional app

これは手動で結果を観察するための**計画**であり、実際に試験した記録ではありません。/ This is a **planned manual checklist**, not a record of tests actually performed.

| 番号 / ID | 操作 / Action | 期待する結果 / Expected observable result |
|---|---|---|
| 1 | 新しい架空の空データを開く / Open a new fictional empty dataset | 一覧0件、表示件数0 / empty list and count 0 |
| 2 | ロット番号空欄で保存 / Save without lot ID | 保存されず、日本語のエラー / no save; Japanese error |
| 3 | 日時または不良種別空欄で保存 / Save without date/time or type | 保存されず、日本語のエラー / no save; Japanese error |
| 4 | `PVC-EX-001`・黒点と `PVC-EX-002`・傷を保存 / Save both sample entries | 一覧に2件、件数2、種別が一致 / two rows, count 2, types correct |
| 5 | アプリ終了・再起動 / Exit and restart | 2件が残る / both records remain |
| 6 | 黒点で絞る / Filter black spot | `PVC-EX-001` のみ、表示件数1 / only first row, visible count 1 |
| 7 | 絞り込み解除・CSV出力 / Clear filter and export CSV | ヘッダー `lot_id,inspected_at,defect_type,description,remarks` と2データ行 / agreed header and two data rows |
| 8 | CSV保存できない場所を指定 / Try unwritable destination | 失敗が通知され、記録2件が残る / visible failure; both records intact |
| 9 | 同じ内容を再度登録 / Enter same record again | 別の記録として追加される / new separate record |

試験後は実測結果・日時・担当者・実行環境・未確認項目を書き足してください。結果を推測で記入しないでください。/ After real testing, add observed results, date, tester, environment and unverified items. Never invent outcomes.
