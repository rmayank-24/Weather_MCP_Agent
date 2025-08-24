#!/bin/bash

echo "========================================"
echo "   India Weather Dashboard Launcher"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Python found. Checking dependencies..."

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "ERROR: requirements.txt not found"
    echo "Please ensure you're in the correct directory"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo
echo "Dependencies installed successfully!"
echo

# Check for .env file
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found"
    echo "Creating .env template..."
    cat > .env << EOF
# OpenWeatherMap API Key
# Get your free API key from: https://openweathermap.org/api
OPENWEATHER_API_KEY=your_api_key_here
EOF
    echo
    echo "Please edit .env file and add your API key"
    echo "Then run this script again"
    exit 1
fi

echo "Starting India Weather Dashboard..."
echo
echo "The app will open in your default browser"
echo "Press Ctrl+C to stop the app"
echo

# Start the app
python3 run_app.py

echo
echo "App stopped."
