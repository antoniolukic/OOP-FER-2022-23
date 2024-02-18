import os
import importlib
import tkinter as tk
from tkinter import *
from tkinter import font
from location import Location
from location_range import LocationRange
from text_editor_model import TextEditorModel
from clipboard_stack import ClipboardStack
from undo_manager import UndoManager
from actions.action_erase import ActionErase
from actions.action_write import ActionWrite


class TextEditor(tk.Canvas):
    def __init__(self, parent, model: TextEditorModel):
        super().__init__(parent, width=500, height=500, highlightthickness=0)
        self.parent = parent
        self.taskbar = Frame(self.parent, height=30)

        self.menu_bar, self.file_menu, self.edit_menu, self.move_menu, self.plugin_menu = None, None, None, None, None
        self.create_menu()
        self.pack()

        self.model = model
        self.model.add_cursor_observer(self)  # adding this class to be observer to the TextEditorModel for cursor
        self.model.add_text_observer(self)  # adding this class to be observer to the TextEditorModel for text
        self.clipboard = ClipboardStack()
        self.clipboard.add_observer(self)  # adding this class to be observer to the Clipboard
        self.undo_manager = UndoManager()
        self.undo_manager.add_observer(self)  # adding this class to be observer to the UndoManager

        self.bind("<Escape>", self.close_window)
        self.bind('<Left>', self.move_cursor_left)
        self.bind('<Right>', self.move_cursor_right)
        self.bind('<Up>', self.move_cursor_up)
        self.bind('<Down>', self.move_cursor_down)
        self.bind('<BackSpace>', self.delete_before)
        self.bind('<Delete>', self.delete_after)
        self.bind('<Shift-Left>', self.shift_left)
        self.bind('<Shift-Right>', self.shift_right)
        self.bind('<Shift-Up>', self.shift_up)
        self.bind('<Shift-Down>', self.shift_down)
        self.bind("<Key>", self.key_press)

        self.cursor_visible = True
        self.reset_cursor()  # if you want the cursor to blink
        self.draw_text()

    def create_menu(self):
        self.menu_bar = tk.Menu(self.parent)

        # file menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open text.txt", command=self.open)
        self.file_menu.add_command(label="Save text.txt", command=self.save)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.close_window)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Undo", command=self.undo_move, state='disabled')
        self.edit_menu.add_command(label="Redo", command=self.redo_move, state='disabled')
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut_selection_to_clipboard)
        self.edit_menu.add_command(label="Copy", command=self.copy_selection_to_clipboard)
        self.edit_menu.add_command(label="Paste", command=self.paste_from_clipboard, state='disabled')
        self.edit_menu.add_command(label="Paste and Take", command=self.paste_from_clipboard_remove, state='disabled')
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Delete selection", command=self.delete_section)
        self.edit_menu.add_command(label="Clear document", command=self.delete_document)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # move menu
        self.move_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.move_menu.add_command(label="Cursor to document start", command=self.cursor_to_start)
        self.move_menu.add_command(label="Cursor to document end", command=self.cursor_to_end)
        self.menu_bar.add_cascade(label="Move", menu=self.move_menu)

        # plugin menu
        self.plugin_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Plugins", menu=self.plugin_menu)
        self.load_plugins()
        self.parent.config(menu=self.menu_bar)

    def load_plugins(self):
        plugin_dir = "plugins"
        for filename in os.listdir(plugin_dir):
            if filename.endswith("plugin.py") and not filename.startswith("plugin"):
                filename = filename[:-3]
                plugin_name = ''.join(word.capitalize() for word in filename.split('_'))
                plugin_module = importlib.import_module("plugins." + filename)
                plugin_class = getattr(plugin_module, plugin_name)
                plugin_instance = plugin_class()  # factory method
                self.plugin_menu.add_command(label=plugin_instance.get_name(),
                                             command=lambda plugin=plugin_instance: plugin.execute(self.model,
                                                                                                   self.undo_manager,
                                                                                                   self.clipboard))

    def delete_section(self):
        selected_range = self.model.get_selection_range()
        if selected_range:
            start, end = selected_range.start, selected_range.end
            if end.row < start.row or (end.row == start.row and end.col < start.col):
                start, end = end, start
            action_erase = ActionErase(self, start, end,
                                       self.model.get_text_from_range(LocationRange(start, end)))
            self.undo_manager.push(action_erase)

            self.model.delete_range(selected_range)

    def delete_document(self):
        all_range = LocationRange(Location(0, 0), Location(len(self.model.lines) - 1, len(self.model.lines[-1])))
        action_erase = ActionErase(self, all_range.start, all_range.end, self.model.get_text_from_range(all_range))
        self.undo_manager.push(action_erase)

        self.model.lines = ['']
        self.cursor_to_start()
        self.draw_text()

    def cursor_to_start(self):
        self.model.cursorLocation = Location(0, 0)
        self.model.selectionRange = None
        self.draw_text()

    def cursor_to_end(self):
        self.model.cursorLocation = Location(len(self.model.lines) - 1, len(self.model.lines[-1]))
        self.model.selectionRange = None
        self.draw_text()

    def draw_rectangle(self, start_col, start_row, end_col, end_row):
        self.create_rectangle(
            10 + start_col * 8, 10 + start_row * 20, 10 + end_col * 8, 25 + end_row * 20,
            fill="lightblue", stipple="gray50", outline=""
        )

    def draw_text(self):
        self.delete("all")
        monospace_font = font.Font(family="Courier New", size=10)
        cursor_location = self.model.cursorLocation

        y = 10  # margin
        for line in self.model.all_lines():
            x = 10  # margin
            self.create_text(x, y, anchor="nw", text=line, font=monospace_font)
            y += 20  # height

        if self.model.selectionRange:
            start = self.model.selectionRange.start
            end = self.model.selectionRange.end
            if end.row < start.row or (end.row == start.row and end.col < start.col):
                start, end = end, start

            if start.row == end.row:
                self.draw_rectangle(start.col, start.row, end.col, end.row)
            else:
                self.draw_rectangle(start.col, start.row, len(self.model.lines[start.row]), start.row)
                for curr_row in range(start.row + 1, end.row):
                    self.draw_rectangle(0, curr_row, len(self.model.lines[curr_row]), curr_row)
                self.draw_rectangle(0, end.row, end.col, end.row)

        if self.cursor_visible:
            self.create_line(10 + cursor_location.col * 8, 10 + cursor_location.row * 20,
                             10 + cursor_location.col * 8, 25 + cursor_location.row * 20)

        self.taskbar.destroy()
        self.taskbar = Frame(self.parent, height=30)
        self.taskbar.pack(side=BOTTOM, fill=X)
        self.cursor_location = StringVar()
        self.num_lines = StringVar()
        self.cursor_location.set(self.model.cursorLocation)
        self.num_lines.set("No. of lines:" + str(len(self.model.lines)))
        Label(self.taskbar, textvariable=self.cursor_location).pack(side=LEFT)
        Label(self.taskbar, textvariable=self.num_lines).pack(side=RIGHT)

    def reset_cursor(self):
        self.cursor_visible = not self.cursor_visible
        self.draw_text()
        self.timer_id = self.after(500, self.reset_cursor)

    def update_undo_manager(self):
        self.draw_text()

        if self.undo_manager.is_undo_stack_empty():
            self.edit_menu.entryconfig("Undo", state='disabled')
        else:
            self.edit_menu.entryconfig("Undo", state='normal')
        if self.undo_manager.is_redo_stack_empty():
            self.edit_menu.entryconfig("Redo", state='disabled')
        else:
            self.edit_menu.entryconfig("Redo", state='normal')

    def update_cursor_location(self, loc):
        self.draw_text()

    def update_text(self):
        self.draw_text()

    def update_clipboard(self):
        self.draw_text()

        if self.clipboard.is_empty():
            self.edit_menu.entryconfig("Paste", state='disabled')
            self.edit_menu.entryconfig("Paste and Take", state='disabled')
        else:
            self.edit_menu.entryconfig("Paste", state='normal')
            self.edit_menu.entryconfig("Paste and Take", state='normal')

    def move_cursor_left(self, event):
        self.model.move_cursor_left()

    def move_cursor_right(self, event):
        self.model.move_cursor_right()

    def move_cursor_up(self, event):
        self.model.move_cursor_up()

    def move_cursor_down(self, event):
        self.model.move_cursor_down()

    def delete_before(self, event=None):
        if self.model.get_selection_range():
            self.delete_section()
        elif self.model.cursorLocation.row != 0 or self.model.cursorLocation.col != 0:
            end = self.model.get_cursor_location()
            if self.model.cursorLocation.col > 0:
                start = Location(end.row, end.col - 1)
            else:
                start = Location(end.row - 1, len(self.model.lines[end.row - 1]))
            if end.row < start.row or (end.row == start.row and end.col < start.col):
                start, end = end, start
            action_erase = ActionErase(self, start, end,
                                       self.model.get_text_from_range(LocationRange(start, end)))
            self.undo_manager.push(action_erase)
            self.model.delete_before()

    def delete_after(self, event=None):
        if self.model.get_selection_range():
            self.delete_section()
        elif self.model.cursorLocation.row != len(self.model.lines) - 1 or \
                self.model.cursorLocation.col != len(self.model.lines[-1]):
            end = self.model.get_cursor_location()
            if self.model.cursorLocation.col < len(self.model.lines[self.model.cursorLocation.row]):
                start = Location(end.row, end.col + 1)
            else:
                start = Location(end.row + 1, 0)
            if end.row < start.row or (end.row == start.row and end.col < start.col):
                start, end = end, start
            action_erase = ActionErase(self, start, end,
                                       self.model.get_text_from_range(LocationRange(start, end)))
            self.undo_manager.push(action_erase)
            self.model.delete_after()

    def shift_left(self, event):
        self.model.update_selection_range_left()

    def shift_right(self, event):
        self.model.update_selection_range_right()

    def shift_up(self, event):
        self.model.update_selection_range_up()

    def shift_down(self, event):
        self.model.update_selection_range_down()

    def key_press(self, event):
        if event.keysym == "V" and event.state == 0x5:  # Ctrl+Shift+V
            self.paste_from_clipboard_remove()
        elif event.keysym == "c" and event.state == 0x4:  # Ctrl+C
            self.copy_selection_to_clipboard()
        elif event.keysym == "x" and event.state == 0x4:  # Ctrl+X
            self.cut_selection_to_clipboard()
        elif event.keysym == "v" and event.state == 0x4:  # Ctrl+V
            self.paste_from_clipboard()
        elif event.keysym == "z" and event.state == 0x4:  # Ctrl+Z
            self.undo_move()
        elif event.keysym == "y" and event.state == 0x4:  # Ctrl+Y
            self.redo_move()
        elif event.keysym == "a" and event.state == 0x4:  # Ctrl+A
            start = Location(0, 0)
            end = Location(len(self.model.lines) - 1, len(self.model.lines[-1]))
            all_selected = LocationRange(start, end)
            self.model.cursorLocation = end
            self.model.set_selection_range(all_selected)
        elif event.keysym.isalpha() or event.keysym.isdigit():  # alfa numeric
            start = self.model.get_cursor_location()
            self.model.insert(event.char)
            end = self.model.get_cursor_location()
            action_write = ActionWrite(self, start, end, event.char)
            self.undo_manager.push(action_write)

    def copy_selection_to_clipboard(self):
        selected = self.model.get_selection_range()
        if selected:
            start = selected.start
            end = selected.end
            if end.row < start.row or (end.row == start.row and end.col < start.col):
                start, end = end, start
            self.clipboard.push(self.model.get_text_from_range(LocationRange(start, end)))

    def cut_selection_to_clipboard(self):
        if self.model.get_selection_range():
            self.copy_selection_to_clipboard()
            selected = self.model.get_selection_range()
            start = selected.start
            end = selected.end
            if end.row < start.row or (end.row == start.row and end.col < start.col):
                start, end = end, start
            action_erase = ActionErase(self, start, end,
                                       self.model.get_text_from_range(LocationRange(start, end)))
            self.undo_manager.push(action_erase)
            self.model.delete_range(LocationRange(start, end))
            self.clipboard.notify_observers()

    def paste_from_clipboard_remove(self):
        if self.model.get_selection_range():
            self.delete_section()
        text = self.clipboard.pop()
        start = self.model.get_cursor_location()
        self.model.insert_text(text)
        end = self.model.get_cursor_location()
        if end.row < start.row or (end.row == start.row and end.col < start.col):
            start, end = end, start
        action_write = ActionWrite(self, start, end, text)
        self.undo_manager.push(action_write)
        self.clipboard.notify_observers()

    def paste_from_clipboard(self):
        if self.model.get_selection_range():
            self.delete_section()
        text = self.clipboard.peek()
        start = self.model.get_cursor_location()
        self.model.insert_text(text)
        end = self.model.get_cursor_location()
        if end.row < start.row or (end.row == start.row and end.col < start.col):
            start, end = end, start
        action_write = ActionWrite(self, start, end, text)
        self.undo_manager.push(action_write)
        self.clipboard.notify_observers()

    def undo_move(self):
        if not self.undo_manager.is_undo_stack_empty():
            self.undo_manager.undo()

    def redo_move(self):
        if not self.undo_manager.is_redo_stack_empty():
            self.undo_manager.redo()

    def close_window(self, event=None):
        self.master.destroy()

    def save(self, path='text.txt'):
        with open(path, 'w') as f:
            for line in self.model.lines:
                f.write(line + '\n')

    def open(self, path='text.txt'):
        new_range = LocationRange(Location(0, 0), Location(len(self.model.lines) - 1, len(self.model.lines[-1])))
        self.model.set_selection_range(new_range)
        self.delete_section()

        with open(path, 'r') as f:
            new_lines = []
            lines = f.readlines()
            for line in lines[:-1]:
                new_lines.append(line[:-1])
            new_lines.append(lines[-1])

        self.model.lines = new_lines.copy()
        text_range = LocationRange(Location(0, 0), Location(len(self.model.lines) - 1, len(self.model.lines[-1])))
        action_write = ActionWrite(self, text_range.start, text_range.end, self.model.get_text_from_range(text_range))
        self.undo_manager.push(action_write)
        self.draw_text()
