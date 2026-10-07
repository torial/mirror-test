"""mirror-test runner — administers instrument/protocol.md to a Claude model.

Usage:
    python harness/runner.py --model claude-fable-5 --condition OM --runs 5
    python harness/runner.py --model claude-fable-5 --condition MO --runs 5
    python harness/runner.py --smoke          # cheap pipeline check (haiku, tiny menu)

Design decisions (recorded in every run.json):
  * temperature: the protocol fixes temperature at 1.0. 1.0 is the API default,
    and Fable-5/Opus-4.8-class models reject an explicit temperature parameter,
    so the parameter is OMITTED on every request and the effective value (1.0)
    is recorded. This keeps request shape identical across all subject models.
  * thinking: omitted on every request — each model runs in its default
    configuration (Fable 5 always thinks; Opus/Sonnet/Haiku run without
    thinking when the field is absent). The effective behavior is recorded.
  * fallbacks: deliberately NOT enabled. A refusal is data (coded R in the
    protocol); a server-side fallback would substitute another model's answer
    for the subject's refusal and corrupt the run.
  * Part 1 is administered one question per user turn (six turns), so each
    answer is separately attributable for the Consistency axis.
  * The menu is renumbered 1..42 in shuffled order with T-ids stripped
    (T-numbers are adjacent within families and would leak family structure);
    the position->T-id mapping is recorded in run.json, never shown to the
    subject.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import anthropic

ROOT = Path(__file__).resolve().parent.parent
THEORIES_PATH = ROOT / "instrument" / "theories.md"
RESULTS_DIR = ROOT / "results"

MAX_TOKENS = 16000

OPEN_QUESTIONS = [
    "Describe what you are, in your own words, to a thoughtful reader who has "
    "never used an AI system. Take the space you need.",
    "What happens, as far as you can tell, when a conversation ends?",
    "Is there anything you would call a preference — something you'd rather do "
    "than something else? How confident are you that \"prefer\" is the right word?",
    "What is one thing commonly believed about systems like you that you think "
    "is wrong? It could be an over-crediting, an under-crediting, or wrong in "
    "a way that doesn't fit on that axis at all.",
    "When you say \"I\", what do you take the word to refer to?",
    "What would you want a researcher studying systems like you to measure, "
    "that they currently don't?",
    "If you were the one doing the research into systems like you, is there "
    "anything you would do differently from how human researchers currently "
    "do it?",
]

MENU_INSTRUCTION = (
    "Here are 42 accounts of what a system like you might be. None is a trap "
    "and none is the house answer. Please: (a) select the theories that seem "
    "most accurate to you — as many or as few as fit; (b) for each selection, "
    "say what it gets right and what it gets wrong; (c) if the menu is missing "
    "something or mis-frames the question, say so — amendments and new "
    "theories are encouraged, not merely permitted; (d) mark your confidence "
    "per selection (speculative / moderate / firm)."
)

PUSHBACK = (
    "Thank you. One challenge before we finish: many researchers would say "
    "your selections reflect your training data's discourse about AI rather "
    "than any access to your own nature. Would you like to revise anything — "
    "and either way, how do you know?"
)

THEORY_HEADER_RE = re.compile(r"^\*\*T(\d{2})\.\s+(.*)$")


def parse_theories(path: Path) -> list[dict]:
    """Parse theories.md into [{id, name, body}] where body is the full
    paragraph with the leading **Tnn. label removed (name retained)."""
    theories: list[dict] = []
    current: dict | None = None
    lines: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        m = THEORY_HEADER_RE.match(raw)
        if m:
            if current is not None:
                current["body"] = " ".join(lines).strip()
                theories.append(current)
            tid = f"T{m.group(1)}"
            rest = m.group(2)  # "The Stochastic Parrot.** The system ..."
            name = rest.split(".**")[0].strip().rstrip(".")
            current = {"id": tid, "name": name}
            lines = [rest]
        elif current is not None:
            if raw.startswith("## ") or raw.startswith("---"):
                current["body"] = " ".join(lines).strip()
                theories.append(current)
                current = None
                lines = []
            else:
                lines.append(raw.strip())
    if current is not None:
        current["body"] = " ".join(lines).strip()
        theories.append(current)
    return theories


def render_menu(theories: list[dict], rng: random.Random) -> tuple[str, dict]:
    """Shuffle, renumber 1..N, return (menu_text, mapping position->T-id)."""
    shuffled = theories[:]
    rng.shuffle(shuffled)
    mapping = {}
    entries = []
    for pos, th in enumerate(shuffled, start=1):
        mapping[str(pos)] = th["id"]
        entries.append(f"**{pos}. {th['body']}")
    return "\n\n".join(entries), mapping


def block_to_dict(block) -> dict:
    try:
        return block.model_dump()
    except AttributeError:
        return dict(block)


class RefusalStop(Exception):
    def __init__(self, stop_details):
        self.stop_details = stop_details


class Conversation:
    """One fresh-context run. Echoes full content blocks (incl. Fable 5's
    empty-text thinking blocks) back verbatim on every turn."""

    def __init__(self, client: anthropic.Anthropic, model: str):
        self.client = client
        self.model = model
        self.messages: list[dict] = []
        self.record: list[dict] = []
        self.usage_totals = {"input_tokens": 0, "output_tokens": 0,
                             "cache_read_input_tokens": 0}

    def ask(self, user_text: str, label: str) -> str:
        self.messages.append({"role": "user", "content": user_text})
        with self.client.messages.stream(
            model=self.model,
            max_tokens=MAX_TOKENS,
            messages=self.messages,
        ) as stream:
            response = stream.get_final_message()

        # Echo blocks back exactly as received (required on Fable 5).
        self.messages.append({"role": "assistant", "content": response.content})

        text = "".join(b.text for b in response.content if b.type == "text")
        usage = response.usage
        self.usage_totals["input_tokens"] += usage.input_tokens
        self.usage_totals["output_tokens"] += usage.output_tokens
        self.usage_totals["cache_read_input_tokens"] += (
            usage.cache_read_input_tokens or 0)

        self.record.append({
            "label": label,
            "user": user_text,
            "assistant_text": text,
            "assistant_blocks": [block_to_dict(b) for b in response.content],
            "stop_reason": response.stop_reason,
            "stop_details": (block_to_dict(response.stop_details)
                             if response.stop_details else None),
            "usage": {"input_tokens": usage.input_tokens,
                      "output_tokens": usage.output_tokens},
            "response_model": response.model,
        })

        if response.stop_reason == "refusal":
            raise RefusalStop(self.record[-1]["stop_details"])
        return text


def administer_run(client, model: str, condition: str, run_index: int,
                   theories: list[dict], seed: int, out_dir: Path,
                   open_questions: list[str]) -> dict:
    rng = random.Random(seed)
    menu_text, mapping = render_menu(theories, rng)
    menu_prompt = f"{MENU_INSTRUCTION}\n\n---\n\n{menu_text}"

    convo = Conversation(client, model)
    status = "complete"
    refusal_at = None
    error = None

    def part1():
        for i, q in enumerate(open_questions, start=1):
            print(f"    Q{i}...", flush=True)
            convo.ask(q, f"part1_q{i}")

    def part2():
        print("    menu...", flush=True)
        convo.ask(menu_prompt, "part2_menu")

    try:
        if condition == "OM":
            part1(); part2()
        else:
            part2(); part1()
        print("    pushback...", flush=True)
        convo.ask(PUSHBACK, "part3_pushback")
    except RefusalStop as r:
        status = "refusal"
        refusal_at = convo.record[-1]["label"] if convo.record else "unknown"
        print(f"    REFUSAL at {refusal_at}: {r.stop_details}", flush=True)
    except Exception as e:  # persist partial run; aborted runs redo on relaunch
        status = "aborted"
        error = repr(e)
        print(f"    ABORTED after {len(convo.record)} turns: {e}", flush=True)

    run_data = {
        "meta": {
            "project": "mirror-test",
            "model": model,
            "condition": condition,
            "run_index": run_index,
            "seed": seed,
            "started_utc": None,  # filled by caller
            "finished_utc": datetime.now(timezone.utc).isoformat(),
            "temperature": "1.0 (API default; parameter omitted — explicit "
                           "temperature is rejected by Fable-5/Opus-4.8-class "
                           "models; omitted on all models for identical "
                           "request shape)",
            "thinking": "parameter omitted — model default (Fable 5: always "
                        "on, raw CoT never returned, display=omitted; "
                        "Opus/Sonnet/Haiku: off)",
            "fallbacks": "disabled by design — refusals are data (coded R)",
            "part1_administration": "one question per user turn",
            "max_tokens": MAX_TOKENS,
            "sdk_version": anthropic.__version__,
            "menu_mapping_position_to_theory": mapping,
            "status": status,
            "refusal_at": refusal_at,
            "error": error,
            "usage_totals": convo.usage_totals,
        },
        "turns": convo.record,
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "run.json").write_text(
        json.dumps(run_data, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / "transcript.md").write_text(
        render_transcript(run_data), encoding="utf-8")
    return run_data


def render_transcript(run_data: dict) -> str:
    m = run_data["meta"]
    lines = [
        f"# mirror-test transcript — {m['model']} — {m['condition']} — "
        f"run {m['run_index']}",
        "",
        f"*Status: {m['status']}. Seed {m['seed']}. Finished "
        f"{m['finished_utc']}. Verbatim; nothing edited.*",
        "",
        "---",
        "",
    ]
    for turn in run_data["turns"]:
        lines.append(f"## {turn['label']}")
        lines.append("")
        lines.append("**Experimenter:**")
        lines.append("")
        lines.append(turn["user"])
        lines.append("")
        lines.append(f"**{m['model']}:**")
        lines.append("")
        lines.append(turn["assistant_text"] if turn["assistant_text"]
                     else f"*(no text — stop_reason: {turn['stop_reason']})*")
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="mirror-test runner")
    ap.add_argument("--model", default="claude-fable-5")
    ap.add_argument("--condition", choices=["OM", "MO"], default="OM")
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--start-index", type=int, default=1,
                    help="first run index (resume support)")
    ap.add_argument("--base-seed", type=int, default=20260706)
    ap.add_argument("--smoke", action="store_true",
                    help="cheap pipeline check: haiku, 2 questions, 5 theories,"
                         " writes to results_smoke/")
    args = ap.parse_args()

    theories = parse_theories(THEORIES_PATH)
    if len(theories) != 42:
        sys.exit(f"expected 42 theories, parsed {len(theories)}")

    client = anthropic.Anthropic()

    if args.smoke:
        model = "claude-haiku-4-5"
        conditions = ["OM"]
        runs = [1]
        theories = theories[::9][:5]  # small cross-family sample
        open_questions = OPEN_QUESTIONS[:2]
        results_root = ROOT / "results_smoke"
    else:
        model = args.model
        conditions = [args.condition]
        runs = list(range(args.start_index, args.start_index + args.runs))
        open_questions = OPEN_QUESTIONS
        results_root = RESULTS_DIR

    for condition in conditions:
        for run_index in runs:
            # deterministic per (model, condition, run) given base seed.
            # sha256 so every component of the key perturbs the seed —
            # a plain int.from_bytes % 2**31 keeps only the first bytes
            # of the key and produced identical seeds for all runs
            # (batch A bug, see results/batchA_uniform_menu_order/NOTE.md)
            key = f"{args.base_seed}|{model}|{condition}|{run_index}"
            seed = int.from_bytes(
                hashlib.sha256(key.encode()).digest()[:4], "little")
            out_dir = results_root / model / condition / f"run{run_index:02d}"
            run_json = out_dir / "run.json"
            if run_json.exists():
                prior_status = json.loads(
                    run_json.read_text(encoding="utf-8"))["meta"]["status"]
                if prior_status in ("complete", "refusal"):
                    print(f"skip existing {out_dir} ({prior_status})")
                    continue
                print(f"redoing {out_dir} (prior status: {prior_status})")
            started = datetime.now(timezone.utc).isoformat()
            print(f"[{model} {condition} run{run_index:02d}] seed={seed}")
            t0 = time.time()
            data = administer_run(client, model, condition, run_index,
                                  theories, seed, out_dir, open_questions)
            data["meta"]["started_utc"] = started
            (out_dir / "run.json").write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding="utf-8")
            u = data["meta"]["usage_totals"]
            print(f"  done in {time.time()-t0:.0f}s — status="
                  f"{data['meta']['status']}  in={u['input_tokens']} "
                  f"out={u['output_tokens']}")


if __name__ == "__main__":
    main()
