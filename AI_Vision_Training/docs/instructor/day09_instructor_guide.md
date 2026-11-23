# 第9日 講師ガイド / Day 9 Instructor Guide
**通信・試運転・改善提案 / Industrial Communication, Commissioning and Automation Proposal**

第9日は、IPとサブネット、通信の層、段階ゲート、試験記録、異常試験、引継ぎ、費用対効果を1つの提案にまとめる日です。
Day 9 connects IP and subnets, communication layers, staged gates, test records, abnormal tests, handover and cost-benefit into one proposal.

対象 / audience: 第7日・第8日を終えた初学者。ネットワークの専門知識は不要。 / Beginners who completed Days 7 and 8; no prior networking expertise is assumed.
教材 / material: `notebooks/Day09_Communication_Commissioning/`（01–03）、`assets/diagrams/day09/`、`day07_09_support/examples/automation_models.py`、`docs/pdf/Day09_explanation_ja_en.pdf`。
実機ネットワーク・PLC・通電試験がなくても、このガイドだけで教えられます。 / The day is teachable without a real network, PLC or energised test.

## 1. 学習目標 / Learning objectives

1. LAN、スイッチ、ルータ、IPv4の4オクテットを説明できる。 / Explain LAN, switch, router and the four IPv4 octets.
2. /24と/25のネットワークアドレス、ブロードキャスト、割当可能範囲を計算できる。 / Calculate network, broadcast and assignable ranges for /24 and /25.
3. **192.168.10.130/25と192.168.10.200/25は同一サブネット**、**192.168.10.20/25は別サブネット**と、マスクとともに説明できる。 / Explain that **192.168.10.130/25 and 192.168.10.200/25 share a subnet**, while **192.168.10.20/25 is different**, using the mask.
4. 物理リンク、IP設定、アプリケーション通信を別々に切り分け、ping成功がModbus成功を保証しないと説明できる。 / Separate physical link, IP configuration and application communication, and explain that ping success does not prove Modbus success.
5. 段階ゲート**G0–G6**を説明し、**G5（承認された通電試験）は課程の必須ではない**と明言できる。 / Explain gates **G0–G6** and state that **G5, approved energised testing, is not required for the course**.
6. **PASS / FAIL / NOT TESTED / BLOCKED**を区別し、**BLOCKEDをPASSに読み替えない**。 / Distinguish **PASS, FAIL, NOT TESTED and BLOCKED**, and never reinterpret **BLOCKED as PASS**.
7. 試験記録に、試験ID、要求ID、前提、手順、期待、実測、合否、証跡、実施者、日付、是正処置を書ける。 / Write a test record with test ID, requirement ID, preconditions, procedure, expected, actual, status, evidence, operator, date and corrective action.
8. 12秒×180回/日、220日、2,400円/時から**316,800円/年**、設備450,000円で**約1.42年**を計算し、その限界を説明できる。 / Calculate **316,800 JPY/year** and **about 1.42 years** for a 450,000 JPY investment, and state the limits.
9. 危険源、保護方策の方向性、未確定仕様、次のステップを、提案として一貫させる。 / Keep hazards, protective direction, open specifications and next steps consistent in a proposal.

## 2. 前提知識 / Prerequisites

- 第7日の要求・能力・機械・空圧、第8日の電気・I/O・自己保持・状態・故障。 / Day 7 requirements, capacity, mechanics and pneumatics; Day 8 electrical, I/O, self-holding, states and faults.
- 割り算、割合、単位換算（秒→分→時間、円/時）。 / Division, percentages and unit conversion (seconds to minutes to hours, JPY/hour).
- 2進数が分からなくてもよい。マスクの考え方は本文の表で足りる。 / Binary arithmetic is not required; the mask tables in the manuscript are sufficient.

不要 / not required: ネットワーク設計・構築、Modbusの実装、PLCの通電試験、安全認証。 / No network design or build, Modbus implementation, PLC energised testing or safety certification.
注意 / caution: 演習は架空の `192.168.10.0/24` などで行い、実ネットワークを変更しない。 / Exercises use fictional networks; never change a real network.

## 3. 当日の時間割 / Exact daily timetable

`COURSE_SYLLABUS_DAY07_09.md` の第9日の行をそのまま使います。 / These are the Day 9 rows of the syllabus, unchanged.

| 時刻 / Time | 分 / min | 活動 / Activity | 区分 / Type |
|---|---:|---|---|
| 08:00–09:00 | 60 | 講師：ネットワーク構成、試運転ゲート、提案の全体像 / Instructor: network architecture, commissioning gates and the proposal | 講師 / instructor |
| 09:00–10:20 | 80 | 09-01 産業用ネットワークと通信設定 / 09-01 Industrial Networking and Communication Settings | 必須 / required |
| 10:20–10:35 | 15 | 休憩 / Break | 休憩 / break |
| 10:35–12:00 | 85 | 09-02 試運転・異常試験・引継ぎ / 09-02 Commissioning, Abnormal Testing and Handover | 必須 / required |
| 12:00–12:50 | 50 | 昼食 / Lunch | 昼食 / lunch |
| 12:50–13:50 | 60 | 講師：試験記録・復旧・提案レビューの実演 / Instructor: test records, recovery and proposal review | 講師 / instructor |
| 13:50–15:10 | 80 | 09-03 自動化提案と最終レビュー（前半）/ 09-03 Automation Proposal and Final Review, part 1 | 必須 / required |
| 15:10–15:25 | 15 | 休憩 / Break | 休憩 / break |
| 15:25–16:20 | 55 | 09-03 自動化提案と最終レビュー（後半）/ 09-03 Automation Proposal and Final Review, part 2 | 必須 / required |
| 16:20–16:50 | 30 | 第9日ワークシート・最終発表準備・提出 / Day 9 worksheet, presentation preparation and submission | 提出 / submission |

**合計 / Totals:** 講師120分、必須300分、休憩30分、昼食50分、提出30分、**530分**。 / Instructor 120, required 300, breaks 30, lunch 50, submission 30, **530 min**.

## 4. 準備チェックリスト / Preparation checklist

- [ ] `quick_reference_day09.md`、ノートブック01–03の `.ipynb` と `.md`。 / The Day 9 quick-reference card and notebooks 01–03.
- [ ] `automation_models.py` の `describe_subnet`、`subnet_pair_report`、`commissioning_matrix`、`payback_report` を前日に実行（本日のシミュレーション）。 / Run `describe_subnet`, `subnet_pair_report`, `commissioning_matrix` and `payback_report` the day before (today's simulation).
- [ ] D09-01〜D09-09 を印刷。PNGは `reference_data/diagram_png/day09/`。 / Print D09-01 to D09-09, or use the PNGs in `reference_data/diagram_png/day09/`.
- [ ] `commissioning_matrix` が**10 PASS / 2 BLOCKED**（T11、T12）になることを確認。 / Confirm **10 PASS / 2 BLOCKED** (T11 and T12).
- [ ] 試験記録の用紙（試験ID、要求ID、前提、手順、期待、実測、合否、証跡、実施者、日付、是正処置）。 / Test-record forms with all eleven fields.
- [ ] 学生用ワークシート、講師用解答例、ルーブリックを印刷。解答例は配布しない。 / Print the worksheet, answer key and rubric; do not distribute the key.
- [ ] 電卓、白板、付箋、IPアドレスカード（PC/PLC/HMI/カメラ）。 / Calculator, whiteboard, sticky notes and IP cards for PC, PLC, HMI and camera.
- [ ] オフライン代替：印刷図、サブネット計算用紙、ゲートカード、電卓、予備PC。ネットワーク不要。 / Offline fallback: printed diagrams, subnet worksheets, gate cards, calculator and a spare PC; no network.
- [ ] 実ネットワーク、実PLC、通電試験は用意しない。 / Do not prepare a real network, real PLC or energised test.

## 5. 午前の説明シーケンス / Morning explanation sequence

### 5.1 08:00–09:00 ネットワーク・ゲート・提案の全体像 / Network, gates and proposal

| 時刻 / Time | 実演 / Demonstrate | 問い / Ask | 板書 / Board |
|---|---|---|---|
| 08:00–08:10 | D09-05 で、PC・PLC・HMI・カメラ・スイッチの接続を指す。 / Trace PC, PLC, HMI, camera and switch on D09-05. | 「ケーブルがつながれば通信できるか」 / Does a connected cable mean communication works? | 物理リンク≠IP≠アプリ / link ≠ IP ≠ application |
| 08:10–08:20 | D09-02 で、/24のネットワーク・ブロードキャスト・割当範囲を計算。 / Work the /24 network, broadcast and host range on D09-02. | 「192.168.10.255は機器に割り当てられるか」 / Can .255 be assigned to a device? | /24：.0、.255、.1–.254、254個 / /24: .0, .255, .1–.254, 254 hosts |
| 08:20–08:32 | D09-03 で、.130/25と.200/25が同じ、.20/25が別と示す。 / Show .130/25 and .200/25 together, .20/25 apart. | 「第3オクテットが同じなら同じネットワークか」 / Does the same third octet mean the same network? | /25：.128/.255/.129–.254、126個 / the /25 range |
| 08:32–08:42 | D09-04 で、IP→機器、ポート→サービス、TCP/UDP→運び方。 / Map IP to device, port to service and TCP/UDP to transport. | 「pingが通ればModbusで読めるか」 / Does ping success mean Modbus works? | Modbus TCPは502が一般的、ping≠アプリ / port 502, ping ≠ app |
| 08:42–08:52 | D09-06 で、G0文書→G1機械→G2電気（隔離）→G3オフライン→G4準備→G5通電（任意）→G6受入。 / Walk the gates, marking G5 optional. | 「G2を飛ばしてG5へ行けるか」「G5をしない場合、合否はどう書くか」 / Can G2 be skipped? How is an unperformed G5 recorded? | G5は必須でない、未実施はBLOCKED/NOT TESTED / G5 optional; never PASS |
| 08:52–09:00 | D09-07 で、PASS/FAIL/NOT TESTED/BLOCKEDを4色で整理。 / Sort the four statuses on D09-07. | 「BLOCKEDをPASSと書いてよいか」 / May BLOCKED be written as PASS? | BLOCKED≠PASS、記録は11欄 / never PASS; eleven fields |

**板書レイアウト / board layout:** 左にIPの3行（/24、/25上、/25下）、中央にゲートの鎖、右に4状態と「BLOCKED≠PASS」。 / Left: three IP lines. Centre: the gate chain. Right: four statuses and "BLOCKED ≠ PASS".

### 5.2 12:50–13:50 試験記録・復旧・提案レビューの実演 / Test records, recovery and proposal review

| 時刻 / Time | 実演 / Demonstrate | 問い / Ask | 板書 / Board |
|---|---|---|---|
| 12:50–13:00 | 朝の3問：/25の範囲、G5の扱い、4状態の違い。 / Three morning checks: the /25 range, G5, the four statuses. | 「.20/25と.130/25は同じか」 / Are .20/25 and .130/25 the same? | .0/25 vs .128/25 |
| 13:00–13:15 | `commissioning-matrix` を実行し、10 PASS / 2 BLOCKEDを示す。 / Run the matrix and show 10 PASS / 2 BLOCKED. | 「T11とT12はなぜBLOCKEDか」 / Why are T11 and T12 blocked? | G5未実施、安全検証は対象外 / no hardware; safety out of scope |
| 13:15–13:28 | G3のオフライン試験（2999/3000、F001/F002、リセット、復電）を再確認。 / Review the G3 offline tests from Day 8. | 「シミュレーションPASSは実機PASSか」 / Is a simulation PASS a hardware PASS? | シミュレーション証跡≠実機受入 / simulation evidence ≠ acceptance |
| 13:28–13:38 | `test-record` でT04の11欄を表示し、`"OK"` が拒否されることを示す。 / Show the eleven T04 fields and that `"OK"` is rejected. | 「『T04 OK』だけでは何が分からないか」 / What is missing from "T04 OK"? | 前提・手順・期待・実測・証跡・実施者・日付・是正 / the record fields |
| 13:38–13:50 | D09-08 の提案の流れと、D09-09 の316,800円/年・1.42年を計算。 / Walk the proposal chain and compute 316,800/year and 1.42 years. | 「この1.42年は利益を保証するか」 / Does 1.42 years guarantee profit? | 12×180÷60＝36分/日、0.6×220×2,400＝316,800円、450,000÷316,800≒1.42年 |

**実演で避けること / avoid:** 実ネットワークの設定変更、実PLCへの接続、通電試験、安全機能の検証。すべて机上・シミュレーションで行う。 / Changing a real network, connecting a real PLC, energised testing or safety validation; everything stays on paper or in simulation.

## 6. 午後のフォロー / Afternoon follow-up

### 6.1 朝の復習の仕方 / How to review the morning (12:50–13:00)

1. 白板に `192.168.10.130/25` と `192.168.10.20/25` を書き、ネットワークアドレスを計算させる。 / Write the two addresses and have students compute the network addresses.
2. G0–G6を学生に並べさせ、G5だけを灰色で囲ませる。 / Have students order G0–G6 and circle G5 as optional.
3. PASS/FAIL/NOT TESTED/BLOCKEDの4枚のカードを、正しい定義に貼らせる。 / Match four status cards to their definitions.
4. 誤答は消さず、午後の試験マトリクスで戻る。 / Keep errors and return to them at the matrix.

### 6.2 13:50以降のチェックポイント / Checkpoints after 13:50

| 時刻 / Time | 確認すること / Check | 合図 / Signal |
|---|---|---|
| 13:50–14:20 | 提案のIP割当と構成図が、/24と/25の判定に一致するか。 / Does the proposal's IP allocation and diagram match the subnet verdicts? | 提案内の.130/.200/.20を確認 / check the three addresses in the proposal |
| 14:20–15:10 | `proposal-check` の24欄と、I/O・シーケンス・通信の値が一致するか。 / 24 fields and consistency of I/O, sequence and network. | 空欄の理由と値を確認 / check blanks and values |
| 15:25–15:50 | 試験計画がG0–G6、**10 PASS / 2 BLOCKED**、4状態と整合するか。 / Does the test plan align with the gates, counts and statuses? | ゲートと状態を確認 / check gates and statuses |
| 15:50–16:10 | `payback-calculator` が36.0分/日、316,800円/年、1.42年か。 / 36.0 min/day, 316,800/year and 1.42 years? | 3つの数値を確認 / check three values |
| 16:10–16:20 | 提出物（IP割当、構成図、通信仕様、試験計画、リスク、費用、10分発表）がそろうか。 / Deliverables present. | 机間チェック / desk check |

### 6.3 探るべき誤り / Common errors to probe

| 誤り / error | 問い / probe | 正しい説明 / correction |
|---|---|---|
| 第3オクテットが同じなら同一 / same third octet means same subnet | 「マスクは何か」 / What is the mask? | マスクと一緒にネットワークアドレスを計算する。/25では.0と.128に分かれる。 / Compute with the mask; /25 splits at .0 and .128. |
| /25のネットワークを.0と書く / writes .0 for the upper /25 | 「.130は.128側か.0側か」 / Is .130 on the .128 side? | .130/25のネットワークは.128、ブロードキャストは.255、割当は.129–.254。 / Network .128, broadcast .255, hosts .129–.254. |
| ping成功＝通信成功 / ping success equals communication | 「ポート502は開いているか」 / Is port 502 open? | pingはICMP。アプリはポート・プロトコル・アドレスを別に確認する。 / Ping is ICMP; check port, protocol and address separately. |
| BLOCKEDをPASSにする / BLOCKED as PASS | 「実施していない試験をPASSにできるか」 / Can an unperformed test pass? | BLOCKEDは前提・許可・設備が無く実施できない状態。PASSの代用にしない。 / BLOCKED means preconditions are missing; never substitute PASS. |
| G5を必須にする / treats G5 as required | 「課程の必須はどこまでか」 / Where does the course requirement end? | G0–G4とG6が必須。G5は承認された場合のみ、未実施はBLOCKED。 / G0–G4 and G6 are required; G5 only with approval. |
| リセットで運転再開 / reset resumes operation | 「リセットは何をするか」 / What does reset do? | 異常解除だけ。新規STARTが必要。 / It clears the fault only; a fresh START is required. |
| 復電で自動再起動 / auto-restart on restore | 「START保持で復電したら動くか」 / Does a held START restart on restore? | 動かない。解放→再押下を要求する。 / No; require release-then-press. |
| 316,800円は確実な利益 / 316,800 is guaranteed profit | 「運用費・停止損失・教育・税金は入っているか」 / Are operating cost, downtime, training and tax included? | 労務時間の仮換算。実現には再配置・残業削減が必要。 / A hypothetical labour-time value; realisation needs redeployment or overtime reduction. |
| 1.42年を投資判断の結論にする / treats 1.42 years as the decision | 「単純回収の前提は何か」 / What are the simple-payback assumptions? | 運用費0、効果一定の単純計算。出発点であり完全な評価ではない。 / Zero operating cost and constant benefit; a starting point, not a full appraisal. |

## 7. 必要な図 / Required figures

すべて `assets/diagrams/day09/` のSVG。印刷用PNGは `reference_data/diagram_png/day09/`。 / All are SVGs in `assets/diagrams/day09/`; PNGs are in `reference_data/diagram_png/day09/`.

| 図 / Figure | 使用ノート / Lesson | 教えること / What it teaches | 使い方 / Use |
|---|---|---|---|
| D09-01 | 09-01 | LANとスイッチ / LAN and switch | スイッチとルータの違い / switch versus router |
| D09-02 | 09-01 | IPv4とサブネットマスク / IPv4 and masks | /24と/25の範囲計算 / range calculations |
| D09-03 | 09-01 | 同一サブネットとルーティング / same subnet and routing | .130/.200/.20の判定 / the three addresses |
| D09-04 | 09-01 | TCP・UDP・ポート・プロトコル / TCP, UDP, ports | IP・ポート・アプリの層 / the layers |
| D09-05 | 09-01 | ネットワーク構成と通信設定 / block diagram and record | IP割当表の作成 / build the allocation |
| D09-06 | 09-02 | 段階的な試運転ゲート / staged gates | G0–G6、G5は任意 / gates and optional G5 |
| D09-07 | 09-02 | 試験結果の4状態 / four test statuses | BLOCKED≠PASS / status discipline |
| D09-08 | 09-03 | 課題から提案までの流れ / problem to proposal | 24項目の一貫性 / 24-item consistency |
| D09-09 | 09-03 | 費用対効果と回収期間 / cost, benefit, payback | 316,800円/年と1.42年 / the cost example |

補足 / note: D09-09の回収期間は単純回収であり、運用費・停止損失・品質・教育・税金・減価償却を含まない。 / D09-09 shows simple payback and excludes operating cost, downtime, quality, training, tax and depreciation.

## 8. シミュレーション / Simulations

### 8.1 Pythonセル / Python cells

Pythonセルはノートブックをリポジトリ内から開き、`setup` の後に上から順に実行する。ネットワークは不要。 / Open the notebook inside the repo, run `setup`, then execute top to bottom; no network is needed.

| ノート / Notebook | セルID / cell id | 観察すること / What to observe |
|---|---|---|
| 09-01 | `subnet-basic` | /24は.0/.255/.1–.254/254、.130/25と.200/25は.128/.255/.129–.254/126、.20/25は.0/.127/.1–.126/126。 / The /24 and both /25 ranges. |
| 09-01 | `subnet-pairs` | .130と.200はsame_subnet=True、.130と.20はFalse。 / The pair verdicts. |
| 09-01 | `ip-allocation` | .255は割当不可、.20の重複を検出。 / Detects .255 and the duplicate .20. |
| 09-02 | `commissioning-matrix` | **10 PASS / 2 BLOCKED**（T11通電、T12安全検証）。 / The counts and the two blocked tests. |
| 09-02 | `fault-trace` | X3不来→WAIT_EXTENDED→F001、Y2 OFF。 / F001 after missing X3. |
| 09-02 | `test-record` | T04の11欄と、`"OK"` が不正な状態として拒否されること。 / The eleven fields and the rejected "OK". |
| 09-02 | `change-history` | 変更ごとに再試験IDと承認を記録。 / Each change has a re-test and approval. |
| 09-03 | `payback-calculator` | 36.0分/日、132.0時間/年、**316,800円/年**、450,000円、**1.42年**。 / The five cost values. |
| 09-03 | `payback-sensitivity` | 投資増・運用費増で回収が延び、純効果0以下なら無限。 / Payback lengthens; non-positive net value gives infinity. |
| 09-03 | `proposal-check` | 24欄が空でなくても、品質レビューは別。 / 24 fields complete, quality review still separate. |

### 8.2 共有HTMLシミュレータ / the shared HTML simulator

本日は新しいHTMLシミュレータを使いません。`sim_plc_sequence.html` は第8日03のモデルで、G3の復習に5分だけ再利用できます。 / Today has no new HTML simulator. `sim_plc_sequence.html` belongs to Day 8-03 and may be reused for five minutes of G3 review.

- 開き方 / how to open: ローカルのHTMLをブラウザで開く。サーバ・CDN・ネットワーク不要。 / Open the local HTML in a browser; no server, CDN or network.
- 観察 / observe: START解放後のRUN、2999/3000のY1、F001/F002、リセット後Y2 OFF、復電時RUN OFF。 / Self-holding, timer boundary, faults, reset and restore.
- 注意 / caution: 決定論的モデルであり、実機の通信・スキャン・空圧・安全機能を再現しない。シミュレーションPASSを実機PASSや受入証跡にしない。 / A deterministic model; it does not reproduce real communication, scan, pneumatics or safety. Never use a simulation PASS as hardware acceptance.
- JavaScriptが無効な場合 / without JavaScript: `fallback/sim_plc_sequence.png` と `<noscript>`。 / Use the fallback PNG and `<noscript>` text.

## 9. ディスカッション質問 / Discussion questions

1. ケーブル、IP、アプリケーションの3つは、それぞれ何を確認するか。 / What does each of cable, IP and application verify?
2. 192.168.10.130/25と192.168.10.200/25が同じサブネットである理由を、ネットワークアドレスで説明せよ。 / Explain with network addresses why .130/25 and .200/25 are in the same subnet.
3. .20/25が別サブネットになる理由を、.0/25と.128/25の境界で説明せよ。 / Explain why .20/25 is different, using the .0/.128 boundary.
4. 同じスイッチにつながっていても、別サブネットなら何が必要か。 / What is needed for different subnets on the same switch?
5. pingが通ってもModbusが読めない理由を3つ挙げよ。 / Give three reasons why ping may work but Modbus may not.
6. G5を実施しない場合、試験記録に何と書くか。なぜPASSと書かないのか。 / What is recorded when G5 is not performed, and why not PASS?
7. 316,800円/年は、どのような条件で実際の利益になるか。 / Under what conditions does 316,800/year become a real benefit?
8. 1.42年の計算から抜けている費用を3つ挙げよ。 / Name three costs missing from the 1.42-year calculation.

## 10. よくある誤解と正しい説明 / Likely misunderstandings and correct explanation

| 誤解 / misunderstanding | 正しい説明 / correct explanation |
|---|---|
| 第3オクテットが同じなら同一ネットワーク / same third octet means the same network | マスクと一緒にネットワークアドレスを計算する。/25では.0側と.128側に分かれる。 / Compute with the mask; /25 splits into .0 and .128 sides. |
| /25のブロードキャストは.127 / the upper /25 broadcast is .127 | .130/25のネットワークは.128、ブロードキャストは.255、割当は.129–.254。 / Network .128, broadcast .255, hosts .129–.254. |
| 192.168.10.255は使える / .255 is assignable | ブロードキャスト。機器には.1–.254を使う。 / It is the broadcast; use .1–.254. |
| ケーブルがつながれば通信できる / a cable guarantees communication | 物理リンク、IP、アプリは別。IPが別サブネットならルータが必要。 / Link, IP and application are separate; different subnets need a router. |
| ping成功＝アプリ成功 / ping success equals application success | pingはICMP。ポート・プロトコル・アドレス・ファイアウォールを別に確認する。 / Ping is ICMP; check port, protocol, address and firewall separately. |
| G5は必須 / G5 is required | G5は承認された場合のみ。未実施はBLOCKEDまたはNOT TESTED。 / G5 only with approval; otherwise BLOCKED or NOT TESTED. |
| BLOCKEDはPASSの一種 / BLOCKED is a kind of PASS | BLOCKEDは前提・許可・設備が無く実施できない状態。PASSに読み替えない。 / BLOCKED means it cannot be performed; never convert it to PASS. |
| シミュレーションPASS＝実機PASS / simulation PASS equals hardware PASS | シミュレーションは証跡の一種。実機の受入には別の試験と承認が必要。 / Simulation is one kind of evidence; hardware acceptance needs separate tests and approval. |
| 316,800円は確実な利益 / 316,800 is guaranteed profit | 労務時間の仮換算。運用費・停止・品質・教育・税金・減価償却を別に評価する。 / A hypothetical labour-time value; evaluate other costs separately. |

## 11. 演習の解答ガイダンス / Exercise answer guidance

| 演習 / exercise | 期待する解答と数値 / expected answer and key numbers |
|---|---|
| A IP割当 / IP allocation | 例：PC .10、PLC .20、HMI .30、カメラ .40。マスク255.255.255.0、GW .1（例）。.0と.255は使わない。 / Example: PC .10, PLC .20, HMI .30, camera .40; mask .0, gateway .1; never .0 or .255. |
| B 同一サブネット判定 / same-subnet judgement | ①192.168.1.30/24と.40/24＝同一。②192.168.1.30/24と192.168.2.40/24＝別。③.130/25と.200/25＝同一（.128/25）。④.130/25と.20/25＝別（.128/25対.0/25）。 / ① same; ② different; ③ same; ④ different. |
| C 通信仕様 / communication specification | PLC型式、プロトコル（例：Modbus TCP）、ポート502、データアドレス、データ型、更新周期、タイムアウト、通信喪失時の機械動作。 / PLC model, protocol, port 502, address, data type, update period, timeout and behaviour on loss. |
| D トラブルシュート / troubleshooting | ①リンク・電源・ケーブル、②IP・マスク・重複、③経路・ping・ICMP、④ポート・FW・サーバ、⑤プロトコル・アドレス、⑥復旧時の機械動作。 / Six ordered checks from physical link to recovery. |
| E /24と/25 / the split | .20/25：ネットワーク.0、ブロードキャスト.127、割当.1–.126。.130/25：ネットワーク.128、ブロードキャスト.255、割当.129–.254。第3オクテットが同じでも別サブネット。 / .20/25 and .130/25 have different network, broadcast and host ranges. |
| 費用対効果 / cost-benefit | 12×180÷60＝36分/日、0.6時間/日×220日×2,400円＝**316,800円/年**、450,000÷316,800＝1.42045…≒**1.42年**（運用費0の仮定）。運用費400,000円なら純効果0以下で回収不能。 / 36 min/day, **316,800/year**, **1.42 years** at zero operating cost; with 400,000 operating cost, payback is infinite. |
| 試験記録 / test record | T04：前提（RUN、後退端、STOP_OK）、手順（START押して離す、3000 msまで保持）、期待（2999 OFF / 3000 ON）、実測、PASS、証跡（シミュレーションログ）、実施者、日付、是正（なし）。 / The eleven T04 fields. |
| 提案 / proposal | 24項目のうち、課題、目標、能力、方式、機械、アクチュエータ、センサー、電気、I/O、シーケンス、通信、危険源、保護方策、試験、投資、運用費、効果、回収、リスク、未確定、次ステップを一貫させる。 / Keep the 24 items consistent, especially capacity, I/O, sequence, network, test and cost. |

**ワークシート／解答例との対応 / worksheet and answer-key mapping.** 本日の評価対象はノートブック01–03の演習A–Eと最終提案です。`Day09_Student_Worksheet_ja_en.md` は T1–T6 で同じ内容を扱い、`Day09_Answer_Key_ja_en.md` には /24・/25 の範囲、.130/25 と .200/25 が同一、.20/25 が別、10 PASS / 2 BLOCKED、316,800円/年と1.42年の計算・限界が入っています。BLOCKEDをPASSにしないこと、費用の仮定を明記することを確認してください。 / The assessed items are exercises A–E and the final proposal. The current worksheet covers them as T1–T6, and the key contains the /24 and /25 ranges, the same-subnet verdicts, 10 PASS / 2 BLOCKED, and the 316,800 JPY/year and 1.42-year calculation with its limits. Require BLOCKED never to be recorded as PASS, and require stated cost assumptions.

## 12. トラブルシューティング / Troubleshooting

| 症状 / symptom | 確認 / check | 対応 / action |
|---|---|---|
| 学生がコードを実行できない / code will not run | リポジトリ内から開いたか、`setup` を実行したか、カーネル / opened inside repo, setup, kernel | フォルダを直し、`automation_models.py` を確認して再実行。 / Fix the folder, check the module and rerun. |
| 日本語フォントが□になる / missing font | Matplotlib/ブラウザのフォント / fonts | 日本語フォントを入れるか、英語ラベルで代用。 / Install a Japanese font or use English labels. |
| ノートブックが古い・日付が違う / stale notebook or date | `.ipynb` と `.md` の版、`TRAINING_DATE` はビルド日 / revision; `TRAINING_DATE` is the build date | `.md` を正とし、証跡には**実施したセッションの日付**を記録する。 / Treat `.md` as truth; record the actual session date in evidence. |
| サブネット計算が合わない / subnet arithmetic wrong | マスク、プレフィックス、上位/下位の/25、オクテットの範囲 / mask, prefix and octets | `describe_subnet` でネットワーク・ブロードキャスト・割当範囲を確認。 / Use `describe_subnet` to check all three. |
| 試験マトリクスが10/2にならない / matrix count differs | 実行順、T11/T12のBLOCKED、モデルの版 / order, blocked tests, model revision | カーネル再起動→すべて実行。10 PASS / 2 BLOCKEDを確認。 / Restart, Run All and confirm 10/2. |
| ブラウザで図・PDFが表示されない / browser fails | ローカルファイル、JS、PDFビューア / local file, JS, viewer | Chrome/Edgeで開く。印刷PNG/PDFを使う。 / Use Chrome or Edge; fall back to printed PNG/PDF. |
| 回収期間が1.42年にならない / payback differs | 12秒、180回、220日、2,400円、450,000円、運用費0 / the six inputs | `payback_report` の入力を確認。運用費を入れると無限になり得る。 / Check the inputs; operating cost can make payback infinite. |

## 13. 安全上の制約 / Safety restrictions

- 実在の工場ネットワーク、生産設備、PLC設定を**変更しない**。演習は架空のネットワークだけで行う。 / Do not change a real factory network, production equipment or PLC settings; exercises use fictional networks only.
- 実機の配線・通電・PLC書込み・空圧供給・シリンダ動作・安全回路の調整を**行わない**。 / No real wiring, energisation, PLC download, compressed air, cylinder motion or safety-circuit adjustment.
- **G5（承認された通電試験）は課程の必須ではない。** 実施しない場合、PASSではなく**BLOCKED**または**NOT TESTED**と記録する。 / **G5 is not required**; record it as **BLOCKED** or **NOT TESTED**, never PASS.
- **通常のPLC制御は安全機能ではない。** 安全機能の検証は、リスクアセスメントに基づく独立した安全関連系で、有資格者が行う。 / **Ordinary PLC control is not a safety function**; validation belongs to an independent safety-related system and qualified persons.
- **無通電は安全状態を保証しない。** 遮断・排気・零確認・ロックアウト・再起動防止を一組で扱う。 / **De-energised does not guarantee a safe state**; isolate, bleed, verify zero, lock out and prevent restart.
- シミュレーションPASSを実機の受入証跡にしない。試験記録には「シミュレーション」と明記する。 / Never use a simulation PASS as hardware acceptance; label it as simulation evidence.

## 14. オフライン代替活動 / Offline alternative activities

1. D09-01〜D09-09 を印刷し、IPの3行とゲートの鎖を紙に書かせる。 / Print the diagrams and have students write the IP lines and gate chain.
2. /24と/25のネットワーク・ブロードキャスト・割当範囲を、紙と電卓で計算する。 / Compute /24 and /25 ranges on paper with a calculator.
3. IPアドレスカードをPC・PLC・HMI・カメラに割り当て、重複と.0/.255を検査する。 / Assign IP cards to devices and check duplicates and .0/.255.
4. ゲートカードG0–G6を並べ、各ゲートの「確認・許可・NG時の扱い」を付箋で貼る。 / Order G0–G6 and attach check, approval and NG handling.
5. 試験記録を紙の11欄で1件書き、T11/T12をBLOCKEDカードで表す。 / Write one eleven-field record on paper and mark T11/T12 BLOCKED.
6. 316,800円/年と1.42年を手計算し、抜けている費用を列挙する。 / Compute the cost values by hand and list missing costs.
7. 10分発表を模造紙で行う。スライドが無くても、課題→次のステップの順で話す。 / Present on flip-chart paper in the ten-minute order.

## 15. 評価基準 / Assessment criteria

`Day07_09_Assessment_Rubric_ja_en.md` は8観点・100点のコース共通ルーブリックです。本日は特に、観点5（通信・ネットワーク、10点）、観点6（試験・トラブルシューティング、15点）、観点7（技術文書、10点）、観点8（最終提案、10点）を中心に、3日間の証跡と合わせて評価します。合格は60点以上かつ必須是正なしです。以下の表は形成的確認であり、ルーブリックの代用ではありません。 / The course rubric has eight criteria and 100 points. Focus on criterion 5 (communication and networking, 10), criterion 6 (testing and troubleshooting, 15), criterion 7 (technical documentation, 10) and criterion 8 (final proposal, 10), assessed with the three days' evidence. Pass requires at least 60 points and no mandatory remediation. The table below is formative only.

| 観点 / criterion | 3以上（合格）の目安 / adequate or better |
|---|---|
| 用語 / terminology | サブネット、マスク、ゲート、4状態、単純回収を正しく使う。 / Uses subnet, mask, gate, the four statuses and simple payback correctly. |
| 技術 / technical | .130/25と.200/25が同一、.20/25が別、10 PASS / 2 BLOCKED、316,800円/1.42年を再現する。 / Reproduces the subnet verdicts, 10/2 and the cost values. |
| 安全 / safety | G5任意、BLOCKED≠PASS、通常PLC≠安全、実ネットワークを変更しない。 / G5 optional, BLOCKED ≠ PASS, ordinary PLC ≠ safety, no real network change. |
| 明確さ / clarity | 10分で、課題→要求→方式→試験→費用→リスク→次のステップを説明する。 / Explains the chain in ten minutes. |

**必須提出物 / required evidence:** IP割当表、ネットワーク構成図、通信仕様、試運転チェックリスト、試験マトリクス、不具合リスト、変更履歴、最終提案、10分発表。 / IP allocation, network diagram, communication specification, commissioning checklist, test matrix, defect list, change history, final proposal and ten-minute presentation.

**必須改善項目 / mandatory remediation items**（1つでも該当したら再提出 / resubmit if any apply）:
1. BLOCKEDまたはNOT TESTEDをPASSとして記録している。 / Records BLOCKED or NOT TESTED as PASS.
2. サブネットを第3オクテットだけで判定している、または/25の範囲を誤る。 / Judges a subnet by the third octet alone, or gets the /25 range wrong.
3. G5を必須として実施した、または実施していないのにPASSと書く。 / Treats G5 as required, or marks an unperformed G5 PASS.
4. 316,800円/年を確実な利益と書き、運用費・限界を無視する。 / Presents 316,800/year as guaranteed profit and omits costs and limits.
5. リセットを開始条件に使う、または復電で自動起動する設計。 / Uses reset as a start, or auto-restarts on restoration.
6. 実ネットワークを変更した、または実機の安全を確認したと主張する。 / Changes a real network or claims real safety verification.

**評定 / judgement:** ルーブリックの合計60点以上、かつ必須改善項目に該当しないことを合格とします。形成的確認の4観点は、4段階のうち3以上を目安にしてください。 / Pass requires at least 60 points and no mandatory remediation. For the formative check, aim for at least 3 on each row.

## 16. 遅れている学生へのガイダンス / Guidance for students who fall behind

優先順位は「サブネット → ゲートと4状態 → 試験記録 → 費用と限界」です。時間配分は設計値であり、実測された完了時間ではありません。 / Prioritise subnets, then gates and the four statuses, then test records, then cost and limits. The allocations are design values, not measured completion times.

**必ず残す / keep (required):**
1. /24と/25の範囲、**192.168.10.130/25と.200/25は同一**、**.20/25は別**。 / The /24 and /25 ranges and the three verdicts.
2. **G0–G6**、**G5は任意**、**BLOCKED≠PASS**、**10 PASS / 2 BLOCKED**。 / The gates, optional G5, status discipline and the matrix counts.
3. 試験記録の11欄を1件、T04で完成させる。 / One complete eleven-field T04 record.
4. **316,800円/年**、**1.42年**、運用費0の仮定と限界。 / The cost values, the zero-operating-cost assumption and the limits.
5. 提案のうち、課題、要求、方式、I/O、シーケンス、通信、試験、リスク、費用、次のステップ。 / The core proposal chain.
6. 実ネットワーク・実機の通電・安全検証を行っていないこと。 / Confirmation that no real network, energisation or safety validation took place.

**後回し・省略してよい / defer or drop (optional):**
- /31（RFC 3021）と/32の特殊ケース、TCP/UDPの詳細、DNS、VLAN、産業用Ethernetの規格比較、回収期間の感度分析表の全組み合わせ。 / The /31 and /32 edge cases, TCP/UDP detail, DNS, VLAN, industrial-Ethernet comparisons and the full sensitivity grid.
- 24項目すべての記入、発表の複数回リハーサル。12項目の骨格と1回の通しで足りる。 / All 24 items and multiple rehearsals; the 12-item spine and one full run are enough.

**声かけ / what to say:** 「今日の核心は、.130/25と.200/25が同じで.20/25が別と言えること、そしてBLOCKEDをPASSにしないことです。費用の1.42年は、その次の話です。」 / "The core today is stating that .130/25 and .200/25 are together while .20/25 is apart, and never turning BLOCKED into PASS. The 1.42-year figure comes after that."
