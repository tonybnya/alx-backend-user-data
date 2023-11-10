#!/usr/bin/env python3
""" Class BasicAuth that inherits from Auth
"""
from api.v1.auth.auth import Auth
from flask import request
from typing import List, TypeVar


class BasicAuth(Auth):
    """This class is the template for all authentication system"""

    def extract_base64_authorization_header(
            self,
            authorization_header: str
        ) -> str:
        """Get the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if (
            authorization_header is None
            or not isinstance(authorization_header, str)
            or not authorization_header.startswith("Basic ")
        ):
            return None

        return authorization_header[6:]
