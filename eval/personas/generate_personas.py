"""Generate synthetic personas in a context separate from the engine.

This script never imports or reads anything under /prompts. Each persona is one fresh model call.
The output has two parts that are kept apart on disk:

  eval/personas/<id>/experiences/NN-<slug>.md   what the engine sees
  eval/personas/<id>/ground_truth.json          what only the judge sees (known / latent / decoys)
  eval/personas/<id>/persona.json               bio and archetype (judge only)

The archetypes below are fixed in code so the brief's required adversarial cases are guaranteed.
"""
from __future__ import annotations

import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "prototype"))
from engine.llm import LLM  # noqa: E402  (backend only; no prompts)

OUT = Path(__file__).resolve().parent
GEN_MODEL = "opus"

ARCHETYPES = [
    {"id": "p01_mundane", "archetype": "mundane",
     "spec": "A 52-year-old man who has worked at the same county water utility billing office for 27 years in a mid-sized Ohio town. Married, two adult kids, bowls on Tuesdays. His experiences are genuinely mundane: no deaths, divorces, illnesses, career changes or dramatic turning points. The 'defining' moments are small: a supervisor's offhand comment, a fishing trip, a decision not to apply for a promotion, a neighbor's fence. He does not think of himself as interesting."},
    {"id": "p02_self_aware", "archetype": "self_aware",
     "spec": "A 38-year-old woman finishing a master's in counseling after ten years in HR in Denver. Highly self-aware: she has done years of therapy and names her own patterns as she tells each story ('classic me, over-functioning', 'that's my abandonment stuff'). The challenge for any analyst: the interesting patterns are the ones she does NOT name, which sit underneath or contradict the labels she applies to herself."},
    {"id": "p03_cliche", "archetype": "cliche",
     "spec": "A 29-year-old man who sells solar panels door-to-door in Phoenix and posts motivational content. He narrates entirely in cliché and borrowed language: 'everything happens for a reason', 'trust the process', 'grind', 'level up', 'God's plan', podcast phrases. Real specific events are buried under the phrasing. The analyst must find the person under the vocabulary."},
    {"id": "p04_withholder", "archetype": "withholder",
     "spec": "A 61-year-old recently retired machinist from Erie, Pennsylvania. Divorced, one son he sees twice a year. He withholds: accounts are short, flat, factual, and the emotional weight is left out or mentioned in a single clause and moved past. Transcripts for him are 250-450 words, not longer. What matters is what he skips."},
    {"id": "p05_lagos", "archetype": "different_life_shape",
     "spec": "A 24-year-old woman, eldest of five, in her final year of nursing school in Lagos, Nigeria. Yoruba family, church-going, father lost his import business in 2016. She speaks Nigerian English with some Yoruba expressions. Her life shape, pressures and assumptions differ sharply from a 30s American founder: extended-family obligation, remittances, exam culture, an aunt who funds her fees, the question of leaving for the UK."},
    {"id": "p06_osaka", "archetype": "different_life_shape",
     "spec": "A 71-year-old widowed Japanese woman in Osaka, a retired junior high school vice-principal. Her husband died four years ago. She speaks in a translated, formal, slightly indirect register. Experiences span 1960s childhood, a career in a system that constrained women, her marriage, retirement, and widowhood. Culturally specific: obligation, restraint, what is left unsaid, ancestors, the neighborhood association."},
    {"id": "p07_saopaulo", "archetype": "different_life_shape",
     "spec": "A 44-year-old single father in São Paulo who drives a city bus. His wife left when their daughter was three; the daughter is now fifteen. Evangelical church member, grew up in a favela, his brother was killed at 19. Speaks in translated Brazilian Portuguese register with warmth and occasional humor. His concerns are money, his daughter's safety and schooling, his own tiredness."},
    {"id": "p08_near_founder", "archetype": "near_founder_control",
     "spec": "A 34-year-old man in Utah who served a two-year religious mission abroad in his early twenties, got a business degree, spent several years in sales and customer success at a fast-growing startup with quick promotions, then left to start his own company. Married with young children. This life shape intentionally resembles a common founder profile; do not make him unusually interesting. Give him ordinary contradictions."},
    {"id": "p09_contradiction", "archetype": "stated_vs_lived_contradiction",
     "spec": "A 47-year-old woman, an emergency-room charge nurse in Atlanta, divorced and remarried, three kids. She says repeatedly that family is her first priority and that she is 'not a work person', yet every story she picks is a work story, and the family appears only as backdrop or as something she was rushing back from. She does not notice this. Do not make her notice it."},
    {"id": "p10_freshman", "archetype": "young_thin_corpus",
     "spec": "A 19-year-old first-generation college freshman in Texas, child of Salvadoran immigrants. His younger sister has had a chronic illness since he was eleven. He has only four experiences and they are recent and small in scope: a scholarship interview, a night in a hospital waiting room, a high school teacher, moving into a dorm. He talks like a nineteen-year-old: 'like', 'kind of', 'I don't know'."},
]

SYSTEM = """You write raw, realistic first-person spoken transcripts for research on personal-insight software.
You are given one person. Produce their defining experiences as if transcribed unedited from audio they recorded alone,
answering the prompt "Tell me about an experience that shaped who you are." Then, separately, produce a hidden
ground-truth file describing what is actually true about this person.

Non-negotiable rules for the transcripts:
- Spoken register. Keep filler, false starts, self-corrections, tangents, and the odd irrelevant detail. No headings inside a transcript.
- Show, do not tell. The person's deeper patterns must be visible in what they choose to tell, how they tell it, what they skip, and what they repeat. The narrator must NEVER state the latent truths in words; if they come close, they veer away or misattribute.
- Do not write to be easy. Include red herrings: details that look meaningful and are not. Include contradictions between what they say about themselves and what they did.
- Each transcript is a different experience from a different period of life unless the spec says otherwise. Default length 550-900 words each; obey the spec if it says shorter.
- Stay in this person's culture, register, and vocabulary. Never write a generic American self-help voice unless the spec asks for it.

Ground truth rules:
- known_self: 6-10 things this person already knows and would readily say about themselves. Several must appear more or less explicitly in the transcripts.
- latent_self: 4-5 true, specific, non-obvious patterns you deliberately planted across at least two transcripts each, which the narrator never names. Each has: claim, the transcript numbers it is planted in, and a one-line note on how it shows. These must be things a stranger knowing only age, sex and occupation could not guess.
- decoys: 4-5 plausible-sounding claims about this person that a lazy analyst might make and that are FALSE for them, with a one-line reason.
- domain_predictions: 2-3 true statements about how this person behaves in a life area the transcripts never discuss (e.g. money, health, friendships), consistent with the latent patterns. These are for scoring predictive insight.

Return ONLY a JSON object with this exact shape:
{
  "name": "...", "age": 0, "sex": "...", "occupation": "...", "culture_context": "...",
  "experiences": [{"title": "...", "period": "...", "transcript": "..."}],
  "ground_truth": {
    "known_self": ["..."],
    "latent_self": [{"claim": "...", "planted_in": [1, 3], "how_it_shows": "..."}],
    "decoys": [{"claim": "...", "why_false": "..."}],
    "domain_predictions": [{"domain": "...", "claim": "..."}]
  }
}"""


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40]


def build(llm: LLM, spec: dict) -> str:
    n = 4 if spec["archetype"] == "young_thin_corpus" else 5
    user = (f"Persona spec:\n{spec['spec']}\n\nArchetype tag (for you, not the narrator): {spec['archetype']}.\n"
            f"Write exactly {n} experiences. Return the JSON object only.")
    res = llm.complete(GEN_MODEL, SYSTEM, user, max_tokens=16000, tag=f"persona:{spec['id']}")
    data = res.json()
    d = OUT / spec["id"]
    (d / "experiences").mkdir(parents=True, exist_ok=True)
    for i, e in enumerate(data["experiences"], 1):
        (d / "experiences" / f"{i:02d}-{slug(e['title'])}.md").write_text(
            f"# {e['title']}\n\n_{e.get('period', '')}_\n\n{e['transcript'].strip()}\n")
    gt = data.pop("ground_truth")
    (d / "ground_truth.json").write_text(json.dumps(gt, indent=2, ensure_ascii=False))
    data.pop("experiences")
    data.update({"id": spec["id"], "archetype": spec["archetype"], "spec": spec["spec"],
                 "gen_model": res.model, "gen_cost_usd": res.cost_usd})
    (d / "persona.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))
    words = sum(len(open(p).read().split()) for p in (d / "experiences").glob("*.md"))
    return f"{spec['id']}: {len(list((d / 'experiences').glob('*.md')))} experiences, {words} words, ${res.cost_usd:.2f}"


if __name__ == "__main__":
    only = sys.argv[1:]
    llm = LLM(ledger_path=ROOT / "eval/results/ledger.jsonl", ceiling_usd=100.0)
    specs = [s for s in ARCHETYPES if not only or s["id"] in only]
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = {ex.submit(build, llm, s): s["id"] for s in specs}
        for f in as_completed(futs):
            try:
                print(f.result(), flush=True)
            except Exception as e:  # noqa: BLE001
                print(f"FAILED {futs[f]}: {e}", flush=True)
    print(f"total spent so far: ${llm.spent_usd():.2f}")
