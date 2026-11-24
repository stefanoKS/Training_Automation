# 第8日 公式・確認カード / Day 8 formula and check card

> このカードは学習用です。実機の盤の製作・配線・通電・保護機器の選定を承認するものではありません。
> This card is for learning. It does not approve building, wiring, energising a real panel or selecting protective devices.

## 1. 電気の基本 / electrical basics

```text
V = I × R            (抵抗モデルが成り立つ場合 / where a resistive model applies)
P = V × I            (直流 / DC)
電力量[kWh] = 電力[kW] × 時間[h]
```

例 / examples:

- DC24V、0.15 A → **3.6 W**。2個で **0.30 A、7.2 W**。
- 100 W を8時間 → **0.8 kWh**。30円/kWh（教材値）→ **24円**。

## 2. 電圧の使い分け / voltage applications

| 電圧 / Voltage | 主な使い道 / Typical use |
|---|---|
| AC100V | 一般機器の電源、小型機器 / common equipment supply, small equipment |
| AC200V | 産業用の動力、対応するモーター駆動 / industrial power, compatible drives |
| DC24V | PLC入出力、センサー、リレー、電磁弁 / PLC I/O, sensors, relays, valves |
| DC12V | 一部のカメラ、電子機器 / some cameras and electronics |
| DC5V | USB機器、マイコン / USB equipment, microcontrollers |

- 電圧だけで制御用・動力用は決まらない。 / Voltage alone does not define control or power.
- ACは W と VA が違う（力率）。 / In AC, W and VA differ (power factor).

## 3. 電源容量の例 / power budget example

| 負荷 / Load | 数量 / Qty | 電流 / Current |
|---|---:|---:|
| PLC | 1 | 0.35 A |
| センサー / sensors | 4 | 0.025 A each |
| 電磁弁 / valves | 2 | 0.15 A each |
| 表示灯 / lamp | 1 | 0.05 A |

合計 **0.80 A**、**19.2 W**。計画余裕25%（教材値）→ **1.00 A**。

- 同時使用・突入電流・温度・メーカーの定格低下・将来増設を確認する。
- Check simultaneity, inrush, temperature, manufacturer derating and future expansion.

## 4. 保護機器の守る範囲 / what protective devices cover

| 機器 / Device | 守る / Covers | 守らない / Does not cover |
|---|---|---|
| 配線用遮断器 / circuit breaker | 定格内の過電流、配線 / overcurrent within ratings, wiring | すべての故障 / every fault |
| 漏電遮断器 / earth-leakage device | 設計に応じた漏れ電流 / specified leakage current | 過電流一般 / general overcurrent |
| ヒューズ / fuse | 規定の過電流特性 / specified overcurrent characteristic | 再利用 / reuse |
| サーマルリレー / overload relay | モーターなどの過負荷 / overload, commonly motors | 短絡保護 / short-circuit protection |

## 5. NPN / PNP

| センサー出力 / Sensor | 動作時 / When active | PLC入力共通 / Input common | 電流 / Current |
|---|---|---|---|
| PNP | +から電流を出す / sources | 0V（シンク入力 / sinking） | +24V → センサー → PLC → 0V |
| NPN | 0Vへ電流を引く / sinks | +24V（ソース入力 / sourcing） | +24V → PLC → センサー → 0V |

- NPN/PNPは出力インターフェース。NO/NCは検出の論理。 / NPN/PNP is the interface; NO/NC is the detection logic.
- PLC全体を「NPNのPLC」と呼べない。入力モジュールと配線で決まる。
- 配線色は例。データシートに従う。 / Wire colours are examples; follow the datasheet.

## 6. ラダー / ladder

```text
AND  |--[ A ]--[ B ]--( Y )--|
OR   |--+--[ A ]--+--( Y )--|
     |  +--[ B ]--+
NOT  |--[/ A ]-------( Y )--|
自己保持 / seal-in: M0 = X1 AND (X0 OR M0)
```

- 接点は論理状態の評価。物理接点や実電流ではない。 / Contacts evaluate logical states.
- 物理NCのSTOPを、プログラムではON許可として使うことがある。 / A physical NC stop may appear as an ON permission.

## 7. 再起動防止の要点 / restart prevention

- 起動時RUN=OFF。 / RUN is OFF at power-up.
- STARTが離れたことを確認してからアームする。 / Arm only after START is seen released.
- 新しい立ち上がりだけで起動。 / Start only on a new rising edge.
- STOPはSTARTより優先。 / STOP precedes START.
- リセットは運転開始ではない。 / Reset is not a start.
- 許可が戻っても自動で動かない。 / Restoring a permissive does not restart.
- **安全機能ではない。** / **Not a safety function.**

## 8. インターロック / interlock

- 同時に成立してはいけない指令を成立させない。 / Prevent incompatible commands.
- 相互に打ち消すだけの形はスキャン順に依存。同時要求は決定的に拒否する。
- 実機の反転接触器は電気的・機械的インターロックも必要。 / Real reversing contactors also need electrical and mechanical interlocking.
- ソフトのインターロックを安全定格のガードにしない。 / Not safety-rated guarding.
