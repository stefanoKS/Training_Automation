# 第9日 解答例と採点の観点 / Day 9 Answer Key (instructor copy)

**学生には配布しません。 / Do not distribute to students.**

## 1. 機械レイアウト / Mechanical layout

Accept a sketch that shows sheet travel, inspection point, camera and lighting, and the downstream position. Deduct if the sheet direction is missing.

## 2. センサ / Sensors

Accept any three with a purpose, signal type and failure behaviour. Typical: presence (digital; hold on failure), encoder (pulse; fault on loss), edge (digital or analog; hold and notify).

## 3. アクチュエータ / Actuators

Accept transport and marking examples. Full marks require command and energy separated, plus a safety note (guards, stored energy, unexpected start).

## 4. PLC

Accept example inputs/outputs. The scan constraint should mention that a fast event shorter than the scan can be missed.

## 5. カメラと照明 / Camera and lighting

- 画素スケール = FOV ÷ 横画素数。例：600 ÷ 4096 ≈ 0.146484 mm/px。
- 1画素未満の欠陥の検出を保証しないと書けているか確認。 / Check that the answer says sub-pixel detection is not guaranteed.
- Lighting choice with a reason (diffuse, direct, backlight, dark field) and a verification note.

## 6. 産業用PC

Accept any three justified components, for example camera interface (data rate), RAM (buffering), storage (image retention), network (PLC handshake), GPU (throughput).

## 7. AIモデル / AI model

- YOLO: labelled data, class/location/confidence, detection threshold.
- PatchCore: normal images, anomaly score/map, anomaly threshold.
- Full marks require the statement that scores are not calibrated probabilities.

## 8. データの流れ / Data flow

Each stage described. Typical latency notes: acquisition (exposure), transfer (bandwidth), preprocessing (resize), inference (model), postprocessing (threshold), result (handshake), record (storage I/O).

## 9. 制御の流れ / Control flow

Five states with conditions. Deduct where a transition lacks a condition or where a fault returns directly to Running.

## 10. 結果の有効性 / Result validity

Must include: unique result ID; validity flag; stale IDs rejected; timeout never OK. Automatic OK only for valid OK.

## 11. タイミング / Timing

Example: 0.5 m/s × 0.12 s = 0.06 m = 60 mm. Accept any consistent values with units. Line rate example: 500 mm/s ÷ 0.2 mm/line = 2,500 lines/s.

## 12. エラー処理 / Error handling

Accept four rows where the quality response is HOLD or review for camera loss, invalid result, comms loss and stale ID. "OK" for any of these is a critical error.

## 13. HMI

Accept four screens with useful information, e.g. overview, camera status, AI status, defect history, alarms, configuration summary.

## 14. 安全境界 / Safety boundaries

| 項目 / item | 通常制御 / ordinary | 安全系 / safety |
|---|---|---|
| ガード開放 / guard open | — | 独立 / independent |
| 非常停止 / emergency stop | — | 独立 / independent |
| AIのNG判定 / AI NG | 品質対応 / quality response | — |
| 予期しない起動 / unexpected start | — | 独立 / independent |

The explanation must state that AI is probabilistic and can fail, so safety needs a validated independent system.

## 15. 受入試験 / Acceptance tests

Accept five checks such as: known good/bad judged correctly; invalid never OK; stale/duplicate rejected; no reuse after restart; fault injection detected; worst-case latency and jitter measured; safety independent of AI.

## 採点表 / Marking scheme（合計30点 / total 30）

| 項目 / item | 点 / points |
|---|---:|
| 機械レイアウトとセンサ・アクチュエータ / layout, sensors, actuators | 5 |
| PLCと制御フロー / PLC and control flow | 4 |
| カメラ・照明・画素計算 / camera, lighting, pixel scale | 5 |
| PCとAIモデル / PC and AI models | 4 |
| データの流れとタイミング / data flow and timing | 4 |
| 結果の有効性とエラー処理 / validity and error handling | 5 |
| HMIと安全境界 / HMI and safety boundaries | 3 |
| 受入試験 / acceptance tests | 3 |

**合格の目安 / pass mark:** 18点以上、かつ次の3条件を満たすこと。 / 18 or more plus all three conditions:
1. 無効・タイムアウト・古いIDをOKにしていない / invalid, timeout and stale IDs are never OK.
2. 安全機能がAIと独立している / safety functions are independent of AI.
3. 平均値ではなく最大値とジッタに触れている / worst case and jitter are considered, not only averages.
