import logging
import os
import functools
import pathlib
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from py_fastapi_logging.formatters.json import JSONLogFormatter


class LogConfigure:
    DEFAULT_FORMAT = "[%(asctime)s] %(levelname)s -- %(progname)s: [%(request_id)10s] %(tags)s %(payload)s"
    DEFAULT_OUTPUTS = "json,stderr"

    FORMAT_MAP = {"console": "stderr"}

    def __init__(
        self,
        app_name=None,
        filename=None,
        format_string=None,
        level=None,
        rotate_mb=None,
        rotate_when=None,
        backup_count=7,
        json_multiline=False,
        request_id_support=True,
        log_output=None,
        colored=True,
        log_dir=None,
        cleanup=False,
    ):
        self.app_name = app_name
        self._format_string = format_string
        self._level = level
        self.rotate_mb = rotate_mb
        self.rotate_when = rotate_when
        self.backup_count = backup_count
        self.json_multiline = json_multiline
        self._log_output = log_output
        self._colored = colored
        self._log_dir = log_dir
        self._filename = pathlib.Path(filename) if filename else None
        self.request_id_support = request_id_support
        self._apply_suffix = False
        self.cleanup = cleanup

    @property
    def base_app_name(self):
        return self.app_name.split(".", 1)[0]

    @functools.cached_property
    def directory(self):
        log_dir = os.environ.get("LOG_DIR")
        if log_dir:
            return pathlib.Path(log_dir)

        if self._filename and self._filename.is_absolute():
            directory = self._filename.parent
            return directory

        return pathlib.Path("/var/log/", self.base_app_name)

    def get_filename(self, suffix):
        if self._filename:
            filename = self._filename
        else:
            filename = os.environ.get("LOG_FILENAME", f"{self.base_app_name}.log")
        filename = self.directory / filename
        if self._apply_suffix:
            filename.with_suffix(suffix)

        self._apply_suffix = True
        return filename

    @property
    def format_string(self):
        return self._format_string or self.DEFAULT_FORMAT

    def _get_file_handler(self, suffix):
        filename = self.get_filename(suffix)
        if self.rotate_mb:
            handler = RotatingFileHandler(
                filename, maxBytes=self.rotate_mb * 1024 * 1024, backupCount=self.backup_count, encoding="utf-8"
            )

        elif self.rotate_when:
            handler = TimedRotatingFileHandler(
                filename, when=self.rotate_when, backupCount=self.backup_count, encoding="utf-8"
            )
        else:
            handler = logging.FileHandler(filename, encoding="utf-8")
        return handler

    def get_handler(self, name):
        if name == "simple":
            handler = self._get_file_handler(".txt")
            formatter = logging.Formatter(self.format_string)
            handler.setFormatter(formatter)
        elif name == "json":
            handler = self._get_file_handler(".json")
            formatter = JSONLogFormatter()
            handler.setFormatter(formatter)
        elif name == "stderr":
            handler = logging.StreamHandler()
            formatter = logging.Formatter(self.format_string)
            handler.setFormatter(formatter)
        else:
            raise ValueError(f"unknown handler type: '{name}'")

        return handler

    @property
    def level(self):
        return os.environ.get("LOG_LEVEL", self._level or "INFO").upper()

    def normalize_format_names(self, names: str):
        names = names.lower().split(",")
        return [self.FORMAT_MAP.get(name, name) for name in names]

    @property
    def formats(self):
        if self._log_output:
            names = self._log_output
        else:
            names = os.environ.get("LOG_OUTPUT") or os.environ.get("LOG_FORMAT")
        if not names:
            names = self.DEFAULT_OUTPUTS
        return self.normalize_format_names(names)

    def get_handlers(self, names):
        handlers = [self.get_handler(name) for name in names]
        return handlers

    @property
    def default_logger_level(self):
        level = os.environ.get("LOGGING_DEFAULT_LEVEL") or os.environ.get("LOG_DEFAULT_LEVEL")
        if level:
            level = level.upper()
        return level

    @property
    def default_logger_output(self):
        return os.environ.get("LOGGING_DEFAULT_HANDLER") or os.environ.get("LOG_DEFAULT_OUTPUT")


def init_logger(config: LogConfigure, logger: logging.Logger = None) -> logging.Logger:
    if not logger:
        logger = logging.getLogger("default")

    if config.cleanup:
        for h in logger.handlers[:]:
            logger.removeHandler(h)
            h.close()
    logger.setLevel(config.level)

    config.directory.mkdir(exist_ok=True)

    handlers = config.get_handlers(config.formats)
    for handler in handlers:
        logger.addHandler(handler)

    return logger
