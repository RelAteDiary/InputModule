from ._anvil_designer import IntakePledgeTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class IntakePledge(IntakePledgeTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.rich_text_goal.content = anvil.server.call('intake_get_answer')

  def goal_radio_other_clicked(self, **event_args):
    self.goal_other.visible = True

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('InTake.IntakeGoal')
