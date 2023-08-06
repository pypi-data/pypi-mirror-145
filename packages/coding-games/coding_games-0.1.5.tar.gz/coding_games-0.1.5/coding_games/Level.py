import pytmx
from pgzero import game

from coding_games.utils.ObjectCreator import Creator


class Level:
    map = None

    def __init__(self, name: str):
        self.load_level(name)
        self.items = Creator.create_items_from_map(self.map, self)
        self.actors = Creator.create_actors(self.map)

        self.name = name
        self.walls = Creator.create_walls(self.map)
        self.width = 32
        self.height = 24

    def load_level(self, name: str):
        self.map = pytmx.load_pygame("maps/{}.tmx".format(name))

    def get_map(self):
        return self.map

    def get_items(self):
        return self.items

    def get_actors(self):
        return self.actors

    def __str__(self):
        return self.name

    def get_walls(self):
        return self.walls

    def draw_background(self, ):
        y = 0
        for row in range(self.height):
            x = 0
            for col in range(0, self.width):
                image = self.map.get_tile_image(col, row, 0)
                if image is not None:
                    game.screen.blit(image,
                                      (x * self.map.tilewidth,
                                       y * self.map.tileheight,),)
                x += 1
            y += 1

    def draw_items(self,):
        for item in self.get_items():
            item.draw()

    def draw_actors(self,):
        for actor in self.get_actors():
            actor.draw()

    def draw(self):
        self.draw_background()
        self.draw_items()
        self.draw_actors()

    def update(self, key):
        for actor in self.actors:
            actor.update(key, self)
