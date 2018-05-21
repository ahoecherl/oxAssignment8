class Tape:

    def __len__(self):
        return self.size

    def append(self, TapeEntry):
        self.tapeList.append(TapeEntry)
        self.size += 1
        return self.size-1

    def __init__(self):
        self.size=0
        self.tapeList=[]

    def clr(self):
        self.__init__()
