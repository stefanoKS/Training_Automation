# 第8日 解答例 / Day 8 Answer Key

> 数値と論理は独立に確認しています。複数の正解がある場合は条件を添えています。
> Numbers and logic were checked independently. Where several answers are valid, the conditions are stated.

## T1 センサーとPLC入力 / sensor and PLC input

1. **適合しない。 / Not compatible.** NPN出力は0Vへ電流を引き込む。入力共通が0Vのシンク入力は、+側から電流を供給するPNP出力を前提とする。 / An NPN output sinks current to 0V. A sinking input with a 0V common expects a PNP output that sources current.

2. 電流の経路が成立しない（+24V → PLC入力 → センサー → 0V の形にならない）。 / The conventional current path cannot be completed.

3. 方法の例 / example remedies:
   - 入力共通を+24Vにする（ソース入力）。 / Move the input common to +24V (sourcing input).
   - PNP出力のセンサーに変える。 / Use a PNP-output sensor.
   - 双方向入力・設定変更できる入力を、マニュアルに従って使う。 / Use a bidirectional or configurable input per the manual.
   - 適合するインターフェース（リレー等）を介する。 / Insert a compatible interface.

4. PNPの経路 / PNP path: **+24V → PNPセンサー出力 → PLC入力回路 → 0V（共通）**。

**採点上の注意 / marking note:** 「PLC全体がNPNだから」という理由は誤り。入力モジュールと共通端子の配線で決まる。 / "The whole PLC is NPN" is wrong; the input module and common wiring decide.

## T2 電力の計算 / electrical power

| # | 式 / Formula | 計算 / Working | 答え / Answer |
|---|---|---|---|
| 1 | 合計 / total | 0.30 + 3×0.02 + 2×0.12 + 0.04 | **0.60 A** |
| 2 | V × I | 24 × 0.60 | **14.4 W** |
| 3 | 合計 × 1.20 | 0.60 × 1.20 | **0.72 A** |

4. 解答例 / example: 突入電流、同時に動く負荷、周囲温度による定格低下、将来の増設、出力特性、配線と保護機器の要件を確認していない。 / Inrush, simultaneous loads, temperature derating, future expansion, output characteristics and wiring/protective-device requirements have not been checked.

**採点上の注意 / marking note:** 0.72 A は「教材の仮定」による計画値であり、選定の承認ではない。 / 0.72 A is a planning value under a training assumption, not a sizing approval.

## T3 ラダーの読取り / reading ladder logic

1. M0のコイルと並列に、M0自身のNO接点があるため。M0がONになると自分の接点が閉じ、X0が開いても論理が成立し続ける（自己保持）。 / An NO contact of M0 is in parallel with the START branch, so the logic stays true after X0 opens.

2. M0がOFFになり、Y0とY2もOFFになる。 / M0 goes OFF, so Y0 and Y2 go OFF.

3. 運転中（M0）で、製品があり（X4）、前進端でない（X3がOFF）。 / While running, with a product present and not at the extended end.

4. 例 / examples: STARTが離れたことの確認（アーム）、立ち上がり検出、STOP優先、起動位置の確認、リセットと起動の分離。 / Start arming, edge detection, STOP precedence, starting-position confirmation, separating reset from start.

5. **両方OFF（競合として拒否）。** 相互に打ち消すだけの回路はスキャン順に依存するため、教材では同時要求を決定的に拒否する設計にしている。実機の反転接触器は電気的・機械的インターロックも必要で、ソフトのインターロックは安全定格のガードではない。 / **Both OFF, treated as a conflict.** A merely cross-linked circuit depends on scan order, so the teaching design rejects simultaneous requests deterministically. Real reversing contactors also need electrical and mechanical interlocking, and software interlocks are not safety-rated guarding.

## 数値の再現方法 / how to reproduce

```text
total   = 0.30 + 3*0.02 + 2*0.12 + 0.04 = 0.60 A
power   = 24*0.60                        = 14.4 W
planned = 0.60*1.20                      = 0.72 A
```
