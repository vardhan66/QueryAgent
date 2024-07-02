import requests 
import os, json 
from dotenv import load_dotenv, find_dotenv 

# Loading the environment variables by finding the .env file
load_dotenv(find_dotenv())

def get_llm_response(model: str, prompt: str) -> str:
    response = requests.post(url=os.environ['OLLAMA_API_URL'], 
                             data=json.dumps(dict(model=model, prompt=prompt, stream=False, keepalive=True)))
    response = response.json()
    return response['response']

