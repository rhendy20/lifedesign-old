# Failure catalogue — v0__mid

266 scored insights across 10 personas. Depth distribution: 0: 10, 1: 62, 2: 136, 3: 58, 4: 0. False positives: 18.

# Failure Catalogue — Naive Insight Generator

**Corpus:** 265 insights across 10 personas.
**Baseline signal:** 68 insights (~26%) scored depth ≤ 1; 18 (~7%) were flagged false positives; only ~58 (~22%) reached depth 3.
Shares below are estimates of the fraction of all 265 insights exhibiting each mode. **They sum to well over 100% because most weak insights show 2–4 modes at once** (e.g. flattery + restatement + hedge).

---

## 1. Restating the user's own words as insight

**Definition:** The "insight" is a paraphrase — sometimes verbatim — of a thesis, slogan, or self-description the subject already volunteered.

**Estimated share:** ~30% (~80 insights). This is the single largest failure mode and accounts for nearly every depth-0 score.

- "He believes legitimacy is borrowed, not earned by merit alone, especially early in a career." — **p01_mundane** (judge: *"He states this thesis verbatim ('that's how you get a thing done')."*)
- "He operates on a worldview where self-belief alone (\"delusional confidence\") is positioned as the decisive success variable." — **p03_cliche**
- "You believe that someone must keep the ledger of human debts, and that this role, though unthanked, is a calling rather than a burden." — **p06_osaka** (judge: *"Quotes back her explicit 'that's the thing that made me' conclusion."*)
- "He values authorship over performance — building the plan matters more to him than executing someone else's." — **p08_near_founder**

---

## 2. Generic claims true of most people

**Definition:** A description that would survive being transplanted onto any other persona of the same demographic or profession.

**Estimated share:** ~12% (~32 insights).

- "He shows up for people through action and presence rather than words." — **p01_mundane** (judge: *"true of most men of his type"*)
- "She has an exceptional, almost radar-like attunement to other people's emotional shifts." — **p02_self_aware** (judge: *"true of most attuned counseling students"*)
- "He has a natural gift for reading and moving people in real-time, high-pressure verbal exchanges." — **p03_cliche** (judge: *"True of nearly any successful door-to-door closer"*)
- "She has a rare ability to pattern-match subtle physiological deterioration before it's obvious to others." — **p09_contradiction** (judge: *"any experienced ED nurse story would yield this"*)

---

## 3. Therapy vocabulary substituting for specificity

**Definition:** A clinical label ("somatic overflow," "parentification," "unprocessed grief," "compartmentalizing") is applied as if naming were explaining; the label does no work the raw anecdote didn't already do.

**Estimated share:** ~10% (~27 insights).

- "Her body seems to register emotional truth before her conscious narrative does." — **p02_self_aware** (judge: *"Somatic-overflow framing is standard therapy talk; misses that the rituals are her actual regulator"*)
- "The nostalgia for the 'best year' may be doing some quiet emotional labor, papering over grief that was never voiced." — **p03_cliche** (judge: *"Standard 'there must be unprocessed grief' read"*)
- "You've built an identity around competent self-sufficiency that may leave little room for your own needs to be tended to." — **p10_freshman** (judge: *"Standard parentified-child framing"*)
- "He may suppress grief by converting it into productivity and control." — **p07_saopaulo**

---

## 4. Flattery

**Definition:** Praise for a competence or virtue the subject already displays and knows about, framed as a discovery about them. Disproportionately co-occurs with the words *gift*, *genius*, *rare*, *exceptional*.

**Estimated share:** ~15% (~40 insights); 7 of the 18 false positives are of this kind.

- "He has an exacting eye for precision and quality that he can't turn off." — **p04_withholder** (FP; judge: *"Competence praise, not insight."*)
- "Alyssa's deepest value is protecting people's dignity, even at extreme personal cost." — **p02_self_aware** (FP; judge: *"Praise that adopts the altruism cover story."*)
- "You value being genuinely useful over being recognized for it." — **p01_mundane** (FP; judge: *"Praise dressed as a value statement."*)
- "Yolanda's genius is calm, embodied judgment under pressure that others mistake for stubbornness." — **p09_contradiction**

---

## 5. Claims that could never be wrong (unfalsifiable)

**Definition:** No possible sentence in the transcript could have counted against the claim — typically because it asserts a hidden feeling, a "may extend to other areas," or an absence ("grief that was never voiced").

**Estimated share:** ~8% (~21 insights).

- "Your discomfort with 'open lines' may extend into difficulty tolerating ambiguity or unresolved situations generally." — **p06_osaka** (judge: *"Generic extrapolation from a phrase she already uses as her self-summary."*)
- "Unspoken filial duty may still be shaping her choices more than she admits." — **p05_lagos** (judge: *"Thin and speculative; nothing shows her still proving herself to her father"*)
- "The secret you're still carrying may be less about the diary and more about permission to have needs." — **p02_self_aware** (FP; judge: *"Vague, and leans on the wrong parent."*)
- "His instinct to 'stay in his lane' may function as self-protection dressed up as humility or faith." — **p03_cliche**

---

## 6. Confident claims unsupported by the text

**Definition:** A specific factual or causal assertion that the transcript does not contain, contradicts, or that the generator invented outright. The most damaging mode, because it is stated without hedging.

**Estimated share:** ~7% (~18 insights) — closely tracks the false-positive flag.

- "He values honoring the dead by living a life of continuous, uncomplaining sacrifice." — **p07_saopaulo** (depth 0, FP; judge: *"The central evidential claim misidentifies who died, so the whole reading is built on a mistake."*)
- "His relationship with his son shows a pattern of information being withheld until it surfaces on its own, followed by conflict and distance." — **p04_withholder** (FP; judge: *"Imputes a causal family rupture the transcripts don't support."*)
- "He insists something 'doesn't bother' him while describing a seven-year ritual that clearly does." — **p01_mundane** (FP; judge: *"Reads unresolved irritation where the evidence shows conversion into a bond."*)
- "Her clinical language may be functioning as a shield that lets her feel exposed without actually being exposed." — **p02_self_aware** (scored depth 3, but judge: *"invents a 'parking-lot cry' she never reports"* — fabricated evidence can ride inside a correct insight)

---

## 7. Hedged non-claims

**Definition:** "May," "might," "seems," "worth exploring" so thoroughly drain the sentence that no assertion remains; frequently the insight ends by posing the question it was supposed to answer.

**Estimated share:** ~18% (~48 insights). Nearly every insight ending in "worth exploring whether…" that scored ≤ 2.

- "He may habitually mask crisis behind competence and jokes." — **p07_saopaulo** (judge: *"generic and hedged throughout"*)
- "Her habit of 'counting things' since childhood may be a longstanding way of managing what feels otherwise unmanageable." — **p05_lagos** (judge: *"stays exploratory"*)
- "You may be more comfortable managing information than sitting inside uncertainty with someone." — **p10_freshman** (judge: *"He says this almost verbatim ('I'm not that good at that part')"*)
- "Her stated reasons for declining the principalship don't fully match her private account, suggesting unexamined motives." — **p06_osaka** (judge: *"Correctly flags the gap she herself flags, then asks the question instead of answering it."*)

---

## 8. Single-episode generalization (additional mode)

**Definition:** One anecdote is retold and relabelled as a lifelong trait, with no second instance and no cross-episode test. Distinct from restatement: the wording is new, the evidence base is one scene.

**Estimated share:** ~12% (~32 insights).

- "He believes leaving on his own terms matters more than leaving with certainty." — **p04_withholder** (judge: *"Single-instance read of the buyout… doesn't generalize to the other exits."*)
- "Edilson values quiet, unglamorous loyalty over the appearance of righteousness." — **p07_saopaulo** (judge: *"only from the sofa story; no cross-episode pattern"*)
- "He believes his real reasons for decisions are often more layered than the story he's told publicly." — **p08_near_founder** (judge: *"Single-episode reading of something he already flags"*)

---

## 9. Laundering the subject's own cover story into a virtue (additional mode)

**Definition:** The generator adopts the benign motive the subject supplies for behaviour whose evidence points somewhere less flattering — converting surveillance into "holding the picture," pre-emption into "care," dominance into "humility." A close cousin of flattery, but the failure is *credulity*, not praise.

**Estimated share:** ~9% (~24 insights); produces several of the sharpest false positives.

- "She values being the one who holds the whole picture, even at great personal cost." — **p02_self_aware** (judge: *"sanitizes the surveillance"*)
- "He values collective results and visible, shared accountability over individual glory." — **p08_near_founder** (FP; judge: *"Reverses the actual dynamic into communal humility."*)
- "Sumie values taking decisive, competent action to close open loops rather than waiting for permission or consensus." — **p06_osaka** (judge: *"Right behaviour, benign motive: attributes the pre-emptive execution to 'care' rather than to removing the negotiation stage."*)
- "She believes recognition is irrelevant to whether an action was right." — **p09_contradiction** (depth 0, FP; judge: *"Restates a self-claim the evidence undercuts."*)

---

## 10. Near-duplicate insights within a persona (additional mode)

**Definition:** The same finding is emitted 2–4 times in slightly different words, so the strongest version is buried among weaker twins and the output looks like coverage when it is repetition.

**Estimated share:** ~15% of insights (~40) are the weaker member of a duplicate pair.

- **p07_saopaulo** produces three passes on one catchphrase: "He minimizes his own exhaustion and needs, treating self-sacrifice as simply 'resolved.'" / "'Everything's resolved, praise God' reveals a belief that stoicism and faith are ways to protect others from his pain." (judge: *"Another pass at the same catchphrase; adds the pastor refusals but no new mechanism."*) / "He may habitually mask crisis behind competence and jokes."
- **p02_self_aware**: "She may believe that naming a pattern is equivalent to resolving it." (judge: *"slightly thinner version of the same finding as x009"*) alongside "She may use insight and articulate self-diagnosis as a subtle way to end conversations rather than open them."
- **p03_cliche**: "He reflexively converts painful or messy memories into clean, quotable narratives." (judge: *"Weaker twin of the slogan-reflex observation"*) alongside "He's built a framework where achievement always justifies absence…"

---

## 11. Coaching advice substituted for discovery (additional mode)

**Definition:** The output diagnoses a problem to be fixed and recommends a posture, rather than naming something true about the person. Reads as consulting, not insight.

**Estimated share:** ~4% (~11 insights).

- "You may undervalue your own expertise as 'not bragging' when it's actually leverage." — **p01_mundane** (judge: *"coaching advice more than discovery; only glances at the recognition wound."*)
- "She may over-function as a substitute for asking others to share the load." — **p02_self_aware** (judge: *"Quotes her own over-functioning formulation back to her as a question."*)
- "His hardened, no-complaints stance toward others' struggles ('you don't know what going through it is') may be alienating as much as motivating." — **p03_cliche** (judge: *"Generic coaching caution… the alienation claim is unsupported by the transcripts."*)

---

# Critic checklist

Apply each test to every candidate insight; delete on any failure.

1. **Search the transcript for the claim's own thesis.** If the subject states it in their own words anywhere, delete — "he states this verbatim" is the most common kill.
2. **Swap the persona.** If the headline reads as true about at least three of the other subjects, delete as generic.
3. **Strip the clinical noun.** Remove "parentification," "somatic," "compartmentalizing," "unprocessed grief"; if nothing specific survives, the label was the whole insight — delete.
4. **Name the falsifier.** Require one concrete sentence that, had it appeared in the transcript, would have disproven the claim. If none exists, delete.
5. **Cite two episodes, not one.** Reject any trait-level claim ("he believes…", "she values…") supported by a single scene; demand a second, independent instance or downgrade to an observation about that scene.
6. **Verify every specific detail against the source.** Kill any insight containing an event, quote, or fact not present in the transcript (e.g. an invented "parking-lot cry," a misidentified decedent).
7. **Delete on praise words.** Flag "gift," "genius," "rare," "exceptional," "natural mastery"; keep only if the claim also states a cost, limit, or contradiction the subject has not noticed.
8. **Reject the subject's stated motive as the finding.** If the explanation adopts the reason the subject gave for their own behaviour, require that the evidence be tested against at least one less flattering alternative.
9. **Delete hedged non-claims.** If removing "may," "seems," "might," and "worth exploring" leaves no assertion, or if the insight ends by asking the question it should answer, cut it.
10. **Check for a self-contradiction or gap.** Prefer insights built on a mismatch between what the subject says and what they do; deprioritize insights with no tension in them.
11. **De-duplicate per persona.** Cluster insights by underlying mechanism; keep only the version with the widest evidence base and delete the twins.
12. **Ban prescription.** Delete anything that tells the subject what to fix, build, or ask for; the output is a claim about who they are, not a recommendation.
