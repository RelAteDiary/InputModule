import anvil.server
from anvil import *
from m3.components import Button, TextBox, CardContentContainer, Checkbox


class DiaryChip:
  def __init__(self):
    pass
  def get_streak_tracker():
    streak = anvil.server.call('diary_get_diary_streak')
    if streak is None:
      return None
    if 'recent' in streak:
      
    

  def get_chip():
    panel = Card(appearance='filled',orientation='column')
    panel.add_component(RichText(content='# Diary'))
    panel.add_component(get_streak_tracker())
    return panel
