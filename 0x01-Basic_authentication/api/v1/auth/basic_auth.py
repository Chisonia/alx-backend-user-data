#!/usr/bin/env python3
""" BasicAuth module """
from api.v1.auth.auth import Auth
import base64
from typing import Tuple


class BasicAuth(Auth):
    """Basic authentication class."""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:  # noqa E501
        """
        Extracts the Base64 part of the Authorization
        header for Basic Authentication.

        Args:
            authorization_header (str): The Authorization header.

        Returns:
            str: The Base64 part of the Authorization header,
            or None if invalid.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]  # Extract the part after "Basic "

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:  # noqa E501
        """
        Decodes a Base64 string to its UTF-8 decoded value.

        Args:
            base64_authorization_header (str): The Base64 string.

        Returns:
            str: The decoded UTF-8 string if valid, otherwise None.
        """
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):  # noqa E501
            return None
        try:
            # Decode Base64 and convert bytes to string
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Tuple[str, str]:  # noqa E501
        """
        Extracts the user email and password from the Base64 decoded value.

        Args:
            decoded_base64_authorization_header (str):
            The Base64 decoded string.

        Returns:
            tuple: A tuple (user_email, user_password)
            or (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):  # noqa E501
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        # Split by the first occurrence of ':'
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password
