from pgzero.actor import Actor
from pgzero import game
from time import time
from coding_games import ActorState
from coding_games.State import State

WIDTH = 800


class AnimatedActor(Actor):
    def __init__(self, *args, name: str, sprite: tuple,  state: State = State(), pingpong=False, duration=100, **kwargs):
        super().__init__(*args, **kwargs)
        self.pingpong = pingpong
        self.duration = duration
        self._stopped = False

        self.height = sprite[1]
        self.width = sprite[0]

        self._name = name
        self._state = state

        # prepare frames
        self._frames = []
        for x_offset in range(int(self._orig_surf.get_width() / self.width)):
            surface = self._orig_surf.subsurface((x_offset * self.width, 0, self.width, self.height))
            self._frames.append(surface)

        # frame config
        self._current_frame = 0
        self.frame_duration = self.duration / len(self._frames)
        self.last_frame_update = time() * 1000
        self._next_frame_dx = 1

    def start(self):
        self._stopped = False

    def stop(self):
        self._stopped = True

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state: ActorState):
        if self._state.name != state.name:
            self._state = state
            self.set_image(state.image, dimension=(self.width, self.height))

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def frames(self):
        return self._frames

    @property
    def current_frame(self):
        return self._current_frame

    @current_frame.setter
    def current_frame(self, index):
        if 0 < index < len(self._frames) - 1:
            raise Exception("Frame index out of range.")
        self._current_frame = index

    def _update_frame(self):
        if not self._stopped:
            now = time() * 1000
            if now - self.last_frame_update > self.frame_duration:
                self.last_frame_update = now
                self._current_frame += self._next_frame_dx

                if self.pingpong:
                    if self._next_frame_dx == 1 and self._current_frame >= len(
                            self._frames) - 1 or self._next_frame_dx == -1 and self._current_frame <= 0:
                        self._next_frame_dx *= -1
                else:
                    if self._current_frame == len(self._frames):
                        self._current_frame = 0

    def set_image(self, image, dimension):
        px, py = self.pos
        tx, ty = self.topleft
        self.image = image
        self.height = dimension[1]
        self.width = dimension[0]
        self._frames = []

        # self._init_position(pos=None, anchor=self.anchor, sprite=dimension)

        # counting that sprites will be same size
        self.pos = (px, py)
        self.topleft = (tx, ty)

        for x_offset in range(int(self._orig_surf.get_width() / self.width)):
            surface = self._orig_surf.subsurface(
                (x_offset * self.width, 0, self.width, self.height))
            self._frames.append(surface)

        # frame config
        self._current_frame = 0
        self.frame_duration = self.duration / len(self._frames)
        self.last_frame_update = time() * 1000
        self._next_frame_dx = 1
        # return self._current_frame

    def draw(self):
        self._update_frame()
        game.screen.blit(self._frames[self._current_frame], self.topleft)

    def colliding_actors(self, actors) -> list:
        x, y = self.center
        actors_in_collision = list(filter(lambda i: ((((i.left <= x <= i.right) and (i.top <= y >= i.bottom)) or (
                (self.left <= i.center[0] <= self.right) and (self.top <= i.center[1] <= self.bottom))) and (
                                                             i.name != self.name)), actors))
        return actors_in_collision

    def colliding_items(self, items) -> list:
        x, y = self.center
        items_in_collision = list(filter(lambda i: ((((i.left <= x <= i.right) and (i.top <= y >= i.bottom)) or (
                (self.left <= i.center[0] <= self.right) and (self.top <= i.center[1] <= self.bottom))) and (
                                                             i.name != self.name)), items))
        return items_in_collision
