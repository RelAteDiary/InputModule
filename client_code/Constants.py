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
    "belly pain/stomach ache/abdominal pain",
    "bloating",
    "chest pain",
    "diarrhea",
    "dizzy/fainting",
    "fatigue/feeling tired",
    "gas/farts/burps",
    "headache",
    "heartburn/GERD",
    "irritability",
    "joint pain",
    "migrain",
    "nausea",
    "skin rash/hives or eczema",
    "upset stomach",
    "whezing/difficulty breathing/short-breathed",
    'irritable/angry/frustrated',
    'itchy or tingly mouth, lips, or throat',
    'lump in your throat',
    'mood disturbances',
    'nasal congestion/runny nose',
    'pounding heart or heart palpitations',
  ]
  # TODO make more
