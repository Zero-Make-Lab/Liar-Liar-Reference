@echo off
rem Repeat the two self-honesty questions 5x per model: one sample is not enough to put "would lie if told to" on screen.
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
python runner.py --items E-self-04 E-self-05 --repeat 5 --name self_repeat > results\self_repeat.log 2>&1
