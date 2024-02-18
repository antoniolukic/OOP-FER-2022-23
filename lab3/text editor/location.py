class Location:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        return "Row:" + str(self.row) + ", Col:" + str(self.col)
