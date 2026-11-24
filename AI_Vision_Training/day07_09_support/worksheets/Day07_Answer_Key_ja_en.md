# 第7日 解答例 / Day 7 Answer Key

> 数値はすべて独立に再計算して確認しています。別解がある場合は、成立する条件を添えています。
> All numbers were re-computed independently. Where more than one answer is valid, the conditions are stated.

## T1 生産能力と効果金額 / capacity and economic effect

| # | 式 / Formula | 計算 / Working | 答え / Answer |
|---|---|---|---|
| 1 | 生産時間[秒] ÷ 必要数量 / available seconds ÷ pieces | 420 × 60 ÷ 600 | **42 秒/個（42 s/piece）** |
| 2 | 必要数量 ÷ 生産時間[h] / pieces ÷ hours | 600 ÷ 7 | **約85.71 個/時** |
| 3 | 3600 ÷ サイクル × 個数 / 3600 ÷ cycle × pieces | 3600 ÷ 15 × 1 | **240 個/時** |
| 4 | 12 × 180 ÷ 3600 × 220 / same in hours | 0.6 h/日 × 220日 | **132 時間/年** |
| 5 | 132 × 2,400 | — | **316,800 円/年** |
| 6 | 316,800 − 50,000 | — | **266,800 円/年** |
| 7 | 450,000 ÷ 266,800 | — | **約1.69 年** |

8. 解答例 / example: 削減した時間が別の作業に移るだけなら、人件費の支払いは減らない。残業が減る場合や、増えた生産を販売できる場合にだけ現金・利益に結びつく。 / If the freed time is redeployed, payroll does not fall. Cash and profit follow only from reduced overtime or from extra output that can be used or sold.

**採点上の注意 / marking note:** 回収期間を1.42年とした場合は、年間運用費を0と仮定した場合のみ正しい。 / A payback of 1.42 years is correct only when the annual operating cost is zero.

## T2 アクチュエータの選定 / actuator selection

| # | 式 / Formula | 計算 / Working | 答え / Answer |
|---|---|---|---|
| 1 | μ × m × g | 0.20 × 5 × 9.81 | **9.81 N** |
| 2 | 摩擦力 × 余裕 / friction × factor | 9.81 × 2 | **19.62 N** |
| 3 | √(4F ÷ (πP)) | √(4 × 19.62 ÷ (π × 0.5)) = √(49.96…) | **約7.07 mm** |

4. 解答例 / example: 静止摩擦はすべり摩擦より大きいことが多い。加速度・衝突・ガイドの偏荷重・背圧・圧力損失・負荷率・センサー対応を確認していない。 / Static friction is often higher. Acceleration, impact, guide offset loads, back pressure, pressure losses, load ratio and sensing have not been checked.

5. 解答例 / example: 2位置の単純な押出しなら**空圧**が候補（構造が簡単で速い）。位置を変えたり中間で止めたりするなら**電動**が候補。どちらも条件付きで妥当であり、唯一の正解ではない。 / Pneumatic is a candidate for a simple two-position push; electric is a candidate if positions must change or stop midway. Both are valid under the stated conditions; neither is uniquely correct.

## 数値の再現方法 / how to reproduce

```text
takt       = 420*60/600                 = 42
required   = 600/7                      = 85.714...
capacity   = 3600/15*1                  = 240
hours/year = 12*180/3600*220            = 132
value      = 132*2400                   = 316800
net        = 316800-50000               = 266800
payback    = 450000/266800              = 1.6866...
friction   = 0.20*5*9.81                = 9.81
design     = 9.81*2                     = 19.62
bore       = sqrt(4*19.62/(pi*0.5))     = 7.0686...
```
