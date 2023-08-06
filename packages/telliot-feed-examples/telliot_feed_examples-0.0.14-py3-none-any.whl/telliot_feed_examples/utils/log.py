import logging
import pathlib
from pathlib import Path

from telliot_core.apps.telliot_config import TelliotConfig
from telliot_core.utils.home import default_homedir


cfg = TelliotConfig()


class DuplicateFilter(logging.Filter):
    """A logger filter for preventing flood of duplicate log messages"""

    def filter(self, record: logging.LogRecord) -> bool:
        """does not print a second consecutive log of the same message"""
        # add other fields if you need more granular comparison, depends on your app
        current_log = (record.module, record.levelno, record.msg)
        if current_log != getattr(self, "last_log", None):
            self.last_log = current_log
            return True
        return False


def default_logsdir() -> pathlib.Path:
    """Return default logs directory, creating it if necessary

    Returns:
        pathlib.Path : Path to logs directory
    """
    logsdir = Path(default_homedir() / ("logs"))
    logsdir = logsdir.resolve().absolute()
    if not logsdir.is_dir():
        logsdir.mkdir()

    return logsdir


def get_logger(name: str) -> logging.Logger:
    """Telliot feed examples logger

    Returns a logger that logs to stdout and file. The name arg
    should be the current file name. For example:
    _ = get_logger(name=__name__)
    """
    logger = logging.getLogger(name)
    logger.addFilter(DuplicateFilter())

    return logger
