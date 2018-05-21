from scipy.stats import norm
from automaticDifferentiation.OperationTypeAad import OperationTypeAad as ot
import math

NORMAL = norm(0, 1)

def interpret(tape):
    nbEntries = tape.size
    tape.tapeList[nbEntries-1].addValueBar(1.0)
    derivativesList = []
    for i in range(nbEntries-1, -1, -1):
        entry = tape.tapeList[i]
        if entry.operationType == ot.INPUT:
            derivativesList.append(entry.valueBar)
        elif entry.operationType == ot.ADDITION:
            tape.tapeList[entry.indexArg1].addValueBar(entry.valueBar)
            tape.tapeList[entry.indexArg2].addValueBar(entry.valueBar)
        elif entry.operationType == ot.ADDITION1:
            tape.tapeList[entry.indexArg1].addValueBar(entry.valueBar)
        elif entry.operationType == ot.MULTIPLICATION:
            tape.tapeList[entry.indexArg1].addValueBar(tape.tapeList[entry.indexArg2].value * entry.valueBar)
            tape.tapeList[entry.indexArg2].addValueBar(tape.tapeList[entry.indexArg1].value * entry.valueBar)
        elif entry.operationType == ot.MULTIPLICATION1:
            tape.tapeList[entry.indexArg1].addValueBar(entry.extraValue * entry.valueBar)
        elif entry.operationType == ot.SUBTRACTION:
            tape.tapeList[entry.indexArg1].addValueBar(entry.valueBar)
            tape.tapeList[entry.indexArg2].addValueBar(-entry.valueBar)
        elif entry.operationType == ot.SUBTRACTION1:
            tape.tapeList[entry.indexArg1].addValueBar(entry.valueBar*entry.extraValue)
        elif entry.operationType == ot.DIVISION:
            tape.tapeList[entry.indexArg1].addValueBar(entry.valueBar/tape.tapeList[entry.indexArg2].value)
            tape.tapeList[entry.indexArg2].addValueBar(-tape.tapeList[entry.indexArg1].value/(tape.tapeList[entry.indexArg2].value * tape.tapeList[entry.indexArg2].value)*entry.valueBar)
        elif entry.operationType == ot.DIVISION1:
            tape.tapeList[entry.indexArg1].addValueBar(entry.valueBar / entry.extraValue)
        elif entry.operationType == ot.DIVISION2:
            tape.tapeList[entry.indexArg1].addValueBar(-entry.extraValue / (tape.tapeList[entry.indexArg1].value * tape.tapeList[entry.indexArg1].value) * entry.valueBar)
        elif entry.operationType == ot.POW:
            x = tape.tapeList[entry.indexArg1].value
            y = tape.tapeList[entry.indexArg2].value
            tape.tapeList[entry.indexArg1].addValueBar(y * entry.value / x * entry.valueBar)
            tape.tapeList[entry.indexArg2].addValueBar(entry.value * math.log(x) * entry.valueBar)
        elif entry.operationType == ot.POW1:
            tape.tapeList[entry.indexArg1].addValueBar(entry.extraValue * entry.value / tape.tapeList[entry.indexArg1].value*entry.valueBar)
        elif entry.operationType == ot.POW2:
            tape.tapeList[entry.indexArg1].addValueBar(entry.value * math.log(entry.extraValue) * entry.valueBar)
        elif entry.operationType == ot.SQRT:
            tape.tapeList[entry.indexArg1].addValueBar(.5 / entry.value * entry.valueBar)
        elif entry.operationType == ot.LOG:
            tape.tapeList[entry.indexArg1].addValueBar(entry.valueBar/tape.tapeList[entry.indexArg1].value)
        elif entry.operationType == ot.EXP:
            tape.tapeList[entry.indexArg1].addValueBar(entry.valueBar * math.exp(tape.tapeList[entry.indexArg1].value))
        elif entry.operationType == ot.NORMALCDF:
            tape.tapeList[entry.indexArg1].addValueBar(entry.valueBar * norm.pdf(tape.tapeList[entry.indexArg1].value))
    nbDerivatives = derivativesList.__len__()
    derivatives = [0.0] * nbDerivatives
    for i in range(0, nbDerivatives):
        derivatives[i] = derivativesList[nbDerivatives-1-i]
    return derivatives
