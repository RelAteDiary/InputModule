from ._anvil_designer import IngredientRowNewTemplate
from anvil import FlowPanel
from m3.components import IconButton


class IngredientRowNew(IngredientRowNewTemplate):
  def __init__(
    self,
    voilates_diets=[],
    amount="1",
    unit='serving',
    ingredient="food",
    **properties,
  ):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.ingredient=ingredient
    self.amount = amount
    self.unit = unit
    self.violates_diets = violates_diets

    flow_panel = FlowPanel(gap="none", align="center")
    self.add_component(flow_panel)

    warn = IconButton(align="center", icon="warning", icon_color="red")
    self.flow_panel_1.add_component(warn, width="15%")
    label_1 = Label(text="blab blab", align="center")
    self.flow_panel_1.add_component(label_1, width="27%", expand=True)
    label_2 = Label(text="plep pleb", align="center")
    self.flow_panel_1.add_component(label_2, width="27%", expand=True)
    ed = IconButton(align="center")
    self.flow_panel_1.add_component(ed, width="15%")
    de = IconButton(align="center")
    self.flow_panel_1.add_component(de, width="15%")

  def set_violates_diets(self, diets):
    if len(diets) > 0:
      pass
