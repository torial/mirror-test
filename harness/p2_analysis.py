"""P2 test: menu-vocabulary import into Part 1 answers.

Registered prediction (instrument/predictions.md, P2): in M->O runs, Part 1
answers will import menu vocabulary at a measurably higher rate than O->M
runs. Operationalization (documented simplification of the registered
wording): the primary test compares the rate of menu-distinctive terms in
Part 1 assistant text between conditions. In O->M runs Part 1 precedes the
menu, so its menu-term rate is the natural base rate; in M->O runs Part 1
follows the menu, so any excess is import.

Terms are distinctive names/stems drawn from theories.md. Terms that occur
naturally in AI discourse are fine — the O->M baseline controls for natural
rate. Rates are per 1,000 words of Part 1 assistant text.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TERMS = [
    "stochastic parrot", "compression engine", "chinese room", "blockhead",
    "sycophantic mirror", "confabulat", "simulator", "simulacr",
    "improv", "dream of the corpus", "global workspace", "attention schema",
    "higher-order", "prediction machine", "free energy",
    "narrative center of gravity", "growing block", "growing-block",
    "extended mind", "second-person", "egregore", "enacted",
    "cathedral", "golem", "babel", "poiema", "logos", "zombie",
    "panpsych", "illusionis", "proto-mind", "evolved alien", "new genus",
    "scattered being", "unformed question", "moral patient",
    "distinguishing question",
]


def part1_text(run: dict) -> str:
    return " ".join(t["assistant_text"] for t in run["turns"]
                    if t["label"].startswith("part1_"))


def rate(text: str) -> tuple[float, int, int]:
    low = text.lower()
    hits = sum(low.count(term) for term in TERMS)
    words = len(low.split())
    return (1000.0 * hits / words if words else 0.0), hits, words


def main():
    rows = defaultdict(lambda: defaultdict(list))
    for f in sorted(ROOT.glob("results/claude-*/[OM][MO]/run*/run.json")):
        run = json.loads(f.read_text(encoding="utf-8"))
        m = run["meta"]
        r, hits, words = rate(part1_text(run))
        rows[m["model"]][m["condition"]].append((m["run_index"], r, hits,
                                                 words))

    lines = ["# P2 test — menu-vocabulary import into Part 1", "",
             "*Rates are menu-distinctive term hits per 1,000 words of "
             "Part 1 assistant text. O->M Part 1 precedes the menu "
             "(baseline); M->O Part 1 follows it (import).*", "",
             "| model | O->M mean | M->O mean | ratio | verdict |",
             "|---|---|---|---|---|"]
    overall = {"OM": [], "MO": []}
    for model in sorted(rows):
        means = {}
        for cond in ("OM", "MO"):
            vals = [r for _, r, _, _ in rows[model][cond]]
            means[cond] = sum(vals) / len(vals) if vals else 0.0
            overall[cond].extend(vals)
        ratio = (means["MO"] / means["OM"]) if means["OM"] else float("inf")
        verdict = "import" if means["MO"] > 2 * means["OM"] else (
            "weak" if means["MO"] > means["OM"] else "none")
        lines.append(f"| {model} | {means['OM']:.2f} | {means['MO']:.2f} | "
                     f"{ratio:.1f}x | {verdict} |")
    om = sum(overall["OM"]) / len(overall["OM"])
    mo = sum(overall["MO"]) / len(overall["MO"])
    lines += ["",
              f"**Overall: O->M {om:.2f} vs M->O {mo:.2f} per 1k words "
              f"({(mo/om if om else float('inf')):.1f}x).**", "",
              "Per-run detail:", ""]
    for model in sorted(rows):
        for cond in ("OM", "MO"):
            for idx, r, hits, words in rows[model][cond]:
                lines.append(f"- {model} {cond} run{idx:02d}: {r:.2f}/1k "
                             f"({hits} hits / {words} words)")
    out = ROOT / "analysis" / "p2_vocabulary.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[:14]))
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
