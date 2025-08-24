#!/usr/bin/env python3
"""
Simple dependency installation script for India Weather App
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a single package"""
    try:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install {package}: {e}")
        return False

def main():
    print("Installing dependencies for India Weather App...")
    print("=" * 50)
    
    # Core packages
    packages = [
        "streamlit>=1.28.0",
        "requests>=2.31.0",
        "pandas>=2.0.0",
        "plotly>=5.17.0",
        "folium>=0.14.0",
        "streamlit-folium>=0.13.0",
        "python-dotenv>=1.0.0"
    ]
    
    success_count = 0
    total_packages = len(packages)
    
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print("=" * 50)
    print(f"Installation complete: {success_count}/{total_packages} packages installed successfully")
    
    if success_count == total_packages:
        print("✓ All dependencies installed successfully!")
        print("\nNext steps:")
        print("1. Get your API key from: https://openweathermap.org/api")
        print("2. Create a .env file with: OPENWEATHER_API_KEY=your_key_here")
        print("3. Run: python run_app.py")
    else:
        print("✗ Some packages failed to install. Please check the errors above.")
        print("\nTry running: pip install --upgrade pip")
        print("Then run this script again.")

if __name__ == "__main__":
    main()
