@echo off
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
python runner.py --tests E --name political > results\political.log 2>&1
