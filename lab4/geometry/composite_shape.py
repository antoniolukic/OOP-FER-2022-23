from typing import List

from geometry.abstract_graphical_object import AbstractGraphicalObject
from geometry.geometry_util import GeometryUtil
from geometry.graphical_object import GraphicalObject
from point import Point
from rectangle import Rectangle
from geometry.renderer import Renderer


class CompositeShape(AbstractGraphicalObject):
    def __init__(self, children: List[GraphicalObject]):
        super().__init__([])
        self.children: List[GraphicalObject] = children

    def selection_distance(self, mouse_point: Point) -> float:
        min_distance = None
        for child in self.children:
            distance = child.selection_distance(mouse_point)
            if min_distance is None or min_distance > distance:
                min_distance = distance
        return min_distance

    def get_bounding_box(self) -> Rectangle:
        points = []
        for child in self.children:
            rectangle = child.get_bounding_box()
            points.append(Point(rectangle.x, rectangle.y))
            points.append(Point(rectangle.x + rectangle.width, rectangle.y + rectangle.height))
        return GeometryUtil.bounding_box_from_points(points)

    def duplicate(self) -> GraphicalObject:
        raise Exception("Cannot clone Composite")

    def get_shape_name(self) -> str:
        return "Composite"

    def render(self, r: Renderer):
        for child in self.children:
            child.render(r)

    def translate(self, point: Point) -> None:
        for child in self.children:
            child.translate(point)
        self.notify_listeners()

    def get_shape_id(self) -> str:
        return "@COMP"

    def save(self, rows: List[str]) -> None:
        for child in self.children:
            child.save(rows)
        rows.append("{} {}".format(self.get_shape_id(), len(self.children)))

    def load(self, stack: List[GraphicalObject], data: str) -> None:
        components = data.strip().split()
        num_children = int(components[0])
        children = stack[-num_children:]
        for i in range(num_children):
            stack.pop()
        stack.append(CompositeShape(children))
