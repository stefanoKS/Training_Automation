# 図と製品の出典 / Figure manifest and product sources

図は本教材のために作成・改訂した編集可能なSVGです。実際の製品画面や第三者のイラストは含みません。架空の塩ビシート画面や会話は実行済みソフトウェア、製品の実画面、または試験記録ではありません。

All diagrams are original editable SVGs made or revised for this course. They do not reproduce third-party artwork or genuine product screenshots. Fictional PVC screens and conversations are not evidence of working software, a product UI or performed tests.

青＝人・指示、青緑＝モデルと作業の流れ、灰＝ツール・環境、琥珀＝確認、赤＝危険・失敗。ただし意味は文字でも示しています。各図のノートブックには日英の説明と代替テキストを付けます。/ Blue=user/instructions, teal=model/workflow, gray=tools/environment, amber=review, red=risk; text labels carry the same meaning. Notebooks include bilingual captions and text alternatives.

| 図 / Figure | 使用章 / Lesson | 教育目的 / Educational objective |
|---|---|---|
| [D06-01.svg](../assets/diagrams/day06/D06-01.svg) | 01 | 第1〜6日の学び / Days 1–6 progression |
| [D06-02.svg](../assets/diagrams/day06/D06-02.svg) | 01 | YOLO・PatchCore・LLMの入出力 / vision versus language outputs |
| [D06-03.svg](../assets/diagrams/day06/D06-03.svg) | 01 | 指示・文脈・LLM・応答 / LLM context and output |
| [D06-04.svg](../assets/diagrams/day06/D06-04.svg) | 01 | 概念としてのトークン / conceptual Japanese/English tokens |
| [D06-05.svg](../assets/diagrams/day06/D06-05.svg) | 01 | 文脈窓と情報の累積 / context window inputs |
| [D06-06.svg](../assets/diagrams/day06/D06-06.svg) | 01 | 提供元・モデル・製品 / publisher, model and product |
| [D06-07.svg](../assets/diagrams/day06/D06-07.svg) | 02 | 会話支援と反復作業 / assistant versus agent |
| [D06-08.svg](../assets/diagrams/day06/D06-08.svg) | 02 | ハーネスとモデルとツール / coding-agent architecture |
| [D06-09.svg](../assets/diagrams/day06/D06-09.svg) | 02 | 権限とツール操作 / permission-checked tools |
| [D06-10.svg](../assets/diagrams/day06/D06-10.svg) | 03 | 問題から人の受入まで / problem to verification |
| [D06-11.svg](../assets/diagrams/day06/D06-11.svg) | 03 | 要件の分類 / requirements structure |
| [D06-12.svg](../assets/diagrams/day06/D06-12.svg) | 04 | 曖昧な依頼と明確な依頼 / prompt comparison |
| [D06-13.svg](../assets/diagrams/day06/D06-13.svg) | 03 | 架空の塩ビシート記録画面 / fictional PVC UI |
| [D06-14.svg](../assets/diagrams/day06/D06-14.svg) | 04 | 人・ChatGPT・実装担当 / three-participant workflow |
| [D06-15.svg](../assets/diagrams/day06/D06-15.svg) | 04 | 段階的な実装 / staged implementation |
| [D06-16.svg](../assets/diagrams/day06/D06-16.svg) | 04 | 不具合と修正依頼 / corrective feedback |
| [D06-17.svg](../assets/diagrams/day06/D06-17.svg) | 05 | 仮の入力・出力料金 / hypothetical input/output rates |
| [D06-18.svg](../assets/diagrams/day06/D06-18.svg) | 05 | 多段階の費用の累積 / multi-step cost |
| [D06-19.svg](../assets/diagrams/day06/D06-19.svg) | 05 | 見た目・動作・受入の証拠 / levels of verification |
| [D06-20.svg](../assets/diagrams/day06/D06-20.svg) | 04 | 要件・計画・試験・受入のゲート / quality gates |
| [D06-21.svg](../assets/diagrams/day06/D06-21.svg) | 05 | 次の担当への引き継ぎ / handover |
| [D06-22.svg](../assets/diagrams/day06/D06-22.svg) | 05 | 情報と設備の安全境界 / privacy and operational safety |

追加の架空画面：[会話](../assets/diagrams/day06/D06-M01-chat-mockup.svg)、[エージェント進捗](../assets/diagrams/day06/D06-M02-agent-progress.svg)、[日報](../assets/diagrams/day06/D06-M03-daily-report.svg)。/ Additional fictional mockups: [conversation](../assets/diagrams/day06/D06-M01-chat-mockup.svg), [agent progress](../assets/diagrams/day06/D06-M02-agent-progress.svg), [daily report](../assets/diagrams/day06/D06-M03-daily-report.svg). The three files are supplementary, not replacements for the 22 principal figures.

**2026-11-22に確認した製品・モデルの公式資料 / Official product and model sources checked 2026-11-22:**

- [OpenAI model catalog](https://developers.openai.com/api/docs/models), [ChatGPT Work and Codex](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex).
- [Google Gemini Developer API pricing/model listing](https://aistudio.google.com/docs/pricing).
- [Anthropic model IDs](https://platform.claude.com/docs/en/models/overview), [Claude Code overview](https://code.claude.com/docs/en/overview).
- [DeepSeek API model names](https://api-docs.deepseek.com/quick_start/pricing).
- [Mistral models](https://docs.mistral.ai/models).
- [xAI models](https://docs.x.ai/developers/models).
- [Alibaba Cloud Model Studio](https://www.alibabacloud.com/help/en/model-studio/model-pricing).
- [Meta Model API models](https://dev.meta.ai/docs/models.md).
- [GitHub Copilot on GitHub.com and mobile](https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-on-github), [VS Code chat](https://code.visualstudio.com/docs/chat/chat-overview).

[料金スナップショットと一行ずつの公式出典](pricing/pricing_sources_2026-11-22.md)も参照。モデルの名前、提供範囲、権限、料金は更新されます。料金の一行からモデルの優劣は決まりません。/ See the [dated per-entry pricing sources](pricing/pricing_sources_2026-11-22.md). Names, availability, permissions and rates change; one price never determines overall quality.
