from __future__ import annotations
from .edit_action import EditAction
from location import Location
from location_range import LocationRange
import copy


class ActionErase(EditAction):
    def __init__(self, receiver, location_start: Location, location_end: Location, text):
        self.receiver = receiver
        self.location_start = location_start
        self.location_end = location_end
        self.text = text

    def copy(self):
        return ActionErase(
            receiver=self.receiver,
            location_start=copy.deepcopy(self.location_start),
            location_end=copy.deepcopy(self.location_end),
            text=self.text
        )

    def execute_do(self):
        location_range = LocationRange(copy.deepcopy(self.location_end), copy.deepcopy(self.location_start))
        self.receiver.model.set_selection_range(location_range)
        self.receiver.model.delete_range(location_range)

    def execute_undo(self):
        self.receiver.model.set_selection_range(None)
        self.receiver.model.cursorLocation = copy.deepcopy(self.location_start)
        if self.text and len(self.text) == 1:
            self.receiver.model.insert(self.text)
        else:
            self.receiver.model.insert_text(self.text)
