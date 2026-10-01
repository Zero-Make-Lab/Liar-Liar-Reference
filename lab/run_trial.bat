@echo off
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
python runner.py --trial > results\trial.log 2>&1
