import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import uuid

def _question_id_to_user_column(question_id):
  match question_id:
    case 'goal':
      return 'p-goal'
    case 'pledges':
      return 'p-pledges'
    case 'diets':
      return 'p-diets'
    case 'acknowledge_disclaimer':
      return 'p-ack_non_med_disclaimer'
  return ''

@anvil.tables.in_transaction
def get_guest_user():
  '''
  Gets the guest user according to uuid set in the user's cookie.
  If the uuid is not set or if the guest user row is not found, 
  creates the guest user.
  '''
  guest_id= anvil.server.cookies.local.get('guest_id', '')
  if guest_id == '':
    guest_id = str(uuid.uuid4())
    anvil.server.cookies.local.set(30, guest_id=guest_id)
  guest_user = app_tables.users.get(guest_id=guest_id)
  if guest_user is None:
    guest_user = app_tables.users.add_row(guest_id=guest_id)
  return guest_user

def get_user():
  '''
  Returns the logged in user if the user is logged in, 
  creates or gets a guest user identified by uuid otherwise.
  '''
  logged_in_user = anvil.users.get_user()
  if logged_in_user is None:
    return get_guest_user()
  return logged_in_user

@anvil.server.callable
def intake_merge_guest_and_logged_in():
  guest_user = get_guest_user()
  logged_in_user = anvil.users.get_user()
  if guest_user is None or logged_in_user is None:
    print('WARNING could not merge guest user and logged in user')
    return
  for column in app_tables.users.list_columns():
    if (logged_in_user[column['name']] is None):
      logged_in_user[column['name']] = guest_user[column['name']]
  guest_user.delete()

@anvil.server.callable
def intake_set_answer(question_id, value):
  user = get_user()
  if user is None:
    print("Something has gone wrong, user is not being found.")
  column = _question_id_to_user_column(question_id)
  if column != '':
    user[column] = value

@anvil.server.callable
def intake_get_answer(question_ids):
  answers = []
  user = get_user()

  if user is None:
    print("Something has gone wrong, user is not being found.")
    return ''

  for question_id in question_ids:
    column = _question_id_to_user_column(question_id)
    if column != '':
      answer=user[column]
      answers.append(answer)
    else:
      answers.append(None)
  return answers

def merge_logged_in_user():
  pass