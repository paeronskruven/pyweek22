import pyglet
import logging

from .scenes import SceneManager, GameScene

logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s %(message)s', level=logging.DEBUG)

window = pyglet.window.Window(width=1024, height=768, caption='The Nightmare')
scene_manager = SceneManager(window)

scene_manager.push(GameScene())

clock_display = pyglet.clock.ClockDisplay()


@window.event
def on_draw():
    window.clear()

    try:
        scene_manager.on_draw()
    except IndexError:
        pyglet.app.exit()

    clock_display.draw()


def on_update(dt):
    try:
        scene_manager.on_update(dt)
    except IndexError:
        pyglet.app.exit()


def main():
    pyglet.clock.schedule_interval(on_update, 1 / 60)
    pyglet.app.run()
