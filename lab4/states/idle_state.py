from states.state import State
from geometry.graphical_object import GraphicalObject
from point import Point
from geometry.renderer import Renderer


class IdleState(State):
    def mouse_down(self, mouse_point: Point, shift_down: bool, ctrl_down: bool) -> None:
        pass

    def mouse_up(self, mouse_point: Point, shift_down: bool, ctrl_down: bool) -> None:
        pass

    def mouse_dragged(self, mouse_point: Point) -> None:
        pass

    def key_pressed(self, key_event) -> None:
        pass

    def after_draw(self, r: Renderer, go: GraphicalObject) -> None:
        pass

    def after_draw_all(self, r: Renderer) -> None:
        pass

    def on_leaving(self) -> None:
        pass
