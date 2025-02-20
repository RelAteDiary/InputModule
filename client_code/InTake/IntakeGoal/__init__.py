from ._anvil_designer import IntakeGoalTemplate
from anvil import *
import anvil.server

class IntakeGoal(IntakeGoalTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    radio_group_name = 'rb_goal'
    radio1 = RadioButton(text='I think I have a food intolerance or allergy, and I want help identifying it.',
                        group_name=radio_group_name,
                        value='find hypersensitivity')
    radio2 = RadioButton(text='I have a chronic health condition and I want to figure out what foods help and what makes it worse.',
                        group_name=radio_group_name,
                        value='manage condition')
    radio3 = RadioButton(text='I want to eat healthier, and I\'m looking for guidance.',
                        group_name=radio_group_name,
                        value='eat healthier')
    radio4 = RadioButton(text='Other',
                        group_name=radio_group_name,
                        value='other',
                        tag='radio_other')
    
    text_area = TextBox(visible=False, tag='text_box_other')
    radio4.add_event_handler('clicked', self.radio_other_clicked)

    rb_goals = [radio1, radio2, radio3, radio4, text_area]
    for rb in rb_goals:
      self.column_panel_1.add_component(rb)

    answer = anvil.server.call('intake_get_answer','goal')
    if answer != '':
      

  def radio_other_clicked(self, **event_args):
    for c in self.column_panel_1.get_components():
      if c.tag == 'text_box_other':
        c.visible=True

  def next_button_click(self, **event_args):
    other_text = ''
    other_radio = None
    for c in self.column_panel_1.get_components():
      if c.tag == 'text_box_other':
        other_text = c.text
    for c in self.column_panel_1.get_components():
      if c.tag == 'radio_other':
        other_radio = c
    other_radio.value = '"' + other_text + '"'

    anvil.server.call('intake_set_answer', 
                      'goal',
                      other_radio.get_group_value())

    open_form('InTake.IntakePledge')

