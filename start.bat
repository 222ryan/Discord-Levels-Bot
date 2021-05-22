@echo off
:loop
echo Starting main.py -- If you run into any issues, Join the support Server!
python main.py
timeout /t 5 > nul
cls
echo Restarting..
goto loop