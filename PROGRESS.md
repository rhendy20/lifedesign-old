# PROGRESS.md

Phase-boundary log. What shipped, what the score was, what changed.

## Pre-flight (2026-09-18)

- Surveyed repo, upload mount, Google Drive. **None of the eight brief inputs are present.** See `OPEN-QUESTIONS.md` Q1–Q5.
- Verified the local `claude` CLI can serve as an authenticated backend for all four tiers (Fable 5.1, Opus 5, Sonnet 5, Haiku 4.5) in an isolated session with a replaced system prompt and no tools.
- Decision: run the full method on synthetic personas; leave the prototype ready for Robert's corpus; report the primary question as unanswered.

## Phase 1 boundary — baseline and personas (2026-09-18 16:20 UTC)

**Shipped**
- 10 synthetic personas (47 experiences, ~35k words) generated in a separate context with hidden ground truth (known / latent / decoys / domain predictions). Cost $3.23.
- v0 naive baseline run on all personas (Sonnet 5, thinking off). Frozen.
- v1 five-stage pipeline run on all personas (Sonnet 5, thinking off). Frozen. Three personas needed a rerun after a JSON escape bug (`\'`) in model output; parser hardened with sanitiser + cheap repair call.
- Blind pooled judging (Opus 5) of v0 + v1 across all 10 personas. Score set `bb1796b8`.

**Score (10 personas, 341 insights judged)**

| condition | insights | depth≥3 | mean depth | hit recall | hit share | FP | grounded | $/exp | model-s/exp |
|---|---|---|---|---|---|---|---|---|---|
| v0 | 266 | 22% | 1.91 | 72% | 26% | 7% | 0% | 0.018 | 12 |
| v1 | 75 | 72% | 2.68 | 62% | 51% | 1% | 68% | 0.145 | 67 |

**Read**: the pipeline more than triples depth rate and removes false positives, but v0's shotgun (26 insights/persona) still recovers more of the planted truths in raw recall. Hit *share* (how often an insight is a hit) doubles under v1. Grounding at 68% means a third of v1's quotes were not verbatim when grounding was only prompted; v2 gates this in code.

**Fixed along the way**: extended thinking was on by default in the CLI (10x cost/latency) → off for engine stages, capped budget for judge; per-persona cost was inflated by parallel runs → per-call sinks; predictions were dropped before the judge saw them → carried through.

**Spend so far**: $18.59 of the $75 ceiling.

## Phase 2 checkpoint — v2 (2026-09-18 17:05 UTC)

**Shipped**: v2 (form layer, narrator-frame rule, twelve-test critic from the v0 catalogue, code-enforced grounding). Pooled blind re-score of v0 + v1 + v2, score set `5b4b1cb0`. Judge consistency check: v0 and v1 re-scored within 3 points of the first set.

| condition | insights | depth≥3 | mean | depth-4s | hit recall | hit share | FP | grounded | $/exp |
|---|---|---|---|---|---|---|---|---|---|
| v0 | 266 | 24% | 1.91 | 0 | 74% | 25% | 5% | 0% | 0.018 |
| v1 | 75 | 75% | 2.76 | 3 | 58% | 52% | 0% | 68% | 0.145 |
| v2 | 90 | 79% | 2.87 | 12 | 52% | 38% | 4% | 100% | 0.185 |

**Read**: depth rate v1→v2 is +4, inside judge noise, so the plateau rule is close to firing. The gain is in depth-4s (predictions) and grounding; the loss is hit share and a return of false positives, all from standalone form/absence claims with unverified universals. v3 targets exactly that and is the last generation regardless of result.

**Spend**: $33.55 of $75.

## Phase 2 boundary — architecture frozen (2026-09-18 17:55 UTC)

**Shipped**: v3 (mechanism-first synthesis, form/absence demoted to evidence, cross-experience critic). Pooled blind re-score of all four generations, score set `50d0a4d5` (10 personas, 511 insights judged).

| condition | insights | depth≥3 | mean | depth-4s | hit recall | hit share | FP | grounded | $/exp | model-s/exp |
|---|---|---|---|---|---|---|---|---|---|---|
| v0 | 266 | 22% | 1.92 | 0 | 74% | 27% | 5% | 0% | 0.018 | 12 |
| v1 | 75 | 76% | 2.80 | 4 | 60% | 52% | 0% | 68% | 0.145 | 67 |
| v2 | 90 | 77% | 2.86 | 12 | 58% | 44% | 2% | 100% | 0.185 | 97 |
| v3 | 80 | 76% | 2.84 | 7 | 58% | 46% | 2% | 100% | 0.216 | 121 |

**Stop rule fired**: depth rate plateaued across three consecutive generations (76 / 77 / 76). Iteration stops; evaluation begins.

**Frozen for the tier comparison: v3.** v2 and v3 are indistinguishable on every judged metric; v3 is the latest generation with 100% grounding and the full stage set, and the Haiku run of it was already underway. v2 is the cost-efficient equivalent (17% cheaper) and is noted as such in DECISION.md.

**Spend**: $48.18 of the raised $100 ceiling (see OPEN-QUESTIONS Q12).
