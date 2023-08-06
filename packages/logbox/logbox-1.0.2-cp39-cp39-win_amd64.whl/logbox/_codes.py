# Copyright (C) 2021 Matthias Nadig


# Logging levels
DEBUG = 0
INFO = 1
WARN = 2
ERROR = 3

DEFAULT_CHANNEL = 'default'

# See ANSI escape codes (=> Wikipedia, english)
# RED = '\033[0;31m'
BLUE = '\033[1;34m'
BRIGHT_BLUE = '\033[38;5;20m'#'\033[0;94m'
ORANGE = '\033[38;5;202m'
CYAN = '\033[1;36m'
GREEN = '\033[0;32m'
LIGHT_GRAY = '\033[38;5;251m'
BOLD = '\033[1;1m'
REVERSE = '\033[;7m'

RESET_CODE = '\033[0;0m'

ERASE_LINE = '\33[2K'
CARRIAGE_RETURN = '\r'

PROGBAR_BG_RIGHT = '\033[48;5;251m'
PROGBAR_BG_LEFT = '\033[48;5;240m'
PROGBAR_FG_RIGHT = '\033[38;5;16m'
PROGBAR_FG_LEFT = '\033[38;5;231m'

COLOR_NEGATIVE = '\033[38;5;1m'
COLOR_NEUTRAL = '\033[38;5;0m'
COLOR_POSITIVE = '\033[38;5;2m'

PROGBAR_INIT = 0
PROGBAR_ACTIVE = 1
PROGBAR_DONE = 2

DEFAULT_STR_INFO = 'Processing step'


def _rgb2hex(color):
    """ Converts RGB tuple (normalized!) to hex representation (eg. (1, 0, 1) -> 'ff00ff') """

    # Must be given normalized RGB color
    (r, g, b) = color

    # Round to 8-bit resolution
    n_values = 255
    r = int(round(r * n_values))
    g = int(round(g * n_values))
    b = int(round(b * n_values))

    # Convert to hex
    r = _int2hex_8bit(r)
    g = _int2hex_8bit(g)
    b = _int2hex_8bit(b)

    color_hex = r + g + b

    return color_hex


def _parse_font_color_from_rgb(color):
    return _parse_color_from_rgb(color, 38)


def _parse_background_color_from_rgb(color):
    return _parse_color_from_rgb(color, 48)


'''def _parse_color_from_8bit_table(id, mode):
    id = int(id)

    # Find 8-bit representation
    # TODO: Get closest number in list instead of the exact one
    for row in list_8bit_to_rgb_translation:
        if id == int(row[0]):
            color_hex = int(row[1])
            break
    else:
        raise RuntimeError('Did not find translation for \'{}\''.format(id))

    r, g, b = _hex2rgb(color_hex)

    return '\33[{};2;{:d};{:d};{:d}m'.format(mode, r, g, b)'''


def _hex2rgb(color):
    r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)

    # Round to 8-bit resolution
    max_value = 255
    r = int(round(r * max_value))
    g = int(round(g * max_value))
    b = int(round(b * max_value))

    return r, g, b


def _parse_color_from_rgb(color, mode):
    """
    Assembles string with with ANSI escape code for 8-bit color (font or background) from
    RGB tuple (normalized!).
    """

    # Convert to hex
    '''color_hex = _rgb2hex(color)

    # Find 8-bit representation
    # TODO: Get closest number in list instead of the exact one
    for row in list_8bit_to_rgb_translation:
        if color_hex == row[1]:
            color_8bit = int(row[0])
            break
    else:
        raise RuntimeError('Did not find translation for \'{}\''.format(color_hex))

    # Assemble color code (font or background depending on mode)
    color = '\033[{};5;{}m'.format(mode, color_8bit)'''
    (r, g, b) = color
    # Round to 8-bit resolution
    max_value = 255
    r = int(round(r * max_value))
    g = int(round(g * max_value))
    b = int(round(b * max_value))
    color = '\33[{};2;{:d};{:d};{:d}m'.format(mode, r, g, b)

    return color


def _int2hex_8bit(num):
    str_hex = hex(num)
    str_hex = str_hex[2:]
    if len(str_hex) > 2:
        raise ValueError(
            'Given number ({} dec. -> {} hex.) was to big (max. {} -> {})'.format(num, hex(num), 255, hex(255)))
    str_hex = str('0' + str_hex)[-2:]
    return str_hex


# Note: Maybe rather use REVERSE to properly set default styles of terminal...
COLOR_DEFAULT_FONT_FG = _parse_font_color_from_rgb((0, 0, 0))
COLOR_DEFAULT_FONT_BG = _parse_background_color_from_rgb((1, 1, 1))
# COLOR_DEFAULT_FONT = COLOR_DEFAULT_FONT_FG + COLOR_DEFAULT_BG
COLOR_DEFAULT_FONT = ''
COLOR_DEFAULT_BG = ''

RESET = COLOR_DEFAULT_FONT_FG + COLOR_DEFAULT_FONT_BG

RED = _parse_font_color_from_rgb((170/255, 0, 0))
