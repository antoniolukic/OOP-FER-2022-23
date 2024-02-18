from __future__ import annotations

from tkinter import messagebox

from .plugin import Plugin
from text_editor_model import TextEditorModel
from undo_manager import UndoManager
from clipboard_stack import ClipboardStack


class StatisticPlugin(Plugin):
    def get_name(self):
        return "Statistic"

    def get_description(self):
        return "Counts rows, words and letters in a file"

    def execute(self, model: TextEditorModel, undo_manager: UndoManager, clipboard_stack: ClipboardStack):
        rows = len(model.lines)
        words = len(" ".join(model.lines).split(" "))
        letters = sum(sum(1 for character in line if character.isalpha()) for line in model.lines)
        messagebox.showinfo(
            self.get_name(),
            "Lines: {}\nWords: {}\nLetters: {}".format(rows, words, letters))
