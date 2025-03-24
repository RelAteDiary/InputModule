from ._anvil_designer import IngredientEditPopupTemplate
from anvil import Label, TextBox, FlowPanel, DropDown


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
    self.add_component(quantity_panel)
    amount = TextBox(type='number')
    quantity_panel.add_component(amount, width='50%')
    amount.add_event_handler('lost_focus', self.set_amount)
    unit = DropDown(items=self.get_unit_choices(self.unit), selected_value=self.unit)
    quantity_panel.add_component(unit, width='50%')

  def get_unit_choices(self, current_unit=None):
    default_units = ['', 'tsp', 'tbsp', 'cups', 'oz', 'lb', 'g', 'piece','slice']
    if current_unit is not None and default_units.count(current_unit) == 0:
      return [current_unit] + default_units
    else:
      return default_units

  def set_ingredient(self,  **args):
    self.ingredient = args['sender'].text

  def 