from __future__ import annotations
from typing import List
from actions.edit_action import EditAction


class UndoManager:
    _single_instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._single_instance:
            cls._single_instance = super().__new__(cls, *args, **kwargs)
        return cls._single_instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.observers = []
            self.undo_stack: List[EditAction] = []
            self.redo_stack: List[EditAction] = []

    def is_undo_stack_empty(self):
        return len(self.undo_stack) <= 0

    def is_redo_stack_empty(self):
        return len(self.redo_stack) <= 0

    def undo(self):
        command = self.undo_stack.pop().copy()
        command.execute_undo()
        self.redo_stack.append(command)
        self.notify_observers()

    def redo(self):
        command = self.redo_stack.pop().copy()
        command.execute_do()
        self.undo_stack.append(command)
        self.notify_observers()

    def push(self, command: EditAction):
        self.redo_stack: List[EditAction] = []
        self.undo_stack.append(command.copy())
        self.notify_observers()

    def add_observer(self, o):
        self.observers.append(o)

    def remove_observer(self, o):
        self.observers.remove(o)

    def notify_observers(self):
        for o in self.observers:
            o.update_undo_manager()
