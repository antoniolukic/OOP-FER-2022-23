import re

class Cell:
    exp = ""
    value = None

    def __init__(self, exp, sheet):
        self.exp = exp
        self.value = None
        self.sheet = sheet
        self.referencedby = []
        self.listeners = []

    def addListener(self, listener):
        self.listeners.append(listener)
    
    def removeListener(self, listener):
        self.listeners.remove(listener)
    
    def evaluate(self):
        old = self.value
        operands = self.referencedby
        value = 0
        if not operands:
            value = int(self.exp)
        else:
            for ref in operands:
                value += ref.value
        self.value = value
        if old != value:
            self.notifyListeners()

    def notifyListeners(self):
        if self.listeners:
            for listener in self.listeners:
                listener.evaluate()

class Sheet:
    table = []

    def __init__(self, row, column):
        self.row = row
        self.column = column
        for i in range(row):
            temp = []
            for j in range(column):
                temp.append(Cell("", Sheet))
            self.table.append(temp)

    def cell(self, ref):
        col = ord(ref[0]) - ord('A')
        row = int(ref[1:]) - 1
        return self.table[row][col]

    def getrefs(self, cell):
        references = re.findall(r'[A-Z]+\d+', cell.exp)
        return [self.cell(ref) for ref in references]

    def getnames(self, cell):
        return re.findall(r'[A-Z]+\d+', cell.exp)

    def set(self, ref, content):
        current = self.cell(ref) 
        # provjeri cirkularnost
        odlcontent = current.exp
        current.exp = content
        try:
            [self.checcircular(x, ref) for x in self.getnames(current)]
        except Exception as e:
            print("CIRCULAR!")
            current.exp = odlcontent
            return

        newReference = [x for x in self.getrefs(current)]
        oldReference = current.referencedby
        current.referencedby = newReference
        self.updateListeners(current, oldReference)
        self.evaluate(current)

    def checcircular(self, currentname, namecheck):
        if namecheck == currentname:
            raise Exception("CIRCULAR!")
        else:
            cell = self.cell(currentname)
            [self.checcircular(x, namecheck) for x in self.getnames(cell)]

    def evaluate(self, cell):
        cell.evaluate()

    def updateListeners(self, cell, oldreference):
        if oldreference:
            for old in oldreference:
                old.removeListener(cell)
        for new in cell.referencedby:
            new.addListener(cell)

    def print(self):
        for i in self.table:
            for j in i:
                if j.value is None:
                    print("N", end=' ')
                else:
                    print(j.value, end=' ')
            print()

s = Sheet(5,5)
s.set('A1','2')
s.set('A2','5')
s.set('A3','A1+A2')
s.print()
print()

s.set('A1','4')
s.set('A4','A1+A3')
s.print()
print()

s.set('A1','A3')
s.print()
print()