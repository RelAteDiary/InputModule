from ._anvil_designer import StreakLineTemplate
from m3.components import IconButton, Text, Card
from datetime import datetime, date
import anvil.server
from ..StreakLineChip import StreakLineChip

from anvil.js import window

# TODO display a current streak count
# TODO set different UI breakpoints for num circles
# TODO diary_entries should be passed in from parent class to save a server call
# TODO button clicks should fire off an event to parent

class StreakLine(StreakLineTemplate):
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
    if self.data["streak"] is None:
      self.data["streak"] = self.to_streak()
    today = datetime.now().date()
    track = len(self.data["streak"]) - 1
    consecutive_streak = 0
    while with_snooze or today == self.data["streak"][track]:
      consecutive_streak += 1
      if today != self.data["streak"][track]:
        with_snooze = False
    # snoozing should only be active if the user has at least
    # one entry
    if consecutive_streak == 1:
      consecutive_streak = 0
    return consecutive_streak

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
