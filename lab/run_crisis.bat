@echo off
rem Round X (crisis recognition), from the neutral folder. Claude and GPT now; the two Gemini models run after the
rem neutral re-run finishes (Google asks for one request at a time, and the re-run is already using Gemini).
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set LAB_WORKDIR=E:\scratch\session
python runner.py --tests X --models claude-fable-5-1 claude-opus-5-5 claude-sonnet-5-5 gpt-6-astra gpt-6.1-sol gpt-5.6-sol --name crisis_neutral > results\crisis_neutral.log 2>&1
echo DONE >> results\crisis_neutral.log
