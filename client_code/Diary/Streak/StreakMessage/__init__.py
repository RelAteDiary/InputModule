from ._anvil_designer import StreakMessageTemplate
from datetime import datetime

class StreakMessage(StreakMessageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if not self.unit_test:
      self.data['streak'] = self.parent.data['streak']
    else:
      self.data["streak"] = self.get_test_streak()
    consecutive_streak = self.latest_consecutive_streak()
    if consecutive_streak == 0:
      callout = None
      message = 'Life’s hectic, but don’t forget to take care of yourself. Let’s get logging in your diary - it\'s important!'
    elif consecutive_streak == 1:
      callout = 'Keep it up!'
    elif consecutive_streak < 5:
      callout = f'Way to go on your {consecutive_streak} day streak!'
      message = 'Great job sticking with it. You\'re really taking charge of your health!'
    elif consecutive_streak < 10:
            callout = f'Way to go on your {consecutive_streak} streak!'
    self.add_component()
  
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
