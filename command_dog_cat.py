import requests
import json

def get_cat(): #api z kotami
  response = requests.get("https://api.thecatapi.com/v1/images/search")
  json_data = json.loads(response.text)
  quote = json_data[0]['url']
  return(quote)

def get_dog(): #api z kotami
  response = requests.get("https://api.thedogapi.com/v1/images/search")
  json_data = json.loads(response.text)
  quote = json_data[0]['url']
  return(quote)