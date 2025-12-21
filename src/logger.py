import logging

class Logger():
    def __init__(self):
        logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
        self.__logger = logging.getLogger(__name__)

    def info(self, msg: str):
        self.__logger.info(msg)

    def error(self, msg: str):
        self.__logger.error(msg)