from ._anvil_designer import IntakeGoalTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class IntakeGoal(IntakeGoalTemplate):
  selected = None
  def __init__(self, **properties):
    self.init_components(**properties)
    anvil.server.call('start_intake_questions')

  def goal_radio_other_clicked(self, **event_args):
    self.goal_other.visible = True

  def next_button_click(self, **event_args):
    print(self.goal_radio_id.get_group_value())
    open_form('InTake.IntakePledge')
