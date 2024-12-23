#!/usr/bin/env python3
"""
Auth module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class template for managing API authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """It checks if a specific URL path is part
           of a list of "safe" paths (excluded from authentication).
        If the path is in this list, no authentication is needed.
        If it’s not, the path requires authentication."""
        if path is None:
            return True
        if not excluded_paths or len(excluded_paths) == 0:
            return True
        if not path.endswith('/'):
            path += '/'
        for excluded_path in excluded_paths:
            if excluded_path == path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Retrieves the Authorization header from the request."""
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the current user from the request."""
        return None
