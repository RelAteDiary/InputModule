from ._anvil_designer import IntakeGoalTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users

class IntakeGoal(IntakeGoalTemplate):
  selected = None
  def __init__(self, **properties):
    self.init_components(**properties)
    anvil.server.call('start_intake_questions')

  def goal_radio_other_clicked(self, **event_args):
    self.goal_other.visible = True

  def next_button_click(self, **event_args):
    open_form('InTake.IntakePledge')
    anvil.server.call('input_intake_answer', 
                      'goal',
                      self.goal_radio_id.get_group_value())
