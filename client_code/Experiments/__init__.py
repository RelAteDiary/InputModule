import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import date
from .. import constants

liu = app_tables.users.get(email='lutetium.helen@gmail.com')
app_tables.experiments.add_row(Person=liu,
                             Text="Jane is a good kid")

def get_current_experiment():
  app_tables.experiments.search(
    user=anvil.users.get_user(),
    end=q.any_of(None, q.greater_than(date.today())))
  

def get_experiment_type_text(db_type):
  if db_type == constants.EXPERIMENT_ELIMINATION:
    return 'Elimination diet'
  elif db_type == constants.EXPERIMENT_REINTRODUCTION:
    return 'Reintroduction diet'
  elif db_type == constants.EXPERIMENT_SELF_DIRECTED:
    return 'Experiment'

def get_experiment_parameter_text(db_text):
  return db_text
