# 第7〜9日 総合評価ルーブリック / Day 7–9 Assessment Rubric

対象 / applies to: 3日間の最終提出物（Day 7 機械構成図、Day 8 PLC入出力・シーケンス表、Day 9 基本設計書）。
The three final deliverables: Day 7 Machine Component Map, Day 8 PLC I/O and Sequence, Day 9 Conceptual Design Sheet.

**理解を評価し、暗記は評価しません。 / Assess understanding, not memorisation.**

## 1. 共通の4観点 / Four common criteria

| 観点 / criterion | 4 十分 / strong | 3 妥当 / adequate | 2 不足 / limited | 1 不十分 / insufficient |
|---|---|---|---|---|
| 用語の正確さ / terminology accuracy | 用語を正しく使い、区別を説明できる / uses terms correctly and explains distinctions | おおむね正しい / mostly correct | 混同がある / some confusion | 主要な用語を誤る / major errors |
| 技術的な妥当性 / technical soundness | 因果関係と単位が正しい / correct causality and units | 小さな誤り / minor errors | 単位や因果に誤り / unit or causal errors | 結論が成り立たない / conclusion invalid |
| 安全の理解 / safety understanding | AI・通常制御・安全系を明確に分ける / clearly separates AI, ordinary control and safety | 区別あり / distinguishes them | あいまい / vague | 混同 / conflates |
| 説明の明確さ / clarity | 初学者にも伝わる日本語と英語 / clear to a beginner in both languages | おおむね明確 / mostly clear | 分かりにくい箇所 / hard to follow | 意味が取りにくい / unclear |

## 2. 第7日 / Day 7

| 項目 / item | 重み / weight | 見る点 / what to look for |
|---|---:|---|
| 部品の識別 / component identification | 20% | 部品名・役割・位置 |
| センサと信号 / sensors and signals | 20% | 対象材質・信号形式・限界 |
| アクチュエータ / actuators | 15% | 指令と動力の区別 |
| 速度計算 / speed calculation | 20% | 式・単位・滑りの仮定 |
| 機械と画像の因果 / mechanics to image | 15% | 振動・しわ・速度変動 |
| 危険源と保護 / hazards | 10% | 3種類の区別 |

## 3. 第8日 / Day 8

| 項目 / item | 重み / weight | 見る点 / what to look for |
|---|---:|---|
| PLC構成とI/O / PLC and I/O | 15% | 入力・出力・デジタル・アナログ |
| 真理値表 / truth tables | 15% | AND/OR/NOT |
| 接点の論理 / contact logic | 20% | NO/NCとビット値 |
| 自己保持 / self-holding | 15% | 停止優先 |
| タイマ・カウンタ / timer and counter | 15% | 時間単位・立ち上がり |
| シーケンスと故障 / sequence and faults | 10% | 遷移条件・復旧 |
| 安全の区別 / safety separation | 10% | 通常ラダーと安全系 |

## 4. 第9日 / Day 9

| 項目 / item | 重み / weight | 見る点 / what to look for |
|---|---:|---|
| アーキテクチャ / architecture | 15% | 層の分離 |
| 光学と画素計算 / optics and pixel scale | 15% | FOV・画素数・単位 |
| ラインレートと露光 / line rate and exposure | 10% | 速度・間隔・ぶれ |
| PCとAI / PC and AI | 15% | YOLO/PatchCoreの出力差 |
| 結果の有効性 / result validity | 20% | ID・有効性・タイムアウト |
| 故障対応 / fault handling | 10% | 検出・記録・人の確認 |
| 安全境界と受入 / safety and acceptance | 15% | AIからの独立性 |

## 5. 重大な誤り / Critical errors（自動的に不合格 / automatic fail）

- 無効・タイムアウト・通信断・古い結果を「良品」と扱う / treating invalid, timeout, comms loss or stale results as OK.
- AIの判定や通常のラダーを安全機能と表現する / calling AI or ordinary ladder a safety function.
- 実機の数値・型番・安全カテゴリを断定する / asserting real specifications, model numbers or safety categories.
- 不安全な作業を指示する / instructing unsafe work.
- 単位を無視した計算、または式と値の不一致 / ignoring units or inconsistent formula and value.

## 6. 評定への変換例 / Example conversion

| 合計 / total（100点換算 / out of 100） | 評定 / judgement |
|---:|---|
| 90–100 | 模範的 / exemplary |
| 75–89 | 十分 / strong |
| 60–74 | 合格 / pass |
| 40–59 | 要再学習 / needs review |
| 0–39 | 不合格 / not yet |

**再提出 / resubmission:** 重大な誤りがある場合は、該当部分を修正して再提出します。他の部分の点は保持します。
If a critical error is present, correct that part and resubmit; marks for other parts are retained.

## 7. 口頭確認の例 / Oral check examples

1. 「NC接点」と「NCスイッチ」はどう違いますか。 / How does an NC contact differ from an NC switch?
2. タイムアウトしたAI結果を、なぜOKにできないのですか。 / Why can a timed-out AI result not be OK?
3. ライン周波数とフレームレートの違いを説明してください。 / Explain line rate versus frame rate.
4. 安全機能がAIと独立している必要がある理由は。 / Why must safety be independent of AI?

口頭確認は点数化せず、理解の確認と補足に使います。 / Oral checks are used to confirm understanding, not to score.
