"""Module for a json formatted logger"""

import logging

import datetime as dt

from typing import Dict, Any

from pythonjsonlogger import jsonlogger


def get_logger(name: str) -> logging.Logger:
    """Returns logger instance"""
    logging.captureWarnings(True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if logger.hasHandlers():
        return logger
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s] %(threadName)s %(name)s [%(levelname)7s] %(message)s"
        )
    )
    logger.addHandler(handler)
    return logger


def get_logger_json(name: str = "logger") -> logging.Logger:
    """Function to get a new logger instance"""
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    if not log.handlers:
        log.addHandler(get_app_logging_handler())
    return log


def get_app_logging_handler() -> logging.StreamHandler:
    """Getting a new logging handler"""
    log_handler = logging.StreamHandler()
    formatter = JsonLogFormatter()
    log_handler.setFormatter(formatter)
    return log_handler


class JsonLogFormatter(jsonlogger.JsonFormatter):
    """Json Log formatter following the Zooplus standards."""

    def add_fields(
        self,
        log_record: Dict[str, Any],
        record: logging.LogRecord,
        message_dict: Dict[str, str],
    ) -> None:
        """Adding json fields for logging"""
        super().add_fields(log_record, record, message_dict)

        log_record["log_type"] = "application_log"
        log_record["@timestamp"] = dt.datetime.now(dt.timezone.utc).isoformat()
        log_record["description"] = log_record.pop("message", None)
        log_record["severity"] = record.levelname.upper()
        log_record["class"] = ":".join(
            [record.module, record.funcName, str(record.lineno)]
        )

        exc_info = log_record.pop("exc_info", None)
        if exc_info:
            log_record["stacktrace"] = exc_info
        if record.process:
            log_record["pid"] = record.process
        if record.threadName:
            log_record["thread"] = record.threadName
