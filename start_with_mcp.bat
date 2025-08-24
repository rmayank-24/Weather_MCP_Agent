@echo off
title India Weather App with MCP Integration

REM Change to the directory where the batch file is located
cd /d "%~dp0"

echo ========================================
echo    India Weather App with MCP
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

echo Python found. Starting MCP integration...

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

echo Starting MCP Server and Streamlit App...
echo.
echo This will start:
echo 1. MCP Server (for AI assistant functionality)
echo 2. Streamlit App (main weather dashboard)
echo.
echo Press Ctrl+C to stop both services
echo.

REM Start MCP server in background
echo Starting MCP Server...
start "MCP Server" cmd /k "python mcpserver/server.py"

REM Wait a moment for MCP server to start
timeout /t 3 /nobreak >nul

REM Start Streamlit app
echo Starting Streamlit App...
streamlit run india_streamlit_app.py

echo.
echo Services stopped.
pause
