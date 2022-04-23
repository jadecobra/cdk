import sniffer.api
import subprocess
import os

def filename_endswith(filename=None, suffix=None):
    return filename.endswith(f'.{suffix}') and not os.path.basename(filename).startswith('.')

@sniffer.api.file_validator
def py_files(filename):
    return filename_endswith(filename, 'py')
    return filename.endswith('.py') and not os.path.basename(filename).startswith('.')

@sniffer.api.file_validator
def json_files(filename):
    return filename_endswith(filename, 'json')
    return filename.endswith('.json') and not os.path.basename(filename).startswith('.')

@sniffer.api.runnable
def run_tests(*args):
    if subprocess.run('python -m unittest -f', shell=True).returncode == 0:
        return True