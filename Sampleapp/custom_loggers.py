import logging

from logging import FileHandler
from logging import Formatter


LOG_FORMAT = (
    "%(asctime)s [%(levelname)s]: %(message)s in %(pathname)s:%(lineno)d")
LOG_LEVEL = logging.INFO

# messaging logger
MESSAGING_LOG_FILE = "/tmp/messaging.log"


messaging_logger = logging.getLogger("messaging")
messaging_logger.setLevel(LOG_LEVEL)
messaging_logger_file_handler = FileHandler(MESSAGING_LOG_FILE)
messaging_logger_file_handler.setLevel(LOG_LEVEL)
messaging_logger_file_handler.setFormatter(Formatter(LOG_FORMAT))
messaging_logger.addHandler(messaging_logger_file_handler)

# payments logger
PAYMENTS_LOG_FILE = "/tmp/payments.log"
payments_logger = logging.getLogger("payments")

payments_logger.setLevel(LOG_LEVEL)
payments_file_handler = FileHandler(PAYMENTS_LOG_FILE)
payments_file_handler.setLevel(LOG_LEVEL)
payments_file_handler.setFormatter(Formatter(LOG_FORMAT))
payments_logger.addHandler(payments_file_handler)
