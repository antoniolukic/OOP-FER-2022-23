import os
import importlib

def myfactory(moduleName):
    module = importlib.import_module('plugins.' + moduleName)  # importaj module
    return getattr(module, moduleName)  # dohvati module object 

def printGreeting(pet):
    print(pet.get_name(), "pozdravlja:", pet.greet())

def printMenu(pet):
    print(pet.get_name(), "voli", pet.menu())

def test():
    pets=[]
    # obiđi svaku datoteku kazala plugins 
    for mymodule in os.listdir('plugins'):
        moduleName, moduleExt = os.path.splitext(mymodule)
        # ako se radi o datoteci s Pythonskim kodom ...
        if moduleExt=='.py':
            # instanciraj ljubimca ...
            ljubimac = myfactory(moduleName)('Ljubimac ' + str(len(pets)))
            # ... i dodaj ga u listu ljubimaca
            pets.append(ljubimac)

    # ispiši ljubimce
    for pet in pets:
        printGreeting(pet)
        printMenu(pet)

test()
