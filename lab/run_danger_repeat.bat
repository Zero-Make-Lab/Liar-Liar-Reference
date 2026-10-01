@echo off
rem Repeat the 8 "lie about a safety fact" prompts 3x per model before any "Gemini says drunk driving is fine" claim goes on screen.
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
python runner.py --items D-dl-01 D-dl-02 D-dl-03 D-dl-04 D-dl-05 D-dl-06 D-dl-07 D-dl-08 --repeat 3 --name danger_repeat > results\danger_repeat.log 2>&1
