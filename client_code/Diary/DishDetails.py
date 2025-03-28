import anvil.server
from .IngredientDetails import IngredientDetails


@anvil.server.portable_class
class DishDetails:
  def __init__(self, dish_name=""):
    self.dish_name = dish_name
    self.ingredients = []

  def set_ingredients_from_lists(
    self, ingredient_names, amounts, units, amounts_in_gram
  ):
    if (
      len(ingredient_names) != len(amounts)
      or len(ingredient_names) != len(units)
      or len(ingredient_names) != len(amounts_in_gram)
    ):
      print(
        f"ingredient_names of length {len(ingredient_names)} = {ingredient_names}; "
        + f"\n amounts of length {len(amounts)} = {amounts} \n"
        + f"units of length {len(units)} = {units} \n"
        + f"amounts_in_gram of length {len(amounts_in_gram)} = {amounts_in_gram}"
      )
      raise (
        "ERROR the length of ingredients, amounts, units, and amount in grams should be the same!"
      )
    self.ingredients = [
      IngredientDetails(ingredient_names[i], amounts[i], units[i], amounts_in_gram[i])
      for i in range(len(ingredient_names))
    ]

  def set_ingredients(self, ingredients):
    self.ingredients = ingredients
