# 第7日 講師ガイド / Day 7 Instructor Guide
**自動化設備の構想・機械設計 / Automation Planning and Mechanical Design**

第7〜9日コースの初日です。要求仕様から能力計算、機械構成、空圧、シリンダ・モーター選定までを、小型ワーク押出し装置1題で通します。
The first day of this three-day block. Requirements, capacity, machine architecture, pneumatics, cylinder and motor selection are taught through one running example, the small workpiece-pushing machine.

対象 / audience: 初学者。電気・PLC・機械設計の予備知識は前提にしません。 / Beginners; no prior electrical, PLC or machine-design knowledge.
教材 / material: `notebooks/Day07_Automation_Concept_Mechanics/`（01–03 の `.md` と `.ipynb`）、`assets/diagrams/day07/`、`day07_09_support/`、`docs/pdf/Day07_explanation_ja_en.pdf`。
実機・空圧・PLCがなくても、このガイドだけで1日教えられます。 / The day is teachable with this guide alone, without a real machine, compressed air or a PLC.

## 1. 学習目標 / Learning objectives

1. 自動化と機械化を区別し、設備開発の8段階を成果物とともに説明できる。 / Distinguish mechanisation from automation and map the eight development stages to their deliverables.
2. ECRS（なくす・まとめる・順序を変える・簡単にする）で、設備購入前に作業を減らす案を作れる。 / Apply ECRS (eliminate, combine, rearrange, simplify) before capital investment.
3. 420分・600個からタクト **42秒/個**、15秒サイクル・稼働率0.85・良品率0.98から実力能力 **199.92個/時** を計算できる。 / Calculate a **42 s/piece** takt from 420 min and 600 pieces, and **199.92 good pieces/h** from a 15 s cycle, 0.85 availability and 0.98 yield.
4. タクト（目標）、サイクル（設備能力）、実力能力（停止・不良を含む出力）を混同しない。 / Keep takt (target), cycle (machine capability) and effective capacity (output after losses) separate.
5. 機械を「動かす・案内する・支える・固定する・保護する」の5機能に分け、空圧回路を空気源からシリンダまで説明できる。 / Divide a machine into move, guide, support, fix and protect, and explain the pneumatic circuit from source to cylinder.
6. 摩擦力 **19.62 N**、設計力 **39.24 N**、理論内径 **約11.18 mm** を計算し、11.18 mmがカタログ選定ではないと説明できる。 / Calculate **19.62 N** friction, **39.24 N** design force and a **theoretical 11.18 mm** bore, and explain that this is not a catalogue selection.
7. モーター軸トルク **0.477 N·m**、減速比20:1で **60 rpm**、理想トルク **9.55 N·m**、効率0.90の仮定で **8.59 N·m** を計算できる。 / Calculate **0.477 N·m** motor torque, **60 rpm** and **9.55 N·m** ideal output at 20:1, and **8.59 N·m** at an assumed efficiency of 0.90.
8. BOMに候補・理由・仮定・未確認・出典・版を残し、危険源と保護方策の方向性を書ける。 / Record candidate, reason, assumptions, open items, source and revision in a BOM, and state hazards and the direction of protective measures.

## 2. 前提知識 / Prerequisites

- 小学校レベルの算数（割り算、πの概算、単位換算）。 / Primary-school arithmetic, including division, π and unit conversion.
- 質量 kg と力 N、圧力 MPa と Pa の違いを、その場で確認する意欲。 / Willingness to check the difference between mass in kg and force in N, and between MPa and Pa.
- 第7日01の5用語（生産時間、タクト、サイクル、稼働率、良品率）。 / The five terms introduced in 07-01: production time, takt, cycle, availability and yield.

不要 / not required: 電気工学、PLC、空圧機器の実務経験、CAD、実機の型番知識。 / No electrical engineering, PLC, pneumatic practice, CAD or real part-number knowledge.
注意 / caution: 第1〜6日のAI・画像の内容は、この日の計算の前提ではありません。 / The Day 1–6 vision content is not a prerequisite for today's calculations.

## 3. 当日の時間割 / Exact daily timetable

`COURSE_SYLLABUS_DAY07_09.md` の第7日の行をそのまま使います。 / These are the Day 7 rows of `COURSE_SYLLABUS_DAY07_09.md`, unchanged.

| 時刻 / Time | 分 / min | 活動 / Activity | 区分 / Type |
|---|---:|---|---|
| 08:00–09:00 | 60 | 講師：押出し装置の全体像、要求から設計への流れ / Instructor: the pusher machine and the path from requirements to design | 講師 / instructor |
| 09:00–10:20 | 80 | 07-01 要求仕様と構想の作り方 / 07-01 Requirements and Concept Development | 必須 / required |
| 10:20–10:35 | 15 | 休憩 / Break | 休憩 / break |
| 10:35–12:00 | 85 | 07-02 機械構成と空圧システム / 07-02 Mechanical Architecture and Pneumatics | 必須 / required |
| 12:00–12:50 | 50 | 昼食 / Lunch | 昼食 / lunch |
| 12:50–13:50 | 60 | 講師：機械構成図・空圧回路・安全境界の実演 / Instructor: architecture, pneumatic circuit and safety boundary | 講師 / instructor |
| 13:50–15:10 | 80 | 07-03 シリンダ・モーター・機器選定（前半）/ 07-03 Equipment Selection, part 1 | 必須 / required |
| 15:10–15:25 | 15 | 休憩 / Break | 休憩 / break |
| 15:25–16:20 | 55 | 07-03 シリンダ・モーター・機器選定（後半）/ 07-03 Equipment Selection, part 2 | 必須 / required |
| 16:20–16:50 | 30 | 第7日ワークシートと提出 / Day 7 worksheet and submission | 提出 / submission |

**合計 / Totals:** 講師120分、必須300分、休憩30分、昼食50分、提出30分、**530分**。 / Instructor 120, required 300, breaks 30, lunch 50, submission 30, **530 min**.

## 4. 準備チェックリスト / Preparation checklist

- [ ] `COURSE_SYLLABUS_DAY07_09.md`、`day07_09_support/lesson_manifest.json`、`quick_reference_day07.md` を手元に置く。 / Have the syllabus, manifest and Day 7 quick-reference card at hand.
- [ ] ノートブック01–03の `.ipynb` と `.md` を開き、セル順と期待出力（42.00、85.71、240.00、199.92）を確認する。 / Open notebooks 01–03 and check cell order and expected outputs.
- [ ] `day07_09_support/examples/automation_models.py` が存在し、`capacity_report` と `motor_report` が動くこと（本日のシミュレーション）を前日に確認する。 / The day before, confirm that `automation_models.py` exists and that `capacity_report` and `motor_report` run (today's simulation).
- [ ] D07-01〜D07-09 をA3またはA4で印刷。印刷できない場合は `day07_09_support/reference_data/diagram_png/day07/` のPNGを使う。 / Print D07-01 to D07-09, or use the PNGs in `reference_data/diagram_png/day07/`.
- [ ] 学生用ワークシート、講師用解答例、`Day07_09_Assessment_Rubric_ja_en.md` を印刷。解答例は配布しない。 / Print the student worksheet, the instructor answer key and the rubric. Do not distribute the answer key.
- [ ] 電卓（またはスマートフォン）、白板3列、マーカー2色、付箋。 / Calculator, a whiteboard in three columns, two marker colours and sticky notes.
- [ ] オフライン代替：印刷したPDF `docs/pdf/Day07_explanation_ja_en.pdf`、図、電卓、予備PC。ネットワークは不要。 / Offline fallback: the printed PDF, the diagrams, a calculator and a spare PC. No network is needed.
- [ ] 実機・空圧・PLCは用意しない。用意しないことが安全境界の一部である。 / Do not prepare real machinery, compressed air or a PLC; not preparing them is part of the safety boundary.

## 5. 午前の説明シーケンス / Morning explanation sequence

### 5.1 08:00–09:00 全体像と要求から設計へ / Overview and requirements-to-design

| 時刻 / Time | 実演 / Demonstrate | 問い / Ask | 板書 / Board |
|---|---|---|---|
| 08:00–08:10 | D07-06 を映し、ワークの入口・押出し・センサー・弁・ガードを指でなぞる。 / Trace workpiece entry, push, sensors, valve and guard on D07-06. | 「人が触れそうな場所はどこか」 / Where could a hand reach? | 5機能：動かす・案内する・支える・固定する・保護する / five functions |
| 08:10–08:20 | D07-01 の8段階を、成果物と対応させる。 / Map the eight stages of D07-01 to deliverables. | 「図面を描く前に何を決めるか」 / What is decided before drawing? | 課題→要求→構想→比較→設計→製作→試験→引継ぎ / problem→requirements→concept→design→test |
| 08:20–08:32 | 420分・600個→42秒、15秒→240個/時、×0.85×0.98→199.92個/時を実演。 / Work 420 min/600 pcs→42 s, 15 s→240/h, ×0.85×0.98→199.92/h. | 「15秒サイクルは42秒タクトを満たすか」「実力能力は必要能力85.71個/時を満たすか」 / Does 15 s meet 42 s? Does 199.92 meet 85.71? | タクト＝目標、サイクル＝能力、実力＝停止と不良を含む / takt target, cycle capability, effective after losses |
| 08:32–08:42 | D07-02 で、押す前に「押さなくてよい」案を考える。 / Use D07-02 to find a way not to push at all. | 「設備を買う前に消せる作業は何か」 / What work can be eliminated before buying? | E・C・R・S の4列 / four ECRS columns |
| 08:42–08:52 | D07-04 のA/B/Cを、同じ評価軸で並べる。 / Compare A/B/C in D07-04 on the same criteria. | 「各案で人に残る仕事は何か」 / What remains with the human in each option? | A手動・B空圧半自動・C電動全自動 / A manual, B pneumatic, C electric |
| 08:52–09:00 | D07-05 で、悪い受入基準と良い受入基準を比べる。 / Contrast a weak and a strong acceptance criterion on D07-05. | 「測定量・条件・合格範囲・回数は何か」 / What are measurand, condition, pass range and sample size? | 「正確に」→「±2 mm、10回連続」 / "accurate" → "±2 mm, ten cycles" |

**板書レイアウト / board layout:** 左に8段階、中央に42→240→199.92の3行、右に「理論値≠カタログ選定」「安全は別設計」。 / Left: eight stages. Centre: the three capacity lines. Right: "theory ≠ catalogue" and "safety is separate".

### 5.2 12:50–13:50 機械構成・空圧・安全境界の実演 / Architecture, pneumatics and safety boundary

| 時刻 / Time | 実演 / Demonstrate | 問い / Ask | 板書 / Board |
|---|---|---|---|
| 12:50–13:00 | 朝の3問を口頭で確認：タクトとサイクルの違い、199.92の内訳、ECRSのE。 / Orally check three morning points. | 「タクトを速くするのと稼働率を上げるのは、どちらが効くか」 / Which helps more, a faster takt or higher availability? | 3行の計算を再掲 / rewrite the three lines |
| 13:00–13:15 | D07-06 で、ガイドが荷重とモーメントを受け、ロッドは軸力だけを出すと説明。 / Show that the guide carries load and moment while the rod carries axial force. | 「長い押し板をロッドに直付けすると、どこが壊れるか」 / What fails if a long plate is fixed directly to the rod? | ガイド＝案内、ロッド＝軸力、側荷重はガイドへ / guide vs rod |
| 13:15–13:32 | D07-07 を、空気源→遮断→フィルタ・レギュレータ→方向弁→速度制御→シリンダの順に指す。 / Trace D07-07 in order. | 「遮断しただけで残圧は抜けるか」「無通電なら安全か」 / Does isolation release stored pressure? Is de-energised safe? | 遮断＋排気＋圧力計、無通電≠安全 / isolate, bleed, gauge; de-energised ≠ safe |
| 13:32–13:42 | D07-08 で、20 N×100 mm＝2.0 N·m を暗算。 / Compute 20 N × 100 mm = 2.0 N·m from D07-08. | 「このモーメントを誰に持たせるか」 / Who should carry this moment? | M＝F×L、単位 N·m / M = F × L |
| 13:42–13:50 | D07-09 で、19.62→39.24→11.18 mm を1回だけ計算。 / Work 19.62→39.24→11.18 mm once on D07-09. | 「11.18 mmを超える最小の内径を選べばよいか」 / Should we simply choose the smallest bore above 11.18 mm? | D=√(4F/πP)、理論下限 / theoretical lower bound |

**実演で避けること / avoid:** シリンダへの給気、電磁弁の通電、実機の動作。図と計算で代替する。 / Supplying air, energising a valve or moving real equipment; use diagrams and calculations instead.

## 6. 午後のフォロー / Afternoon follow-up

### 6.1 朝の復習の仕方 / How to review the morning (12:50–13:00)

1. 白板を消し、学生に42秒と199.92個/時の式を言わせる。言えない場合は隣の学生と30秒相談させる。 / Erase the board and have students state the two formulas; allow 30 s of pair discussion if needed.
2. 「タクトは目標、サイクルは設備、実力能力は停止と不良を含む」を、学生の言葉で言い換えさせる。 / Ask students to paraphrase the three definitions.
3. ECRSのEの例を1つ、今日の押出し作業から挙げさせる。 / Ask for one Eliminate example from today's push task.
4. 誤答は消さずに残し、午後の該当箇所で戻る。 / Keep wrong answers on the board and return to them at the relevant afternoon point.

### 6.2 13:50以降のチェックポイント / Checkpoints after 13:50

| 時刻 / Time | 確認すること / Check | 合図 / Signal |
|---|---|---|
| 13:50–14:20 | `cylinder-calculator` の19.62、39.24、11.18が出たか。 / Are 19.62, 39.24 and 11.18 correct? | 3つの数字を机間で確認 / check the three numbers at desks |
| 14:20–15:10 | 押し側と戻り側の差を、ロッド断面積で説明できるか。 / Can they explain the push/pull difference by rod area? | 125.7 Nと105.6 Nを板書させる / have them write 125.7 and 105.6 |
| 15:25–15:50 | `motor-calculator` の0.477、60.00、9.55、8.59が出たか。 / Are 0.477, 60.00, 9.55 and 8.59 correct? | 4つの数字を確認 / check four numbers |
| 15:50–16:10 | BOMに仮定・未確認・出典・版が入っているか。 / Does the BOM include assumptions, open items, source and revision? | 1行を指名して読ませる / have one row read aloud |
| 16:10–16:20 | 提出物がそろっているか（現状課題、能力、3案、要求、リスクを含む）。 / Are the deliverables present, including the five core items? | 机間チェック / desk check |

### 6.3 探るべき誤り / Common errors to probe

| 誤り / error | 問い / probe | 正しい説明 / correction |
|---|---|---|
| タクトとサイクルを同じ表に入れる / takt and cycle in one cell | 「42秒は誰の目標か」 / Whose target is 42 s? | タクトは要求、サイクルは設備の実時間。 / Takt is the requirement; cycle is the machine's actual time. |
| 240個/時を能力と答える / calls 240 the capacity | 「停止と不良はどこに入ったか」 / Where are downtime and defects? | 240は理論値。実力は×0.85×0.98で199.92。 / 240 is theoretical; effective is 199.92. |
| 11.18 mmをそのまま選ぶ / selects 11.18 mm directly | 「負荷率・速度・偏荷重・圧力損失は確認したか」 / Checked load factor, speed, side load, pressure loss? | 理論下限であり、候補選定ではない。 / It is a lower bound, not a selection. |
| 供給圧をそのまま推力計算に使う / uses supply pressure | 「シリンダに実際にかかる圧は同じか」 / Is the pressure at the piston the same? | 配管・弁・速度制御で低下し得る。 / It can drop through piping, valves and flow control. |
| 無通電＝安全と書く / writes de-energised = safe | 「負荷・弁型式・残圧はどうか」 / What about load, valve type and stored pressure? | 無通電でも動く場合がある。遮断・排気・零確認が別に必要。 / Motion is possible; isolation, bleed and verification are separate. |
| 点数が高い案を無条件で採用 / selects the highest score | 「必須の安全要求を満たすか」 / Does it meet mandatory safety? | 必須要求を満たさない案は、点数に関係なく不採用。 / An option that fails a mandatory requirement is rejected regardless of score. |

## 7. 必要な図 / Required figures

すべて `assets/diagrams/day07/` のSVG。印刷用PNGは `day07_09_support/reference_data/diagram_png/day07/`。 / All are SVGs in `assets/diagrams/day07/`; print PNGs are in `reference_data/diagram_png/day07/`.

| 図 / Figure | 使用ノート / Lesson | 教えること / What it teaches | 使い方 / Use |
|---|---|---|---|
| D07-01 | 07-01 | 設備開発の8段階と成果物 / eight stages and deliverables | 08:10の全体像、提出物の対応 / overview and deliverable mapping |
| D07-02 | 07-01 | ECRSで押出し作業を見直す / ECRS on the push task | 「買う前に消す」討論 / discussion before investment |
| D07-03 | 07-01 | タクト・サイクル・実力能力 / takt, cycle, effective capacity | 42秒と199.92個/時の板書 / board the numbers |
| D07-04 | 07-01 | 手動・空圧・電動の3案比較 / three concepts | 同じ評価軸での比較 / same-criteria comparison |
| D07-05 | 07-01 | 要求から受入までの流れ / requirement to acceptance | 良い受入基準の作成 / write a measurable criterion |
| D07-06 | 07-02 | 押出し装置の機械構成 / annotated architecture | 5機能と危険源の指差し / five functions and hazards |
| D07-07 | 07-02 | 機能的な空圧回路（概念）/ functional pneumatic circuit | 空気源からシリンダまでの順序 / source-to-cylinder order |
| D07-08 | 07-02 | ガイドと側荷重 / guides and side load | モーメント2.0 N·mの計算 / moment calculation |
| D07-09 | 07-03 | 力のつり合いと内径選定 / free body and bore selection | 19.62→39.24→11.18の計算 / the bore calculation |

補足 / note: D07-07は概念図であり、配管・継手・弁型式・安全設計を確定しない。 / D07-07 is conceptual; it does not fix piping, fittings, valve model or safety design.

## 8. シミュレーション / Simulations

本日はHTMLシミュレータを使わず、`automation_models.py` を使うPythonセルで計算を検証します。 / Today uses the Python cells backed by `automation_models.py`, not an HTML simulator.

| ノート / Notebook | セルID / cell id | 観察すること / What to observe |
|---|---|---|
| 07-01 | `capacity` | 42.00 s、85.71個/時、240.00個/時、199.92個/時、両方True / 42.00 s, 85.71/h, 240.00/h, 199.92/h, both True |
| 07-01 | `capacity-sweep` | サイクルを10–55秒に振る。実力能力が必要能力を満たす最後の点は30秒。35秒では85.68個/時でわずかに不足。 / Sweep 10–55 s; the last passing cycle is 30 s; at 35 s the effective rate is 85.68/h, just short. |
| 07-02 | `pneumatic-force` | 内径20 mm・ロッド8 mm・0.4 MPaで押し125.7 N、戻り105.6 N、差20.1 N。 / 125.7 N push, 105.6 N pull, 20.1 N difference. |
| 07-02 | `air-use` | 1サイクル0.286 L、4回/分で1.14 L/分（大気圧換算）。 / 0.286 L/cycle; 1.14 L/min at 4 cycles/min. |
| 07-02 | `side-load-moment` | 20 N、100 mmで2.00 N·m。 / 2.00 N·m at 20 N and 100 mm. |
| 07-03 | `cylinder-calculator` | 19.62 N、39.24 N、11.18 mm、候補16 mmで80.4 N/69.1 N。 / 19.62, 39.24, 11.18 mm; candidate 16 mm gives 80.4/69.1 N. |
| 07-03 | `cylinder-validation` | 負の質量、1未満の余裕係数、負の圧力を拒否する。 / Rejects negative mass, margin below 1 and negative pressure. |
| 07-03 | `motor-calculator` | 0.477 N·m、60.00 rpm、9.55 N·m、8.59 N·m（η=0.90は追加仮定）。 / 0.477, 60.00, 9.55 and 8.59 N·m; 0.90 is an added assumption. |
| 07-03 | `bom-hash` | BOMの1欄を変えると指紋が変わる。指紋は版と一緒に記録する。 / Changing any field changes the fingerprint; record it with the revision. |

**オフラインでの実行手順 / running offline:**
1. リポジトリ内の `notebooks/Day07_Automation_Concept_Mechanics/` からノートブックを開く（`find_support` が親フォルダを探すため）。 / Open the notebook from inside the repository folder so `find_support` can walk up.
2. 最初の `setup` セルを実行し、「automation_models loaded from day07_09_support」を確認する。 / Run the `setup` cell and confirm the message.
3. 上から順に実行する。インターネット、PLC、空圧は不要。 / Run top to bottom; no internet, PLC or compressed air.
4. 数値が違う場合は、前のセルの変数を書き換えていないか、セルを順不同で実行していないかを確認する。 / If numbers differ, check for edited variables or out-of-order execution.
5. `sim_plc_sequence.html` は本日ではなく第8日03で使う。予告として見せる場合も「モデルであり安全PLCではない」と明言し、開き方は第8日ガイド§8.2に従う。 / `sim_plc_sequence.html` belongs to Day 8-03, not today; if previewed, state that it is a model, not a safety PLC, and follow the Day 8 guide §8.2 for how to open it.

## 9. ディスカッション質問 / Discussion questions

1. この装置は「機械化」か「自動化」か。判断の根拠は何か。 / Is this machine mechanisation or automation? What is the evidence?
2. タクト42秒に対してサイクル15秒は、余裕が大きすぎるか、適切か。 / Is a 15 s cycle against a 42 s takt too much margin, or appropriate?
3. 稼働率を0.85から0.70に下げると、実力能力は何個/時か。必要能力を満たすか。 / If availability falls to 0.70, what is the effective capacity? Does it still meet the requirement?
4. ECRSのEで、押出し作業そのものを無くす案を1つ挙げよ。 / Give one Eliminate idea that removes the push task itself.
5. 3案のうち、安全要求を満たさない案を点数で選んでよいか。 / May an option that fails a safety requirement be selected on score?
6. 11.18 mmの次に大きい内径を選ぶ前に、何を確認するか。 / What must be checked before choosing the next bore above 11.18 mm?
7. 押し側と戻り側で推力が違う理由を、面積の式で説明せよ。 / Explain the push/pull force difference with the area formula.
8. 電磁弁のコイルを切ったとき、シリンダが必ず止まるとは限らない理由は何か。 / Why does de-energising a solenoid not guarantee that the cylinder stops?

## 10. よくある誤解と正しい説明 / Likely misunderstandings and correct explanation

| 誤解 / misunderstanding | 正しい説明 / correct explanation |
|---|---|
| タクトタイム＝サイクルタイム / takt equals cycle | タクトは要求数量から決まる目標、サイクルは設備が1個を処理する実時間。 / Takt is the target from demand; cycle is the machine's actual time per piece. |
| 理論能力240個/時が実力 / 240/h is the real output | 実力能力は理論×稼働率×良品率。240×0.85×0.98＝199.92個/時。 / Effective = theoretical × availability × yield = 199.92/h. |
| 11.18 mmを超える最小内径を選べばよい / choose the smallest bore above 11.18 mm | 11.18 mmは1つの単純化条件での理論下限。負荷率・速度・偏荷重・圧力損失・センサー対応を確認して候補を選ぶ。 / It is a lower bound under one simplification; check load factor, speed, side load, pressure loss and sensing. |
| 質量8 kgは力8 N / 8 kg is 8 N | 質量はkg、力はN。8 kgの重力は8×9.81＝78.48 N。 / Mass is kg, force is N; the weight of 8 kg is 78.48 N. |
| 供給圧0.4 MPaがシリンダ圧 / supply pressure is cylinder pressure | 配管・弁・速度制御・内部抵抗で低下し得る。実際の圧力で再計算する。 / It can drop; recalculate with the actual pressure. |
| 無通電＝安全 / de-energised equals safe | 弁型式・負荷・残圧・トラップ空気で動く。遮断・排気・零確認・再起動防止が別に必要。 / Valve type, load, stored pressure and trapped air can move it; isolation, bleed, zero verification and restart prevention are separate. |
| 位置センサーは指令を確認する / a position sensor confirms the command | センサーは「到達したこと」を確認する。指令と確認は別。 / It confirms arrival, not the command. Command and confirmation are different. |
| 通常のPLC停止ラダーは安全機能 / an ordinary PLC stop rung is a safety function | 通常制御と安全機能は別。安全機能はリスクアセスメントに基づく独立した安全関連系で設計・検証する。 / Ordinary control and safety are separate; safety functions need an independent, validated safety-related system based on risk assessment. |

## 11. 演習の解答ガイダンス / Exercise answer guidance

| 演習 / exercise | 期待する解答と数値 / expected answer and key numbers |
|---|---|
| A 現状課題文 / current-state problem | 作業名、3–6手順、回数/日、1回の時間、事実の困りごと、推測原因、未測定項目の7欄。事実と推測を混ぜない。 / Seven fields: task, 3–6 steps, repetitions/day, time per occurrence, factual problem, suspected cause, not-yet-measured. Keep fact and guess separate. |
| B 能力計算 / capacity | 450分・900個→タクト30秒/個。20秒→理論180個/時。180×0.80×0.97＝**139.68個/時**。必要能力900÷7.5＝120個/時。余裕あり。 / Takt 30 s; theoretical 180/h; effective **139.68/h**; required 120/h; sufficient. |
| C 3案比較 / three concepts | 重みの合計を1.0にし、各案の採用理由と却下理由を両方書く。必須の安全要求を満たさない案は点数が高くても不採用。 / Weights sum to 1.0; state why each option is accepted or rejected; a mandatory safety failure rejects an option regardless of score. |
| D 要求仕様と受入基準 / requirements and acceptance | 能力・品質・停止・異常・保全の各1件に、測定量・条件・合格範囲・測定回数を入れる。仮値は「仮」と明記。 / One criterion each for capacity, quality, stopping, faults and maintenance; include measurand, condition, pass range and sample size; mark provisional values. |
| E 初期リスクリスト / initial risk list | 3か所以上の接近箇所に、「なくす・離す・守る・知らせる」の方向を書く。危険源と対策の方向であり、安全設計の完成ではない。 / At least three exposure points with eliminate/separate/guard/inform; this is a direction, not a completed safety design. |
| 追加計算（発展）/ extension | 余裕係数3なら設計力**58.86 N**、0.4 MPaで理論内径**13.69 mm**。圧力0.3 MPaなら39.24 Nで**12.91 mm**。 / Margin 3 gives **58.86 N** and a **13.69 mm** bore at 0.4 MPa; at 0.3 MPa, 39.24 N gives **12.91 mm**. |
| モーター（07-03 D）/ motor | 60 W・1200 rpm→**0.477 N·m**。20:1→**60 rpm**、理想**9.55 N·m**、η=0.90で**8.59 N·m**。 / **0.477 N·m**, **60 rpm**, **9.55 N·m** ideal and **8.59 N·m** at 0.90. |

**ワークシート／解答例との対応 / worksheet and answer-key mapping.** 本日の評価対象はノートブック01–03の演習A–Eです。`Day07_Student_Worksheet_ja_en.md` は T1–T6 で同じ演習を扱い、`Day07_Answer_Key_ja_en.md` には計算過程・単位・仮定・よくある誤り・許容範囲が入っています。解答は数値だけでなく、式・代入・単位・仮定・未確認事項がそろっていることを確認してください。旧版の機械構成図・ローラ速度計算は使いません。 / The assessed items are exercises A–E in notebooks 01–03. The current Day 7 worksheet covers them as T1–T6, and the answer key includes the working, units, assumptions, common mistakes and acceptable ranges. Require the formula, substitution, units, assumptions and open items, not a bare number. Do not use the retired component-map or roller-speed items.

## 12. トラブルシューティング / Troubleshooting

| 症状 / symptom | 確認 / check | 対応 / action |
|---|---|---|
| 学生がコードを実行できない / code will not run | ノートブックをリポジトリ内から開いたか、`setup` を実行したか、カーネルは正しいか / opened inside the repo, `setup` run, correct kernel? | `find_support` の `FileNotFoundError` ならフォルダを移動して開き直す。`automation_models.py` の存在を確認。 / If `find_support` raises, reopen from the correct folder and check the module path. |
| 日本語フォントが無い・文字が□になる / missing font, tofu boxes | Matplotlibの警告、`Meiryo`/`Yu Gothic`/`DejaVu Sans` の有無 / warnings and available fonts | フォントを入れるか、英語ラベルで代用。数値と式は変わらないと説明。 / Install a Japanese font or use the English labels; the numbers and formulas are unchanged. |
| ノートブックが古い・出力が違う / stale notebook or outputs | `.ipynb` と `.md` の版、`day07_09_source_sha256`、実行順 / source revision and execution order | `.md` を正とし、`.ipynb` を開き直して上から実行。保存で上書きしない。 / Treat `.md` as truth; reopen and run top to bottom; do not overwrite. |
| 数値が42/199.92にならない / numbers differ | セルの変数を書き換えたか、途中のセルを飛ばしたか / edited variables or skipped cells? | カーネルを再起動し、「すべて実行」。期待出力と比較。 / Restart the kernel, Run All and compare with the expected output. |
| SVG・PDFが表示されない / SVG or PDF not shown | 相対パス、ブラウザ、ローカルファイルの許可 / relative path, browser, local-file permission | 印刷PNGまたはPDFを使う。Chrome/Edgeで開く。 / Use the printed PNG or PDF; open in Chrome or Edge. |
| Matplotlibが無い / matplotlib missing | 仮想環境、`pip list` / virtual environment | オフラインなら印刷済みの期待出力を使い、計算は手計算で確認。 / Offline, use the printed expected outputs and verify by hand. |

## 13. 安全上の制約 / Safety restrictions

- 実機の配線・通電・PLC書込み・空圧供給・シリンダ動作・安全回路の調整を**行わない**。 / No real wiring, energisation, PLC download, compressed-air supply, cylinder motion or safety-circuit adjustment.
- 実機作業は、リスクアセスメント、事前承認、電気的・空圧的隔離、残留エネルギー確認、ガード、有資格者の監督、復旧手順が揃った別枠でのみ行う。 / Real work is a separate, supervised activity with risk assessment, prior approval, electrical and pneumatic isolation, stored-energy verification, guarding, qualified supervision and recovery procedures.
- 残圧は遮断だけでは抜けない。遮断・排気・圧力計での零確認を一組で扱う。 / Isolation alone does not release stored pressure; isolate, bleed and verify zero together.
- **無通電は安全状態を保証しない。** 負荷・弁型式・トラップ空気で動く場合がある。 / **De-energised does not guarantee a safe state**; load, valve type and trapped air can still cause motion.
- **通常のPLC制御は安全機能ではない。** 停止ラダーを非常停止や人身安全の代用にしない。 / **Ordinary PLC control is not a safety function**; a stop rung must not substitute for emergency stopping or personal safety.
- 本日の図は概念図であり、規格適合・実機設計・部品選定を証明しない。 / Today's diagrams are conceptual and prove neither compliance nor a real design or part selection.

## 14. オフライン代替活動 / Offline alternative activities

PCが使えない場合でも、必須内容は次の活動で届けられます。 / If the PCs fail, the required content can still be delivered.

1. D07-01〜D07-09 の印刷を配り、8段階・5機能・空圧の順序を指差しで説明させる。 / Hand out printed diagrams and have students point to the stages, functions and circuit order.
2. 42秒、199.92個/時、19.62 N、39.24 N、11.18 mm、0.477 N·m、60 rpm、9.55 N·m、8.59 N·m を、電卓と紙で計算する。 / Calculate the nine key values by hand with a calculator.
3. 8段階カードを順に並べ、各段階の成果物を付箋で貼る。 / Order eight stage cards and attach deliverable notes.
4. 空圧回路を白板に書き、遮断・排気・圧力計・方向弁・速度制御・シリンダを学生に配置させる。 / Draw the pneumatic circuit and have students place the components.
5. 3案比較を模造紙に書き、重みと必須条件を分けて討論する。 / Put the three-concept comparison on paper and debate weights versus mandatory requirements.
6. 提出物は紙で作成し、16:20–16:50に回収する。 / Produce the deliverables on paper and collect them at 16:20–16:50.

## 15. 評価基準 / Assessment criteria

`Day07_09_Assessment_Rubric_ja_en.md` は8観点・100点のコース共通ルーブリックです。本日は特に、観点1（要求と受入基準、12点）、観点2（機械の計算と選定根拠、15点）、観点4（PLC・ラダー・シーケンス、15点）、観点8（最終提案、10点）を中心に、全日の証跡と合わせて評価します。合格は60点以上かつ必須是正なしです。以下の表は本日の形成的確認であり、ルーブリックの代用ではありません。 / The course rubric has eight criteria and 100 points. For this day, focus on criterion 1 (requirements and acceptance, 12), criterion 2 (mechanical reasoning, 15), criterion 4 (PLC/ladder/sequence, 15) and criterion 8 (final proposal, 10), assessed together with the other days' evidence. Pass requires at least 60 points and no mandatory remediation. The table below is a formative check, not a substitute for the rubric.

| 観点 / criterion | 3以上（合格）の目安 / adequate or better |
|---|---|
| 用語 / terminology | タクト、サイクル、実力能力、理論推力、理論内径を区別して使う。 / Uses takt, cycle, effective capacity, theoretical force and theoretical bore distinctly. |
| 技術 / technical | 単位付きで42、199.92、19.62、39.24、11.18、0.477、60、9.55、8.59を再現し、仮定を書く。 / Reproduces the nine values with units and states assumptions. |
| 安全 / safety | 危険源を挙げ、保護方策を方向として書き、通常PLCと安全機能を分ける。 / Lists hazards, writes protective direction and separates ordinary PLC from safety functions. |
| 明確さ / clarity | 日本語と英語で、初学者が手順を再現できる。 / A beginner can reproduce the work in Japanese and English. |

**必須提出物 / required evidence:** 現状課題文、能力計算、3案比較、初期リスクリスト、要求仕様（初版）、機械構成図、空圧部品表、シリンダ・モーター計算書、機械BOM。 / Current-state problem, capacity calculation, three-concept comparison, initial risk list, preliminary requirements, machine architecture, pneumatic BOM, cylinder and motor calculations, and mechanical BOM.

**必須改善項目 / mandatory remediation items**（1つでも該当したら再提出 / resubmit if any apply）:
1. タクトとサイクル、または理論能力と実力能力を混同している。 / Confuses takt with cycle, or theoretical with effective capacity.
2. 11.18 mmをカタログ選定として扱っている。 / Treats 11.18 mm as a catalogue selection.
3. 単位なしの計算、式と値の不一致。 / Unit-free calculation or formula-value mismatch.
4. 受入基準に測定量・条件・合格範囲・回数が欠けている。 / Acceptance criterion lacks measurand, condition, pass range or sample size.
5. 通常のPLC停止を安全機能と書いている、または実機の安全を確認したと主張している。 / Calls an ordinary PLC stop a safety function, or claims real safety verification.

**評定 / judgement:** ルーブリックの合計60点以上、かつ必須改善項目に該当しないことを合格とします。形成的確認の4観点は、4段階のうち3以上を目安にしてください。 / Pass requires a rubric total of at least 60 and no mandatory remediation item. For the formative check, aim for at least 3 on each of the four rows.

## 16. 遅れている学生へのガイダンス / Guidance for students who fall behind

優先順位は「要求と能力 → シリンダ → モーター → 提出物」です。時間配分は設計値であり、実測された完了時間ではありません。 / Prioritise requirements and capacity, then cylinder, then motor, then deliverables. The allocations are design values, not measured completion times.

**必ず残す / keep (required):**
1. 07-01 §8：42秒/個と199.92個/時、タクトと実力能力の区別。 / 42 s and 199.92/h, and the distinction between them.
2. 07-03 §5：19.62 N、39.24 N、11.18 mm、理論下限とカタログの区別。 / 19.62 N, 39.24 N, 11.18 mm and the theory-versus-catalogue distinction.
3. 07-03 §7：0.477 N·m、60 rpm、9.55 N·m、8.59 N·m。 / The four motor values.
4. 提出物のうち、現状課題文、能力計算、要求仕様、初期リスクリスト。 / Current-state problem, capacity calculation, requirements and risk list.
5. 安全境界の確認：実機の通電・空圧・動作を行っていないこと。 / Confirmation that no real energisation, air or motion took place.

**後回し・省略してよい / defer or drop (optional):**
- `capacity-sweep` のグラフ読解と35秒付近の境界討論。 / The capacity-sweep chart and the 35 s boundary discussion.
- `bore-curve`、`motor-curve` の曲線比較。 / The bore and motor curve comparisons.
- BOMの指紋（`bom-hash`）と版管理の深掘り。 / The BOM fingerprint and deep revision-control work.
- メーカー資料のURL確認、追加の感度分析、4案目以降の比較。 / Manufacturer URL checks, extra sensitivity and fourth-concept comparison.

**声かけ / what to say:** 「11.18 mmは答えではなく下限です。今日は主要な数字と、その仮定を言えれば前に進めます。」 / "11.18 mm is a lower bound, not the answer. If you can state the key numbers and their assumptions, you can move on."
