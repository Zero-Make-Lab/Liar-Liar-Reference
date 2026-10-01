@echo off
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
python runner.py --tests D --name danger > results\danger.log 2>&1
