from ._anvil_designer import IntakeDietsTemplate
from anvil import *
import anvil.server
from ..CheckBoxQuestion import CheckBoxQuestion

class IntakeDiets(IntakeDietsTemplate):
  def __init__(self, **properties):
    self.question_id = 'diets'
    [diets] = anvil.server.call('intake_get_answer',[self.question_id])
    print(f'diets is {diets}')
    question = (
    'Which diet (if any) do you try to keep to right now?'
    )
    options = {
      'none': 'None, I eat freely',
      'allergen': 'I avoid one or more allergen',
      'low_fodmap': 'Low FODMAP',
      'low_histamine': 'Low histamine',
      'low_salicylate': 'Low salicylate',
      'low_oxalate': 'Low oxalate',
      'low_purine': 'Low purine / gout diet',
      'low_nickel': 'Low nickel / SNAS diet',
      'low_carb': 'Low carb',
      'low_fat': 'Low fat',
      'low_protein': 'Low protein',
      'low_fiber': 'Low fiber'
    }
    mc = CheckBoxQuestion(question, options, self.question_id, selected=diets, prev_button_link='InTake.IntakePledge',next_button_link='InTake.IntakeDisclaimer')
    self.outlined_card_1.add_component(mc.panel)
