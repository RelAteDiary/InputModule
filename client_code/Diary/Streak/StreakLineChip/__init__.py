from ._anvil_designer import StreakLineChipTemplate
from m3.components import IconButton, Card
from anvil import RichText

class StreakLineChip(StreakLineChipTemplate):
  def __init__(self, icon="mi:star", enabled=True, text="", **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.container.align = "center"
    self.container.orientation = ("column",)
    self.container.appearance = "outlined"
    self.container.border = "rgba(0,0,0,0.001)"
    # self.container.spacing = '0px'

    self.button = IconButton(icon=icon, appearance="tonal", enabled=enabled)
    self.label = RichText(content=text, align="center")

    self.container.add_component(self.button)
    self.container.add_component(self.label)
