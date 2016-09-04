import pyglet

from .world import World


class SceneManager:

    _scenes = []

    def __init__(self, window):
        self.window = window

    def push(self, scene):
        scene.scene_manager = self
        self._scenes.append(scene)

    def pop(self):
        self._scenes.pop()

    def on_draw(self):
        self._scenes[-1].on_draw()

    def on_update(self, dt):
        self._scenes[-1].on_update(dt)


class Scene:

    scene_manager = None

    def on_draw(self):
        raise NotImplementedError()

    def on_update(self, dt):
        raise NotImplementedError()


class MenuScene(Scene):
    pass  # todo: implement this


class GameScene(Scene):

    def __init__(self):
        self._world = World()
        self._world.generate()

    def on_draw(self):
        self._world.on_draw()

    def on_update(self, dt):
        pass
