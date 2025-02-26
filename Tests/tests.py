import unittest

import anvil.server
import anvil.users
from anvil.tables import app_tables

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

import server_code.serverExperiments


class TestMethods(unittest.TestCase):
    def test_string_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_string_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_string_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])

    def test_math_multiplikation(self):
        self.assertEqual(2 * 2, 5)
