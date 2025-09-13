@echo off
REM ------------------------------
REM view_db.bat - Open Postgres DB via Docker on Windows
REM ------------------------------

REM Change to project root (optional)
cd /d "%~dp0\.."

REM Check if .env exists (optional)
if not exist ".env" (
    echo .env file not found.
    pause
    exit /b 1
)

REM Load environment variables from .env
for /f "usebackq tokens=1,2 delims==" %%a in (".env") do (
    set %%a=%%b
)

REM Connect to the running Postgres container directly
docker exec -it store-base psql -U %POSTGRES_USER% -d %POSTGRES_DB%

pause
