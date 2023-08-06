import pgzrun

from coding_games import Level, DizzyActor, WIDTH, HEIGHT, ICON, Flare, Backpack, Item, Dialog, Hud, AnimatedActor
from coding_games.Usable import UsableItem

level = Level("moving_things")


class Leaves(UsableItem):
    def __init__(self, image='leaves', name='leaves', dimensions=(64, 32), *args, **kwargs):
        super().__init__(image, name, dimensions, *args, **kwargs)

    def can_be_used(self, items: list):
        return True

    def use(self, items: list):
        super().use(items)


class Matches(UsableItem):
    def __init__(self, image='matches', name='matches', dimensions=(64, 64), *args, **kwargs):
        super().__init__(image, name, dimensions, *args, **kwargs)

    def can_be_used(self, items: list):
        if leaves in self.colliding_items(items) and leaves.can_be_used(items):
            print('Can be used')
            return True
        return False

    def use(self, items):
        print("Using item")
        items.remove(leaves)
        fire = AnimatedActor(name='fire', image='fire', sprite=(64, 32))
        fire.pos = self.pos
        level.items.append(fire)
        super().use(items)


flare = Flare()
flare.pos = (350, 350)
backpack = Backpack()
dizzy = level.actors[0]
matches = Matches()
matches.pos = (400, 450)
level.items.append(matches)

leaves = Leaves()
leaves.pos = (550, 450)
level.items.append(leaves)

dialog = Dialog(["Hello I'm Dizzy", "Let's play a game"], color=(100, 244, 200), width=14)

hud = Hud(hp_percentage=100, lives=3)


def update():
    level.update(keyboard)


def on_key_down(key):
    if (key == keys.B):
        backpack.isOpened = not backpack.isOpened

    if (key == keys.G):
        item = dizzy.grabItem(level.items)
        if item is not None:
            level.items.remove(item)
            backpack.add_item(item)

    # if (key == keys.U):
    #     matches.use(level.get_items())

    if backpack.isOpened:
        if key == key.DOWN:
            backpack.next_position()
        if key == key.UP:
            backpack.previous_position()
        if key == key.RETURN:
            item = backpack.use_item()
            if item is not None:
                level.items.append(item)
                item.pos = dizzy.pos
                if isinstance(item, UsableItem):
                    # check ci sa da pouzit
                    if item.can_be_used(level.items):
                        item.use(level.items)
        return


def draw():
    screen.clear()
    level.draw()
    flare.draw()
    if backpack.isOpened:
        backpack.draw_backpack(screen=screen)

    # dialog.draw(screen)
    hud.draw(screen=screen, title="Dizzy locked..")


pgzrun.go()
