import pgzrun

from coding_games import Level, AnimatedActor, Direction, Hud, WIDTH, HEIGHT, ICON, DizzyActor
from coding_games.Harmfull import Harmful
from coding_games.State import State


class Bat(AnimatedActor, Harmful):
    def __init__(self, image, dimensions, state: State = State(), name="bat"):
        super().__init__(image, name=name, state=state, sprite=dimensions)
        self.flight_direction = None
        self.flight_progress = 0

    def update(self):
        self.harm()
        if self.flight_direction is None:
            self.flight_direction = Direction.right
        if self.flight_direction == Direction.right:
            self.x += 1
            self.flight_progress += 1
            if self.flight_progress == 500:
                self.flight_direction = Direction.left
        elif self.flight_direction == Direction.left:
            self.x -= 1
            self.flight_progress -= 1
            if self.flight_progress == 0:
                self.flight_direction = Direction.right

    def harm(self, **kwargs):
        actors = self.colliding_actors(level.get_actors())
        if len(actors) != 0:
            hud.hp_percentage -= 1

    def __str__(self):
        return self.name


hud = Hud(hp_percentage=100, lives=3)
level = Level("lets_get_moving")
dizzy = DizzyActor()
dizzy.pos = (300, 500)
level.actors.append(dizzy)

bat = Bat('bat', (32, 32))
bat.pos = (300, 500)
level.actors.append(bat)


def update():
    dizzy.update(keyboard, level)
    bat.update()


def draw():
    screen.clear()
    level.draw()
    hud.draw(screen=screen, title="Dizzy locked..")
    # dizzy.draw()


pgzrun.go()
