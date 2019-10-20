from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

import math

from controller import controller
from Map import WALL


class RenderWindow(QWidget):

    def __init__(self):
        super(RenderWindow, self).__init__()

        self.setWindowTitle("AI - Path Finding")
        self.setGeometry(50, 100, 960, 540)

        self.screenOffsetX = 0
        self.screenOffsetY = 0
        self.viewPort = 0, 0, 960, 540
        self.scale = 1.0

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

    def updateViewPort(self):
        lX, lY = self.screenToWorld(0, 0)
        hX, hY = self.screenToWorld(self.width(), self.height())
        self.viewPort = int(lX), int(lY), int(hX), int(hY)

    def paintEvent(self, e):
        self.updateViewPort()
        qp = self.painter
        qp.begin(self)

        lX, lY, hX, hY = self.viewPort
        m = controller.map
        gs = controller.gridSize
        w = (m.width + 1) * gs
        h = (m.height + 1) * gs

        c = self.colors['WALL']

        for x in range(
            max(0, lX // gs - 2),
            min(m.width + 1, hX // gs + 2)
        ):
            for y in range(
                max(0, lY // gs - 2),
                min(m.height + 1, hY // gs + 2)
            ):
                if m[x, y] == WALL:
                    self.qpFillRect(
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

        for x in range(
            max(0, lX - lX % gs),
            min(w + 2, hX),
            gs
        ):
            self.qpDrawLine(x, 0, x, h)

        for y in range(
            max(0, lY - lY % gs),
            min(h + 2, hY),
            gs
        ):
            self.qpDrawLine(0, y, w, y)

        self.drawPath(controller.getPfPaths())

        qp.end()

    def drawPoints(self, points, color):
        gs = controller.gridSize
        c = self.colors[color]

        lX, lY, hX, hY = self.viewPort

        for x, y in points:
            pX = x * gs
            pY = y * gs
            if lX - gs <= pX <= hX + gs and lY - gs <= pY <= hY + gs:
                self.qpFillRect(
                    pX, pY,
                    gs, gs, c
                )

    def drawPath(self, paths):

        pen = QPen(QColor('#000000'))
        pen.setStyle(Qt.DashLine)
        pen.setDashPattern([10, 4])

        self.painter.setPen(pen)

        gs = controller.gridSize

        for path in paths:
            for i in range(len(path) - 1):
                a = path[i]
                b = path[i + 1]
                vx, vy = b[0] - a[0], b[1] - a[1]
                d = math.sqrt(vx * vx + vy * vy)

                # Chuyển về vector đơn vị
                vx = vx / d
                vy = vy / d
                # Xoay 90 độ
                vx, vy = -vy, vx

                vx = vx * 2 + gs / 2
                vy = vy * 2 + gs / 2

                self.qpDrawLine(
                    a[0] * gs + vx, a[1] * gs + vy,
                    b[0] * gs + vx, b[1] * gs + vy
                )

        self.painter.setPen(Qt.SolidLine)

    # Event Handler
    def mouseMoveEvent(self, event):
        self.screenOffsetX = self.storedOX + (self.mouseDownX - event.x()) / self.scale
        self.screenOffsetY = self.storedOY + (self.mouseDownY - event.y()) / self.scale

        event.accept()
        self.update()

    def mousePressEvent(self, event):

        self.mouseDownX = event.x()
        self.mouseDownY = event.y()
        self.storedOX = self.screenOffsetX
        self.storedOY = self.screenOffsetY

        event.accept()

    def wheelEvent(self, event):

        mouseBeforeX, mouseBeforeY = self.screenToWorld(event.x(), event.y())

        if event.angleDelta().y() > 0:
            self.scale *= 1.05
        else:
            self.scale *= 0.95

        mouseAfterX, mouseAfterY = self.screenToWorld(event.x(), event.y())
        self.screenOffsetX += (mouseBeforeX - mouseAfterX)
        self.screenOffsetY += (mouseBeforeY - mouseAfterY)

        event.accept()
        self.update()

    # World to Screen transform
    def worldToScreen(self, x, y):
        rX = (x - self.screenOffsetX) * self.scale
        rY = (y - self.screenOffsetY) * self.scale
        return rX, rY

    def screenToWorld(self, x, y):
        rX = (x / self.scale) + self.screenOffsetX
        rY = (y / self.scale) + self.screenOffsetY
        return rX, rY

    def qpFillRect(self, x, y, w, h, c):
        p = self.worldToScreen(x, y)
        w, h = w * self.scale, h * self.scale

        self.painter.fillRect(*p, w, h, c)

    def qpDrawLine(self, x1, y1, x2, y2):
        p1 = self.worldToScreen(x1, y1)
        p2 = self.worldToScreen(x2, y2)

        self.painter.drawLine(*p1, *p2)
