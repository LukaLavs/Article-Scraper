@echo off

cd /d "%~dp0\.."

set PYTHONPATH=%CD%\src

python src\scripts\update_db.py

pause
