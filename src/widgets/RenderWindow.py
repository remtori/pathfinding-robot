from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget

from controller import controller
from Map import WALL


class RenderWindow(QWidget):

    def __init__(self):
        super(RenderWindow, self).__init__()

        self.setWindowTitle("AI - Path Finding")
        self.setGeometry(50, 100, 960, 540)

        self.offsetX = 0
        self.offsetY = 0

        self.colors = {
            'WALL': QColor(145, 145, 145),
            'START': QColor(0, 255, 0),
            'TARGET': QColor(255, 0, 0),
            'PASSENGER': QColor(3, 252, 244),
            'OPEN': QColor("#4287f5"),
            'CLOSE': QColor("#02cf21")
        }

        self.painter = QPainter()
        self.show()

    def paintEvent(self, e):
        qp = self.painter
        qp.begin(self)

        m = controller.map
        gs = controller.gridSize
        h = (m.height + 1) * gs
        w = (m.width + 1) * gs

        c = self.colors['WALL']

        for x in range(m.width + 1):
            for y in range(m.height + 1):
                if m[x, y] == WALL:
                    qp.fillRect(
                        x * gs, y * gs,
                        gs, gs,
                        c
                    )

        openList, closeList = controller.getPfList()

        self.drawPoints(openList, 'OPEN')
        self.drawPoints(closeList, 'CLOSE')

        self.drawPoints([m.startPoint], 'START')
        self.drawPoints([m.targetPoint], 'TARGET')
        self.drawPoints(m.passPoint, 'PASSENGER')

        for x in range(0, w + 2, gs):
            qp.drawLine(x, 0, x, h)

        for y in range(0, h + 2, gs):
            qp.drawLine(0, y, w, y)

        qp.end()

    def drawPoints(self, points, color):
        gs = controller.gridSize
        c = self.colors[color]

        for p in points:
            self.painter.fillRect(
                p[0] * gs,
                p[1] * gs,
                gs, gs, c
            )
