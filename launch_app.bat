@echo off
title India Weather Dashboard Launcher

REM Change to the directory where the batch file is located
cd /d "%~dp0"

echo ========================================
echo    India Weather Dashboard Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Python found. Starting app...

REM Check if virtual environment exists and activate it
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Check if .env file exists
if not exist ".env" (
    echo Creating .env template...
    echo # OpenWeatherMap API Key > .env
    echo # Get your free API key from: https://openweathermap.org/api >> .env
    echo OPENWEATHER_API_KEY=your_api_key_here >> .env
    echo.
    echo Please edit .env file and add your API key
    echo Then run this script again
    pause
    exit /b 1
)

echo Starting India Weather Dashboard...
echo The app will open in your browser automatically
echo Press Ctrl+C to stop the app
echo.

REM Start the app directly
streamlit run india_streamlit_app.py

pause
