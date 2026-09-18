"""Pull the best insights from one condition, ranked by judge score, with their evidence chains and judge notes.

    python3 eval/harness/best_insights.py --condition v3__mid --tag <score-set> --n 10 > INSIGHTS_body.md

Ranking: depth desc, then hit, then grounded, then confidence. Verbatim headlines; nothing rewritten.
"""
from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "eval/results/outputs"
SCORES = ROOT / "eval/results/scores"
PERSONAS = ROOT / "eval/personas"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--per-persona", type=int, default=2, help="cap per persona so one person does not dominate")
    args = ap.parse_args()
    rows = []
    for sf in sorted(SCORES.glob(f"*__{args.tag}.json")):
        d = json.loads(sf.read_text()); pid = d["persona"]
        outf = OUT / args.condition / f"{pid}.json"
        if not outf.exists():
            continue
        o = json.loads(outf.read_text()); ins = {i["id"]: i for i in o["insights"]}
        gt = json.loads((PERSONAS / pid / "ground_truth.json").read_text())
        persona = json.loads((PERSONAS / pid / "persona.json").read_text())
        titles = {}
        for k, f in enumerate(sorted((PERSONAS / pid / "experiences").glob("*.md")), 1):
            titles[k] = f.read_text().splitlines()[0].lstrip("# ").strip()
        for s in d["scores"]:
            if s.get("condition") != args.condition or s.get("insight_id") not in ins:
                continue
            i = ins[s["insight_id"]]
            conf = {"high": 2, "medium": 1}.get(i.get("confidence", ""), 0)
            rows.append((s["depth"], s.get("hit") is not None, i["grounded"], conf, pid, persona, titles, i, s, gt))
    rows.sort(key=lambda r: (r[0], r[1], r[2], r[3]), reverse=True)
    picked, per = [], {}
    for r in rows:
        if per.get(r[4], 0) >= args.per_persona:
            continue
        picked.append(r); per[r[4]] = per.get(r[4], 0) + 1
        if len(picked) >= args.n:
            break
    for n, (depth, hit, grounded, _, pid, persona, titles, i, s, gt) in enumerate(picked, 1):
        who = f"{persona.get('name','?')}, {persona.get('age','?')}, {persona.get('occupation','?')} ({persona['archetype']})"
        print(f"## {n}. {i['headline']}\n")
        print(f"_{who} · {i['category']} · confidence {i['confidence']} · judge depth **{depth}**"
              + (f" · **hit** on planted truth #{s['hit']}" if hit else "") + (" · grounded" if grounded else " · quote not verbatim") + "_\n")
        print(i["explanation"] + "\n")
        for e in i["evidence"]:
            t = titles.get(e.get("exp"), "?")
            print(f"> “{e['quote']}” — _{t}_")
        if i.get("would_predict"):
            print(f"\n_Would predict:_ {i['would_predict']}")
        if hit:
            print(f"\n_Planted truth it matched (judge-only file):_ {gt['latent_self'][s['hit']]['claim']}")
        print(f"\n_Judge note:_ {s.get('note','')}\n")


if __name__ == "__main__":
    main()
