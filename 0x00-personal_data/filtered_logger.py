#!/usr/bin/env python3
'''This module returns obfuscated logs'''
import re


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
