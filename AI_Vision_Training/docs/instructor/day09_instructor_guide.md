# 第9日 講師ガイド / Day 9 Instructor Guide
**カメラ・PLC・PC・AIの統合による自動検査システム / Integrated Machine Vision, PLC, PC and AI**

対象 / audience: 第7日・第8日を終えた初学者 / beginners who completed Days 7 and 8
教材 / material: `notebooks/Day09_System_Integration/`、`assets/diagrams/day09/`、`day07_09_support/simulations/`
実機のカメラ・PLC・ネットワークがなくても授業できます。
The day is teachable without real cameras, PLCs or networks.

## 1. 学習目標 / Learning objectives

1. エリアスキャンとラインスキャンの違いを説明する。 / Explain area scan versus line scan.
2. FOVと画素数から画素スケールを計算する。 / Calculate pixel scale from FOV and pixels.
3. 速度とサンプル間隔からライン周波数を計算する。 / Calculate line rate from speed and sampling interval.
4. 露光時間とモーションブラーの関係を説明する。 / Explain exposure and motion blur.
5. YOLOとPatchCoreの出力の違いを説明する。 / Distinguish YOLO and PatchCore outputs.
6. 判定の6状態を区別し、無効をOKにしない。 / Distinguish six decision states and never OK an invalid result.
7. PCとPLCの結果受け渡しで、IDと有効性の必要性を説明する。 / Explain result ID and validity in the PC–PLC handshake.
8. 遅延中の移動と位置追跡の違いを説明する。 / Separate travel during latency from position tracking.
9. 故障対応と安全境界を、設計として整理する。 / Organise fault handling and safety boundaries as a design.

## 2. 前提知識 / Prerequisites

- 第7日の機械・センサ、第8日のPLC・ラダー・シーケンス。 / Day 7 mechanics/sensors and Day 8 PLC/ladder/sequence.
- 第3〜5日のYOLOとPatchCoreの基本用語。 / Day 3–5 YOLO and PatchCore terminology.
- 割り算と単位換算（m/min→mm/s）。 / Division and unit conversion.

不要：光学設計、ネットワーク実装、AIモデルの再学習。 / No optics design, network implementation or model retraining.

## 3. 時間割 / Exact timetable

| 時刻 / time | 分 / min | 内容 / content | 区分 / type |
|---|---:|---|---|
| 08:00–09:00 | 60 | 講師：全体の信号とデータ / signals and data across the system | 講師 / instructor |
| 09:00–10:20 | 80 | 09-01 視覚ハードウェア / vision hardware | 必須 / required |
| 10:20–10:35 | 15 | 休憩 / break | 休憩 / break |
| 10:35–12:00 | 85 | 09-02 PCとAI処理 / PC and AI processing | 必須 / required |
| 12:00–12:50 | 50 | 昼食 / lunch | 昼食 / lunch |
| 12:50–13:50 | 60 | 講師：ハンドシェイクと故障対応 / handshake and faults | 講師 / instructor |
| 13:50–15:10 | 80 | 09-03 統合（前半） / integration, part 1 | 必須 / required |
| 15:10–15:25 | 15 | 休憩 / break | 休憩 / break |
| 15:25–16:20 | 55 | 09-03（後半） / part 2 | 必須 / required |
| 16:20–16:50 | 30 | 基本設計書 / conceptual design sheet | 提出 / submission |

**合計 / total 530分（講師120・必須300・休憩30・昼食50・提出30）。**

## 4. 午前の講師説明 / Morning presentation（08:00–09:00）

1. D09-01 を映し、6層（機械・センサ・制御・画像・AI・記録と人）を学生に指させる（10分）。 / Have students point to the six layers.
2. 「画像データと制御コマンドは同じ種類か」を問う（5分）。 / Ask whether image data and commands are the same kind of information.
3. D09-09 を使い、結果IDと有効性がないと何が起きるかを説明（15分）。 / Use D09-09 to show why ID and validity matter.
4. 画素スケールとライン周波数の式を、単位付きで一度だけ実演（15分）。 / Demonstrate pixel scale and line rate with units.
5. 「タイムアウトは良品ではない」を強調（5分）。 / Emphasise that a timeout is not OK.
6. 質問対応（10分）。 / Questions.

**板書例 / board:** 左に6層、中央に「mm/px = FOV ÷ pixels」「lines/s = mm/s ÷ mm/line」、右に判定の6状態。

## 5. 午後の講師実演 / Afternoon demonstration（12:50–13:50）

- **実演A（15分）**：`sim_camera_timing.html` で速度・画素数・間隔・露光を変え、値の関係を示す。 / Vary inputs and show relationships.
- **実演B（15分）**：`sim_ai_result_protocol.html` で無効・タイムアウト・重複・古いIDを送り、判定を確認。 / Send invalid, timeout, duplicate and stale results.
- **実演C（15分）**：D09-10 で遅延中の移動と位置追跡を区別。 / Separate travel during latency from tracking.
- **実演D（15分）**：D09-12 で故障の4分岐と受入確認を確認。 / Walk through the four branches and acceptance checks.

## 6. 必要な図 / Required diagrams

D09-01 全体構成、D09-02 エリア／ライン、D09-03 光学と画素、D09-04 照明、D09-05 ぶれ、D09-06 同期、D09-07 処理パイプライン、D09-08 YOLOとPatchCore、D09-09 ハンドシェイク、D09-10 位置追跡、D09-11 遅延とバッファ、D09-12 故障と受入。加えて D08-11（HMI画面の例）。

## 7. 必要なシミュレーション / Required simulations

- `sim_camera_timing.html`（09-01）
- `sim_ai_result_protocol.html`（09-03）

JavaScriptが無効な場合は `fallback/sim_camera_timing.png`、`fallback/sim_ai_result_protocol.png` と `<noscript>` 説明を使用。

## 8. 学生に問いかける質問 / Questions to ask

1. ライン周波数とフレームレートは同じですか。 / Are line rate and frame rate the same?
2. 画素数を2倍にすると、画素スケールはどうなりますか。 / What happens to pixel scale when pixel count doubles?
3. 露光を半分にすると、何を調整する必要がありますか。 / If exposure halves, what must be adjusted?
4. YOLOの信頼度は、合格確率ですか。 / Is a YOLO confidence an acceptance probability?
5. PatchCoreは欠陥の種類を教えますか。 / Does PatchCore report a defect type?
6. 通信が成功したら、結果は正しいですか。 / Does successful communication prove correctness?
7. タイムアウトした結果は、良品ですか。 / Is a timed-out result OK?
8. 遅延中の移動60 mmは、そのまま60 mmの位置ずれですか。 / Is 60 mm of travel the same as 60 mm of positioning error?

## 9. よくある誤解 / Common misunderstandings

| 誤解 / misunderstanding | 実際 / reality |
|---|---|
| 画素数が多いほど必ず良い / more pixels always better | 光学・照明・コントラスト次第 / optics, lighting and contrast matter |
| 1画素の欠陥は必ず検出 / sub-pixel defects always found | 保証されない / not guaranteed |
| ラインスキャンが常に優れる / line scan always wins | 照明と同期が難しい / lighting and sync are harder |
| 推論時間＝応答時間 / inference time equals response | 取得・転送・待ち・通信が加わる / other stages add time |
| 平均値で十分 / averages are enough | 最大値とジッタ / worst case and jitter |
| 通信成功＝結果が正しい / comms success equals correctness | 別の情報 / different facts |
| スコア＝校正済み確率 / score equals calibrated probability | そうではない / it is not |
| 無効・タイムアウトもOK / invalid or timeout is OK | 絶対にOKにしない / never OK |
| AIが安全を担保 / AI provides safety | 独立した安全系が必要 / independent safety system |

## 10. 正しい説明の例 / Correct explanations

- **画素スケール**：FOV ÷ 横画素数。1画素未満の検出は保証しない。 / FOV ÷ pixels; sub-pixel detection is not guaranteed.
- **ライン周波数**：速度（mm/s） ÷ サンプル間隔（mm/line）。fpsとは別。 / speed ÷ sampling; distinct from fps.
- **ぶれ**：速度 × 露光時間。露光を短くすると光量かゲインが必要。 / velocity × exposure; shorter exposure needs light or gain.
- **YOLO/PatchCore**：既知クラス検出と正常差分。どちらも校正済み確率ではない。 / Known-class detection and normal-difference; neither is a calibrated probability.
- **結果の有効性**：ID＋有効フラグ。古いID・重複・タイムアウトは拒否または保留。 / ID plus validity; stale, duplicate and timeout are rejected or held.
- **安全**：AIと独立。危険源とリスクアセスメントから設計。 / Independent of AI; designed from hazards and risk assessment.

## 11. 期待される演習解答 / Expected exercise responses

- 600 ÷ 4096 ≈ 0.146484 mm/px。
- 30 m/min = 500 mm/s、0.2 mm/line → 2,500 lines/s。
- 4096 × 2500 × 1 = 10.24 MB/s（≈ 81.92 Mb/s）。
- 0.5 m/s × 0.12 s = 60 mm（位置ずれ誤差とは別）。
- 自動OKは「有効なOK」のみ。
- 詳細は `worksheets/Day09_Answer_Key_ja_en.md`。

## 12. トラブル対応 / Troubleshooting

| 症状 / symptom | 対応 / action |
|---|---|
| 画素計算が合わない / pixel maths mismatch | FOVと画素数の単位、桁を確認 / check units and magnitudes |
| ライン周波数が極端 / line rate extreme | m/min→mm/s の換算を確認 / check the m/min to mm/s conversion |
| シミュレータが無反応 / simulator dead | ローカルファイルとして開く、JS有効化、`fallback/` を使用 / open locally, enable JS, use fallback |
| MBとMbを混同 / MB versus Mb | 1 byte = 8 bits を板書 / write the conversion |
| 「無効でもOK」と答える / invalid treated as OK | D09-12 の必須原則を再提示 / restate the mandatory rule |
| 時間が足りない / short of time | 09-03 の演習1・3・5を必須、2・4を宿題 / keep 1, 3, 5 in class |

## 13. 安全上の制約 / Safety restrictions

- 実機カメラ・照明・PLC・ネットワークへの接続を**行わせない**。 / No connection to real cameras, lighting, PLCs or networks.
- 高輝度光源の直接視を避ける。 / Avoid direct viewing of high-intensity light.
- 安全機能をAIで代替する説明をしない。 / Never suggest AI replaces safety functions.
- 実機の設計・設置・運転は、有資格技術者と法規・規格・現地手順に従う。 / Real design and operation require qualified engineers and applicable rules.

## 14. オフライン代替 / Offline fallback

- D09-01〜D09-12 と D08-11 を印刷。 / Print the diagrams.
- `fallback/` のPNGを印刷し、計算は手計算。 / Print fallback images and calculate by hand.
- ハンドシェイクはカード（PLC／PC）を使って机上演習。 / Act out the handshake with PLC/PC cards.
- ネットワーク・実機不要。 / No network or real equipment.

## 15. 評価の指針 / Assessment guidance

- 基本設計書を `Day09_Answer_Key_ja_en.md` と `Day07_09_Assessment_Rubric_ja_en.md` で評価。 / Mark the design sheet with the answer key and rubric.
- 重視するのは、層の分離、単位付き計算、結果の有効性、故障対応、安全の独立。 / Value layer separation, unit-bearing calculations, result validity, fault handling and safety independence.
- 重大な誤り：無効・タイムアウト・古いIDをOKにする、AIを安全機能とする、実機仕様を断定する。 / Critical: invalid/timeout/stale as OK, AI as safety, asserting real specifications.
- 口頭確認（例：タイムアウトをOKにできない理由）で理解を確認。 / Oral checks to confirm understanding.
