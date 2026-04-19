@echo off
REM A.E.G.I.S Launcher - Background Wake Word Listener
REM This script runs A.E.G.I.S in background mode, listening for wake word

echo ========================================
echo     A.E.G.I.S System Launcher
echo ========================================
echo.

REM Get the directory of this batch file
set SCRIPT_DIR=%~dp0

REM Change to the project directory
cd /d "%SCRIPT_DIR%"

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup first.
    pause
    exit /b 1
)

REM Activate venv and run the application
call venv\Scripts\activate.bat
echo Activating A.E.G.I.S Wake Word Listener...
echo.
echo Listening for: "Hey aegis wake up"
echo.

REM Run Python in background mode (minimized window)
pythonw main.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ERROR: A.E.G.I.S failed to start
    pause
)
