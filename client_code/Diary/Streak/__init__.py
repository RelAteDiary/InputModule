from ._anvil_designer import StreakTemplate
from m3.components import IconButton, Text
from anvil import FlowPanel

from anvil.js import window


class Streak(StreakTemplate):
  def __init__(self, **properties):
    self.num_circles = 0
    self.init_components(**properties)
    self.on_resize()

  def redraw(self):
    self.clear()
    for i in range(self.num_circles):
      day = FlowPanel()
      day.add_component(IconButton(text=i, icon='mi:check', appearance='tonal'))
      day.add_component(Text(text='Feb 2'))
      self.add_component(day)
      # self.add_component(IconButton(text=i, icon='mi:close', appearance='tonal', enabled=False))
      # self.add_component(IconButton(text=i, icon='mi:snooze', appearance='tonal', enabled=False))

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
