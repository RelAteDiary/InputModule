from ._anvil_designer import IngredientEditPopupTemplate
from anvil import Label, TextBox


class IngredientEditPopup(IngredientEditPopupTemplate):
  def __init__(self, ingredient='', quantity=1, unit='', **properties):
    self.ingredient = ingredient
    self.quantity = quantity
    self.unit = unit
    
    self.init_components(**properties)
    self.add_component(Label(text='The dish contains this ingredient:'))
    ingredient_name_text_box = TextBox(text=ingredient)
    self.add_component(ingredient_name_text_box)
    ingredient_name_text_box.add_event_handler('lost_focus', self.set_ingredient)

    self.add_component(Label('In this quantity:'))
    quantity_panel = FlowPanel()
    self.add_component()

  def get_default_units(self):
    return ['', 'tsp', 'tbsp', 'cups', 'oz', 'lb', 'g', 'piece','slice']

  def set_ingredient(self,  **args):
    self.ingredient = args['sender'].text