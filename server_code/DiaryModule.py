import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from collections import Counter
from datetime import datetime, date, timedelta


@anvil.server.callable
def diary_get_entries(latest=None, days_prior=7, fetch_only_columns=None):
  me = anvil.users.get_user()
  last_day = latest if latest is not None else datetime.now()
  fetch_only_columns = (
    fetch_only_columns
    if fetch_only_columns is not None
    else [x["name"] for x in app_tables.diary.list_columns()]
  )
  entries = app_tables.diary.search(
    q.fetch_only(*fetch_only_columns),
    user=me,
    time=q.between(last_day - timedelta(days=days_prior), last_day, max_inclusive=True),
  )
  print(f"Entries in DiaryModule is {[x for x in entries]}")
  # Search iterator is lazy. To avoid additional calls to server, materialize
  # this list, which should be quite short.
  return [x for x in entries]


@anvil.server.callable
def diary_get_frequent_recent_symptoms(top=5):
  """
  Find the `top` most frequent symptoms for the user in the past 7 days.
  """
  me = anvil.users.get_user()
  rows = app_tables.diary.search(
    q.fetch_only("symptom"),
    q.all_of(
      user=me,
      symptom=q.not_(None),
      time=q.greater_than(datetime.now() - timedelta(days=7)),
    ),
  )

  symptoms = [r["symptom"] for r in rows]
  frequent_symptoms_and_count = Counter(symptoms).most_common(top)
  frequent_symptoms = [symptom for (symptom, count) in frequent_symptoms_and_count]
  print(frequent_symptoms)
  return frequent_symptoms


@anvil.server.callable
def diary_add_entry(
  time=None,
  note=None,
  note_color=None,
  symptom=None,
  symptom_severity=None,
  type=None,
  image=None,
):
  me = anvil.users.get_user()
  if note is not None:
    app_tables.diary.add_row(
      user=me,
      time=time,
      notes=note,
      note_color=note_color,
      symptom=symptom,
      symptom_severity=symptom_severity,
      image=image
    )
    return True
  else:
    return False
