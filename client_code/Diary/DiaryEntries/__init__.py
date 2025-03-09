from ._anvil_designer import DiaryEntriesTemplate
from anvil import DataGrid


class DiaryEntries(DiaryEntriesTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.data_grid = DataGrid(auto_header=False)

    # Any code you write here will run before the form opens.
