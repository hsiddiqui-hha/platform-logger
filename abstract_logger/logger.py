import logging
import sys

import structlog

from abstract_logger.anonymizer import Anonymizer
from abstract_logger.app_config import AppConfig


class Logger:
    def __init__(self, config=None, config_file=None):
        if config_file:
            self.config = AppConfig(config_file).config
        elif config:
            self.config = config
        else:
            self.config = {}

        self.anonymizer = Anonymizer(self.config)
        self.anonymize_fields = set(self.config.get("anonymize_fields", []))
        self.logger = self._configure_logger()

    def _configure_logger(self):
        log_level = self.config.get("log_level", 'DEBUG').upper()
        log_format = self.config.get("log_format", "plain")
        log_destination = self.config.get("log_destination", "console")

        # Convert log level string to logging level
        level = getattr(logging, log_level, logging.DEBUG)

        logging.basicConfig(level=level,
                            format='%(message)s',
                            stream=sys.stdout if log_destination == 'console' else None)

        processors = [
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
        ]

        if log_format == 'json':
            processors.append(structlog.processors.JSONRenderer())
        else:
            processors.append(structlog.dev.ConsoleRenderer(colors=True))

        structlog.configure(
            processors=processors,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

        return structlog.get_logger()

    def anonymize_message(self, message):
        return self.anonymizer.anonymize(message)

    def anonymize(self, **kwargs):
        for key in kwargs:
            if key in self.anonymize_fields:
                kwargs[key] = self.anonymizer.anonymize(kwargs[key])
        return kwargs

    def _log(self, level, message, **kwargs):
        message = self.anonymize_message(message)
        kwargs = self.anonymize(**kwargs)
        getattr(self.logger, level)(message, **kwargs)

    def info(self, message, **kwargs):
        self._log('info', message, **kwargs)

    def debug(self, message, **kwargs):
        self._log('debug', message, **kwargs)

    def warning(self, message, **kwargs):
        self._log('warning', message, **kwargs)

    def error(self, message, **kwargs):
        self._log('error', message, **kwargs)

    def critical(self, message, **kwargs):
        self._log('critical', message, **kwargs)
