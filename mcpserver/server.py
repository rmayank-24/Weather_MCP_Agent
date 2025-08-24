
import os
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP(
    name="weather",
    host="0.0.0.0",
    port=8000,
)

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
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
                {period['name']}:
                Temperature: {period['temperature']}°{period['temperatureUnit']}
                Wind: {period['windSpeed']} {period['windDirection']}
                Forecast: {period['detailedForecast']}
                """
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

# Run the server
if __name__ == "__main__":
    transport = "sse"
    if transport == "stdio":
        print("Running server with stdio transport")
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Running server with SSE transport")
        mcp.run(transport="sse")
    else:
        raise ValueError(f"Unknown transport: {transport}")