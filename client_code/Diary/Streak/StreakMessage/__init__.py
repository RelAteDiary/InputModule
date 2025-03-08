from ._anvil_designer import StreakMessageTemplate
from datetime import datetime
from anvil import RichText

class StreakMessage(StreakMessageTemplate):
  def __init__(self, is_unit_test=True, **properties):
    self.init_components(**properties)
    self.data = {}
    self.is_unit_test = is_unit_test
    if not is_unit_test:
      self.data['streak'] = self.parent.data['streak']
    else:
      self.data["streak"] = self.get_test_streak()
    consecutive_streak = self.latest_consecutive_streak()
    consecutive_streak = 1
    # TODO there should be more options for messages. 
    if consecutive_streak == 0:
      callout = None
      message = 'Life’s hectic, but don’t forget to take care of yourself. Let’s get logging in your diary - it\'s important!'
    elif consecutive_streak == 1:
      callout = 'Keep it up! The first steps are always the hardest.'
    elif consecutive_streak < 5:
      callout = f'Way to go on your {consecutive_streak} days streak!'
      message = 'Great job sticking with it. You\'re really taking charge of your health!'
    elif consecutive_streak < 10:
      callout = f'Nicely done on your {consecutive_streak} days streak!'
      message = 'Amazing job staying on top of your diary. Identifying patterns in your diary is the most valuable tool for understanding things clearly.'
    else:
      callout = f'Bravo! A {consecutive_streak} days streak!'
      message = 'You\'re getting closer to figuring things out with every entry!'
    if callout is not None:
      self.add_component(RichText(content='# ' + callout))
    self.add_component(RichText(content=message))
  
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
