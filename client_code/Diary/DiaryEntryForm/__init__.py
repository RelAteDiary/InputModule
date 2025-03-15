from ._anvil_designer import DiaryEntryFormTemplate
from m3.components import (
  Card,
  CardContentContainer,
  Button,
  ButtonMenu,
  MenuItem,
  TextArea,
  InteractiveCard,
)
from anvil import (
  Label,
  DatePicker,
  DataGrid,
  ColumnPanel,
  FlowPanel,
  DropDown,
  Image,
  Spacer,
  alert,
  open_form,
)
from ... import Constants
from .SymptomPips import SymptomPips
from datetime import datetime
from anvil_extras import Slider, Autocomplete, Chip
import anvil.server


class DiaryEntryForm(DiaryEntryFormTemplate):
  def __init__(self, type="symptom", **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.set_consts()

    self.type = type
    self.entry = {}
    self.next_page = "HomePage"

    card = Card(appearance="outlined")
    self.add_component(card)

    date_entry_content_container = CardContentContainer()
    card.add_component(date_entry_content_container)
    self.add_date_entry_component(date_entry_content_container)

    entry_container = CardContentContainer()
    card.add_component(entry_container)

    syptom_or_diary_card = Card(appearance="filled")
    syptom_or_diary_card_content = CardContentContainer()
    syptom_or_diary_card.add_component(syptom_or_diary_card_content)
    if type == "symptom":
      self.add_symptom_entry(syptom_or_diary_card_content)
      entry_container.add_component(syptom_or_diary_card)
    elif type == 'food':
      entry_container.add_component(syptom_or_diary_card)

    self.add_notes_entry(entry_container, is_optional=type != "note")

    buttons_content_container = CardContentContainer()
    card.add_component(buttons_content_container)
    self.add_buttons(buttons_content_container)

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

  def add_buttons(self, container):
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

  def add_notes_entry(self, container, is_optional=True):
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
    self.entry["note"] = ""

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

  def select_note_color(self, **args):
    self.color_menu.icon_color = args["sender"].leading_icon_color
    self.entry["note_color"] = args["sender"].leading_icon_color

  # note should work
  def add_symptom_entry(self, container):
    container.add_component(Label(text="What was the symptom?"))
    symptom = Autocomplete.Autocomplete(
        suggestions=self.app_constants.symptoms_list,
        suggest_if_empty=True,
        filter_mode="contains",
      )
    # TODO handle these events properly
    symptom.add_event_handler('suggestion_clicked', lambda **args : print('clicked'))
    symptom.add_event_handler('pressed_enter', lambda **args : print('pressed_enter'))

    container.add_component(symptom)
    container.add_component(Label(text="How severe was the symptom?"))

    default_severity = 3
    self.entry['symptom_severity'] = default_severity

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
    container.add_component(slider)
    slider.add_event_handler("change", self.slider_move)
    # Pips float awkwardly, so add a spacer to make it easier to
    container.add_component(Spacer(height="40px"))

  def slider_move(self, **args):
    self.entry['symptom_severity'] = args["sender"].value

  def submit_entry(self, **args):
    # TODO data validation
    if self.type == "note":
      self.entry["note"] = self.note_component.text
    print(f"entry is {self.entry}")
    if anvil.server.call("diary_add_entry", **self.entry):
      open_form(self.next_page)
    else:
      alert("Something went wrong with submitting your entry, please try again later.")

    # Any code you write here will run before the form opens.
