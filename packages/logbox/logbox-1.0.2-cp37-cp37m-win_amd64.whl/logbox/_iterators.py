# Copyright (C) 2021 Matthias Nadig

import inspect

from ._codes import DEFAULT_STR_INFO, DEFAULT_CHANNEL
from ._logger import _register_progbar


class IteratorBase:
    def __init__(self,
                 iterator,
                 n_elements,
                 str_info=DEFAULT_STR_INFO,
                 channel=DEFAULT_CHANNEL):
        self.iterator = iterator
        self.n_elements = n_elements
        self.progbar = _register_progbar(limit_updates=self.n_elements,
                                         str_info=str_info,
                                         channel=channel)

    def __len__(self):
        return self.n_elements

    def __enter__(self):
        # When using with-statement (entering)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # When using with-statement (exiting)
        self._on_stop()

    def __iter__(self):
        """ Called when entering the iteration cycle (for-loop) """
        self._on_iter()
        self.progbar.start()
        return self

    def __next__(self):
        """ Called before every step of iteration """

        # Catch StopIteration during _on_next() in case a generator is used
        try:
            # Get next item
            item = self._on_next()

            # Update progbar
            self.progbar.update(1)

            # Yield next item
            return item
        except StopIteration:
            # Clean up before ending the iteration process
            self._on_stop()
            raise StopIteration

    def _on_iter(self):
        pass

    def _on_next(self):
        return next(self.iterator)

    def _on_stop(self):
        self.progbar.stop()

    def add_column(self,
                   name_column, type,
                   show_change_negative=True, show_change_positive=True, show_change_neutral=True,
                   improvement_case='greater'):
        self.progbar.add_column(name_column, type,
                                show_change_negative=show_change_negative,
                                show_change_positive=show_change_positive,
                                show_change_neutral=show_change_neutral,
                                improvement_case=improvement_case)

        return self

    def update_columns(self, values):
        self.progbar.update_columns(values)
        return self


class IteratorLengthKnown(IteratorBase):
    def __init__(self,
                 iterator,
                 n_elements,
                 str_info=DEFAULT_STR_INFO,
                 channel=DEFAULT_CHANNEL):
        super().__init__(iterator, n_elements=n_elements, str_info=str_info, channel=channel)


class IteratorLengthUnknown(IteratorBase):
    def __init__(self,
                 iterator,
                 str_info=DEFAULT_STR_INFO,
                 channel=DEFAULT_CHANNEL):
        super().__init__(iterator, n_elements=None, str_info=str_info, channel=channel)


def _log_range(index_start, index_stop, step=1, str_info=DEFAULT_STR_INFO, channel=DEFAULT_CHANNEL):
    iterable = range(index_start, index_stop, step)
    iterator = iter(iterable)
    return IteratorLengthKnown(iterator, n_elements=len(iterable), str_info=str_info, channel=channel)


def _log_iter(iterable, str_info=DEFAULT_STR_INFO, channel=DEFAULT_CHANNEL, n_elements=None):
    return _iterate_single(iterable, fn_iter=iter, str_info=str_info, channel=channel, n_elements=n_elements)


def _log_enumerate(iterable, str_info=DEFAULT_STR_INFO, channel=DEFAULT_CHANNEL, n_elements=None):
    return _iterate_single(iterable, fn_iter=enumerate, str_info=str_info, channel=channel, n_elements=n_elements)


def _log_zip(*iterables, str_info=DEFAULT_STR_INFO, channel=DEFAULT_CHANNEL, n_elements=None):
    return _iterate_multiple(*iterables, fn_iter=zip, str_info=str_info, channel=channel, n_elements=n_elements)


def _iterate_single(iterable, fn_iter, str_info=DEFAULT_STR_INFO, channel=DEFAULT_CHANNEL, n_elements=None):
    if _check_length_known(iterable):
        n_elements = len(iterable)

    return _build_iterator(iterable, fn_iter=fn_iter, str_info=str_info, channel=channel, n_elements=n_elements)


def _iterate_multiple(*iterables, fn_iter, str_info=DEFAULT_STR_INFO, channel=DEFAULT_CHANNEL, n_elements=None):
    # Check all iterables for their length
    n_elements_found = None
    for iterable in iterables:
        if _check_length_known(iterable):
            if n_elements_found is None:
                n_elements_found = len(iterable)
            else:
                n_elements_found = min(n_elements_found, len(iterable))
        else:
            # Current iterable is a generator or other kind of iterable of undetermined length
            # (--> has no specific length and might be shorter than other iterators)
            break
    else:
        # If for-loop has not been broken, overwrite n_elements
        n_elements = n_elements_found

    return _build_iterator(*iterables, fn_iter=fn_iter, str_info=str_info, channel=channel, n_elements=n_elements)


def _build_iterator(*iterables, fn_iter, str_info=DEFAULT_STR_INFO, channel=DEFAULT_CHANNEL, n_elements=None):
    iterator = _start_iterator(*iterables, fn_iter=fn_iter)

    if n_elements is None:
        return IteratorLengthUnknown(iterator, str_info=str_info, channel=channel)
    else:
        return IteratorLengthKnown(iterator, n_elements=n_elements, str_info=str_info, channel=channel)
    
    
def _check_length_known(iterable):
    return hasattr(iterable, '__len__')


def _require_iterable(iterable):
    if hasattr(iterable, '__iter__'):
        iterable = iterable
    elif inspect.isgeneratorfunction(iterable):
        iterable = iterable()
    else:
        raise ValueError('Must receive an iterable or a generator function, got {}'.format(type(iterable)))

    return iterable


def _start_iterator(*iterables, fn_iter):
    iterator = fn_iter(*(_require_iterable(iterable) for iterable in iterables))
    return iterator


def _check_generator(gen):
    return inspect.isgenerator(gen) or inspect.isgeneratorfunction(gen)


def _require_generator(gen):
    """ Helper that checks for generator function, in case not given the generator directly """
    if inspect.isgenerator(gen):
        pass
    elif inspect.isgeneratorfunction(gen):
        # raise ValueError('Got a generator function that must be invoked first')
        gen = gen()
    else:
        raise ValueError('Must be given either generator or generator function, got {}'.format(type(gen)))

    return gen
