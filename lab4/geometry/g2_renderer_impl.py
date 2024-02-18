from typing import List

from tkinter import *
from model.document_model import DocumentModel, DocumentModelListener
from geometry.renderer import Renderer
from point import Point
from states.state import State
from states.idle_state import IdleState


class G2RendererImpl(Canvas, Renderer):

    class G2AsDocumentModelListener(DocumentModelListener):
        def __init__(self, G2R):
            self.G2RendererImpl = G2R

        def document_change(self, dm):
            self.G2RendererImpl.draw()

    def __init__(self, document_model: DocumentModel, **kw):
        super().__init__(**kw)
        self.dm = document_model
        self.dm_listener = self.G2AsDocumentModelListener(self)
        self.dm.attach_document_model_listener(self.dm_listener)
        self.current_state: State = IdleState()
        self.pack(side=BOTTOM, fill=BOTH, expand=1)

        self.bind_all("<Key>", self.key_pressed)
        self.bind("<ButtonPress-1>", self.left_mouse_pressed)
        self.bind("<ButtonRelease-1>", self.left_mouse_released)
        self.bind("<B1-Motion>", self.left_mouse_dragged)

    def draw_line(self, s: Point, e: Point, color: str):
        self.create_line(self.canvasx(s.x), self.canvasy(s.y),
                         self.canvasx(e.x), self.canvasy(e.y),
                         fill=color)

    def fill_polygon(self, points: List[Point]):
        extracted_points = []
        for p in points:
            extracted_points.extend([p.x, p.y])
        self.create_polygon(extracted_points, outline='black', fill='blue')

    def draw(self):
        self.delete("all")
        for go in self.dm.get_objects():
            go.render(self)
            self.current_state.after_draw(self, go)
        self.current_state.after_draw_all(self)

    def key_pressed(self, event):
        if event.keysym == "Escape":
            self.current_state.on_leaving()
            self.current_state = IdleState()
        else:
            self.current_state.key_pressed(event)

    def left_mouse_pressed(self, event):
        self.current_state.mouse_down(Point(event.x, event.y), event.state & 0x1, event.state & 0x4)

    def left_mouse_released(self, event):
        self.current_state.mouse_up(Point(event.x, event.y), event.state & 0x1, event.state & 0x4)

    def left_mouse_dragged(self, event):
        self.current_state.mouse_dragged(Point(event.x, event.y))
