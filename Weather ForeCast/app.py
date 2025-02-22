# app.py
from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("OPENWEATHER_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")

        if not city:
            error = "Please enter a city name."
        else:
            # Build API URL
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            
            try:
                response = requests.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    # Extract weather data
                    weather_data = {
                        "city": data.get("name", city),
                        "temperature": data["main"]["temp"],
                        "description": data["weather"][0]["description"].capitalize(),
                        "icon": data["weather"][0]["icon"],
                        "humidity": data["main"]["humidity"],
                        "wind_speed": data["wind"]["speed"]
                    }
                else:
                    error = f"Error: {response.json().get('message', 'Unknown error')}"
            
            except requests.exceptions.RequestException as e:
                error = f"Connection error: {str(e)}"
    
    return render_template("index.html", weather=weather_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)

# app.py (additional imports)
from flask import jsonify

# Add these routes
@app.route('/weather')
def weather_by_coords():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    # ... same as index() route ...

@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('query')
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={query}&limit=5&appid={API_KEY}"
    response = requests.get(url)
    cities = [{"name": city["name"], "country": city["country"]} for city in response.json()]
    return jsonify(cities)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)  # Allow phone access