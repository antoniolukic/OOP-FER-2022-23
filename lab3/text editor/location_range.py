class LocationRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        print("start:", self.start)
        print("end:", self.end)
