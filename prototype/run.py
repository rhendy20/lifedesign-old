#!/usr/bin/env python3
"""Defining Experiences insight engine — one command.

    python3 prototype/run.py path/to/experiences/            # a folder with one .txt/.md file per experience
    python3 prototype/run.py path/to/one_experience.txt
    python3 prototype/run.py my_experiences/ --tier cheap    # fable | mid | cheap (default mid)
    python3 prototype/run.py my_experiences/ --gen v0        # run the naive baseline instead

Needs either ANTHROPIC_API_KEY in the environment, or a logged-in `claude` CLI (Claude Code) on PATH.
Audio files are sent for transcription only if OPENAI_API_KEY is set (unverified path).

Writes: <out>/insights.md (readable) and <out>/insights.json (full audit trail incl. every stage).
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from engine.corpus import load_corpus  # noqa: E402
from engine.llm import LLM, resolve_model  # noqa: E402
from engine.pipeline import Pipeline  # noqa: E402

LATEST_GEN = "v3"


def render_md(out: dict, corpus) -> str:
    lines = [f"# Insights from {len(corpus)} defining experiences",
             f"_engine {out['generation']} · model {out['model']} · {datetime.now():%Y-%m-%d %H:%M} · cost ${out['cost_usd']:.2f}_", ""]
    lines.append("Every insight below cites the words it came from. Confidence is stated, not implied. "
                 "Contradictions are left in. Treat each one as a question to check against your life, not a verdict.")
    lines.append("")
    by_cat = {}
    for i in out["insights"]:
        by_cat.setdefault(i["category"], []).append(i)
    names = {"core_values": "Core values", "zone_of_genius": "Zone of genius", "defining_beliefs": "Defining beliefs",
             "patterns_to_explore": "Patterns to explore"}
    for cat in ["core_values", "zone_of_genius", "defining_beliefs", "patterns_to_explore"]:
        items = by_cat.get(cat, [])
        if not items:
            continue
        lines += [f"## {names[cat]}", ""]
        for it in items:
            flag = "" if it["grounded"] else " ⚠ quote not found verbatim"
            lines += [f"### {it['headline']}", f"*Confidence: {it['confidence']}*{flag}", "", it["explanation"], ""]
            for e in it["evidence"]:
                exp = corpus[e["exp"] - 1].title if e.get("exp") and 0 < e["exp"] <= len(corpus) else "?"
                lines.append(f"> “{e['quote']}” — _{exp}_")
            if it.get("would_predict"):
                lines.append(f"\n_Would predict:_ {it['would_predict']}")
            lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--tier", default="mid", help="fable | mid | cheap | opus, or a model id")
    ap.add_argument("--gen", default=LATEST_GEN, help="prompt generation: v0 (baseline) .. v3")
    ap.add_argument("--out", default=None, help="output folder (default: <path>/insights-<timestamp>)")
    ap.add_argument("--workers", type=int, default=3)
    args = ap.parse_args()

    if not shutil.which("claude") and not __import__("os").environ.get("ANTHROPIC_API_KEY"):
        sys.exit("Need ANTHROPIC_API_KEY set, or Claude Code installed and logged in (the `claude` command).")

    corpus = load_corpus(args.path)
    print(f"Loaded {len(corpus)} experiences: " + "; ".join(f"E{e.index} {e.title!r} ({len(e.text.split())} words)" for e in corpus))
    src = Path(args.path)
    outdir = Path(args.out) if args.out else (src if src.is_dir() else src.parent) / f"insights-{datetime.now():%Y%m%d-%H%M%S}"
    outdir.mkdir(parents=True, exist_ok=True)

    llm = LLM(ledger_path=outdir / "ledger.jsonl")
    print(f"Running engine {args.gen} on {resolve_model(args.tier)} via {llm.backend} backend ...")
    out = Pipeline(llm, args.gen, resolve_model(args.tier), workers=args.workers).run(corpus)
    (outdir / "insights.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    md = render_md(out, corpus)
    (outdir / "insights.md").write_text(md)
    print("\n" + md)
    print(f"\nSaved to {outdir}/insights.md and insights.json  (cost ${out['cost_usd']:.2f}, {out['latency_ms']/1000:.0f}s)")


if __name__ == "__main__":
    main()
