from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QIntValidator, QIcon
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

from controller import controller


class ControllerWindow(QWidget):

    def __init__(self):
        super(ControllerWindow, self).__init__()

        self.setWindowTitle("Controller")
        self.setGeometry(1060, 100, 240, 540)

        self.initUI()
        self.show()

    def initUI(self):

        self.wHLayoutWidget = QWidget(self)
        self.wHLayoutWidget.setGeometry(0, 0, 240, 50)
        self.wHLayout = QHBoxLayout(self.wHLayoutWidget)
        self.wHLayout.setContentsMargins(5, 5, 5, 5)

        self.btnStepBackward = QToolButton(self.wHLayoutWidget)
        self.btnStepBackward.setIcon(QIcon("./assets/icons/step-backward.svg"))
        self.btnStepBackward.setToolTip("Quay lại bước trước")
        self.btnStepBackward.clicked.connect(controller.debugStepBackward)
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
        self.btnStepForward.clicked.connect(controller.debugStepForward)
        self.wHLayout.addWidget(self.btnStepForward)

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

        for algo in controller.algorithms:
            self.algorithmChoice.addItem(algo['name'])

        self.algorithmChoice.currentIndexChanged.connect(self.changeAlgo)

        self.wFormLayout.setWidget(
            0, QFormLayout.FieldRole, self.algorithmChoice
        )

        self.labelGS, self.gridSize = self._createLineInput(
            1, "Độ rộng mỗi ô", "20",
            QIntValidator(1, 9999999),
            self.wFormLayout, self.wFormLayoutWidget
        )

        self.labelWidth, self.inpWidth = self._createLineInput(
            2, "Số ô ngang", "20",
            QIntValidator(1, 9999999),
            self.wFormLayout, self.wFormLayoutWidget
        )

        self.labelHeight, self.inpHeight = self._createLineInput(
            3, "Số ô dọc", "20",
            QIntValidator(1, 9999999),
            self.wFormLayout, self.wFormLayoutWidget
        )

        self.labelDelayTime, self.delayTime = self._createLineInput(
            4, "Thời gian đợi", "50",
            QIntValidator(20, 9999999),
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

        self.btnApply = QPushButton(self)
        self.btnApply.setText("Áp dụng")
        self.btnApply.setGeometry(5, 220, 230, 25)
        self.btnApply.clicked.connect(self.applySettings)

        self.infoSeperator = QFrame(self)
        self.infoSeperator.setGeometry(0, 250, 240, 5)
        self.infoSeperator.setFrameShape(QFrame.HLine)
        self.infoSeperator.setFrameShadow(QFrame.Sunken)

        self.wInfoLayoutWidget = QWidget(self)
        self.wInfoLayoutWidget.setGeometry(0, 260, 240, 300)
        self.wInfoLayout = QFormLayout(self.wInfoLayoutWidget)
        self.wInfoLayout.setContentsMargins(5, 5, 5, 5)

        self.labelCost, self.valCost = self._createInfo(
            0, "Cost", "_", self.wInfoLayout, self.wInfoLayoutWidget
        )

        self.labelTimeCost, self.valTimeCost = self._createInfo(
            1, "Duration", "_", self.wInfoLayout, self.wInfoLayoutWidget
        )

        # self.btnToggle3D = QPushButton(self)
        # self.btnToggle3D.setText("Đổi sang chế độ 3D")
        # self.btnToggle3D.setGeometry(5, 510, 230, 25)
        # self.btnToggle3D.clicked.connect(self.toggle_3D)

        self.updateValuesFromState()

    def updateValuesFromState(self):
        self.inpWidth.setText(
            str(controller.map.width)
        )
        self.inpHeight.setText(
            str(controller.map.height)
        )

        if controller.running:
            self.btnToggleRun.setIcon(self.iconPause)
        else:
            self.btnToggleRun.setIcon(self.iconPlay)

    def applySettings(self):
        controller.gridSize = int(self.gridSize.text())
        controller.delayTime = int(self.delayTime.text())
        controller.setMapWidth(int(self.inpWidth.text()))
        controller.setMapHeight(int(self.inpHeight.text()))
        controller.winRenderer.update()

    def changeAlgo(self, v):
        controller.currentAlgo = int(v)

    def toggleRun(self):
        newV = not controller.running

        if newV:
            self.btnToggleRun.setIcon(self.iconPause)
        else:
            self.btnToggleRun.setIcon(self.iconPlay)

        controller.running = newV
        if newV and controller.started:
            controller.update()

        if not controller.started and newV is True:
            controller.pfStart()

    def pick_input(self):

        filename, _ = QFileDialog.getOpenFileName(
            None,
            "Chọn file Input",
            "",
            "All Files (*);;Text Files (*.txt)"
        )
        if filename:
            inp = open(filename, "r")

            controller.setNewInput(
                ''.join([line for line in inp.readlines()])
            )

            self.updateValuesFromState()

    def setPfResult(self, cost, time):
        self.valCost.setText(str(cost))
        self.valTimeCost.setText('{:.2f}ms'.format(time * 1000))

    def _createInfo(
        self, index, text, valText, parent, container
    ):
        label = QLabel(container)
        label.setText(text)
        parent.setWidget(
            index, QFormLayout.LabelRole, label
        )

        val = QLabel(container)
        val.setText(valText)
        val.setAlignment(Qt.AlignRight)
        parent.setWidget(
            index, QFormLayout.FieldRole, val
        )

        return label, val

    def _createLineInput(
        self, index, text, inpText, validator, parent, container
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
        parent.setWidget(
            index, QFormLayout.FieldRole, inp
        )

        return label, inp
