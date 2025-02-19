from ._anvil_designer import IntakeLandingTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil.js.window import jQuery

class IntakeLanding(IntakeLandingTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.symptom_rich_text.content = 'bloated'

    # Any code you write here will run before the form opens.

  def clear_inputs(self):
    # Clear our three text boxes
    self.name_box.text = ""
    self.email_box.text = ""
    self.feedback_box.text = ""
    
  def submit_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    name = self.name_box.text
    email = self.email_box.text
    feedback = self.feedback_box.text

    anvil.server.call('send_feedback',name,email,feedback)

    Notification("Feedback submitted!").show()
    self.clear_inputs()

  def outlined_button_1_click(self, **event_args):
    open_form('InTake.IntakeGoal')
