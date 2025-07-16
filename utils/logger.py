import logging
from logging.handlers import TimedRotatingFileHandler

from config import config

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL


class Logger(object):

    level = logging.DEBUG if config.env.debug else logging.INFO

    @classmethod
    def get(cls, name):
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(cls.level)

        # Formatter
        fmt = '%(asctime)s [%(levelname)s] %(process)d (%(filename)s#%(lineno)d) ~ %(message)s'
        # datefmt = '%Y-%m-%d %H:%M:%S,uuu'
        formatter = logging.Formatter(fmt)

        # Stream based handler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(cls.level)
        stream_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)

        return logger


logger = Logger.get(config.project.id)
