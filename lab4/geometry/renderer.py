from abc import ABC, abstractmethod
from typing import List

from point import Point


class Renderer(ABC):
    @abstractmethod
    def draw_line(self, s: Point, e: Point, color: str):
        pass

    def fill_polygon(self, points: List[Point]):
        pass
