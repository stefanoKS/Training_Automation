# 第9日 解答例と採点の観点 / Day 9 Answer Key (instructor copy)

**学生には配布しません。 / Do not distribute to students.**

**採点の原則 / Marking principles**

数値が一致しただけでは正解にしません。式、単位、マスクとの組み合わせ、そして「その数字が何を意味するか」の説明を確認します。特に、BLOCKEDをPASSとして扱う答案、実機の通電試験を実施したと書く答案、実在ネットワークの設定を変更したと書く答案は、内容の正誤にかかわらず受理しません。

A matching number is not a correct answer. Check the formula, the units, the mask that goes with the address, and the explanation of what the number means. In particular, an answer that records BLOCKED as PASS, claims a real energised test, or claims a change to a real network is not accepted regardless of its arithmetic.

**この解答例の位置づけ / Status of this key:** 架空ネットワークと教材のシミュレーションに基づきます。実ネットワーク、実機の試運転、投資判断を承認するものではありません。 / Fictional networks and training simulation only; this key approves no real network, commissioning or investment.

## T1 /24と/25のサブネット計算 / /24 and /25 subnet calculations

**期待される答え / Expected answers**

| 項目 / Item | 192.168.10.0 **/24** | 192.168.10.128 **/25** |
|---|---|---|
| マスク / mask | 255.255.255.0 | 255.255.255.128 |
| ネットワーク部のビット / network bits | 24 | 25 |
| ホスト部のビット / host bits | 8 | 7 |
| ネットワークアドレス / network | 192.168.10.0 | 192.168.10.128 |
| ブロードキャスト / broadcast | 192.168.10.255 | 192.168.10.255 |
| 割当可能な先頭 / first host | 192.168.10.1 | 192.168.10.129 |
| 割当可能な末尾 / last host | 192.168.10.254 | 192.168.10.254 |
| 割当可能数 / usable count | **254** | **126** |
| 割当可能数の式 / count formula | 2⁸ − 2 = 254 | 2⁷ − 2 = 126 |

- `192.168.10.20/25` は **192.168.10.0/25** に入ります。ネットワーク .0、ブロードキャスト .127、割当可能範囲 **.1〜.126**（126個）。 / `192.168.10.20/25` sits in `192.168.10.0/25`: network .0, broadcast .127, hosts .1–.126.
- 参考: /25 の2つのサブネットは `.0/25`（.0〜.127）と `.128/25`（.128〜.255）に分かれます。ブロードキャストがそれぞれ .127 と .255 になる点に注意します。 / A /24 splits into .0/25 and .128/25, with broadcasts .127 and .255.

**「先頭3オクテットが同じ」で判定できない理由 / Why the third octet is not enough**

`192.168.10.130/25` と `192.168.10.20/25` は、どちらも先頭3オクテットが `192.168.10` ですが、前者は `.128/25`、後者は `.0/25` に入るため別サブネットです。第3オクテットが同じでも、第4オクテットの最上位ビットがネットワーク部に含まれるかで境界が変わります。判定は必ずマスクと一緒に行います。

Both addresses share the first three octets, yet .130 is in .128/25 and .20 is in .0/25. The top bit of the fourth octet belongs to the network part under /25, so the boundary moves. Always judge with the mask.

**よくある誤り / Common mistakes**

- ネットワークアドレスを `.1`、ブロードキャストを `.254` と書く（ホストに割り当てる範囲と混同）。 / Swapping the network address with the first host.
- /25の割当可能数を 128 とする（ネットワークとブロードキャストを引いていない）。 / Reporting 128 usable hosts for /25.
- /25のブロードキャストを .127 と書く（.128/25 では .255）。 / Using .127 as the broadcast of .128/25.
- マスクを書かずに「同じネットワーク」と断定する。 / Judging without stating the mask.

**許容範囲 / Acceptable range**

ネットワークとブロードキャストは完全一致を要求します。割当可能数は 254 と 126、範囲は .1〜.254 と .129〜.254。末尾のホストを「.254まで」と書いていれば可。 / Exact match for network and broadcast; 254/126 and the stated ranges.

## T2 IPアドレスの割当 / IP allocation

**期待される答えの例 / Model allocation**

| 機器 / Device | IP | マスク / Mask | GW | 役割 / Role |
|---|---|---|---|---|
| PC | 192.168.10.10 | 255.255.255.0 | 192.168.10.1 | 設定・監視 / configuration and monitoring |
| PLC | 192.168.10.20 | 255.255.255.0 | 192.168.10.1 | 制御・状態の提供 / control and state |
| カメラ / camera | 192.168.10.30 | 255.255.255.0 | 192.168.10.1 | 画像 / image data |
| HMI | 192.168.10.40 | 255.255.255.0 | 192.168.10.1 | 表示・操作 / display and operation |
| 予備 / spare | 192.168.10.50 | 255.255.255.0 | 192.168.10.1 | 将来の増設 / future expansion |

- 使ってはいけないアドレスは **ネットワークアドレス .0** と **ブロードキャストアドレス .255**。前者はネットワーク自体を表し、後者は全ホスト宛てのため、個別の機器に割り当てられません。 / The network address .0 identifies the network and the broadcast .255 addresses all hosts, so neither can belong to one device.
- 重複の検査は、割当表のIPを並べ、同じ値がないかを確認します。ツールがあれば、稼働中の機器へのpingやARPの確認も行いますが、実ネットワークでは管理者の許可が必要です。 / List the addresses and compare; tools such as ping or ARP checks need administrator approval on a real network.
- 同じサブネット内なら、通常はゲートウェイを経由せずに通信できます。ゲートウェイは別サブネット宛ての出口です。 / Within one subnet, traffic normally does not need the gateway; it is the exit to another subnet.

**よくある誤り / Common mistakes**

- `.0` や `.255` を機器に割り当てる。 / Assigning .0 or .255.
- 2台に同じIPを割り当てる。 / Duplicate addresses.
- ゲートウェイに機器と同じIPを使う。 / Using a device address as the gateway.
- マスクを書かず、IPだけで「同じネットワーク」と判断する。 / Omitting the mask.

**許容範囲 / Acceptable range**

5台がすべて .1〜.254 の範囲にあり、重複せず、.0 と .255 を使っていなければ受理します。値そのものは自由ですが、GWが .1 であることと、役割が書かれていることを条件とします。 / Accept any five unique addresses in .1–.254 that avoid .0 and .255, provided the gateway is .1 and each role is stated.

## T3 同一サブネットの判定 / Same-subnet judgement

**期待される答え / Expected answers**

| # | 組合せ / Pair | 同一か / Same? | ネットワーク / Networks | 理由 / Reason |
|---|---|---|---|---|
| 1 | 192.168.1.30/24 と 192.168.1.40/24 | **同一 / same** | 192.168.1.0/24 | 同じマスクで計算したネットワークアドレスが一致。 |
| 2 | 192.168.1.30/24 と 192.168.2.40/24 | **別 / different** | 192.168.1.0 と 192.168.2.0 | 第3オクテットが違い、ネットワークが異なる。ルータが必要。 |
| 3 | 192.168.10.130/25 と 192.168.10.200/25 | **同一 / same** | 192.168.10.128/25 | どちらも .128〜.255 の後半に入る。 |
| 4 | 192.168.10.130/25 と 192.168.10.20/25 | **別 / different** | 192.168.10.128/25 と 192.168.10.0/25 | 同じ第3オクテットだが、/25で前半と後半に分かれる。 |

別サブネットの機器と通信するには、通常ルータと、各機器のデフォルトゲートウェイ設定が必要です。スイッチは同一LAN内の中継であり、ネットワーク間の経路は作りません。

Communication with another subnet normally needs a router and a default gateway on each device. A switch forwards within the LAN; it does not route between networks.

**よくある誤り / Common mistakes**

- 3番を「別」とする（/25の後半を同一と見られない）。 / Marking pair 3 as different.
- 4番を「同一」とする（第3オクテットだけで判断）。 / Marking pair 4 as the same from the third octet.
- 「ルータがあれば同じサブネット」と書く。 / Equating a router with same-subnet membership.

**許容範囲 / Acceptable range**

4組の判定は完全一致を要求します（同一・別・同一・別）。理由にネットワークアドレスが入っていることを条件とし、「第3オクテットが同じ」だけの理由は不受理です。 / The four verdicts must be same, different, same, different. The reason must cite the network address; the third octet alone is not accepted.

## T4 通信仕様 / Communication specification

**期待される答えの例 / Model specification**

| 項目 / Item | 記入例 / Example |
|---|---|
| 通信する相手 / peer | 産業用PCからPLCへ / industrial PC to PLC |
| プロトコル / protocol | Modbus TCP（例）/ example |
| ポート番号 / port | TCP 502（代表値。機器仕様で確認）/ typical, confirm |
| 読み取るデータ / data | 運転状態、故障コード、サイクル数 / RUN state, fault code, cycle count |
| データ型・表現 / data type | 16ビットレジスタ、ビット / 16-bit registers and bits |
| 更新周期 / update period | 100 ms（仮）/ hypothetical |
| タイムアウト / timeout | 500 ms（仮）、3回連続で異常 / hypothetical, three consecutive misses |
| 通信喪失時の機械動作 / behaviour on loss | 運転を継続し、監視を警報に切り替え、自動再起動しない / keep running, raise an alarm, never auto-restart |
| 復旧時の動作 / behaviour on recovery | 自動で運転を再開しない。人が確認して新しいSTART / no automatic resume; a person confirms and issues a fresh START |

**代表的なプロトコルとポート / Typical protocols and ports**

| プロトコル / Protocol | ポート / Port | 用途 / Use |
|---|---|---|
| Modbus TCP | TCP 502 | レジスタ・コイルの読み書き / register and coil access |
| EtherNet/IP（明示的）/ explicit | TCP 44818 | 設定・診断 / configuration and diagnostics |
| EtherNet/IP（I/O）/ implicit | UDP 2222 | 周期的なI/Oデータ / cyclic I/O data |
| HTTP | TCP 80 | 機器のWeb設定画面 / web configuration |
| SNTP | UDP 123 | 時刻同期 / time synchronisation |

いずれも代表値です。実機では機器のマニュアルで確認し、ファイアウォールやVLANで遮断されていないかを確認します。

All values are typical. Confirm them in the device manual and check that firewalls or VLANs do not block the traffic.

**3つの事実の区別 / The three facts**

- リンク点灯 = 物理層がつながっている。IP設定やアプリの正しさは分からない。 / Link LED means the physical layer is up; it says nothing about IP settings or the application.
- ping成功 = IP到達性がある。ただしICMPを返さない機器もあり、アプリ通信の成功は保証しない。 / Ping success shows IP reachability, not application success; some devices do not answer ICMP.
- アプリがデータを読める = プロトコル、ポート、アドレス、データ型まで一致している。 / Reading data proves the protocol, port, address and data type all match.

**よくある誤り / Common mistakes**

- IPアドレスだけ書いて、プロトコルとポートがない。 / Giving only the IP address.
- pingが通れば通信成功と書く。 / Treating ping as proof of application success.
- 通信喪失時に「自動で再開」と書く。 / Specifying automatic resume on communication loss.
- ポート番号を確定値として断定する。 / Asserting a port as a fixed requirement.

**許容範囲 / Acceptable range**

相手・プロトコル・ポート・更新周期・タイムアウト・喪失時の動作がすべて埋まり、喪失時に「自動再開しない」と書かれていれば受理します。プロトコルはModbus TCPに限らず、EtherNet/IPなどでも、ポートを機器仕様で確認すると書いてあれば可。 / Accept when peer, protocol, port, period, timeout and loss behaviour are filled and loss behaviour excludes automatic resume. Modbus TCP is not mandatory if the port is to be confirmed in the device documentation.

## T5 段階ゲート / Staged verification gates

**期待される答え / Expected answers**

| ゲート / Gate | 確認すること / What to verify | 記録 / Record | NGならどうするか / If NG |
|---|---|---|---|
| G0 文書 / documentation | 要求、図面、BOM、I/O表、ラダー、試験計画、変更履歴 / requirements, drawings, BOM, I/O, ladder, test plan, changes | レビュー結果と版 / review result and revision | 文書を修正し、再レビュー。次へ進まない / fix and re-review |
| G1 機械 / mechanical | 取付、ボルト、ガイド、ストローク、干渉、カバー、挟まれ / mounting, bolts, guide, stroke, interference, cover, pinch | 検査記録と写真（許可範囲）/ record and photos if permitted | 修正して再検査 / correct and re-inspect |
| G2 電気（隔離）/ electrical | 図面照合、極性、短絡、端子、保護、接地、無電圧 / drawing, polarity, short, terminals, protection, earth, zero energy | 無電圧確認とロックアウトの記録 / zero-energy and lockout record | 配線を修正し、有資格者が再確認 / fix and re-check |
| G3 オフライン制御 / offline | 自己保持、I/Oトレース、タイマー、異常処理、再起動防止 / ladder, trace, timer, faults, restart | シミュレーションのログ / simulation log | ラングを修正し、試験を再実行 / fix and re-run |
| G4 監督下準備 / readiness | 実機の状態、ガード、隔離、残留エネルギー、復旧手順 / state, guard, isolation, stored energy, recovery | 監督者の承認 / supervisor approval | 承認を取り消し、準備をやり直す / withdraw approval |
| G5 通電試験 / energised | 承認された手順、立会い、観察、記録 / approved procedure, witness, observation | 立会い記録 / witnessed record | 中止し、原因を記録。無承認では再開しない / stop and record |
| G6 最終受入 / acceptance | 要求仕様との照合、記録、引継ぎ、教育 / requirements, records, handover, training | 受入記録 / acceptance record | 未達項目を不具合リストへ / add to the defect list |

**G5を実施しない場合の記録 / Recording an unperformed G5**

**BLOCKED**（前提条件・許可・設備がない）または **NOT TESTED**（まだ実施していない）と記録します。PASSにしてよいのは、承認された手順で実施し、観察結果が期待と一致し、証跡と実施者が記録された場合だけです。未実施をPASSに読み替えることは、試験記録の意味を失わせます。

Record **BLOCKED** (preconditions, approval or equipment missing) or **NOT TESTED** (not yet performed). PASS requires an approved procedure, an observation matching the expectation, and recorded evidence and operator. Reinterpreting an unperformed test as PASS destroys the meaning of the record.

**よくある誤り / Common mistakes**

- G2を飛ばしてG5へ進む。 / Skipping G2 and jumping to G5.
- G5を「時間がないのでPASS」とする。 / Marking G5 PASS because time ran out.
- ゲートの承認者を本人だけにする。 / Self-approval at every gate.

**許容範囲 / Acceptable range**

7ゲートすべてに確認・記録・NG時の対応が入っていれば受理します。G5が「未実施」または「承認時のみ」と書かれ、G2を飛ばしていなければ可。表現の違いは問いません。 / Accept when all seven gates have a check, a record and an NG action, G5 is marked unperformed or approval-only, and G2 is not skipped.

## T6 試験記録と合否の状態 / Test records and statuses

**期待される答え / Expected answers**

| 状態 / Status | 意味 / Meaning | 使ってよい場面 / When to use | 使ってはいけない場面 / Never for |
|---|---|---|---|
| PASS | 期待と実測が一致した / actual matched the expectation | 手順どおり実施し、証跡がある / performed as specified with evidence | 未実施、前提未達、シミュレーションのみを実機の合格とする / unperformed or simulated-only hardware claims |
| FAIL | 期待と一致しなかった / did not match | 実施して不一致を観測した / performed with a mismatch | 原因不明のまま保留したいとき / parking an unexplained result |
| NOT TESTED | まだ実施していない / not yet performed | 計画はあるが未実施 / planned but not done | 実施を忘れたまま放置 / forgotten work |
| BLOCKED | 前提・許可・設備がなく実施できない / cannot be performed | 承認や設備がない / approval or equipment missing | PASSの代用 / a substitute for PASS |

**シミュレーション試験の件数 / Simulated test counts**

PASS: **10** 件　BLOCKED: **2** 件　FAIL: **0** 件　NOT TESTED: **0** 件

T11は実機の通電試験、T12は安全機能の検証であり、どちらも承認された設備・隔離手順・有資格者の監督（T12はさらにリスクアセスメントと検証済みの安全関連システム）を必要とします。本研修では実施しないため **BLOCKED** です。シミュレーションのPASSは実機のPASSではありません。

T11 is an energised hardware test and T12 is safety-function validation. Both need approved equipment, isolation procedures and qualified supervision; T12 also needs a risk assessment and a validated safety-related system. Neither is performed here, so both are BLOCKED. A simulation PASS is not a hardware PASS.

**T04の記録例 / Model T04 record**

| 欄 / Field | 記入例 / Example |
|---|---|
| 試験ID / test ID | T04 |
| 要求ID / requirement ID | R-04 |
| 前提条件 / preconditions | 運転状態、後退端確認、STOP許可ON / RUN established, retracted confirmed, STOP_OK on |
| 手順 / procedure | STARTを押して離し、T0が3,000 msに達するまで待つ / press and release START, wait for T0 = 3,000 ms |
| 期待結果 / expected | T0=2,999 msでY1 OFF、T0=3,000 msでY1 ON |
| 実測 / actual | T0=2,999 ms Y1 OFF、T0=3,000 ms Y1 ON（シミュレーション）/ simulated |
| 合否 / status | PASS |
| 証跡 / evidence | オフラインのシミュレーションログ、2026-11-23 / offline simulation log |
| 実施者 / operator | 研修生（役割）/ trainee role |
| 日付 / date | 2026-11-23 |
| 是正処置 / corrective action | なし / none |

**よくある誤り / Common mistakes**

- 状態に OK、NG、保留 を使う。 / Using OK, NG or "pending" as a status.
- 「実測」に期待値をそのまま写す。 / Copying the expectation into the actual column.
- 証跡欄が空、または「画面を見た」だけ。 / Empty evidence or "I looked at the screen".
- シミュレーションを実機の合格として書く。 / Presenting simulation as a hardware pass.

**許容範囲 / Acceptable range**

4状態の意味が正しく、件数が PASS 10・BLOCKED 2・FAIL 0・NOT TESTED 0 と一致し、T04の11欄が埋まっていれば受理します。証跡が「シミュレーション」と明記されていることを必須とします。 / Accept when the four meanings are correct, the counts are 10/2/0/0, and the T04 record has all eleven fields. The evidence must be labelled as simulation.

## T7 故障ケースの記録 / Fault case record

**期待される答え / Expected answers**

| 時点 / Point | 状態 / State | RUN | Y2 | T0 (ms) | 故障 / Fault |
|---|---|---|---|---|---|
| START押下 / START pressed | READY | 1 | 0 | 0 | なし / none |
| 前進指令の直後 / after extend | EXTEND → WAIT_EXTENDED | 1 | 1 | 増加 / rising | なし / none |
| タイムアウト / timeout | **FAULT** | **0** | **0** | 0 | **F001** |
| リセット後 / after reset | **IDLE** | **0** | **0** | 0 | なし / none |

シミュレーションでは、前進指令の後もX3がONにならないため、タイムアウトでF001になり、記録上の時刻は **3,350 ms** でした。Y2とRUNは0になります。 / In the simulation the missing X3 produced F001 at 3,350 ms on the trace, with Y2 and RUN at 0.

**タイムアウトが意味すること／しないこと / What it does and does not mean**

- 意味すること: 指令した動作が、設定時間内に位置確認できなかったという事実。 / It means the commanded motion was not confirmed within the set time.
- 意味しないこと: シリンダが壊れた、センサーが故障した、という診断。原因は複数あり得ます。 / It is not a diagnosis that the cylinder or sensor failed; several causes remain possible.

**原因候補と確認順序 / Candidate causes and order**

1. **圧力不足**: 供給圧とシリンダ部の圧力を測る。遮断弁の開閉、レギュレータ設定を確認。 / Low pressure: measure supply and at-cylinder pressure; check the isolation valve and regulator.
2. **機械の詰まり・干渉**: 手で動かせる範囲か、ガイドやワークの引っかかりを確認。 / Jam or interference: check free travel by hand where safe, and guide or workpiece snags.
3. **センサー位置・配線・弁**: X3の取付位置、応答、配線、弁の切替を確認。 / Sensor position, wiring or valve: check X3 mounting, response, wiring and valve switching.

順序は、機械を動かさずに測れるもの、次に状態を観測できるもの、最後に分解や調整が必要なものです。安全な隔離の下で行います。 / The order goes from measurements that need no motion, to observable states, to work needing adjustment, all under safe isolation.

**タイムアウトを延ばすことが対策にならない理由 / Why a longer timeout is not a fix**

タイムアウトは「確認できなかった」という事実の検出であり、原因そのものではありません。時間を延ばすと、異常が見えなくなるだけで、圧力不足や詰まりは残ります。また、異常時の停止が遅れ、被害が大きくなる可能性があります。

The timeout detects the fact that confirmation did not arrive; it is not the cause. Extending it hides the symptom while the low pressure or jam remains, and it delays the stop, which can make the consequence worse.

**よくある誤り / Common mistakes**

- 原因を1つに断定する。 / Declaring a single cause.
- タイマーを延ばす、センサーを無効にする、を対策とする。 / Lengthening the timer or disabling a sensor as the fix.
- リセット後に自動で再開する記録を書く。 / Recording an automatic restart after reset.

**許容範囲 / Acceptable range**

タイムアウト時の状態がFAULT、RUNとY2が0、故障がF001、リセット後がIDLEであることが一致すれば受理します。原因候補は3つ以上で、確認順序に理由があれば、順序そのものは問いません。 / Accept when the timeout state is FAULT with RUN and Y2 at 0 and fault F001, and the post-reset state is IDLE. Three or more candidate causes with a reasoned order are acceptable regardless of the exact order.

## T8 費用対効果 / Cost and benefit

**期待される答え / Expected answers**

| # | 量 / Quantity | 式と代入 / Formula and substitution | 答え / Answer |
|---|---|---|---|
| 1 | 1日の削減時間 / time per day | 12 × 180 = 2,160 秒 ÷ 60 | **36.0 分/日**（0.6 時間/日） |
| 2 | 年間の削減時間 / hours per year | 0.6 × 220 | **132.0 時間/年** |
| 3 | 年間の労務費換算 / annual value | 132 × 2,400 | **316,800 円/年（316800 JPY/year）** |
| 4 | 年間の純効果 / net annual value | 316,800 − 0 | **316,800 円/年** |
| 5 | 単純回収期間 / simple payback | 450,000 ÷ 316,800 | **1.42 年（1.42 years、約1年5か月）** |

- 運用費50,000円/年では、純効果 316,800 − 50,000 = 266,800円/年、回収期間 450,000 ÷ 266,800 = **1.69 年**。運用費100,000円なら 216,800円/年で **2.08 年**。 / With 50,000 JPY the payback becomes 1.69 years; with 100,000 it becomes 2.08 years.
- 別の見方: 1日の効果は 0.6 × 2,400 = **1,440円/日**。450,000 ÷ 1,440 = **312.5稼働日**。月あたり 316,800 ÷ 12 = 26,400円、450,000 ÷ 26,400 = 約17.0か月。 / The daily value is 1,440 JPY, so the payback is 312.5 working days, or about 17.0 months.

**「利益と一致しない」理由 / Why it is not realised profit**

1. 316,800円は、削減した時間を労務費に換算した**仮の値**であり、人員の再配置や残業削減が実現しなければ、そのまま現金の利益にはならない。 / It is a hypothetical conversion of saved time; without redeployment or reduced overtime it is not cash.
2. 電気・エア・保守・消耗品・段取り・停止損失などの運用費を含んでいない。 / Operating costs such as power, air, maintenance, consumables, changeover and downtime are excluded.
3. 故障時の停止損失、品質不良、教育時間、立上げ損失を含んでいない。 / Downtime loss, quality loss, training and ramp-up are excluded.

**抜けている費用 / Missing costs**

- 設計・組立・配線・試運転・ガード・検査・搬入・予備品・教育（設備費に含めるべき費用）。 / Design, assembly, wiring, commissioning, guards, inspection, transport, spares and training.
- 運用費（電気、エア、保守、消耗品）。 / Operating costs: power, air, maintenance, consumables.
- 税金、減価償却、資金コスト。 / Tax, depreciation and cost of capital.

**よくある誤り / Common mistakes**

- 12 × 180 = 2,160 をそのまま「2,160分」と書く（秒を分に換算していない）。 / Reporting 2,160 minutes instead of converting seconds to minutes.
- 220日を掛け忘れて、1,440円/年とする。 / Forgetting the working days.
- 450,000 ÷ 316,800 を 0.70年 と計算する（分母と分子が逆）。 / Inverting the payback division.
- 1.42年を「1.42か月」と書く。 / Writing 1.42 months.
- 316,800円を「確実な利益」と断定する。 / Asserting the value as guaranteed profit.

**許容範囲 / Acceptable range**

36.0分/日、132.0時間/年、316,800円/年、1.42年（1.420〜1.421）。1.4年、約17か月、312〜313稼働日も可。ただし式が示されていることを条件とします。 / Accept 1.4 years, about 17 months or 312–313 working days, provided the formula is shown.

## T9 最終提案チェック / Final proposal check

**期待される状態 / What a consistent proposal looks like**

| 確認項目 / Check | 一致の条件 / Condition for agreement |
|---|---|
| 要求能力と実力能力 | 必要能力 85.71個/時 < 実力能力 199.92個/時。要求が実力を上回っていない。 / required below effective. |
| シリンダ推力とワーク質量・摩擦 | 設計力 39.24 N の根拠（8 kg、μ 0.25、余裕2）がBOMと計算書で同じ。 / the same basis in the BOM and the calculation. |
| センサー数とI/O入力数 | 位置センサー2個＋START＋STOP許可＝入力4点（X0〜X3）。 / two position sensors plus START and STOP permission give four inputs. |
| 電磁弁数とI/O出力数 | 前進弁1個＝Y2。Y1は遅延ランプで、弁に使わない。 / one extend valve on Y2; Y1 stays a lamp. |
| シーケンス状態と試験項目 | IDLE〜FAULTの各遷移に試験IDが対応し、未実施はBLOCKEDまたはNOT TESTED。 / every transition maps to a test id, with unperformed tests marked honestly. |
| 通信要件とIP・プロトコル・ポート | 読む相手、プロトコル、ポート、更新周期、喪失時の動作が仕様書と構成図で同じ。 / peer, protocol, port, period and loss behaviour agree. |

**提案書の必須項目 / Required proposal items**

10項目のうち、空欄があっても理由が書かれていれば受理します。ただし、5（電気機器とI/O表）、7（通信仕様）、10（次のステップ）が空のままでは、提案として完結しません。各項目の「有」は、該当する図・表・計算書の場所が示されていることを条件とします。

Among the ten items, a blank is acceptable only with a stated reason. A proposal is incomplete if item 5 (electrical equipment and I/O), 7 (network specification) or 10 (next steps) is blank. Each "yes" requires the location of the supporting drawing, table or calculation.

**未確定仕様の書き方の例 / Model open specification**

```text
未確定: シリンダに実際にかかる圧力
確認者: 設備担当
期限: 試作前
方法: 圧力計で3条件を測定
判断: 設計力39.24 Nに対して余裕があるか
```

「未確定」とだけ書かず、誰が、いつまでに、何を、どの方法で確認するかを書きます。 / Never write only "undecided": state who confirms what, by when and how.

**よくある誤り / Common mistakes**

- 提案書の能力値が、計算書と発表資料で違う。 / Different capacity values in the sheet and the slides.
- センサー数を「2個」と書きながら、I/O表に5入力ある。 / Two sensors claimed but five inputs listed.
- Y1を電磁弁として提案書に書く。 / Using Y1 for the solenoid in the proposal.
- 未確定仕様に責任者も期限もない。 / No owner or date for open items.
- 「安全はPLCで担保する」と書く。 / Claiming PLC logic provides safety.

**許容範囲 / Acceptable range**

提案の数値そのものは現場で決まります。6項目すべてに「提案値・根拠・一致」の3つが入り、未確定仕様に確認者と期限があれば受理します。値が要求と違っても、意図した差（例: 要求85.7個/時に対し提案90個/時）が説明されていれば可。 / The values depend on the site. Accept when all six rows carry a value, its evidence and an agreement, and open specifications have an owner and a date. A value that differs from the requirement is acceptable when the intended difference is explained.
