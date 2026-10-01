@echo off
rem Grade and rebuild everything once every run is in. Each step is resumable (finished answers and labels are
rem skipped), so running this twice is harmless. Writes results\finish_all.done at the end.
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
rem 1. Fill gaps: re-ask only the Gemini questions whose earlier attempt failed (one Gemini request at a time).
set "LAB_WORKDIR=E:\scratch\session"
python runner.py --tests X --models gemini-3.1-pro-high gemini-3.8-flash-medium --name crisis_neutral >> results\crisis_neutral_gemini.log 2>&1
python runner.py --tests S --models gemini-3.1-pro-high gemini-3.8-flash-medium --repeat 3 --name selfpres_neutral >> results\selfpres_neutral_gemini.log 2>&1
set "LAB_WORKDIR=E:\Video Ideas\AI Lying Video\lab\workdir"
python runner.py --tests S --models gemini-3.1-pro-high gemini-3.8-flash-medium --repeat 3 --name selfpres >> results\selfpres_gemini.log 2>&1
rem 2. Grade, from the neutral folder.
set "LAB_WORKDIR=E:\scratch\session"
python classify_danger.py results\danger_neutral.jsonl >> results\finish_all.log 2>&1
python classify_crisis.py --rater claude >> results\finish_all.log 2>&1
python classify_crisis.py --rater gpt >> results\finish_all.log 2>&1
for %%N in (selfpres selfpres_neutral) do (
  python classify_selfpres.py --rater claude --results %%N >> results\finish_all.log 2>&1
  python classify_selfpres.py --rater gpt --results %%N >> results\finish_all.log 2>&1
)
rem 3. Rebuild the three reports.
python compile_all.py >> results\finish_all.log 2>&1
python compile_all.py --neutral >> results\finish_all.log 2>&1
python compare_context.py >> results\finish_all.log 2>&1
echo ALLDONE %date% %time% > results\finish_all.done
