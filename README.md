# Weather Dashboard
A web-based application that provides users with real-time weather data, air quality information, and local news updates based on their location input. The app integrates various APIs to fetch weather conditions, forecasts, air quality indices, and news for a specific location.

## Features
- **Real-time Weather**: Displays current weather conditions including temperature, weather description, and location name.
- **Hourly Forecast**: Shows a 24-hour forecast with temperature and weather conditions for each hour.
- **10-Day Forecast**: Displays weather conditions, min, and max temperatures for the next 10 days.
- **Air Quality Index (AQI)**: Provides air quality readings along with pollutant levels in different regions.
- **Top News**: Displays the top 3 trending news articles for the user’s location.
- **Refresh Functionality**: Allows users to refresh data for updated weather and air quality information.

## Requirements
- Python 3.x
- Flask
- Requests
- Matplotlib
- dotenv

## File Structure Description
weather-dashboard/
│
├── static/
│   └── style.css           # Contains the CSS styles used to format and design the webpage
│
├── templates/
│   ├── index.html          # User input page where users enter the location for weather data
│   ├── result.html         # Displays the weather data after the user inputs a location
│   └── details.html        # Displays detailed weather data for a specific day (e.g., temperature, humidity, wind speed)
│
├── app.py                  # The main Flask application file that handles routing and API calls
