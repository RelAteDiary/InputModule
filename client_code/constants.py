import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# database enums
EXPERIMENT_ELIMINATION = 'elimination'
EXPERIMENT_REINTRODUCTION = 'reintroduction'
EXPERIMENT_SELF_DIRECTED = 'self_directed'

FOOD_GROUP_FODMAP = 'fodmap'
FOOD_GROUP_HISTMAINE = 'histamine'
FOOD_GROUP_SALICYLATES = 'salicylates'
# TODO make more
