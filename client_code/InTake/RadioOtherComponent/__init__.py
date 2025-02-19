from ._anvil_designer import RadioOtherComponentTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RadioOtherComponent(RadioOtherComponentTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def radio_other_clicked(self, **event_args):
    self.text_field.visible=True

  def text_field_lost_focus(self, **event_args):
    self.radio_other.value = self.text_field.text
  
  def text_field_pressed_enter(self, **event_args):
    self.radio_other.value = self.text_field.text
