from ._anvil_designer import StreakTemplate
from m3.components import IconButton, Text, Card
from datetime import datetime, date
import anvil.server
# from anvil import Components

from anvil.js import window


class Streak(StreakTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.data = {}
    # self.data['diary_entries'] = self.parent.data['diary_entries']
    # self.data['diary_entries'] = anvil.server.call('diary_get_entries')
    self.data["streak"] = self.to_streak()
    self.num_circles = 0
    self.on_resize()

  def to_streak(self):
    """
    self.data['diary_entries'] to [{date: Datetime, has_entry: Bool, snooze: Bool}]
    """
    return [
      {"date": datetime(2017, 12, 31), "has_entry": True, "snooze": False},
      {"date": datetime(2017, 12, 30), "has_entry": False, "snooze": True},
      {"date": datetime(2017, 12, 29), "has_entry": False, "snooze": False},
    ]

  def days_streak(self):
    pass

  def add_new_entry_chip(self):
    pass
  
  def older_entries_chip(self):
    pass

  def redraw(self):
    self.clear()
    for day in self.data["streak"][: self.num_circles]:
      chip = Card(
        align="center",
        orientation="column",
        appearance="outlined",
        border="rgba(0,0,0,0.001)",
      )

      if day["has_entry"]:
        icon = "mi:check"
      elif day["snooze"]:
        icon = "mi:snooze"
      else:
        icon = "mi:close"

      chip.add_component(
        IconButton(icon=icon, appearance="tonal", enabled=day["has_entry"])
      )
      chip.add_component(Text(text=day["date"].strftime("%b %d"), align="center"))
      self.add_component(chip)

  def on_resize(self, *e):
    width = window.innerWidth
    if width < 768:
      num_circles = 5
    else:
      num_circles = 10

    if self.num_circles != num_circles:
      self.num_circles = num_circles
      self.redraw()

  def form_show(self, **event_args):
    window.addEventListener("resize", self.on_resize)

  def form_hide(self, **event_args):
    window.removeEventListener("resize", self.on_resize)
