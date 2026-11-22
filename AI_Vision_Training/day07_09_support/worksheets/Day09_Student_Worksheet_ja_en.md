# 第9日 ワークシート：AI検査装置の基本設計書 / Day 9 Worksheet: Conceptual Design Sheet

氏名 / Name: ____________________　日付 / Date: ____________　班 / Group: ______

**記入のきまり / How to fill this in**

- この設計書は**概念設計**です。実機の仕様・型番・安全カテゴリを断定しません。 / This is a **conceptual design**; do not assert real specifications, model numbers or safety categories.
- 数値は仮定と明記し、単位を書きます。 / State assumptions and always write units.
- **有効なAI結果がないまま「良品」にしない**方針を必ず書きます。 / Always state the policy that **no valid AI result means no OK**.

## 1. 機械レイアウト / Mechanical layout

検査点・カメラ・照明・搬送・下流の位置を、文章と簡単な図で書いてください。 / Describe inspection point, camera, lighting, transport and downstream position with a sketch.

______________________________________________________________________________

## 2. センサ / Sensors

| センサ / sensor | 目的 / purpose | 信号 / signal（digital/analog/pulse） | 故障時の扱い / behaviour on failure |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

## 3. アクチュエータ / Actuators

| アクチュエータ / actuator | 目的 / purpose | 指令 / command | 動力 / energy | 安全上の注意 / safety note |
|---|---|---|---|---|
| | | | | |
| | | | | |

## 4. PLC / PLC

- 入力の例 / example inputs: ______________________________________
- 出力の例 / example outputs: ____________________________________
- スキャン周期に関係する制約 / constraints related to scan time: ______________________________

## 5. カメラと照明 / Camera and lighting

| 項目 / item | 仮定値 / hypothetical value | 根拠・確認事項 / basis or check |
|---|---|---|
| 方式 / type（area or line） | | |
| 視野 FOV / field of view | | |
| 横画素数 / horizontal pixels | | |
| 画素スケール / pixel scale | | |
| 照明方式 / lighting type | | |
| 露光時間 / exposure | | |

**画素スケールの計算 / pixel-scale calculation:** ________ ÷ ________ = ________ mm/px

## 6. 産業用PC / Industrial PC

CPU・GPU・RAM・ストレージ・カメラインタフェース・ネットワークのうち、**検査に影響する3つ**を選び、理由を書いてください。 / Choose three components that affect inspection and explain why.

1. ____________________
2. ____________________
3. ____________________

## 7. AIモデル / AI model

| 観点 / aspect | 内容 / content |
|---|---|
| 使うモデル / model(s) | |
| 学習データ / training data | |
| 出力 / output | |
| 閾値の決め方 / threshold method | |
| 既知の限界 / known limitation | |

## 8. データの流れ / Data flow

取得 → 転送 → 前処理 → 推論 → 後処理 → 結果 → 記録 の各段階で、何が起きるかを書いてください。 / Describe each stage.

| 段階 / stage | 内容 / what happens | 遅延の目安 / latency note |
|---|---|---|
| 取得 / acquire | | |
| 転送 / transfer | | |
| 前処理 / preprocess | | |
| 推論 / inference | | |
| 後処理 / postprocess | | |
| 結果 / result | | |
| 記録 / record | | |

## 9. 制御の流れ / Control flow

起動から停止までの状態を5つ書き、遷移条件を添えてください。 / Write five states with transition conditions.

1. ________ → 条件 / condition: ________
2. ________ → 条件 / condition: ________
3. ________ → 条件 / condition: ________
4. ________ → 条件 / condition: ________
5. ________ → 条件 / condition: ________

## 10. 結果の有効性 / Result validity

結果IDと有効性をどう扱うかを書いてください。 / Describe result ID and validity handling.

- 結果ID / result ID: ______________________________________
- 有効フラグ / validity flag: ________________________________
- 古い結果の拒否 / stale-result rejection: ______________________
- タイムアウト時の扱い / timeout handling: ______________________

## 11. タイミング / Timing

仮定値を入れて計算してください。 / Insert hypothetical values and calculate.

| 項目 / item | 値 / value | 計算 / calculation |
|---|---|---|
| 材料速度 / material speed | ______ m/s | |
| 結果遅延 / result latency | ______ s | |
| 遅延中の移動 / travel during latency | | ______ m = ______ mm |
| ライン周波数 / line rate | | ______ lines/s |

## 12. エラー処理 / Error handling

| 故障 / failure | 検出 / detection | 品質対応 / quality response | 人が確認すること / human review |
|---|---|---|---|
| カメラ断 / camera lost | | | |
| 結果無効 / invalid result | | | |
| 通信断 / comms lost | | | |
| 古いID / stale ID | | | |

## 13. HMI

表示すべき画面を4つ選び、それぞれに必要な情報を書いてください。 / Choose four screens and list the information each needs.

1. ____________________
2. ____________________
3. ____________________
4. ____________________

## 14. 安全境界 / Safety boundaries

| 項目 / item | 通常の制御で扱うか / ordinary control | 独立した安全系か / independent safety system |
|---|---|---|
| ガード開放 / guard open | | |
| 非常停止 / emergency stop | | |
| AIのNG判定 / AI NG result | | |
| 予期しない起動 / unexpected start | | |

**なぜAIと安全を分けるのか、一文で書いてください。 / Why separate AI and safety? One sentence.**
______________________________________________________________________

## 15. 受入試験 / Acceptance tests

確認項目を5つ書き、合否の見方を添えてください。 / Write five checks with pass criteria.

| # | 確認項目 / check | 合否の見方 / pass criteria |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

**安全に関する注意 / Safety note:** 本設計書は概念検討用です。実機の設計・製作・運転は、有資格技術者のレビューと法規・規格・現地手順に従います。
**Safety note:** This is conceptual work. Real design, build and operation require qualified review and compliance with regulations, standards and site procedures.
