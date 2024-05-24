#!/usr/bin/env python3
"""
class to manage the API authentication
"""
from flask import request
from typing import List, TypeVar
import os


class Auth():
    """class to manage the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """public method require_auth"""
        if path is None or not excluded_paths:
            return True
        if path in excluded_paths:
            return False

        path = path + '/' if not path.endswith('/') else path

        for excl_path in excluded_paths:
            if excl_path.endswith('*'):
                norm_excl_path = excl_path[:-1]
                if path.startswith(norm_excl_path):
                    return False
            else:
                excl_path = excl_path + '/' if not\
                    excl_path.endswith('/') else excl_path
                if path == excl_path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """public method authorization_header"""
        if request is None:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """public method current_user"""
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie value from a request based on the
        SESSION_NAME variable.
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
