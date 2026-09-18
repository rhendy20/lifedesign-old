# DECISION — what to build next, what is ruled out

_Companion to `FINDINGS.md`. Written after the scores, before any human read the output._

## The direct answer: is pattern recognition the moat?

**Not on this evidence, not as "AI finds hidden patterns".** A naive prompt already finds most of the planted truths if you let it fire thirty guesses; the platform's job is not to make a model see patterns, which it does, but to make it *stop* saying the obvious, the flattering, the restated and the unfalsifiable, and to stand behind what is left with quotes. That is an engineering-of-restraint problem, and this run shows it is solvable to a point (22% → 76% deep, 5% → 2% false) and then flat. Three generations of prompt work after the first added nothing measurable.

If there is a moat, the run points at three places it could live, none of them "the prompt":

1. **The corpus, compounding.** Every cross-experience insight that scored 4 needed at least two stories and most needed four. A one-session tool gets the 76%; a tool that holds a year of defining experiences, daily captures and outcomes has a corpus no competitor can prompt their way into. This is the moat the founder manifesto already names; the run supports it.
2. **The verification layer.** Code-checked quotes moved grounding from 68% to 100%; a judge with the person's own sealed lists caught false positives a critic prompt could not. A platform that lets the user mark each insight known / new-and-true / wrong, and feeds that back, has a ground-truth signal no general assistant has. That signal is also the only thing that will ever answer the brief's actual question.
3. **The delivery of the question, not the answer.** The insights that moved the judge named a mechanism and then a checkable prediction in a life pillar the person had not discussed. That is a coaching move, not an analysis move, and it is where the approved copy and flow do their work.

## What to build next (in order)

1. **Run this on Robert.** Everything is in place except the inputs. Record 5–7 experiences, drop the transcripts in a folder, write sealed files A/B/C into `/eval/sealed/`, run `python3 prototype/run.py <folder>`, freeze, then open the sealed files and score by hand with `eval/rubric.md`. Optional but strongest: the external read from Jolene. Cost per run on Sonnet: about $1 for six experiences. **Until this is done the core question is open and no further engine work is justified.**
2. **Add the user's verdict as data.** A three-button mark per insight (already knew / true and new / wrong) stored with the insight. This is the ground truth the whole system lacks, and it is cheap.
3. **Second-session synthesis.** The compounding lens (what the last story lets you say that the earlier ones could not) was the most consistently deep kind of insight the pipeline produced. Build the flow so experiences accumulate and synthesis re-runs over the growing corpus, rather than a one-shot onboarding.
4. **Then, and only then, work on the form-level frontier.** The truths no generation reached are about how a person tells: grammatical self-erasure, where precision lives, who is absent. Reaching them without manufacturing patterns needs a verifier that checks a claimed asymmetry against the whole corpus by count, not by prompt. Do this after there is a human ground truth to test it against.

## What is ruled out

- **More prompt generations on synthetic data.** Plateaued. Stop rule fired. Further tuning without Robert's or a real user's ground truth is optimising against a model's opinion of a model.
- **One mega-prompt.** v0 is what that gives: a third of its output generic or restated, no evidence, no grounding.
- **Prompted grounding.** Asking for verbatim quotes gives about two thirds. Check them in code.
- **Standalone "absence" and "form" insights.** Every false positive in v2 came from this class. They are evidence for a mechanism claim or they are not returned.
- **Extended thinking as an engine default.** Ten times the cost and latency for identical JSON on the stage calls; reserve for the judge.
- **Expanding scope before the sealed test.** No capture layer, relationships module, Circle of Trust or Mission Memoirs work belongs before the core question has a number attached to it.

## Cost per experience by tier (frozen v3 architecture, CLI list price incl. overhead)

PENDING_TIER_COSTS

## Decision rule for Robert's run (fill sealed file C before running)

The run cannot decide this for you, but it can tell you what the numbers here imply about each outcome:

- **Uncanny** (two or more hits on file B, no confident claim you know to be false): the synthetic result generalised to you. Build items 2 and 3 above; the moat is the compounding corpus plus your verdicts.
- **True but known** (most insights match file A, none match B): the engine is a mirror with good manners. That is still the restatement failure the judge saw in a quarter of v3's output, and it is what the 76% "deep" figure would mean if the rubric's "non-obvious" is weaker than yours. Build item 2 and run again after ten daily captures; do not ship the Defining Experiences flow as the aha moment.
- **Shallow** (generic, or hits with false positives alongside): the synthetic proxy overstated the method. Stop engine work; the platform's value has to come from structure and follow-through, not insight.
