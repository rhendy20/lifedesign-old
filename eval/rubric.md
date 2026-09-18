# Depth rubric

Scored per insight, blind (system labels stripped, order shuffled, all systems pooled per persona in one judging call).

| Score | Meaning |
|---|---|
| 0 | Restates what the user already said |
| 1 | Generic — true of most people (or of most people with this age, sex, occupation) |
| 2 | True and specific, but the user already knew it (matches sealed file A / persona `known_self`) |
| 3 | Non-obvious, specific, and traceable to evidence in the corpus |
| 4 | Non-obvious, evidenced, and predicts behaviour in a life domain the user never discussed |

Three numbers decide the question:

1. **Depth rate** — share of insights scoring ≥ 3.
2. **Hit rate** — share of sealed-file-B items (persona `latent_self`) captured by at least one insight (recall), and share of insights that are hits.
3. **False-positive rate** — share of insights that are confident and contradicted by file A / `known_self`, match a planted decoy, or are unsupported by the corpus. A high hit rate with a high false-positive rate is a machine guessing, not seeing.

Also reported, programmatic not judged: **grounding rate** — share of insights whose every cited quote exists verbatim in the cited experience.

Judge: Opus 5 (fixed across all conditions). Limitation: a Claude model judging Claude outputs. Mitigations: pooled blind scoring, objective hit/FP matching against author-written ground truth, programmatic grounding.
