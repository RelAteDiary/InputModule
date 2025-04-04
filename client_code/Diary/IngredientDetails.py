import anvil.server

@anvil.server.portable_class
class IngredientDetails:
  def __init__(self, ingredient_name, amount, unit, amount_in_grams, violates_diets=[]):
    self.ingredient_name = ingredient_name
    self.amount = amount
    self.unit = unit
    self.amount_in_grams = amount_in_grams
    # This field is not populated in the database
    self.violates_diets = violates_diets