class TapeEntry:

    def __init__(self, operationType, value, indexArg1 = -1, indexArg2 = -1, extraValue = 0):
        self.operationType = operationType
        self.indexArg1 = indexArg1
        self.indexArg2 = indexArg2
        self.value = value
        self.extraValue = extraValue
        self.valueBar = 0

    def __str__(self):
        s = "TapeEntry: " + self.operationType + ", " + self.indexArg1 + ", " + self.indexArg2 + ": " + self.value + ", " + self.extraValue + ", " + self.valueBar;
        return s

    def addValueBar(self, input):
        self.valueBar += input