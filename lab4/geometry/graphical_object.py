from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from point import Point
from rectangle import Rectangle
from geometry.renderer import Renderer


class GraphicalObject(ABC):
    @abstractmethod
    def is_selected(self) -> bool:
        pass

    @abstractmethod
    def set_selected(self, selected: bool) -> None:
        pass

    @abstractmethod
    def get_number_of_hot_points(self) -> int:
        pass

    @abstractmethod
    def get_hot_point(self, index: int) -> Point:
        pass

    @abstractmethod
    def set_hot_point(self, index: int, point: Point) -> None:
        pass

    @abstractmethod
    def is_hot_point_selected(self, index: int) -> bool:
        pass

    @abstractmethod
    def set_hot_point_selected(self, index: int, selected: bool) -> None:
        pass

    @abstractmethod
    def get_hot_point_distance(self, index: int, mouse_point: Point) -> float:
        pass

    @abstractmethod
    def translate(self, delta: Point) -> None:
        pass

    @abstractmethod
    def get_bounding_box(self) -> Rectangle:
        pass

    @abstractmethod
    def selection_distance(self, mouse_point: Point) -> float:
        pass

    @abstractmethod
    def add_graphical_object_listener(self, l: GraphicalObjectListener) -> None:
        pass

    @abstractmethod
    def remove_graphical_object_listener(self, l: GraphicalObjectListener) -> None:
        pass

    @abstractmethod
    def get_shape_name(self) -> str:
        pass

    @abstractmethod
    def duplicate(self) -> GraphicalObject:
        pass

    @abstractmethod
    def render(self, r: Renderer):
        pass

    @abstractmethod
    def get_shape_id(self) -> str:
        pass

    @abstractmethod
    def load(self, stack: List[GraphicalObject], data: str) -> None:
        pass

    @abstractmethod
    def save(self, rows: List[str]) -> None:
        pass


class GraphicalObjectListener:
    @abstractmethod
    def graphical_object_changed(self, go: GraphicalObject) -> None:
        pass

    @abstractmethod
    def graphical_object_selection_changed(self, go: GraphicalObject) -> None:
        pass
