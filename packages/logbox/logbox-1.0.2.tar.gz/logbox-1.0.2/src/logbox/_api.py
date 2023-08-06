# Copyright (C) 2021 Matthias Nadig

from ._codes import DEFAULT_STR_INFO, DEFAULT_CHANNEL
from ._logger import _info, _warn, _notify_print
from ._logger import _print_time_since_start, _print_time
from ._logger import _register, _register_progbar

from ._iterators import _log_iter
from ._iterators import _log_range, _log_enumerate, _log_zip


def info(*str_out, channel=DEFAULT_CHANNEL):
    """ Print multiple arguments (info level) """
    _info(*str_out, channel=channel)


def warn(*str_out, channel=DEFAULT_CHANNEL):
    """ Print multiple arguments (warn level) """
    _warn(*str_out, channel=channel)


def register(name_channel, mode='sub', **params):
    """
    Register a new channel
    E.g. different modules can set up their own channels for logging.
    """
    _register(name_channel, mode=mode, **params)


def register_progbar(limit_updates=None, str_info=DEFAULT_STR_INFO, channel=DEFAULT_CHANNEL):
    """
    Register a new progbar
    E.g. done by log_range(...) and other iterators.
    """
    _register_progbar(limit_updates=limit_updates,
                      str_info=str_info,
                      channel=channel)


def notify_print():
    """ Invoke notify_print() to force print of most recent output """
    _notify_print()


def print_time_since_start(*str_out):
    """
    Print the total runtime since the logger has been started
    Note: The time will automatically be appended to the given output string.
    """
    _print_time_since_start(*str_out)


def print_time(*args):
    """
    Print the given time interval (last item of args)
    """
    _print_time(*args)


def log_range(a, b=None, step=1, str_info=DEFAULT_STR_INFO, channel=DEFAULT_CHANNEL):
    """ Use in for-loop instead of range(...) """
    index_start = 0 if b is None else a
    index_stop = a if b is None else b
    return _log_range(index_start, index_stop, step=step, str_info=str_info, channel=channel)


def log_iter(iterable, str_info=DEFAULT_STR_INFO, channel=DEFAULT_CHANNEL):
    """
    Use in for-loop
        `for item in log_iter(some_list):`
    instead of
        `for item in some_list:`
    """
    return _log_iter(iterable, str_info=str_info, channel=channel)


def log_enumerate(iterable, str_info=DEFAULT_STR_INFO, channel=DEFAULT_CHANNEL):
    """ Use in for-loop instead of enumerate(...) """
    return _log_enumerate(iterable, str_info=str_info, channel=channel)


def log_zip(*iterables, str_info=DEFAULT_STR_INFO, channel=DEFAULT_CHANNEL):
    """ Use in for-loop instead of zip(...) """
    return _log_zip(*iterables, str_info=str_info, channel=channel)
