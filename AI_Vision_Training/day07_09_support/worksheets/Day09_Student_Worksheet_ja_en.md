# 第9日 学生ワークシート：通信・試運転・自動化提案 / Day 9 Student Worksheet: Communication, Commissioning and Proposal

氏名 / Name: ________________________________　日付 / Date: ____________________

所属・班 / Group: ____________________________　講師 / Instructor: ______________

**推定時間 / Estimated time:** 90分。ノートブックの演習中に下書きし、16:20–16:50の提出時間30分で仕上げます。発表準備は別に10分確保します。 / 90 minutes, drafted during the notebook exercises, finished in the 30-minute submission slot, with 10 more minutes for the presentation.

**対象の原稿 / Source notebooks:** `Day09_01_Industrial_Networking.md`（09-01）、`Day09_02_Commissioning.md`（09-02）、`Day09_03_Automation_Proposal.md`（09-03）。ネットワークは架空の `192.168.10.0/24` だけを使い、実在の工場ネットワーク、PLC、カメラの設定は変更しません。 / Only the fictional network is used; no real factory network, PLC or camera setting is changed.

**安全境界 / Safety boundary:** 本ワークシートは机上演習です。実機の通電、空圧供給、シリンダ動作、安全回路の調整、安全機能の検証、実ネットワークの設定変更は行いません。実機の試運転は、リスクアセスメント、事前承認、電気的・空圧的隔離、残留エネルギー確認、ガード、有資格者の監督、復旧手順がそろった場合にだけ行います。課程の完了に、実機の通電試験は不要です。

This worksheet is a desk exercise. It does not involve real energisation, compressed air, cylinder motion, safety-circuit adjustment, safety-function validation or changes to a real network. Real commissioning requires a risk assessment, prior approval, electrical and pneumatic isolation, stored-energy verification, guarding, qualified supervision and a recovery procedure. Course completion does not require an energised hardware test.

**記入のきまり / How to fill this in**

- 計算は式と単位を書き、ネットワークは「マスクと一緒に」判定します。 / Show formulas and units, and always judge a network together with its mask.
- 試験の合否は PASS、FAIL、NOT TESTED、BLOCKED の4つだけを使います。OK/NGは使いません。 / Use only the four statuses PASS, FAIL, NOT TESTED and BLOCKED. Do not use OK/NG.
- 金額と年数には「仮定」と「単純回収」であることを添えます。 / Label money and years as hypothetical and as a simple payback.

## T1 /24と/25のサブネット計算 / /24 and /25 subnet calculations

*参照 / Reference: 09-01 §6 サブネットマスク、§11 サブネット計算、セル `subnet-basic`。*

マスクは、IPアドレスのどこまでがネットワーク部かを示します。ネットワークアドレスとブロードキャストアドレスはホストに割り当てられません。ホスト部のビット数から、割当可能数を計算します。

A mask shows where the network part ends. The network and broadcast addresses cannot be assigned to hosts. Derive the usable count from the number of host bits.

| 項目 / Item | 192.168.10.0 **/24** | 192.168.10.128 **/25** |
|---|---|---|
| マスク / mask | 255.255.255.0 | 255.255.255.128 |
| ネットワーク部のビット / network bits | 24 | |
| ホスト部のビット / host bits | | |
| ネットワークアドレス / network | | |
| ブロードキャスト / broadcast | | |
| 割当可能な先頭 / first host | | |
| 割当可能な末尾 / last host | | |
| 割当可能数 / usable count | | |
| 割当可能数の式 / count formula | 2⁸ − 2 | |

`192.168.10.20/25` は、どのサブネットに入りますか。ネットワーク、ブロードキャスト、割当可能範囲を書いてください。 / Which /25 subnet contains 192.168.10.20?

______________________________________________________________________________

「先頭3オクテットが同じなら同じネットワーク」と言えない理由を、/25の例を使って書いてください。 / Using the /25 example, explain why "the first three octets match" does not prove the same network.

______________________________________________________________________________

## T2 IPアドレスの割当 / IP allocation

*参照 / Reference: 09-01 §9 通信設定の記録、§11.1 IP割当表の検査、セル `ip-allocation`。*

`192.168.10.0/24` から、PC、PLC、カメラ、HMI、予備に重複しないIPを割り当てます。ネットワークアドレスとブロードキャストアドレスは使いません。ゲートウェイは仮に `192.168.10.1` とします。

Assign unique addresses from `192.168.10.0/24` to a PC, PLC, camera, HMI and a spare. Do not use the network or broadcast address. Assume the gateway is `192.168.10.1`.

| 機器 / Device | IPアドレス / IP | マスク / Mask | ゲートウェイ / GW | 役割 / Role |
|---|---|---|---|---|
| PC | | 255.255.255.0 | | |
| PLC | | 255.255.255.0 | | |
| カメラ / camera | | 255.255.255.0 | | |
| HMI | | 255.255.255.0 | | |
| 予備 / spare | | 255.255.255.0 | | |

- 割当に使ってはいけない2つのアドレスと、その理由を書いてください。 / Name the two addresses that must not be assigned, and why.
- 重複をどう検査するかを、一文で書いてください。 / Describe in one sentence how you would check for duplicates.

______________________________________________________________________________

## T3 同一サブネットの判定 / Same-subnet judgement

*参照 / Reference: 09-01 §7 同一サブネットとルーティング、セル `subnet-pairs`。*

同じマスクで計算したネットワークアドレスが一致すれば同一サブネットです。第3オクテットが同じでも、マスクが違えば別サブネットになります。

Two addresses are in the same subnet when their network addresses, computed with the same mask, are equal. The same third octet does not guarantee the same subnet.

| # | 組合せ / Pair | 同一か / Same? | それぞれのネットワーク / Networks | 理由 / Reason |
|---|---|---|---|---|
| 1 | 192.168.1.30/24 と 192.168.1.40/24 | | | |
| 2 | 192.168.1.30/24 と 192.168.2.40/24 | | | |
| 3 | 192.168.10.130/25 と 192.168.10.200/25 | | | |
| 4 | 192.168.10.130/25 と 192.168.10.20/25 | | | |

別サブネットの機器と通信するために、通常必要になるものは何ですか。 / What is normally required to communicate with a different subnet?

______________________________________________________________________________

## T4 通信仕様 / Communication specification

*参照 / Reference: 09-01 §8 TCP・UDP・ポート、演習C。*

PCからPLCの「現在の運転状態」を読む想定で、通信仕様を書きます。プロトコルとポートは「一般的な値」であり、実機では機器の仕様書で確認します。

Assume a PC reads the PLC's current run state. Protocol and port values are typical; confirm them in the device documentation.

| 項目 / Item | 記入 / Your answer |
|---|---|
| 通信する相手 / peer | |
| プロトコル / protocol | |
| ポート番号 / port | |
| 読み取るデータ / data | |
| データ型・表現 / data type | |
| 更新周期 / update period | |
| タイムアウト / timeout | |
| 通信喪失時の機械動作 / behaviour on loss | |
| 復旧時の動作 / behaviour on recovery | |

- 代表的な組合せを1つ書いてください。 / Write one typical pairing.

プロトコル / protocol: ____________　ポート / port: ____________

- 「リンクが点灯している」「pingが通る」「アプリがデータを読める」は別の事実です。それぞれ何を確認したことになるかを、一文ずつ書いてください。 / The three facts are different. State what each one proves.

______________________________________________________________________________

## T5 段階ゲート / Staged verification gates

*参照 / Reference: 09-02 §4 段階ゲート、演習A。*

前のゲートが完了するまで次へ進みません。実機の通電試験（G5）は、G0〜G4が完了し、承認された場合にだけ実施します。本研修ではG5を実施しません。

Do not pass a gate before the previous one is complete. The energised test (G5) happens only after G0–G4 and with approval. This course does not perform G5.

| ゲート / Gate | 確認すること / What to verify | 記録 / Record | NGならどうするか / If NG |
|---|---|---|---|
| G0 文書 / documentation | | | |
| G1 機械 / mechanical | | | |
| G2 電気（隔離）/ electrical, isolated | | | |
| G3 オフライン制御 / offline control | | | |
| G4 監督下準備 / supervised readiness | | | |
| G5 通電試験 / energised test | | | |
| G6 最終受入 / final acceptance | | | |

G5を実施しない場合、その試験をどう記録しますか。PASSにしてよい条件と合わせて書いてください。 / How do you record a test that was not performed? State when PASS is allowed.

______________________________________________________________________________

## T6 試験記録と合否の状態 / Test records and statuses

*参照 / Reference: 09-02 §7 シミュレーション試験、§8 試験記録の書き方、セル `commissioning-matrix` と `test-record`。*

試験記録は、第三者が同じ条件で再現できるように書きます。OK/NGだけでは不十分です。状態は4種類だけを使います。

A test record must let another person reproduce the conditions. OK/NG is not enough. Use exactly four statuses.

| 状態 / Status | 意味 / Meaning | 使ってよい場面 / When to use | 使ってはいけない場面 / Never use for |
|---|---|---|---|
| PASS | | | |
| FAIL | | | |
| NOT TESTED | | | |
| BLOCKED | | | |

シミュレーション試験の件数を確認してください。 / Check the counts of the simulated test matrix.

PASS: ______ 件　BLOCKED: ______ 件　FAIL: ______ 件　NOT TESTED: ______ 件

T11とT12がBLOCKEDである理由を書いてください。 / Why are T11 and T12 BLOCKED?

______________________________________________________________________________

1件の試験記録を完成させてください。T04（3秒タイマー）を例にします。実測はシミュレーション結果で構いませんが、「シミュレーション」と明記します。 / Complete one record, using T04 (3 s timer). Simulated actuals are acceptable if labelled as simulation.

| 欄 / Field | 記入 / Your answer |
|---|---|
| 試験ID / test ID | |
| 要求ID / requirement ID | |
| 前提条件 / preconditions | |
| 手順 / procedure | |
| 期待結果 / expected | |
| 実測 / actual | |
| 合否 / status | |
| 証跡 / evidence | |
| 実施者 / operator | |
| 日付 / date | |
| 是正処置 / corrective action | |

## T7 故障ケースの記録 / Fault case record

*参照 / Reference: 09-02 §7.1 異常ケース、§9 異常試験の設計、セル `fault-trace`。*

「前進指令を出したが、X3が最後までONにならない」という想定です。状態、出力、故障コードを記録し、タイムアウトが何を意味するかを考えます。

Assume the extend command is issued but X3 never turns ON. Record the state, outputs and fault code, and decide what the timeout means.

| 時点 / Point | 状態 / State | RUN | Y2 | T0 (ms) | 故障 / Fault |
|---|---|---|---|---|---|
| START押下 / START pressed | | | | | |
| 前進指令の直後 / just after extend | | | | | |
| タイムアウト / timeout | | | | | |
| リセット後 / after reset | | | | | |

- タイムアウトが意味することと、意味しないことを1つずつ書いてください。 / State one thing the timeout means and one thing it does not mean.
- 原因候補を3つと、最初に確認する順序を書いてください。 / Give three possible causes and the order in which to check them.

______________________________________________________________________________

- タイムアウト時間を延ばすことが対策にならない理由を書いてください。 / Why is lengthening the timeout not a fix?

______________________________________________________________________________

## T8 費用対効果 / Cost and benefit

*参照 / Reference: 09-03 §8 費用対効果、セル `payback-calculator` と `payback-sensitivity`。*

次の値は教材用の仮定です。式中間値も残してください。 / These are training assumptions. Keep the intermediate values.

- 1回あたりの削減時間 / time saved per occurrence: **12秒**　回数 / occurrences: **180回/日**
- 年間稼働日 / working days: **220日**　労務費換算 / labour rate: **2,400円/時**
- 設備総費用 / investment: **450,000円**（仮）　年間運用費 / operating cost: **0円**（仮）

| # | 量 / Quantity | 式 / Formula | 計算 / Working | 答え / Answer |
|---|---|---|---|---|
| 1 | 1日の削減時間 / time saved per day | 12 × 180 ÷ 60 | | ______ 分/日 |
| 2 | 年間の削減時間 / hours per year | | | ______ 時間/年 |
| 3 | 年間の労務費換算 / annual value | | | ______ 円/年 |
| 4 | 年間の純効果 / net annual value | 年間効果 − 運用費 | | ______ 円/年 |
| 5 | 単純回収期間 / simple payback | 450,000 ÷ 純効果 | | ______ 年 |

検算 / check: 年間効果は **316,800円/年**、単純回収期間は **1.42年** になります。合わない場合は、秒→分→時間の換算と、投資÷純効果の向きを見直してください。 / The annual value should be **316,800 JPY/year** and the payback **1.42 years**; if not, recheck the time conversion and the direction of the division.

- 運用費が年間 **50,000円** の場合の回収期間を計算してください。 / Recalculate the payback with an operating cost of 50,000 JPY per year.

______________________________________________________________________________

- この年間効果が「実現する利益」と一致しない理由を2つ書いてください。 / Give two reasons this annual value is not realised profit.
- この回収期間の計算から抜けている費用を2つ書いてください。 / Name two costs missing from the payback.

______________________________________________________________________________

## T9 最終提案チェック / Final proposal check

*参照 / Reference: 09-03 §4 一貫性の確認、§5 提案書の構成、§12 最終課題、セル `proposal-check`。*

提案書では、同じ値を複数の場所に書きます。値が食い違うと、提案全体の信頼性が落ちます。自分の提案について、値と根拠を対応させてください。

A proposal states the same values in several places. Inconsistent values undermine the whole proposal. Match each value to its evidence.

| 確認項目 / Check | 提案の値 / Value in your proposal | 根拠 / Evidence | 一致 / Agree |
|---|---|---|---|
| 要求能力と実力能力 / required versus effective capacity | | | |
| シリンダ推力とワーク質量・摩擦 / cylinder force versus mass and friction | | | |
| センサー数とI/O入力数 / sensors versus inputs | | | |
| 電磁弁数とI/O出力数 / valves versus outputs | | | |
| シーケンス状態と試験項目 / states versus test items | | | |
| 通信要件とIP・プロトコル・ポート / network requirement versus settings | | | |

提案書に含める項目を確認してください。空欄には理由を書きます。 / Check the required proposal items; give a reason for any blank.

| # | 項目 / Item | 有 / Yes | 根拠の場所 / Where the evidence is |
|---|---|---|---|
| 1 | 現状課題と測定可能な目標 / problem and measurable target | □ | |
| 2 | タクト・サイクル・実力能力 / takt, cycle and effective capacity | □ | |
| 3 | 方式比較と採用理由 / concept comparison and selection | □ | |
| 4 | 機械構想とアクチュエータ候補 / mechanical concept and actuator candidates | □ | |
| 5 | 電気機器とI/O表 / electrical equipment and I/O map | □ | |
| 6 | シーケンスと異常処理 / sequence and fault handling | □ | |
| 7 | 通信仕様 / network specification | □ | |
| 8 | 試運転・受入試験とリスク / commissioning, acceptance tests and risks | □ | |
| 9 | 投資・運用費・効果・回収 / investment, operating cost, benefit and payback | □ | |
| 10 | 次のステップ（責任者・期限）/ next steps with owner and date | □ | |

未確定の仕様を3つ選び、「誰が・いつまでに・何を確認するか」を書いてください。 / Choose three open specifications and state who confirms what, by when.

| # | 未確定仕様 / Open specification | 確認者 / Owner | 期限 / Due | 方法 / Method |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

実装前に残る最大のリスクを1つ選び、その理由を書いてください。 / Name the largest remaining risk and why.

______________________________________________________________________________

## 完了チェックリスト / Completion checklist

- [ ] T1 /24と/25のネットワーク・ブロードキャスト・範囲を計算した / calculated both subnets
- [ ] T1 ホスト部のビット数から割当可能数を出した / derived the count from the host bits
- [ ] T2 重複しないIPを割り当て、予約アドレスを避けた / allocated unique addresses and avoided reserved ones
- [ ] T3 4組をマスクと一緒に判定した / judged four pairs with the mask
- [ ] T4 プロトコル・ポート・喪失時の動作を書いた / wrote protocol, port and loss behaviour
- [ ] T5 7ゲートの確認・記録・NG時の対応を書いた / completed the seven gates
- [ ] T6 4つの状態を定義し、PASSとBLOCKEDを区別した / defined four statuses and separated PASS from BLOCKED
- [ ] T6 試験記録の11欄を埋めた / completed all eleven record fields
- [ ] T7 タイムアウトの意味と原因候補を書いた / explained the timeout and candidate causes
- [ ] T8 316,800円/年と1.42年を式付きで計算した / calculated the annual value and payback with formulas
- [ ] T8 回収期間の限界と抜けている費用を書いた / stated the limits and missing costs
- [ ] T9 6項目の一貫性を確認した / checked six consistency items
- [ ] T9 提案書の必須10項目を確認した / checked the ten required proposal items
- [ ] T9 未確定仕様に責任者と期限を書いた / gave owners and dates for open specifications
- [ ] 実機の通電・空圧・動作・ネットワーク変更を行っていない / did not energise, pressurise, move equipment or change a real network
