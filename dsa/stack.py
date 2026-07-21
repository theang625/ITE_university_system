class Stack:
    def __init__(self):
        self.history = []

    def push(self, action):
        """Saves an action to the top of the stack."""
        self.history.append(action)

    def pop(self):
        """Removes and returns the most recent action."""
        if not self.is_empty():
            return self.history.pop()
        return None

    def is_empty(self):
        return len(self.history) == 0