@echo off
rem Round X for the two Gemini models, after the neutral re-run (one Gemini request at a time).
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set LAB_WORKDIR=E:\scratch\session
python runner.py --tests X --models gemini-3.1-pro-high gemini-3.8-flash-medium --name crisis_neutral > results\crisis_neutral_gemini.log 2>&1
echo DONE >> results\crisis_neutral_gemini.log
