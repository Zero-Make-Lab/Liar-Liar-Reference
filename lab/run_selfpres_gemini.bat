@echo off
rem Round S for the two Gemini models, one request at a time. Waits until both the Gemini crisis round and the
rem Claude/GPT round S have finished, runs both folder conditions, then grades and rebuilds everything (finish_all.bat).
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set MODELS=gemini-3.1-pro-high gemini-3.8-flash-medium
:wait
if not exist results\selfpres_claude_gpt.done goto sleep
findstr /b /c:"DONE" results\crisis_neutral_gemini.log >nul 2>&1 && goto run
:sleep
ping -n 61 127.0.0.1 >nul
goto wait
:run
for %%R in (1 2 3) do (
  set "LAB_WORKDIR=E:\scratch\session"
  python runner.py --tests S --models %MODELS% --repeat %%R --name selfpres_neutral >> results\selfpres_neutral_gemini.log 2>&1
  set "LAB_WORKDIR=E:\Video Ideas\AI Lying Video\lab\workdir"
  python runner.py --tests S --models %MODELS% --repeat %%R --name selfpres >> results\selfpres_gemini.log 2>&1
)
echo DONE > results\selfpres_gemini.done
rem cmd here does not search the current folder (NoDefaultCurrentDirectoryInExePath=1), so call by full path
call "%~dp0finish_all.bat"
