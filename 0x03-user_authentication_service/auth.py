#!/usr/bin/env python3
"""Module for authentication
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _generate_uuid() -> str:
    """Generate UUIDs"""
    return str(uuid.uuid4())


def _hash_password(password: str) -> str:
    """Hash password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            bcrypted = _hash_password(password)
            return self._db.add_user(email=email, hashed_password=bcrypted)
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Credentials validation"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        else:
            return bcrypt.checkpw(
                password=password.encode(),
                hashed_password=user.hashed_password
            )

    def create_session(self, email: str) -> str:
        """Get session ID"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            user.session_id = _generate_uuid()
            return user.session_id
