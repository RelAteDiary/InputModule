from ._anvil_designer import IntakeDisclaimerTemplate
from anvil import *
import anvil.server
import anvil.users
from ..MultipleChoiceQuestion import MultipleChoiceQuestion


class IntakeDisclaimer(IntakeDisclaimerTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.question_id = "acknowledge_disclaimer"
        [prev_answer] = anvil.server.call("intake_get_answer", [self.question_id])
        question = (
            "Do you understand that relATE is not a substitute for medical advice? "
            + "This means:\n"
            + "* This app cannot diagnose a medical condition.\n"
            + "* This app cannot treat a medical condition.\n\n"
            + "Despite best efforts, there can be incorrect information. "
            + "If you suspect you have a serious medical condition, "
            + "continue to work with your doctors."
        )
        options = {True: "Yes, I understand that I am not getting medical advice."}
        mc = MultipleChoiceQuestion(
            question,
            options,
            self.question_id,
            selected=prev_answer,
            has_other_textbox=False,
            prev_button_link="InTake.IntakePledge",
            next_button_link="InTake.IntakeLanding",
        )
        mc.next_button.set_event_handler(
          'click',
          mc._update_question_answer
        )
        mc.next_button.set_event_handler(
          'click',
          self.create_account_and_navigate
        )
        self.outlined_card_1.add_component(mc.panel)

    def create_account_and_navigate(self, **event_args):
      # TODO check whether user is logged in first
      anvil.users.login_with_form()
      anvil.server.call('intake_merge_guest_and_logged_in')
      open_form("InTake.IntakeLanding")