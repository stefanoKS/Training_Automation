# 第6日：AIエージェントによるソフトウェア開発入門
# Day 6: Introduction to Software Development with AI Agents

この教材は第1〜5日の内容を変更しない、独立した第2週の授業です。プログラムを書く授業ではありません。人が問題を決め、AIへの指示を確認し、結果を検証します。

This independent Week 2 lesson does not alter Days 1–5. It is not a coding class. The human defines the problem, reviews AI instructions and verifies the result.

## 読む順番 / Reading order

1. [時間割 / Syllabus](DAY06_SYLLABUS_ja_en.md)
2. [01 LLM・エージェント・ハーネス / LLMs, agents and harnesses](lessons/Day06_01_LLM_Agent_Harness.ipynb)
3. [02 アイデアと要件 / Ideas and requirements](lessons/Day06_02_Ideas_and_Requirements.ipynb)
4. [03 エージェントへの指示 / Communicating with agents](lessons/Day06_03_Prompting_and_Agents.ipynb)
5. [04 検証と引き継ぎ / Verification and handover](lessons/Day06_04_Testing_and_Handover.ipynb)
6. [最終ワークシート / Final worksheet](worksheets/Day06_Student_Worksheet_ja_en.md)

ノートブックはすべて文章とローカル図だけです。Jupyter を使わず PDF で読んでも構いません。AIアカウントがない場合は [会話例](examples/example_agent_conversation_ja_en.md) を読み、紙で演習します。実際の生産情報や顧客情報は入力しないでください。

All notebooks contain only prose and local figures. You can read the [PDF](pdf/Day06_explanation_ja_en.pdf) without Jupyter. Without an AI account, use the [sample conversation](examples/example_agent_conversation_ja_en.md) and work on paper. Never enter real production or customer information.

講師向け：[ガイド](instructor/day06_instructor_guide_ja_en.md)・[採点表](worksheets/Day06_Assessment_Rubric_ja_en.md)。教材を編集する場合は各 `.md` を修正し、リポジトリのルートから `python AI_Vision_Training\week2\day06\scripts\build_day06_notebooks.py`、次に `python AI_Vision_Training\week2\day06\scripts\export_day06_pdf.py` を実行します。教材作成者の環境に ReportLab、Pillow、Playwright と Chrome または Edge が必要です。検証は `python -m pytest AI_Vision_Training\week2\day06\tests\test_day06_contracts.py -q`（pytest、pypdf が必要）。授業での実行は不要です。

For instructors: [guide](instructor/day06_instructor_guide_ja_en.md) and [rubric](worksheets/Day06_Assessment_Rubric_ja_en.md). To change a lesson, edit its `.md` manuscript, run `python AI_Vision_Training\week2\day06\scripts\build_day06_notebooks.py` from repository root, then `python AI_Vision_Training\week2\day06\scripts\export_day06_pdf.py`. The authoring machine needs ReportLab, Pillow, Playwright and Chrome or Edge. Check with `python -m pytest AI_Vision_Training\week2\day06\tests\test_day06_contracts.py -q` (requires pytest and pypdf). Learners run nothing.
