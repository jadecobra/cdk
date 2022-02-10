import unittest
import json
import os
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


class TestTemplates(unittest.TestCase):

    maxDiff = None

    @unittest.expectedFailure
    def assert_template_equal(self, template_name, stack_name):
        os.system('clear')
        # time_it(os.system, f'cdk ls {template_name} --version-reporting=false --path-metadata=false --asset-metadata=false', description=f'synthesize stack: {template_name}')
        # with open(f'cdk.out/{template_name}.template.json') as template:
        #     return self.assertEqual(json.load(template), stack_name)