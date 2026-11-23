# 第8日 学生ワークシート：電気・センサー・PLCラダー / Day 8 Student Worksheet: Electrical, Sensors and PLC Ladder

氏名 / Name: ________________________________　日付 / Date: ____________________

所属・班 / Group: ____________________________　講師 / Instructor: ______________

**推定時間 / Estimated time:** 90分。ノートブックの演習中に下書きし、16:20–16:50の提出時間30分で仕上げます。 / 90 minutes, drafted during the notebook exercises and finished in the 30-minute submission slot.

**対象の原稿 / Source notebooks:** `Day08_01_Electrical_Fundamentals.md`（08-01）、`Day08_02_Sensors_and_IO.md`（08-02）、`Day08_03_Ladder_Sequence.md`（08-03）。シミュレーションは `automation_models.py` の決定論的モデルで、実機のスキャンやタイマー精度は再現しません。 / The simulations are deterministic models; they do not reproduce a real PLC scan or timer.

**安全境界 / Safety boundary:** 本ワークシートは机上演習です。実機の配線、通電、絶縁測定、PLCへの書き込み、強制出力、圧縮空気の供給、シリンダの動作、安全回路の調整、安全機能の検証は行いません。シリンダが動く可能性のある作業は、リスクアセスメント、事前承認、電気的・空圧的隔離、残留エネルギー確認、ガード、有資格者の監督、復旧手順がそろった場合にだけ行います。DC24Vでも短絡・発熱・不意動作の危険はあり、「低電圧だから安全」とは限りません。

This worksheet is a desk exercise. It does not involve real wiring, energisation, insulation testing, PLC downloads, forced outputs, compressed air, cylinder motion, safety-circuit adjustment or safety-function validation. Any task that could move a cylinder requires a risk assessment, prior approval, electrical and pneumatic isolation, stored-energy verification, guarding, qualified supervision and a recovery procedure. Even at DC24V, short circuits, heat and unexpected motion remain hazards; low voltage does not automatically mean safe.

**記入のきまり / How to fill this in**

- 電流・電圧・電力には単位を付け、負荷は「定常」か「突入」かを区別して書きます。 / Give units and distinguish steady-state from inrush values.
- アドレス（X0、Y1など）と物理端子番号は別物として扱います。 / Treat addresses and physical terminal numbers as different things.
- 「シミュレーションで確認した」と「実機で確認した」を混ぜません。本研修で実機の確認は行いません。 / Never mix "verified in simulation" with "verified on hardware". No hardware verification happens in this course.

## T1 電気負荷の計算 / Electrical load calculation

*参照 / Reference: 08-01 §10 負荷電流の計算、セル `load-budget` と `ohms-law`。*

DC24Vで、ランプ（3 W×2個）、センサー（0.06 A×3個）、電磁弁コイル（0.15 A×2個）を同時に使います。ワットで書かれた負荷は、電流に換算してから合計します。

At DC24V, two 3 W lamps, three sensors at 0.06 A and two solenoid coils at 0.15 A operate together. Convert the wattage to current before summing.

| 負荷 / Load | 数量 / Qty | 単位電流の式 / Unit-current formula | 単位電流 / Unit current (A) | 合計 / Total (A) |
|---|---:|---|---:|---:|
| ランプ / lamp（3 W） | 2 | | | |
| センサー / sensor | 3 | | | |
| 電磁弁 / solenoid valve | 2 | | | |
| **定常合計 / steady-state total** | | | | |

- 全負荷の消費電力の合計を計算してください。 / Calculate the total power of all loads. ____________________ W
- 余裕率25 %（仮）を置いた計画電流を計算してください。 / Calculate the planning current with a hypothetical 25 % margin. ____________________ A

検算 / check: 定常合計は **0.73 A** になります。合わない場合は、ワットからアンペアへの換算を見直してください。 / The steady-state total should be **0.73 A**; if not, recheck the watt-to-ampere conversion.

この定常合計が「電源選定の承認」ではない理由を、3つ書いてください。 / Give three reasons why this steady-state total is not approval of a power-supply selection.

______________________________________________________________________________

______________________________________________________________________________

## T2 センサーとNPN/PNPの互換性 / Sensor and NPN/PNP compatibility

*参照 / Reference: 08-02 §4 センサーの種類、§5 NPN・PNPとPLC入力、セル `sensor-compatibility`。*

次の構成は教育用の架空例です。入力共通端子の電位まで含めて電流経路を考え、判定と理由を書いてください。

These are fictional training configurations. Think in a closed circuit that includes the input common, then write the verdict and the reason.

| 構成 / Config | PLC入力 / PLC input | センサー出力 / Sensor output | 判定 / Verdict | 理由 / Reason |
|---|---|---|---|---|
| A | シンク入力、共通0V / sinking, common 0 V | PNP（ソース）/ PNP sourcing | | |
| B | ソース入力、共通+24V / sourcing, common +24 V | NPN（シンク）/ NPN sinking | | |
| C | シンク入力、共通0V / sinking, common 0 V | NPN（シンク）/ NPN sinking | | |
| D | ソース入力、共通+24V / sourcing, common +24 V | PNP（ソース）/ PNP sourcing | | |
| E | 2線式対応入力 / two-wire capable | 2線式 / two-wire | | |

PNPセンサーとシンク入力の組合せについて、電流の向きを順に書いてください。 / Write the current path for a PNP sensor with a sinking input, in order.

+24V → ______________ → ______________ → ______________ → ______________ → 0V

2線式センサーで確認すべき2項目を書いてください。 / Name two things to check for a two-wire sensor.

______________________________________________________________________________

## T3 統一I/O表 / Canonical I/O map

*参照 / Reference: 08-02 §7 統一I/O表、セル `io-table` と `io-validation`。*

Day 8とDay 9で同じI/O表を使います。機器と正常時の状態を埋めて、このコースの唯一の正しい表を再現してください。アドレスは架空の訓練用で、物理端子番号ではありません。

Days 8 and 9 share one I/O map. Fill in the device and normal state to reproduce the single source of truth. The addresses are fictional training assignments, not terminal numbers.

| 種別 / Kind | アドレス / Address | 機器 / Device | 正常時の状態 / Normal state |
|---|---|---|---|
| 入力 / input | X0 | | |
| 入力 / input | X1 | | |
| 入力 / input | X2 | | |
| 入力 / input | X3 | | |
| 内部 / internal | M0 | | |
| 出力 / output | Y0 | | |
| 出力 / output | Y1 | | |
| 出力 / output | Y2 | | |
| タイマー / timer | T0 | | |

- Y1とY2の使い分けを、一文で書いてください。 / Explain the split between Y1 and Y2 in one sentence.
- X1が正常時にONである理由を、物理接点と論理接点の区別を使って書いてください。 / Explain why X1 is ON when healthy, using the difference between a physical and a logical contact.

______________________________________________________________________________

故意に作った誤ったI/O表から、検査が検出する2つの問題を書いてください。 / Name the two problems that the validation cell detects in the deliberately wrong table.

______________________________________________________________________________

## T4 修正した自己保持ラング / Corrected self-holding rung

*参照 / Reference: 08-03 §6 自己保持回路、セル `sim-selfhold`。*

元PDFの自己保持回路には並列の保持接点がなく、STARTを離すと運転状態が消えます。正しいラングを、接点記号とアドレスを使って描いてください。

The source circuit lacks a parallel holding contact, so RUN disappears when START is released. Draw the corrected rung with contact symbols and addresses.

```text
（この枠にラングを描く / draw the rung in this box）



```

| 要素 / Element | アドレス / Address | 直列か並列か / Series or parallel | 役割 / Role |
|---|---|---|---|
| 開始条件 / start condition | | | |
| 開始時の位置条件 / position at start | | | |
| 保持接点 / holding contact | | | |
| 停止許可 / stop permission | | | |
| コイル / coil | | | |

シミュレーションの出力を予想してから、実際の値で確認してください。 / Predict the trace, then confirm with the simulated values.

| 時点 / Step | 状態 / State | RUN | Y0 | Y1 | Y2 | T0 (ms) |
|---|---|---|---|---|---|---|
| 初期 / initial | | | | | | |
| START押下 / pressed | | | | | | |
| STARTを離して+1 / released +1 | | | | | | |
| STARTを離して+2 / released +2 | | | | | | |
| STOPを開く / STOP opened | | | | | | |

- X2を保持枝に入れてはいけない理由を書いてください。 / Why must X2 stay out of the holding branch?

______________________________________________________________________________

## T5 タイマーの境界 / Timer boundary

*参照 / Reference: 08-03 §9.1 タイマーの境界、セル `sim-timer`。*

T0はM0がONの間だけ数えるオン遅延タイマーで、3,000 msでY1を点灯します。境界の前後と、停止時のリセットを確認します。

T0 is an on-delay timer that counts while M0 is ON and turns Y1 on at 3,000 ms. Check both sides of the boundary and the reset.

| 時点 / Point | T0 | Y1 | 状態 / State |
|---|---:|---|---|
| 境界の直前 / just before | 2,999 ms | | |
| 境界 / at the boundary | 3,000 ms | | |
| STOP直後 / after STOP | ______ ms | | |

実機で「3.000秒ちょうど」に点灯するとは限らない理由を、2つ書いてください。 / Give two reasons why a real PLC may not switch at exactly 3.000 s.

______________________________________________________________________________

## T6 シーケンスの状態 / Sequence states

*参照 / Reference: 08-03 §7 状態ベースのシーケンス、セル `sim-sequence` と `sim-faults`。*

出力のON/OFFだけでなく、「いま何をしている状態か」を管理します。各状態の出力と、次へ進む条件を埋めてください。

Manage the state the machine is in, not only output ON/OFF. Fill in the outputs and the transition condition for each state.

| 状態 / State | 出力 / Outputs | 次へ進む条件 / Transition | タイムアウト / Timeout |
|---|---|---|---|
| IDLE | | | — |
| READY | | | — |
| EXTEND | | | — |
| WAIT_EXTENDED | | | |
| RETRACT | | | — |
| WAIT_RETRACTED | | | |
| COMPLETE | | | — |
| FAULT | | | — |

- 正常サイクルの状態の並びを書いてください。 / Write the state sequence of a normal cycle.

IDLE → ______ → ______ → ______ → ______ → ______ → ______

- 「指令」と「確認」の違いを、Y2とX3を使って一文で書いてください。 / Explain command versus confirmation using Y2 and X3.

______________________________________________________________________________

## T7 異常処理と再起動 / Fault handling and restart

*参照 / Reference: 08-03 §8 異常処理・復旧・再起動防止、セル `sim-faults` と `sim-reset`。*

異常の検出、応答、リセット、再起動の条件を書きます。リセットは「動作開始」ではありません。

Write detection, response, reset and restart conditions. Reset is not a start command.

| 異常 / Fault | 検出 / Detection | 応答 / Response | リセット / Reset | 再起動 / Restart |
|---|---|---|---|---|
| F001 前進端未確認 / extend not confirmed | | | | |
| F002 前後端同時ON / both sensors ON | | | | |
| F003 後退端未確認 / retract not confirmed | | | | |
| STOP操作 / stop operated | | | | |
| 停電・復電 / power loss and restore | | | | |
| リセット中のSTART / START held during reset | | | | |

- FAULTからリセットした直後の状態とY2の値を、シミュレーションの観測値で書いてください。 / State the simulated state and Y2 value immediately after a reset from FAULT.

状態 / state: ____________　Y2: ____________　RUN: ____________

- 「保持されているから大丈夫」「保持されていないから大丈夫」の両方が危険な理由を書いてください。 / Why are both "it is retained, so it is fine" and "it is not retained, so it is fine" unsafe?

______________________________________________________________________________

## T8 通電前の確認 / Pre-power verification

*参照 / Reference: 08-02 §9 通電前の確認、演習E。*

通電前には、電気を入れずに配線と状態を確認します。本研修では実際の通電を行わないため、この表は手順を理解するための机上演習です。

Before energising, verify wiring and state without power. This course never energises equipment, so the table is a paper exercise to understand the procedure.

| 区分 / Area | 確認する内容 / What to check | 合格の判断 / Pass condition | 実施者 / By whom |
|---|---|---|---|
| 遮断・無電圧 / isolation and zero energy | | | |
| 図面との照合 / drawing check | | | |
| 定格・極性 / ratings and polarity | | | |
| 導体・端子 / conductors and terminals | | | |
| 安全・立入り / safety and access | | | |
| 承認 / approval | | | |

電磁弁のコイルをOFFにしただけでは、シリンダが安全な状態にならない理由を書いてください。 / Why does de-energising a solenoid coil not make the cylinder safe?

______________________________________________________________________________

## 完了チェックリスト / Completion checklist

- [ ] T1 ランプを電流に換算して合計した / converted the lamps to current and summed
- [ ] T1 定常合計と計画電流を区別した / separated steady-state total from planning current
- [ ] T1 0.73 Aが承認ではない理由を3つ書いた / gave three reasons it is not approval
- [ ] T2 5構成を判定し、入力共通端子まで理由を書いた / judged five configurations including the common
- [ ] T2 2線式の確認項目を書いた / listed the two-wire checks
- [ ] T3 統一I/O表を再現した / reproduced the canonical I/O map
- [ ] T3 Y1を電磁弁に使わず、X1を正常時ONと書いた / kept Y1 off the solenoid and X1 ON when healthy
- [ ] T4 並列の保持接点を入れたラングを描いた / drew the rung with a parallel holding contact
- [ ] T4 X2を保持枝に入れない理由を書いた / explained why X2 is not in the holding branch
- [ ] T5 2,999 msと3,000 msを区別した / distinguished 2,999 ms and 3,000 ms
- [ ] T6 8状態の出力と遷移条件を書いた / wrote outputs and transitions for eight states
- [ ] T7 リセット後に動作しないことを確認した / confirmed no motion after reset
- [ ] T8 無電圧・図面・定格・導体・安全・承認の順で書いた / ordered the checks correctly
- [ ] 実機の配線・通電・書込み・空圧・動作を行っていない / did not wire, energise, download, pressurise or move real equipment
