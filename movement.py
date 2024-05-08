
class MovementStack:
    def __init__(self):
        self.stack = []

    def push(self, movement):
        self.stack.append(movement)

    def pop(self):
        return self.stack.pop()

    def get(self):
        return self.stack[-1]

    def __len__(self):
        return len(self.stack)

