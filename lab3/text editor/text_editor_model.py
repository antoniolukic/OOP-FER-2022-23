from location import Location
from location_range import LocationRange
import copy


class TextEditorModel:
    def __init__(self, text):
        self.lines = text.split("\n")
        self.selectionRange = None
        self.cursorLocation = Location(0, 0)
        self.cursorObservers = []
        self.textObservers = []

    def all_lines(self):
        return iter(self.lines)
    
    def lines_range(self, index1, index2):
        return iter(self.lines[index1:index2])
    
    def add_cursor_observer(self, observer):
        self.cursorObservers.append(observer)
    
    def remove_cursor_observer(self, observer):
        self.cursorObservers.remove(observer)
    
    def notify_cursor_observers(self):
        for observer in self.cursorObservers:
            observer.update_cursor_location(self.cursorLocation)

    def move_cursor_left(self):
        self.selectionRange = None
        if self.cursorLocation.col > 0:
            self.cursorLocation.col -= 1
        elif self.cursorLocation.row > 0:
            self.cursorLocation.col = len(self.lines[self.cursorLocation.row - 1])
            self.cursorLocation.row -= 1
        self.notify_cursor_observers()

    def move_cursor_right(self):
        self.selectionRange = None
        if self.cursorLocation.col < len(self.lines[self.cursorLocation.row]):
            self.cursorLocation.col += 1
        elif self.cursorLocation.row < len(self.lines) - 1:
            self.cursorLocation.col = 0
            self.cursorLocation.row += 1
        self.notify_cursor_observers()

    def move_cursor_up(self):
        self.selectionRange = None
        if self.cursorLocation.row > 0:
            self.cursorLocation.row -= 1
        if self.cursorLocation.col > len(self.lines[self.cursorLocation.row]):
            self.cursorLocation.col = len(self.lines[self.cursorLocation.row])
        self.notify_cursor_observers()

    def move_cursor_down(self):
        self.selectionRange = None
        if self.cursorLocation.row < len(self.lines) - 1:
            self.cursorLocation.row += 1
        if self.cursorLocation.col > len(self.lines[self.cursorLocation.row]):
            self.cursorLocation.col = len(self.lines[self.cursorLocation.row])
        self.notify_cursor_observers()

    def delete_before(self):
        if self.cursorLocation.col > 0:
            self.lines[self.cursorLocation.row] = (
                self.lines[self.cursorLocation.row][: self.cursorLocation.col - 1]
                + self.lines[self.cursorLocation.row][self.cursorLocation.col :]
            )
            self.cursorLocation.col -= 1
            self.notify_text_observers()
        elif self.cursorLocation.row > 0:
            cursor_location = len(self.lines[self.cursorLocation.row - 1])
            self.lines[self.cursorLocation.row - 1] += self.lines.pop(self.cursorLocation.row)
            self.cursorLocation.row -= 1
            self.cursorLocation.col = cursor_location
            self.notify_text_observers()

    def delete_after(self):
        if self.cursorLocation.col < len(self.lines[self.cursorLocation.row]):
            self.lines[self.cursorLocation.row] = (
                self.lines[self.cursorLocation.row][:self.cursorLocation.col]
                + self.lines[self.cursorLocation.row][self.cursorLocation.col + 1:]
            )
            self.notify_text_observers()
        elif self.cursorLocation.row + 1 < len(self.lines):
            self.lines[self.cursorLocation.row] += self.lines.pop(self.cursorLocation.row + 1)
            self.notify_text_observers()

    def delete_range(self, r):
        start = r.start
        end = r.end
        if end.row < start.row or (end.row == start.row and end.col < start.col):
            start, end = end, start
        if start.row == end.row:  # if it's the same row erase in between
            self.lines[start.row] = (self.lines[start.row][:start.col] + self.lines[start.row][end.col:])
        else:  # if it's not the same row
            self.lines[start.row] = (self.lines[start.row][:start.col] + self.lines[end.row][end.col:])
            del self.lines[start.row + 1: end.row + 1]  # erase the lines in between
        self.cursorLocation = start
        self.selectionRange = None
        self.notify_text_observers()

    def get_selection_range(self) -> LocationRange:
        return copy.deepcopy(self.selectionRange)

    def get_cursor_location(self) -> Location:
        return copy.deepcopy(self.cursorLocation)
    
    def set_selection_range(self, range: LocationRange):
        self.selectionRange = range
        self.notify_text_observers()

    def add_text_observer(self, observer):
        self.textObservers.append(observer)
    
    def remove_text_observer(self, observer):
        self.textObservers.remove(observer)

    def update_selection_range_left(self):
        if self.cursorLocation.col > 0:
            if self.selectionRange:
                end = Location(self.cursorLocation.row, self.cursorLocation.col - 1)
                self.cursorLocation.col -= 1
                self.set_selection_range(LocationRange(self.selectionRange.start, end))
            else:
                start = Location(self.cursorLocation.row, self.cursorLocation.col)
                end = Location(self.cursorLocation.row, self.cursorLocation.col - 1)
                self.cursorLocation.col -= 1
                self.set_selection_range(LocationRange(start, end))
        elif self.cursorLocation.row > 0:
            if self.selectionRange:
                end = Location(self.cursorLocation.row - 1, len(self.lines[self.cursorLocation.row - 1]))
                self.cursorLocation.row -= 1
                self.cursorLocation.col = len(self.lines[self.cursorLocation.row])
                self.set_selection_range(LocationRange(self.selectionRange.start, end))
            else:
                self.move_cursor_left()

    def update_selection_range_right(self):
        if self.cursorLocation.col < len(self.lines[self.cursorLocation.row]):
            if self.selectionRange:
                end = Location(self.cursorLocation.row, self.cursorLocation.col + 1)
                self.cursorLocation.col += 1
                self.set_selection_range(LocationRange(self.selectionRange.start, end))
            else:
                start = Location(self.cursorLocation.row, self.cursorLocation.col)
                end = Location(self.cursorLocation.row, self.cursorLocation.col + 1)
                self.cursorLocation.col += 1
                self.set_selection_range(LocationRange(start, end))
        elif self.cursorLocation.row < len(self.lines) - 1:
            if self.selectionRange:
                end = Location(self.cursorLocation.row + 1, 0)
                self.cursorLocation.row += 1
                self.cursorLocation.col = 0
                self.set_selection_range(LocationRange(self.selectionRange.start, end))
            else:
                self.move_cursor_right()

    def update_selection_range_up(self):
        if self.cursorLocation.row > 0:
            if self.selectionRange:
                start = self.selectionRange.start
            else:
                start = Location(self.cursorLocation.row, self.cursorLocation.col)                
            end = Location(self.cursorLocation.row - 1, min(self.cursorLocation.col, len(self.lines[self.cursorLocation.row - 1])))
            self.cursorLocation.row -= 1
            self.cursorLocation.col = min(self.cursorLocation.col, len(self.lines[self.cursorLocation.row]))
            self.set_selection_range(LocationRange(start, end))

    def update_selection_range_down(self):
        if self.cursorLocation.row < len(self.lines) - 1:
            if self.selectionRange:
                start = self.selectionRange.start
            else:
                start = Location(self.cursorLocation.row, self.cursorLocation.col)                
            end = Location(self.cursorLocation.row + 1, min(self.cursorLocation.col, len(self.lines[self.cursorLocation.row + 1])))
            self.cursorLocation.row += 1
            self.cursorLocation.col = min(self.cursorLocation.col, len(self.lines[self.cursorLocation.row]))
            self.set_selection_range(LocationRange(start, end))

    def notify_text_observers(self):
        for observer in self.textObservers:
            observer.update_text()

    def insert(self, c):
        if self.get_selection_range():
            self.delete_range(self.get_selection_range())
        if c == '\n' or c == '\r':  # enter
            self.lines.insert(self.cursorLocation.row + 1, self.lines[self.cursorLocation.row][self.cursorLocation.col:])
            self.lines[self.cursorLocation.row] = self.lines[self.cursorLocation.row][:self.cursorLocation.col]
            self.cursorLocation.row += 1
            self.cursorLocation.col = 0
        else:  # all other characters
            row = self.cursorLocation.row
            col = self.cursorLocation.col
            self.lines[row] = self.lines[row][:col] + c + self.lines[row][col:]
            self.cursorLocation.col += 1
        self.notify_text_observers()

    def insert_text(self, t):
        if self.get_selection_range():
            self.delete_range(self.get_selection_range())

        if t:
            lines_to_insert = t.split('\n')
            current_line = self.lines[self.cursorLocation.row]
            remaining_text = current_line[self.cursorLocation.col:]
        
            self.lines[self.cursorLocation.row] = current_line[:self.cursorLocation.col] + lines_to_insert[0]  # first line

            if len(lines_to_insert) > 1:  # all in between
                self.lines[self.cursorLocation.row + 1: self.cursorLocation.row + 1] = lines_to_insert[1:]

            self.lines[self.cursorLocation.row + len(lines_to_insert) - 1] += remaining_text  # last line

            self.cursorLocation.row += len(lines_to_insert) - 1
            if len(lines_to_insert) > 1:
                self.cursorLocation.col = len(lines_to_insert[-1])
            else:
                self.cursorLocation.col += len(lines_to_insert[-1])
            self.notify_text_observers()

    def get_text_from_range(self, selected):
        if selected:
            start = selected.start
            end = selected.end
            if end.row < start.row or (end.row == start.row and end.col < start.col):
                start, end = end, start
            if start.row == end.row:
                return self.lines[start.row][start.col:end.col]
            else:
                selectedText = [self.lines[start.row][start.col:]]
                for i in range(start.row + 1, end.row):
                    selectedText.append(self.lines[i])
                selectedText.append(self.lines[end.row][:end.col])
                return "\n".join(selectedText)
