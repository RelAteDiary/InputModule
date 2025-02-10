from ._anvil_designer import ExperimentAtGlanceTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ExperimentAtGlance(ExperimentAtGlanceTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    gp = GridPanel()
    gp.add_component(Label(text=anvil.server.call.get_experiment_type_text("""TODO""")),
                 row="title", col_xs=0, width_xs=2)
    gp.add_component(Label(text=Experiments.get_experiment_parameter_text("""TODO""")),
                 row="content", col_xs=0, width_xs=2)
