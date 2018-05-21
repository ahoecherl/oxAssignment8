from finance.BlackScholesOptionPricer import *
from finiteDifference.FiniteDifferenceFirstOrder import differentiate
from automaticDifferentiation.DoubleAad import DoubleAad
from automaticDifferentiation.Tape import Tape
from automaticDifferentiation.TapeUtils import interpret
from automaticDifferentiation.TapeEntry import TapeEntry
from automaticDifferentiation.OperationTypeAad import OperationTypeAad
import timeit

option = [0] * 2

option[0] = (10, .23, 8, .4, 0.2, True)
option[1] = (12, .05, 18, .02, .1, False)


aaad_option = [0] * 2
tapes = [0] * 2
tapes[0] = Tape()
aaad_option[0] = (DoubleAad(10, 0, tapes[0]), DoubleAad(.23, 1, tapes[0]), DoubleAad(8, 2, tapes[0]), DoubleAad(.4, 3, tapes[0]), DoubleAad(.2, 4, tapes[0]), True)
tapes[1] = Tape()
aaad_option[1] = (DoubleAad(12, 0, tapes[1]), DoubleAad(.05, 1, tapes[1]), DoubleAad(18, 2, tapes[1]), DoubleAad(.02, 3, tapes[1]), DoubleAad(.1, 4, tapes[1]), True)

def price_only():
    for i in range(0, option.__len__()):
        price = BSPrice(*option[i])

def forward_bump_derivatives():
    for i in range(0, option.__len__()):
        price = differentiate(BSPrice, *option[i])

def analytical_derivatives():
    for i in range(0, option.__len__()):
        result = BSPrice_Analytical(*option[i])

def SAD_derivatives():
    for i in range(0, option.__len__()):
        result = BSPrice_SAD(*option[i])

def AAD_derivatives():
    for i in range(0, option.__len__()):
        result = BSPrice_AAD(*option[i])

def AAAD_derivatives():
    for i in range(0, aaad_option.__len__()):
        for j in range(0, aaad_option[i].__len__()-1):
            aaad_option[i][j].tape.append(TapeEntry(OperationTypeAad.INPUT, aaad_option[i][j].value))
        result = BSPrice_AAAD(*aaad_option[i])
        derivatives = interpret(result.tape)
        result.tape.clr()

print('Time for 5000 pricings')
print(timeit.timeit(lambda: price_only(), number=1000))
print('Time for 5000 pricings with analytical delta, vega, theta, rho')
print(timeit.timeit(lambda: analytical_derivatives(), number=1000))
print('Time for 5000 pricings and derivatives with forward Bump')
print(timeit.timeit(lambda: forward_bump_derivatives(), number=1000))
print('Time for 5000 pricings and derivatives with SAD')
print(timeit.timeit(lambda: SAD_derivatives(), number=1000))
print('Time for 5000 pricings and derivatives with AAD')
print(timeit.timeit(lambda: AAD_derivatives(), number=1000))
print('Time for 5000 pricings and derivatives with AAAD')
print(timeit.timeit(lambda: AAAD_derivatives(), number=1000))
asdf=1
