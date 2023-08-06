from pgzero.screen import Screen

from coding_games.Dialog import Dialog


class Backpack:
    items = []
    isOpened = False
    _internal_position = 0
    itemPosition = 0
    max_items = 5

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.items)

    def __next__(self):
        """
        :return: Returns the next item in backpack
        """
        while self._internal_position < len(self.items):
            item = self.items[self._internal_position]
            self._internal_position += 1
            return item
        raise StopIteration

    def add_item(self, item):
        """
        Adding items to backpack
        :param item: Item to add to backpack
        """
        if len(self) < self.max_items:
            self.items.append(item)
        else:
            raise Exception("Could not add item, backpack is full")

    def remove_item(self, item):
        """
        Removing item from a game backpack
        :param item: Item to be removed
        """
        try:
            self.items.remove(item)
        except IndexError:
            print("Nothing in backpack")

    def use_item(self):
        """
        Using item from backpack, and then the item is removed from backpack and returned
        """
        try:
            item = self.items[self.itemPosition]
            self.remove_item(item)
            self.hide_backpack()
            item.use_item()
            return item
        except IndexError:
            print("Nothing in backpack")

    def next_position(self):
        """
        Moving active position in drawing dialog forward
        """
        if self.itemPosition == len(self.items) - 1:
            return
        self.itemPosition += 1

    def previous_position(self):
        """
        Moving active position in drawing dialog backward
        """
        if self.itemPosition == 0:
            return
        self.itemPosition -= 1

    def show_backpack(self):
        """
        Opening a backpack
        """
        self.itemPosition = 0
        self.isOpened = True

    def hide_backpack(self):
        """
        Hiding backpack
        """
        self.isOpened = False

    def draw_backpack(self, screen: Screen):
        """
        Drawing a backpack, backpack is displayed as a dialog
        :param screen: screen to be displayed
        """
        if self.isOpened:
            if len(self.items) == 0:
                Dialog.draw_dialog(["Empty"], screen)
            else:
                Dialog.draw_dialog(self.items, screen, active_position=self.itemPosition)




