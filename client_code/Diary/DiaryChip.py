import anvil.server
from anvil import *
from m3.components import Button, TextBox, CardContentContainer, Checkbox


class DiaryChip:
  def __init__(self):
    pass
  def get_streak_tracker():
    pass

  def get_chip():
    panel = Card(appearance='filled',orientation='column')
    panel.add_component(RichText(content='# Diary'))
    # panel.add_component(get_streak_tracker())
    panel.add_component()
    return panel
