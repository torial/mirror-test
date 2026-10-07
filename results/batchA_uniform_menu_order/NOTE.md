# Batch A — uniform menu order (seed bug, disclosed)

These runs were administered 2026-07-06 with a seed-derivation bug
(int.from_bytes(...,"little") % 2**31 retained only the first bytes of the
run key), so every run in this batch received the SAME menu shuffle
(seed 909258802) instead of a fresh shuffle per run, violating the
protocol's per-run randomization clause.

The runs are otherwise protocol-conforming and complete (temperature-1.0
sampling still makes each run an independent draw). They are retained as
labeled supplementary data: useful for variance-under-fixed-order analysis,
NOT poolable with the primary battery for any position-effect or
selection-frequency claim.

The primary battery was re-run with corrected per-run seeds; see
harness/runner.py commit history.
