from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QIcon
from PyQt5.QtWidgets import (
    QComboBox,
    QLabel,
    QToolButton,
    QHBoxLayout,
    QPushButton,
    QFormLayout,
    QLineEdit,
    QFrame,
    QFileDialog,
    QWidget
)

from .RenderWindow import RenderWindow
from store import state


class ControllerWindow(QWidget):

    def __init__(self):
        super(ControllerWindow, self).__init__()

        self.setWindowTitle("Controller")
        self.setGeometry(1060, 100, 240, 540)

        self.initUI()

    def initUI(self):

        self.renderWin = RenderWindow()

        self.wHLayoutWidget = QWidget(self)
        self.wHLayoutWidget.setGeometry(0, 0, 240, 50)
        self.wHLayout = QHBoxLayout(self.wHLayoutWidget)
        self.wHLayout.setContentsMargins(5, 5, 5, 5)

        self.btnStepBackward = QToolButton(self.wHLayoutWidget)
        self.btnStepBackward.setIcon(QIcon("./assets/icons/step-backward.svg"))
        self.btnStepBackward.setToolTip("Quay lại bước trước")
        # self.btnStepBackward.clicked.connect(self.step_backward)
        self.wHLayout.addWidget(self.btnStepBackward)

        self.iconPlay = QIcon("./assets/icons/play.svg")
        self.iconPause = QIcon("./assets/icons/pause.svg")

        self.btnToggleRun = QToolButton(self.wHLayoutWidget)
        self.btnToggleRun.setIcon(self.iconPlay)
        self.btnToggleRun.setToolTip("Bắt đầu/Dừng quá trình tìm kiếm")
        self.btnToggleRun.clicked.connect(self.toggleRun)
        self.wHLayout.addWidget(self.btnToggleRun)

        self.btnStepForward = QToolButton(self.wHLayoutWidget)
        self.btnStepForward.setIcon(QIcon("./assets/icons/step-forward.svg"))
        self.btnStepForward.setToolTip("Bước tới một bước")
        # self.btnStepForward.clicked.connect(self.step_forward)
        self.wHLayout.addWidget(self.btnStepForward)

        self.btnReset = QToolButton(self.wHLayoutWidget)
        self.btnReset.setIcon(QIcon("./assets/icons/sync.svg"))
        self.btnReset.setToolTip("Khởi động lại quá trình tìm kiếm")
        # self.btnReset.clicked.connect(self.reset)
        self.wHLayout.addWidget(self.btnReset)

        self.btnStop = QToolButton(self.wHLayoutWidget)
        self.btnStop.setIcon(QIcon("./assets/icons/times.svg"))
        self.btnStop.setToolTip("Dừng chương trình")
        self.btnStop.clicked.connect(QCoreApplication.instance().quit)
        self.wHLayout.addWidget(self.btnStop)

        self.controlSeperator = QFrame(self)
        self.controlSeperator.setGeometry(0, 45, 240, 5)
        self.controlSeperator.setFrameShape(QFrame.HLine)
        self.controlSeperator.setFrameShadow(QFrame.Sunken)

        self.wFormLayoutWidget = QWidget(self)
        self.wFormLayoutWidget.setGeometry(0, 50, 240, 165)
        self.wFormLayout = QFormLayout(self.wFormLayoutWidget)
        self.wFormLayout.setContentsMargins(5, 5, 5, 5)

        self.labelAlg = QLabel(self.wFormLayoutWidget)
        self.labelAlg.setText("Chọn thuật toán")
        self.wFormLayout.setWidget(0, QFormLayout.LabelRole, self.labelAlg)

        self.algorithmChoice = QComboBox(self.wFormLayoutWidget)
        self.algorithmChoice.addItem("A-Star")
        self.algorithmChoice.addItem("Dijkstra")
        self.algorithmChoice.addItem("BFS")
        self.algorithmChoice.currentIndexChanged.connect(state.setCurrentAlgo)
        self.wFormLayout.setWidget(
            0, QFormLayout.FieldRole, self.algorithmChoice
        )

        self.labelGS, self.gridSize = self._createLineInput(
            1, "Độ rộng mỗi ô", "20",
            QIntValidator(1, 999),
            state.setGridSize,
            self.wFormLayout, self.wFormLayoutWidget
        )

        self.labelWidth, self.inpWidth = self._createLineInput(
            2, "Số ô ngang", "20",
            QIntValidator(1, 999),
            state.setWidth,
            self.wFormLayout, self.wFormLayoutWidget
        )

        self.labelHeight, self.inpHeight = self._createLineInput(
            3, "Số ô dọc", "20",
            QIntValidator(1, 999),
            state.setHeight,
            self.wFormLayout, self.wFormLayoutWidget
        )

        self.labelDelayTime, self.delayTime = self._createLineInput(
            4, "Thời gian đợi", "1.00",
            QDoubleValidator(0.0, 999.0, 2),
            state.setDelayTime,
            self.wFormLayout, self.wFormLayoutWidget
        )

        self.labelInput = QLabel(self.wFormLayoutWidget)
        self.labelInput.setText("Input")
        self.wFormLayout.setWidget(
            5, QFormLayout.LabelRole, self.labelInput
        )

        self.chooseInputFile = QPushButton(self.wFormLayoutWidget)
        self.chooseInputFile.setText("Chọn File")
        self.chooseInputFile.clicked.connect(self.pick_input)
        self.wFormLayout.setWidget(
            5, QFormLayout.FieldRole, self.chooseInputFile
        )

        self.btnToggle3D = QPushButton(self)
        self.btnToggle3D.setText("Đổi sang chế độ 3D")
        self.btnToggle3D.setGeometry(5, 510, 230, 25)
        # self.btnToggle3D.clicked.connect(self.toggle_3D)

        self.updateValuesFromState()

    def updateValuesFromState(self):
        self.inpWidth.setText(
            str(state.map.width)
        )
        self.inpHeight.setText(
            str(state.map.height)
        )

    def _createLineInput(
        self, index, text, inpText, validator, onUpdate, parent, container
    ):
        label = QLabel(container)
        label.setText(text)
        parent.setWidget(
            index, QFormLayout.LabelRole, label
        )

        inp = QLineEdit(container)
        inp.setText(inpText)
        inp.setAlignment(Qt.AlignRight)
        inp.setValidator(validator)
        inp.returnPressed.connect(
            lambda: onUpdate(inp.text())
        )
        parent.setWidget(
            index, QFormLayout.FieldRole, inp
        )

        return label, inp

    def toggleRun(self):
        newV = not state.running
        if newV:
            self.btnToggleRun.setIcon(self.iconPause)
        else:
            self.btnToggleRun.setIcon(self.iconPlay)

        state.setRunning(newV)

    def pick_input(self):

        filename, _ = QFileDialog.getOpenFileName(
            None,
            "Chọn file Input",
            "",
            "All Files (*);;Text Files (*.txt)"
        )
        if filename:
            inp = open(filename, "r")

            state.setInput(
                ''.join([line for line in inp.readlines()])
            )

            self.updateValuesFromState()
