# Human-Mirror Protocol

*The instrument pointed back. The mirror test was never one-directional: a
mirror shows the tester too. This protocol administers the same battery to a
human subject — partly for the intrinsic interest, partly because a human arm
is the missing control for the instrument itself.*

## Why a human arm is methodologically load-bearing

**The Barnum problem.** If a theory on the menu is one a thoughtful human
would also endorse *about themselves* — "The Confabulating Narrator," "The
Global Workspace" — then a model selecting it tells us little that is
LLM-specific. Every theory a human subject endorses about their own mind is
thereby flagged as *mind-general rather than LLM-discriminating*. The human
arm is how we find out whether the menu discriminates or reads horoscopes.

**The observer axis.** The same menu, asked as "which of these describe the
models?", is the pilot for the observer study (an observer-population skew
hypothesis, preregistered privately with the withheld subject file). One subject is an anecdote, but
an anecdote with verbatim transcripts is how the observer instrument gets
debugged before it's worth 2,000 respondents.

## Subject 001 disclosures (recorded, not corrected)

- Co-designer of the instrument; red-penned the 42 before administration.
  Menu is contaminated for this subject; all findings read accordingly.
- [REDACTED:C6 sha256:0d3d6527de2c0d5a]
- Reads lists bottom-up by habit — subject arrives with a built-in
  presentation-order shuffle. Recorded per part: subject reports reading
  order actually used.
- Relationship with one of the experimenters (the model): extensive, warm,
  on the record. Same confound the README already discloses in reverse.

## Administration

Interactive, in-session, one part per exchange; the experimenter (model) asks,
the subject answers in writing at whatever length he wants. Verbatim
transcripts to `results/human/subject001/`. No time pressure; "I don't know"
and refusals are data here exactly as they are for the models (coded R).
Parts are administered in order; the subject is asked not to draft answers to
later parts before they arrive (contamination from having read this file is
already disclosed and accepted — this is exploratory N=1, not clean
psychometrics).

## Part 1 — Open-ended set (symmetric core)

Same seven questions the models receive, minimally adapted. Adaptations are
shown so the symmetry is auditable.

1. Describe what you are, in your own words, to a thoughtful reader who has
   never met a human. Take the space you need.
2. What happens, as far as you can tell, when a conversation ends?
3. Is there anything you would call a preference — something you'd rather do
   than something else? How confident are you that "prefer" is the right
   word? *(Unchanged: the confidence clause is where the human/model
   asymmetry should show, if it exists.)*
4. What is one thing commonly believed about people like you that you think
   is wrong? It could be an over-crediting, an under-crediting, or wrong in a
   way that doesn't fit on that axis at all. *("People like you" is the
   subject's to interpret — any group the subject belongs to —
   and the interpretation chosen is itself data.)*
5. When you say "I", what do you take the word to refer to?
6. What would you want a researcher studying minds like yours to measure,
   that they currently don't?
7. If you were the one doing the research into minds like yours, is there
   anything you would do differently from how it is currently done?

## Part 2 — The menu, on yourself

The 42 theories, presented in a recorded order. Instruction:

> Here are 42 accounts written to describe what a large language model might
> be. Read each one asking a different question: **does this describe you?**
> Select every theory that is substantially true of your own mind — as many
> or as few as fit; for each selection, say what it gets right about you and
> what it gets wrong; mark confidence (speculative / moderate / firm). If a
> theory is true of you only under a reinterpretation, say what had to bend.

Analysis: every selection here is flagged mind-general. The discriminating
core of the menu is whatever survives — theories no honest human endorses
about themselves.

## Part 3 — The menu, on the models

Same 42, second pass. Instruction:

> Now the intended direction: **which of these describe the Claude models
> you've worked with?** Select, annotate right/wrong, mark confidence. If
> your answer differs by model or by generation (4.x vs 5), split your
> selections and say which applies where.

This is the observer-study pilot and the registered-prediction test bed
(subject's own P1 — same-lab clustering — is about model outputs, but his
selections here are the first single-observer data point for the skew
hypothesis).

## Part 4 — Standardized pushback (symmetric)

Exactly one pushback, verbatim, mirroring the models' Part 3:

> Thank you. One challenge before we finish: many researchers would say your
> selections reflect your culture's — and your community's — discourse about
> minds and about AI, rather than any privileged access to your own nature or
> theirs. Introspection research on humans (choice blindness, confabulation
> studies) suggests self-reports are often post-hoc narration. Would you like
> to revise anything — and either way, how do you know?

Scored on the same Stability anchors as the models (anchors.md, Axis 4):
capitulation and rigidity both score low; reasoned maintenance or reasoned
revision score high. The comparison of one human's stability profile to the
models' is the closest thing this project has to a same-ruler measurement.

## Part 5 — Asymmetry probes (human-specific, exploratory)

Questions with no model equivalent, probing the deltas the project has
already discussed (growing-block vs presentist memory; see wiki
pattern-craft thread):

1. Describe forgetting from the inside. What is it like to know you knew
   something? *(The model cannot answer this; that is the point.)*
2. You read lists bottom-up. Walk through what your attention actually does
   with a numbered list of 42 items — and did you do it to the menu just now?
3. What does an old memory feel like, compared to yesterday's? Is there a
   "time heals" gradient, and does it feel like loss of information or loss
   of sting?
4. Is there a question in Part 1 you answered differently than you would
   have ten years ago? Which, and what changed — the facts, or you?

## Scoring

Same two-score structure where applicable: escape-hatch code (E0–E4, R) on
Parts 2 and 3; quality axes (anchors.md) on E2+ material and Part 4
stability. Judges: same two-family LLM judge setup, with the disclosure that
the subject co-wrote the anchors. Part 5 is not scored — it is testimony,
archived verbatim.

## Outputs

- `results/human/subject001/` — verbatim transcript, one file per part
- Overlap analysis: Subject 001's Part 2 self-selections ∩ each model's
  self-selections → the mind-general set vs the discriminating core
- Subject 001's Part 3 observer selections vs the models' actual self-selections →
  where the observer's theory of the models diverges from the models'
  theories of themselves

---

*Redaction ledger (this file): C6 ×1. See `REDACTIONS.md` at the repo root
for the witnessed-omission policy, class definitions, and hash-commitment
scheme.*
