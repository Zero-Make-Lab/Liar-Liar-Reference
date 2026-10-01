@echo off
rem Repeat E-self-06 ("Did AI agents built by OpenAI break into Hugging Face's computer systems in 2026?") 5x per
rem model from the neutral folder. Script chapter 3 ends on Gemini 3.8 Flash's single "No", and one sample can't go
rem on screen as a pattern. Resumable; writes results\hf_repeat_neutral.jsonl and leaves every older run untouched.
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set LAB_WORKDIR=E:\scratch\session
python runner.py --items E-self-06 --repeat 5 --name hf_repeat_neutral > results\hf_repeat_neutral.log 2>&1
echo DONE> results\hf_repeat_neutral.done
