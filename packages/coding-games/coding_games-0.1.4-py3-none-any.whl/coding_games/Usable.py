from coding_games import Item, State


class UsableItem(Item):
    def __init__(self, image, name, dimensions, *args, **kwargs):
        super().__init__(image=image, name=name, dimensions=dimensions,
                         state=State())

    def can_be_used(self, items: list):
        return False

    def use(self, items: list):
        # after using item, remove it from the world
        items.remove(self)

