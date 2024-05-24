#!/usr/bin/env python3
"""SessionAuth class that inherits from Auth."""
from api.v1.auth.auth import Auth
import uuid
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.user import User
from os import getenv


class SessionAuth(Auth):
    """SessionAuth class that inherits from Auth."""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.__class__.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        user_id = self.__class__.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """
        Retrieves the User instance based on a cookie value.
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return None

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        """Deletes the user session / logout."""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None or session_id not in self.user_id_by_session_id:
            return False

        del self.user_id_by_session_id[session_id]
        return True
