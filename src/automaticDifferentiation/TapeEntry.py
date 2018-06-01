class TapeEntry:

    def __init__(self, operationType, value, indexArg1 = -1, indexArg2 = -1, extraValue = 0):
        self.operationType = operationType
        self.indexArg1 = indexArg1
        self.indexArg2 = indexArg2
        self.value = value
        self.extraValue = extraValue
        self.valueBar = 0

    def __str__(self):
        s = "TapeEntry: " + self.operationType.name + ", " + str(self.indexArg1) + ", " + str(self.indexArg2) + ": " + str(self.value) + ", " + str(self.extraValue) + ", " + str(self.valueBar);
        return s

    def addValueBar(self, input):
        self.valueBar += input