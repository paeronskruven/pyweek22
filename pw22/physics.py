import pyglet
import math
import logging

from .world import TILE_SIZE, TILE_WALL

class PhysicsSimulation:

    _shapes = []
    _world = None
    _batch = pyglet.graphics.Batch()

    def __init__(self):
        logging.info('Initializing PhysicsWorld')
        pass

    def register_shape(self, shape):
        self._shapes.append(shape)

    def register_world(self, world):
        self._world = PhysicsWorld(world)

    def on_update(self):
        # check all shapes against the world
        for shape in self._shapes:
            self._world.collide(shape)

    def on_draw(self):
        for shape in self._shapes:
            shape.debug_draw()


class PhysicsWorld:

    def __init__(self, world):
        self._world = world
        self._tiles = self._world.get_tiles()

    def collide(self, obj):
        """
        Crappy collision code begins here
        :param obj: circle shape to try collision against
        """
        ix = int(obj.x / TILE_SIZE)
        iy = int(obj.y / TILE_SIZE)

        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                tx = ix + x
                ty = iy + y
                tile = self._tiles[ty][tx]
                if tile == TILE_WALL:
                    nx = max(tx * TILE_SIZE, min(obj.x, (tx * TILE_SIZE) + TILE_SIZE))
                    ny = max(ty * TILE_SIZE, min(obj.y, (ty * TILE_SIZE) + TILE_SIZE))
                    dx = obj.x - nx
                    dy = obj.y - ny
                    if (math.pow(dx, 2) + math.pow(dy, 2)) < math.pow(obj.radius, 2):
                        data = {}
                        if obj.x < tx * TILE_SIZE and not self._tiles[ty][tx - 1] == TILE_WALL:
                            data['left'] = True
                        elif obj.x > (tx * TILE_SIZE) + TILE_SIZE and not self._tiles[ty][tx + 1] == TILE_WALL:
                            data['right'] = True
                        if obj.y < ty * TILE_SIZE and not self._tiles[ty - 1][tx] == TILE_WALL:
                            data['bottom'] = True
                        elif obj.y > (ty * TILE_SIZE) + TILE_SIZE and not self._tiles[ty + 1][tx] == TILE_WALL:
                            data['top'] = True
                        obj.callback(**data)


class PhysicsShape:

    x = 0
    y = 0
    _callback = None

    def set_callback(self, func):
        self._callback = func

    def callback(self, **kwargs):
        if self._callback:
            self._callback(**kwargs)

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
