from ._anvil_designer import IngredientRowTemplate
from anvil import FlowPanel, Label, alert
from m3.components import IconButton, CardContentContainer

from ..IngredientWarningPopup import IngredientWarningPopup
from ..IngredientEditPopup import IngredientEditPopup


class IngredientRow(IngredientRowTemplate):
  def __init__(
    self,
    violates_diets=[],
    amount="1",
    unit="serving",
    ingredient_name="food",
    **properties,
  ):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.ingredient_name = ingredient_name
    self.amount = amount
    self.unit = unit
    self.violates_diets = violates_diets

    self.amount_and_unit_column = None
    self.ingredient_name_column = None

    # The warning button that shows if this ingredient conflicts with a diet
    self.warn = None

    flow_panel = FlowPanel(
      gap="none", align="center", spacing_above="none", spacing_below="none"
    )
    self.add_component(flow_panel)

    self.maybe_warn = CardContentContainer(margin="0px")
    flow_panel.add_component(self.maybe_warn, width="15%")
    self.set_violates_diets(self.violates_diets)

    amount_and_unit_column = Label(
      text=str(self.amount) + " " + self.unit, align="center"
    )
    flow_panel.add_component(amount_and_unit_column, width="27%", expand=True)
    ingredient_name_column = Label(text=self.ingredient_name, align="center")
    flow_panel.add_component(ingredient_name_column, width="27%", expand=True)

    edit = IconButton(icon="mi-edit", align="center")
    flow_panel.add_component(edit, width="15%")

    edit_popup = IngredientEditPopup(
      ingredient=self.ingredient_name,
      quantity=amount,
      unit=unit,
    )
    edit.add_event_handler(
      "click",
      lambda **args: print(alert(content=edit_popup, buttons=[])),
    )
    delete = IconButton(icon="mi-delete", align="center")
    flow_panel.add_component(delete, width="15%")

  def set_violates_diets(self, violates_diets):
    self.violates_diets = violates_diets
    if len(violates_diets) > 0:
      self.warn = IconButton(
        align="center",
        icon="mi-warning",
        icon_color="red",
        visible=len(self.violates_diets) > 0,
      )
      self.warn.add_event_handler(
        "click",
        lambda **args: alert(
          content=IngredientWarningPopup(
            ingredient_name=self.ingredient_name, dietary_conflicts=violates_diets
          )
        ),
      )
      self.maybe_warn.add_component(self.warn)

  def update_row(self, ingredient, update_violates_diets=False):
    self.ingredient_name = ingredient.ingredient_name
    self.amount=ingredient.amount
    self.unit=ingredient.unit
    if update_violates_diets:
      self.violates_diets=ingredient.violates_diets
