import pyglet
import logging

logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s %(message)s', level=logging.DEBUG)

# setup resource paths before importing any game code
pyglet.resource.path = ['data', 'data/tiles']
pyglet.resource.reindex()

from .scenes import SceneManager, GameScene

window = pyglet.window.Window(width=1024, height=768, caption='The Nightmare')

scene_manager = SceneManager(window)
scene_manager.push(GameScene(scene_manager))

clock_display = pyglet.clock.ClockDisplay()

pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)


@window.event
def on_draw():
    window.clear()

    try:
        scene_manager.on_draw()
    except IndexError:
        pyglet.app.exit()

    pyglet.gl.glLoadIdentity()
    clock_display.draw()


def on_update(dt):
    try:
        scene_manager.on_update(dt)
    except IndexError:
        pyglet.app.exit()


def main():
    pyglet.clock.schedule(on_update)
    pyglet.app.run()
