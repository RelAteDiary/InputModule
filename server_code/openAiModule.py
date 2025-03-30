import anvil.secrets
import anvil.users
import anvil.server

from pydantic import BaseModel
from openai import OpenAI

from .Diary.DishDetails import DishDetails

openai_client = OpenAI(api_key=anvil.secrets.get_secret("openai_api_key"))


class DishModel(BaseModel):
  name: str
  ingredients: list[str]
  ingredient_amounts: list[float]
  ingredient_units: list[str]
  ingredient_amount_in_grams: list[float]


class MealEntryModel(BaseModel):
  dishes: list[DishModel]


class MealFormat(BaseModel):
  food_diary_entries: list[MealEntryModel]


FETCH_INGREDIENTS_PROMPT = """
You will fetch the common basic ingredients for the food given in a short string. If the dish specifies a quantity or unit of measurement, use that; otherwise use one reasonable serving as the size of the dish. Use a reasonable unit of measurement for an ingredient, priority to volume measurements like cup, tablespoon, teaspoon. 
Return it as JSON with the following fields: dishes.
Where dishes is a list of DishModel, a JSON with the following fields:
name, ingredients, ingredient_amounts, ingredient_units,ingredient_amount_in_grams.
name is a string representing the food that the user gave you.
ingredients is a list of strings of the common ingredients for that food.
ingredient_amounts and ingredient_units are two lists that represent the amount found in a typical single serving size (i.e. what one person can reasonably eat in one sitting) of the food as a number and the unit of measurement for that serving as a string.
ingredient_amount_in_grams is the amount in a typical serving in grams; this should match the amount specified in ingredient_amounts and ingredient_units.
If there is no food, then return an empty list. If you are not able to fetch ingredients of a food, leave ingredients, ingredient_amounts, ingredient_units, ingredient_amount_in_grams blank but fill in name.
"""


def call_open_ai_and_get_ingredients(food_text, is_unit_test=False):
  if is_unit_test:
    return MealFormat(
      food_diary_entries=[
        MealEntryModel(
          dishes=[
            DishModel(
              name="Chicken Soup",
              ingredients=[
                "chicken",
                "carrots",
                "celery",
                "onions",
                "garlic",
                "chicken broth",
                "noodles",
              ],
              ingredient_amounts=[1.0, 1.0, 1.0, 0.5, 1.0, 4.0, 1.0],
              ingredient_units=["kg", "cup", "cup", "cup", "clove", "liter", "cup"],
              ingredient_amount_in_grams=[
                1000.0,
                150.0,
                150.0,
                75.0,
                5.0,
                1000.0,
                120.0,
              ],
            ),
            DishModel(
              name="Sourdough Bread",
              ingredients=["sourdough starter", "flour", "water", "salt"],
              ingredient_amounts=[0.1, 0.25, 0.15, 0.01],
              ingredient_units=["kg", "kg", "liter", "g"],
              ingredient_amount_in_grams=[100.0, 250.0, 150.0, 10.0],
            ),
            DishModel(
              name="Fruit Bowl",
              ingredients=["mixed fruits (e.g., apples, bananas, berries)"],
              ingredient_amounts=[1.0],
              ingredient_units=["kg"],
              ingredient_amount_in_grams=[1000.0],
            ),
          ]
        )
      ]
    )
  response = openai_client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
      {"role": "system", "content": FETCH_INGREDIENTS_PROMPT},
      {"role": "user", "content": food_text},
    ],
    response_format=MealFormat,
  )
  return response.choices[0].message.parsed


@anvil.server.callable(require_user=True)
def text_to_ingredients(food_text):
  """
  Calls chatGPT to turn a description of a meal into a list of DishDetails
  Example input: "chicken soup and sourdough bread with fruit bowl"
  Uses O(750) tokens per call.
  """
  try:
    dish_details_list = []
    openai_response = call_open_ai_and_get_ingredients(food_text)
    for food_diary_entry in openai_response.food_diary_entries:
      for dish in food_diary_entry.dishes:
        dish_details = DishDetails(dish_name=dish.name)
        dish_details.set_ingredients_from_lists(
          dish.ingredients,
          dish.ingredient_amounts,
          dish.ingredient_units,
          dish.ingredient_amount_in_grams,
        )
        dish_details_list.append(dish_details)
    print(f"openai_response is {openai_response}")
    return dish_details_list
  except (ValueError, KeyError):
    print("Automatically generating ingredients is not possible right now. Sorry!")

@anvil.server.callable(require_user=True)
def ingredient_is_safe(ingredient):
  diet_restrictions = get_diet_restriction()
  
