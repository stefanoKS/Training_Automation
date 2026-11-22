# 第8日 ワークシート：PLC入出力・シーケンス表 / Day 8 Worksheet: PLC I/O and Sequence

氏名 / Name: ____________________　日付 / Date: ____________　班 / Group: ______

**記入のきまり / How to fill this in**

- すべて**訓練用の仮想入出力**です。実機のアドレスや配線は書きません。 / Everything is **simulated training I/O**; do not state real addresses or wiring.
- 安全機能と通常の制御論理を混ぜないでください。 / Keep safety functions separate from ordinary control logic.

## 1. PLCの構成要素 / PLC components

| # | 構成要素 / component | 役割 / role |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

## 2. 入出力の分類 / I/O classification

| 信号 / signal | 入力か出力か / input or output | デジタルかアナログか / digital or analog | 何を表すか / meaning |
|---|---|---|---|
| 材料有無センサ / presence sensor | | | |
| 表示灯 / indicator lamp | | | |
| エンコーダのパルス / encoder pulses | | | |
| 圧力センサの値 / pressure value | | | |
| 電磁弁の指令 / valve command | | | |
| ブザー / buzzer | | | |

## 3. 真理値表 / Truth tables

X0 と X1 の AND、OR、NOT X0 を完成させてください。 / Complete AND, OR and NOT X0.

| X0 | X1 | AND | OR | NOT X0 |
|---|---|---|---|---|
| 0 | 0 | | | |
| 0 | 1 | | | |
| 1 | 0 | | | |
| 1 | 1 | | | |

## 4. 接点の読み方 / Reading contacts

1. 参照ビット X0 = 0 のとき、NO接点は導通しますか。 / Does an NO contact conduct when X0 = 0?
   答え / answer: __________
2. 参照ビット X0 = 0 のとき、NC接点は導通しますか。 / Does an NC contact conduct when X0 = 0?
   答え / answer: __________
3. 「NC接点は、現場のNCスイッチのことである」という文は正しいですか。理由も書いてください。 / Is “an NC contact means a field NC switch” correct? Explain.
   ______________________________________________________________________

## 5. 自己保持 / Self-holding

起動 X0、停止 X1（NC接点）、保持 M0 の自己保持について、次の表を完成させてください。
Complete the table for start X0, stop X1 (NC contact) and held bit M0.

| 前のM0 / previous M0 | X0 | X1 | 次のM0 / next M0 |
|---|---|---|---|
| 0 | 0 | 0 | |
| 0 | 1 | 0 | |
| 1 | 0 | 0 | |
| 1 | 0 | 1 | |
| 1 | 1 | 1 | |

**停止要求と起動要求が同時に来たとき、どちらを優先しますか。理由も書いてください。**
**Which wins when start and stop arrive together? Explain.**
______________________________________________________________________

## 6. タイマとカウンタ / Timer and counter

1. オン遅延タイマで、設定値が 100 ms 単位の K30 のとき、設定時間は何秒ですか。 / An ON-delay with K30 at a 100 ms base: what is the preset time?
   答え / answer: __________
2. プリセット3のカウンタで、X0 が 1→0→1→0→1→0 と変化しました。カウントはいくつですか。 / Preset 3 counter, X0 goes 1→0→1→0→1→0. What is the count?
   答え / answer: __________
3. X0 が1のまま5秒続いた場合、カウントは増えますか。 / If X0 stays 1 for five seconds, does the count increase?
   答え / answer: __________

## 7. シーケンス表 / Sequence table

状態と遷移条件を書いてください。 / Write states and transition conditions.

| 状態 / state | 入る条件 / entry condition | 出る条件 / exit condition | 次の状態 / next state |
|---|---|---|---|
| 待機 / Idle | | | |
| 準備完了 / Ready | | | |
| 起動中 / Starting | | | |
| 運転中 / Running | | | |
| 検査中 / Inspecting | | | |
| 停止処理 / Stopping | | | |
| 故障 / Fault | | | |
| 復旧 / Recovery | | | |

## 8. インターロック / Interlocks

| 種類 / class | 例 / example | 通常のラダーで実装してよいか / OK in ordinary ladder? |
|---|---|---|
| プロセス / process | | |
| 品質 / quality | | |
| 安全関連 / safety-related | | |

## 9. 警報と故障対応 / Alarms and fault response

| 事象 / event | 症状 / symptom | 検出方法 / detection | 記録する情報 / log | 人の確認 / human review | 自動で仮定しないこと / must not be assumed |
|---|---|---|---|---|---|
| AI結果タイムアウト / AI timeout | | | | | |
| カメラ未準備 / camera not ready | | | | | |
| 通信断 / comms lost | | | | | |

## 10. 復旧の説明 / Recovery explanation

故障から復旧までの手順を、4段階で書いてください。自動再起動を前提にしないでください。
Describe recovery in four steps without assuming automatic restart.

1. ____________________
2. ____________________
3. ____________________
4. ____________________

**安全に関する注意 / Safety note:** 実機のPLCプログラム変更・配線は、権限・バックアップ・検証・現地手順が必要です。本ワークシートは机上の学習です。
**Safety note:** Real PLC program and wiring changes need authority, backups, verification and site procedure. This worksheet is a desk exercise.
