#!/usr/bin/env python3
"""Module for authentication
"""
import bcrypt


def _hash_password(password: str) -> str:
    """Hash password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
