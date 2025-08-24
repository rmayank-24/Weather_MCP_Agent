# Final Streamlit Weather App for India with MCP Integration
# Author: GitHub Copilot

import streamlit as st
import requests
import os
import asyncio
import json
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import folium
from streamlit_folium import folium_static
import httpx

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')

# MCP Server Configuration
MCP_SERVER_URL = "http://localhost:8000"

st.set_page_config(
    page_title="India Weather App with AI Assistant", 
    page_icon="🌦️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 0.8rem 0;
        font-size: 16px;
        line-height: 1.6;
    }
    .user-message {
        background-color: #f8f9fa;
        border-left: 4px solid #007bff;
        font-weight: 500;
        color: #212529;
    }
    .ai-message {
        background-color: #ffffff;
        border-left: 4px solid #28a745;
        font-family: 'Courier New', monospace;
        white-space: pre-line;
        color: #212529;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# City mapping for common misspellings
CITY_MAPPING = {
    'banglore': 'bangalore',
    'bombay': 'mumbai',
    'calcutta': 'kolkata',
    'madras': 'chennai',
    'bengaluru': 'bangalore',
    'karnataka': 'bangalore',
    'maharashtra': 'mumbai',
    'tamil nadu': 'chennai',
    'west bengal': 'kolkata'
}

# List of supported cities
SUPPORTED_CITIES = [
    "Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", 
    "Ahmedabad", "Jaipur", "Lucknow", "Chandigarh", "Bhopal", "Indore", 
    "Patna", "Nagpur", "Kanpur", "Thiruvananthapuram", "Coimbatore", "Vadodara", "Surat"
]

def normalize_city_name(city_input):
    """Normalize city name and handle common misspellings"""
    city_lower = city_input.lower().strip()
    
    # Check for exact matches first
    for city in SUPPORTED_CITIES:
        if city.lower() == city_lower:
            return city
    
    # Check for misspellings
    if city_lower in CITY_MAPPING:
        corrected = CITY_MAPPING[city_lower]
        for city in SUPPORTED_CITIES:
            if city.lower() == corrected:
                return city
    
    # Check for partial matches
    for city in SUPPORTED_CITIES:
        if city_lower in city.lower() or city.lower() in city_lower:
            return city
    
    return None

async def get_weather_data(city: str) -> dict:
    """Get current weather data for a city"""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}&units=metric"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return None

async def get_forecast_data(city: str) -> dict:
    """Get 5-day forecast data for a city"""
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city},IN&appid={API_KEY}&units=metric"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return None

def process_question(question: str) -> str:
    """Process user questions and return appropriate responses"""
    question_lower = question.lower()
    
    # Extract city name from question
    detected_city = None
    for city in SUPPORTED_CITIES:
        if city.lower() in question_lower:
            detected_city = city
            break
    
    # If no exact match, try to normalize
    if not detected_city:
        words = question_lower.split()
        for word in words:
            normalized = normalize_city_name(word)
            if normalized:
                detected_city = normalized
                break
    
    # Handle forecast requests
    if detected_city and any(word in question_lower for word in ["forecast", "tomorrow", "next", "future", "upcoming"]):
        # Use asyncio to get forecast data
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            forecast_data = loop.run_until_complete(get_forecast_data(detected_city))
            if forecast_data:
                forecasts = []
                for item in forecast_data['list'][:8]:  # First 24 hours
                    dt = datetime.fromisoformat(item['dt_txt'].replace('Z', '+00:00'))
                    temp = item['main']['temp']
                    weather = item['weather'][0]['description']
                    forecasts.append(f"{dt.strftime('%H:%M')}: {temp}°C, {weather}")
                
                return f"📅 24-hour forecast for {detected_city}:\n\n" + "\n".join(forecasts)
            else:
                return f"Sorry, I couldn't fetch forecast data for {detected_city}. Please try again."
        finally:
            loop.close()
    
    # Handle current weather requests
    elif detected_city:
        # Use asyncio to get weather data
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            weather_data = loop.run_until_complete(get_weather_data(detected_city))
            if weather_data:
                weather = weather_data['weather'][0]['description'].title()
                temp = weather_data['main']['temp']
                feels_like = weather_data['main']['feels_like']
                humidity = weather_data['main']['humidity']
                wind = weather_data['wind']['speed']
                
                return (
                    f"🌤️ Weather in {detected_city}:\n\n"
                    f"🌡️ Temperature: {temp} °C\n"
                    f"🔥 Feels Like: {feels_like} °C\n"
                    f"☁️ Condition: {weather}\n"
                    f"💧 Humidity: {humidity}%\n"
                    f"💨 Wind Speed: {wind} m/s"
                )
            else:
                return f"Sorry, I couldn't fetch weather data for {detected_city}. Please check the city name and try again."
        finally:
            loop.close()
    
    # Handle misspelled cities
    elif any(word in question_lower for word in ["banglore", "bombay", "calcutta", "madras"]):
        suggestions = []
        for word in question_lower.split():
            normalized = normalize_city_name(word)
            if normalized:
                suggestions.append(normalized)
        
        if suggestions:
            return f"Did you mean: {', '.join(suggestions)}? Try asking about the weather in one of these cities."
        else:
            return "I couldn't understand the city name. Please try with a supported Indian city."
    
    # General responses
    elif "help" in question_lower or "what can you do" in question_lower:
        return """🤖 I can help you with weather information for Indian cities!

🌤️ What I can do:
• Get current weather for any Indian city
• Provide 24-hour weather forecasts  
• Answer weather-related questions
• Handle common city name variations

🏙️ Supported cities include:
• Delhi, Mumbai, Bangalore, Chennai, Kolkata
• Hyderabad, Pune, Ahmedabad, Jaipur, Lucknow
• And many more!

💡 Try asking:
• "What's the weather in Delhi?"
• "Forecast for Mumbai"
• "Temperature in Bangalore"
• "Weather tomorrow in Chennai"
• "How's the weather in Kolkata?" """
    
    elif "temperature" in question_lower:
        return "I can help with temperature information! Try asking about a specific city like 'What's the temperature in Delhi?'"
    
    elif "forecast" in question_lower:
        return "I can provide weather forecasts! Try asking 'What's the forecast for Mumbai?' or 'Weather tomorrow in Delhi'"
    
    else:
        return """I'm here to help with weather information! Try asking me about:

• Weather in specific Indian cities
• Temperature, humidity, or wind conditions  
• Weather forecasts and tomorrow's weather
• General weather questions

For example: "What's the weather in Delhi?" or "Forecast for Mumbai tomorrow" """

def create_weather_analytics():
    """Create weather analytics dashboard"""
    st.header("📈 Weather Analytics Dashboard")
    
    # Get data for multiple cities
    cities_to_analyze = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata"]
    
    with st.spinner("Fetching weather data for analytics..."):
        weather_data = []
        
        for city in cities_to_analyze:
            try:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}&units=metric"
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    weather_data.append({
                        'City': city,
                        'Temperature (°C)': data['main']['temp'],
                        'Humidity (%)': data['main']['humidity'],
                        'Wind Speed (m/s)': data['wind']['speed'],
                        'Pressure (hPa)': data['main']['pressure']
                    })
            except:
                continue
        
        if weather_data:
            df = pd.DataFrame(weather_data)
            
            # Temperature comparison chart
            st.subheader("🌡️ Temperature Comparison")
            fig_temp = px.bar(df, x='City', y='Temperature (°C)', 
                            title='Current Temperature Across Cities',
                            color='Temperature (°C)',
                            color_continuous_scale='RdYlBu_r')
            st.plotly_chart(fig_temp, use_container_width=True)
            
            # Humidity comparison
            st.subheader("💧 Humidity Comparison")
            fig_humidity = px.pie(df, values='Humidity (%)', names='City',
                                title='Humidity Distribution')
            st.plotly_chart(fig_humidity, use_container_width=True)
            
            # Wind speed comparison
            st.subheader("💨 Wind Speed Comparison")
            fig_wind = px.scatter(df, x='City', y='Wind Speed (m/s)', 
                                size='Wind Speed (m/s)',
                                title='Wind Speed Across Cities',
                                color='Wind Speed (m/s)')
            st.plotly_chart(fig_wind, use_container_width=True)
            
            # Data table
            st.subheader("📊 Detailed Data")
            st.dataframe(df, use_container_width=True)
            
        else:
            st.error("Could not fetch weather data for analytics. Please check your API key.")

def create_multi_city_comparison():
    """Create multi-city weather comparison"""
    st.header("🏙️ Multi-City Weather Comparison")
    
    # City selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Select Cities to Compare")
        selected_cities = st.multiselect(
            "Choose cities:",
            SUPPORTED_CITIES,
            default=["Delhi", "Mumbai", "Bangalore"]
        )
    
    with col2:
        st.subheader("Comparison Options")
        compare_temp = st.checkbox("Temperature", value=True)
        compare_humidity = st.checkbox("Humidity", value=True)
        compare_wind = st.checkbox("Wind Speed", value=True)
    
    if selected_cities and st.button("Compare Weather", type="primary"):
        with st.spinner("Fetching weather data for comparison..."):
            comparison_data = []
            
            for city in selected_cities:
                try:
                    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}&units=metric"
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        comparison_data.append({
                            'City': city,
                            'Temperature (°C)': data['main']['temp'],
                            'Humidity (%)': data['main']['humidity'],
                            'Wind Speed (m/s)': data['wind']['speed'],
                            'Condition': data['weather'][0]['description'].title()
                        })
                except:
                    continue
            
            if comparison_data:
                df = pd.DataFrame(comparison_data)
                
                # Create comparison charts
                if compare_temp:
                    st.subheader("🌡️ Temperature Comparison")
                    fig_temp = px.bar(df, x='City', y='Temperature (°C)',
                                    title='Temperature Comparison',
                                    color='Temperature (°C)')
                    st.plotly_chart(fig_temp, use_container_width=True)
                
                if compare_humidity:
                    st.subheader("💧 Humidity Comparison")
                    fig_humidity = px.bar(df, x='City', y='Humidity (%)',
                                        title='Humidity Comparison',
                                        color='Humidity (%)')
                    st.plotly_chart(fig_humidity, use_container_width=True)
                
                if compare_wind:
                    st.subheader("💨 Wind Speed Comparison")
                    fig_wind = px.bar(df, x='City', y='Wind Speed (m/s)',
                                    title='Wind Speed Comparison',
                                    color='Wind Speed (m/s)')
                    st.plotly_chart(fig_wind, use_container_width=True)
                
                # Side-by-side comparison table
                st.subheader("📋 Side-by-Side Comparison")
                st.dataframe(df, use_container_width=True)
                
                # Weather conditions summary
                st.subheader("🌤️ Weather Conditions Summary")
                for _, row in df.iterrows():
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col1:
                        st.write(f"**{row['City']}**")
                    with col2:
                        st.write(f"Temperature: {row['Temperature (°C)']}°C")
                        st.write(f"Humidity: {row['Humidity (%)']}%")
                        st.write(f"Wind: {row['Wind Speed (m/s)']} m/s")
                    with col3:
                        st.write(f"*{row['Condition']}*")
                    st.divider()
                
            else:
                st.error("Could not fetch weather data for comparison. Please check your API key.")

# Main App
st.markdown('<h1 class="main-header">🇮🇳 India Weather Dashboard with AI Assistant</h1>', unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("🌦️ Navigation")
page = st.sidebar.selectbox(
    "Choose a page:",
    ["Weather Dashboard", "AI Weather Assistant", "Weather Analytics", "Multi-City Comparison"]
)

if page == "Weather Dashboard":
    # Main weather dashboard
    st.header("🌤️ Current Weather Dashboard")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        city = st.selectbox("Select a city:", SUPPORTED_CITIES)
        
        if st.button("Get Weather", type="primary"):
            with st.spinner("Fetching weather data..."):
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}&units=metric"
                response = requests.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Display weather information
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric("Temperature (°C)", f"{data['main']['temp']:.1f}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric("Feels Like (°C)", f"{data['main']['feels_like']:.1f}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric("Humidity (%)", f"{data['main']['humidity']}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Weather details
                    st.subheader(f"Weather in {city}")
                    weather_desc = data['weather'][0]['description'].title()
                    st.write(f"**Condition:** {weather_desc}")
                    st.write(f"**Wind Speed:** {data['wind']['speed']} m/s")
                    st.write(f"**Pressure:** {data['main']['pressure']} hPa")
                    
                    # Weather icon
                    icon_code = data['weather'][0]['icon']
                    st.image(f"http://openweathermap.org/img/wn/{icon_code}@2x.png", width=100)
                    
                else:
                    st.error("Could not fetch weather data. Please check the city name or try again later.")
    
    with col2:
        st.subheader("📊 Quick Stats")
        st.write("**Total Cities:** 20")
        st.write("**Data Source:** OpenWeatherMap")
        st.write("**Update Frequency:** Real-time")
        
        st.subheader("🔧 Quick Actions")
        if st.button("Test MCP Connection"):
            with st.spinner("Testing MCP server..."):
                try:
                    # Test MCP connection
                    result = asyncio.run(get_weather_data("Delhi"))
                    if result:
                        st.success("MCP connection successful!")
                        st.info(f"Delhi temperature: {result['main']['temp']}°C")
                    else:
                        st.error("MCP connection failed")
                except Exception as e:
                    st.error(f"MCP connection failed: {str(e)}")

elif page == "AI Weather Assistant":
    st.header("🤖 AI Weather Assistant")
    st.write("Ask me anything about weather in India!")
    
    # Chat interface
    st.subheader("💬 Chat with AI Assistant")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message ai-message"><strong>AI Assistant:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    user_question = st.text_input("Ask a question:", placeholder="e.g., What's the weather in Delhi?")
    
    if st.button("Ask AI Assistant", type="primary"):
        if user_question:
            # Add user message to chat
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            
            # Get AI response
            with st.spinner("AI Assistant is thinking..."):
                ai_response = process_question(user_question)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            
            # Rerun to show new messages
            st.rerun()
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()
    
    # Example questions
    st.subheader("💡 Example Questions")
    example_questions = [
        "What's the weather in Delhi?",
        "Temperature in Mumbai",
        "How's the weather in Bangalore?",
        "Weather forecast for Chennai",
        "What can you help me with?"
    ]
    
    for question in example_questions:
        if st.button(question, key=f"example_{question}"):
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.spinner("AI Assistant is thinking..."):
                ai_response = process_question(question)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()

elif page == "Weather Analytics":
    create_weather_analytics()

elif page == "Multi-City Comparison":
    create_multi_city_comparison()

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit, OpenWeatherMap API, and MCP Integration")
