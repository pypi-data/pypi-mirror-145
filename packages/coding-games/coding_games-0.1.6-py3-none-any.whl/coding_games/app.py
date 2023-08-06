import pgzrun
from coding_games.controller import Controller
from coding_games.Settings import  *

controller = Controller()


def draw():
    """
    Main "draw" method, if the controller doesnt have a screen property, this method will pass it to the controller as
    well as calling drawing method from a controller
    :return:
    """
    if controller.get_screen() is None:
        controller.set_screen(screen)
    controller.draw()


def update():
    """
    Main "update" method of the app
    """
    controller.update(keyboard)


def on_key_down(key):
    """
    Passing the on key down event to the controller
    :param key: Key that is pressed
    """
    controller.on_key_down(key, keys)

pgzrun.go()
