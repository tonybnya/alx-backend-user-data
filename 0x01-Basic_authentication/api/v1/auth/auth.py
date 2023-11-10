#!/usr/bin/env python3
""" Class to manage the API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """This class is the template for all authentication system"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if routes require authentication"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        for string_path in excluded_paths:
            if string_path.endswith("*") and path.startswith(string_path[:-1]):
                return False
            elif string_path in (path, f"{path}/"):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Validate all requests to secure the API"""
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar("User"):
        """Get the current user"""
        return None
