import numpy as np

from Map import Map
from controller import controller


def greedy(start, target, map: Map):

    openList = set([start])
    closeList = set([])

    path = np.full(map.width * map.height, -1)

    g = np.zeros(map.width * map.height)

    while len(openList) > 0:

        controller.pfAddState((openList.copy(), closeList.copy()))

        thePoint = None
        minVal = float('Inf')

        for point in openList:
            d = map.distance(point, target)
            if d < minVal:
                minVal = d
                thePoint = point

        if thePoint == target:
            controller.pfAddState(
                path=controller.resolvePath(path, target)
            )
            return g[map.toIndex(target)]

        openList.remove(thePoint)
        closeList.add(thePoint)

        tpI = map.toIndex(thePoint)
        for point, cost in map.getNextPoints(thePoint):
            pI = map.toIndex(point)
            if point not in closeList:
                path[pI] = tpI
                g[pI] = g[tpI] + cost
                openList.add(point)

    return -1
