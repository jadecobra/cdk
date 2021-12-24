from unittest import TestCase
from json import load
from os import system

true = True
false = False

class TestTemplates(TestCase):
    maxDiff = None

    def assert_template_equal(self, template_name, expected_template):
        system('clear')
        system('cdk ls')
        with open(f'cdk.out/{template_name}.template.json') as template:
            self.assertEqual(load(template), expected_template)