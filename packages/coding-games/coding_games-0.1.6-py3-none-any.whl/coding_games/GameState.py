from coding_games.State import State


class GamePaused(State):
    def __init__(self, world):
        super().__init__()
        self.name = "paused"

    def update(self, key, world):
        pass


class GameActive(State):
    def __init__(self, world):
        super().__init__()
        self.name = "active"

    def update(self, key, world):
        pass