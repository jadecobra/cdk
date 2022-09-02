import sniffer.api
import subprocess
import os

watch_paths = ['tests/', 'src/']

@sniffer.api.runnable
def run_tests(*args):
    if subprocess.run('python -m unittest -f', shell=True).returncode == 0:
        return True