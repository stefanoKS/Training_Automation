# 承認用の架空仕様 / Fictional specification for approval

**塩ビシート不良記録アプリ / PVC Sheet Defect Recording Application.** 学習用、架空・ローカルのみ。実装済みの製品ではありません。/ Educational, fictional and local-only; this is not an implemented product.

| 項目 / Item | 日本語 | English |
|---|---|---|
| 目的 / Purpose | 手書きの不良記録を探す手間を減らす | Make handwritten defect records easier to find |
| 利用者 / User | 検査担当者 | Inspection operator |
| 必須入力 / Required | ロット番号、検査日時、不良種別（黒点・傷・すじ） | Lot ID, inspection date/time, defect type (black spot, scratch, streak) |
| 任意入力 / Optional | 不良の説明、備考 | Defect description, remarks |
| 入力検査 / Validation | 必須項目が空なら保存せず、日本語のエラーを出す | Reject missing required values and show a Japanese error |
| 重複 / Duplicates | 同じ内容でも1件ずつ別の記録として保存する | Preserve repeated submissions as separate records |
| 保存 / Persistence | ローカルへ保存し、終了と再起動後も記録を残す。削除機能は設けない | Save locally and retain records across restart; no deletion feature |
| 一覧・集計 / List/count | すべての記録、ロット/不良種別の絞り込み、表示中の記録件数 | List all, filter by lot/type, count visible entries |
| CSV / CSV | `lot_id,inspected_at,defect_type,description,remarks` の順。保存失敗は通知し、元の記録を残す | Columns in that order; report export failure without destroying records |
| 画面 / UI | 日本語の欄名・ボタン・エラー表示 | Japanese labels, buttons and errors |
| 禁止 / Out of scope | 実データ、画像判定、クラウド、本番DB・カメラ・PLC・ロボットへの接続 | No real data, image inference, cloud or connection to live DB, camera, PLC or robot |

**架空例 / Fictional examples:** `PVC-EX-001`・黒点 / black spot; `PVC-EX-002`・傷 / scratch. 日時は架空の値を入力して試します。/ Use fictional timestamps.

**受入 / Acceptance:** 0件では一覧が空で件数0。必須の空欄は拒否。2件を保存すると件数2、再起動後も2件。黒点で絞ると前者だけで件数1。CSVはヘッダー1行と正しいデータ2行を含み、指定列順になる。出力失敗は日本語で通知され、記録は残る。/ Empty list shows 0; required-field omissions are rejected; two entries remain after restart; filtering black spot shows only the first with count 1; CSV contains one header and two correct data rows in the agreed order; export errors are reported in Japanese without losing records.

技術選定や保存形式は、既存プロジェクトを確認してから計画段階で提案します。/ Propose technologies and local storage format only after inspecting the project during planning.
