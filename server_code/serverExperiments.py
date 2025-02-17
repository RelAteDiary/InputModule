# import anvil.secrets
# import anvil.google.auth, anvil.google.drive, anvil.google.mail
# from anvil.google.drive import app_files
# import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables
# import anvil.server
# from Constants import Constants
# import datetime

# liu = app_tables.users.get(email='lutetium.helen@gmail.com')
# app_tables.experiments.add_row(user=liu,
#                              Text="Jane is a good kid")

# @anvil.server.callable
# def experiments_get_current():
#   app_tables.experiments.search(
#     user=anvil.users.get_user(),
#     end=q.any_of(None, q.greater_than(datetime.today())))
  
# @anvil.server.callable
# def experiments_get_type_text(db_type):
#   if db_type == Constants.EXPERIMENT_ELIMINATION:
#     return 'Elimination diet'
#   elif db_type == Constants.EXPERIMENT_REINTRODUCTION:
#     return 'Reintroduction diet'
#   elif db_type == Constants.EXPERIMENT_SELF_DIRECTED:
#     return 'Experiment'

# @anvil.server.callable
# def experiments_get_parameter_text(db_text):
#   return db_text
