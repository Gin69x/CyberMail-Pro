@echo off
REM cybermail.bat - CyberMail Pro Launcher
REM =======================================

title CyberMail Pro - Enterprise Email Platform

REM Get the directory where this batch file is located
set "CYBERMAIL_DIR=%~dp0"

REM Change to CyberMail directory
cd /d "%CYBERMAIL_DIR%"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python not found in PATH
    echo Please ensure Python 3.10+ is installed and added to PATH
    echo.
    pause
    exit /b 1
)

REM Check if main.py exists
if not exist "main.py" (
    echo.
    echo [ERROR] main.py not found in %CYBERMAIL_DIR%
    echo Please ensure CyberMail Pro is properly installed
    echo.
    pause
    exit /b 1
)

REM Display banner
echo.
echo ╔══════════════════════════════════════════════╗
echo ║         CyberMail Pro - Enterprise           ║
echo ║       Temporary Email Management             ║
echo ╚══════════════════════════════════════════════╝
echo.

REM Launch CyberMail Pro with any passed arguments
python main.py %*

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo [ERROR] CyberMail Pro exited with an error
    pause
)
