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
from anvil import Label, DatePicker, FlowPanel, alert, open_form
from datetime import datetime
import anvil.server


class DiaryEntryForm(DiaryEntryFormTemplate):
  def __init__(self, type="note", **properties):
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
    if type == "note":
      self.add_notes_entry(entry_container)
    elif type == "symptom":
      self.add_symptom_entry(entry_container)
    # TODO food and symptom entry

    buttons_content_container = CardContentContainer()
    card.add_component(buttons_content_container)
    self.add_buttons(buttons_content_container)

  def set_consts(self):
    self.consts = {}
    self.consts["note_colors"] = {
      'default': '#000000',
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
    print(f'set time to {args["sender"].date}')

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

  def add_notes_entry(self, container):
    container.add_component(
      Label(text="What do you want to make note of?", font_size=20)
    )
    # TODO come up with better phrasing here
    container.add_component(
      Label(
        text="You can make a note of any notable event here, "
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
      text="Note color", appearance="outlined", icon="mi:circle", icon_color='#000000'
    )
    self.entry['note_color'] = '#000000'
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

  def add_symptom_entry(self, container):
    panel = Card(appearance="tonal")
    container.add_component(panel)

    # TODO finish this function

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
