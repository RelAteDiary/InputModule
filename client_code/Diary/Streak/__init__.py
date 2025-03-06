from ._anvil_designer import StreakTemplate
from m3.components import IconButton, Text, Card
from datetime import datetime, date
import anvil.server
# from anvil import Components

from anvil.js import window


class Streak(StreakTemplate):
  def __init__(self, **properties):
    self.unit_test = True
    self.init_components(**properties)
    self.data = {}
    if not self.unit_test:
      # self.data['diary_entries'] = self.parent.data['diary_entries']
      self.data["diary_entries"] = anvil.server.call("diary_get_entries")
    self.data["streak"] = self.to_streak()
    self.num_circles = 0
    self.on_resize()

  def to_streak(self):
    """
    self.data['diary_entries'] to [{date: Datetime, has_entry: Bool, snooze: Bool}]
    """
    if self.unit_test:
      return [
        {"date": datetime(2017, 12, 31), "has_entry": True, "snooze": False},
        {"date": datetime(2017, 12, 30), "has_entry": False, "snooze": True},
        {"date": datetime(2017, 12, 29), "has_entry": False, "snooze": False},
      ]

    streak = []
    seen_date = set()
    for diary_entry in self.data["diary_entries"]:
      if diary_entry["time"].date() not in seen_date:
        seen_date.add(diary_entry["time"].date())
        streak_entry = {}
        streak_entry["date"] = diary_entry["time"].date()
        streak_entry["has_entry"] = True
        streak_entry["snooze"] = False
        streak.append(streak_entry)
    streak.sort(key=lambda streak_entry: streak_entry["date"])
    return streak

  def latest_consecutive_streak(self, with_snooze=True):
    if self.data['streak'] is None:
      self.data['streak'] = self.to_streak()
    today = datetime.now().date()
    track = len(self.data['streak']) - 1
    consecutive_streak = 0
    while with_snooze or today==self.data['streak'][track]:
      consecutive_streak += 1
      if today!=self.data['streak'][track]:
        with_snooze = False
    # snoozing should only be active if the user has at least
    # one entry
    if consecutive_streak == 1:
      consecutive_streak = 0
    return consecutive_streak
      
  def add_new_entry_chip(self):
    if 

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
