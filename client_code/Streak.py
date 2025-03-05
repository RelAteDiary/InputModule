import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import date
from functools import reduce


class Streak(app_tables.users.Row):
  def has_update(days_prior):
    return False
  @property
  def has_snooze(self):
    # number of days before snooze refreshes
    snooze_refresh_frequency = 7
    has_update = [self.has_update(i) for i in range(snooze_refresh_frequency)]
    return reduce(lambda x, y : x and y, has_update)
    
