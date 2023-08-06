"""
Regression from fig10 legend

Typos have been corrected
"""
from math import exp


def reg_a(x):
    return -2.65 + 22.27 / (1 + exp(-(x - 3.86) / 0.85))


def reg_b(x):
    return 19.49 - 41.74 * exp(-x)
