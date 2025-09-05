@echo off
echo ==============================
echo     Gym Attendance Sync Started
echo ==============================

:: Activate the virtual environment
call venv\Scripts\activate.bat

:loop
echo --------------------------------
echo Running attendance sync at %time%
python manage.py pull_zkteco

:: Wait for 5 seconds before the next sync
timeout /t 5 >nul

goto loop
