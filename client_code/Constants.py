import anvil.server


@anvil.server.portable_class
class Constants:
  # database enums
  EXPERIMENT_ELIMINATION = "elimination"
  EXPERIMENT_REINTRODUCTION = "reintroduction"
  EXPERIMENT_SELF_DIRECTED = "self_directed"

  FOOD_GROUP_FODMAP = "fodmap"
  FOOD_GROUP_HISTMAINE = "histamine"
  FOOD_GROUP_SALICYLATES = "salicylates"

  symptoms_list = [
    "bloating",
    "belly pain/stomach ache/abdominal pain",
    "diarrhea",
    "gas/farts/burps",
    "bloating",
    "nausea",
    "heartburn/GERD",
    "headache",
    "migrain",
    "upset stomach",
    "joint pain",
    "fatigue/feeling tired",
    "skin rash/hives or eczema",
    "whezing/difficulty breathing/short-breathed",
    "dizzy/fainting",
    "chest pain",
    "irritability",
    'itchy or tingly mouth, lips, or throat',
    'nasal congestion/runny nose',
    'lump in your throat',
    'pounding heart or heart palpitations',
    'mood disturbances',
    'irritable/angry/frustrated'
  ]
  # TODO make more
