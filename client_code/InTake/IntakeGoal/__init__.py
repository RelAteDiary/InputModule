from ._anvil_designer import IntakeGoalTemplate
from anvil import *
import anvil.server
from m3._Components import RadioGroupPanel, RadioButton, Button

class MultipleChoiceQuestion:
  def __init__(self, value_to_questions, has_other_text=True, button_text=''):
    self.panel = RadioGroupPanel()
    self.has_other_text = has_other_text
    for value in value_to_questions:
      self.panel.add_component(RadioButton(text=value_to_questions[value], value=value))
    if has_other_text:
      self.other_radio = RadioButton(text-'other', value='other')
      self.panel.add_component(self.other_radio)
      self.other_text = TextBox(visible=False)
      self.panel.add_component(self.other_text)
    if len(button_text) > 0:
      self.submit_button = Button()
      self.panel.add_component(self.submit_button)
  def submit_click(self):
    if self.submit_button is None:
      print('WARNING: there is not submit button')
    if self.other_radio is not None and self.other_text is not None:
      self.other_radio.value = self.other_text.text

class IntakeGoal(IntakeGoalTemplate):
  def __init__(self, **properties):
    self.item = {'selected': anvil.server.call('intake_get_answer','goal')}
    self.init_components(**properties)
    
    mc = MultipleChoiceQuestion({'val':'text'},button_text='next')
    self.column_panel_1.add_component(mc.panel)
    
  #   radio_group_name = 'rb_goal'
  #   self.radios = {
  #     'find_hypersensitivity': 'I think I have a food intolerance or allergy, and I want help identifying it.',
  #     'manage_condition': 'I have a chronic health condition and I want to figure out what foods help and what makes it worse.',
  #     'eat_healthier': 'I want to eat healthier, and I\'m looking for guidance.'
  #   }
  #   for value in radios:
  #     radio_button = RadioButton(text=radios[value],
  #                                group_name=radio_group_name,
  #                                value=value,
  #                                tag=value,
  #                                selected=(value==self.item['selected']))
  #     self.column_panel_1.add_component(radio_button)

  #   radio_other = RadioButton(text='Other',
  #                             group_name=radio_group_name,
  #                             value='other',
  #                             tag='radio_other',
  #                             selected=(len(self.item['selected'])>0 
  #                                       and self.item['selected'][0] == '_')
  #   text_box = TextBox(tag='text_box_other', text=self.item['selected'][1:] if (len(self.item['selected'])>0 
  #                                       and self.item['selected'][0] == '_') else '')
  #   self.column_panel_1.add_component(radio_other)
  #   self.column_panel_1.add_component(text_box)

  # def next_button_click(self, **event_args):
  #   other_text = ''
  #   other_radio = None
  #   for c in self.column_panel_1.get_components():
  #     if c.tag == 'text_box_other':
  #       other_text = c.text
  #   for c in self.column_panel_1.get_components():
  #     if c.tag == 'radio_other':
  #       other_radio = c
  #   other_radio.value = '_' + other_text

  #   anvil.server.call('intake_set_answer', 
  #                     'goal',
  #                     other_radio.get_group_value())

  #   open_form('InTake.IntakePledge')

