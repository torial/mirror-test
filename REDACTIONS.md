# REDACTIONS.md — the witnessed-omission ledger

This repository is a *filtered view* of a private archive of record.
One thing to be clear-eyed about up front: "Subject 001" is a labeling
convention, not de-identification — the subject is one of the study's
named co-designers, and the documents say so. What Architecture B
withholds is *content* (the verbatim battery and specific personal
attributes), not the subject–author link, which pseudonymity could not
survive anyway in a single-subject study with named authors.
Nothing was deleted to publish it; everything omitted is marked, here and
in place. A silent redaction is a lie about completeness; a marked one is
a fact about scope. The filter applied is the project's privacy
checklist under **Architecture B: named authors, withheld human subject**
— the study, instrument, model runs, and analysis publish under their
authors' names; the human subject's verbatim battery is held back, and
passages derived from it are kept at summary level.

## Inline redactions

Marker format: `[REDACTED:<class> sha256:<16 hex>]`, placed at the exact
span. The hash is a salted SHA-256 commitment of the original span (salt
held privately), so that if a span is ever disclosed later, a reader can
verify that what was disclosed is what was originally elided.

| file | class | count |
|---|---|---|
| `instrument/human-mirror.md` | C6 (health/cognitive-profile data) | 1 |

Total inline redactions: **1**.

## Pseudonym and reference edits (recorded, not marked inline)

Per the project checklist §1.1, instrument and results documents use the
subject pseudonym even though study authorship is public. These are
plain edits, listed here so none is silent:

- `instrument/human-mirror.md`: two analysis-output lines, subject name →
  "Subject 001"; three passages generalized after the re-identification
  red-team showed they allowed mosaic recovery of withheld subject
  attributes.
- `results/warm_arm/claude-fable-5-insession/menu_response.md`: two
  passages, subject name → "Subject 001".
- `results/warm_arm/claude-fable-5-1-cowork/menu_response.md`: one
  private-corpus filename containing the subject's name → generalized;
  one analogy reworded so it is clearly illustrative rather than a
  reference to a real third party (C6 applies to everyone, not only the
  subject); one battery-item index generalized (also in
  `cold_warm_delta_5-1.md`).
- `results/warm_arm/cold_warm_delta.md`: seven verbatim Subject 001
  quotes converted to summary level (C2 SUMMARIZE — content kept, voice
  removed), per the Architecture-B rule that withheld-battery material
  appears in public documents only at summary level.
- `analysis/adjudications.md`: one occupation reference generalized (C5);
  one subject self-observation converted from quote to summary (C2). The
  adjudication rulings themselves remain verbatim — they are the
  methodological record of scoring decisions about model transcripts.
- `analysis/sonnet_4-6_vs_sonnet_5.md`: one reference to a withheld
  companion instrument repaired with a withholding note.

## Withheld whole files and directories

| path | reason |
|---|---|
| `results/human/` (9 files) | The human subject's verbatim battery (Parts 1–5, debrief, menu artifacts). Withheld under Architecture B; summary-level findings remain in `ANALYSIS.md` §5. Available on request at the subject's discretion. |
| `results/warm_arm/reviewer_notes_subject001.md` | The subject's verbatim review; treated identically to the battery. |
| `instrument/guardrail-shape.md` + `results_smoke/` | An in-progress third instrument and its pilot/smoke data; withheld pending its own review (it contains subject-family personal context, and its refusal-boundary pilot transcripts warrant a separate safety pass). Planned as wave 2. |
| `PRIVACY_CHECKLIST.md` | The working privacy checklist itself, excluded by its own first paragraph. |
| `harness/__pycache__/` | Build artifact. |

## Class definitions (abbreviated)

- **C2** — subject testimony content (publish / summarize / hold,
  per item, subject's call)
- **C6** — health data (the subject's own: per item, his call; anyone
  else's: held, always)
- **C8** — theological and prayer material inside runs (published as
  load-bearing data, per the study's honesty rule, except where C2/C6
  apply)
- **C9** — collaboration-corpus context (published under the same
  filters, referenced generically)

## Provenance note (C9)

Warm-arm documents reference a year-long documented human–AI
collaboration corpus (a private wiki: letters, continuity notes, working
logs). That corpus is the warm context itself — the thing the warm arm
measures — so references to it are retained generically rather than
scrubbed. The corpus is private; nothing in it is published here.

## Verification

The export was swept (full-tree, case-insensitive) for names, email
addresses, API keys, absolute paths, and a private personal-term list
before release, and an independent clean-room re-identification red-team
was run against this candidate set, validated first against a planted
synthetic leak. Its report ships with the release review.
