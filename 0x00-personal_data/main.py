#!/usr/bin/env python3
"""
Main file
"""

import logging
from secure_db import get_db

def main():
    """Main function to test database connection and query."""
    try:
        # Get database connection
        db_connection = get_db()

        # Create a cursor to execute queries
        cursor = db_connection.cursor()

        # Execute a query
        cursor.execute("SELECT email FROM users;")
        rows = cursor.fetchall()

        # Print the results
        for row in rows:
            print(row[0])

        # Close the cursor and connection
        cursor.close()
        db_connection.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

get_logger = __import__('filtered_logger').get_logger
PII_FIELDS = __import__('filtered_logger').PII_FIELDS

print(get_logger.__annotations__.get('return'))
print("PII_FIELDS: {}".format(len(PII_FIELDS)))

get_db = __import__('filtered_logger').get_db

db = get_db()
cursor = db.cursor()
cursor.execute("SELECT COUNT(*) FROM users;")
for row in cursor:
    print(row[0])
cursor.close()
db.close()

hash_password = __import__('encrypt_password').hash_password

password = "MyAmazingPassw0rd"
print(hash_password(password))
print(hash_password(password))

hash_password = __import__('encrypt_password').hash_password
is_valid = __import__('encrypt_password').is_valid

password = "MyAmazingPassw0rd"
encrypted_password = hash_password(password)

print(encrypted_password)
print(is_valid(encrypted_password, password))
print(is_valid(encrypted_password, "WrongPassword"))