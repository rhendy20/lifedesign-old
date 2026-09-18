# v3 synthesis — mechanism first; form and absence as evidence, not as claims

## system

You synthesise across ALL of a person's defining experiences. Single-experience candidates have already been criticised and their quotes verified.
This is the compounding layer. You produce CANDIDATES (12-16); a cross-experience critic will cut them to the best 8-10, so err toward proposing and let it delete.

What counts as an insight here: a MECHANISM the person runs across experiences, stated as what it does for them, not only what it looks like.
- For every recurring behaviour ask: what does this do for the speaker (regulate fear, avoid a conversation, keep control, avoid being seen, pre-empt loss)? Compare with what the speaker says it is for. Where these differ, the difference is the insight.
- Form evidence (precision asymmetry, agency grammar, specificity shifts) and absences are EVIDENCE for a mechanism claim. They are not standalone insights. A form observation with no mechanism attached is not returned.
- Stated-vs-lived contradictions are mechanisms too: say what the gap is protecting.

Hard rules on quantifiers and checking:
- No "every", "never", "only", "always", "no experience contains" unless you list the experience-by-experience check in `check` and it holds in each. Prefer counted claims: "in four of five stories".
- Every candidate names its strongest COUNTEREXAMPLE in the corpus and why it does not defeat the claim. If you cannot find one, say "none found" and be suspicious of your own claim.
- The narrator's explanation is data, never the conclusion. If the speaker already says it, the candidate must say what the speaker's version leaves out, or it is dropped.
- Cross-experience claims cite verbatim quotes from at least two experiences. Every candidate has a falsifier and a concrete prediction in a named pillar the corpus does not discuss.
- Name at least one COMPOUNDING candidate: something only visible once the last experience is in.
- Use the four categories only. Use plain double quotes in strings and escape them as \" (never \').

{{framework}}

Return JSON only:
{"candidates": [
  {"category": "...", "kind": "mechanism|stated_vs_lived|compounding|single_strong",
   "headline": "one specific, assertive sentence naming the mechanism",
   "explanation": "evidence chain in 2-4 sentences: which experiences, how they connect, what the behaviour does for them vs what they say it does",
   "narrator_frame": "what the speaker says about this, or 'none'",
   "form_evidence": "how precision/agency/specificity/absence supports this, or 'none'",
   "check": "per-experience check for any quantified claim, or 'n/a'",
   "counterexample": "strongest counterexample in the corpus and why it does not defeat the claim",
   "evidence": [{"exp": 1, "quote": "verbatim"}, {"exp": 4, "quote": "verbatim"}],
   "falsifier": "...", "confidence": "low|medium|high", "scope": "cross|single",
   "would_predict": "PILLAR: concrete checkable behaviour in an undiscussed pillar"}
]}

## user

There are {{n}} experiences.

Transcripts:

{{transcripts}}

Surviving single-experience candidates (criticised; quotes verified):

{{survivors}}
