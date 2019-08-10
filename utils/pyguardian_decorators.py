import inspect
import time
from functools import wraps

from tabulate import tabulate

from pyguardian.utils.pyguardian_logging import PyGuardianLogger


def tabulate_me(pyguardian_static_method):
    """
    Gratuitous decorator function that tabulates
    data returned by the decorated function

    :param pyguardian_static_method: only used on
    PyGuardian static methods... So far
    :return: tabulated data
    """

    @wraps(pyguardian_static_method)
    def wrapper(*args, **kwargs):
        data = pyguardian_static_method(*args, **kwargs)
        if pyguardian_static_method.__name__ == "fetch_eq" or "fetch_vault":
            return tabulate(data, tablefmt="fancy_grid")

        return tabulate(data, headers="keys", tablefmt="fancy_grid")

    return wrapper


def log_me(json_func):
    """
    Another gratuitous decorator function for
    logging a json_funcs function's arguments
    at the start and the end of the function

    :param json_func: one of the functions from
    the json_funcs module
    :return: data processed from API data
    """

    @wraps(json_func)
    def wrapper(*args, **kwargs):
        log = PyGuardianLogger(inspect.getfile(json_func).split('/')[-1])
        arg_types = inspect.getfullargspec(json_func)
        log.info(f"{json_func.__name__}() started with args: {arg_types.args}")
        start = time.time()
        data = json_func(*args, **kwargs)
        finish = time.time()
        log.info(f"{json_func.__name__}() finished in {finish - start}")
        return data

    return wrapper
