import inspect
import platform
import re
import time
from functools import wraps

from tabulate import tabulate

from pyguardian.utils.pyguardian_logging import PyGuardianLogger


def tabulate_me(pyguardian_static_method):
    """
    Gratuitous decorator function that tabulates
    data returned by the decorated function

    :param pyguardian_static_method: only used on
    pyguardian static methods... So far
    :return: tabulated data
    """

    @wraps(pyguardian_static_method)
    def wrapper(*args, **kwargs):
        data = pyguardian_static_method(*args, **kwargs)
        if pyguardian_static_method.__name__ in ("fetch_eq", "fetch_vault"):
            return tabulate(data, tablefmt="fancy_grid")
        if isinstance(data, tuple):
            tables = []
            for datum in data:
                tables.append(tabulate(datum, tablefmt="fancy_grid"))

            return tables

        return tabulate(data, headers="keys", tablefmt="fancy_grid")

    return wrapper


def log_me(function_to_log):
    """
    Another gratuitous decorator function for
    logging a function's arguments and timing
    the function's execution

    :param function_to_log: some function from
    this package
    :return: various functions
    """

    @wraps(function_to_log)
    def wrapper(*args, **kwargs):
        delimiter = '\\' if platform.system().lower() == "windows" else '/'
        log = PyGuardianLogger(inspect.getfile(function_to_log).split(delimiter)[-1])
        log.info(f"{function_to_log.__name__}() started.")
        start = time.time()
        data = function_to_log(*args, **kwargs)
        finish = time.time()
        log.info(f"{function_to_log.__name__}() finished in {finish - start}")

        return data

    return wrapper
