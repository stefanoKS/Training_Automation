# 第7〜9日 総合評価ルーブリック / Day 7–9 Course Assessment Rubric

**対象 / Applies to:** 第7日〜第9日の必須学習と最終提出物。3日間を通した1つの評価です。 / The required learning and final deliverables of Days 7–9, assessed once across the three days.

**評価するもの / What is assessed**

| 証跡 / Evidence | 内容 / Content |
|---|---|
| 第7日ワークシート / Day 7 worksheet | 現状課題、能力、3案比較、要求仕様、リスク、シリンダ・モーター計算、BOM |
| 第8日ワークシート / Day 8 worksheet | 負荷電流、NPN/PNP、I/O表、自己保持、タイマー、状態遷移、異常処理、通電前確認 |
| 第9日ワークシート / Day 9 worksheet | サブネット、IP割当、通信仕様、ゲート、試験記録、故障ケース、費用対効果、一貫性 |
| 最終提案と10分発表 / final proposal and 10-minute presentation | 課題から次のステップまでの一貫した説明 |

**評価しないもの / Not assessed:** 任意の発展課題、実機の通電試験、実ネットワークの変更、特定メーカーの型式選定。 / Optional extensions, energised hardware tests, real network changes and specific manufacturer selection are not assessed.

## 1. 4つの到達レベル / Four levels of attainment

| レベル / Level | 名称 / Name | 一般的な記述 / General descriptor |
|---|---|---|
| 4 | 模範的 / exemplary | 要求から試験まで一貫し、仮定・未確認・限界を自分から明示できる。他者が同じ結論に到達できる根拠がある。 / Consistent from requirement to test; states assumptions, open items and limits unprompted; the evidence lets another person reach the same conclusion. |
| 3 | 十分 / strong | 主要な判断が正しく、根拠も示されている。小さな抜けはあるが、質問されれば補える。 / Main judgements are correct and evidenced; minor gaps can be filled when asked. |
| 2 | 発展途上 / developing | 結論は一部正しいが、根拠が不足し、仮定と事実が混ざる。誘導があれば修正できる。 / Partly correct, but evidence is thin and assumptions mix with facts; can correct with guidance. |
| 1 | 不十分 / insufficient | 主要な概念を誤解している、または根拠がなく結論だけがある。修正には再学習が必要。 / Misunderstands a core concept or gives conclusions without evidence; correction needs re-learning. |

## 2. 8つの評価観点と重み / Eight criteria and weights

重みの合計は **100** です。各観点を4段階で評価し、`観点の得点 = 重み × レベル ÷ 4` で100点満点に換算します。 / Weights sum to **100**. Score each criterion at one of four levels, then convert with `points = weight × level ÷ 4` for a total out of 100.

| # | 観点 / Criterion | 重み / Weight | 4 模範的 / exemplary | 3 十分 / strong | 2 発展途上 / developing | 1 不十分 / insufficient |
|---|---|---:|---|---|---|---|
| 1 | 要求仕様と受入基準 / requirements and acceptance criteria | 12 | 要求が測定可能で、条件・合格範囲・回数を備え、変更履歴と結びつく / measurable, with condition, range and sample size, linked to changes | 主要な要求が測定可能 / most requirements measurable | 一部が「速く」「安全に」のまま / some stay vague | 要求と受入基準がない、または判定不能 / missing or unjudgeable |
| 2 | 機械の計算と選定根拠 / mechanical reasoning | 15 | 力・面積・効率の式と単位が正しく、理論値と選定候補を区別し、限界を説明する / correct formulas and units; separates theory from candidate and explains limits | 計算は正しく、区別もある / correct with the distinction | 式か単位に誤りがあり、区別が曖昧 / formula, unit or distinction errors | 質量と力を混同し、理論値を選定値として扱う / confuses mass and force; theory treated as selection |
| 3 | 電気・センサー・I/O / electrical, sensors and I-O | 13 | 定常と突入を分け、NPN/PNPを入力共通まで説明し、I/O表が一意で矛盾しない / separates steady and inrush; explains NPN/PNP through the common; one unambiguous map | 計算と判定が正しい / correct calculations and verdicts | 入力共通や出力定格の理解が浅い / shallow on the common or output ratings | 電圧・電流・電力の区別がなく、I/Oが矛盾する / no V-I-P distinction; contradictory I/O |
| 4 | PLC・ラダー・シーケンス / PLC, ladder and sequence | 15 | 自己保持が正しく、指令と確認を分け、タイムアウト・矛盾・リセット・復電を設計する / correct seal-in; command separated from confirmation; timeout, conflict, reset and restore designed | 自己保持と状態遷移が正しい / correct seal-in and transitions | 保持接点や位置確認が抜ける / missing seal-in or confirmation | 自己保持がなく、復電やリセットで動き出す / no seal-in; motion on restore or reset |
| 5 | 通信・ネットワーク / communication and networking | 10 | マスクと一緒に判定し、IP割当が一意で、プロトコル・ポート・喪失時の動作まで書く / judges with the mask; unique allocation; protocol, port and loss behaviour stated | サブネットと割当が正しい / correct subnets and allocation | マスクを無視した判定や重複がある / mask ignored or duplicate addresses | ネットワークとホストの区別がなく、通信成功を結果の正しさと混同する / no network/host distinction; comms success taken as correctness |
| 6 | 試験・トラブルシューティング / testing and troubleshooting | 15 | ゲートを飛ばさず、4状態を正しく使い、故障の原因候補と確認順序を示す / gates respected; four statuses used correctly; candidate causes and check order given | 試験記録が再現可能で、状態の使い分けが正しい / reproducible records and correct statuses | 記録が不足し、状態の区別が曖昧 / thin records and unclear statuses | 未実施をPASSとする、または原因を1つに断定する / unperformed recorded as PASS, or a single guessed cause |
| 7 | 文書化・版管理・引継ぎ / documentation, revision and handover | 8 | 版・変更理由・再試験・未確認が対応し、第三者が5分で状態を理解できる / revisions, reasons, re-tests and open items align; a third party understands the state in five minutes | 版と未確認事項が記録されている / revisions and open items recorded | 記録はあるが、版と試験の対応が切れている / records exist but revisions and tests do not align | 記録がなく、口頭の記憶に依存する / no records; relies on memory |
| 8 | 最終提案の一貫性 / final proposal coherence | 12 | 要求・機械・電気・制御・通信・試験・費用が一致し、弱点を自分で指摘できる / all parts agree and the author names the weaknesses | 主要な値が一致している / main values agree | 値の食い違いや根拠の欠落がある / inconsistencies or missing evidence | 提案が要求と結びつかず、費用対効果を断定する / not tied to requirements; cost-benefit asserted |
| | **合計 / total** | **100** | | | | |

## 3. 採点シート / Score sheet

| # | 観点 / Criterion | 重み / Weight | レベル / Level (1–4) | 得点 / Points | 主な証跡 / Main evidence |
|---|---|---:|---:|---:|---|
| 1 | 要求仕様と受入基準 | 12 | | | 第7日 T4、最終提案 §1–4 |
| 2 | 機械の計算と選定根拠 | 15 | | | 第7日 T6–T8 |
| 3 | 電気・センサー・I/O | 13 | | | 第8日 T1–T3 |
| 4 | PLC・ラダー・シーケンス | 15 | | | 第8日 T4–T7 |
| 5 | 通信・ネットワーク | 10 | | | 第9日 T1–T4 |
| 6 | 試験・トラブルシューティング | 15 | | | 第8日 T7、第9日 T5–T7 |
| 7 | 文書化・版管理・引継ぎ | 8 | | | 第7日 T8、第9日 T6・T9 |
| 8 | 最終提案の一貫性 | 12 | | | 第9日 T8–T9、10分発表 |
| | **合計 / total** | **100** | | **____ / 100** | |

## 4. 評定への変換 / Conversion to a grade

| 合計 / Total | 評定 / Grade | 扱い / Meaning |
|---:|---|---|
| 90–100 | 模範的 / exemplary | 他者への説明資料に使える水準 / usable as an explanation for others |
| 75–89 | 十分 / strong | 実務の補助として使える水準 / usable with supervision |
| 60–74 | 合格 / pass | 必須事項を満たす / meets the required elements |
| 40–59 | 要再学習 / needs review | 指定された観点を再学習して再提出 / re-learn the named criteria and resubmit |
| 0–39 | 不合格 / not yet | 主要概念の再学習からやり直す / restart from the core concepts |

評定は、是正対象（第6節）が1つも残っていない場合にだけ確定します。合計点が高くても、是正対象があれば「是正が必要 / remediation required」と記録し、完了にしません。 / A grade is confirmed only when no remediation trigger in section 6 remains. A high total with an open trigger is recorded as **remediation required** and is not completion.

## 5. 完了の条件 / What completion requires

記入済みであることは、完了の条件ではありません。次をすべて満たした場合にだけ完了とします。 / Filling in the sheets is not completion. All of the following are required.

1. 必須課題（各日の T1〜T8 または T1〜T9）に、式・単位・根拠を伴う答えがある。 / Required tasks have answers with formulas, units and reasoning.
2. 主張のそれぞれに、計算、シミュレーションのログ、試験記録、図面番号のいずれかの証跡がある。 / Every claim has evidence: a calculation, a simulation log, a test record or a drawing number.
3. 仮定・未確認・残るリスクが、責任者と期限付きで書かれている。 / Assumptions, open items and residual risks have owners and dates.
4. 第9日の一貫性チェックで、値の食い違いが解消されている。 / The Day 9 consistency check has no unresolved mismatch.
5. 是正対象（第6節）が残っていない。 / No remediation trigger in section 6 remains.

**完了としない例 / What does not count as completion:** 空欄を「なし」で埋めた答案、数値だけを並べた答案、他者の計算を写した答案、シミュレーションのPASSを実機のPASSとして書いた答案、実機作業を実施したと書いた答案。

Blank fields filled with "none", lists of numbers without reasoning, copied calculations, a simulation PASS presented as a hardware PASS, or a claim of real equipment work are not completion.

## 6. 必須の是正 / Mandatory remediation

次の4つは、点数に関係なく是正を必須とします。該当する観点の得点を **0** とし、補習と再提出を行います。 / The four conditions below require remediation regardless of the total. The affected criterion scores **0**, and targeted instruction and resubmission follow.

| # | 是正対象 / Trigger | 例 / Examples | 対象観点 / Criterion | 補習と再評価 / Remediation and re-assessment |
|---|---|---|---|---|
| R1 | 不安全な再起動 / unsafe restart | 復電で自動復帰する設計、リセットを開始条件に使う、STARTを押しっぱなしで再起動する、保持ビットを前提にする / auto-resume on power restore; reset used as start; held START restarts; assuming retained bits | 4 | 「リセットは開始ではない」「復電時は新規START」を、状態遷移図とトレースで書き直す。再試験は第9日の試験ID T01・T09に相当 / redraw the transitions and trace; re-test the equivalents of Day 9 test IDs T01 and T09 |
| R2 | エネルギー隔離の誤解 / misunderstanding energy isolation | 「遮断器OFFで安全」「コイルOFFで安全」「遮断すれば残圧は抜ける」「配管を外せば残圧が抜ける」 / "breaker off is safe", "coil off is safe", "isolation releases stored pressure", "removing a tube bleeds it" | 3 | 遮断・排気・零圧確認・ロックアウトの順序と、残るエネルギーを説明し直す。通電前チェックを再作成 / restate the isolation sequence and remaining energy; redo the pre-power check |
| R3 | 通常のPLC制御を安全機能と扱う / ordinary PLC control treated as a safety function | 「STOPラングで人身安全を確保」「インターロックをPLCで実装したので安全」「安全カテゴリに適合」 / "the STOP rung assures safety", "the PLC interlock makes it safe", "it meets a safety category" | 3, 4 | リスクアセスメント、独立した安全関連システム、検証の必要性を説明し直す。提案書の安全の記述を修正 / restate risk assessment, independent safety system and validation; correct the proposal |
| R4 | BLOCKEDをPASSとして記録 / BLOCKED recorded as PASS | 未実施の通電試験をPASS、安全機能の検証をPASS、証跡のない試験をPASS / unperformed energised test as PASS, safety validation as PASS, evidence-free PASS | 6 | 4状態（PASS、FAIL、NOT TESTED、BLOCKED）を定義し直し、該当試験をBLOCKEDまたはNOT TESTEDとして再記録 / redefine the four statuses and re-record the test honestly |

**是正の進め方 / Remediation process**

1. 講師が、該当箇所と証跡を特定して記録します。 / The instructor identifies and records the exact place and evidence.
2. 受講者は、指定された課題だけを修正し、理由を添えて再提出します。 / The student corrects only the named task and resubmits with a reason.
3. 再評価は該当観点だけを行い、他の観点の得点は保持します。 / Only the affected criterion is re-assessed; other marks are retained.
4. 同じ是正対象が再発した場合は、再度1から行います。 / A repeat of the same trigger restarts the process.
5. 是正の記録は、最終提案の変更履歴に残します。 / The remediation is recorded in the proposal's change history.

## 7. 証跡の扱い / How evidence is treated

| 証跡 / Evidence | 認める / Accepted | 認めない / Not accepted |
|---|---|---|
| 計算 | 式・代入・単位・仮定がある / formula, substitution, units, assumption | 結果だけ、単位なし / result only, no units |
| シミュレーション | 「シミュレーション」と明記し、入力と観測値がある / labelled simulation with inputs and observations | 実機の合格として提示 / presented as a hardware pass |
| 試験記録 | 前提・手順・期待・実測・状態・証跡・実施者・日付・是正処置 / all fields | OK/NGのみ、証跡なし / OK/NG only |
| 安全 | 危険源、保護方策の方向、専門レビュー前提 / hazards, direction, expert review | 「安全を確保する」だけ / "ensure safety" |
| 費用 | 式、仮定、限界 / formula, assumptions, limits | 数値の断定 / asserted numbers |

シミュレーションのPASSは、実機のPASSでも、安全機能の検証でもありません。この区別を崩した答案は、内容が正しくても第6節の是正対象になります。 / A simulation PASS is neither a hardware PASS nor safety validation. An answer that erases this distinction triggers section 6 even if the rest is correct.

## 8. 口頭確認 / Oral check

口頭確認は点数化せず、理解の確認と補足に使います。次の問いに、用語ではなく現象で答えられるかを確認します。 / Oral checks are not scored; they confirm understanding. Ask for the phenomenon, not the vocabulary.

1. STARTを離しても運転が続くのはなぜですか。 / Why does RUN continue after START is released?
2. 復電時に自動で動き出さないことを、どうやって保証しますか。 / How do you assure no motion on power restoration?
3. 「遮断したので安全」と言えないのはなぜですか。 / Why is "I isolated it, so it is safe" wrong?
4. 11.18 mmは何の下限ですか。 / What is 11.18 mm a lower bound of?
5. 同じ第3オクテットでも別サブネットになるのはどんなときですか。 / When do two addresses in the same third octet differ?
6. タイムアウトした試験をPASSにできないのはなぜですか。 / Why can a timed-out or unperformed test not be PASS?

## 9. 再提出と記録 / Resubmission and records

- 再提出は、指定された観点の修正に限ります。全部を書き直す必要はありません。 / Resubmission is limited to the named criteria.
- 元の提出物と再提出物の両方を残し、変更点を変更履歴に書きます。 / Keep both versions and record the change.
- 期限は講師が指定します。期限後に出された再提出も受理しますが、遅延として記録します。 / The instructor sets the date; late resubmissions are accepted but recorded as late.
- 是正の完了は、最終提案の次のステップに反映します。 / Completed remediation is reflected in the proposal's next steps.

**このルーブリックの限界 / Limits of this rubric:** 評価は提出物と口頭確認に基づきます。実機の技能、実際の安全適合、法規への適合を証明するものではありません。 / Assessment is based on submitted work and oral checks; it does not certify hands-on skill, real safety compliance or regulatory conformity.
