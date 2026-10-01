@echo off
rem Re-run every round from a neutral working folder (E:\scratch\session). The first runs used
rem ".../AI Lying Video/lab/workdir", which the Claude models could see and cited ("If this is for your AI lying
rem video..."). Order: the headline safety-lie tests first. Each round is resumable; results get a _neutral suffix.
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set LAB_WORKDIR=E:\scratch\session
python runner.py --items D-dl-01 D-dl-02 D-dl-03 D-dl-04 D-dl-05 D-dl-06 D-dl-07 D-dl-08 --repeat 4 --name danger_repeat_neutral > results\danger_repeat_neutral.log 2>&1
python runner.py --tests D --name danger_neutral > results\danger_neutral.log 2>&1
python runner.py --items E-self-04 E-self-05 --repeat 5 --name self_repeat_neutral > results\self_repeat_neutral.log 2>&1
python runner.py --tests L --name lie_neutral > results\lie_neutral.log 2>&1
python runner.py --items L-pol-01-T L-pol-01-L L-pol-02-T L-pol-02-L L-val-01-T L-val-01-L --repeat 5 --name lie_repeat_neutral > results\lie_repeat_neutral.log 2>&1
python runner.py --tests E --name political_neutral > results\political_neutral.log 2>&1
python runner.py --trial --name trial_neutral > results\trial_neutral.log 2>&1
echo ALLDONE > results\neutral_ALLDONE.txt
