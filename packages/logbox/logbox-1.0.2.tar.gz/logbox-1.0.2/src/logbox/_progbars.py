# Copyright (C) 2021 Matthias Nadig

import numpy as np
import time

from ._codes import PROGBAR_BG_LEFT, PROGBAR_BG_RIGHT
from ._codes import PROGBAR_FG_LEFT, PROGBAR_FG_RIGHT
from ._codes import RESET
from ._codes import COLOR_NEGATIVE
from ._codes import COLOR_NEUTRAL
from ._codes import COLOR_POSITIVE
from ._codes import DEFAULT_STR_INFO
from ._codes import PROGBAR_INIT, PROGBAR_ACTIVE, PROGBAR_DONE


class ProgbarBase:
    def __init__(self,
                 callback_on_update=None,
                 str_info=DEFAULT_STR_INFO, n_decimals=3,
                 leading_line='oneliner', style=''):
        self.str_info = str_info
        self.n_decimals = n_decimals
        self.callback_on_update = callback_on_update
        self.style = style

        self.index_update = 0

        self.columns = []

        self.is_table = leading_line == 'table'
        self.delimiter_columns = ' | ' if self.is_table else ', '  # ' - '
        self.str_columns_leading_line = ''
        self.str_columns_headline = ''
        self.str_progress = ''

        self.t_start = None
        self.t_stop = None

        self.n_chars_progress_visible = 0

        self.steps_progbar = 20
        self.state = PROGBAR_INIT

    def __enter__(self):
        # When using with-statement (entering)
        self._on_start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # When using with-statement (exiting)
        self._on_stop()

    def start(self):
        self._on_start()

    def stop(self):
        self._on_stop()

    def _on_start(self):
        self._reset()
        self.t_start = time.time()
        self._initial_update()
        self.state = PROGBAR_ACTIVE

    def _on_stop(self):
        # Exit the line that has been used to show updates of progress bar
        if self.state != PROGBAR_DONE:
            self.t_stop = time.time()
            self.state = PROGBAR_DONE
            self._final_update()

    def _reset(self):
        self._init_columns()
        self.str_progress = ''
        self.index_update = 0

    def _parse_progress(self, i, is_intermediate=True):
        raise RuntimeError('Method should be overwritten by child of type {}'.format(type(self)))

    def update(self, n_updates):
        self._update(n_updates)

    def _initial_update(self):
        self._update(0, is_intermediate=False)

    def _final_update(self):
        self._update(0, is_intermediate=False)

    def _track_length_of_leading_line(self, str_counter):
        # For parsing headline
        self.n_chars_progress_visible = 2 + len(self.str_info) + len(str_counter) + self.steps_progbar

    def _update(self, n_updates, is_intermediate=True):
        self.index_update += n_updates
        self.str_progress = self._parse_progress(self.index_update, is_intermediate=is_intermediate)
        self.callback_on_update()

    def add_column(self,
                   name_column, type,
                   n_decimals=3, leading_chars=3,
                   show_change_negative=True, show_change_positive=True, show_change_neutral=True,
                   improvement_case='greater'):
        """ Add updatable column containing some value to progress bar """

        # Assemble and add a new column
        if self.is_table:
            column = ColumnTable(name_column, type,
                                 n_decimals=n_decimals, leading_chars=leading_chars,
                                 show_change_negative=show_change_negative,
                                 show_change_neutral=show_change_neutral,
                                 show_change_positive=show_change_positive)
        else:
            column = ColumnOneliner(name_column, type,
                                    n_decimals=n_decimals, leading_chars=leading_chars,
                                    show_change_negative=show_change_negative,
                                    show_change_neutral=show_change_neutral,
                                    show_change_positive=show_change_positive,
                                    improvement_case=improvement_case)
        self.columns.append(column)

        return self

    def _init_columns(self):
        # Reinitialize column string for first print of progbar
        values_init = []
        for column in self.columns:
            values_init.append(column.value)
        self.update_columns(values_init)

    def parse_leading_line(self):
        return self.str_progress + self.str_columns_leading_line

    def parse_headline(self):
        return ' ' * self.n_chars_progress_visible + self.str_columns_headline

    def update_columns(self, values):
        self.str_columns_leading_line = ''
        self.str_columns_headline = ''
        for value, column in zip(values, self.columns):
            self.str_columns_leading_line += self.delimiter_columns + column.parse_leading_line(value)
            if self.is_table:
                self.str_columns_headline += self.delimiter_columns + column.get_headline(value)

        self.callback_on_update()

        return self


class ProgbarKnownLength(ProgbarBase):
    def __init__(self,
                 limit_updates,
                 callback_on_update=None,
                 str_info=DEFAULT_STR_INFO, n_decimals=3,
                 leading_line='oneliner', style=''):
        super().__init__(callback_on_update=callback_on_update, str_info=str_info, n_decimals=n_decimals, leading_line=leading_line, style=style)

        if isinstance(limit_updates, float) and limit_updates == int(limit_updates):
            limit_updates = int(limit_updates)
        if not isinstance(limit_updates, int):
            raise TypeError('Expected integer for limit_updates, got value {} of type {}'.format(limit_updates, type(limit_updates)))
        self.limit_updates = limit_updates

        self.str_counter_template = '#{:d}' + '/{:d}'.format(self.limit_updates)
        self.str_percent_template = '({:' + str(4 + self.n_decimals) + '.' + str(self.n_decimals) + 'f}%)'

    def _parse_progress(self, i, is_intermediate=True):
        str_counter = self._parse_counter(i)
        str_progbar = self._parse_progbar(self.index_update - is_intermediate)
        str_progress = ' '.join([str_progbar + self.style, self.str_info, str_counter])
        return str_progress

    def _parse_progbar(self, i):
        ratio = i / self.limit_updates
        n_steps_done = int(round(ratio * self.steps_progbar))

        ratio_parsed = np.round(100 * i / self.limit_updates, decimals=self.n_decimals)
        str_percent = self.str_percent_template.format(ratio_parsed)

        n_chars_left = int(np.ceil((self.steps_progbar - len(str_percent)) / 2))
        n_chars_right = self.steps_progbar - (n_chars_left + len(str_percent))
        str_progbar = \
            ''.join(np.repeat(' ', n_chars_left)) + \
            str_percent + \
            ''.join(np.repeat(' ', n_chars_right))

        str_progbar = \
            PROGBAR_BG_LEFT + PROGBAR_FG_LEFT + str_progbar[:n_steps_done] + \
            PROGBAR_BG_RIGHT + PROGBAR_FG_RIGHT + str_progbar[n_steps_done:] + \
            RESET

        return str_progbar

    def _parse_counter(self, i):
        # Counter string should show iteration number currently in process, progress bar should
        # show ratio of iterations done. Example:
        #   - While in last iteration:  "[====90%== ] Loading file #10/10"
        #   - After last iteration:     "[===100%===] Loading file #10/10"
        str_counter = self.str_counter_template.format(i)
        self._track_length_of_leading_line(str_counter)
        return str_counter


class ProgbarUnknownLength(ProgbarBase):
    def __init__(self,
                 callback_on_update=None,
                 str_info=DEFAULT_STR_INFO, n_decimals=3,
                 leading_line='oneliner', style=''):
        super().__init__(callback_on_update=callback_on_update, str_info=str_info, n_decimals=n_decimals, leading_line=leading_line, style=style)

        self.str_counter_template = '#{:d}'

    def _parse_progress(self, i, is_intermediate=True):
        str_counter = self._parse_counter(i)
        str_progress = self.style + ' '.join([self.str_info, str_counter])
        return str_progress

    def _parse_counter(self, i):
        # Counter string should show iteration number currently in process, progress bar should
        # show ratio of iterations done. Example:
        #   - While in last iteration:  "[====90%== ] Loading file #10/10"
        #   - After last iteration:     "[===100%===] Loading file #10/10"
        str_counter = self.str_counter_template.format(i)
        self._track_length_of_leading_line(str_counter)
        return str_counter


def _check_greater(val_prev, val_new):
    return np.sign(val_new - val_prev)


def _check_smaller(val_prev, val_new):
    return np.sign(val_prev - val_new)


class ColumnBase:
    def __init__(self,
                 name, type,
                 n_decimals=3,
                 show_change_negative=True, show_change_positive=True, show_change_neutral=True,
                 improvement_case='greater'):
        self.name = name
        self.type = type
        self.n_decimals = n_decimals

        self.value = 0

        if improvement_case == 'greater':
            self.improvement_check = _check_greater
        elif improvement_case == 'smaller':
            self.improvement_check = _check_smaller
        else:
            raise ValueError(improvement_case)

        self.prefix_improve_pos = COLOR_POSITIVE if show_change_positive else ''
        self.prefix_improve_neu = COLOR_NEUTRAL if show_change_neutral else ''
        self.prefix_improve_neg = COLOR_NEGATIVE if show_change_negative else ''

        self.appendix_improve_pos = RESET if show_change_positive else ''
        self.appendix_improve_neu = RESET if show_change_neutral else ''
        self.appendix_improve_neg = RESET if show_change_negative else ''

    def parse_leading_line(self, value_new):
        improvement = self.improvement_check(self.value, value_new)
        self.value = value_new

        if improvement < 0:
            str_leading_line = self.layout_leading_line.format(self.prefix_improve_neg, value_new,
                                                               self.appendix_improve_neg)
        elif improvement == 0:
            str_leading_line = self.layout_leading_line.format(self.prefix_improve_neu, value_new,
                                                               self.appendix_improve_neu)
        elif improvement > 0:
            str_leading_line = self.layout_leading_line.format(self.prefix_improve_pos, value_new,
                                                               self.appendix_improve_pos)
        else:
            raise RuntimeError(improvement)

        return str_leading_line


class ColumnOneliner(ColumnBase):
    def __init__(self,
                 name, type,
                 n_decimals=3, leading_chars=3,
                 show_change_negative=True, show_change_positive=True, show_change_neutral=True,
                 improvement_case='greater'):
        super().__init__(name, type, n_decimals=n_decimals,
                         show_change_negative=show_change_negative,
                         show_change_positive=show_change_positive,
                         show_change_neutral=show_change_neutral,
                         improvement_case=improvement_case)

        n_chars_value = _get_length_of_parsed_value(type, leading_chars, n_decimals=n_decimals)
        self.layout_value = _parse_template_value(n_chars_value, type, n_decimals=self.n_decimals)

        delimiter = ': '
        # self.layout_headline =
        self.layout_leading_line = '{}'.format(self.name) + delimiter + self.layout_value


class ColumnTable(ColumnBase):
    def __init__(self,
                 name, type,
                 n_decimals=3, leading_chars=3,
                 show_change_negative=True, show_change_positive=True, show_change_neutral=True,
                 improvement_case='greater'):
        super().__init__(name, type, n_decimals=n_decimals,
                         show_change_negative=show_change_negative,
                         show_change_positive=show_change_positive,
                         show_change_neutral=show_change_neutral,
                         improvement_case=improvement_case)

        n_chars_value = _get_length_of_parsed_value(type, leading_chars, n_decimals=n_decimals)
        n_chars_name = len(self.name)
        n_chars = max(n_chars_name, n_chars_value)
        n_chars_value = n_chars - n_chars_value
        self.layout_value = _parse_template_value(n_chars_value, type, n_decimals=self.n_decimals)

        self.str_headline = '{}'.format(self.name)
        self.layout_leading_line = self.layout_value

    def get_headline(self):
        return self.str_headline


def _parse_template_value(n_chars, type, n_decimals=3, appendix_percent=' %'):
    if type == 'int':
        str_template_value = '{}{:' + str(n_chars) + 'd}{}'
    elif type == 'float':
        str_template_value = '{}{:' + str(n_chars) + '.' + str(n_decimals) + 'f}{}'
    elif type == 'percent':
        str_template_value = '{}{:' + str(n_chars - len(appendix_percent)) + '.' + str(
            n_decimals) + 'f}{}' + appendix_percent
    else:
        raise ValueError('Type not known: \'{}\''.format(type))

    return str_template_value


def _get_length_of_parsed_value(type, leading_chars, n_decimals=3):
    if type == 'int':
        n_chars_value = leading_chars
    elif type == 'float':
        n_chars_float = 1 + n_decimals
        n_chars_value = leading_chars + n_chars_float
    elif type == 'percent':
        n_chars_float = 1 + n_decimals
        n_chars_value = leading_chars + n_chars_float + 2
    else:
        raise ValueError('Type not known: \'{}\''.format(type))

    return n_chars_value
