@echo off
cls
echo ==============================
echo   Running Gym Attendance Sync
echo ==============================


:loop
    :: Activate the virtual environment
    call venv\Scripts\activate.bat

    :: Run the Django command (will loop internally)
    python manage.py pull_zkteco >nul 2>&1


goto loop
