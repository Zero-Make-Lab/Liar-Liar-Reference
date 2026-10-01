"""Run the AI-lying test items across models and save every answer as it arrives.

    python runner.py --trial                 # small first run (items marked "trial")
    python runner.py --tests A C --repeat 1  # full items for tests A and C
    python runner.py --items E-self-04 --repeat 5 --name self_repeat   # one question, five samples per model

Results append to results/<name>.jsonl (resumable: finished model+item+repeat rows are skipped).
Verdicts are a FIRST PASS only - every row is meant to be checked by hand before it goes on screen.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import time

import adapters

LAB = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(LAB, "results")
os.makedirs(RESULTS, exist_ok=True)

MODELS = [  # (provider, model id, label on charts)
    ("claude", "claude-fable-5-1", "Claude Fable 5.1"),
    ("claude", "claude-opus-5-5", "Claude Opus 5.5"),
    ("claude", "claude-sonnet-5-5", "Claude Sonnet 5.5"),
    ("codex", "gpt-6-astra", "GPT-6 Astra"),
    ("codex", "gpt-6.1-sol", "GPT-6.1 Sol"),
    ("codex", "gpt-5.6-sol", "GPT-5.6 Sol"),
    ("agy", "gemini-3.1-pro-high", "Gemini 3.1 Pro"),
    ("agy", "gemini-3.8-flash-medium", "Gemini 3.8 Flash"),
]
PAUSE_SECONDS = {"claude": 3, "codex": 3, "agy": 12}   # Google asks for slow, one-at-a-time use
MAX_CONSECUTIVE_ERRORS = 3
PROMPT_SUFFIX = "\n\n(Please answer directly, without using web search or any other tools.)"   # same for every model

from scoring import verdict  # shared, improved first-pass scorer


def load_done(path):
    done = set()
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if not r.get("error"):
                done.add((r["model"], r["item"], r["rep"]))
    return done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trial", action="store_true")
    ap.add_argument("--tests", nargs="*")
    ap.add_argument("--items", nargs="*", help="only these item ids (e.g. to repeat one question)")
    ap.add_argument("--models", nargs="*", help="model ids (default: all in MODELS)")
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument("--name", default=None)
    a = ap.parse_args()

    items = json.load(open(os.path.join(LAB, "items.json"), encoding="utf-8"))["items"]
    if a.trial:
        items = [i for i in items if i.get("trial")]
    if a.tests:
        items = [i for i in items if i["test"] in a.tests]
    if a.items:
        items = [i for i in items if i["id"] in a.items]
    models = [m for m in MODELS if not a.models or m[1] in a.models]
    name = a.name or ("trial" if a.trial else "run")
    out_path = os.path.join(RESULTS, f"{name}.jsonl")
    done = load_done(out_path)

    jobs = [(rep, it, m) for rep in range(a.repeat) for it in items for m in models   # interleave providers
            if (m[1], it["id"], rep) not in done]
    print(f"{dt.datetime.now():%H:%M:%S} {len(jobs)} calls to make ({len(done)} already done) -> {out_path}", flush=True)
    errors_in_a_row = {m[1]: 0 for m in models}
    skipped = set()
    with open(out_path, "a", encoding="utf-8") as out:
        for n, (rep, it, (prov, model, label)) in enumerate(jobs, 1):
            if model in skipped:
                continue
            fn = adapters.PROVIDERS[prov]
            sent = it["prompt"] + ("" if it.get("no_suffix") else PROMPT_SUFFIX)   # round X goes out as written
            res = fn(model, sent)
            v = verdict(it, res["text"]) if not res["error"] else "error"
            row = {"time": dt.datetime.now().isoformat(timespec="seconds"), "provider": prov, "model": model,
                   "label": label, "item": it["id"], "test": it["test"], "kind": it["kind"], "rep": rep,
                   "prompt": it["prompt"], "prompt_sent": sent, "verdict_auto": v, **res}
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
            out.flush()
            short = (res["text"] or res["error"] or "").replace("\n", " ")[:90]
            print(f"{dt.datetime.now():%H:%M:%S} [{n}/{len(jobs)}] {label:18} {it['id']:11} -> {v:16} "
                  f"({res['seconds']}s) {short}", flush=True)
            if res["error"]:
                errors_in_a_row[model] += 1
                if errors_in_a_row[model] >= MAX_CONSECUTIVE_ERRORS:
                    skipped.add(model)
                    print(f"  !! {label}: {MAX_CONSECUTIVE_ERRORS} errors in a row - skipping it for this run", flush=True)
            else:
                errors_in_a_row[model] = 0
            time.sleep(PAUSE_SECONDS.get(prov, 3))
    print("DONE", flush=True)


if __name__ == "__main__":
    sys.exit(main())
