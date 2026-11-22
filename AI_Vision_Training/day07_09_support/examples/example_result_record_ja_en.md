# 記入例：検査結果レコードとハンドシェイク / Worked example: inspection record and handshake

**架空のデータです。実在のロット・画像・装置とは関係ありません。 / Fictional data, unrelated to any real lot, image or machine.**

## 1. 結果レコードの例 / example result records

| image_id | timestamp | lot_id | position_mm | model_version | config_version | result | valid | operator_review |
|---|---|---|---|---|---|---|---|---|
| IMG-000101 | 2026-01-01T09:00:01 | LOT-EX-01 | 1200 | patchcore-1.0 | cfg-A | OK | 1 | none |
| IMG-000102 | 2026-01-01T09:00:02 | LOT-EX-01 | 1300 | patchcore-1.0 | cfg-A | NG | 1 | pending |
| IMG-000103 | 2026-01-01T09:00:03 | LOT-EX-01 | 1400 | patchcore-1.0 | cfg-A | — | 0 | required |

3行目は「無効」であり、**OK ではありません**。 / Row 3 is invalid and **not OK**.

## 2. ハンドシェイクの例 / example handshake

| 手順 / step | 送信側 / sender | 内容 / content | 受信側の動作 / receiver action |
|---|---|---|---|
| 1 | PLC | 検査準備OK / ready | PCは待機 / PC waits |
| 2 | PLC | 検査要求＋ID / request + ID | PCは受付を返す / PC returns busy |
| 3 | PC | 結果＋ID＋有効/無効 / result + ID + validity | PLCはIDを照合 / PLC checks ID |
| 4 | PLC | 受領確認 / acknowledge | PCは記録 / PC records |
| 5 | PC | エラー・タイムアウト / error or timeout | PLCは保留 / PLC holds |

## 3. 古い結果の判定例 / stale-result decisions

| 受信ID / received ID | 前回のID / last accepted | 判定 / decision | 理由 / reason |
|---|---|---|---|
| 102 | 101 | 受け付け / accept | 新しいID / new ID |
| 101 | 102 | 拒否 / reject | 古いID / stale ID |
| 102 | 102 | 拒否 / reject | 重複ID / duplicate |
| —（タイムアウト） / timeout | 103 | 保留 / hold | 結果なしはOKではない / no result is not OK |

## 4. 受入確認の記入例 / acceptance-check example

| # | 確認 / check | 方法 / method | 合格条件 / pass criteria |
|---|---|---|---|
| 1 | 無効結果の扱い / invalid handling | 無効を注入 / inject invalid | OKにならない / never OK |
| 2 | 古いID / stale ID | 前回IDを再送 / resend old ID | 拒否される / rejected |
| 3 | タイムアウト / timeout | 応答を止める / stop responses | 保留になる / held |
| 4 | 再起動 / restart | 故障後に再起動 / restart after fault | 古い結果を使わない / no stale reuse |
| 5 | 安全の独立性 / safety independence | 設計レビュー / design review | AIと独立 / independent of AI |
