class ClipboardStack:
    def __init__(self):
        self.texts = []
        self.observers = []
    
    def push(self, v):
        self.texts.append(v)
        self.notify_observers()
        
    def pop(self):
        if not self.is_empty():
            text = self.texts.pop()
            self.notify_observers()
            return text
        return None
    
    def peek(self):
        if self.texts:
            return self.texts[-1]
        return None
    
    def is_empty(self):
        return len(self.texts) <= 0
    
    def delete(self):
        self.texts = []
        self.notify_observers()

    def add_observer(self, o):
        self.observers.append(o)

    def remove_observer(self, o):
        self.observers.remove(o)

    def notify_observers(self):
        for o in self.observers:
            o.update_clipboard()
