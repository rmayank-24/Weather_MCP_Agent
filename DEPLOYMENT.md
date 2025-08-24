# 🚀 Deployment Guide - WeatherAI India

## Quick Deployment Options

### 1. **Streamlit Cloud (Recommended)**

1. **Fork the Repository**
   - Go to the GitHub repository
   - Click "Fork" to create your own copy

2. **Connect to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"

3. **Configure the App**
   - **Repository**: Select your forked repository
   - **Branch**: `main`
   - **Main file path**: `india_streamlit_app.py`
   - **App URL**: Choose your custom URL

4. **Add Secrets**
   - In Streamlit Cloud dashboard, go to "Settings" → "Secrets"
   - Add your OpenWeatherMap API key:
   ```toml
   OPENWEATHER_API_KEY = "your_api_key_here"
   ```

5. **Deploy**
   - Click "Deploy" and wait for the build to complete

### 2. **Heroku Deployment**

1. **Create Heroku App**
   ```bash
   heroku create your-weather-app-name
   ```

2. **Add Buildpacks**
   ```bash
   heroku buildpacks:add heroku/python
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set OPENWEATHER_API_KEY=your_api_key_here
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

### 3. **Docker Deployment**

1. **Build Docker Image**
   ```bash
   docker build -t weather-ai-india .
   ```

2. **Run Container**
   ```bash
   docker run -p 8501:8501 -e OPENWEATHER_API_KEY=your_key weather-ai-india
   ```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENWEATHER_API_KEY` | Your OpenWeatherMap API key | Yes |
| `STREAMLIT_SERVER_PORT` | Port for Streamlit server | No (default: 8501) |
| `STREAMLIT_SERVER_ADDRESS` | Server address | No (default: localhost) |

## API Key Setup

1. **Get OpenWeatherMap API Key**
   - Visit [openweathermap.org/api](https://openweathermap.org/api)
   - Sign up for a free account
   - Generate an API key

2. **Test Your API Key**
   ```bash
   python test_mcp_fixes.py
   ```

## Production Considerations

### Security
- ✅ Never commit API keys to version control
- ✅ Use environment variables for secrets
- ✅ Enable HTTPS in production

### Performance
- ✅ Enable caching for weather data
- ✅ Monitor API rate limits
- ✅ Use CDN for static assets

### Monitoring
- ✅ Set up logging
- ✅ Monitor API usage
- ✅ Track application performance

## Troubleshooting

### Common Issues

1. **API Key Not Working**
   ```bash
   # Test API connection
   curl "https://api.openweathermap.org/data/2.5/weather?q=Delhi,IN&appid=YOUR_API_KEY&units=metric"
   ```

2. **Port Already in Use**
   ```bash
   # Use different port
   streamlit run india_streamlit_app.py --server.port 8502
   ```

3. **Dependencies Missing**
   ```bash
   # Install requirements
   pip install -r requirements.txt
   ```

## Support

For deployment issues:
- Check the [Streamlit documentation](https://docs.streamlit.io/)
- Review the troubleshooting section
- Open an issue on GitHub

---

**Happy Deploying! 🌤️**
