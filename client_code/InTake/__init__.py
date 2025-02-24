import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from m3.components import RadioGroupPanel, RadioButton, Button, TextBox

class MultipleChoiceQuestion:
  def __init__(self, value_to_questions, 
               has_other_text=True, 
               prev_button_link='',
               next_button_link=''):
    self.panel = RadioGroupPanel()
    self.has_other_text = has_other_text
    for value in value_to_questions:
      self.panel.add_component(RadioButton(text=value_to_questions[value], value=value))
    if has_other_text:
      self.other_radio = RadioButton(text='other', value='other')
      self.other_radio.add_event_handler('select', self.show_other_textbox)
      self.panel.add_component(self.other_radio)
      self.other_text = TextBox(visible=False)
      self.panel.add_component(self.other_text)
      
    if len(button_text_to_links) > 0:
      for button_text in button_text_to_links:
        self.t
      self.submit_button = Button()
      self.panel.add_component(self.submit_button)

  def show_other_textbox(self, **event_args):
    if self.other_text is None:
      print('ERROR: there is no other textbox!!!')
    self.other_text.visible = True
  
  def button_click(self, **event_args):
    if self.submit_button is None:
      print('ERROR: there is not submit button!!!')
    if self.other_radio is not None and self.other_text is not None:
      self.other_radio.value = self.other_text.text
    print(self.radio_group_panel_1.selected_value)
    

def say_hello():
  print("Hello, world")
