import tkinter as tk
from text_editor import TextEditor
from text_editor_model import TextEditorModel


window = tk.Tk()
window.title("TextEditor")
window.geometry("500x550")

initial_text = "Prvi redak\nDrugi redak\nTreći redak"
model = TextEditorModel(initial_text)

custom_component = TextEditor(window, model)
custom_component.focus_set()

window.mainloop()
