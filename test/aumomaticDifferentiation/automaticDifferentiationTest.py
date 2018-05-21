from automaticDifferentiation.Tape import Tape
from automaticDifferentiation.DoubleAad import DoubleAad
from automaticDifferentiation.TapeEntry import TapeEntry
from automaticDifferentiation.OperationTypeAad import OperationTypeAad
from automaticDifferentiation.TapeUtils import interpret
from scipy.stats import norm

import math
import unittest

class TapeTest(unittest.TestCase):

    def setUp(self):
        self.tape = Tape()
        self.input1 = DoubleAad(3, 0, self.tape)
        self.tape.append(TapeEntry(OperationTypeAad.INPUT, self.input1.value))
        self.input2 = DoubleAad(5, 1, self.tape)
        self.tape.append(TapeEntry(OperationTypeAad.INPUT, self.input2.value))

    def test_add_1(self):
        var2 = self.input1+self.input2
        constant = 4
        var3 = var2 + constant
        self.assertEqual(var3.value, 12)

    def test_add_2(self):
        res = 1 + self.input1
        self.assertEqual(res.value, 4)

    def test_add_3(self):
        var2 = self.input1 + self.input2
        constant = 4
        var3 = var2 + constant
        derivatives = interpret(self.tape)
        self.assertEqual(derivatives[0], 1)
        self.assertEqual(derivatives[1], 1)

    def test_mul_1(self):
        var1 = self.input1*3
        var2 = var1 * self.input2
        derivatives = interpret(self.tape)
        self.assertEqual(derivatives[0], 15)
        self.assertEqual(derivatives[1], 9)

    def test_mul_2(self):
        res = 2*self.input1*self.input2*3
        derivatives = interpret(self.tape)
        self.assertEqual(res.value, 90)
        self.assertEqual(derivatives[0], 30)
        self.assertEqual(derivatives[1], 18)

    def test_min_1(self):
        res = self.input1 - self.input2
        derivatives = interpret(self.tape)
        self.assertEqual(derivatives[0], 1)
        self.assertEqual(derivatives[1], -1)

    def test_min_2(self):
        res = 5.0 - self.input1 - 4 - self.input2
        derivatives = interpret(self.tape)
        self.assertEqual(derivatives[0], -1)
        self.assertEqual(derivatives[1], -1)

    def test_min_3(self):
        res = 1 - self.input1
        derivatives = interpret(self.tape)
        self.assertEqual(derivatives[0], -1)

    def test_min_4(self):
        res = self.input1 - 2
        derivatives = interpret(self.tape)
        self.assertEqual(derivatives[0], 1)

    def test_div1(self):
        res = self.input1/5
        derivatives = interpret(self.tape)
        self.assertEqual(derivatives[0], .2)

    def test_div2(self):
        res = 5/self.input1
        derivatives = interpret(self.tape)
        self.assertEqual(derivatives[0], -5/9)

    def test_div3(self):
        res = self.input2/self.input1
        derivatives = interpret(self.tape)
        self.assertEqual(derivatives[0], -5/9)
        self.assertEqual(derivatives[1], 1/3)

    def test_div_sub_combo(self):
        var1 = self.input1-self.input2
        var2 = self.input1 * self.input2
        var3 = var1/(2*var2)
        derivatives = interpret(self.tape)
        self.assertEqual(derivatives[0], 1/18)
        self.assertEqual(derivatives[1], -1/50)

    def test_div4(self):
        res = 1/(2*self.input1*self.input2)
        derivatives = interpret(self.tape)
        self.assertEqual(derivatives[0], -1/(45*2))
        self.assertAlmostEqual(derivatives[1], -1/(75*2), places=8)

    def test_div5(self):
        res = 1/(self.input1 - self.input2)
        derivatives = interpret(self.tape)
        self.assertEqual(derivatives[0], -1/4)
        self.assertEqual(derivatives[1], 1/4)

    def test_pow1(self):
        res = self.input1**2
        derivatives = interpret(self.tape)
        self.assertEqual(res.value, 9)
        self.assertEqual(derivatives[0], 6)

    def test_pow2(self):
        res = self.input2 ** self.input1
        derivatives = interpret(self.tape)
        self.assertEqual(res.value, 125)
        self.assertEqual(derivatives[0], (5 ** 3 * math.log(5)))
        self.assertEqual(derivatives[1], 75)

    def test_pow3(self):
        res = 4 ** self.input1
        derivatives = interpret(self.tape)
        self.assertEqual(res.value, 64)
        self.assertEqual(derivatives[0], 4**self.input1.value * math.log(4))

    def test_sqrt(self):
        res = self.input1.sqrt()
        derivatives = interpret(self.tape)
        self.assertEqual(res.value, math.sqrt(3))
        self.assertEqual(derivatives[0], 0.5/math.sqrt(3))

    def test_log(self):
        res = self.input1.log()
        derivative = interpret(self.tape)
        self.assertEqual(res.value, math.log(3))
        self.assertEqual(derivative[0], 1/3)

    def test_exp(self):
        res = self.input1.exp()
        derivative = interpret(self.tape)
        self.assertEqual(res.value, math.exp(3))
        self.assertEqual(derivative[0], math.exp(3))

    def test_normalcdf(self):
        res = self.input1.normalcdf()
        derivative = interpret(self.tape)
        self.assertEqual(res.value, norm.cdf(3))
        self.assertEqual(derivative[0], norm.pdf(3))

    def test_negate(self):
        res = -self.input1
        derivative = interpret(res.tape)
        self.assertEqual(-3, res.value)
        self.assertEqual(derivative[0], -1)

if __name__ == '__main__':
    unittest.main()