import pgzrun

from coding_games import Backpack, WIDTH, HEIGHT, AnimatedActor
from coding_games.Level import Level
from coding_games.Usable import UsableItem


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


class Jug(UsableItem):
    def __init__(self, image='jug', name='jug', dimensions=(64, 64), *args, **kwargs):
        super().__init__(image, name, dimensions, *args, **kwargs)

    def can_be_used(self, items: list):
        if fire in self.colliding_items(items) and leaves.can_be_used(items):
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




backpack = Backpack()

level = Level("locked")

dizzy = level.actors[0]
matches = Matches()
matches.pos = (600, 650)
level.items.append(matches)

leaves = Leaves()
leaves.pos = (850, 550)
level.items.append(leaves)


def update():
    level.update(keyboard)


def draw():
    screen.clear()
    level.draw()
    backpack.draw_backpack(screen=screen)

def on_key_down(key):
    if(key == keys.B):
        backpack.isOpened = not backpack.isOpened

    if(key == keys.G):
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

pgzrun.go()
