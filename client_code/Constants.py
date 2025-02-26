import anvil.server

@anvil.server.portable_class
class Constants():
  # database enums
  EXPERIMENT_ELIMINATION = 'elimination'
  EXPERIMENT_REINTRODUCTION = 'reintroduction'
  EXPERIMENT_SELF_DIRECTED = 'self_directed'
  
  FOOD_GROUP_FODMAP = 'fodmap'
  FOOD_GROUP_HISTMAINE = 'histamine'
  FOOD_GROUP_SALICYLATES = 'salicylates'
  # TODO make more
