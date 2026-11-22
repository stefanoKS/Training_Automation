# コピーして調整する指示集 / Adaptable bilingual prompt library

**使用前に必ず人が見直してください。実データを入力しないでください。** `[]` は自分の架空の情報へ置き換えます。どの指示も正しさを保証しません。/ **Review each prompt before use; never insert real data.** Replace `[]` with fictional details. No prompt guarantees correctness.

## A. アイデアの探索 / Idea exploration

**いつ / When:** 問題はあるが方法を決めていない時。/ When you know the problem but not the solution.

**日本語 / Japanese:** 「私はプログラミング初心者です。[架空の現場の問題]を解決したいです。紙の改善、単純な表、アプリなど異なる方法を3つ示し、それぞれの利点・欠点・利用者・必要な確認事項・成功の測り方を比べてください。コードはまだ書かないでください。」

**English:** “I am new to programming. I want to solve [fictional workflow problem]. Compare three different approaches, such as improving paper forms, using a simple table or building an app. Give pros, cons, users, unknowns and success measures. Do not write code yet.”

**変える所 / Customize:** 問題と利用者 / problem and users. **期待 / Expect:** 比較表 / comparison. **間違い / Pitfall:** AIが不要な機能を足す / accepting extra features. **確認 / Check:** 3案・利点・欠点・コードなし / three options, trade-offs, no code.

## B. 要件の確認 / Requirements clarification

**いつ / When:** 案を選んでから。/ After selecting an approach.

**日本語 / Japanese:** 「[選んだ架空の案]を仕様にしてください。まず足りない条件を質問してください。目的、利用者、入力、処理、出力、画面、制約、エラー、受入基準を整理し、未確認の前提は明記してください。必須と任意を分け、コードは書かないでください。」

**English:** “Turn [chosen fictional idea] into a specification. Ask about missing conditions first. Organize purpose, users, inputs, processing, outputs, UI, constraints, errors and acceptance checks. Mark unconfirmed assumptions. Separate must-haves from optional features. No code yet.”

**変える所 / Customize:** 案・必要な項目 / idea and needed fields. **期待 / Expect:** 質問と仕様案 / questions and draft. **間違い / Pitfall:** 前提を事実扱い / treating assumptions as facts. **確認 / Check:** 質問・優先度・エラー / questions, priorities, errors.

## C. 実装指示を作る / Generate a coding-agent command

**いつ / When:** 人が仕様を承認した後。/ After a human approves the specification.

**日本語 / Japanese:** 「承認済みの[仕様]から、コーディングエージェントへの指示案を作ってください。役割、目的、既存プロジェクトの背景、必須機能、変更してよい場所[範囲]、触れてはいけないファイル・情報、段階（調査→計画→承認→実装→試験）、各段階の確認、受入基準、成果物、最終報告（変更ファイル・試験結果・未解決事項）を含めてください。計画は最初に提示させ、承認前の変更を禁止してください。不要な機能は追加しないでください。」

**English:** “Draft a coding-agent instruction from [approved specification]. Include role, objective, existing project context, required features, allowed file scope [scope], prohibited files/data, stages (inspect → plan → approval → implementation → tests), checkgates, acceptance checks, deliverables and a completion report (changed files, test evidence, open issues). Require a plan before any changes. Do not add optional features.”

**変える所 / Customize:** 承認済み仕様・範囲・禁止事項 / approved specification, scope and exclusions. **期待 / Expect:** 確認用の指示案 / instruction draft. **間違い / Pitfall:** AI案を無審査で実行 / using draft unchecked. **確認 / Check:** 承認前は変更なし・範囲・受入基準 / no changes before approval, scope, acceptance.

## D. 計画だけ / Plan only

**いつ / When:** コーディングエージェントへ最初に依頼する時。/ First request to a coding agent.

**日本語 / Japanese:** 「[架空仕様]を満たすため、既存のプロジェクトを調べて、既存機能、変更予定ファイル、単純な実装方法、危険、試験方法と未確認事項を示してください。今は計画だけです。ファイルの編集・削除、コマンド実行、実データへのアクセスは行わず、計画を提示して承認を待ってください。」

**English:** “Inspect the existing project for [fictional specification] and propose a simple plan: current behavior, files to change, risks, tests and open questions. Plan only: do not edit/delete files, run commands or access real data. Wait for approval.”

**変える所 / Customize:** 仕様と範囲 / specification and scope. **期待 / Expect:** 未実行の計画 / unexecuted plan. **間違い / Pitfall:** 計画と同時に実装 / implementation during planning. **確認 / Check:** 未変更・予定ファイル・危険 / no modifications, files, risks.

## E. 修正 / Correction and debugging

**いつ / When:** 観察した不具合がある時。/ When you have observed a failure.

**日本語 / Japanese:** 「観察：[架空の手順と実際の結果]。期待：[承認済み要件の結果]。再現：[操作手順]。原因を調べ、[対象箇所]だけ直し、無関係な機能・ファイルを維持してください。修正後、失敗した場合と正常な場合の両方を再確認し、実際に行った試験と未確認事項を報告してください。」

**English:** “Observed: [fictional steps and actual result]. Expected: [approved behavior]. Reproduce using [steps]. Investigate and fix only [scope], preserving unrelated files and working features. Recheck both the failure and a valid case; report actual tests and anything unverified.”

**変える所 / Customize:** 観察・期待・手順 / observations, expectation and steps. **期待 / Expect:** 限定的な修正と証拠 / focused fix and evidence. **間違い / Pitfall:** 「全部直して」 / “fix everything.” **確認 / Check:** 再現・正常系・変更範囲 / reproduction, valid case, scope.

## F. 引き継ぎ / Handover and continuation

**いつ / When:** 作業を中断・交代する時。/ When stopping or changing agents.

**日本語 / Japanese:** 「[承認済み仕様]と現在の状態を照合し、引き継ぎ文を作ってください。完成した機能、残る仕事、変更したファイル、実際の試験と結果、未確認事項、既知の問題、次の操作、触れてはいけない箇所を区別して記録してください。新担当にはまず既存の状態を確認させ、根拠のない『完了』は書かないでください。」

**English:** “Compare current state with [approved specification] and prepare a handover: completed features, remaining work, changed files, actual tests and results, unverified items, known issues, next actions and protected files. Ask the receiving agent to inspect current state before editing; do not claim unverified completion.”

**変える所 / Customize:** 仕様・現在の進捗 / specification and progress. **期待 / Expect:** 証拠付きの引き継ぎ / evidence-based handover. **間違い / Pitfall:** 「完了」だけ / only “done.” **確認 / Check:** 残作業・試験・禁止箇所 / remaining work, tests, exclusions.

**提案を却下する例 / Reject an unnecessary suggestion:** 「画像判定機能は承認していません。追加せず、ローカルの記録・絞り込み・CSVだけに計画を限定してください。」 / “Image classification is not approved. Remove it and limit the plan to local recording, filters and CSV.”
