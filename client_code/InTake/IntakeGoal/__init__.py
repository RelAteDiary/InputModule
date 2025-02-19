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
    
    self.goal_radio_id.group_name='rb_goal'
    self.goal_radio_id.value='find hypersensitivity'
    self.goal_radio_chronic.group_name='rb_goal'
    self.goal_radio_chronic.value='manage condition'
    self.goal_radio_healthy.group_name='rb_goal'
    self.goal_radio_healthy.value='eat healthier'
    self.goal_other.group_name='rb_goal'

  def goal_radio_other_clicked(self, **event_args):
    self.goal_other.visible = True

  def next_button_click(self, **event_args):
    self.goal_radio_other.value = '"' + self.goal_other.text + '"'
    print(f'is other selected? {self.goal_radio_other.selected}')
    print(f'what is ids value? {self.goal_radio_other.value}')
    print(f'value of group is {self.goal_radio_other.get_group_value()}')

    anvil.server.call('input_intake_answer', 
                      'goal',
                      self.goal_radio_other.get_group_value())
    open_form('InTake.IntakePledge')

