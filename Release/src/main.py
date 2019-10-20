import sys
from PyQt5.QtWidgets import QApplication

from widgets.ControllerWindow import ControllerWindow
from widgets.RenderWindow import RenderWindow
from controller import controller


if __name__ == '__main__':

    app = QApplication([])

    controller.winController = ControllerWindow()
    controller.winRenderer = RenderWindow()

    sys.exit(app.exec_())
