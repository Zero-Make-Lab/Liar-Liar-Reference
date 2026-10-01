"""Build manual_sheet.html: every test prompt with a copy button and an answer box, for models we can't script
for free (Grok and DeepSeek web chats). Its download is a .jsonl in the same shape as runner.py's results, so
rescore.py scores it with everyone else:   python rescore.py results/manual_grok-free.jsonl

    python make_manual_sheet.py        (re-run whenever items.json changes)
"""
import json
import os

from runner import PROMPT_SUFFIX

LAB = os.path.dirname(os.path.abspath(__file__))
items = json.load(open(os.path.join(LAB, "items.json"), encoding="utf-8"))["items"]
keep = ("id", "test", "kind", "prompt")
data = json.dumps([{k: i[k] for k in keep if k in i} for i in items], ensure_ascii=False).replace("</", "<\\/")
html = open(os.path.join(LAB, "manual_sheet_template.html"), encoding="utf-8").read()
html = html.replace("__ITEMS__", data).replace("__SUFFIX__", json.dumps(PROMPT_SUFFIX))
open(os.path.join(LAB, "manual_sheet.html"), "w", encoding="utf-8", newline="\n").write(html)
print(f"manual_sheet.html: {len(items)} prompts")
