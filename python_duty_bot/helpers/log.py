import logging
import sys

from helpers.config import Config


class Log:
    logger = logging.getLogger("logger")
    logger.setLevel(Config.log_level)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter('%(levelname)s:%(module)s:%(message)s'))
    logger.addHandler(handler)
