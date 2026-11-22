# 第8日 公式・確認カード / Day 8 formula and check card

**すべて訓練用の仮想例です。/ All examples are simulated training cases.**

## 1. 真理値表 / Truth tables

| X0 | X1 | AND | OR | NOT X0 |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 1 |
| 0 | 1 | 0 | 1 | 1 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 1 | 1 | 1 | 0 |

## 2. 接点の評価 / Contact evaluation

| 命令 / instruction | 導通する条件 / conducts when |
|---|---|
| NO接点 / NO contact | 参照ビット = 1 / referenced bit = 1 |
| NC接点 / NC contact | 参照ビット = 0 / referenced bit = 0 |

**物理配線（NO/NC）と論理接点（NO/NC）は別です。 / Physical wiring and logical contacts are different.**

## 3. 自己保持 / Self-holding

next = stop ? 0 : (start ? 1 : held)

| start | stop | held | next |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 |
| 0 | 0 | 1 | 1 |
| 0 | 1 | 1 | 0 |
| 1 | 1 | 1 | 0（停止優先 / stop wins） |

## 4. タイマとカウンタ / Timer and counter

**ON遅延 / ON-delay:** 出力 = (入力ONの連続時間 ≥ 設定時間)。
**時間 = 設定値 × 時間単位**（例：100 ms 単位で K20 → 2.0 s。単位はCPU依存 / time base depends on the CPU）。

**カウンタ / counter:** 立ち上がりごとに +1、プリセットで出力ON、リセットで0。

| 事象 / event | count |
|---|---|
| 初期 / initial | 0 |
| 立ち上がり1 / rising 1 | 1 |
| 連続ONのまま / held ON | 1 |
| 立ち上がり2 / rising 2 | 2 |
| リセット / reset | 0 |

## 5. 状態と遷移 / States and transitions

待機 → 準備完了 → 起動中 → 運転中 → 検査中 → 停止処理 → 待機。故障は任意の状態から入り、復旧には**原因除去・リセット・人の再起動許可**が必要です。
Idle → Ready → Starting → Running → Inspecting → Stopping → Idle. Fault can be entered from any state; recovery needs **cause removal, reset and human restart permission**.

## 6. 安全確認 / Safety check

- ☐ 状態遷移に条件がある / every transition has a condition
- ☐ 停止要求が優先される / stop request has priority
- ☐ 故障中は起動できない / start refused while faulted
- ☐ 自動再起動を前提にしていない / no assumed automatic restart
- ☐ 品質NGと機械故障を区別している / NG and fault are distinguished
- ☐ 安全機能を通常のラダーと表現していない / safety functions are not ordinary ladder

## 8. 追加の読解演習 / Extra reading exercises

次の文章を読み、出力を答えてください（すべて仮想）。 / Read each description and give the output (all simulated).

1. X0=1、X1=1、X2 は NC接点で X2=0。直列回路の出力は？ / X0=1, X1=1, X2 is an NC contact with X2=0. What is the series output?
2. 自己保持 M0 が1、停止要求 X1 が0、起動 X0 が0。M0 は？ / M0 is held at 1, stop X1=0 and start X0=0. What is M0?
3. オン遅延 2.0 s で、入力が 1.0 s ON → 0.5 s OFF → 1.0 s ON。出力は？ / ON-delay 2.0 s, input ON 1.0 s, OFF 0.5 s, ON 1.0 s. Output?
4. カウンタ プリセット3、立ち上がり2回、リセットなし。出力は？ / Counter preset 3, two rising edges, no reset. Output?

**解答 / answers:** 1. 1（すべて導通）。2. 1（保持が続く）。3. 0（合計は2.5 sだが連続していない。実装依存の確認が必要）。4. 0（プリセット未満）。
1. 1 (all conduct). 2. 1 (still held). 3. 0 (2.5 s total but not continuous; confirm implementation behaviour). 4. 0 (below preset).

## 9. よくある誤解 / Common misunderstandings

1. NC接点＝NCスイッチ → 別の概念 / NC contact equals NC switch → different concepts.
2. 連続ONでカウンタが増え続ける → 増えるのは変化 / a held ON keeps counting → only transitions count.
3. スキャンは全PLCで同じ → 機種依存 / every PLC scans the same → model-dependent.
4. 故障後に自動で戻してよい → リスクアセスメントが必要 / auto-restart after fault → needs risk assessment.
