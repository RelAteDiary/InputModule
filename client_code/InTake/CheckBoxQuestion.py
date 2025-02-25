import anvil.server
from anvil import *
import anvil
from m3.components import Button, TextBox, CardContentContainer, Checkbox

class CheckBoxQuestion:
  def __init__(self, question, value_to_questions,
               question_id,
               callout=None, 
               has_other_textbox=True, 
               prev_button_link=None,
               next_button_link=None):
    self.question_id = question_id
    self.has_other_textbox = has_other_textbox
    self.selected = []
    
    self.panel = CardContentContainer(
      background_color='transparent', border='0px')
    if callout is not None:
      callout = anvil.RichText(content='# ' + callout, format='markdown')
      self.panel.add_component(callout)
    question = anvil.RichText(content=question, format='markdown')
    self.panel.add_component(question)
    
    for value in value_to_questions:
      checkbox = Checkbox(
        text=value_to_questions[value])
      checkbox.add_event_handler(
        'change', 
        self._change_selected(checkbox, value))
      self.panel.add_component(checkbox)

    if has_other_textbox:
      self.other_checkbox = Checkbox(text='Other')
      self.other_checkbox.add_event_handler(
        'change', self._show_other_textbox)
      self.panel.add_component(self.other_checkbox)
      self.other_text = TextBox(visible=False)
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
  
  def _change_selected(self, checkbox, value):
    def f(**event_args):
      if checkbox.checked:
        self.selected.append(value)
      else :
        self.selected.remove(value)
    return f

  def _show_other_textbox(self, **event_args):
    if self.other_text is None:
      print('ERROR: there is no other textbox!!!')
    self.other_text.visible = True
  
  def _update_question_answer(self, **event_args):
    if self.has_other_textbox and self.other_checkbox.checked:
      self.selected.append('other-' + self.other_text.text)
    print(f'panel value is {self.selected}')
    anvil.server.call('intake_set_answer', 
                      self.question_id, 
                      self.selected)
