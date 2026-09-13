"""
Logging configuration for the FastAPI application.

Provides JSON and colored log formatters, and a function to configure logging.
"""

import json
import logging
from datetime import datetime
from logging.config import dictConfig


class JsonFormatter(logging.Formatter):
    """
    Formatter for logging in JSON format.
    """

    def format(self, record):
        """
        Format a log record as JSON.

        Args:
            record (logging.LogRecord): The log record.

        Returns:
            str: The formatted JSON log string.
        """
        log_record = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "line": record.lineno,
            "message": record.getMessage(),
        }

        # Add exception info if available
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)


class ColoredFormatter(logging.Formatter):
    """
    Colored log formatter using ANSI escape codes.
    """

    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }

    RESET = "\033[0m"  # Reset color
    BOLD = "\033[1m"  # Bold text

    def format(self, record):
        """
        Format a log record with color for the log level.

        Args:
            record (logging.LogRecord): The log record.

        Returns:
            str: The formatted colored log string.
        """
        # Get the original formatted message
        log_message = super().format(record)

        # Get color for the log level
        color = self.COLORS.get(record.levelname, "")

        # Format: [LEVEL] in color, rest in normal color
        if color:
            # Split the message to color only the level part
            parts = log_message.split("]", 1)
            if len(parts) == 2:
                level_part = parts[0] + "]"
                rest_part = parts[1]
                return f"{color}{self.BOLD}{level_part}{self.RESET}{rest_part}"

        return log_message


log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {"()": JsonFormatter},
        "colored": {
            "()": ColoredFormatter,
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "default": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "colored",
            "stream": "ext://sys.stdout",
        },
        # "file": {
        #     "class": "logging.FileHandler",
        #     "level": "INFO",
        #     "formatter": "json",
        #     "filename": "fastapi.log",
        #     "mode": "a",
        # },
    },
    "loggers": {
        "app": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
    },
    "root": {"handlers": ["console"], "level": "DEBUG"},
}


def configure_logging():
    """
    Configure logging for the application using the defined log_config.

    Returns:
        None
    """
    dictConfig(log_config)
