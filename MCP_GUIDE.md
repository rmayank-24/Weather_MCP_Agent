# 🤖 MCP Integration Guide - Weather AI Assistant

## What is MCP?

**MCP (Model Context Protocol)** allows you to ask questions about weather data and get automated answers. Think of it as an AI assistant that understands weather information and can respond to your natural language queries.

## 🚀 How to Use MCP with Your Weather App

### Option 1: Full Integration (Recommended)

**Double-click `start_with_mcp.bat`** - This starts both:
- MCP Server (AI assistant backend)
- Streamlit App (main weather dashboard)

### Option 2: Separate Components

1. **Start MCP Server:**
   ```bash
   python mcpserver/server.py
   ```

2. **Start Streamlit App:**
   ```bash
   streamlit run india_streamlit_app.py
   ```

3. **Use MCP Client (Optional):**
   ```bash
   python mcp_client.py
   ```

## 💬 How to Ask Questions

### In the Streamlit App:
1. Go to **"AI Weather Assistant"** page
2. Type your question in the chat box
3. Click **"Ask AI Assistant"**

### In the MCP Client:
1. Run `python mcp_client.py`
2. Type your questions directly in the terminal

## 🎯 Example Questions You Can Ask

### Weather Queries:
- "What's the weather in Delhi?"
- "Temperature in Mumbai"
- "How's the weather in Bangalore?"
- "Weather forecast for Chennai"
- "Humidity in Kolkata"

### General Questions:
- "What can you help me with?"
- "Help"
- "What cities do you support?"
- "Tell me about temperature"
- "How do forecasts work?"

## 🏙️ Supported Cities

The AI assistant supports all major Indian cities:
- Delhi, Mumbai, Bangalore, Chennai, Kolkata
- Hyderabad, Pune, Ahmedabad, Jaipur, Lucknow
- Chandigarh, Bhopal, Indore, Patna, Nagpur
- Kanpur, Thiruvananthapuram, Coimbatore, Vadodara, Surat

## 🔧 How It Works

### 1. **Natural Language Processing**
The AI understands your questions and extracts:
- City names
- Weather parameters (temperature, humidity, etc.)
- Question types (current weather, forecast, etc.)

### 2. **API Integration**
- Connects to OpenWeatherMap API
- Fetches real-time weather data
- Processes and formats responses

### 3. **Smart Responses**
- Provides relevant weather information
- Suggests related questions
- Offers help and guidance

## 📱 Features

### ✅ What Works:
- Current weather for any Indian city
- Temperature, humidity, wind speed
- Weather conditions and descriptions
- Natural language understanding
- Interactive chat interface
- Real-time data updates

### 🔄 Coming Soon:
- 5-day weather forecasts
- Historical weather data
- Weather comparisons
- Advanced analytics

## 🛠️ Troubleshooting

### If MCP doesn't work:

1. **Check API Key:**
   - Ensure `.env` file has your OpenWeatherMap API key
   - Get free API key from: https://openweathermap.org/api

2. **Check Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Check Ports:**
   - MCP server runs on port 8000
   - Streamlit runs on port 8501
   - Make sure these ports are available

4. **Restart Services:**
   - Stop all running processes
   - Run `start_with_mcp.bat` again

### Common Issues:

**"MCP connection failed"**
- Make sure MCP server is running
- Check if port 8000 is available

**"API key not found"**
- Create `.env` file with your API key
- Format: `OPENWEATHER_API_KEY=your_key_here`

**"City not found"**
- Use supported city names
- Check spelling and capitalization

## 🎉 Quick Start Commands

```bash
# Option 1: One-click start (Windows)
start_with_mcp.bat

# Option 2: Manual start
python mcpserver/server.py &
streamlit run india_streamlit_app.py

# Option 3: Interactive MCP client
python mcp_client.py
```

## 💡 Pro Tips

1. **Be Specific:** Ask "What's the weather in Delhi?" instead of just "weather"

2. **Use City Names:** Include the city name in your question

3. **Try Different Formats:**
   - "Temperature in Mumbai"
   - "How's the weather in Bangalore?"
   - "Weather forecast for Chennai"

4. **Ask for Help:** Type "help" or "what can you do" to see available features

5. **Use the Chat Interface:** The Streamlit app has a nice chat interface for better experience

## 🔗 Integration with Other Tools

The MCP server can be integrated with:
- **AI Assistants** (Claude, GPT, etc.)
- **IDEs** (VS Code, PyCharm)
- **Chat Applications**
- **Custom Applications**

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Ensure all dependencies are installed
3. Verify your API key is working
4. Try restarting the services

---

**Enjoy your AI-powered weather assistant! 🌤️**
