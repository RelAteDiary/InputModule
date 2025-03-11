from ._anvil_designer import EntryTypePopupTemplate
from anvil import FlowPanel
from m3.components import InteractiveCard, CardContentContainer, Button

class EntryTypePopup(EntryTypePopupTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    flow_panel = FlowPanel(align="center", spacing="small")
    flow_panel.add_component(Button(icon='mi:nutrition',text='Food Entry'))
    flow_panel.add_component(Button(icon='mi:sentiment_stressed',text='Symptoms Entry'))
    flow_panel.add_component(Button(icon='mi:sticky_note_2',text='Event or Note'))
    self.add_component(flow_panel)