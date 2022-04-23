import sniffer.api
import subprocess
import os

@sniffer.api.file_validator
def py_files(filename):
    return filename.endswith('.py') and not os.path.basename(filename).startswith('.')

@sniffer.api.file_validator
def py_files(filename):
    return filename.endswith('.json') and not os.path.basename(filename).startswith('.')

@sniffer.api.runnable
def run_tests(*args):
    if subprocess.run('python -m unittest -f', shell=True).returncode == 0:
        return True