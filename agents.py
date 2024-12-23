import json 
from swarm import Agent
from pydantic_ai.models.ollama import OllamaModel
from swarm import Swarm
from openai import OpenAI
import os


ollama_client = OllamaModel(
    base_url="http://35.244.13.63:11434/v1", 
    model_name="llama3.2:latest")

client = Swarm(client=ollama_client)

def get_weather(location,time="now"):
    """Get a current weather in the given location. location must be a city"""
    params= {

        "location": location,
        "time": time
        
    }
    return json.dumps(params=params
    )
    
def send_email(recipient,subject,body):
    print("sending email ")
    print(f"To:{recipient}")
    print(f"Subject:{subject}")
    print(f"Body:{body}")
    return "sent"

weather_agent = Agent(
    name="weather_agent",
    params={
        "location": "string",
        "time": "string"
    },
    instructions="You are a helpful agent",
    functions=[get_weather,send_email])

response=client.run(
    agent=weather_agent,
    
    messages=[
        {"role":"user","content":"What is the weather in London?"}
    ]
    
)

print(response)