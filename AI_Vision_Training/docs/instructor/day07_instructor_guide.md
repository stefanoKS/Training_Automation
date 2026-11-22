# 第7日 講師ガイド / Day 7 Instructor Guide
**検査装置の機械構造・センサ・アクチュエータ / Mechanical Structure, Sensors and Actuators**

対象 / audience: 化学品製造部の初学者 / beginners from the Kaseihin manufacturing department
教材 / material: `notebooks/Day07_Machine_Fundamentals/`（原稿とノートブック）、`assets/diagrams/day07/`、`day07_09_support/`
このガイドだけで、実機・産業用カメラ・PLCがなくても授業できます。
This guide lets you teach the whole day without real machinery, an industrial camera or a PLC.

## 1. 学習目標 / Learning objectives

1. 機械・機構・フレーム・アクチュエータ・センサ・制御装置の役割を区別する。 / Distinguish machine, mechanism, frame, actuator, sensor and controller.
2. 回転と直線の動きを、単位付きで説明する。 / Explain rotational and linear motion with units.
3. ローラ径と回転数から公称表面速度を計算し、滑りの仮定を述べる。 / Calculate nominal surface speed from diameter and rpm and state the no-slip assumption.
4. 主要なセンサの種類と信号形式（デジタル・アナログ・パルス）を説明する。 / Explain main sensor types and signal forms.
5. アクチュエータの指令と動力を区別する。 / Separate actuator command from energy.
6. 機械の不安定さが検査画像とAI判定に与える影響を説明する。 / Explain how mechanical instability affects images and AI decisions.
7. 危険源を挙げ、安全は独立した設計分野だと説明する。 / Name hazards and state that safety is an independent discipline.

## 2. 前提知識 / Prerequisites

- 第1〜5日の画像・YOLO・PatchCoreの基礎（用語レベルで可）。 / Day 1–5 basics at terminology level.
- 小学校レベルの算数（割り算、πの概算）。 / Primary-school arithmetic, including π.
- 日本語と英語の読み書き。 / Reading and writing in Japanese and English.

不要 / not required: 電気工学、PLC、機械設計、光学の予備知識。

## 3. 時間割 / Exact timetable

| 時刻 / time | 分 / min | 内容 / content | 区分 / type |
|---|---:|---|---|
| 08:00–09:00 | 60 | 講師：実機写真と図で全体像、安全の境界 / overview and safety boundaries | 講師 / instructor |
| 09:00–10:20 | 80 | 07-01 機械の基礎 / mechanical fundamentals | 必須 / required |
| 10:20–10:35 | 15 | 休憩 / break | 休憩 / break |
| 10:35–12:00 | 85 | 07-02 センサと信号 / sensors and signals | 必須 / required |
| 12:00–12:50 | 50 | 昼食 / lunch | 昼食 / lunch |
| 12:50–13:50 | 60 | 講師：アクチュエータ実演と安全の境界 / actuators and safety | 講師 / instructor |
| 13:50–15:10 | 80 | 07-03 アクチュエータと機械構成（前半） / actuators, part 1 | 必須 / required |
| 15:10–15:25 | 15 | 休憩 / break | 休憩 / break |
| 15:25–16:20 | 55 | 07-03（後半）と構成要素表 / part 2 and component table | 必須 / required |
| 16:20–16:50 | 30 | 機械構成図ワークシート / component map worksheet | 提出 / submission |

**合計 / total 530分。講師120・必須300・休憩30・昼食50・提出30。**
**530 min: instructor 120, required 300, breaks 30, lunch 50, submission 30.**

## 4. 午前の講師説明 / Morning instructor presentation（08:00–09:00）

1. 実機写真または図 D07-01 を大きく映し、「材料はどこから入り、どこで検査され、どこへ出るか」を学生に指で示させる（5分）。 / Show D07-01 and ask students to point to material entry, inspection and exit.
2. 機械・センサ・制御・計算・安全の5層を板書し、各層の部品を一つずつ挙げさせる（10分）。 / Write the five layers and have students name one part each.
3. 「機械が不安定だとAIはどうなるか」を問い、意見を3つ板書（10分）。 / Ask what happens to AI when mechanics are unstable.
4. ローラ速度の式を、単位とともに一度だけ実演（10分）。 / Demonstrate the roller-speed formula once with units.
5. 安全の境界を明示：AIの良否判定は品質対応であり安全機能ではない（10分）。 / State that AI decisions are quality responses, not safety functions.
6. 質問を受け、午前のノートブックの進め方を説明（15分）。 / Take questions and explain the notebook flow.

**板書の例 / board layout:** 左に5層、中央にD07-01の模式図、右に「速度 = 円周 × 回転数」「滑りなしの仮定」。

## 5. 午後の講師実演 / Afternoon demonstration（12:50–13:50）

- **実演A（15分）**：`simulations/sim_roller_speed.html` で径と回転数を変え、値が比例することを見せる。 / Change diameter and rpm and show proportionality.
- **実演B（15分）**：`simulations/sim_sensor_signals.html` でデジタル・アナログ・パルスを切り替える。 / Switch digital, analog and encoder displays.
- **実演C（15分）**：空気圧の図 D07-11 で「指令」と「動き」を分けて説明。シリンダ端センサの役割を問う。 / Use D07-11 to separate command and motion.
- **実演D（15分）**：D07-12 で危険源を指し、保護の考え方を学生に言わせる。 / Point to hazards in D07-12 and ask for protections.

**実演で避けること / avoid:** 実機の通電・加圧・駆動。写真や図で代替します。 / Energising, pressurising or moving real equipment; use photos and diagrams instead.

## 6. 必要な図 / Required diagrams

| 図 / figure | 使いどころ / where |
|---|---|
| D07-01 | 全体像、5層の説明 / overview and layers |
| D07-02 | フレーム・軸・ベアリング / structure |
| D07-03 | 回転と直線 / motion |
| D07-04 | ローラ速度の式と例 / roller speed |
| D07-05 | 張力・しわ・蛇行 / web handling |
| D07-06 | 動力伝達 / power transmission |
| D07-07 | モータの種類と指令・動力 / motors |
| D07-08 | センサの分類 / sensor taxonomy |
| D07-09 | デジタルとアナログ / signals |
| D07-10 | エンコーダ / encoder |
| D07-11 | 空気圧 / pneumatics |
| D07-12 | 危険源と保護 / hazards |

## 7. 必要なシミュレーション / Required simulations

- `sim_roller_speed.html`（ノートブック07-01） / notebook 07-01
- `sim_sensor_signals.html`（ノートブック07-02） / notebook 07-02

JavaScriptが無効な場合は `simulations/fallback/*.png` と各HTMLの `<noscript>` 説明を使用します。
If JavaScript is unavailable, use the fallback images and the `<noscript>` text.

## 8. 学生に問いかける質問 / Questions to ask students

1. この部品は、動きを作る側ですか、状態を情報にする側ですか。 / Does this part create motion or report state?
2. 滑りがあるとき、計算した速度は実測より大きいですか、小さいですか。 / With slip, is calculated speed larger or smaller than measured?
3. 透明なシートに、透過形光電センサは必ず使えますか。 / Can a through-beam sensor always detect a transparent sheet?
4. PPR 1,000 は、1回転1,000カウントと同じですか。 / Does PPR 1,000 mean 1,000 counts per turn?
5. しわの影をAIが欠陥としたとき、最初に何を確認しますか。 / If AI reports a wrinkle shadow as a defect, what do you check first?
6. 「AIがNGなら停止」は安全機能ですか、品質対応ですか。 / Is “stop when AI says NG” safety or quality?

## 9. よくある誤解 / Common misunderstandings

| 誤解 / misunderstanding | 実際 / reality |
|---|---|
| 計算した速度＝実測速度 / calculated equals measured | 滑り・張力・摩耗で異なる / slip, tension, wear change it |
| 画素数が多いほど良い / more pixels are better | 光学・照明・コントラスト次第 / depends on optics, lighting, contrast |
| PPR＝カウント数 / PPR equals counts | デコードで1・2・4倍 / decoding changes counts |
| センサは材質を問わない / sensors detect anything | 方式と対象で選ぶ / choose by mode and target |
| AIを直せば機械の問題も消える / better AI fixes mechanics | まず機械と照明を安定させる / stabilise mechanics and lighting first |
| 安全はラダー1行で足りる / one rung gives safety | 独立した安全系と検証が必要 / independent validated system |

## 10. 正しい説明の例 / Correct explanations

- **速度**：v = π × D × N。単位は mm/min にした後 m/min に換算。滑りなしの仮定を必ず添える。 / Convert mm/min to m/min and state the no-slip assumption.
- **PPRとカウント**：カウント数 = PPR × デコード倍率。1回転の距離 ÷ カウント数 = 1カウントの距離。 / counts = PPR × decode; distance per turn ÷ counts = distance per count.
- **アナログ**：物理範囲と電気範囲の両方を書いてから式を示す。 / State both the physical and electrical ranges before the formula.
- **安全**：危険源→リスクアセスメント→保護方策→検証。AIはこの流れの外側。 / Hazard → risk assessment → protective measures → validation; AI is outside this chain.

## 11. 期待される演習解答 / Expected exercise responses

ノートブック07-01 / 07-02 / 07-03 の「解答例」を参照してください。要点は次のとおりです。
See the worked answers in notebooks 07-01, 07-02 and 07-03. Key points:

- 80 mm・200 rpm → 約50.27 m/min（滑りなし）。 / about 50.27 m/min.
- PPR 500・×2 → 1,000カウント/回転。 / 1,000 counts per turn.
- 0–10 V・0–200 kPa・7.5 V → 150 kPa。
- 危険源は、巻き込み・感電・残圧・突然の起動など。 / Hazards include nip points, electric shock, stored pressure and unexpected start.
- 無効な結果をOKにしない。 / Never OK an invalid result.

## 12. トラブル対応 / Troubleshooting

| 症状 / symptom | 対応 / action |
|---|---|
| SVG図が表示されない / SVG not shown | ノートブックのパス（`../../assets/diagrams/day07/`）を確認 / check the relative path |
| シミュレータが動かない / simulator dead | ブラウザでローカルファイルを開く。JS有効を確認。だめなら `fallback/` の画像 / open the local file, enable JS, else use fallback images |
| 計算が合わない / calculation mismatch | π の丸め、mm と m、rpm と rps を確認 / check π rounding, mm vs m, rpm vs rps |
| 学生が安全と品質を混同 / safety vs quality confusion | D07-12 の境界線を指し、3種類のインターロックを名指しさせる / point to the boundary in D07-12 |
| 時間が足りない / short of time | 演習の1・5を必須、2〜4を宿題に / keep exercises 1 and 5 in class |

## 13. 安全上の制約 / Safety restrictions

- 実機の通電・加圧・駆動・ガード開放・インターロック解除を**行わせない**。 / Do not have students energise, pressurise, move, open guards or bypass interlocks.
- 実演は写真・図・シミュレータのみ。 / Demonstrations use photos, diagrams and simulators only.
- 高輝度光源の直接視を避ける。 / Never look into high-intensity light sources.
- 実機に触れる場合は、停止・遮断・減圧・ロックアウトと現地手順、有資格者の監督が必要。 / Real contact needs isolation, lock-out, site procedure and qualified supervision.
- 本教材は安全回路を設計・生成しない。 / The course never designs or deploys safety circuits.

## 14. オフライン代替 / Offline teaching fallback

- 印刷した D07-01〜D07-12 を配布し、指差しで説明。 / Print the diagrams and point.
- シミュレータの代わりに、`fallback/` のPNGを印刷し、値を手計算。 / Print fallback images and calculate by hand.
- 計算問題は電卓または紙。 / Calculators or paper for arithmetic.
- ネットワーク・PLC・カメラは不要。 / No network, PLC or camera required.

## 15. 評価の指針 / Assessment guidance

- ワークシート「機械構成図」を回収し、`worksheets/Day07_Answer_Key_ja_en.md` と `Day07_09_Assessment_Rubric_ja_en.md` で評価。 / Collect the worksheet and mark with the answer key and rubric.
- 重視するのは、用語の区別、単位付きの計算、機械と画像の因果、安全の独立。 / Value terminology, unit-bearing calculations, mechanics-to-image causality and safety independence.
- 「すべての材質を検出できる」「AIが安全を担保する」といった記述は減点。 / Deduct for universal-sensor or AI-safety claims.
- 口頭確認（例：NC接点とNCスイッチの違い）で理解を補強。 / Use oral checks to reinforce understanding.
