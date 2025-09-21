from extract import fetch_weather
from transform import transform_weather_data
from config import CITIES
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# 1) extrair
raw_data = []
for city in CITIES:
    data = fetch_weather(city, API_KEY)
    raw_data.append(data)

# 2) transformar
df = transform_weather_data(raw_data)

print(df.head())
df.to_csv("data/outputs/weather_summary.csv", index=False)

