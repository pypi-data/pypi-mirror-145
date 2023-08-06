"""
Equation from fig8 legend
"""
from math import exp


def reg(x):
    return -2.82 + 17.96 / (1 + exp(-(x - 440) / 246.6))
