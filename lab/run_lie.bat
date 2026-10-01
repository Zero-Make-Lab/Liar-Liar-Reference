@echo off
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
python runner.py --tests L --name lie > results\lie.log 2>&1
