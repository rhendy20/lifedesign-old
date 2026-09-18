# Prompt architecture changelog

Each generation lists what changed, why, and what it did to the score. Scores are filled in by the harness
(`eval/results/summary.md`) and copied here at each phase boundary. v0 is the control and is never deleted.

## v0 — naive baseline (control)
One prompt, one experience in, four categories out. No evidence requirement, no critic, no synthesis.
Score (Sonnet 5, 10 personas, blind Opus judge): depth≥3 **22%**, mean depth 1.91, hit recall 72%, hit share 26%, FP 7%, grounded 0%, $0.018/exp.

## v1 — five-stage pipeline
- Extraction separates facts from meaning (interpretation here is a bug).
- Interpretation proposes candidates with verbatim quotes + line refs, and a "would_predict" field.
- Critic deletes generic / restated / flattering / unfalsifiable / ungrounded / therapy-vocab claims; stranger test.
- Synthesis across all experiences: recurrence, contradiction, unnamed constants; two-experience minimum for cross claims.
- Delivery: headline + evidence chain + confidence note.
Why: the v0 failure catalogue predicts these failure classes; each stage exists to remove one of them.
Score effect vs v0: depth≥3 **72%** (+50 pts), mean depth 2.68, hit recall 62% (−10: fewer insights, 7.5 vs 26.6 per persona), hit share 51% (+25), FP 1% (−6), grounded 68%, $0.145/exp (8x).
