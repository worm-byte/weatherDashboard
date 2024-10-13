'''
Replace API key with your API key from OpenWeatherMap.
To run, use command: streamlit run fetchWeatherData.py
'''
import requests
from datetime import datetime
import pytz
import streamlit as st

API_KEY = "your_API_key"

def convert_unix_to_time(timestamp):
    local_tz = pytz.timezone('America/New_York')
    dt = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
    return dt.astimezone(local_tz).strftime('%I:%M %p')

def get_weather(city):
    BASE_URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "City": city,
            "Country": data["sys"]["country"],
            "Temperature (°C)": data["main"]["temp"],
            "FeelsLike": data["main"]["feels_like"],
            "Weather": data["weather"][0]["description"],
            "Humidity (%)": data["main"]["humidity"],
            "WindSpeed": data["wind"]["speed"],
            "Sunrise":convert_unix_to_time(data["sys"]["sunrise"]),
            "Sunset":convert_unix_to_time(data["sys"]["sunset"])
        }
        return weather_info
    else:
        return None

st.title("Real-Time :blue[Weather] Dashboard 🌦️")

city = st.text_input("Enter a city:")

if city:
    data = get_weather(city)
    if data:
        st.write(f"### Weather in {city}, {data['Country']}")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Temperature (°C) 🌡", data['Temperature (°C)'])
        col2.metric("FeelsLike (°C) 🤭", data['FeelsLike'])
        col3.metric("Wind km/h 🌬️", data['WindSpeed'])
        col4.metric("Humidity % 😅", data['Humidity (%)'])

        col5, col6 = st.columns(2)
        col5.metric("Sunrise 🌞", data['Sunrise'])
        col6.metric("Sunset 🌚", data['Sunset'])

    else:
        st.error("City not found. Please try again.")










