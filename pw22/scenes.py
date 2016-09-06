import pyglet
import logging

from .world import World
from .physics import PhysicsWorld
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
    _physics_world = None
    _player = None
    _camera = None

    def on_init(self):
        logging.info('Initializing GameScene')
        self._world = World()
        self._world.generate()

        self._physics_world = PhysicsWorld()

        self._player = Player()
        self._physics_world.register_shape(self._player.physics_shape)

        self._camera = self.Camera(self._scene_manager.window)
        self._camera.attach(self._player)

        self._actors.append(self._player)

    def on_draw(self):
        self._world.on_draw()

        for actor in self._actors:
            actor.on_draw()

        self._physics_world.on_draw()

    def on_update(self, dt):
        for actor in self._actors:
            actor.on_update(dt)
        self._camera.apply()

        self._physics_world.on_update(dt)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.A:
            self._player.left_move = -1
        elif symbol == pyglet.window.key.D:
            self._player.right_move = 1
        elif symbol == pyglet.window.key.W:
            self._player.up_move = 1
        elif symbol == pyglet.window.key.S:
            self._player.down_move = -1

    def on_key_release(self, symbol, modifiers):
        if symbol == pyglet.window.key.A:
            self._player.left_move = 0
        elif symbol == pyglet.window.key.D:
            self._player.right_move = 0
        elif symbol == pyglet.window.key.W:
            self._player.up_move = 0
        elif symbol == pyglet.window.key.S:
            self._player.down_move = 0

    def on_mouse_motion(self, x, y, dx, dy):
        self._player.look_at(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    class Camera:

        x = 0
        y = 0
        z = 0

        _attached_to = None

        def __init__(self, window):
            self._window = window

        def attach(self, obj):
            self._attached_to = obj

        def apply(self):
            pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
            pyglet.gl.glLoadIdentity()
            if self._attached_to:
                pyglet.gl.glTranslatef(
                    -(self._attached_to.x - self._window.width / 2),
                    -(self._attached_to.y - self._window.height / 2),
                    -self.z
                )
                return
            pyglet.gl.glTranslatef(-self.x, -self.y, -self.z)
