# 第8日 学生ワークシート / Day 8 Student Worksheet

氏名 / Name: ______________________________　日付 / Date: __________________

所属・班 / Group: __________________________　講師 / Instructor: ____________

**推定時間 / Estimated time:** 60分。演習中に下書きし、最後の30分で仕上げます。 / 60 minutes; draft during the exercises and finish in the final 30 minutes.

**対象の原稿 / Source notebooks:** `Day08_01_Electrical_Fundamentals.md`、`Day08_02_Sensors_and_IO.md`、`Day08_03_Ladder_Sequence.md`。

**安全境界 / Safety boundary.** 机上の演習です。実際の盤への配線・通電・絶縁測定・保護機器の選定は行いません。 / A desk exercise. No real panel wiring, energisation, insulation testing or protective-device selection.

## T1 センサーとPLC入力 / sensor and PLC input

*参照 / Reference: 08-02 §7–§8。*

条件 / conditions: 3線式の**NPN**出力センサー、PLC入力の共通端子は**0V**。

| # | 問い / Question | 答え / Answer |
|---|---|---|
| 1 | この組み合わせは適合するか / is it compatible? | |
| 2 | 適合しない理由 / why not? | |
| 3 | 適合させる方法を2つ / two ways to make it work | |

4. PNPのときの電流経路を書いてください（+24Vから0Vまで）。 / Write the PNP current path from +24V to 0V.

____________________________________________________________________________

## T2 電力の計算 / electrical power

*参照 / Reference: 08-01 §7。*

条件 / conditions: DC24V。PLC 0.30 A、センサー 0.02 A × 3個、電磁弁 0.12 A × 2個、表示灯 0.04 A × 1個。

| # | 問い / Question | 式と計算 / Working | 答え / Answer |
|---|---|---|---|
| 1 | 合計電流 / total current | | |
| 2 | 合計電力 / total power | | |
| 3 | 計画電流（余裕20%、教材の仮定）/ planning current | | |

4. この合計だけで電源を選べない理由を1つ書いてください。 / Give one reason why the total alone cannot select a power supply.

____________________________________________________________________________

## T3 ラダーの読取り / reading ladder logic

*参照 / Reference: 08-03 §7–§9。*

条件 / conditions: `M0 = X1 AND (X0 OR M0)`、`Y2 = M0 AND X4 AND NOT X3`。

| # | 問い / Question | 答え / Answer |
|---|---|---|
| 1 | START（X0）を離してもRUNが続く理由 / why RUN stays on after X0 is released | |
| 2 | STOP許可（X1）がOFFになったとき / what happens when X1 goes OFF | |
| 3 | Y2がONになる条件 / when is Y2 ON | |
| 4 | 基本回路に足りない再起動防止の要素を2つ / two missing restart-prevention elements | |

5. 前進と後退を同時に要求したとき、教材の設計ではどうなるか。理由も書いてください。 / What happens when forward and reverse are requested together in the teaching design, and why?

____________________________________________________________________________

## 提出前チェック / before submitting

- [ ] 単位を書いた / units given
- [ ] 電流の向きを矢印で書いた / current direction drawn
- [ ] 「安全機能ではない」と区別した / safety distinguished from ordinary control
