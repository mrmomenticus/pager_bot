import logging
from pager.configs import cfg
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
            info_handler = RotatingFileHandler(
                f"{self._path}/info.log",
                maxBytes=self._max_bytes,
                backupCount=self._backup_count,
            )
        else:
            info_handler = logging.FileHandler(f"{self._path}/info.log", mode="w")

        info_handler.setLevel(self._get_level_from_string(cfg["logger"]["level"]))
        info_handler.setFormatter(self._setup_formatter())

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self._get_level_from_string(cfg["logger"]["level"]))
        stream_handler.setFormatter(self._setup_formatter())

        handlers.append(info_handler)
        handlers.append(stream_handler)

        if self._rotate:
            debug_handler = RotatingFileHandler(
                f"{self._path}/debug.log",
                maxBytes=self._max_bytes,
                backupCount=self._backup_count,
            )
        else:
            debug_handler = logging.FileHandler(f"{self._path}/debug.log", mode="w")

        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(self._setup_formatter_full())

        debug_stream_handler = logging.StreamHandler()
        debug_stream_handler.setLevel(logging.DEBUG)
        debug_stream_handler.setFormatter(self._setup_formatter_full())

        handlers.append(debug_handler)
        handlers.append(debug_stream_handler)

        if self._rotate:
            warning_handler = RotatingFileHandler(
                f"{self._path}/warning.log",
                maxBytes=self._max_bytes,
                backupCount=self._backup_count,
            )
        else:
            warning_handler = logging.FileHandler(f"{self._path}/warning.log", mode="w")

        warning_handler.setLevel(logging.WARNING)
        warning_handler.setFormatter(self._setup_formatter())

        warning_stream_handler = logging.StreamHandler()
        warning_stream_handler.setLevel(logging.WARNING)
        warning_stream_handler.setFormatter(self._setup_formatter())

        handlers.append(warning_handler)
        handlers.append(warning_stream_handler)

        if self._rotate:
            error_handler = RotatingFileHandler(
                f"{self._path}/error.log",
                maxBytes=self._max_bytes,
                backupCount=self._backup_count,
            )
        else:
            error_handler = logging.FileHandler(f"{self._path}/error.log", mode="w")

        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(
            logging.Formatter(
                self._setup_formatter_full()
            )
        )

        error_stream_handler = logging.StreamHandler()
        error_stream_handler.setLevel(logging.ERROR)
        error_stream_handler.setFormatter(
            logging.Formatter(
                self._setup_formatter()
            )
        )

        handlers.append(error_handler)
        handlers.append(error_stream_handler)

        if self._rotate:
            critical_handler = RotatingFileHandler(
                f"{self._path}/critical.log",
                maxBytes=self._max_bytes,
                backupCount=self._backup_count,
            )
        else:
            critical_handler = logging.FileHandler(
                f"{self._path}/critical.log", mode="w"
            )

        critical_handler.setLevel(logging.CRITICAL)
        critical_handler.setFormatter(
            logging.Formatter(
                self._setup_formatter_full()
            )
        )

        critical_stream_handler = logging.StreamHandler()
        critical_stream_handler.setLevel(logging.CRITICAL)
        critical_stream_handler.setFormatter(
            logging.Formatter(
                self._setup_formatter()
            )
        )

        handlers.append(critical_handler)
        handlers.append(critical_stream_handler)

        return handlers

    def configure(self):
        self.root_logger.handlers = self._setup_handlers()
