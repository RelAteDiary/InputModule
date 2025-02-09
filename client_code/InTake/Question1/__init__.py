from ._anvil_designer import Question1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Question1(Question1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def goal_radio_other_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    self.goal_other.visible = self.goal_radio_other_clicked


