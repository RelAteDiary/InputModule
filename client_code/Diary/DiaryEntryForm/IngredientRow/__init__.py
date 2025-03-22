from ._anvil_designer import IngredientRowTemplate
from anvil import alert

class IngredientRow(IngredientRowTemplate):
  def __init__(
    self,
    voilates_diets=['test_diet'],
    amount_and_unit="1 serving",
    ingredient="food",
    **properties,
  ):
    self.init_components(**properties)
    if len(voilates_diets) == 0:
      self.dom_nodes["warning-column"].style.visibility = "hidden"
    else:
      self.dom_nodes['warning-button'].addEventListener('click', lambda **args : print('clicked'))
    self.dom_nodes['quantity-column'].innerText = amount_and_unit
    self.dom_nodes['food-column'].innerText=ingredient
    # Any code you write here will run before the form opens.
