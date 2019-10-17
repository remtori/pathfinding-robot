import numpy as np
from typing import List, Tuple


Point = Tuple[int, int]


AIR     = False
WALL    = True

DELTA = [
    (1, 0, 1), (0, 1, 1), (-1, 0, 1), (0, -1, 1),
    (1, 1, 1.5), (1, -1, 1.5), (-1, 1, 1.5), (-1, -1, 1.5)
]


class Map:
    def __init__(self, s: str):

        lines = s.splitlines()

        w, h = lines[0].split(',')
        self.width = int(w)
        self.height = int(h)
        self.map = np.full([self.width * self.height], AIR)

        points = self._getPoints(lines[1])
        self.startPoint, self.targetPoint, *self.passPoint = points

        self.polygons = []
        for i in range(int(lines[2])):
            self.polygons.append(
                self._getPoints(lines[i + 3])
            )

        self.rasterize()

    def rasterize(self):

        self.map = np.full([self.width * self.height], AIR)

        for points in self.polygons:
            self._verticiesToMatrix(points)

    def save(self) -> None:
        self.backup = self.map.copy()

    def restore(self) -> None:
        self.map = self.backup

    def getNextPoints(self, point: Point):
        result = []
        x, y = point
        for dx, dy, cost in DELTA:
            aX, aY = x + dx, y + dy
            if self[aX, aY] != WALL:
                result.append(((aX, aY), cost))

        return result

    def distance(self, pointA: Point, pointB: Point):
        x1, y1 = pointA
        x2, y2 = pointB
        return abs(x1 - x2) + abs(y1 - y2)

    def _verticiesToMatrix(self, verticies: List[Point]) -> None:

        MAX_VAL = 10**4

        minY = MAX_VAL
        maxY = -MAX_VAL

        for x, y in verticies:
            if y < minY:
                minY = y
            if y > maxY:
                maxY = y

        lines = []
        for i in range(maxY - minY + 1):
            lines.append([MAX_VAL, -MAX_VAL])

        def connectVertex(x0, y0, x1, y1):
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            x, y = x0, y0
            sx = -1 if x0 > x1 else 1
            sy = -1 if y0 > y1 else 1

            if dx > dy:
                err = dx / 2.0
                while x != x1:
                    setMinMaxX(x, y)
                    err -= dy
                    if err < 0:
                        y += sy
                        err += dx
                    x += sx
            else:
                err = dy / 2.0
                while y != y1:
                    setMinMaxX(x, y)
                    err -= dx
                    if err < 0:
                        x += sx
                        err += dy
                    y += sy
            setMinMaxX(x, y)

        def setMinMaxX(x, y):
            if x > lines[y - minY][1]:
                lines[y - minY][1] = x
            if x < lines[y - minY][0]:
                lines[y - minY][0] = x

        prevVertex = verticies[-1]
        for vertex in verticies:
            connectVertex(*prevVertex, *vertex)
            prevVertex = vertex

        for i in range(len(lines)):
            y = i + minY
            for x in range(lines[i][0], lines[i][1]):
                self[x, y] = WALL

    def _getPoints(self, s: str) -> List[Point]:

        results = []
        nums = [int(n) for n in s.split(',')]

        for i in range(0, len(nums), 2):
            results.append(
                (nums[i], nums[i + 1])
            )

        return results

    def toIndex(self, point: Point) -> int:
        return point[0] + point[1] * self.width

    def toPoint(self, index) -> Point:
        return index % self.width, index // self.width

    # Overloading [] operator

    def __getitem__(self, key):
        x, y = key

        if 0 < x < self.width and 0 < y < self.height:
            return self.map[x + y * self.width]
        else:
            return WALL

    def __setitem__(self, key, value):
        x, y = key
        i = x + y * self.width

        if 0 <= i < len(self.map):
            self.map[i] = value
