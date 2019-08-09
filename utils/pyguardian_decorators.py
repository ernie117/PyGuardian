from functools import wraps
from tabulate import tabulate


def tabulate_me(pyguardian_static_method):
    @wraps(pyguardian_static_method)
    def tabulate_guardian_data(*args):
        data = pyguardian_static_method(*args)
        return tabulate(data, headers="keys", tablefmt="fancy_grid")
    return tabulate_guardian_data

