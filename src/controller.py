import threading
from PyQt5.QtCore import QTimer

from Map import Map


a = Map("""22,18
2,2,19,16
3
4,4,5,9,8,10,9,5
8,12,8,17,13,12
11,1,11,6,14,6,14,1""")


class _Controller:
    def __init__(self):
        self.gridSize = 20
        self.algorithms = []
        self.currentAlgo = 0
        self.delayTime = 100
        self.running = False

        self.started = False
        self.finished = False

        self.map = a
        self.emitters = []

        self.states = []
        self.paths = []
        self.currentStateIndex = -1

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.update)

    def pfStart(self):
        self.states = []
        self.paths = []
        self.currentStateIndex = -1

        self.agent = threading.Thread(
            name='Agents',
            daemon=True,
            target=self.algorithms[self.currentAlgo]['func'],
            args=(self.map,)
        )

        self.started = True
        self.running = True
        self.finished = False

        self.agent.start()
        self.update()

    def pfEnd(self):
        if self.started:
            self.finished = True

    def update(self):

        if self.currentStateIndex < len(self.states) - 1:
            self.currentStateIndex += 1
        elif self.finished:
            self.running = False
            self.started = False
            self.finished = False
            self.winController.updateValuesFromState()

        self.winRenderer.update()

        if self.running:
            self.timer.start(self.delayTime)

    def setNewInput(self, inp: str):
        self.pfTerminate()
        self.map = Map(inp)

    def pfAddState(self, states=None, path=None):

        if states is not None:
            self.states.append(states)

        if path is not None:
            self.paths.append(path)

    def getPfList(self):
        if self.currentStateIndex > 0:
            return self.states[
                self.currentStateIndex
            ]

        return [], []

    def getPfPaths(self):
        return self.paths

    def debugStepForward(self):
        if self.started and not self.running and self.currentStateIndex < len(self.states) - 1:

            self.currentStateIndex += 1
            self.winRenderer.update()

    def debugStepBackward(self):
        if self.started and not self.running and self.currentStateIndex > 0:

            self.currentStateIndex -= 1
            self.winRenderer.update()

    def setMapWidth(self, v):
        try:
            self.map.width = int(v)
            self.map.rasterize()
        except ValueError:
            pass

    def setMapHeight(self, v):
        try:
            self.map.height = int(v)
            self.map.rasterize()
        except ValueError:
            pass

    def addAlgorithm(self, name: str, func) -> None:
        self.algorithms.append({
            'name': name,
            'func': func
        })

        print(name)


controller = _Controller()


__import__('agents')
