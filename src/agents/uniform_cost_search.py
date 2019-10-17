import numpy as np

from Map import Map
from controller import controller


def uniform_cost_search(start, target, map: Map):
    openList = set([start])
    closeList = set([])

    path = np.full(map.width * map.height, -1)

    g = np.full(map.width * map.height, float('Inf'))
    g[map.toIndex(start)] = 0

    while len(openList) > 0:

        controller.pfAddState((openList.copy(), closeList.copy()))

        thePoint = None
        minVal = float('Inf')

        for point in openList:
            v = g[map.toIndex(point)]
            if v < minVal:
                minVal = v
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
                alt = g[tpI] + cost
                if alt < g[pI]:
                    g[pI] = alt
                    path[pI] = tpI
                if point not in openList:
                    openList.add(point)

    return -1
