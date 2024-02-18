from __future__ import annotations
from abc import ABC, abstractmethod
from undo_manager import UndoManager
from clipboard_stack import ClipboardStack
from text_editor_model import TextEditorModel


class Plugin(ABC):
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def execute(self, model: TextEditorModel, undo_manager: UndoManager, clipboard_stack: ClipboardStack):
        pass
