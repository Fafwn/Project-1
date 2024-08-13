import logging


def setup_logger():
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format, datefmt="%H:%M:%S")


def run():
    setup_logger()
