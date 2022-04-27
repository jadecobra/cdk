import unittest
import json
import os
# os.system('pip install -r requirements.txt')
from time import time
from datetime import datetime

true = True
false = False

def log(message):
    result = f"{datetime.now()}::{message}\n"
    print(result)
    return result

def log_performance(result):
    os.makedirs('logs', exist_ok=True)
    with open('logs/performance.log', 'a') as writer:
        writer.write(result)

def time_it(function, *args, description='run process', **kwargs):
    start_time = time()
    function(*args, **kwargs)
    result = f'Time taken to {description}::  {time() - start_time:.4f} seconds'
    log_performance(log(result))


def load_json(filepath):
    with open(filepath) as f:
        return json.load(f)

class TestTemplates(unittest.TestCase):

    maxDiff = None

    def assert_template_equal(self, stack_name):
        os.system('clear')
        time_it(os.system, f'cdk ls {stack_name} --version-reporting=false --path-metadata=false --asset-metadata=false', description=f'synthesize stack: {stack_name}')
        # time_it(os.system, f'cdk ls {stack_name}', description=f'synthesize stack: {stack_name}')

        return self.assertEqual(
            load_json(f'cdk.out/{stack_name}.template.json'),
            load_json(f'tests/templates/{stack_name}.template.json')
        )