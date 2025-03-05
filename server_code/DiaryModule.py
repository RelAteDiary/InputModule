import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime, date, timedelta

@anvil.server.callable
def diary_get_entries(latest=None, days_prior=7, fetch_only_columns=None):
  me = anvil.users.get_user()
  last_day = latest if latest is not None else datetime.now()
  fetch_only_columns = (
    fetch_only_columns
    if fetch_only_columns is not None
    else [x['name'] for x in app_tables.diary.list_columns()]
  )
  entries = app_tables.diary.search(q.fetch_only(*fetch_only_columns),
    user=me, time=q.between(last_day - timedelta(days=days_prior), last_day)
  )
  # Search iterator is lazy. To avoid additional calls to server, materialize
  # this list, which should be quite short.
  return [x for x in entries]
