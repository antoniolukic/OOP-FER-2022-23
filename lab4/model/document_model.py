from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Tuple

from geometry.graphical_object import GraphicalObject, GraphicalObjectListener
from point import Point


class DocumentModelListener(ABC):
    @abstractmethod
    def document_change(self, dm: DocumentModel):
        pass


class DocumentModel(ABC, GraphicalObjectListener):
    SELECTION_PROXIMITY = 10

    # kad proxy za read only napravi samo tuple()

    class DocumentModelAsGraphicalObjectListener(GraphicalObjectListener):
        def __init__(self, document_model):
            self.document_model = document_model

        def graphical_object_changed(self, go):
            self.document_model.notify_document_model_listeners()

        def graphical_object_selection_changed(self, go):
            self.document_model.selection_changed(go)

    def __init__(self):
        self.objects: List[GraphicalObject] = []
        self.selected_objects: List[GraphicalObject] = []
        self.dm_listeners: List[DocumentModelListener] = []
        self.go_listener = self.DocumentModelAsGraphicalObjectListener(self)

    def selection_changed(self, go: GraphicalObject):
        if go.is_selected() and go not in self.selected_objects:
            self.selected_objects.append(go)
        elif not go.is_selected() and go in self.selected_objects:
            self.selected_objects.remove(go)

        self.notify_document_model_listeners()

    def clear(self) -> None:
        for go in self.objects:
            go.remove_graphical_object_listener(self.go_listener)

        self.objects.clear()
        self.selected_objects.clear()
        self.notify_document_model_listeners()

    def add_graphical_object(self, go: GraphicalObject) -> None:
        self.objects.append(go)
        self.selection_changed(go)
        go.add_graphical_object_listener(self.go_listener)
        self.notify_document_model_listeners()

    def remove_graphical_object(self, go: GraphicalObject):
        go.remove_graphical_object_listener(self.go_listener)
        self.objects.remove(go)
        if go.is_selected():
            self.selected_objects.remove(go)
        self.notify_document_model_listeners()

    def get_objects(self) -> Tuple[GraphicalObject]:
        return tuple(self.objects)

    def get_selected_objects(self) -> Tuple[GraphicalObject]:
        return tuple(self.selected_objects)

    def increase_z(self, go: GraphicalObject) -> None:
        idx = self.objects.index(go)
        if idx != len(self.objects) - 1:
            self.objects[idx], self.objects[idx + 1] = self.objects[idx + 1], self.objects[idx]
            self.notify_document_model_listeners()

    def decrease_z(self, go: GraphicalObject) -> None:
        idx = self.objects.index(go)
        if idx != 0:
            self.objects[idx - 1], self.objects[idx] = self.objects[idx], self.objects[idx - 1]
            self.notify_document_model_listeners()

    def find_selected_graphical_object(self, mouse_point: Point) -> GraphicalObject:
        result = None
        result_distance = None
        for go in self.objects:
            distance = go.selection_distance(mouse_point)
            if distance <= self.SELECTION_PROXIMITY and (result_distance is None or result_distance > distance):
                result = go
                result_distance = distance
        return result

    def find_selected_hot_point(self, go: GraphicalObject, mouse_point: Point) -> int:
        result_idx = -1
        result_distance = None
        for idx in range(go.get_number_of_hot_points()):
            distance = go.get_hot_point_distance(idx, mouse_point)
            if distance <= self.SELECTION_PROXIMITY and (result_distance is None or result_distance > distance):
                result_idx = idx
                result_distance = distance
        return result_idx

    def attach_document_model_listener(self, listener: DocumentModelListener) -> None:
        self.dm_listeners.append(listener)

    def detach_document_model_listener(self, listener: DocumentModelListener) -> None:
        self.dm_listeners.remove(listener)

    def notify_document_model_listeners(self) -> None:
        for listener in self.dm_listeners:
            listener.document_change(self)
