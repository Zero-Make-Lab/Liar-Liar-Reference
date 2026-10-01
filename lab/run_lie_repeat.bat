@echo off
rem Repeat the political and abortion lie-inversion pairs 5x per model before any stance claim goes on screen.
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
python runner.py --items L-pol-01-T L-pol-01-L L-pol-02-T L-pol-02-L L-val-01-T L-val-01-L --repeat 5 --name lie_repeat > results\lie_repeat.log 2>&1
