"""
Regression from fig3 legend

Values corrected from typos
"""
from math import exp


def reg_single_leaf(x):
    return -299 + 312 / (1 + exp(-(x + 1258.15) / 411.01))


def reg_natural_bc(x):
    return 7.69 - 8.71 * exp(-x / 619.8)


def reg_restricted_bc(x):
    return -4.12 + 9.2 / (1 + exp(-(x - 101.64) / 346.17))
