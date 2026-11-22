# Day 6 final revision review / 第6日改訂の最終確認

**Review date: 2026-11-22.** The five-module, notebook-first no-code course is ready for an instructor-led pilot. This review records what was actually checked; it does not claim that a real PVC application was built, that provider prices are permanent, or that a beginner classroom pilot has occurred.

## Deliverables and migration

- Five Markdown-only [notebooks](../../notebooks/Day06_LLM_Agents/) built from five adjacent `.md` manuscripts: [01 LLM fundamentals](../../notebooks/Day06_LLM_Agents/Day06_01_LLM_Fundamentals.ipynb), [02 agents and harnesses](../../notebooks/Day06_LLM_Agents/Day06_02_Agents_and_Harness.ipynb), [03 ideas and specifications](../../notebooks/Day06_LLM_Agents/Day06_03_Idea_to_Specification.ipynb), [04 prompting and supervision](../../notebooks/Day06_LLM_Agents/Day06_04_Prompting_and_Execution.ipynb), and [05 verification and costs](../../notebooks/Day06_LLM_Agents/Day06_05_Verification_and_Cost.ipynb). The builder checks source hashes and expands the nine-template prompt library and dated pricing table.
- Revised [60-page PDF](../pdf/Day06_explanation_ja_en.pdf), independently exported from those notebooks. Its last page includes a model-by-model list of official price URLs and conditions. The PDF contains 25 embedded figures (22 numbered figures and three fictional mockups).
- [Syllabus](../../COURSE_SYLLABUS_DAY06.md): five modules of 50, 55, 80, 65 and 50 minutes; 300 minutes of mandatory instruction within a 530-minute day. [Instructor guide](../instructor/day06_instructor_guide.md), [worksheets](../../day06_support/worksheets/), [nine prompt templates](../../day06_support/examples/example_agent_prompts_ja_en.md), [pricing snapshot](../../day06_support/pricing/pricing_snapshot_2026-11-22.json), and [submissions guidance](../../submissions/day06/README.md) complete the separate support structure.
- The previous four lesson/notebook pairs, support documents, report and PDF were moved or revised rather than overwritten in place. The former 14 SVGs were removed **only after** their 22 numbered successors and the three mockups were verified; the old `week2/day06/` directory and duplicate active lessons are gone. The earlier report is retained as a [historical record](Day06_Original_Implementation_Report.md), alongside the [pre-revision audit](Day06_PreRevision_Audit.md).

## Figure-by-figure audit

The [manifest](../../day06_support/SOURCES_AND_LICENSES.md) links each editable SVG. All 25 were XML-parsed, checked for SVG title and description, at least five Japanese-bearing labels and five English-bearing labels, absence of replacement/doubled-question-mark placeholders, and an actual lesson reference. The diagram creator also checked browser-rendered text bounds and overlaps. Representative rendered PDF pages (including diagrams 01, 10, 13, 18, 19, 20 and 22 and mockups) were visually inspected for legible Japanese/English labels, framing and page flow. This is not a native-speaker linguistic review of every label.

| Figure | Tested teaching purpose / audit result |
|---|---|
| D06-01 | Day 1–6 progression; paired stage labels, used in 01 |
| D06-02 | YOLO, PatchCore and LLM input/output; distinct roles, used in 01 |
| D06-03 | Instruction/context/model/response flow; used in 01 |
| D06-04 | Token concept, not a literal one-character tokenizer; used in 01 |
| D06-05 | Context-window accumulation and limits; used in 01 |
| D06-06 | Publisher, model and product distinction; used in 01 |
| D06-07 | Assistant versus agent behavior; used in 02 |
| D06-08 | Model, harness and tools as distinct parts; used in 02 |
| D06-09 | Tool permissions, not unapproved equipment action; used in 02 |
| D06-10 | Problem-to-human-acceptance sequence; used in 03 |
| D06-11 | Requirements categories and testability; used in 03 |
| D06-12 | Vague versus bounded prompt; used in 04 |
| D06-13 | Fictional local PVC record form, not a real app; used in 03 |
| D06-14 | Human, brainstorming assistant and coding agent; used in 04 |
| D06-15 | Small staged implementation and review; used in 04 |
| D06-16 | Specific corrective feedback rather than a restart; used in 04 |
| D06-17 | Hypothetical input/output token billing; used in 05 |
| D06-18 | Illustrative cumulative multi-call cost, separate from the worksheet's $0.43 example; used in 05 |
| D06-19 | Screenshot versus behavior versus human acceptance; used in 05 |
| D06-20 | Approval gates and return paths; used in 04 |
| D06-21 | Evidence, limits and next steps at handover; used in 05 |
| D06-22 | Privacy and operational-safety boundary; used in 05 |

The additional conversation, agent-progress and daily-report SVGs are explicitly fictional, referenced in lessons, bilingual, and included in the PDF.

## Pricing and pedagogical accuracy

The [dated source sheet](../../day06_support/pricing/pricing_sources_2026-11-22.md) is rendered from one JSON snapshot: 16 exact model IDs from eight hosted API providers, each with a provider URL, input and output rates, cached-read rate where verified, applicable tier and caveat. Units are **USD per million tokens**, not subscription fees or per-request prices. `Not verified` is not zero. Rates are illustrative and conditional: DeepSeek's listed prices are off-peak; xAI and Anthropic have context-length tiers; the Qwen example is Model Studio International; the Google Carbon example has a dated rate transition. Hosted Meta Muse is not identified as Meta Llama. Recheck all current official prices and availability before purchasing or teaching. These examples do not rank model capability or guarantee access.

Lesson 05 separately calculates **$0.40** for 100,000 input and 20,000 output tokens at *hypothetical* $2/$10 rates; four calls total 115,000 input and 20,000 output tokens for **$0.43**. Arithmetic tests cover both and negative-token rejection. The independent $1.50 illustration in D06-18 is labelled as a different hypothetical series, not the four-call worksheet rate.

The course distinguishes model output from executed tool actions, brainstorming from implementation, and screenshots from functional and human acceptance evidence. The PVC record and daily-report narratives are simulated, use invented lot IDs, and do not claim production access or actual test execution.

## Verification gates and limits

1. `python AI_Vision_Training\day06_support\scripts\build_day06_notebooks.py` — five notebooks rebuilt from current manuscripts.
2. `python AI_Vision_Training\day06_support\scripts\export_day06_pdf.py` — revised PDF rebuilt, with 25 images and official-source appendix.
3. `python -m pytest AI_Vision_Training\day06_support\tests\test_day06_contracts.py -q` — **11 passed**: notebook schema/no code, lesson and relative image links, 25 SVGs and bilingual text, syllabus minutes, prompts, snapshot, arithmetic, PDF chapter order and figures, migration scope.
4. Local Markdown-link audit of the active Day 6 materials and historical report found no broken local links. PDF text was checked for five ordered chapter headings, Japanese PVC terminology and the price-source section; selected pages of the 60-page PDF were rasterized for visual inspection, including the pricing table and the final citations.
5. The pre-edit SHA-256 baseline contained 368 tracked files: 38 former Day 6 files in the migration and **330 protected files outside Day 6**. All 330 protected file hashes still match byte-for-byte; Week 1 discovery/export code was untouched. The legacy Day 6 directory no longer exists.

**Remaining limitations:** No beginner timing pilot, native-speaker editorial pass, live-agent execution, live-provider purchase or external pricing guarantee was performed. The source URLs and rates are a dated snapshot. This revision was not pushed or committed.
