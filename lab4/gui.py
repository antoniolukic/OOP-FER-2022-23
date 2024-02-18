from tkinter import *
from tkinter import simpledialog

from model.document_model import DocumentModel
from geometry.g2_renderer_impl import G2RendererImpl
from states.add_shape_state import AddShapeState
from states.selecet_state_shape import SelectShapeState
from states.eraser_state import EraserState
from geometry.svg_renderer_impl import SvgRendererImpl
from geometry.composite_shape import CompositeShape


class Gui(Frame):
    def __init__(self, objects, **kw):
        super().__init__(**kw)
        self.objects = objects
        self.dm = DocumentModel()

        self.map_prototypes()
        #self.dm.add_graphical_object(LineSegment(Point(100, 10), Point(200, 140)))
        #self.dm.add_graphical_object(LineSegment(Point(70, 10), Point(20, 130)))
        #self.dm.add_graphical_object(Oval(Point(25, 25), Point(40, 30)))

        self.canvas = G2RendererImpl(self.dm)
        self.canvas.draw()
        self.init_toolbar()

    def map_prototypes(self):
        self.prototype = dict()
        for object in self.objects:
            self.prototype[object.get_shape_id()] = object
        self.prototype["@COMP"] = CompositeShape([])

    def init_toolbar(self):
        def create_command(item):
            def command():
                self.canvas.current_state.on_leaving()
                self.canvas.current_state = AddShapeState(item, self.dm)
            return command

        def select_command():
            def command():
                self.canvas.current_state.on_leaving()
                self.canvas.current_state = SelectShapeState(self.dm)
            return command

        def erase_command():
            def command():
                self.canvas.current_state.on_leaving()
                self.canvas.current_state = EraserState(self.dm, self.canvas)
            return command

        def svg_export_command():
            def command():
                file = simpledialog.askstring("Input", "Enter your svg save file:")
                r = SvgRendererImpl(file)
                for go in self.dm.get_objects():
                    go.render(r)
                r.close()
            return command

        def save_native_command():
            def command():
                file = simpledialog.askstring("Input", "Enter your native save file:")
                elements = []
                for go in self.dm.get_objects():
                    go.save(elements)
                f = open(file + ".txt", "w")
                for element in elements:
                    f.write(element + "\n")
                f.close()
            return command

        def load_native_command():
            def command():
                stack = []
                file = simpledialog.askstring("Input", "Enter your native load file:")
                f = open(file + ".txt", "r")
                lines = f.readlines()
                lines = lines[:-1]
                for line in lines:
                    line = line.strip()
                    id, info = line.split(maxsplit=1)
                    self.prototype[id].load(stack, info)
                self.dm.clear()
                for go in stack:
                    self.dm.add_graphical_object(go)
            return command

        toolbar = Frame(self.master)

        for item in self.objects:
            command = create_command(item)
            button = Button(toolbar, text=item.get_shape_name(), command=command)
            button.pack(side=LEFT, padx=2, pady=2)

        select = Button(toolbar, text="Select", command=select_command())
        select.pack(side=LEFT, padx=2, pady=2)

        erase = Button(toolbar, text="Erase", command=erase_command())
        erase.pack(side=LEFT, padx=2, pady=2)

        export = Button(toolbar, text="Export", command=svg_export_command())
        export.pack(side=LEFT, padx=2, pady=2)

        save = Button(toolbar, text="Save", command=save_native_command())
        save.pack(side=LEFT, padx=2, pady=2)

        load = Button(toolbar, text="Load", command=load_native_command())
        load.pack(side=LEFT, padx=2, pady=2)

        toolbar.pack(side=TOP, fill=X)
