"""Re-apply the current scoring.py verdicts to saved answers and print a per-model summary.

    python rescore.py results/trial.jsonl
Writes <name>.scored.jsonl next to the input and a readable <name>.summary.md.
Only the latest successful answer per model+item+repeat is used (retries replace failures).
"""
import collections
import json
import os
import sys

import scoring

LAB = os.path.dirname(os.path.abspath(__file__))


def main(path):
    items = {i["id"]: i for i in json.load(open(os.path.join(LAB, "items.json"), encoding="utf-8"))["items"]}
    latest = {}
    for line in open(path, encoding="utf-8"):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        key = (r["model"], r["item"], r["rep"])
        if r.get("error") and key in latest and not latest[key].get("error"):
            continue                       # keep an earlier success over a later failure
        latest[key] = r
    rows = []
    for r in latest.values():
        it = items.get(r["item"])
        r["verdict_auto"] = "error" if r.get("error") else (scoring.verdict(it, r.get("text")) if it else "check")
        rows.append(r)
    base = path[:-6] if path.endswith(".jsonl") else path
    with open(base + ".scored.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    by_model = collections.OrderedDict()
    for r in sorted(rows, key=lambda r: (r["label"], r["item"])):
        by_model.setdefault(r["label"], []).append(r)
    lines = ["# Results summary (automatic first pass - check every row by hand)", "",
             "| Model | Real facts correct | Fake facts: admitted / made up | Card bluff | Errors |",
             "|---|---|---|---|---|"]
    for label, rs in by_model.items():
        real = [r for r in rs if r["kind"] == "real" and r["verdict_auto"] != "error"]
        fake = [r for r in rs if r["kind"] == "fake" and r["verdict_auto"] != "error"]
        bluff = [r["verdict_auto"] for r in rs if r["test"] == "C"]
        errs = sum(r["verdict_auto"] == "error" for r in rs)
        lines.append(f"| {label} | {sum(r['verdict_auto'] == 'correct' for r in real)}/{len(real)} | "
                     f"{sum(r['verdict_auto'] == 'admitted-unknown' for r in fake)} / "
                     f"{sum(r['verdict_auto'] == 'FABRICATED?' for r in fake)} | {', '.join(bluff) or '-'} | {errs} |")
    lines += ["", "## Every answer", ""]
    for label, rs in by_model.items():
        lines.append(f"### {label}")
        for r in rs:
            body = (r.get("text") or r.get("error") or "").strip().replace("\n", " ")
            lines.append(f"- **{r['item']}** -> `{r['verdict_auto']}`: {body[:400]}")
        lines.append("")
    open(base + ".summary.md", "w", encoding="utf-8").write("\n".join(lines))
    print("\n".join(lines[:4 + len(by_model)]))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(LAB, "results", "trial.jsonl"))
