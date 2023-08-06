class State:
    def __init__(self, name="state"):
        self.name = name

    def update(self, key, world):
        pass

    def __str__(self):
        return self.name
