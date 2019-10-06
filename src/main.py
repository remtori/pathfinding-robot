import pyglet
from pyglet.gl import *
from pyglet import graphics

window = pyglet.window.Window(800, 600)

def line(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2

    graphics.draw(
        2, GL_LINES,
        ('v2i', ( x1, y1, x2, y2 )),
        ('c3B', (0, 0, 0, 0, 0, 0))
    )

@window.event
def on_draw():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    graphics.draw(
        3, GL_TRIANGLES,
        ('v2i', ( 50, 50, 550, 50, 300, 300)),
        ('c3B', (255, 0, 0, 0, 255, 0, 0, 0, 255))
    )
    
    for i in range(0, 400, 50):
        line((0, i), (400, i))
        line((i, 0), (i, 400))

pyglet.app.run()