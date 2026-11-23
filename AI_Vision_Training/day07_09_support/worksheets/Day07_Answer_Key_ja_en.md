# 第7日 解答例と採点の観点 / Day 7 Answer Key (instructor copy)

**学生には配布しません。 / Do not distribute to students.**

**採点の原則 / Marking principles**

数値が一致しただけでは正解にしません。式、代入、単位、仮定、判定の理由を確認します。途中の値がなく最終値だけが書かれている答案は、たまたま一致した可能性を排除できないため、減点対象です。逆に、仮定を明示して妥当な範囲で違う値になった答案は、理由が正しければ受理します。

A matching number alone is not a correct answer. Check the formula, the substitution, the unit, the assumption and the reason for the verdict. An answer that shows only the final value cannot be distinguished from a lucky guess and is marked down. An answer with a different but well-justified value inside the stated range is accepted when the reasoning is sound.

**この解答例の位置づけ / Status of this key:** 教材用の仮定に基づく計算例です。実機の設計値・選定値ではありません。 / These are worked examples on training assumptions, not real design or selection values.

## T1 現状課題文 / Current-state problem

**期待される内容 / What to expect**

- 作業名、手順、回数、1回の時間が具体的で、測った条件（作業者・品種・時間帯）が添えられている。 / The task, steps, frequency and time per occurrence are concrete, with the measurement conditions.
- 困りごとが観測できる事実で書かれ、「遅い」「危ない」などの評価語だけで終わっていない。 / The problem is an observable fact, not only an evaluation word.
- 推測した原因が、事実の欄と混ざっていない。 / Suspected causes are kept out of the fact column.
- まだ測っていない項目が、次の確認項目として残っている。 / Unmeasured items remain as the next checks.
- ECRSの案が「なくす」「まとめる」「順序・配置を変える」「簡単にする」のどれかに該当する。 / The ECRS idea maps to eliminate, combine, rearrange or simplify.

**よくある誤り / Common mistakes**

- 1回の時間を測らずに「約10秒」と概算で書き、条件を残さない。 / Guessing the time without recording conditions.
- 原因（ガイド摩耗など）を事実の欄に書いてしまう。 / Putting a cause in the fact column.
- ECRSを飛ばして、いきなり設備の案を書く。 / Jumping to equipment before ECRS.

**許容範囲 / Acceptable range**

作業内容が違えば数値は違って当然です。回数と時間が測定条件付きで書かれ、事実と推測が分離されていれば、値そのものは問いません。 / Values differ by task; what matters is that frequency and time carry measurement conditions and that fact and assumption are separated.

## T2 生産能力の計算 / Capacity calculation

**期待される答え / Expected answers**

| # | 量 / Quantity | 式と代入 / Formula and substitution | 答え / Answer |
|---|---|---|---|
| 1 | タクトタイム / takt time | 420 × 60 ÷ 600 = 25,200 ÷ 600 | **42.0 s/個** |
| 2 | 理論能力 / theoretical capacity | 3,600 ÷ 15 | **240.00 個/時** |
| 3 | 実力能力 / effective capacity | 240 × 0.85 × 0.98 = 204 × 0.98 | **199.92 個/時** |
| 4 | 必要能力 / required rate | 600 ÷ (420 ÷ 60) = 600 ÷ 7 | **85.71 個/時** |
| 5 | サイクルはタクトを満たすか | 15 ≤ 42、利用率 15 ÷ 42 | **Yes、35.7 %** |
| 6 | 実力能力は必要能力を満たすか | 199.92 ÷ 85.71 | **Yes、2.33 倍** |

- 余裕は 199.92 − 85.71 = **114.21 個/時**。600個の処理に必要な時間は 600 ÷ 199.92 = **3.00時間（約180分）**で、使える420分より短い。 / The margin is 114.21 pieces/h; 600 pieces need about 180 minutes of the 420 available.
- 感度の確認（発展・任意）/ sensitivity check (optional extension): 稼働率0.70では 240 × 0.70 × 0.98 = **164.64 個/時**。必要能力85.71個/時に対して **1.92倍**なので、依然として満たす。 / At 0.70, effective capacity is 164.64 pieces/h, still 1.92 times the requirement.
- 実力能力が必要能力と等しくなるサイクルタイムは 3,600 × 0.85 × 0.98 ÷ 85.71 ≈ **35.0秒**。これを超えると能力不足になる。 / Break-even cycle time is about 35.0 s.

**解説 / Why this works**

タクトは「目標ペース」、サイクルは「設備の実力」、実力能力は「停止と不良を織り込んだ出力」で、3つは別の量です。タクト42秒に対してサイクル15秒なので、設備は目標より速い。さらに稼働率と良品率を掛けても、なお必要能力を上回ります。ただし稼働率0.85と良品率0.98は仮定であり、現場で測るまでは保証されません。

Takt is the target pace, cycle time is the machine's capability, and effective capacity includes downtime and defects. The 15 s cycle is faster than the 42 s takt, and even after applying availability and yield the output exceeds the requirement. The 0.85 and 0.98 are assumptions, not guarantees, until measured on site.

**よくある誤り / Common mistakes**

- タクトと実力能力を混同し、「能力は42個/時」と書く。 / Confusing takt with capacity.
- 420分をそのまま時として扱い、必要能力を 600 ÷ 420 = 1.43 個/時とする。 / Treating 420 minutes as 420 hours.
- 稼働率を85（百分率）のまま掛けて、19,992個/時のような桁違いの値にする。 / Multiplying by 85 instead of 0.85, giving a value around 19,992 pieces/h.
- 理論能力240個/時だけを見て、停止と不良を無視する。 / Using theoretical capacity alone.
- 利用率を 42 ÷ 15 = 280 % と書く（分母と分子が逆）。 / Inverting the utilisation ratio.

**許容範囲 / Acceptable range**

タクト42.0秒、実力能力199.9〜199.92個/時、必要能力85.7個/時。小数第1位までの丸めは可。ただし丸めた値を使った後続の判定（2.33倍、35.0秒）が整合していることを確認します。 / Accept 42.0 s, 199.9–199.92 pieces/h and 85.7 pieces/h, provided the downstream verdicts stay consistent.

## T3 3案の比較 / Three-concept comparison

**重みと点数の一例 / A worked weighting**

| 観点 / Criterion | 重み / Weight | A | B | C |
|---|---:|---:|---:|---:|
| 初期費用 / initial cost | 0.20 | 5 | 3 | 1 |
| 省人効果 / labour saving | 0.25 | 1 | 4 | 5 |
| 品種変更 / product change | 0.15 | 3 | 3 | 4 |
| 停止時の復旧 / recovery | 0.15 | 5 | 4 | 2 |
| 安全上の論点 / safety | 0.25 | 4 | 2 | 1 |
| **加重合計 / weighted total** | **1.00** | **3.45** | **3.15** | **2.60** |

計算例（A）: 0.20×5 + 0.25×1 + 0.15×3 + 0.15×5 + 0.25×4 = 1.00 + 0.25 + 0.45 + 0.75 + 1.00 = **3.45**。

**解説 / Why this is not the decision**

この重みではAが最高点になりますが、Aは省人効果が1点で、押出し作業を人から機械へ移すという目的を満たしません。点数が高い案をそのまま採用するのではなく、必須条件（省人、安全、復旧性）を先に確認します。BとCの選択は、必要な能力と品種変更の頻度で変わります。たとえば重みを「初期費用0.10、省人効果0.40、品種変更0.10、復旧0.10、安全0.30」に変えると、A 2.90、B 3.20、C 3.00 となり、Bが最高になります。順位が変わった理由を説明できれば、別の重みでも受理します。

A wins under this weighting, yet A scores 1 for labour saving and therefore fails the purpose of moving the push from a person to a machine. Check the mandatory requirements before trusting the total. B versus C depends on the required capacity and change frequency. With weights of 0.10, 0.40, 0.10, 0.10 and 0.30 the scores become A 2.90, B 3.20 and C 3.00, putting B first. A different weighting that changes the ranking is acceptable if the reason is explained.

**よくある誤り / Common mistakes**

- 重みの合計が1.00になっていない。 / Weights that do not sum to 1.00.
- 点数だけを書き、採用理由と却下理由がない。 / Scores without accept and reject reasons.
- 安全を「点数が高いから大丈夫」と扱う。 / Treating a high score as proof of safety.
- 5点満点の向きを逆にし、5が不利なのに有利として集計する。 / Inverting the 1–5 scale.

**必須条件の例 / Examples of a mandatory requirement**

- 可動部への接近を、通常運転中は機構またはガードで防ぐ方向を要求仕様に書く。 / The requirement states that access to the moving part is prevented by design or guarding during normal operation.
- STARTを1回押したら1サイクルだけ実行し、押しっぱなしで連続動作しない。 / One press gives exactly one cycle; holding START must not repeat it.
- 停止後の再開は、新しいSTART操作を必要とする。 / Restart after a stop needs a fresh START.

**許容範囲 / Acceptable range**

重みの合計が1.00で、各案の加重合計が計算過程と一致していれば受理します。採用案が必須条件を満たしていること、却下案の理由が1つ以上あることが条件です。重みが違って順位が変わっても、理由が説明されていれば可。 / Accept when the weights sum to 1.00 and each total matches its working. The selected concept must satisfy the mandatory requirements and each rejected concept needs a reason. A different weighting and ranking is acceptable when explained.

## T4 要求仕様と受入基準 / Requirements and acceptance criteria

**期待される答えの例 / Model answers**

| 分類 / Category | 要求 / Requirement | 測定量 / Measurand | 条件 / Condition | 合格範囲 / Pass range | 回数 / Sample |
|---|---|---|---|---|---|
| 能力 / capacity | 1日600個を420分で処理する / 600 pieces in 420 min | 実力能力 / effective capacity | 連続運転、停止と不良を含む / continuous run including stops and defects | 85.7個/時以上 / at least 85.7 per hour | 3回 / 3 runs |
| 品質 / quality | 押出し後の位置が安定する / stable pushed position | 基準面からの押出し面の位置 / pusher face position from datum | 後退端で停止、常温 / stopped retracted, ambient | ±2 mm以内 / within ±2 mm | 10サイクル連続 / 10 consecutive |
| 運転 / operation | STARTで1サイクルだけ動く / one cycle per START | サイクル数 / cycle count | STARTを押し続ける / START held | 1サイクル、連続動作なし / 1 cycle, no repeat | 5回 / 5 trials |
| 安全 / safety | 可動部への接近を防ぐ方向を決める / direction for preventing access | ガード開口と可動部の距離 / guard opening and distance | 設計レビュー / design review | 指が届かない、またはインターロック / unreachable or interlocked | レビュー1回 / one review |
| 保全 / maintenance | センサーを調整できる / sensor adjustable | 調整代と工具スペース / adjustment range and tool space | カバーを開けた状態 / cover open | 規定工具で規定時間内 / with the specified tool and time | 1回 / once |

**書き直しの例 / Model rewrite**

悪い例「位置決めが正確なこと」→「後退端で停止したとき、押出し面の基準面からのずれが±2 mm以内。10回連続で測定し、10回すべて合格」。測定量（押出し面の位置）、条件（後退端で停止）、合格範囲（±2 mm）、回数（10回）が入っています。

Bad: "positioning must be accurate." Good: "with the pusher retracted, the pusher face is within ±2 mm of the datum; measure 10 consecutive cycles and all 10 must pass." It states the measurand, the condition, the pass range and the sample size.

**よくある誤り / Common mistakes**

- 合格範囲が「適切に」「問題なく」のまま。 / Pass ranges such as "properly" or "without problems".
- 条件（速度、温度、ワーク品種）が抜けている。 / Missing conditions such as speed, temperature or product.
- 安全の欄に「安全を確保する」とだけ書き、危険源と方策の方向がない。 / Writing only "ensure safety" in the safety row.
- 測定回数がなく、1回の観察で合格としている。 / No sample size, passing on a single observation.

**許容範囲 / Acceptable range**

数値そのものは現場で決まります。測定量・条件・合格範囲・回数の4要素がそろっていることを必須とします。安全の欄は、完成した安全設計ではなく「危険源と保護方策の方向」で足ります。 / The four elements matter, not the specific numbers. The safety row needs hazards and a direction for protective measures, not a completed safety design.

## T5 初期リスクリスト / Initial risk list

**期待される危険源 / Expected hazards**

| 危険源 / Hazard | 想定する事故 / Possible harm | 低減の方向 / Reduction direction |
|---|---|---|
| 押出し部の挟まれ / pinch at the pusher | 手指の圧挫 / finger crush | 機構で接近を防ぐ → ガード → 監視 / prevent by design, then guard, then monitor |
| ワークの飛出し / workpiece ejection | 眼・顔面の負傷 / eye or face injury | ストッパ、カバー、低速度化 / stopper, cover, lower speed |
| 残圧 / stored air pressure | 保全中の不意動作 / unexpected motion during maintenance | 遮断、排気、圧力計で零確認、ロックアウト / isolate, bleed, verify zero, lock out |
| 復電・再給気 / power or air restore | 不意起動 / unexpected start | 再起動条件を設計し、新規STARTを要求 / design restart conditions and require a fresh START |
| 電気 / electricity | 感電、短絡、発熱 / shock, short, heat | 保護、絶縁、接地、無電圧確認 / protection, insulation, earthing, verification |

**解説 / Why the order matters**

「なくす」が最上位です。押す必要自体を消せれば、挟まれも飛出しも発生しません。「守る」（ガード）は有効ですが、開口や保全時の接近が残ります。「知らせる」（表示・警報）は最後の手段で、人に依存します。

Elimination comes first: if the push is unnecessary, neither pinch nor ejection can occur. Guarding is effective but leaves openings and maintenance access. Informing is the last layer because it depends on people.

**「通常のPLCのSTOPは安全機能ではない」の説明例 / Model explanation**

通常のPLCは、故障時に出力がどうなるかを保証せず、プログラム変更や強制出力で停止条件を無効にできるため、人身安全を担保する安全機能にはなりません。安全機能はリスクアセスメントに基づき、独立した安全関連システムとして設計・検証します。

An ordinary PLC does not guarantee output behaviour under fault, and its stop condition can be defeated by a program change or a forced output, so it cannot assure personal safety. Safety functions are designed and validated as an independent safety-related system based on a risk assessment.

**よくある誤り / Common mistakes**

- 危険源を「機械」とだけ書き、挟まれ・飛出し・残圧・再起動に分けない。 / Writing only "the machine" instead of specific hazards.
- 「注意する」「教育する」を対策の中心にする。 / Relying on caution or training as the main measure.
- 通常のPLCの停止ラングを安全対策として挙げる。 / Listing ordinary PLC stop logic as a safety measure.

**許容範囲 / Acceptable range**

危険源が3つ以上あり、挟まれ・飛出し・残圧・再起動のうち2つ以上を名指ししていれば受理します。低減の方向が「なくす → 離す → 守る → 知らせる」の順に沿っていれば、表現は問いません。 / Accept three or more hazards naming at least two of pinch, ejection, stored pressure and restart. Wording is free if the reduction follows eliminate, separate, guard, inform.

## T6 シリンダの計算 / Cylinder calculation

**期待される答え / Expected answers**

| # | 量 / Quantity | 式と代入 / Formula and substitution | 答え / Answer |
|---|---|---|---|
| 1 | 摩擦力 / friction | 0.25 × 8 × 9.81 | **19.62 N** |
| 2 | 設計力 / design force | 19.62 × 2 | **39.24 N** |
| 3 | 理論内径 / theoretical bore | √(4 × 39.24 ÷ (π × 400,000)) = √(1.249 × 10⁻⁴) | **11.18 mm**（11.176） |
| 4 | 押し側推力 / push（20 mm） | 400,000 × π × 0.02² ÷ 4 | **125.66 N** |
| 5 | 戻り側推力 / pull（20 mm、ロッド8 mm） | 400,000 × π × (0.02² − 0.008²) ÷ 4 | **105.56 N** |
| 6 | 差 / difference | 125.66 − 105.56 | **20.11 N** |

- 質量8 kgの重力は 8 × 9.81 = 78.48 N。質量[kg]と力[N]は別の量であり、摩擦力19.62 Nとは区別します。 / The weight is 78.48 N; mass and force are different quantities, and neither equals the 19.62 N friction.
- 戻り側は、ロッドの断面積が加圧されないため受圧面積が小さく、その分だけ推力が下がります。比は 105.56 ÷ 125.66 = 0.840。 / The rod area is not pressurised on the pull side, so the effective area and force are smaller; the ratio is 0.840.
- 余裕係数3: 設計力 19.62 × 3 = **58.86 N**、理論内径 √(4 × 58.86 ÷ (π × 400,000)) = **13.69 mm**。 / Margin 3 gives 58.86 N and 13.69 mm.
- 圧力0.3 MPa: √(4 × 39.24 ÷ (π × 300,000)) = **12.91 mm**。圧力が下がると必要な内径は大きくなります（面積で割るため）。 / At 0.3 MPa the bore is 12.91 mm; lower pressure needs a larger bore.

**理論下限であって選定ではない理由 / Why the bore is a lower bound**

1. シリンダに実際にかかる圧力は、配管・弁・速度制御・内部抵抗で供給圧より低いことがある。 / The pressure at the piston can be below the supply pressure because of piping, valves, flow control and internal resistance.
2. 加速、衝突、ガイド抵抗、偏荷重、クッション、押し方の偏心を式が含んでいない。 / The formula excludes acceleration, impact, guide resistance, side load, cushioning and off-centre pushing.
3. メーカーの負荷率、許容モーメント、速度制限、標準内径の段階を確認していない。 / The manufacturer's load factor, allowable moment, speed limits and standard bore steps have not been applied.

**よくある誤り / Common mistakes**

- 圧力0.4をPaに換算せず、内径が 11.18 m や 0.011 mm になる。 / Not converting 0.4 MPa to 400,000 Pa.
- 質量8 kgをそのまま力として使い、摩擦力を 0.25 × 8 = 2 N とする。 / Using 8 kg directly as a force.
- 戻り側でもボア面積をそのまま使う。 / Using the full bore area on the pull side.
- 「11.18 mmを超える最小の内径を選ぶ」と結論する。 / Concluding "choose the smallest bore above 11.18 mm".
- 余裕係数を3にしたとき、内径が3倍になると考える（面積に比例するので√3倍）。 / Thinking the bore triples with margin 3; it scales with the square root.

**許容範囲 / Acceptable range**

摩擦19.6〜19.62 N、設計力39.2〜39.24 N、内径11.1〜11.2 mm、押し側125.6〜125.7 N、戻り側105.5〜105.6 N。g = 9.8 を使った場合は摩擦19.6 N、設計力39.2 N、内径11.17 mmとなり、これも受理します。ただし以後の計算で同じgを使っていることを確認します。 / Accept g = 9.8 variants if used consistently.

## T7 モーターと減速機の計算 / Motor and reducer calculation

**期待される答え / Expected answers**

| # | 量 / Quantity | 式と代入 / Formula and substitution | 答え / Answer |
|---|---|---|---|
| 1 | 角速度 / angular velocity | 2π × 1,200 ÷ 60 | **125.66 rad/s** |
| 2 | 軸トルク / motor torque | 60 ÷ 125.66 | **0.477 N·m** |
| 3 | 出力回転数 / output speed | 1,200 ÷ 20 | **60.0 rpm** |
| 4 | 理想出力トルク / ideal torque | 0.477 × 20 | **9.55 N·m** |
| 5 | 効率込み / delivered torque | 0.477 × 20 × 0.90 | **8.59 N·m** |
| 6 | 出力動力 / output power | 8.59 × (2π × 60 ÷ 60) | **54.0 W** |

- 効率込みの動力は 60 × 0.90 = 54 W でも一致します。速度はそのまま、トルクだけが0.90倍になる、という関係です。 / The delivered power also equals 60 × 0.90 = 54 W: speed is unchanged and torque is scaled by 0.90.
- 9.55 N·mは効率を1.0と置いた理想値、8.59 N·mは効率0.90を明示した値です。差は約0.95 N·m（約10 %）。 / 9.55 is the ideal value at efficiency 1.0; 8.59 uses the stated 0.90. The difference is about 0.95 N·m, roughly 10 %.

**重要な注意 / Essential caution**

この計算は「定格動力から軸トルクを出す」変換であり、負荷トルクと比較していません。8.59 N·mが出せることは、その機械を動かせることを意味しません。負荷トルク、慣性、加減速時間、起動停止回数、保持ブレーキの要否を別に確認します。

This converts rated power into shaft torque; it does not compare the result with the load torque. Being able to deliver 8.59 N·m does not prove the machine can be driven. Load torque, inertia, acceleration time, start-stop frequency and the need for a holding brake must be checked separately.

**よくある誤り / Common mistakes**

- ωを rpm のまま使い、トルクが 60 ÷ 1,200 = 0.05 N·m になる。 / Using rpm instead of rad/s.
- 減速比を掛けずに9.55 N·mを「出力トルク」と書く。 / Reporting the motor torque as the output torque.
- 効率をトルクに掛けず、8.59を「効率を考慮した速度」と書く。 / Applying efficiency to speed instead of torque.
- 8.59 N·mを「必要トルクを満たす」と断定する。 / Claiming the value satisfies the load requirement.

**許容範囲 / Acceptable range**

軸トルク0.477〜0.478 N·m、出力回転数60 rpm、理想トルク9.55 N·m、効率込み8.59 N·m、出力動力54 W。π = 3.14 を使った場合は 0.477、9.55、8.60 程度になり、これも受理します。 / Accept small π rounding differences if used consistently.

## T8 機械BOM / Mechanical bill of materials

**期待される内容の例 / Model rows**

| 品名 / Item | 候補仕様 / Candidate spec | 理由 / Reason | 仮定 / Assumption | 未確認 / Open item | 出典・版 / Source and revision |
|---|---|---|---|---|---|
| 複動シリンダ / double-acting cylinder | 内径16 mm級、ストローク100 mm級 / bore class 16 mm, stroke class 100 mm | 理論内径11.18 mmに対し候補 / candidate above the 11.18 mm bound | 圧力0.4 MPa、摩擦0.25 / pressure 0.4 MPa, friction 0.25 | 負荷率、圧力損失、速度 / load factor, pressure loss, speed | 教材の計算例、版A / course example, rev A |
| リニアガイド / linear guide | ワーク8 kg＋押し板を支持 / supports 8 kg plus pusher | 側荷重とモーメントを受ける / carries side load and moment | 重心位置は未測定 / centre of gravity not measured | 許容モーメント、寿命 / allowable moment, life | 版A / rev A |
| 方向切替弁 / directional valve | 5ポート2位置、DC24V級 / 5/2, DC24V class | 前進・後退の切替 / extend and retract | 単一ソレノイド、ばね戻り / single solenoid, spring return | 無通電時の挙動、流量 / de-energised behaviour, flow | 版A / rev A |
| 位置センサー / position sensors | シリンダ用磁気式、2個 / magnetic, qty 2 | 前進端と後退端の確認 / end confirmation | 取付位置は仮 / mounting provisional | 対応シリンダ、応答時間 / compatibility, response | 版A / rev A |
| 速度制御弁 / flow control valves | 排気絞り、2個 / meter-out, qty 2 | 速度調整 / speed adjustment | メータアウトと仮定 / assumed meter-out | メーカー推奨、実機確認 / guidance, real test | 版A / rev A |

**版を上げるときの記録 / Revision records**

日時、変更内容、変更理由、再試験の結果（該当する試験ID）を記録します。古い版は消さずに残し、図面・I/O表・ラダー・試験記録の版番号を対応させます。

Record the date, what changed, why, and the re-test result with its test id. Keep old revisions, and keep drawings, I/O table, ladder and test records on matching revisions.

**よくある誤り / Common mistakes**

- 「未確認」の欄が空、または「なし」と書かれている（未確認は必ず残る）。 / Leaving the open-items column empty or writing "none"; some open items always remain.
- 型式やメーカー名を書く。 / Writing part numbers or manufacturer names.
- 選定理由が「安い」「有名」だけ。 / Reasons such as "cheap" or "well known" only.
- 仮定の欄に、摩擦係数や圧力などの数値の出どころがない。 / No basis for assumed values.

**許容範囲 / Acceptable range**

行数は5行以上。型式ではなく仕様クラスで書かれ、理由・仮定・未確認・出典・版の5欄がすべて埋まっていれば受理します。候補の内径やストロークが違っても、11.18 mmとの関係を説明していれば可。 / Five or more rows, specification classes rather than part numbers, and all five columns filled. A different candidate bore or stroke is acceptable if its relation to 11.18 mm is explained.
