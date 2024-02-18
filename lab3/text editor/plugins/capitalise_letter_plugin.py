from __future__ import annotations

from tkinter import messagebox

from .plugin import Plugin
from text_editor_model import TextEditorModel
from undo_manager import UndoManager
from clipboard_stack import ClipboardStack


class CapitaliseLetterPlugin(Plugin):
    def get_name(self):
        return "CapitaliseLetter"

    def get_description(self):
        return "Capitalises the first letter of all words"

    def execute(self, model: TextEditorModel, undo_manager: UndoManager, clipboard_stack: ClipboardStack):
        for i, line in enumerate(model.lines):
            words = line.split()
            capitalized_words = [word.capitalize() for word in words]
            model.lines[i] = ' '.join(capitalized_words)
        model.notify_text_observers()
        # too much work to write undo_manager for this :)

        messagebox.showinfo("Capitalise letters", "Your words have been capitalised")
