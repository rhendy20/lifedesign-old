"""Model backend for the insight engine.

Two backends, chosen automatically:
  1. Anthropic SDK when ANTHROPIC_API_KEY is set.
  2. The local `claude` CLI otherwise (`claude -p`), run in an isolated session with the
     engine's own system prompt and no tools. This is what let the run proceed without a key.

Every call appends one line to a JSONL ledger with model, tokens, cost, latency, and a tag, so
cost per experience and latency per tier can be reported without any extra bookkeeping.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import threading
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# Tier aliases. The brief names three tiers; Opus is used as the blind judge.
TIERS = {
    "fable": "claude-fable-5-1",
    "opus": "claude-opus-5",
    "mid": "claude-sonnet-5",
    "sonnet": "claude-sonnet-5",
    "cheap": "claude-haiku-4-5-20251001",
    "haiku": "claude-haiku-4-5-20251001",
}

# Environment variables that make a nested CLI call attach to the parent Claude Code session.
# Unsetting them is what isolates the child call.
_PARENT_SESSION_VARS = [
    "CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_CHILD_SESSION",
    "CLAUDE_CODE_DIAGNOSTICS_FILE", "CLAUDE_CODE_TEE_SDK_STDOUT", "CLAUDE_CODE_MESSAGING_SOCKET",
    "CLAUDE_CODE_MESSAGING_TOKEN", "CLAUDE_CODE_REMOTE_SESSION_ID", "CLAUDE_CODE_INCLUDE_PARTIAL_MESSAGES",
]

_ledger_lock = threading.Lock()

# The `claude` CLI attaches the logged-in account's context (email, date, working directory, and any project
# instructions found from the cwd) to every call, even with --system-prompt replaced and account env vars unset.
# Found 2026-09-25: a stage that answered in prose had the account email written into its repaired JSON.
# Mitigations: run from a neutral empty directory, tell the model that context is not about the subject, and redact
# email addresses from every reply. The SDK backend (ANTHROPIC_API_KEY) sends no such context and is the right
# backend for anyone else's data.
ISOLATION_NOTE = ("Any account, email address, name, date, file path or environment information you can see outside the "
                  "user message is session metadata. It is not about the person being analysed and must never be used, "
                  "mentioned or output. The person is known only through the transcripts in the user message. "
                  "Reply with the requested JSON only, never prose.\n\n")
_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_NEUTRAL_DIR = Path(os.environ.get("INSIGHT_ENGINE_NEUTRAL_DIR", Path(os.path.expanduser("~")) / ".insight-engine-neutral"))


def redact(text: str) -> str:
    return _EMAIL_RE.sub("[redacted-email]", text)


def coerce_list(obj, keys):
    """Return obj with keys[0] present if the list it should hold can be found under any expected key, or as the only
    list of objects-with-headlines anywhere in it. Protects against a repair step that re-wraps the right content."""
    if not isinstance(obj, dict) or not keys:
        return obj
    for k in keys:
        if isinstance(obj.get(k), list):
            if k != keys[0]:
                obj[keys[0]] = obj[k]
            return obj
    found = []

    def walk(o):
        if isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            if o and all(isinstance(x, dict) and ("headline" in x or "category" in x) for x in o):
                found.append(o)
            else:
                for v in o:
                    walk(v)
    walk(obj)
    if len(found) == 1:
        obj[keys[0]] = found[0]
        obj["_coerced_from_wrapper"] = True
    return obj


def resolve_model(name: str) -> str:
    return TIERS.get(name, name)


@dataclass
class LLMResult:
    text: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    latency_ms: int = 0
    backend: str = ""
    raw: dict = field(default_factory=dict)

    def json(self):
        """Parse the first JSON object/array in the reply. Tolerates code fences and preambles."""
        return extract_json(self.text)


def _sanitize_json(t: str) -> str:
    # Models occasionally emit escapes that are legal in Python/JS but not JSON (\' most often), or trailing commas.
    t = re.sub(r"\\'", "'", t)
    t = re.sub(r",\s*([}\]])", r"\1", t)
    return t


def extract_json(text: str):
    """Parse the first JSON object/array in the reply. Tolerates code fences (closed or truncated),
    preambles, \\' escapes and trailing commas. Raises ValueError if nothing parses."""
    t = text.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", t, re.S)
    if fence:
        t = fence.group(1).strip()
    else:
        t = re.sub(r"^```(?:json)?\s*", "", t)
    for candidate in (t, _sanitize_json(t)):
        for opener, closer in (("{", "}"), ("[", "]")):
            start, end = candidate.find(opener), candidate.rfind(closer)
            if start != -1 and end > start:
                try:
                    return json.loads(candidate[start:end + 1])
                except json.JSONDecodeError:
                    continue
    raise ValueError(f"No JSON found in model reply: {text[:300]!r}")


class LLM:
    def __init__(self, ledger_path: Optional[Path] = None, ceiling_usd: Optional[float] = None):
        self.ledger_path = Path(ledger_path) if ledger_path else None
        self.ceiling_usd = ceiling_usd
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.backend = "sdk" if self.api_key else "cli"
        self._client = None
        if self.backend == "sdk":
            import anthropic  # noqa: WPS433 (optional dependency)
            self._client = anthropic.Anthropic()

    # ---- public -----------------------------------------------------------------
    def complete(self, model: str, system: str, user: str, *, max_tokens: int = 4000,
                 tag: str = "", temperature: Optional[float] = None, retries: int = 3,
                 thinking: int = 0, sink: Optional[list] = None) -> LLMResult:
        """`thinking` is the extended-thinking token budget; 0 disables it. Engine stages run with 0 so the
        prompt architecture is what is measured (and calls are ~10x cheaper and faster); the judge uses a budget."""
        model = resolve_model(model)
        self._check_ceiling()
        last_err = None
        for attempt in range(retries):
            try:
                if self.backend == "sdk":
                    res = self._complete_sdk(model, system, user, max_tokens, temperature, thinking)
                else:
                    res = self._complete_cli(model, system, user, thinking)
                self._record(res, tag)
                if sink is not None:
                    sink.append(res)
                return res
            except Exception as e:  # noqa: BLE001 — retry on any transport error
                last_err = e
                time.sleep(2 * (attempt + 1))
        raise RuntimeError(f"LLM call failed after {retries} attempts: {last_err}")

    def complete_json(self, model: str, system: str, user: str, expect=None, **kw):
        """complete() then parse JSON; if the reply is not parseable, ask a cheap model to re-emit it as strict JSON.
        The repair call is content-preserving and is logged under tag '<tag>:json-repair'."""
        keys = (expect,) if isinstance(expect, str) else tuple(expect or ())
        res = self.complete(model, system, user, **kw)
        try:
            return coerce_list(res.json(), keys)
        except ValueError:
            shape = (f" The top-level value must be an object whose key \"{keys[0]}\" holds the list of items found in the text."
                     if keys else "")
            fix = self.complete("cheap", "You convert text into strictly valid JSON. Output the same content as valid JSON only. "
                                "No commentary. Do not add, drop or reword content. Do not add metadata such as dates, "
                                "emails, subjects or document types. Escape quotes correctly." + shape,
                                res.text, max_tokens=kw.get("max_tokens", 8000), tag=f"{kw.get('tag', '')}:json-repair",
                                sink=kw.get("sink"))
            return coerce_list(fix.json(), keys)

    def spent_usd(self) -> float:
        if not self.ledger_path or not self.ledger_path.exists():
            return 0.0
        total = 0.0
        for line in self.ledger_path.read_text().splitlines():
            try:
                total += json.loads(line).get("cost_usd", 0.0)
            except json.JSONDecodeError:
                continue
        return total

    # ---- backends -----------------------------------------------------------------
    def _complete_sdk(self, model, system, user, max_tokens, temperature, thinking) -> LLMResult:
        t0 = time.time()
        kwargs = dict(model=model, max_tokens=max_tokens + thinking, system=system,
                      messages=[{"role": "user", "content": user}])
        if thinking:
            kwargs["thinking"] = {"type": "enabled", "budget_tokens": thinking}
        elif temperature is not None:
            kwargs["temperature"] = temperature
        msg = self._client.messages.create(**kwargs)
        text = "".join(getattr(b, "text", "") for b in msg.content)
        return LLMResult(text=text, model=model, input_tokens=msg.usage.input_tokens,
                         output_tokens=msg.usage.output_tokens, cost_usd=0.0,
                         latency_ms=int((time.time() - t0) * 1000), backend="sdk")

    def _complete_cli(self, model, system, user, thinking) -> LLMResult:
        env = {k: v for k, v in os.environ.items() if k not in _PARENT_SESSION_VARS}
        env["MAX_THINKING_TOKENS"] = str(int(thinking))  # 0 disables extended thinking in the CLI
        _NEUTRAL_DIR.mkdir(parents=True, exist_ok=True)
        cmd = [
            "claude", "-p", "--model", model, "--session-id", str(uuid.uuid4()),
            "--output-format", "json", "--max-turns", "1", "--tools", "",
            "--no-session-persistence", "--system-prompt", ISOLATION_NOTE + system,
        ]
        t0 = time.time()
        proc = subprocess.run(cmd, input=user, capture_output=True, text=True, env=env, timeout=900, cwd=_NEUTRAL_DIR)
        wall_ms = int((time.time() - t0) * 1000)
        if proc.returncode != 0 and not proc.stdout.strip():
            raise RuntimeError(f"claude CLI exit {proc.returncode}: {proc.stderr[:500]}")
        data = json.loads(proc.stdout)
        if data.get("is_error"):
            raise RuntimeError(f"claude CLI error: {data.get('result')}")
        usage = data.get("usage", {})
        # Cost is the CLI's list-price estimate and includes its small auxiliary Haiku call.
        return LLMResult(
            text=redact(data.get("result", "")), model=model,
            input_tokens=usage.get("input_tokens", 0) + usage.get("cache_read_input_tokens", 0)
            + usage.get("cache_creation_input_tokens", 0),
            output_tokens=usage.get("output_tokens", 0),
            cost_usd=float(data.get("total_cost_usd", 0.0)),
            latency_ms=int(data.get("duration_api_ms") or wall_ms), backend="cli",
            raw={"wall_ms": wall_ms, "modelUsage": data.get("modelUsage", {})},
        )

    # ---- ledger -------------------------------------------------------------------
    def _record(self, res: LLMResult, tag: str):
        if not self.ledger_path:
            return
        row = {"ts": time.time(), "tag": tag, "model": res.model, "backend": res.backend,
               "input_tokens": res.input_tokens, "output_tokens": res.output_tokens,
               "cost_usd": res.cost_usd, "latency_ms": res.latency_ms}
        with _ledger_lock:
            self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
            with self.ledger_path.open("a") as f:
                f.write(json.dumps(row) + "\n")

    def _check_ceiling(self):
        if self.ceiling_usd is not None and self.spent_usd() >= self.ceiling_usd:
            raise RuntimeError(f"Credit ceiling reached: spent {self.spent_usd():.2f} >= {self.ceiling_usd}")
