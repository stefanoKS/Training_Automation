# 第8日 講師ガイド / Day 8 Instructor Guide

教材 / material: `notebooks/Day08_Electrical_PLC/`（01–03）、`assets/diagrams/day08/`、`day07_09_support/examples/automation_models.py`、`docs/pdf/Day08_explanation_ja_en.pdf`、`day07_09_support/worksheets/Day08_Student_Worksheet_ja_en.md`、`day07_09_support/simulations/sim_plc_sequence.html`。

> このガイドは講師用です。受講者に配布する必要はありません。
> This guide is for the instructor and need not be distributed.

## 1. 学習目標 / learning objectives

受講者は次のことを説明できるようになります。 / Trainees should be able to explain:

1. AC100/200V、DC24/12/5Vの使い道と、電圧だけでは制御用・動力用が決まらないこと。
2. 制御盤の主要機器の役割と、保護機器の守る範囲の違い。
3. 電流・電力・電力量の計算と、電源容量の検討項目。
4. 入力・出力・指令・確認の違い。
5. 代表的なセンサーの原理と選定手順。
6. NPN/PNPの電流経路と、PLC入力共通端子との整合。
7. ラダーの基本、自己保持、再起動防止、インターロック。
8. 通常の制御と安全機能の境界。

## 2. 必要な教材 / required materials

- ノートブック01〜03（投影用と受講者PC用）。
- 図 D08-01〜D08-14（投影）。
- ワークシートと解答例。
- オフラインシミュレータ `sim_plc_sequence.html`（ブラウザで開くだけ。外部通信なし）。
- 可能なら実物：遮断器、サーマルリレー、スイッチング電源、リレー、センサー各種（**通電しない**）。
- 実物がない場合は図とカタログのコピーで代替。

## 3. 午前の説明（08:00–09:00）/ morning explanation

| 時間 / min | 内容 / Content | 使う図 / Figure |
|---:|---|---|
| 5 | 今日のゴール、身近な盤の写真の話 / today's goal | — |
| 10 | 電圧・電流・抵抗・電力、水のたとえと限界 / basic quantities | D08-01 |
| 15 | 電圧の使い分けと電力の流れ / voltage applications | D08-02 |
| 15 | 盤の機器を1つずつ / panel components | D08-03, D08-04, D08-05 |
| 10 | 電流・電力・電力量の計算 / calculations | — |
| 5 | 安全機能との区別 / safety boundary | — |

**板書の約束 / board rules:** 単位（V, A, W, kWh）を書く。保護機器は「守る範囲」と「守らない範囲」を対で書く。

## 4. 午後のフォロー（12:50–13:50）/ afternoon follow-up

| 時間 / min | 内容 / Content |
|---:|---|
| 10 | 午前の質問 / morning questions |
| 15 | シミュレータで自己保持を演示（START保持、STOP、復電）/ demonstrate seal-in in the simulator |
| 15 | 基本回路と拡張ロジックの違いを並べて説明 / basic versus extended logic |
| 10 | 同時要求を「両方OFF」にする理由 / why simultaneous requests are rejected |
| 10 | センサーの実物観察（出力形式の表示を探す）/ find the output type on a real sensor |

## 5. よくある誤解と正しい説明 / common misunderstandings

| 誤解 / Misunderstanding | 正しい説明 / Correct explanation |
|---|---|
| DC24Vなら安全 / DC24V is safe | 短絡・発熱・火災・予期しない動作の危険がある / hazards remain |
| ブレーカーですべて守れる / the breaker protects everything | 定格と特性の範囲内だけ / only within its ratings |
| サーマルリレーは短絡保護 / overload relay is short-circuit protection | 過負荷保護。短絡は別 / overload only |
| PLC全体がNPN / the PLC is NPN | 入力モジュールと配線で決まる / module and wiring decide |
| 配線色でNPN/PNPが決まる / wire colour decides NPN/PNP | データシートで確認 / check the datasheet |
| 物理NCはNC論理接点で使う / an NC switch needs an NC instruction | 状態の意味で決める / decide from the meaning |
| 自己保持があれば再起動も防げる / seal-in prevents restart | アーム・立ち上がり・STOP優先・リセット分離が必要 / extra logic is required |
| 相互インターロックで十分 / cross-linked interlocks suffice | スキャン順に依存。同時要求は拒否する設計に / make it deterministic |
| シミュレーションで安全が証明できる / a simulation proves safety | 教育用モデル。安全は別の設計 / a teaching model |

## 6. 理解確認の質問と期待する答え / comprehension questions

| # | 質問 / Question | 期待する答え / Expected answer |
|---|---|---|
| 1 | DC24V、0.15 A の電力 / power at 24 V, 0.15 A | 3.6 W |
| 2 | 合計0.80 A、余裕25%の計画電流 / planning current | 1.00 A |
| 3 | PNPと共通0Vの入力は適合するか / PNP with a 0V common | 適合する / compatible |
| 4 | 入力共通0VにNPNを繋ぐと / NPN with a 0V common | 適合しない / not compatible |
| 5 | 基本の自己保持で許可が戻ると / permission restored in basic seal-in | STARTを押しっぱなしならRUNが戻る / RUN returns while START is held |
| 6 | 同時要求の扱い / simultaneous requests | 両方OFF（拒否） / both OFF |

## 7. ワークシートとの対応 / worksheet mapping

- **T1**（センサーとPLC入力）は 08-02 §7–§8 に対応。 / T1 maps to 08-02 sections 7-8.
- **T2**（電力の計算）は 08-01 §7 に対応。 / T2 maps to 08-01 section 7.
- **T3**（ラダーの読取り）は 08-03 §7–§9 に対応。 / T3 maps to 08-03 sections 7-9.
- 追加課題は出しません。 / Do not add extra assignments.

## 8. 安全上の制約 / safety restrictions

- 実機の盤への配線・通電・絶縁測定・保護機器の選定を行わない。 / No real wiring, energisation, insulation testing or device selection.
- AC100/200V の露出部に近づかない。 / Keep clear of exposed AC100/200V parts.
- 学習コードが実機の出力を動かさないことを明言する。 / State that the training code never drives real outputs.
- 非常停止・ガード・安全扉は、独立した安全関連システムで設計する。通常のPLC制御で代用しない。 / Safety functions belong to an independent safety-related system.

## 9. 時間配分 / timing

08:00–09:00 講師説明、09:00–10:20 ノートブック01、10:20–10:35 休憩、10:35–12:00 ノートブック02、12:00–12:50 昼食、12:50–13:50 講師フォロー、13:50–15:10 ノートブック03前半、15:10–15:25 休憩、15:25–16:20 ノートブック03後半、16:20–16:50 ワークシートと提出。合計530分。
