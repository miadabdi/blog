"""
User role definitions for access control.
"""

import enum


class UserRole(str, enum.Enum):
    """
    Enum for user roles.
    """

    ADMIN = "ADMIN"
    USER = "USER"
