import logging
import sys
from typing import Union


class CustomFormatter(logging.Formatter):
    GREEN = '\x1b[32m'
    GREY = '\x1b[37m'
    YELLOW = '\x1b[33m'
    RED = '\x1b[31;1m'
    RED_BOLD = '\x1b[31;1m'
    RESET = '\x1b[0m'

    def __init__(self, fmt: str, date_ftm: str = None, use_color: bool = True, *args, **kwargs):
        super().__init__(fmt=fmt, datefmt=date_ftm, *args, **kwargs)

        fmt_template = f'%(asctime)-15s | %(levelname)-9s | %(name)-18s %(lineno)4d | %(message)s'
        self.fmt = fmt if fmt is not None else fmt_template
        self.date_ftm = date_ftm if date_ftm is not None else '%Y-%m-%d %H:%M:%S'
        self.use_color = use_color

    def _get_formats(self):
        # export const RESET = "\x1b[0m"
        # export const bright = "\x1b[1m"
        # export const dim = "\x1b[2m"
        # export const underscore = "\x1b[4m"
        # export const blink = "\x1b[5m"
        # export const reverse = "\x1b[7m"
        # export const hidden = "\x1b[8m"
        #
        # export const black = "\x1b[30m"
        # export const RED = "\x1b[31m"
        # export const GREEN = "\x1b[32m"
        # export const YELLOW = "\x1b[33m"
        # export const blue = "\x1b[34m"
        # export const magenta = "\x1b[35m"
        # export const cyan = "\x1b[36m"
        # export const white = "\x1b[37m"
        #
        # export const BG_black = "\x1b[40m"
        # export const BG_red = "\x1b[41m"
        # export const BG_green = "\x1b[42m"
        # export const BG_yellow = "\x1b[43m"
        # export const BG_blue = "\x1b[44m"
        # export const BG_magenta = "\x1b[45m"
        # export const BG_cyan = "\x1b[46m"
        # export const BG_white = "\x1b[47m"

        formats = {
            'DEBUG': f'{self.GREY}{self.fmt}{self.RESET}',
            'INFO': f'{self.GREEN}{self.fmt}{self.RESET}',
            'WARNING': f'{self.YELLOW}{self.fmt}{self.RESET}',
            'ERROR': f'{self.RED}{self.fmt}{self.RESET}',
            'CRITICAL': f'{self.RED_BOLD}{self.fmt}{self.RESET}',
        }

        return formats

    def format(self, record):
        """Override formatter with necessary colors"""

        if self.use_color:
            formatter_custom = self._get_formats()
            log_fmt = formatter_custom.get(record.levelname)
            formatter = logging.Formatter(fmt=log_fmt, datefmt=self.date_ftm)
        else:
            formatter = logging.Formatter(fmt=self.fmt, datefmt=self.date_ftm)

        return formatter.format(record)


def logger(name: str,
           fmt: str = None,
           date_fmt: str = None,
           console: bool = True,
           console_output=sys.stderr,
           file: bool = False,
           enabled: bool = True,
           level: Union[str, int] = 'INFO',
           use_color: bool = True):
    """Simple logger

    Log levels:

    - CRITICAL 50
    - ERROR 40
    - WARNING 30
    - INFO 20
    - DEBUG 10
    - NOTSET 0

    :param name:
    :param fmt:
    :param date_fmt:
    :param console:
    :param console_output: Use None to stream into the sys.stderr.
    :param file:
    :param enabled:
    :param level: INFO by default. 
    :param use_color:
    :return:
    """

    # Get logger
    logger_instance = logging.getLogger(name)

    # Clear handlers if exists (to avoid entries duplicate)
    if logger_instance.hasHandlers():
        logger_instance.handlers.clear()

    # Set log level
    try:
        log_level = level if isinstance(level, int) else getattr(logging, level)
    except AttributeError as err:
        msg = ('CRITICAL = 50\n'
               'FATAL = CRITICAL\n'
               'ERROR = 40\n'
               'WARNING = 30\n'
               'WARN = WARNING\n'
               'INFO = 20\n'
               'DEBUG = 10\n'
               'NOTSET = 0')
        print(f'Invalid log level specified ({level}). Use one of the following:\n{msg}', file=sys.stderr)
        raise err
    else:
        logger_instance.setLevel(log_level)

    # Set log entries format
    logger.disabled = not enabled

    # Console handler with a INFO log level
    if console:
        # use param stream=sys.stdout for stdout printing
        ch = logging.StreamHandler(stream=console_output)
        logger_instance.setLevel(log_level)

        formatter_ch = CustomFormatter(fmt=fmt, date_ftm=date_fmt, use_color=use_color)
        ch.setFormatter(formatter_ch)  # Add the formatter
        logger_instance.addHandler(ch)  # Add the handlers to the logger

    # File handler which logs debug messages
    if file:
        fh = logging.FileHandler(f'{name}.log', mode='w')
        logger_instance.setLevel(log_level)
        formatter_file = CustomFormatter(fmt=fmt, date_ftm=date_fmt, use_color=False)
        fh.setFormatter(formatter_file)  # Add the formatter
        logger_instance.addHandler(fh)  # Add the handlers to the logger
    return logger_instance


class Logger:
    """Simple logger for inheritance only. By default, log into console with INFO level"""

    def __init__(self,
                 name: str,
                 console: bool = True,
                 console_level: str = 'INFO',
                 console_output=sys.stderr,
                 file: bool = False,
                 file_level: str = 'DEBUG',
                 date_format: str = '%Y-%m-%d %H:%M:%S',
                 log_format: str = '%(asctime)-15s [%(name)s] [LINE:%(lineno)d] [%(levelname)s] %(message)s',
                 enabled: bool = True):

        self.name = name
        self.console = console
        self.console_level = console_level
        self.file = file
        self.file_level = file_level
        self.date_format = date_format
        self.log_format = log_format
        self.enabled = enabled

        # Get logger
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)
        self.formatter = logging.Formatter(fmt=self.log_format, datefmt=self.date_format)
        self.logger.disabled = not self.enabled

        # Console handler with a INFO log level
        if self.console:
            # use param stream=sys.stdout for stdout printing
            ch = logging.StreamHandler(stream=console_output)
            ch.setLevel(logging.INFO)
            ch.setFormatter(self.formatter)  # Add the formatter
            self.logger.addHandler(ch)  # Add the handlers to the logger

        # File handler which logs debug messages
        if self.file:
            fh = logging.FileHandler(f'{self.name}.log', mode='w')
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(self.formatter)  # Add the formatter
            self.logger.addHandler(fh)  # Add the handlers to the logger

    def __call__(self, *args, **kwargs):
        return self.logger

    def __str__(self):
        return f'Name: {self.name}\n' \
               f'Enabled: {self.enabled}\n' \
               f'Console logging: {self.console}\n' \
               f'Console level: {self.console_level}\n' \
               f'File logging: {self.file}\n' \
               f'File level: {self.file_level}\n' \
               f'File name: {self.name}.log'
