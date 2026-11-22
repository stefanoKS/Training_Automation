# 第6日 01：LLM・エージェント・ハーネス / Day 6 01: LLMs, agents and harnesses

**目安：70分 / Estimated duration: 70 min.** 全体の時間は[第6日時間割](../DAY06_SYLLABUS_ja_en.md)を参照。コードセルはありません。/ See the [sole Day 6 timetable](../DAY06_SYLLABUS_ja_en.md). There are no code cells.

**目標 / Objectives:** 言語モデル、支援ツール、エージェント、ハーネスを区別し、画像AIとの違いとアクセス権の限界を説明する。/ Distinguish a language model, assistant, agent and harness; explain how they differ from vision AI and what permissions limit them.

## 1. 第1〜5日から第6日へ / From Days 1–5 to Day 6

第1〜5日は画像の扱いとAIの基礎を学びました。第6日は「何を作るか」を人が言葉で決め、AIが作ったものを人が確かめる練習です。

Days 1–5 introduced image processing and AI foundations. Today we practise stating what software should do, then checking what AI produces.

![第1〜5日の学びから第6日の要件・実装・検証への流れ / Progression from vision lessons to requirements and verification](../assets/diagrams/D06-01.svg)

**図 D06-01 / Figure D06-01:** 基礎知識から人の監督へ。/ From technical foundations to human supervision. **問い / Reflect:** 画像を判定する仕事と、アプリの目的を決める仕事はどう違いますか？ / How does image detection differ from defining an application's purpose?

## 2. 言語モデルとは / What is a language model?

大規模言語モデル（Large Language Model: LLM）は、大量の資料から言葉や情報の関係を学習し、入力された指示（プロンプト）と文脈に続く応答を生成するモデルです。「学習」はモデルを作る段階、「利用」は完成したモデルへ指示を送る段階です。文章の整理、説明、設計案、コード案に役立ちますが、もっともらしい誤答も作ります。応答は証拠ではありません。ツールで今調べた情報と、モデルが以前の学習から得た知識は区別しましょう。

A Large Language Model (LLM) learns patterns from large amounts of material and generates responses to a supplied prompt and context. Training builds the model; using it means sending instructions to a trained model. It can explain, organize, design and draft code, but may produce convincing errors. A response is not proof. Distinguish earlier learned knowledge from fresh information retrieved through a tool.

| 方式 / System | 入力 / Typical input | 目的 / Purpose | 出力 / Typical output |
|---|---|---|---|
| YOLO | 画像 / image | 対応する物体クラスと位置の検出 / detect supported classes and locations | クラスと囲み枠 / classes and bounding boxes |
| PatchCore | 画像 / image | 正常例の画像特徴との差の計測 / compare features with learned normal examples | 異常スコア・マップ / anomaly score and map |
| LLM | 指示と文脈 / instructions and context | 応答生成 / generate a response | 文章・構造化出力 / text or structured output |

一部の製品は画像入力やツール操作にも対応しますが、すべてのLLMに共通ではありません。言語モデル単体にはローカルファイルを読む権限はありません。

Some products support images or tools, but not every LLM does. A language model by itself has no permission to read local files.

![YOLO・PatchCore・LLMの入力と出力の違い / Parallel input-process-output flows](../assets/diagrams/D06-02.svg)

**図 D06-02 / Figure D06-02:** 出力の種類を比べる。/ Compare output types. **問い / Reflect:** YOLOの囲み枠とLLMの文章は同じ種類の「判定」ですか？ / Are YOLO boxes and LLM text the same kind of output?

## 3. 支援ツール・エージェント・ハーネス / Assistants, agents and harnesses

AIアシスタント（AI assistant）は人が会話するための仕組みです。ツールを持つアシスタントもあります。AIエージェント（AI agent）は、目標へ向かって複数の判断・操作・確認を繰り返す**進め方**です。プログラム作成に特化すればコーディングエージェント（coding agent）と呼びます。名前だけで能力は決まりません。作業者の例なら、質問に答えることと、資料を確認して許可された作業を行い結果を報告することの違いです。ただしAIには人間の責任や独立した理解はありません。

An AI assistant is a user-facing conversation system; some assistants can use tools. An AI agent describes a **workflow** that pursues a goal through decisions, actions and checks. A coding agent specializes in software work. A worker answering a question differs from one checking documents, performing authorized steps and reporting findings; unlike a person, an AI agent does not have human accountability or independent understanding.

ハーネス（agent harness）はモデルに文脈を渡し、ツール、許可、実行結果、次の操作を管理するソフトウェア側の仕組みです。モデルが「ファイルを修正したい」と出しても、実行するのは許可を確認したハーネスとツールです。人は重要な操作を承認し、結果を監督します。

An agent harness is the software that manages context, tools, permissions, execution results and subsequent steps. A model may propose an edit; an authorized harness and tool perform it. The human approves sensitive operations and monitors progress.

![モデル、支援ツール、エージェント、ハーネスの関係 / Conceptual layers, not exclusive product types](../assets/diagrams/D06-03.svg)

**図 D06-03 / Figure D06-03:** これらは排他的な製品分類ではありません。/ These are overlapping concepts, not mutually exclusive product types. **問い / Reflect:** 「モデルを変更した」だけでファイル権限は変わりますか？ / Does changing a model alone change file permissions?

![ユーザーから権限確認、ツール実行、結果の観察まで / Proposed action, permission and observed result cycle](../assets/diagrams/D06-04.svg)

**図 D06-04 / Figure D06-04:** 提案と実行は別。機密操作は人に確認する。/ Proposal differs from execution; ask a human before sensitive operations. **問い / Reflect:** ファイルを実際に変更するのはどこですか？ / Which component actually changes a file?

モデルを変えると応答の傾向が変わる場合があります。アプリやハーネスを変えると作業の流れ、指示を変えると目標、ツールを変えると操作範囲、実行環境を変えると使えるファイルなどが変わります。どれも同じ変更ではありません。

Changing the model may affect answers; changing the application/harness affects workflow; instructions change the goal; tools change available actions; the execution environment changes accessible resources. These are different changes.

## 4. 製品名は役割と分けて読む / Product names are not roles

ChatGPTは会話用の製品、CodexやClaude Codeはコーディング作業に使う製品、GitHub Copilotは複数の画面・作業形態で使われる製品です。OpenAI、Anthropic、Google、DeepSeekはモデル提供元の例です。製品、モデル、エディタ、ハーネスを同じものと呼ばないでください。利用できるツールと承認方法は製品・設定・契約で異なります。特定の画面や有料機能はこの授業に必要ありません。

ChatGPT is a conversation product; Codex and Claude Code are examples of coding tools; GitHub Copilot spans multiple surfaces and workflows. OpenAI, Anthropic, Google and DeepSeek are examples of model providers. Do not equate products, models, editors and harnesses. Tools and approval vary by product, configuration and access; no paid feature is mandatory here. [確認した公式資料 / Checked official references](../assets/SOURCES_AND_LICENSES.md).

**問い / Reflect:** 製品名だけから「すべてのPCファイルが読める」と推測できますか？ / Can a product name alone establish that it can read every file?

## 5. 誤解を解く / Correcting misconceptions

| よくある誤解 / Misconception | 実際 / Correction |
|---|---|
| エージェントは希望を正確に知っている / It knows exactly what I want | 曖昧な点を質問させる / Ask it to clarify ambiguity |
| 「完了」は正しさの証明 / “Done” proves correctness | 基準と実物を比べる / Compare the result with acceptance criteria |
| モデルはPC上の何でも読める / A model can read everything | ツール・権限・環境による / Access depends on tools, permissions and environment |
| モデルを替えるとハーネスも替わる / Changing the model changes the harness | 別の仕組み / They are separate components |
| 詳細に書けば必ず正しい / More detail guarantees success | 指示を改善しても検証は必要 / Better instructions still need verification |
| AI製ソフトは試さなくてよい / No testing is needed | 人が受入条件を確かめる / Humans still verify acceptance |
| エージェントが全判断を代行する / An agent replaces all decisions | 目的・リスク・許可は人が決める / Humans own purpose, risk and approval |

**問い / Reflect:** 「終わりました」と言われたら、何を確認しますか？ / If it says “finished,” what would you check?

## 6. 演習（合計15分）/ Practice (15 min total)

**演習 A / Activity A (6 min):** 「言語を生成するモデル」「会話画面」「許可を管理する仕組み」「CSVを保存する操作」「計画→編集→確認を繰り返す流れ」を、モデル・アシスタント・ハーネス・ツール・エージェントに分けてください。/ Classify a response-generating model, chat interface, permission manager, CSV-save action, and iterative plan–edit–check workflow. **提出 / Output:** 5組の対応 / five matches. **よくある間違い / Pitfall:** 製品名だけで決める / classifying by brand alone.

**演習 B / Activity B (4 min):** YOLOとLLMの入力・出力を各1文で比べる。/ Compare YOLO and an LLM in one sentence each. **提出 / Output:** 2文 / two sentences. **間違い / Pitfall:** LLMが直接PCを動かすと書く / claiming a standalone LLM controls the PC.

**演習 C / Activity C (5 min):** 図 D06-04 の「実行する部品」を示し、許可なしの操作の危険を一つ書く。/ Identify the executing component in D06-04 and one risk of acting without approval. **提出 / Output:** 部品と危険 / component and risk. **間違い / Pitfall:** 提案と実行を混同する / confusing a proposed action with execution. [講師の解答](../instructor/day06_instructor_guide_ja_en.md) / [Instructor answers](../instructor/day06_instructor_guide_ja_en.md).

**完了チェック / Completion:** 違いを説明できる、図で権限を示せる、成功宣言と証拠を区別できる。/ Explain the distinctions, locate permission checks and separate claims from evidence.
