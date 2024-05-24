#!/usr/bin/env python3
"""SessionExpAuth class that inherits from SessionAuth."""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class that inherits from SessionAuth."""

    def __init__(self):
        """Overload the init method."""
        session_duration = getenv('SESSION_DURATION', 0)
        try:
            self.session_duration = int(session_duration)
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Creates a Session ID with expiration."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get user_id from session_id considering expiration."""
        if session_id is None:
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None

        if self.session_duration <= 0:
            return session_dictionary.get('user_id')
