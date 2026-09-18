# FINDINGS — Defining Experiences insight engine

_Run date 2026-09-18. Engine, prompts, harness and every scored output are in this repo. Numbers below come from `eval/results/summary.md` and the score files in `eval/results/scores/`._

## The question

**Does AI pattern recognition across defining experiences produce insight deep enough that the user recognises something true about himself he had not articulated?**

## The answer, in one paragraph

**Not answered for Robert. Answered, with caveats, for the method.** None of the brief's inputs existed when the run started: no transcripts, no sealed files A/B/C, no 26-subsection framework, no approved copy, no API key (see `OPEN-QUESTIONS.md` Q1–Q5). The primary measure, hits against Robert's sealed "suspected self" list, therefore has no value in this report. What the run could do, and did, was build the engine, then test it on ten synthetic people whose authors planted hidden truths in a separate context, and measure whether a staged architecture beats a naive prompt at surfacing those truths without guessing. PENDING_SUMMARY_SENTENCE

## What was built

- A five-stage pipeline (extraction → interpretation → adversarial critic → cross-experience synthesis → delivery), three generations deep (v1–v3), plus a naive one-prompt control (v0). From v2 on, every quoted span is verified verbatim against the transcript in code; from v3 on, a second critic checks cross-experience claims against the whole corpus.
- A one-command prototype (`python3 prototype/run.py my_experiences/`) that runs on either an API key or a logged-in Claude Code install.
- An eval harness: ten personas (47 experiences) with author-hidden ground truth playing the role of sealed files A and B plus planted decoys; a blind pooled judge (Opus 5, labels stripped, all systems shuffled together per persona); a depth rubric; cost and latency ledger.

## Method notes that affect how to read the numbers

- **Synthetic, not Robert.** Ground truth is what a persona's author planted, judged by a model. A "hit" means the engine captured a pattern the author deliberately hid and the narrator never named. This is a fair proxy for "suspected but never articulated", but it is a proxy.
- **Judge = Claude judging Claude.** Mitigated by pooled blind scoring (the judge cannot tell which system produced an insight), objective matching against written ground truth, programmatic quote grounding, and a consistency check: v0 and v1 re-scored in a second pooled set landed within 3 points of the first.
- **Engine ran with extended thinking off** so prompts, not thinking budget, are the variable. Cost is the CLI's list-price estimate and includes about a cent of CLI overhead per call.

PENDING_RESULTS

## Disconfirming evidence

PENDING_DISCONFIRMING

## What this does not show

PENDING_LIMITS
