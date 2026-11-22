# 第6日 講師ガイド / Day 6 instructor guide

**主題 / Message:** コードはエージェントが書けても、目的・承認・検証は人が担当します。/ Agents may write code; people own purpose, approval and verification. [唯一の時間割](../DAY06_SYLLABUS_ja_en.md) / [Sole timetable](../DAY06_SYLLABUS_ja_en.md). 時間は初学者との試行前の暫定値です。/ Durations are provisional until piloted.

## 午前 08:00–09:00 / Morning 08:00–09:00

| 分 / Minutes | 話す順番・投影図 / Speaking sequence and diagrams | 質問・理解の目安 / Question and expected understanding |
|---|---|---|
| 0–10 | D06-01で第1〜5日との違い。/ D06-01: transition from vision lessons. | 「人が決める仕事は？」→目的と受入条件。/ Human defines goals and acceptance. |
| 10–22 | D06-02でYOLO・PatchCore・LLMの入力と出力。/ Compare input and output. | 「LLMの文章は画像の判定結果？」→異なる。/ No. |
| 22–35 | D06-03/04でモデル、会話支援、エージェント、ハーネス、許可。/ Explain components and permission. | 作業者の比喩：質問へ答える人／資料確認・許可済み作業・結果報告をする人。AIには人の責任はない。/ Worker analogy, with accountability limit. |
| 35–45 | D06-06で曖昧な依頼と仕様を比較。/ Compare vague request and specification. | ロット番号が空ならどうする？/ What about an empty lot? |
| 45–55 | [会話例](../examples/example_agent_conversation_ja_en.md)を紙で演じる。/ Role-play the simulated conversation. | ChatGPTの画像判定案を断らせる。/ Reject image AI. |
| 55–60 | 質問と確認。/ Q&A. | 「完了」は証拠？→違う。/ “Done” is not proof. |

AIが使える場合も架空データだけを投影し、機密を入力しません。製品画面や権限の表示は環境で異なるため、固定の操作を必須にしません。/ If demonstrating a live agent, use fictional data only; interfaces and permissions vary, so no particular product is required.

## 午後 12:50–13:50 / Afternoon 12:50–13:50

| 分 / Minutes | 講師が行うこと / Instructor action |
|---|---|
| 0–12 | 学習者のアイデアから問題・望む結果・解決策を区別する。/ Separate student problems, outcomes and solutions. |
| 12–25 | [仕様例](../examples/inspection_app_spec_ja_en.md)で入力、欠落、再起動、CSVを質問する。/ Use sample spec to ask about inputs, missing values, restart and CSV. |
| 25–40 | D06-09/10：仕様を承認してから、**変更しない計画**を依頼。余計なクラウドDBを却下する。/ Approve specification; request plan-only; reject cloud DB. |
| 40–50 | D06-08/11：架空の未完成結果でCSVがないと指摘し、保存機能を守る修正依頼を示す。/ Find absent CSV in simulated incomplete result; request focused correction. |
| 50–60 | D06-12/14：受入の証拠と機密・設備の境界を話し、質問を受ける。/ Discuss evidence and privacy/equipment boundaries. |

## 実演できない場合の完全な代替 / Complete offline demonstration fallback

1. **最初の依頼 / Request:** 「手書きの不良記録が探しにくい。質問して、コードは書かないで」。/ “Handwritten defect notes are hard to search. Ask questions; no code.”
2. **確認 / Clarification:** 誰が使う？何を記録？再起動後？CSVは？/ Who uses it? What fields? Restart? CSV?
3. **構造化仕様 / Specification:** [承認用仕様](../examples/inspection_app_spec_ja_en.md)。必須はロット・日時・種別、任意は説明・備考。/ Required lot, date/time, type; optional description, remarks.
4. **計画 / Plan:** 日本語フォーム→検査/保存→絞り込み/CSV→確認。最初の案にクラウドを含めて却下させる。/ Japanese form → validation/save → filters/CSV → checks. Reject an initial cloud suggestion.
5. **架空進捗 / Simulated progress:** 「保存・一覧・絞り込み完了。試験詳細なし」。本当に完了したと表現しない。/ “Save/list/filters done; test evidence missing.” Do not present as actual completion.
6. **意図的な不足 / Intentional defect:** D06-08の画面からCSVボタンを紙で覆う。仕様との違いを探す。/ Cover the CSV button in D06-08; ask students to find the difference.
7. **修正依頼 / Correction:** 「CSVが見当たりません。指定の列順・架空2件を出力し、既存の保存と絞り込みを守り、両方を再確認してください」。/ “CSV is absent. Export the specified columns and two fictional rows; preserve saving and filters and recheck both.”
8. **確認表 / Verification:** [受入表](../examples/example_test_cases_ja_en.md)で空欄、再起動、件数、CSVを照合。紙上の予想と実測は分ける。/ Use the checklist for missing inputs, restart, counts and CSV; distinguish planned from observed results.

## 演習解答・指導の目安 / Exercise answer key and guidance

| 演習 / Activity | 目的・答えの例 / Objective and model answer | よくある間違い・指導 / Common mistake and guidance | 目安 / Time |
|---|---|---|---:|
| A 分類 / Classify | 言語生成＝モデル、会話画面＝アシスタント、反復作業＝エージェント、権限管理＝ハーネス、CSV保存＝ツール / model, assistant, agent, harness, tool respectively | 製品名だけで判断しない / Do not classify by brand | 6 |
| B 発想 / Idea | 紙の記録が探しにくい→検索可能な記録 / hard-to-search notes → searchable records | 解決名を問題としない / Do not confuse product and problem | 5 |
| C 要件 / Requirements | 利用者＝検査員、必須ロット等、空欄エラー、CSV / operator, required lot etc., missing-field error, CSV | エラーを加える / Include error behavior | 5 |
| D 指示 / Agent command | 計画を先に、承認後にローカルのみ実装、試験を報告 / plan first; local-only after approval; report tests | 万能を要求しない / Avoid “make it perfect” | 5 |
| E 弱い指示 / Missing guardrails | 利用者・入力・受入基準がない、全ファイル変更を許す / missing users, inputs, checks; broad file permissions | 3点以上特定 / Find at least three | 4 |
| F 計画 / Plan review | クラウドDB・実データは範囲外。計画のみ再提出 / reject cloud and real data; request revised plan only | 実装前に止める / Stop before implementation | 4 |
| G 画面 / Mockup review | CSV出力がないと仕様に反する / absent CSV violates spec | 見た目だけで判定しない / Compare to requirements | 5 |
| H 受入 / Acceptance | 空欄拒否、2件保存、再起動、黒点絞り込み1件、CSV列と2行 / reject empty, save two, restart, filter one, CSV schema and rows | 観察できる値を書く / Include observable values | 5 |
| I 引き継ぎ / Handover | 仕様、変更ファイル、試験結果、未完了、禁止事項 / requirements, files, evidence, remaining work, exclusions | 主張と証拠を区別 / Distinguish claim from evidence | 5 |

モジュール01の追加問題：YOLOは画像→位置とクラス、LLMは指示→応答。D06-04で動くのは権限確認後のツール、無許可の削除は危険。モジュール03の修正演習：CSVなし→指定列順で追加、保存を維持、架空2件で確認。モジュール04の安全問題：PLCへの接続を拒否し、架空のオフライン例を使う。/ Additional answers: YOLO outputs classes/boxes, LLM responses; tools act only after permission; fix missing CSV without breaking saves; reject PLC access and use fictional offline data.

## 誤解を直す / Misconceptions to correct

- **エージェントとLLM / Agent vs LLM:** モデルは応答を生成し、作業の反復はアプリ・ハーネスとツールによる。/ Model generates responses; workflow depends on harness and tools.
- **プロンプトと要件 / Prompt vs requirements:** 指示文は依頼、仕様は合意した動作の基準。/ Instructions request work; requirements define agreed behavior.
- **実装と検証 / Implementation vs verification:** 作ることと確かめることは別。/ Building differs from checking.
- **計画と実行 / Plan vs execution:** 「変更します」は実際の変更ではない。/ “Will change” is not a change.
- **見た目と正しさ / Appearance vs correctness:** ボタンが見えてもCSVの中身は未確認。/ A visible button does not prove CSV contents.
- **試作と本番 / Prototype vs production:** 本番には別途安全・セキュリティ審査が必要。/ Production needs separate safety and security approval.

## 準備 / Instructor preparation

- [ ] 4冊が開き、D06-01〜14がオフラインで見える / Four notebooks open; all figures work offline.
- [ ] 日本語が表示でき、PDFの各章・表・図が読める / Japanese and PDF figures/tables are legible.
- [ ] 架空の仕様、画面、会話、受入表、ワークシートを準備 / Have fictional spec, mockup, conversation, checklist and worksheet.
- [ ] 実情報を使わず、アカウントがなくても代替実演ができる / No real data; offline fallback ready.
