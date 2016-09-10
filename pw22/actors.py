import pyglet

from .physics import Circle


TEXTURE_PLAYER = pyglet.resource.texture('char.png')
TEXTURE_PLAYER.anchor_x = TEXTURE_PLAYER.width / 2
TEXTURE_PLAYER.anchor_y = TEXTURE_PLAYER.height / 2


class Actor:
    """
    Base class for all actors
    """

    _x = 0
    _y = 0
    _last_x = 0
    _last_y = 0
    _batch = pyglet.graphics.Batch()
    _sprite = None
    _physics_shape = None

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._last_x = self._x
        self._x = value
        if self._sprite:
            self._sprite.x = self._x
        if self._physics_shape:
            self._physics_shape.x = self._x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._last_y = self._y
        self._y = value
        if self._sprite:
            self._sprite.y = self._y
        if self._physics_shape:
            self._physics_shape.y = self._y

    def get_shape(self):
        return self._physics_shape

    def on_draw(self):
        self._batch.draw()

    def on_update(self, dt):
        raise NotImplementedError()


class Player(Actor):

    VELOCITY = 200

    should_move_left = False
    should_move_right = False
    should_move_up = False
    should_move_down = False

    left_move = 0
    right_move = 0
    up_move = 0
    down_move = 0

    def __init__(self):
        self._physics_shape = Circle(TEXTURE_PLAYER.width / 2)
        self._physics_shape.set_callback(self._collision_callback)
        self._sprite = pyglet.sprite.Sprite(
            img=TEXTURE_PLAYER,
            batch=self._batch
        )

    def _collision_callback(self, **kwargs):
        x = self._x
        y = self._y

        if kwargs.get('left') or kwargs.get('right'):
            x = self._last_x
        if kwargs.get('top') or kwargs.get('bottom'):
            y = self._last_y

        self.x = x
        self.y = y

    def look_at(self, x, y):
        pass
        """
        dx = x - self.x
        dy = y - self.y

        radians = math.atan2(dy, dx)
        self._sprite.rotation = -radians * (180 / math.pi)
        """

    def on_update(self, dt):
        force_x = 0
        force_y = 0

        if self.should_move_left:
            force_x -= 1
        if self.should_move_right:
            force_x += 1
        if self.should_move_up:
            force_y += 1
        if self.should_move_down:
            force_y -= 1

        # update position if we are moving
        self.x += int((force_x * self.VELOCITY) * dt)
        self.y += int((force_y * self.VELOCITY) * dt)
