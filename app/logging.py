"""Logging Module."""
import logging
import sys

from flask import current_app as app


class Logger():
    """Logging Class."""
    def __init__(self, name):
        """Logging construction."""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(app.config.get('LOG_LEVEL'))
        self.logger.addHandler(logging.StreamHandler(sys.stdout))

    def debug(self, message, data=None):
        """Debug"""
        self._log(level=logging.DEBUG, message=message, data=data)

    def info(self, message, data=None):
        """info"""
        self._log(level=logging.INFO, message=message, data=data)

    def warning(self, message, data=None):
        """warning"""
        self._log(level=logging.WARNING, message=message, data=data)

    def error(self, message, data=None):
        """error"""
        self._log(level=logging.ERROR, message=message, data=data)

    def critical(self, message, data=None):
        """critical"""
        self._log(level=logging.CRITICAL, message=message, data=data)

    def _log(self, level, message, data):
        """Internal method. not intended for external use."""
        if data is None:
            self.logger.log(level, message)
        else:
            self.logger.log(level, message, extra={'props': data})
