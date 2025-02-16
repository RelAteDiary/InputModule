import unittest
import anvil.server

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
        self.assertEqual(2*2, 5)

@anvil.server.callable
def run_tests():
  unittest.main(verbosity=1)