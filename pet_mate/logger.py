import logging
from settings import is_verbose

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(logging.ERROR)
        logger.addHandler(handler)


def log(*values: object):
    if is_verbose():
        print(values)