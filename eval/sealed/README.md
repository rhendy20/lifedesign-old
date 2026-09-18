# /eval/sealed — Robert's sealed files

Put these three files here **before** running the engine on your own transcripts, and do not open them
again until every engine output is frozen (the harness writes `FROZEN.json` with hashes and timestamps).

| File | Contents | How it is scored |
|---|---|---|
| `A-known-self.md` | 10 things you already know about yourself | An insight matching one of these scores **2**, not 3. No credit. |
| `B-suspected-self.md` | 3–5 things you suspect but have never said out loud | Matches here are the **primary score** (hit rate). |
| `C-decision-rule.md` | What you will conclude if the result is uncanny / true-but-known / shallow. Written before you see output. | Read after scoring; it decides what the numbers mean. |

Rules the engine and harness follow:
- Nothing in this folder is ever passed into a prompt. The engine reads only your experience files.
- The judge sees these files only after `FROZEN.json` exists for the condition being scored.
- This run (2026-09-18) had **no** sealed files and **no** transcripts; the equivalent role was played by
  each synthetic persona's hidden `ground_truth.json`. See `FINDINGS.md`.

Optional: `D-external-read.md`, a 10-line read on your patterns from your wife or one trusted person.
Strongest available ground truth; scored the same way as B.
