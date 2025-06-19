import logging

class AppLogger:

    def __init__(self, name: str = "scheduler"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Prevent adding multiple handlers if logger reused
        if not self.logger.handlers:
            # Console handler
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)

            # Formatter
            formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)s: %(message)s'
            )
            ch.setFormatter(formatter)

            self.logger.addHandler(ch)

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)
