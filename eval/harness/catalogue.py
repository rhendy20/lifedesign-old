"""Catalogue the failure modes of a condition (by default v0) using judge scores + the outputs.

    python3 eval/harness/catalogue.py --condition v0__mid --tag <score-set-tag>

Writes eval/results/failure_catalogue_<condition>.md: each failure mode with counts and verbatim examples.
The list of modes is the brief's expected set plus whatever else the judge notes reveal. The catalogue becomes
the critic's checklist in v2.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "prototype"))
from engine.llm import LLM  # noqa: E402

OUT = ROOT / "eval/results/outputs"
SCORES = ROOT / "eval/results/scores"

SYSTEM = """You are auditing the output of a naive insight generator. You get its insights about several people, each with a blind judge's depth
score (0-4), false-positive flag and note. Produce a failure catalogue in markdown:
- One section per failure mode. Start with these expected modes and add any others the data shows:
  restating the user's own words as insight; generic claims true of most people; therapy vocabulary substituting for specificity;
  flattery; claims that could never be wrong (unfalsifiable); confident claims unsupported by the text; hedged non-claims.
- For each mode: a one-line definition, an estimated share of insights showing it, and 2-3 verbatim example headlines with the persona id.
- End with a "Critic checklist" section: 8-12 imperative one-line tests a critic stage should apply to delete such claims.
Be concrete. Quote exactly."""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", default="v0__mid")
    ap.add_argument("--tag", required=True)
    ap.add_argument("--judge", default="opus")
    args = ap.parse_args()
    items = []
    for sf in sorted(SCORES.glob(f"*__{args.tag}.json")):
        d = json.loads(sf.read_text())
        pid = d["persona"]
        outs = json.loads((OUT / args.condition / f"{pid}.json").read_text())
        ins = {i["id"]: i for i in outs["insights"]}
        for s in d["scores"]:
            if s.get("condition") == args.condition and s.get("insight_id") in ins:
                i = ins[s["insight_id"]]
                items.append({"persona": pid, "headline": i["headline"], "explanation": i["explanation"],
                              "depth": s["depth"], "false_positive": s["false_positive"], "note": s.get("note", "")})
    if not items:
        sys.exit("no scored items for that condition/tag")
    llm = LLM(ledger_path=ROOT / "eval/results/ledger.jsonl", ceiling_usd=100.0)
    res = llm.complete(args.judge, SYSTEM, json.dumps(items, indent=1, ensure_ascii=False), max_tokens=8000, tag="catalogue", thinking=4000)
    target = ROOT / f"eval/results/failure_catalogue_{args.condition}.md"
    hdr = f"# Failure catalogue — {args.condition}\n\n{len(items)} scored insights across {len({i['persona'] for i in items})} personas. " \
          f"Depth distribution: " + ", ".join(f"{k}: {sum(1 for i in items if i['depth']==k)}" for k in range(5)) + \
          f". False positives: {sum(1 for i in items if i['false_positive'])}.\n\n"
    target.write_text(hdr + res.text.strip() + "\n")
    print(target)


if __name__ == "__main__":
    main()
