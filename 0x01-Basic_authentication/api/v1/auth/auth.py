#!/usr/bin/env python3
""" Class to manage the API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ This class is the template for all authentication system
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if routes require authentication"""
        if path is None or excluded_paths is None or not len(excluded_paths) == 0:
            return True

    def authorization_header(self, request=None) -> str:
        """Validate all requests to secure the API"""
        pass

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user"""
        pass
