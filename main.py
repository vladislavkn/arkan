import io

import sys

from internal.parser import Parser

if __name__ == '__main__':
    tasks_filename = None

    # Read filename from the console (e.g. 'py main.py <filename>')
    try:
        tasks_filename = sys.argv[1]
    except IndexError:
        print("tasks filename is not set. Using 'arkconf'")
        tasks_filename = './arkconf'

    # Read specified file and parse groups
    with io.open(tasks_filename) as f:
        lines = f.readlines()
        root_task = Parser(lines).parse()
        root_task.execute()
