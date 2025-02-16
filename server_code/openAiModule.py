import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from pydantic import BaseModel
from openai import OpenAI

openai_client = OpenAI(api_key=anvil.secrets.get_secret('openai_api_key'))
fetch_common_ingredients_prompt = '''
You will fetch the common basic ingredients for the food given in a short string. If the dish specifies a quantity or unit of measurement, use that; otherwise use one reasonable serving as the size of the dish. Prioritize familiarity when choosing unit of measurement for an ingredient. 
Return it as JSON with the following fields: dishes.
Where dishes is a list of DishDetails, a JSON with the following fields:
food, ingredients, ingredient_amount, ingredient_unit.
food is a string representing the food that the user gave you.
ingredients is a list of strings of the common ingredients for that food.
ingredient_amount and ingredient_unit are two lists that represent the amount found in a typical serving size of the food as a number and the unit of measurement for that serving as a string.
If there is no food, then return an empty list. If you are not able to fetch ingredients of a food, leave ingredients, ingredient_amount, ingredient_unit blank but fill in food.
'''
food_text = 'chicken soup and sourdough bread with fruit bowl'

class FoodDiaryEntry(BaseModel):
  class DishDetails(BaseModel):
    food:str
    ingredients: list[str]
    ingredient_amount: list[float]
    ingredient_unit: list[str]
  class FoodDiaryEntryDetails(BaseModel):
    dishes: list[DishDetails]

  food_diary_entries: list[FoodDiaryDetails]
  
response = openai_client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": fetch_common_ingredients_prompt},
        {"role": "user", "content": food_text},
    ],
    response_format=FoodDiaryEntry,
)

def text_to_ingredients(food_text):
  response = openai_client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": fetch_common_ingredients_prompt},
        {"role": "user", "content": food_text},
    ],
    response_format=FoodDiaryEntry,
  )
  return response.choices[0].message.parsed