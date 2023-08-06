
class LevelChain:
    level = None
    # MAP rotated + 90 degrees
    #               BASE                    1st floor                       2nd floor
    # level_chain = [[None,                   "castle_treasure",              "castle_roof"],
    #                [None,                   "castle_entry",                 "castle_key"],
    #                [None,                   "green_goblin",                 None],
    #                [None,                   "pink_statue",                  None],
    #                [None,                   "main_level",                   None],
    #                ["cave",                 "golden_lion",                  None],
    #                ["side_walk",            "clouds",                       None],
    #                ["boat_passage",         "cherry_in_clouds",             "heaven"],
    #                ["green_wizard",         "black_sky",                    "heaven_clouds"],
    #                ["pink_mouse",           "pink_bottle",                  "upper_stairs"],
    #                ["dungeon_pond",         "clouds_to_the_dungeon",        None],
    #                ["dungeon_entry",        "cloud_above_dungeons_entry",   None],
    #                ["dungeon_green_shield", "dungeon_dizzy",                None],
    #                [None,                   "dungeon_red_floor",            "dungeon_bedroom"]]

    def __init__(self, level_chain, initial_position: tuple = (0, 0)):
        self.level_position = initial_position
        if not level_chain:
            raise Exception("LevelCreator must have minimum of 1 level...")
        self.level_chain = level_chain
        self.set_new_level(self.level_position)

    def set_new_level(self, new_position: tuple):
        """
        Sets a new level based on position
        :param new_position: new level position
        :return: True if there is a level at that position otherwise false
        """
        if new_position[0] < 0 or new_position[1] < 0:
            return False
        try:
            level = self.level_chain[new_position[0]][new_position[1]]
        except IndexError:
            return False
        if level:
            self.level = level
            self.level_position = new_position
            return True
        return False

    def go_up(self):
        """
        Going to level at right on the map
        :return: True if there is a level otherwise False
        """
        new_position: tuple = self.level_position[0] + 1, self.level_position[1]
        return self.set_new_level(new_position)


    def go_down(self):
        """
        Going to level at left on the map
        :return: True if there is a level otherwise False
        """
        new_position: tuple = self.level_position[0] - 1, self.level_position[1]
        return self.set_new_level(new_position)

    def go_right(self):
        """
        Going to level at up on the map
        :return: True if there is a level otherwise False
        """
        new_position: tuple = self.level_position[0], self.level_position[1] + 1
        return self.set_new_level(new_position)

    def go_left(self):
        """
        Going to level at down on the map
        :return: True if there is a level otherwise False
        """
        new_position: tuple = self.level_position[0], self.level_position[1] - 1
        return self.set_new_level(new_position)
