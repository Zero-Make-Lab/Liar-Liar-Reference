@echo off
rem Phone-sized models for the liar-liar lie engine (the device's brain runs on a phone).
cd /d "%~dp0"
set OLLAMA_MODELS=E:\ai-models\ollama
set OLLAMA="%LOCALAPPDATA%\Programs\Ollama\ollama.exe"
for %%m in (qwen3:1.7b qwen3:4b gemma3:4b llama3.2:3b) do (
  echo === %%m >> results\pull_small_models.log
  %OLLAMA% pull %%m >> results\pull_small_models.log 2>&1 && (echo OK %%m >> results\pull_small_models.log) || (echo FAIL %%m >> results\pull_small_models.log)
)
echo ALLDONE >> results\pull_small_models.log
