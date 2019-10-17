import numpy as np

from Map import Map
from controller import controller


def greedy(map: Map):

    start = map.startPoint
    target = map.targetPoint
    # passengers = map.passPoint

    openList = set([start])
    closeList = set([])
    path = np.zeros(map.width * map.height)

    while len(openList) > 0:

        controller.pfAddState((openList.copy(), closeList.copy()))

        thePoint = None
        minVal = float('Inf')

        for point in openList:
            d = map.distance(point, target)
            if d < minVal:
                minVal = d
                thePoint = point

        if thePoint is None:
            controller.pfEnd()
            return
        elif thePoint == target:
            controller.pfAddState(path=path.copy())
            controller.pfEnd()
            return

        openList.remove(thePoint)
        closeList.add(thePoint)

        for x, y, _ in map.getNextPoints(thePoint):
            point = (x, y)
            if point not in closeList:
                path[map.toIndex(point)] = map.toIndex(thePoint)
                openList.add(point)

    controller.pfEnd()
    return
