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
  def __init__(self, **properties):
    self.init_components(**properties)
    anvil.server.call('start_intake_questions')

  def goal_radio_other_clicked(self, **event_args):
    self.goal_other.visible = True

  def diet_allergen_change(self, **event_args):
    self.diet_allergen_text_box.visible = True

  def diet_other_change(self, **event_args):
    self.diet_other_text_box.visible = True

  def create_account_button_click(self, **event_args):
    anvil.server.call('submit_intake_question')
    user =  anvil.users.login_with_form()
    open_form('Homepage')



