#!/usr/bin/env python3
'''Database module'''
import os
import mysql.connector
from mysql.connector import connection


def get_db() -> connection.MySQLConnection:
    """
    Connects to a secure MySQL database and returns the connection object.
    Retrieves credentials from environment variables.
    """
    return mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )
