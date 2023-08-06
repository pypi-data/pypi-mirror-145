from coding_games.ActorState import ActorState
from coding_games.Item import Item
from coding_games.Harmfull import Harmful


class Flare(Item, Harmful):
    def __init__(self):
        super().__init__(image='animated-flare', name='flare', dimensions=(64, 128), state=ActorState(name='burning', actor=self, image='animated-flare'))

    def update(self):
        pass