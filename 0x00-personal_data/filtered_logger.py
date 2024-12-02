#!/usr/bin/env python3
"""
Module to filter and log sensitive user data.
"""

import logging
import os
import re
import mysql.connector
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = ("[HOLBERTON] user_data INFO %(asctime)s: "
              "%(message)s")
    SEPARATOR = "; "

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, filtering sensitive data.
        """
        record.msg = self.filter_datum(self.fields, self.REDACTION,
                                       record.msg, self.SEPARATOR)
        return super().format(record)

    @staticmethod
    def filter_datum(fields: List[str], redaction: str, message: str,
                     separator: str) -> str:
        """
        Filters sensitive data in a log message.
        """
        for field in fields:
            pattern = f"{field}=.*?(?={separator}|$)"
            message = re.sub(pattern, f"{field}={redaction}", message)
        return message


def get_logger() -> logging.Logger:
    """
    Creates a logger instance.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Connects to a secure MySQL database and returns the connection object.
    """
    return mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )


def main() -> None:
    """
    Main function to fetch and log data from the users table.
    """
    logger = get_logger()

    try:
        db_connection = get_db()
        cursor = db_connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users;")
        rows = cursor.fetchall()

        for row in rows:
            msg = "; ".join([f"{key}={value}" for key, value in row.items()])
            logger.info(msg)

        cursor.close()
        db_connection.close()

    except Exception as e:
        logger.error(f"Error: {e}")


if __name__ == "__main__":
    main()
