# Defining Experiences insight engine — prototype

Takes raw defining-experience transcripts, returns structured insight with an evidence chain per claim.
Ugly on purpose. The only thing under test is whether the insight is deep.

## Run it (one command)

```bash
python3 prototype/run.py path/to/my_experiences/
```

`my_experiences/` holds one file per experience (`.txt` or `.md`; audio if `OPENAI_API_KEY` is set).
Talk for 3–10 minutes per experience, transcribe, drop the raw text in. Do not edit it: filler carries signal.

Needs one of:
- `ANTHROPIC_API_KEY` in the environment, or
- Claude Code installed and logged in (the `claude` command). No key needed then.

Options: `--tier fable|mid|cheap` (default `mid` = Sonnet 5; `fable` scored deepest, at about 10x the cost), `--gen v0|v1|v2|v3` (default latest), `--out folder`.

Output: `insights.md` (read this) and `insights.json` (every stage's raw output, for audit).

## What it does

```
raw experience -> extraction (facts, verbatim) -> interpretation (candidates + quotes)
              -> adversarial critic (deletes generic/restated/flattering/unfalsifiable)
              -> cross-experience synthesis (recurrence, contradiction, unnamed constants)
              -> delivery (headline + evidence chain + confidence)
```

Hard rules enforced in code, not just in prompts: every quote is checked verbatim against the transcript
(`engine/corpus.py::find_quote`); from v2 on, candidates whose quotes are not verbatim are dropped before the critic.

Prompts live in `/prompts/<generation>/`. The framework the engine reasons with is `/prompts/framework.json`
(currently a **reconstruction** marked GUESSED; replace with the real one).

## Layout

| Path | What |
|---|---|
| `run.py` | entry point |
| `engine/llm.py` | model backend (SDK or `claude -p`), cost/latency ledger |
| `engine/corpus.py` | normalise inputs, line numbering, verbatim quote check |
| `engine/prompts.py` | load versioned prompt files |
| `engine/pipeline.py` | the five stages; v0 control path |

## Privacy note on the two backends

- **API key (SDK backend):** sends only the engine's prompts and your transcripts.
- **Claude Code login (CLI backend):** the CLI also attaches your account email, the date and the working directory to every call.
  The engine runs from a neutral empty folder, tells the model this is not about the subject, and redacts email addresses
  from every reply, but the model still sees it. That is fine for your own experiences. Use an API key for anyone else's.

## Verified

2026-09-25: `python3 prototype/run.py eval/personas/p10_freshman/experiences --tier mid` completed in one command.
It returned 7 insights from 4 experiences, all quotes verbatim, no JSON repairs, $0.82 and 5 minutes on the CLI backend.
The audio path is implemented but unverified; no transcription key was available.
