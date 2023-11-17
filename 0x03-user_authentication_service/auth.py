#!/usr/bin/env python3
"""Module for authentication
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


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

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """Find user by session ID"""
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        if user.session_id is None:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroy session"""
        if user_id is None:
            return None

        self._db.update_user(user_id, session_id=None)
