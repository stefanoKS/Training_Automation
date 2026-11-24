# 第7日〜第9日 理解度評価 / Day 7-9 understanding-based assessment

> この評価は「説明できるか」を見ます。提案書の完成度、ネットワーク設計、試運転計画、BOMの作成は評価対象ではありません。
> This assessment checks whether the trainee can **explain**. Proposal quality, network design, commissioning plans and BOM creation are not assessed.

## 1. 評価の構成 / what is assessed

| 観点 / Area | 重み / Weight | 見る内容 / What is checked |
|---|---:|---|
| ことばの正確さ / accurate terminology | 25% | タクトとサイクル、質量と力、NPN/PNP、精度と繰返し精度など / takt vs cycle, mass vs force, NPN/PNP, accuracy vs repeatability |
| 計算の再現 / reproducing calculations | 25% | 式・代入・単位・答えが一致する / formula, substitution, unit, answer |
| 図の読解 / reading a diagram | 20% | 電流経路、信号の流れ、構成図を説明できる / current path, signal flow, architecture |
| 安全性の区別 / safety distinction | 15% | 通常制御と安全機能を混同しない / ordinary control versus safety functions |
| 限界の説明 / stating limits | 15% | 計算値が選定・保証ではないと言える / a calculation is not a selection or a guarantee |

## 2. 到達レベル / levels

| レベル / Level | 目安 / Description |
|---|---|
| A（十分 / secure） | 主要な用語・計算・図を、自分の言葉で正確に説明できる。限界も言える。 / Terms, calculations and diagrams explained accurately in own words, including limits. |
| B（おおむね十分 / mostly secure） | 計算はできるが、限界の説明が不足する、または用語に一部混同がある。 / Calculations correct, with gaps in limits or terminology. |
| C（要復習 / needs review） | 用語の混同が複数、または単位・式の誤りがある。 / Several terminology confusions, or errors in units or formulas. |
| D（未到達 / not yet） | 計算の再現ができず、安全と通常制御の区別も説明できない。 / Cannot reproduce the calculations or distinguish safety from ordinary control. |

## 3. 確認質問の例 / example check questions

### 第7日 / Day 7

1. タクトタイムとサイクルタイムの違いを、単位を付けて説明してください。 / Explain takt time and cycle time with units.
2. 3600 ÷ 15 が「240 個/時」になる条件を言ってください。 / Under what condition is 3600 ÷ 15 equal to 240 pieces/hour?
3. 8 kg の物体にはたらく重力は何 N ですか。 / What is the weight force of 8 kg?
4. 油圧が「いつも強い」と言えない理由を1つ。 / Give one reason hydraulics is not always stronger.
5. 11.18 mm が最終選定でない理由を2つ。 / Two reasons 11.18 mm is not a final selection.

### 第8日 / Day 8

1. 遮断器とサーマルリレーの守る範囲の違いを説明してください。 / Explain breaker versus overload relay.
2. PNPセンサーとNPNセンサーの電流経路を、+24Vと0Vから書いてください。 / Draw PNP and NPN current paths.
3. 入力共通が0Vのとき、適合するのはどちらですか。 / Which sensor suits a 0V input common?
4. 基本の自己保持回路で、STOP許可が戻るとRUNが戻るのはなぜですか。 / Why does basic seal-in restore RUN when permission returns?
5. 同時要求を「両方OFF」にする理由を説明してください。 / Why reject simultaneous requests?

### 第9日 / Day 9

1. 視野240 mm、1,920 px のときの1ピクセルの実寸を計算してください。 / Calculate the sampling.
2. ぶれが8 px になる条件を説明してください。 / Explain the conditions for 8 px of blur.
3. グローバルシャッターで「ゆがみは減るがぶれは減らない」理由を説明してください。 / Why does a global shutter remove skew but not blur?
4. 透明シートの内部異物に、バックライトが候補になる理由。 / Why is backlight a candidate for internal contamination?
5. 通信が切れたときに「OKで流す」のが危険な理由。 / Why is "pass as OK" dangerous when the link fails?

## 4. 評価の記録 / recording

| 観点 / Area | A | B | C | D | コメント / comment |
|---|---|---|---|---|---|
| ことば / terminology | | | | | |
| 計算 / calculations | | | | | |
| 図 / diagrams | | | | | |
| 安全 / safety | | | | | |
| 限界 / limits | | | | | |

**講師記入 / instructor:** 氏名 / name、日付 / date、総合 / overall。
