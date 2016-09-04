import pyglet

window = pyglet.window.Window(width=1024, height=768, caption='The Nightmare')


@window.event
def on_draw():
    window.clear()


def on_update(dt):
    pass


def main():
    pyglet.clock.schedule_interval(on_update, 1 / 60)
    pyglet.app.run()
