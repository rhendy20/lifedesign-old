# Prompt architecture changelog

Each generation lists what changed, why, and what it did to the score. Scores are filled in by the harness
(`eval/results/summary.md`) and copied here at each phase boundary. v0 is the control and is never deleted.

## v0 — naive baseline (control)
One prompt, one experience in, four categories out. No evidence requirement, no critic, no synthesis.
Score: see eval/results/summary.md.

## v1 — five-stage pipeline
- Extraction separates facts from meaning (interpretation here is a bug).
- Interpretation proposes candidates with verbatim quotes + line refs, and a "would_predict" field.
- Critic deletes generic / restated / flattering / unfalsifiable / ungrounded / therapy-vocab claims; stranger test.
- Synthesis across all experiences: recurrence, contradiction, unnamed constants; two-experience minimum for cross claims.
- Delivery: headline + evidence chain + confidence note.
Why: the v0 failure catalogue predicts these failure classes; each stage exists to remove one of them.
Score effect: pending.
