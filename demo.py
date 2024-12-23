import os
import requests
from swarm import Swarm, Agent
from openai import OpenAI
import requests 

ollama_client = OpenAI(
    base_url="http://35.244.13.63:11434/v1", 
    api_key='ollama'
)

client = Swarm(client=ollama_client)

API_KEY = os.environ.get('OPENWEATHER_API_KEY')

if not API_KEY:
    raise Exception("OPENWEATHER_API_KEY not set in environment variables")

base_url = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        temperature = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        city_name = data["name"]
        return f"The weather in {city_name} is {weather_description} with a temperature of {temperature}°C."
    else:
        return "Error getting weather data. Please check the city name."

def get_weather_function(arguments):
    city = arguments.get("city")
    if not city:
        return "City name is missing."
    return get_weather(city)

weather_agent = Agent(
    model="llama3.1:latest",
    name="weather_assistant",
    instructions="Provide weather information for a given city name.",
    functions=[get_weather_function]
)

def transfer_to_weather_assistant():
    print("Transferring to the weather assistant...")
    return weather_agent

manager_agent = Agent(
    model="llama3.1:latest",
    name="manager",
    instructions="You help users by directing them to the appropriate assistant.",
    functions=[transfer_to_weather_assistant]
)

response = client.run(
    agent=manager_agent,
    messages=[
        {"role": "user", "content": "Can you tell me the weather in London?"}
    ]
)

print(response)
