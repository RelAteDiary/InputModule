from ._anvil_designer import IngredientEditPopupTemplate
from ...IngredientDetails import IngredientDetails

from anvil import Label, TextBox, FlowPanel, DropDown
from m3.components import Button

# TODO add a convert unit feature
class IngredientEditPopup(IngredientEditPopupTemplate):
  def __init__(self, ingredient="", quantity=1, unit="", **properties):
    self.ingredient = ingredient
    self.quantity = quantity
    self.unit = unit

    self.init_components(**properties)
    self.add_component(Label(text="The dish contains this ingredient:"))
    ingredient_name_text_box = TextBox(text=ingredient)
    self.add_component(ingredient_name_text_box)
    ingredient_name_text_box.add_event_handler("lost_focus", self.set_ingredient)

    self.add_component(Label(text="In this quantity:"))
    quantity_panel = FlowPanel()
    self.add_component(quantity_panel)
    amount = TextBox(text=quantity, type="number")
    quantity_panel.add_component(amount, width="40%")
    amount.add_event_handler("lost_focus", self.set_quantity)
    unit = DropDown(items=self.get_unit_choices(self.unit), selected_value=self.unit)
    quantity_panel.add_component(unit, width="40%")
    unit.add_event_handler("change", self.set_unit)

    button_panel = FlowPanel(align="center")
    self.add_component(button_panel)

    discard_button = Button(text="Discard", appearance="outlined")
    button_panel.add_component(discard_button)
    discard_button.add_event_handler(
      "click",
      lambda **args: self.raise_event("x-close-alert", value=None),
    )

    save_button = Button(text="Save")
    button_panel.add_component(save_button)
    save_button.add_event_handler(
      "click",
      lambda **args: self.raise_event("x-close-alert", value=self.to_ingredient_details()),
    )

  def to_ingredient_details(self):
    # TODO violate diet should be checked!
    return IngredientDetails(self.ingredient, self.quantity, self.unit, None, None)

  def get_unit_choices(self, current_unit=None):
    default_units = ["", "tsp", "tbsp", "cups", "oz", "lb", "g", "piece", "slice"]
    if current_unit is not None and default_units.count(current_unit) == 0:
      return [current_unit] + default_units
    else:
      return default_units

  def set_ingredient(self, **args):
    self.ingredient = args["sender"].text

  def set_quantity(self, **args):
    self.quantity = args["sender"].text

  def set_unit(self, **args):
    self.unit = args["sender"].selected_value
