from coding_games.DizzyState import ActorStanding
from coding_games.AnimatedActor import AnimatedActor
from coding_games.Controlable import Controlable
from coding_games.Direction import Direction
from pgzero.keyboard import Keyboard


class DizzyActor(AnimatedActor, Controlable):
    def __init__(self, *args, **kwargs):
        super().__init__('dizzy-standing', name='dizzy', sprite=(72, 60), duration=500, pingpong=False, gravity=True, state=ActorStanding(self))

    def update(self, key: Keyboard, world):
        direction = None
        if key.SPACE and key.RIGHT:
            direction = Direction.up_right
        elif key.SPACE and key.LEFT:
            direction = Direction.up_left
        elif key.RIGHT:
            direction = Direction.right
        elif key.LEFT:
            direction = Direction.left
        elif key.SPACE:
            direction = Direction.up
        self.move(direction, key, world)
