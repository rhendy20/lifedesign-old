"""The insight pipeline.

    Raw experience -> Extraction -> Interpretation -> Adversarial critic -> Cross-experience synthesis -> Delivery

Every generation from v1 on uses these five stages; what differs between generations is the prompt text
(and, from v2, programmatic quote grounding between stages). v0 is the naive control: one prompt per
experience, no stages. Both paths return the same output contract so the judge scores them identically.

Output contract (per corpus):
{
  "generation": "v1", "model": "...", "insights": [
     {"id": "i1", "category": "core_values", "headline": "...", "explanation": "...",
      "evidence": [{"exp": 2, "quote": "verbatim span"}], "confidence": "low|medium|high",
      "scope": "single|cross", "grounded": true}
  ],
  "stages": {...raw stage outputs for audit...}, "cost_usd": 0.0, "latency_ms": 0
}
"""
from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor
from typing import List

from .corpus import Experience, find_quote
from .llm import LLM
from .prompts import PROMPTS_DIR, fill, framework_brief, load_framework, load_prompt

VALID_CATEGORIES = {"core_values", "zone_of_genius", "defining_beliefs", "patterns_to_explore"}


def _transcript_block(e: Experience) -> str:
    return f"[{e.tag()}] \"{e.title}\"\n{e.numbered()}"


class Pipeline:
    def __init__(self, llm: LLM, generation: str, model: str, workers: int = 4, label: str = "run"):
        self.llm, self.generation, self.model, self.workers = llm, generation, model, workers
        self.fw = load_framework()
        self.fw_brief = framework_brief(self.fw)
        self.tag_prefix = f"{generation}:{model}:{label}"
        self._sink: list = []  # every LLMResult this pipeline instance produced; exact cost regardless of parallel runs

    # ------------------------------------------------------------------ public
    def run(self, corpus: List[Experience]) -> dict:
        t0 = time.time()
        self._sink.clear()
        if self.generation == "v0":
            out = self._run_v0(corpus)
        else:
            out = self._run_staged(corpus)
        out["generation"], out["model"] = self.generation, self.model
        out["cost_usd"] = round(sum(r.cost_usd for r in self._sink), 4)
        out["n_calls"] = len(self._sink)
        out["model_latency_ms"] = sum(r.latency_ms for r in self._sink)  # summed per-call API time
        out["latency_ms"] = int((time.time() - t0) * 1000)             # wall-clock with internal parallelism
        out["insights"] = self._normalize(out["insights"], corpus)
        return out

    # ------------------------------------------------------------------ v0 control
    def _run_v0(self, corpus):
        p = load_prompt("v0", "baseline")

        def one(e):
            res = self.llm.complete_json(self.model, p["system"], fill(p["user"], transcript=e.text), expect="insights", tag=f"{self.tag_prefix}:baseline:E{e.index}", sink=self._sink)
            items = res.get("insights", [])
            for it in items:
                it["scope"], it["evidence"], it["_exp"] = "single", [], e.index
            return items

        with ThreadPoolExecutor(self.workers) as ex:
            per_exp = list(ex.map(one, corpus))
        return {"insights": [i for items in per_exp for i in items], "stages": {}}

    # ------------------------------------------------------------------ v1+ staged
    def _run_staged(self, corpus):
        g = self.generation
        p_ext, p_int, p_crit = load_prompt(g, "extraction"), load_prompt(g, "interpretation"), load_prompt(g, "critic")
        p_syn, p_del = load_prompt(g, "synthesis"), load_prompt(g, "delivery")
        grounding_gate = self.generation not in ("v1",)  # v2+ drop candidates whose quotes are not verbatim

        def per_experience(e: Experience):
            block = _transcript_block(e)
            ext = self.llm.complete_json(self.model, p_ext["system"], fill(p_ext["user"], transcript=block),
                                         tag=f"{self.tag_prefix}:extraction:E{e.index}", sink=self._sink)
            interp = self.llm.complete_json(self.model, fill(p_int["system"], framework=self.fw_brief),
                                       fill(p_int["user"], transcript=block, extraction=ext),
                                       expect="candidates", tag=f"{self.tag_prefix}:interpretation:E{e.index}", sink=self._sink)
            cands = interp.get("candidates", [])
            if grounding_gate:
                cands, dropped = self._ground_filter(cands, corpus, default_exp=e.index)
                interp["_dropped_ungrounded"] = dropped
            crit = self.llm.complete_json(self.model, fill(p_crit["system"], framework=self.fw_brief),
                                     fill(p_crit["user"], transcript=block, candidates={"candidates": cands}),
                                     expect="survivors", tag=f"{self.tag_prefix}:critic:E{e.index}", sink=self._sink)
            survivors = crit.get("survivors", [])
            for s in survivors:
                s.setdefault("exp", e.index)
            return {"exp": e.index, "extraction": ext, "interpretation": interp, "critic": crit, "survivors": survivors}

        with ThreadPoolExecutor(self.workers) as ex:
            stage_out = list(ex.map(per_experience, corpus))

        all_transcripts = "\n\n".join(_transcript_block(e) for e in corpus)
        survivors = [s for so in stage_out for s in so["survivors"]]
        syn = self.llm.complete_json(self.model, fill(p_syn["system"], framework=self.fw_brief),
                                fill(p_syn["user"], transcripts=all_transcripts, survivors={"survivors": survivors},
                                     n=str(len(corpus))), max_tokens=8000, expect=("insights", "candidates"), tag=f"{self.tag_prefix}:synthesis", sink=self._sink)
        syn_items = syn.get("insights") or syn.get("candidates", [])
        if grounding_gate:
            syn_items, dropped = self._ground_filter(syn_items, corpus)
            syn["_dropped_ungrounded"] = dropped

        # v3+: a cross-experience critic verifies synthesis candidates against the whole corpus before delivery.
        cross = None
        if (PROMPTS_DIR / g / "cross_critic.md").exists():
            p_x = load_prompt(g, "cross_critic")
            cross = self.llm.complete_json(self.model, fill(p_x["system"], framework=self.fw_brief),
                                           fill(p_x["user"], transcripts=all_transcripts, candidates={"candidates": syn_items}),
                                           max_tokens=8000, expect="insights", tag=f"{self.tag_prefix}:cross_critic", sink=self._sink)
            syn_items = cross.get("insights", syn_items)
            if grounding_gate:
                syn_items, dropped = self._ground_filter(syn_items, corpus)
                cross["_dropped_ungrounded"] = dropped

        deliv = self.llm.complete_json(self.model, p_del["system"],
                                  fill(p_del["user"], insights={"insights": syn_items}, transcripts=all_transcripts),
                                  max_tokens=8000, expect="insights", tag=f"{self.tag_prefix}:delivery", sink=self._sink)
        final = deliv.get("insights", syn_items)
        return {"insights": final, "stages": {"per_experience": stage_out, "synthesis": syn, "cross_critic": cross, "delivery": deliv}}

    # ------------------------------------------------------------------ helpers
    @staticmethod
    def _ground_filter(items, corpus, default_exp=None):
        kept, dropped = [], []
        for it in items:
            ev = it.get("evidence", [])
            ok = [q for q in ev if find_quote(corpus, q.get("quote", ""), q.get("exp", default_exp))]
            if ok:
                it["evidence"] = ok
                kept.append(it)
            else:
                dropped.append(it)
        return kept, dropped

    @staticmethod
    def _normalize(insights, corpus):
        out = []
        for n, it in enumerate(insights, 1):
            cat = str(it.get("category", "")).strip().lower().replace(" ", "_")
            if cat not in VALID_CATEGORIES:
                cat = "patterns_to_explore"
            ev = []
            for q in it.get("evidence", []) or []:
                if isinstance(q, dict) and q.get("quote"):
                    exp = q.get("exp")
                    try:
                        exp = int(str(exp).lstrip("E")) if exp is not None else None
                    except ValueError:
                        exp = None
                    ev.append({"exp": exp, "quote": str(q["quote"]), "verbatim": find_quote(corpus, str(q["quote"]), exp)})
            out.append({
                "id": f"i{n}", "category": cat,
                "headline": str(it.get("headline", "")).strip(),
                "explanation": str(it.get("explanation", it.get("evidence_chain", ""))).strip(),
                "evidence": ev,
                "confidence": str(it.get("confidence", "unstated")).lower(),
                "scope": it.get("scope", "cross" if len({e["exp"] for e in ev}) > 1 else "single"),
                "grounded": bool(ev) and all(e["verbatim"] for e in ev),
                "would_predict": str(it.get("would_predict", "")).strip(),
                "source_exp": it.get("_exp"),
            })
        return out
