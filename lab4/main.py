from tkinter import *

from geometry.line_segment import LineSegment
from geometry.oval import Oval
from gui import Gui

objects = [LineSegment(), Oval()]

root = Tk()
root.title("Paint")
root.geometry("600x600")
gui = Gui(objects)
root.mainloop()
