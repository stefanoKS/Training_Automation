# 第7日 講師ガイド / Day 7 Instructor Guide

教材 / material: `notebooks/Day07_Automation_Concept_Mechanics/`（01–03）、`assets/diagrams/day07/`、`day07_09_support/examples/automation_models.py`、`docs/pdf/Day07_explanation_ja_en.pdf`、`day07_09_support/worksheets/Day07_Student_Worksheet_ja_en.md`。

> このガイドは講師用です。受講者に配布する必要はありません。
> This guide is for the instructor and need not be distributed.

## 1. 学習目標 / learning objectives

受講者は次のことを説明できるようになります。 / Trainees should be able to explain:

1. 自動化設備の構成（入力・取扱い・加工/検査・出力、6要素）。
2. タクトタイムとサイクルタイムの違い、生産能力の計算。
3. 改善の効果金額と簡易回収期間の計算。
4. 空圧・油圧・電気の動力の違いと制約。
5. シリンダ・モーター・その他のアクチュエータの使い道。
6. 選定に必要な仕様と、計算値が選定ではない理由。

## 2. 必要な教材 / required materials

- ノートブック01〜03（投影用と受講者PC用）。
- 電卓（関数電卓またはスマートフォン）。
- 図 D07-01〜D07-14（投影）。
- ワークシートと解答例。
- 可能なら実物：空圧シリンダ、電磁弁、ギヤードモーター、電動リニアアクチュエータ（**通電・加圧しない**、見て触るだけ）。
- 実物がない場合は図とカタログのコピーで代替。 / Use diagrams and catalogue extracts if no hardware is available.

## 3. 午前の説明（08:00–09:00）/ morning explanation

| 時間 / min | 内容 / Content | 使う図 / Figure |
|---:|---|---|
| 5 | 3日間の位置づけ、今日のゴール / where Day 7 fits, today's goal | — |
| 10 | 自動化とは何か、何を自動化するか / what automation is | D07-01 |
| 15 | タクトとサイクル、能力の計算（単位を板書）/ takt, cycle, capacity | D07-03, D07-02 |
| 10 | ボトルネック / bottleneck | D07-04 |
| 10 | 効果金額と回収期間 / effect and payback | D07-05 |
| 10 | 3つの動力の違い / the three power sources | D07-06 |

**板書の約束 / board rules:** 単位を必ず書く。タクトは「秒/個」、サイクルは「秒/サイクル」、能力は「個/時」。

## 4. 午後のフォロー（12:50–13:50）/ afternoon follow-up

| 時間 / min | 内容 / Content |
|---:|---|
| 10 | 午前の質問に答える / answer morning questions |
| 20 | シリンダの実物観察（形状・ロッド・ポート・センサー溝）/ examine a cylinder |
| 15 | 押し側・引き側の力の計算を実演 / demonstrate extension vs retraction force |
| 15 | 「速いアクチュエータを入れても生産は増えない」を図で説明 / bottleneck with a faster actuator |

**演示の注意 / demonstration caution.** 実物は通電・加圧しません。ばね戻りシリンダは手で動かさない（挟まれ）。 / Do not energise or pressurise anything. Do not hand-move a spring-return cylinder.

## 5. よくある誤解と正しい説明 / common misunderstandings

| 誤解 / Misunderstanding | 正しい説明 / Correct explanation |
|---|---|
| タクトとサイクルは同じ / takt equals cycle | タクトは必要ペース、サイクルは機械の時間 / required pace versus machine time |
| 3600 ÷ 15 はいつでも240個/時 / always 240 pieces/hour | 1サイクルあたりの個数を確認 / check pieces per cycle |
| 稼働率を掛ければ実力 / multiply by availability for "real" capacity | この研修では扱わない。停止・不良は別に考える / not part of this course |
| 削減時間×時給が利益 / saved time × rate is profit | 労務費換算額。現金化には条件 / a monetary equivalent, not cash |
| 油圧はいつも強い・速い・効率がよい / hydraulics always best | システム設計で決まる / the system design decides |
| 空圧で中間位置に精度よく止まる / pneumatics position precisely | 通常の空圧回路では苦手 / difficult with ordinary arrangements |
| 真空はどんな面でも吸着できる / vacuum holds anything | ざらつき・通気性・反り・油分で変わる / roughness, porosity, warping, oil |
| 理論内径の次サイズで決まり / next bore size is the answer | 負荷率・偏重・速度・安全を確認 / check load ratio, offset load, speed, safety |

## 6. 理解確認の質問と期待する答え / comprehension questions

| # | 質問 / Question | 期待する答え / Expected answer |
|---|---|---|
| 1 | タクト42秒、サイクル15秒。速度は足りるか / is 15 s enough for a 42 s takt? | 足りる。ただし停止と不良は別 / yes, but stops and defects are separate |
| 2 | 1サイクル2個なら能力は / capacity with two pieces per cycle | 480個/時 / 480 pieces/hour |
| 3 | 8 kgの物体の重力は / weight of 8 kg | 約78.5 N |
| 4 | 引き側が弱い理由 / why retraction is weaker | ロッドの断面積の分、受圧面積が小さい / the rod reduces the area |
| 5 | 11.18 mmで選定してよいか / may we select 11.18 mm? | だめ。仮定と余裕、実機条件を確認 / no; check assumptions, margins and conditions |

## 7. ワークシートとの対応 / worksheet mapping

- **T1**（生産能力と効果金額）は 07-01 §5–§6 に対応。 / T1 maps to 07-01 sections 5-6.
- **T2**（アクチュエータ選定）は 07-02 §4–§9 と 07-03 §7 に対応。 / T2 maps to 07-02 sections 4-9 and 07-03 section 7.
- 追加課題は出しません。 / Do not add extra assignments.
- 解答例の数値は `automation_models.py` で再現できます。 / The answer-key numbers can be reproduced with the module.

## 8. 安全上の制約 / safety restrictions

- 実機の配線・通電・加圧・動作確認を行わない。 / No real wiring, energisation, pressurisation or motion checks.
- 回転ローラー、カレンダーロール、挟まれ箇所に近づかない。 / Keep clear of rollers, calender rolls and trapping points.
- 残留圧力・残留油圧・重力による落下を前提にする。 / Assume residual pressure, residual oil pressure and gravity.
- 実機の演示が必要な場合は、事前承認・リスクアセスメント・有資格者の監督を条件とする。 / Any real demonstration requires prior approval, a risk assessment and qualified supervision.

## 9. 時間配分 / timing

08:00–09:00 講師説明、09:00–10:20 ノートブック01、10:20–10:35 休憩、10:35–12:00 ノートブック02、12:00–12:50 昼食、12:50–13:50 講師フォロー、13:50–15:10 ノートブック03前半、15:10–15:25 休憩、15:25–16:20 ノートブック03後半、16:20–16:50 ワークシートと提出。合計530分。

These durations are planned, not empirically verified with a beginner pilot. / この時間配分は計画値であり、初心者パイロットで実測したものではありません。
