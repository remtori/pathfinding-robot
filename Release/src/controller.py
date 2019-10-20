import threading
from collections import deque
from time import time
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
        self.delayTime = 10
        self.running = False

        self.started = False
        self.finished = False

        self.map = a
        self.states = deque()
        self.paths = []
        self.currentStateIndex = -1

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.update)

    def pfStart(self):
        self.states = deque()
        self.paths = []
        self.currentStateIndex = -1

        self.winController.setPfResult('_', '_')

        self.agent = threading.Thread(
            name='Agents',
            daemon=True,
            target=self.doPF
        )

        self.started = True
        self.running = True
        self.finished = False

        self.agent.start()
        self.update()

    def doPF(self):
        startTime = time()
        cost = 0

        pf = self.algorithms[self.currentAlgo]['func']
        start = self.map.startPoint
        target = self.map.targetPoint
        pas = self.map.passPoint.copy()

        while len(pas) > 0:
            pI = -1
            minV = float('Inf')
            for i in range(len(pas)):
                d = self.map.distance(start, pas[i])
                if d < minV:
                    minV = d
                    pI = i

            c = pf(start, pas[pI], self.map)
            start = pas[pI]
            pas.pop(pI)

            if c == -1:
                return self.pfEnd(-1, time() - startTime)
            else:
                cost += c

        c = pf(start, target, self.map)
        if c == -1:
            return self.pfEnd(-1, time() - startTime)
        else:
            cost += c

        self.pfEnd(cost, time() - startTime)

    def pfEnd(self, cost=None, duration=None):
        if self.started:
            self.finished = True
            if cost is not None and duration is not None:
                self.winController.setPfResult(cost, '{:.2f}ms'.format(duration * 1000))

    def update(self):

        if self.currentStateIndex < len(self.states) - 1:
            if self.map.width * self.map.height > 2500:
                while len(self.states) > 1:
                    self.states.popleft()
            else:
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
        self.pfEnd()
        self.running = False
        self.started = False
        self.finished = False
        self.states = deque()
        self.paths = []
        self.currentStateIndex = -1
        self.map = Map(inp)

    def pfAddState(self, states=None, path=None):

        if states is not None:
            self.states.append(states)
            if self.currentStateIndex < 0:
                self.currentStateIndex = 0

        if path is not None:
            self.paths.append(path)

    def getPfList(self):
        if self.currentStateIndex >= 0:
            return self.states[self.currentStateIndex]

        return [], []

    def getPfPaths(self):
        return self.paths

    def debugStepForward(self):
        if self.currentStateIndex < len(self.states) - 1:
            self.currentStateIndex += 1
            self.winRenderer.update()

    def debugStepBackward(self):
        if self.currentStateIndex > 0:
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

    def resolvePath(self, path, target):
        resultPath = []

        i = self.map.toIndex(target)
        while True:
            resultPath.append(self.map.toPoint(i))
            i = path[i]
            if i == -1:
                break

        return resultPath


controller = _Controller()


__import__('agents')
