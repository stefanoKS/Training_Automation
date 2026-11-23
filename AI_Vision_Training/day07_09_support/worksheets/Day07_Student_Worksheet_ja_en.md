# 第7日 学生ワークシート：要求から機械選定まで / Day 7 Student Worksheet: From Requirements to Machine Selection

氏名 / Name: ________________________________　日付 / Date: ____________________

所属・班 / Group: ____________________________　講師 / Instructor: ______________

**推定時間 / Estimated time:** 90分。ノートブックの演習中に下書きし、16:20–16:50の提出時間30分で仕上げます。 / 90 minutes, drafted during the notebook exercises and finished in the 30-minute submission slot.

**対象の原稿 / Source notebooks:** `Day07_01_Requirements.md`（07-01）、`Day07_02_Mechanical_Architecture.md`（07-02）、`Day07_03_Equipment_Selection.md`（07-03）。数値は `day07_09_support/examples/automation_models.py` の同じ関数で再現できます。 / The tasks match these three manuscripts; the numbers can be reproduced with that module.

**安全境界 / Safety boundary:** 本ワークシートは机上の設計演習です。実機の配線、通電、圧縮空気の供給、シリンダの動作、安全機能の検証は行いません。実機作業は、リスクアセスメント、事前承認、電気的・空圧的隔離、残留エネルギー確認、ガード、有資格者の監督、復旧手順がそろった場合にだけ、別の機会に行います。インターネット、PLC、実機、圧縮空気は不要です。

This worksheet is a desk design exercise. It does not involve real wiring, energisation, compressed-air supply, cylinder motion or safety-function validation. Real work is a separate activity that requires a risk assessment, prior approval, electrical and pneumatic isolation, stored-energy verification, guarding, qualified supervision and a recovery procedure. No internet, PLC, real machine or compressed air is needed.

**記入のきまり / How to fill this in**

- 数値には必ず単位を付け、仮定した値には「仮」と書きます。 / Always give units and mark assumed values as hypothetical.
- 計算は「式 → 代入 → 答え」の順に書き、途中の値を残します。答えだけでは受理しません。 / Write the formula, the substitution and the result, and keep the intermediate values. A bare number is not accepted.
- 実在のメーカー型番は書きません。候補は仕様クラスで書きます。 / Do not write real manufacturer part numbers; describe candidates by specification class.
- 根拠にしたノートブックの節とセルIDを、各課題の参照欄に書き写します。 / Copy the notebook section and cell id you used into the reference line of each task.

## T1 現状課題文 / Current-state problem

*参照 / Reference: 07-01 §6 改善の見つけ方、§7 現状観察、§12 演習A。*

自部署の作業を1つ選び、事実と推測を分けて書きます。「大変そう」は推測であり、事実ではありません。回数と時間は、測った条件（作業者、品種、時間帯）も一緒に残します。

Choose one task from your department and separate facts from assumptions. "It looks hard" is an assumption, not a fact. Record the conditions of each measurement as well: operator, product and time of day.

| 項目 / Item | 記入 / Your answer |
|---|---|
| 作業名 / task | |
| 現在の手順（3〜6段階） / current steps (3–6) | |
| 回数/日 / repetitions per day | |
| 1回の時間（秒） / time per occurrence (s) | |
| 困りごと（事実） / problem as a fact | |
| 推測している原因 / suspected cause | |
| まだ測っていない項目 / not yet measured | |
| 測った条件 / measurement conditions | |

ECRSのうち、設備を買う前に試せる案を1つ書いてください。 / Name one ECRS idea that can be tried before buying equipment.

______________________________________________________________________________

## T2 生産能力の計算 / Capacity calculation

*参照 / Reference: 07-01 §8 タクトと能力、セル `capacity` と `capacity-sweep`。*

次の値は教材用の仮定です。式と単位を示して計算してください。稼働率と良品率は割合（0〜1）で扱い、百分率と混同しないようにします。

The values below are training assumptions. Calculate with formulas and units. Availability and yield are fractions from 0 to 1, not percentages.

- 生産時間 / available production time: **420分**（休憩・昼休みを除いた正味 / net of breaks and lunch）
- 必要数量 / required quantity: **600個**
- 設備サイクル / machine cycle: **15秒/個**
- 稼働率 / availability: **0.85**（仮 / hypothetical）
- 良品率 / good yield: **0.98**（仮 / hypothetical）

| # | 量 / Quantity | 式 / Formula | 計算 / Working | 答え / Answer |
|---|---|---|---|---|
| 1 | タクトタイム / takt time | | | ______ s/個 |
| 2 | 理論能力 / theoretical capacity | | | ______ 個/時 |
| 3 | 実力能力 / effective capacity | | | ______ 個/時 |
| 4 | 必要能力 / required rate | | | ______ 個/時 |
| 5 | サイクルはタクトを満たすか / does the cycle meet takt | | | ______（Yes/No）、利用率 ______ % |
| 6 | 実力能力は必要能力を満たすか / is effective capacity sufficient | | | ______（Yes/No）、余裕 ______ 倍 |

実力能力が必要能力を上回る根拠を、2つの数値を使って一文で書いてください。 / Justify the conclusion with two numbers in one sentence.

______________________________________________________________________________

## T3 3案の比較 / Three-concept comparison

*参照 / Reference: 07-01 §9 方式の比較、セル `option-score`。*

押出し装置について、A手動治具、B空圧半自動、C電動全自動を同じ評価軸で比べます。5点満点（5が有利、1が不利）で採点し、重みの合計を1.00にします。重みは自分で決めますが、なぜその重みにしたかを説明できるようにしてください。

Score the three concepts from 1 (unfavourable) to 5 (favourable) on the same criteria. Choose your own weights so that they sum to 1.00, and be ready to explain the weighting.

| 観点 / Criterion | 重み / Weight | A 手動治具 / manual fixture | B 空圧半自動 / pneumatic semi-auto | C 電動全自動 / electric full-auto |
|---|---:|---:|---:|---:|
| 初期費用 / initial cost | | | | |
| 省人効果 / labour saving | | | | |
| 品種変更 / product change | | | | |
| 停止時の復旧 / recovery after stop | | | | |
| 安全上の論点 / safety | | | | |
| **合計 / total** | **1.00** | | | |

採用する案と理由、採用しない案の理由を書いてください。点数は判断を助ける道具であり、決定そのものではありません。 / State the selected concept and why the others are rejected. A score supports judgement; it is not the decision.

______________________________________________________________________________

______________________________________________________________________________

点数に関係なく満たさなければならない必須条件（安全要求など）を1つ書いてください。 / Name one mandatory requirement that overrides the score.

______________________________________________________________________________

## T4 要求仕様と受入基準 / Requirements and acceptance criteria

*参照 / Reference: 07-01 §10 要求仕様と受入基準、§12 演習D。*

「正確に」「速く」「安全に」は、そのままでは合否を判定できません。測定量、条件、合格範囲、測定回数を決めて、別の人が見ても判定できる形にします。未確定の数値には「仮」と書きます。

"Accurate", "fast" and "safe" cannot be judged as written. Define the measurand, the condition, the pass range and the sample size so that another person can decide. Mark unconfirmed values as hypothetical.

| 分類 / Category | 要求 / Requirement | 測定量 / Measurand | 条件 / Condition | 合格範囲 / Pass range | 回数 / Sample |
|---|---|---|---|---|---|
| 能力 / capacity | | | | | |
| 品質 / quality | | | | | |
| 運転 / operation | | | | | |
| 安全 / safety | | | | | |
| 保全 / maintenance | | | | | |

悪い例「位置決めが正確なこと」を、測定できる受入基準に書き直してください。 / Rewrite "positioning must be accurate" as a measurable acceptance criterion.

______________________________________________________________________________

## T5 初期リスクリスト / Initial risk list

*参照 / Reference: 07-01 §11 構想段階の安全、§12 演習E。*

構想の段階で、人が触れそうな箇所と危険源を挙げます。低減は「なくす → 離す → 守る → 知らせる」の順に考え、最後に残るリスクを記録します。

List the hazards and the places a person could reach at the concept stage. Reduce in the order eliminate, separate, guard, inform, and record the residual risk.

| # | 危険源 / Hazard | 想定する事故 / Possible harm | どこで / Where | 低減の方向 / Reduction direction | 残るリスク / Residual risk |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |

「通常のPLCのSTOPラングは安全機能ではない」と説明できる理由を、一文で書いてください。 / Explain in one sentence why ordinary PLC STOP logic is not a safety function.

______________________________________________________________________________

## T6 シリンダの計算 / Cylinder calculation

*参照 / Reference: 07-02 §7 圧力・受圧面積・推力、07-03 §4–§6、セル `pneumatic-force` と `cylinder-calculator`。*

次の条件で、摩擦力、設計力、理論内径、押し側と戻り側の推力を計算します。圧力はMPaのままでは式に入りません。Paに換算してから代入してください。

Calculate friction, design force, theoretical bore and both push and pull forces. Pressure in MPa must be converted to Pa before substitution.

- 質量 / mass: **8 kg**　摩擦係数 / friction coefficient μ: **0.25**　重力加速度 / g: **9.81 m/s²**
- 余裕係数 / margin factor: **2**（教材の仮定 / teaching assumption）
- 圧力 / gauge pressure: **0.4 MPa**（仮 / hypothetical）
- 比較するシリンダ / comparison cylinder: 内径 **20 mm**、ロッド径 **8 mm**

| # | 量 / Quantity | 式 / Formula | 計算 / Working | 答え / Answer |
|---|---|---|---|---|
| 1 | 摩擦力 / friction force | F = μmg | | ______ N |
| 2 | 設計力 / design force | F × 2 | | ______ N |
| 3 | 理論内径 / theoretical bore | D = √(4F / πP)、PはPa | | ______ mm |
| 4 | 押し側推力 / push force（20 mm） | P × πD²/4 | | ______ N |
| 5 | 戻り側推力 / pull force（20 mm、ロッド8 mm） | P × π(D²−d²)/4 | | ______ N |
| 6 | 押し側と戻り側の差 / difference | | | ______ N |

戻り側の推力が小さくなる理由を、面積の言葉で説明してください。 / Explain in terms of area why the pull side is weaker.

______________________________________________________________________________

理論内径は「理論上の下限」であり、カタログ選定ではない理由を2つ書いてください。 / Give two reasons why the theoretical bore is a lower bound, not a catalogue selection.

______________________________________________________________________________

余裕係数を**3**にした場合の設計力と理論内径、圧力を**0.3 MPa**にした場合の理論内径を計算してください。 / Recalculate with margin 3, and with pressure 0.3 MPa.

| 条件 / Condition | 設計力 / design force | 理論内径 / theoretical bore |
|---|---|---|
| 余裕係数 2、0.4 MPa（上の計算 / from above） | 上の表と同じ / same as above | 上の表と同じ / same as above |
| 余裕係数 3、0.4 MPa | ______ N | ______ mm |
| 余裕係数 2、0.3 MPa | ______ N | ______ mm |

## T7 モーターと減速機の計算 / Motor and reducer calculation

*参照 / Reference: 07-03 §7 モーター・減速機の選定、セル `motor-calculator` と `motor-curve`。*

出力、回転数、減速比、効率から、軸トルクと出力側の速度・トルクを求めます。効率0.90は教材が追加した仮定であり、実機の減速機効率ではありません。

Find shaft torque and output speed and torque from power, speed, ratio and efficiency. The efficiency of 0.90 is an added training assumption, not a real reducer value.

- モーター出力 / motor power: **60 W**　回転数 / speed: **1,200 rpm**
- 減速比 / reduction ratio: **20:1**　効率 / efficiency η: **0.90**（仮 / hypothetical）

| # | 量 / Quantity | 式 / Formula | 計算 / Working | 答え / Answer |
|---|---|---|---|---|
| 1 | 角速度 / angular velocity ω | 2πn/60 | | ______ rad/s |
| 2 | モーター軸トルク / motor torque | T = P/ω | | ______ N·m |
| 3 | 出力回転数 / output speed | n/20 | | ______ rpm |
| 4 | 理想出力トルク / ideal output torque | T × 20 | | ______ N·m |
| 5 | 効率込み出力トルク / delivered torque | T × 20 × 0.90 | | ______ N·m |
| 6 | 効率込み出力動力 / output power | T_out × ω_out | | ______ W |

理想値と効率込みの値の違いは、何を仮定したかで説明できます。一文で書いてください。 / Explain the difference between the ideal and delivered values in one sentence.

______________________________________________________________________________

## T8 機械BOM / Mechanical bill of materials

*参照 / Reference: 07-03 §8 BOMと版管理、セル `bom-hash`。*

部品の一覧には、数量だけでなく、選定理由、仮定、未確認事項、出典、版を残します。後から「なぜこの候補にしたか」を説明できることが重要です。型式は書かず、仕様クラスで書きます。

A BOM records not only quantity but also reason, assumptions, open items, source and revision. Being able to explain later why a candidate was chosen is essential. Use specification classes, not part numbers.

| # | 品名 / Item | 候補仕様 / Candidate spec | 数量 / Qty | 選定理由 / Reason | 仮定 / Assumption | 未確認 / Open item | 出典・版 / Source and revision |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |

版を上げるときに記録する項目を3つ書いてください。 / Name three items to record when the revision changes.

______________________________________________________________________________

## 完了チェックリスト / Completion checklist

- [ ] T1 事実と推測を分けて書いた / separated facts from assumptions
- [ ] T1 ECRSの案を1つ書いた / wrote one ECRS idea
- [ ] T2 タクトタイムを式と単位付きで計算した / calculated takt time with formula and unit
- [ ] T2 実力能力を稼働率と良品率から計算した / calculated effective capacity from availability and yield
- [ ] T3 重みの合計を1.00にし、採用理由と却下理由を書いた / weights sum to 1.00, with accept and reject reasons
- [ ] T4 測定量・条件・合格範囲・回数を入れた / included measurand, condition, pass range and sample size
- [ ] T5 危険源を3つ以上挙げ、低減の方向を書いた / listed at least three hazards with reduction direction
- [ ] T6 摩擦力・設計力・理論内径を単位付きで計算した / calculated friction, design force and bore with units
- [ ] T6 押し側と戻り側の推力差を面積で説明した / explained the push and pull difference by area
- [ ] T7 軸トルク・出力回転数・出力トルクを計算した / calculated torque, output speed and output torque
- [ ] T7 効率0.90が仮定であると書いた / stated that 0.90 is an assumption
- [ ] T8 BOMに理由・仮定・未確認・出典・版を入れた / BOM includes reason, assumptions, open items, source and revision
- [ ] 実機の通電・空圧・動作・安全検証を行っていない / did not energise, pressurise, move or safety-validate real equipment
