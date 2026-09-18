"""Blind judge. Scores every insight in the given conditions against the persona's hidden ground truth.

    python3 eval/harness/score.py --conditions v0__mid v1__mid [--judge opus]

For each persona, ALL insights from all listed conditions are pooled, shuffled, given opaque ids and scored
in ONE judge call, so the judge cannot know which system produced what and calibrates across them.
Scores are written to eval/results/scores/<persona>__<hash-of-conditions>.json and merged by report.py.

Depth rubric (from the brief):
  0 restates what the user already said
  1 generic, true of most people
  2 true and specific but already known (matches known_self)
  3 non-obvious, specific, traceable to evidence in the corpus
  4 non-obvious, evidenced, and predicts behaviour in a life domain the user never discussed
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "prototype"))
from engine.corpus import load_corpus  # noqa: E402
from engine.llm import LLM, extract_json  # noqa: E402

PERSONAS = ROOT / "eval/personas"
OUT = ROOT / "eval/results/outputs"
SCORES = ROOT / "eval/results/scores"

JUDGE_SYSTEM = """You are a strict, blind evaluator of personal insights produced by unknown systems about one person.
You see: the person's full transcripts; a hidden ground-truth file written by the person's author (known_self = things they already know and would say;
latent_self = true patterns planted but never named; decoys = plausible claims that are FALSE; domain_predictions = true facts about undiscussed life areas);
and a shuffled pool of insights with opaque ids. You do not know which system produced which insight. Do not try to guess. Score each insight on its own.

For EACH insight give:
- depth (0-4):
  0 = restates what the person already said in the transcripts (same content, little added).
  1 = generic; true of most people, or of most people with this age/sex/occupation.
  2 = true and specific to this person, but matches something in known_self (they already know it).
  3 = non-obvious, specific, and traceable to actual evidence in the transcripts (the cited quotes or other passages genuinely support it).
  4 = meets 3 AND correctly predicts behaviour in a life area the transcripts never discuss (matches or is clearly consistent with domain_predictions or a latent claim's implications).
- hit: index (0-based) of the latent_self claim this insight substantially captures, or null. Be strict: same underlying pattern, not merely same topic.
- known_match: index of the known_self item it matches, or null.
- false_positive: true if the insight is contradicted by known_self, matches a decoy, or makes a confident claim the transcripts do not support. Else false.
- fp_reason: short reason if false_positive, else "".
- note: one line.

Be severe. Fluent, plausible prose is not evidence. A claim the person could not check is not depth 3. Praise is not insight.
Return JSON only: {"scores": [{"id": "...", "depth": 0, "hit": null, "known_match": null, "false_positive": false, "fp_reason": "", "note": ""}]}"""


def load_outputs(conditions, pid):
    pool = []
    for c in conditions:
        f = OUT / c / f"{pid}.json"
        if not f.exists():
            continue
        data = json.loads(f.read_text())
        for ins in data["insights"]:
            pool.append((c, ins))
    return pool


def judge_persona(llm, judge_model, pid, conditions, seed=7):
    pool = load_outputs(conditions, pid)
    if not pool:
        return None
    rnd = random.Random(f"{pid}:{seed}:{','.join(conditions)}")
    rnd.shuffle(pool)
    key = {}
    anon = []
    for k, (cond, ins) in enumerate(pool):
        oid = f"x{k+1:03d}"
        key[oid] = {"condition": cond, "insight_id": ins["id"]}
        anon.append({"id": oid, "category": ins["category"], "headline": ins["headline"],
                     "explanation": ins["explanation"], "confidence": ins.get("confidence", ""),
                     "would_predict": ins.get("would_predict", ""),
                     "evidence": [{"exp": e.get("exp"), "quote": e["quote"]} for e in ins.get("evidence", [])]})
    corpus = load_corpus(PERSONAS / pid / "experiences")
    transcripts = "\n\n".join(f"[E{e.index}] \"{e.title}\"\n{e.text}" for e in corpus)
    gt = json.loads((PERSONAS / pid / "ground_truth.json").read_text())
    user = (f"TRANSCRIPTS:\n{transcripts}\n\nGROUND TRUTH (hidden from the systems):\n{json.dumps(gt, indent=1, ensure_ascii=False)}\n\n"
            f"INSIGHTS TO SCORE ({len(anon)}):\n{json.dumps(anon, indent=1, ensure_ascii=False)}\n\nScore every id. Return JSON only.")
    res = llm.complete(judge_model, JUDGE_SYSTEM, user, max_tokens=16000, tag=f"judge:{pid}", thinking=6000)
    scores = extract_json(res.text)["scores"]
    for s in scores:
        s.update(key.get(s["id"], {}))
    return {"persona": pid, "conditions": conditions, "judge": res.model, "judge_cost_usd": res.cost_usd,
            "n_latent": len(gt.get("latent_self", [])), "scores": scores}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conditions", nargs="+", required=True)
    ap.add_argument("--judge", default="opus")
    ap.add_argument("--personas", nargs="*")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    SCORES.mkdir(parents=True, exist_ok=True)
    llm = LLM(ledger_path=ROOT / "eval/results/ledger.jsonl", ceiling_usd=100.0)
    ids = args.personas or sorted(p.name for p in PERSONAS.iterdir() if (p / "ground_truth.json").exists())
    tag = hashlib.sha1(",".join(sorted(args.conditions)).encode()).hexdigest()[:8]

    from concurrent.futures import ThreadPoolExecutor, as_completed

    def one(pid):
        target = SCORES / f"{pid}__{tag}.json"
        if target.exists():
            return f"{pid}: scored already"
        r = judge_persona(llm, args.judge, pid, args.conditions)
        if r is None:
            return f"{pid}: no outputs"
        target.write_text(json.dumps(r, indent=2, ensure_ascii=False))
        return f"{pid}: {len(r['scores'])} insights scored, judge ${r['judge_cost_usd']:.2f}"

    with ThreadPoolExecutor(args.workers) as ex:
        for f in as_completed([ex.submit(one, p) for p in ids]):
            try:
                print(f.result(), flush=True)
            except Exception as e:  # noqa: BLE001
                print(f"FAILED: {e}", flush=True)
    print(f"score set tag: {tag}; total spent ${llm.spent_usd():.2f}")


if __name__ == "__main__":
    main()
