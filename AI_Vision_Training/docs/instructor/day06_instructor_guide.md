# 第6日 講師ガイド / Day 6 instructor guide

**主題 / Message:** AIがコードを書いても、課題、権限、費用、合否は人が管理します。/ AI may write code, but humans own the problem, permissions, budget and acceptance. 時刻は[第6日時間割](../../COURSE_SYLLABUS_DAY06.md)だけを参照。/ Use the [sole Day 6 timetable](../../COURSE_SYLLABUS_DAY06.md).

## 事前準備 / Preparation

- [ ] 5冊のノートブックと[図の目録](../../day06_support/SOURCES_AND_LICENSES.md)をオフラインで開ける / Open five notebooks and the figure manifest offline.
- [ ] 日本語・英語の図ラベルと[PDF](../pdf/Day06_explanation_ja_en.pdf)が読める / Check bilingual figures and PDF readability.
- [ ] [架空の仕様](../../day06_support/examples/inspection_app_spec_ja_en.md)、[会話](../../day06_support/examples/example_agent_conversation_ja_en.md)、[受入表](../../day06_support/examples/example_test_cases_ja_en.md)を印刷する / Print fictional examples.
- [ ] [価格と出典](../../day06_support/pricing/pricing_sources_2026-11-22.md)の確認日と条件を確認する / Check dated pricing sources and conditions; never promise current rates.
- [ ] 顧客資料、実データ、鍵、本番機器を実演に使わない / No customer documents, real data, API keys or production equipment.
- [ ] ライブAIが利用できなくても紙の代替実演を準備 / Prepare offline demonstration; no paid account is mandatory.

## 午前 08:00–09:00 / Morning instructor session

| 分 / Minutes | 話す順番と図 / Speaking sequence and figures | 質問・期待する答え / Question and expected answer |
|---|---|---|
| 0–10 | D06-01/02。第1〜5日の画像AIと第6日の「人が仕事を決める」をつなぐ / Connect vision AI with human-directed software work | YOLOの出力は？→クラスと囲み枠。/ Classes and bounding boxes. |
| 10–22 | D06-03/04/05。LLM、概念上のトークン、文脈窓。具体的なトークン境界はモデル次第 / Explain LLM, conceptual tokens and context | 会話を長くすると？→文脈や費用が増える場合がある。/ Context and cost may grow. |
| 22–32 | D06-06。出版社・モデル・製品を別の列に。ブランドを順位にしない / Separate publisher, model and product | ChatGPTはモデル名？→製品。/ A product, not one model ID. |
| 32–45 | D06-07/08/09。質問に答える作業者と許可を得て複数作業をする作業者の比喩 / Worker analogy and permission diagram | 誰がファイルを実際に変える？→許可後のツール。AIに人の責任はない。/ Tool after permission; AI lacks human accountability. |
| 45–55 | D06-10/11/13。紙の不良記録→目的→必須欄とエラー→架空画面 / Problem, requirements, fictional UI | 空欄なら？→保存を拒否して日本語エラー。/ Reject and explain. |
| 55–60 | 誤解を尋ねる：「完成した」は証拠？ / Ask whether “done” is proof | いいえ。実物・試験・人の受入を確認。/ No; inspect evidence. |

図 D06-08 はモデル単体がPCを操作する説明ではありません。ハーネスが文脈とツールを管理し、敏感な操作では人が許可します。モデルの違いとハーネスの違いを同一視させないでください。

D06-08 must never suggest the bare model controls a computer. The harness manages context and tools, and sensitive operations require a human decision. Changing models and changing harnesses are different decisions.

## 午後 12:50–13:50 / Afternoon follow-up and demonstration

| 分 / Minutes | 講師の行動 / Instructor action |
|---|---|
| 0–12 | 学習者の問題、原因の仮説、望む結果を区別。業務上の機密は架空の例に置き換える / Separate problems, causes and outcomes; fictionalize sensitive details. |
| 12–25 | [仕様](../../day06_support/examples/inspection_app_spec_ja_en.md)の入力・保存・再起動・CSVを質問。D06-13でフォームを投影 / Review fields, persistence, CSV and mockup. |
| 25–40 | D06-14/15/20。ChatGPTに仕様案を作らせ、人が承認した後、実装担当に**編集せず計画だけ**を求める / Approve specification, then request plan without editing. |
| 40–50 | クラウドDB・本番データを含む危険な案を却下。D06-M02の架空進捗でCSVがないと指摘し、D06-16に沿って修正を依頼 / Reject cloud/live data; identify missing CSV and request focused correction. |
| 50–60 | D06-17/18/19/22。架空の$0.40と$0.43の計算、受入と安全を確認 / Calculate fictional costs, then review evidence and safety. |

価格は契約を勧めるためではなく、「AI作業は無料・一回のチャット＝一回の請求」という誤解を直すためです。実際の価格は[日付付き表](../../day06_support/pricing/pricing_sources_2026-11-22.md)の条件によります。**APIキーを貼る実演は絶対にしません。**

Pricing teaches why agent usage may cost money, not which service to purchase. Actual rates are conditional and dated. **Never demonstrate by pasting an API key.**

## 通信やアカウントがない場合の全手順 / Complete offline fallback

1. **問題 / Problem:** 「紙の塩ビシート不良メモが探しにくい」。/ “Paper PVC defect notes are hard to find.”
2. **質問 / Clarification:** 誰が使う？必須欄は？再起動後？CSVは？ 学習者の答え：検査員、ロット/日時/種別、保存保持、一覧/件数/絞り込み/CSV。/ Users, required fields, persistence and CSV.
3. **仕様 / Specification:** [承認用仕様](../../day06_support/examples/inspection_app_spec_ja_en.md)を示す。`PVC-EX-001` 黒点と `PVC-EX-002` 傷は架空。/ Show approved fictional specification and sample lots.
4. **指示 / Agent command:** [Hのテンプレート](../../day06_support/examples/example_agent_prompts_ja_en.md)を読む前に、Dの「計画だけ」を読み、変更を止める。/ Read plan-only instruction before implementation.
5. **悪い計画 / Bad plan:** 「本番DB接続、クラウド、画像判定を追加」。学習者に却下させ、ローカル記録だけの計画へ戻す。/ Reject live DB, cloud and image inference.
6. **承認した計画 / Approved plan:** 画面→検査→保存→絞り込みとCSV→試験。次の段階へは人の確認後。/ Form, validation, persistence, filters/CSV, tests; human approval between stages.
7. **架空進捗 / Simulated progress:** 「保存と一覧を作りました」だが、D06-M02ではCSVが未実装、試験の証拠なし。これは**実際の実行報告ではない**。/ “Save/list done,” but simulated UI lacks CSV and evidence; not a real run.
8. **修正 / Correction:** 「CSVが見当たりません。指定の列順、架空2件を確認し、保存・絞り込みを維持してください」。/ Add CSV only, preserve working features and verify two rows.
9. **受入 / Verification:** [受入表](../../day06_support/examples/example_test_cases_ja_en.md)の空欄、再起動、件数、CSVを紙上で討議。実測したとは書かない。/ Discuss expected results on paper; never claim an actual test.

講師はD06-13のCSVボタンを紙で覆って「ボタンがない」結果も作れます。現実のアプリをその場で作らなくても授業の到達点を満たします。/ Cover the CSV button in the fictional UI to stage an error; no live app is needed.

## 演習の答え・指導 / Exercise answer guidance

| 章 / Module | 問題とよい答え / Exercise and model answer | よくある間違い / Pitfall |
|---|---|---|
| 01 | YOLO=位置と種類、PatchCore=正常との差、LLM=文脈から応答。トークンは単語と同じではない。大きい文脈窓も正解保証なし。簡単な分類なら低価格・短い応答の案も検討 / compare outputs, conceptual tokens/context, model choice | すべてのモデルが画像・ツールに対応すると思う / universal capabilities |
| 02 | モデルが操作を提案、ハーネスが許可確認、ツールが実行。削除・ネットワーク送信は人に確認。モデルを変えても同じハーネスは同じ許可を持ちうる / distinguish harness/tool and approval | AIモデル単体が全ファイルを読めると考える / unlimited access |
| 03 | 問題=記録が探しにくい、望む結果=検索、機能=絞り込み。検査員、必須ロット等、空欄拒否、CSV。画像判定は範囲外。日報の仮データは良品18/不良3 / problem, requirements and daily report | 解決名を問題と呼ぶ / product as problem |
| 04 | 計画のみ→範囲・試験を確認→承認→段階実装。CSVがない場合は列順・架空2行と既存機能の回帰確認を具体的に依頼 / plan, scope and focused correction | 無許可の一括変更、無根拠な完了報告 / broad edits or unsupported “done” |
| 05 | 仮の100,000入力×$2/100万＋20,000出力×$10/100万＝$0.40。4回の合計は$0.43（どちらも架空、追加料金なし）。黒点絞り込みは1件、CSVはヘッダー＋2行。APIキー・PLCは禁止 / calculate, verify and protect | 仮の値を実価格や見積と呼ぶ / invented rates as a quote |

すべての課題はオフラインでも解けます。答えは正しい日本語・英語の一方だけでも内容で評価し、プログラミング構文は評価しません。/ All tasks work offline; assess the content rather than coding syntax.

## よくある誤解とトラブル対応 / Misconceptions and troubleshooting

- モデルと製品は別。ChatGPTのプランがAPI料金を含むと推測しない。/ A product subscription is not proof of API credit.
- プロンプトは依頼、仕様は合意した動作。計画は作業の提案、実装はファイル変更。/ Prompt vs requirements; plan vs execution.
- 画面の見た目、試験結果、人による受入は別。本番システムへの接続は教材の範囲外。/ Appearance, evidence and acceptance differ; production integration is excluded.
- 図が表示されない場合はローカルSVGとPDFで説明する。AIサービスが使えなければ前節の紙の会話を使う。/ Use PDF or local SVG when notebook figures fail; use offline conversation if services are unavailable.
- 価格表と請求が違う場合は地域、長い文脈、キャッシュ、ツール、契約の条件を確認。推測で数字を埋めない。/ Investigate region, context tiers, caching, tools and contract; never guess missing prices.

## まとめと提出 / Final review and submission

16:20〜16:50は[最終ワークシート](../../day06_support/worksheets/Day06_Student_Worksheet_ja_en.md)だけを記入します。[評価表](../../day06_support/worksheets/Day06_Assessment_Rubric_ja_en.md)は目的・要件・修正・安全・費用を見ます。作動するアプリや有料ツールは不要です。

At 16:20–16:50, complete only the [final worksheet](../../day06_support/worksheets/Day06_Student_Worksheet_ja_en.md). The [rubric](../../day06_support/worksheets/Day06_Assessment_Rubric_ja_en.md) evaluates purpose, requirements, corrections, safety and cost, not a running app or paid account.
