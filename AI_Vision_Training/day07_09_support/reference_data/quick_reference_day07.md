# 第7日 公式・確認カード / Day 7 formula and check card

> このカードは学習用です。実機の設計・選定・安全確認を承認するものではありません。
> This card is for learning. It does not approve a real design, selection or safety verification.

## 1. 生産能力 / production capacity

| 量 / Quantity | 式 / Formula | 例 / Example |
|---|---|---|
| タクトタイム / takt time | 生産時間[秒] ÷ 必要数量 / available seconds ÷ required pieces | 420×60 ÷ 600 = **42 s/個** |
| 必要生産能力 / required rate | 必要数量 ÷ 生産時間[h] / pieces ÷ hours | 600 ÷ 7 ≈ **85.71 個/時** |
| 理論能力（サイクル）/ theoretical cycles | 3600 ÷ サイクルタイム[秒] / 3600 ÷ cycle time | 3600 ÷ 15 = **240 サイクル/時** |
| 理論能力（個数）/ theoretical pieces | 3600 ÷ サイクルタイム × 1サイクルの個数 / × pieces per cycle | 240 × 1 = **240 個/時** |

- タクトは「必要なペース」、サイクルは「機械の時間」。 / Takt is the required pace; cycle is the machine time.
- **1サイクルあたりの個数**を言わないと、能力は決まらない。 / Capacity is undefined without pieces per cycle.
- 稼働率・OEEはこの研修の必須範囲外。 / Availability and OEE are outside this course.

## 2. 効果金額 / economic effect

```text
1日の削減時間[h] = 1回の削減時間[s] × 1日の回数 ÷ 3600
年間削減工数[h]  = 1日の削減時間 × 年間稼働日数
労務費換算額[円]  = 年間削減工数 × 時給[円/時]
年間純効果[円]    = 労務費換算額 − 年間運用費
簡易回収期間[年]  = 設備導入費 ÷ 年間純効果
```

例 / example: 12 s × 180回/日 ÷ 3600 = **0.6 h/日** → × 220日 = **132 h/年** → × 2,400円 = **316,800 円/年**。
運用費0なら回収期間 **450,000 ÷ 316,800 ≈ 1.42 年**。運用費50,000円なら **266,800 円/年 → 約1.69 年**。

- 削減時間がそのまま現金になるとは限らない。 / Saved time is not automatically cash.
- 年間純効果が0以下なら、回収期間は意味を持たない。 / Payback is meaningless at zero or negative net benefit.

## 3. シリンダの力 / cylinder force

```text
押し側 F = P × π × D² ÷ 4          extension
引き側 F = P × (π × (D² − d²) ÷ 4)  retraction
理論内径 D = √(4 × F ÷ (π × P))
摩擦力 F = μ × m × g
```

- P：ゲージ圧 [MPa]、1 MPa = 1 N/mm² / gauge pressure
- D：内径 [mm]、d：ロッド径 [mm]、m：質量 [kg]、g = 9.81 m/s²

例 / examples:

- D20、d8、P0.5 → 押し **157.08 N**、引き **131.95 N**
- 8 kg、μ0.25 → 19.62 N → 余裕2 → 39.24 N → P0.4 MPa → D ≈ **11.18 mm**

> 理論値です。背圧・摩擦・加速度・偏荷重・損失は含みません。11.18 mm はカタログ選定ではありません。
> Theoretical values. Back pressure, friction, acceleration, offset loads and losses are excluded. 11.18 mm is not a catalogue selection.

## 4. モーターと減速機 / motor and reducer

```text
角速度 ω = 2 × π × rpm ÷ 60        [rad/s]
機械出力 P = T × ω                 [W]
トルク T = P ÷ ω                   [N·m]
出力回転数 = 入力回転数 ÷ 減速比
出力トルク = 入力トルク × 減速比 × 減速機効率
```

例 / example: 60 W、1,200 rpm → T ≈ **0.477 N·m**。減速比20、効率0.90 → 出力 **60 rpm**、**約8.59 N·m**。

- 機械出力と電気入力は別。 / Mechanical output and electrical input differ.
- 減速機効率はモーター効率の代わりにならない。 / Reducer efficiency does not replace motor efficiency.

## 5. 速度 / speed

```text
平均速度 = 移動距離 ÷ 移動時間
```

例 / example: 100 mm ÷ 0.5 s = **200 mm/s**。平均は最高速度ではない。 / Average is not peak speed.

## 6. 選定前のチェック / before selecting

- [ ] 質量 kg と力 N を分けた / mass and force separated
- [ ] ストローク、速度、サイクルタイムを測った / stroke, speed, cycle time measured
- [ ] 中間位置に止める必要があるか決めた / intermediate positions decided
- [ ] 取付姿勢・偏荷重・ガイドを確認した / orientation, offset load, guides
- [ ] 使える動力（空気・油・電気）を確認した / available power
- [ ] 停止したときの動きを確認した / behaviour at stop
