# Copyright (C) 2021 Matthias Nadig

import sys
import time
import threading
import traceback
import atexit

from ._codes import ERASE_LINE, CARRIAGE_RETURN
from ._codes import COLOR_DEFAULT_FONT, COLOR_DEFAULT_BG
from ._codes import COLOR_DEFAULT_FONT_FG, COLOR_DEFAULT_FONT_BG
from ._codes import RESET
from ._codes import RESET_CODE
from ._codes import RED, LIGHT_GRAY
from ._codes import PROGBAR_INIT, PROGBAR_ACTIVE, PROGBAR_DONE
from ._codes import DEFAULT_STR_INFO, DEFAULT_CHANNEL
from ._codes import DEBUG, INFO, WARN, ERROR
from ._channels import Channel, SubChannel, ParallelChannel
from ._progbars import ProgbarKnownLength, ProgbarUnknownLength
from ._timeformat import format_time

from ._cli import activate_esc, deactivate_esc


exception = None
global_default_channel = None
global_channels = []

t_start = time.time()


class Logger:
    def __init__(self, layout_leading_line='oneliner'):
        # FOR DEBUGGING
        # print('Logger.__init__')

        # Refresh rate and timer for calculating minimum interval between terminal outputs
        self.refresh_interval = 0
        self.set_refresh_rate(25)
        self.t_last_update = time.time() - self.refresh_interval

        # Output string that will be printed to terminal during every update and lock object
        self.outputs = []

        # Output event handling
        self.lock_output = threading.Lock()
        self.event_wait_interval = threading.Event()
        self.event_print_requested = threading.Event()
        self.cond_print_requested = threading.Condition()

        # Channels that can be registered, e.g. by different modules
        global global_default_channel
        global_default_channel = Channel(name=DEFAULT_CHANNEL, show_prefix_module=False, show_prefix_level=False)
        self.default_channel = global_default_channel
        self.channels = [
            self.default_channel,
        ]

        # Progress bars will always be printed into the most recent line
        # self.progbars = []
        if layout_leading_line == 'table':
            self.leading_line = LeadingLineTable()
        elif layout_leading_line == 'oneliner':
            self.leading_line = LeadingLineOneliner()
        else:
            raise ValueError(layout_leading_line)

        # Activate ANSI escape codes if necessary
        activate_esc()
        sys.stdout.write(COLOR_DEFAULT_FONT_FG + COLOR_DEFAULT_FONT_BG)

        self.is_running = True
        self.th_print = threading.Thread(target=self._on_print)

    def _on_exception(self, exc_type, exc_value, exc_traceback):
        """
        Callback for exceptions
        Exceptions will be logged to each channel and then reraised.
        """
        global exception

        # Get current exception
        # exc_type, exc_value, exc_traceback = sys.exc_info()
        # print(exc_type, exc_value, exc_traceback)

        # Handle exception in case there is one
        if exc_type is not None:
            # Note the exception for exit handling
            exception = (exc_type, exc_value, exc_traceback)

            # Parse the traceback
            str_traceback = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            str_traceback = RED + str_traceback

            self.leading_line.stop_on_exit()

            # Write error report to channels
            # print('\n\nLogger traceback:\n', str_traceback)
            # print('\n' + str_traceback)
            for channel in self.channels:
                channel.on_error('\n\n' + str_traceback, self.default_channel)

            return self._reraise(exc_type, exc_value, exc_traceback)

    def _print_time_since_start(self, *args):
        """ Print the total runtime since the logger has been started """
        t_elapsed = time.time() - t_start
        self._print_time(*args, t_elapsed)

    def _print_time(self, *args):
        t = args[-1]
        str_time = format_time(t)
        self.print(*args[:-1], str_time)

    def _reraise(self, exc_type, exc_value, exc_traceback):
        # Wait until all outputs have been printed
        while self.th_print.is_alive():
            pass

        # Add newlines
        # self.print('\n')

        # Re-raise the exception
        return sys.__excepthook__(exc_type, exc_value, exc_traceback)

    def set_refresh_rate(self, refresh_rate):
        """ Calculate refresh interval [s] given a refresh rate [Hz] """
        self.refresh_interval = 1 / refresh_rate

    def print(self, *str_new, level=INFO, channel=DEFAULT_CHANNEL, use_style=True):
        """ Method that will be invoked by logger.info(...) or logger.warn(...) """

        # Can be given multiple arguments to be joined into one string (as Python's standard print-function)
        str_new = ' '.join([str(item) for item in str_new])
        # str_new = ' '.join(np.asarray(str_new).astype('str'))  # --> Error with torch.Size

        # Get channel (in case name is given)
        channel = self._get_channel(channel)

        # Apply style if requested
        if use_style:
            str_new = self._apply_params(str_new, level, channel)
        else:
            str_new += '\n'

        # Write to enabled logfiles
        channel.on_log(str_new, self.default_channel)

        # Queue to terminal outputs
        with self.lock_output:
            self.outputs.append(str_new)

        self.notify_print()

    def notify_print(self):
        """ Serves as callback for progbar to request a print update """
        self.event_print_requested.set()
        if not self.th_print.is_alive():
            self.th_print = threading.Thread(target=self._on_print)
            self.th_print.start()

    def _get_channel(self, channel):
        """ Chooses corresponding channel if specified by name """

        # In case string is given, select channel by name
        if isinstance(channel, str):
            for channel_check in self.channels:
                if channel_check.name == channel:
                    channel = channel_check
                    break
            else:
                raise ValueError('Channel could not be found by name: \'{}\''.format(channel))

        return channel

    def _apply_params(self, str_new, level, channel):
        """ Given string will be added prefixes, colors, etc. based on channel parameters """

        # Prefix to be added to every line of output
        prefix_line = ''
        prefix_line = channel.prefix_line_debug if level == DEBUG else prefix_line
        prefix_line = channel.prefix_line_info if level == INFO else prefix_line
        prefix_line = channel.prefix_line_warn if level == WARN else prefix_line
        prefix_line = channel.prefix_line_error if level == ERROR else prefix_line

        # Appendix to be added to every line of output
        appendix_line = ''
        appendix_line = channel.appendix_line_debug if level == DEBUG else appendix_line
        appendix_line = channel.appendix_line_info if level == INFO else appendix_line
        appendix_line = channel.appendix_line_warn if level == WARN else appendix_line
        appendix_line = channel.appendix_line_error if level == ERROR else appendix_line

        # Disassemble output into lines
        lines = str_new.split('\n')

        # Reassemble lines
        #   1. Set font and background color
        #   2. Concatenate lines by inserting prefix and appendix for each line
        #   3. Reset all parameters
        # print(appendix_line+'\n'+prefix_line, lines)
        str_new = \
            prefix_line + \
            str(appendix_line+RESET+prefix_line).join(lines) + \
            appendix_line + RESET

        return str_new

    def _on_print(self):
        """
        Print current output
        First check refresh timer, sleep if necessary and then print.
        """

        while self.event_print_requested.is_set():
            # Set flag for blocking further invocations during refresh interval
            self.event_wait_interval.set()

            # Sleep until end of refresh interval
            t_wait = max(0, self.refresh_interval - (time.time() - self.t_last_update))
            time.sleep(t_wait)

            # Assemble strings for leading line
            leading_line_done, leading_line_active = self.leading_line.get_leading_line()

            # Lock output string
            with self.lock_output:
                self.event_print_requested.clear()

                # Update timer and reset flag
                self.t_last_update = time.time()
                self.event_wait_interval.clear()

                # Remove previous leading line and add the current one
                str_out = ERASE_LINE + CARRIAGE_RETURN + RESET + leading_line_done + ''.join(self.outputs) + leading_line_active

                # Reset output queue
                if len(self.outputs) > 0:
                    self.leading_line.is_headline_overwritten = True
                else:
                    self.leading_line.is_headline_overwritten = False
                self.outputs = []

            # Print to terminal
            sys.stdout.write(str_out)
            # print(str_out, end='')

    def register(self, name, mode='sub', **params):
        """ Method that will be invoked by logger.register(...) to set up a new channel """

        if mode == 'parallel':
            channel = ParallelChannel(name=name, **params)
        elif mode == 'sub':
            channel = SubChannel(name=name, **params)
        else:
            raise ValueError(mode)

        global global_channels
        global_channels.append(channel)
        self.channels.append(channel)

        return channel

    def register_progbar(self, limit_updates=None, str_info=DEFAULT_STR_INFO, channel=DEFAULT_CHANNEL):
        """ Method that will be invoked by logger.register_progbar(...) to set up a new progbar """
        channel = self._get_channel(channel)
        return self.leading_line.register_progbar(channel, self.default_channel,
                                                  limit_updates=limit_updates,
                                                  str_info=str_info)


class LeadingLineOneliner:
    def __init__(self):
        self.delimiter_progbars = ' | '
        self.str_leading_line = ''

        self.is_headline_overwritten = True

        self.progbars = []
        self.channels = []
        self.default_channels = []

    def register_progbar(self, channel, default_channel, limit_updates=None, str_info=DEFAULT_STR_INFO):
        """ Method that will be invoked by logger.register_progbar(...) to set up a new progbar """

        if limit_updates is None:
            progbar = ProgbarUnknownLength(callback_on_update=_notify_print, str_info=str_info, style=COLOR_DEFAULT_FONT+COLOR_DEFAULT_BG)
        else:
            progbar = ProgbarKnownLength(limit_updates=limit_updates, callback_on_update=_notify_print, str_info=str_info, style=COLOR_DEFAULT_FONT+COLOR_DEFAULT_BG)
        self.progbars.append(progbar)
        self.channels.append(channel)
        self.default_channels.append(default_channel)

        return progbar

    def stop_on_exit(self):
        """ Handle exit when exception has been raised """

        # Write to log files
        for channel, default_channel, progbar in zip(self.channels, self.default_channels, self.progbars):
            channel.on_log(progbar.parse_leading_line() + '\n\t\u2ba9 Process \'{}\' stopped due to error (see traceback below).\n'.format(progbar.str_info), default_channel)

        # Remove all progbars
        self.progbars = []
        self.channels = []
        self.default_channels = []

    def get_leading_line(self):
        return self._get_leading_line()

    def _get_leading_line(self):
        """
        Leading line contains progress bar
        This line is always removed and again appended to the output (while any progbar is active).
        """

        indices_active = []
        indices_done = []

        for index_progbar, progbar in enumerate(self.progbars):
            if progbar.state == PROGBAR_ACTIVE:
                indices_active.append(index_progbar)
            elif progbar.state == PROGBAR_DONE:
                indices_done.append(index_progbar)

        leading_line_active = self._parse_leading_line_active(indices_active)
        leading_line_done = self._parse_leading_line_done(indices_done)

        # Remove progbars that are done
        for index_progbar in reversed(indices_done):
            del self.progbars[index_progbar]
            del self.channels[index_progbar]
            del self.default_channels[index_progbar]

        # When any progbar is active, always append the "logbox symbol" to the end of the leading line
        if len(leading_line_active) > 0:
            style = COLOR_DEFAULT_FONT + COLOR_DEFAULT_BG
            leading_line_active = style + leading_line_active + ' |\u02E1\u1d52\u1d4d\u1d47\u1d52\u02e3' + RESET

        return leading_line_done, leading_line_active

    def _parse_leading_line_active(self, indices_progbar):
        leading_line = []
        delimiter = self.delimiter_progbars
        for index_progbar in indices_progbar:
            leading_line.append(self.progbars[index_progbar].parse_leading_line())
        leading_line = delimiter.join(leading_line)
        return leading_line

    def _parse_leading_line_done(self, indices_progbar):
        leading_line = ''
        style = COLOR_DEFAULT_FONT + COLOR_DEFAULT_BG
        newline = '\n' + RESET
        appendix = newline + style + '\t\u2ba9 Complete, time elapsed: {}'
        for index_progbar in indices_progbar:
            channel, default_channel, progbar = self.channels[index_progbar], self.default_channels[index_progbar], self.progbars[index_progbar]
            str_time_elapsed = format_time(progbar.t_stop - progbar.t_start)
            # str_leading_line = progbar.parse_leading_line() + appendix.format(progbar.str_info, str_time_elapsed)
            str_leading_line = (
                style + progbar.parse_leading_line() +
                # ' |\u02E1\u1d52\u1d4d\u1d47\u1d52\u02e3' +
                appendix.format(str_time_elapsed))
            leading_line += str_leading_line + newline
            channel.on_log(str_leading_line + '\n', default_channel)
        return leading_line


class LeadingLineTable:
    def __init__(self):
        self.delimiter_progbars = ' | '
        self.str_headline = ''
        self.str_leading_line = ''

        self.is_headline_overwritten = True

        self.progbars = []

        raise NotImplementedError('Usage of logger.LeadingLineTable not recommended and might behave differently than Oneliner')

    def register_progbar(self, limit_updates=None, str_info=DEFAULT_STR_INFO):
        """ Method that will be invoked by logger.register_progbar(...) to set up a new progbar """

        if limit_updates is None:
            progbar = ProgbarUnknownLength(callback_on_update=_notify_print, str_info=str_info)
        else:
            progbar = ProgbarKnownLength(limit_updates=limit_updates, callback_on_update=_notify_print, str_info=str_info)
        self.progbars.append(progbar)

        return progbar

    def get_leading_line(self):
        return self._get_leading_line()

    def _get_leading_line(self):
        """
        Leading line contains progress bar
        This line is always removed and again appended to the output (while any progbar is active).
        """

        indices_active = []
        indices_done = []

        for index_progbar, progbar in enumerate(self.progbars):
            if progbar.state == PROGBAR_ACTIVE:
                indices_active.append(index_progbar)
            elif progbar.state == PROGBAR_DONE:
                indices_done.append(index_progbar)

        headline_active, leading_line_active = self._parse_leading_line(indices_active)
        headline_done, leading_line_done = self._parse_leading_line(indices_done)

        # Remove progbars that are done
        for index_progbar in reversed(indices_done):
            del self.progbars[index_progbar]

        # Compare "active" headline with currently printed one
        n_chars_min = min(len(self.str_headline), len(headline_active))
        if ((self.str_headline == '' or headline_active[:n_chars_min] != self.str_headline[:n_chars_min]) and \
            headline_active[n_chars_min:] != ' ' * len(headline_active[n_chars_min:])) or \
            self.is_headline_overwritten:
            # Headlines differ, append to reprint
            leading_line_active = headline_active + '\n' + leading_line_active  # + ' |\u02E1\u1d52\u1d4d\u1d47\u1d52\u02e3'
            self.str_headline = headline_active

        # Reprint headline of progbars that are done, if not empty
        if headline_done != ' ' * len(headline_done) and (self.is_headline_overwritten or len(indices_active) > 0):
            leading_line_done = headline_done + '\n' + leading_line_done

        # Concatenate leading lines
        if len(leading_line_done) == 0:
            leading_line = leading_line_active
        else:
            leading_line = leading_line_done + '\n' + leading_line_active

        return leading_line

    def _parse_leading_line(self, indices_progbar):
        headline = []
        leading_line = []

        for index_progbar in indices_progbar:
            headline.append(self.progbars[index_progbar].parse_headline())
            leading_line.append(self.progbars[index_progbar].parse_leading_line())

        headline = self.delimiter_progbars.join(headline)
        leading_line = self.delimiter_progbars.join(leading_line)

        return headline, leading_line


def _on_exit():
    """
    Prints total runtime when Python exits
    Note:
        Does not make sense to make this a method of logger. Logger will be cleaned up first (?).
        The Method would then still be executed but can not access attributes of logger anymore.
        Thus we need to use globals anyways.
    """
    # if exception is None:
    t_elapsed = time.time() - t_start
    str_timer_info = ('\n\nTotal runtime: {} ' + LIGHT_GRAY + '(since logbox import)' + RESET_CODE + '\n').format(format_time(t_elapsed))
    sys.stdout.write(str_timer_info)

    # Explicitly log time to all channels
    for channel in global_channels:
        channel.on_log(str_timer_info + ' ' + format_time(time.time()-t_start), global_default_channel)
    
    # Deactivate ANSI escape codes if necessary
    # sys.stdout.write(RESET_CODE)
    # time.sleep(0.1)
    deactivate_esc()


# Logger is started here to handle output to the terminal and can be used by functions below
logger = Logger()

# Exceptions should always be given to the logger
sys.excepthook = logger._on_exception
atexit.register(_on_exit)


def _info(*str_out, channel=DEFAULT_CHANNEL):
    """ Print multiple arguments (info level) """
    logger.print(*str_out, level=INFO, channel=channel, use_style=True)


def _warn(*str_out, channel=DEFAULT_CHANNEL):
    """ Print multiple arguments (warn level) """
    logger.print(*str_out, level=WARN, channel=channel, use_style=True)


def _register(name_channel, mode='sub', **params):
    """
    Register a new channel
    E.g. different modules can set up their own channels for logging.
    """
    return logger.register(name_channel, mode=mode, **params)


def _register_progbar(limit_updates=None, str_info=DEFAULT_STR_INFO, channel=DEFAULT_CHANNEL):
    """
    Register a new progbar
    E.g. done by log_range(...) and other iterators.
    """
    return logger.register_progbar(limit_updates=limit_updates,
                                   str_info=str_info,
                                   channel=channel)


def _notify_print():
    """ Invoke notify_print() to force print of most recent output """
    return logger.notify_print()


def _print_time_since_start(*str_out):
    """
    Print the total runtime since the logger has been started
    Note: The time will automatically be appended to the given output string.
    """
    logger._print_time_since_start(*str_out)


def _print_time(*args):
    """
    Print the given time interval (last item of args)
    """
    logger._print_time(*args)
