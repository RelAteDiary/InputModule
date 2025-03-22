from ._anvil_designer import IngredientRowTemplate
from anvil import alert
from ..IngredientWarningPopup import IngredientWarningPopup


class IngredientRow(IngredientRowTemplate):
  def __init__(
    self,
    voilates_diets=["test_diet"],
    amount_and_unit="1 serving",
    ingredient="food",
    **properties,
  ):
    self.init_components(**properties)
    
    self.ingredient=ingredient

    if len(voilates_diets) == 0:
      self.dom_nodes["warning-column"].style.visibility = "hidden"
    else:
      self.dom_nodes["warning-button"].addEventListener(
        "click",
        lambda event: alert(
          content=IngredientWarningPopup(
            ingredient_name=ingredient, dietary_conflicts=voilates_diets
          )
        ),
      )
    self.dom_nodes["quantity-column"].innerText = amount_and_unit
    self.dom_nodes["food-column"].innerText = ingredient
    self.dom_nodes["edit-column"].addEventListener(
      "click", lambda event: self.raise_event("x-edit-click")
    )
    self.dom_nodes["delete-column"].addEventListener(
      "click", lambda event: self.raise_event("x-delete-click")
    )

