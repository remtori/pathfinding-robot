from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget

from store import state
from Map import AIR


class RenderWindow(QWidget):

    def __init__(self):
        super(RenderWindow, self).__init__()

        self.setWindowTitle("AI - Path Finding")
        self.setGeometry(50, 100, 960, 540)

        self.offsetX = 0
        self.offsetY = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.mapDataToColor = [
            None,
            QColor(145, 145, 145),
            QColor(0, 255, 0),
            QColor(255, 0, 0),
            QColor(3, 252, 244),
            QColor("#afeeee"),
            QColor("#98fb98")
        ]
        self.painter = QPainter()
        self.show()

    def paintEvent(self, e):
        qp = self.painter
        qp.begin(self)

        gs = state.gridSize
        h = (state.map.height + 1) * gs
        w = (state.map.width + 1) * gs

        for x in range(state.map.width + 1):
            for y in range(state.map.height + 1):
                if state.map[x, y] != AIR:
                    qp.fillRect(
                        x * gs, y * gs,
                        gs, gs,
                        self.mapDataToColor[state.map[x, y]]
                    )

        for x in range(0, w + 2, gs):
            qp.drawLine(x, 0, x, h)

        for y in range(0, h + 2, gs):
            qp.drawLine(0, y, w, y)

        qp.end()
        self.timer.start(100)
