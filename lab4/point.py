from __future__ import annotations


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def translate(self, dp: Point) -> Point:
        return Point(self.x + dp.x, self.y + dp.y)

    def difference(self, p: Point) -> Point:
        return Point(self.x - p.x, self.y - p.y)
