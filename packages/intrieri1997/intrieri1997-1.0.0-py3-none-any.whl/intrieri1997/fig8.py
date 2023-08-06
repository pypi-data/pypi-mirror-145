"""
Regression from fig8 legend
"""
from math import log


def reg_tva(x):
    return 101.9 - 0.654 * x * log(x)
