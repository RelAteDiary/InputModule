from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ..Diary import DishDetails


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)


    # Any code you write here will run before the form opens.

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.login_with_form()

  def outlined_button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    response = anvil.server.call('text_to_ingredients', 'chicken soup and sourdough bread with fruit bowl')
    
    print(response)
