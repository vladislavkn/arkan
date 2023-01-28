import multiprocessing
import os


# Basic observable task class
class Task:
    def __init__(self):
        self._done_callback = None
        self.parent = None

    def execute_on_done(self, fn):
        self._done_callback = fn

    def _on_done(self):
        if self._done_callback:
            self._done_callback()


# Shell command class
class Command(Task):
    def __init__(self, command):
        super().__init__()
        self.command = command
        self.parent = None

    def execute(self):
        os.system(self.command)
        self._on_done()

    def get_name(self):
        return self.command + f"({self.__hash__()})"

    def get_string_with_indent(self, indent_level=0):
        return "\t" * indent_level + self.get_name()

    def __str__(self):
        return self.get_string_with_indent()


# Basic command group class
class Group(Task):
    SERIES = "series"
    PARALLEL = "parallel"

    def __init__(self, exec_type, subtasks=None):
        super().__init__()
        if subtasks is None:
            subtasks = []
        for task in subtasks:
            task.parent = self
        self.exec_type = exec_type
        self.subtasks = subtasks
        self.parent = None

    def execute(self):
        raise NotImplemented()

    def add_subtask(self, subtask):
        if subtask != self:
            subtask.parent = self
            self.subtasks.append(subtask)

    def get_name(self):
        return self.exec_type + f"({self.__hash__()})"

    def get_string_with_indent(self, indent_level=0):
        result = "\t" * indent_level + self.get_name()
        for subtask in self.subtasks:
            result += '\n' + subtask.get_string_with_indent(indent_level + 1)
        return result

    def __str__(self):
        return self.get_string_with_indent()


# Group that execute commands in series
class Series(Group):

    def __init__(self, subtasks=None):
        super().__init__(Group.SERIES, subtasks)
        self.current_task_index = 0

    def execute(self):
        if self.current_task_index < len(self.subtasks):
            next_task = self.subtasks[self.current_task_index]
            self.current_task_index += 1
            next_task.execute_on_done(self.execute)
            next_task.execute()
        else:
            self._on_done()


# Group that execute commands in parallel
class Parallel(Group):
    def __init__(self, subtasks=None):
        super().__init__(Group.PARALLEL, subtasks)
        self.done_tasks = 0

    def execute(self):
        threads = []

        for task in self.subtasks:
            thread = multiprocessing.Process(target=task.execute)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self._on_done()
