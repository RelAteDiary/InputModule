from ._anvil_designer import StreakLineChipTemplate
from m3.components import IconButton, Card
from anvil import RichText


class StreakLineChip(StreakLineChipTemplate):
  def __init__(self, icon="mi:star", enabled=True, text="", **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.tag = text

    self.container.align = "center"
    self.container.orientation = ("column",)
    self.container.appearance = "outlined"
    self.container.border = "rgba(0,0,0,0.001)"

    self.button = IconButton(icon=icon, appearance="tonal", enabled=enabled, tag=text)
    self.button.set_event_handler('click', self.raise_chip_click)
    self.label = RichText(content=text, align="center")

    self.container.add_component(self.button)
    self.container.add_component(self.label)

  def raise_chip_click(self, sender, **event_args):
    self.raise_event('x-streak-line-chip-click')
