@echo off
setlocal ENABLEDELAYEDEXPANSION
cd /d "%~dp0"

echo =========================================
echo   FRED Dashboard V2 - Launch
echo =========================================
echo.

if not exist ".venv\Scripts\python.exe" (
  echo ERROR: Virtual environment not found.
  echo Please run 01_setup_once.bat first.
  pause
  exit /b 1
)

echo [1/4] Running ingestion...
call .venv\Scripts\python.exe -m ingest.run
if errorlevel 1 (
  echo WARNING: Ingestion returned an error. The app may still run with existing data.
)

echo [2/4] Starting API server on http://127.0.0.1:8000 ...
start "FRED Dashboard API" cmd /c "cd /d %~dp0 && .venv\Scripts\python.exe -m uvicorn api.main:app --host 127.0.0.1 --port 8000"

timeout /t 2 /nobreak >nul

echo [3/4] Starting Streamlit UI on http://127.0.0.1:8501 ...
start "FRED Dashboard UI" cmd /c "cd /d %~dp0 && .venv\Scripts\python.exe -m streamlit run app\main.py --server.port 8501 --server.address 127.0.0.1"

timeout /t 3 /nobreak >nul

echo [4/4] Opening dashboard in your default browser...
start "" "http://127.0.0.1:8501"

echo.
echo Launched. You can close this window; API/UI run in their own windows.
exit /b 0
