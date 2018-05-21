Automatic Algorithmic Adjoint Differentiation for finance in Python
============

This library has been created as part of an Assignment at the Financial Mathematics part-time Master studies at Oxford University by Andreas Höcherl.

The library implements different ways of calculating derivatives for of the Black-Scholes-Formula and a specific pricing problem requiring Monte Carlo Simulation.
The approaches include
1. Forward bump and revalue
2. The direct formulas for the derivatives as found in the literature
3. Manual "Standard" or "Forward" algorithmic differentiation
4. Manual "Adjoint" of "Backward" algorithmic differentiation
5. Automatic adjoint algorithmic differentiation

The main scripts which execute a performance comparison between the different approaches are
1. 'test/BlackScholesDerivatives_SpeedComparison.py'

The 'automaticDifferentiation' subfolder is mostly a python port of the java code accompanying the book [Algorithmic Differentiation In Finance Explained] (https://www.palgrave.com/gp/book/9783319539782) by Marc Henrard.
