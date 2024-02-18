from states.state import State
from geometry.geometry_util import GeometryUtil
from geometry.graphical_object import GraphicalObject
from model.document_model import DocumentModel
from point import Point
from geometry.renderer import Renderer
from geometry.composite_shape import CompositeShape


class SelectShapeState(State):

    def __init__(self, dm: DocumentModel):
        self.dm = dm
        self.hot_point_index = -1
        self.go: GraphicalObject = None

    def mouse_down(self, mouse_point: Point, shift_down: bool, ctrl_down: bool) -> None:
        if not ctrl_down:
            for go in self.dm.get_selected_objects():
                go.set_selected(False)

        selected_object = self.dm.find_selected_graphical_object(mouse_point)
        if selected_object:
            selected_object.set_selected(True)

        selected_objects = self.dm.get_selected_objects()
        if len(selected_objects) == 1:
            self.go = selected_objects[0]
            self.hot_point_index = self.dm.find_selected_hot_point(selected_objects[0], mouse_point)
        else:
            self.go = None
            self.hot_point_index = -1

    def mouse_up(self, mouse_point: Point, shift_down: bool, ctrl_down: bool) -> None:
        pass

    def mouse_dragged(self, mouse_point: Point) -> None:
        if self.hot_point_index != -1:
            self.go.set_hot_point(self.hot_point_index, mouse_point)

    def key_pressed(self, key_code: int) -> None:
        selected_objects = self.dm.get_selected_objects()
        translation = {"Right": Point(1, 0), "Left": Point(-1, 0), "Up": Point(0, -1), "Down": Point(0, 1)}
        if key_code.keysym in translation:
            for go in selected_objects:
                go.translate(translation[key_code.keysym])

        if len(selected_objects) == 1:
            go = selected_objects[0]
            if key_code.keysym == "plus":
                self.dm.increase_z(go)
            elif key_code.keysym == "minus":
                self.dm.decrease_z(go)
            elif key_code.keysym == "u":
                if go.get_shape_name() == "Composite":
                    self.dm.remove_graphical_object(go)
                    for child in go.children:
                        self.dm.add_graphical_object(child)
                        child.set_selected(True)
        elif len(selected_objects) > 1:
            if key_code.keysym == "g":
                for go in selected_objects:
                    go.set_selected(False)
                    self.dm.remove_graphical_object(go)
                composed = CompositeShape(list(selected_objects))
                composed.set_selected(True)
                self.dm.add_graphical_object(composed)

    def after_draw(self, r: Renderer, go: GraphicalObject) -> None:
        if go.is_selected():
            rectangle = go.get_bounding_box()
            bl = Point(rectangle.x, rectangle.y)
            br = Point(rectangle.x + rectangle.width, rectangle.y)
            tl = Point(rectangle.x, rectangle.y + rectangle.height)
            tr = Point(rectangle.x + rectangle.width, rectangle.y + rectangle.height)
            r.draw_line(bl, br, 'orange')
            r.draw_line(br, tr, 'orange')
            r.draw_line(tr, tl, 'orange')
            r.draw_line(tl, bl, 'orange')

    def after_draw_all(self, r: Renderer) -> None:
        selected_objects = self.dm.get_selected_objects()
        if len(selected_objects) == 1:
            go = selected_objects[0]
            for hotPoint in go.hot_points:
                bl = Point(hotPoint.x - 4, hotPoint.y - 4)
                br = Point(hotPoint.x + 4, hotPoint.y - 4)
                tl = Point(hotPoint.x - 4, hotPoint.y + 4)
                tr = Point(hotPoint.x + 4, hotPoint.y + 4)
                r.draw_line(bl, br, 'orange')
                r.draw_line(br, tr, 'orange')
                r.draw_line(tr, tl, 'orange')
                r.draw_line(tl, bl, 'orange')

    def on_leaving(self) -> None:
        for go in self.dm.get_selected_objects():
            go.set_selected(False)
