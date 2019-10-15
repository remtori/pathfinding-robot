from Map import Map


a = Map("""22,18
2,2,19,16
3
4,4,5,9,8,10,9,5
8,12,8,17,13,12
11,1,11,6,14,6,14,1""")


class _State:
    def __init__(self):
        self.running = False
        self.gridSize = 20
        self.algorithms = []
        self.currentAlgo = 0
        self.delayTime = 1

        self.map = a
        self.mapStates = []

    def setGridSize(self, s):
        self.gridSize = int(s)

    def setCurrentAlgo(self, i):
        self.currentAlgo = int(i)

    def setInput(self, str):
        self.map = Map(str)

    def setDelayTime(self, v):
        self.delayTime = float(v)

    def setRunning(self, r: bool):
        self.running = bool(r)
        print(self.running)
        print(self.gridSize)
        print(self.currentAlgo)
        print(self.delayTime)

    def setWidth(self, v):
        try:
            self.map.width = int(v)
            self.map.rasterize()
        except ValueError:
            pass

    def setHeight(self, v):
        try:
            self.map.height = int(v)
            self.map.rasterize()
        except ValueError:
            pass

    def debugStepBackward(self):
        pass

    def debugStepForward(self):
        pass


state = _State()


def addAlgorithm(name: str, func) -> None:
    state.algorithms.append({
        'name': name,
        'func': func
    })
