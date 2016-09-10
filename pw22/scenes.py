import pyglet
import logging

from .world import World
from .physics import PhysicsSimulation
from .actors import Player


class SceneManager:

    _scenes = []

    def __init__(self, window):
        logging.info('Initializing SceneManager')
        self.window = window

    def push(self, scene):
        logging.info('Pushing scene: {}'.format(scene))
        try:
            self.window.pop_handlers()
        except AssertionError:
            pass

        self._push_handlers(scene)
        self._scenes.append(scene)

    def pop(self):
        self.window.pop_handlers()
        self._scenes.pop()

        self._push_handlers(self._scenes[-1])

    def _push_handlers(self, scene):
        self.window.push_handlers(
            scene.on_key_press,
            scene.on_key_release,
            scene.on_mouse_motion,
            scene.on_mouse_release
        )

    def on_draw(self):
        self._scenes[-1].on_draw()

    def on_update(self, dt):
        self._scenes[-1].on_update(dt)


class Scene:
    """
    Base class for scenes
    """

    def __init__(self, scene_manager):
        self._scene_manager = scene_manager
        self.on_init()

    def on_init(self):
        raise NotImplementedError()

    def on_draw(self):
        raise NotImplementedError()

    def on_update(self, dt):
        raise NotImplementedError()

    def on_key_press(self, symbol, modifiers):
        raise NotImplementedError()

    def on_key_release(self, symbol, modifiers):
        raise NotImplementedError()

    def on_mouse_motion(self, x, y, dx, dy):
        raise NotImplementedError()

    def on_mouse_release(self, x, y, button, modifiers):
        raise NotImplementedError()


class MenuScene(Scene):
    pass  # todo: implement this


class GameScene(Scene):

    _actors = []
    _world = None
    _physics_simulation = None
    _player = None
    _camera = None

    def on_init(self):
        logging.info('Initializing GameScene')
        self._world = World()
        self._world.generate()

        self._player = Player()
        self._player.x = self._world.get_spawn_x()
        self._player.y = self._world.get_spawn_y()
        self._actors.append(self._player)

        self._physics_simulation = PhysicsSimulation()
        self._physics_simulation.register_world(self._world)
        self._physics_simulation.register_shape(self._player.get_shape())

    def on_draw(self):
        # center view on players position
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glTranslatef(
            -int(self._player.x - self._scene_manager.window.width / 2),
            -int(self._player.y - self._scene_manager.window.height / 2),
            -1
        )

        self._world.on_draw()
        for actor in self._actors:
            actor.on_draw()

        self._physics_simulation.on_draw()  # only to debug physics shapes

    def on_update(self, dt):
        for actor in self._actors:
            actor.on_update(dt)

        self._physics_simulation.on_update()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.A:
            self._player.should_move_left = -1
        elif symbol == pyglet.window.key.D:
            self._player.should_move_right = 1
        elif symbol == pyglet.window.key.W:
            self._player.should_move_up = 1
        elif symbol == pyglet.window.key.S:
            self._player.should_move_down = -1

    def on_key_release(self, symbol, modifiers):
        if symbol == pyglet.window.key.A:
            self._player.should_move_left = 0
        elif symbol == pyglet.window.key.D:
            self._player.should_move_right = 0
        elif symbol == pyglet.window.key.W:
            self._player.should_move_up = 0
        elif symbol == pyglet.window.key.S:
            self._player.should_move_down = 0

    def on_mouse_motion(self, x, y, dx, dy):
        self._player.look_at(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        pass
