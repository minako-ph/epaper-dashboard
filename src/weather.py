import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import math

# Load .env file
load_dotenv()


def get_weather():
    # Read values from .env file
    api_key = os.getenv("OPENWEATHER_API_KEY")
    latitude = os.getenv("LATITUDE")
    longitude = os.getenv("LONGITUDE")
    timezone_offset = int(os.getenv("TIMEZONE_OFFSET"))

    base_url = "https://api.openweathermap.org/data/2.5/onecall?"
    url = f"{base_url}lat={latitude}&lon={longitude}&exclude=minutely,hourly,alerts&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    today = datetime.now()
    seven_days_later = today + timedelta(days=7)

    result = []
    for day in data["daily"]:
        dt = datetime.fromtimestamp(day["dt"] + timezone_offset)
        if today <= dt < seven_days_later:
            weather_id = day["weather"][0]["id"]
            max_temp = day["temp"]["max"]
            min_temp = day["temp"]["min"]
            day = dt.strftime('%A')
            result.append({
                'weather_id': str(weather_id),
                'max_temp': math.trunc(max_temp),
                'min_temp': math.trunc(min_temp),
                'day': day
            })
    return result


def get_contents_coordinates():
    result = []
    for i in range(7):
        if i <= 3:
            result.append({
                'image': {
                    'y': 225,
                    'x': 24 + (132 + 8) * i + 8,
                },
                'day': {
                    'y': 235,
                    'x': 24 + (132 + 8) * i + 60
                },
                'temperature': {
                    'y': 255,
                    'x': 24 + (132 + 8) * i + 60
                }
            })
        else:
            result.append({
                'image': {
                    'y': 333,
                    'x': 24 + (132 + 8) * (i - 4) + 8,
                },
                'day': {
                    'y': 343,
                    'x': 24 + (132 + 8) * (i - 4) + 60
                },
                'temperature': {
                    'y': 363,
                    'x': 24 + (132 + 8) * (i - 4) + 60
                }
            })
    return result


def get_weather_icon(id):
    if (id[0] == '2'):
        return 'kaminari.jpg'
    elif (id[0] == '3'):
        return 'ame.jpg'
    elif (id[0] == '5'):
        return 'ame.jpg'
    elif (id[0] == '6'):
        return 'yuki.jpg'
    elif (id[0] == '7'):
        return 'kumori.jpg'
    elif (id == '800'):
        return 'hare.jpg'
    elif (id[0] == '8'):
        return 'kumori.jpg'
