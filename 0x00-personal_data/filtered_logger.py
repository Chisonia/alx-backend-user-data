#!/usr/bin/env python3
'''This module returns obfuscated logs'''
import re
import logging
from typing import List
# Define the constant PII_FIELDS
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields, redaction, message, seperator):
    '''
    Obfuscate fields in a og message
    Arg:
        fields: List of fields to obfuscate
        redaction:The string to replace the field value
        message: The lig line to process
        seperator: The field seperator in the log line.
        Returns str (The log line with obfuscsted fields)
        '''
    pattern = f"({'|'.join(fields)})=.*?{seperator}"
    return re.sub(pattern, lambda match: f"{match.group(1)}={redaction}{seperator}", message)  # noqa E5O1


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializes the formatter with fields to redact.

        Args:
            fields (List[str]): Fields to redact.
        """
        super().__init__(self.FORMAT)
        self.fields = fields  # Store fields as an instance attribute

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a log record, redacting sensitive fields.

        Args:
            record (LogRecord): The log record to process.

        Returns:
            str: The formatted and redacted log message.
        """
        record.msg = filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)  # noqa E501
        return super().format(record)


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger named 'user_data'.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)  # Log only up to INFO level
    logger.propagate = False  # Do not propagate messages to other loggers

    # Set up the StreamHandler with RedactingFormatter
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
