# 第7〜9日 最終レビュー / Day 7–9 Final Review

作成日 / Written: 2026-11-22
実装対象 / Scope: 第7日〜第9日のみ / Days 7–9 only
リポジトリ / Repository: `stefanoKS/Training_Automation`, branch `main`

> この文書の数値・結果は、この作業環境で**実際に実行したコマンドの出力**です。実機・実プラントでの試験は行っていません。
> The figures and results below come from commands actually run in this environment. **No production hardware was tested.**

## 1. 初期と最終のリポジトリ状態 / Initial and final repository state

| 項目 / item | 初期 / initial | 最終 / final |
|---|---|---|
| ブランチ / branch | `main` | `main` |
| HEAD | `0d30045b663104867ec77da9ac55e34714527695` | `0d30045b663104867ec77da9ac55e34714527695`（変更なし / unchanged） |
| 未コミット変更 / uncommitted | なし / none | 新規追加のみ 100 ファイル＋本報告 / 100 new files plus this report |
| コミット・push | 行っていない / not performed | 行っていない / not performed |
| `week2/` | なし / none | なし / none |

`git fetch` は実行していません。リモートとの一致は未確認です。 / No `git fetch`; equality with the remote is unverified.

## 2. 保護ファイルの基準値 / Protected-file baseline

- 基準: `day07_09_support/reference_data/protected_baseline_hashes.txt`（HEAD 時点の全 387 追跡ファイルの `git hash-object`）。
- 検証: `test_protected_files_match_baseline` が 387 ファイルすべてを再計算して一致を確認。**変更 0 件**。
- 検証: `test_only_authorised_paths_changed` が、作業ツリーの変更が許可した新規パスのみであることを確認。
- Day 1–6 のノートブック・原稿・図・PDF・翻訳・データ・重み・既存テスト・Week 1／Day 6 時間割は未変更。
- 既存 Day 6 テストも実行し、**11 passed**（既存テストは修正していません）。

**注意（重要）/ Important caveat:** Day 6 の `test_protected_files_and_no_duplicate_active_lessons` は `git diff HEAD --name-only` を使い、Day 6 の許可パスだけを想定しています。現在は新規ファイルが未追跡のため通っていますが、**コミットすると新規パスが diff に現れ、この既存テストは失敗します**。指示により既存テストは変更していません。別途、許可リストを Day 7–9 に拡張する承認済み変更が必要です。
The Day 6 test lists changed paths with `git diff HEAD` and only allows Day 6 paths. It passes now because the new files are untracked. **Once committed, that pre-existing test will fail** because the new paths appear in the diff. The existing test was not modified, per instruction; extending its allow-list needs a separate authorised change.

## 3. 作成したファイル / Created files（101 / 100 new + this report）

**ルート / root（1）**
- `COURSE_SYLLABUS_DAY07_09.md`

**ノートブック / notebooks（18）**
- `notebooks/Day07_Machine_Fundamentals/`: `Day07_01_Mechanical_Fundamentals.md` / `.ipynb`, `Day07_02_Sensors_and_Signals.md` / `.ipynb`, `Day07_03_Actuators_and_Machine.md` / `.ipynb`
- `notebooks/Day08_PLC_Control/`: `Day08_01_PLC_Fundamentals.md` / `.ipynb`, `Day08_02_Ladder_Basics.md` / `.ipynb`, `Day08_03_Sequence_Control.md` / `.ipynb`
- `notebooks/Day09_System_Integration/`: `Day09_01_Vision_Hardware.md` / `.ipynb`, `Day09_02_PC_AI_Processing.md` / `.ipynb`, `Day09_03_Complete_Integration.md` / `.ipynb`

**図 / diagrams（36）**
- `assets/diagrams/day07/D07-01.svg` … `D07-12.svg`
- `assets/diagrams/day08/D08-01.svg` … `D08-12.svg`
- `assets/diagrams/day09/D09-01.svg` … `D09-12.svg`

**サポート / support（38）**
- `day07_09_support/README_ja_en.md`, `SOURCES_AND_LICENSES.md`
- `examples/`: `example_machine_component_map_ja_en.md`, `example_plc_io_table_ja_en.md`, `example_result_record_ja_en.md`
- `reference_data/`: `protected_baseline_hashes.txt`, `quick_reference_day07.md`, `quick_reference_day08.md`, `quick_reference_day09.md`
- `scripts/`: `svgkit.py`, `generate_day07_09_diagrams.py`, `build_day07_09_notebooks.py`, `export_day07_09_pdf.py`, `inspect_day07_09_pdf.py`, `render_simulation_fallbacks.py`, `engineering_examples.py`
- `simulations/`: `sim_roller_speed.html`, `sim_sensor_signals.html`, `sim_ladder_logic.html`, `sim_machine_sequence.html`, `sim_camera_timing.html`, `sim_ai_result_protocol.html`
- `simulations/fallback/`: 同名 6 点の PNG
- `tests/`: `test_day07_09_contracts.py`, `run_simulation_logic_tests.py`（Node 用 `.js`）
- `worksheets/`: `Day07_Student_Worksheet_ja_en.md`, `Day08_…`, `Day09_…`, `Day07_Answer_Key_ja_en.md`, `Day08_…`, `Day09_…`, `Day07_09_Assessment_Rubric_ja_en.md`, `Glossary_ja_en.md`

**文書 / docs（7 + 本報告）**
- `docs/instructor/day07_instructor_guide.md`, `day08_…`, `day09_…`
- `docs/pdf/Day07_explanation_ja_en.pdf`, `Day08_…`, `Day09_…`
- `docs/reviews/Day07_09_PreImplementation_Audit.md`
- `docs/reviews/Day07_09_Final_Review.md`（本ファイル / this file）

## 4. コース構造 / Course structure

```
第7日 機械 → 第8日 制御 → 第9日 統合
Day 7 mechanics → Day 8 control → Day 9 integration
各日 80分＋85分＋135分 = 必須300分 / 80 + 85 + 135 = 300 required minutes
```

- 時間割は `COURSE_SYLLABUS_DAY07_09.md` が唯一の正本。各日 08:00–16:50、530分、講師120・必須300・休憩30・昼食50・提出30。
- 原稿（Markdown）が唯一の説明原稿。`.ipynb` は原稿から生成（SHA-256 をメタデータに保持）。PDFはノートブックから生成。
- 中心事例は架空の連続塩ビシート検査機。実機の速度・幅・型番・安全カテゴリは断定していません。

## 5. 9つのノートブック / Nine notebook summaries

| Notebook | セル数 / cells | 主要内容 / main content |
|---|---:|---|
| 07-01 Mechanical Fundamentals | 11 | 機械と機構、構造部品、回転と直線、ローラ速度 v=πDN、搬送、機械→画像の因果 |
| 07-02 Sensors and Signals | 11 | 検出と計測、センサ分類、デジタル／アナログ、スケーリング、エンコーダ PPR とカウント、故障 |
| 07-03 Actuators and Machine | 10 | モータ・空気圧・電気制御部品、取付、安全境界、20 要素の構成表、連続材料の品質対応 |
| 08-01 PLC Fundamentals | 10 | 電気の基礎、信号経路、PLC 構成、I/O 表、スキャン周期、PLC と PC、X/Y/M/T/C |
| 08-02 Ladder Basics | 13 | 接点・コイル、物理配線と論理の区別、AND/OR/NOT、内部ビット、自己保持、タイマ、カウンタ、シミュレータ、真理値表 |
| 08-03 Sequence Control | 11 | 状態遷移、起動・停止、3 種のインターロック、タイミング、故障対応、HMI、シーケンスシミュレータ |
| 09-01 Vision Hardware | 11 | カメラ、エリア／ライン、光学と画素スケール、照明、モーションブラー、エンコーダ同期、インタフェース |
| 09-02 PC and AI Processing | 13 | PC 構成、処理パイプライン、前処理、YOLO、PatchCore、比較、判定 6 状態、記録、性能、データ量 |
| 09-03 Complete Integration | 14 | 全体アーキテクチャ、通信、ハンドシェイク、位置追跡、遅延、リアルタイム、14 故障、HMI、安全境界、最終設計 15 項目 |

各ノートブックは到達目標、図、確認質問、演習、解答例、まとめ、完了条件、安全注記を持ちます（テストで検証）。

## 6. 図の一覧 / Diagram inventory（36）

| ID | 内容 / content |
|---|---|
| D07-01 | 検査機の全体構成 / full machine overview |
| D07-02 | フレーム・軸・ベアリング・ローラ / frame, shafts, bearings |
| D07-03 | 回転と直線 / rotation vs linear |
| D07-04 | ローラ径・回転数・速度 / roller speed |
| D07-05 | 張力・しわ・蛇行 / tension, wrinkles, drift |
| D07-06 | 動力伝達 / power transmission |
| D07-07 | モータの種類 / motor types |
| D07-08 | センサ分類 / sensor taxonomy |
| D07-09 | デジタルとアナログ / digital vs analog |
| D07-10 | エンコーダ / encoder |
| D07-11 | 空気圧 / pneumatics |
| D07-12 | 危険源と保護 / hazards and guards |
| D08-01 | PLC 構成 / PLC rack |
| D08-02 | 信号経路 / signal path |
| D08-03 | スキャン周期 / scan cycle |
| D08-04 | 物理状態とビット / physical state vs bit |
| D08-05 | NO/NC 接点 / NO and NC contacts |
| D08-06 | AND/OR/NOT と真理値表 / boolean ladder |
| D08-07 | 自己保持 / self-holding |
| D08-08 | オン遅延タイマ / ON-delay timing |
| D08-09 | カウンタと立ち上がり / counter and edges |
| D08-10 | 状態遷移 / state sequence |
| D08-11 | HMI と診断 / HMI and diagnostics |
| D08-12 | インターロックの境界 / interlock classes |
| D09-01 | 全体アーキテクチャ / system architecture |
| D09-02 | エリアとライン / area vs line scan |
| D09-03 | 光学と画素スケール / optics and pixel scale |
| D09-04 | 照明比較 / lighting comparison |
| D09-05 | モーションブラー / motion blur |
| D09-06 | エンコーダ同期 / encoder sync |
| D09-07 | 取得と処理 / acquisition pipeline |
| D09-08 | YOLO と PatchCore / model outputs |
| D09-09 | ハンドシェイク / result handshake |
| D09-10 | 位置追跡 / position tracking |
| D09-11 | 遅延とバッファ / latency and buffering |
| D09-12 | 故障と受入 / faults and acceptance |

すべて編集可能 SVG、`<title>`/`<desc>` 付き、日英ラベル付き。実際の装置写真は使用していません（利用権を確認できる写真がないため）。

## 7. シミュレーション / Simulation inventory（6 + fallback）

| ファイル / file | 学習内容 / learning |
|---|---|
| `sim_roller_speed.html` | 径・回転数 → 公称表面速度、滑りなしの仮定 |
| `sim_sensor_signals.html` | デジタル、0–10 V、4–20 mA、エンコーダカウント |
| `sim_ladder_logic.html` | AND/OR/NOT、自己保持、オン遅延、カウンタ、理由表示 |
| `sim_machine_sequence.html` | 状態遷移、故障注入、リセット、再起動許可 |
| `sim_camera_timing.html` | mm/px、ライン周波数、露光中の移動 |
| `sim_ai_result_protocol.html` | 有効/無効/タイムアウト/重複/古いID の判定 |

すべてローカル HTML のみ。外部 CDN・通信 API・PLC ドライバなし（テストで禁止文字列を検査）。`<noscript>` 説明と `fallback/*.png` を各シミュレーションに用意。

## 8. 出典とライセンスの確認 / Sources and licensing review

- `day07_09_support/SOURCES_AND_LICENSES.md` に 12 の出典（IEC、ISO、IEC 60204-1、EMVA、Basler、OPC Foundation、Modbus、Ultralytics、Anomalib）を記録。確認日 2026-11-22。
- 規格本文・図表の転載なし。出典は主張の確認にのみ使用。
- 図・シミュレータ・文章は本教材のために新規作成。外部画像・アイコン素材なし。
- PDF 生成時のみローカルの日本語フォントを使用し、フォントファイルは再配布していません。
- 数値・ロット・画像ID はすべて架空。

## 9. 技術的正確性のレビュー / Engineering accuracy review

適用したルール（`12. MANDATORY ENGINEERING CORRECTNESS RULES` に対応）:

- 機械: 力とトルク、位置と速度、回転と直線、駆動とアイドラ、搬送と検査を区別。
- 電気: 制御信号と動力、入力と出力、論理接点と物理接点、通常 PLC と安全系を区別。
- PLC: 「全 PLC が同じスキャン」「全 CPU が同じアドレス」「全タイマが同じ時間単位」「内部ビットが必ず保持」「PLC 出力がモータ電力を供給」と主張していない。
- AI: YOLO が未知欠陥を必ず検出、PatchCore が原因を説明、スコアが校正済み確率、といった主張をしていない。
- 視覚: 画素数が多いほど必ず良い、1 画素の欠陥が必ず検出可能、ラインスキャンが常に優位、任意速度で撮影可能、照明が性能に無関係、といった主張をしていない。
- 統合: ID なしの OK ビット、通信成功＝正しさ、平均推論時間＝応答時間、タイムアウト＝良品、PC が安全制御を代替、AI が非常停止を実行、といった主張をしていない。
- 安全: 危険源・リスクアセスメント・独立した安全系として説明。展開可能な安全プログラムは生成していません。

## 10. 数値の検証 / Numerical verification

`day07_09_support/scripts/engineering_examples.py` の値を pytest で検証（`test_numeric_examples_meet_the_specification`）。

| 例 / example | 入力 / input | 期待 / expected | 実測 / measured | 判定 / result |
|---|---|---|---|---|
| ローラ速度 | D=100 mm, 100 rpm | 31.416 m/min | 31.416 | PASS |
| ローラ速度（追加） | D=80 mm, 200 rpm | 50.265 m/min | 50.265 | PASS |
| 画素スケール | 600 mm / 4096 px | 0.146484 mm/px | 0.146484375 | PASS |
| 画素スケール（追加） | 400 mm / 2048 px | 0.195313 mm/px | 0.1953125 | PASS |
| ライン周波数 | 30 m/min, 0.2 mm/line | 2,500 lines/s | 2500.0 | PASS |
| ライン周波数（追加） | 60 m/min, 0.1 mm/line | 10,000 lines/s | 10000.0 | PASS |
| 生データ量 | 4096 px, 2500 lines/s, 1 B | 10,240,000 B/s | 10240000 | PASS |
| 生データ量（追加） | 2048 px, 5000 lines/s, 1 B | 10,240,000 B/s | 10240000 | PASS |
| 遅延中の移動 | 0.5 m/s, 0.12 s | 60 mm | 60.0 | PASS |
| 遅延中の移動（追加） | 0.4 m/s, 0.15 s | 60 mm | 60.0 | PASS |
| アナログ 0–10 V | 5 V / 0–100 kPa | 50 kPa | 50.0 | PASS |
| アナログ 0–10 V | 7.5 V / 0–200 kPa | 150 kPa | 150.0 | PASS |
| アナログ 4–20 mA | 12 mA / 0–100 kPa | 50 kPa | 50.0 | PASS |
| エンコーダ | PPR 1000, ×4 | 4000 counts/turn | 4000 | PASS |
| エンコーダ角度 | PPR 1000, ×4 | 0.09 °/count | 0.09 | PASS |
| エンコーダ距離 | D=100 mm, PPR 1000, ×4 | 0.07854 mm/count | 0.0785398 | PASS |

追加で `test_manuscripts_quote_the_verified_numbers` が、原稿が 31.416 / 0.09° / 0.07854 / 150 kPa / 0.146484 / 2,500 lines/s / 10.24 MB/s / 60 mm / 81.92 Mb/s を実際に記載していることを確認。

**単位の一貫性 / unit consistency:** mm と m、m/min と mm/s、MB/s と Mb/s、PPR とカウントを区別して記述。カメラ fps とライン周波数、モータ回転数とシート速度、推論時間と全体応答時間を混同していません。

## 11. ラダーと結果プロトコルの検証 / Ladder and protocol verification

- `day07_09_support/tests/run_simulation_logic_tests.js` を Node で実行し、**97 checks passed across 6 simulations**。
- 対象: AND/OR/NOT の真理値表、自己保持（停止優先を含む）、オン遅延（設定前・設定時・入力OFF でリセット）、カウンタ（立ち上がり・保持・プリセット・リセット）、状態遷移（停止優先・起動タイムアウト・故障・リセット・再起動許可・自動再起動なし）、カメラ計算、結果プロトコル。
- 結果プロトコルは、無効・タイムアウト・`valid=false` を **HOLD**、古い ID を **REJECT_STALE**、重複 ID を **REJECT_DUPLICATE**、新しい有効 OK/NG のみ受け付け。
- Python 側でも同じ規則を `engineering_examples.py` で実装し、pytest で検証（二重実装による相互確認）。

## 12. 日英のレビュー / Bilingual review

- すべての原稿・図・ワークシート・ガイド・PDF が日本語と英語を併記。
- 順序は「日本語 → 英語 → 図 → 日英キャプション → 例 → 確認質問」。毎段落への「日本語:」「English:」の反復は避けています。
- 図の主要ノードは図の中に日英ラベルを持ちます（テストで各図 5 つ以上を確認）。
- テストは文字種の存在、図のバイリンガルラベル、PDF の日英テキストを検証。
- **限界:** 日本語母語話者・英語母語話者による独立校正は行っていません。表現の自然さは人間のレビューが必要です。

## 13. PDF の検証 / PDF verification

| PDF | ページ / pages | 埋め込み画像 / images | 目視確認したページ / visually inspected pages |
|---|---:|---:|---|
| Day07 | 36 | 13 | 1（表紙・目次）, 5（D07-04・数式・図）, 25（D07-12・危険源） |
| Day08 | 35 | 12 | 8（レッスン冒頭）, 12（D08-06 真理値表）, 15（D08-08 タイミング）, 30（付録・演習解答） |
| Day09 | 35 | 13 | 18（D09-09 ハンドシェイク・16 進に依存しない確認） |

- `inspect_day07_09_pdf.py` が全 106 ページを PNG 化（`docs/pdf/_pages/`、Git 管理外）。全ページが生成でき、`pypdfium2` の描画で空白ページがないことをテストで確認。
- テキスト検査: 3 モジュールの順序、日英テキスト、目次、公式カード、技術用語集、参考資料、「架空の学習用資料」フッター。
- 文字化け（`??` の連続）がないことをテストで確認。
- 図の重複キャプションを避けるため、PDF では図の直後に置かれる原稿の「図 D0X-XX …」キャプションを使用。
- A4、ページ番号、検索可能テキスト、ローカル画像のみ。
- **限界:** 全 106 ページのうち上記のページを目視確認しました。残りは自動検査（テキスト・画像数・描画の空白判定）のみです。PDF の組版は ReportLab の標準的な流し込みで、専門の組版品質ではありません。

## 14. 自動テストの結果 / Automated test results

```
python -m pytest day07_09_support/tests/test_day07_09_contracts.py -q
27 passed, 9 warnings in 17.95s

python -m pytest day06_support/tests/test_day06_contracts.py -q
11 passed in 2.85s

node day07_09_support/tests/run_simulation_logic_tests.js
SIMULATION LOGIC TESTS PASSED: 97 checks across 6 simulations

python day07_09_support/scripts/inspect_day07_09_pdf.py
PDF inspection passed   (Day07 36p / Day08 35p / Day09 35p)

python day07_09_support/scripts/render_simulation_fallbacks.py
All simulations rendered without page errors
```

Day 7–9 テストの内訳（27）: 保護ハッシュ、許可パス、重複排除、ノートブック 9 本（パラメータ化）、教材要素、事例と安全、図 36、数値、ラダー／プロトコル、原稿の数値記載、シミュレーションのオフライン性、Node ロジック、PDF 3 本（パラメータ化）、PDF 空白判定、時間割、サポート文書、ガイド 15 項目。

## 15. 残る制約 / Outstanding limitations

1. **実機検証なし。** PLC・産業用カメラ・照明・ネットワーク・実材料での試験は行っていません。数値はすべて仮定です。
2. **人間の言語校正なし。** 日英の文章は本実装で作成し、テストは併記の存在のみを確認しています。母語話者の校正が必要です。
3. **講師パイロットなし。** 530 分の配分は規定どおりですが、実際の初学者での時間適合は未検証です。
4. **写真なし。** 利用権を確認できる実機写真がないため、すべてオリジナル SVG です。
5. **図は概念図。** 寸法・比率は物理的に正確な設計図ではありません（誤解を招かない範囲で模式化）。
6. **Day 6 既存テストとの相互作用。** 新規ファイルをコミットすると、Day 6 の許可パス限定テストが失敗します（第 2 節）。既存テストは未変更のため、許可リスト拡張は別途承認が必要です。
7. **PDF の目視はサンプル。** 全 106 ページのうち第 13 節のページを目視、残りは自動検査のみです。
8. **シミュレータのブラウザ差。** Chrome/Edge で page error がないこととスクリーンショットを確認しましたが、複数ブラウザ・複数解像度での回帰試験はしていません。
9. **PDF ページ画像は未コミット。** `docs/pdf/_pages/` は点検用で `.gitignore` 対象です。
10. **RT（リアルタイム）性能の実測なし。** 遅延・ジッタ・バッファの数値は説明用の割合で、実測値ではありません。

## 16. 講師準備状況の評価 / Instructor readiness assessment

**判定 / status: READY WITH DOCUMENTED LIMITATIONS（文書化された制約付きで講師パイロット可能）**

理由 / reasons:

- 9 ノートブック、36 図、6 シミュレーション、3 ワークシート＋解答＋ルーブリック、3 講師ガイド、3 PDF、用語集、公式カードがそろっている。
- 講師ガイドは 15 項目（目標・前提・時間割・午前・午後・図・シミュレーション・質問・誤解・正しい説明・演習解答・トラブル対応・安全制約・オフライン代替・評価）を網羅。
- 実機なし・ネットワークなしでも実施可能。オフライン代替（印刷図、fallback 画像、手計算）を用意。
- 主要な数値はテストで検証済み。安全境界と「無効は OK ではない」原則を全教材で統一。
- 制約（第 15 節）を講師が理解していれば、パイロット実施に支障はない。実機を使う場合は、別途承認された手順と有資格者の監督が必要。

## 17. 明示的に行っていないこと / Explicitly not done

- 実機の設計・製作・設置・運転・安全認証。
- 展開可能な安全 PLC プログラムの生成。
- 実プラントの通信設定・IP アドレス・型番の断定。
- 外部 AI サービスへの機密情報の送信。
- コミット、push、ブランチ作成、履歴書き換え。
- Days 1–6 のファイル変更。

**教育目標 / educational goal:** 受講者が、提案された自動 PVC 検査機を見て、物理構成要素を特定し、センサとラダーが動作を調整する仕組みを説明し、カメラと YOLO/PatchCore が画像を処理する流れを説明し、統合・監視・検証・安全運転を概念レベルで説明できる状態を目指しています。実際の設計・運転は、有資格の機械・電気・自動化・ソフトウェア技術者とともに進める前提です。
