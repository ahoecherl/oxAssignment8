class Tape:

    def __len__(self):
        return self.size

    def append(self, TapeEntry):
        self.tapeList.append(TapeEntry)
        self.size += 1
        return self.size-1

    def __init__(self):
        self.size = 0
        self.tapeList = []

    def __str__(self):
        s = ''
        for i in self.tapeList:
            s += i.__str__()+"\n"
        return s

    def clr(self):
        self.size = 0
        self.tapeList = []
