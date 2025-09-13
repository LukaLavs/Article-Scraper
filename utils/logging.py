import logging
from logging.handlers import RotatingFileHandler

from ..config import get_path, ROOT_DIR

log_file_default = get_path(filename="log/flin.log", folder=ROOT_DIR)
error_log_file_default = get_path(filename="log/error.log", folder=ROOT_DIR)
log_name_default = "flin"

def get_logger(
    log_file: str = log_file_default, 
    log_name: str = log_name_default, 
    error_log_file: str = error_log_file_default
):
    """Create and return logger with DEBUG and ERROR handlers."""
    log = logging.getLogger(log_name)
    log.setLevel(logging.DEBUG)  # the smallest possible log level; increase with handler's log levels if needed.
    _formatter = logging.Formatter("[%(asctime)s] %(levelname)7s {%(filename)16s:%(lineno)4d} - %(message)s")
    _handler = RotatingFileHandler(log_file, maxBytes=16777216, backupCount=5, encoding="utf-8")  # 16MB
    _handler.setLevel(logging.DEBUG)
    _handler.setFormatter(_formatter)
    log.addHandler(_handler)
    _error_handler = RotatingFileHandler(error_log_file, maxBytes=16777216, backupCount=5, encoding="utf-8")  # 16MB
    _error_handler.setLevel(logging.ERROR)
    _error_handler.setFormatter(_formatter)
    log.addHandler(_error_handler)
    return log


def add_log_handler(log: logging.Logger, suffix: str, remove_original: bool = False):
    _formatter = logging.Formatter("[%(asctime)s] %(levelname)7s {%(filename)16s:%(lineno)4d} - %(message)s")
    _handler = RotatingFileHandler(
        new_handler_path := get_path(filename=f"log/flin_{suffix}.log", folder=ROOT_DIR),
        maxBytes=16777216,
        backupCount=5,
        encoding="utf-8",
    )
    _handler.setLevel(logging.DEBUG)
    _handler.setFormatter(_formatter)
    log.info(f"Adding handler: {new_handler_path}")
    log.addHandler(_handler)
    if remove_original:  # NOTE order of adding handlers in get_log method is important!
        log.info(f"Removing original handler {log.handlers[0]}!")
        log.removeHandler(log.handlers[0])

