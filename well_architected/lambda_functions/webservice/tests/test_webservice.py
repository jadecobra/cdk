import unittest
import webservice


class TestWebservice(unittest.TestCase):

    def test_failing(self):
        self.assertEqual(5, 6)