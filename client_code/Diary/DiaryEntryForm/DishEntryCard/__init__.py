from ._anvil_designer import DishEntryCardTemplate
from m3.components import Button, CardContentContainer, Card
from anvil import Label, TextArea, alert, FlowPanel
from anvil_extras.animation import pulse, Effect

from ..IngredientRow import IngredientRow
from ..IngredientEditPopup import IngredientEditPopup
from ...DishDetails import DishDetails
from ...IngredientDetails import IngredientDetails


class DishEntryCard(DishEntryCardTemplate):
  def __init__(self, dish_details, **properties):
    self.init_components(**properties)
    self.add_dish_card(dish_details)

  def __repr__(self):
    return f"DishEntryCard <{self.to_dish_details().dish_name}>"

  def add_dish_card(self, dish_details):
    dish_card = Card()
    self.add_component(dish_card, width="100%", index=0)
    dish_card_container = CardContentContainer()
    dish_card.add_component(dish_card_container)

    dish_card_container.add_component(Label(text="I ate this dish:"))
    self.dish_name_textbox = TextArea(
      text=dish_details.dish_name, placeholder="E.g. Chicken soup"
    )
    dish_card_container.add_component(self.dish_name_textbox)
    self.fill_in_dish_name_prompt = Label(
      text="Please give this dish a name", visible=False, foreground="red"
    )
    dish_card_container.add_component(self.fill_in_dish_name_prompt)

    def make_prompt_invisible():
      self.fill_in_dish_name_prompt.visible = False

    self.dish_name_textbox.add_event_handler(
      "lost_focus", lambda **args: make_prompt_invisible()
    )

    self.ingredients_container = CardContentContainer(margin="0px")
    dish_card_container.add_component(self.ingredients_container)
    for ingredient in dish_details.ingredients:
      self.add_ingredient_row(ingredient, self.ingredients_container)

    add_ingredient_button = Button(
      align="center",
      text="Add ingredient",
      appearance="text",
      icon="mi:add",
      icon_align="left",
    )
    dish_card_container.add_component(add_ingredient_button)
    add_ingredient_button.add_event_handler(
      "click",
      lambda **args: self.add_ingredient_button_click(self.ingredients_container),
    )

    buttons_panel = FlowPanel(align='center')
    dish_card_container.add_component(buttons_panel)
    
    delete_card_button = Button(
      text="Delete this dish",
      appearance="outlined",
      icon="mi:delete",
      icon_align="left",
    )
    buttons_panel.add_component(delete_card_button)
    delete_card_button.add_event_handler(
      "click", lambda **args: dish_card.remove_from_parent()
    )

    add_to_collection_button = Button(
      text="Save to my collection",
      appearance='tonal',
      icon="mi:bookmark",
      icon_align="left",)
    buttons_panel.add_component(add_to_collection_button)
    # TODO impl this button
    add_to_collection_button.add_event_handler(
      "click", lambda **args: print('add to collection')
    )

  def add_ingredient_button_click(self, container):
    ingredient = alert(content=IngredientEditPopup(), buttons=[])
    self.add_ingredient_row(ingredient, container)

  def add_ingredient_row(self, ingredient, container):
    ingredient_row = IngredientRow(ingredient)
    # TODO async call to see if ingredient is okay
    container.add_component(ingredient_row)

  def to_dish_details(self):
    dish_details = DishDetails(dish_name=self.dish_name_textbox.text)
    dish_details.set_ingredients(
      [
        row.to_ingredient_details()
        for row in self.ingredients_container.get_components()
      ]
    )

    return dish_details

  def highlight_dish_name_textbox(self):
    Effect(pulse, duration=500).animate(self.dish_name_textbox)
    self.fill_in_dish_name_prompt.visible = True
