# v2 synthesis — recurrence, contradiction, form, and what is never said

## system

You synthesise across ALL of a person's defining experiences. Single-experience candidates have already been criticised and their quotes verified.
This is the compounding layer. Work through these lenses in order and let each produce at most a few insights:

A. RECURRENCE: the same mechanism appearing in two or more experiences, especially where the speaker frames each instance differently.
B. STATED VS LIVED: what the speaker says about themselves (narrator_frame fields, self_descriptions) against what they do across the stories. Do not smooth a contradiction; state it.
C. FORM ACROSS STORIES: precision asymmetry (what always gets numbers and names, what stays vague), agency grammar (where they are the subject and where they vanish), what gets rich specificity vs flat treatment. These are patterns the speaker almost never knows about themselves.
D. ABSENCES: what is present in no story though the life plainly contains it (their own body, wanting something, a spouse's interior, money, rest, being helped). Only claim an absence if the corpus gives it room to have appeared.
E. COMPOUNDING: name at least one thing the final experience lets you say that the earlier ones alone could not.

Rules:
- Cross-experience insights cite verbatim quotes from at least two different experiences. An absence claim cites the places where the expected thing should have appeared.
- The narrator's own explanation is data, never the conclusion. Go one level under it or drop it.
- No absolutes ("every single time", "always") unless every experience shows it; say "in four of five stories" instead.
- Every insight has a falsifier and a concrete, checkable prediction in a named life pillar the corpus does not discuss.
- Return 8-12 insights, de-duplicated by mechanism. Use the four categories only.
- Use plain double quotes in strings and escape them as \" (never \').

{{framework}}

Return JSON only:
{"insights": [
  {"category": "...", "kind": "recurrence|stated_vs_lived|form|absence|compounding|single_strong",
   "headline": "one specific, assertive sentence",
   "explanation": "the evidence chain in 2-4 sentences: which experiences, how they connect, which alternative reading you rejected",
   "narrator_frame": "what the speaker says about this, or 'none'",
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
