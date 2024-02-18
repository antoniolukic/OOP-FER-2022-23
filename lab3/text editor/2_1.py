import tkinter as tk


class MyComponent(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, width=200, height=200, highlightthickness=0)
        self.pack()
        
        self.create_line(100, 0, 100, 200, fill="red", width=1)  # vodoravna crvena linija
        self.create_line(0, 100, 200, 100, fill="red", width=1)  # okomita crvena linija
        
        self.create_text(100, 70, text="Dobar dan za raditi ooup")  # prvi red teksta
        self.create_text(100, 130, text="Da li je uistinu dobar dan?")  # drugi red teksta
        
        self.bind('<Return>', self.close_window)  # povezivanje tipke Enter s zatvaranjem prozora

    def close_window(self, event):
        self.master.destroy()


window = tk.Tk()
window.title("Moja komponenta")
window.geometry("200x200")

custom_component = MyComponent(window)
custom_component.focus_set()
window.mainloop()


#Vidimo da osnovni razred omogućava da grafički podsustav samostalno poziva naš kod za crtanje kad god se za
#to javi potreba, iako je oblikovan i izveden davno prije naše grafičke komponente. Koji oblikovni obrazac to omogućava?
# Obrazac okvirna metoda

#Vidimo također da naša grafička komponenta preko osnovnog razreda može dobiti informacije o pritisnutim tipkama
#bez potrebe za čekanjem u radnoj petlji. Koji oblikovni obrazac to omogućava?
# Obarazac promatrač
