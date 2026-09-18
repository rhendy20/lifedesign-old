# OPEN-QUESTIONS.md

Questions the run could not resolve, with the assumption made so the run could continue.
Written in the order they arose. Nothing here was asked; every item was decided and logged.

## Q1. None of the eight inputs were supplied. Stop, or proceed on what can be built?

**Found at start:** the repo, the upload mount (`/mnt/user-data`), and Google Drive contain none of:
transcripts (input 1), the 26-subsection framework (2), the approved Defining Experiences spec/copy (3),
sealed files A/B/C (4–6), an external read (7), or run constraints and API keys (8).
`/eval/sealed/` did not exist. The API returns 401 without a key.

**Assumption:** proceed with the parts that do not depend on Robert's data, and say plainly in every
deliverable that the primary question (does the engine surface something Robert suspected but never
articulated) is **not answered** by this run. The secondary questions (does the pipeline beat the naive
baseline; does a cheap tier hold up) can be answered on synthetic personas and are worth answering
because they decide what a real run should look like. The reversible path is to build and measure;
the irreversible path is to invent Robert's data, which was not taken.

## Q2. Should Robert's existing Drive writings stand in for the transcripts?

Drive holds reflective material in his voice (course decks with his journey, a pitch transcript telling
his father's story, 2026 planning and health documents, and private personal documents).

**Decision: no.** The brief specifies raw, unedited audio transcripts of defining experiences that he
chooses. Pulling personal documents he did not assemble for this purpose into prompts oversteps the
request, and without sealed files there would be nothing to score them against anyway. Fork noted.

## Q3. No API key. How does the engine call a model?

**Assumption:** the local `claude` CLI is authenticated in this environment and supports
`claude -p --model ... --system-prompt ... --tools ""` in an isolated session. The engine uses the
Anthropic SDK when `ANTHROPIC_API_KEY` is set and falls back to the CLI otherwise. For a non-technical
user with Claude Code installed this is arguably the better default: no key to manage.

Consequences: cost figures are the CLI's list-price estimate (`total_cost_usd`), which includes a small
auxiliary Haiku call the CLI makes per invocation. Latency includes CLI start-up (~1–2 s). Both are
reported as measured and labelled.

## Q4. No credit ceiling was given.

**Assumption:** a self-imposed ceiling of USD 75 (CLI list-price basis) for the whole run, tracked in
`eval/results/ledger.jsonl`. Fable is used only for the final tier comparison, not for development.

## Q5. The six pillars and 26 subsections were not supplied.

**Assumption:** reconstructed from Robert's own Drive documents (2024 "Vision Requirements":
Foundation = Design your purpose + Design yourself; four pillars = work, relationships, health and
wellness, personal growth; "Personal Vision" doc for subsection candidates) and the repo's `context.md`.
Every pillar and subsection in `prompts/framework.json` is marked `"provenance": "GUESSED"` with the
source it was inferred from. No category was invented or renamed; the four insight categories are
exactly as the brief names them. Robert should replace `framework.json` with the real one before his
run; the engine reads it at start-up.

## Q6. How is "the user already knew it" (rubric score 2) scored for synthetic personas?

**Assumption:** each persona is generated with a hidden `ground_truth.json` written by the persona
author in a context that never sees the engine prompts: `known_self` (things the narrator states or
would readily say), `latent_self` (true patterns the author planted but the narrator never names),
and `decoys` (plausible-sounding claims that are false for this person). These play the role of sealed
files A and B, and the decoys give the false-positive check a floor. The judge sees ground truth; the
engine never does.

## Q7. Who judges?

**Assumption:** a fixed judge model (Opus 5) scores every output with generation and tier labels
stripped and the order shuffled. Where the engine tier equals the judge tier, this is noted as a
limitation. Verbatim-quote grounding is checked programmatically, not by a model.

## Q8. Audio input cannot be tested here.

No `ffmpeg` or transcription key is available. The prototype accepts `.txt`/`.md`/`.json`, and will send
audio files to the same OpenAI transcription endpoint the existing API uses if `OPENAI_API_KEY` is set.
That path is implemented but unverified.

## Q9. Extended thinking: on or off for the engine?

The CLI enables extended thinking by default; a Haiku extraction call produced 12k output tokens (10.7k thinking) in 119 s for 6 cents,
versus 1.3k tokens in 11 s for 1 cent with thinking off, with identical valid JSON.
**Assumption:** engine stages run with thinking off, so the prompt architecture is the variable under test and tier cost/latency
comparisons are clean. The judge runs with a 6k budget. A thinking-on variant is a candidate for v3 only if budget remains after
the tier comparison; it would need to be reported as a separate condition, not folded into an architecture generation.

## Q10. The judge did not see `would_predict` for v0/v1 in score set bb1796b8.

The normaliser dropped the prediction field, so no insight in that set could earn depth 4 on prediction grounds (0 fours were given).
**Fix:** field carried through from now on; v1 frozen outputs amended (prediction copied from the raw delivery stage, nothing else
changed, noted in FROZEN.json). The final comparison re-scores v0, v1 and later generations together in one pooled set, so the
earlier set is treated as a development readout, not the headline number.

## Q11. Should v1 count as "beating v0" when its raw recall is lower?

v1 finds 62% of planted truths against v0's 72%, but with 7.5 insights per persona against 26.6. Per insight, v1 is twice as likely
to be a hit and seven times less likely to be a false positive. **Assumption:** depth rate is the primary architecture metric as the
brief specifies; recall is reported alongside insights-per-persona so the volume effect is visible, and v2 raises the target count
to 8-12 to test whether recall recovers without FP rising.
