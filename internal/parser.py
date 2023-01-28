import re

from internal.task_classes import Series, Parallel, Group, Command


class Parser:
    def __init__(self, code_lines):
        self.code_lines = code_lines
        self.last_nesting = 0
        self.current_parent = None
        self.last_node = None
        self.root_node = None

    @staticmethod
    def _get_line_info(line, i):
        match = re.search("^(\s*)([\w| |'|\"]+)#?", line)
        spaces, key = match.group(1), match.group(2).strip()
        nesting = len(spaces) / 4
        if nesting != len(spaces) // 4:
            raise RuntimeError(f"Arkan parsing error: wrong indent on line {i+1}: '{line.strip()}'")
        return int(nesting), key

    @staticmethod
    def _create_node(key):
        if key == Group.SERIES:
            return Series()
        elif key == Group.PARALLEL:
            return Parallel()
        return Command(key)

    @staticmethod
    def _is_comment(line):
        match = re.search("^\s*#", line)
        return match is not None

    def parse(self):
        for i, line in enumerate(self.code_lines):

            # Process comments & empty lines
            if self._is_comment(line) or len(line.strip()) == 0:
                continue
            nesting, key = self._get_line_info(line, i)

            if nesting == 0 and self.root_node is not None:
                raise RuntimeError(f"Arkan parsing error on line {i+1}: only one root task allowed")

            # Create node for current string
            node = self._create_node(key)

            # Update current parent node if nesting changed
            if nesting < self.last_nesting:
                temp_node = self.last_node
                for j in range(nesting, self.last_nesting + 1):
                    temp_node = temp_node.parent
                self.current_parent = temp_node
            elif nesting > self.last_nesting:
                self.current_parent = self.last_node

            # Assign created node to current parent node
            if self.current_parent:
                self.current_parent.add_subtask(node)

            # Set root node if created node is first
            if self.root_node is None:
                self.root_node = node
                self.current_parent = node

            self.last_node = node
            self.last_nesting = nesting

        return self.root_node
