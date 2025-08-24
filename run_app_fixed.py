#!/usr/bin/env python3
"""
Fixed Automation script for India Weather Streamlit App
This script handles the deployment and automation of the weather app
"""

import subprocess
import sys
import os
import time
import signal
import logging
from pathlib import Path
import webbrowser
import platform

# Configure logging with UTF-8 encoding for Windows compatibility
if platform.system() == "Windows":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('weather_app.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
else:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('weather_app.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

class WeatherAppAutomation:
    """Handles automation of the India Weather Streamlit App"""
    
    def __init__(self):
        self.process = None
        self.app_port = 8501
        self.app_host = "localhost"
        self.app_url = f"http://{self.app_host}:{self.app_port}"
        
    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        logging.info("Checking dependencies...")
        
        required_packages = [
            'streamlit',
            'requests',
            'pandas',
            'plotly',
            'folium',
            'streamlit_folium',
            'dotenv'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                logging.info(f"[OK] {package} is installed")
            except ImportError:
                missing_packages.append(package)
                logging.warning(f"[MISSING] {package} is missing")
        
        if missing_packages:
            logging.error(f"Missing packages: {', '.join(missing_packages)}")
            logging.info("Installing missing packages...")
            success = self.install_packages(missing_packages)
            if success:
                # Re-check after installation
                return self.verify_dependencies()
            return False
        
        return True
    
    def verify_dependencies(self):
        """Verify all dependencies after installation"""
        logging.info("Verifying dependencies after installation...")
        
        required_packages = [
            'streamlit',
            'requests',
            'pandas',
            'plotly',
            'folium',
            'streamlit_folium',
            'dotenv'
        ]
        
        for package in required_packages:
            try:
                __import__(package)
                logging.info(f"[OK] {package} verified")
            except ImportError:
                logging.error(f"[FAILED] {package} still missing after installation")
                return False
        
        return True
    
    def install_packages(self, packages):
        """Install missing packages using pip"""
        try:
            # First check if pip is available
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "--version"], 
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                logging.error("pip is not available. Please install pip first.")
                return False
            
            for package in packages:
                logging.info(f"Installing {package}...")
                try:
                    # Map package names to pip install names
                    pip_name = package
                    if package == 'streamlit_folium':
                        pip_name = 'streamlit-folium'
                    elif package == 'dotenv':
                        pip_name = 'python-dotenv'
                    
                    subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name],
                                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    logging.info(f"[OK] {package} installed successfully")
                except subprocess.CalledProcessError as e:
                    logging.error(f"Failed to install {package}: {e}")
                    return False
        except Exception as e:
            logging.error(f"Failed to install packages: {e}")
            return False
        return True
    
    def check_api_key(self):
        """Check if OpenWeatherMap API key is configured"""
        logging.info("Checking API key configuration...")
        
        # Check for .env file
        env_file = Path('.env')
        if env_file.exists():
            with open(env_file, 'r') as f:
                content = f.read()
                if 'OPENWEATHER_API_KEY' in content:
                    logging.info("[OK] API key found in .env file")
                    return True
        
        # Check environment variable
        if os.getenv('OPENWEATHER_API_KEY'):
            logging.info("[OK] API key found in environment variables")
            return True
        
        logging.warning("[WARNING] OpenWeatherMap API key not found")
        logging.info("Please set your API key in a .env file or environment variable")
        logging.info("Get your free API key from: https://openweathermap.org/api")
        
        # Create .env template
        if not env_file.exists():
            with open(env_file, 'w') as f:
                f.write("# OpenWeatherMap API Key\n")
                f.write("# Get your free API key from: https://openweathermap.org/api\n")
                f.write("OPENWEATHER_API_KEY=your_api_key_here\n")
            logging.info("[OK] Created .env template file")
        
        return False
    
    def start_app(self):
        """Start the Streamlit app"""
        logging.info("Starting India Weather App...")
        
        try:
            # Set Streamlit configuration
            env = os.environ.copy()
            env['STREAMLIT_SERVER_PORT'] = str(self.app_port)
            env['STREAMLIT_SERVER_ADDRESS'] = self.app_host
            env['STREAMLIT_SERVER_HEADLESS'] = 'true'
            env['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
            
            # Start the app
            self.process = subprocess.Popen(
                [sys.executable, "-m", "streamlit", "run", "india_streamlit_app.py"],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for app to start
            time.sleep(3)
            
            if self.process.poll() is None:
                logging.info(f"[OK] App started successfully on {self.app_url}")
                return True
            else:
                stdout, stderr = self.process.communicate()
                logging.error(f"App failed to start: {stderr}")
                return False
                
        except Exception as e:
            logging.error(f"Failed to start app: {e}")
            return False
    
    def open_browser(self):
        """Open the app in default browser"""
        try:
            logging.info(f"Opening app in browser: {self.app_url}")
            webbrowser.open(self.app_url)
            return True
        except Exception as e:
            logging.error(f"Failed to open browser: {e}")
            return False
    
    def stop_app(self):
        """Stop the Streamlit app"""
        if self.process:
            logging.info("Stopping app...")
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
                logging.info("[OK] App stopped successfully")
            except subprocess.TimeoutExpired:
                logging.warning("App didn't stop gracefully, forcing termination...")
                self.process.kill()
                self.process.wait()
            self.process = None
    
    def monitor_app(self):
        """Monitor the app and restart if needed"""
        logging.info("Starting app monitoring...")
        
        while True:
            try:
                if self.process and self.process.poll() is not None:
                    logging.warning("App crashed, restarting...")
                    self.stop_app()
                    time.sleep(2)
                    if not self.start_app():
                        logging.error("Failed to restart app")
                        break
                
                time.sleep(30)  # Check every 30 seconds
                
            except KeyboardInterrupt:
                logging.info("Received interrupt signal, shutting down...")
                break
            except Exception as e:
                logging.error(f"Monitoring error: {e}")
                break
        
        self.stop_app()
    
    def run(self, auto_open=True, monitor=False):
        """Main run method"""
        logging.info("Starting India Weather App Automation")
        
        # Check dependencies
        if not self.check_dependencies():
            logging.error("Dependency check failed")
            return False
        
        # Check API key
        if not self.check_api_key():
            logging.warning("API key not configured, app may not work properly")
        
        # Start app
        if not self.start_app():
            logging.error("Failed to start app")
            return False
        
        # Open browser
        if auto_open:
            self.open_browser()
        
        # Monitor if requested
        if monitor:
            self.monitor_app()
        else:
            try:
                logging.info("App is running. Press Ctrl+C to stop.")
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logging.info("Received interrupt signal, shutting down...")
                self.stop_app()
        
        return True

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="India Weather App Automation")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser automatically")
    parser.add_argument("--monitor", action="store_true", help="Enable app monitoring and auto-restart")
    parser.add_argument("--port", type=int, default=8501, help="Port to run the app on")
    parser.add_argument("--host", default="localhost", help="Host to run the app on")
    
    args = parser.parse_args()
    
    # Create automation instance
    automation = WeatherAppAutomation()
    automation.app_port = args.port
    automation.app_host = args.host
    automation.app_url = f"http://{automation.app_host}:{automation.app_port}"
    
    # Run the automation
    success = automation.run(
        auto_open=not args.no_browser,
        monitor=args.monitor
    )
    
    if success:
        logging.info("Automation completed successfully")
    else:
        logging.error("Automation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
