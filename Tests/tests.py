from unittest import TestCase

# Server is required for the uplink connection
import anvil.server

# The user service can be useful to sign in and find database rows linked 
# to the current user.
import anvil.users

# The tables can be used to check test results or to get the user row.
from anvil.tables import app_tables

# Different statements to import Globals when running on uplink vs on server.
# Importing Globals will instantiate the global variable that will contain all 
# the data used on the client.
# For this example let's make "boxes" that global variable.
if anvil.server.context.type == 'uplink':
    print('Running unit test locally...')
    import sys
    sys.path.insert(0, r'C:\Users\Liu\Documents\GitHub\InputModule')
    uplink_key = open('anvil_dev_server_uplink_key.txt', 'r')
    anvil.server.connect(uplink_key.read())
    # running tests on pc
    from client_code.Globals import *
else:
    # running on Anvil server
    from .Globals import *

# This import allows the decorated server callable to run on the uplink.
# Without it, they will run inside the app.
# With this import the server callable will run in a thread different from the
# test. Set a breakpoint on the server callable function to debug.
import server_code.serverExperiments
