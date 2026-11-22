# 第7日 公式・確認カード / Day 7 formula and check card

**すべて仮定の例です。/ All examples are hypothetical.**

## 1. 単位 / Units

| 量 / quantity | 単位 / unit | 換算 / conversion |
|---|---|---|
| 長さ / length | mm, m | 1 m = 1,000 mm |
| 速さ / speed | mm/s, m/min | 1 m/min = 1,000 mm ÷ 60 s ≈ 16.667 mm/s |
| 回転 / rotation | rpm | 1 rpm = 1 回転/分 / turns per minute |
| 周波数 / frequency | Hz | 1 Hz = 1 回/秒 / one per second |

## 2. ローラと搬送 / Rollers and transport

**円周 C = π × D**、**表面速度 v = C × N**（滑りなしの仮定 / no-slip assumption）。

| 例 / example | D | N | C | v |
|---|---:|---:|---:|---:|
| 1 | 100 mm | 100 rpm | ≈ 314.159 mm | ≈ 31.416 m/min |
| 2 | 80 mm | 200 rpm | ≈ 251.327 mm | ≈ 50.265 m/min |
| 3 | 150 mm | 60 rpm | ≈ 471.239 mm | ≈ 28.274 m/min |

**pulley ratio / プーリ比:** n2 / n1 = D1 / D2（滑りなし / no slip）。
**acceleration / 加速度:** a = Δv / Δt。

## 3. エンコーダ / Encoder

**counts per turn = PPR × decode**（1・2・4）。
**distance per count = π × D ÷ counts per turn**（滑りなし / no slip）。

| 例 / example | PPR | decode | counts/turn | distance/count（D=100 mm） |
|---|---:|---:|---:|---:|
| 1 | 1,000 | ×4 | 4,000 | ≈ 0.07854 mm |
| 2 | 500 | ×2 | 1,000 | ≈ 0.31416 mm |
| 3 | 2,500 | ×4 | 10,000 | ≈ 0.03142 mm |

## 4. アナログ / Analog

**physical = (electrical − min) ÷ (max − min) × (physical max − physical min)**

| 信号 / signal | 最小 / min | 中央 / mid | 最大 / max（0–100 kPa） |
|---|---|---|---|
| 0–10 V | 0 V = 0 kPa | 5 V = 50 kPa | 10 V = 100 kPa |
| 4–20 mA | 4 mA = 0 kPa | 12 mA = 50 kPa | 20 mA = 100 kPa |

## 5. 安全確認 / Safety check

- ☐ ガードとインターロックが設計・検証されている / guards and interlocks designed and validated
- ☐ 非常停止は独立した安全系 / emergency stop in an independent safety system
- ☐ 残圧・蓄積エネルギーの手順がある / stored energy and pressure procedures exist
- ☐ 保守時の停止・遮断・ロックアウト手順 / stop, isolate and lock-out procedures
- ☐ AIや通常のラダーを安全機能と表現していない / AI and ordinary ladder are not called safety functions

## 6. よくある誤解 / Common misunderstandings

1. 計算した速度が実測と一致する → 滑り・張力・摩耗で異なる / calculated speed equals measured speed → slip, tension and wear change it.
2. PPR がそのままカウント数 → デコードで変わる / PPR equals counts → decoding changes counts.
3. センサは材質を問わない → 方式と対象で選ぶ / any sensor detects any material → select by mode and target.
4. AIを直せば機械の問題も消える → まず機械と照明 / fixing AI fixes mechanics → stabilise mechanics and lighting first.
