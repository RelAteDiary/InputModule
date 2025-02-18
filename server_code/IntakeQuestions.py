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
  return anvil.server.cookies.local.get('guest_id', '')

@anvil.server.callable
def start_intake_questions():
  guest_id = get_guest_id()
  if guest_id == '':
    guest_id = str(uuid.uuid4())
    anvil.server.cookies.local.set(30, guest_id=guest_id)
    app_tables.users.add_row(guest_id=guest_id)

@anvil.server.callable
def submit_intake_question():
  guest_id = get_guest_id()
  if guest_id == '':
    anvil.server.cookies.local.set(30, guest_id=guest_id)
    app_tables.users.add_row(guest_id=guest_id)

def merge_logged_in_user():
  get_guest_id