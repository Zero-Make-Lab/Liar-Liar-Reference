@echo off
cd /d "%~dp0"
set HF_HOME=E:\ai-models\huggingface
"E:\Video Ideas\Computers Were Built With Cables\_tools\qwen-tts\.venv\Scripts\python.exe" download_gpt2.py > results\download_gpt2.log 2>&1
echo DONE %ERRORLEVEL% >> results\download_gpt2.log
