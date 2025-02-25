from ._anvil_designer import IntakeGoalTemplate
from anvil import *
import anvil.server
from ..MultipleChoiceQuestion import MultipleChoiceQuestion

class IntakeGoal(IntakeGoalTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    question = 'What do you want to accomplish with relATE?'
    options = {
      'find_hypersensitivity': 'I think I have a food intolerance or allergy, and I want help identifying it.',
      'manage_condition': 'I have a chronic health condition and I want to figure out what foods help and what makes it worse.',
      'eat_healthier': 'I want to eat healthier, and I\'m looking for guidance.'
    }
    mc = MultipleChoiceQuestion(question, options, 'goal', next_button_link='InTake.IntakeLanding')
    self.column_panel_1.add_component(mc.panel)
    

