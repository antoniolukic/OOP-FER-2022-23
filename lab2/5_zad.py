import datetime
import time

class SlijedBrojeva:
    def __init__(self, izvor):
        self.kolekcija = []
        self.izvor = izvor
        self.akcije = []
        
    def dodaj_akciju(self, akcija):
        self.akcije.append(akcija)
    
    def makni_akciju(self, akcija):
        self.akcije.remove(akcija)
    
    def obavijesti_promatrace(self):
        for i in self.akcije:
            i.akcija(self.kolekcija)

    def kreni(self):
        broj = 1
        while True:
            broj = self.izvor.broj()
            if broj < 0:
                break
            self.kolekcija.append(broj)
            self.obavijesti_promatrace()
            time.sleep(1)

class Zapis:
    def akcija(kolekcija):
        f = open("kolekcija.txt", "a")
        print("kolekcija.txt")
        f.write(str(datetime.datetime.now()) + ": " + str(kolekcija) + "\n")
        f.close()

class Suma:
    def akcija(kolekcija):
        print("Suma: " + str(sum(kolekcija)))

class Prosjek:
    def akcija(kolekcija):
        print("Prosjek: " + str(sum(kolekcija) / len(kolekcija)))

class Medijan:
    def akcija(kolekcija):
        sortirano = sorted(kolekcija)
        if len(sortirano) % 2 == 1:
            print("Medijan: " + str(sortirano[len(sortirano) // 2]))
        else:
            print("Medijan: " + str((sortirano[len(sortirano) // 2] + sortirano[len(sortirano) // 2 - 1]) / 2))

class TipkovniciIzvor:
    def broj(self):
        return int(input("Upisi broj: "))

class DatotecniIzvor:
    def __init__(self, putanja):
        self.brojevi = []
        f = open(putanja, "r")
        lines = f.readlines()
        for i in lines:
            self.brojevi.append(int(i))
            
    def broj(self):
        if len(self.brojevi) > 0:
            print("Dodani broj: " + str(self.brojevi[0]))
            return self.brojevi.pop(0)
        else:
            return -1
    
brojevi = SlijedBrojeva(DatotecniIzvor("brojevi.txt"))
brojevi.dodaj_akciju(Suma)
brojevi.dodaj_akciju(Prosjek)
brojevi.dodaj_akciju(Medijan)
brojevi.kreni()
