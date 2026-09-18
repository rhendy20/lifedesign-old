"""Prompt loading. Each stage prompt is a markdown file with `## system` and `## user` sections and
`{{placeholders}}`. Generations live in /prompts/vN/. Keeping prompts as files, not strings in code,
is what makes them diffable and versionable."""
from __future__ import annotations

import json
import re
from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parents[2] / "prompts"


def load_framework() -> dict:
    return json.loads((PROMPTS_DIR / "framework.json").read_text())


def framework_brief(fw: dict) -> str:
    """Compact rendering of the framework for prompts: categories with disambiguation, pillars with subsections."""
    cats = "\n".join(f"- {c['id']}: {c['definition']} Disambiguation: {c['disambiguation']}" for c in fw["insight_categories"])
    pillars = "\n".join(f"- {p['name']}: " + ", ".join(s["name"] for s in p["subsections"]) for p in fw["pillars"])
    return f"INSIGHT CATEGORIES (use these ids exactly):\n{cats}\n\nLIFE PILLARS (domains where behaviour shows up):\n{pillars}"


def load_prompt(generation: str, stage: str) -> dict:
    path = PROMPTS_DIR / generation / f"{stage}.md"
    text = path.read_text()
    sections = {}
    for m in re.finditer(r"^## (\w+)\s*\n(.*?)(?=^## \w+\s*$|\Z)", text, re.S | re.M):
        sections[m.group(1).strip()] = m.group(2).strip()
    if "system" not in sections or "user" not in sections:
        raise ValueError(f"{path} needs '## system' and '## user' sections")
    return sections


def fill(template: str, **kw) -> str:
    out = template
    for k, v in kw.items():
        out = out.replace("{{" + k + "}}", v if isinstance(v, str) else json.dumps(v, indent=2, ensure_ascii=False))
    leftover = re.findall(r"{{(\w+)}}", out)
    if leftover:
        raise ValueError(f"Unfilled placeholders: {leftover}")
    return out
