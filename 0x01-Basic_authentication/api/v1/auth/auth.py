#!/usr/bin/env python3
""" Class to manage the API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ This class is the template for all authentication system
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        pass

    def authorization_header(self, request=None) -> str:
        pass

    def current_user(self, request=None) -> TypeVar('User'):
        pass