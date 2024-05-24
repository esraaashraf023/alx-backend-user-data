#!/usr/bin/env python3
"""Authentication via session database."""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from os import getenv
import uuid


class SessionDBAuth(SessionExpAuth):
    """Authentication via session database."""

    def create_session(self, user_id=None):
        """Create and store new instance of UserSession, return Session ID."""
        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return the User ID by querying UserSession based on session_id."""
        if session_id:
            user_sessions = UserSession.search({'session_id': session_id})
            if user_sessions:
                return user_sessions[0].user_id
        return None

    def destroy_session(self, request=None):
        """Destroy the UserSession based on the Session ID
        from request cookie."""
        if request:
            session_id = self.session_cookie(request)
            if session_id:
                user_sessions = UserSession.search({'session_id': session_id})
                if user_sessions:
                    user_sessions[0].remove()
                    return True
        return False
