from ._anvil_designer import StreakLineTemplate
from m3.components import IconButton, Text, Card
from datetime import datetime, date
import anvil.server
from ..StreakLineChip import StreakLineChip

from anvil.js import window

# TODO set different UI breakpoints for num circles
# TODO diary_entries should be passed in from parent class to save a server call
# TODO button clicks should fire off an event to parent

class StreakLine(StreakLineTemplate):
  def __init__(self, is_unit_test=False, **properties):
    self.unit_test = True
    self.init_components(**properties)
    self.data = {}
    if not self.unit_test:
      self.data['streak'] = self.parent.data['streak']
    else:
      self.data["streak"] = self.get_test_streak()
    self.num_circles = 0
    self.on_resize()

  # TODO move this into a unit test
  def get_test_streak(self):
    streak = [
        {"date": datetime(2017, 12, 31), "has_entry": True, "snooze": False},
        {"date": datetime(2017, 12, 30), "has_entry": False, "snooze": True},
        {"date": datetime(2017, 12, 29), "has_entry": False, "snooze": False},
        {"date": datetime(2017, 12, 28), "has_entry": True, "snooze": False},
        {"date": datetime(2017, 12, 27), "has_entry": False, "snooze": False},
        {"date": datetime(2017, 12, 26), "has_entry": False, "snooze": False},
        {"date": datetime(2017, 12, 25), "has_entry": False, "snooze": False},
        {"date": datetime(2017, 12, 24), "has_entry": False, "snooze": False},
        {"date": datetime(2017, 12, 23), "has_entry": False, "snooze": False},
        {"date": datetime(2017, 12, 22), "has_entry": False, "snooze": False},
    ]
    streak.reverse()
    return streak

  # TODO this should fire off an event to allow user to add to entries
  def get_new_entry_chip(self):
    return StreakLineChip(icon="mi:add", enabled=True, text="Add\nEntry")

  # TODO chip should fire off an event to show that day when clicked
  def get_day_chip(self, day):
    """Returns a StreakChip for a day"""
    if day["has_entry"]:
      icon = "mi:check"
    elif day["snooze"]:
      icon = "mi:snooze"
    else:
      icon = "mi:close"

    return StreakLineChip(
      icon=icon, enabled=day["has_entry"], text=day["date"].strftime("%b %d")
    )

  # TODO this chip should fire off an event to allow user to search for more entries
  def older_entries_chip(self):
    return StreakLineChip(icon="mi:more_horiz", enabled=True, text="More")

  def redraw(self):
    self.clear()
    
    self.add_component(self.older_entries_chip())
    for day in self.data["streak"][len(self.data['streak']) - self.num_circles:]:
      self.add_component(self.get_day_chip(day))
    self.add_component(self.get_new_entry_chip())

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
