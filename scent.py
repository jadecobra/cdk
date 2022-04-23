import sniffer.api
import subprocess
import os

# from sniffer.api import * # import the really small API
# import os, termstyle

# you can customize the pass/fail colors like this
# pass_fg_color = termstyle.green
# pass_bg_color = termstyle.bg_default
# fail_fg_color = termstyle.red
# fail_bg_color = termstyle.bg_default

# All lists in this variable will be under surveillance for changes.
watch_paths = [
    '.',
    'tests/',
    # 'cdk.out/'
]

# this gets invoked on every file that gets changed in the directory. Return
# True to invoke any runnable functions, False otherwise.
#
# This fires runnables only if files ending with .py extension and not prefixed
# with a period.
# @sniffer.api.file_validator
# def py_files(filename):
#     return filename.endswith('.py') and not os.path.basename(filename).startswith('.')

def suffix(text):
    return f'.{text}'

def filename_endswith(filename=None, suffix=None):
    return filename.endswith(f'.{suffix}')

@sniffer.api.file_validator
def json_files(filename):
    return (
        filename.endswith(suffix('py'))
     or filename.endswith(suffix('json'))
    ) and not os.path.basename(filename).startswith('.')

@sniffer.api.runnable
def run_tests(*args):
    if subprocess.run('python -m unittest -f', shell=True).returncode == 0:
        return True