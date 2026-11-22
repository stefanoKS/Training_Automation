# 第7〜9日 サポート教材ガイド / Day 7–9 Support Guide

このフォルダには、第7日〜第9日のノートブックを支える教材があります。ノートブックの本文が**唯一の説明原稿**であり、ここにある資料は演習・参照・検証のための補助です。
This folder holds the material that supports the Day 7–9 notebooks. The notebook manuscripts are the **single source of the explanations**; the files here support practice, reference and verification.

## 構成 / Contents

| フォルダ / folder | 内容 / content |
|---|---|
| `examples/` | 記入例（機械構成図、PLC入出力、結果レコード）/ worked examples |
| `simulations/` | 完全オフラインのHTMLシミュレータ6種 / six fully offline HTML simulators |
| `simulations/fallback/` | JavaScriptが使えない場合の静的画像 / static images when JS is unavailable |
| `worksheets/` | 学生用ワークシート、解答例、評価ルーブリック、用語集 / worksheets, answer keys, rubric, glossary |
| `reference_data/` | 公式カードと保護ファイルの基準ハッシュ / formula cards and protected-file baseline |
| `scripts/` | 図・ノートブック・PDFの生成、PDF検査 / generators and inspectors |
| `tests/` | 契約テストと数値検証 / contract and numeric tests |

## シミュレータ / Simulations

| ファイル / file | 学ぶこと / what it teaches |
|---|---|
| `sim_roller_speed.html` | ローラ径・回転数と表面速度 / diameter, rpm and surface speed |
| `sim_sensor_signals.html` | デジタル・アナログ・エンコーダ / digital, analog and encoder |
| `sim_ladder_logic.html` | AND/OR/NOT・自己保持・タイマ・カウンタ / ladder logic |
| `sim_machine_sequence.html` | 状態遷移と故障 / states and faults |
| `sim_camera_timing.html` | mm/px・ライン周波数・ぶれ / camera timing |
| `sim_ai_result_protocol.html` | 結果の有効性と古いID / result validity and stale IDs |

すべて **ローカルHTMLのみ**で動作し、外部CDN・PLCドライバ・工場ネットワーク・実機制御はありません。JavaScriptが無い環境でも、各ファイル内の `<noscript>` 説明と `fallback/` の画像で学習できます。
All run as **local HTML only**, with no CDN, PLC driver, factory network or real-machine control. Where JavaScript is unavailable, the `<noscript>` text inside each file and the images in `fallback/` keep the exercise usable.

## 再生成の手順 / Regenerating the material

```powershell
# 1. 図 / diagrams (36 SVG, deterministic)
python AI_Vision_Training\day07_09_support\scripts\generate_day07_09_diagrams.py

# 2. 原稿からノートブック / notebooks from manuscripts
python AI_Vision_Training\day07_09_support\scripts\build_day07_09_notebooks.py

# 3. PDF（3冊）/ three PDFs
python AI_Vision_Training\day07_09_support\scripts\export_day07_09_pdf.py

# 4. PDFのページ画像化と検査 / rasterise and inspect
python AI_Vision_Training\day07_09_support\scripts\inspect_day07_09_pdf.py

# 5. シミュレータの論理テストと画面生成 / simulation logic tests and screenshots
node AI_Vision_Training\day07_09_support\tests\run_simulation_logic_tests.js
python AI_Vision_Training\day07_09_support\scripts\render_simulation_fallbacks.py
```

## 教材の原則 / Teaching principles

1. **物理から始める**：部品・力・信号を見てから、アドレスや記号を学ぶ。 / Start from physical reality, then symbols and addresses.
2. **日英を並べる**：同じ場所で日本語と英語を示す。 / Japanese and English sit side by side.
3. **仮定を明示する**：数値は仮定と書く。実機の仕様を断定しない。 / Label assumptions and never assert real specifications.
4. **安全は別**：AI・通常制御・安全系を混ぜない。 / Keep AI, ordinary control and safety separate.
5. **無効はOKではない**：結果の有効性を必ず扱う。 / Invalid is never OK; always handle validity.

## 注意 / Cautions

- 本教材は教育用であり、実機の設計・運転・安全認証ではありません。 / Training material only, not machine design, operation or safety certification.
- シミュレータは実機制御に接続しません。 / The simulators never connect to real control equipment.
- 数値例はすべて仮定です。 / All numeric examples are hypothetical.
