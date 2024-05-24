#!/usr/bin/env python3
"""Represents a User Session for storing session IDs and user IDs."""
from models.base import Base


class UserSession(Base):
    """Represents a User Session for storing session IDs and user IDs."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a UserSession instance."""
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
        super().__init__(*args, **kwargs)
