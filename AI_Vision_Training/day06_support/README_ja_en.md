# 第6日：AIエージェントによるソフトウェア開発入門
# Day 6: Introduction to Software Development with AI Agents

第1〜5日の次に読む独立した教材です。**生徒はプログラムを書かず、実行もしません。** 人が問題と合否を決め、AIが提案した内容を確かめます。/ This independent follow-up to Days 1–5 requires **no student programming or code execution**. People define the problem and acceptance and review AI proposals.

## 読む順番 / Reading order

1. [第6日時間割](../COURSE_SYLLABUS_DAY06.md) / [Day 6 syllabus](../COURSE_SYLLABUS_DAY06.md).
2. [01 LLMの基礎と主なモデル](../notebooks/Day06_LLM_Agents/Day06_01_LLM_Fundamentals.ipynb) / [LLM fundamentals and major models](../notebooks/Day06_LLM_Agents/Day06_01_LLM_Fundamentals.ipynb).
3. [02 エージェントとハーネス](../notebooks/Day06_LLM_Agents/Day06_02_Agents_and_Harness.ipynb) / [Agents and harnesses](../notebooks/Day06_LLM_Agents/Day06_02_Agents_and_Harness.ipynb).
4. [03 アイデアから仕様へ](../notebooks/Day06_LLM_Agents/Day06_03_Idea_to_Specification.ipynb) / [Idea to specification](../notebooks/Day06_LLM_Agents/Day06_03_Idea_to_Specification.ipynb).
5. [04 指示と実行の監督](../notebooks/Day06_LLM_Agents/Day06_04_Prompting_and_Execution.ipynb) / [Prompting and execution](../notebooks/Day06_LLM_Agents/Day06_04_Prompting_and_Execution.ipynb).
6. [05 検証・費用・安全・引き継ぎ](../notebooks/Day06_LLM_Agents/Day06_05_Verification_and_Cost.ipynb) / [Verification, costs, safety and handover](../notebooks/Day06_LLM_Agents/Day06_05_Verification_and_Cost.ipynb).
7. [最終ワークシート](worksheets/Day06_Student_Worksheet_ja_en.md) / [Final worksheet](worksheets/Day06_Student_Worksheet_ja_en.md).

ノートブックは文章とローカル図だけ。Jupyterが使えなければ[図入りPDF](../docs/pdf/Day06_explanation_ja_en.pdf)で読めます。AIアカウントがなければ[架空の会話例](examples/example_agent_conversation_ja_en.md)を紙で読んでください。実在する会社の資料やAPIキーは使用しません。

The notebooks contain prose and local figures only. Read the [illustrated PDF](../docs/pdf/Day06_explanation_ja_en.pdf) without Jupyter, and use [fictional conversations](examples/example_agent_conversation_ja_en.md) on paper without an AI account. Never use real company data or API keys.

## 講師・教材作成者 / Instructor and author

[講師ガイド](../docs/instructor/day06_instructor_guide.md)、[評価表](worksheets/Day06_Assessment_Rubric_ja_en.md)、[図と製品の出典](SOURCES_AND_LICENSES.md)、[2026-11-22のAPI料金と出典](pricing/pricing_sources_2026-11-22.md)。料金は変わります。課金前に公式の現行価格と契約を確認してください。

See the [instructor guide](../docs/instructor/day06_instructor_guide.md), [rubric](worksheets/Day06_Assessment_Rubric_ja_en.md), [figure/product sources](SOURCES_AND_LICENSES.md) and [dated API pricing sources](pricing/pricing_sources_2026-11-22.md). Prices change: check current terms before spending.

原稿は5冊と同名の `.md`。教材を改訂した場合はリポジトリのルートから次を順に実行します。これは**教材作成者のみ**で、生徒には不要です。PDF作成にはReportLab、Pillow、PlaywrightとChromeまたはEdge、日本語フォントが必要です。テストにはpytestとpypdfが必要です。第1週の環境や出力は変更しません。

The five `.md` manuscripts next to the notebooks are the editable sources. From repository root, an **author only** runs the following after an edit. PDF generation needs ReportLab, Pillow, Playwright, Chrome or Edge and a Japanese font. Tests need pytest and pypdf. Week 1 dependencies and output remain unchanged.

```cmd
python AI_Vision_Training\day06_support\scripts\build_day06_notebooks.py
python AI_Vision_Training\day06_support\scripts\export_day06_pdf.py
python -m pytest AI_Vision_Training\day06_support\tests\test_day06_contracts.py -q
```

価格は `pricing/pricing_snapshot_2026-11-22.json` を唯一の数字の元とし、生成スクリプトがノートブックの表と出典表を揃えます。独立した第1週用PDF出力・ノートブック発見処理は呼び出しません。/ `pricing/pricing_snapshot_2026-11-22.json` is the sole source of price numbers; the generator keeps notebook and source tables aligned. This workflow does not invoke Week 1 exporters or discovery.
