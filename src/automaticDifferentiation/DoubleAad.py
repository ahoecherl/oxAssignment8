from .TapeEntry import TapeEntry
from .OperationTypeAad import OperationTypeAad
import math
from scipy.stats import norm

class DoubleAad:

    def __init__(self, value, tapeIndex, tape):
        self.value = value
        self.tapeIndex = tapeIndex
        self.tape = tape

    def __add__(self, other):
        if isinstance(other, DoubleAad):
            valueOut = self.value + other.value
            index = self.tape.append(TapeEntry(operationType=OperationTypeAad.ADDITION, indexArg1=self.tapeIndex, indexArg2=other.tapeIndex, value=valueOut))
            return DoubleAad(valueOut, index, self.tape)
        else:
            valueOut = self.value + other
            index = self.tape.append(TapeEntry(operationType=OperationTypeAad.ADDITION1, indexArg1=self.tapeIndex, value=valueOut))
            return DoubleAad(valueOut, index, self.tape)

    def __radd__(self, other):
        valueOut = self.value + other
        index =self.tape.append(TapeEntry(operationType=OperationTypeAad.ADDITION1, indexArg1=self.tapeIndex, value=valueOut))
        return DoubleAad(valueOut, index, self.tape)

    def __sub__(self, other):
        if isinstance(other, DoubleAad):
            valueOut = self.value - other.value
            index = self.tape.append(TapeEntry(operationType=OperationTypeAad.SUBTRACTION, indexArg1=self.tapeIndex, indexArg2=other.tapeIndex, value=valueOut))
            return DoubleAad(valueOut, index, self.tape)
        else:
            valueOut = self.value - other
            index = self.tape.append(TapeEntry(operationType=OperationTypeAad.SUBTRACTION1, indexArg1=self.tapeIndex, value=valueOut, extraValue=1))
            return DoubleAad(valueOut, index, self.tape)

    def __rsub__(self, other):
        valueOut = other - self.value
        index = self.tape.append(TapeEntry(operationType=OperationTypeAad.SUBTRACTION1, indexArg1=self.tapeIndex, value=valueOut, extraValue=-1))
        return DoubleAad(valueOut, index, self.tape)

    def __neg__(self):
        valueOut = -self.value
        index = self.tape.append(TapeEntry(operationType=OperationTypeAad.SUBTRACTION1, indexArg1=self.tapeIndex, value=valueOut, extraValue=-1))
        return DoubleAad(valueOut, index, self.tape)

    def __mul__(self, other):
        if isinstance(other, DoubleAad):
            valueOut = self.value * other.value
            index = self.tape.append(TapeEntry(operationType=OperationTypeAad.MULTIPLICATION, indexArg1=self.tapeIndex, indexArg2=other.tapeIndex, value=valueOut))
            return DoubleAad(valueOut, index, self.tape)
        else:
            valueOut = self.value * other
            index = self.tape.append(TapeEntry(operationType=OperationTypeAad.MULTIPLICATION1, indexArg1=self.tapeIndex, value=valueOut, extraValue=other))
            return DoubleAad(valueOut, index, self.tape)

    def __rmul__(self, other):
        valueOut = other * self.value
        index = self.tape.append(TapeEntry(operationType=OperationTypeAad.MULTIPLICATION1, indexArg1=self.tapeIndex, value=valueOut, extraValue=other))
        return DoubleAad(valueOut, index, self.tape)

    def __truediv__(self, other):
        if isinstance(other, DoubleAad):
            valueOut = self.value / other.value
            index = self.tape.append(TapeEntry(operationType=OperationTypeAad.DIVISION, indexArg1=self.tapeIndex, indexArg2=other.tapeIndex, value=valueOut))
            return DoubleAad(valueOut, index, self.tape)
        else:
            valueOut = self.value / other
            index = self.tape.append(TapeEntry(operationType=OperationTypeAad.DIVISION1, indexArg1=self.tapeIndex, value=valueOut, extraValue=other))
            return DoubleAad(valueOut, index, self.tape)

    def __rtruediv__(self, other):
        valueOut = other / self.value
        index = self.tape.append(TapeEntry(operationType=OperationTypeAad.DIVISION2, indexArg1=self.tapeIndex, value=valueOut, extraValue=other))
        return DoubleAad(valueOut, index, self.tape)

    def __pow__(self, other):
        if isinstance(other, DoubleAad):
            valueOut = self.value ** other.value
            index = self.tape.append(TapeEntry(operationType=OperationTypeAad.POW, indexArg1=self.tapeIndex, indexArg2=other.tapeIndex, value=valueOut))
            return DoubleAad(valueOut, index, self.tape)
        else:
            valueOut = self.value ** other
            index = self.tape.append(TapeEntry(operationType=OperationTypeAad.POW1, indexArg1=self.tapeIndex, value=valueOut, extraValue=other))
            return DoubleAad(valueOut, index, self.tape)

    def __rpow__(self, other):
        valueOut = other ** self.value
        index = self.tape.append(TapeEntry(operationType=OperationTypeAad.POW2, indexArg1=self.tapeIndex, value=valueOut, extraValue=other))
        return DoubleAad(valueOut, index, self.tape)

    def sqrt(self):
        valueOut = math.sqrt(self.value)
        index = self.tape.append(TapeEntry(operationType=OperationTypeAad.SQRT, indexArg1=self.tapeIndex, value=valueOut))
        return DoubleAad(valueOut, index, self.tape)

    def exp(self):
        valueOut = math.exp(self.value)
        index = self.tape.append(TapeEntry(operationType=OperationTypeAad.EXP, indexArg1=self.tapeIndex, value=valueOut))
        return DoubleAad(valueOut, index, self.tape)

    def log(self):
        valueOut = math.log(self.value)
        index = self.tape.append(TapeEntry(operationType=OperationTypeAad.LOG, indexArg1=self.tapeIndex, value=valueOut))
        return DoubleAad(valueOut, index, self.tape)

    def normalcdf(self):
        valueOut = norm.cdf(self.value)
        index = self.tape.append(TapeEntry(operationType=OperationTypeAad.NORMALCDF, indexArg1=self.tapeIndex, value=valueOut))
        return DoubleAad(valueOut, index, self.tape)