import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import uuid

def _question_id_to_user_column(question_id):
  match question_id:
    case 'goal':
      return 'p-goal'
    case 'pledge':
      return 'p-pledge'
  return ''

def get_guest_id():
  guest_id= anvil.server.cookies.local.get('guest_id', '')
  if guest_id == '':
    guest_id = str(uuid.uuid4())
    anvil.server.cookies.local.set(30, guest_id=guest_id)
    app_tables.users.add_row(guest_id=guest_id)
  return guest_id

@anvil.server.callable
def intake_submit():
  pass

@anvil.server.callable
def intake_set_answer(question_id, value):
  guest_id = get_guest_id()
  user = app_tables.users.get(guest_id=guest_id)
  if user is None:
    print("Something has gone wrong, user is not being found.")
  column = _question_id_to_user_column(question_id)
  if column != '':
    user[column] = value

@anvil.server.callable
def intake_get_answer(question_ids):
  answers = []
  guest_id = get_guest_id()
  user = app_tables.users.get(guest_id=guest_id)
  if user is None:
    print("Something has gone wrong, user is not being found.")
    return ''

  for question_id in question_ids:
    column = _question_id_to_user_column(question_id)
    if column != '':
      answer=user[column]
      if answer is None:
        answer = ''
      answers.append(answer)
    else:
      answers.append('')
  return answers

def merge_logged_in_user():
  pass