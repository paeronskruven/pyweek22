import pyglet


class Actor:

    _batch = pyglet.graphics.Batch()

    def on_draw(self):
        self._batch.draw()

    def on_update(self, dt):
        raise NotImplementedError()


class Player(Actor):

    VELOCITY = 100
    _x = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._sprite.x = self._x

    def __init__(self):
        self._sprite = pyglet.sprite.Sprite(
            x=150,
            y=150,
            img=pyglet.image.SolidColorImagePattern(color=(120, 120, 255, 255)).create_image(64, 64),
            batch=self._batch
        )

    def on_update(self, dt):
        pass
