# -*- coding: utf-8 -*-
"""collectdata_capstone.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1d7Y8xFVePURt4-p-xjiGk7yWZ31vd3gd
"""

import requests
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()

API_URL = 'http://api.weatherstack.com/current'
API_KEY = os.getenv('api_key')
DB_HOST = os.getenv('db_host')
DB_PORT = os.getenv('db_port')
DB_NAME = os.getenv('db_name')
DB_USER = os.getenv('db_user')
DB_PASS = os.getenv('db_pass')

cities = ["New York", "London", "Tokyo", "Dubai", "Cape Town", "Paris", "Mexico city", "Shanghai", "Cairo", "Lagos", "São Paulo", "Mumbai", "Moscow", "Istanbul", "Seoul"]


def fetch_weather(city):
    params = {
        'access_key': API_KEY,
        'query': city
    }
    response = requests.get(API_URL, params=params)
    data = response.json()
    return {
        'city': city,
        'temperature': data['current']['temperature'],
        'weather_descriptions': data['current']['weather_descriptions'][0],
        'wind_speed': data['current']['wind_speed'],
        'pressure': data['current']['pressure'],
        'humidity': data['current']['humidity'],
        'observation_time': data['current']['observation_time']
          }

def create_engine_connection():
    engine_url = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(engine_url)
    return engine

def store_data(engine, data):
    df = pd.DataFrame([data])
    df.to_sql('Deens_weather', engine, if_exists='append', index=False, schema='student')

def main():
    engine = create_engine_connection()
    for city in cities:
        weather_data = fetch_weather(city)
        store_data(engine, weather_data)

if __name__ == "__main__":
    main()