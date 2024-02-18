def mymax(iterable, key=lambda x: x):
    # incijaliziraj maksimalni element i maksimalni ključ
    max_x=max_key=None

    # obiđi sve elemente
    for x in iterable:
        if max_key is None or max_key < key(x):  # ako je key(x) najveći -> ažuriraj max_x i max_key
            max_key = key(x)
            max_x = x
    
    return max_x # vrati rezultat
    
key = lambda x: len(x)
example = ["prvi", "drugi", "konobar", "automehatronicarka", "madrac"]
print(mymax(example, key))

maxint = mymax([1, 3, 5, 7, 4, 6, 9, 2, 0])
maxchar = mymax("Suncana strana ulice")
maxstring = mymax(["Gle", "malu", "vocku", "poslije", "kise", "Puna", "je", "kapi", "pa", "ih", "njise"])
print(maxint, maxchar, maxstring)
D={'burek':8, 'buhtla':5}
print(mymax(D, D.get))  #  možemo koristiti kao slobodnu funkciju get jer get nije vezana uz instancu riječnika vec je zajednička svim rječnicima
osobe = [("Joza", "Jozic"), ("Pero", "Peric"), ("Joza", "Markić"), ("Pero", "Lukic"), ("Marko", "Horvat")]
print(mymax(osobe))
