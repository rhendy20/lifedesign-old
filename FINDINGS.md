# FINDINGS — Defining Experiences insight engine

_Run date 2026-09-18. Engine, prompts, harness and every scored output are in this repo. Numbers below come from `eval/results/summary.md` and the score files in `eval/results/scores/`._

## The question

**Does AI pattern recognition across defining experiences produce insight deep enough that the user recognises something true about himself he had not articulated?**

## The answer, in one paragraph

**Not answered for Robert. Answered, with caveats, for the method.** None of the brief's inputs existed when the run started: no transcripts, no sealed files A/B/C, no 26-subsection framework, no approved copy, no API key (see `OPEN-QUESTIONS.md` Q1–Q5). The primary measure, hits against Robert's sealed "suspected self" list, therefore has no value in this report. What the run could do, and did, was build the engine, then test it on ten synthetic people whose authors planted hidden truths in a separate context, and measure whether a staged architecture beats a naive prompt at surfacing those truths without guessing. On that proxy the answer is: **the staged architecture roughly triples the share of deep insights over a naive prompt (22% → 76%) and removes almost all false positives (5% → 2%), but the gain plateaued after one generation, single-run recall of the planted truths stayed near 58%, and the deepest class of truth (patterns in *how* a person tells, not what they tell) was never reliably reached; attempts to reach it produced the remaining false positives.**

## What was built

- A five-stage pipeline (extraction → interpretation → adversarial critic → cross-experience synthesis → delivery), three generations deep (v1–v3), plus a naive one-prompt control (v0). From v2 on, every quoted span is verified verbatim against the transcript in code; from v3 on, a second critic checks cross-experience claims against the whole corpus.
- A one-command prototype (`python3 prototype/run.py my_experiences/`) that runs on either an API key or a logged-in Claude Code install.
- An eval harness: ten personas (47 experiences) with author-hidden ground truth playing the role of sealed files A and B plus planted decoys; a blind pooled judge (Opus 5, labels stripped, all systems shuffled together per persona); a depth rubric; cost and latency ledger.

## Method notes that affect how to read the numbers

- **Synthetic, not Robert.** Ground truth is what a persona's author planted, judged by a model. A "hit" means the engine captured a pattern the author deliberately hid and the narrator never named. This is a fair proxy for "suspected but never articulated", but it is a proxy.
- **Judge = Claude judging Claude.** Mitigated by pooled blind scoring (the judge cannot tell which system produced an insight), objective matching against written ground truth, programmatic quote grounding, and a consistency check: v0 and v1 re-scored in a second pooled set landed within 3 points of the first.
- **Engine ran with extended thinking off** so prompts, not thinking budget, are the variable. Cost is the CLI's list-price estimate and includes about a cent of CLI overhead per call.

## Results

### 1. Architecture vs baseline (Sonnet 5, ten personas, 47 experiences, blind pooled judge, score set `50d0a4d5`)

| condition | insights | depth≥3 | mean depth | depth-4s | hit recall | hit share | FP rate | grounded | $/exp | model-s/exp |
|---|---|---|---|---|---|---|---|---|---|---|
| v0 naive prompt | 266 | **22%** | 1.92 | 0 | 74% | 27% | 5% | 0% | 0.018 | 12 |
| v1 five stages | 75 | **76%** | 2.80 | 4 | 60% | 52% | 0% | 68% | 0.145 | 67 |
| v2 + form layer, 12-test critic, code grounding | 90 | **77%** | 2.86 | 12 | 58% | 44% | 2% | 100% | 0.185 | 97 |
| v3 + mechanism synthesis, cross-critic | 80 | **76%** | 2.84 | 7 | 58% | 46% | 2% | 100% | 0.216 | 121 |

- **Depth rate**: the architecture beats the baseline by 54 points. All of that gain arrives in v1; v2 and v3 are within judge noise (v0 and v1 re-scored across three separate pooled sets moved by at most 3 points). The brief's plateau rule fired and iteration stopped.
- **Hit rate**: read the two columns together. v0 recovers more planted truths in total (74%) because it fires 26.6 insights per persona; only one in four of them is a hit and a third are generic or restated. v1–v3 fire 7.5–9 per persona and roughly half are hits. Per insight, the pipeline is twice as likely to be right about something hidden. Across all four generations together, 92% of planted truths were found by at least one; no single generation exceeds 60%.
- **False-positive rate**: 5% → 0–2%. The pipeline's confident claims are almost never contradicted by the persona's known self or the planted decoys.
- **Grounding**: prompting for verbatim quotes gave 68%; checking them in code gave 100%. The brief's hard rule "no insight without a cited source line" is not achievable by prompt alone.
- **Depth 4** (predicts behaviour in an undiscussed pillar): zero for v0, 4–12 for the pipeline, and only once predictions were made explicit and pillar-named (v2). The judge confirmed several against the personas' hidden domain facts (see `INSIGHTS.md` #1–#4).

### 2. Where the depth comes from (v2 insight kinds, judged)

| kind | n | depth≥3 | hit share | FP |
|---|---|---|---|---|
| recurrence (same mechanism across experiences) | 39 | 87% | 46% | 0% |
| stated vs lived | 10 | 70% | 50% | 0% |
| compounding (visible only with the last experience) | 12 | 67% | 50% | 8% |
| form (precision asymmetry, agency grammar) | 13 | 69% | 31% | 8% |
| absence (what is never said) | 13 | 77% | 8% | 15% |

Cross-experience recurrence is the engine. Form and absence claims read as deep but rarely matched what the author planted and produced every false positive, each through an unverified universal ("every woman in his life…", "never names a want") or a manufactured axis. v3 demoted them to evidence and added a corpus-level critic; false positives did not fall further (2 remained, both over-tightened boundary conditions on otherwise correct patterns).

### 3. Generalisation (Phase 3)

| archetype | v0 depth / hit / FP | v3 depth / hit / FP |
|---|---|---|
| mundane (no dramatic turning points) | 28% / 16% / 4% | 71% / 43% / 0% |
| highly self-aware (names her own patterns) | 25% / 25% / 7% | 86% / 29% / 0% |
| cliché narrator | 29% / 32% / 0% | 100% / 57% / 0% |
| withholder (short, flat) | 15% / 31% / 12% | 86% / 57% / 0% |
| different life shape (Lagos 24, Osaka 71, São Paulo 44) | 23% / 35% / 4% | 77% / 42% / 0% |
| stated-vs-lived contradiction | 10% / 10% / 10% | 67% / 33% / 0% |
| young, thin corpus (19, four short stories) | 11% / 42% / 5% | 50% / 75% / 12% |
| **near-founder control** (life shape close to Robert's) | 31% / 19% / 4% | 78% / 44% / 11% |

- **No overfit to the founder shape.** The near-founder control scores the same as the other nine on depth (78% vs 76%) and hit share (44% vs 46%) in v3. The framework reconstruction from Robert's documents did not tilt the engine toward his kind of life.
- Every adversarial case improved. The cliché narrator and the withholder, the two the brief expected to be hardest, ended among the best: the engine reads what is skipped and finds the person under the vocabulary. The hardest cases were the thin corpus (four short stories: depth 50%, one FP) and the stated-vs-lived contradiction (67%): with little material, the engine over-tightens; with a self-consistent cover story, it too often adopts it.
- The self-aware persona shows the ceiling: 86% deep by rubric but only 29% hits, because most of what is "deep" about someone who already names her patterns is what she says; the unnamed truths underneath (withdrawing at the moment of being *described*) were found once across all generations.

### 4. Tier comparison (Phase 4)

PENDING_TIERS


## Disconfirming evidence

This section exists so the encouraging numbers above cannot be read alone.

1. **The gain stopped after one generation.** Three architecture generations moved depth rate 76 → 77 → 76. Everything the pipeline adds over a naive prompt is captured by the first staged version; two further rounds of targeted prompt work, driven by the judge's own diagnosis of the failures, changed nothing the judge could detect. Prompt architecture is not a compounding lever here.
2. **The deepest truths were not reached.** Four of fifty planted truths were never surfaced by any generation. All four are form-level: a man who erases himself as the grammatical subject of his own life; a woman whose grief is bodily for two women and logistical for her husband; a man who has never had a personal conversation with a male friend; a man who keeps one-way proximity to people he has left. These are the truths a wife or a lifelong friend would name. When v2 was told to look for exactly this class, it produced every one of its false positives ("every woman…", "never names a want") and the judge caught it against the transcripts. The engine currently cannot tell a real form pattern from a manufactured one.
3. **"Deep" by rubric is not the same as "hit".** Across v1–v3, roughly half the insights the judge scored 3 or higher were not matched to any planted truth. Some are real patterns the author did not plant; some are well-evidenced re-descriptions the judge let through. There is no way to separate the two without a human reading, and a human reading is exactly what this run lacked.
4. **The modal failure of the best generation is still restatement.** Eighteen of v3's eighty insights scored 2, and the judge's note on almost every one is a variant of "restates his own stated calculus", "known territory with a mild reframe", "she says this herself". The critic deletes the obvious restatements; it does not catch the well-dressed ones, where the speaker's own explanation is returned in the engine's voice with two quotes attached.
5. **Recall is bought with volume, not depth.** The baseline's 74% recall against the pipeline's 58% is the number a demo would hide. A user who wants to be sure the engine saw everything would be better served by 26 mediocre insights than 8 sharp ones. The pipeline deliberately trades coverage for precision; whether that is the right trade for a first-session "aha" is Robert's call, not the engine's.
6. **Everything here is synthetic and machine-judged.** The personas were written by Opus 5, the engine ran on Sonnet 5, the judge was Opus 5. All three share priors about what a "hidden pattern" looks like. A real transcript from a real person, scored by that person against a list they wrote in advance, could come out anywhere. That test is still the only one that answers the brief's question, and it has not been run.

## What this does not show

- It does not show that Robert will recognise something true about himself he had not articulated. Nothing about Robert was processed.
- It does not show the engine works on audio, or on transcripts longer or messier than 900 words; the corpus was model-written prose in a spoken register.
- It does not show the framework is right: the six pillars and 26 subsections are a reconstruction from Robert's 2024 documents, marked GUESSED, and only used to name prediction domains.
- It does not separate "judge error" from "engine error" in the roughly half of deep-by-rubric insights that matched no planted truth.
- Cost figures are the CLI's list-price estimate through an authenticated Claude Code install, including about a cent of CLI overhead per call; API pricing would differ.
