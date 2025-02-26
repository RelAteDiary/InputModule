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
    case 'pledges':
      return 'p-pledges'
    case 'diets':
      return 'p-diets'
    case 'acknowledge_disclaimer':
      return 'p-ack_non_med_disclaimer'
  return ''

def get_guest_id():
  guest_id= anvil.server.cookies.local.get('guest_id', '')
  if guest_id == '':
    print('guest_id is empty string')
    guest_id = str(uuid.uuid4())
    anvil.server.cookies.local.set(30, guest_id=guest_id)
  if len(app_tables.users.search(guest_id=guest_id))==0:
    print('adding new row to db')
    app_tables.users.add_row(guest_id=guest_id)
  return guest_id

@anvil.server.callable
def intake_merge_guest_and_logged_in():
  guest_user = app_tables.users.get(guest_id=get_guest_id())
  logged_in_user = anvil.users.get_user()
  if guest_user is None or logged_in_user is None:
    return
  for column in app_tables.users.list_columns():
    if (logged_in_user[column['name']] is None):
      logged_in_user[column['name']] = guest_user[column['name']]
  guest_user.delete()

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
  if anvil.users.get_user():
    user = anvil.users.get_user()
  else:
    user = app_tables.users.get(guest_id=get_guest_id())

  if user is None:
    print("Something has gone wrong, user is not being found.")
    return ''

  for question_id in question_ids:
    column = _question_id_to_user_column(question_id)
    print(f'in IntakeQuestions column is {column}')
    if column != '':
      answer=user[column]
      print(f'in IntakeQuestions answer is {answer}')
      answers.append(answer)
    else:
      answers.append(None)
  return answers

def merge_logged_in_user():
  pass