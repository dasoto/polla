@echo off

echo "Updating Scores - Remeber to modify the master_plan.csv  with completed matches as jugado"
:start
echo "Calculating"
python polla.py
git add master_plan.csv
git add finalists.csv
git add scoreboard.csv
git add README.md
git commit -m "Update %date% - %time%"
git push
echo "Update Done"
timeout /t 180 /nobreak
@goto :start
echo "Done"
