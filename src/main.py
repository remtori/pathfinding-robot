import sys
from PyQt5.QtWidgets import QApplication

from widgets.ControllerWindow import ControllerWindow


if __name__ == '__main__':

    app = QApplication([])
    window = ControllerWindow()
    window.show()
    sys.exit(app.exec_())
