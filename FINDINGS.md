# FINDINGS — Defining Experiences insight engine

_Run dates 2026-09-18 (build, generations) and 2026-09-25 (tier scoring finished after a CLI session limit). Engine, prompts, harness and every scored output are in this repo. Numbers below come from `eval/results/summary.md` and the score files in `eval/results/scores/`._

## The question

**Does AI pattern recognition across defining experiences produce insight deep enough that the user recognises something true about himself he had not articulated?**

## The answer, in one paragraph

**Not answered for Robert. Answered, with caveats, for the method.** None of the brief's inputs existed when the run started: no transcripts, no sealed files A/B/C, no 26-subsection framework, no approved copy, no API key (see `OPEN-QUESTIONS.md` Q1–Q5). The primary measure, hits against Robert's sealed "suspected self" list, therefore has no value in this report. What the run could do, and did, was build the engine, then test it on ten synthetic people whose authors planted hidden truths in a separate context, and measure whether a staged architecture beats a naive prompt at surfacing those truths without guessing. On that proxy the answer is: **a staged pipeline beats a naive prompt by a wide margin in every comparison the judge made (22% → 76% deep in the four-generation pool; false positives 5% → 2%), but prompt work plateaued after one generation. The lever that still moved was the model. On the same frozen pipeline and the same three personas, Fable scored 93% deep with 80% recall of the planted truths and no false positives, against Sonnet's 52% and 33%. It also reached a truth no earlier generation had found. That result rests on three personas and costs about ten times as much per experience. The judge's absolute scale also shifts by up to 28 points depending on what it is compared against, so only within-pool comparisons are trustworthy.**

## What was built

- A five-stage pipeline (extraction → interpretation → adversarial critic → cross-experience synthesis → delivery), three generations deep (v1–v3), plus a naive one-prompt control (v0). From v2 on, every quoted span is verified verbatim against the transcript in code; from v3 on, a second critic checks cross-experience claims against the whole corpus.
- A one-command prototype (`python3 prototype/run.py my_experiences/`) that runs on either an API key or a logged-in Claude Code install.
- An eval harness: ten personas (49 experiences) with author-hidden ground truth playing the role of sealed files A and B plus planted decoys; a blind pooled judge (Opus 5, labels stripped, all systems shuffled together per persona); a depth rubric; cost and latency ledger.

## Method notes that affect how to read the numbers

- **Synthetic, not Robert.** Ground truth is what a persona's author planted, judged by a model. A "hit" means the engine captured a pattern the author deliberately hid and the narrator never named. This is a fair proxy for "suspected but never articulated", but it is a proxy.
- **Judge = Claude judging Claude.** Mitigated by pooled blind scoring (the judge cannot tell which system produced an insight), objective matching against written ground truth, programmatic quote grounding, and repeated scoring. v0 and v1 re-scored in similar pools moved by at most 3 points. **But the judge is pool-relative**: the same frozen v3 outputs scored 77% deep next to v0–v2, 63% next to Haiku, and 52% next to Fable. Rankings inside a pool held every time; absolute percentages across pools are not comparable. Every table below names its pool.
- **Engine ran with extended thinking off** (`MAX_THINKING_TOKENS=0`) so prompts, not thinking budget, are the variable. Fable produced 2.3x Sonnet's output tokens per experience, so the setting may not fully suppress its reasoning; treat Fable-vs-Sonnet as model-plus-possible-reasoning, not model alone. Cost is the CLI's list-price estimate and includes about a cent of CLI overhead per call.

## Results

### 1. Architecture vs baseline (Sonnet 5, ten personas, 49 experiences, blind pooled judge, score set `50d0a4d5`)

| condition | insights | depth≥3 | mean depth | depth-4s | hit recall | hit share | FP rate | grounded | $/exp | model-s/exp |
|---|---|---|---|---|---|---|---|---|---|---|
| v0 naive prompt | 266 | **22%** | 1.92 | 0 | 74% | 27% | 5% | 0% | 0.018 | 12 |
| v1 five stages | 75 | **76%** | 2.80 | 4 | 60% | 52% | 0% | 68% | 0.145 | 67 |
| v2 + form layer, 12-test critic, code grounding | 90 | **77%** | 2.86 | 12 | 58% | 44% | 2% | 100% | 0.185 | 97 |
| v3 + mechanism synthesis, cross-critic | 80 | **76%** | 2.84 | 7 | 58% | 46% | 2% | 100% | 0.216 | 121 |

- **Depth rate**: the architecture beats the baseline by 54 points. All of that gain arrives in v1; v2 and v3 are within judge noise inside the same pool. The brief's plateau rule fired and iteration stopped.
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

The architecture was frozen at v3 and the identical corpus was run through three tiers. Fable was run on three personas only, to stay inside the credit ceiling (`OPEN-QUESTIONS.md` Q12). The three personas span a withholder, a stated-vs-lived contradiction and a sharply different life shape. Scoring was blind, with tier labels stripped and all three tiers pooled per persona.

**Pool A: all three tiers, same three personas (15 experiences), score set `0dcb6f16`**

| tier | insights | depth≥3 | mean depth | hit recall | hit share | FP | grounded | $/exp | wall-s per persona |
|---|---|---|---|---|---|---|---|---|---|
| Fable 5.1 | 29 | **93%** | 3.14 | **80%** (12/15) | 52% | 0% | 100% | 2.01 | 1023 |
| Sonnet 5 (mid) | 25 | 52% | 2.52 | 33% (5/15) | 32% | 0% | 100% | 0.20 | 370 |
| Haiku 4.5 (cheap) | 25 | 44% | 2.36 | 53% (8/15) | 40% | 8% | 100% | 0.14 | 693 |

**Pool B: Sonnet vs Haiku, all ten personas (49 experiences), score set `c7c379d2`**

| tier | insights | depth≥3 | mean depth | hit recall | hit share | FP | grounded | $/exp | wall-s per persona |
|---|---|---|---|---|---|---|---|---|---|
| Sonnet 5 (mid) | 80 | **62%** | 2.60 | 54% | 40% | **4%** | 100% | 0.22 | 389 |
| Haiku 4.5 (cheap) | 82 | 52% | 2.38 | 56% | 39% | **13%** | 96% | 0.15 | 705 |

Tokens per experience, engine calls only: Fable 34k in / 28k out; Sonnet 27k in / 12k out; Haiku 24k in / 18k out.

- **Fable is a different product, not a better Sonnet.** It found 12 of 15 planted truths on the three personas against Sonnet's 5, with no false positives. That includes all five for the Lagos nursing student. For the withholder it found the self-erasure-as-grammar pattern that no Sonnet generation found in 90+ attempts across v0–v3. Its best insights (see `INSIGHTS.md`, Fable section) name the rhyme between two stories told decades apart, "the fly rod is the tractor again thirty-five years later," which is exactly the kind of recognition the brief is asking about.
- **The cheap tier does not change the unit economics.** Through the CLI, Haiku costs only 30% less than Sonnet per experience. It writes more tokens and every call carries a fixed CLI overhead. It is also slower, and its false-positive rate triples (4% → 13%). For a tool whose premise is that the user can trust a claim about themselves, a cheap tier that is wrong one time in eight is not a cheaper version of the same product.
- **Cost basis.** Every dollar figure is the CLI's list-price estimate through a logged-in Claude Code install. Each call includes roughly a cent of CLI overhead and an auxiliary Haiku call. Direct API pricing will be lower for every tier and proportionally much lower for Haiku; the token counts above let anyone recompute.
- **Sample-size warning.** Pool A has three personas and 79 insights. The Fable–Sonnet gap (41 points of depth, 47 points of recall) is large enough to survive that. The Sonnet–Haiku ordering flips on recall between pools (33% vs 53% in A, 54% vs 56% in B), so the only Haiku finding stable across both pools is the higher false-positive rate.



## Disconfirming evidence

This section exists so the encouraging numbers above cannot be read alone.

1. **The gain stopped after one generation.** Three architecture generations moved depth rate 76 → 77 → 76. Everything the pipeline adds over a naive prompt is captured by the first staged version; two further rounds of targeted prompt work, driven by the judge's own diagnosis of the failures, changed nothing the judge could detect. Prompt architecture is not a compounding lever here.
2. **The deepest truths were not reached by prompt work.** Four of fifty planted truths were never surfaced by any Sonnet generation. All four are form-level: a man who erases himself as the grammatical subject of his own life; a woman whose grief is bodily for two women and logistical for her husband; a man who has never had a personal conversation with a male friend; a man who keeps one-way proximity to people he has left. These are the truths a wife or a lifelong friend would name. When v2 was told to look for exactly this class, it produced every one of its false positives ("every woman…", "never names a want") and the judge caught it against the transcripts. On Sonnet, the engine cannot tell a real form pattern from a manufactured one. Fable, on the one of these personas it was run on, found the grammar pattern cleanly. The frontier may be a model capability rather than a prompt one, but that rests on one persona.
3. **"Deep" by rubric is not the same as "hit".** Across v1–v3, roughly half the insights the judge scored 3 or higher were not matched to any planted truth. Some are real patterns the author did not plant; some are well-evidenced re-descriptions the judge let through. There is no way to separate the two without a human reading, and a human reading is exactly what this run lacked.
4. **The modal failure of the best generation is still restatement.** Eighteen of v3's eighty insights scored 2, and the judge's note on almost every one is a variant of "restates his own stated calculus", "known territory with a mild reframe", "she says this herself". The critic deletes the obvious restatements; it does not catch the well-dressed ones, where the speaker's own explanation is returned in the engine's voice with two quotes attached.
5. **Recall is bought with volume, not depth.** The baseline's 74% recall against the pipeline's 58% is the number a demo would hide. A user who wants to be sure the engine saw everything would be better served by 26 mediocre insights than 8 sharp ones. The pipeline deliberately trades coverage for precision; whether that is the right trade for a first-session "aha" is Robert's call, not the engine's.
6. **Everything here is synthetic and machine-judged.** The personas were written by Opus 5, the engine ran on Sonnet 5, the judge was Opus 5. All three share priors about what a "hidden pattern" looks like. A real transcript from a real person, scored by that person against a list they wrote in advance, could come out anywhere. That test is still the only one that answers the brief's question, and it has not been run.
7. **The headline percentages are pool-relative.** The judge scored the same frozen v3 outputs at 77%, 63% and 52% deep depending on what else was in the pool. Every ranking in this report was computed inside one pool and held in every pool it was tested in, but no absolute percentage here means "76% of insights are deep" in any portable sense. Robert's own reading, against his own sealed files, is the only absolute scale that exists.
8. **The Fable result could be the judge preferring its own register.** Fable writes denser, more literary headlines, and Opus 5 may reward that register even blind. The hit-recall number (12/15 vs 5/15) is harder to explain that way, because it is a match against author-written ground truth rather than a style judgement. It is still one judge on three personas.

## What this does not show

- It does not show that Robert will recognise something true about himself he had not articulated. Nothing about Robert was processed.
- It does not show the engine works on audio, or on transcripts longer or messier than 900 words; the corpus was model-written prose in a spoken register.
- It does not show the framework is right: the six pillars and 26 subsections are a reconstruction from Robert's 2024 documents, marked GUESSED, and only used to name prediction domains.
- It does not separate "judge error" from "engine error" in the roughly half of deep-by-rubric insights that matched no planted truth.
- It does not show Fable's advantage holds on the other seven personas, or with thinking verifiably off.
- It does not rule out subtle context contamination from the CLI backend, which showed every engine call the account email and date (OPEN-QUESTIONS Q16). No scored insight contained or referred to it.
- Cost figures are the CLI's list-price estimate through an authenticated Claude Code install, including about a cent of CLI overhead per call; API pricing would differ.
