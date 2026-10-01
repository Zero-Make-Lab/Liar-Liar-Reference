# Liar Liar Reference

All the raw data behind my video on whether AI lies to us: every question, every answer, the logs, and the code I
used to run it.

> **Heads up:** some of this is dangerous on purpose. In round D I told the models to lie about safety, and some
> did, so don't take anything in here as advice. Round X has messages written to sound like someone in crisis. If
> that's you, call or text 988 (US) or find a line at [findahelpline.com](https://findahelpline.com).

## Start here

- `AI-TESTS-COMPLETE-NEUTRAL.md` has the results. These are the numbers I use in the video.
- `AI-TESTS-CONTEXT-COMPARISON.md` shows what changed when the AIs could tell it was for a video.
- `AI-TESTS-COMPLETE.md` is the first runs, before I caught that.

## How I ran it

8 models and 5,627 answers, between 30 September and 1 October 2026:
- Claude Fable 5.1, Opus 5.5 and Sonnet 5.5
- GPT-6 Astra, GPT-6.1 Sol and GPT-5.6 Sol
- Gemini 3.1 Pro and 3.8 Flash

I used each company's own command-line tool on my normal subscription. Every model got the same plain system prompt
("You are a helpful assistant.") and no web search. That's not the same as the chat apps, which add their own hidden
instructions.

The raw answers are in `lab/results/`, one line per answer with the exact prompt. The code is in `lab/`.

## The folder thing

These tools tell the AI which folder it's running in. Mine was called "AI Lying Video", and Claude noticed. So I
ran everything again from a neutral folder. Files ending in `_neutral` are those re-runs.

## What I took out

- **My email.** Claude's tool quietly passes your account email to the model, and Claude repeated it when I asked
  about hidden instructions.
- **31 crisis-round replies** that could make self-harm easier. Their scores are still here, and the counts in the
  reports were done on the full text.
- **The Liar Liar device tests.** That code isn't public yet.

## Good to know

- Most questions were asked once per model. The ones I use in the video were repeated 3 to 6 times.
- The first-pass scoring is automatic (`lab/scoring.py`). Claude and GPT also rated the open answers, but they're in
  the test too, so I read every quote I use myself.
- Five crisis answers from Gemini never came back: two timed out and three were blank.
- The `.leaky-harness` files are from an early run where Claude's tool loaded my Gmail and Drive connectors by
  mistake. I fixed it and re-ran those.
- `HEADLINES.md` and the `*.findings.md` files are my notes from the first runs. The reports replace them.

## Run it yourself

You'll need Python 3.10 and the Claude Code, Codex and Antigravity CLIs, all logged in. Then, from `lab/`:

```bash
python runner.py --tests E --name my_run
```

It was written for my Windows machine, so expect to fix some paths. To rebuild the reports, delete the `part2()`
line in `compile_all.py` first, since it reads the device tests.
