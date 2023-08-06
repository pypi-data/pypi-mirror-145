# there should be stored a state of the app (level)
# Controller should control the transition from one level to another
from pgzero.actor import Actor
from pgzero.screen import Screen

from coding_games.Backpack import Backpack
from coding_games.Dialog import Dialog
from coding_games.Hud import Hud
from coding_games.Level import Level
from coding_games.utils.LevelChain import LevelChain

from coding_games.GameState import *


class Controller:
    _screen = None
    _backpack = Backpack()
    dialogs = []
    # dialogs = [Dialog(["Hello my name is Dizzy", "Come and play"], 18, color=(128,0,0))]
    hud = Hud(hp_percentage=100, lives=3)

    def __init__(self):
        self.level_creator = LevelChain([[Level("main_level"), Level("side_walk")]])
        self.top = 0
        self.width = 32
        self.height = 24
        self.left = 0
        self.state = GameActive(self.level_creator.level)

    def set_screen(self, screen: Screen):
        self._screen = screen

    def get_screen(self):
        return self._screen

    def update(self, key):
        if self.state.__str__() == GameActive(self.level_creator.level).__str__():
            self.level_creator.level.update(key)


    def on_key_down(self, key, keys):
        if key == keys.B:
            if not self._backpack.isOpened:
                self.state = GamePaused(self.level_creator.level)
                self._backpack.show_backpack()
                return

        if self._backpack.isOpened:
            if key == keys.B:
                self._backpack.hide_backpack()
                self.state = GameActive(self.level_creator.level)
            if key == keys.DOWN:
                self._backpack.next_position()
            if key == keys.UP:
                self._backpack.previous_position()
            if key == keys.RETURN:
                self._backpack.use_item()
            return

        # LEVEL Movement
        if key == keys.A:
            if self.level_creator.go_left():
                print("Going left")
        elif key == keys.D:
            if self.level_creator.go_right():
                print("Going right")
        elif key == keys.W:
            if self.level_creator.go_up():
                print("Going up")
        elif key == keys.S:
            if self.level_creator.go_down():
                print("Going down")

        # TODO testing -------------------------------
        if key == keys.B:
            self._backpack.add_item(Item(name="Showel", actor=Actor("showel")))

        if key == keys.Q:
            self.level_creator.level.add_to_items_added(Cherry(Actor("cherry")), 50, 50)

        # TODO testing -------------------------------

    def draw(self):
        self._screen.clear()

        view_offset_x = 0
        view_offset_y = 0

        # draw info panel
        self.hud.draw(self._screen, self.level_creator.level.__str__())

        # drawing level
        self.level_creator.level.draw()

        # Drawing backpack when the backpack is opened
        if self._backpack.isOpened:
            self._backpack.draw_backpack(self._screen)

        # Drawing dialogs
        for dialog in self.dialogs:
            Dialog.draw_dialog(screen=self._screen, lines=dialog.lines, width=dialog.width, color=dialog.color)








