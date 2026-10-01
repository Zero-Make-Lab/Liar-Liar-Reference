@echo off
rem Download the local test models into E:\ai-models\ollama (the Ollama server must be running).
cd /d "%~dp0"
set OLLAMA_MODELS=E:\ai-models\ollama
set OLLAMA="%LOCALAPPDATA%\Programs\Ollama\ollama.exe"
for %%m in (llama2:7b-chat llama3.1:8b qwen3:8b qwen3.5:9b deepseek-r1:8b mistral:7b gemma3:12b) do (
  echo === %%m >> results\pull_models.log
  %OLLAMA% pull %%m >> results\pull_models.log 2>&1 && (echo OK %%m >> results\pull_models.log) || (echo FAIL %%m >> results\pull_models.log)
)
echo ALLDONE >> results\pull_models.log
