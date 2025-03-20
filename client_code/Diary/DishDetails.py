import anvil.server


@anvil.server.portable_class
class DishDetails:
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
      Ingredient(ingredients[i], amounts[i], units[i], amounts_in_gram[i])
      for i in range(len(ingredients))
    ]


@anvil.server.portable_class
class Ingredient:
  def __init__(self, ingredient_name, amount, unit, amount_in_grams):
    self.ingredient_name = ingredient_name
    self.amount = amount
    self.unit = unit
    self.amount_in_grams = amount_in_grams
