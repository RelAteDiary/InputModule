from ._anvil_designer import IngredientRowNewTemplate
from anvil import FlowPanel, Label
from m3.components import IconButton


class IngredientRowNew(IngredientRowNewTemplate):
  def __init__(
    self,
    voilates_diets=[],
    amount="1",
    unit='serving',
    ingredient_name="food",
    **properties,
  ):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.ingredient_name=ingredient_name
    self.amount = amount
    self.unit = unit
    self.violates_diets = voilates_diets

    flow_panel = FlowPanel(gap="none", align="center")
    self.add_component(flow_panel)

    warn = IconButton(align="center", icon="warning", icon_color="red")
    flow_panel.add_component(warn, width="15%")
    amount_and_unit = Label(text=str(self.amount) + ' ' + self.unit, align="center")
    flow_panel.add_component(amount_and_unit, width="27%", expand=True)
    label_2 = Label(text=self.ingredient_name, align="center")
    flow_panel.add_component(label_2, width="27%", expand=True)
    edit = IconButton(icon='edit', align="center")
    flow_panel.add_component(edit, width="15%")
    delete = IconButton(icon='delete', align="center")
    flow_panel.add_component(delete, width="15%")

  def set_violates_diets(self, diets):
    if len(diets) > 0:
      pass
