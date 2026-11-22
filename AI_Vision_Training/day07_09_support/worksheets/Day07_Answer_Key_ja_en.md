# 第7日 解答例と採点の観点 / Day 7 Answer Key (instructor copy)

**学生には配布しません。 / Do not distribute to students.**

## 1. 部品の識別 / Component identification

受け入れる例 / acceptable examples: 供給ロール（材料を供給）、ガイドローラ（方向と張力）、検査ステーション（撮像）、駆動ローラ（搬送）、巻取り（回収）、カメラ（画像）、照明（見え方）、フレーム（支持）、ベアリング（回転支持）、エンコーダ（移動量）。
Supply roll (feeds material), guide rollers (direction and tension), inspection station (imaging), driven roller (transport), winder (collection), camera (image), lighting (appearance), frame (support), bearing (rotation support), encoder (travel).

採点 / marking: 部品名・役割・位置がそろっていれば1点ずつ。役割が「動く」だけの説明は0.5点。
One point each for name, purpose and location; a purpose such as only "it moves" earns 0.5.

## 2. 信号とエネルギー / Signal and energy

| 例 / example | 信号 / signal | 源 / source |
|---|---|---|
| 材料有無センサ / presence sensor | デジタル / digital | センサ→PLC入力 / sensor → PLC input |
| エンコーダ / encoder | パルス / pulses | エンコーダ→PLC / encoder → PLC |
| モータ / motor | 電力＋指令 / power + command | ドライブ→モータ / drive → motor |
| 照明 / lighting | 電力 / power | 電源 / supply |

## 3. センサの選択 / Sensor selection

- シート有無 / presence: 透過形光電など。透明体では感度・背景・汚れを確認。 / through-beam photoelectric; verify sensitivity, background and contamination for transparent sheet.
- 移動量 / travel: ロータリエンコーダ（測定ローラに取付ける例）。滑りに注意。 / rotary encoder (for example on a measuring roller); watch for slip.
- 「すべての材質を同じように検出できる」と書いた答案は減点。 / Deduct for claiming one sensor detects all materials equally.

## 4. アクチュエータの選択 / Actuator selection

- 搬送 / transport: 誘導モータ＋VFD またはサーボ。連続運転・速度安定・保守で選ぶ。 / induction motor with VFD, or servo; choose by continuous duty, speed stability and maintenance.
- 位置マーク / position mark: 空気圧シリンダまたは電動シリンダ。速度・停止位置・残圧に注意。 / pneumatic or electric cylinder; watch speed, stopping position and stored pressure.

## 5. 速度の計算 / Speed calculation

1. C = π × 120 ≈ **376.991 mm**
2. v = 376.991 × 80 ≈ **30,159.3 mm/min**
3. v ≈ **30.159 m/min**
4. 実測と違う理由 / reasons: 滑り、張力、摩耗、ローラ径の変化、材料の伸び / slip, tension, wear, diameter change, material stretch.

採点 / marking: 式・単位・数値が一致して2点、単位なしは1点。

## 6. 機械の問題 / Mechanical problems

- 振動 / vibration → ぼけ / blur → 小さな傷の見落とし / missed fine defects → 取付剛性・緩み / mount stiffness and looseness.
- しわ / wrinkle → 明暗むら / shading → 誤検出 / false positive → 張力・ローラ平行 / tension and roller alignment.
- 速度変動 / speed variation → 同期ずれ / sync error → 位置ずれ / position shift → エンコーダ・駆動の確認 / check encoder and drive.

## 7. 危険源 / Hazards

例 / examples: ローラ間の巻き込み / nip point、駆動部 / drive、感電 / electric shock、残圧 / stored pressure、高温 / hot surface。
保護 / protection: ガード、インターロック、非常停止、遮断・減圧手順。確認 / verification: 有資格者とリスクアセスメント。
Accept answers that separate guarding/interlocks from AI or ordinary ladder logic.

## 8. 相互作用 / Interactions

例 / example: ベアリング摩耗 → ローラ振れ → 画像ぼけ → 欠陥の見落とし。
Full marks require three distinct steps and a decision-level effect.

## 9. 振り返り / Reflection

例 / example: 「照明や機械が不安定だと、AIの性能だけでは安定した検査にならない」。
Accept any statement that recognises a non-AI cause of inspection instability.

## 採点表 / Marking scheme（合計20点 / total 20）

| 項目 / item | 点 / points |
|---|---:|
| 部品の識別（6部品）/ component identification | 4 |
| 信号とエネルギー / signal and energy | 2 |
| センサ選択と限界 / sensor choice and limits | 3 |
| アクチュエータ選択 / actuator choice | 2 |
| 速度計算（式・単位・値） / speed calculation | 3 |
| 機械の問題と画像 / mechanical effects | 2 |
| 危険源と保護 / hazards and protection | 2 |
| 相互作用と振り返り / interactions and reflection | 2 |

**合格の目安 / pass mark:** 12点以上、かつ「安全」と「AIは安全機能ではない」の記述があること。
12 or more, and the answer must state that safety is separate and AI is not a safety function.
