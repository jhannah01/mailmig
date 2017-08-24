''' mailmig Logger helper

'''

import logging
import os
import os.path

_log_fmt_prefix = '[%(asctime)s] %(name)s [%(levelname)s]'
_log_Fmt_location = '(%(filename)s@%(lineno)s in %(funcName)s)'


def get_logger(name=None, log_level=None, log_to_console=True, log_filename=None, overwrite=True):
    fmt = logging.Formatter('%s %s -- %(message)s' % (_log_fmt_prefix, _log_Fmt_location))
    if not name:
        name = 'mailmig'

    if not log_level:
        log_level = logging.INFO

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if log_to_console:
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(log_level)
        logger.addHandler(sh)

    if log_filename:
        fh = logging.FileHandler(log_filename, mode='w')
        fh.setFormatter(fmt)
        fh.setLevel(log_level)
        logger.addHandler(fh)

    return logger


__all__ = ['get_logger']
