from ._anvil_designer import DiaryTemplate
import anvil.server
from datetime import datetime
from ..Streak import Streak
from .EntryTypePopup import EntryTypePopup
from anvil import alert


class Diary(DiaryTemplate):
  def __init__(self, is_unit_test=True, **properties):
    self.init_components(**properties)
    self.data = {}
    self.is_unit_test = is_unit_test
    self.data["diary_entries"] = self.get_entries()
    self.streak = Streak(is_unit_test=False)
    self.streak.add_event_handler(
      "x-new-entry",
      lambda **args: alert(
        content=EntryTypePopup(), large=True, buttons=[], title="What are you entering?"
      ),
    )
    self.add_component(self.streak)

  def get_entries(self):
    if self.is_unit_test:
      return [
        {"time": datetime(2022, 12, 28, 23, 55, 59)},
        {"time": datetime(2022, 12, 27, 23, 55, 59)},
        {"time": datetime(2022, 12, 26, 23, 55, 59)},
        {"time": datetime(2022, 12, 25, 23, 55, 59)},
      ]
    return anvil.server.call("diary_get_entries")
