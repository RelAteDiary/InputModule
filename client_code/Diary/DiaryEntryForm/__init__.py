from ._anvil_designer import DiaryEntryFormTemplate


from datetime import datetime
from anvil_extras import Slider, Autocomplete, Chip
import anvil.server
from m3.components import (
  Card,
  CardContentContainer,
  Button,
  ButtonMenu,
  MenuItem,
  TextArea,
  TextBox,
  InteractiveCard,
  Divider,
)
from anvil import (
  Label,
  DatePicker,
  DataGrid,
  ColumnPanel,
  FlowPanel,
  RichText,
  DropDown,
  FileLoader,
  Image,
  Spacer,
  alert,
  open_form,
)

from ... import Constants
from ..DishDetails import DishDetails
from ..IngredientDetails import IngredientDetails
from .DishEntryCard import DishEntryCard

# from .IngredientEditPopup import IngredientEditPopup
# from .IngredientRow import IngredientRow
from .OrDivider import OrDivider


# A form for entering diary entries.
# Here are the entries that should be populated for each type:
#   all  - time : datetime,
#          [optional] image : media
#   note - note : str,
#          note_color : str
#   food - dishes : list of DishDetails,
#          [optional] meal_freeform_text : str,
#          [opitonal] note : str,
#          [optional] note_color : str
#   symptom - symptom : str,
#          symptom_severity : float[0,5],
#          [opitonal] note : str,
#          [optional] note_color : str
# self.dish_container
# TODO self.entry['symptom'] should be a list of Symptoms
class DiaryEntryForm(DiaryEntryFormTemplate):
  def __init__(self, type="food", **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.type = type
    self.set_consts()
    self.entry = {}

    entry_content_container = CardContentContainer()
    self.add_component(entry_content_container)

    self.add_date_entry_component(entry_content_container)

    if type == "symptom":
      self.add_symptom_entry_fields(entry_content_container)
    elif type == "food":
      self.add_food_entry_fields(entry_content_container)

    self.add_notes_entry_fields(entry_content_container, is_optional=type != "note")

    self.add_buttons(entry_content_container)

  #############################################################
  # Shared components and helper functions

  def set_consts(self):
    self.app_constants = Constants.Constants()

    self.consts = {}
    self.consts["note_colors"] = {
      "default": "#000000",
      "red": "#FE2712",
      "orange": "#FB9902",
      "yellow": "#FEFE33",
      "green": "#66B032",
      "blue": "#0247FE",
      "purple": "#8601AF",
    }
    self.consts["pin_icon"] = "📍"
    self.next_page = "HomePage"

  def add_date_entry_component(self, container):
    if self.type == "food":
      datetime_message = "I ate this at"
    elif self.type == "symptom":
      datetime_message = "I felt this at"
    else:
      datetime_message = "When did this happen?"

    container.add_component(Label(text=datetime_message))
    # by default select now as the time
    now = datetime.now()
    date_component = DatePicker(pick_time=True, date=now)
    self.entry["time"] = now
    date_component.add_event_handler("change", self.update_time)
    container.add_component(date_component)

  def update_time(self, **args):
    self.entry["time"] = args["sender"].date

  def upload_image(self, container):
    container.add_component(Label(text="(OPTIONAL) Add a photo."))

    upload_image = FileLoader(
      multiple=False, file_types=".png, .jpg, .jpeg", icon="fa:camera"
    )
    container.add_component(upload_image)
    upload_image.add_event_handler("change", self.set_image)
    self.image = Image(visible=False)
    container.add_component(self.image)

  def set_image(self, **args):
    image_file = args["sender"].files[0]
    self.entry["image"] = image_file
    self.image.source = image_file
    self.image.visible = True

  def add_buttons(self, container):
    """Add the `discard` and `submit` buttons"""
    flow_panel = FlowPanel(align="center")
    container.add_component(flow_panel)

    discard_button = Button(text="Discard", appearance="outlined")
    flow_panel.add_component(discard_button)
    discard_button.add_event_handler(
      "click",
      lambda **args: open_form(self.next_page)
      if alert("Are you sure you want to discard this entry?")
      else "",
    )

    submit_button = Button(text="Submit", appearance="filled")
    flow_panel.add_component(submit_button)
    submit_button.add_event_handler("click", self.submit_entry)

  def submit_entry(self, **args):
    print(f"entry is {self.entry}")

    if self.type == "food":
      dishes = self.dishes_container.get_components()
      if len(dishes) == 0:
        alert("Please enter at least one dish")
        return
      for dish in dishes:
        if dish.to_dish_details().dish_name == "":
          dish.scroll_into_view()
          dish.highlight_dish_name_textbox()
          return
      self.entry["dishes"] = [dish.to_dish_details() for dish in dishes]
    if self.type == "symptom" and not self.entry.get("symptom"):
      alert("Please fill in the symptom")
      return
    elif self.type == "note" and not self.entry.get("note"):
      alert("Please fill in the note")
      return

    if anvil.server.call("diary_add_entry", **self.entry):
      open_form(self.next_page)
    else:
      alert("Something went wrong with submitting your entry.")

  #############################################################
  # Note entry components (also used in other entry types)

  def add_notes_entry_fields(self, container, is_optional=True):
    # TODO come up with better phrasing here
    container.add_component(
      Label(
        text=("(OPTIONAL) " if is_optional else "")
        + "You can make a note of any thing interesting here, "
        + "though it won't be analyzed automatically."
      )
    )
    self.note_component = TextArea()
    container.add_component(self.note_component)
    self.note_component.add_event_handler("lost_focus", self.set_note)

    # TODO this may be better as a flow panel instead of a dropdown
    container.add_component(
      Label(text="(OPTIONAL) Add a color to this note to stay organized.")
    )
    self.color_menu = ButtonMenu(
      text="Note color", appearance="outlined", icon="mi:circle", icon_color="#000000"
    )
    self.entry["note_color"] = "#000000"
    container.add_component(self.color_menu)

    color_menu_item = []
    for color in self.consts["note_colors"]:
      option = MenuItem(
        leading_icon="mi:circle",
        leading_icon_color=self.consts["note_colors"][color],
        text=color,
      )
      option.add_event_handler("click", self.select_note_color)
      color_menu_item.append(option)
    self.color_menu.menu_items = color_menu_item

  def set_note(self, **args):
    self.entry["note"] = args["sender"].text

  def select_note_color(self, **args):
    self.color_menu.icon_color = args["sender"].leading_icon_color
    self.entry["note_color"] = args["sender"].leading_icon_color

  #############################################################
  # Symptom entry components
  def add_symptom_entry_fields(self, container):
    syptom_card = Card(appearance="filled")
    container.add_component(syptom_card)
    syptom_content = CardContentContainer()
    syptom_card.add_component(syptom_content)

    syptom_content.add_component(Label(text="What was the symptom?"))

    recent_symptoms = anvil.server.call("diary_get_frequent_recent_symptoms")
    from_symptom_list = list(
      filter(lambda x: x not in recent_symptoms, self.app_constants.symptoms_list)
    )
    suggestions = [
      self.consts["pin_icon"] + x for x in recent_symptoms
    ] + from_symptom_list

    symptom = Autocomplete.Autocomplete(
      suggestions=suggestions,
      suggest_if_empty=True,
      filter_mode="contains",
    )
    symptom.add_event_handler("suggestion_clicked", self.set_symptom)
    symptom.add_event_handler("lost_focus", self.set_symptom)
    # TODO should also dismiss the suggestion box after enter
    symptom.add_event_handler("pressed_enter", self.set_symptom)

    syptom_content.add_component(symptom)
    syptom_content.add_component(Label(text="How severe was the symptom?"))

    default_severity = 3
    self.entry["symptom_severity"] = default_severity

    def value_to_pip(value):
      emoticons = {
        1: "_/theme/material_icons/sentiment_calm.svg",
        2: "_/theme/material_icons/sentiment_content.svg",
        3: "_/theme/material_icons/sentiment_neutral.svg",
        4: "_/theme/material_icons/sentiment_dissatisfied.svg",
        5: "_/theme/material_icons/sentiment_sad.svg",
      }
      text = {
        1: "Unnoticeable",
        2: "Mild",
        3: "Moderate",
        4: "Severe",
        5: "Incapacitating",
      }
      return f'<img src="{emoticons.get(value)}"><p>{text.get(value)}</p>'

    slider = Slider.Slider(
      start=3,
      min=1,
      max=5,
      step=0.5,
      pips=True,
      pips_density=-1,
      pips_mode="values",
      pips_stepped=True,
      pips_values=[1, 2, 3, 4, 5],
      format={"to": value_to_pip, "from": lambda v: v},
      role=["symptom-slider-spacer"],
    )
    syptom_card.add_component(slider)
    slider.add_event_handler("change", self.slider_move)
    # Pips float awkwardly, so add a spacer to make it easier to
    syptom_card.add_component(Spacer(height="40px"))

    self.upload_image(container)

  def set_symptom(self, **args):
    if (
      len(args["sender"].text) > 0 and args["sender"].text[0] == self.consts["pin_icon"]
    ):
      self.entry["symptom"] = args["sender"].text[1:]
    else:
      self.entry["symptom"] = args["sender"].text

  def slider_move(self, **args):
    self.entry["symptom_severity"] = args["sender"].value

  #############################################################
  # Food entry components

  def add_food_entry_fields(self, container):
    entry_card = Card()
    container.add_component(entry_card)
    entry_card_container = CardContentContainer()
    entry_card.add_component(entry_card_container)

    entry_card_container.add_component(RichText(content="# What did you eat? "))
    entry_card_container.add_component(Label(text="Describe your meal:"))
    food_description_text = TextArea(
      auto_expand=True,
      placeholder='E.g. "chicken soup and sourdough bread with fruit bowl"',
    )
    entry_card_container.add_component(food_description_text)
    draft_entry_button = Button(text="Draft my food diary entry for me", align="center")
    entry_card_container.add_component(draft_entry_button)
    draft_entry_button.add_event_handler(
      "click",
      lambda **args: self.get_dishes_from_description(
        food_description_text.text, self.dishes_container
      ),
    )

    entry_card_container.add_component(OrDivider())

    entry_card_container.add_component(
      Label(text="Choose dishes from your recent meals.")
    )
    # TODO populate chips from recent
    recent_meals = FlowPanel(align="left")
    entry_card_container.add_component(recent_meals)
    recent_meals.add_component(Chip.Chip(text="banana smoothie", close_icon=False))
    recent_meals.add_component(Chip.Chip(text="mango", close_icon=False))
    recent_meals.add_component(Chip.Chip(text="turkey burger", close_icon=False))

    entry_card_container.add_component(OrDivider())

    manual_add_button = Button(
      text="Add manually",
      align="center",
      appearance="outlined",
      icon="mi:add",
      icon_align="left",
    )
    entry_card_container.add_component(manual_add_button)

    self.dishes_container = CardContentContainer()
    container.add_component(self.dishes_container)

    manual_add_button.add_event_handler(
      "click",
      lambda **args: self.dishes_container.add_component(
        DishEntryCard(DishDetails()), index=0
      ),
    )

    example_dish = DishDetails("apple pie")
    example_dish.set_ingredients(
      [
        IngredientDetails("apple", "1", "", 100, ["fodmap"]),
        IngredientDetails("sugar", "100", "g", 100, []),
      ]
    )
    self.dishes_container.add_component(DishEntryCard(example_dish), index=0)

    self.upload_image(container)
    container.add_component(
      Button(text="Save and finish later", align="center", appearance="outlined")
    )

  def get_dishes_from_description(self, description, dish_entry_container):
    if 
    try:
      dishes = anvil.server.call("text_to_ingredients", description)
    # TODO this exception should be more informative.
    except (ValueError, KeyError):
      alert(
        content="Something went wrong and we can't generate your dishes for to automatically right now. Please make sure you are signed in."
      )
    if len(dishes) == 0:
      alert(
        content="We couldn't find any dishes in your description. Please try rephrasing."
      )
    for dish in dishes:
      dish_entry_card = DishEntryCard(dish)
      dish_entry_card.add_component(dish_entry_card)
