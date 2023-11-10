#!/usr/bin/env python3
""" Class BasicAuth that inherits from Auth
"""
from api.v1.auth.auth import Auth
from flask import request
from typing import List, TypeVar


class BasicAuth(Auth):
    """ This class is the template for all authentication system
    """
    pass
