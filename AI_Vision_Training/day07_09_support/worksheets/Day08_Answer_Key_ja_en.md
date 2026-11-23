# 第8日 解答例と採点の観点 / Day 8 Answer Key (instructor copy)

**学生には配布しません。 / Do not distribute to students.**

**採点の原則 / Marking principles**

数値の一致だけでは正解にしません。式、単位、定常と突入の区別、そして「何を確認したことになるか」の説明を確認します。特に、PLCのアドレスと物理端子、物理接点と論理接点、指令と確認を混同している答案は、値が合っていても減点します。

A matching value is not enough. Check the formula, the units, the steady-versus-inrush distinction and the explanation of what has actually been verified. Answers that confuse addresses with terminals, physical with logical contacts, or a command with a confirmation are marked down even when the number is right.

**この解答例の位置づけ / Status of this key:** 教育用の架空のアドレスと決定論的シミュレーションに基づきます。実機の応答・タイマー精度・安全機能を保証するものではありません。 / Fictional training addresses and a deterministic simulation; nothing here certifies real response, timer accuracy or safety functions.

## T1 電気負荷の計算 / Electrical load calculation

**期待される答え / Expected answers**

| 負荷 / Load | 数量 / Qty | 単位電流の式 / Unit-current formula | 単位電流 / Unit current | 合計 / Total |
|---|---:|---|---:|---:|
| ランプ / lamp（3 W） | 2 | 3 W ÷ 24 V | 0.125 A | 0.250 A |
| センサー / sensor | 3 | 指定値 / given | 0.060 A | 0.180 A |
| 電磁弁 / solenoid valve | 2 | 指定値 / given | 0.150 A | 0.300 A |
| **定常合計 / steady-state total** | | 0.250 + 0.180 + 0.300 | | **0.73 A** |

- 消費電力の合計は 24 V × 0.73 A = **17.52 W**。内訳（6.0 + 4.32 + 7.2 W）でも一致します。 / The total power is 17.52 W; the itemised sum (6.0 + 4.32 + 7.2 W) agrees.
- 余裕率25 %の計画電流は 0.73 × 1.25 = 0.9125 → **0.91 A**。 / A 25 % margin gives 0.91 A.
- 参考: 6 Wランプ1個は 6 ÷ 24 = 0.25 A、動作点の抵抗は 24 ÷ 0.25 = 96 Ω。ただしランプの抵抗は温度で変わるため、この96 Ωを一定値として扱えません。 / A 6 W lamp draws 0.25 A and shows about 96 Ω at its operating point, but lamp resistance changes with temperature.

**「承認ではない」理由 / Why the total is not approval**

1. 0.73 Aは**定常状態**の合計で、ランプの突入電流、電磁弁のサージ、電源投入時の同時ONを含まない。 / It is a steady-state sum and excludes lamp inrush, valve surge and simultaneous switch-on.
2. 全負荷が同時にONになるという仮定を置いている。実際の同時使用率は運転モードで変わる。 / It assumes every load is on at once; the real simultaneity depends on the operating mode.
3. 周囲温度・密閉盤・隣接機器による電源の定格低下（ディレーティング）を確認していない。 / Supply derating for ambient temperature, enclosure and adjacent equipment is unchecked.
4. 電線の許容電流、端子の定格、ヒューズ・遮断器の定格と選択協調を確認していない。 / Wire ampacity, terminal ratings and fuse or breaker coordination are unchecked.
5. 将来の拡張と保守の余裕を、根拠付きで決めていない。 / Future expansion and maintenance margin are not justified.

上のうち3つ以上を、定常・突入・定格低下・電線・保護の区別を含めて書いていれば受理します。 / Accept three or more of these, provided the distinctions are stated.

**よくある誤り / Common mistakes**

- ランプの3 Wをそのまま3 Aとして合計し、6.48 A とする（3 × 2 + 0.18 + 0.30）。 / Treating 3 W as 3 A and reporting 6.48 A.
- 余裕率25 %を 0.73 ÷ 0.75 と計算する（正しくは × 1.25）。 / Dividing by 0.75 instead of multiplying by 1.25.
- 0.73 Aを「電源は0.73 A以上でよい」と断定する。 / Concluding "any supply above 0.73 A is fine".
- 突入電流を「0.73 Aに含まれている」と書く。 / Claiming inrush is included.
- 合計にすでに含まれる負荷数を、電力の計算でもう一度掛ける。 / Multiplying by the load count again after it is already in the total.

**許容範囲 / Acceptable range**

0.73 A（0.729〜0.731）、計画電流0.91 A（0.912〜0.913）、電力17.5〜17.52 W。0.9125 Aを丸めずに書いた答案も可。 / Values within these bands are acceptable, including unrounded intermediates.

## T2 センサーとNPN/PNPの互換性 / Sensor and NPN/PNP compatibility

**期待される答え / Expected answers**

| 構成 / Config | 判定 / Verdict | 理由 / Reason |
|---|---|---|
| A シンク入力＋PNP | **適合 / compatible** | PNPはONで出力を+側につなぐ。電流は+24V → センサー → 出力 → PLC入力 → 入力共通（0V）へ流れ、閉回路になる。 |
| B ソース入力＋NPN | **適合 / compatible** | NPNはONで出力を0V側につなぐ。電流は+24V → 入力共通 → PLC入力回路 → 入力端子 → センサー → 0Vへ流れる。 |
| C シンク入力＋NPN | **不適合の可能性 / likely incompatible** | センサーも入力共通も0V側になり、入力回路に電流を流す電位差ができない。 |
| D ソース入力＋PNP | **不適合の可能性 / likely incompatible** | センサー出力も入力共通も+24V側になり、やはり電位差ができない。 |
| E 2線式 | **要確認 / check** | 漏れ電流とOFF時の電圧を確認する。微小漏れで入力がONのままになることがある。 |

**電流経路の答え / Current path**

+24V → センサー（茶）/ sensor brown → センサー出力（黒）/ output black → PLC入力端子 / input terminal → PLC入力回路 / input circuit → 入力共通端子（0V）/ input common.

**2線式で確認する2項目 / Two-wire checks**

- 漏れ電流（OFF時にも微小電流が流れ、入力が落ちないことがある）。 / Leakage current, which can hold an input ON.
- OFF時の端子間電圧が、PLC入力のOFFしきい値を下回るか。 / Whether the OFF-state voltage is below the input's OFF threshold.

**解説 / Why the common matters**

NPN/PNPは「信号の極性」ではなく「電流をどこへ流すか」の違いです。判定はセンサー単体では完結せず、PLC入力の共通端子の電位と入力回路の方式で決まります。2線式は3線式と同じ扱いにできません。

NPN and PNP describe where the current flows, not a "positive or negative signal". The verdict cannot be made from the sensor alone: it depends on the input common potential and the input circuit. A two-wire sensor cannot be treated like a three-wire one.

**よくある誤り / Common mistakes**

- 「PNPは＋の信号なので、どの入力でもつながる」と書く。 / "A PNP is a positive signal, so it works with any input."
- センサーの出力線だけを見て、入力共通端子を無視する。 / Looking only at the output wire and ignoring the common.
- NPNを「危険」「使えない」と断定する。 / Calling NPN dangerous or unusable.
- 2線式を「3線式と同じ」と扱う。 / Treating two-wire as three-wire.

**許容範囲 / Acceptable range**

AとBを適合、CとDを不適合（または「不適合の可能性」）、Eを「要確認」としていれば受理します。理由に「入力共通端子」と「電流の向き」の両方が入っていることを必須とします。 / A and B compatible, C and D incompatible, E to be checked, with both the common and the current direction in the reason.

## T3 統一I/O表 / Canonical I/O map

**期待される答え / Expected answers**

| 種別 / Kind | アドレス / Address | 機器 / Device | 正常時の状態 / Normal state |
|---|---|---|---|
| 入力 / input | X0 | START押しボタン / START pushbutton | OFF（押している間ON）/ OFF, ON while pressed |
| 入力 / input | X1 | STOP許可（物理NC停止）/ STOP_OK from physical NC stop | 健全時ON / ON while healthy |
| 入力 / input | X2 | 後退端確認 / retracted confirmation | 後退端でON / ON at retracted end |
| 入力 / input | X3 | 前進端確認 / extended confirmation | 前進端でON / ON at extended end |
| 内部 / internal | M0 | 運転状態 / RUN state | 電源投入時OFF / OFF at power-up |
| 出力 / output | Y0 | 運転表示ランプ / RUN lamp | 停止時OFF / OFF when stopped |
| 出力 / output | Y1 | 遅延表示ランプ（T0完了）/ delayed lamp (T0 done) | 3秒未満はOFF / OFF before 3 s |
| 出力 / output | Y2 | 前進電磁弁指令 / extend solenoid command | OFF＝ばね戻り（訓練用弁）/ OFF = spring return |
| タイマー / timer | T0 | 3秒オン遅延 / 3 s on-delay | 運転OFFで0 / 0 when RUN off |

**Y1とY2 / Y1 and Y2**

Y1は遅延ランプ専用で、電磁弁には使いません。電磁弁の前進指令はY2です。1つの出力を2つの負荷に使うと、ランプの故障や電流容量の超過が弁の動作に影響します。

Y1 is reserved for the delayed lamp and is never used for the solenoid; the extend command is Y2. Sharing one output between two loads lets a lamp fault or an exceeded current rating affect the valve.

**X1が正常時ONの理由 / Why X1 is ON when healthy**

X1は物理的にはNC（通常閉）の停止ボタンから来ます。ボタンが押されていない健全な状態では接点が閉じており、入力はONです。ラダーでは「X1がONなら許可」としてNO接点で読みます。物理接点のNCと、ラダー上のNC接点は別の概念です。

X1 comes from a physical NC stop button. While the button is not pressed, the contact is closed and the input is ON. The ladder reads it with an NO contact as "permission when ON". A physical NC contact and a ladder NC instruction are different concepts.

**検査が検出する2つの問題 / The two detected problems**

- Y1に電磁弁を割り当てている（Y1は遅延ランプ専用、電磁弁はY2）。 / Y1 assigned to the solenoid.
- X1の正常状態をOFFと書いている（正しくはON）。 / X1 recorded as normal OFF.

**よくある誤り / Common mistakes**

- T0を出力の一種として「Y」で書く。 / Writing the timer as a Y output.
- M0を入力として分類する。 / Classifying M0 as an input.
- 「Y1は予備」と書く。 / Describing Y1 as a spare.
- アドレスを物理端子番号として説明する。 / Treating addresses as physical terminals.

**許容範囲 / Acceptable range**

9行の機器と正常時の状態は完全一致を要求します。表現の揺れ（「押している間ON」など）は可ですが、Y1への電磁弁割当、X1の正常時OFF、T0の出力扱いは、いずれも不受理です。 / Exact device and normal-state values are required for all nine rows. Wording may vary, but Y1 for the solenoid, X1 normal OFF or T0 as an output is not accepted.

## T4 修正した自己保持ラング / Corrected self-holding rung

**期待されるラング / Expected rung**

```text
|--+--[ X0 ]--[ X2 ]--+--[ X1 ]--( M0 )--|
|  |                  |
|  +--[ M0 ]----------+
```

**要素の整理 / Element check**

| 要素 / Element | アドレス / Address | 直列か並列か / Series or parallel | 役割 / Role |
|---|---|---|---|
| 開始条件 / start condition | X0 | 並列枝の直列要素 / series inside one branch | START押下で始める / start on press |
| 開始時の位置条件 / position at start | X2 | 開始枝のみ / start branch only | 後退端でのみ開始 / start only when retracted |
| 保持接点 / holding contact | M0 | 開始枝と並列 / parallel with the start branch | STARTを離しても保持 / hold after release |
| 停止許可 / stop permission | X1 | 全体に直列 / series with the whole branch | OFFで運転を落とす / OFF drops RUN |
| コイル / coil | M0 | — | 運転状態の記憶 / stores RUN |

**シミュレーションの答え / Expected simulated trace**

| 時点 / Step | 状態 / State | RUN | Y0 | Y1 | Y2 | T0 (ms) |
|---|---|---|---|---|---|---|
| 初期 / initial | IDLE | 0 | 0 | 0 | 0 | 0 |
| START押下 / pressed | READY | 1 | 1 | 0 | 0 | 0 |
| STARTを離して+1 / released +1 | EXTEND | 1 | 1 | 0 | 1 | 100 |
| STARTを離して+2 / released +2 | WAIT_EXTENDED | 1 | 1 | 0 | 1 | 200 |
| STOPを開く / STOP opened | IDLE | 0 | 0 | 0 | 0 | 0 |

読み取る点は3つです。STARTを離してもRUNが1のままであること、STOPでRUN・Y0・Y2がOFFになりT0が0に戻ること、Y2がEXTENDとWAIT_EXTENDEDの間だけONであることです。

Three things to read: RUN stays 1 after START is released; STOP clears RUN, Y0 and Y2 and resets T0 to 0; Y2 is ON only during EXTEND and WAIT_EXTENDED.

**X2を保持枝に入れない理由 / Why X2 stays out of the holding branch**

X2は後退端でON、前進するとOFFになります。保持枝にもX2を入れると、シリンダが前進してX2がOFFになった瞬間にM0が落ち、動作が途中で止まります。開始条件と保持条件を分ける必要があります。

X2 is ON at the retracted end and turns OFF as the cylinder extends. With X2 also in the holding branch, M0 would drop the moment the cylinder starts to move. The start condition and the run condition must be separated.

**よくある誤り / Common mistakes**

- 保持接点（M0の並列枝）がない。 / No seal-in contact.
- X2を全体の直列に入れ、前進直後に運転が落ちる。 / Putting X2 in series with everything.
- X1をNC接点で読む（X1は健全時ONなので、NOで読む）。 / Reading X1 with an NC contact.
- STOPを自己保持の外に置き、保持が切れない。 / Leaving STOP outside the holding path.

**許容範囲 / Acceptable range**

ラングの形は問いませんが、(X0 AND X2) OR M0 の並列枝があり、X1が全体に直列で、M0の保持枝がX2を通らないことが条件です。トレースの5行は完全一致を要求します。 / Any drawing is acceptable if the parallel branch is (X0 AND X2) OR M0, X1 is in series with the whole branch, and the M0 path avoids X2. The five trace rows must match exactly.

## T5 タイマーの境界 / Timer boundary

**期待される答え / Expected answers**

| 時点 / Point | T0 | Y1 | 状態 / State |
|---|---:|---|---|
| 境界の直前 / just before | 2,999 ms | **OFF** | RUN継続 / RUN continues |
| 境界 / at the boundary | 3,000 ms | **ON** | RUN継続 / RUN continues |
| STOP直後 / after STOP | **0 ms** | **OFF** | IDLE |

T0はRUNがONの間だけ増え、3,000 msで頭打ちになります。STOPでRUNが落ちるとT0は0に戻り、Y1もOFFになります。つまりY1は「3秒経過した」という事実の表示であり、シリンダの位置や安全状態の表示ではありません。

T0 accumulates only while RUN is ON and saturates at 3,000 ms. When STOP drops RUN, T0 returns to 0 and Y1 goes OFF. Y1 indicates that three seconds have elapsed, not a cylinder position or a safe state.

**実機で「ちょうど3.000秒」にならない理由 / Why a real PLC may differ**

- スキャン周期の分だけ、タイマーの更新が遅れる。 / The scan period delays the timer update.
- タイマーの時間単位・分解能が機種で異なる（10 ms、100 msなど）。 / Time base and resolution differ by model.
- 入力フィルタや通信の更新周期が、見かけの応答を変える。 / Input filters and communication cycles change the apparent response.

**よくある誤り / Common mistakes**

- 2,999 msでONと書く（境界の意味を取り違えている）。 / Marking Y1 ON at 2,999 ms.
- STOP後もT0が3,000 msのまま残ると書く。 / Leaving T0 latched after STOP.
- Y1を「シリンダが前進した」の表示と説明する。 / Describing Y1 as an extend confirmation.

**許容範囲 / Acceptable range**

2,999 msでOFF、3,000 msでON、STOP後は0 msでOFF、状態はIDLE。この4点が一致すれば受理します。丸めや「約3秒」の表現は、境界の数値が示されている場合に限り可。 / Accept when 2,999 ms is OFF, 3,000 ms is ON, STOP gives 0 ms and OFF, and the state is IDLE. Approximate wording is acceptable only if the boundary values are shown.

## T6 シーケンスの状態 / Sequence states

**期待される答え / Expected answers**

| 状態 / State | 出力 / Outputs | 次へ進む条件 / Transition | タイムアウト / Timeout |
|---|---|---|---|
| IDLE | 全出力OFF / all OFF | 新規START、X2 ON、X1 ON / fresh START, X2, X1 | — |
| READY | Y0 ON、M0 ON | 次スキャンでEXTEND / next scan | — |
| EXTEND | Y2 ON | WAIT_EXTENDEDへ / to WAIT_EXTENDED | — |
| WAIT_EXTENDED | Y2 ON | X3 ONかつX2 OFF → RETRACT | F001（3秒仮）/ 3 s |
| RETRACT | Y2 OFF | WAIT_RETRACTEDへ / to WAIT_RETRACTED | — |
| WAIT_RETRACTED | Y2 OFF | X2 ONかつX3 OFF → COMPLETE | F003（3秒仮）/ 3 s |
| COMPLETE | Y0 ON、T0完了ならY1 ON | 新規START / fresh START | — |
| FAULT | 全出力OFF、警報 / all OFF, alarm | リセット＋新規START / reset plus fresh START | — |

**正常サイクル / Normal cycle**

IDLE → **READY** → **EXTEND** → **WAIT_EXTENDED** → **RETRACT** → **WAIT_RETRACTED** → **COMPLETE**

**指令と確認 / Command versus confirmation**

Y2をONにしたのは「前進せよ」という指令であり、X3がONになったのは「前進端に到達した」という確認です。指令を出しただけでは動いた証拠になりません。

Y2 ON is the command "extend"; X3 ON is the confirmation "the extended end was reached". A command alone is not evidence of motion.

**よくある誤り / Common mistakes**

- EXTENDとWAIT_EXTENDEDを1つの状態にまとめ、位置確認の待ちを表現しない。 / Merging the command and the wait, losing the confirmation.
- タイムアウト値を「3秒で確定」と書く（3秒は教材の仮値）。 / Treating 3 s as a fixed requirement.
- FAULTから直接READYへ戻る矢印を書く。 / Drawing FAULT → READY directly.

**許容範囲 / Acceptable range**

8状態の名前は完全一致を要求します。遷移条件は言葉が違っても、位置確認（X2・X3）、停止許可（X1）、新規STARTの3要素が入っていれば受理します。 / The eight state names must match. Transition wording may vary if it includes position confirmation (X2, X3), stop permission (X1) and a fresh START.

## T7 異常処理と再起動 / Fault handling and restart

**期待される答え / Expected answers**

| 異常 / Fault | 検出 / Detection | 応答 / Response | リセット / Reset | 再起動 / Restart |
|---|---|---|---|---|
| F001 前進端未確認 | WAIT_EXTENDEDで3秒超過 / over 3 s | Y2 OFF、RUN OFF、FAULT | 原因除去＋リセット / clear cause, reset | 新規START / fresh START |
| F002 前後端同時ON | X2とX3が同時ON / both ON | 全出力OFF、FAULT | 原因除去＋リセット / clear cause, reset | 新規START / fresh START |
| F003 後退端未確認 | WAIT_RETRACTEDで3秒超過 / over 3 s | Y2 OFF、RUN OFF、FAULT | 原因除去＋リセット / clear cause, reset | 新規START / fresh START |
| STOP操作 | X1がOFF / X1 OFF | RUN OFF、Y2 OFF、T0=0、IDLE | 停止を戻す / release stop | 新規START / fresh START |
| 停電・復電 | 電源監視・初期化 / supply monitor | 出力OFF、M0 OFF | 自動で開始しない / no auto-start | 新規START / fresh START |
| リセット中のSTART | リセットとSTARTが同時 / both ON | リセットを受け付けない / reset refused | STARTを離す / release START | 新規START / fresh START |

**リセット直後の観測値 / Observation right after reset**

状態 / state: **IDLE**　Y2: **OFF（0）**　RUN: **OFF（0）**

シミュレーションでは、FAULTでX2とX3を同時ONにした後、STARTを押したままリセットすると **FAULT** のまま拒否され、STARTを離してからリセットすると **IDLE**・故障コードなし・Y2 OFFになります。リセットは異常状態を解除する操作であり、動作を開始する操作ではありません。

In the simulation, resetting with START held keeps the state at FAULT; releasing START and then resetting gives IDLE with no fault code and Y2 OFF. Reset clears a fault state; it does not start motion.

**「保持されている／いない」の両方が危険な理由 / Why both assumptions are unsafe**

内部ビットが保持されるかは、機種・設定・電池・不揮発メモリで変わります。保持される場合、復電時に前回の運転状態が残る可能性があります。保持されない場合でも、押しっぱなしのSTARTや初期化の順序によって動き出す可能性があります。どちらの前提にも立たず、復電時は必ず「STARTを離す → 新しく押す」を要求する設計にします。

Whether a bit is retained depends on the model, settings, battery and non-volatile memory. If retained, the previous RUN state may survive a power cycle. If not retained, a held START or the initialisation order may still cause motion. Rely on neither assumption: always require "release START, then press again" after power restoration.

**よくある誤り / Common mistakes**

- リセットを開始条件として使い、リセットで動き出す設計にする。 / Using reset as a start condition.
- 復電時に自動復帰する設計を「効率的」と評価する。 / Praising automatic resume after power restoration.
- F002を「センサーの故障」とだけ書き、配線・位置・詰まりの確認を落とす。 / Calling F002 only a sensor failure.
- タイムアウトを延ばすことを対策とする。 / Treating a longer timeout as the fix.

**補足 / Note on F003:** モデルの `run_scenario("retract_stuck")` が後退端未確認を再現し、`F003` でFAULTになることを単体テストで確認しています。ただし、12件の試運転マトリクスにはF003専用の行がないため、マトリクス上は「設計上の応答＋別途のモデル試験」であり、実機の証跡ではありません。実機では後退端未確認の試験を追加してください。 / `run_scenario("retract_stuck")` reproduces the missing retract confirmation and a unit test confirms F003. The 12-case commissioning matrix has no dedicated F003 row, so it is a design response plus a separate model test, not hardware evidence. Add a retract-confirmation test on the real machine.

**許容範囲 / Acceptable range**

6行すべてに検出・応答・リセット・再起動が入っていれば受理します。リセット後に「新しいSTART」と書いてあることを必須とし、「リセットで再開」は不受理です。 / Accept when all six rows cover detection, response, reset and restart. A fresh START after reset is mandatory; restart on reset is not accepted.

## T8 通電前の確認 / Pre-power verification

**期待される答え / Expected answers**

| 区分 / Area | 確認する内容 / What to check | 合格の判断 / Pass condition | 実施者 / By whom |
|---|---|---|---|
| 遮断・無電圧 / isolation | 遮断器、別電源、バックフィード、蓄電部、検電 / breaker, alternative supply, backfeed, stored energy, tester | 無電圧を確認し、ロックアウト済み / zero verified and locked out | 有資格者 / qualified person |
| 図面との照合 / drawings | 配線図、機器、端子番号、線番 / drawing, device, terminal, wire number | 図面と一致 / matches the drawing | 実施者＋確認者 / worker and checker |
| 定格・極性 / ratings | 電圧、極性、信号方式、保護装置 / voltage, polarity, signal type, protection | 定格内で向きが正しい / within rating and correctly oriented | 有資格者 / qualified person |
| 導体・端子 / conductors | ほつれ、露出、短絡、緩み、曲げ / strands, exposure, short, looseness, bend | 損傷なし、規定トルク / no damage, correct torque | 実施者 / worker |
| 安全・立入り / safety | 可動部への接近、飛出し、ガード / access, ejection, guard | ガードが固定され、立入り不可 / guard fixed, no access | 講師・安全担当 / instructor and safety |
| 承認 / approval | チェック結果の記録と署名 / records and signature | 有資格者と講師の承認 / qualified and instructor approval | 有資格者・講師 / both |

**電磁弁OFFで安全にならない理由 / Why de-energising the valve is not enough**

コイルをOFFにしても、弁の種類（単一ソレノイド・ダブルソレノイド・中央閉止）、ばねの向き、負荷、配管に閉じ込められた空気によって、シリンダは動く可能性があります。残圧は遮断しただけでは抜けません。遮断・排気・零圧確認・ロックアウトをそろえて初めて、保全できる状態になります。

Switching the coil off does not guarantee a safe cylinder: the valve type, spring direction, load and trapped air all affect motion. Isolation alone does not release stored pressure. Only isolation, bleed, zero-pressure verification and lockout together give a state fit for maintenance.

**よくある誤り / Common mistakes**

- 「遮断器をOFFにした」で無電圧確認を省略する。 / Skipping zero-voltage verification because the breaker is off.
- 通電前チェックに「動作確認」を入れる（通電前には動作しない）。 / Including a motion test in the pre-power check.
- 承認者を本人だけにする。 / Self-approval only.
- 空圧の残圧を「配管を外せば抜ける」と扱う。 / Assuming removing a tube releases stored pressure.

**重要な限界 / Important limit:** この表は実機の通電前手順を理解するための机上演習です。本研修では通電も空圧供給も行いません。実機では、電気設備の規格、社内ルール、有資格者、リスクアセスメント、隔離・ロックアウトの手順に従います。 / This is a paper exercise. The course never energises or pressurises; real work follows electrical standards, company rules, qualified persons, risk assessment and isolation procedures.

**許容範囲 / Acceptable range**

6区分すべてに確認内容・合格判断・実施者が入り、無電圧の確認が最初に来ていれば受理します。表現や順序の細部は問いませんが、承認を本人だけにしている答案は減点します。 / All six areas filled with a check, a pass condition and a responsible role, with zero-energy verification first. Wording may vary; self-approval is marked down.
