#!/usr/bin/env python3
""" BasicAuth module """
from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar, Optional
from models.user import User


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

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):  # noqa E501
        """
        Retrieve a User instance by email and password.

        Args:
            user_email (str): The user's email address.
            user_pwd (str): The user's password.

        Returns:
            User: The matching User instance, or None if no match is found.
        """
        # Validate email and password
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None

        try:
            # Search for the user by email
            users = User.search({'email': user_email})
            if not users or len(users) == 0:  # If no users are found
                return None

            # Assuming email is unique, fetch the first user
            user = users[0]

            # Validate the password
            if not user.is_valid_password(user_pwd):
                return None

            return user

        except Exception as e:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request using Basic Authentication.

        Args:
            request: The Flask request object.

        Returns:
            User: The authenticated User instance,
            or None if authentication fails.
        """
        if request is None:
            return None

        # Step 1: Extract the Authorization header
        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None

        # Step 2: Extract the Base64 part of the Authorization header
        base64_authorization_header = self.extract_base64_authorization_header(authorization_header)  # noqa E501
        if base64_authorization_header is None:
            return None

        # Step 3: Decode the Base64 part to a UTF-8 string
        decoded_base64 = self.decode_base64_authorization_header(base64_authorization_header)  # noqa E501
        if decoded_base64 is None:
            return None

        # Step 4: Extract the user credentials (email and password)
        user_email, user_pwd = self.extract_user_credentials(decoded_base64)
        if user_email is None or user_pwd is None:
            return None

        # Step 5: Retrieve the User object using the credentials
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
