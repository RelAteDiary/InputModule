# from ._anvil_designer import HomepageTemplate
# from anvil import *
# import anvil.server
# import anvil.google.auth, anvil.google.drive
# from anvil.google.drive import app_files
# import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables


# class Homepage(HomepageTemplate):
#   def __init__(self, **properties):
#     # Set Form properties and Data Bindings.
#     self.init_components(**properties)

#     gp = self.grid_panel_1
#     gp.add_component(Label(text="Name:"),
#                  row="ExperimentAt", col_xs=0, width_xs=2)
#     gp.add_component(Label(text="Name:"),
#                  row="ExperimentAt", col_xs=0, width_xs=2)

#     # Any code you write here will run before the form opens.

#   def outlined_button_1_click(self, **event_args):
#     """This method is called when the button is clicked"""
#     anvil.users.logout()
