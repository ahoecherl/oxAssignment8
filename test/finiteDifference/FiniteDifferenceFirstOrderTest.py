import unittest
from finiteDifference.FiniteDifferenceFirstOrder import differentiate

class FiniteDifferenceFirstOrderTest(unittest.TestCase):

    def setUp(self):
        self.x = 2
        self.y = 3
        self.eps =0.001

    def test(self):
        def t_fun(x, y):
            return x**4 + y**3
        derivatives = differentiate(t_fun, self.x, self.y, epsilon=self.eps)
        self.assertAlmostEqual(4*self.x**3, derivatives[0], places=1)
        self.assertAlmostEqual(3*self.y**2, derivatives[1], places=1)


if __name__ == '__main__':
    unittest.main()