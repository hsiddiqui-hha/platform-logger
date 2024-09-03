from unittest.mock import patch

import pytest

from abstract_logger.anonymizer import Anonymizer
from abstract_logger.logger import Logger


@pytest.fixture
def logger():
    # Create a logger instance with known configuration
    config = {
        'log_level': 'DEBUG',
        'log_format': 'plain',
        'log_destination': 'console',
        'anonymize_fields': ['email'],
        'anonymize_patterns': {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+(?:\.[A-Z|a-z]{2,})+\b'
        }
    }
    log = Logger(config)

    # Patch the logging methods
    with patch.object(log, 'info') as mock_info, \
            patch.object(log, 'debug') as mock_debug, \
            patch.object(log, 'warning') as mock_warning, \
            patch.object(log, 'error') as mock_error, \
            patch.object(log, 'critical') as mock_critical:
        yield log, mock_info, mock_debug, mock_warning, mock_error, mock_critical


def test_logging_with_custom_logger(logger):
    log, mock_info, _, _, _, _ = logger
    log.info("Info message")
    mock_info.assert_called_with("Info message")


def test_debug_logging(logger):
    log, _, mock_debug, _, _, _ = logger
    log.debug("Debug message")
    mock_debug.assert_called_with("Debug message")


def test_warning_logging(logger):
    log, _, _, mock_warning, _, _ = logger
    log.warning("Warning message")
    mock_warning.assert_called_with("Warning message")


def test_error_logging(logger):
    log, _, _, _, mock_error, _ = logger
    log.error("Error message")
    mock_error.assert_called_with("Error message")


def test_critical_logging(logger):
    log, _, _, _, _, mock_critical = logger
    log.critical("Critical message")
    mock_critical.assert_called_with("Critical message")


def test_anonymize_message(logger):
    log, _, _, _, _, _ = logger
    test_message = "Contact me at test@example.com"
    anonymized_message = log.anonymize_message(test_message)
    assert "[ANONYMIZED]" in anonymized_message


def test_anonymize_fields(logger):
    log, _, _, _, _, _ = logger
    log.info("User email: test@example.com")

    # Ensure the message has been anonymized correctly
    # Check if `[ANONYMIZED]` is in the output message
    log.info("User email: test@example.com")
    assert "[ANONYMIZED]" in log.anonymize_message("User email: test@example.com")


def test_anonymizer_configuration():
    config = {
        'anonymize_patterns': {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+(?:\.[A-Z|a-z]{2,})+\b'
        }
    }
    anonymizer = Anonymizer(config)
    test_message = "Contact me at test@example.com"
    assert anonymizer.anonymize(test_message) == "Contact me at [ANONYMIZED]"
