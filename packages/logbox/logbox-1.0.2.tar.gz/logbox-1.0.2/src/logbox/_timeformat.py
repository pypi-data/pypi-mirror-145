# Copyright (C) 2021 Matthias Nadig


def format_time(t):
    """ Parse time given in seconds to a reasonable format (days, hh:mm.ss) """

    str_format = ''

    is_less_than_second = t < 1

    if is_less_than_second:
        str_format = '{} ms'.format(t*1e3)
    else:
        # t = int(round(t))

        # Days
        conversion_sec2day = 60 * 60 * 24
        t_days = int(t / conversion_sec2day)
        t_remain = t - t_days * conversion_sec2day
        if t_days > 0:
            str_unit = 'day' if t_days == 1 else 'days'
            str_format = '{} {}, '.format(t_days, str_unit) + str_format
        if t_remain > 0:
            str_format += '{:02d}:{:02d}:{:02d}.{} h'
            str_milli = '{:03d}'
            # Hours
            conversion_sec2hour = 60 * 60
            t_hours = int(t_remain / conversion_sec2hour)
            t_remain = t_remain - t_hours * conversion_sec2hour
            # Minutes
            conversion_sec2min = 60
            t_min = int(t_remain / conversion_sec2min)
            t_remain = t_remain - t_min * conversion_sec2min
            # Seconds
            t_sec = int(t_remain)
            t_remain = t_remain - t_sec
            # Milliseconds
            t_milli = int(round(t_remain*1e3))
            str_milli = str_milli.format(t_milli)
            str_milli = _convert_numbers_to_subscript(str_milli)
            # Format
            str_format = str_format.format(t_hours, t_min, t_sec, str_milli)
    return str_format


def _convert_numbers_to_subscript(str_numbers):
    subscript_mapping = {
        '0': '\u2080',
        '1': '\u2081',
        '2': '\u2082',
        '3': '\u2083',
        '4': '\u2084',
        '5': '\u2085',
        '6': '\u2086',
        '7': '\u2087',
        '8': '\u2088',
        '9': '\u2089',
    }

    str_out = ''.join([subscript_mapping[num] for num in str_numbers])

    return str_out
