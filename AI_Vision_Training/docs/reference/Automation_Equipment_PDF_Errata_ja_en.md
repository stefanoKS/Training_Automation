# 元PDF 技術正誤表 / Source PDF technical errata (Japanese–English)

**対象 / Subject:** `docs/reference/自動化設備製作研修_5日間_詳細版_受講者用.pdf`
**SHA-256:** `3380c2b67e148cd9a71b0f9071963744f3b0acba7491b309708b0f31183707ae`
**ページ数 / Pages:** 51
**方針 / Policy:** 元PDFは一次資料として変更しない。教育上の誤りは、この正誤表と新しいDay 7–9教材で修正する。
The source PDF is the primary reference and is **not modified**. Teaching errors are corrected in this errata and in the replacement Day 7–9 materials.

> 本正誤表は、元PDFのすべての記述を否定するものではありません。学習目標、例、計算の流れは尊重し、技術的に誤解を招く箇所、または初心者に不足している説明を明確にします。
> This errata does not reject the source PDF. It preserves its learning objectives, examples and workflow, and clarifies statements that are technically misleading or insufficient for beginners.

---

## E-01 自己保持回路に並列保持接点がない（PDF p.31）

### 原文の状態 / what the source shows

p.31「ラダーの基礎：接点・コイル・自己保持」の図は、START接点とSTOP（許可）接点を直列にし、M0コイルへ接続しています。M0の接点は別の行でY0を駆動していますが、**STARTと並列にM0を接続する保持枝がありません**。

The p.31 figure places START and STOP(permission) in series to the M0 coil. M0's contact drives Y0 on another rung, but there is **no holding branch in parallel with START**.

### 問題 / problem

この図のままでは、STARTを離した瞬間にM0が落ち、運転状態が保持されません。自己保持の説明と図が一致していません。また、STARTとSTOPのラベルが図上で重なって読みにくくなっています。

With this rung, M0 drops as soon as START is released; the RUN state is not held. The explanation and the diagram disagree. The START and STOP labels also overlap and are hard to read.

### 修正 / correction

正しい自己保持は、**開始条件**と**保持条件**を分けます。

Correct self-holding separates the **start condition** from the **run/hold condition**.

```text
|--+--[ X0 ]--[ X2 ]--+--[ X1 ]--( M0 )--|
|  |                  |
|  +--[ M0 ]----------+
```

- **X0**: START（押している間ON）/ START, ON while pressed
- **X2**: 後退端確認。**開始時だけ**必要 / retracted confirmation, required **only at start**
- **M0**: 運転状態。自分の接点で保持 / RUN state, held by its own contact
- **X1**: 停止許可。健全時ON / stop permission, ON while healthy

M0の保持枝はX2を通りません。したがって、シリンダが前進してX2がOFFになってもRUNを維持できます。X2を保持枝に入れると、前進した瞬間にRUNが落ちます。

The M0 holding branch does not pass through X2, so RUN survives X2 turning OFF as the cylinder extends. Putting X2 in the holding branch would drop RUN as soon as the cylinder moves.

### 検証 / verification

- `D08-08.svg` に正しい回路を描いた / the corrected rung is drawn in D08-08.
- `automation_models.PusherSequence` で、START押下→離してもRUNが続くことをテスト / the simulator tests that RUN survives START release.
- ノートブック `Day08_03_Ladder_Sequence` の `sim-selfhold` セル / the `sim-selfhold` cell in the notebook.
- 試験: `test_start_release_self_holding_and_stop` / test name.

---

## E-02 順序制御に位置確認の状態がない（PDF p.32）

### 原文の状態 / what the source shows

p.32は「待機→前進→前進確認→後退→後退確認→完了」という流れを示しますが、表では「前進」の次条件が「前進端がON」となっており、**指令を出す状態と、到達を確認する状態**が明確に分かれていません。タイマーだけでは実動作を保証しない、という注意は書かれていますが、状態機械としては不完全です。

p.32 shows "idle → extend → confirm extend → retract → confirm retract → complete", but the table gives "extend end ON" as the next condition of the extend state. The **command state** and the **confirmation state** are not clearly separated. The text warns that a timer does not prove motion, but the state machine is incomplete.

### 問題 / problem

指令を出したことと、シリンダが実際に到達したことを混同すると、位置センサー故障や詰まりを見逃します。また、確認が来ない場合のタイムアウトと異常状態が定義されていません。

Confusing a command with arrival hides sensor failure and jamming. The source also does not define a timeout and fault state when confirmation never arrives.

### 修正 / correction

次の8状態を使います。

Use eight states.

| 状態 / State | 出力 / Outputs | 次へ進む条件 / Transition |
|---|---|---|
| IDLE | 全出力OFF / all OFF | 新規START、X1、X2 / fresh START, X1, X2 |
| READY | M0, Y0 ON | 次スキャンでEXTEND / next scan |
| EXTEND | Y2 ON（指令）/ command | WAIT_EXTENDEDへ / next scan |
| WAIT_EXTENDED | Y2 ON | X3 ON かつ X2 OFF / X3 ON and X2 OFF |
| RETRACT | Y2 OFF（指令）/ command | WAIT_RETRACTEDへ / next scan |
| WAIT_RETRACTED | Y2 OFF | X2 ON かつ X3 OFF / X2 ON and X3 OFF |
| COMPLETE | Y0 ON、T0完了でY1 / Y0 ON, Y1 after T0 | 新規START / fresh START |
| FAULT | 全出力OFF、警報 / all OFF, alarm | リセット＋新規START / reset + fresh START |

タイムアウトはF001（前進端未確認）とF003（後退端未確認）、前後端同時ONはF002とします。3秒は教材上の仮値です。

Timeouts are F001 (extend confirmation missing) and F003 (retract confirmation missing); both end sensors ON is F002. The 3 s value is a training assumption.

### 検証 / verification

- `D08-09.svg` と `D08-11.svg` / diagrams.
- `normal_cycle`, `sensor_stuck_off`, `sensor_conflict`, `motion_slow` のシミュレーションテスト / simulation tests.
- ノートブック `Day08_03` の状態遷移表と I/O トレース / state table and I/O trace.

---

## E-03 Y1の用途が一貫していない（PDF p.27 と p.31–33）

### 原文の状態 / what the source shows

p.27のI/O表では **Y0 = 運転ランプ、Y1 = 動作指令ランプ** です。一方、p.31–33の例では、Y0が運転状態、Y1が3秒後の遅延ランプとして使われ、電磁弁の出力アドレスが明確でありません。同じY1が、ランプと電磁弁の両方を指すように読める箇所があります。

p.27 assigns **Y0 = RUN lamp, Y1 = operation-command lamp**. In the p.31–33 examples, Y0 is the RUN state and Y1 is the delayed lamp after 3 s, while the solenoid output address is unspecified. Some readers can interpret Y1 as both a lamp and a valve.

### 問題 / problem

同じアドレスを異なる機器に使うと、配線・ラダー・HMI・試験記録が一致しません。実機では二重コイルや誤配線の原因になります。

Using one address for different devices breaks consistency across wiring, ladder, HMI and test records, and can cause double-coil or wiring errors on a real machine.

### 修正 / correction

Day 8–9の**統一I/O表**を次のように固定します。

The canonical I/O for Days 8–9 is fixed as follows.

| アドレス / Address | 機器 / Device |
|---|---|
| X0 | START押しボタン / START pushbutton |
| X1 | STOP_OK（物理NC、健全時ON）/ physical NC stop, ON while healthy |
| X2 | 後退端確認 / retracted confirmation |
| X3 | 前進端確認 / extended confirmation |
| M0 | 運転状態 / RUN state |
| Y0 | 運転ランプ / RUN lamp |
| Y1 | 遅延ランプ（T0完了）/ delayed lamp, T0 done |
| Y2 | 前進電磁弁指令 / extend solenoid command |
| T0 | 3秒オン遅延 / 3 s on-delay |

- Y1は**ランプ専用**。電磁弁はY2。
- 実機の端子番号は別。アドレスは架空の訓練用。
- `validate_io()` がY1の電磁弁流用とX1の正常状態の誤りを検出する。

- Y1 is **lamp only**; the valve is Y2.
- Physical terminal numbers are separate; these addresses are fictional training values.
- `validate_io()` detects Y1 solenoid reuse and an incorrect X1 normal state.

### 検証 / verification

`test_canonical_io_is_unambiguous`, `test_io...` in the notebook, and `Day08_02`'s `io-validation` cell.

---

## E-04 シリンダ選定の誤解を招く書き方（PDF p.15）

### 原文の状態 / what the source shows

p.15は、8 kg、μ=0.25、余裕係数2、0.4 MPaから、摩擦力19.6 N、設計力39.2 N、理論内径11.2 mmを導きます。注意書きはありますが、表の流れは「カタログ選定」へ直結して見え、11.2 mmを超える最小内径を選ぶように読めます。

p.15 derives 19.6 N friction, 39.2 N design force and 11.2 mm theoretical bore from 8 kg, μ=0.25, factor 2 and 0.4 MPa. A caution exists, but the table flows directly into "catalogue selection" and can be read as "choose the smallest bore above 11.2 mm".

### 問題 / problem

理論内径は、単純化した1条件での下限です。実際のシリンダ圧力は供給圧より低いことがあり、加速・衝撃・ガイド抵抗・偏荷重・クッション・負荷率・速度制限を無視しています。11.18 mmを超える最小内径をそのまま選ぶと、不足する可能性があります。

The theoretical bore is a lower bound under one simplified condition. Actual cylinder pressure can be below supply pressure, and the calculation ignores acceleration, impact, guide resistance, side load, cushioning, load factor and speed limits. Choosing the smallest bore above 11.18 mm can be insufficient.

### 修正 / correction

- 数値は維持: 19.62 N、39.24 N、11.18 mm。
- **理論下限 / theoretical lower bound** と **カタログ候補 / catalogue candidate** を別の欄にする。
- 候補は複数示し、負荷率・速度・モーメント・圧力損失・センサー対応・取付を確認する。
- 特定の実機型式を割り当てない。16 mmは「比較用の仮の候補」であり、選定結果ではない。
- ロッド側の有効面積（D²−d²）を明示する。

- Keep the numbers: 19.62 N, 39.24 N, 11.18 mm.
- Separate the **theoretical lower bound** from a **catalogue candidate**.
- Show several candidates and require checks for load factor, speed, moment, pressure loss, sensing and mounting.
- Do not assign a real part number. The 16 mm value is a **comparison candidate**, not a selection.
- State the rod-side effective area (D²−d²).

### 検証 / verification

`test_mechanical_numbers`; `Day07_03`'s `cylinder-calculator`; the explicit caption "not a selection" in the notebook and PDF.

---

## E-05 モーター・減速機の効率が示されていない（PDF p.17）

### 原文の状態 / what the source shows

60 W、1200 rpm、減速比20:1から、軸トルク約0.477 N·m、出力回転数60 rpm、出力トルク約9.55 N·mを示します。減速機効率には触れていません。

It shows about 0.477 N·m motor torque, 60 rpm output speed and about 9.55 N·m output torque from 60 W, 1200 rpm and a 20:1 ratio, without mentioning reducer efficiency.

### 問題 / problem

9.55 N·mは**理想値**です。実際の出力トルクは効率、損失、温度、バックラッシュ、許容荷重で低下します。効率を明示しないと、実機のトルク余裕を過大評価します。

9.55 N·m is an **ideal** value. Real output torque is reduced by efficiency, losses, temperature, backlash and allowable load. Without stating efficiency, the torque margin is overstated.

### 修正 / correction

- 0.477 N·m、60 rpm、9.55 N·mは維持し、**理想値**と明記する。
- 追加の仮定としてη=0.90を明示し、8.59 N·mを示す。
- 0.90は教育用の仮定であり、実機の減速機効率ではないと書く。
- 起動トルク、慣性、連続定格、保持ブレーキ、ラジアル・アキシャル荷重、寿命を別に確認する。

- Keep 0.477 N·m, 60 rpm and 9.55 N·m and label them **ideal**.
- Add an explicit η = 0.90 assumption and show 8.59 N·m.
- State that 0.90 is a training assumption, not a real reducer efficiency.
- Require separate checks for starting torque, inertia, continuous rating, holding brake, radial/axial load and life.

### 検証 / verification

`test_motor_numbers`; `Day07_03`'s `motor-calculator` and `motor-curve`.

---

## E-06 NPN/PNPの説明に入力共通端子がない（PDF p.25）

### 原文の状態 / what the source shows

p.25は、NPNはON時に出力を0V側へ引き込み、PNPは＋側の電位を出す、と説明します。しかし、PLC入力の**共通端子（COM）**と入力回路を含む電流経路が示されていません。

p.25 explains that NPN pulls the output to 0 V and PNP outputs the positive potential, but it does not show the PLC input **common (COM)** or the current path through the input circuit.

### 問題 / problem

NPN/PNPは、センサー単体の性質ではなく、PLC入力の方式と共通端子の電位を含む**閉回路**で決まります。共通端子を無視すると、適合する組み合わせを誤ります。

NPN/PNP is not a property of the sensor alone; it is a **closed circuit** including the PLC input type and common potential. Ignoring the common leads to wrong compatibility conclusions.

### 修正 / correction

- PNP＋シンク入力（共通0V）: +24V → センサー → 出力 → PLC入力 → COM(0V)。
- NPN＋ソース入力（共通+24V）: +24V → COM → PLC入力 → センサー出力 → 0V。
- 2線式は漏れ電流とOFF時電圧を確認する。
- 実機の端子配置・入力方式はPLCハードウェアマニュアルで確認する。
- 本教材の「シンク/ソース」は教育用の整理であり、すべてのPLCに同じ用語が当てはまるわけではない。

- PNP with a sinking input (common 0 V): +24 V → sensor → output → PLC input → COM (0 V).
- NPN with a sourcing input (common +24 V): +24 V → COM → PLC input → sensor output → 0 V.
- Two-wire sensors require leakage and OFF-state voltage checks.
- Confirm terminal arrangement and input type in the PLC hardware manual.
- The sink/source labels are a teaching simplification; not every PLC uses the same terms.

### 検証 / verification

`D08-06.svg`, `Day08_02`'s `sensor-compatibility` cell, and tests of the fictional configurations A–E.

---

## E-07 電気・空圧の安全境界が弱い（PDF p.10, p.14, p.41）

### 原文の状態 / what the source shows

安全の注意は随所にありますが、次の点が初心者に明確ではありません。

- 通常のPLC STOPと、非常停止・安全機能の違い。
- 電磁弁の無通電が、シリンダの安全状態を保証しないこと。
- 遮断だけでは残圧が抜けないこと。
- 段階ゲートG5（通電試験）を、課程の必須項目と誤解しないこと。
- リセットが動作開始ではないこと。

Safety warnings exist, but beginners may not clearly see: the difference between ordinary PLC STOP and emergency stopping/safety functions; that a de-energised valve does not guarantee a safe cylinder; that isolation alone does not release residual pressure; that gate G5 (energised testing) is not a course requirement; and that reset is not a start command.

### 修正 / correction

- 通常のPLC制御と安全機能を、本文・図・試験で分離した。
- 実機の通電・空圧・動作・安全検証を、課程の必須から外した。
- G5は「該当する場合のみ、承認・立会い・有資格者のもとで行う」と明記した。
- 未実施は **BLOCKED** または **NOT TESTED** と記録し、PASSにしない。
- リセット後は新しいSTARTを要求し、リセット自体が動作を開始しないことをテストした。
- 復電時に保持ビットや押しっぱなしのSTARTで自動再起動しないことをテストした。

- Ordinary PLC control and safety functions are separated in text, diagrams and tests.
- Real energisation, pneumatics, motion and safety validation are not course requirements.
- G5 is described as "only if applicable, with approval, witness and qualified persons".
- Unperformed tests are **BLOCKED** or **NOT TESTED**, never PASS.
- Reset requires a fresh START and does not start motion; this is tested.
- Power restoration from a retained bit or a held START does not restart the machine; this is tested.

### 検証 / verification

`test_fault_reset_never_starts_motion`, `test_power_restore_with_held_start_and_new_start`, `D08-11`, `D09-06`, `D09-07`, and the commissioning matrix (T11/T12 BLOCKED).

---

## E-08 元PDFのレイアウト問題 / source PDF layout problems

元PDFは全体として読みやすい一方、次の問題があります。

The source PDF is generally readable but has these layout problems.

| 問題 / Problem | 例 / Example | 新教材での扱い / treatment in the replacement |
|---|---|---|
| 改行位置の不自然さ / awkward line breaks | p.25「192.1\n68.2.20」のようなIPの分割 / IP split across lines | PDF生成時にIPv4を`<nobr>`で保護し、抽出テストで確認 / `<nobr>` protection and extraction test |
| 表セルの極端な細さ / very narrow cells | p.7、p.13など / p.7, p.13 | 列幅を文字幅から計算し、内容に応じて配分 / widths computed from text width |
| 図のラベルの重なり / overlapping labels | p.31のSTART/STOP / p.31 START/STOP | 図を再設計し、ラベル位置を分離 / redesigned diagram |
| 図が小さい / small figures | p.14のブロック図 / p.14 block flow | 機能的な空圧回路図を追加し、必要な要素を明示 / functional pneumatic schematic added |
| 生のHTML / raw HTML | p.51 の`<br/>` / p.51 `<br/>` | 新PDFではHTMLタグを除去・テスト / stripped and tested |
| 数式の折り返し / formula wrapping | 長い式・単位 / long expressions | コード/式は折り返し幅を制御 / controlled wrapping |

**検証 / verification:** `check_day07_09_pdfs.py` が全ページをPNGに描画し、テキスト抽出で `??`、生HTML、壊れたIPv4を検査する。レイアウトは目視でも確認する。
`check_day07_09_pdfs.py` renders every page, and extraction checks for `??`, raw HTML and broken IPv4. Layout is also reviewed visually.

---

## E-09 その他の改善 / other improvements

| 項目 / Item | 改善 / improvement |
|---|---|
| 5日→3日 / five days to three | 元の5日間の学習目標を、3日×3ノートブックに再配置。重複を削除し、実習時間を確保。 / remapped into three days and nine notebooks; duplicates removed |
| AI・カメラ中心の旧教材 / old vision-centred course | **2026-11-24 改訂で更新 / updated 2026-11-24:** 第9日は再び AI 検査カメラ（カメラ・レンズ・照明・撮像環境・構成）を中心とする内容になった。ただし今回は元PDFの機械・電気・PLCの流れを第7日・第8日に残している。 / Day 9 is again centred on the AI inspection camera, while the source PDF's mechanical, electrical and PLC flow stays in Days 7 and 8. |
| 用語の一貫性 / terminology | 「タクト」「サイクル」「停止許可」「リセット」などを用語集で固定。稼働率・良品率による能力計算は必須範囲から外した。 / fixed in the glossary; availability and yield capacity models were removed |
| BLOCKEDの扱い / BLOCKED | 未実施を合格にしない記録規則を追加。 / added a rule that unperformed tests are not passes |
| 初学者向け / beginners | 物理的意味→図→計算→演習→確認→期待結果の順に統一。 / consistent explanation → visual → worked example → exercise → check → expected result |

---

## E-10 2026-11-24 改訂後の参照先 / reference anchors after the 2026-11-24 revision

本文の技術的な修正内容は有効なままです。改訂でセル名・節番号・図番号が変わった箇所の現在の参照先を示します。履歴は書き換えていません。

The technical corrections above remain valid. Where the revision changed cell names, section numbers or figure numbers, the current anchors are listed below. The historical text is not rewritten.

| 旧参照 / old reference | 現在の参照 / current reference |
|---|---|
| `Day08_03` の `sim-selfhold` セル / the `sim-selfhold` cell | `Day08_03_Ladder_Sequence` の `seal-in-vs-extended`（基本回路と拡張ロジックの比較）/ the `seal-in-vs-extended` cell |
| `Day08_03` の状態遷移表 / state table | 08-03 §10「基本のシーケンス」と §8「拡張ロジック」 / sections 8 and 10 |
| `Day08_02` の `sensor-compatibility` セル | `Day08_02_Sensors_and_IO` の `npn-pnp` セル / the `npn-pnp` cell |
| `Day08_02` の `io-validation` セル | 08-02 §4 の統一I/O表と `validate_io` のテスト / the I/O table and `validate_io` test |
| `D08-06.svg`（センサー方式の図）/ sensor types figure | `D08-07.svg`。`D08-06` は入力→出力の信号の流れ / `D08-07`; `D08-06` is now the I/O signal flow |
| `Day07_03` の `cylinder-calculator` | `Day07_03` §6–§7（紙と電卓）と `test_mechanical_numbers` / sections 6-7 and the test |
| `Day07_03` の `motor-calculator` / `motor-curve` | `Day07_03` §8 と `test_motor_numbers` / section 8 and the test |
| `Day07_03` の `bom-hash` | 削除。BOM と版管理は必須教材から外した / removed with BOM and version fingerprinting |
| ネットワーク・試運転・提案の各節 / networking, commissioning, proposal sections | `Day09_Communication_Commissioning` は削除。相当する記述は `curriculum_source_map.csv` の `REMOVED_FROM_ACTIVE` / `SUPERSEDED_BY_NEW_AI_CAMERA` 行を参照 / the folder was removed; see the source-map rows |

**改訂後の数値の不変条件 / numeric invariants after the revision**

- タクト42秒/個、必要能力85.71個/時、理論能力240個/時（15秒・1個/サイクル）。
- 労務費換算316,800円/年、回収1.42年（運用費0）、1.69年（運用費50,000円）。
- 押し側157.08 N、引き側131.95 N（D20・d8・0.5 MPa）。11.18 mm は理論最小内径であり選定ではない。
- 電気負荷0.80 A / 19.2 W、計画1.00 A（25%は教材の仮定）。
- 1ピクセル0.125 mm/px、欠陥4 px、ぶれ1 mm / 8 px、露光0.125 ms、8,000 line/s、33.33 mm。

---

## 未解決・実機依存の事項 / open, hardware-dependent items

以下は、この教材だけでは確定できません。実機・メーカー資料・有資格者のレビューが必要です。

The following cannot be settled by this course alone. They require the real machine, manufacturer documents and qualified review.

- 実際のシリンダにかかる圧力、負荷率、許容モーメント、速度、クッション。
- 実際の摩擦係数、重心、ガイド抵抗、ワークの変形。
- 実機のPLC入力方式、端子配置、共通端子、出力定格、漏れ電流。
- 実機の弁型式、無通電位置、残圧、配管抵抗、エア品質。
- 実ネットワークのIP、VLAN、ルーティング、ファイアウォール、ポート。
- 安全機能の要求性能、保護方策、検証方法、規格適合。
- 実機の通電試験、空圧試験、異常試験、受入試験の結果。

- Actual cylinder pressure, load factor, allowable moment, speed and cushioning.
- Actual friction, centre of gravity, guide resistance and workpiece deformation.
- Actual PLC input type, terminals, commons, output ratings and leakage.
- Actual valve type, de-energised position, residual pressure, piping resistance and air quality.
- Real network IP, VLAN, routing, firewall and ports.
- Safety-function performance level, protective measures, validation and compliance.
- Real energised, pneumatic, abnormal and acceptance test results.

これらを、教材の仮定やシミュレーション結果と混同しないでください。

Do not confuse these with the course's assumptions or simulation results.
