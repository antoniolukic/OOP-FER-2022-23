import math
from typing import List

from geometry.abstract_graphical_object import AbstractGraphicalObject
from geometry.geometry_util import GeometryUtil
from geometry.graphical_object import GraphicalObject
from geometry.renderer import Renderer
from point import Point
from rectangle import Rectangle


class Oval(AbstractGraphicalObject):
    def __init__(self, bottom: Point = Point(0, 10), right: Point = Point(10, 0)):
        super().__init__([bottom, right])

    def selection_distance(self, mouse_point: Point) -> float:
        center = Point(self.hot_points[0].x, self.hot_points[1].y)
        a = GeometryUtil.distance_from_point(center, self.hot_points[1])
        b = GeometryUtil.distance_from_point(center, self.hot_points[0])
        if (mouse_point.x - center.x) ** 2 / a ** 2 + (mouse_point.y - center.y) ** 2 / b ** 2 <= 1:
            return 0

        min_dist = -1
        n_points = 60

        for x in range(n_points):
            p = Point(center.x + a * math.cos(x * 2 * math.pi / n_points),
                      center.y + b * math.sin(x * 2 * math.pi / n_points))
            distance = GeometryUtil.distance_from_point(p, mouse_point)
            if min_dist == -1 or min_dist > distance:
                min_dist = distance
        return min_dist

    def get_bounding_box(self) -> Rectangle:
        left_bottom = Point(self.hot_points[0].x - (self.hot_points[1].x - self.hot_points[0].x),
                            self.hot_points[0].y)
        right_top = Point(self.hot_points[1].x,
                          self.hot_points[1].y + (self.hot_points[1].y - self.hot_points[0].y))

        return GeometryUtil.bounding_box_from_points([left_bottom, right_top])

    def duplicate(self) -> GraphicalObject:
        return Oval(self.hot_points[0], self.hot_points[1])

    def get_shape_name(self) -> str:
        return "Oval"

    def render(self, r: Renderer) -> None:
        center = Point(self.hot_points[0].x, self.hot_points[1].y)
        a = GeometryUtil.distance_from_point(center, self.hot_points[1])
        b = GeometryUtil.distance_from_point(center, self.hot_points[0])
        points = []
        n_points = 60
        for x in range(n_points + 1):
            points.append(
                Point(center.x + a * math.cos(x * 2 * math.pi / n_points),
                      center.y + b * math.sin(x * 2 * math.pi / n_points))
            )
        r.fill_polygon(points)

    def get_shape_id(self) -> str:
        return "@OVAL"

    def save(self, rows: List[str]) -> None:
        rows.append("{} {} {} {} {}".format(self.get_shape_id(), self.hot_points[0].x, self.hot_points[0].y,
                                            self.hot_points[1].x, self.hot_points[1].y))

    def load(self, stack: List[GraphicalObject], data: str) -> None:
        components = data.strip().split()
        bottom = Point(int(components[0]), int(components[1]))
        right = Point(int(components[2]), int(components[3]))
        stack.append(Oval(bottom, right))
