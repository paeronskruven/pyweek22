import pyglet
import math
import logging


class PhysicsWorld:

    _shapes = []
    _batch = pyglet.graphics.Batch()

    def __init__(self):
        logging.info('Initializing PhysicsWorld')
        pass

    def register_shape(self, shape):
        self._shapes.append(shape)

    def on_update(self, dt):
        pass

    def on_draw(self):
        for shape in self._shapes:
            shape.debug_draw()


class PhysicsShape:

    x = 0
    y = 0

    def debug_draw(self):
        raise NotImplementedError()


class Rectangle(PhysicsShape):

    def __init__(self):
        pass

    def debug_draw(self):
        pass


class Circle(PhysicsShape):

    def __init__(self, radius):
        self.radius = radius

    def debug_draw(self):
        vertices = []
        for i in range(0, 20):
            theta = 2.0 * math.pi * i / 20
            x = self.x + (self.radius * math.cos(theta))
            y = self.y + (self.radius * math.sin(theta))

            vertices.append(x)
            vertices.append(y)

        pyglet.graphics.draw(
            int(len(vertices) / 2),
            pyglet.gl.GL_TRIANGLE_FAN,
            ('v2f', tuple(vertices)),
            ('c4B', (100, 100, 255, 150) * int(len(vertices) / 2))
        )
