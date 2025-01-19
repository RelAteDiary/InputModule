import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.email
import anvil.server
from datetime import datetime

@anvil.server.callable
def send_feedback(name, email, feedback):
  # Send yourself an email each time feedback is submitted
  anvil.email.send(to="lutetium.helen@gmail.com", # Change this to your email address and remove the #!
                   subject=f"Feedback from {name}",
                   text=f"""
                   
  A new person has filled out the feedback form!

  Name: {name}
  Email address: {email}
  Feedback:
  {feedback}
  """)
  app_tables.feedback_table.add_row(Name=name,Email=email,feedback=feedback,created=datetime.now())