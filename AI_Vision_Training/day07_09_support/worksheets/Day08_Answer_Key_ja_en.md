# 第8日 解答例と採点の観点 / Day 8 Answer Key (instructor copy)

**学生には配布しません。 / Do not distribute to students.**

## 1. PLCの構成要素 / PLC components

例 / examples: CPU、電源、入力モジュール、出力モジュール、通信、メモリ、診断表示。
Accept five correct items; "the box" alone earns nothing.

## 2. 入出力の分類 / I/O classification

| 信号 / signal | 入出力 / I/O | 種類 / kind |
|---|---|---|
| 材料有無センサ / presence sensor | 入力 / input | デジタル / digital |
| 表示灯 / indicator | 出力 / output | デジタル / digital |
| エンコーダ / encoder | 入力 / input | パルス / pulse |
| 圧力センサ / pressure | 入力 / input | アナログ / analog |
| 電磁弁指令 / valve command | 出力 / output | デジタル（またはアナログ） / digital or analog |
| ブザー / buzzer | 出力 / output | デジタル / digital |

## 3. 真理値表 / Truth tables

| X0 | X1 | AND | OR | NOT X0 |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 1 |
| 0 | 1 | 0 | 1 | 1 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 1 | 1 | 1 | 0 |

## 4. 接点の読み方 / Contacts

1. 導通しない / does not conduct.
2. 導通する / conducts.
3. 正しくない。NC接点はビット0で導通する論理命令であり、現場スイッチの物理接点形式とは別。 / Not correct; an NC contact conducts when the bit is 0 and is unrelated to the switch's physical contact form.

## 5. 自己保持 / Self-holding

| 前 / previous | X0 | X1 | 次 / next |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 1 | 0 |

停止優先 / stop wins. Reason: the NC contact breaks the seal-in path; safety and process intent require the stop to dominate.
Full marks require both the table and the priority statement.

## 6. タイマとカウンタ / Timer and counter

1. 30 × 100 ms = **3.0 s**（時間単位は実装依存 / time base is implementation-specific）。
2. 立ち上がり3回 → **3**。
3. 増えない（連続ONは数えない） / no increase; a held ON is not counted.

## 7. シーケンス表 / Sequence table

Accept any consistent table where each transition has a condition. Typical answers:
Idle→Ready when controller, sensors, camera, AI and mode conditions hold; Ready→Starting on start; Starting→Running when material and camera are ready; Running→Inspecting when the camera is ready; Inspecting→Stopping on stop; Stopping→Idle when stopping completes; any→Fault on fault; Fault→Recovery on reset; Recovery→Idle only with a restart permit.
Deduct when a transition has no condition.

## 8. インターロック / Interlocks

| 種類 / class | 例 / example | 通常ラダー可否 / ordinary ladder |
|---|---|---|
| プロセス / process | 材料なしで開始しない / no start without material | 可 / yes |
| 品質 / quality | 無効結果をOKにしない / invalid never OK | 可 / yes |
| 安全関連 / safety | ガード開放で危険動作停止 / guard open stops hazard | **不可（別設計）/ no** |

## 9. 警報と故障対応 / Alarms and fault response

- AIタイムアウト / timeout: 更新停止 / no update → 期限超過 / deadline → 保留・時刻・ID / hold, time, ID → 必須 / yes → 「良品」と仮定しない / never OK.
- カメラ未準備 / camera not ready: 状態異常 / status abnormal → 状態監視 / monitoring → 状態・最後の正常時刻 / state, last good time → 必須 / yes.
- 通信断 / comms lost → ハートビート途絶 / heartbeat lost → タイムアウト / timeout → 最後の値と時刻 / last value and time → 必須 / yes → 「最新値が有効」と仮定しない / never assume the last value is valid.

## 10. 復旧 / Recovery

例 / example: ①原因の確認と除去 / find and clear the cause、②リセット / reset、③再起動条件の確認 / check restart conditions、④人が再起動を許可 / a person permits restart.
Deduct if any answer implies automatic restart.

## 採点表 / Marking scheme（合計20点 / total 20）

| 項目 / item | 点 / points |
|---|---:|
| PLC構成 / PLC components | 2 |
| 入出力分類 / I/O classification | 2 |
| 真理値表 / truth tables | 3 |
| 接点の読み方 / contacts | 3 |
| 自己保持と停止優先 / self-holding and stop priority | 3 |
| タイマ・カウンタ / timer and counter | 2 |
| シーケンス表 / sequence table | 3 |
| インターロックと安全の区別 / interlocks and safety separation | 2 |

**合格の目安 / pass mark:** 12点以上、かつ「無効な結果をOKにしない」「安全は通常のラダーと別」の記述があること。
12 or more, and the answer must state that invalid results are never OK and that safety is separate from ordinary ladder logic.
