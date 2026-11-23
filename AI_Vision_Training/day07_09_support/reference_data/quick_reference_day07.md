# 第7日 公式・確認カード / Day 7 formula and check card

> このカードは学習用です。実機の設計・選定・安全確認を承認するものではありません。
> This card is for learning. It does not approve a real design, selection or safety verification.

## 1. 生産能力 / production capacity

| 量 / Quantity | 式 / Formula | 例 / Example |
|---|---|---|
| タクトタイム / takt time | 生産時間[秒] ÷ 必要数量 / available seconds ÷ required pieces | 420×60 ÷ 600 = **42 s/個** |
| 理論能力 / theoretical capacity | 3600 ÷ サイクルタイム[秒] / 3600 ÷ cycle time | 3600 ÷ 15 = **240 個/時** |
| 実力能力 / effective capacity | 理論能力 × 稼働率 × 良品率 / theoretical × availability × yield | 240×0.85×0.98 = **199.92 個/時** |
| 必要能力 / required rate | 必要数量 ÷ 生産時間[h] / pieces ÷ hours | 600 ÷ 7 = **85.71 個/時** |

## 2. 力とシリンダ / force and cylinder

```text
F_friction = μ × m × g
F_design   = F_friction × factor
D_theory   = √(4 × F_design / (π × P))
F_push     = P × π × D² / 4
F_pull     = P × π × (D² − d²) / 4
```

- m: 質量 [kg] / mass
- g: 9.81 m/s²（教材値）/ teaching value
- μ: 摩擦係数（単位なし）/ friction coefficient
- P: シリンダにかかるゲージ圧 [Pa] / gauge pressure at the cylinder
- D: 内径 [m] / bore
- d: ロッド径 [m] / rod diameter
- factor: 余裕係数（教材の仮定）/ teaching margin

**例 / example**: 8 kg、μ=0.25 → 19.62 N。factor 2 → 39.24 N。P=0.4 MPa → D ≈ **11.18 mm**（理論下限）。
**Example**: 8 kg, μ=0.25 → 19.62 N; factor 2 → 39.24 N; 0.4 MPa → D ≈ **11.18 mm** (theoretical lower bound).

> 11.18 mm はカタログ選定ではありません。負荷率・速度・偏荷重・圧力損失・センサー対応を確認します。
> 11.18 mm is not a catalogue selection. Check load factor, speed, side load, pressure loss and sensing.

## 3. モーターと減速機 / motor and reducer

```text
ω = 2πn / 60
T = P / ω
n_out = n_in / ratio
T_out = T_in × ratio × η
```

**例 / example**: 60 W、1200 rpm → T ≈ **0.477 N·m**。20:1 → 60 rpm、理想 T ≈ **9.55 N·m**。η=0.90（追加仮定）→ **8.59 N·m**。
**Example**: 60 W at 1200 rpm → T ≈ **0.477 N·m**; 20:1 → 60 rpm, ideal T ≈ **9.55 N·m**; η=0.90 (added assumption) → **8.59 N·m**.

## 4. 空圧回路の確認 / pneumatic circuit checks

- 空気源 → 遮断 → 空気準備（フィルタ・レギュレータ）→ 方向切替弁 → 速度制御 → シリンダ / source, isolation, preparation, directional valve, flow control, cylinder.
- 遮断の下流に排気（ブリード）と圧力計 / bleed and gauge downstream of isolation.
- 無通電時の弁位置は機種依存 / de-energised valve position is model-dependent.
- 残圧は遮断だけでは抜けない / isolation alone does not release stored pressure.
- 電磁弁OFFは安全状態を保証しない / de-energising a solenoid does not guarantee safety.

## 5. 提出前チェック / pre-submission checks

- [ ] タクトと実力能力を分けた / separated takt and effective capacity
- [ ] 質量[kg]と力[N]を区別した / distinguished mass and force
- [ ] 理論値とカタログ候補を分けた / separated theoretical values from catalogue candidates
- [ ] 仮定・未確認・出典・版を書いた / recorded assumptions, open items, sources and revisions
- [ ] 危険源と保護方策の方向性を書いた / wrote hazards and the direction of protective measures
- [ ] 実機の通電・空圧・安全確認は行っていない / did not energise or pressurise real equipment
