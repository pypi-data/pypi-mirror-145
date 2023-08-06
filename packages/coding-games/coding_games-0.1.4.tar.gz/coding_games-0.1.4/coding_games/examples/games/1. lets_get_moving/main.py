import pgzrun

from coding_games import Level, DizzyActor, WIDTH, HEIGHT

level = Level("lets_get_moving")
dizzy = DizzyActor()
dizzy.pos = (300, 300)


def update():
    dizzy.update(keyboard, level)

def draw():
    screen.clear()
    level.draw()
    dizzy.draw()

pgzrun.go()
