# 第8日 01 電気の基礎と DC24V 制御 / Day 8-01 Electrical Fundamentals and DC24V Control

> 所要時間 / Duration: **80分 / 80 minutes**
> 元資料 / Source pages: 21–23
> 共通題材 / Running example: 小型ワーク押出し装置 / small workpiece-pushing machine

## 1. 概要 / Overview

このノートブックでは、電圧・電流・抵抗・電力の意味を、物理的なイメージから始めて、DC24V制御盤の設計につなげます。中心になる問いは、次の3つです。

This notebook starts from the physical meaning of voltage, current, resistance and power, then connects them to a DC24V control panel. Three questions are central.

1. 機器が必要とする電圧と電流は何か。
2. 電源は、その電流を余裕をもって供給できるか。
3. PLCの出力は、その負荷を直接駆動できるか。

1. What voltage and current does each device need?
2. Can the power supply deliver that current with margin?
3. Can the PLC output drive that load directly?

**安全に関する前提 / Safety boundary**

電気は、正しく扱わなければ感電・短絡・発熱・火災・不意動作の原因になります。本研修は教育用で、実機の配線・通電・絶縁測定・保護装置の選定を行いません。実作業は、電気設備の規格、社内ルール、有資格者、リスクアセスメント、遮断・無電圧確認・ロックアウトの手順に従ってください。

Electricity can cause shock, short circuits, heat, fire and unexpected motion. This is a training course; it does not cover real wiring, energisation, insulation testing or protective-device selection. Real work follows electrical standards, company rules, qualified persons, risk assessment and isolation/lockout procedures.

## 2. 学習目標 / Learning objectives

1. 電圧・電流・抵抗・電力を、単位とともに説明できる。
2. オームの法則 V = IR を使える。
3. 直流電力 P = VI を計算できる。
4. DCとACの違いを説明できる。
5. DC24V制御の役割を説明できる。
6. 負荷の定常電流を合計できる。
7. 電源選定前に確認する項目を列挙できる。
8. スイッチ・リレー・ランプの役割を区別できる。
9. PLC出力と負荷の関係を説明できる。
10. ヒューズ・遮断器・接地・絶縁の目的を説明できる。
11. 「制御信号」と「負荷へ届ける電力」を区別できる。
12. 0.73 Aの負荷例を計算し、電源選定の承認と混同しない。

By the end of this notebook you can:

1. Explain voltage, current, resistance and power with units.
2. Use Ohm's law, V = IR.
3. Calculate DC power, P = VI.
4. Explain the difference between DC and AC.
5. Explain the role of DC24V control.
6. Sum the steady-state current of loads.
7. List the checks required before selecting a power supply.
8. Distinguish switches, relays and indicator lamps.
9. Explain the relation between a PLC output and its load.
10. Explain the purpose of fuses, breakers, earthing and insulation.
11. Distinguish a control signal from the power delivered to a load.
12. Calculate the 0.73 A load example without treating it as approval of a power-supply design.

## 3. 前提知識 / Prerequisites

第7日を終えていること。特に、電磁弁・センサー・ランプが「負荷」であり、PLCが「信号」を出す装置であることを確認してください。電気の専門知識は前提にしません。

Complete Day 7. In particular, confirm that solenoid valves, sensors and lamps are loads and that the PLC produces signals. No prior electrical expertise is assumed.

### 実行環境 / executable environment

このノートのコードは、リポジトリ内の `day07_09_support/examples/automation_models.py` を使います。最初のセルを実行してから、後のセルを順に実行してください。インターネット接続は不要です。

The code uses `day07_09_support/examples/automation_models.py` in this repository. Run the first cell, then the following cells in order. No internet connection is required.

```python exec id="setup"
import sys, pathlib
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["Meiryo", "Yu Gothic", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

def find_support(start):
    for base in [start, *start.parents]:
        if (base / "day07_09_support" / "examples" / "automation_models.py").is_file():
            return base / "day07_09_support"
    raise FileNotFoundError("Open this notebook inside the Training_Automation repository.")

SUPPORT = find_support(pathlib.Path.cwd())
sys.path.insert(0, str(SUPPORT / "examples"))
import automation_models as am
print("automation_models loaded from", SUPPORT.name)
print("No internet, hardware, PLC software or compressed air is used.")
```

**期待される出力 / Expected output**

```text
automation_models loaded from day07_09_support
No internet, hardware, PLC software or compressed air is used.
```

## 4. 電圧・電流・抵抗・電力 / Voltage, current, resistance and power

**電圧 / voltage** は「電位差」です。高い電位と低い電位の差が、電荷を動かす力になります。単位は V（ボルト）。

**Voltage** is a potential difference. The difference between a higher and a lower potential drives charge. The unit is the volt (V).

**電流 / current** は「流れる電気の量」です。単位は A（アンペア）。電気の流れは、1秒間に断面を通過する電荷の量で表します。

**Current** is the amount of charge flowing. The unit is the ampere (A), the charge passing a cross-section per second.

**抵抗 / resistance** は「電流の流れにくさ」です。単位は Ω（オーム）。抵抗が大きいほど、同じ電圧では電流が小さくなります。

**Resistance** is opposition to current flow. The unit is the ohm (Ω). A larger resistance gives less current at the same voltage.

**電力 / power** は「単位時間当たりのエネルギー」です。単位は W（ワット）。電気がする仕事の速さです。

**Power** is energy per unit time. The unit is the watt (W), the rate at which electrical energy is transferred.

![電圧・電流・抵抗のアナロジー / voltage, current and resistance analogy](../../assets/diagrams/day08/D08-01.svg)

*図 D08-01：水路のアナロジーです。水位差＝電圧、流量＝電流、管の狭さ＝抵抗に対応します。ただし、アナロジーはすべての電気現象を表すものではありません。 / Figure D08-01: a water analogy. Head difference = voltage, flow = current, pipe restriction = resistance. The analogy does not represent every electrical effect.*

| 量 / Quantity | 記号 / Symbol | 単位 / Unit | 物理的な意味 / Physical meaning |
|---|---|---|---|
| 電圧 / voltage | V | ボルト / volt (V) | 電位差 / potential difference |
| 電流 / current | I | アンペア / ampere (A) | 電荷の流れ / flow of charge |
| 抵抗 / resistance | R | オーム / ohm (Ω) | 流れにくさ / opposition to flow |
| 電力 / power | P | ワット / watt (W) | エネルギー移動の速さ / rate of energy transfer |

**アナロジーの限界 / Limits of the analogy**

水路のアナロジーは直感的ですが、次の点は異なります。

- 電流は1本の管の水のように「減る」のではなく、回路を流れて戻ります。
- 電圧は「高さ」ではなく、2点間の差です。
- 交流では向きと大きさが時間で変わります。
- コイルやコンデンサは、時間遅れや逆起電力を生みます。

The water analogy is intuitive but differs in important ways: current flows in a closed loop; voltage is a difference between two points; AC changes direction and magnitude with time; coils and capacitors introduce delay and back-EMF.

## 5. オームの法則と電力 / Ohm's law and power

**オームの法則 / Ohm's law**

```text
V = I × R
I = V / R
R = V / I
```

**直流電力 / DC power**

```text
P = V × I
P = I² × R
P = V² / R
```

- **V**: 電圧 [V] / voltage
- **I**: 電流 [A] / current
- **R**: 抵抗 [Ω] / resistance
- **P**: 電力 [W] / power

**例：DC24V・6Wランプ / example: a 6 W lamp at DC24V**

```text
I = P / V = 6 / 24 = 0.25 A
```

3個なら、定常電流の合計は 0.25 × 3 = **0.75 A** です。ただし、ランプの突入電流、温度による抵抗変化、同時動作、電源の余裕は別に確認します。

For three lamps the steady-state total is 0.75 A. Inrush current, temperature dependence, simultaneous operation and supply margin must still be checked.

**DCとAC / DC and AC**

| 項目 / Item | DC（直流）/ direct current | AC（交流）/ alternating current |
|---|---|---|
| 向き / direction | 一定 / constant | 周期的に変化 / changes periodically |
| 例 / example | DC24V制御、バッテリー / 24 V control, battery | 工場の動力、AC100/200V / factory power |
| 注意 / caution | 極性、短絡、誘導負荷 / polarity, short circuit, inductive load | 周波数、力率、感電、遮断 / frequency, power factor, shock, isolation |

本研修の制御はDC24Vを前提にします。AC動力回路の設計・施工は、有資格者と社内ルールの範囲です。

This course assumes DC24V control. AC power circuits are outside the scope and require qualified persons and company rules.

## 6. DC24V制御と電源 / DC24V control and power supply

DC24Vは、PLC、センサー、リレー、表示灯、電磁弁などで広く使われます。しかし、24Vでも短絡・発熱・不意動作の危険はあります。「低電圧だから安全」とは限りません。

DC24V is widely used for PLCs, sensors, relays, lamps and solenoid valves. Even at 24 V, short circuits, heat and unexpected motion are hazards. "Low voltage" does not automatically mean "safe".

![DC24Vの電力供給と保護 / DC24V distribution and protection](../../assets/diagrams/day08/D08-02.svg)

*図 D08-02：電源、保護、分岐、負荷の関係を示します。実際の遮断器・ヒューズ・端子台の選定は、定格・遮断容量・電線保護・選択協調を確認して行います。 / Figure D08-02: the relation between supply, protection, branches and loads. Real breaker/fuse selection requires ratings, breaking capacity, wire protection and coordination.*

**電源を選ぶ前に確認すること / Check before selecting a supply**

| 確認項目 / Check | 内容 / Detail |
|---|---|
| 入力電圧 / input voltage | AC100V？AC200V？単相/三相？ / what is available? |
| 出力電圧 / output voltage | DC24Vの許容範囲 / regulation range |
| 定格電流 / rated current | 連続で出せる電流 / continuous output |
| 突入電流 / inrush | ランプ・モーター・コンデンサ / lamps, motors, capacitors |
| 負荷の同時動作 / simultaneity | 全負荷が同時にONか / all loads at once? |
| 周囲温度 / ambient temperature | 高温では定格が下がる / derating |
| 設置方法 / mounting | 密閉盤、通風、隣接機器 / enclosure, ventilation |
| 保護 / protection | 短絡・過電流・過電圧 / short circuit, overcurrent, overvoltage |
| 電線・端子 / wiring and terminals | 許容電流、端子定格 / ampacity and terminal rating |
| 接地・絶縁 / earthing and insulation | 保護接地、SELV/PELV、絶縁 / PE, SELV/PELV, insulation |

**電源容量の考え方 / Sizing logic**

1. 負荷ごとの定常電流を求める。
2. 同時に使う負荷を合計する。
3. 突入電流と時間を確認する。
4. 周囲温度・設置条件による定格低下を確認する。
5. 電線・端子・保護装置の定格を確認する。
6. 将来拡張と保守の余裕を、根拠を明示して加える。
7. メーカーの電源マニュアルで最終確認する。

1. Find the steady current of each load.
2. Sum the loads that operate simultaneously.
3. Check inrush current and duration.
4. Check derating for ambient temperature and mounting.
5. Check wire, terminal and protective-device ratings.
6. Add margin for future expansion and maintenance with a stated basis.
7. Confirm in the supply manufacturer's manual.

> **重要 / Important**: 余裕率は、機器仕様・将来拡張・運用条件から決めます。「25%にすればよい」という万能の値はありません。本教材の25%は計算例です。
> Margin comes from device specifications, future expansion and operating conditions. There is no universal "25% is correct". The 25% in this course is a worked example.

## 7. スイッチ・リレー・ランプ / Switches, relays and lamps

**スイッチ / switch** は、回路を開閉して信号や電力を切り替えます。**リレー / relay** は、コイルに電流を流すと電磁力で接点を切り替える部品です。小さな制御信号で、より大きな負荷を間接的に扱えます。**ランプ / indicator lamp** は、状態を人に知らせます。

A **switch** opens or closes a circuit. A **relay** uses an electromagnetic coil to change contacts, allowing a small control signal to switch a larger load. An **indicator lamp** communicates state to a person.

![スイッチとリレーの違い / switch versus relay](../../assets/diagrams/day08/D08-03.svg)

*図 D08-03：スイッチは人が直接操作する接点、リレーはコイルの励磁で接点を動かします。どちらも接点定格と負荷種別を確認します。 / Figure D08-03: a switch is operated directly by a person; a relay moves contacts via an energised coil. Both require contact ratings and load-type checks.*

**NOとNC / normally open and normally closed**

- **NO（Normally Open）**: 通常は開。操作すると閉じる。
- **NC（Normally Closed）**: 通常は閉。操作すると開く。

- **NO**: normally open; closes when operated.
- **NC**: normally closed; opens when operated.

**物理接点と論理接点は別 / physical contacts are not logical contacts**

物理的なNC接点は、通常時に導通しています。PLCのプログラムでは、その入力を「論理的にどう扱うか」を別に決めます。物理NCだからといって、ラダーで必ずNC命令を使うわけではありません。実際の入力状態（ON/OFF）を確認して論理を組み立てます。

A physical NC contact conducts in its normal state. The PLC program separately decides how to evaluate that input. A physical NC device does not automatically mean an NC instruction in the ladder; build the logic from the actual ON/OFF state.

**停止入力にNCを使う理由と限界 / why NC is used for stop inputs, and its limits**

停止入力にNCを使うと、配線断線時に「停止側」と見なせる場合があります。ただし、断線検知の能力や本質的安全性は、回路全体の設計に依存します。非常停止は、リスク評価に基づく安全関連設計が必要で、通常のNCスイッチを付ければ足りるものではありません。

An NC stop input can sometimes be arranged so that a broken wire looks like a stop request. However, fault detection and intrinsic safety depend on the whole circuit. Emergency stopping requires a safety-related design based on risk assessment; adding an ordinary NC switch is not sufficient.

## 8. PLC出力と負荷 / PLC outputs and loads

PLCは、プログラムで決めた信号を出力します。しかし、出力端子には電圧・電流の定格があり、すべての負荷を直接駆動できるわけではありません。

A PLC outputs the signal decided by its program. But each output terminal has voltage and current ratings; not every load can be driven directly.

![PLCから負荷までの構成 / PLC-to-load architecture](../../assets/diagrams/day08/D08-04.svg)

*図 D08-04：PLC出力は「信号」であり、負荷に電力を届ける経路は別にあります。リレー出力とトランジスタ出力では、使える負荷と配線が違います。 / Figure D08-04: the PLC output is a signal; the path that delivers power to the load is separate. Relay and transistor outputs support different loads and wiring.*

| 負荷 / Load | 主な仕様 / Main specification | 追加で確認 / Also check |
|---|---|---|
| 表示灯 / indicator lamp | 電圧、消費電流 / voltage, current | 極性、輝度、点灯条件 / polarity, brightness, condition |
| 電磁弁 / solenoid valve | コイル電圧、W、応答時間 / coil voltage, power, response | サージ対策、無通電時の弁位置 / suppression, de-energised position |
| リレーコイル / relay coil | コイル電圧、消費電力 / coil voltage, power | 逆起電力対策、接点側定格 / back-EMF, contact rating |
| モータードライバ / motor driver | 制御入力方式、必要電源 / control input, supply | インターフェース、安全回路 / interface, safety circuit |

**リレー出力とトランジスタ出力 / relay versus transistor output**

| 項目 / Item | リレー出力 / relay output | トランジスタ出力 / transistor output |
|---|---|---|
| 接点 / contact | 機械接点 / mechanical contact | 半導体 / semiconductor |
| 負荷 / load | AC・DCの広い負荷 / wide AC/DC load | DC負荷が中心 / mainly DC |
| 寿命 / life | 接点寿命に依存 / contact life | 半導体寿命、過電流に注意 / semiconductor life, overcurrent |
| 応答 / response | 比較的遅い / relatively slow | 速い / fast |
| 極性 / polarity | 比較的自由 / relatively flexible | シンク/ソースの向きに注意 / sink/source |
| 漏れ電流 / leakage | 小さい / low | OFF時の漏れに注意 / off-state leakage |

**出力容量の確認 / checking output capacity**

- 1点当たりの最大電流 / maximum current per point
- 共通端子当たりの最大電流 / maximum current per common terminal
- 同時ONする点数 / number of points ON together
- 突入電流とサージ / inrush and surge
- 誘導性負荷のサージ吸収 / inductive-load suppression
- 出力素子の保護 / output protection

> PLC出力を「無制限の電源」と考えてはいけません。出力定格を超えると、誤動作・破損・発熱の原因になります。負荷が大きい場合は、リレーやコンタクタを介します。
> Do not treat a PLC output as an unrestricted power supply. Exceeding its rating causes malfunction, damage or heat. Use a relay or contactor for larger loads.

### 電源容量の計画値を感度で見る / sensitivity of the planning current

次のセルは、同じ0.73 Aの定常負荷に対して、余裕率を変えた計画値を示します。余裕率は設計判断であり、この表の値をそのまま採用するものではありません。

The next cell shows planning values for the same 0.73 A steady load at different margins. The margin is a design decision; do not adopt these values directly.

```python exec id="supply-margin"
steady = 0.73
print(f"steady-state load: {steady:.2f} A")
print(f"{'margin':>8} {'planning current [A]':>22}")
for margin in (0.0, 0.10, 0.25, 0.50, 1.00):
    planning = steady * (1 + margin)
    print(f"{margin:>8.0%} {planning:>22.2f}")
print("\nMargin must come from device specifications, future expansion and operating conditions.")
print("This table is not a power-supply selection or an approval.")
```

**期待される出力 / Expected output**

```text
steady-state load: 0.73 A
  margin   planning current [A]
      0%                   0.73
     10%                   0.80
     25%                   0.91
     50%                   1.09
    100%                   1.46

Margin must come from device specifications, future expansion and operating conditions.
This table is not a power-supply selection or an approval.
```

## 9. 保護・接地・絶縁 / Protection, earthing and isolation

**ヒューズ・遮断器 / fuse and circuit breaker**

ヒューズや遮断器は、主に**電線と機器を過電流から守る**ためのものです。人の感電を防ぐ装置ではありません。定格電圧・定格電流・遮断容量・電線保護・選択協調を確認します。

Fuses and breakers primarily **protect wiring and equipment from overcurrent**. They are not a device for preventing electric shock. Check voltage rating, current rating, breaking capacity, wire protection and coordination.

**接地と保護接地 / earthing and protective earth**

保護接地（PE）は、故障時に金属製の筐体などが危険な電位にならないようにするための重要な手段です。接地の方法は、設備の電気規格と社内ルールに従います。

Protective earthing (PE) is an important measure to prevent metal enclosures from reaching a hazardous potential under fault conditions. Earthing practice follows electrical standards and company rules.

**絶縁・遮断・無電圧確認 / insulation, isolation and verification of de-energisation**

配線を変更するときは、その場所に電気が来ていないことを確実にします。遮断器をOFFにした「つもり」で作業せず、設備の構造、別電源、バックフィード、蓄電部を確認します。必要に応じて、検電、無電圧確認、ロックアウト・タグアウトを行います。

Before changing wiring, make sure the location is de-energised. Do not rely on "I think the breaker is off". Check the equipment structure, alternative supplies, backfeed and stored energy. Use voltage verification, lockout and tagout as required.

**制御信号と電力の区別 / control signal versus delivered power**

| 概念 / Concept | 例 / Example | 役割 / Role |
|---|---|---|
| 制御信号 / control signal | PLCのY出力、センサー入力 / PLC Y output, sensor input | 状態を伝える / communicate state |
| 負荷への電力 / power to load | DC24V電源から電磁弁への電流 / supply current to a valve | エネルギーを供給 / deliver energy |
| 間接操作 / indirect operation | PLC出力→リレー→モーター / PLC → relay → motor | 大きい負荷を扱う / handle a larger load |

## 10. 負荷電流の計算 / Load current calculation

PDFの例を確認します。DC24Vのランプ（3W×2個）、センサー（0.06A×3個）、電磁弁コイル（0.15A×2個）を同時使用した場合の定常電流を求めます。

Check the PDF example: at DC24V, two 3 W lamps, three sensors at 0.06 A each and two solenoid valve coils at 0.15 A each, all simultaneous. Find the steady-state total current.

```python exec id="load-budget"
loads = am.pdf_electrical_example()
report = am.load_report(loads, supply_margin=0.25)

print(f"{'load':<20} {'qty':>4} {'unit [A]':>10} {'total [A]':>10}")
for row in report["rows"]:
    print(f"{row['name']:<20} {row['quantity']:>4} {row['unit_current_a']:>10.3f} {row['total_current_a']:>10.3f}")
print(f"\nsteady-state total : {report['steady_total_a']:.2f} A")
print(f"planning margin    : {report['margin_fraction']:.0%}")
print(f"planning current   : {report['planning_current_a']:.2f} A")
print(f"is sizing approval : {report['is_sizing_approval']}")
print("This is a steady-state sum, not a power-supply selection or approval.")
```

**期待される出力 / Expected output**

```text
load                  qty   unit [A]  total [A]
lamp                    2      0.125      0.250
sensor                  3      0.060      0.180
solenoid valve          2      0.150      0.300

steady-state total : 0.73 A
planning margin    : 25%
planning current   : 0.91 A
is sizing approval : False
This is a steady-state sum, not a power-supply selection or approval.
```

**この結果の読み方 / How to read the result**

- 0.73 Aは、**定常状態の合計**です。
- ランプの突入電流、電磁弁のサージ、同時ONの条件、周囲温度による電源の定格低下は含みません。
- 0.91 Aは、25%の余裕を仮に置いた**計画値**です。承認された電源容量ではありません。
- 電線の許容電流、端子の定格、ヒューズ・遮断器の定格、電源の出力定格を別に確認します。

- 0.73 A is the **steady-state sum**.
- It excludes lamp inrush, valve surge, simultaneity assumptions and supply derating with ambient temperature.
- 0.91 A is a **planning value** with a hypothetical 25% margin, not an approved supply rating.
- Wire ampacity, terminal ratings, fuse/breaker ratings and supply output ratings require separate checks.

```python exec id="ohms-law"
# DC24V・6Wランプの例 / 6 W lamp at DC24V
voltage_v = 24.0
lamp_power_w = 6.0
lamp_current_a = lamp_power_w / voltage_v
lamp_resistance_ohm = voltage_v / lamp_current_a
print(f"one lamp current     : {lamp_current_a:.3f} A")
print(f"one lamp resistance  : {lamp_resistance_ohm:.2f} ohm (at this operating point)")
print(f"three lamps current  : {lamp_current_a * 3:.3f} A")
print(f"three lamps power    : {lamp_power_w * 3:.1f} W")

# 電線の電圧降下の概算 / rough voltage drop, copper conductor
length_m = 10.0          # 片道 / one way
current_a = 0.73
area_mm2 = 0.75
resistivity = 0.0175     # ohm*mm2/m, copper, 20 C, teaching value
resistance = resistivity * (2 * length_m) / area_mm2
drop_v = current_a * resistance
print(f"\nloop resistance      : {resistance:.3f} ohm")
print(f"voltage drop         : {drop_v:.3f} V")
print(f"voltage at load      : {voltage_v - drop_v:.3f} V")
print("Rough estimate only: includes no connector, fuse or temperature correction.")
```

**期待される出力 / Expected output**

```text
one lamp current     : 0.250 A
one lamp resistance  : 96.00 ohm (at this operating point)
three lamps current  : 0.750 A
three lamps power    : 18.0 W

loop resistance      : 0.467 ohm
voltage drop         : 0.341 V
voltage at load      : 23.659 V
Rough estimate only: includes no connector, fuse or temperature correction.
```

**注意 / Caution**: ランプの抵抗は温度で変わります。上の96Ωは、6W・24Vの動作点での概算です。コイルや電子機器は、単純な抵抗として扱えません。
> Lamp resistance changes with temperature. The 96 Ω is an estimate at the 6 W, 24 V operating point. Coils and electronic devices are not simple resistors.

## 11. 演習 / Exercises

### 演習 A：オームの法則 / Exercise A: Ohm's law

DC24Vで0.25 Aが流れる負荷の抵抗を求めてください。次に、同じ負荷をDC12Vで使った場合の電流を求めてください。ただし、負荷を単純な抵抗と仮定します。

Find the resistance of a load that draws 0.25 A at DC24V. Then find the current at DC12V, assuming a simple resistance.

### 演習 B：電力 / Exercise B: power

DC24V・0.15 Aの電磁弁コイルの消費電力を求めてください。2個同時に使う場合の合計電力も求めてください。

Find the power of a solenoid coil at DC24V and 0.15 A, and the total for two coils.

### 演習 C：負荷合計 / Exercise C: load total

次の負荷の定常電流合計を求めてください。

Find the steady-state total current.

| 負荷 / Load | 数量 / Qty | 電圧 / Voltage | 電流または電力 / Current or power |
|---|---|---|---|
| ランプ / lamp | 2 | 24 V | 3 W each |
| センサー / sensor | 3 | 24 V | 0.06 A each |
| 電磁弁 / valve | 2 | 24 V | 0.15 A each |

### 演習 D：電源選定前の確認 / Exercise D: checks before supply selection

上の合計0.73 Aを使って、電源を選ぶ前に確認すべき項目を5つ以上書いてください。「0.73 Aより大きい電源を選ぶ」だけでは不十分です。

Using the 0.73 A total, list at least five checks before selecting a supply. "Choose a supply above 0.73 A" is not sufficient.

### 演習 E：信号と電力 / Exercise E: signal and power

「PLCのY出力で電磁弁を動かす」構成について、制御信号と負荷への電力の経路を分けて説明してください。PLC出力の定格を超える場合、どのような方法が考えられますか。

For "the PLC Y output drives a solenoid valve", explain the control-signal path separately from the power path. What can be done if the load exceeds the PLC output rating?

**提出物 / Deliverables**

1. 負荷電流の計算書 / load-current calculation
2. 電源選定前に確認すべき項目5つ以上 / at least five checks before supply selection
3. 電圧降下の概算と仮定 / voltage-drop estimate and assumptions
4. 信号と電力の経路図 / signal and power path sketch
5. スイッチ・リレー・ランプの役割表 / roles of switch, relay and lamp

## 12. 期待される結果 / Expected result

- 電圧・電流・抵抗・電力の単位と意味を説明できる。
- V = IR と P = VI を使える。
- DC24Vの6Wランプが0.25 Aであることを計算できる。
- 3W×2、0.06A×3、0.15A×2の合計が **0.73 A** であることを計算できる。
- 0.73 Aが定常電流の合計であり、電源選定の承認ではないと説明できる。
- 突入電流、定格低下、電線、端子、保護装置を別に確認すべきと説明できる。
- 制御信号と負荷への電力を区別できる。

- You can explain the units and meaning of voltage, current, resistance and power.
- You can use V = IR and P = VI.
- You can calculate 0.25 A for a 6 W lamp at DC24V.
- You can calculate the **0.73 A** total for 3 W × 2, 0.06 A × 3 and 0.15 A × 2.
- You can explain that 0.73 A is a steady-state sum, not approval of a power-supply selection.
- You can explain that inrush, derating, wiring, terminals and protection require separate checks.
- You can distinguish a control signal from the power delivered to a load.

## 13. トラブルシューティング / Troubleshooting

| 症状 / Symptom | 確認すること / Check | よくある原因 / Typical cause |
|---|---|---|
| ランプが暗い / lamp is dim | 電圧、電線の電圧降下、接点 / voltage, drop, contacts | 電源電圧不足、配線抵抗 / low supply, wiring resistance |
| 電源が過負荷になる / supply overloads | 同時動作、突入電流、定格低下 / simultaneity, inrush, derating | 定常電流だけで選定 / selecting on steady current only |
| 電磁弁が動かない / valve does not move | コイル電圧、極性、出力定格 / coil voltage, polarity, output rating | PLC出力容量不足、配線 / insufficient output, wiring |
| ヒューズが切れる / fuse blows | 短絡、突入、定格 / short, inrush, rating | 配線ミス、サージ / wiring error, surge |
| 出力が壊れる / output damaged | 誘導性負荷、サージ、共通電流 / inductive load, surge, common current | サージ対策なし、定格超過 / no suppression, over rating |

## 14. まとめ / Summary

- 電圧は電位差、電流は電荷の流れ、抵抗は流れにくさ、電力はエネルギーの移動速度。
- V = IR、P = VI が基本。ただし負荷は単純な抵抗とは限らない。
- DC24Vは制御で広く使われるが、短絡・発熱・不意動作の危険は残る。
- 負荷電流は合計できるが、突入電流・定格低下・電線・端子・保護を別に確認する。
- 0.73 Aは定常合計であり、電源選定の承認ではない。
- スイッチは直接操作、リレーはコイルで接点を操作、ランプは状態表示。
- PLC出力は信号であり、無制限の電源ではない。
- ヒューズ・遮断器は主に電線と機器を守る。接地・絶縁・遮断・無電圧確認は別の対策。
- 制御信号と負荷への電力を区別する。

- Voltage is a potential difference; current is charge flow; resistance opposes flow; power is the rate of energy transfer.
- V = IR and P = VI are basic, but loads are not always simple resistors.
- DC24V is common for control, but short circuits, heat and unexpected motion remain hazards.
- Load currents can be summed, but inrush, derating, wiring, terminals and protection need separate checks.
- 0.73 A is a steady-state sum, not approval of a supply selection.
- A switch is operated directly; a relay uses a coil; a lamp indicates state.
- A PLC output is a signal, not an unrestricted supply.
- Fuses and breakers mainly protect wiring and equipment. Earthing, insulation, isolation and de-energisation verification are separate measures.
- Distinguish the control signal from the power delivered to the load.

## 15. 完了チェックリスト / Completion checklist

- [ ] 電圧・電流・抵抗・電力の単位を書いた / wrote the units of voltage, current, resistance and power
- [ ] V = IR を使った / used V = IR
- [ ] P = VI を使った / used P = VI
- [ ] 6Wランプの0.25 Aを計算した / calculated 0.25 A for the 6 W lamp
- [ ] 負荷合計0.73 Aを計算した / calculated the 0.73 A total
- [ ] 0.73 Aが承認ではないと説明した / explained that 0.73 A is not approval
- [ ] 突入電流・定格低下・電線・端子・保護を確認項目に入れた / included inrush, derating, wiring, terminals and protection
- [ ] スイッチ・リレー・ランプの役割を区別した / distinguished switch, relay and lamp
- [ ] 制御信号と電力の経路を分けた / separated the control signal from the power path
- [ ] 電圧降下の概算と仮定を書いた / wrote the voltage-drop estimate and assumptions
