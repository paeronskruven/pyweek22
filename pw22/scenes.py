import pyglet

from .world import World
from .actors import Player


class SceneManager:

    _scenes = []

    def __init__(self, window):
        self.window = window

    def push(self, scene):
        try:
            self.window.pop_handlers()
        except AssertionError:
            pass

        self._push_handlers(scene)
        scene.scene_manager = self
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

    scene_manager = None

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
    _player = None

    def __init__(self):
        self._world = World()
        #self._world.generate()

        self._player = Player()

        self._actors.append(self._player)

    def on_draw(self):
        self._world.on_draw()

        for actor in self._actors:
            actor.on_draw()

    def on_update(self, dt):
        for actor in self._actors:
            actor.on_update(dt)

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass
