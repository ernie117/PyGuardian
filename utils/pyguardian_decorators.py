from functools import wraps

from tabulate import tabulate


def tabulate_me(pyguardian_static_method):
    """
    Gratuitous decorator function that tabulates data
    returned by the decorated function

    :param pyguardian_static_method: only used on
    PyGuardian static methods... So far
    :return: tabulated data
    """

    @wraps(pyguardian_static_method)
    def tabulate_guardian_data(*args):
        data = pyguardian_static_method(*args)
        return tabulate(data, headers="keys", tablefmt="fancy_grid")

    return tabulate_guardian_data
