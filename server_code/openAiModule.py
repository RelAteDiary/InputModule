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

openai_client = OpenAI(api_key=anvil.secrets.get_secret("openai_api_key"))


class DishDetails(BaseModel):
  food: str
  ingredients: list[str]
  ingredient_amount: list[float]
  ingredient_unit: list[str]


class MealEntryDetails(BaseModel):
  dishes: list[DishDetails]


class MealEntry(BaseModel):
  food_diary_entries: list[MealEntryDetails]


class DishEntry:
  def __init__(self, dish_name, ingredients, amounts, units, amounts_in_gram):
    self.dish_name = dish_name
    if (
      len(ingredients) != len(amounts)
      or len(ingredients) != len(units)
      or len(ingredients) != len(amounts_in_gram)
    ):
      raise (
        "ERROR the length of ingredients, amounts, units, and amount in grams should be the same!"
      )
    self.ingredients = [
      self.Ingredients(
        ingredients[i], amounts[i], amounts[i], units[i], amounts_in_gram[i]
      )
      for i in range(len(ingredients))
    ]

  class Ingredients:
    def __init__(self, ingredient_name, amount, unit, amount_in_grams):
      self.ingredient_name = ingredient_name
      self.amount = amount
      self.unit = unit
      self.amount_in_grams = amount_in_grams


FETCH_INGREDIENTS_PROMPT = """
You will fetch the common basic ingredients for the food given in a short string. If the dish specifies a quantity or unit of measurement, use that; otherwise use one reasonable serving as the size of the dish. Prioritize familiarity when choosing unit of measurement for an ingredient. 
Return it as JSON with the following fields: dishes.
Where dishes is a list of DishDetails, a JSON with the following fields:
food, ingredients, ingredient_amount, ingredient_unit.
food is a string representing the food that the user gave you.
ingredients is a list of strings of the common ingredients for that food.
ingredient_amount and ingredient_unit are two lists that represent the amount found in a typical serving size of the food as a number and the unit of measurement for that serving as a string.
If there is no food, then return an empty list. If you are not able to fetch ingredients of a food, leave ingredients, ingredient_amount, ingredient_unit blank but fill in food.
"""
unit_test_food_text = "chicken soup and sourdough bread with fruit bowl"


def call_open_ai_and_get_ingredients(food_text):
  response = openai_client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
      {"role": "system", "content": FETCH_INGREDIENTS_PROMPT},
      {"role": "user", "content": food_text},
    ],
    response_format=MealEntry,
  )
  return response.choices[0].message.parsed


@anvil.server.callable(require_user=True)
def text_to_ingredients(food_text):
  # TODO check user is logged in
  try:
    openai_response = call_open_ai_and_get_ingredients(food_text)
    openai_response.MealEntry
    print(f"openai_response is {openai_response}")
    # for food_diary_entry in openai_response:
  except (ValueError, KeyError):
    print("Automatically generating ingredients is not possible right now. Sorry!")
