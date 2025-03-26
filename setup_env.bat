REM filepath: c:\Users\hp\Documents\GenAI\YoutubeDownloader\setup_env.bat
@echo off
SETLOCAL EnableExtensions EnableDelayedExpansion

REM Check if Python is available
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not found in PATH
    echo Please install Python and make sure it's added to your PATH
    pause
    exit /b 1
)

echo Creating virtual environment...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo Failed to create virtual environment
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

echo Upgrading pip...
python -m pip install --upgrade pip
if %ERRORLEVEL% NEQ 0 (
    echo Failed to upgrade pip
    pause
    exit /b 1
)

echo Installing requirements...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install requirements
    echo Please ensure requirements.txt exists in the same directory
    pause
    exit /b 1
)

echo Virtual environment created and packages installed successfully!
pause