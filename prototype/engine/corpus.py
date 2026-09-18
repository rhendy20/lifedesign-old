"""Corpus loading: turn a directory (or single file) of experiences into a normalized structure.

Speaker words are preserved verbatim. Each experience is split into numbered lines so that later
stages can cite `E2:L14` and the harness can verify that a quoted span really exists.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List

TEXT_EXT = {".txt", ".md", ".markdown"}
AUDIO_EXT = {".m4a", ".mp3", ".wav", ".webm", ".mp4", ".ogg"}


@dataclass
class Experience:
    index: int              # 1-based, in corpus order
    title: str
    source: str
    text: str               # verbatim body
    lines: List[str] = field(default_factory=list)

    def numbered(self) -> str:
        return "\n".join(f"L{i+1}: {ln}" for i, ln in enumerate(self.lines))

    def tag(self) -> str:
        return f"E{self.index}"


def _split_lines(text: str) -> List[str]:
    # Sentence-ish segmentation that keeps the speaker's words intact. Filler stays in.
    text = re.sub(r"\s+", " ", text.strip())
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'“‘(])", text)
    return [p.strip() for p in parts if p.strip()]


def _strip_md_header(raw: str):
    lines = raw.strip().splitlines()
    title = None
    body = []
    for ln in lines:
        if title is None and ln.startswith("# "):
            title = ln[2:].strip()
            continue
        if title is not None and re.fullmatch(r"_.*_", ln.strip()) and not body:
            continue  # period line written by the persona generator; not the speaker's words
        body.append(ln)
    return title, "\n".join(body).strip()


def _transcribe_audio(path: Path) -> str:
    """Send audio to OpenAI transcription (same provider the repo's API already uses).
    Unverified in this environment: no audio tooling or key was available."""
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError(f"{path.name}: audio input needs OPENAI_API_KEY for transcription")
    import urllib.request
    boundary = "----insightengine"
    data = path.read_bytes()
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"model\"\r\n\r\nwhisper-1\r\n"
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{path.name}\"\r\n"
            f"Content-Type: application/octet-stream\r\n\r\n").encode() + data + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request("https://api.openai.com/v1/audio/transcriptions", data=body, method="POST",
                                 headers={"Authorization": f"Bearer {key}",
                                          "Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read())["text"]


def load_corpus(path: str | Path) -> List[Experience]:
    p = Path(path)
    files = [p] if p.is_file() else sorted(q for q in p.iterdir() if q.suffix.lower() in TEXT_EXT | AUDIO_EXT)
    if not files:
        raise SystemExit(f"No experience files found in {p}. Put one .txt/.md (or audio) file per experience there.")
    out = []
    for i, f in enumerate(files, 1):
        if f.suffix.lower() in AUDIO_EXT:
            text, title = _transcribe_audio(f), f.stem
        else:
            title, text = _strip_md_header(f.read_text(encoding="utf-8"))
            title = title or f.stem
        out.append(Experience(index=i, title=title, source=str(f), text=text, lines=_split_lines(text)))
    return out


def corpus_to_json(corpus: List[Experience]) -> str:
    return json.dumps([asdict(e) for e in corpus], indent=2, ensure_ascii=False)


def find_quote(corpus: List[Experience], quote: str, exp_index: int | None = None) -> bool:
    """Programmatic grounding check: does this quoted span appear verbatim (whitespace/case-insensitive,
    punctuation-tolerant) in the cited experience? Used by the harness; models never self-certify this."""
    def norm(s):
        return re.sub(r"[^a-z0-9 ]", "", re.sub(r"\s+", " ", s.lower())).strip()
    q = norm(quote)
    if len(q) < 12:
        return False
    targets = [e for e in corpus if exp_index is None or e.index == exp_index]
    return any(q in norm(e.text) for e in targets)
