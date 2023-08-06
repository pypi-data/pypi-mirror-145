import pgzrun

from coding_games import Level, WIDTH, HEIGHT, Flare, Backpack, Item, Dialog, Hud

level = Level("moving_things")

flare = Flare()
flare.pos = (350, 350)

backpack = Backpack()

box = Item("crate", (32, 32))
box.pos = (400, 450)


def remove():
    level.items.append(box)
    box.pos = dizzy.pos


box.use_item = remove

level.items.append(box)

dizzy = level.actors[0]

dialog = Dialog(["Hello I'm Dizzy", "Let's play a game", "",  "Your task is to ", "move the things",
                 "to the bottom ", "chamber..", "", "Are you ready?.."], color=(100, 244, 200), width=14)

hud = Hud(hp_percentage=100, lives=3)


def update():
    level.update(keyboard)


def on_key_down(key):
    global dialog
    if key == keys.RETURN:
        if dialog is not None:
            dialog = None

    if key == keys.B:
        backpack.isOpened = not backpack.isOpened

    if key == keys.G:
        item = dizzy.grabItem(level.items)
        if item is not None:
            level.items.remove(item)
            backpack.add_item(item)

    if backpack.isOpened:
        if key == key.DOWN:
            backpack.next_position()
        if key == key.UP:
            backpack.previous_position()
        if key == key.RETURN:
            backpack.use_item()
        return


def draw():
    screen.clear()
    level.draw()
    flare.draw()

    backpack.draw_backpack(screen=screen)

    hud.draw(screen=screen, title="Moving things..")

    if dialog is not None:
        dialog.draw(screen)


pgzrun.go()
