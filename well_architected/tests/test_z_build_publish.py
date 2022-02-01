import unittest
import os

def tasks_path(filename):
    return f'tests/tasks/{filename}'

def get_tasks():
    return get_task_file_contents('tasklist')

def get_completed():
    return get_task_file_contents('completed')

def get_todo():
    return get_task_file_contents('todo')

def get_task_file_contents(filename):
  try:
      with open(tasks_path(filename)) as reader:
          return reader.readlines()
  except FileNotFoundError:
      return []

def write_to_file(filename=None, contents=None):
    with open(tasks_path(filename), 'w') as writer:
        for item in contents:
            writer.write(item)

def get_unique(collection):
    return list(set(collection))

def get_todo_list():
    return get_unique([task for task in get_tasks() if task not in get_completed()])

def create_todo():
    write_to_file(filename='todo', contents=get_todo_list())

def add_to_completed(task):
    result = get_completed()
    print(result)
    result.append(task)
    write_to_file(filename='completed', contents=get_unique(result))

def commit(task):
    add_to_completed(task)
    os.system(f'git commit -am {task}')

def record_task(task=None, response='y'):
    if response.lower() != 'y':
        print(f'go work on {task}...')
    else:
        commit(task)


class TestBuildDeploy(unittest.TestCase):

    def test_focusing_on_task(self):
        create_todo()
        self.assertEqual(
            sorted(get_unique(get_todo() + get_completed())),
            sorted(get_tasks())
        )
        task = get_todo()[0]
        record_task(
            task=task,
            response=input(f'do you want to commit this change as {task}: [y]/n: ')
        )
