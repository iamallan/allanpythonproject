import streamlit as st
import os
import json
import requests
from git import Repo

def fetch_weather(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to fetch weather data.")
        return None

def convert_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def convert_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

def format_weather(data, temp_format):
    temperature = data['main']['temp']
    if temp_format == 'fahrenheit':
        temperature = convert_to_fahrenheit(temperature)
        unit = '°F'
    else:
        unit = '°C'
    formatted_data = f"Weather Report\n\n"
    formatted_data += f"City: {data['name']}\n"
    formatted_data += f"Temperature: {temperature}{unit}\n"
    formatted_data += f"Description: {data['weather'][0]['description'].capitalize()}\n"
    return formatted_data

def push_to_github(data, repo_path, filename):
    with open(filename, 'w') as f:
        f.write(data)
    
    repo = Repo(repo_path)
    repo.index.add([filename])
    repo.index.commit("Update weather data")
    origin = repo.remote(name='origin')
    origin.push()

if __name__ == "__main__":
    API_KEY = "your_openweathermap_api_key"
    CITY = "your_city"
    REPO_PATH = "path_to_your_local_git_repository"
    FILENAME = "weather.txt"
    TEMP_FORMAT = "fahrenheit"  # or "celsius"

    weather_data = fetch_weather(API_KEY, CITY)
    if weather_data:
        formatted_weather = format_weather(weather_data, TEMP_FORMAT)
        push_to_github(formatted_weather, REPO_PATH, FILENAME)
