import pyglet

from .physics import Circle


TEXTURE_PLAYER = pyglet.resource.texture('char.gif')


class Actor:

    _x = 0
    _y = 0
    _batch = pyglet.graphics.Batch()
    _sprite = None
    physics_shape = None

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        if self._sprite:
            self._sprite.x = self._x
        if self.physics_shape:
            self.physics_shape.x = self._x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        if self._sprite:
            self._sprite.y = self._y
        if self.physics_shape:
            self.physics_shape.y = self._y

    def on_draw(self):
        self._batch.draw()

    def on_update(self, dt):
        raise NotImplementedError()


class Player(Actor):

    VELOCITY = 200

    left_move = 0
    right_move = 0
    up_move = 0
    down_move = 0

    def __init__(self):
        self.physics_shape = Circle(24)
        #_img.anchor_x = 24
        #_img.anchor_y = 24
        self._sprite = pyglet.sprite.Sprite(
            img=TEXTURE_PLAYER,
            batch=self._batch
        )
        self.x = 150
        self.y = 150



    def look_at(self, x, y):
        pass
        """
        dx = x - self.x
        dy = y - self.y

        radians = math.atan2(dy, dx)
        self._sprite.rotation = -radians * (180 / math.pi)
        """

    def on_update(self, dt):
        # update position if we are moving
        self.x += ((self.left_move + self.right_move) * self.VELOCITY) * dt
        self.y += ((self.up_move + self.down_move) * self.VELOCITY) * dt
