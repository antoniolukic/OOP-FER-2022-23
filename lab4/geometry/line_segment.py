from typing import List

from geometry.abstract_graphical_object import AbstractGraphicalObject
from geometry.geometry_util import GeometryUtil
from geometry.graphical_object import GraphicalObject
from geometry.renderer import Renderer
from point import Point
from rectangle import Rectangle


class LineSegment(AbstractGraphicalObject):
    def __init__(self, s: Point = Point(0, 0), e: Point = Point(10, 0)):
        super().__init__([s, e])

    def selection_distance(self, mouse_point: Point) -> float:
        return GeometryUtil.distance_from_line_segment(self.hot_points[0], self.hot_points[1], mouse_point)

    def get_bounding_box(self) -> Rectangle:
        return GeometryUtil.bounding_box_from_points(self.hot_points)

    def duplicate(self) -> GraphicalObject:
        return LineSegment(self.hot_points[0], self.hot_points[1])

    def get_shape_name(self) -> str:
        return "Line"

    def render(self, r: Renderer) -> None:
        r.draw_line(self.hot_points[0], self.hot_points[1], 'black')

    def get_shape_id(self) -> str:
        return "@LINE"

    def save(self, rows: List[str]) -> None:
        rows.append("{} {} {} {} {}".format(self.get_shape_id(), self.hot_points[0].x, self.hot_points[0].y,
                                            self.hot_points[1].x, self.hot_points[1].y))

    def load(self, stack: List[GraphicalObject], data: str) -> None:
        components = data.strip().split()
        start = Point(int(components[0]), int(components[1]))
        end = Point(int(components[2]), int(components[3]))
        stack.append(LineSegment(start, end))
