import unittest
from finance.BlackScholesOptionPricer import *
from finiteDifference.FiniteDifferenceFirstOrder import differentiate
from automaticDifferentiation.DoubleAad import DoubleAad
from automaticDifferentiation.Tape import Tape
from automaticDifferentiation.TapeEntry import TapeEntry
from automaticDifferentiation.OperationTypeAad import OperationTypeAad
from automaticDifferentiation.TapeUtils import interpret

class BlackScholesFormulaTest(unittest.TestCase):

    def setUp(self):
        self.St = 20
        self.sigma = 0.80
        self.K = 17
        self.tau = 3
        self.r = 0.1
        self.input = (self.St, self.sigma, self.K, self.tau, self.r)

        self.tape = Tape()
        self.St_aaad = DoubleAad(self.St, 0, self.tape)
        self.tape.append(TapeEntry(OperationTypeAad.INPUT, self.St_aaad.value))
        self.sigma_aaad = DoubleAad(self.sigma, 1, self.tape)
        self.tape.append(TapeEntry(OperationTypeAad.INPUT, self.sigma_aaad.value))
        self.K_aaad = DoubleAad(self.K, 2, self.tape)
        self.tape.append(TapeEntry(OperationTypeAad.INPUT, self.K_aaad.value))
        self.tau_aaad = DoubleAad(self.tau, 3, self.tape)
        self.tape.append(TapeEntry(OperationTypeAad.INPUT, self.tau_aaad.value))
        self.r_aaad = DoubleAad(self.r, 4, self.tape)
        self.tape.append((TapeEntry(OperationTypeAad.INPUT, self.r_aaad.value)))
        self.input_aaad = (self.St_aaad, self.sigma_aaad, self.K_aaad, self.tau_aaad, self.r_aaad)

    def test_prices(self):
        call_price = BSPrice_Analytical(*self.input, True)['price']
        put_price = BSPrice_Analytical(*self.input, False)['price']
        self.assertAlmostEqual(call_price, BSPrice(*self.input, True), places=6)
        self.assertAlmostEqual(put_price, BSPrice(*self.input, False), places=6)
        self.assertAlmostEqual(call_price, BSPrice_SAD(*self.input, True)['price'], places=6)
        self.assertAlmostEqual(put_price, BSPrice_SAD(*self.input, False)['price'], places=6)
        self.assertAlmostEqual(call_price, BSPrice_AAD(*self.input, True)['price'], places=6)
        self.assertAlmostEqual(put_price, BSPrice_AAD(*self.input, False)['price'], places=6)

    def test_delta(self):
        call_delta = BSPrice_Analytical(*self.input, True)['derivatives'][0]
        put_delta = BSPrice_Analytical(*self.input, False)['derivatives'][0]
        self.assertAlmostEqual(call_delta, differentiate(BSPrice, *self.input, True)[0], places=3)
        self.assertAlmostEqual(put_delta, differentiate(BSPrice, *self.input, False)[0], places=3)
        self.assertAlmostEqual(call_delta, BSPrice_SAD(*self.input, True)['derivatives'][0], places=8)
        self.assertAlmostEqual(put_delta, BSPrice_SAD(*self.input, False)['derivatives'][0], places=8)
        self.assertAlmostEqual(call_delta, BSPrice_AAD(*self.input, True)['derivatives'][0], places=8)
        self.assertAlmostEqual(put_delta, BSPrice_AAD(*self.input, False)['derivatives'][0], places=8)

    def test_vega(self):
        call_vega = BSPrice_Analytical(*self.input, True)['derivatives'][1]
        put_vega = BSPrice_Analytical(*self.input, False)['derivatives'][1]
        self.assertAlmostEqual(call_vega, differentiate(BSPrice, *self.input, True)[1], places=3)
        self.assertAlmostEqual(put_vega, differentiate(BSPrice, *self.input, False)[1], places=3)
        self.assertAlmostEqual(call_vega, BSPrice_SAD(*self.input, True)['derivatives'][1], places=8)
        self.assertAlmostEqual(put_vega, BSPrice_SAD(*self.input, False)['derivatives'][1], places=8)
        self.assertAlmostEqual(call_vega, BSPrice_AAD(*self.input, True)['derivatives'][1], places=8)
        self.assertAlmostEqual(put_vega, BSPrice_AAD(*self.input, False)['derivatives'][1], places=8)

    def test_Kpoint(self):
        call_KPoint = differentiate(BSPrice, *self.input, True)[2]
        self.assertAlmostEqual(call_KPoint, BSPrice_SAD(*self.input, True)['derivatives'][2], places=4)
        self.assertAlmostEqual(call_KPoint, BSPrice_AAD(*self.input, True)['derivatives'][2], places=4)

    def test_theta(self):
        call_theta = -1 * BSPrice_Analytical(*self.input, True)['derivatives'][3]
        put_theta = -1 * BSPrice_Analytical(*self.input, False)['derivatives'][3]
        self.assertAlmostEqual(call_theta, differentiate(BSPrice, *self.input, True)[3], places=3)
        self.assertAlmostEqual(put_theta, differentiate(BSPrice, *self.input, False)[3], places=3)
        self.assertAlmostEqual(call_theta, BSPrice_SAD(*self.input, True)['derivatives'][3], places=8)
        self.assertAlmostEqual(put_theta, BSPrice_SAD(*self.input, False)['derivatives'][3], places=8)
        self.assertAlmostEqual(call_theta, BSPrice_AAD(*self.input, True)['derivatives'][3], places=8)
        self.assertAlmostEqual(put_theta, BSPrice_AAD(*self.input, False)['derivatives'][3], places=8)

    def test_rho(self):
        call_rho = BSPrice_Analytical(*self.input, True)['derivatives'][4]
        put_rho = BSPrice_Analytical(*self.input, False)['derivatives'][4]
        self.assertAlmostEqual(call_rho, differentiate(BSPrice, *self.input, True)[4], places=3)
        self.assertAlmostEqual(put_rho, differentiate(BSPrice, *self.input, False)[4], places=3)
        self.assertAlmostEqual(call_rho, BSPrice_SAD(*self.input, True)['derivatives'][4], places=8)
        self.assertAlmostEqual(put_rho, BSPrice_SAD(*self.input, False)['derivatives'][4], places=8)
        self.assertAlmostEqual(call_rho, BSPrice_AAD(*self.input, True)['derivatives'][4], places=8)
        self.assertAlmostEqual(put_rho, BSPrice_AAD(*self.input, False)['derivatives'][4], places=8)

    def test_aaad(self):
        call = BSPrice_Analytical(*self.input, True)
        aaad_price = BSPrice_AAAD(*self.input_aaad, True)
        aaad_derivatives = interpret(aaad_price.tape)
        self.assertAlmostEqual(call['price'], aaad_price.value, places=8)
        self.assertAlmostEqual(call['derivatives'][0], aaad_derivatives[0], places=8)
        self.assertAlmostEqual(call['derivatives'][1], aaad_derivatives[1], places=8)
        self.assertAlmostEqual(-call['derivatives'][3], aaad_derivatives[3], places=8)
        self.assertAlmostEqual(call['derivatives'][4], aaad_derivatives[4], places=8)

if __name__ == '__main__':
    unittest.main()