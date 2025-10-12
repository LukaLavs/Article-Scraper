import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class Logger:

    def __init__(
        self,
        log_path: str | Path = "logs/app.log",
        max_bytes: int = 5 * 1024 * 1024,  # 5 MB max per file
        backup_count: int = 3,  # keep 3 backups
    ):
        log_path = Path(log_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger("app_logger")
        self.logger.setLevel(logging.INFO)

        # Avoid duplicate handlers if logger is reused
        if not self.logger.handlers:
            handler = RotatingFileHandler(
                log_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
            )
            formatter = logging.Formatter(
                "[%(asctime)s] %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def debug(self, message: str):
        self.logger.debug(message)

log = Logger()

__all__ = ["Logger", "log"]