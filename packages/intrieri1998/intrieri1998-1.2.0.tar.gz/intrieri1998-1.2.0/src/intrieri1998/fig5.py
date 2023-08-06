"""
Equation from fig5 legend
"""


def ns_reg(x):
    return 0.19 + 0.0022 * x + 8.04e-6 * x ** 2 - 4.7e-9 * x ** 3


def ew_reg(x):
    return 0.19 + 0.0027 * x
