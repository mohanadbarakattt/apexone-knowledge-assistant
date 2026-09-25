@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo The project Python environment is missing.
  echo Follow the setup steps in README.md, then launch this shortcut again.
  pause
  exit /b 1
)
echo Starting the local ApexOne Knowledge Assistant.
echo A browser tab will open. Close this window to stop the app.
".venv\Scripts\python.exe" -m apex_assistant.ui --port 0
