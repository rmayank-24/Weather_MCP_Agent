
import os
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# List of popular Indian cities
INDIAN_CITIES = [
    "Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
    "Chandigarh", "Bhopal", "Indore", "Patna", "Nagpur", "Kanpur", "Thiruvananthapuram", "Coimbatore", "Vadodara", "Surat"
]

async def fetch_weather(city: str) -> dict:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}&units=metric"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=20.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

@mcp.tool()
async def get_weather(city: str) -> str:
    """Get current weather for an Indian city.
    Args:
        city: Name of the city (e.g. Delhi)
    """
    if city not in INDIAN_CITIES:
        return f"City '{city}' is not supported. Choose from: {', '.join(INDIAN_CITIES)}"
    data = await fetch_weather(city)
    if not data or "main" not in data:
        return "Unable to fetch weather data."
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

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"