from __future__ import annotations

import math
from typing import List

from point import Point
from rectangle import Rectangle


class GeometryUtil:
    @staticmethod
    def distance_from_point(point1: Point, point2: Point) -> float:
        return math.sqrt(math.pow(point1.x - point2.x, 2) + math.pow(point1.y - point2.y, 2))

    @staticmethod
    def distance_from_line_segment(s: Point, e: Point, p: Point):
        vector_se = e.difference(s)
        vector_se_norm = math.sqrt(math.pow(vector_se.x, 2) + math.pow(vector_se.y, 2))
        vector_sp = p.difference(s)

        dot = vector_se.x * vector_sp.x + vector_se.y * vector_sp.y
        dot = dot / (vector_se_norm ** 2)

        if dot > 1:
            return GeometryUtil.distance_from_point(e, p)
        elif dot < 0:
            return GeometryUtil.distance_from_point(s, p)
        else:
            projected = Point(s.x + dot * vector_se.x, s.y + dot * vector_se.y)
            return GeometryUtil.distance_from_point(projected, p)

    @staticmethod
    def bounding_box_from_points(points: List[Point]):
        x_min, x_max, y_min, y_max = points[0].x, points[0].x, points[0].y, points[0].y
        for p in points:
            x_min = min(x_min, p.x)
            x_max = max(x_max, p.x)
            y_min = min(y_min, p.y)
            y_max = max(y_max, p.y)

        return Rectangle(x_min, y_min, x_max - x_min, y_max - y_min)
