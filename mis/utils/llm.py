import requests 
import os, json 
from dotenv import load_dotenv, find_dotenv 

# Loading the environment variables by finding the .env file
load_dotenv(find_dotenv())

# Loading prototype data file 
global prototype_data, prototype_file
prototype_file = open(os.environ['PROTOTYPE_FILE'])
prototype_data = json.load(prototype_file)


def get_llm_response(model: str, prompt: str) -> str:
    response = requests.post(url=os.environ['OLLAMA_API_URL'], 
                             data=json.dumps(dict(model=model, prompt=prompt, stream=False, keepalive=True)))
    response = response.json()
    return response['response']


def get_function_prototypes(category_map: dict) -> str:
    primary_category: str = category_map['primary_category']
    secondary_categories: list[str] = category_map['secondary_category']
    prototypes: list[str] = list() 

    for category in secondary_categories:
        function_prototypes: str = prototype_data[primary_category][category]
        prototypes.append(function_prototypes)

    return prototypes

