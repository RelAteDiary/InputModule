from ._anvil_designer import IngredientWarningPopupTemplate
from anvil import Label, FlowPanel
from m3.components import Button
import anvil.js


class IngredientWarningPopup(IngredientWarningPopupTemplate):
  def __init__(
    self, ingredient_name="food", dietary_conflicts=["test1", "test2"], **properties
  ):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.add_component(
      Label(
        text=f'The ingredient "{ingredient_name}" may conflict with the following diets you\'re keeping.'
      )
    )
    diets_panel = FlowPanel(align="center")
    self.add_component(diets_panel)
    for diet in dietary_conflicts:
      link_button = Button(
        appearance="text",
        text=diet,
      )
      diets_panel.add_component(link_button)
      link_button.add_event_handler(
        "click",
        lambda **args: anvil.js.window.open(
          f"https://www.google.com/search?q={diet}+diet", "_blank"
        ),
      )

    # Any code you write here will run before the form opens.
