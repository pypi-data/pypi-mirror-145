"""
Regression from fig6 legend
"""


def reg_sva(x):
    """

    Args:
        x (float): number of days since 1st of august

    Returns:

    """
    return 32.9 + 3.7 * x - 0.034 * x ** 2
