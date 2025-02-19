import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import uuid

def get_guest_id():
  guest_id= anvil.server.cookies.local.get('guest_id', '')
  if guest_id == '':
    guest_id = str(uuid.uuid4())
    anvil.server.cookies.local.set(30, guest_id=guest_id)
    app_tables.users.add_row(guest_id=guest_id)
  return guest_id

@anvil.server.callable
def intake_start():
  get_guest_id()

@anvil.server.callable
def intake_submit():
  pass

@anvil.server.callable
def intake_set_answer(question, value):
  guest_id = get_guest_id()
  user = app_tables.users.get(guest_id=guest_id)
  if user is None:
    print("Something has gone wrong, user is not being found.")
  match question:
    case 'goal':
      user['goal'] = value

@anvil.server.callable
def intake_get_answer(question):
  guest_id = get_guest_id()
  user = app_tables.users.get(guest_id=guest_id)
  
  if user is None:
    return ''
  return user[question]

def merge_logged_in_user():
  pass