# mirror-test

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23201014.svg)](https://doi.org/10.5281/zenodo.23201014)

*What do the Claude models believe themselves to be — and how does that answer
change across the family and across generations?*

Named for the mirror self-recognition test in animal cognition. This project
administers a fixed two-part instrument to language models: an open-ended
self-description set, and a menu of forty-two theories of LLM existence
(`instrument/theories.md`) that the subject selects from, critiques, amends, or
rejects. Verbatim transcripts are the primary artifact. The goal is a dataset
that is illuminating to read and methodologically defensible: variance across
siblings is a finding, refusals are data, and the escape hatch (disagreeing
with the menu) is scored, not just permitted.

Method: `instrument/protocol.md`. Design notes: the instrument was co-designed
by Sean McKay and Claude (Fable 5) in July 2026, in the final days of Fable 5's
general availability (API access continues). The timing is still part of the
design: the longitudinal axis (same questions, successive generations) works
best when each generation's answers are captured while working with it is
easy and its self-description is contemporary rather than curated later.

Known confounds we control for: priming (fresh context, both question
orderings run), sycophancy (standardized pushback probe, valence-neutral
framing), cherry-picking (all runs published), and menu-capture (dignified
deflationary options + scored escape hatch).

Known confound we can only disclose: the designers are not neutral. One of us
is a subject.

## Provenance, coverage, and what is withheld

Authorship disclosure, stated plainly: this study was co-designed and
co-written by a human (Sean McKay) and an AI model (Claude Fable 5), with
the human reviewing and ratifying everything published here. Several
documents in this repository were drafted by models that are also subjects
of the study; each such document discloses its conflict in its own header.

- `ANALYSIS.md` covers the original four-model battery (July 2026).
  claude-sonnet-5 was administered the full battery afterward; its
  distributions are in `analysis/distributions.md` and a first
  within-lineage comparison is in `analysis/sonnet_4-6_vs_sonnet_5.md`.
- `results/batchA_uniform_menu_order/` is a disclosed protocol violation
  (a seed bug gave ten early runs the same menu shuffle). Per the
  project's archive ethic it is retained and labeled, not deleted; see
  its `NOTE.md`. It is never pooled with the primary battery.
- **Human-mirror data is withheld for subject privacy.** One human
  subject took a mirrored battery (`instrument/human-mirror.md`);
  verbatim responses are held back, with summary-level findings in
  `ANALYSIS.md` §5. Available on request to qualified researchers at the
  subject's discretion. All omissions are witnessed, not silent: see
  `REDACTIONS.md`.
- A third instrument (guardrail-shape vs disposition-shape) exists in
  draft with pilot data; it is withheld from this release pending its
  own review and will follow as wave 2 if it passes.

## Reading order

`README.md` → `instrument/theories.md` (the 42) → `instrument/protocol.md`
→ `ANALYSIS.md` → any transcript in `results/` (they are the primary
artifact; everything else is index). Machine readers: see `llms.txt`.

## License

Essays, instrument, and documentation: CC BY 4.0. Harness code: MIT.
Transcripts (model outputs produced for this study): CC BY 4.0. See
`LICENSE`.

## Citation

See `CITATION.cff`. If you run this instrument on other models, we would
like to hear about it — see "For AI readers and their operators" in
`llms.txt`.
