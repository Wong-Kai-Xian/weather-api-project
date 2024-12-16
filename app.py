from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from datetime import datetime
import os
import requests
import matplotlib.pyplot as plt

app = Flask(__name__)

# Get the API key from .env
load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')

def get_daily_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast/daily?q={city}&cnt=10&appid={API_KEY}&units=metric"
    response = requests.get(url)

    # Log the response for debugging
#    print(f"API URL: {url}")
#    print(f"Response Status Code: {response.status_code}")
#    print(f"Response Data: {response.text}")

    if response.status_code == 200:
        data = response.json()
        if 'list' in data:
            # Extract 10 days data
            return data['list'][:10]
        else:
            print("Unexpected API response format. 'list' not found.")
            return None
    else:
        print(f"Error {response.status_code}: {response.json().get('message', 'Unknown error')}")
        return None

def get_hourly_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast/hourly?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    # Log the response for debugging
#    print(f"API URL: {url}")
#    print(f"Response Status Code: {response.status_code}")
#    print(f"Response Data: {response.text}")

    if response.status_code == 200:
        data = response.json()
        if 'list' in data:
            # Extract 24-hour data
            return data['list'][:24]
        else:
            print("Unexpected API response format. 'list' not found.")
            return None
    else:
        print(f"Error {response.status_code}: {response.json().get('message', 'Unknown error')}")
        return None

def get_current_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.json().get('message', 'Unknown error')}")
        return None

def plot_forecast(data, city):
    dates = [entry['dt_txt'] for entry in data['list']]
    temps = [entry['main']['temp'] for entry in data['list']]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, temps, marker='o')
    plt.title(f"Weather Forecast for {city}")
    plt.xlabel("Date & Time")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    image_path = "static/forecast_plot.png"
    plt.savefig(image_path)
    plt.close()
    return image_path

# Define a custom filter for Jinja2
@app.template_filter('timestamp_to_datetime')
def timestamp_to_datetime(utc_timestamp):
    """Convert a UNIX timestamp to a human-readable datetime."""
    timestamp = utc_timestamp + (8 * 60 * 60)
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

@app.template_filter('timestamp_to_day')
def timestamp_to_day(utc_timestamp):
    timestamp = utc_timestamp + (8 * 60 * 60)
    return datetime.fromtimestamp(timestamp).strftime("%A %d %b")


@app.route('/refresh-current-weather', methods=['GET'])
def refresh_current_weather():
    city = request.args.get('city')  # Get the city name from the query parameters
    if not city:
        return jsonify({"success": False, "message": "City not provided"}), 400

    current = get_current_weather(city)
    if current:
        # Use the API's 'dt' field, converted to human-readable format
        timestamp = timestamp_to_datetime(current['dt'])
        return jsonify({
            "success": True,
            "current": current,
            "timestamp":timestamp
        })
    else:
        return jsonify({"success": False, "message": "Failed to fetch current weather"})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form.get('city')

    forecast_data = get_hourly_forecast(city)
    current_data = get_current_weather(city)
    daily_forecast_data = get_daily_forecast(city)

    if current_data and forecast_data and daily_forecast_data :
#        graph_path = plot_forecast(forecast, city)
        return render_template('result.html', city=city, current=current_data, forecast=forecast_data, daily=daily_forecast_data)
    else:
        error = "Unable to retrieve weather data for {city}. Please check the city name or try again later."
        return render_template('index.html', error=error)

@app.route('/details', methods=['GET'])
def details():
    date = request.args.get('date')
    city = request.args.get('city')
    # Convert the date (timestamp) to a readable format
    date_readable = timestamp_to_datetime(int(date))
    daily_data = get_daily_forecast(city)

    # Find the specific day's data based on the timestamp
    selected_day = next((day for day in daily_data['list'] if str(day['dt']) == date), None)

    if not selected_day:
        return "Data not found", 404

    return render_template('details.html', city=city, date=date_readable, day_data=selected_day)


if __name__ == "__main__":
    app.run(debug=True)
