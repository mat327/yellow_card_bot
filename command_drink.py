import requests
import json

def get_drink(): #api z drinkami
  response = requests.get("https://www.thecocktaildb.com/api/json/v1/1/random.php")
  json_data = json.loads(response.text)
  quote = json_data["drinks"][0]['strDrink'] + " -" + json_data["drinks"][0]['strInstructions'] + " " + json_data["drinks"][0]['strDrinkThumb']

  i = [] #tworzenie stringa ze składnikami
  ingredients = " \n Ingredients : "
  for n in range(15): 
   i.append(json_data["drinks"][0]['strIngredient' + str(n+1)])
   if str(i[n]) != "None":
      ingredients += str(i[n]) + ", "

  return(quote + ingredients)