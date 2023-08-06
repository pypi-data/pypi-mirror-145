import pgzrun

from coding_games import Backpack, WIDTH, HEIGHT, Dialog
from coding_games.Level import Level
from coding_games.utils.LevelChain import LevelChain

backpack = Backpack()

levelchain = LevelChain([[Level("boat_passage"), Level("green_wizard")]])
dizzy = levelchain.level.actors[0]

dialogs = []


def update():
    global dizzy
    levelchain.level.update(keyboard)

    if levelchain.level.name == "boat_passage" and dizzy.pos[0] > 1050:
        levelchain.go_right()
        old_pos = dizzy.pos
        dizzy = levelchain.level.actors[0]
        dizzy.pos = (170, old_pos[1] - 10)

    if levelchain.level.name == "green_wizard" and dizzy.pos[0] < 160:
        levelchain.go_left()
        old_pos = dizzy.pos
        dizzy = levelchain.level.actors[0]
        dizzy.pos = (1000, old_pos[1] - 10)

    if levelchain.level.name == "green_wizard" and dizzy.pos[0] > 950:
        if len(dialogs) == 0:
            dialogs.append(Dialog(["Good job dizzy..", "", "Thank you..."], width=14, color=(255, 230, 200)))


def draw():
    screen.clear()
    levelchain.level.draw()

    for dialog in dialogs:
        dialog.draw(screen)


def on_key_down(key):
    # LEVEL Movement
    if key == keys.A:
        if levelchain.go_left():
            print("Going left")
    elif key == keys.D:
        if levelchain.go_right():
            print("Going right")
    elif key == keys.W:
        if levelchain.go_up():
            print("Going up")
    elif key == keys.S:
        if levelchain.go_down():
            print("Going down")

pgzrun.go()
