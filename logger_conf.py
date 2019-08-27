import logging
import os
logging.REGISTERED = False

default_logger_level = int(os.environ.get("OCVL_LOGGER_LEVEL", logging.WARNING))


def register():
    if logging.REGISTERED:
        return
    logging.REGISTERED = True
    # create logger
    logger = logging.getLogger()
    logger.setLevel(default_logger_level)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(default_logger_level)

    # create formatter
    LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    formatter = logging.Formatter(LOG_FORMAT)

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(ch)

    # 'application' code
    logger.debug('debug message')
    logger.info('info message')
