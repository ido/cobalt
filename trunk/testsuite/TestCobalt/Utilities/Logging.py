'''logging utilities'''

__revision__ = '$Revision:$'

__all__ = ["setup_file_logging"]

import logging

LOGGING_LEVELS = {
    "DEBUG" : logging.DEBUG,
    "INFO" : logging.INFO,
    "WARNING" : logging.WARNING,
    "ERROR" : logging.ERROR,
    "CRITICAL" : logging.CRITICAL,
    }

def setup_file_logging(log_name, file_name, level):
    logger = logging.getLogger(log_name)
    file_handler = logging.FileHandler(file_name)
    file_formatter = logging.Formatter("%(asctime)s %(name)s[%(process)d]: %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(LOGGING_LEVELS[level])
    logger.addHandler(file_handler)
    logger.setLevel(LOGGING_LEVELS[level])
    return logger
