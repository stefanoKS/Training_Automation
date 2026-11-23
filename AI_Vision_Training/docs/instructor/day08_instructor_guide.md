# 第8日 講師ガイド / Day 8 Instructor Guide
**電気設計・センサー・PLC・ラダー制御 / Electrical Design, Sensors and PLC Control**

第8日は、DC24Vの電気、センサーとI/O、NPN/PNP、PLCラダー、自己保持、タイマー、状態シーケンス、異常処理、復電時の再起動防止を1日で扱います。
Day 8 covers DC24V electricity, sensors and I/O, NPN/PNP, PLC ladder, self-holding, timers, state sequences, fault handling and restart prevention after power restoration.

対象 / audience: 第7日を終えた初学者。電気・PLCの実務経験は不要。 / Beginners who completed Day 7; no electrical or PLC practice is assumed.
教材 / material: `notebooks/Day08_Electrical_PLC/`（01–03）、`assets/diagrams/day08/`、`day07_09_support/examples/automation_models.py`、`day07_09_support/simulations/sim_plc_sequence.html`、`docs/pdf/Day08_explanation_ja_en.pdf`。
実機のPLC・配線・空圧がなくても、このガイドだけで教えられます。 / The day is teachable without a real PLC, wiring or compressed air.

## 1. 学習目標 / Learning objectives

1. 電圧・電流・抵抗・電力の単位と関係を説明し、V＝IR、P＝VIを使える。 / Explain voltage, current, resistance and power with units, and use V = IR and P = VI.
2. DC24Vの負荷を合計し、ランプ2個・センサー3個・電磁弁2個で**0.73 A**を計算できる。 / Sum a DC24V load and calculate **0.73 A** for two lamps, three sensors and two valves.
3. 0.73 Aが定常電流の合計であり、電源選定の承認ではないと説明できる。 / Explain that 0.73 A is a steady-state sum, not approval of a power-supply selection.
4. センサーの方式を対象物・環境・信号から選び、**PNP＋シンク入力**、**NPN＋ソース入力**を入力共通端子まで説明できる。 / Select sensor technologies and explain **PNP with a sinking input** and **NPN with a sourcing input**, including the input common.
5. 統一I/O表（X0–X3、M0、Y0、Y1、Y2、T0）を再現し、Y1は遅延ランプ専用、電磁弁はY2と説明できる。 / Reproduce the canonical I/O and explain that Y1 is the delayed lamp only and the solenoid is Y2.
6. 正しい自己保持回路を書き、**STARTと並列の保持接点**が必要で、**X2は開始枝だけ**に入れると説明できる。 / Write the correct self-holding rung with a **parallel holding contact**, keeping **X2 in the start branch only**.
7. タイマーが**2999 msでY1 OFF、3000 msでON**になることと、STOPでT0が0に戻ることを確認できる。 / Verify Y1 OFF at **2999 ms** and ON at **3000 ms**, and T0 reset on STOP.
8. **F001**（前進端未確認）、**F002**（前後端同時ON）、**F003**（後退端未確認）を区別し、**リセットは動作開始ではない**、**復電時に自動再起動しない**と説明できる。 / Distinguish **F001**, **F002** and **F003**, and explain that **reset is not a start** and **power restoration must not restart the machine**.

## 2. 前提知識 / Prerequisites

- 第7日の「信号と電力」「シリンダ」「センサー」の用語。 / Day 7 terminology for signal and power, cylinders and sensors.
- 0と1の二状態、表の読み書き、割り算と単位換算。 / Two-state logic, reading tables, division and unit conversion.
- 「負荷」「指令」「状態」という言葉を、部品と結びつける意欲。 / Willingness to connect load, command and state to physical parts.

不要 / not required: 電気工学、ラダープログラミング、GX Works3、実機の端子知識。 / No electrical engineering, ladder programming, GX Works3 or real terminal knowledge.
注意 / caution: 本日のアドレスは**架空の訓練用**であり、実機の端子番号ではない。 / Today's addresses are **fictional training assignments**, not real terminal numbers.

## 3. 当日の時間割 / Exact daily timetable

`COURSE_SYLLABUS_DAY07_09.md` の第8日の行をそのまま使います。 / These are the Day 8 rows of the syllabus, unchanged.

| 時刻 / Time | 分 / min | 活動 / Activity | 区分 / Type |
|---|---:|---|---|
| 08:00–09:00 | 60 | 講師：DC24V制御盤、センサー、PLCの信号の流れ / Instructor: DC24V panel, sensors and PLC signal flow | 講師 / instructor |
| 09:00–10:20 | 80 | 08-01 電気の基礎とDC24V制御 / 08-01 Electrical Fundamentals and DC24V Control | 必須 / required |
| 10:20–10:35 | 15 | 休憩 / Break | 休憩 / break |
| 10:35–12:00 | 85 | 08-02 センサー・I/O・電気インターフェース / 08-02 Sensors, I/O and Electrical Interfaces | 必須 / required |
| 12:00–12:50 | 50 | 昼食 / Lunch | 昼食 / lunch |
| 12:50–13:50 | 60 | 講師：自己保持・タイマー・異常処理の実演 / Instructor: self-holding, timers and fault handling | 講師 / instructor |
| 13:50–15:10 | 80 | 08-03 PLC・ラダー・シーケンス制御（前半）/ 08-03 PLC, Ladder and Sequence Control, part 1 | 必須 / required |
| 15:10–15:25 | 15 | 休憩 / Break | 休憩 / break |
| 15:25–16:20 | 55 | 08-03 PLC・ラダー・シーケンス制御（後半）/ 08-03 PLC, Ladder and Sequence Control, part 2 | 必須 / required |
| 16:20–16:50 | 30 | 第8日ワークシートと提出 / Day 8 worksheet and submission | 提出 / submission |

**合計 / Totals:** 講師120分、必須300分、休憩30分、昼食50分、提出30分、**530分**。 / Instructor 120, required 300, breaks 30, lunch 50, submission 30, **530 min**.

## 4. 準備チェックリスト / Preparation checklist

- [ ] `quick_reference_day08.md`、統一I/O表、ノートブック01–03の `.ipynb` と `.md`。 / The Day 8 quick-reference card, the canonical I/O table and notebooks 01–03.
- [ ] `automation_models.py` の `CANONICAL_IO`、`PusherSequence`、`commissioning_matrix` が動くことを前日に確認。 / Confirm the day before that `CANONICAL_IO`, `PusherSequence` and `commissioning_matrix` run.
- [ ] D08-01〜D08-11 を印刷。PNGは `day07_09_support/reference_data/diagram_png/day08/`。 / Print D08-01 to D08-11, or use the PNGs in `reference_data/diagram_png/day08/`.
- [ ] `sim_plc_sequence.html` をローカルで開き、START、STOP、故障リセット、復電、故障注入の3チェックを試す。 / Open `sim_plc_sequence.html` locally and test START, STOP, reset, power restore and the three fault injections.
- [ ] ブラウザのJavaScriptを有効にし、`simulations/fallback/sim_plc_sequence.png` も印刷しておく。 / Enable JavaScript and print the fallback PNG as well.
- [ ] 学生用ワークシート、講師用解答例、ルーブリックを印刷。解答例は配布しない。 / Print the worksheet, instructor answer key and rubric; do not distribute the key.
- [ ] 白板に自己保持のラングと状態の鎖を書くスペースを確保。 / Reserve board space for the self-holding rung and the state chain.
- [ ] オフライン代替：印刷図、ラダー記号カード、電卓、予備PC。ネットワーク不要。 / Offline fallback: printed diagrams, ladder-symbol cards, calculator and a spare PC; no network.
- [ ] 実機PLC・配線・空圧は用意しない。 / Do not prepare a real PLC, wiring or compressed air.

## 5. 午前の説明シーケンス / Morning explanation sequence

### 5.1 08:00–09:00 DC24V盤・センサー・PLCの信号 / Panel, sensors and signal flow

| 時刻 / Time | 実演 / Demonstrate | 問い / Ask | 板書 / Board |
|---|---|---|---|
| 08:00–08:10 | D08-02 で、電源→保護→分岐→負荷を指す。 / Trace supply→protection→branch→load on D08-02. | 「24Vなら感電しないか」 / Is 24 V free of shock risk? | 信号（細い）と電力（太い）を2色で / signal and power in two colours |
| 08:10–08:20 | D08-04 で、PLC出力は信号で、負荷への電力は別経路と説明。 / Show that a PLC output is a signal; load power is a separate path. | 「PLC出力は無制限の電源か」 / Is a PLC output an unlimited supply? | PLC出力→リレー／ドライバ→負荷 / output→relay/driver→load |
| 08:20–08:32 | D08-01 の水路アナロジーでV＝IR、P＝VI。6Wランプ→0.25 A。 / Use D08-01 for V = IR and P = VI; a 6 W lamp draws 0.25 A. | 「3W×2、0.06A×3、0.15A×2の合計は」 / What is the total for the three load groups? | 0.25＋0.18＋0.30＝**0.73 A** |
| 08:32–08:42 | 0.73 Aに25%を置くと0.91 A。これは計画値で承認ではない。 / 0.73 A with 25% gives 0.91 A, a planning value, not approval. | 「突入電流・定格低下・電線・端子はどこで確認するか」 / Where are inrush, derating, wire and terminals checked? | 0.73 A（定常）≠電源選定承認 / steady sum ≠ approval |
| 08:42–08:52 | D08-05 で、鉄・透明樹脂・シリンダ端のセンサー候補を出させる。 / Use D08-05 to choose sensors for steel, clear resin and a cylinder end. | 「同じ『位置検出』でも、なぜ方式が変わるか」 / Why does the technology change for the same "position"? | 対象・距離・環境・信号の4軸 / target, distance, environment, signal |
| 08:52–09:00 | D08-07 の統一I/O表を読み、Y1は遅延ランプ、Y2は電磁弁、X1は健全時ONと確認。 / Read the canonical I/O: Y1 delayed lamp, Y2 solenoid, X1 ON when healthy. | 「X0と物理端子番号は同じか」 / Is X0 the same as a physical terminal? | アドレス≠端子、Y1≠電磁弁 / address ≠ terminal |

**板書レイアウト / board layout:** 左に「電源→保護→負荷」、中央に0.73 Aの3行、右に統一I/O表の9行。 / Left: supply→protection→load. Centre: the three 0.73 A lines. Right: the nine I/O rows.

### 5.2 12:50–13:50 自己保持・タイマー・異常処理の実演 / Self-holding, timer and fault handling

| 時刻 / Time | 実演 / Demonstrate | 問い / Ask | 板書 / Board |
|---|---|---|---|
| 12:50–13:00 | 朝の3問：0.73 Aの内訳、PNP＋シンク、Y1とY2の役割。 / Three morning checks: 0.73 A breakdown, PNP+sinking, Y1 versus Y2. | 「0.73 Aより大きい電源を選べば終わりか」 / Is choosing a supply above 0.73 A enough? | 0.73 A、PNP→シンク、Y1/Y2 |
| 13:00–13:15 | D08-08 のラングを1行ずつ読む。 / Read the D08-08 rung element by element. | 「STARTを離してもM0が続く理由は」「X2を保持枝に入れると何が起きるか」 / Why does M0 stay on? What if X2 is in the hold branch? | `(X0 AND X2) OR M0` → 直列X1 → `(M0)` |
| 13:15–13:28 | D08-09 の状態を、指令と確認に分けて指す。 / Point to commands and confirmations in D08-09. | 「Y2 ONは『動いた』ことの証明か」 / Does Y2 ON prove motion? | IDLE→READY→EXTEND→WAIT_EXTENDED→RETRACT→WAIT_RETRACTED→COMPLETE |
| 13:28–13:38 | D08-10 で、T0がM0の間だけ進み、STOPで0に戻ることを示す。 / Show T0 advancing only while M0 is ON and resetting on STOP. | 「2999 msと3000 msでY1はどう違うか」 / How does Y1 differ at 2999 and 3000 ms? | 2999 OFF / 3000 ON |
| 13:38–13:50 | D08-11 で、F001・F002・F003、リセット、復電を対応づける。 / Map F001, F002, F003, reset and power restoration on D08-11. | 「リセットは開始か」「復電でSTARTを押しっぱなしなら動くか」 / Is reset a start? Does a held START restart on power restore? | リセット≠開始、復電→新規START / reset ≠ start |

**実演で避けること / avoid:** 実機PLCへの接続、プログラム書込み、強制出力、配線、通電。シミュレータは実機制御に接続しない。 / Connecting to a real PLC, downloading, forcing outputs, rewiring or energising; the simulator never connects to real control.

## 6. 午後のフォロー / Afternoon follow-up

### 6.1 朝の復習の仕方 / How to review the morning (12:50–13:00)

1. 0.73 Aを、負荷ごとの式（3W÷24V×2、0.06×3、0.15×2）で言わせる。 / Have students restate 0.73 A load by load.
2. PNP＋シンク、NPN＋ソースを、入力共通端子の電位と電流の向きで言わせる。 / Have them state PNP+sinking and NPN+sourcing with the common potential and current direction.
3. Y1とY2を逆に使うと何が起きるか（遅延ランプと電磁弁の取り違え）を問う。 / Ask what happens if Y1 and Y2 are swapped.
4. 誤答は消さず、午後のラングとI/O表で戻る。 / Keep wrong answers and return to them at the rung and I/O table.

### 6.2 13:50以降のチェックポイント / Checkpoints after 13:50

| 時刻 / Time | 確認すること / Check | 合図 / Signal |
|---|---|---|
| 13:50–14:20 | `sim-selfhold` でSTART解放後もRUN=1、`sim-timer` で2999 ms Y1=False、3000 ms Trueか。 / RUN survives release, and the timer boundary? | 3行のトレースと2つの数値を確認 / check three trace lines and both values |
| 14:20–15:10 | `sim-sequence` の状態順序と、Y2がEXTEND/WAIT_EXTENDEDだけONか。 / State order, and Y2 ON only in EXTEND/WAIT_EXTENDED. | 状態の鎖を板書 / write the state chain |
| 15:25–15:50 | `sim-faults` でF001/F002/F003を区別できるか。 / Are F001, F002 and F003 distinguished? | 3つの故障コードを確認 / check three codes |
| 15:50–16:10 | `sim-reset` でリセット後Y2=False、復電時RUN=Falseか。 / Y2 False after reset and RUN False on restore? | 画面またはログで確認 / check screen or log |
| 16:10–16:20 | 主要な提出物（ラング説明、シミュ結果、状態表、I/Oトレース、異常マトリクス、試験証跡）がそろうか。 / Are the core deliverables present? | 机間チェック / desk check |

### 6.3 探るべき誤り / Common errors to probe

| 誤り / error | 問い / probe | 正しい説明 / correction |
|---|---|---|
| 保持接点が無い / no seal-in contact | 「STARTを離した瞬間、M0は何でONを続けるか」 / What keeps M0 ON after release? | STARTと並列のM0接点が必要。 / A holding contact in parallel with START is required. |
| X2を保持枝にも入れる / X2 in the hold branch | 「前進してX2がOFFになったらM0はどうなるか」 / What happens to M0 when X2 turns OFF? | 保持枝からX2を外す。開始条件と保持条件を分ける。 / Remove X2 from the hold branch; separate start from hold. |
| 物理NC＝ラダーNC / physical NC equals ladder NC | 「X1は健全時にONかOFFか」 / Is X1 ON or OFF when healthy? | 物理NC停止は健全時ON。ラダーではNO接点で「ONなら許可」と読む。 / A physical NC stop is ON when healthy; read it with an NO contact as permission. |
| リセットで動き出す / motion on reset | 「リセットは何をする操作か」 / What does reset do? | 異常状態を解除するだけ。動作開始ではない。 / It clears the fault only; it is not a start. |
| 復電で自動再起動 / auto-restart on power restore | 「保持M0や押しっぱなしSTARTで動かない理由は」 / Why no restart from a retained M0 or held START? | 冷起動でfresh start requiredにし、STARTの解放→再押下を要求する。 / Cold power-up requires a fresh release-then-press. |
| Y1を電磁弁に使う / Y1 for the solenoid | 「Y1とY2の役割は」 / What are Y1 and Y2? | Y1は遅延ランプ専用、電磁弁指令はY2。 / Y1 is the delayed lamp only; the solenoid is Y2. |
| PLC出力を電源と考える / output as a supply | 「出力定格を超えたらどうするか」 / What if the load exceeds the rating? | リレーやコンタクタを介する。出力は信号。 / Use a relay or contactor; the output is a signal. |
| 通常ラダーを安全機能とする / ordinary ladder as safety | 「このSTOPラングは人身安全を保証するか」 / Does this STOP rung guarantee personal safety? | 保証しない。安全機能は独立した安全関連系で設計・検証する。 / No; safety functions need an independent validated system. |

## 7. 必要な図 / Required figures

すべて `assets/diagrams/day08/` のSVG。印刷用PNGは `reference_data/diagram_png/day08/`。 / All are SVGs in `assets/diagrams/day08/`; PNGs are in `reference_data/diagram_png/day08/`.

| 図 / Figure | 使用ノート / Lesson | 教えること / What it teaches | 使い方 / Use |
|---|---|---|---|
| D08-01 | 08-01 | 電圧・電流・抵抗のアナロジー / V, I, R analogy | V＝IR、P＝VIの導入 / introduce the formulas |
| D08-02 | 08-01 | DC24Vの電力供給と保護 / distribution and protection | 信号と電力の分離 / separate signal from power |
| D08-03 | 08-01 | スイッチとリレーの違い / switch versus relay | 直接操作とコイル操作 / direct versus coil operation |
| D08-04 | 08-01 / 08-03 | PLC出力から負荷まで / PLC output to load | 出力は信号、電力は別経路 / output is a signal |
| D08-05 | 08-02 | センサーの種類と選び方 / sensor types | 対象物・環境で選ぶ / choose by target and environment |
| D08-06 | 08-02 | NPN・PNPとPLC入力の電流経路 / NPN and PNP current paths | 入力共通端子まで描く / draw through the common |
| D08-07 | 08-02 | 統一I/O表と概略配線 / canonical I/O and wiring | Y1/Y2、X1の正常状態 / Y1, Y2 and X1 normal state |
| D08-08 | 08-03 | 正しい自己保持回路 / correct self-holding | 並列保持接点とX2の位置 / seal-in and X2 placement |
| D08-09 | 08-03 | 状態ベースのシーケンス / state-based sequence | 指令と確認の分離 / command versus confirmation |
| D08-10 | 08-03 | タイミングチャート / timing chart | 2999/3000 msとT0リセット / timer boundary and reset |
| D08-11 | 08-03 | 異常処理マトリクス / fault matrix | F001/F002/F003、リセット、復電 / faults, reset, restore |

補足 / note: D08-08は元PDFの自己保持図の誤り（並列保持接点の欠落）を修正した図である。 / D08-08 corrects the source PDF's missing parallel holding contact.

## 8. シミュレーション / Simulations

### 8.1 Pythonセル / Python cells

Pythonセルはノートブックをリポジトリ内から開き、`setup` の後に上から順に実行する。ネットワークは不要。 / Open the notebook inside the repo, run `setup`, then execute top to bottom; no network is needed.

| ノート / Notebook | セルID / cell id | 観察すること / What to observe |
|---|---|---|
| 08-01 | `load-budget` | 0.250＋0.180＋0.300＝**0.73 A**、25%で**0.91 A**、`is_sizing_approval=False`。 / 0.73 A, 0.91 A at 25%, and `False`. |
| 08-01 | `supply-margin` | 0.73 Aに対する0/10/25/50/100%の計画値。承認ではない。 / Planning values; not approval. |
| 08-02 | `sensor-compatibility` | A（PNP＋シンク）とB（NPN＋ソース）がCOMPATIBLE、C/DはLIKELY INCOMPATIBLE、EはCHECK。 / A and B compatible; C and D likely incompatible; E check. |
| 08-02 | `io-table` / `io-validation` | 統一表の9行と、Y1電磁弁・X1正常OFFの誤り検出。 / Nine rows; detects Y1 solenoid and X1 normal-OFF errors. |
| 08-03 | `sim-selfhold` | START解放後もRUN=1、STOPでRUN/Y0/Y2=0、T0=0。 / RUN survives release; STOP clears outputs and T0. |
| 08-03 | `sim-timer` | **2999 ms Y1=False、3000 ms Y1=True**、STOP後T0=0。 / The timer boundary and reset. |
| 08-03 | `sim-sequence` | IDLE→…→COMPLETE、cycle_count=1、Y1=False。 / Full normal sequence. |
| 08-03 | `sim-faults` | `sensor_stuck_off`→F001、`motion_slow`→F001、`sensor_conflict`→F002。 / The three fault outcomes. |
| 08-03 | `sim-reset` | START保持中のリセット拒否、解放後IDLE、復電時RUN=False、再押下でREADY、2サイクル目。 / Reset refusal, release, restore, repeat. |
| 08-03 | `sim-invalid` | IDLE→COMPLETEなどの不正遷移を拒否。 / Invalid transitions rejected. |

### 8.2 `sim_plc_sequence.html` / the HTML PLC simulator

- 開き方 / how to open: ファイルをダブルクリックするか、ブラウザにドラッグする。サーバ、CDN、ネットワークは不要。 / Double-click the file or drag it into a browser; no server, CDN or network.
- 操作 / controls: X0 START、X1 STOP_OK、X2 後退端、X3 前進端、START/STOP/故障リセット/復電、故障注入（X3不来・X2X3同時・X3遅れ）。 / The four input checkboxes, the four buttons and the three fault injections.
- 観察 / observe: 状態、Y0/Y1/Y2ランプ、T0、cycle count、fresh start required、START armed、I/Oトレース。 / State, lamps, T0, cycle count, fresh-start and armed flags, and the trace.
- 手順例 / example sequence: START→離す（RUN継続）→STOP（全OFF、T0=0）→再度START→3秒待つ（Y1 ON）→STOP→故障注入X3不来→F001→リセット（Y2 OFFのまま）→復電（START保持でも動かない）。 / Press and release START, STOP, restart, wait 3 s, inject X3-stuck, reset, then power restore.
- 注意 / caution: 100 ms刻みの決定論的モデル。実機のスキャン、入力フィルタ、タイマー精度、空圧応答は再現しない。安全PLCではない。 / A deterministic 100 ms model; it does not reproduce real scan, filters, timer accuracy or pneumatics, and it is not a safety PLC.
- JavaScriptが無効な場合 / without JavaScript: `<noscript>` の説明と `simulations/fallback/sim_plc_sequence.png` を使う。 / Use the `<noscript>` text and the fallback PNG.

## 9. ディスカッション質問 / Discussion questions

1. 0.73 Aは電源選定の承認か。承認でないなら、何を確認すれば承認になるか。 / Is 0.73 A approval? If not, what checks would make it one?
2. PNP＋シンク入力で、電流はどこからどこへ流れるか。入力共通端子の電位も言え。 / Trace PNP into a sinking input, including the common potential.
3. NPN＋ソース入力は、なぜPNP＋シンクと同じ「適合」なのか。 / Why is NPN with a sourcing input equally compatible?
4. 物理NCの停止ボタンを、ラダーでNO接点として読む理由は何か。 / Why read a physical NC stop with an NO ladder contact?
5. STARTを離してもRUNが続く理由を、保持接点の言葉で説明せよ。 / Explain self-holding in terms of the seal-in contact.
6. X2を保持枝に入れると、どの時点で運転が落ちるか。 / At what moment does RUN drop if X2 is in the hold branch?
7. 2999 msと3000 msでY1が変わるのはなぜか。実機でも3.000秒ちょうどになるか。 / Why does Y1 change between 2999 and 3000 ms? Is it exact on real hardware?
8. リセットと復電の後、機械が動き出さないために、設計は何を要求するか。 / What must the design require after reset and power restoration so the machine does not move?

## 10. よくある誤解と正しい説明 / Likely misunderstandings and correct explanation

| 誤解 / misunderstanding | 正しい説明 / correct explanation |
|---|---|
| 物理NC接点＝ラダーのNC接点 / physical NC equals ladder NC | 物理接点は部品の通常状態、ラダー接点はビットの評価。X1は健全時ONなのでNO接点で「許可」と読む。 / Physical contacts describe the component; ladder contacts evaluate the bit. X1 is ON when healthy, so an NO contact reads permission. |
| NPNは「マイナス信号」で危険 / NPN is a "negative signal" and unsafe | NPNは0V側へ電流を吸い込む（シンク）。ソース入力と組み合わせれば正常に使える。 / NPN sinks current to 0 V; it works correctly with a sourcing input. |
| PNPならどのPLC入力でもつながる / a PNP works with any input | 入力共通端子の電位と入力回路で決まる。PNPはシンク入力と組み合わせる。 / It depends on the common potential and input circuit; PNP pairs with a sinking input. |
| 0.73 Aは電源容量の承認 / 0.73 A approves the supply | 定常電流の合計にすぎない。突入、定格低下、電線、端子、保護を別に確認する。 / It is only a steady sum; check inrush, derating, wire, terminals and protection. |
| Y1は電磁弁、Y2はランプ / Y1 is the solenoid, Y2 the lamp | 逆。Y1は遅延ランプ専用、Y2が前進電磁弁指令。 / The reverse: Y1 is the delayed lamp only; Y2 is the extend solenoid. |
| STARTを離すと止まるのが正常 / stopping on release is normal | 自己保持が正しければRUNは続く。止まるのは保持接点が無いから。 / With correct self-holding RUN stays; stopping indicates a missing seal-in. |
| リセットで運転が再開する / reset resumes RUN | リセットは異常解除だけ。新しいSTARTが必要。 / Reset clears the fault only; a fresh START is required. |
| 復電時は保持されているから安全 / retained state makes restore safe | 保持の有無にかかわらず自動再起動させない設計が必要。 / Regardless of retention, the design must prevent automatic restart. |
| 通常のPLC停止ラダーは安全機能 / an ordinary stop rung is safety | 通常制御と安全機能は別。安全はリスクアセスメントに基づく独立系で設計・検証する。 / Ordinary control and safety are separate; safety needs an independent validated system. |

## 11. 演習の解答ガイダンス / Exercise answer guidance

| 演習 / exercise | 期待する解答と数値 / expected answer and key numbers |
|---|---|
| A 自己保持 / self-holding | ①M0の並列保持接点がSTART解放後もM0をONに保つ。②X2は前進でOFFになるため、保持枝に入れるとRUNが落ちる。③X1 OFFでIDLE、M0/Y0/Y2がOFF、T0=0。④冷起動でfresh start requiredとし、START解放→再押下を要求する。 / ①The parallel M0 contact holds RUN. ②X2 turns OFF on extend, so it must not be in the hold branch. ③X1 OFF clears M0/Y0/Y2 and T0. ④Cold power-up requires a fresh release-then-press. |
| B 物理NCと論理接点 / physical NC and logical contacts | 物理NC停止は健全時ON。ラダーではX1をNO接点で読み「ONなら許可」とする。物理NOのSTARTも押している間ONなのでNO接点で読む。物理接点のNO/NCと命令のNO/NCは別。 / A physical NC stop is ON when healthy; the ladder reads X1 with an NO contact as permission. A physical NO START is also ON while pressed, so it is read with an NO contact. Physical and instruction contacts are independent. |
| C 状態遷移表 / state table | IDLE（全OFF、新規START＋X2＋X1でREADY）、READY（Y0/M0、次スキャンでEXTEND）、EXTEND（Y2）、WAIT_EXTENDED（X3 ONかつX2 OFFでRETRACT、3秒超過でF001）、RETRACT（Y2 OFF）、WAIT_RETRACTED（X2 ONかつX3 OFFでCOMPLETE、3秒超過でF003）、COMPLETE、FAULT（全OFF、リセット＋新規START）。 / The eight states, their outputs and transitions with timeouts. |
| D タイムアウト設計 / timeouts | ストローク、速度、圧力、負荷、弁応答、センサー応答、PLCスキャン、温度を確認する。3秒は**訓練用の仮値**で、実機にそのまま使わない。 / Need stroke, speed, pressure, load, valve and sensor response, scan and temperature. 3 s is a training value, not for a real machine. |
| E 異常処理マトリクス / fault matrix | F001前進端未確認、F002前後端同時ON、F003後退端未確認、STOPでIDLE、停電復電で自動起動なし、リセット中START保持は拒否。いずれも「原因除去→リセット→新規START」。 / F001, F002, F003, STOP, power restore and held START; all require clear cause → reset → fresh START. |
| F リセット後の確認 / verify no motion on reset | FAULTからリセット直後、state=IDLE、RUN=False、Y2=Falseを確認し、日時・入力・状態・出力を記録する。 / After reset: IDLE, RUN False, Y2 False; record time, inputs, state and outputs. |
| 電気（08-01）/ electrical | 6Wランプ0.25 A、抵抗約96Ω（動作点）、3個で0.75 A。負荷合計**0.73 A**、25%計画値**0.91 A**は承認ではない。 / 0.25 A, about 96 Ω at the operating point, 0.75 A for three; **0.73 A** total and **0.91 A** planning, not approval. |
| I/O（08-02）/ I/O | X0 START、X1 STOP_OK（健全時ON）、X2後退端、X3前進端、M0 RUN、Y0運転ランプ、Y1遅延ランプ、Y2前進電磁弁、T0 3秒。 / The nine canonical rows. |

**ワークシート／解答例との対応 / worksheet and answer-key mapping.** 本日の評価対象はノートブック01–03の演習A–Fです。`Day08_Student_Worksheet_ja_en.md` は T1–T7 で同じ演習を扱い、`Day08_Answer_Key_ja_en.md` には 0.73 A の内訳、NPN/PNP の電流経路、統一I/O、正しい自己保持、2999/3000 ms、F001/F002/F003、リセットと復電の期待値が入っています。答えだけでなく、入力共通・接点・状態・証跡が説明されていることを確認してください。 / The assessed items are exercises A–F in notebooks 01–03. The current worksheet covers them as T1–T7, and the key contains the 0.73 A breakdown, NPN/PNP current paths, canonical I/O, correct self-holding, 2999/3000 ms, F001/F002/F003 and reset/power-restore expectations. Require the common, contacts, states and evidence, not only a final number.

## 12. トラブルシューティング / Troubleshooting

| 症状 / symptom | 確認 / check | 対応 / action |
|---|---|---|
| 学生がコードを実行できない / code will not run | リポジトリ内から開いたか、`setup` を実行したか、カーネル / opened inside the repo, setup run, kernel | `FileNotFoundError` ならフォルダを直す。`automation_models.py` を確認。 / Fix the folder; check the module path. |
| 日本語フォントが□になる / missing font | Matplotlib/ブラウザのフォント / Matplotlib or browser fonts | 日本語フォントを入れるか、英語ラベルで代用。 / Install a Japanese font or use English labels. |
| ノートブックが古い・トレースが違う / stale notebook or trace | `.ipynb` と `.md` の版、実行順、`sim-selfhold` の初期解放スキャン / revision and execution order | カーネル再起動→すべて実行。`.md` を正とする。 / Restart and Run All; treat `.md` as truth. |
| 2999/3000にならない / timer boundary wrong | `sim-timer` の開始T0、1 ms刻みで進めたか / start T0 and 1 ms steps | `normal_cycle` 後にT0を2999まで進め、1 msずつ確認する。 / Advance to 2999 after a normal cycle and step by 1 ms. |
| シミュレータが動かない / simulator dead | ローカルファイルとして開いたか、JS有効か / local file and JavaScript | ブラウザで開き直す。だめなら `fallback/sim_plc_sequence.png` と `<noscript>`。 / Reopen in a browser; otherwise use the fallback PNG and `<noscript>`. |
| リセットで動いてしまう / motion on reset | リセットを開始条件に使っていないか / reset used as a start | リセットはFAULT解除だけ。新規STARTを別に要求する。 / Reset only clears FAULT; require a fresh START. |
| 復電で動いてしまう / motion on restore | 保持M0、押しっぱなしSTART、初期化 / retained M0, held START, initialisation | 冷起動でRUN=False、fresh start requiredにする。 / Cold-start with RUN False and a fresh-start requirement. |

## 13. 安全上の制約 / Safety restrictions

- 実機の配線・通電・絶縁測定・PLC書込み・強制出力・空圧供給・シリンダ動作・安全回路の調整を**行わない**。 / No real wiring, energisation, insulation testing, PLC download, forcing, compressed air, cylinder motion or safety-circuit adjustment.
- 実機作業は、リスクアセスメント、事前承認、電気的・空圧的隔離、無電圧確認、ロックアウト、ガード、有資格者の監督、復旧手順が揃った別枠でのみ行う。 / Real work is separate and requires risk assessment, approval, isolation, zero-energy verification, lockout, guarding, qualified supervision and recovery procedures.
- DC24Vでも短絡・発熱・不意動作の危険は残る。「低電圧だから安全」と教えない。 / Even 24 V can short, heat and cause unexpected motion; never teach "low voltage means safe".
- **無通電は安全状態を保証しない。** 弁型式・負荷・残圧・トラップ空気を確認する。 / **De-energised does not guarantee a safe state**; check valve type, load, stored pressure and trapped air.
- **通常のPLC制御は安全機能ではない。** STOPラダーを非常停止・ガードインターロック・人身安全の代用にしない。 / **Ordinary PLC control is not a safety function**; never substitute a STOP rung for emergency stopping, guard interlocks or personal safety.
- 安全機能の検証は、リスクアセスメントに基づく独立した安全関連系で、有資格者が行う。本研修では実施しない。 / Safety-function validation belongs to an independent safety-related system and qualified persons; it is not performed here.

## 14. オフライン代替活動 / Offline alternative activities

1. D08-01〜D08-11 を印刷し、0.73 Aの内訳とPNP/NPNの電流経路を紙に描かせる。 / Print the diagrams and have students draw the 0.73 A breakdown and the NPN/PNP paths.
2. 自己保持ラングを、接点記号カードで机上に組む。X2を保持枝から外す理由を口頭で説明させる。 / Build the rung with contact cards and explain why X2 is outside the hold branch.
3. 2999 msと3000 msのタイムラインを紙に書き、Y1の変化を矢印で示す。 / Draw the 2999/3000 ms timeline and mark the Y1 change.
4. 状態カード（IDLE〜FAULT）を並べ、各状態の出力と遷移条件を付箋で貼る。 / Order state cards and attach outputs and transitions.
5. F001/F002/F003のカードを使い、検出・応答・リセット・再起動を4列に分類する。 / Sort fault cards into detection, response, reset and restart.
6. 提出物は紙で作成し、16:20–16:50に回収する。 / Produce deliverables on paper and collect them at 16:20–16:50.

## 15. 評価基準 / Assessment criteria

`Day07_09_Assessment_Rubric_ja_en.md` は8観点・100点のコース共通ルーブリックです。本日は特に、観点3（電気・センサー・I/O、13点）、観点4（PLC・ラダー・シーケンス、15点）、観点6（試験・トラブルシューティング、15点）、観点8（最終提案、10点）を中心に評価します。合格は60点以上かつ必須是正なしです。以下の表は形成的確認であり、ルーブリックの代用ではありません。 / The course rubric has eight criteria and 100 points. Focus on criterion 3 (electrical, sensors and I/O, 13), criterion 4 (PLC/ladder/sequence, 15), criterion 6 (testing and troubleshooting, 15) and criterion 8 (final proposal, 10). Pass requires at least 60 points and no mandatory remediation. The table below is formative only.

| 観点 / criterion | 3以上（合格）の目安 / adequate or better |
|---|---|
| 用語 / terminology | 物理接点と論理接点、シンク/ソース、自己保持、状態、故障コードを区別する。 / Separates physical and logical contacts, sink/source, self-holding, states and fault codes. |
| 技術 / technical | 0.73 A、PNP＋シンク、NPN＋ソース、2999/3000、F001/F002/F003を再現する。 / Reproduces 0.73 A, the NPN/PNP pairings, 2999/3000 and the three faults. |
| 安全 / safety | リセット≠開始、復電時自動起動なし、通常PLC≠安全機能を明記する。 / States reset ≠ start, no auto-restart and ordinary PLC ≠ safety. |
| 明確さ / clarity | ラング、状態表、I/Oトレースが第三者に再現できる。 / The rung, state table and trace are reproducible by another person. |

**必須提出物 / required evidence:** 電気機器リスト、センサー選定表、統一I/O表、入力共通・出力互換性チェック、概略配線図、ラダー説明、状態遷移表、シミュレーション結果、異常処理マトリクス、試験証跡。 / Electrical equipment list, sensor selection table, canonical I/O, input-common/output compatibility check, conceptual wiring diagram, ladder explanation, state-transition table, simulation results, fault matrix and test evidence.

**必須改善項目 / mandatory remediation items**（1つでも該当したら再提出 / resubmit if any apply）:
1. 自己保持に並列保持接点が無い、またはX2を保持枝に入れている。 / Missing parallel seal-in, or X2 in the hold branch.
2. リセットを開始条件に使う、または復電で自動起動する設計。 / Reset used as a start, or automatic restart on power restoration.
3. 物理NCとラダーNCを同一視している。 / Treats physical NC and ladder NC as the same.
4. Y1を電磁弁、Y2をランプに割り当てている。 / Assigns Y1 to the solenoid or Y2 to the lamp.
5. F001/F002/F003の対応を誤る、またはPLC出力を無制限の電源と書く。 / Mixes the fault codes, or treats the PLC output as an unlimited supply.
6. 通常のPLC停止を安全機能と書く。 / Calls an ordinary PLC stop a safety function.

**評定 / judgement:** ルーブリックの合計60点以上、かつ必須改善項目に該当しないことを合格とします。形成的確認の4観点は、4段階のうち3以上を目安にしてください。 / Pass requires at least 60 points and no mandatory remediation. For the formative check, aim for at least 3 on each row.

## 16. 遅れている学生へのガイダンス / Guidance for students who fall behind

優先順位は「0.73 A → 統一I/OとNPN/PNP → 自己保持 → タイマーと故障 → 復電」です。時間配分は設計値であり、実測された完了時間ではありません。 / Prioritise 0.73 A, then canonical I/O and NPN/PNP, then self-holding, then timer and faults, then power restore. The allocations are design values, not measured completion times.

**必ず残す / keep (required):**
1. 08-01の負荷合計**0.73 A**と、0.91 Aは計画値で承認ではないこと。 / The **0.73 A** total and that 0.91 A is planning, not approval.
2. 統一I/O表（Y1遅延ランプ、Y2電磁弁、X1健全時ON）と、**PNP＋シンク／NPN＋ソース**。 / The canonical I/O and the **PNP+sinking / NPN+sourcing** pairings.
3. 正しい自己保持ラング：**並列保持接点、X2は開始枝だけ**。 / The correct rung: **parallel seal-in, X2 only in the start branch**.
4. **2999/3000 ms**のY1と、STOPでT0=0。 / The timer boundary and T0 reset.
5. **F001/F002/F003**、**リセット≠開始**、**復電時自動起動なし**。 / The three faults, reset ≠ start and no auto-restart.
6. 提出物のうち、ラング説明、状態表、異常マトリクス、試験証跡。 / The rung explanation, state table, fault matrix and test evidence.

**後回し・省略してよい / defer or drop (optional):**
- 2線式センサーの漏れ電流、リレー/トランジスタ出力の詳細比較、カウンタ、不正遷移の拒否デモ、追加の故障ケース。 / Two-wire leakage, the detailed relay/transistor comparison, the counter, the invalid-transition demo and extra fault cases.
- `io-validation` の誤り検出デモ、BOMや版管理の深掘り。 / The I/O validation demo and deeper BOM/revision work.
- 実機を想定したタイムアウト値の設計討論（3秒は訓練値のまま）。 / Real-machine timeout design debate; keep 3 s as the training value.

**声かけ / what to say:** 「今日の合格点は、自己保持の1行と、復電で動かないことを説明できることです。部品の暗記ではありません。」 / "Today's pass is one self-holding rung and the explanation of why the machine does not restart on power restoration. It is not component memorisation."
