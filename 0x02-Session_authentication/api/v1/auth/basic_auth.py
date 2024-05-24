#!/usr/bin/env python3
"""class BasicAuth that inherits from Auth
For the moment this class will be empty."""
from .auth import Auth
import base64
from models.user import User
from typing import TypeVar

UserType = TypeVar('User')


class BasicAuth(Auth):
    """class BasicAuth that inherits from Auth"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if authorization_header is None or not\
                isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        base64_part = authorization_header[6:]
        return base64_part

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
        Decodes a Base64 string.
        """
        if base64_authorization_header is None or not\
                isinstance(base64_authorization_header, str):
            return None

        try:
            base64_bytes = base64_authorization_header.encode('utf-8')
            message_bytes = base64.b64decode(base64_bytes)
            message = message_bytes.decode('utf-8')
            return message
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        Extracts the user email and password from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        credentials_split = decoded_base64_authorization_header.split(':', 1)
        if len(credentials_split) != 2:
            return (None, None)

        user_email, user_pwd = credentials_split
        return user_email, user_pwd

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> UserType:
        """
        Retrieves the User instance based on email and password.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})

            if not users:
                return None

            user = users[0]

            if user.is_valid_password(user_pwd):
                return user
            else:
                return None
        except Exception:
            return None

    def current_user(self, request=None) -> UserType:
        """
        Retrieves the User instance for a request using Basic Authentication.
        """
        auth_header = self.authorization_header(request)
        base64_auth_header =\
            self.extract_base64_authorization_header(auth_header)
        decoded_auth_header =\
            self.decode_base64_authorization_header(base64_auth_header)
        user_email, user_pwd =\
            self.extract_user_credentials(decoded_auth_header)
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
