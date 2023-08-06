from coding_games.State import State
from coding_games.AnimatedActor import AnimatedActor


class ActorState(State):
    def __init__(self, name, actor: AnimatedActor, image):
        super().__init__(name)
        self.actor = actor
        self.image = image

    def update(self, key, world):
        pass