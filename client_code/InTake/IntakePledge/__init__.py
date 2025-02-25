from ._anvil_designer import IntakePledgeTemplate
from anvil import *
import anvil.server
from ..CheckBoxQuestion import CheckBoxQuestion


class IntakePledge(IntakePledgeTemplate):
  def __init__(self, **properties):
    goal = 'foo'
    question = f'''
    Pledge to work towards your goal: {goal}
    The more accurately you log in the food and symptoms diary, 
    the more information we can use to figure out what foods are 
    making you feel bad. Are you willing to make **a commitment 
    to yourself to work on feeling better**?
    '''
    options = {
      'persevere': 'I pledge to keep trying and not give up on my health.',
      'log_daily': 'I pledge to log my meals and symptoms every day this week, or at least try my best to',
    }
    mc = CheckBoxQuestion(question, options, 'goal', next_button_link='InTake.IntakeLanding')
    self.column_panel_1.add_component(mc.panel)