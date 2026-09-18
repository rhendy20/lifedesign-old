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

## v2 — form layer, narrator-frame rule, twelve-test critic, code-enforced grounding
Driven by the v0 failure catalogue (`eval/results/failure_catalogue_v0__mid.md`) and the judge's notes on v1's depth-2 insights,
which almost all "adopt the narrator's own explanation as the finding", and on the truths v1 missed, which were mostly about
form (what gets exact numbers vs vagueness, who is the grammatical subject, what is absent) rather than content.
- Extraction adds a form layer: narrator_explanations, precision_asymmetry, agency_grammar, specificity_shift, absences.
- Interpretation: narrator explanations are evidence, never the insight; test each motive against a less flattering alternative; every candidate carries a falsifier and a pillar-named prediction; form/absence/asymmetry candidates are first-class.
- Grounding gate in code: candidates whose quotes are not verbatim are dropped before the critic (v1 only prompted for this; 32% of its quotes failed).
- Critic: the catalogue's 12-test checklist (own-thesis, swap, strip-the-label, falsifier, two-instances, detail-check, praise, narrator-motive, hedge, tension, dedupe, no-prescription).
- Synthesis: five lenses (recurrence, stated-vs-lived, form across stories, absences, compounding); 8-12 insights to recover some of v0's volume-driven recall; no uncovered absolutes.
- Delivery: names the narrator's framing where it differs; states falsifier and prediction.
Score effect (pooled re-score, set 5b4b1cb0, v0=24% / v1=75%): depth≥3 **79%** (+4 vs v1, within judge noise), mean depth 2.87 (+0.11), depth-4 count 12 vs 3, grounded **100%** (+32), hit recall 52% (−6), hit share 38% (−14), FP 4% (+4), $0.185/exp (+28%). Read: the form layer earns depth-4s and full grounding but its standalone form/absence claims match the planted truths less often and let a few unsupported claims through; synthesis has no critic after it.
