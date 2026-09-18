"""Run one (generation, tier) condition over all personas and freeze the outputs.

    python3 eval/harness/run_eval.py --gen v1 --tier mid [--personas p01_mundane p02_self_aware]

Outputs: eval/results/outputs/<gen>__<tier>/<persona>.json plus FROZEN.json (sha256 + timestamp per file).
Nothing under eval/personas/*/ground_truth.json or eval/sealed/ is read here. The engine only sees experiences/.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "prototype"))
from engine.corpus import load_corpus  # noqa: E402
from engine.llm import LLM, resolve_model  # noqa: E402
from engine.pipeline import Pipeline  # noqa: E402

PERSONAS = ROOT / "eval/personas"
OUT = ROOT / "eval/results/outputs"


def persona_ids():
    return sorted(p.name for p in PERSONAS.iterdir() if (p / "experiences").is_dir())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gen", required=True)
    ap.add_argument("--tier", required=True, help="fable|mid|cheap|opus or a model id")
    ap.add_argument("--personas", nargs="*")
    ap.add_argument("--workers", type=int, default=3, help="personas in parallel")
    ap.add_argument("--stage-workers", type=int, default=3)
    ap.add_argument("--ceiling", type=float, default=75.0)
    args = ap.parse_args()

    llm = LLM(ledger_path=ROOT / "eval/results/ledger.jsonl", ceiling_usd=args.ceiling)
    cond = f"{args.gen}__{args.tier}"
    outdir = OUT / cond
    outdir.mkdir(parents=True, exist_ok=True)
    ids = args.personas or persona_ids()

    from concurrent.futures import ThreadPoolExecutor, as_completed

    def one(pid):
        target = outdir / f"{pid}.json"
        if target.exists():
            return f"{pid}: exists, skipped"
        corpus = load_corpus(PERSONAS / pid / "experiences")
        pipe = Pipeline(llm, args.gen, resolve_model(args.tier), workers=args.stage_workers)
        out = pipe.run(corpus)
        out.update({"persona": pid, "n_experiences": len(corpus), "condition": cond,
                    "frozen_at": datetime.now(timezone.utc).isoformat()})
        target.write_text(json.dumps(out, indent=2, ensure_ascii=False))
        g = sum(1 for i in out["insights"] if i["grounded"])
        return f"{pid}: {len(out['insights'])} insights ({g} grounded), ${out['cost_usd']:.2f}, {out['latency_ms']/1000:.0f}s"

    t0 = time.time()
    with ThreadPoolExecutor(args.workers) as ex:
        futs = {ex.submit(one, pid): pid for pid in ids}
        for f in as_completed(futs):
            try:
                print(f.result(), flush=True)
            except Exception as e:  # noqa: BLE001
                print(f"FAILED {futs[f]}: {e}", flush=True)

    # Freeze manifest: hash every output before any sealed/ground-truth file is opened by the scorer.
    manifest = {"condition": cond, "frozen_at": datetime.now(timezone.utc).isoformat(), "files": {}}
    for f in sorted(outdir.glob("p*.json")):
        manifest["files"][f.name] = hashlib.sha256(f.read_bytes()).hexdigest()
    (outdir / "FROZEN.json").write_text(json.dumps(manifest, indent=2))
    print(f"frozen {len(manifest['files'])} outputs for {cond} in {time.time()-t0:.0f}s; total spent ${llm.spent_usd():.2f}")


if __name__ == "__main__":
    main()
