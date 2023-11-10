#!/usr/bin/env python3
""" Class BasicAuth that inherits from Auth
"""
from api.v1.auth.auth import Auth
from models.user import User
from base64 import b64decode
from typing import TypeVar


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

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """Get the user email and password from the Base64 decoded value"""
        if (
            decoded_base64_authorization_header is None
            or not isinstance(decoded_base64_authorization_header, str)
            or ':' not in decoded_base64_authorization_header
        ):
            return (None, None)

        credentials = decoded_base64_authorization_header.split(':')

        return credentials[0], credentials[-1]

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Get the User instance based on his email and password"""
        if (
            user_email is None
            or not isinstance(user_email, str)
            or user_pwd is None
            or not isinstance(user_pwd, str)
        ):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None
