from states.idle_state import IdleState
from model.document_model import DocumentModel
from geometry.g2_renderer_impl import G2RendererImpl
from point import Point


class EraserState(IdleState):
    def __init__(self, dm: DocumentModel, canvas: G2RendererImpl):
        self.dm = dm
        self.canvas = canvas
        self.objects_to_erase = []
        self.all_mouse_points = []
        self.last_mouse_point = None

    def mouse_down(self, mouse_point: Point, shift_down: bool, ctrl_down: bool) -> None:
        self.all_mouse_points = []
        self.objects_to_erase = []
        self.all_mouse_points.append(mouse_point)
        self.last_mouse_point = mouse_point

    def mouse_up(self, mouse_point: Point, shift_down: bool, ctrl_down: bool) -> None:
        for go in self.objects_to_erase:
            self.dm.remove_graphical_object(go)
        self.canvas.draw()

    def mouse_dragged(self, mouse_point: Point) -> None:
        if mouse_point not in self.all_mouse_points:
            self.all_mouse_points.append(mouse_point)
            self.canvas.draw_line(self.last_mouse_point, mouse_point, 'red')
            self.last_mouse_point = mouse_point
            for go in self.dm.get_objects():
                if go not in self.objects_to_erase and go.selection_distance(mouse_point) <= 3:
                    self.objects_to_erase.append(go)

    def on_leaving(self) -> None:
        self.canvas.draw()
