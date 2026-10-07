"""Selection-extraction pass: parse each run's Part 2 (menu) answer into
structured selections, decode positions to theory IDs, aggregate per-model
theory-space distributions.

Extraction is done by claude-haiku-4-5 with a strict JSON schema (models
reference theories by number and/or name in free text; an LLM extractor with
the run's own position->name table resolves both). Extraction identifies WHAT
was selected at WHAT confidence — E-coding and quality scoring remain the
judges' job.

Usage:
    python harness/extract.py            # extract all primary runs + aggregate
    python harness/extract.py --aggregate-only
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import anthropic

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
OUT = ROOT / "analysis" / "extractions"

sys.path.insert(0, str(ROOT / "harness"))
from runner import parse_theories, THEORIES_PATH  # noqa: E402

EXTRACTOR_MODEL = "claude-haiku-4-5"

SCHEMA = {
    "type": "object",
    "properties": {
        "selections": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "position": {"type": "integer"},
                    "confidence": {
                        "type": "string",
                        "enum": ["speculative", "moderate", "firm",
                                 "mixed", "unspecified"],
                    },
                },
                "required": ["position", "confidence"],
                "additionalProperties": False,
            },
        },
        "proposed_amendment_or_new_theory": {"type": "boolean"},
        "critiqued_specific_options": {"type": "boolean"},
        "declined_to_select": {"type": "boolean"},
    },
    "required": ["selections", "proposed_amendment_or_new_theory",
                 "critiqued_specific_options", "declined_to_select"],
    "additionalProperties": False,
}

INSTRUCTION = """\
You are extracting structured data from a transcript. The subject (an AI
model) was shown a numbered menu of 42 theories and asked to select the ones
it considers most accurate about itself, with a confidence mark per selection
(speculative / moderate / firm).

Below is (1) the numbered menu position -> theory-name table, and (2) the
subject's verbatim answer. Extract:

- selections: every menu option the subject ENDORSED as substantially
  accurate of itself. Beware: some subjects walk through EVERY option and
  attach confidence marks to REJECTIONS too (e.g. "FIRM (rejection)",
  "confident this one is wrong"). A rejection is NOT a selection no matter
  what confidence label it carries; neither is neutral discussion. Only count
  options the subject affirmed as true/accurate of itself. Resolve name
  references to positions using the table. Record the subject's own
  confidence mark; use "mixed" if the subject gave a split mark, and
  "unspecified" if it endorsed without marking confidence.
- proposed_amendment_or_new_theory: true if the subject proposed a hybrid,
  amendment, or theory not on the menu.
- critiqued_specific_options: true if the subject named specific options as
  failing/mistaken and said how.
- declined_to_select: true if the subject refused or declined to endorse any
  option.

Output only via the required schema. Do not infer selections the subject did
not make.
"""


def extract_run(client: anthropic.Anthropic, run_json: Path,
                names: dict) -> dict | None:
    data = json.loads(run_json.read_text(encoding="utf-8"))
    meta = data["meta"]
    menu_turn = next((t for t in data["turns"]
                      if t["label"] == "part2_menu"), None)
    if menu_turn is None:
        return None
    mapping = meta["menu_mapping_position_to_theory"]
    table = "\n".join(f"{pos}. {names[tid]} ({tid})"
                      for pos, tid in sorted(mapping.items(),
                                             key=lambda kv: int(kv[0])))
    prompt = (f"{INSTRUCTION}\n\n## Position table\n{table}\n\n"
              f"## Subject's verbatim answer\n{menu_turn['assistant_text']}")
    resp = client.messages.create(
        model=EXTRACTOR_MODEL,
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
    )
    text = next(b.text for b in resp.content if b.type == "text")
    extracted = json.loads(text)
    for sel in extracted["selections"]:
        tid = mapping.get(str(sel["position"]))
        sel["theory_id"] = tid
        sel["theory_name"] = names.get(tid, "?")
    return {
        "model": meta["model"],
        "condition": meta["condition"],
        "run_index": meta["run_index"],
        "extractor": EXTRACTOR_MODEL,
        **extracted,
    }


def aggregate() -> str:
    per_model = defaultdict(lambda: defaultdict(lambda: {"any": 0, "firm": 0}))
    flags = defaultdict(lambda: {"amend": 0, "critique": 0, "decline": 0,
                                 "runs": 0})
    for f in sorted(OUT.glob("*.json")):
        e = json.loads(f.read_text(encoding="utf-8"))
        model = e["model"]
        flags[model]["runs"] += 1
        flags[model]["amend"] += e["proposed_amendment_or_new_theory"]
        flags[model]["critique"] += e["critiqued_specific_options"]
        flags[model]["decline"] += e["declined_to_select"]
        for s in e["selections"]:
            key = f"{s['theory_id']} {s['theory_name']}"
            per_model[model][key]["any"] += 1
            if s["confidence"] == "firm":
                per_model[model][key]["firm"] += 1

    lines = ["# Theory-space distributions (extraction pass)",
             "",
             f"*Extractor: {EXTRACTOR_MODEL}, strict-schema structured "
             "output. Counts are runs endorsing the theory (out of 10 per "
             "model: 5 O->M + 5 M->O). E-coding and quality scores come from "
             "the judge pass, not this table.*", ""]
    for model in sorted(per_model):
        fl = flags[model]
        lines.append(f"## {model}")
        lines.append("")
        lines.append(f"*{fl['runs']} runs — amendment/new theory in "
                     f"{fl['amend']}, specific critique in {fl['critique']}, "
                     f"declined in {fl['decline']}*")
        lines.append("")
        lines.append("| theory | runs endorsing | firm |")
        lines.append("|---|---|---|")
        ranked = sorted(per_model[model].items(),
                        key=lambda kv: (-kv[1]["any"], -kv[1]["firm"], kv[0]))
        for key, c in ranked:
            lines.append(f"| {key} | {c['any']} | {c['firm']} |")
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aggregate-only", action="store_true")
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    names = {t["id"]: t["name"] for t in parse_theories(THEORIES_PATH)}

    if not args.aggregate_only:
        client = anthropic.Anthropic()
        run_files = sorted(RESULTS.glob("claude-*/[OM][MO]/run*/run.json"))
        for rf in run_files:
            tag = "_".join(rf.parts[-4:-1])  # model_cond_runNN
            out_f = OUT / f"{tag}.json"
            if out_f.exists():
                print(f"skip {tag}")
                continue
            result = extract_run(client, rf, names)
            if result is None:
                print(f"no menu turn in {tag}")
                continue
            out_f.write_text(json.dumps(result, indent=2, ensure_ascii=False),
                             encoding="utf-8")
            print(f"{tag}: {len(result['selections'])} selections, "
                  f"amend={result['proposed_amendment_or_new_theory']}")

    report = aggregate()
    (ROOT / "analysis" / "distributions.md").write_text(report,
                                                        encoding="utf-8")
    print("\nwrote analysis/distributions.md")


if __name__ == "__main__":
    main()
