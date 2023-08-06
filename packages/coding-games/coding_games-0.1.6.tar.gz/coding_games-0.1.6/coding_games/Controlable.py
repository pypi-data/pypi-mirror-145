from pgzero.actor import Actor
from coding_games.Direction import Direction


class Controlable(Actor):
    def __init__(self, image, gravity=False, *args, **kwargs):
        super().__init__(image, **kwargs)
        self.gravity = gravity
        self.jump_progress = 0
        self.jump_direction: Direction = None
        self.is_falling = False

    def can_move(self, walls, direction):
        walls_on_actor_level = list(filter(lambda w: (w.y < self.y < (w.y + w.height)), walls))
        if len(walls_on_actor_level) == 0:
            return True
        if direction == Direction.right:
            pos_x, pos_y = self.midright
            for wall in walls_on_actor_level:
                if round(pos_x + 1) == (wall.x + wall.width):
                    return False
        elif direction == Direction.left:
            pos_x, pos_y = self.midleft
            for wall in walls_on_actor_level:
                if round(pos_x - 1) == (wall.x + wall.width):
                    return False
        return True

    def calculate_y_position(self, walls):
        x, y = self.midbottom
        walls_bellow_actor = list(filter(lambda w: ((w.left <= x <= w.right) and (w.y >= y)), walls))
        if len(walls_bellow_actor) == 0:
            return -1
        else:
            y_position = walls_bellow_actor[0].y
            for wall in walls_bellow_actor:
                if wall.y < y_position:
                    y_position = wall.y
            y_position -= 1
        return y_position

    def jump(self, fixed_y, walls, direction=Direction.up):
        x, y = self.midbottom
        if self.jump_direction is None:
            self.jump_direction = direction
        if self.jump_direction == Direction.up:
            self.y -= 2
            self.jump_progress += 1
            if self.jump_progress == 50:
                self.jump_direction = Direction.down
        elif self.jump_direction == Direction.up_right:
            self.y -= 2
            self.jump_progress += 1
            if self.can_move(walls=walls, direction=Direction.right):
                self.x += 1
            if self.jump_progress == 50:
                self.jump_direction = Direction.down_right
        elif self.jump_direction == Direction.up_left:
            self.y -= 2
            self.jump_progress += 1
            if self.can_move(walls=walls, direction=Direction.left):
                self.x -= 1
            if self.jump_progress == 50:
                self.jump_direction = Direction.down_left
        elif self.jump_direction == Direction.down:
            if (fixed_y is not None and fixed_y > (y + 1)) or (fixed_y is None):
                self.y += 2
                self.jump_progress -= 1
            elif fixed_y <= y:
                self.jump_progress = 0
                self.jump_direction = None
            if self.jump_progress == 0:
                self.jump_direction = None
        elif self.jump_direction == Direction.down_right:
            if (fixed_y is not None and fixed_y > (y + 1)) or (fixed_y is None):
                self.y += 2
                self.jump_progress -= 1
                if self.can_move(walls=walls, direction=Direction.right):
                    self.x += 1
            elif fixed_y <= y:
                self.jump_progress = 0
                self.jump_direction = None
            if self.jump_progress == 0:
                self.jump_direction = None
        elif self.jump_direction == Direction.down_left:
            if (fixed_y is not None and fixed_y > (y + 1)) or (fixed_y is None):
                self.y += 2
                self.jump_progress -= 1
                if self.can_move(walls=walls, direction=Direction.left):
                    self.x -= 1
            elif fixed_y <= y:
                self.jump_progress = 0
                self.jump_direction = None
            if self.jump_progress == 0:
                self.jump_direction = None

    def move(self, direction: Direction, key, world):
        walls = world.get_walls()
        apply_gravity = False
        new_y_position = None
        x, y = self.midbottom
        if self.gravity:
            new_y_position = self.calculate_y_position(walls)
            if new_y_position == -1:
                apply_gravity = True
                self.is_falling = True
            elif (new_y_position is not None) and (new_y_position > y):
                apply_gravity = True
                if new_y_position > (33 + y):
                    self.is_falling = True
            else:
                self.is_falling = False
                apply_gravity = False
        if self.jump_direction is not None:
            self.jump(new_y_position, walls=walls)
        elif self.is_falling:
            self.y += 1
        elif direction is not None and self.can_move(walls=walls, direction=direction) and self.jump_direction is None:
            if direction == Direction.right:
                self.x += 1
                if apply_gravity:
                    self.y += 1
            elif direction == Direction.left:
                self.x -= 1
                if apply_gravity:
                    self.y += 1
            elif direction == Direction.up:
                self.jump(new_y_position, walls=walls, direction=direction)
            elif Direction == Direction.down:
                self.y += 1
            elif direction == Direction.up_right:
                self.jump(new_y_position, direction=direction, walls=walls)
            elif direction == Direction.up_left:
                self.jump(new_y_position, direction=direction, walls=walls)
            self.state.update(key, world)
        elif direction is None and self.jump_direction is None:
            self.state.update(key, world)

    def grabItem(self, items: list):
        return self.colliding_items(items).pop()


