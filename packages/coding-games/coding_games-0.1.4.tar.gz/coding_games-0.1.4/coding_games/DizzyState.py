from coding_games.ActorState import ActorState
from coding_games.Direction import Direction



class ActorStanding(ActorState):
    def __init__(self, actor):
        super().__init__(name="standing", image="dizzy-standing.png", actor=actor)

    def update(self, key, world):
        if key.left:
            self.actor.state = ActorMoving(self.actor, Direction.left)
        elif key.space:
            self.actor.state = ActorJumping(self.actor)
        elif key.right:
            self.actor.state = ActorMoving(self.actor, Direction.right)


class ActorMoving(ActorState):
    def __init__(self, actor, direction):
        if direction == Direction.right:
            name = "moving-right"
            dizzy_image = "dizzy-right.png"
        else:
            name = "moving-left"
            dizzy_image = "dizzy-left.png"
        super().__init__(name=name, actor=actor, image=dizzy_image)
        self.direction = direction

    def update(self, key, world):
        if key.left:
            self.actor.state = ActorMoving(self.actor, Direction.left)
        elif key.right:
            self.actor.state = ActorMoving(self.actor, Direction.right)
        elif key.space:
            self.actor.state = ActorJumping(self.actor)
        else:
            self.actor.state = ActorStanding(self.actor)


class ActorJumping(ActorState):
    def __init__(self, actor):
        super().__init__(name="jumping", actor=actor, image= "dizzy_jump.png")

    def update(self, key, world):
        if key.left:
            self.actor.state = ActorMoving(self.actor, Direction.left)
        elif key.right:
            self.actor.state = ActorMoving(self.actor, Direction.right)
        elif key.space:
            self.actor.state = ActorJumping(self.actor)
        else:
            self.actor.state = ActorStanding(self.actor)


class ActorFalling(ActorState):
    def __init__(self, actor):
        super().__init__(name="falling", actor=actor, image= "dizzy-standing.png")

    def update(self, key, world):
        pass
