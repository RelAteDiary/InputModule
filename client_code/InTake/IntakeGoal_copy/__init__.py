from ._anvil_designer import IntakeGoal_copyTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class IntakeGoal_copy(IntakeGoal_copyTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    anvil.server.call("start_intake_questions")

  def goal_radio_other_clicked(self, **event_args):
    self.goal_other.visible = True
