class Stack:
    def __init__(self, init_list=None):
        if init_list is None:
            self.stack = []
        else:
            self.stack = init_list

    @property
    def pop(self):
        return self.stack.pop()

    def push(self, item):
        self.stack.append(item)

    @property
    def peek(self):
        return self.stack[-1] if self.stack else None

    @property
    def is_empty(self):
        return len(self.stack) == 0

    def __len__(self):
        return len(self.stack)