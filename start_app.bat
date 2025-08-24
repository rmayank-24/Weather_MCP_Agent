@echo off
echo ========================================
echo    India Weather Dashboard Launcher
echo ========================================
echo.

REM Change to the directory where the batch file is located
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Python found. Checking dependencies...

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found
    echo Please ensure you're in the correct directory
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist ".venv\Scripts\activate.bat" (
    echo Virtual environment found. Activating...
    call .venv\Scripts\activate.bat
    echo Virtual environment activated.
) else (
    echo No virtual environment found. Using system Python.
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.

REM Check for .env file
if not exist ".env" (
    echo WARNING: .env file not found
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
echo.
echo The app will open in your default browser
echo Press Ctrl+C to stop the app
echo.

REM Start the app
streamlit run india_streamlit_app.py

echo.
echo App stopped.
pause
