from ._anvil_designer import IngredientRowTemplate
from anvil import FlowPanel, Label, alert
from m3.components import IconButton, CardContentContainer

from ..IngredientWarningPopup import IngredientWarningPopup
from ..IngredientEditPopup import IngredientEditPopup
from ...IngredientDetails import IngredientDetails


class IngredientRow(IngredientRowTemplate):
  def __init__(
    self,
    ingredient,
    **properties,
  ):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.set_fields_from_ingredient(ingredient)

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
    self.check_violates_diets()

    self.amount_and_unit_column = Label(
      text=str(self.amount) + " " + self.unit, align="center"
    )
    flow_panel.add_component(self.amount_and_unit_column, width="27%", expand=True)
    self.ingredient_name_column = Label(text=self.ingredient_name, align="center")
    flow_panel.add_component(self.ingredient_name_column, width="27%", expand=True)

    edit = IconButton(icon="mi:edit", align="center")
    flow_panel.add_component(edit, width="15%")
    edit.add_event_handler(
      "click",
      lambda **args: self.update_row(
        alert(
          content=IngredientEditPopup(
            ingredient=self.ingredient_name,
            quantity=self.amount,
            unit=self.unit,
          ),
          buttons=[],
        )
      ),
    )

    delete = IconButton(icon="mi:delete", align="center")
    flow_panel.add_component(delete, width="15%")
    delete.add_event_handler("click", lambda **args: self.remove_from_parent())

  def set_fields_from_ingredient(self, ingredient, update_violates_diets=True):
    if ingredient is None:
      return
    """Initialize some object fields from an Ingredient object"""
    self.ingredient_name = ingredient.ingredient_name
    self.amount = ingredient.amount
    self.unit = ingredient.unit
    self.amount_in_grams = ingredient.amount_in_grams
    if update_violates_diets:
      self.violates_diets = ingredient.violates_diets

  def check_violates_diets(self):
    if self.violates_diets is not None and len(self.violates_diets) > 0:
      self.warn = IconButton(
        align="center",
        icon="mi:warning",
        icon_color="red",
        visible=len(self.violates_diets) > 0,
      )
      self.warn.add_event_handler(
        "click",
        lambda **args: alert(
          content=IngredientWarningPopup(
            ingredient_name=self.ingredient_name, dietary_conflicts=self.violates_diets
          )
        ),
      )
      self.maybe_warn.add_component(self.warn)

  def update_row(self, ingredient, update_violates_diets=False):
    if ingredient is None:
      return
    self.set_fields_from_ingredient(
      ingredient, update_violates_diets=update_violates_diets
    )

    self.amount_and_unit_column.text = str(self.amount) + " " + self.unit
    self.ingredient_name_column.text = self.ingredient_name

  def to_ingredient_details(self):
    IngredientDetails(
      self.ingredient_name,
      self.amount,
      self.unit,
      self.amount_in_grams,
      self.violates_diets,
    )
