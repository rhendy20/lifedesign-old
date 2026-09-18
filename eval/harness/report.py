"""Aggregate scores into the three numbers that decide the question, per condition and per archetype.

    python3 eval/harness/report.py [--tag <score-set-tag>]  -> prints markdown, writes eval/results/summary.md

Depth rate   = share of insights with depth >= 3
Hit rate     = distinct latent_self claims captured / total latent_self claims (recall), plus share of insights that are hits
FP rate      = share of insights flagged false_positive
Grounding    = share of insights whose every quote is verbatim in the cited experience (programmatic, not judged)
Cost/latency = per experience, from the frozen outputs (CLI list-price basis)
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "eval/results/outputs"
SCORES = ROOT / "eval/results/scores"
PERSONAS = ROOT / "eval/personas"


def archetype(pid):
    f = PERSONAS / pid / "persona.json"
    return json.loads(f.read_text()).get("archetype", "?") if f.exists() else "?"


def collect(tag=None):
    rows = []  # one per scored insight
    latent_total = {}
    for f in sorted(SCORES.glob("*.json")):
        if tag and not f.stem.endswith(tag):
            continue
        d = json.loads(f.read_text())
        pid = d["persona"]
        latent_total[pid] = d["n_latent"]
        for s in d["scores"]:
            if "condition" not in s:
                continue
            rows.append({"persona": pid, "archetype": archetype(pid), "set": f.stem.split("__")[-1], **s})
    # grounding + cost from outputs
    meta = {}
    for cdir in OUT.iterdir():
        if not cdir.is_dir():
            continue
        for pf in cdir.glob("p*.json"):
            d = json.loads(pf.read_text())
            g = {i["id"]: i["grounded"] for i in d["insights"]}
            meta[(cdir.name, pf.stem)] = {"grounded": g, "cost": d["cost_usd"], "latency": d["latency_ms"],
                                          "n_exp": d["n_experiences"], "n_ins": len(d["insights"])}
    return rows, latent_total, meta


def summarise(rows, latent_total, meta, group_key="condition"):
    by = defaultdict(list)
    for r in rows:
        by[(r[group_key], r["set"])].append(r)
    lines = []
    header = "| condition | set | insights | depth≥3 | mean depth | hit recall | hit share | FP rate | grounded | $/exp | s/exp |"
    lines += [header, "|" + "---|" * 11]
    for (cond, sset), rs in sorted(by.items()):
        n = len(rs)
        depth = sum(1 for r in rs if r["depth"] >= 3) / n
        mean_d = sum(r["depth"] for r in rs) / n
        hits = defaultdict(set)
        for r in rs:
            if r.get("hit") is not None:
                hits[r["persona"]].add(r["hit"])
        personas = {r["persona"] for r in rs}
        recall = sum(len(hits[p]) for p in personas) / max(1, sum(latent_total.get(p, 0) for p in personas))
        hit_share = sum(1 for r in rs if r.get("hit") is not None) / n
        fp = sum(1 for r in rs if r.get("false_positive")) / n
        gr = [meta.get((cond, r["persona"]), {}).get("grounded", {}).get(r["insight_id"], False) for r in rs]
        grounded = sum(gr) / n
        ms = [meta[(cond, p)] for p in personas if (cond, p) in meta]
        cost = sum(m["cost"] for m in ms) / max(1, sum(m["n_exp"] for m in ms))
        lat = sum(m["latency"] for m in ms) / 1000 / max(1, sum(m["n_exp"] for m in ms))
        lines.append(f"| {cond} | {sset} | {n} | {depth:.0%} | {mean_d:.2f} | {recall:.0%} | {hit_share:.0%} | {fp:.0%} | {grounded:.0%} | {cost:.3f} | {lat:.0f} |")
    return "\n".join(lines)


def by_archetype(rows):
    by = defaultdict(list)
    for r in rows:
        by[(r["condition"], r["archetype"])].append(r)
    lines = ["| condition | archetype | insights | depth≥3 | hit share | FP rate |", "|---|---|---|---|---|---|"]
    for (cond, arch), rs in sorted(by.items()):
        n = len(rs)
        lines.append(f"| {cond} | {arch} | {n} | {sum(1 for r in rs if r['depth']>=3)/n:.0%} | "
                     f"{sum(1 for r in rs if r.get('hit') is not None)/n:.0%} | {sum(1 for r in rs if r.get('false_positive'))/n:.0%} |")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag")
    ap.add_argument("--out", default=str(ROOT / "eval/results/summary.md"))
    args = ap.parse_args()
    rows, latent_total, meta = collect(args.tag)
    if not rows:
        print("no scores yet")
        return
    md = "# Eval summary\n\nScores are blind (labels stripped, pooled per persona). Cost is CLI list-price basis incl. CLI overhead.\n\n"
    md += "## By condition\n\n" + summarise(rows, latent_total, meta) + "\n\n## By archetype\n\n" + by_archetype(rows) + "\n"
    Path(args.out).write_text(md)
    print(md)


if __name__ == "__main__":
    main()
