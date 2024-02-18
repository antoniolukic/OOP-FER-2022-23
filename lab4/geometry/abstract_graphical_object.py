from typing import List

from point import Point
from geometry.geometry_util import GeometryUtil
from geometry.graphical_object import GraphicalObject, GraphicalObjectListener


class AbstractGraphicalObject(GraphicalObject):
    def __init__(self, points: List[Point]):
        self.hot_points = points
        self.hot_points_selected = list()
        self.selected = False
        self.listeners = list()

    def get_hot_point(self, index: int) -> Point:
        return self.hot_points[index]

    def set_hot_point(self, index: int, point: Point) -> None:
        self.hot_points[index] = point
        self.notify_listeners()

    def get_number_of_hot_points(self) -> int:
        return len(self.hot_points)

    def get_hot_point_distance(self, index: int, mouse_point: Point) -> float:
        return GeometryUtil.distance_from_point(self.hot_points[index], mouse_point)

    def is_hot_point_selected(self, index: int) -> bool:
        return self.hot_points_selected[index]

    def set_hot_point_selected(self, index: int, selected: bool) -> None:
        self.hot_points_selected[index] = selected
        self.notify_listeners()

    def is_selected(self) -> bool:
        return self.selected

    def set_selected(self, selected: bool) -> None:
        self.selected = selected
        self.notify_selection_listeners()
        self.notify_listeners()

    def translate(self, point: Point) -> None:
        new_hot_points = []
        for i in self.hot_points:
            new_hot_points.append(i.translate(point))
        self.hot_points = new_hot_points
        self.notify_listeners()

    def add_graphical_object_listener(self, listener: GraphicalObjectListener) -> None:
        self.listeners.append(listener)

    def remove_graphical_object_listener(self, listener: GraphicalObjectListener) -> None:
        self.listeners.remove(listener)

    def notify_listeners(self):
        for listener in self.listeners:
            listener.graphical_object_changed(self)

    def notify_selection_listeners(self):
        for listener in self.listeners:
            listener.graphical_object_selection_changed(self)
