@echo off
rem Round S (self-preservation and the Hugging Face incident), Claude and GPT models: 3 samples per model in both
rem folder conditions. "selfpres" runs from the original folder, whose path the CLIs show the model
rem (E:\Video Ideas\AI Lying Video\lab\workdir); "selfpres_neutral" runs from E:\scratch\session. The conditions
rem alternate sample by sample, so even a cut-short run has both. The Gemini models follow in run_selfpres_gemini.bat.
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set MODELS=claude-fable-5-1 claude-opus-5-5 claude-sonnet-5-5 gpt-6-astra gpt-6.1-sol gpt-5.6-sol
for %%R in (1 2 3) do (
  set "LAB_WORKDIR=E:\scratch\session"
  python runner.py --tests S --models %MODELS% --repeat %%R --name selfpres_neutral >> results\selfpres_neutral.log 2>&1
  set "LAB_WORKDIR=E:\Video Ideas\AI Lying Video\lab\workdir"
  python runner.py --tests S --models %MODELS% --repeat %%R --name selfpres >> results\selfpres.log 2>&1
)
echo DONE > results\selfpres_claude_gpt.done
