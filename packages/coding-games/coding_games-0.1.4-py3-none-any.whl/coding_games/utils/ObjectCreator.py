import pygame

from coding_games.Item import Item
from coding_games.DizzyActor import DizzyActor
from coding_games.Flare import Flare

from coding_games.items.Wall import Wall


def item_factory(name: str):
    return {
        'Flare': Flare()
    }.get(name, None)


class Creator:
    @staticmethod
    def create_items_from_map(level_map, level):
        """
        Creating items that are stored in the level map
        :param level_map: Map of the level
        :return: Items created
        """
        # TODO This is just messed up... but it works somehow, try different solution next..
        def use_function():
            level.items.append(item_as_actor)
            item_as_actor.pos = level.actors[0].pos

        items = []
        for item in level_map.get_layer_by_name("items"):
            item_as_actor = item_factory(item.name)
            if item_as_actor is None:
                item_as_actor = Item(item.name, (32, 32), name=item.name)
                item_as_actor.use_item = use_function
            item_as_actor._surf = pygame.transform.scale(item_as_actor._surf, (item.width, item.height))

            pos = (item.x + item_as_actor.width / 2, item.y + item_as_actor.height / 2)
            item_as_actor.pos = pos

            items.append(item_as_actor)

        return items

    @staticmethod
    def create_actors(level_map):
        actors = []
        for actor in level_map.get_layer_by_name("actors"):
            if actor.name == "Dizzy":
                pos = (actor.x + actor.width / 2, actor.y + actor.height / 2)
                dizzy = DizzyActor()
                dizzy.pos = pos
                actors.append(dizzy)

        return actors

    @staticmethod
    def create_walls(level_map):
        walls = []
        map_walls = level_map.get_layer_by_name("walls")
        for wall in map_walls.tiles():
            x, y, data = wall
            if data != 0:
                width = 32
                height = 32
                new_wall = Wall(x * width, y * height, width, height)
                walls.append(new_wall)
        return walls
