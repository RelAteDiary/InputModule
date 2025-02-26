from ._anvil_designer import IntakeGoalTemplate
from anvil import *
import anvil.server
from ..MultipleChoiceQuestion import MultipleChoiceQuestion

class IntakeGoal(IntakeGoalTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    [goal] = anvil.server.call('intake_get_answer',['goal'])
    question = 'What do you want to accomplish with relATE?'
    options = {
      'find_hypersensitivity': 'I think I have a food intolerance or allergy, and I want help identifying it.',
      'manage_chronic_condition': 'I have a chronic condition and I want to figure out what foods help and what makes it worse.',
      'eat_healthier': 'I want to eat healthier, and I\'m looking for guidance.'
    }
    mc = MultipleChoiceQuestion(question, options, 'goal', selected=goal, next_button_link='InTake.IntakePledge')
    self.column_panel_1.add_component(mc.panel)
    

