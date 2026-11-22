# Day 6 pre-revision audit / 第6日改訂前の監査

**Recorded before migration or lesson edits: 2026-11-22.** Current branch `main`, HEAD `439f07fc54316d92887f3e8b0bddc6d8db3a0918`; clean worktree. Local `main` contains one Day 6 commit beyond `origin/main` and the remote's advertised `main` (`3443340e98b958d3d5245c6e8ed3f8eb5f17a8cf`). Do not pull or reset. All 330 tracked files outside `AI_Vision_Training/week2/day06/` were hashed to a session-local baseline before editing. The 38 tracked Day 6 files are valuable existing work, not disposable drafts.

## Existing materials and confirmed findings

| Notebook in `week2/day06/lessons/` | Markdown/code cells | Objectives and existing topics | Figures / activities | Duration | Missing for revised curriculum |
|---|---:|---|---|---:|---|
| `Day06_01_LLM_Agent_Harness.ipynb` | 7 / 0 | LLM vs vision AI, assistant/agent/harness, permissions, misconceptions | 4 figures; classification, comparison and risk questions | 70 min | Tokens, context window, substantial provider/model discussion, explicit capability distinctions |
| `Day06_02_Ideas_and_Requirements.ipynb` | 8 / 0 | Problem, ChatGPT brainstorming, local PVC record spec, MVP, simulated clarification | 4 figures; problem/feature/input/output exercises | 95 min | Cause vs outcome, secondary manufacturing case, fuller UI and requirement examples |
| `Day06_03_Prompting_and_Agents.ipynb` | 8 / 0 | Request stages, plan-only prompt, approval, feedback, handover | 5 figure placements; prompt, plan and correction exercises | 80 min | Three complete failure/correction demonstrations, expanded end-to-end supervision |
| `Day06_04_Testing_and_Handover.ipynb` | 8 / 0 | Acceptance, regression, safety, Git and handover | 3 figure placements; acceptance/safety/handover exercises | 55 min | API, token billing, subscriptions, provider pricing, agent-cost scenarios |

All four have paired Japanese and English explanations and no executable cells. Their `.md` files are source manuscripts; `scripts/build_day06_notebooks.py` generates the `.ipynb` files. Relative image references and existing tests pass (10 passed before revision). The standalone `scripts/export_day06_pdf.py` uses ReportLab, Pillow and a locally installed Chrome/Edge via Playwright. Its 22-page A4 PDF currently lives in `week2/day06/pdf/`. Week 1 discovery explicitly enumerates Days 0–5 in `assets/scripts/course_notebooks.py`; it must remain unchanged.

Existing support: five example documents, six bilingual prompt templates, a bilingual instructor guide and two worksheets, a 14-figure SVG set, an asset manifest, an independent syllabus and an implementation report. The first course provided meaningful beginner-safe examples, so these must be retained or carefully adapted.

## Existing figure inventory

All SVGs currently reside in `week2/day06/assets/diagrams/`. Text counts are an automated warning, not a translation-quality verdict. Several labels contain both languages, but many other important labels contain only one. English captions in notebooks do not substitute for English labels inside a figure. Original SVG rendering and its previous PDF render were inspected during initial implementation; the new PDF needs a fresh visual inspection after changes.

| Figure | Existing lesson / purpose | JP / EN / mixed label counts | Bilingual or semantic concern to check |
|---|---|---:|---|
| D06-01 | 01: Days 1–6 transition | 20 / 23 / 14 | Stage descriptions are partly one-language |
| D06-02 | 01: YOLO, PatchCore, LLM | 23 / 25 / 17 | Check precise input/output labels |
| D06-03 | 01: model, assistant, agent, harness | 12 / 16 / 6 | Definitions and arrows need paired translations |
| D06-04 | 01: permission loop | 22 / 22 / 13 | Model-to-tool action must pass harness permission |
| D06-05 | 02: problem to implementation | 18 / 13 / 10 | Stage labels need two languages |
| D06-06 | 02,03: poor versus good prompt | 15 / 7 / 5 | English scope and acceptance detail missing |
| D06-07 | 02: requirements | 24 / 20 / 13 | Category and example pairs need checking |
| D06-08 | 02: fictional UI | 31 / 33 / 28 | Keep original local-only case fields |
| D06-09 | 03: human, ChatGPT, agent | 15 / 12 / 7 | Explicit human approval before implementation |
| D06-10 | 03: conversation stages | 20 / 13 / 10 | Corrections and branch need paired labels |
| D06-11 | 03: quality gates | 17 / 13 / 6 | Return arrows and approval states |
| D06-12 | 04: testing evidence | 12 / 10 / 4 | Distinguish screenshot and functional evidence |
| D06-13 | 03,04: handover | 19 / 11 / 8 | Individual handover inputs need paired terms |
| D06-14 | 04: safety boundary | 15 / 13 / 7 | Restricted/production labels and warnings |

## Classification and change plan

- **Confirmed defects:** Day 6 is under the historical `week2/day06/` hierarchy rather than the requested notebook-first layout; only four modules and a 22-page PDF; no token/API/pricing lesson or dated pricing source; 6 rather than 8 prompt templates; some diagram labels not independently bilingual.
- **Reported and partly reproduced:** “Too brief for a full day” is supported by ~750–1,035 English whitespace-delimited tokens per notebook plus paired Japanese and 22 PDF pages, but actual pacing needs a beginner pilot. Existing diagrams are not wholesale wrong; they require targeted translation/accuracy improvements and visual rechecking.
- **Educational additions:** Split the existing four lessons into five without losing the continuous PVC example; add a small fictional daily-report example, glossary, worked cost arithmetic, more conversations and three correction scenarios. Keep mandatory learning within 300 minutes; mark deeper material optional.
- **Technical corrections:** Move notebooks, SVGs, materials and independent exporter to the requested hierarchy; update relative paths, output and tests; preserve Week 1 discovery/export behavior; generate numeric pricing only from a dated source with official references, never guessed values.
- **Optional enhancements:** More UI mockups and optional appendix only where they improve comprehension; do not inflate mandatory work with filler.

**G0 baseline complete:** no local modifications at start; branch/remote divergence and protected hashes recorded, existing Day 6 inventory and reuse plan documented. Do not edit or remove original files until the new location and references have been verified.
