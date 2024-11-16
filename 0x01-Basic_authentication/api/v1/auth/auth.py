#!/usr/bin/env python3
"""
Auth module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class template for managing API authentication."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of
            paths that don't require authentication.

        Returns:
            bool: True if the path is not in excluded_paths; otherwise, False.
        """
        if path is None:
            return True
        if not excluded_paths or len(excluded_paths) == 0:
            return True

        # Normalize the path by adding a trailing slash if it's missing
        if not path.endswith('/'):
            path += '/'

        # Check if the normalized path is in excluded_paths
        for excluded_path in excluded_paths:
            if excluded_path == path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the request.

        Args:
            request: The Flask request object.

        Returns:
            str: None for now (to be implemented later).
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request.

        Args:
            request: The Flask request object.

        Returns:
            User: None for now (to be implemented later).
        """
        return None
