import anvil.server
from anvil import *
from m3.components import RadioGroupPanel, RadioButton, Button, TextBox

class MultipleChoiceQuestion:
  def __init__(self, question, value_to_questions,
               question_id,
               selected=None,
               has_other_textbox=True, 
               prev_button_link=None,
               next_button_link=None):
    self.question_id = question_id
    self.has_other_textbox = has_other_textbox
    
    self.panel = RadioGroupPanel()
    
    self.panel.add_component(RichText(content=question))
    
    for value in value_to_questions:
      self.panel.add_component(
        RadioButton(
          text=value_to_questions[value], value=value,
          selected=(selected is not None and selected==value))
      )

    if has_other_textbox:
      self.other_radio = RadioButton(
        text='other', value='other', selected = selected is not None and selected.startswith('other-'))
      self.other_radio.add_event_handler(
        'select', self._show_other_textbox)
      self.panel.add_component(self.other_radio)
      self.other_text = TextBox(visible=selected is not None and selected.startswith('other-'),
                               text=selected[len('other-'):] if selected is not None and selected.startswith('other-') else '')
      self.panel.add_component(self.other_text)

    flow_panel = FlowPanel(align='center')

    if prev_button_link is not None:
      self.prev_button = Button(
        appearance='outlined',
        text='previous')
      self.prev_button.add_event_handler(
        'click',self._update_question_answer)
      self.prev_button.add_event_handler(
        'click', lambda **event_args : open_form(prev_button_link))
      flow_panel.add_component(self.prev_button)
      
    if next_button_link is not None:
      self.next_button = Button(
        appearance='filled',
        text='next')
      self.next_button.add_event_handler(
        'click',self._update_question_answer)
      self.next_button.add_event_handler(
        'click', lambda **event_args : open_form(next_button_link))
      flow_panel.add_component(self.next_button)

    self.panel.add_component(flow_panel)

  def _show_other_textbox(self, **event_args):
    if self.other_text is None:
      print('ERROR: there is no other textbox!!!')
    self.other_text.visible = True
  
  def _update_question_answer(self, **event_args):
    if self.has_other_textbox and self.other_radio.selected:
      self.other_radio.value = 'other-' + self.other_text.text
    print(f'panel value is {self.panel.selected_value}')
    anvil.server.call('intake_set_answer', 
                      self.question_id, 
                      self.panel.selected_value)
