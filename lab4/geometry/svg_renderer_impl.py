from typing import List

from point import Point
from geometry.renderer import Renderer


class SvgRendererImpl(Renderer):
    def __init__(self, filename):
        self.file_name = filename
        self.lines = ['<svg xmlns="http://www.w3.org/2000/svg">']

    def close(self) -> None:
        self.lines.append("</svg>")
        f = open(self.file_name + ".svg", "w")
        f.writelines(self.lines)
        f.close()

    def draw_line(self, s: Point, e: Point, color: str):
        line = "    <line x1=\"{:f}\" y1=\"{:f}\" x2=\"{:f}\" y2=\"{:f}\" " \
               "stroke=\"#000000\" stroke-width=\"4\" />".format(s.x, s.y, e.x, e.y)
        self.lines.append(line)

    def fill_polygon(self, points: List[Point]):
        extracted_points = ""
        for p in points:
            extracted_points += str(p.x) + "," + str(p.y) + " "
        line = '   <polygon points="' + extracted_points + \
               '" style="fill:#0000FF;stroke:#000000;stroke-width:1" />'
        self.lines.append(line)
