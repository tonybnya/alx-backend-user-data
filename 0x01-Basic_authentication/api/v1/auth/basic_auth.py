#!/usr/bin/env python3
""" Class BasicAuth that inherits from Auth
"""
from api.v1.auth.auth import Auth
from base64 import b64decode


class BasicAuth(Auth):
    """This class is the template for all authentication system"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
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

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """Get the decoded value of a Base64 string base64_authorization_header
        """
        if (
            base64_authorization_header is None
            or not isinstance(base64_authorization_header, str)
        ):
            return None

        try:
            data = b64decode(base64_authorization_header)
        except Exception:
            return None

        return data.decode('utf-8')
