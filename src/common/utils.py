"""
Utility classes and helpers for the application.
"""

import threading


class Singleton:
    """
    Thread-safe Singleton base class.

    Ensures only one instance of the subclass exists.

    Usage:
        class MySingleton(Singleton):
            pass

        instance = MySingleton()

    Attributes:
        _instance: The singleton instance.
        _lock: Lock for thread safety.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """
        Create or return the singleton instance.

        Returns:
            Singleton: The singleton instance.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance
