# 記入例：PLC入出力表とシーケンス / Worked example: PLC I/O table and sequence

**架空の訓練用データです。実機のアドレスではありません。 / Fictional training data; not real addresses.**

## 1. 入出力表 / I/O table

| デバイス / device | 種類 / kind | 内容 / description | 故障時の扱い / on failure |
|---|---|---|---|
| X0 | デジタル入力 / DI | 材料有無 / material presence | 保留・確認 / hold and check |
| X1 | デジタル入力 / DI | 起動要求 / start request | 受け付けない / refuse |
| X2 | デジタル入力 / DI | 停止要求 / stop request | 停止優先 / stop priority |
| X3 | パルス入力 / pulse | エンコーダ / encoder | 故障 / fault |
| Y0 | デジタル出力 / DO | 運転表示 / running lamp | 消灯 / off |
| Y1 | デジタル出力 / DO | マーキング指令 / marking command | 停止 / stop |
| M0 | 内部ビット / internal | 運転状態 / running state | 保持は要確認 / retention to verify |
| D100 | 数値 / register | アナログ値の例 / example analog value | 無効扱い / treat as invalid |

## 2. ラダーの説明例 / ladder explanation examples

1. `X1`（NO）と `X2`（NC）を直列し、`M0` を駆動。起動は停止要求が無いときだけ有効。 / X1 (NO) in series with X2 (NC) drives M0; start is valid only without a stop request.
2. `M0`（NO）を `X1` と並列にして自己保持。停止要求で解除。 / M0 (NO) parallels X1 for self-holding; the stop request clears it.
3. `X0` が ON の間だけ `Y0` を点灯。材料がないときは運転表示を出さない。 / Y0 is ON only while X0 is ON; no running indication without material.

## 3. 状態表 / state table

| 状態 / state | 入る条件 / entry | 出る条件 / exit |
|---|---|---|
| 待機 / Idle | 起動していない / not started | 準備条件成立 / readiness holds |
| 準備完了 / Ready | 準備条件成立 / readiness | 起動要求 / start |
| 運転中 / Running | 材料あり＋カメラ準備 / material and camera ready | 停止要求・故障 / stop or fault |
| 停止処理 / Stopping | 停止要求 / stop | 停止完了 / stopping done |
| 故障 / Fault | 故障信号 / fault | リセット＋原因除去 / reset and cause cleared |

## 4. 警報の例 / alarm example

| 警報 / alarm | 原因候補 / likely cause | 記録 / log | 対応 / action |
|---|---|---|---|
| AI結果タイムアウト / AI timeout | PC負荷・通信 / PC load, comms | 時刻・ID / time, ID | 保留・人へ連絡 / hold and notify |
| カメラ未準備 / camera not ready | 接続・設定 / connection, settings | 状態・最終正常時刻 / state, last good time | 開始しない / do not start |
