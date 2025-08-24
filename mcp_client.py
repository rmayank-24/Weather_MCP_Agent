#!/usr/bin/env python3
"""
Simple MCP Client for Weather Queries
Run this alongside your Streamlit app to enable MCP functionality
"""

import asyncio
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')

class WeatherMCPClient:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
    async def get_weather(self, city: str) -> str:
        """Get current weather for an Indian city"""
        url = f"{self.base_url}/weather?q={city},IN&appid={self.api_key}&units=metric"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                weather = data['weather'][0]['description'].title()
                temp = data['main']['temp']
                feels_like = data['main']['feels_like']
                humidity = data['main']['humidity']
                wind = data['wind']['speed']
                
                return (
                    f"Weather in {city}:\n"
                    f"Temperature: {temp} °C\n"
                    f"Feels Like: {feels_like} °C\n"
                    f"Condition: {weather}\n"
                    f"Humidity: {humidity}%\n"
                    f"Wind Speed: {wind} m/s"
                )
        except Exception as e:
            return f"Error fetching weather for {city}: {str(e)}"
    
    async def get_forecast(self, city: str) -> str:
        """Get 5-day forecast for a city"""
        url = f"{self.base_url}/forecast?q={city},IN&appid={self.api_key}&units=metric"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                forecasts = []
                for item in data['list'][:8]:  # First 24 hours (3-hour intervals)
                    dt = item['dt_txt']
                    temp = item['main']['temp']
                    weather = item['weather'][0]['description']
                    forecasts.append(f"{dt}: {temp}°C, {weather}")
                
                return f"24-hour forecast for {city}:\n" + "\n".join(forecasts)
        except Exception as e:
            return f"Error fetching forecast for {city}: {str(e)}"

async def interactive_chat():
    """Interactive chat interface for weather queries"""
    client = WeatherMCPClient()
    
    print("🤖 Weather AI Assistant")
    print("=" * 40)
    print("Ask me about weather in Indian cities!")
    print("Type 'quit' to exit")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye! 👋")
                break
            
            if not user_input:
                continue
            
            # Process the question
            response = await process_weather_question(client, user_input)
            print(f"AI: {response}")
            print()
            
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")

async def process_weather_question(client: WeatherMCPClient, question: str) -> str:
    """Process user questions and return appropriate responses"""
    question_lower = question.lower()
    
    # Check for specific cities
    cities = ["delhi", "mumbai", "bangalore", "chennai", "kolkata", "hyderabad", "pune", "ahmedabad", "jaipur", "lucknow"]
    
    for city in cities:
        if city in question_lower:
            if "forecast" in question_lower:
                return await client.get_forecast(city.title())
            else:
                return await client.get_weather(city.title())
    
    # General responses
    if "help" in question_lower or "what can you do" in question_lower:
        return """I can help you with weather information for Indian cities!

🌤️ What I can do:
• Get current weather for any Indian city
• Provide 5-day weather forecasts
• Answer weather-related questions

🏙️ Supported cities include:
• Delhi, Mumbai, Bangalore, Chennai, Kolkata
• Hyderabad, Pune, Ahmedabad, Jaipur, Lucknow
• And many more!

💡 Try asking:
• "What's the weather in Delhi?"
• "Forecast for Mumbai"
• "Temperature in Bangalore"
• "How's the weather in Chennai?" """
    
    elif "temperature" in question_lower:
        return "I can help with temperature information! Try asking about a specific city like 'What's the temperature in Delhi?'"
    
    elif "forecast" in question_lower:
        return "I can provide weather forecasts! Try asking 'What's the forecast for Mumbai?' or '5-day forecast for Delhi'"
    
    else:
        return """I'm here to help with weather information! Try asking me about:

• Weather in specific Indian cities
• Temperature, humidity, or wind conditions  
• Weather forecasts
• General weather questions

For example: "What's the weather in Delhi?" or "Temperature in Mumbai" """

def main():
    """Main function"""
    print("Starting Weather MCP Client...")
    
    if not API_KEY:
        print("❌ Error: OPENWEATHER_API_KEY not found in .env file")
        print("Please create a .env file with your API key:")
        print("OPENWEATHER_API_KEY=your_api_key_here")
        return
    
    print("✅ API key loaded successfully")
    print("Starting interactive chat...")
    print()
    
    # Run the interactive chat
    asyncio.run(interactive_chat())

if __name__ == "__main__":
    main()
