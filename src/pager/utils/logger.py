import logging
from pager.utils.configs import cfg
from logging.handlers import RotatingFileHandler


class LoggerConfigurator:
    def __init__(self):
        self.root_logger = logging.getLogger()
        self.root_logger.setLevel(self._get_level_from_string(cfg["logger"]["level"]))
        self._rotate: int = cfg["logger"]["rotate"]
        self._path: str = cfg["logger"]["path"]
        self._max_bytes: int = cfg["logger"]["max_bytes"]
        self._backup_count: int = cfg["logger"]["backup_count"]

    def _get_level_from_string(self, level_str):
        levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        return levels.get(level_str.upper(), logging.NOTSET)

    def _setup_formatter_full(self):
        return logging.Formatter(
            "%(asctime)s %(levelname)-8s %(filename)s:%(lineno)d %(funcName)s %(message)s %(exc_info)s"
        )

    def _setup_formatter(self):
        return logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")

    def _setup_handlers(self):
        handlers = []

        if self._rotate:
            log_handler = RotatingFileHandler(
                f"{self._path}/all_log.log",
                maxBytes=self._max_bytes,
                backupCount=self._backup_count,
            )
        else:
            log_handler = logging.FileHandler(f"{self._path}/all_log.log", mode="w")

        log_handler.setLevel(self._get_level_from_string(cfg["logger"]["level"]))
        log_handler.setFormatter(self._setup_formatter())

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self._get_level_from_string(cfg["logger"]["level"]))
        stream_handler.setFormatter(self._setup_formatter_full())

        if self._rotate:
            error_handler = RotatingFileHandler(
                f"{self._path}/error_log.log",
                maxBytes=self._max_bytes,
                backupCount=self._backup_count,
            )
        else:
            error_handler = logging.FileHandler(f"{self._path}/error_log.log", mode="w")

        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(self._setup_formatter_full())

        handlers.append(log_handler)
        handlers.append(stream_handler)
        handlers.append(error_handler)

        return handlers

    def configure(self):
        self.root_logger.handlers = self._setup_handlers()
