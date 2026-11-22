# 第8日 講師ガイド / Day 8 Instructor Guide
**PLC制御とラダープログラムの基礎 / PLC Control and Ladder Programming**

対象 / audience: 第7日を終えた初学者 / beginners who completed Day 7
教材 / material: `notebooks/Day08_PLC_Control/`、`assets/diagrams/day08/`、`day07_09_support/simulations/`
実機PLCがなくても、シミュレータと図だけで授業できます。
The day is teachable with the diagrams and simulators alone; no real PLC is needed.

## 1. 学習目標 / Learning objectives

1. 電圧・電流・電力の関係を機能として説明する。 / Explain voltage, current and power functionally.
2. センサ→PLC入力→プログラム→PLC出力→ドライバ→アクチュエータの経路をたどる。 / Trace the signal path.
3. デジタル／アナログ、入力／出力、信号／動力を区別する。 / Separate digital/analog, input/output and signal/power.
4. NO/NC接点を「ビットの値」として説明し、物理配線と区別する。 / Explain NO/NC contacts as bit evaluation, separate from wiring.
5. AND/OR/NOTの真理値表を書き、ラダーと対応させる。 / Write truth tables and map them to ladder.
6. 自己保持・オン遅延タイマ・カウンタの動作を予測する。 / Predict self-holding, ON-delay and counter behaviour.
7. 状態遷移を条件付きで書き、故障とNGを区別する。 / Write conditional transitions and separate fault from NG.
8. 安全機能が通常のラダーと別だと説明する。 / State that safety functions differ from ordinary ladder.

## 2. 前提知識 / Prerequisites

- 第7日の機械・センサ・アクチュエータの用語。 / Day 7 terminology.
- 0 と 1 の二状態、簡単な表の読み書き。 / Two-state logic and reading simple tables.
- 不要：電気工学、プログラミング、GX Works3の操作経験。 / No electrical engineering, programming or GX Works3 experience.

## 3. 時間割 / Exact timetable

| 時刻 / time | 分 / min | 内容 / content | 区分 / type |
|---|---:|---|---|
| 08:00–09:00 | 60 | 講師：PLCラックの見取りと信号の流れ / rack walkthrough and signal flow | 講師 / instructor |
| 09:00–10:20 | 80 | 08-01 PLCの基礎 / PLC fundamentals | 必須 / required |
| 10:20–10:35 | 15 | 休憩 / break | 休憩 / break |
| 10:35–12:00 | 85 | 08-02 ラダーの基礎 / ladder basics | 必須 / required |
| 12:00–12:50 | 50 | 昼食 / lunch | 昼食 / lunch |
| 12:50–13:50 | 60 | 講師：ラダーシミュレータと誤り探し / simulator and debugging | 講師 / instructor |
| 13:50–15:10 | 80 | 08-03 シーケンス制御（前半） / sequence control, part 1 | 必須 / required |
| 15:10–15:25 | 15 | 休憩 / break | 休憩 / break |
| 15:25–16:20 | 55 | 08-03（後半） / part 2 | 必須 / required |
| 16:20–16:50 | 30 | PLC入出力・シーケンス表 / I/O and sequence worksheet | 提出 / submission |

**合計 / total 530分（講師120・必須300・休憩30・昼食50・提出30）。**

## 4. 午前の講師説明 / Morning presentation（08:00–09:00）

1. D08-01 の架空ラックを示し、電源・CPU・入力・出力・通信の位置を学生に指させる（10分）。 / Have students point to modules in D08-01.
2. D08-02 で「信号」と「動力」を色分けして板書（10分）。 / Draw signal and power paths in different colours.
3. D08-03 のスキャン周期を、3つの箱と矢印で説明（10分）。 / Explain the three-box scan cycle.
4. 「入力の変化が出力に出るまで時間がかかる」ことを、通過する欠陥の例で説明（10分）。 / Use a passing defect to show that response takes time.
5. X/Y/M/T/C は**導入の慣例**であり、実機のマニュアル確認が必要だと明言（10分）。 / State that X/Y/M/T/C are conventions needing manual verification.
6. 質問対応（10分）。 / Questions.

**板書例 / board:** 左：センサ→入力→プログラム→出力→ドライバ→アクチュエータ。右：信号（24 V DC の例）／動力（モータ電源）の2列。

## 5. 午後の講師実演 / Afternoon demonstration（12:50–13:50）

- **実演A（20分）**：`sim_ladder_logic.html` で AND → OR → NOT を切り替え、真理値表と出力理由を読み上げる。 / Switch AND/OR/NOT and read the truth table and reasons.
- **実演B（15分）**：自己保持で起動・停止を操作し、停止優先を確認。 / Operate self-holding and confirm stop priority.
- **実演C（15分）**：オン遅延タイマを動かし、「時間単位は実装依存」と説明。 / Run the ON-delay and note the time base dependency.
- **実演D（10分）**：カウンタで連続ONが増えないことを見せる。 / Show that a held ON does not increase the count.

## 6. 必要な図 / Required diagrams

D08-01 PLC構成、D08-02 信号経路、D08-03 スキャン、D08-04 物理状態とビット、D08-05 NO/NC接点、D08-06 AND/OR/NOT、D08-07 自己保持、D08-08 タイマ、D08-09 カウンタ、D08-10 状態遷移、D08-11 HMIと診断、D08-12 インターロックの境界。

## 7. 必要なシミュレーション / Required simulations

- `sim_ladder_logic.html`（08-02）
- `sim_machine_sequence.html`（08-03）

JavaScriptが無効な場合は `fallback/sim_ladder_logic.png` と `fallback/sim_machine_sequence.png`、および各HTMLの `<noscript>` を使用。
If JavaScript is unavailable, use the fallback images and `<noscript>` text.

## 8. 学生に問いかける質問 / Questions to ask

1. PLC出力がONになると、モータに電流を流すのはどの機器ですか。 / Which device makes motor current flow?
2. ビットが0のとき、NO接点とNC接点はそれぞれ導通しますか。 / Which contact conducts when the bit is 0?
3. NC接点はNCスイッチと同じですか。 / Is an NC contact the same as an NC switch?
4. 連続ONが5秒続くと、カウンタは増えますか。 / Does a 5 s held ON increase a counter?
5. 起動と停止が同時に来たら、どちらを優先しますか。 / Which wins when start and stop coincide?
6. 故障とNGは同じですか。 / Are fault and NG the same?
7. この警報は、原因の除去なしに消してよいですか。 / May this alarm be cleared without removing the cause?

## 9. よくある誤解 / Common misunderstandings

| 誤解 / misunderstanding | 実際 / reality |
|---|---|
| NC接点＝NCスイッチ / NC contact = NC switch | ビット評価と物理配線は別 / bit evaluation versus wiring |
| 連続ONでカウントが増える / held ON increments | 立ち上がりだけ / rising edges only |
| PLCは出力でモータ電力を供給 / PLC output powers a motor | ドライバ・接触器が供給 / drivers and contactors supply power |
| 全PLCが同じスキャン / every PLC scans alike | 機種・設定依存 / model and configuration dependent |
| タイマは必ず100 ms単位 / timers are always 100 ms | 実装依存 / implementation-specific |
| 故障後は自動で戻る / automatic restart is fine | 人が許可する設計を検討 / consider human-authorised restart |
| 非常停止はラダー1行 / E-stop is one rung | 独立した安全系と検証 / independent validated safety system |

## 10. 正しい説明の例 / Correct explanations

- **接点**：NOはビット1で導通、NCはビット0で導通。物理配線はビットの値に影響するが、接点命令はビットだけを見る。 / Contacts evaluate bits only; wiring only influences the bit.
- **自己保持**：起動で自己保持、停止要求で解除。停止を優先。 / Set on start, clear on stop; stop wins.
- **タイマ**：設定時間 = 設定値 × 時間単位。単位はCPU・命令で確認。 / Preset = value × time base; confirm the base.
- **カウンタ**：立ち上がりごとに+1。プリセットで出力、リセットで0。 / +1 per rising edge; output at preset; reset to zero.
- **安全**：危険源→リスクアセスメント→保護方策→検証。通常のラダーはこの代用にならない。 / Ordinary ladder cannot substitute for the safety process.

## 11. 期待される演習解答 / Expected exercise responses

- 真理値表（AND/OR/NOT）は D08-06 と一致。 / Truth tables match D08-06.
- 自己保持の停止優先。 / Stop priority in self-holding.
- オン遅延 K30（100 ms）＝3.0 s。
- カウンタ 3回の立ち上がり＝3。
- 故障中は起動不可、リセット後も人の再起動許可が必要。 / No start while faulted; human restart permit after reset.
- 詳細は `worksheets/Day08_Answer_Key_ja_en.md`。 / Details in the answer key.

## 12. トラブル対応 / Troubleshooting

| 症状 / symptom | 対応 / action |
|---|---|
| 真理値表とラダーが一致しない / table and ladder disagree | 直列＝AND、並列＝OR、NC＝反転を一つずつ確認 / check series, parallel and inversion separately |
| 自己保持が解除されない / self-hold will not clear | 停止接点がNCか、停止ビットが1になっているか / check the NC contact and the stop bit |
| タイマが動かない / timer idle | タブが「タイマ」か、入力X0がONか / check the tab and X0 |
| カウンタが増えない / counter idle | 一度OFFにしてから再度ONにする（立ち上がり） / toggle OFF then ON |
| 学生が安全と品質を混同 / safety vs quality | D08-12 の境界を指し、3種類を名指し / point to D08-12 |
| 時間が足りない / short of time | 演習1・3・4を必須、2・5を宿題 / keep 1, 3 and 4 in class |

## 13. 安全上の制約 / Safety restrictions

- 実機PLCへの接続、プログラム変更、強制出力、配線変更を**行わせない**。 / No connection to a real PLC, no program changes, forcing or rewiring.
- シミュレータは実機制御に接続しない。 / Simulators never connect to real control.
- 安全回路の設計・生成をしない。 / Do not design or produce safety circuits.
- 「非常停止をラダーで実装した」という説明をしない。 / Never claim an emergency stop is implemented in ordinary ladder.

## 14. オフライン代替 / Offline fallback

- D08-01〜D08-12 を印刷して配布。 / Print the diagrams.
- `fallback/` の画面を印刷し、真理値表を手書き。 / Print the fallback screens and write truth tables by hand.
- ラダーは紙に接点記号で書かせる。 / Have students draw ladder rungs on paper.
- PLC・ネットワーク不要。 / No PLC or network needed.

## 15. 評価の指針 / Assessment guidance

- ワークシートを `Day08_Answer_Key_ja_en.md` と `Day07_09_Assessment_Rubric_ja_en.md` で評価。 / Mark with the answer key and rubric.
- 重視するのは、接点の論理、停止優先、真理値表との一致、故障とNGの区別、安全の独立。 / Value contact logic, stop priority, truth-table consistency, fault/NG separation and safety independence.
- 「無効な結果をOKにする」「自動再起動を前提にする」答案は重大な誤り。 / Treat invalid-as-OK and assumed auto-restart as critical errors.
