# 第9日 講師ガイド / Day 9 Instructor Guide

教材 / material: `notebooks/Day09_AI_Camera_Imaging/`（01–03）、`assets/diagrams/day09/`、`day07_09_support/examples/automation_models.py`、`docs/pdf/Day09_explanation_ja_en.pdf`、`day07_09_support/worksheets/Day09_Student_Worksheet_ja_en.md`。

> このガイドは講師用です。受講者に配布する必要はありません。
> This guide is for the instructor and need not be distributed.

## 1. 学習目標 / learning objectives

受講者は次のことを説明できるようになります。 / Trainees should be able to explain:

1. 産業用カメラ・スマートカメラ・PCベース自作の違い。
2. 撮像の流れと、解像度・視野・1ピクセルの実寸。
3. レンズ選定の要素（視野・作動距離・センササイズ・絞り・被写界深度）。
4. グローバルとローリングシャッターの違い、露光と動体ぶれ。
5. エリアセンサとラインセンサの違い。
6. 照明の種類と使い分け、反射・グレア・環境の影響。
7. AI検査システムの構成と、PC・PLC・機械の関係。
8. OK・NG・無効（INVALID）の扱い。

## 2. 必要な教材 / required materials

- ノートブック01〜03（投影用と受講者PC用）。
- 図 D09-01〜D09-11（投影）。
- ワークシートと解答例。
- 可能なら実物：産業用カメラ、レンズ、リング照明、バックライト、吸着パッド（**カメラを開かない、設備に取り付けない**）。
- サンプル画像（リポジトリ内の既存サンプルで可）。外部取得は行わない。

## 3. 午前の説明（08:00–09:00）/ morning explanation

| 時間 / min | 内容 / Content | 使う図 / Figure |
|---:|---|---|
| 5 | 9日間のまとめと今日の位置づけ / where Day 9 fits | — |
| 10 | カメラの種類と撮像の流れ / camera types and imaging chain | D09-01 |
| 15 | 解像度・視野・1ピクセルの実寸・欠陥のピクセル数 / sampling and defect pixels | D09-02 |
| 10 | レンズと作動距離、被写界深度 / lens, WD, depth of field | D09-03 |
| 10 | シャッターとぶれ / shutter and blur | D09-04, D09-05 |
| 10 | 照明の種類と環境 / lighting and environment | D09-06, D09-07 |

## 4. 午後のフォロー（12:50–13:50）/ afternoon follow-up

| 時間 / min | 内容 / Content |
|---:|---|
| 10 | 午前の質問 / morning questions |
| 20 | レンズと照明の実物観察（マウント、絞り、照射角）/ examine lens and lighting |
| 10 | 合成比較図で露出・コントラスト・グレアを説明 / explain exposure, contrast and glare |
| 10 | ノートブックのオフライン演示（数値と判定）/ offline demonstrations |
| 10 | 撮像条件の記録項目を一緒に埋める / fill the imaging-condition record together |

**実機を使う場合の注意 / caution with real hardware.** カメラ・照明を生産設備に取り付けない。ローラー・カレンダーロールに近づかない。ネットワーク設定を変更しない。 / Do not mount cameras or lights on production equipment, do not approach rollers or calender rolls, and do not change network settings.

## 5. よくある誤解と正しい説明 / common misunderstandings

| 誤解 / Misunderstanding | 正しい説明 / Correct explanation |
|---|---|
| 解像度が高ければ検出できる / higher resolution always detects | 光学・照明・ぶれ・検証で決まる / optics, lighting, blur and validation decide |
| 4ピクセルなら必ず見える / four pixels guarantees detection | 保証ではない / not a guarantee |
| カメラFPS＝検査能力 / camera FPS is inspection capacity | 転送・推論・判定・応答を含める / include transfer, inference, decision, response |
| グローバルならぶれない / a global shutter has no blur | ぶれは露光時間で決まる / blur depends on exposure |
| レンズは焦点距離だけで決まる / focal length decides the lens | 視野・WD・センササイズ・絞り / FOV, WD, sensor size, aperture |
| 明るければよい / brighter is always better | 飽和で情報が失われる / saturation destroys information |
| 1種類の照明で全欠陥が見える / one light shows every defect | 材質と欠陥形状で変わる / depends on material and geometry |
| 結果がないのでOKにする / no result means OK | 無効として扱う / treat as INVALID |
| 合成画像で性能を証明できる / synthetic images prove performance | 実対象の検証が必要 / validate on real samples |

## 6. 理解確認の質問と期待する答え / comprehension questions

| # | 質問 / Question | 期待する答え / Expected answer |
|---|---|---|
| 1 | 視野240 mm、1,920 px の1ピクセル / sampling | 0.125 mm/px |
| 2 | 0.5 mm の欠陥 / 0.5 mm defect | 4 px |
| 3 | 1,000 mm/s、1 ms の移動量 / movement | 1 mm（8 px） |
| 4 | 30 FPS、1,000 mm/s のフレーム間移動 / frame interval | 約33.33 mm |
| 5 | 8,000 lines/s の条件 / line-rate condition | 0.125 mm/line、1,000 mm/s |
| 6 | 通信断のときの扱い / link failure | 無効。OKにしない / INVALID, never OK |
| 7 | 内部異物の照明候補 / internal contamination | バックライト / backlight |

## 7. ワークシートとの対応 / worksheet mapping

- **T1**（カメラと照明の選定チェックリスト）は 09-01 §5–§10 と 09-02 §5–§9 に対応。 / T1 maps to 09-01 sections 5-10 and 09-02 sections 5-9.
- **T2**（撮像条件のレビュー）は 09-02 §8–§9 に対応。 / T2 maps to 09-02 sections 8-9.
- 提案書・発表・ネットワーク設計は課題にしない。 / No proposal, presentation or network design.
- PDFは19ページ以内。付録は短縮版の用語集を使う。 / The PDF is capped at 19 pages and uses the compact glossary.

## 8. 安全上の制約 / safety restrictions

- 生産設備へのカメラ・照明の取付を行わない。 / Do not install cameras or lighting on production equipment.
- 回転ローラー、カレンダーロール、挟まれ箇所に近づかない。 / Keep clear of rollers, calender rolls and trapping points.
- 工場ネットワークの設定を変更しない。 / Do not change factory network settings.
- AIソフトが危険なアクチュエータを直接動かさない構成にする。 / AI must not directly operate hazardous actuators.
- 撮像の観察は、停止・隔離・有資格者の監督のもとで行う。 / Observation of imaging equipment requires stopping, isolation and qualified supervision.

## 9. 時間配分 / timing

08:00–09:00 講師説明、09:00–10:20 ノートブック01、10:20–10:35 休憩、10:35–12:00 ノートブック02、12:00–12:50 昼食、12:50–13:50 講師フォロー、13:50–15:10 ノートブック03前半、15:10–15:25 休憩、15:25–16:20 ノートブック03後半、16:20–16:50 ワークシートと提出。合計530分。
