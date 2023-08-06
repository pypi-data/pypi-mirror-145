from coding_games import ActorState
from coding_games.AnimatedActor import AnimatedActor
from coding_games.State import State

class Item(AnimatedActor):
    def __init__(self, image, dimensions, state: State = State(), name='item'):
        super().__init__(image, name=name, state=state, sprite=dimensions)

    def update(self):
        pass

    def use_item(self):
        pass

    def __str__(self):
        return self.name
