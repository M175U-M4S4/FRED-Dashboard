@echo off
setlocal ENABLEDELAYEDEXPANSION
cd /d "%~dp0"

echo =========================================
echo   FRED Dashboard V2 - First Time Setup
echo =========================================
echo.

if not exist ".venv" (
  echo [1/4] Creating virtual environment...
  py -3 -m venv .venv
  if errorlevel 1 (
    echo ERROR: Could not create virtual environment.
    echo Ensure Python 3.10+ is installed and added to PATH.
    pause
    exit /b 1
  )
) else (
  echo [1/4] Virtual environment already exists.
)

echo [2/4] Upgrading pip...
call .venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 (
  echo ERROR: pip upgrade failed.
  pause
  exit /b 1
)

echo [3/4] Installing dependencies...
call .venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
  echo ERROR: Dependency installation failed.
  pause
  exit /b 1
)

echo [4/4] Setup complete.
echo.
echo Optional: create a .env file and set FRED_API_KEY=your_key
echo.
echo Done! You can now double-click 02_run_dashboard.bat
pause
