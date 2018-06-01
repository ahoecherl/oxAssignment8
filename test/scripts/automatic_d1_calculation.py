import unittest
from finance.BlackScholesOptionPricer import *
from finiteDifference.FiniteDifferenceFirstOrder import differentiate
from automaticDifferentiation.DoubleAad import DoubleAad
from automaticDifferentiation.Tape import Tape
from automaticDifferentiation.TapeEntry import TapeEntry
from automaticDifferentiation.OperationTypeAad import OperationTypeAad
from automaticDifferentiation.TapeUtils import interpret

tape = Tape()
sigma_hat = DoubleAad(0.2*math.sqrt(0.5), 0, tape)
tape.append(TapeEntry(OperationTypeAad.INPUT, sigma_hat.value))
S_t = DoubleAad(20, 1, tape)
tape.append(TapeEntry(OperationTypeAad.INPUT, S_t.value))
K = DoubleAad(25, 2, tape)
tape.append(TapeEntry(OperationTypeAad.INPUT, K.value))
r = DoubleAad(0.05, 3, tape)
tape.append(TapeEntry(OperationTypeAad.INPUT, r.value))
sigma = DoubleAad(0.2, 4, tape)
tape.append(TapeEntry(OperationTypeAad.INPUT, sigma.value))
tau = DoubleAad(0.5, 5, tape)
tape.append(TapeEntry(OperationTypeAad.INPUT, tau.value))

d1 = 1/sigma_hat * ((S_t/K).log()+(r+sigma**2/2)*tau)
interpret(tape)
print(tape)
asdf=1