from ._anvil_designer import StreakTemplate
import anvil.server
from datetime import datetime
from .StreakLine import StreakLine
from .StreakMessage import StreakMessage


class Streak(StreakTemplate):
  def __init__(self, is_unit_test=True, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.is_unit_test = is_unit_test
    self.data={}

    if not is_unit_test:
      self.data["diary_entries"] = anvil.server.call("diary_get_entries")
    self.data["streak"] = self.to_streak()

    self.card_content_container_1.add_component(StreakMessage())
    self.card_content_container_1.add_component(StreakLine())

   
  def to_streak(self):
    """
    self.data['diary_entries'] to [{date: Datetime, has_entry: Bool, snooze: Bool}]
    """
    if self.is_unit_test:
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
