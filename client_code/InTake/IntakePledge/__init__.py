from ._anvil_designer import IntakePledgeTemplate
from anvil import *
import anvil.server
from ..CheckBoxQuestion import CheckBoxQuestion


class IntakePledge(IntakePledgeTemplate):
    def __init__(self, **properties):
        self.question_id = "pledges"
        [goal, pledges] = anvil.server.call(
            "intake_get_answer", ["goal", self.question_id]
        )
        print(f'goal and pledges are {goal} and {pledges}')
        if goal is None:
          goal_text = ''
        elif goal.startswith("other-"):
          goal_text = goal[len("other-") :]
        else:
          goal_text = goal.replace("_", " ")

        callout = "Pledge to work towards your goal: " + goal_text
        question = (
            "The more accurately you log in the food and symptoms diary, "
            + "the more information we can use to figure out what foods are "
            + "making you feel bad. Are you willing to make **a commitment "
            + "to yourself to work on feeling better**?"
        )
        options = {
            "persevere": "I pledge to keep trying and not give up on my health.",
            "log_daily": "I pledge to log my meals and symptoms every day this week, or at least try my best to",
        }
        mc = CheckBoxQuestion(
            question,
            options,
            self.question_id,
            selected=pledges,
            callout=callout,
            prev_button_link="InTake.IntakeGoal",
            next_button_link="InTake.IntakeDiets",
        )
        self.outlined_card_1.add_component(mc.panel)
